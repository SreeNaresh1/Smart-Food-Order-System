"""
Test Script: Verify Customer Dashboard Ultra-Vibrant Features
This script checks if the dashboard file has all ultra-vibrant features.
"""

import os

# Path to customer dashboard
dashboard_path = "templates/dashboards/customer.html"

print("=" * 70)
print("🔍 TESTING CUSTOMER DASHBOARD ULTRA-VIBRANT FEATURES")
print("=" * 70)
print()

# Check if file exists
if not os.path.exists(dashboard_path):
    print("❌ ERROR: Dashboard file not found!")
    exit(1)

# Read the file
with open(dashboard_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Features to check
features = {
    "Rainbow Gradient Background": "gradientFlow",
    "Animated Background": "animation: gradientFlow",
    "Star Particles": "createParticles()",
    "Particle Function": "function createParticles()",
    "Food Icon Floats": "createFoodIcons()",
    "Food Icon Function": "function createFoodIcons()",
    "Celebration Confetti": "createConfetti()",
    "Confetti Function": "function createConfetti()",
    "Particle Container": "particle-container",
    "Food Float Class": "food-icon-float",
    "Twinkle Animation": "@keyframes twinkle",
    "Float Food Animation": "@keyframes floatFood",
    "Custom Scrollbar": "::-webkit-scrollbar",
    "Glow Effects": "filter: brightness",
    "Shimmer Effects": "@keyframes shimmer",
}

print("📋 CHECKING ULTRA-VIBRANT FEATURES:")
print("-" * 70)

results = []
for feature_name, search_string in features.items():
    found = search_string in content
    status = "✅ FOUND" if found else "❌ MISSING"
    results.append(found)
    print(f"{status:15} {feature_name}")

print("-" * 70)

# Summary
found_count = sum(results)
total_count = len(results)
percentage = (found_count / total_count) * 100

print()
print("📊 SUMMARY:")
print(f"   Features Found: {found_count}/{total_count} ({percentage:.1f}%)")
print()

if percentage == 100:
    print("✅ EXCELLENT! All ultra-vibrant features are present!")
    print()
    print("🎯 NEXT STEPS:")
    print("   1. Make sure Flask server is running (python app.py)")
    print("   2. Clear ALL browser data (Ctrl+Shift+Delete)")
    print("   3. Close and reopen your browser completely")
    print("   4. Go to: http://localhost:5000/dashboard")
    print("   5. Login as customer (Eriz)")
    print()
    print("💡 TIP: Try opening in Incognito/Private mode first!")
    print("   This ensures NO cache is being used.")
    print()
elif percentage >= 80:
    print("⚠️  WARNING: Most features present but some are missing")
elif percentage >= 50:
    print("⚠️  WARNING: Only some features are present")
else:
    print("❌ ERROR: Most ultra-vibrant features are missing!")

# File size check
file_size = os.path.getsize(dashboard_path)
print(f"📄 File Size: {file_size:,} bytes ({file_size / 1024:.1f} KB)")

# Line count
with open(dashboard_path, 'r', encoding='utf-8') as f:
    line_count = sum(1 for _ in f)
print(f"📝 Line Count: {line_count:,} lines")

print()
print("=" * 70)
print("🎉 TEST COMPLETE!")
print("=" * 70)
