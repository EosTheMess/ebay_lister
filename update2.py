import os
import shutil

# 1. Nuclear option: Delete the old android folder using Python
if os.path.exists("android"):
    print("Deleting old android folder...")
    shutil.rmtree("android")

# 2. Create the exact modern folder hierarchy
folders = [
    "android/app/src/main/kotlin/com/example/ebay_lister",
    "android/app/src/main/res/values",
    "android/gradle/wrapper"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

# 3. settings.gradle (The critical fix for modern Flutter)
with open("android/settings.gradle", "w") as f:
    f.write('''
pluginManagement {
    def flutterSdkPath = {
        def properties = new Properties()
        file("local.properties").withInputStream { properties.load(it) }
        def flutterSdkPath = properties.getProperty("flutter.sdk")
        assert flutterSdkPath != null, "flutter.sdk not set in local.properties"
        return flutterSdkPath
    }()
    includeBuild("$flutterSdkPath/packages/flutter_tools/gradle")
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
plugins {
    id "dev.flutter.flutter-gradle-plugin" version "1.0.0" apply false
}
include ":app"
''')

# 4. App-level build.gradle
with open("android/app/build.gradle", "w") as f:
    f.write('''
plugins {
    id "com.android.application"
    id "kotlin-android"
    id "dev.flutter.flutter-gradle-plugin"
}
android {
    namespace "com.example.ebay_lister"
    compileSdk 34
    defaultConfig {
        applicationId "com.example.ebay_lister"
        minSdk 21
        targetSdk 34
        versionCode 1
        versionName "1.0"
    }
    buildTypes {
        release {
            signingConfig signingConfigs.debug
        }
    }
}
''')

# 5. MainActivity.kt
with open("android/app/src/main/kotlin/com/example/ebay_lister/MainActivity.kt", "w") as f:
    f.write('''package com.example.ebay_lister
import io.flutter.embedding.android.FlutterActivity
class MainActivity: FlutterActivity() {}
''')

# 6. AndroidManifest.xml
with open("android/app/src/main/AndroidManifest.xml", "w") as f:
    f.write('''<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.CAMERA" />
    <application android:label="eBay Lister">
        <activity android:name=".MainActivity"
            android:exported="true"
            android:launchMode="singleTop"
            android:theme="@android:style/Theme.NoTitleBar"
            android:configChanges="orientation|screenSize">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>
        <meta-data android:name="flutterEmbedding" android:value="2" />
    </application>
</manifest>''')

# 7. Local.properties (Crucial for the build scripts above to work)
with open("android/local.properties", "w") as f:
    f.write('flutter.sdk=/opt/flutter\\n')

print("Rebuild complete. Now push these changes to GitHub.")