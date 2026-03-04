import os
import re

file_path = 'android/settings.gradle'

if os.path.exists(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    # 1. Update Android Application Plugin version to 8.6.0
    content = re.sub(
        r'id "com.android.application" version ".*?"', 
        'id "com.android.application" version "8.6.0"', 
        content
    )

    # 2. Update Kotlin Android Plugin version to 2.1.0
    content = re.sub(
        r'id "org.jetbrains.kotlin.android" version ".*?"', 
        'id "org.jetbrains.kotlin.android" version "2.1.0"', 
        content
    )

    with open(file_path, 'w') as f:
        f.write(content)

    print("✅ Updated AGP to 8.6.0 and Kotlin to 2.1.0 in settings.gradle")
else:
    print("❌ Error: android/settings.gradle not found.")
