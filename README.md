# AI Agent for TPRM (Third-Party Risk Management)

## Overview

This project presents an AI-based monitoring agent designed to evaluate the reliability of third-party ICT service providers over time. Developed as part of a thesis focusing on operational resilience in the banking sector, this tool aims to support the strategic activities of an **Integrated Operational Resilience Centre (IORC)** within financial institutions. It offers a data-driven approach to continuously track the operational soundness of external vendors, aligning with modern regulatory expectations.

### Understanding the Integrated Operational Resilience Centre (IORC)

In the contemporary financial landscape, characterized by rapid digitalization, globalized supply chains, and increasing interdependencies, organizations face significant challenges in maintaining operational continuity and responding effectively to crises. The Integrated Operational Resilience Centre (IORC) is introduced as a conceptual framework designed to address these challenges, particularly within the banking sector.

Inspired by NATO's Consultation, Command and Control (C3) Taxonomy, the IORC functions as a multi-layered hub for governance, monitoring, decision-making, and crisis communication. Its primary goal is to enable rapid and informed interventions by integrating organizational and situational data. Key features of the IORC include [\[1\]](#ref1):

* **Multi-layered Architecture**: Structured across six levels, covering governance, core services, communication, processes, roles, and user-facing applications.

* **Data-driven Awareness**: Leverages data to enhance situational awareness, detect anomalies, and guide crisis management decisions.

* **AI and Digital Twin Integration**: Incorporates Artificial Intelligence for observability, predictive analysis, and anomaly detection, alongside Digital Twins for infrastructure replication, impact assessment, and stress testing. This enables continuous validation and learning.

* **Regulatory Alignment**: Designed to be in line with regulations such as the EU’s Digital Operational Resilience Act (DORA), emphasizing oversight of critical ICT providers and promoting accountability and traceability.

In essence, the IORC is not a rigid solution but a flexible, modular, and scalable reference architecture that transforms resilience into a dynamic and measurable capability, crucial for strengthening stability and accelerating recovery in the financial ecosystem.

### Project Contribution to IORC

This AI agent specifically contributes to the IORC's capabilities by providing a robust Third-Party Risk Management (TPRM) monitoring solution. It addresses the critical need for ongoing risk assessments and third-party oversight, as mandated by regulations like DORA. By integrating this monitoring tool into existing operational workflows, the IORC can better anticipate disruptions, comply with audit requirements, and enhance overall resilience against ICT-related vulnerabilities stemming from external dependencies.

## Project Structure and File Overview

Here's a quick guide to the main files included in this project:

* `monitor.py` is the main script. It contains the logic for retrieving financial data, calculating indicators and Trust Scores, generating plots, and saving outputs for each vendor.

* `config.py` allows you to configure the tool. Here you define which vendors to monitor, how much historical data to collect (via the `period` parameter), how frequently to sample it (`interval`), and where to save the results.

* `requirements.txt` lists all the required Python packages.

* Once the program is executed, a `monitoring/` folder is automatically created. This directory will contain CSV files with financial data and computed scores, trend plots for each vendor, and logs with the aggregated Trust Scores.

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

    * `.csv` files with daily metrics and trust scores;
    * `.png` plots of trust score trends;
    * `.txt` file with aggregated trust score value.

5. At the end, deactivate a virtual environment

    ```bash
    deactivate
    ```

## Configuration Options

### Vendors to Monitor

The agent is designed to work with publicly listed ICT providers, whose financial data is available through platforms like Yahoo Finance. Below are examples of vendors you can include in the configuration:

* **Cloud and Infrastructure Providers**

    | Company             | Ticker | Description                                |
    | ------------------- | ------ | ------------------------------------------ |
    | Microsoft           | MSFT   | Azure, Office 365, enterprise platforms    |
    | Amazon Web Services | AMZN   | Cloud infrastructure and computing         |
    | Google Cloud        | GOOG   | Google Cloud Platform, Workspace tools     |
    | Oracle              | ORCL   | Databases, business software, Oracle Cloud |
    | IBM                 | IBM    | Hybrid cloud, AI, legacy systems           |

* **Cybersecurity and Identity Management**

    | Company             | Ticker | Description                                |
    | ------------------- | ------ | ------------------------------------------ |
    | Palo Alto Networks  | PANW   | Advanced threat protection                 |
    | Fortinet            | FTNT   | Network firewalls, endpoint security       |
    | CrowdStrike         | CRWD   | Threat intelligence, endpoint detection    |
    | Okta                | OKTA   | Identity and access management             |

* **Software, Platforms, and IT Operations**

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

* `period` (How far back to fetch data)

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

* `interval` (Sampling frequency)

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

* `Open`: the price at which the stock began trading at the start of the market session (typically at 09:30 AM US Eastern Time).

* `High`: the highest price reached during the selected time interval.

* `Low`: the lowest price recorded during the same interval.

* `Close`: the final price of the stock at the end of the interval or market session.

* `Volume`: the total number of shares traded within that interval — a useful indicator of market interest or unusual activity.

* `Dividends`: if applicable, this field shows the dividend payout declared to shareholders on that day.

* `Stock Splits`: this field records events where a company's shares are split or consolidated (e.g., 2-for-1 split). These are rare but relevant structural changes in stock behavior.

**Note**: `Dividend` and `Stock Splits` values are often zero, as these events do not occur on a daily basis.

### Derived Indicators for Vendor Behavior

To evaluate the reliability of each vendor over time, the system calculates a set of behavioral indicators based on historical stock data. These indicators help detect signs of instability, risk, or unusual market activity.

Specifically, the agent computes the following indicators:

* **`Percent_Change`**: This metric calculates the percentage variation of the closing price compared to the previous interval. It measures the immediate volatility of the stock.

    $$ Percent\_Change_t = \left( \frac{Close_t - Close_{t-1}}{Close_{t-1}} \right) \times 100 $$

    Where:
  * $Close_t$: The closing price at the current time period $t$.
  * $Close_{t-1}$: The closing price at the previous time period $t-1$.

* **`Close_MA_3`**: This is the 3-period moving average of the closing price. It computes the average of closing prices over the last 3 periods, helping to smooth short-term fluctuations and identify general trends.

    $$ Close\_MA_t = \frac{Close_t + Close_{t-1} + Close_{t-2}}{3} $$

    Where:
  * $Close_t$: The closing price at the current time period $t$.
  * $Close_{t-1}$: The closing price at the previous time period $t-1$.
  * $Close_{t-2}$: The closing price at two time periods prior to $t$.

* **`Close_STD_3`**: This is the 3-period standard deviation of the closing price, measuring stock volatility over 3 periods. A high standard deviation indicates price instability.

    $$ Close\_STD_t = \sqrt{\frac{1}{3} \sum_{i=0}^{2} (Close_{t-i} - Close\_MA_t)^2} $$

    Where:
  * $Close_{t-i}$: The closing price at time period $t-i$.
  * $Close\_MA_t$: The moving average calculated for the current time period $t$.

* **`Volume_MA_3`**: This is the 3-period moving average of the trading volume. It calculates the average trading volume over the last 3 periods, useful for comparing current volume with recent behavior.

    $$ Volume\_MA_t = \frac{Volume_t + Volume_{t-1} + Volume_{t-2}}{3} $$

    Where:
  * $Volume_t$: The trading volume at the current time period $t$.
  * $Volume_{t-1}$: The trading volume at the previous time period $t-1$.
  * $Volume_{t-2}$: The trading volume at two time periods prior to $t$.

* **`Volume_Spike`**: This flag indicates the detection of anomalous volume spikes. A value of 1 signifies that the current volume is more than twice the recent average, potentially signaling extraordinary events or market turbulence.

    $$ Volume\_Spike_t = \begin{cases} 1 & \text{if } Volume_t > 2 \times Volume\_MA_t \\ 0 & \text{otherwise} \end{cases} $$

    Where:
  * $Volume_t$: The trading volume at the current time period $t$.
  * $Volume\_MA_t$: The moving average of the trading volume calculated for the current time period $t$.

* **`Down_Trend`**: This flag indicates a downward trend. A value of 1 means the stock closed lower than the previous period, useful for identifying moments of decline.

    $$ Down\_Trend_t = \begin{cases} 1 & \text{if } Close_t < Close_{t-1} \\ 0 & \text{otherwise} \end{cases} $$

    Where:
  * $Close_t$: The closing price at the current time period $t$.
  * $Close_{t-1}$: The closing price at the previous time period $t-1$.

* **`Consecutive_Drops`**: This indicator counts how many of the last 3 periods registered a price drop. More consecutive drops signal a potential deterioration of investor confidence.

    $$ Consecutive\_Drops_t = \sum_{i=0}^{2} Down\_Trend_{t-i} $$

    Where:
  * $Down\_Trend_{t-i}$: The `Down_Trend` indicator value at time period $t-i$.

### Trust Score Logic Calculation and Risk Interpretation

To quantify the overall reliability of each vendor, the system assigns a Trust Score on a scale from 0 to 10.
This score is calculated dynamically for each time interval (e.g., hourly or daily), based on the vendor's financial behavior over time.

The calculation starts from the maximum score of 10, and specific conditions trigger score reductions, based on risk indicators:

* If the price variation (`Percent Change`) exceeds ±1% compared to the previous period, **1 point** is subtracted. This kind of volatility may reflect instability, strong speculation, or sudden market reactions.

* If the price volatility (`Close_STD_3`) is greater than 3 — meaning the stock has fluctuated significantly over the past 3 periods — the score is penalized by **2 points**. High volatility is often a sign of market uncertainty or poor investor confidence.

* If a Volume Spike is detected — meaning the trading volume is more than twice the 3-period average — the system considers it an anomaly and subtracts **1 point**. This could indicate abnormal interest, speculative trades, or undisclosed information circulating in the market.

* If the stock price drops for 3 consecutive periods, the vendor is flagged for a possible negative trend, and the score is reduced by **2 points**. This suggests declining performance or reduced market trust.

At the end of this process, the final Trust Score reflects the vendor's current risk posture. The score is always bounded between **0 (worst)** and **10 (best)**.

The score is then interpreted as follows:

* **8 to 10**: The vendor is considered reliable and stable.

* **5 to 7**: The vendor shows some warning signals and should be monitored.

* **0 to 4**: The vendor is at risk and may require further evaluation or action.

In addition to per-interval scores, the system also computes an aggregated Trust Score, which represents the average score across the entire analysis period.
This value is plotted as a horizontal red line on each vendor's chart, making it easier to compare short-term changes against long-term performance.

## References

<a id="ref1"></a>
[1] Marino, Alberto (2024/2025). Design of an Integrated Operational Resilience Centre for Crisis Management in the Banking Sector. Master's Thesis, Politecnico di Torino.
