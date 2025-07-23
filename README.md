# AI Agent for TPRM (Third-Party Risk Management)

## Overview

This project is part of my thesis work and aims to design and implement an AI-based monitoring agent for evaluating the reliability of third-party ICT service providers over time. The goal is to support the strategic activities of the Integrated Operational Resilience Centre (IORC) within a financial institution, by offering a tool that continuously tracks the operational soundness of external vendors based on objective, data-driven metrics.

The system relies on financial market data as a proxy for vendor health and stability. For each selected supplier, it collects stock price information from Yahoo Finance, analyzes short-term behavioral patterns, and derives custom indicators such as price volatility, volume anomalies, and trend persistence. These indicators are then combined to calculate a dynamic Trust Score on a scale from 0 to 10, which reflects the vendor’s level of risk or reliability at any given time.

The Trust Score is recalculated at regular intervals (hourly or daily), depending on the configuration, and is visualized through automated charts and summary reports. In addition to individual trend analysis, the system provides an aggregate score for each vendor over the entire monitoring period. This allows the institution to detect emerging risks early, assess whether a vendor’s performance is deteriorating over time, and make more informed decisions regarding long-term contracts or critical service dependencies.

The project aligns with regulatory expectations such as those outlined in the European DORA (Digital Operational Resilience Act), which emphasize the need for ongoing risk assessments and third-party oversight in the financial sector. By integrating this monitoring tool into existing operational workflows, the IORC can better anticipate disruptions, comply with audit requirements, and enhance overall resilience against ICT-related vulnerabilities.

## Project Structure and File Overview

Here’s a quick guide to the main files included in this project:

- `monitor.py` is the main script. It contains the logic for retrieving financial data, calculating indicators and Trust Scores, generating plots, and saving outputs for each vendor.

- `config.py` allows you to configure the tool. Here you define which vendors to monitor, how much historical data to collect (via the `period` parameter), how frequently to sample it (`interval`), and where to save the results.

- `requirements.txt` lists all the required Python packages.

- Once the program is executed, a `monitoring/` folder is automatically created. This directory will contain CSV files with financial data and computed scores, trend plots for each vendor, and logs with the aggregated Trust Scores.

Before launching the tool, make sure to check and customize the vendor list and parameters inside `config.py` to match your monitoring needs.

## Getting Started

1. Create and activate a virtual environment

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

5. At the end, deactivate a virtual environment

    ```bash
    deactivate
    ```

## Configuration Options

### Vendors to Monitor

The agent is designed to work with publicly listed ICT providers, whose financial data is available through platforms like Yahoo Finance. Below are examples of vendors you can include in the configuration:

- **Cloud and Infrastructure Providers**

    | Company             | Ticker | Description                                |
    | ------------------- | ------ | ------------------------------------------ |
    | Microsoft           | MSFT   | Azure, Office 365, enterprise platforms    |
    | Amazon Web Services | AMZN   | Cloud infrastructure and computing         |
    | Google Cloud        | GOOG   | Google Cloud Platform, Workspace tools     |
    | Oracle              | ORCL   | Databases, business software, Oracle Cloud |
    | IBM                 | IBM    | Hybrid cloud, AI, legacy systems           |

- **Cybersecurity and Identity Management**

    | Company             | Ticker | Description                                |
    | ------------------- | ------ | ------------------------------------------ |
    | Palo Alto Networks  | PANW   | Advanced threat protection                 |
    | Fortinet            | FTNT   | Network firewalls, endpoint security       |
    | CrowdStrike         | CRWD   | Threat intelligence, endpoint detection    |
    | Okta                | OKTA   | Identity and access management             |

- **Software, Platforms, and IT Operations**

    | Company             | Ticker | Description                                |
    | ------------------- | ------ | ------------------------------------------ |
    | NVIDIA              | NVDA   | AI hardware, GPUs, cloud data centers      |
    | Cisco Systems       | CSCO   | Networking, security, infrastructure       |
    | ServiceNow          | NOW    | IT service management, workflows           |
    | Salesforce          | CRM    | CRM, analytics, SaaS platforms             |
    | Atlassian           | TEAM   | Jira, Confluence, cloud development tools  |
    | Adobe               | ADBE   | Creative and document cloud platforms      |
    | HP Enterprise       | HPE    | Hybrid IT, edge-to-cloud infrastructure    |
    | Dell Technologies   | DELL   | Servers, storage, enterprise solutions     |

    **Note**: You can include any of these vendors in your `config.py` file by adding their stock ticker and name. Make sure the ticker is valid on Yahoo Finance.

### `period` and `interval` parameters

The `period` and `interval` parameters define how much historical data is collected and how frequently data points are sampled. These values follow [(Python) Yahoo Finance API](https://pypi.org/project/yfinance/) limitations.

- `period` (How far back to fetch data)

    Valid values include:

    | Value    | Description                          |
    |----------|--------------------------------------|
    | `1d`     | 1 day                                |
    | `5d`     | 5 days                               |
    | `7d`     | 7 days                               |
    | `14d`    | 14 days                              |
    | `1mo`    | 1 month                              |
    | `3mo`    | 3 months                             |
    | `6mo`    | 6 months                             |
    | `1y`     | 1 year                               |
    | `2y`     | 2 years                              |
    | `5y`     | 5 years                              |
    | `10y`    | 10 years                             |
    | `ytd`    | Year-to-date (from Jan 1st)          |
    | `max`    | Full historical data                 |

    **Note**: If you use `interval="1h"` (hourly data), the maximum allowed period is `730d` (2 years).

- `interval` (Sampling frequency)

    Valid values include:

    | Value     | Description                         |
    |-----------|-------------------------------------|
    | `1m`      | Every 1 minute *(recent days only)* |
    | `2m`      | Every 2 minutes                     |
    | `5m`      | Every 5 minutes                     |
    | `15m`     | Every 15 minutes                    |
    | `30m`     | Every 30 minutes                    |
    | `60m`     | Every 1 hour                        |
    | `1h`      | Every 1 hour (same as "60m")        |
    | `90m`     | Every 90 minutes                    |
    | `1d`      | Daily                               |
    | `5d`      | Every 5 days                        |
    | `1wk`     | Weekly                              |
    | `1mo`     | Monthly                             |
    | `3mo`     | Quarterly                           |

    **Note**: Minute-level intervals (`1m`, `5m`, etc.) only work with short periods like `7d` or `14d`.

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

- If the price variation (`Percent Change`) exceeds ±1% compared to the previous period, **1 point** is subtracted. This kind of volatility may reflect instability, strong speculation, or sudden market reactions.

- If the price volatility (`Close_STD_3`) is greater than 3 — meaning the stock has fluctuated significantly over the past 3 periods — the score is penalized by **2 points**. High volatility is often a sign of market uncertainty or poor investor confidence.

- If a Volume Spike is detected — meaning the trading volume is more than twice the 3-period average — the system considers it an anomaly and subtracts **1 point**. This could indicate abnormal interest, speculative trades, or undisclosed information circulating in the market.

- If the stock price drops for 3 consecutive periods, the vendor is flagged for a possible negative trend, and the score is reduced by **2 points**. This suggests declining performance or reduced market trust.

At the end of this process, the final Trust Score reflects the vendor’s current risk posture. The score is always bounded between **0 (worst)** and **10 (best)**.

The score is then interpreted as follows:

- **8 to 10**: The vendor is considered reliable and stable.

- **5 to 7**: The vendor shows some warning signals and should be monitored.

- **0 to 4**: The vendor is at risk and may require further evaluation or action.

In addition to per-interval scores, the system also computes an aggregated Trust Score, which represents the average score across the entire analysis period.
This value is plotted as a horizontal red line on each vendor's chart, making it easier to compare short-term changes against long-term performance.
