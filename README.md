# AI Agent for TPRM (Third-Party Risk Management)

## Overview

This project implements an AI-based monitoring agent for assessing the reliability of third-party ICT vendors over time. The system is designed to support the IORC (Integrated Operational Resilience Centre) in financial institutions, with features aligned to regulatory frameworks like DORA.

The agent collects financial data, derives behavioral indicators, and computes a dynamic Trust Score (0–10) for each supplier. It also visualizes trends and flags suppliers that become potentially risky during long-term contracts.

## Getting Started

1. **Create and activate a virtual environment**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the script**

    ```bash
    python3 monitor.py
    ```

4. **Check the `monitoring/` folder**

    You'll find:

    - `.csv` files with daily metrics and trust scores;
    - `.png` plots of trust score trends;
    - `.txt` file with aggregated trust score value.

5. **At the end, deactivate a virtual environment**

    ```bash
    deactivate
    ```

## Configuration Options

The `period` and `interval` parameters define how much historical data is collected and how frequently data points are sampled. These values follow [(Python) Yahoo Finance API](https://pypi.org/project/yfinance/) limitations.

### `period` (How far back to fetch data)

Valid values include:

| Value    | Description                  |
|----------|------------------------------|
| `"1d"`   | 1 day                        |
| `"5d"`   | 5 days                       |
| `"7d"`   | 7 days                       |
| `"14d"`  | 14 days                      |
| `"1mo"`  | 1 month                      |
| `"3mo"`  | 3 months                     |
| `"6mo"`  | 6 months                     |
| `"1y"`   | 1 year                       |
| `"2y"`   | 2 years                      |
| `"5y"`   | 5 years                      |
| `"10y"`  | 10 years                     |
| `"ytd"`  | Year-to-date (from Jan 1st)  |
| `"max"`  | Full historical data         |

**Note**: If you use `interval="1h"` (hourly data), the maximum allowed period is `"730d"` (2 years).

### `interval` (Sampling frequency)

Valid values include:

| Value     | Description                         |
|-----------|-------------------------------------|
| `"1m"`    | Every 1 minute *(recent days only)* |
| `"2m"`    | Every 2 minutes                     |
| `"5m"`    | Every 5 minutes                     |
| `"15m"`   | Every 15 minutes                    |
| `"30m"`   | Every 30 minutes                    |
| `"60m"`   | Every 1 hour                        |
| `"1h"`    | Every 1 hour (same as "60m")        |
| `"90m"`   | Every 90 minutes                    |
| `"1d"`    | Daily                               |
| `"5d"`    | Every 5 days                        |
| `"1wk"`   | Weekly                              |
| `"1mo"`   | Monthly                             |
| `"3mo"`   | Quarterly                           |

**Note**: Minute-level intervals (`1m`, `5m`, etc.) only work with short periods like `"7d"` or `"14d"`.

## Input Metrics and Trust Evaluation Logic

### Financial Metrics Collected from Yahoo Finance

For each monitored vendor (such as Microsoft, IBM, or NVIDIA), the system collects time-series financial data directly from Yahoo Finance. These metrics reflect how the stock has behaved during each market interval (hourly, daily, etc.), and serve as the foundation for all trust-related analysis.

The retrieved data includes:

- `Open`: the price at which the stock began trading at the start of the market session (typically at 09:30 AM US Eastern Time).

- `High`: the highest price reached during the selected time interval.

- `Low`: the lowest price recorded during the same interval.

- `Close`: the final price of the stock at the end of the interval or market session.

- `Volume`: the total number of shares traded within that interval — a useful indicator of market interest or unusual activity.

- `Dividends`: if applicable, this field shows the dividend payout declared to shareholders on that day.

- `Stock Splits`: this field records events where a company's shares are split or consolidated (e.g., 2-for-1 split). These are rare but relevant structural changes in stock behavior.

**Note**: `Dividend` and `Stock Splits` values are often zero, as these events do not occur on a daily basis.

### Derived Indicators for Vendor Behavior

To evaluate the reliability of each vendor over time, the system calculates a set of behavioral indicators based on historical stock data. These indicators help detect signs of instability, risk, or unusual market activity.

Specifically, the agent computes:

- `Percent Change`: This metric captures how much the closing price has changed compared to the previous interval (e.g., the previous hour or day). Sudden large variations — for example, a spike or drop greater than ±5% — may signal news events or abnormal market behavior.

- `Close_MA_3`: This is the moving average of the closing price over the last 3 time periods. It serves to smooth out short-term fluctuations and highlight the general trend of the stock.

- `Close_STD_3`: The standard deviation of the closing price over the last 3 periods. Higher values indicate greater volatility, which is often associated with increased uncertainty or risk.

- `Volume_MA_3` and `Volume_Spike`: The system computes the average trading volume over 3 periods and flags a "spike" if the current volume exceeds twice that average. A spike may suggest abnormal interest in the stock — potentially due to insider activity, speculative moves, or unexpected news.

- `Consecutive_Drops`: This indicator counts how many consecutive periods the stock has closed lower than the previous one. A downward trend lasting 3 or more periods may reflect market concerns or a loss of confidence in the vendor.

### Trust Score Logic Calculation and Risk Interpretation

To quantify the overall reliability of each vendor, the system assigns a Trust Score on a scale from 0 to 10.
This score is calculated dynamically for each time interval (e.g., hourly or daily), based on the vendor’s financial behavior over time.

The calculation starts from the maximum score of 10, and specific conditions trigger score reductions, based on risk indicators:

- If the price variation (Percent Change) exceeds ±1% compared to the previous period, **1 point** is subtracted. This kind of volatility may reflect instability, strong speculation, or sudden market reactions.

- If the price volatility (Close_STD_3) is greater than 3 — meaning the stock has fluctuated significantly over the past 3 periods — the score is penalized by **2 points**. High volatility is often a sign of market uncertainty or poor investor confidence.

- If a Volume Spike is detected — meaning the trading volume is more than twice the 3-period average — the system considers it an anomaly and subtracts **1 point**. This could indicate abnormal interest, speculative trades, or undisclosed information circulating in the market.

- If the stock price drops for 3 consecutive periods, the vendor is flagged for a possible negative trend, and the score is reduced by **2 points**. This suggests declining performance or reduced market trust.

At the end of this process, the final Trust Score reflects the vendor’s current risk posture. The score is always bounded between **0 (worst)** and **10 (best)**.

The score is then interpreted as follows:

- **8 to 10**: The vendor is considered reliable and stable.

- **5 to 7**: The vendor shows some warning signals and should be monitored.

- **0 to 4**: The vendor is at risk and may require further evaluation or action.

In addition to per-interval scores, the system also computes an aggregated Trust Score, which represents the average score across the entire analysis period.
This value is plotted as a horizontal red line on each vendor's chart, making it easier to compare short-term changes against long-term performance.
