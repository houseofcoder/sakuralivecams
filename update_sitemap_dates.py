#!/usr/bin/env python3
"""
Update sitemap.xml with today's date to signal freshness to search engines.
Also boosts priority for top-performing pages.
"""

import re
from datetime import datetime

def update_sitemap():
    """Update lastmod dates in sitemap.xml"""
    with open('sitemap.xml', 'r', encoding='utf-8') as f:
        content = f.read()

    # Get today's date
    today = datetime.now().strftime('%Y-%m-%d')

    # Replace all lastmod dates with today
    content = re.sub(
        r'<lastmod>\d{4}-\d{2}-\d{2}</lastmod>',
        f'<lastmod>{today}</lastmod>',
        content
    )

    # Boost priority for high-value pages
    high_value_urls = [
        'shibuya-crossing-scramble-crossing.html',
        'mount-fuji-oshino.html',
        'osaka-dotonbori-live-camera.html',
        'tokyo-tower.html',
        'sapporo-station.html',
    ]

    for url in high_value_urls:
        # Find this URL and boost its priority to 0.90
        pattern = f'(<url><loc>https://sakuralivecams.com/cameras/{re.escape(url)}</loc><lastmod>{today}</lastmod><priority>)0\\.80(</priority></url>)'
        content = re.sub(pattern, r'\g<1>0.90\2', content)

    # Write back
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(content)

    return True

def main():
    print("📅 Updating sitemap.xml with fresh dates...")

    if update_sitemap():
        today = datetime.now().strftime('%Y-%m-%d')
        print(f"✅ Updated all lastmod dates to {today}")
        print("\nBoosted priority for top cameras:")
        print("  • Shibuya Crossing (0.90)")
        print("  • Mount Fuji (0.90)")
        print("  • Osaka Dotonbori (0.90)")
        print("  • Tokyo Tower (0.90)")
        print("  • Sapporo Station (0.90)")
        print("\nFresh dates signal to search engines that content is actively maintained!")
    else:
        print("❌ Failed to update sitemap")

if __name__ == '__main__':
    main()
