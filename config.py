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
period = "50d"

# Data sampling frequency (granularity)
interval = "1d"

# Folder where output files (CSV, images, etc.) will be saved
output_dir = "monitoring"

