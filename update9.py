import os

gradle_path = 'android/app/build.gradle'

if os.path.exists(gradle_path):
    with open(gradle_path, 'r') as f:
        content = f.read()

    # 1. Update the compileOptions to Java 17
    # 2. Update the kotlinOptions to Java 17
    
    new_java_block = """
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = '17'
    }
    """
    
    # This regex-free replacement is safer for standard Flutter templates
    import re
    
    # Replace the old blocks if they exist, or add them to the 'android' block
    content = re.sub(r'compileOptions\s*{.*?}', new_java_block, content, flags=re.DOTALL)
    
    # If the replacement didn't happen (because the block was missing), 
    # we inject it into the 'android' section
    if 'compileOptions' not in content:
        content = content.replace('android {', f'android {{{new_java_block}')

    with open(gradle_path, 'w') as f:
        f.write(content)

    print("✅ Java and Kotlin targets synced to Version 17.")
else:
    print("❌ Could not find android/app/build.gradle")