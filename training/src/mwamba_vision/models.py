"""CNN and transfer-learning model definitions."""

from __future__ import annotations

from typing import Optional

import tensorflow as tf


def build_custom_cnn(
    image_size: tuple[int, int],
    num_classes: int,
    learning_rate: float = 0.001,
    augmentation: Optional[tf.keras.Model] = None,
) -> tf.keras.Model:
    """Build a compact CNN suitable for small fruit datasets."""
    inputs = tf.keras.Input(shape=(*image_size, 3), name="image")
    x = augmentation(inputs) if augmentation is not None else inputs
    x = tf.keras.layers.Rescaling(1.0 / 255, name="rescale")(x)

    for filters in (32, 64, 128):
        x = tf.keras.layers.Conv2D(filters, 3, padding="same", activation="relu")(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.MaxPooling2D()(x)

    x = tf.keras.layers.Dropout(0.25)(x)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dense(128, activation="relu")(x)
    x = tf.keras.layers.Dropout(0.35)(x)
    outputs = tf.keras.layers.Dense(num_classes, activation="softmax", name="class_probabilities")(x)

    model = tf.keras.Model(inputs, outputs, name="mwamba_custom_cnn")
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
        loss="categorical_crossentropy",
        metrics=["accuracy", tf.keras.metrics.Precision(name="precision"), tf.keras.metrics.Recall(name="recall")],
    )
    return model


def build_transfer_learning_model(
    image_size: tuple[int, int],
    num_classes: int,
    learning_rate: float = 0.0005,
    train_base: bool = False,
) -> tf.keras.Model:
    """Build a MobileNetV2 transfer-learning classifier."""
    inputs = tf.keras.Input(shape=(*image_size, 3), name="image")
    x = tf.keras.layers.Resizing(96, 96, name="mobilenet_resize")(inputs)
    x = tf.keras.applications.mobilenet_v2.preprocess_input(x)

    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(96, 96, 3),
        include_top=False,
        weights="imagenet",
    )
    base_model.trainable = train_base

    x = base_model(x, training=False)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dropout(0.3)(x)
    outputs = tf.keras.layers.Dense(num_classes, activation="softmax", name="class_probabilities")(x)

    model = tf.keras.Model(inputs, outputs, name="mwamba_transfer_mobilenetv2")
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
        loss="categorical_crossentropy",
        metrics=["accuracy", tf.keras.metrics.Precision(name="precision"), tf.keras.metrics.Recall(name="recall")],
    )
    return model
