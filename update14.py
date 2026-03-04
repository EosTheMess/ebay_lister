import os

workflow_path = '.github/workflows/build.yml'

with open(workflow_path, 'r') as f:
    content = f.read()

# Add the 'flutter create' step specifically for the iOS job
repair_step = """
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
        with:
          channel: 'stable'
          architecture: ARM64

      # This is the "Magic Fix" - it recreates the iOS folder on a real Mac
      - name: Regenerate iOS Folder
        run: |
          rm -rf ios
          flutter create --platforms ios .
"""

# Inject the repair step into the build_ios job
if 'name: Regenerate iOS Folder' not in content:
    content = content.replace('- uses: actions/checkout@v4', repair_step, 1) # Note: Be careful with which checkout it replaces

with open(workflow_path, 'w') as f:
    f.write(content)

print("✅ Workflow updated: GitHub will now self-repair the iOS project.")
