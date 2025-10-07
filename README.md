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

# AI Agent for TPRM (Third-Party Risk Management)

## Overview

This project presents an AI-based monitoring agent designed to evaluate the reliability of third-party ICT service providers over time. Developed as part of a thesis focusing on operational resilience in the banking sector, this tool aims to support the strategic activities of an **Integrated Operational Resilience Centre (IORC)** within financial institutions. It offers a data-driven approach to continuously track the operational soundness of external vendors, aligning with modern regulatory expectations.

### Understanding the Integrated Operational Resilience Centre (IORC)

In the contemporary financial landscape, characterized by rapid digitalization, globalized supply chains, and increasing interdependencies, organizations face significant challenges in maintaining operational continuity and responding effectively to crises. The **Integrated Operational Resilience Centre (IORC)** is introduced as a conceptual framework designed to address these challenges, particularly within the banking sector.

Inspired by NATO's Consultation, Command and Control (C3) Taxonomy, the IORC functions as a multi-layered hub for governance, monitoring, decision-making, and crisis communication. Its primary goal is to enable rapid and informed interventions by integrating organizational and situational data. Key features of the IORC include [1]:

* **Multi-layered Architecture**: Structured across six levels, covering governance, core services, communication, processes, roles, and user-facing applications.
* **Data-driven Awareness**: Leverages data to enhance situational awareness, detect anomalies, and guide crisis management decisions.
* **AI and Digital Twin Integration**: Incorporates Artificial Intelligence for observability, predictive analysis, and anomaly detection, alongside Digital Twins for infrastructure replication, impact assessment, and stress testing. This enables continuous validation and learning.
* **Regulatory Alignment**: Designed to be in line with regulations such as the EU’s Digital Operational Resilience Act (DORA), emphasizing oversight of critical ICT providers and promoting accountability and traceability.

In essence, the IORC is not a rigid solution but a flexible, modular, and scalable reference architecture that transforms resilience into a dynamic and measurable capability, crucial for strengthening stability and accelerating recovery in the financial ecosystem.

### Project Contribution to IORC

This AI agent specifically contributes to the IORC's capabilities by providing a robust Third-Party Risk Management (TPRM) monitoring solution. It addresses the critical need for ongoing risk assessments and third-party oversight, as mandated by regulations like DORA. By integrating this monitoring tool into existing operational workflows, the IORC can better anticipate disruptions, comply with audit requirements, and enhance overall resilience against ICT-related vulnerabilities stemming from external dependencies.

## How the Agent Works

The system relies on financial market data as a proxy for vendor health and stability. For each selected supplier, it collects stock price information from Yahoo Finance, analyzes short-term behavioral patterns, and derives custom indicators such as price volatility, volume anomalies, and trend persistence. These indicators are then combined to calculate a dynamic **Trust Score** on a scale from 0 to 10, which reflects the vendor’s level of risk or reliability at any given time.

The Trust Score is recalculated at regular intervals (hourly or daily), depending on the configuration, and is visualized through automated charts and summary reports. In addition to individual trend analysis, the system provides an aggregate score for each vendor over the entire monitoring period. This allows the institution to detect emerging risks early, assess whether a vendor’s performance is deteriorating over time, and make more informed decisions regarding long-term contracts or critical service dependencies.

## Project Structure and File Overview

Here’s a quick guide to the main files included in this project:

* `monitor.py`: The main script containing the logic for retrieving financial data, calculating indicators and Trust Scores, generating plots, and saving outputs for each vendor.
* `config.py`: Allows configuration of the tool, including defining vendors to monitor, historical data collection parameters (`period`, `interval`), and output save locations.
* `requirements.txt`: Lists all the required Python packages.
* `monitoring/`: This directory is automatically created upon execution and will contain CSV files with financial data and computed scores, trend plots for each vendor, and logs with aggregated Trust Scores.

Before launching the tool, ensure to check and customize the vendor list and parameters inside `config.py` to match your monitoring needs.

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

    * `.csv` files with daily metrics and trust scores;
    * `.png` plots of trust score trends;
    * `.txt` file with aggregated trust score value.

5. **Deactivate the virtual environment**

    ```bash
    deactivate
    ```

## Configuration Options

### Vendors to Monitor

The agent is designed to work with publicly listed ICT providers whose financial data is available through platforms like Yahoo Finance. Below are examples of vendors you can include in the configuration:

* **Cloud and Infrastructure Providers**

    | Company             | Ticker | Description                                |
    | :------------------ | :----- | :----------------------------------------- |
    | Microsoft           | MSFT   | Azure, Office 365, enterprise platforms    |
    | Amazon Web Services | AMZN   | Cloud infrastructure and computing         |
    | Google Cloud        | GOOG   | Google Cloud Platform, Workspace tools     |
    | Oracle              | ORCL   | Databases, business software, Oracle Cloud |
    | IBM                 | IBM    | Hybrid cloud, AI, legacy systems           |

* **Cybersecurity and Identity Management**

    | Company             | Ticker | Description                                |
    | :------------------ | :----- | :----------------------------------------- |
    | Palo Alto Networks  | PANW   | Advanced threat protection                 |
    | Fortinet            | FTNT   | Network firewalls, endpoint security       |
    | CrowdStrike         | CRWD   | Threat intelligence, endpoint detection    |
    | Okta                | OKTA   | Identity and access management             |

* **Software, Platforms, and IT Operations**

    | Company             | Ticker | Description                                |
    | :------------------ | :----- | :----------------------------------------- |
    | NVIDIA              | NVDA   | AI hardware, GPUs, cloud data centers      |
    | Cisco Systems       | CSCO   | Networking, security, infrastructure       |
    | ServiceNow          | NOW    | IT service management, workflows           |
    | Salesforce          | CRM    | CRM, analytics, SaaS platforms             |
    | Atlassian           | TEAM   | Jira, Confluence, cloud development tools  |
    | Adobe               | ADBE   | Creative and document cloud platforms      |
    | HP Enterprise       | HPE    | Hybrid IT, edge-to-cloud infrastructure    |
    | Dell Technologies   | DELL   | Servers, storage, enterprise solutions     |

    **Note**: You can include any of these vendors in your `config.py` file by adding their stock ticker and name. Ensure the ticker is valid on Yahoo Finance.

### `period` and `interval` parameters

The `period` and `interval` parameters define how much historical data is collected and how frequently data points are sampled. These values follow [(Python) Yahoo Finance API](https://pypi.org/project/yfinance/) limitations.

* `period` (How far back to fetch data)

    | Value    | Description                          |
    | :------- | :----------------------------------- |
    | `1d`     | 1 day                                |
    | `5d`     | 5 days                               |
    | `7d`     | 7 days                               |
    | `14d`    | 14 days                              |
    | `1mo`    | 1 month                              |
    | `3mo`    | 3 months                             |\n    | `6mo`    | 6 months                             |
    | `1y`     | 1 year                               |
    | `2y`     | 2 years                              |
    | `5y`     | 5 years                              |
    | `10y`    | 10 years                             |
    | `ytd`    | Year-to-date (from Jan 1st)          |
    | `max`    | Full historical data                 |

    **Note**: If you use `interval="1h"` (hourly data), the maximum allowed period is `730d` (2 years).

* `interval` (Sampling frequency)

    | Value     | Description                         |
    | :-------- | :---------------------------------- |
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

* `Open`: The price at which the stock began trading at the start of the market session (typically at 09:30 AM US Eastern Time).
* `High`: The highest price reached during the selected time interval.
* `Low`: The lowest price recorded during the same interval.
* `Close`: The final price of the stock at the end of the interval or market session.
* `Volume`: The total number of shares traded within that interval — a useful indicator of market interest or unusual activity.
* `Dividends`: If applicable, this field shows the dividend payout declared to shareholders on that day.
* `Stock Splits`: This field records events where a company's shares are split or consolidated (e.g., 2-for-1 split). These are rare but relevant structural changes in stock behavior.

**Note**: `Dividend` and `Stock Splits` values are often zero, as these events do not occur on a daily basis.

### Derived Indicators for Vendor Behavior

To evaluate the reliability of each vendor over time, the system calculates a set of behavioral indicators based on historical stock data. These indicators help detect signs of instability, risk, or unusual market activity.

Specifically, the agent computes the following indicators:

* **`Percent_Change`**: This metric captures how much the closing price (`Close_t`) has changed compared to the previous interval (`Close_{t-1}`). It measures the immediate volatility of the stock. Sudden large variations — for example, a spike or drop greater than ±1% — may signal news events or abnormal market behavior.

* **`Close_MA_3`**: This is the moving average of the closing price over the last 3 time periods. It computes the average of the current closing price (`Close_t`), the previous closing price (`Close_{t-1}`), and the closing price from two periods prior (`Close_{t-2}`). It serves to smooth out short-term fluctuations and highlight the general trend of the stock.

* **`Close_STD_3`**: The standard deviation of the closing price over the last 3 periods. This measures the stock volatility, where higher values indicate greater uncertainty or risk. It is calculated based on the closing prices (`Close_{t-i}`) and the moving average (`Close_MA_t`) over the last three periods.

* **`Volume_MA_3`**: This is the 3-period moving average of the trading volume. It calculates the average of the current trading volume (`Volume_t`), the previous trading volume (`Volume_{t-1}`), and the trading volume from two periods prior (`Volume_{t-2}`). This is useful for comparing current volume with recent behavior.

* **`Volume_Spike`**: This flag indicates the detection of anomalous volume spikes. A spike is flagged (value of 1) if the current trading volume (`Volume_t`) exceeds twice the 3-period moving average of the trading volume (`Volume_MA_t`). Otherwise, the value is 0. This may suggest abnormal interest in the stock — potentially due to insider activity, speculative moves, or unexpected news.

* **`Down_Trend`**: This flag indicates a downward trend. A value of 1 means the stock's current closing price (`Close_t`) is lower than its previous closing price (`Close_{t-1}`). Otherwise, the value is 0. This is useful to identify moments of decline.

* **`Consecutive_Drops`**: This indicator counts how many of the last 3 periods registered a price drop. It sums the `Down_Trend` indicator values (`Down_Trend_{t-i}`) over the last three periods. More consecutive drops signal a potential deterioration of investor confidence.

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
