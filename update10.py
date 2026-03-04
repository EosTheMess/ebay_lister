import os
import re

file_path = 'android/app/build.gradle'

if os.path.exists(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    # 1. Update/Add compileOptions inside the android block
    compile_options = """    compileOptions {
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }"""

    if 'compileOptions' in content:
        content = re.sub(r'compileOptions\s*\{.*?\}', compile_options, content, flags=re.DOTALL)
    else:
        content = content.replace('android {', f'android {{\n{compile_options}')

    # 2. Append the Kotlin task configuration to the end of the file
    kotlin_task_fix = """
tasks.withType(org.jetbrains.kotlin.gradle.tasks.KotlinCompile).configureEach {
    kotlinOptions {
        jvmTarget = "17"
    }
}
"""
    # Remove old versions of this block if they exist to prevent duplicates
    content = re.sub(r'tasks\.withType\(org\.jetbrains\.kotlin\.gradle\.tasks\.KotlinCompile\).*?\{.*?\}', '', content, flags=re.DOTALL)
    content = content.strip() + "\n" + kotlin_task_fix

    with open(file_path, 'w') as f:
        f.write(content)

    print("✅ Fixed JVM target mismatch: Java and Kotlin now both set to 17.")
else:
    print("❌ Error: android/app/build.gradle not found.")
