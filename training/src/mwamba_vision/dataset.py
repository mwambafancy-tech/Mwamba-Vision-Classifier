"""Dataset loading and image preprocessing helpers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import tensorflow as tf


@dataclass(frozen=True)
class DatasetConfig:
    data_dir: Path
    image_size: tuple[int, int] = (32, 32)
    batch_size: int = 32
    validation_split: float = 0.2
    seed: int = 42


def load_image_datasets(config: DatasetConfig) -> tuple[tf.data.Dataset, tf.data.Dataset, list[str]]:
    """Load train/validation datasets from class-named folders.

    Expected folder format:

    data/
      apple/
      banana/
      orange/
    """
    train_ds = tf.keras.utils.image_dataset_from_directory(
        config.data_dir,
        validation_split=config.validation_split,
        subset="training",
        seed=config.seed,
        image_size=config.image_size,
        batch_size=config.batch_size,
        label_mode="categorical",
    )
    val_ds = tf.keras.utils.image_dataset_from_directory(
        config.data_dir,
        validation_split=config.validation_split,
        subset="validation",
        seed=config.seed,
        image_size=config.image_size,
        batch_size=config.batch_size,
        label_mode="categorical",
    )

    class_names = list(train_ds.class_names)
    autotune = tf.data.AUTOTUNE
    train_ds = train_ds.cache().shuffle(1000, seed=config.seed).prefetch(autotune)
    val_ds = val_ds.cache().prefetch(autotune)
    return train_ds, val_ds, class_names


def build_augmentation_layer() -> tf.keras.Sequential:
    """Create image augmentation for more robust computer vision training."""
    return tf.keras.Sequential(
        [
            tf.keras.layers.RandomFlip("horizontal"),
            tf.keras.layers.RandomRotation(0.08),
            tf.keras.layers.RandomZoom(0.12),
            tf.keras.layers.RandomContrast(0.1),
        ],
        name="image_augmentation",
    )


def write_labels(class_names: Iterable[str], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(class_names) + "\n", encoding="utf-8")
