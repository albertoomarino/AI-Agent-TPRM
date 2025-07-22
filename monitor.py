import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

from config import vendors, period, interval, output_dir

os.makedirs(output_dir, exist_ok=True)


def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period,
                         interval=interval)
    hist["Percent Change"] = hist["Close"].pct_change() * 100
    hist["Close_MA_3"] = hist["Close"].rolling(window=3).mean()
    hist["Close_STD_3"] = hist["Close"].rolling(window=3).std()
    hist["Volume_MA_3"] = hist["Volume"].rolling(window=3).mean()
    hist["Volume_Spike"] = hist["Volume"] > (hist["Volume_MA_3"] * 2)
    hist["Down_Trend"] = hist["Close"] < hist["Close"].shift(1)
    hist["Consecutive_Drops"] = hist["Down_Trend"].rolling(window=3).sum()
    return hist.round(2)


def compute_trust_score(row):
    score = 10
    if abs(row["Percent Change"]) > 1:
        score -= 1
    if pd.notna(row["Close_STD_3"]) and row["Close_STD_3"] > 3:
        score -= 2
    if row["Volume_Spike"]:
        score -= 1
    if pd.notna(row["Consecutive_Drops"]) and row["Consecutive_Drops"] >= 3:
        score -= 2
    return max(score, 0)


def plot_trust_score(df, ticker, date_str):
    plt.figure(figsize=(10, 5))
    df["Trust Score"].plot(
        linestyle="-", title=f"{ticker} - Trust Score Trend", label="Trust Score")
    plt.ylabel("Trust Score (0-10)")
    plt.xlabel("Date")
    plt.grid(True)

    # Linea rossa della media, PRIMA del savefig
    if "Aggregated" in df.index:
        avg_score = df.loc["Aggregated", "Trust Score"]
        if pd.notna(avg_score):
            plt.axhline(y=avg_score, color="red", linestyle="--",
                        linewidth=1, label="Avg Trust Score")
            plt.legend()

    plt.tight_layout()
    plt.savefig(f"{output_dir}/{ticker}_ts_{date_str}.png")
    plt.close()


def plot_combined_trust_scores(all_data):
    plt.figure(figsize=(12, 6))
    for ticker, df in all_data.items():
        df["Trust Score"].plot(label=ticker)
    plt.title("Trust Score Comparison Across Vendors")
    plt.ylabel("Trust Score")
    plt.xlabel("Date")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    today = datetime.today().strftime("%Y-%m-%d")
    plt.savefig(f"{output_dir}/global_ts_{today}.png")
    plt.close()


def process_vendor(ticker, name, all_data):
    today = datetime.today().strftime("%Y-%m-%d")
    print(f"[INFO] Processing {name} ({ticker})")

    stock_data = get_stock_data(ticker)
    stock_data["Trust Score"] = stock_data.apply(compute_trust_score, axis=1)

    # Calcola il Trust Score aggregato (media)
    aggregated_score = stock_data["Trust Score"].mean()

    # Aggiunge una riga 'Aggregated' nel CSV (ultima riga)
    stock_data.loc["Aggregated"] = [None] * \
        (stock_data.shape[1] - 1) + [aggregated_score]

    # Grafico ora include la linea rossa della media
    plot_trust_score(stock_data, ticker, today)

    # Salva il CSV aggiornato
    stock_data.to_csv(f"{output_dir}/{ticker}_stock_{today}.csv")

    # Salva anche il valore aggregato in un file .txt
    with open(f"{output_dir}/{ticker}_aggregated_score.txt", "w") as f:
        f.write(
            f"Aggregated Trust Score ({period}): {aggregated_score:.2f}")

    # Salva i dati anche nel dizionario condiviso
    all_data[ticker] = stock_data


if __name__ == "__main__":
    combined_data = {}
    for vendor in vendors:
        try:
            process_vendor(vendor["ticker"], vendor["name"], combined_data)
        except Exception as e:
            print(f"[ERROR] Failed for {vendor['ticker']}: {e}")
    plot_combined_trust_scores(combined_data)
