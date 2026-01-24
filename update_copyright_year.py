#!/usr/bin/env python3
import os
import re
import glob

def update_copyright(file_path):
    """Update copyright year to be dynamic."""
    filename = os.path.basename(file_path)
    print(f"Processing: {filename}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already updated
    if '<span id="copyright-year"></span>' in content:
        print(f"  ⏭️  Copyright already dynamic")
        return False

    # Pattern to find hardcoded year in copyright
    pattern = r'&copy; 2025 SakuraLive\.'

    if not re.search(pattern, content):
        print(f"  ⚠️  Could not find copyright pattern")
        return False

    # Replace with dynamic year span
    content = re.sub(
        pattern,
        r'&copy; <span id="copyright-year"></span> SakuraLive.',
        content
    )

    # Add copyright year JavaScript if not already present
    if 'copyright-year' in content and 'document.getElementById(\'copyright-year\')' not in content:
        # Find the existing time update script and add copyright year update
        time_script_pattern = r'(        updateTime\(\);\n        setInterval\(updateTime, 1000\);)'

        copyright_js = r'''\1
        document.getElementById('copyright-year').textContent = new Date().getFullYear();'''

        content = re.sub(time_script_pattern, copyright_js, content)

    # Write updated content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  ✅ Copyright year made dynamic")
    return True

def main():
    camera_files = glob.glob('/home/user/sakuralivecams/cameras/*.html')

    # Filter out non-camera pages
    camera_files = [f for f in camera_files if not os.path.basename(f).startswith('index')]

    print(f"Found {len(camera_files)} camera pages to update\n")

    updated_count = 0
    skipped_count = 0
    error_count = 0

    for file_path in sorted(camera_files):
        try:
            if update_copyright(file_path):
                updated_count += 1
            else:
                skipped_count += 1
        except Exception as e:
            print(f"  ❌ Error: {e}")
            error_count += 1
        print()

    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Updated: {updated_count}")
    print(f"  Skipped: {skipped_count}")
    print(f"  Errors:  {error_count}")
    print(f"  Total:   {len(camera_files)}")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
