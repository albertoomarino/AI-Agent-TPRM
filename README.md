# AI Agent for TPRM (Third-Party Risk Management)

## Overview

This project implements an AI-based monitoring agent for assessing the reliability of third-party ICT vendors over time. The system is designed to support the IORC (Integrated Operational Resilience Centre) in financial institutions, with features aligned to regulatory frameworks like DORA.

The agent collects financial data, derives behavioral indicators, and computes a dynamic Trust Score (0–10) for each supplier. It also visualizes trends and flags suppliers that become potentially risky during long-term contracts.

## Getting Started

1. **Create and activate a virtual environment (recommended)**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2. Install dependencies

    ```bash
    pip install -r requirements.txt
    ```

3. Run the script

    ```bash
    python3 monitor.py
    ```

4. Check the `monitoring/` folder

    You'll find:

    - `.csv` files with daily metrics and trust scores;
    - `.png` plots of trust score trends;
    - `.txt` file with aggregated trust score value.

## Parametri considerati

### Raw Data from Yahoo Finance

For each monitored vendor (e.g., Microsoft, IBM, NVIDIA), the system retrieves the following financial data:

| Parameter        | Description                                |
| ---------------- | ------------------------------------------ |
| **Open**         | Price at market open (e.g., 09:30 US time) |
| **High**         | Highest price reached during the interval  |
| **Low**          | Lowest price during the interval           |
| **Close**        | Final trading price at market close        |
| **Volume**       | Total number of shares traded              |
| **Dividends**    | Amount paid to shareholders (if any)       |
| **Stock Splits** | Share division events (rare)               |

**Note**: Dividends and stock splits are infrequent and may appear as 0 for most days.

### Derived Indicators

The agent computes several indicators to assess vendor stability and detect anomalies:

- **Percent Change**: Daily or hourly percent variation in closing price. Sharp changes (e.g., ±5%) may indicate market reaction to news or instability.

- **Close_MA_3**: 3-period moving average of the closing price. Smooths fluctuations to reveal the general price trend.

- **Close_STD_3**: 3-period standard deviation of closing price. High values suggest volatility, a proxy for market uncertainty.

- **Volume_MA_3 and Volume_Spike**: Average volume over 3 periods. A spike is detected when current volume is more than twice the average → may signal insider activity or unusual events.

- **Consecutive_Drops**: Counts if the vendor’s stock declined for 3 consecutive periods. Indicates a negative performance streak.

### Trust Score Calculation

Each vendor is assigned a Trust Score from 0 to 10. The score starts at 10 and decreases based on negative signals:

| Condition                 | Penalty | Reason                     |
| ------------------------- | ------- | -------------------------- |
| Percent Change > ±1%      | -1      | Too volatile               |
| Volatility > 3            | -2      | Excessive fluctuation      |
| Volume anomaly detected   | -1      | Suspicious activity        |
| 3 consecutive price drops | -2      | Negative performance trend |

Interpretation:

| Trust Score | Status          |
| ----------- | ----------------|
| **8–10**    | Reliable vendor |
| **5–7**     | To be monitored |
| **0–4**     | At-risk vendor  |

An aggregated Trust Score is also computed over the entire time period and visualized as a red reference line in trend charts.
