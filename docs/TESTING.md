# Testing Guide

## Local Validation

Run XML validation from the project root:

```bash
xmllint --noout \
  app/src/main/AndroidManifest.xml \
  app/src/main/res/layout/activity_main.xml \
  app/src/main/res/values/strings.xml \
  app/src/main/res/values/colors.xml \
  app/src/main/res/values/themes.xml \
  app/src/main/res/values-night/themes.xml
```

Run Android unit tests after Gradle dependencies are available:

```bash
GRADLE_USER_HOME=.gradle-user-home ./gradlew test
```

## Manual App Test

1. Launch Mwamba Vision Classifier on an Android device or emulator.
2. Tap **Take Picture** and capture a fruit image.
3. Confirm that the image preview appears and the app displays a class label.
4. Tap **Choose from Gallery** and select a fruit image.
5. Confirm that the result updates without crashing.

## Expected Labels

- Apple
- Banana
- Orange

## Known Environment Notes

The Gradle wrapper must download Gradle `7.0.2` on a fresh machine. If command-line testing fails before compilation, confirm network access and a compatible Android SDK/JDK setup.
