#!/usr/bin/env bash
set -euo pipefail

DATA_DIR="${1:-training/data}"

PYTHONPATH=training/src python -m mwamba_vision.train \
  --data-dir "$DATA_DIR" \
  --model-type transfer \
  --image-size 32 \
  --batch-size 32 \
  --epochs 12 \
  --learning-rate 0.0005 \
  --output-dir training/artifacts
