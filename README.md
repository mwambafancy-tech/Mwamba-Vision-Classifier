# Mwamba Vision Classifier

Mwamba Vision Classifier is an Android image classification app built by **Mwamba Mutale**. It uses a custom TensorFlow Lite model to classify selected or captured images into fruit categories.

## Features

- Capture an image with the device camera.
- Select an image from the device gallery.
- Run on-device inference with TensorFlow Lite.
- Display the predicted class instantly.
- Clean mobile interface branded for Mwamba Mutale.

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
- TensorFlow Lite
- TensorFlow Lite Support Library
- Gradle

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
```

## Credits

Designed and customized by **Mwamba Mutale**.

This repository retains its upstream open-source license metadata where required.
