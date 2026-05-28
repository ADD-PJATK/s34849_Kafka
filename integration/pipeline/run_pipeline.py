#!/usr/bin/env python3
"""
Integration pipeline: load fixture ticks -> write raw CSV -> run anonymizer -> out/pipeline_output.csv
"""

import csv
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
FIXTURES = REPO_ROOT / "mock" / "fixtures" / "ticks.json"
MAPPING = Path(__file__).resolve().parent / "mapping.json"
OUT_DIR = REPO_ROOT / "out"
TEMP_CSV = OUT_DIR / "raw_export.csv"
OUT_FILE = OUT_DIR / "pipeline_output.csv"
ANONYMIZER = REPO_ROOT / "anonymizer" / "anonymize.py"

FIELDS = ["ticker", "lastPrice", "volume", "trader_email", "operator_name", "comment", "timestamp"]


def main():
    OUT_DIR.mkdir(exist_ok=True)

    with open(FIXTURES, encoding="utf-8") as f:
        ticks = json.load(f)

    with open(TEMP_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(ticks)

    result = subprocess.run(
        [sys.executable, str(ANONYMIZER),
         "--mapping", str(MAPPING),
         "--input", str(TEMP_CSV),
         "--output", str(OUT_FILE)],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"Anonymizer error:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

    print(result.stdout.strip())
    print(f"Raw CSV : {TEMP_CSV}")
    print(f"Anonymized: {OUT_FILE}")


if __name__ == "__main__":
    main()
