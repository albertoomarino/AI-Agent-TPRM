# List of vendors to monitor
# Each vendor is defined by its stock ticker and a readable name
vendors = [
    {"ticker": "MSFT", "name": "Microsoft"},
    {"ticker": "IBM", "name": "IBM"},
    {"ticker": "ORCL", "name": "Oracle"},
    {"ticker": "NVDA", "name": "NVIDIA"},
    {"ticker": "GOOG", "name": "Google Cloud"}
]

# Time period for historical data to analyze (how far back to look)
# Possible values: 1d, 5d, 7d, 14d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd
period = "1y"

# Data sampling frequency (granularity)
# Possible values: 1m, 2m, 5m, 15m, 30m, 60m, 1h, 90m, 1d, 5d, 1wk, 1mo, 3mo
interval = "1d"

# Folder where output files (CSV, images, etc.) will be saved
output_dir = "monitoring"
