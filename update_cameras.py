#!/usr/bin/env python3
import os
import re
import glob

# Time display HTML to add after LIVE indicator
time_display = '''                <span class="flex items-center gap-2">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                    <span id="current-time" class="font-medium">--:--:-- JST</span>
                </span>'''

# JavaScript to add before </body>
time_script = '''
    <script>
        function updateTime() {
            const now = new Date();
            const options = {
                timeZone: 'Asia/Tokyo',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
                hour12: false
            };
            const timeString = now.toLocaleTimeString('en-US', options) + ' JST';
            document.getElementById('current-time').textContent = timeString;
        }

        updateTime();
        setInterval(updateTime, 1000);
    </script>'''

def update_camera_page(file_path):
    """Update a single camera page with time display and JavaScript."""
    print(f"Processing: {os.path.basename(file_path)}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already updated
    if 'id="current-time"' in content:
        print(f"  ⏭️  Already has time display, skipping")
        return False

    # Add time display after LIVE indicator
    # Pattern: Find the LIVE span closing tag and add time display after it
    pattern = r'(                <span class="flex items-center gap-2">\s*<span class="w-2 h-2 bg-red-500 rounded-full animate-pulse"></span>\s*LIVE\s*</span>)\s*(\n\s*</div>)'

    if re.search(pattern, content):
        content = re.sub(
            pattern,
            r'\1\n' + time_display + r'\2',
            content
        )
        print(f"  ✅ Added time display")
    else:
        print(f"  ⚠️  Could not find LIVE indicator pattern")
        return False

    # Add JavaScript before </body>
    if '</body>' in content and time_script not in content:
        content = content.replace('</body>', time_script + '\n</body>')
        print(f"  ✅ Added JavaScript")

    # Write updated content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return True

def main():
    camera_files = glob.glob('/home/user/sakuralivecams/cameras/*.html')

    # Exclude tokyo-tower.html as it's already updated
    camera_files = [f for f in camera_files if 'tokyo-tower.html' not in f]

    print(f"Found {len(camera_files)} camera pages to update\n")

    updated_count = 0
    skipped_count = 0

    for file_path in sorted(camera_files):
        if update_camera_page(file_path):
            updated_count += 1
        else:
            skipped_count += 1
        print()

    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Updated: {updated_count}")
    print(f"  Skipped: {skipped_count}")
    print(f"  Total:   {len(camera_files)}")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
