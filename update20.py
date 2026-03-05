import os

file_path = 'android/app/build.gradle'

# The bulletproof 2026 app-level build.gradle
new_app_gradle = """plugins {
    id "com.android.application"
    id "org.jetbrains.kotlin.android"
    // This plugin is the one that fixes the 'io.flutter' unresolved reference
    id "dev.flutter.flutter-gradle-plugin"
}

android {
    namespace "com.example.ebay_lister"
    compileSdk 35

    sourceSets {
        main.java.srcDirs += 'src/main/kotlin'
    }

    defaultConfig {
        applicationId "com.example.ebay_lister"
        minSdk 21
        targetSdk 35
        versionCode flutterVersionCode.toInteger()
        versionName flutterVersionName
    }

    compileOptions {
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = '17'
    }

    buildTypes {
        release {
            signingConfig signingConfigs.debug
        }
    }
}

flutter {
    source '../..'
}

dependencies {
    // These are standard, the flutter-gradle-plugin handles the rest
    implementation "org.jetbrains.kotlin:kotlin-stdlib:2.1.0"
}
"""

if os.path.exists(file_path):
    with open(file_path, 'w') as f:
        f.write(new_app_gradle)
    print("✅ Fixed: android/app/build.gradle updated with correct Flutter plugin.")
else:
    print("❌ Error: android/app/build.gradle not found.")
