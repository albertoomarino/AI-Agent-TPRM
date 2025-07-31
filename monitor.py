import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os
import re
from config import vendors, period, interval, output_dir

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)


# Fetch stock data and calculate additional metrics
def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period, interval=interval)
    # Daily percent change in stock price
    hist["Percent Change"] = hist["Close"].pct_change() * 100
    # 3-day moving average of closing price
    hist["Close_MA_3"] = hist["Close"].rolling(window=3).mean()
    # 3-day standard deviation of closing price (volatility)
    hist["Close_STD_3"] = hist["Close"].rolling(window=3).std()
    # 3-day moving average of trading volume
    hist["Volume_MA_3"] = hist["Volume"].rolling(window=3).mean()
    # Detect abnormal spikes in trading volume
    hist["Volume_Spike"] = hist["Volume"] > (hist["Volume_MA_3"] * 2)
    # Detect if the price is going down compared to previous day
    hist["Down_Trend"] = hist["Close"] < hist["Close"].shift(1)
    # Count consecutive days of price drops
    hist["Consecutive_Drops"] = hist["Down_Trend"].rolling(window=3).sum()
    return hist.round(2)


# Calculate trust score based on penalties and bonuses
def compute_trust_score(row):
    # Penalty for high volatility
    vol_penalty = min(row["Close_STD_3"] / 2, 3) if pd.notna(row["Close_STD_3"]) else 0
    # Penalty for large daily price changes
    change_penalty = min(abs(row["Percent Change"]) / 2, 2)
    # Penalty for a negative spike in volume
    spike_penalty = 1 if row["Volume_Spike"] and row["Percent Change"] <= 0 else 0
    # Bonus for a positive spike in volume
    spike_bonus = 1 if row["Volume_Spike"] and row["Percent Change"] > 0 else 0
    # Penalty for 3 or more consecutive price drops
    drops_penalty = (
        2 if pd.notna(row["Consecutive_Drops"]) and row["Consecutive_Drops"] >= 3 else 0
    )
    # Calculate final score (base 10)
    score = (
        10
        - (vol_penalty + change_penalty + spike_penalty + drops_penalty)
        + spike_bonus
    )
    # Clamp score between 0 and 10
    return float(max(0, min(10, score)))


# Plot the trust score trend for a single vendor
def plot_trust_score(df, ticker, date_str):
    plt.figure(figsize=(10, 5))
    # Highlight risk zones with background colors
    plt.axhspan(0, 5, facecolor="red", alpha=0.1)
    plt.axhspan(5, 8, facecolor="yellow", alpha=0.1)
    plt.axhspan(8, 10, facecolor="green", alpha=0.1)
    # Plot the trust score line
    df["Trust Score"].plot(
        linestyle="-",
        title=f"{ticker} - Trust Score Trend",
        label="Trust Score",
    )
    plt.ylabel("Trust Score (0-10)")
    plt.xlabel("Date")
    plt.ylim(0, 10)
    plt.grid(True)
    # Draw the aggregated average score as a dashed line if it exists
    if "Aggregated" in df.index:
        avg_score = df.loc["Aggregated", "Trust Score"]
        if pd.notna(avg_score):
            plt.axhline(
                y=avg_score,
                color="red",
                linestyle="--",
                linewidth=1,
                label="Avg Trust Score",
            )
            plt.legend()
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{ticker}_ts_{date_str}.png")
    plt.close()


# Plot combined trust scores for all vendors
def plot_combined_trust_scores(all_data):
    # If period is longer than 1 month, use monthly averages
    long_period_values = ["3mo", "6mo", "1y", "2y", "5y", "10y", "ytd"]
    use_monthly_avg = period in long_period_values
    records = []
    # Prepare data for plotting
    for ticker, df in all_data.items():
        df = df[df.index != "Aggregated"].reset_index()
        df.rename(columns={df.columns[0]: "Date"}, inplace=True)
        df["Vendor"] = ticker
        records.append(df[["Date", "Trust Score", "Vendor"]])
    combined_df = pd.concat(records)
    combined_df = combined_df[combined_df["Date"] != "Aggregated"]
    combined_df["Date"] = pd.to_datetime(combined_df["Date"], errors="coerce")
    combined_df = combined_df.dropna(subset=["Date"])
    plt.figure(figsize=(12, 6))
    # Highlight risk zones
    plt.axhspan(0, 5, facecolor="red", alpha=0.1)
    plt.axhspan(5, 8, facecolor="yellow", alpha=0.1)
    plt.axhspan(8, 10, facecolor="green", alpha=0.1)
    # Use monthly averages for long periods
    if use_monthly_avg:
        combined_df = combined_df.set_index("Date")
        combined_df = (
            combined_df.groupby([pd.Grouper(freq="ME"), "Vendor"])["Trust Score"]
            .mean()
            .reset_index()
        )
        for vendor in combined_df["Vendor"].unique():
            df = combined_df[combined_df["Vendor"] == vendor]
            plt.plot(df["Date"], df["Trust Score"], label=vendor, marker="o")
    else:
        # Plot daily data points for short periods
        for vendor in combined_df["Vendor"].unique():
            df = combined_df[combined_df["Vendor"] == vendor]
            plt.plot(
                df["Date"], df["Trust Score"], label=vendor, linestyle="-", marker="."
            )
    plt.title("Trust Score Comparison Across Vendors")
    plt.ylabel("Trust Score (0–10")
    plt.xlabel("Date")
    plt.ylim(0, 10)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    today = datetime.today().strftime("%Y-%m-%d")
    plt.savefig(f"{output_dir}/global_ts_{today}.png")
    plt.close()


# Process each vendor: fetch data, compute score, save results
def process_vendor(ticker, name, all_data):
    today = datetime.today().strftime("%Y-%m-%d")
    print(f"\nCOMPANY: {name} ({ticker})")
    stock_data = get_stock_data(ticker)
    stock_data["Trust Score"] = stock_data.apply(compute_trust_score, axis=1)
    aggregated_score = stock_data["Trust Score"].mean()
    # Print vendor status based on average trust score
    if pd.notna(aggregated_score):
        if aggregated_score >= 8:
            status = "RELIABLE: the vendor is considered stable"
        elif 5 <= aggregated_score < 8:
            status = "WARNING: the vendor shows some signals and should be monitored"
        else:
            status = "AT RISK: the vendor may require further evaluation or action"
        print(f"Trust Score = {aggregated_score:.2f} → {status}")
    else:
        print(
            "Trust Score = nan → AT RISK: the vendor may require further evaluation or action"
        )
    # Add aggregated row
    stock_data.loc["Aggregated"] = [None] * (stock_data.shape[1] - 1) + [
        aggregated_score
    ]
    # Save chart and CSV
    plot_trust_score(stock_data, ticker, today)
    stock_data.to_csv(f"{output_dir}/{ticker}_stock_{today}.csv")
    # Save aggregated score in a text file
    with open(f"{output_dir}/{ticker}_aggregated_score.txt", "w") as f:
        f.write(f"Aggregated Trust Score ({period}): {aggregated_score:.2f}")
    all_data[ticker] = stock_data


# Main script execution
if __name__ == "__main__":
    print(f"Initial Configuration: \n- Period: {period} \n- Interval: {interval}")
    combined_data = {}
    for vendor in vendors:
        try:
            process_vendor(vendor["ticker"], vendor["name"], combined_data)
        except Exception as e:
            print(f"[ERROR] Failed for {vendor['ticker']}: {e}")
    # Plot combined scores for all vendors
    plot_combined_trust_scores(combined_data)
