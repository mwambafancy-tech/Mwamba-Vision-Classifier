# Model Card

## Project

Mwamba Vision Classifier

## Owner

Mwamba Mutale

## Purpose

The app demonstrates on-device image classification using a bundled TensorFlow Lite model. It is designed as a compact Android portfolio project that classifies fruit images.

## Model File

```text
app/src/main/ml/model.tflite
```

## Input

- Image resized to `32 x 32` pixels.
- RGB channels.
- Float tensor input shaped as `1 x 32 x 32 x 3`.

## Output

The app maps the highest-confidence output index to:

- Apple
- Banana
- Orange

## Limitations

- The model is trained for a small fruit label set only.
- Predictions should not be treated as general object recognition.
- Image quality, lighting, angle, and background can affect results.

## Recommended Improvements

- Add a larger and more balanced training dataset.
- Add confidence percentages to the user interface.
- Add automated instrumentation tests on an emulator.
- Replace the launcher icon with a custom Mwamba Vision brand icon.
