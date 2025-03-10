from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_element_value(parent, xpath_expr):
    """
    Retrieves the value of an element based on the given XPath.
    - If the XPath includes '/@attribute', extracts that attribute.
    - If it's a normal XPath, returns the element's text.
    - If it's an object, returns the full element (for debugging).
    
    Args:
        parent: Selenium WebElement or driver object.
        xpath_expr (str): XPath expression.

    Returns:
        str: The extracted text or attribute value.
    """
    try:
        if '/@' in xpath_expr:
            # Extract attribute
            base_xpath, attr = xpath_expr.rsplit('/@', 1)
            element = parent.find_element(By.XPATH, base_xpath)
            return element.get_attribute(attr)

        else:
            # Extract text content
            element = parent.find_element(By.XPATH, xpath_expr)
            return element.text.strip() if element.text.strip() else None

    except Exception as e:
        print(f"⚠️ Error extracting value using XPath: {xpath_expr} - {e}")
        return None  # Return None if element not found

def get_modified_xpath(base_xpath, index, target_xpath):
    """
    Takes the base `items_out` XPath and replaces '.' in `target_xpath` 
    with the specific indexed XPath for the current article.
    """
    article_xpath = f"({base_xpath})[{index + 1}]"  # XPath is 1-based index
    return target_xpath.replace('.', article_xpath)


def handle_popup(driver, popup_xpath):
    """
    Handles popups by searching for the popup button inside iframes first,
    and then on the main page. If the popup is found, it is clicked.
    
    Args:
        driver (webdriver): Selenium WebDriver instance.
        popup_xpath (str): XPath of the popup button.

    Returns:
        bool: True if popup was successfully clicked, False otherwise.
    """
    if not popup_xpath or not isinstance(popup_xpath, str):
        return False  # No popup to handle

    try:
        print("🔍 Checking for popup...")

        # Wait for the popup to appear (handles JavaScript-delayed popups)
        time.sleep(1)

        # Step 1: Check if the popup is inside an iframe
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        print(f"🔄 Found {len(iframes)} iframes on the page.")

        for i, iframe in enumerate(iframes):
            driver.switch_to.frame(iframe)  # Switch to iframe
            print(f"🔍 Switched to iframe {i+1}")

            try:
                # Wait for the popup inside the iframe
                popup_element = WebDriverWait(driver, 1).until(
                    EC.element_to_be_clickable((By.XPATH, popup_xpath))
                )

                # Scroll into view (ensures visibility)
                driver.execute_script("arguments[0].scrollIntoView(true);", popup_element)
                time.sleep(1)

                try:
                    popup_element.click()  # Normal click
                    print(f"✅ Popup clicked inside iframe {i+1}.")
                except Exception as selenium_click_error:
                    print(f"⚠️ Selenium click failed, trying JavaScript: {selenium_click_error}")
                    driver.execute_script("arguments[0].click();", popup_element)  # JavaScript click
                    print(f"✅ Popup clicked inside iframe {i+1} using JavaScript.")

                driver.switch_to.default_content()  # Return to main page
                return True  # Popup handled successfully

            except:
                print(f"❌ No popup found in iframe {i+1}. Trying next iframe...")
                driver.switch_to.default_content()  # Return to main page before checking next iframe

        # Step 2: Try finding the popup outside of iframes (on the main page)
        print("🔍 Checking for popup outside iframes...")
        popup_element = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.XPATH, popup_xpath))
        )

        # Scroll into view (ensures visibility)
        driver.execute_script("arguments[0].scrollIntoView(true);", popup_element)
        time.sleep(1)

        try:
            popup_element.click()  # Normal click
            print("✅ Popup clicked outside iframe.")
        except Exception as selenium_click_error:
            print(f"⚠️ Selenium click failed outside iframe, trying JavaScript: {selenium_click_error}")
            driver.execute_script("arguments[0].click();", popup_element)  # JavaScript click
            print("✅ Popup clicked outside iframe using JavaScript.")

        return True  # Popup handled successfully

    except Exception as e:
        print(f"⚠️ No popup found or could not be clicked: {e}")
        driver.switch_to.default_content()  # Ensure we return to the main page
        return False  # No popup present

