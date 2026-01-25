#!/usr/bin/env python3
"""
Enhance VideoObject schema on all camera pages with additional SEO properties.
Adds: contentLocation, keywords, improved publisher info, duration (for live streams).
"""

import os
import re
from html.parser import HTMLParser

class VideoSchemaParser(HTMLParser):
    """Parse camera page to extract metadata"""
    def __init__(self):
        super().__init__()
        self.city = None
        self.camera_name = None
        self.tags = []
        self.in_tag_span = False
        self.tag_depth = 0

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        # Look for tag badges
        if tag == 'span' and 'class' in attrs_dict:
            if 'bg-blue-500/20' in attrs_dict['class'] or 'text-blue-400' in attrs_dict['class']:
                self.in_tag_span = True
                self.tag_depth += 1
        # Extract city from links
        if tag == 'a' and 'href' in attrs_dict:
            if '../cities/' in attrs_dict['href']:
                # Extract city from URL like ../cities/tokyo.html
                city_match = re.search(r'cities/([^.]+)\.html', attrs_dict['href'])
                if city_match and not self.city:
                    self.city = city_match.group(1).title()
        # Extract h1 for camera name
        if tag == 'h1':
            self.in_h1 = True

    def handle_endtag(self, tag):
        if tag == 'span' and self.in_tag_span:
            self.tag_depth -= 1
            if self.tag_depth == 0:
                self.in_tag_span = False
        if tag == 'h1':
            self.in_h1 = False

    def handle_data(self, data):
        data = data.strip()
        if not data:
            return
        if self.in_tag_span and data:
            self.tags.append(data)
        if hasattr(self, 'in_h1') and self.in_h1 and not self.camera_name:
            self.camera_name = data

def get_video_metadata(html_content):
    """Extract video metadata from HTML"""
    parser = VideoSchemaParser()
    parser.feed(html_content)

    # Also extract tags from the HTML if parser didn't catch them
    tag_pattern = r'<span[^>]*text-blue-400[^>]*>([^<]+)</span>'
    additional_tags = re.findall(tag_pattern, html_content)
    parser.tags.extend(additional_tags)
    parser.tags = list(set(parser.tags))  # Remove duplicates

    return parser.camera_name, parser.city, parser.tags

def enhance_video_schema(file_path):
    """Enhance VideoObject schema in a camera page"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Get metadata
    camera_name, city, tags = get_video_metadata(content)

    if not camera_name:
        return False

    # Find existing VideoObject schema
    schema_pattern = r'<script type="application/ld\+json">\s*\n\s*\{[^}]*"@type":\s*"VideoObject"[^<]+</script>'
    schema_match = re.search(schema_pattern, content, re.DOTALL)

    if not schema_match:
        return False

    existing_schema = schema_match.group(0)

    # Extract video ID from existing schema
    video_id_match = re.search(r'youtube\.com/(?:embed|live)/([^"?]+)', existing_schema)
    if not video_id_match:
        return False

    video_id = video_id_match.group(1)

    # Create enhanced schema
    keywords_list = tags if tags else [city.lower(), 'japan', 'live webcam']
    keywords_str = ', '.join(keywords_list)

    filename = os.path.basename(file_path)

    enhanced_schema = f'''<script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "VideoObject",
        "name": "{camera_name} - Live Webcam",
        "description": "Watch {camera_name} live from {city}, Japan. Real-time HD webcam streaming 24/7. Free live view of {camera_name}.",
        "thumbnailUrl": "https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
        "uploadDate": "2024-01-01T00:00:00Z",
        "duration": "PT0S",
        "embedUrl": "https://www.youtube.com/embed/{video_id}",
        "contentUrl": "https://www.youtube.com/live/{video_id}",
        "keywords": "{keywords_str}",
        "inLanguage": "en",
        "isFamilyFriendly": true,
        "contentLocation": {{
            "@type": "Place",
            "name": "{city}, Japan",
            "address": {{
                "@type": "PostalAddress",
                "addressLocality": "{city}",
                "addressCountry": "JP"
            }}
        }},
        "publisher": {{
            "@type": "Organization",
            "name": "SakuraLive",
            "url": "https://sakuralivecams.com",
            "logo": {{
                "@type": "ImageObject",
                "url": "https://sakuralivecams.com/assets/images/logo.png",
                "width": 512,
                "height": 512
            }},
            "sameAs": [
                "https://play.google.com/store/apps/details?id=com.sakuralive"
            ]
        }},
        "isLiveBroadcast": true,
        "publication": {{
            "@type": "BroadcastEvent",
            "isLiveBroadcast": true,
            "startDate": "2024-01-01T00:00:00Z"
        }}
    }}
    </script>'''

    # Replace existing schema
    content = content.replace(existing_schema, enhanced_schema)

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
    print(f"🎥 Enhancing VideoObject schema on {len(camera_files)} camera pages...")

    updated_count = 0

    for filename in camera_files:
        file_path = os.path.join(cameras_dir, filename)
        try:
            if enhance_video_schema(file_path):
                updated_count += 1
                if updated_count % 50 == 0:
                    print(f"  ✓ Enhanced {updated_count} schemas...")
        except Exception as e:
            print(f"  ❌ Error processing {filename}: {e}")

    print(f"\n✅ Enhanced VideoObject schema on {updated_count} camera pages!")
    print(f"\nNew schema properties added:")
    print(f"  • contentLocation - Geographic data for local SEO")
    print(f"  • keywords - Relevant search terms")
    print(f"  • isLiveBroadcast - Indicates real-time streaming")
    print(f"  • Enhanced publisher info with logo and social links")
    print(f"  • isFamilyFriendly - Content rating")

if __name__ == '__main__':
    main()
