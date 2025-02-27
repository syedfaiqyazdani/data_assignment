import time
import json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import scrapy
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService

def instantiate_driver():
    """
    Initializes and returns a Firefox WebDriver instance with JavaScript disabled.
    This speeds up page loads and minimizes unwanted pop-ups or dynamic content.
    """
    options = Options()
    options.set_preference('javascript.enabled', False)  # Disable JavaScript for faster loading
    # driver = webdriver.Firefox(options=options)
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()),options=options)
    driver.implicitly_wait(180)  # Implicit wait for elements to appear
    return driver

def scrape_futures_data(driver):
    """
    Scrapes futures market data from MarketWatch.
    Iterates through pages and collects relevant details such as URL, name, price, volume, and open interest.
    """
    page = 1
    data = []
    wait = WebDriverWait(driver, 30)  # Explicit wait for elements to load

    while True:
        # Load the page containing the futures market data
        driver.get(f"https://www.marketwatch.com/tools/markets/futures/{page}")

        try:
            # Wait until the table containing futures data is visible
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "table.table.table-condensed > tbody > tr")))
        except:
            print(f"No more data found on page {page}. Exiting loop.")
            break  # Exit loop if no table rows are found

        time.sleep(1)  # Short delay to ensure complete page load
        response = scrapy.Selector(text=driver.page_source)

        # If no futures data is found, break the loop
        if response.css("table.table.table-condensed > tbody > tr") == []:
            break

        # Iterate through each future entry in the table
        for future in response.css("table.table.table-condensed > tbody > tr"):
            future_url = future.css("a::attr(href)").get()

            driver.get(future_url)
            time.sleep(3)

            respo = scrapy.Selector(text=driver.page_source)

            # Skip if the page leads to a search results page (invalid future data)
            if "".join(respo.css("header.header.header--primary.no-background h2")[0].css(
                    "::text").extract()).strip() == "Search Results":
                continue

            # Extracting required data
            item = {
                'url': future_url,
                'name': respo.css("h1::text").get(),
                'price': extract_price(respo),
                'volume': extract_volume(respo),
                'open_interest': extract_open_interest(respo),
                'open': extract_open_price(respo)
            }
            data.append(item)

        page += 1
        print(f"Scraped page: {page}")

    return data

def extract_price(respo):
    """
    Extracts the price of the future contract, including the currency symbol.
    """
    try:
        return respo.css("h2.intraday__price sup.character::text").get() + " " + [y for y in respo.css("h2.intraday__price ::text").getall() if y.strip()][-1]
    except:
        return "N/A"

def extract_volume(respo):
    """
    Extracts the trading volume of the future contract.
    """
    return "".join([v.css("::text").get().split(":")[-1].strip() for v in respo.css("div.range__header span.primary") if "Volume" in v.css("::text").get()])

def extract_open_interest(respo):
    """
    Extracts the open interest value of the future contract.
    """
    return "".join([t.css("span.primary::text").get() for t in respo.css("li.kv__item") if "Open Interest" in t.css("small.label::text").get()])


def extract_open_price(respo):
    """
    Extracts the opening price of the future contract.
    """
    return "".join([t.css("span.primary::text").get() for t in respo.css("li.kv__item") if "Open" == t.css("small.label::text").get()])


def save_data_to_json(data, filename="output.json"):
    """
    Saves the scraped data to a JSON file.
    """
    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Data saved to {filename}")

if __name__ == '__main__':
    driver = instantiate_driver()
    scraped_data = scrape_futures_data(driver)
    driver.quit()
    save_data_to_json(scraped_data)
