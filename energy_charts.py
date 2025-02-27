from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from prices_transformation import clean_data,compute_time_series
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService

def instantiate_driver():
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    driver.implicitly_wait(180)
    return driver

def download_yearly_price_file(driver,country,year):
    """
    Navigates to the energy price chart website, waits for the page to load,
    selects the CSV download option, and downloads the yearly price file.
    """

    wait = WebDriverWait(driver, 10)  # Wait up to 30 seconds

    # Open the webpage containing energy price data for a specific country for a specifc year
    driver.get(f"https://energy-charts.info/charts/price_spot_market/chart.htm?l=en&c={country}&interval=year&year={year}")

    # Wait until the page title is visible to ensure the page has loaded
    element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "h4#pagetitle")))
    time.sleep(2)

    # Click the export button to open the download format selection
    driver.find_element(By.CSS_SELECTOR,'span[is-for="export"]').click()
    time.sleep(1)

    # Select CSV format from the download options
    [v for v in driver.find_element(By.CSS_SELECTOR,"select#downloadFormat").find_elements(By.CSS_SELECTOR,"option") if "CSV" in v.text][0].click()
    time.sleep(1)

    # Click the download button to initiate the file download
    driver.find_element(By.CSS_SELECTOR,"button.pseudo-round-btn.btn-tn.download").click()
    time.sleep(2)


if __name__ == '__main__':
    country = "BE"
    # DE - for Germany
    # BE -  for Belgium
    # FR - for France

    year = 2024

    # Instantiate the WebDriver
    driver = instantiate_driver()

    # Download the monthly price CSV file
    download_yearly_price_file(driver,country,year)

    # Clean and transform the downloaded data
    df_cleaned = clean_data()

    # Perform time series computation on the cleaned data
    compute_time_series(df_cleaned,country,year)
    driver.quit()