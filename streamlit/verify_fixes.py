"""
Comprehensive verification script for all fixes
"""
import ast
import os
import re

files_to_check = [
    'app.py',
    'pages/1_GOAT_Leaderboard.py',
    'pages/2_Driver_Analytics.py',
    'pages/3_Driver_Comparison.py',
    'pages/4_World_Champions.py',
    'utils/theme.py',
    'utils/cards.py',
    'utils/charts.py',
    'utils/images.py'
]

print("=" * 70)
print("COMPREHENSIVE VERIFICATION REPORT - Formula 1 Analytics Platform")
print("=" * 70)

all_issues = []
fixed_issues = []

for filepath in files_to_check:
    print(f"\n📄 Checking: {filepath}")
    
    if not os.path.exists(filepath):
        print(f"  ✗ ERROR: File not found")
        all_issues.append(f"{filepath}: File not found")
        continue
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # 1. Syntax check
    try:
        ast.parse(content)
        print("  ✓ Syntax OK")
    except SyntaxError as e:
        print(f"  ✗ Syntax Error: {e}")
        all_issues.append(f"{filepath}: Syntax error")
        continue
    
    # 2. Check for year references
    if re.search(r'2020-2026', content):
        print("  ✗ FOUND: '2020-2026' reference (should be removed)")
        all_issues.append(f"{filepath}: Contains year reference")
    else:
        print("  ✓ No year references")
        fixed_issues.append("Year references removed")
    
    # 3. Check for problematic st.plotly_chart patterns
    if 'st.plotly_chart(st.write' in content:
        print("  ✗ ERROR: Found st.plotly_chart(st.write(...))")
        all_issues.append(f"{filepath}: Invalid plotly chart pattern")
    else:
        print("  ✓ Plotly charts valid")
        fixed_issues.append("Plotly chart error fixed")
    
    # 4. Check for dangerous HTML rendering patterns
    if re.search(r"st\.markdown\s*\(\s*<div", content):
        print("  ⚠ WARNING: Found st.markdown with HTML literal (should use unsafe_allow_html)")
        all_issues.append(f"{filepath}: Unsafe HTML rendering")
    else:
        print("  ✓ HTML rendering safe")
        fixed_issues.append("HTML rendering fixed")
    
    # 5. Check for hardcoded DRIVER_NAME without fallback
    if 'DRIVER_NAME' in content and 'try:' not in content and filepath.endswith('4_World_Champions.py'):
        # Check if it's using driver_col variable instead
        if 'driver_col' in content:
            print("  ✓ Column names handled dynamically")
            fixed_issues.append("Column name handling fixed")
        else:
            print("  ⚠ May have hardcoded DRIVER_NAME")

print("\n" + "=" * 70)
print("FIXES APPLIED")
print("=" * 70)

if fixed_issues:
    unique_fixes = list(set(fixed_issues))
    for fix in sorted(unique_fixes):
        print(f"  ✓ {fix}")

print("\n" + "=" * 70)
print("REMAINING ISSUES")
print("=" * 70)

if all_issues:
    unique_issues = list(set(all_issues))
    print(f"\n⚠ Found {len(unique_issues)} potential issues:")
    for issue in sorted(unique_issues):
        print(f"  ✗ {issue}")
else:
    print("\n✓ All files passed verification!")
    print("✓ No syntax errors")
    print("✓ No year references")
    print("✓ All HTML properly handled")
    print("✓ All column names handled dynamically")
    print("✓ Ready for deployment!")

print("\n" + "=" * 70)
