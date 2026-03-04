#!/bin/bash

# 1. Backup current pubspec
cp pubspec.yaml pubspec.yaml.bak

# 2. Overwrite pubspec.yaml with the optimized configuration
cat <<EOF > pubspec.yaml
name: ebay_lister
publish_to: 'none'
version: 1.0.0+1

environment:
  sdk: '>=3.2.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  camera: ^0.12.0
  path_provider: ^2.1.5
  path: ^1.9.0
  shared_preferences: ^2.3.0

flutter:
  uses-material-design: true

dependency_overrides:
  meta: 1.18.1
  win32: 6.0.0
  win32_registry: 3.0.2
  matcher: 0.12.19
  test_api: 0.7.10
EOF

# 3. Clean and Update
echo "Applying overrides..."
flutter pub get
