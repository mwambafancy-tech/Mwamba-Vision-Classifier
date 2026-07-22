# Training Pipeline

This folder contains the machine learning workflow for **Mwamba Vision Classifier** by **Mwamba Mutale**.

## What It Covers

- Custom CNN image classifier.
- MobileNetV2 transfer learning classifier.
- Dataset loading from class-named folders.
- Image resizing, batching, caching, augmentation, and prefetching.
- Evaluation with accuracy, precision, recall, F1-score, and confusion matrix.
- TensorFlow Lite export for Android deployment.

## Dataset Format

Place images in class folders:

```text
training/data/
  apple/
    image_001.jpg
  banana/
    image_001.jpg
  orange/
    image_001.jpg
```

The loader automatically builds labels from folder names and splits the data into training and validation sets.

## Install Dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r training/requirements.txt
```

## Train a Custom CNN

```bash
./training/scripts/train_cnn.sh training/data
```

## Train With Transfer Learning

```bash
./training/scripts/train_transfer_learning.sh training/data
```

## Evaluate

```bash
./training/scripts/evaluate_model.sh training/data
```

Evaluation outputs:

```text
training/reports/classification_report.txt
training/reports/confusion_matrix.png
```

## Export to Android

```bash
./training/scripts/export_tflite.sh
```

The exported model is written to:

```text
app/src/main/ml/model.tflite
```

## Notes

The repository does not include a large image dataset. Add your own images under `training/data/` before training.
