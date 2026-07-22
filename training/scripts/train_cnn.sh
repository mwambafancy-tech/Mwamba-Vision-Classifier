#!/usr/bin/env bash
set -euo pipefail

DATA_DIR="${1:-training/data}"

PYTHONPATH=training/src python -m mwamba_vision.train \
  --data-dir "$DATA_DIR" \
  --model-type cnn \
  --image-size 32 \
  --batch-size 32 \
  --epochs 20 \
  --output-dir training/artifacts
