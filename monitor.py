import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os
import re
from config import vendors, period, interval, output_dir

os.makedirs(output_dir, exist_ok=True)


def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period, interval=interval)
    hist["Percent Change"] = hist["Close"].pct_change() * 100
    hist["Close_MA_3"] = hist["Close"].rolling(window=3).mean()
    hist["Close_STD_3"] = hist["Close"].rolling(window=3).std()
    hist["Volume_MA_3"] = hist["Volume"].rolling(window=3).mean()
    hist["Volume_Spike"] = hist["Volume"] > (hist["Volume_MA_3"] * 2)
    hist["Down_Trend"] = hist["Close"] < hist["Close"].shift(1)
    hist["Consecutive_Drops"] = hist["Down_Trend"].rolling(window=3).sum()
    return hist.round(2)


def compute_trust_score(row):
    vol_penalty = min(row["Close_STD_3"] / 2, 3) if pd.notna(row["Close_STD_3"]) else 0
    change_penalty = min(abs(row["Percent Change"]) / 2, 2)
    spike_penalty = 1 if row["Volume_Spike"] and row["Percent Change"] <= 0 else 0
    spike_bonus = 1 if row["Volume_Spike"] and row["Percent Change"] > 0 else 0
    drops_penalty = (
        2 if pd.notna(row["Consecutive_Drops"]) and row["Consecutive_Drops"] >= 3 else 0
    )
    score = (
        10
        - (vol_penalty + change_penalty + spike_penalty + drops_penalty)
        + spike_bonus
    )
    return float(max(0, min(10, score)))


def plot_trust_score(df, ticker, date_str):
    plt.figure(figsize=(10, 5))
    plt.axhspan(0, 5, facecolor="red", alpha=0.1)
    plt.axhspan(5, 8, facecolor="yellow", alpha=0.1)
    plt.axhspan(8, 10, facecolor="green", alpha=0.1)
    df["Trust Score"].plot(
        linestyle="-",
        title=f"{ticker} - Trust Score Trend",
        label="Trust Score",
    )
    plt.ylabel("Trust Score (0-10)")
    plt.xlabel("Date")
    plt.ylim(0, 10)
    plt.grid(True)
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


def plot_combined_trust_scores(all_data):
    # Only treat as long period if the period string is in predefined values beyond 1mo
    long_period_values = ["3mo", "6mo", "1y", "2y", "5y", "10y", "ytd"]
    use_monthly_avg = period in long_period_values
    records = []
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
    plt.axhspan(0, 5, facecolor="red", alpha=0.1)
    plt.axhspan(5, 8, facecolor="yellow", alpha=0.1)
    plt.axhspan(8, 10, facecolor="green", alpha=0.1)
    if use_monthly_avg:
        combined_df = combined_df.set_index("Date")
        # Use 'ME' instead of deprecated 'M'
        combined_df = (
            combined_df.groupby([pd.Grouper(freq="ME"), "Vendor"])["Trust Score"]
            .mean()
            .reset_index()
        )
        for vendor in combined_df["Vendor"].unique():
            df = combined_df[combined_df["Vendor"] == vendor]
            plt.plot(df["Date"], df["Trust Score"], label=vendor, marker="o")
    else:
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


def process_vendor(ticker, name, all_data):
    today = datetime.today().strftime("%Y-%m-%d")
    print(f"\nCOMPANY: {name} ({ticker})")
    stock_data = get_stock_data(ticker)
    stock_data["Trust Score"] = stock_data.apply(compute_trust_score, axis=1)
    aggregated_score = stock_data["Trust Score"].mean()
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
    stock_data.loc["Aggregated"] = [None] * (stock_data.shape[1] - 1) + [
        aggregated_score
    ]
    plot_trust_score(stock_data, ticker, today)
    stock_data.to_csv(f"{output_dir}/{ticker}_stock_{today}.csv")
    with open(f"{output_dir}/{ticker}_aggregated_score.txt", "w") as f:
        f.write(f"Aggregated Trust Score ({period}): {aggregated_score:.2f}")
    all_data[ticker] = stock_data


if __name__ == "__main__":
    print(f"Initial Configuration: \n- Period: {period} \n- Interval: {interval}")
    combined_data = {}
    for vendor in vendors:
        try:
            process_vendor(vendor["ticker"], vendor["name"], combined_data)
        except Exception as e:
            print(f"[ERROR] Failed for {vendor['ticker']}: {e}")
    plot_combined_trust_scores(combined_data)
