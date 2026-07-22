"""Evaluate a trained Mwamba Vision model."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import tensorflow as tf

from .dataset import DatasetConfig, load_image_datasets
from .metrics import evaluate_predictions, save_confusion_matrix


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate image classification performance.")
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--model-path", type=Path, default=Path("training/artifacts/best_model.keras"))
    parser.add_argument("--output-dir", type=Path, default=Path("training/reports"))
    parser.add_argument("--image-size", type=int, default=32)
    parser.add_argument("--batch-size", type=int, default=32)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    _, val_ds, class_names = load_image_datasets(
        DatasetConfig(
            data_dir=args.data_dir,
            image_size=(args.image_size, args.image_size),
            batch_size=args.batch_size,
        )
    )

    model = tf.keras.models.load_model(args.model_path)
    y_true_batches = []
    y_pred_batches = []
    for images, labels in val_ds:
        predictions = model.predict(images, verbose=0)
        y_true_batches.append(np.argmax(labels.numpy(), axis=1))
        y_pred_batches.append(np.argmax(predictions, axis=1))

    y_true = np.concatenate(y_true_batches)
    y_pred = np.concatenate(y_pred_batches)
    report = evaluate_predictions(y_true, y_pred, class_names)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "classification_report.txt").write_text(report, encoding="utf-8")
    save_confusion_matrix(y_true, y_pred, class_names, args.output_dir / "confusion_matrix.png")
    print(report)


if __name__ == "__main__":
    main()
