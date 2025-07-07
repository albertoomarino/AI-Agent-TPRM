import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import feedparser
import matplotlib.pyplot as plt
import json

# STEP 1 – Download stock data


def get_stock_data(ticker="MSFT"):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="7d", interval="1d")
    hist['Percent Change'] = hist['Close'].pct_change() * 100
    hist = hist.round(2)
    return hist

# STEP 2 – Calculate indicators


def enhance_stock_data(df):
    df['Close_MA_3'] = df['Close'].rolling(window=3).mean()
    df['Close_STD_3'] = df['Close'].rolling(window=3).std()
    df['Volume_MA_3'] = df['Volume'].rolling(window=3).mean()
    df['Volume_Spike'] = df['Volume'] > (df['Volume_MA_3'] * 2)
    df['Down_Trend'] = df['Close'] < df['Close'].shift(1)
    df['Consecutive_Drops'] = df['Down_Trend'].rolling(window=3).sum()
    return df

# STEP 3 – Scoring logic


def compute_trust_score(row):
    score = 10
    if abs(row['Percent Change']) > 1:
        score -= 1
    if row['Close_STD_3'] and row['Close_STD_3'] > 3:
        score -= 2
    if row['Volume_Spike']:
        score -= 1
    if row['Consecutive_Drops'] and row['Consecutive_Drops'] >= 3:
        score -= 2
    return max(score, 0)

# STEP 4 – News via RSS


def get_latest_news(company="Microsoft"):
    query = company.replace(" ", "+")
    url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(url)
    news_list = []
    for entry in feed.entries[:5]:
        news_list.append((entry.title, entry.link))
    return news_list

# STEP 5 – Save news


def save_news_to_txt(news, filename):
    with open(filename, "w", encoding="utf-8") as f:
        for title, link in news:
            f.write(f"{title}\n{link}\n\n")

# STEP 6 – Plot Trust Score


def plot_trust_score(df, ticker, date_str, output_dir="monitoring"):
    plt.figure(figsize=(10, 5))
    df['Trust Score'].plot(marker='o', linestyle='-',
                           title=f"{ticker} - Trust Score Trend")
    plt.ylabel("Trust Score (0-10)")
    plt.xlabel("Date")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{ticker}_trust_score_plot_{date_str}.png")
    plt.close()

# MAIN RUNNER


def save_monitoring_data_with_visuals(ticker="MSFT", company_name="Microsoft"):
    today = datetime.today().strftime("%Y-%m-%d")
    directory = "monitoring"
    os.makedirs(directory, exist_ok=True)

    # Data pipeline
    stock_data = get_stock_data(ticker)
    stock_data = enhance_stock_data(stock_data)
    stock_data['Trust Score'] = stock_data.apply(compute_trust_score, axis=1)

    # Save all
    stock_data.to_csv(f"{directory}/{ticker}_stock_{today}.csv")
    news = get_latest_news(company_name)
    save_news_to_txt(news, f"{directory}/{ticker}_news_{today}.txt")
    plot_trust_score(stock_data, ticker, today, directory)

    print(f"[INFO] Monitoring package saved for {ticker} on {today}")


# Run everything
if __name__ == "__main__":
    vendors = [
        {"ticker": "MSFT", "name": "Microsoft"},
        {"ticker": "IBM", "name": "IBM"},
        {"ticker": "ORCL", "name": "Oracle"},
        {"ticker": "AMZN", "name": "Amazon Web Services"},
        {"ticker": "GOOGL", "name": "Google Cloud"}
    ]

    for vendor in vendors:
        print(f"\n[INFO] Processing {vendor['name']} ({vendor['ticker']})")
        try:
            save_monitoring_data_with_visuals(vendor['ticker'], vendor['name'])
        except Exception as e:
            print(f"[ERROR] Failed for {vendor['ticker']}: {e}")
