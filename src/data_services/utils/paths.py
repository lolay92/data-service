from pathlib import Path

# Output locations
OUTPUT_BASE_DIR = Path(__file__).resolve().parents[3]
OUTPUT_BASE_DIR = Path(OUTPUT_BASE_DIR, "out")
OUTPUT_METADATA = Path(OUTPUT_BASE_DIR, "metadata")
OUTPUT_ETF_OHLCV = Path(OUTPUT_BASE_DIR, "etf/ohlcv")
OUTPUT_CRYPTO = Path(OUTPUT_BASE_DIR, "crypto")

OUTPUT_BASE_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_METADATA.mkdir(parents=True, exist_ok=True)
OUTPUT_ETF_OHLCV.mkdir(parents=True, exist_ok=True)
