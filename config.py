# Allowed values based on Yahoo Finance documentation
ALLOWED_PERIODS = [ 
    "1d", "5d", "7d", "14d", "1mo", "3mo",
    "6mo", "1y", "2y", "5y", "10y", "ytd",
]

ALLOWED_INTERVALS = [
    "1m", "2m", "5m", "15m", "30m", "60m",
    "1h", "90m", "1d", "5d", "1wk", "1mo",
    "3mo",
]

# Parameters
period = "1y"
interval = "1d"
output_dir = "output"

# Vendors list example
vendors = [
    {"ticker": "MSFT", "name": "Microsoft"},
    {"ticker": "IBM", "name": "IBM"},
    {"ticker": "ORCL", "name": "Oracle"},
    {"ticker": "NVDA", "name": "NVIDIA"},
    {"ticker": "GOOG", "name": "Google Cloud"}
]

# Validation to enforce allowed period and interval values
if period not in ALLOWED_PERIODS:
    raise ValueError(
        f"Invalid period '{period}'. Allowed values are: {', '.join(ALLOWED_PERIODS)}"
    )

if interval not in ALLOWED_INTERVALS:
    raise ValueError(
        f"Invalid interval '{interval}'. Allowed values are: {', '.join(ALLOWED_INTERVALS)}"
    )
