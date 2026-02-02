#!/usr/bin/env python3
"""
Internationalization (i18n) Page Generator for SakuraLiveCams

This script generates Japanese versions of all HTML pages by:
1. Creating a /ja/ directory structure mirroring the English pages
2. Translating UI text using translation JSON files
3. Adding hreflang tags for SEO
4. Updating internal links to point to correct language versions
"""

import os
import re
import json
import shutil
from pathlib import Path
from html import escape

# Configuration
BASE_DIR = Path('/home/user/sakuralivecams')
TRANSLATIONS_DIR = BASE_DIR / 'translations'
JA_DIR = BASE_DIR / 'ja'

def load_translations(lang):
    """Load translations for a given language."""
    file_path = TRANSLATIONS_DIR / f'{lang}.json'
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_hreflang_tags(page_path, is_japanese=False):
    """Generate hreflang tags for a page."""
    # Normalize path
    if page_path.startswith('/'):
        page_path = page_path[1:]

    base_url = 'https://sakuralivecams.com'

    if is_japanese:
        en_url = f'{base_url}/{page_path}'
        ja_url = f'{base_url}/ja/{page_path}'
    else:
        en_url = f'{base_url}/{page_path}'
        ja_url = f'{base_url}/ja/{page_path}'

    return f'''    <link rel="alternate" hreflang="en" href="{en_url}">
    <link rel="alternate" hreflang="ja" href="{ja_url}">
    <link rel="alternate" hreflang="x-default" href="{en_url}">'''

def get_language_switcher_html(current_lang, page_path):
    """Generate language switcher HTML."""
    if current_lang == 'ja':
        en_path = f'../{page_path}' if '/' in page_path else f'../{page_path}'
        ja_path = page_path
        # Adjust paths for nested directories
        if page_path.startswith('cities/') or page_path.startswith('cameras/'):
            en_path = f'../../{page_path}'
        elif page_path == 'index.html':
            en_path = '../index.html'
    else:
        en_path = page_path
        ja_path = f'ja/{page_path}'

    return f'''<div class="flex items-center gap-2 text-sm">
                    <a href="{en_path}" class="{'text-white font-semibold' if current_lang == 'en' else 'text-gray-400 hover:text-white'}">EN</a>
                    <span class="text-gray-500">|</span>
                    <a href="{ja_path}" class="{'text-white font-semibold' if current_lang == 'ja' else 'text-gray-400 hover:text-white'}">日本語</a>
                </div>'''

def translate_index_page(content, translations):
    """Translate the main index.html page."""
    t = translations

    # Change html lang attribute
    content = re.sub(r'<html lang="en">', '<html lang="ja">', content)

    # Translate header tagline
    content = content.replace(
        'Watch live webcams across Japan',
        t['header']['tagline']
    )

    # Translate navigation
    content = content.replace('>Cities</a>', f'>{t["nav"]["cities"]}</a>')
    content = content.replace('>Cameras</a>', f'>{t["nav"]["cameras"]}</a>')
    content = content.replace('>Contact</a>', f'>{t["nav"]["contact"]}</a>')

    # Translate hero section
    content = re.sub(
        r'Live Japan Webcams - Watch 200\+ Real-Time HD Cameras from Tokyo, Kyoto, Osaka & Beyond',
        t['hero']['title'],
        content
    )
    content = re.sub(
        r'Experience Japan live with FREE HD webcam streams from 34\+ cities\. Watch Shibuya Crossing, Mt Fuji, temples, airports, and scenic landmarks - all streaming 24/7',
        t['hero']['subtitle'],
        content
    )

    # Translate statistics
    content = re.sub(r'<div class="text-gray-400">Live Cameras</div>', f'<div class="text-gray-400">{t["stats"]["cameras"]}</div>', content)
    content = re.sub(r'<div class="text-gray-400">Cities & Regions</div>', f'<div class="text-gray-400">{t["stats"]["cities"]}</div>', content)
    content = re.sub(r'<div class="text-gray-400">Live Streaming</div>', f'<div class="text-gray-400">{t["stats"]["streaming"]}</div>', content)
    content = re.sub(r'<div class="text-gray-400">Free Access</div>', f'<div class="text-gray-400">{t["stats"]["free"]}</div>', content)

    # Translate cities section
    content = re.sub(
        r'Explore Japan by City',
        t['cities_section']['title'],
        content
    )
    content = re.sub(
        r'Browse our curated collection of live webcams organized by major cities and regions across Japan',
        t['cities_section']['subtitle'],
        content
    )
    content = re.sub(r'>View All Cities</button>', f'>{t["cities_section"]["view_all"]}</button>', content)
    content = re.sub(r'>Show Less', f'>{t["cities_section"]["show_less"]}', content)
    content = re.sub(r'<h3 class="text-2xl font-bold text-white mb-6">All Locations</h3>',
                     f'<h3 class="text-2xl font-bold text-white mb-6">{t["cities_section"]["all_locations"]}</h3>', content)

    # Translate city cards
    content = re.sub(r"Japan's vibrant capital with 33\+ cameras", t['city_cards']['tokyo']['description'], content)
    content = re.sub(r"Japan's kitchen with 25\+ cameras", t['city_cards']['osaka']['description'], content)
    content = re.sub(r"Ancient capital with 10\+ cameras", t['city_cards']['kyoto']['description'], content)
    content = re.sub(r"Northern island with 15\+ cameras", t['city_cards']['hokkaido']['description'], content)
    content = re.sub(r"Tropical paradise with 8\+ cameras", t['city_cards']['okinawa']['description'], content)
    content = re.sub(r"Japan's icon with 12\+ cameras", t['city_cards']['mount_fuji']['description'], content)

    # Translate filter section
    content = re.sub(r'<h2 class="text-xl font-bold text-gray-800">Filter Streams</h2>',
                     f'<h2 class="text-xl font-bold text-gray-800">{t["filters"]["title"]}</h2>', content)
    content = re.sub(r'placeholder="Search tags \(e\.g\., skyline, airport\)…"',
                     f'placeholder="{t["filters"]["search_placeholder"]}"', content)
    content = re.sub(r'>Clear Filters</button>', f'>{t["filters"]["clear_filters"]}</button>', content)
    content = re.sub(r'Tip: tap a tag to toggle it\. Tags on cards are clickable too\.',
                     t['filters']['tip'], content)

    # Translate "Why Watch" section
    content = re.sub(r'Why Watch Live Japan Webcams\?', t['why_watch']['title'], content)
    content = re.sub(r'Experience Japan in real-time from anywhere in the world',
                     t['why_watch']['subtitle'], content)
    content = re.sub(r'<h3 class="text-xl font-bold text-gray-900 mb-3">Virtual Tourism & Trip Planning</h3>',
                     f'<h3 class="text-xl font-bold text-gray-900 mb-3">{t["why_watch"]["tourism"]["title"]}</h3>', content)
    content = re.sub(r'<h3 class="text-xl font-bold text-gray-900 mb-3">Cultural Connection</h3>',
                     f'<h3 class="text-xl font-bold text-gray-900 mb-3">{t["why_watch"]["cultural"]["title"]}</h3>', content)
    content = re.sub(r'<h3 class="text-xl font-bold text-gray-900 mb-3">24/7 Live Coverage</h3>',
                     f'<h3 class="text-xl font-bold text-gray-900 mb-3">{t["why_watch"]["coverage"]["title"]}</h3>', content)

    # Translate About section
    content = re.sub(r'<h2 class="text-2xl font-bold mb-3">About SakuraLive - Your Gateway to Japan</h2>',
                     f'<h2 class="text-2xl font-bold mb-3">{t["about"]["title"]}</h2>', content)

    # Translate FAQ section
    content = re.sub(r'<h3 class="text-xl font-semibold mb-3">Frequently Asked Questions</h3>',
                     f'<h3 class="text-xl font-semibold mb-3">{t["faq"]["title"]}</h3>', content)
    content = re.sub(r'<summary class="cursor-pointer font-medium">Are these official live cameras\?</summary>',
                     f'<summary class="cursor-pointer font-medium">{t["faq"]["q1"]["question"]}</summary>', content)
    content = re.sub(r'<summary class="cursor-pointer font-medium">How do I find specific locations\?</summary>',
                     f'<summary class="cursor-pointer font-medium">{t["faq"]["q2"]["question"]}</summary>', content)
    content = re.sub(r'<summary class="cursor-pointer font-medium">Can I watch on mobile\?</summary>',
                     f'<summary class="cursor-pointer font-medium">{t["faq"]["q3"]["question"]}</summary>', content)
    content = re.sub(r'<summary class="cursor-pointer font-medium">What are the best times to watch\?</summary>',
                     f'<summary class="cursor-pointer font-medium">{t["faq"]["q4"]["question"]}</summary>', content)

    # Translate footer
    content = re.sub(r'<h4 class="font-semibold text-white mb-4">Major Cities</h4>',
                     f'<h4 class="font-semibold text-white mb-4">{t["footer"]["major_cities"]}</h4>', content)
    content = re.sub(r'<h4 class="font-semibold text-white mb-4">Popular Cameras</h4>',
                     f'<h4 class="font-semibold text-white mb-4">{t["footer"]["popular_cameras"]}</h4>', content)
    content = re.sub(r'<h4 class="font-semibold text-white mb-4">Resources</h4>',
                     f'<h4 class="font-semibold text-white mb-4">{t["footer"]["resources"]}</h4>', content)
    content = re.sub(r'<h4 class="font-semibold text-white mb-3 text-sm">Browse by Type</h4>',
                     f'<h4 class="font-semibold text-white mb-3 text-sm">{t["footer"]["browse_by_type"]}</h4>', content)
    content = re.sub(r'>View All Cities →</a>', f'>{t["footer"]["view_all_cities"]}</a>', content)
    content = re.sub(r'>Browse All Cameras →</a>', f'>{t["footer"]["browse_all_cameras"]}</a>', content)
    content = re.sub(r'<p class="text-gray-400">Live webcams from across Japan in HD quality</p>',
                     f'<p class="text-gray-400">{t["footer"]["quality_tagline"]}</p>', content)

    # Update links to point to Japanese versions
    content = re.sub(r'href="cities/', 'href="cities/', content)
    content = re.sub(r'href="cameras/', 'href="cameras/', content)
    content = re.sub(r'href="contact\.html"', 'href="contact.html"', content)
    content = re.sub(r'href="privacy\.html"', 'href="privacy.html"', content)
    content = re.sub(r'href="terms\.html"', 'href="terms.html"', content)

    return content

def translate_city_page(content, translations, city_name):
    """Translate a city page."""
    t = translations

    # Change html lang attribute
    content = re.sub(r'<html lang="en">', '<html lang="ja">', content)

    # Translate header tagline
    content = content.replace(
        'Live Webcams from Japan',
        t['header']['tagline_short']
    )

    # Translate breadcrumb
    content = re.sub(r'>Home</a>', f'>{t["nav"]["home"]}</a>', content)

    # Translate statistics labels
    content = re.sub(r'<div class="text-sm opacity-90">Live Cameras</div>',
                     f'<div class="text-sm opacity-90">{t["city_page"]["live_cameras"]}</div>', content)
    content = re.sub(r'<div class="text-sm opacity-90">Live Streaming</div>',
                     f'<div class="text-sm opacity-90">{t["city_page"]["live_streaming"]}</div>', content)
    content = re.sub(r'<div class="text-sm opacity-90">Quality</div>',
                     f'<div class="text-sm opacity-90">{t["city_page"]["quality"]}</div>', content)
    content = re.sub(r'<div class="text-sm opacity-90">No Subscription</div>',
                     f'<div class="text-sm opacity-90">{t["city_page"]["no_subscription"]}</div>', content)

    # Translate current time label
    content = re.sub(r'Current Time \(JST\):',
                     f'{t["city_page"]["current_time"]}:', content)

    # Update link to index
    content = re.sub(r'href="\.\./index\.html"', 'href="../index.html"', content)

    return content

def translate_camera_page(content, translations, camera_name, city_name):
    """Translate a camera page."""
    t = translations

    # Change html lang attribute
    content = re.sub(r'<html lang="en">', '<html lang="ja">', content)

    # Translate header tagline
    content = content.replace(
        'Live Webcams from Japan',
        t['header']['tagline_short']
    )

    # Translate breadcrumb
    content = re.sub(r'>Home</a>', f'>{t["nav"]["home"]}</a>', content)

    # Translate "About This Camera" heading
    content = re.sub(r'<h2 class="text-2xl font-bold mb-4">About This Camera</h2>',
                     f'<h2 class="text-2xl font-bold mb-4">{t["camera_page"]["about_camera"]}</h2>', content)

    # Translate "Share This Camera" heading
    content = re.sub(r'<h3 class="text-xl font-bold mb-3">Share This Camera</h3>',
                     f'<h3 class="text-xl font-bold mb-3">{t["camera_page"]["share_camera"]}</h3>', content)

    # Translate section headings that contain city name
    content = re.sub(r'>More Cameras in ([^<]+)</h3>',
                     lambda m: f'>{m.group(1)}{t["camera_page"]["related_cameras"].replace("{city}", "")}</h3>', content)

    # Update links
    content = re.sub(r'href="\.\./index\.html"', 'href="../index.html"', content)
    content = re.sub(r'href="\.\./cities/', 'href="../cities/', content)

    return content

def add_hreflang_to_content(content, page_path, is_japanese):
    """Add hreflang tags to the HTML content."""
    hreflang_tags = get_hreflang_tags(page_path, is_japanese)

    # Insert after <meta charset="UTF-8">
    if '<meta charset="UTF-8"' in content:
        content = re.sub(
            r'(<meta charset="UTF-8"[^>]*>)',
            f'\\1\n{hreflang_tags}',
            content,
            count=1
        )

    return content

def add_language_switcher(content, current_lang, page_path):
    """Add language switcher to the header."""
    switcher_html = get_language_switcher_html(current_lang, page_path)

    # Find the nav element and add language switcher after it
    # Look for the Google Play Store button and add before it
    pattern = r'(<a href="https://play\.google\.com/store/apps/details\?id=com\.sakuralive"[^>]*>)'
    replacement = f'{switcher_html}\n            \\1'

    content = re.sub(pattern, replacement, content, count=1)

    return content

def update_canonical_url(content, page_path, is_japanese):
    """Update canonical URL for Japanese pages."""
    if is_japanese:
        base_url = 'https://sakuralivecams.com/ja'
        content = re.sub(
            r'<link rel="canonical" href="https://sakuralivecams\.com/([^"]*)"',
            f'<link rel="canonical" href="{base_url}/\\1"',
            content
        )
    return content

def process_index_page(translations):
    """Process and generate Japanese version of index.html."""
    print("Processing index.html...")

    source_path = BASE_DIR / 'index.html'
    dest_path = JA_DIR / 'index.html'

    with open(source_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Translate content
    content = translate_index_page(content, translations)

    # Add hreflang tags
    content = add_hreflang_to_content(content, 'index.html', is_japanese=True)

    # Add language switcher
    content = add_language_switcher(content, 'ja', 'index.html')

    # Update canonical URL
    content = update_canonical_url(content, 'index.html', is_japanese=True)

    # Update relative paths to go up one level for assets
    content = re.sub(r'href="assets/', 'href="../assets/', content)
    content = re.sub(r'src="assets/', 'src="../assets/', content)
    content = re.sub(r"'https://sakuralivecams\.com/assets/", "'../assets/", content)

    # Update links to other pages to stay in Japanese version
    content = re.sub(r'href="cities/', 'href="cities/', content)
    content = re.sub(r'href="cameras/', 'href="cameras/', content)
    content = re.sub(r'href="contact\.html"', 'href="contact.html"', content)
    content = re.sub(r'href="privacy\.html"', 'href="privacy.html"', content)
    content = re.sub(r'href="terms\.html"', 'href="terms.html"', content)

    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  ✅ Created {dest_path}")

def process_city_pages(translations):
    """Process and generate Japanese versions of city pages."""
    print("\nProcessing city pages...")

    cities_dir = BASE_DIR / 'cities'
    ja_cities_dir = JA_DIR / 'cities'

    for city_file in cities_dir.glob('*.html'):
        city_name = city_file.stem.title()
        dest_path = ja_cities_dir / city_file.name

        with open(city_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Translate content
        content = translate_city_page(content, translations, city_name)

        # Add hreflang tags
        content = add_hreflang_to_content(content, f'cities/{city_file.name}', is_japanese=True)

        # Add language switcher
        content = add_language_switcher(content, 'ja', f'cities/{city_file.name}')

        # Update canonical URL
        content = update_canonical_url(content, f'cities/{city_file.name}', is_japanese=True)

        # Update relative paths (go up two levels now)
        content = re.sub(r'href="\.\./assets/', 'href="../../assets/', content)
        content = re.sub(r'src="\.\./assets/', 'src="../../assets/', content)

        # Keep camera links within Japanese version
        content = re.sub(r'href="\.\./cameras/', 'href="../cameras/', content)
        content = re.sub(r'href="\.\./index\.html"', 'href="../index.html"', content)

        with open(dest_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"  ✅ Created {dest_path.name}")

def process_camera_pages(translations):
    """Process and generate Japanese versions of camera pages."""
    print("\nProcessing camera pages...")

    cameras_dir = BASE_DIR / 'cameras'
    ja_cameras_dir = JA_DIR / 'cameras'

    count = 0
    for camera_file in cameras_dir.glob('*.html'):
        camera_name = camera_file.stem.replace('-', ' ').title()
        dest_path = ja_cameras_dir / camera_file.name

        with open(camera_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract city name from breadcrumb
        city_match = re.search(r'href="\.\./cities/([^"]+)\.html"', content)
        city_name = city_match.group(1).title() if city_match else 'Japan'

        # Translate content
        content = translate_camera_page(content, translations, camera_name, city_name)

        # Add hreflang tags
        content = add_hreflang_to_content(content, f'cameras/{camera_file.name}', is_japanese=True)

        # Add language switcher
        content = add_language_switcher(content, 'ja', f'cameras/{camera_file.name}')

        # Update canonical URL
        content = update_canonical_url(content, f'cameras/{camera_file.name}', is_japanese=True)

        # Update relative paths (go up two levels now)
        content = re.sub(r'href="\.\./assets/', 'href="../../assets/', content)
        content = re.sub(r'src="\.\./assets/', 'src="../../assets/', content)

        # Keep links within Japanese version
        content = re.sub(r'href="\.\./cities/', 'href="../cities/', content)
        content = re.sub(r'href="\.\./cameras/', 'href="../cameras/', content)
        content = re.sub(r'href="\.\./index\.html"', 'href="../index.html"', content)

        with open(dest_path, 'w', encoding='utf-8') as f:
            f.write(content)

        count += 1

    print(f"  ✅ Created {count} camera pages")

def process_utility_pages(translations):
    """Process utility pages (contact, privacy, terms)."""
    print("\nProcessing utility pages...")

    utility_pages = ['contact.html', 'privacy.html', 'terms.html']

    for page_name in utility_pages:
        source_path = BASE_DIR / page_name
        dest_path = JA_DIR / page_name

        if not source_path.exists():
            print(f"  ⚠️  {page_name} not found, skipping...")
            continue

        with open(source_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Change lang attribute
        content = re.sub(r'<html lang="en">', '<html lang="ja">', content)

        # Add hreflang tags
        content = add_hreflang_to_content(content, page_name, is_japanese=True)

        # Add language switcher
        content = add_language_switcher(content, 'ja', page_name)

        # Update canonical URL
        content = update_canonical_url(content, page_name, is_japanese=True)

        # Update relative paths
        content = re.sub(r'href="assets/', 'href="../assets/', content)
        content = re.sub(r'src="assets/', 'src="../assets/', content)

        # Update links to stay in Japanese version
        content = re.sub(r'href="index\.html"', 'href="index.html"', content)
        content = re.sub(r'href="cities/', 'href="cities/', content)

        with open(dest_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"  ✅ Created {page_name}")

def add_hreflang_to_english_pages():
    """Add hreflang tags to all English pages."""
    print("\nAdding hreflang tags to English pages...")

    # Process index.html
    index_path = BASE_DIR / 'index.html'
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'hreflang="ja"' not in content:
        content = add_hreflang_to_content(content, 'index.html', is_japanese=False)
        content = add_language_switcher(content, 'en', 'index.html')

        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("  ✅ Updated index.html")

    # Process city pages
    cities_dir = BASE_DIR / 'cities'
    for city_file in cities_dir.glob('*.html'):
        with open(city_file, 'r', encoding='utf-8') as f:
            content = f.read()

        if 'hreflang="ja"' not in content:
            content = add_hreflang_to_content(content, f'cities/{city_file.name}', is_japanese=False)
            content = add_language_switcher(content, 'en', f'cities/{city_file.name}')

            with open(city_file, 'w', encoding='utf-8') as f:
                f.write(content)

    print("  ✅ Updated city pages")

    # Process camera pages
    cameras_dir = BASE_DIR / 'cameras'
    for camera_file in cameras_dir.glob('*.html'):
        with open(camera_file, 'r', encoding='utf-8') as f:
            content = f.read()

        if 'hreflang="ja"' not in content:
            content = add_hreflang_to_content(content, f'cameras/{camera_file.name}', is_japanese=False)
            content = add_language_switcher(content, 'en', f'cameras/{camera_file.name}')

            with open(camera_file, 'w', encoding='utf-8') as f:
                f.write(content)

    print("  ✅ Updated camera pages")

    # Process utility pages
    for page_name in ['contact.html', 'privacy.html', 'terms.html']:
        page_path = BASE_DIR / page_name
        if page_path.exists():
            with open(page_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if 'hreflang="ja"' not in content:
                content = add_hreflang_to_content(content, page_name, is_japanese=False)
                content = add_language_switcher(content, 'en', page_name)

                with open(page_path, 'w', encoding='utf-8') as f:
                    f.write(content)

    print("  ✅ Updated utility pages")

def create_directory_structure():
    """Create the Japanese pages directory structure."""
    print("Creating directory structure...")

    # Create main ja directory
    JA_DIR.mkdir(exist_ok=True)

    # Create subdirectories
    (JA_DIR / 'cities').mkdir(exist_ok=True)
    (JA_DIR / 'cameras').mkdir(exist_ok=True)

    print("  ✅ Created /ja/, /ja/cities/, /ja/cameras/")

def main():
    """Main function to generate all Japanese pages."""
    print("="*60)
    print("SakuraLiveCams i18n Page Generator")
    print("="*60)

    # Load Japanese translations
    print("\nLoading translations...")
    ja_translations = load_translations('ja')
    print("  ✅ Loaded Japanese translations")

    # Create directory structure
    create_directory_structure()

    # Process all pages
    process_index_page(ja_translations)
    process_city_pages(ja_translations)
    process_camera_pages(ja_translations)
    process_utility_pages(ja_translations)

    # Add hreflang to English pages
    add_hreflang_to_english_pages()

    print("\n" + "="*60)
    print("Generation complete!")
    print("="*60)

    # Count generated files
    ja_files = list(JA_DIR.rglob('*.html'))
    print(f"\nTotal Japanese pages generated: {len(ja_files)}")
    print(f"  - Index: 1")
    print(f"  - Cities: {len(list((JA_DIR / 'cities').glob('*.html')))}")
    print(f"  - Cameras: {len(list((JA_DIR / 'cameras').glob('*.html')))}")
    print(f"  - Utility: {len([f for f in JA_DIR.glob('*.html') if f.name != 'index.html'])}")

if __name__ == '__main__':
    main()
