import os
import shutil

# 1. Clean up the old structure
if os.path.exists("android"):
    shutil.rmtree("android")

# 2. Define the exact modern structure
folders = [
    "android/app/src/main/kotlin/com/example/ebay_lister",
    "android/app/src/main/res/drawable",
    "android/app/src/main/res/values",
    "android/gradle/wrapper"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

# 3. Create MainActivity.kt
with open("android/app/src/main/kotlin/com/example/ebay_lister/MainActivity.kt", "w") as f:
    f.write('package com.example.ebay_lister\nimport io.flutter.embedding.android.FlutterActivity\nclass MainActivity: FlutterActivity() {}')

# 4. Create a robust AndroidManifest.xml
with open("android/app/src/main/AndroidManifest.xml", "w") as f:
    f.write('''<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.CAMERA" />
    <application android:label="ebay_lister" android:icon="@mipmap/ic_launcher">
        <activity android:name="com.example.ebay_lister.MainActivity"
            android:exported="true"
            android:launchMode="singleTop"
            android:theme="@android:style/Theme.Translucent.NoTitleBar"
            android:configChanges="orientation|keyboardHidden|keyboard|screenSize|locale|layoutDirection|fontScale|screenLayout|density|uiMode"
            android:hardwareAccelerated="true"
            android:windowSoftInputMode="adjustResize">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/><category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>
        <meta-data android:name="flutterEmbedding" android:value="2" />
    </application>
</manifest>''')

# 5. Create the App-level build.gradle
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
}''')

# 6. Create the Project-level build.gradle
with open("android/build.gradle", "w") as f:
    f.write('''
allprojects {
    repositories {
        google()
        mavenCentral()
    }
}
rootProject.buildDir = '../build'
subprojects {
    project.buildDir = "${rootProject.buildDir}/${project.name}"
}
subprojects {
    project.evaluationDependsOn(':app')
}''')

# 7. Create settings.gradle
with open("android/settings.gradle", "w") as f:
    f.write('''
include ":app"
def localPropertiesFile = new File(rootProject.projectDir, "local.properties")
def properties = new Properties()
assert localPropertiesFile.exists()
localPropertiesFile.withReader("UTF-8") { reader -> properties.load(reader) }
def flutterSdkPath = properties.getProperty("flutter.sdk")
assert flutterSdkPath != null, "flutter.sdk not set in local.properties"
apply from: "$flutterSdkPath/packages/flutter_tools/gradle/app_plugin_loader.gradle"
''')

print("Structure rebuilt. Ready to push.")