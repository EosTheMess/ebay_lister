import os

# 1. Update pubspec.yaml with 2026-compatible dependencies
pubspec_content = """
name: ebay_lister
description: A new Flutter project for eBay listing.
version: 1.0.1+1

environment:
  sdk: '>=3.2.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  camera: ^0.13.0
  path_provider: ^2.1.3
  path: ^1.9.1
  device_info_plus: ^10.1.0
  # Adding this to ensure the iOS build has the correct architecture hooks
  cupertino_icons: ^1.0.6

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0

flutter:
  uses-material-design: true
"""

with open('pubspec.yaml', 'w') as f:
    f.write(pubspec_content.strip())

# 2. Update the GitHub Workflow to "Auto-Repair" the iOS project
workflow_path = '.github/workflows/build.yml'
if os.path.exists(workflow_path):
    with open(workflow_path, 'r') as f:
        workflow = f.read()
    
    # We add a step to the build_ios job that deletes and regenerates the folder on the Mac
    repair_logic = """
      - name: Hard Reset iOS Project
        run: |
          rm -rf ios
          flutter create --platforms ios .
          flutter pub get
"""
    if 'Hard Reset iOS Project' not in workflow:
        workflow = workflow.replace('- uses: actions/checkout@v4', '- uses: actions/checkout@v4' + repair_logic)
    
    with open(workflow_path, 'w') as f:
        f.write(workflow)

print("✅ Dependencies updated and GitHub iOS 'Auto-Repair' enabled.")
