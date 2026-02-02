#!/usr/bin/env python3
"""
Update sitemap.xml with Japanese (ja) URLs for internationalization.

This script adds all Japanese page URLs to the sitemap and updates to use
proper multilingual sitemap format with xhtml:link hreflang attributes.
"""

import os
import re
from datetime import date
from pathlib import Path

BASE_DIR = Path('/home/user/sakuralivecams')
JA_DIR = BASE_DIR / 'ja'
SITEMAP_PATH = BASE_DIR / 'sitemap.xml'

def get_today():
    """Get today's date in YYYY-MM-DD format."""
    return date.today().strftime('%Y-%m-%d')

def generate_sitemap():
    """Generate a new sitemap with both English and Japanese URLs."""

    today = get_today()
    base_url = 'https://sakuralivecams.com'

    # Header with xhtml namespace for hreflang
    sitemap_content = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
'''

    # Helper function to create URL entry with hreflang
    def create_url_entry(path, priority, is_homepage=False):
        if is_homepage:
            en_url = f'{base_url}/'
            ja_url = f'{base_url}/ja/'
        else:
            en_url = f'{base_url}/{path}'
            ja_url = f'{base_url}/ja/{path}'

        return f'''    <url>
        <loc>{en_url}</loc>
        <xhtml:link rel="alternate" hreflang="en" href="{en_url}"/>
        <xhtml:link rel="alternate" hreflang="ja" href="{ja_url}"/>
        <xhtml:link rel="alternate" hreflang="x-default" href="{en_url}"/>
        <lastmod>{today}</lastmod>
        <priority>{priority}</priority>
    </url>
    <url>
        <loc>{ja_url}</loc>
        <xhtml:link rel="alternate" hreflang="en" href="{en_url}"/>
        <xhtml:link rel="alternate" hreflang="ja" href="{ja_url}"/>
        <xhtml:link rel="alternate" hreflang="x-default" href="{en_url}"/>
        <lastmod>{today}</lastmod>
        <priority>{priority}</priority>
    </url>
'''

    # Homepage (highest priority)
    sitemap_content += create_url_entry('', '1.00', is_homepage=True)
    sitemap_content += create_url_entry('index.html', '1.00')

    # City pages (high priority)
    cities_dir = BASE_DIR / 'cities'
    major_cities = ['tokyo', 'osaka', 'kyoto', 'hokkaido', 'okinawa', 'yokohama', 'fukuoka']

    for city_file in sorted(cities_dir.glob('*.html')):
        city_name = city_file.stem
        priority = '0.95' if city_name in major_cities else '0.85'
        sitemap_content += create_url_entry(f'cities/{city_file.name}', priority)

    # Camera pages (medium priority)
    cameras_dir = BASE_DIR / 'cameras'
    popular_cameras = [
        'shibuya-crossing-scramble-crossing',
        'mount-fuji-oshino',
        'osaka-dotonbori-live-camera',
        'tokyo-tower',
        'sapporo-station'
    ]

    for camera_file in sorted(cameras_dir.glob('*.html')):
        camera_name = camera_file.stem
        priority = '0.90' if camera_name in popular_cameras else '0.80'
        sitemap_content += create_url_entry(f'cameras/{camera_file.name}', priority)

    # Utility pages (lower priority)
    utility_pages = [
        ('contact.html', '0.60'),
        ('privacy.html', '0.50'),
        ('terms.html', '0.50'),
    ]

    for page, priority in utility_pages:
        if (BASE_DIR / page).exists():
            sitemap_content += create_url_entry(page, priority)

    # Close urlset
    sitemap_content += '</urlset>\n'

    return sitemap_content

def main():
    """Main function to update the sitemap."""
    print("="*60)
    print("Sitemap i18n Updater")
    print("="*60)

    # Generate new sitemap
    print("\nGenerating multilingual sitemap...")
    sitemap_content = generate_sitemap()

    # Write to file
    with open(SITEMAP_PATH, 'w', encoding='utf-8') as f:
        f.write(sitemap_content)

    print(f"✅ Updated {SITEMAP_PATH}")

    # Count URLs
    url_count = sitemap_content.count('<loc>')
    print(f"\nTotal URLs in sitemap: {url_count}")
    print(f"  - English pages: {url_count // 2}")
    print(f"  - Japanese pages: {url_count // 2}")

if __name__ == '__main__':
    main()
