# AI Agent for TPRM (Third-Party Risk Management)

## Overview

This project implements an AI-based monitoring agent for assessing the reliability of third-party ICT vendors over time. The system is designed to support the IORC (Integrated Operational Resilience Centre) in financial institutions, with features aligned to regulatory frameworks like DORA.

The agent collects financial data, derives behavioral indicators, and computes a dynamic Trust Score (0–10) for each supplier. It also visualizes trends and flags suppliers that become potentially risky during long-term contracts.

## Getting Started

1. **Create and activate a virtual environment (recommended)**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On macOS/Linux
    ```

2. Install dependencies

    ```bash
    pip install -r requirements.txt
    ```

3. Run the script

    ```bash
    python monitor.py
    ```

4. Check the `monitoring/` folder

    You'll find:

    - `CSV` files with daily metrics and trust scores
    - `PNG` plots of trust score trends
    - `TXT` files with recent news headlines
