#!/usr/bin/env python3
"""
Optimize camera page title tags to be more competitive and SEO-friendly.
Adds power words and location-specific keywords to improve rankings.
"""

import os
import re

def optimize_title(file_path):
    """Optimize the title tag in a camera page"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find existing title
    title_pattern = r'<title>([^<]+)</title>'
    title_match = re.search(title_pattern, content)

    if not title_match:
        return False

    existing_title = title_match.group(1)

    # Skip if already optimized with "Watch" at start
    if existing_title.startswith('Watch '):
        return False

    # Extract camera name and city from existing title
    # Format is usually: "Camera Name - Live Webcam from City, Japan | SakuraLive"
    parts = existing_title.split(' - ')
    if len(parts) < 2:
        return False

    camera_name = parts[0].strip()

    # Check if it's a generic format or already has good keywords
    if 'Live Webcam from' in existing_title:
        # Extract city
        city_match = re.search(r'Live Webcam from ([^,]+),', existing_title)
        if city_match:
            city = city_match.group(1)
            # Create more competitive title
            new_title = f'Watch {camera_name} Live - FREE HD Webcam {city}, Japan 24/7 | SakuraLive'

            # Replace title
            content = content.replace(f'<title>{existing_title}</title>', f'<title>{new_title}</title>')

            # Also update meta description to be more competitive
            meta_desc_pattern = r'<meta name="description" content="([^"]+)"'
            meta_match = re.search(meta_desc_pattern, content)

            if meta_match:
                old_desc = meta_match.group(1)
                new_desc = f'Watch {camera_name} live webcam from {city}, Japan - FREE HD streaming 24/7. Real-time views, no registration required. Best Japan webcam site with 200+ cameras.'

                content = content.replace(
                    f'<meta name="description" content="{old_desc}"',
                    f'<meta name="description" content="{new_desc}"'
                )

            # Write back
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            return True

    return False

def main():
    """Process all camera HTML files"""
    cameras_dir = 'cameras'

    if not os.path.exists(cameras_dir):
        print(f"❌ Directory '{cameras_dir}' not found")
        return

    camera_files = [f for f in os.listdir(cameras_dir) if f.endswith('.html')]
    print(f"📝 Optimizing title tags on {len(camera_files)} camera pages...")

    updated_count = 0

    for filename in camera_files:
        file_path = os.path.join(cameras_dir, filename)
        try:
            if optimize_title(file_path):
                updated_count += 1
                if updated_count % 50 == 0:
                    print(f"  ✓ Optimized {updated_count} titles...")
        except Exception as e:
            print(f"  ❌ Error processing {filename}: {e}")

    print(f"\n✅ Optimized {updated_count} camera page titles!")
    print(f"\nTitle improvements:")
    print(f"  • Added 'Watch' action word at start")
    print(f"  • Emphasized 'FREE HD' unique selling points")
    print(f"  • Added '24/7' availability")
    print(f"  • Improved meta descriptions with competitive keywords")

if __name__ == '__main__':
    main()
