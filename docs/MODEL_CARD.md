# Model Card

## Project

Mwamba Vision Classifier

## Owner

Mwamba Mutale

## Purpose

The app demonstrates on-device image classification using a bundled TensorFlow Lite model. The repository also includes a training pipeline for CNN training, transfer learning, preprocessing, dataset handling, evaluation metrics, and TensorFlow Lite export.

## Model File

```text
app/src/main/ml/model.tflite
```

## Input

- Image resized to `32 x 32` pixels.
- RGB channels.
- Float tensor input shaped as `1 x 32 x 32 x 3`.

## Training Options

- `mwamba_custom_cnn`: a compact CNN with convolution, batch normalization, pooling, dropout, and dense classification layers.
- `mwamba_transfer_mobilenetv2`: a MobileNetV2 transfer-learning classifier for stronger feature extraction.

## Dataset Handling

Training expects class-named folders:

```text
training/data/apple/
training/data/banana/
training/data/orange/
```

Images are resized, batched, cached, augmented, and prefetched using TensorFlow data pipelines.

## Output

The app maps the highest-confidence output index to:

- Apple
- Banana
- Orange

## Limitations

- The model is trained for a small fruit label set only.
- Predictions should not be treated as general object recognition.
- Image quality, lighting, angle, and background can affect results.
- The repository includes the pipeline, but a large production dataset is not bundled.

## Evaluation Metrics

The evaluation script produces:

- Accuracy
- Precision
- Recall
- F1-score
- Confusion matrix

## Recommended Improvements

- Add a larger and more balanced training dataset.
- Add confidence percentages to the user interface.
- Add automated instrumentation tests on an emulator.
- Replace the launcher icon with a custom Mwamba Vision brand icon.
