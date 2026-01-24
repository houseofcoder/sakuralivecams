#!/usr/bin/env python3
import os
import re
import glob
from html.parser import HTMLParser

class CameraInfoExtractor(HTMLParser):
    """Extract camera name and city from HTML."""
    def __init__(self):
        super().__init__()
        self.camera_name = None
        self.city = None
        self.in_h1 = False
        self.in_breadcrumb_city = False
        self.breadcrumb_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag == 'h1':
            self.in_h1 = True
        # Look for city link in breadcrumb
        if tag == 'a':
            attrs_dict = dict(attrs)
            href = attrs_dict.get('href', '')
            if '../cities/' in href:
                self.in_breadcrumb_city = True

    def handle_endtag(self, tag):
        if tag == 'h1':
            self.in_h1 = False
        if tag == 'a':
            self.in_breadcrumb_city = False

    def handle_data(self, data):
        data = data.strip()
        if self.in_h1 and data and not self.camera_name:
            self.camera_name = data
        if self.in_breadcrumb_city and data and not self.city:
            # Remove ", Japan" if present and ignore "View All" text
            if not data.startswith('View All'):
                self.city = data.replace(', Japan', '')

def create_detailed_description(camera_name, city):
    """Create a detailed description template for a camera location."""

    # Create the description with generic but informative content
    description = f'''                    <div class="text-gray-300 space-y-3 mb-4">
                        <p>Experience the vibrant atmosphere of <strong class="text-white">{camera_name}</strong> through this live streaming webcam. Located in {city}, Japan, this camera provides real-time views of one of the area's notable locations, bringing you closer to Japanese culture and daily life.</p>

                        <p>This live feed offers an authentic window into {city}, allowing viewers from around the world to observe the local atmosphere, weather conditions, and the dynamic rhythm of Japanese life as it unfolds in real-time.</p>

                        <p><strong class="text-white">What you can see:</strong> Watch the area come alive throughout the day, from the early morning hours through the evening. The camera captures the authentic character of this location, including pedestrian activity, local architecture, and the changing ambiance across different times of day.</p>

                        <p><strong class="text-white">Best viewing times:</strong> Early morning (6:00-8:00 JST) to see the day beginning, midday (11:00-14:00 JST) for peak activity, sunset hours (17:00-19:00 JST) for beautiful lighting, and evening (19:00-22:00 JST) when many locations showcase their illuminated charm.</p>
                    </div>'''

    return description

def update_camera_description(file_path):
    """Update a camera page with detailed description."""
    filename = os.path.basename(file_path)

    # Skip tokyo-tower.html as it already has a custom description
    if filename == 'tokyo-tower.html':
        print(f"Processing: {filename}")
        print(f"  ⏭️  Skipping (already has custom description)")
        return False

    print(f"Processing: {filename}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already has detailed description (space-y-3 class indicates detailed format)
    if 'space-y-3 mb-4' in content and '<strong class="text-white">' in content:
        print(f"  ⏭️  Already has detailed description")
        return False

    # Extract camera name and city
    extractor = CameraInfoExtractor()
    extractor.feed(content)

    camera_name = extractor.camera_name
    city = extractor.city

    if not camera_name or not city:
        print(f"  ⚠️  Could not extract camera name or city")
        print(f"      Camera: {camera_name}, City: {city}")
        return False

    # Pattern to find the simple description paragraph
    # Looking for: <p class="text-gray-300 mb-4">Live webcam view of ..., Japan.</p>
    pattern = r'<p class="text-gray-300 mb-4">Live webcam view of [^<]+, Japan\.</p>'

    if not re.search(pattern, content):
        print(f"  ⚠️  Could not find description pattern to replace")
        return False

    # Create the new detailed description
    new_description = create_detailed_description(camera_name, city)

    # Replace the old description
    content = re.sub(pattern, new_description, content)

    # Write updated content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  ✅ Updated description for {camera_name}, {city}")
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
            if update_camera_description(file_path):
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
