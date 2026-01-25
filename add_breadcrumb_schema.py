#!/usr/bin/env python3
"""
Add BreadcrumbList schema to all camera pages for better SEO and rich snippets.
This helps search engines understand site hierarchy and can show breadcrumbs in search results.
"""

import os
import re
from html.parser import HTMLParser

class CameraPageParser(HTMLParser):
    """Parse camera page to extract city and camera name"""
    def __init__(self):
        super().__init__()
        self.city = None
        self.camera_name = None
        self.in_breadcrumb = False
        self.in_h1 = False

    def handle_starttag(self, tag, attrs):
        if tag == 'nav':
            self.in_breadcrumb = True
        if tag == 'h1':
            self.in_h1 = True

    def handle_endtag(self, tag):
        if tag == 'nav':
            self.in_breadcrumb = False
        if tag == 'h1':
            self.in_h1 = False

    def handle_data(self, data):
        data = data.strip()
        if not data:
            return
        # Extract city from breadcrumb
        if self.in_breadcrumb and not self.city and data not in ['Home', '/', 'View All']:
            # Remove ", Japan" if present
            if ', Japan' in data:
                data = data.replace(', Japan', '')
            if data and data != 'Home' and data != '/':
                self.city = data
        # Extract camera name from h1
        if self.in_h1 and not self.camera_name:
            self.camera_name = data

def get_camera_info(html_content):
    """Extract camera name and city from HTML"""
    parser = CameraPageParser()
    parser.feed(html_content)
    return parser.camera_name, parser.city

def add_breadcrumb_schema(file_path):
    """Add BreadcrumbList schema to a camera page"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already has BreadcrumbList schema
    if '"@type": "BreadcrumbList"' in content or '"@type":"BreadcrumbList"' in content:
        return False

    # Get camera info
    camera_name, city = get_camera_info(content)

    if not camera_name or not city:
        print(f"  ⚠️  Could not extract info from {os.path.basename(file_path)}")
        return False

    # Get filename for camera URL
    filename = os.path.basename(file_path)
    city_slug = city.lower().replace(' ', '-')

    # Create breadcrumb schema
    breadcrumb_schema = f'''
    <!-- Breadcrumb Schema for SEO -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {{
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": "https://sakuralivecams.com/"
            }},
            {{
                "@type": "ListItem",
                "position": 2,
                "name": "{city}",
                "item": "https://sakuralivecams.com/cities/{city_slug}.html"
            }},
            {{
                "@type": "ListItem",
                "position": 3,
                "name": "{camera_name}",
                "item": "https://sakuralivecams.com/cameras/{filename}"
            }}
        ]
    }}
    </script>
'''

    # Find where to insert - after existing VideoObject schema
    video_schema_pattern = r'(</script>\s*\n\s*<style>)'

    if re.search(video_schema_pattern, content):
        content = re.sub(
            video_schema_pattern,
            f'</script>{breadcrumb_schema}\n    <style>',
            content,
            count=1
        )
    else:
        # Fallback: insert before </head>
        content = content.replace('</head>', f'{breadcrumb_schema}\n</head>')

    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return True

def main():
    """Process all camera HTML files"""
    cameras_dir = 'cameras'

    if not os.path.exists(cameras_dir):
        print(f"❌ Directory '{cameras_dir}' not found")
        return

    camera_files = [f for f in os.listdir(cameras_dir) if f.endswith('.html')]
    print(f"📍 Adding BreadcrumbList schema to {len(camera_files)} camera pages...")

    updated_count = 0
    skipped_count = 0

    for filename in camera_files:
        file_path = os.path.join(cameras_dir, filename)
        try:
            if add_breadcrumb_schema(file_path):
                updated_count += 1
                if updated_count % 50 == 0:
                    print(f"  ✓ Processed {updated_count} files...")
            else:
                skipped_count += 1
        except Exception as e:
            print(f"  ❌ Error processing {filename}: {e}")

    print(f"\n✅ Complete!")
    print(f"  • Updated: {updated_count} files")
    print(f"  • Skipped: {skipped_count} files")
    print(f"\nBreadcrumbList schema helps search engines:")
    print(f"  • Understand your site structure")
    print(f"  • Show breadcrumbs in search results")
    print(f"  • Improve click-through rates")

if __name__ == '__main__':
    main()
