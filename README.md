# Mwamba Vision Classifier

Mwamba Vision Classifier is a computer vision and Android image classification project built by **Mwamba Mutale**. It includes an Android TensorFlow Lite app plus a Python training pipeline for CNNs, transfer learning, preprocessing, dataset handling, model evaluation, and TensorFlow Lite export.

## Features

- Capture an image with the device camera.
- Select an image from the device gallery.
- Run on-device inference with TensorFlow Lite.
- Display the predicted class instantly.
- Clean mobile interface branded for Mwamba Mutale.
- Train a custom CNN from class-named image folders.
- Train a MobileNetV2 transfer-learning model.
- Evaluate with accuracy, precision, recall, F1-score, and confusion matrix.
- Export trained models to Android-ready TensorFlow Lite format.

## Model

The bundled model is stored at:

```text
app/src/main/ml/model.tflite
```

Current class labels:

```text
Apple
Banana
Orange
```

The app resizes input images to `32 x 32` pixels before passing them into the model.

## Tech Stack

- Java
- Android SDK
- Python
- TensorFlow / Keras
- TensorFlow Lite
- TensorFlow Lite Support Library
- scikit-learn
- Matplotlib
- Gradle

## Machine Learning Pipeline

The training workflow lives in:

```text
training/
```

It supports:

- Dataset loading from folders such as `training/data/apple`, `training/data/banana`, and `training/data/orange`.
- Image preprocessing with resizing, batching, caching, augmentation, and prefetching.
- Custom CNN training.
- MobileNetV2 transfer learning.
- Evaluation reports with classification metrics and confusion matrix.
- Export to `app/src/main/ml/model.tflite`.

Training docs:

```text
training/README.md
docs/MODEL_CARD.md
docs/TESTING.md
```

## Run Locally

1. Open the project in Android Studio.
2. Let Android Studio sync Gradle dependencies.
3. Connect an Android device or start an emulator.
4. Run the `app` configuration.

Command-line test run:

```bash
GRADLE_USER_HOME=.gradle-user-home ./gradlew test
```

## Project Structure

```text
app/src/main/java/                 Android application code
app/src/main/ml/model.tflite       TensorFlow Lite model
app/src/main/res/layout/           Mobile UI layouts
app/src/main/res/values/           App strings, colors, and themes
training/src/mwamba_vision/        CNN, transfer learning, preprocessing, and metrics code
training/scripts/                  Training, evaluation, and export commands
training/configs/                  Example model configuration
```

## Credits

Designed and customized by **Mwamba Mutale**.

This repository retains its upstream open-source license metadata where required.
