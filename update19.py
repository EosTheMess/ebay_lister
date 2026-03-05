import os

workflow_path = '.github/workflows/build.yml'

workflow_content = r'''
name: eBay Lister Production Build

on:
  push:
    branches: [ main ]

jobs:
  build_android:
    name: Build Android Release
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

      - name: Get Dependencies
        run: flutter pub get

      - name: Build Full APK
        # This creates a single, universal release APK
        run: flutter build apk --release --build-number=${{ github.run_number }} --target-platform android-arm64

      - name: Archive Android APK
        uses: actions/upload-artifact@v4
        with:
          name: ebay-lister-android-v${{ github.run_number }}
          path: build/app/outputs/flutter-apk/app-release.apk

  build_ios:
    name: Build iOS Release
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

      - name: Build iOS App
        run: flutter build ios --release --no-codesign --build-number=${{ github.run_number }}

      - name: Create Flashable IPA
        # This converts the .app folder into a .ipa file for Sideloadly/AltStore
        run: |
          mkdir -p Payload
          mv build/ios/iphoneos/Runner.app Payload/
          zip -r ebay-lister-ios-v${{ github.run_number }}.ipa Payload

      - name: Archive iOS IPA
        uses: actions/upload-artifact@v4
        with:
          name: ebay-lister-ios-v${{ github.run_number }}
          path: "*.ipa"
'''

with open(workflow_path, 'w') as f:
    f.write(workflow_content.strip())

print("✅ Production workflow updated. GitHub will now produce full .apk and .ipa files.")
