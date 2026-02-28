import os
import shutil

# 1. Wipe the old, conflicting Android folder
if os.path.exists("android"):
    shutil.rmtree("android")

# 2. Recreate the structure
os.makedirs("android/app/src/main/kotlin/com/example/ebay_lister", exist_ok=True)
os.makedirs("android/gradle/wrapper", exist_ok=True)

# 3. settings.gradle (The main fix for the 'declarative' error)
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

# 4. App-level build.gradle (Updated for modern Flutter)
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

# 6. AndroidManifest.xml (Ensuring permissions are right)
with open("android/app/src/main/AndroidManifest.xml", "w") as f:
    f.write('''<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.CAMERA" />
    <application android:label="eBay Lister" android:icon="@mipmap/ic_launcher">
        <activity android:name="com.example.ebay_lister.MainActivity"
            android:exported="true"
            android:launchMode="singleTop"
            android:theme="@android:style/Theme.NoTitleBar"
            android:configChanges="orientation|screenSize"
            android:hardwareAccelerated="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>
    </application>
</manifest>''')

# 7. Dummy local.properties (GitHub Actions will overwrite this, but the script needs it locally)
with open("android/local.properties", "w") as f:
    f.write('flutter.sdk=/tmp/flutter')

print("Android files updated to modern declarative style. Pushing to GitHub...")