# List of vendors to monitor.
# Each vendor is defined by its stock ticker and a readable name.
vendors = [
    {"ticker": "MSFT", "name": "Microsoft"},
    {"ticker": "IBM", "name": "IBM"},
    {"ticker": "ORCL", "name": "Oracle"},
    {"ticker": "NVDA", "name": "NVIDIA"},
    {"ticker": "GOOG", "name": "Google Cloud"}
]

# Time period for historical data to analyze (how far back to look).
# Examples: '7d' for 7 days, '30d' for 30 days, '365d' for 1 year
period = "365d"

# Data sampling frequency (granularity).
# '1h' means hourly data points; '1d' means daily
interval = "1h"

# Folder where output files (CSV, images, etc.) will be saved
output_dir = "monitoring"

