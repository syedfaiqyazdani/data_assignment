import pandas as pd


def clean_data():
    # Load the CSV file
    file_path = "energy-charts_Electricity_production_and_spot_prices_in_Germany_in_2025.csv"
    df = pd.read_csv(file_path)

    # Drop the first row, which contains unit information
    df_cleaned = df.iloc[1:].copy()

    # Rename columns for clarity
    df_cleaned.columns = ["Date", "Non-Renewable", "Renewable", "Day-Ahead Auction"]

    # Convert data types
    df_cleaned["Date"] = pd.to_datetime(df_cleaned["Date"].str[:10])  # Extract YYYY-MM-DD and convert to datetime
    df_cleaned["Non-Renewable"] = pd.to_numeric(df_cleaned["Non-Renewable"], errors='coerce')
    df_cleaned["Renewable"] = pd.to_numeric(df_cleaned["Renewable"], errors='coerce')
    df_cleaned["Day-Ahead Auction"] = pd.to_numeric(df_cleaned["Day-Ahead Auction"], errors='coerce')

    # Extract year-month for aggregation
    df_cleaned["Month"] = df_cleaned["Date"].dt.to_period("M")
    return df_cleaned

def compute_time_series(df_cleaned,country,year):
    # Compute monthly averages
    monthly_avg = df_cleaned.groupby("Month")[["Non-Renewable", "Renewable", "Day-Ahead Auction"]].mean().reset_index()

    # Add country column
    monthly_avg["Country"] = country

    # Save the transformed data to a CSV file
    output_csv_path = f"{country}_{year}.csv"
    monthly_avg.to_csv(output_csv_path, index=False)

    print(f"Monthly averaged data saved to {output_csv_path}")