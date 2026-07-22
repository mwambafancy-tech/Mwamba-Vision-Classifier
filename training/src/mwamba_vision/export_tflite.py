"""Export a trained Keras model to TensorFlow Lite for Android."""

from __future__ import annotations

import argparse
from pathlib import Path

import tensorflow as tf


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export Keras model to TensorFlow Lite.")
    parser.add_argument("--model-path", type=Path, default=Path("training/artifacts/best_model.keras"))
    parser.add_argument("--output-path", type=Path, default=Path("app/src/main/ml/model.tflite"))
    parser.add_argument("--optimize", action="store_true", help="Apply default TensorFlow Lite optimizations.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    model = tf.keras.models.load_model(args.model_path)
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    if args.optimize:
        converter.optimizations = [tf.lite.Optimize.DEFAULT]

    tflite_model = converter.convert()
    args.output_path.parent.mkdir(parents=True, exist_ok=True)
    args.output_path.write_bytes(tflite_model)
    print(f"Exported TensorFlow Lite model to {args.output_path}")


if __name__ == "__main__":
    main()
