"""Computer vision evaluation metrics."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix


def evaluate_predictions(y_true: np.ndarray, y_pred: np.ndarray, class_names: list[str]) -> str:
    """Return precision, recall, F1-score, and support per class."""
    return classification_report(y_true, y_pred, target_names=class_names, digits=4)


def save_confusion_matrix(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    class_names: list[str],
    output_path: Path,
) -> None:
    """Save a confusion matrix plot for model evaluation."""
    matrix = confusion_matrix(y_true, y_pred)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(7, 6))
    im = ax.imshow(matrix, interpolation="nearest", cmap="Greens")
    ax.figure.colorbar(im, ax=ax)
    ax.set(
        xticks=np.arange(len(class_names)),
        yticks=np.arange(len(class_names)),
        xticklabels=class_names,
        yticklabels=class_names,
        ylabel="True label",
        xlabel="Predicted label",
        title="Mwamba Vision Confusion Matrix",
    )
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    threshold = matrix.max() / 2 if matrix.size else 0
    for row in range(matrix.shape[0]):
        for col in range(matrix.shape[1]):
            color = "white" if matrix[row, col] > threshold else "black"
            ax.text(col, row, matrix[row, col], ha="center", va="center", color=color)

    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)
