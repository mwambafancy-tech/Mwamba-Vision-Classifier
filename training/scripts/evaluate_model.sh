#!/usr/bin/env bash
set -euo pipefail

DATA_DIR="${1:-training/data}"

PYTHONPATH=training/src python -m mwamba_vision.evaluate \
  --data-dir "$DATA_DIR" \
  --model-path training/artifacts/best_model.keras \
  --output-dir training/reports
