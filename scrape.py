import time
import pandas as pd
from IPython.display import display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers import get_element_value, get_modified_xpath, handle_popup
from urllib.parse import urljoin

def scrape_site(config, human_mode=False):
    print("🚀 Starting web scraping...")

    # Extract parameters from YAML file
    start_url = config['start_url']
    print(f"🌐 Navigating to start_url: {start_url}")

    # Setup Selenium WebDriver
    driver = webdriver.Chrome()
    driver.get(start_url)

    # Handle pop-ups initially
    handle_popup(driver, config.get('click_popup', False))

    # Human mode pause
    if human_mode:
        input("👤 Human mode: Press Enter to start scraping...")

    time.sleep(3)

    # Step 1: Collect all article URLs
    print(f"🔍 Looking for articles using XPath: {config['items_out']}")
    WebDriverWait(driver, 2).until(
        EC.presence_of_all_elements_located((By.XPATH, config['items_out']))
    )
    article_elements = driver.find_elements(By.XPATH, config['items_out'])
    print(f"✅ Found {len(article_elements)} articles.")

    article_urls = []

    for i, article in enumerate(article_elements):
        try:
            # Get modified XPath for current article item
            modified_url_xpath = get_modified_xpath(config['items_out'], i, config['url'])

            # Extract the correct URL
            article_url = get_element_value(driver, modified_url_xpath)
            
            print(f"🔗 Raw extracted URL: {article_url}")

            # Ensure URL is absolute
            if article_url and not article_url.startswith("http"):
                article_url = urljoin(start_url, article_url)

            print(f"✅ Processed Absolute URL: {article_url}")
            article_urls.append(article_url)

        except Exception as e:
            print(f"⚠️ Error extracting URL from article {i+1}: {e}")

    print(f"\n✅ Total URLs collected: {len(article_urls)}")
    
    if not article_urls:
        print("❌ No article URLs found. Exiting script.")
        driver.quit()
        return

    # Step 2: Visit each article URL and extract data
    articles = []

    for i, article_url in enumerate(article_urls):
        try:
            print(f"\n🌍 Navigating to article {i+1}: {article_url}")
            driver.get(article_url)

            # ✅ Check for popups again on article pages
            handle_popup(driver, config.get('click_popup', False))

            if human_mode:
                input("👤 Human mode: Press Enter to scrape the article page...")

            # ✅ **Key Fix: Adjust XPath usage based on `in_url`**
            if config.get('in_url', False):
                # If extracting from the article page itself, use XPaths as-is
                title_xpath = config['Title']
                author_xpath = config['Author']
                date_xpath = config['Date']
                synopsis_xpath = config['Synopsis']
            else:
                # If extracting from listing page, modify XPaths relative to items_out
                title_xpath = get_modified_xpath(config['items_out'], i, config['Title'])
                author_xpath = get_modified_xpath(config['items_out'], i, config['Author'])
                date_xpath = get_modified_xpath(config['items_out'], i, config['Date'])
                synopsis_xpath = get_modified_xpath(config['items_out'], i, config['Synopsis'])

            # Extract content
            title = get_element_value(driver, title_xpath)
            author = get_element_value(driver, author_xpath)
            date = get_element_value(driver, date_xpath)
            synopsis = get_element_value(driver, synopsis_xpath)

            print(f"✅ Scraped article {i+1}: {title} by {author} on {date}")

            articles.append({
                "Title": title,
                "Author": author,
                "Date": date,
                "Synopsis": synopsis,
                "URL": article_url
            })

        except Exception as e:
            print(f"⚠️ Error processing article {i+1} at {article_url}: {e}")

    driver.quit()

    # Step 3: Save data and display
    df = pd.DataFrame(articles)
    df.to_excel("scraped_articles.xlsx", index=False)
    print("\n✅ Data saved to scraped_articles.xlsx")

    display(df)
