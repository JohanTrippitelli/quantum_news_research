# Web Scraper Project

## Overview

This project is a web scraping pipeline that extracts articles from websites using configurable XPath expressions. The configuration for each target website is maintained in a YAML file (`x_paths.yaml`), allowing you to adjust scraping parameters without modifying the code.

The project consists of three main files:
- **main.py:** The entry point that reads the YAML configuration and invokes the scraping process based on a command-line parameter.
- **scrape.py:** Contains the scraping logic, utilizing Selenium (and optionally requests) to extract article details.
- **x_paths.yaml:** A YAML file holding the scraping parameters, including the starting URL and XPaths for the article elements (Title, Author, Date, Synopsis).

## Features

- **Configurable Scraping:** Easily define the starting URL and XPath selectors for each website in the YAML file.
- **Dynamic Extraction:** Supports scraping both from listing pages and individual article pages, based on the configuration.
- **Command-Line Operation:** Run the scraper by specifying the site configuration name as a command-line argument.
- **Basic Error Handling:** Logs errors encountered during the scraping process and continues with other articles.

## Requirements

- **Python 3.6+**
- **Selenium:** For web automation.
- **PyYAML:** To parse the YAML configuration.
- **Requests:** (Optional) For handling HTTP requests if needed.

> **Note:** Ensure you have the appropriate WebDriver (e.g., [ChromeDriver](https://chromedriver.chromium.org/downloads)) installed and available in your system PATH.


## Set Up instructions:
1. Create a virtual environment in the desired folder:
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