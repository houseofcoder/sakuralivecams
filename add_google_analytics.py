#!/usr/bin/env python3
"""
Add Google Tag Manager and Google Analytics to all camera and city pages.
Critical for tracking site performance and user behavior.
"""

import os
import re

# GTM and GA tracking codes
GTM_HEAD_CODE = '''    <!-- Google Tag Manager -->
    <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
    new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    })(window,document,'script','dataLayer','GTM-5CGB48MH');</script>
    <!-- End Google Tag Manager -->

    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-BLTYH5F771"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-BLTYH5F771');
    </script>

'''

GTM_BODY_CODE = '''  <!-- Google Tag Manager (noscript) -->
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-5CGB48MH"
  height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
  <!-- End Google Tag Manager (noscript) -->
'''

def add_analytics_to_file(file_path):
    """Add GTM and GA tracking codes to a single HTML file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already has both GTM in head AND noscript in body
    has_gtm_head = 'GTM-5CGB48MH' in content and '<!-- Google Tag Manager -->' in content
    has_gtm_body = 'googletagmanager.com/ns.html' in content

    if has_gtm_head and has_gtm_body:
        return False

    modified = False

    # Add GTM and GA to <head> (before </head>) if not present
    if '</head>' in content and not has_gtm_head:
        content = content.replace('</head>', f'{GTM_HEAD_CODE}</head>')
        modified = True

    # Add GTM noscript to <body> (right after <body>) if not present
    if '<body' in content and not has_gtm_body:
        # Match <body> or <body class="...">
        body_pattern = r'(<body[^>]*>)'
        content = re.sub(body_pattern, f'\\1\n{GTM_BODY_CODE}', content)
        modified = True

    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True

    return False

def process_directory(directory, file_type):
    """Process all HTML files in a directory"""
    if not os.path.exists(directory):
        print(f"⚠️  Directory '{directory}' not found")
        return 0

    html_files = [f for f in os.listdir(directory) if f.endswith('.html')]

    if not html_files:
        print(f"⚠️  No HTML files found in '{directory}'")
        return 0

    print(f"\n📊 Adding analytics to {len(html_files)} {file_type} pages...")

    updated_count = 0
    skipped_count = 0

    for filename in html_files:
        file_path = os.path.join(directory, filename)
        try:
            if add_analytics_to_file(file_path):
                updated_count += 1
                if updated_count % 50 == 0:
                    print(f"  ✓ Processed {updated_count} files...")
            else:
                skipped_count += 1
        except Exception as e:
            print(f"  ❌ Error processing {filename}: {e}")

    print(f"✅ {file_type.capitalize()} pages complete!")
    print(f"  • Updated: {updated_count} files")
    print(f"  • Skipped: {skipped_count} files (already have analytics)")

    return updated_count

def main():
    """Add Google Analytics to all camera and city pages"""
    print("=" * 70)
    print("🎯 Adding Google Tag Manager & Google Analytics to All Pages")
    print("=" * 70)

    total_updated = 0

    # Process camera pages
    total_updated += process_directory('cameras', 'camera')

    # Process city pages
    total_updated += process_directory('cities', 'city')

    print("\n" + "=" * 70)
    print(f"✅ COMPLETE! Updated {total_updated} total pages")
    print("=" * 70)
    print("\n📈 Analytics Tracking Now Active:")
    print("  • Google Tag Manager: GTM-5CGB48MH")
    print("  • Google Analytics 4: G-BLTYH5F771")
    print("\nBenefits:")
    print("  ✓ Track user behavior and page views")
    print("  ✓ Monitor traffic sources and conversions")
    print("  ✓ Analyze which cameras are most popular")
    print("  ✓ Measure SEO performance improvements")
    print("  ✓ Understand user journey and engagement")

if __name__ == '__main__':
    main()
