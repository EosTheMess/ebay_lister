import os
import re

def update_version(new_version):
    # 1. Update pubspec.yaml
    if os.path.exists('pubspec.yaml'):
        with open('pubspec.yaml', 'r') as f:
            lines = f.readlines()
        with open('pubspec.yaml', 'w') as f:
            for line in lines:
                if line.startswith('version:'):
                    f.write(f'version: {new_version}\n')
                else:
                    f.write(line)
        print(f"✅ Updated pubspec.yaml to {new_version}")

    # 2. Update Android build.gradle (Ensure placeholders exist)
    gradle_path = 'android/app/build.gradle'
    if os.path.exists(gradle_path):
        with open(gradle_path, 'r') as f:
            content = f.read()
        
        # Replace hardcoded values with Flutter environment variables
        content = re.sub(r'versionCode\s+\d+', 'versionCode flutterVersionCode.toInteger()', content)
        content = re.sub(r'versionName\s+".*?"', 'versionName flutterVersionName', content)
        
        with open(gradle_path, 'w') as f:
            f.write(content)
        print("✅ Android Gradle configured to sync with pubspec")

    # 3. Update iOS Info.plist (Ensure placeholders exist)
    plist_path = 'ios/Runner/Info.plist'
    if os.path.exists(plist_path):
        with open(plist_path, 'r') as f:
            content = f.read()
        
        # Ensure Build Name and Build Number use Flutter variables
        # Look for CFBundleShortVersionString and CFBundleVersion
        content = re.sub(r'<key>CFBundleShortVersionString</key>\s*<string>.*?</string>', 
                         '<key>CFBundleShortVersionString</key>\\n\\t<string>$(FLUTTER_BUILD_NAME)</string>', content)
        content = re.sub(r'<key>CFBundleVersion</key>\s*<string>.*?</string>', 
                         '<key>CFBundleVersion</key>\\n\\t<string>$(FLUTTER_BUILD_NUMBER)</string>', content)
        
        with open(plist_path, 'w') as f:
            f.write(content)
        print("✅ iOS Info.plist configured to sync with pubspec")

if __name__ == "__main__":
    version = input("Enter new version (e.g., 1.0.5+5): ")
    if '+' in version:
        update_version(version)
    else:
        print("❌ Error: Version must include a '+' (e.g., 1.2.0+4)")