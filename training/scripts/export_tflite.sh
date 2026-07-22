#!/usr/bin/env bash
set -euo pipefail

PYTHONPATH=training/src python -m mwamba_vision.export_tflite \
  --model-path training/artifacts/best_model.keras \
  --output-path app/src/main/ml/model.tflite \
  --optimize
