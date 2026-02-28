import os

# 1. Update settings.gradle (The "Brain" of the build)
settings_gradle = '''
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
    id "com.android.application" version "8.2.1" apply false
    id "org.jetbrains.kotlin.android" version "1.8.22" apply false
}

include ":app"
'''

# 2. Update app-level build.gradle (The "Body" of the build)
app_build_gradle = '''
plugins {
    id "com.android.application"
    id "org.jetbrains.kotlin.android"
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
'''

# Write the fixes
with open('android/settings.gradle', 'w') as f:
    f.write(settings_gradle)

with open('android/app/build.gradle', 'w') as f:
    f.write(app_build_gradle)

print("Gradle files synchronized for Flutter 3.41.2.")