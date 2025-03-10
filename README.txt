# 🕵️‍♂️ Web Scraper Project

## 📌 Overview

This project is a **web scraping pipeline** that extracts articles from websites using **configurable XPath expressions**.  
The scraping configuration is stored in a **YAML file (`x_paths.yaml`)**, allowing you to easily update scraping parameters without modifying the code.

### 📂 Project Structure
- **`main.py`** – The entry point that reads the YAML configuration and invokes the scraper via the command line.
- **`scrape.py`** – Contains the scraping logic, utilizing **Selenium** (and optionally **Requests**) to extract article details.
- **`x_paths.yaml`** – Stores the scraping parameters, including the starting URL and **XPaths** for article elements *(Title, Author, Date, Synopsis, etc.)*.

---

## 🚀 Features

- ✅ **Configurable Scraping** – Define the **starting URL** and **XPath selectors** in a YAML file.  
- ✅ **Dynamic Extraction** – Supports scraping from both **listing pages** and **individual article pages**.  
- ✅ **Command-Line Operation** – Run the scraper using a simple **CLI command**.  
- ✅ **Basic Error Handling** – Logs errors while scraping and continues with the next available article.  

---

## 🛠️ Requirements

📌 Ensure you have the following installed:  
- **Python 3.6+**  
- **Selenium** (for web automation)  
- **PyYAML** (to parse the YAML configuration)  
- **Requests** *(optional, for handling HTTP requests if needed)*  

> **Note:** Make sure you have the appropriate WebDriver installed (e.g., [ChromeDriver](https://chromedriver.chromium.org/downloads)) and available in your system **PATH**.

---

## 📥 Setup Instructions

### 🔹 Create a Virtual Environment
```sh
python -m venv venv


2. Activate the environment:
    On macOS/Linux:
        source venv/bin/activate
    On Windows:
        venv\Scripts\activate

2. Give executable permission to the makeFile:
    macOS/Linux:
        chmod +x setup.sh
    Windows:
        Skip Step

3. Run the setup.sh file:
    macOS/Linux:
        ./setup.sh
    Windows:
        setup.bat

4. Run the following command line:
    python main.py x_paths.yaml example_site -hm
