import os

# Create the full Android directory structure
dirs = [
    "android/app/src/main/kotlin/com/example/ebay_lister",
    "android/app/src/main/res/values",
    "android/gradle/wrapper"
]

for d in dirs:
    os.makedirs(d, exist_ok=True)

# 1. MainActivity.kt
with open("android/app/src/main/kotlin/com/example/ebay_lister/MainActivity.kt", "w") as f:
    f.write('''package com.example.ebay_lister
import io.flutter.embedding.android.FlutterActivity
class MainActivity: FlutterActivity() {}
''')

# 2. AndroidManifest.xml
with open("android/app/src/main/AndroidManifest.xml", "w") as f:
    f.write('''<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="com.example.ebay_lister">
    <uses-permission android:name="android.permission.CAMERA" />
    <application android:label="ebay_lister" android:icon="@mipmap/ic_launcher">
        <activity android:name=".MainActivity" android:exported="true" android:launchMode="singleTop"
            android:theme="@android:style/Theme.Black.NoTitleBar" android:configChanges="orientation|screenSize">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/><category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>
        <meta-data android:name="flutterEmbedding" android:value="2" />
    </application>
</manifest>''')

# 3. App-level build.gradle
with open("android/app/build.gradle", "w") as f:
    f.write('''plugins { id "com.android.application" }
android {
    namespace "com.example.ebay_lister"
    compileSdk 34
    defaultConfig { applicationId "com.example.ebay_lister"; minSdk 21; targetSdk 34; versionCode 1; versionName "1.0" }
}''')

# 4. Settings.gradle
with open("android/settings.gradle", "w") as f:
    f.write('include ":app"')

print("Fix applied. Now run: git add . && git commit -m 'Fix embedding' && git push")
