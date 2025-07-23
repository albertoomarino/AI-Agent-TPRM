# Import external libraries used for data collection, processing and visualization
import yfinance as yf           # Library to fetch financial data from Yahoo Finance
# Library for working with tabular data (dataframes)
import pandas as pd
import matplotlib.pyplot as plt  # Library to create charts and plots
from datetime import datetime   # Module to work with dates and times
import os                       # Module to interact with the file system

# Import project-specific settings from config.py
from config import vendors, period, interval, output_dir

# Create the output directory if it doesn't already exist
os.makedirs(output_dir, exist_ok=True)


def get_stock_data(ticker):
    """
    Fetches historical stock data for a given company (ticker)
    and calculates several financial indicators used for risk monitoring.
    """

    # Download the stock data for the selected company (ticker symbol)
    stock = yf.Ticker(ticker)

    # Get the historical price data using the configured period and interval
    hist = stock.history(period=period, interval=interval)

    # Calculate the percentage change from the previous closing price
    hist["Percent Change"] = hist["Close"].pct_change() * 100

    # Calculate a 3-period moving average of the closing price
    hist["Close_MA_3"] = hist["Close"].rolling(window=3).mean()

    # Calculate the 3-period standard deviation (volatility) of the closing price
    hist["Close_STD_3"] = hist["Close"].rolling(window=3).std()

    # Calculate a 3-period moving average of trading volume
    hist["Volume_MA_3"] = hist["Volume"].rolling(window=3).mean()

    # Check if today's volume is more than double the 3-period average (anomaly)
    hist["Volume_Spike"] = hist["Volume"] > (hist["Volume_MA_3"] * 2)

    # Check if the stock closed lower than the previous period (downtrend flag)
    hist["Down_Trend"] = hist["Close"] < hist["Close"].shift(1)

    # Count how many of the last 3 periods had a downtrend
    hist["Consecutive_Drops"] = hist["Down_Trend"].rolling(window=3).sum()

    # Round all values to 2 decimal places and return the final table
    return hist.round(2)


def compute_trust_score(row):
    """
    Calculates the Trust Score (0–10) for a single time point based on risk signals.
    The score starts at 10 and decreases according to volatility, volume spikes,
    strong price changes, and negative trends.
    """

    score = 10  # Start from the maximum trust score

    # If the price changed more than ±1%, reduce the score (indicates instability)
    if abs(row["Percent Change"]) > 1:
        score -= 1

    # If volatility (standard deviation) is high, reduce the score more
    if pd.notna(row["Close_STD_3"]) and row["Close_STD_3"] > 3:
        score -= 2

    # If there is a volume spike (trading volume unusually high), reduce the score
    if row["Volume_Spike"]:
        score -= 1

    # If the stock has dropped for 3 periods in a row, reduce the score more
    if pd.notna(row["Consecutive_Drops"]) and row["Consecutive_Drops"] >= 3:
        score -= 2

    # Ensure the final score is not negative
    return max(score, 0)


def plot_trust_score(df, ticker, date_str):
    """
    Plots the Trust Score trend for a specific vendor.
    The chart includes a line for each time point and a horizontal red line
    showing the average Trust Score over the period.
    Saves the chart as a .png image in the output folder.
    """

    # Create a new figure with custom size
    plt.figure(figsize=(10, 5))

    # Plot the Trust Score as a line chart
    df["Trust Score"].plot(
        linestyle="-",                     # solid line
        title=f"{ticker} - Trust Score Trend",  # title with company name
        label="Trust Score"               # legend label for the line
    )

    # Label the axes
    plt.ylabel("Trust Score (0-10)")
    plt.xlabel("Date")

    # Show grid lines for easier reading
    plt.grid(True)

    # If the average score is available, draw it as a red dashed line
    if "Aggregated" in df.index:
        avg_score = df.loc["Aggregated", "Trust Score"]
        if pd.notna(avg_score):
            plt.axhline(                  # horizontal line for average
                y=avg_score,
                color="red",
                linestyle="--",
                linewidth=1,
                label="Avg Trust Score"
            )
            plt.legend()  # Show the legend if average line is added

    # Improve spacing and layout
    plt.tight_layout()

    # Save the chart as an image file
    plt.savefig(f"{output_dir}/{ticker}_ts_{date_str}.png")
    plt.close()


def plot_combined_trust_scores(all_data):
    """
    Creates a single line chart to compare Trust Scores across all vendors.
    Each vendor's Trust Score is shown with a different colored line.
    The chart is saved as an image in the output folder.
    """

    # Create a new figure for the combined chart
    plt.figure(figsize=(12, 6))

    # Loop through all vendors and plot their Trust Scores
    for ticker, df in all_data.items():
        # Use vendor ticker as legend label
        df["Trust Score"].plot(label=ticker)

    # Set chart title and axis labels
    plt.title("Trust Score Comparison Across Vendors")
    plt.ylabel("Trust Score")
    plt.xlabel("Date")

    # Add legend to identify each vendor
    plt.legend()

    # Add grid lines for readability
    plt.grid(True)

    # Adjust layout spacing
    plt.tight_layout()

    # Save the chart with today's date in the filename
    today = datetime.today().strftime("%Y-%m-%d")
    plt.savefig(f"{output_dir}/global_ts_{today}.png")

    # Close the plot to free memory
    plt.close()


def process_vendor(ticker, name, all_data):
    """
    Executes the full monitoring process for a single vendor:
    - Downloads stock data
    - Computes trust scores
    - Calculates the average score
    - Generates and saves visualizations and CSV reports
    """

    # Get today's date in YYYY-MM-DD format
    today = datetime.today().strftime("%Y-%m-%d")

    # Print progress message in the terminal
    print(f"[INFO] Processing {name} ({ticker})")

    # Get stock data and calculate financial indicators
    stock_data = get_stock_data(ticker)

    # Compute the Trust Score for each row in the dataset
    stock_data["Trust Score"] = stock_data.apply(compute_trust_score, axis=1)

    # Compute the average Trust Score over the entire period
    aggregated_score = stock_data["Trust Score"].mean()

    # Add a new row to the DataFrame to store the average score
    stock_data.loc["Aggregated"] = [None] * \
        (stock_data.shape[1] - 1) + [aggregated_score]

    # Create a chart showing Trust Score and average line
    plot_trust_score(stock_data, ticker, today)

    # Save the full stock + trust score data to CSV
    stock_data.to_csv(f"{output_dir}/{ticker}_stock_{today}.csv")

    # Save the average score in a separate .txt file
    with open(f"{output_dir}/{ticker}_aggregated_score.txt", "w") as f:
        f.write(f"Aggregated Trust Score ({period}): {aggregated_score:.2f}")

    # Add this vendor's data to the shared dictionary for global plotting
    all_data[ticker] = stock_data


if __name__ == "__main__":
    """
    This is the main entry point of the program.
    It loops through all vendors, processes their data,
    and generates the final comparison chart.
    """

    # Create an empty dictionary to store all vendors' processed data
    combined_data = {}

    # Loop through each vendor defined in the config
    for vendor in vendors:
        try:
            # Run the full monitoring process for each vendor
            process_vendor(vendor["ticker"], vendor["name"], combined_data)
        except Exception as e:
            # If something goes wrong, print an error message but continue
            print(f"[ERROR] Failed for {vendor['ticker']}: {e}")

    # After all vendors are processed, generate the global comparison chart
    plot_combined_trust_scores(combined_data)
