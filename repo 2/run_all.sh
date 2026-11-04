#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 src/01_build_database.py
python3 src/02_analysis.py > /dev/null
python3 src/03_charts.py
python3 src/04_validate.py | head -1
