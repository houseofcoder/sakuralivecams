#!/usr/bin/env python3
import os
import re
import glob
from html.parser import HTMLParser

# City-specific data for places to visit (SEO-optimized)
CITY_PLACES = {
    'tokyo': [
        'Shibuya Crossing - World\'s busiest pedestrian crossing',
        'Senso-ji Temple - Tokyo\'s oldest Buddhist temple in Asakusa',
        'Tokyo Skytree - Japan\'s tallest structure with observation decks',
        'Meiji Shrine - Peaceful Shinto shrine in a forested area',
        'Tsukiji Outer Market - Fresh seafood and street food paradise',
        'Harajuku - Youth fashion and pop culture hub',
        'Akihabara - Electronics and anime district',
        'Imperial Palace East Gardens - Historic Japanese gardens'
    ],
    'osaka': [
        'Osaka Castle - Historic 16th-century fortress',
        'Dotonbori - Neon-lit entertainment district with street food',
        'Kuromon Ichiba Market - "Osaka\'s Kitchen" fresh food market',
        'Umeda Sky Building - Futuristic twin-tower with observatory',
        'Shitennoji Temple - Japan\'s oldest officially-administered temple',
        'Osaka Aquarium Kaiyukan - One of the world\'s largest aquariums',
        'Shinsekai - Retro neighborhood with Tsutenkaku Tower',
        'Universal Studios Japan - Popular theme park resort'
    ],
    'kyoto': [
        'Fushimi Inari Shrine - Famous for thousands of red torii gates',
        'Kinkaku-ji (Golden Pavilion) - Stunning gold-leaf covered temple',
        'Arashiyama Bamboo Grove - Ethereal bamboo forest path',
        'Kiyomizu-dera Temple - UNESCO World Heritage site with city views',
        'Gion District - Historic geisha quarter with traditional architecture',
        'Nijo Castle - UNESCO site with famous "nightingale floors"',
        'Philosopher\'s Path - Cherry blossom-lined canal walk',
        'Nishiki Market - 400-year-old covered food market'
    ],
    'hokkaido': [
        'Sapporo Snow Festival - World-famous winter ice sculpture event',
        'Odori Park - Central park hosting seasonal events',
        'Mount Hakodate - Spectacular night views of the city',
        'Noboribetsu Onsen - Premier hot spring resort area',
        'Furano Lavender Fields - Purple blooms in summer',
        'Asahiyama Zoo - Innovative wildlife exhibits',
        'Lake Toya - Caldera lake with hot spring resorts',
        'Shiretoko National Park - UNESCO World Heritage wilderness'
    ],
    'okinawa': [
        'Shuri Castle - Restored Ryukyu Kingdom palace (UNESCO)',
        'Churaumi Aquarium - World-class ocean exhibit',
        'Kokusai Street - Main shopping and dining boulevard',
        'Cape Manzamo - Dramatic coastal cliff formations',
        'Naminoue Shrine - Seaside Shinto shrine on cliff',
        'Okinawa World - Cultural theme park with limestone caves',
        'Beaches - Pristine white sand beaches and coral reefs',
        'American Village - Shopping complex with Ferris wheel'
    ],
}

# Generic places for cities without specific data
GENERIC_PLACES = [
    'Historic temples and shrines',
    'Traditional markets and shopping districts',
    'Local museums and cultural centers',
    'Scenic parks and gardens',
    'Popular restaurants and food streets',
    'Historic landmarks and monuments'
]

def get_city_places(city_name):
    """Get places to visit for a city."""
    city_key = city_name.lower()
    return CITY_PLACES.get(city_key, GENERIC_PLACES)

class CityNameExtractor(HTMLParser):
    """Extract city name from HTML h1."""
    def __init__(self):
        super().__init__()
        self.city_name = None
        self.in_h1 = False

    def handle_starttag(self, tag, attrs):
        if tag == 'h1':
            self.in_h1 = True

    def handle_endtag(self, tag):
        if tag == 'h1':
            self.in_h1 = False

    def handle_data(self, data):
        if self.in_h1 and data.strip() and not self.city_name:
            # Extract city name (remove "Live Webcams" suffix)
            text = data.strip()
            self.city_name = text.replace(' Live Webcams', '').replace(' Webcams', '')

def update_city_page(file_path):
    """Comprehensive update for a city page."""
    filename = os.path.basename(file_path)
    city_slug = filename.replace('.html', '')

    print(f"Processing: {filename}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract city name
    extractor = CityNameExtractor()
    extractor.feed(content)
    city_name = extractor.city_name or city_slug.title()

    changes_made = []

    # 1. Add current time display in hero section (after the 4-grid stats)
    if 'id="current-time"' not in content:
        time_display = '''            </div>

            <div class="mt-6 flex items-center gap-2 text-white">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                <span class="text-lg font-semibold">Current Time (JST): <span id="current-time" class="font-bold">--:--:--</span></span>
            </div>'''

        pattern = r'(            </div>\s*</div>\s*</section>)'
        replacement = time_display + r'\n        \1'

        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content, count=1)
            changes_made.append("time display")

    # 2. Enhance About section with places to visit
    if 'Places to Visit' not in content:
        places = get_city_places(city_name)
        places_html = '\n'.join([f'                <li class="flex items-start gap-2"><span class="text-rose-600 mt-1">•</span><span>{place}</span></li>' for place in places])

        enhanced_about = f'''    <section class="py-12 bg-white">
        <div class="max-w-7xl mx-auto px-4">
            <div class="grid md:grid-cols-2 gap-12">
                <div>
                    <h2 class="text-3xl font-bold text-gray-900 mb-6">About {city_name} Webcams</h2>
                    <div class="prose prose-lg text-gray-700 space-y-4">
                        <p>
                            Experience {city_name} in real-time through our strategically positioned HD webcams.
                            Whether you're planning your visit, reminiscing about past travels, or simply curious
                            about life in {city_name}, these live streams offer an authentic window into this
                            captivating Japanese destination.
                        </p>
                        <p>
                            Our cameras capture the essence of {city_name} 24/7, from bustling daytime activity
                            to serene evening atmospheres. Watch as locals go about their daily lives, observe
                            weather patterns in real-time, and discover the unique rhythm that makes {city_name}
                            one of Japan's most fascinating locations.
                        </p>
                        <p>
                            All webcam streams are free to watch, with no subscription required. Bookmark this
                            page to check back anytime and stay connected to {city_name} from anywhere in the world.
                        </p>
                    </div>
                </div>

                <div>
                    <h3 class="text-2xl font-bold text-gray-900 mb-6">Places to Visit in {city_name}</h3>
                    <ul class="space-y-3 text-gray-700">
{places_html}
                    </ul>
                    <div class="mt-6 p-4 bg-rose-50 rounded-lg">
                        <p class="text-sm text-gray-700">
                            <strong class="text-rose-700">Pro Tip:</strong> Use our live webcams to check current
                            weather conditions and crowd levels before visiting popular attractions in {city_name}.
                        </p>
                    </div>
                </div>
            </div>'''

        # Find the old about section and replace it
        old_about_pattern = r'    <section class="py-12 bg-white">.*?</section>'

        if re.search(old_about_pattern, content, re.DOTALL):
            content = re.sub(old_about_pattern, enhanced_about + '\n    </section>', content, flags=re.DOTALL, count=1)
            changes_made.append("enhanced about section")

    # 3. Replace footer with SEO-optimized version
    if 'Popular Cities' not in content:
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
                        <li><a href="tokyo.html" class="text-gray-400 hover:text-white transition">Tokyo Webcams</a></li>
                        <li><a href="osaka.html" class="text-gray-400 hover:text-white transition">Osaka Webcams</a></li>
                        <li><a href="kyoto.html" class="text-gray-400 hover:text-white transition">Kyoto Webcams</a></li>
                        <li><a href="okinawa.html" class="text-gray-400 hover:text-white transition">Okinawa Webcams</a></li>
                        <li><a href="hokkaido.html" class="text-gray-400 hover:text-white transition">Hokkaido Webcams</a></li>
                    </ul>
                </div>

                <!-- More Destinations -->
                <div>
                    <h4 class="text-white font-semibold mb-3">More Destinations</h4>
                    <ul class="space-y-2 text-sm">
                        <li><a href="yokohama.html" class="text-gray-400 hover:text-white transition">Yokohama Webcams</a></li>
                        <li><a href="fukuoka.html" class="text-gray-400 hover:text-white transition">Fukuoka Webcams</a></li>
                        <li><a href="hiroshima.html" class="text-gray-400 hover:text-white transition">Hiroshima Webcams</a></li>
                        <li><a href="nagano.html" class="text-gray-400 hover:text-white transition">Nagano Webcams</a></li>
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
                <p>&copy; <span id="copyright-year"></span> SakuraLive. All rights reserved. Live webcams from Japan - Tokyo, Osaka, Kyoto and beyond.</p>
            </div>
        </div>
    </footer>'''

        old_footer_pattern = r'    <footer class="bg-black.*?</footer>'
        if re.search(old_footer_pattern, content, re.DOTALL):
            content = re.sub(old_footer_pattern, new_footer, content, flags=re.DOTALL)
            changes_made.append("SEO footer")

    # 4. Add JavaScript for time and copyright year (before </body>)
    if 'updateTime()' not in content:
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
            const timeString = now.toLocaleTimeString('en-US', options);
            const timeElement = document.getElementById('current-time');
            if (timeElement) {
                timeElement.textContent = timeString;
            }
        }

        updateTime();
        setInterval(updateTime, 1000);

        const copyrightYear = document.getElementById('copyright-year');
        if (copyrightYear) {
            copyrightYear.textContent = new Date().getFullYear();
        }
    </script>'''

        content = content.replace('</body>', time_script + '\n</body>')
        changes_made.append("JavaScript")

    # Write updated content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    if changes_made:
        print(f"  ✅ Updated: {', '.join(changes_made)}")
        return True
    else:
        print(f"  ⏭️  Already up to date")
        return False

def main():
    city_files = glob.glob('/home/user/sakuralivecams/cities/*.html')

    print(f"Found {len(city_files)} city pages to update\n")

    updated_count = 0
    skipped_count = 0
    error_count = 0

    for file_path in sorted(city_files):
        try:
            if update_city_page(file_path):
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
    print(f"  Total:   {len(city_files)}")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
