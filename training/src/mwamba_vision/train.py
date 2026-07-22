"""Train Mwamba Vision Classifier models."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import tensorflow as tf

from .dataset import DatasetConfig, build_augmentation_layer, load_image_datasets, write_labels
from .models import build_custom_cnn, build_transfer_learning_model


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train an image classification model.")
    parser.add_argument("--data-dir", type=Path, required=True, help="Folder containing class-named image folders.")
    parser.add_argument("--output-dir", type=Path, default=Path("training/artifacts"), help="Where outputs are saved.")
    parser.add_argument("--model-type", choices=["cnn", "transfer"], default="cnn")
    parser.add_argument("--image-size", type=int, default=32)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--learning-rate", type=float, default=0.001)
    parser.add_argument("--validation-split", type=float, default=0.2)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    image_size = (args.image_size, args.image_size)
    config = DatasetConfig(
        data_dir=args.data_dir,
        image_size=image_size,
        batch_size=args.batch_size,
        validation_split=args.validation_split,
    )

    train_ds, val_ds, class_names = load_image_datasets(config)
    num_classes = len(class_names)

    if args.model_type == "transfer":
        model = build_transfer_learning_model(image_size, num_classes, args.learning_rate)
    else:
        model = build_custom_cnn(
            image_size,
            num_classes,
            args.learning_rate,
            augmentation=build_augmentation_layer(),
        )

    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_accuracy",
            patience=5,
            restore_best_weights=True,
        ),
        tf.keras.callbacks.ModelCheckpoint(
            filepath=args.output_dir / "best_model.keras",
            monitor="val_accuracy",
            save_best_only=True,
        ),
    ]

    args.output_dir.mkdir(parents=True, exist_ok=True)
    history = model.fit(train_ds, validation_data=val_ds, epochs=args.epochs, callbacks=callbacks)

    model.save(args.output_dir / "final_model.keras")
    write_labels(class_names, args.output_dir / "labels.txt")
    (args.output_dir / "history.json").write_text(json.dumps(history.history, indent=2), encoding="utf-8")
    print(f"Training complete. Saved outputs to {args.output_dir}")


if __name__ == "__main__":
    main()
