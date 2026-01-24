#!/usr/bin/env python3
import os
import re
import glob

# SEO-optimized footer HTML
new_footer = '''    <footer class="bg-black py-12 mt-12">
        <div class="max-w-7xl mx-auto px-4">
            <div class="grid md:grid-cols-4 gap-8 mb-8">
                <!-- About Section -->
                <div class="md:col-span-1">
                    <h3 class="text-white font-bold text-lg mb-3">SakuraLive</h3>
                    <p class="text-gray-400 text-sm">Experience Japan in real-time with 200+ live webcams across Tokyo, Osaka, Kyoto, and more. Watch live streams 24/7 from iconic landmarks, bustling streets, and scenic locations.</p>
                </div>

                <!-- Popular Cities -->
                <div>
                    <h4 class="text-white font-semibold mb-3">Popular Cities</h4>
                    <ul class="space-y-2 text-sm">
                        <li><a href="../cities/tokyo.html" class="text-gray-400 hover:text-white transition">Tokyo Webcams</a></li>
                        <li><a href="../cities/osaka.html" class="text-gray-400 hover:text-white transition">Osaka Webcams</a></li>
                        <li><a href="../cities/kyoto.html" class="text-gray-400 hover:text-white transition">Kyoto Webcams</a></li>
                        <li><a href="../cities/okinawa.html" class="text-gray-400 hover:text-white transition">Okinawa Webcams</a></li>
                        <li><a href="../cities/hokkaido.html" class="text-gray-400 hover:text-white transition">Hokkaido Webcams</a></li>
                    </ul>
                </div>

                <!-- More Destinations -->
                <div>
                    <h4 class="text-white font-semibold mb-3">More Destinations</h4>
                    <ul class="space-y-2 text-sm">
                        <li><a href="../cities/yokohama.html" class="text-gray-400 hover:text-white transition">Yokohama Webcams</a></li>
                        <li><a href="../cities/fukuoka.html" class="text-gray-400 hover:text-white transition">Fukuoka Webcams</a></li>
                        <li><a href="../cities/hiroshima.html" class="text-gray-400 hover:text-white transition">Hiroshima Webcams</a></li>
                        <li><a href="../cities/nagano.html" class="text-gray-400 hover:text-white transition">Nagano Webcams</a></li>
                        <li><a href="../index.html" class="text-gray-400 hover:text-white transition">Browse All Cameras</a></li>
                    </ul>
                </div>

                <!-- Information -->
                <div>
                    <h4 class="text-white font-semibold mb-3">Information</h4>
                    <ul class="space-y-2 text-sm">
                        <li><a href="../privacy.html" class="text-gray-400 hover:text-white transition">Privacy Policy</a></li>
                        <li><a href="../terms.html" class="text-gray-400 hover:text-white transition">Terms of Service</a></li>
                        <li><a href="../contact.html" class="text-gray-400 hover:text-white transition">Contact Us</a></li>
                    </ul>
                </div>
            </div>

            <!-- Copyright -->
            <div class="border-t border-gray-800 pt-6 text-center text-gray-400 text-sm">
                <p>&copy; 2025 SakuraLive. All rights reserved. Live webcams from Japan - Tokyo, Osaka, Kyoto and beyond.</p>
            </div>
        </div>
    </footer>'''

def update_footer(file_path):
    """Update footer in a camera page."""
    filename = os.path.basename(file_path)
    print(f"Processing: {filename}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already updated (look for new footer marker)
    if 'Popular Cities' in content and 'More Destinations' in content:
        print(f"  ⏭️  Footer already updated")
        return False

    # Pattern to match the old footer (from <footer> to </footer>)
    old_footer_pattern = r'    <footer class="bg-black py-8 mt-12">.*?</footer>'

    if not re.search(old_footer_pattern, content, re.DOTALL):
        print(f"  ⚠️  Could not find footer pattern")
        return False

    # Replace the footer
    content = re.sub(old_footer_pattern, new_footer, content, flags=re.DOTALL)

    # Write updated content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  ✅ Footer updated")
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
            if update_footer(file_path):
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
