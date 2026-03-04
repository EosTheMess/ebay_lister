import os

workflow_path = '.github/workflows/build.yml'
os.makedirs(os.path.dirname(workflow_path), exist_ok=True)

workflow_content = r'''
name: eBay Lister Build

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build_android:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Java 17
        uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'

      - name: Set up Flutter
        uses: subosito/flutter-action@v2
        with:
          channel: 'stable'

      - name: Install Dependencies
        run: flutter pub get

      - name: Build Android APK
        run: flutter build apk --release --build-number=${{ github.run_number }} --build-name=1.0.${{ github.run_number }}

      - name: Rename APK
        run: mv build/app/outputs/flutter-apk/app-release.apk build/app/outputs/flutter-apk/ebay-lister-v${{ github.run_number }}.apk

      - name: Upload Android Artifact
        uses: actions/upload-artifact@v4
        with:
          name: android-build
          path: build/app/outputs/flutter-apk/*.apk

  build_ios:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Flutter
        uses: subosito/flutter-action@v2
        with:
          channel: 'stable'

      - name: Hard Reset iOS Project
        run: |
          rm -rf ios
          flutter create --platforms ios .
          flutter pub get

      - name: Build iOS
        run: flutter build ios --release --no-codesign --build-number=${{ github.run_number }}

      - name: Upload iOS Artifact
        uses: actions/upload-artifact@v4
        with:
          name: ios-build
          path: build/ios/iphoneos/*.app
'''

with open(workflow_path, 'w') as f:
    f.write(workflow_content.strip())

print("✅ .github/workflows/build.yml rewritten with correct Flutter setup order.")
