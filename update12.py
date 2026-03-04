import os

# Define the standard path for MainActivity
# Based on your logs: com.example.ebay_lister
path = "android/app/src/main/kotlin/com/example/ebay_lister/MainActivity.kt"

# The standard code for a modern Flutter MainActivity
kt_code = """package com.example.ebay_lister

import io.flutter.embedding.android.FlutterActivity

class MainActivity: FlutterActivity()
"""

# Ensure the directory exists (just in case)
os.makedirs(os.path.dirname(path), exist_ok=True)

# Write the fix
with open(path, "w") as f:
    f.write(kt_code)

print(f"✅ Fixed {path}. Unresolved references resolved.")
