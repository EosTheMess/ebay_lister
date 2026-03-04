import os

pubspec_path = 'pubspec.yaml'

content = """
name: ebay_lister
description: A new Flutter project for eBay listing.
version: 1.0.1+1

environment:
  sdk: '>=3.2.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  # Stable versions for early 2026
  camera: ^0.11.0+4
  path_provider: ^2.1.2
  path: ^1.9.0
  device_info_plus: ^10.1.0
  cupertino_icons: ^1.0.6

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0

flutter:
  uses-material-design: true
"""

with open(pubspec_path, 'w') as f:
    f.write(content.strip())

print("✅ pubspec.yaml updated with stable camera: ^0.11.0+4")
