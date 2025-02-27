# Web Scraping and Data Processing Scripts  

## Overview  
This repository contains two Selenium-based web scraping scripts and a data processing module:  

1. **`energy_charts.py`** - Scrapes yearly energy price data from `energy-charts.info`, downloads a CSV file, and processes it.  
2. **`marketwatch_disable.py`** - Scrapes futures market data from `marketwatch.com` with JavaScript disabled for efficiency.  
3. **`prices_transformation.py`** - Cleans and processes energy price data for time series analysis.  

---

## Installation  

### Prerequisites  
Ensure you have the following installed:  

- **Python 3.12**  
- **Firefox** (for Selenium)  
- **Geckodriver** (for Selenium WebDriver)  
- **Required Python Libraries**  

Install dependencies using:  
```bash
pip install -r requirements.txt
```

---

## How to Run  

### 1. **Energy Price Scraper (`energy_charts.py`)**  
This script:  
- Scrapes energy price data for a specified country and year. You can add country and year in function download_yearly_price_file to get prices data for a specific year and country 
- Downloads the CSV file.  
- Cleans and processes the data for time series analysis.  

**Run the script:**  
```bash
python energy_charts.py
```

---

### 2. **MarketWatch Futures Scraper (`marketwatch_disable.py`)**  
This script:  
- Scrapes futures market data from MarketWatch.  
- Extracts price, volume, open interest, and other details.  
- Saves the extracted data to `output.json`.  

**Run the script:**  
```bash
python marketwatch_disable.py
```

---

### 3. **Data Processing (`prices_transformation.py`)**  
This module provides:  
- `clean_data()`: Cleans energy price data from a CSV file.  
- `compute_time_series(df_cleaned)`: Computes monthly averages and saves them to a CSV.  

It is automatically used in `energy_charts.py`.  

---

## Assumptions  

- The CSV file in `prices_transformation.py` is downloaded via `energy_charts.py`.  
- Selenium WebDriver has a long implicit wait to handle slow-loading pages.  
- JavaScript is disabled in `marketwatch_disable.py` to speed up avoid blocking issues but still it gives javascript disabled error after some successful requests.
---

## Code Structure  

- **`energy_charts.py`**:  
  - Initializes the Selenium WebDriver.  
  - Navigates to the energy price page and downloads a CSV CSV is already downloaded you change country and year and download any CSV file add it file_path in clean_data function in price_transformation.py.  
  - Calls `clean_data()` and `compute_time_series()`.  

- **`marketwatch_disable.py`**:  
  - Disables JavaScript for efficiency.  
  - Iterates through pages, extracts futures data, and saves it as JSON.  

- **`prices_transformation.py`**:  
  - Cleans "energy-charts_Electricity_production_and_spot_prices_in_Germany_in_2025.csv" and formats CSV data.  
  - Aggregates monthly energy price trends.  

---

## Output  

- `energy_charts.py`: Processed CSV file (for eg.`germany_2025.csv`).  
- `marketwatch_disable.py`: JSON file (`output.json`).  
