#!/usr/bin/env python3
import os
import re
import glob

# Unique city descriptions - SEO optimized, city-specific
CITY_DESCRIPTIONS = {
    'tokyo': {
        'para1': 'Watch Tokyo live through our extensive network of HD webcams capturing Japan\'s dynamic capital city. From the world-famous Shibuya Scramble Crossing to the serene gardens of the Imperial Palace, our cameras provide real-time views of Tokyo\'s incredible contrast between ultramodern technology and traditional culture.',
        'para2': 'Our Tokyo webcams stream 24/7 from strategic locations including Shinjuku\'s neon-lit streets, the iconic Tokyo Tower, bustling Tokyo Station, and peaceful temple districts like Asakusa. Experience the morning rush of salarymen, the vibrant energy of Harajuku, and the stunning city lights that transform Tokyo after dark.',
        'para3': 'Whether you\'re planning your first visit to Japan\'s capital, checking current weather and crowd conditions, or simply captivated by Tokyo\'s unique urban landscape, our free live streams keep you connected to this extraordinary metropolis where ancient traditions meet cutting-edge innovation.'
    },
    'osaka': {
        'para1': 'Discover Osaka through live webcams showcasing Japan\'s third-largest city and culinary capital. Known as the "Nation\'s Kitchen," Osaka offers a unique blend of street food culture, historic castles, and friendly locals with a distinct Kansai dialect and personality that sets it apart from Tokyo.',
        'para2': 'Our Osaka cameras capture the neon spectacle of Dotonbori\'s entertainment district, the majestic Osaka Castle surrounded by cherry blossoms, and the bustling Kuromon Ichiba Market where locals shop for fresh ingredients. Watch as this merchant city comes alive with its famous takoyaki vendors, comedy theaters, and vibrant nightlife.',
        'para3': 'Stream live views of Osaka 24/7 completely free. Check real-time conditions at Umeda Sky Building, observe the Tsutenkaku Tower in retro Shinsekai, or watch crowds at Universal Studios Japan. Experience why Osakans proudly embrace their city\'s motto: "kuidaore" - eat until you drop.'
    },
    'kyoto': {
        'para1': 'Experience Kyoto live - Japan\'s ancient capital and cultural heartbeat. With 17 UNESCO World Heritage sites, over 2,000 temples and shrines, and traditional geisha districts, Kyoto preserves Japanese heritage like nowhere else. Our webcams offer glimpses into this timeless city where every season brings breathtaking natural beauty.',
        'para2': 'Watch live as monks tend to Zen gardens, observe the changing colors at famous temples like Kiyomizu-dera, and see visitors walking through thousands of vermillion torii gates at Fushimi Inari. Our cameras capture the serene Philosopher\'s Path during cherry blossom season and the magical Arashiyama Bamboo Grove swaying in the wind.',
        'para3': 'Free 24/7 streaming from Kyoto lets you witness traditional tea ceremonies in historic districts, explore the covered stalls of Nishiki Market, and observe the elegant wooden machiya townhouses in Gion where geishas still practice their ancient art. Connect with 1,000 years of Japanese history in real-time.'
    },
    'hokkaido': {
        'para1': 'Explore Hokkaido live - Japan\'s wild northern frontier and winter wonderland. As Japan\'s second-largest island, Hokkaido offers dramatic seasonal contrasts from the world-famous Sapporo Snow Festival to summer lavender fields in Furano. Our webcams capture pristine wilderness, volcanic hot springs, and unique wildlife found nowhere else in Japan.',
        'para2': 'Stream live views from Sapporo\'s urban center, watch steam rising from Noboribetsu\'s volcanic hot spring resort, and observe the spectacular night views from Mount Hakodate. Our cameras showcase Hokkaido\'s powder snow that attracts skiers worldwide, fresh seafood markets offering uni and crab, and the untamed beauty of Shiretoko National Park.',
        'para3': 'Watch Hokkaido\'s four distinct seasons unfold in real-time. Check current snow conditions at ski resorts, observe wildlife in national parks, or plan your visit to see the famous Blue Pond. Free live streams connect you to Japan\'s last frontier where nature reigns supreme.'
    },
    'okinawa': {
        'para1': 'Dive into Okinawa through live webcams showcasing Japan\'s tropical paradise. This subtropical island chain offers crystal-clear waters, white sandy beaches, and a unique Ryukyuan culture distinct from mainland Japan. Former seat of the Ryukyu Kingdom, Okinawa blends Japanese heritage with Southeast Asian and American influences.',
        'para2': 'Our Okinawa cameras stream turquoise waters perfect for diving and snorkeling, the restored grandeur of Shuri Castle, and the lively atmosphere of Kokusai Street in Naha. Watch palm trees sway in ocean breezes, observe traditional Eisa dance performances, and see why Okinawans enjoy one of the world\'s longest life expectancies.',
        'para3': 'Experience Okinawa\'s eternal summer live and free. Check beach conditions at pristine coastlines, watch sunset at Cape Manzamo\'s dramatic cliffs, or observe the massive whale sharks at Churaumi Aquarium. Stream the subtropical beauty that makes Okinawa Japan\'s premier beach destination.'
    },
    'fukuoka': {
        'para1': 'Watch Fukuoka live - Kyushu\'s largest city and ancient gateway to Asia. This vibrant port city combines modern shopping districts with historic shrines and is famous for Hakata ramen, yatai street food stalls, and warm Kyushu hospitality. Our webcams capture Fukuoka\'s perfect blend of urban energy and coastal relaxation.',
        'para2': 'Stream views of Hakata Station\'s impressive architecture, observe the busy Port of Hakata welcoming international ferries, and watch locals enjoying Ohori Park\'s peaceful lake. Our cameras showcase Canal City\'s colorful shopping complex, traditional festivals at Kushida Shrine, and the famous yatai food stalls lighting up at dusk.',
        'para3': 'Connect with Fukuoka 24/7 through free live streams. Check current conditions at Fukuoka Airport, one of Asia\'s most conveniently located urban airports, or explore the city that bridges modern Japan with its ancient continental connections to Korea and China.'
    },
    'yokohama': {
        'para1': 'Discover Yokohama live - Japan\'s second-largest city and premier port. Just south of Tokyo, Yokohama pioneered Japan\'s opening to the world with the largest Chinatown in Japan, historic Western architecture, and innovative modern development. Our webcams showcase this cosmopolitan waterfront city where East meets West.',
        'para2': 'Watch live as ships navigate Yokohama Harbor, observe the iconic Ferris wheel at Minato Mirai 21, and see visitors exploring the Cup Noodles Museum and Ramen Museum. Our cameras capture the Red Brick Warehouse shopping district, Yamashita Park\'s waterfront promenade, and Japan\'s largest Chinatown bursting with authentic restaurants.',
        'para3': 'Stream Yokohama free in real-time. Check weather at the historic port, watch the futuristic Landmark Tower dominate the skyline, and observe this international city that retains its unique character while complementing nearby Tokyo.'
    },
    'hiroshima': {
        'para1': 'Experience Hiroshima live - a city of peace, resilience, and natural beauty. Rising from the ashes of 1945, modern Hiroshima stands as a symbol of peace with the UNESCO-listed Peace Memorial and A-Bomb Dome. Beyond its powerful history, this vibrant city offers the nearby sacred island of Miyajima and delicious Hiroshima-style okonomiyaki.',
        'para2': 'Our Hiroshima webcams stream the serene Peace Memorial Park, the rebuilt city center along the Ota River delta, and views toward the famous floating torii gate at Itsukushima Shrine. Watch the city that transformed tragedy into a message of hope, now thriving with museums, parks, and local cuisine.',
        'para3': 'Connect with Hiroshima through free 24/7 live streams. Observe the illuminated A-Bomb Dome at night, check conditions for visiting Miyajima Island, and witness how this resilient city balances remembrance with optimism for the future.'
    },
    'nagano': {
        'para1': 'Explore Nagano live - Japan\'s mountain prefecture and host of the 1998 Winter Olympics. Surrounded by the Japanese Alps, Nagano offers world-class skiing, historic temples including the famous Zenko-ji, and the adorable snow monkeys bathing in natural hot springs. Our webcams capture this mountainous region\'s stunning four-season beauty.',
        'para2': 'Watch live snow conditions at premier ski resorts, observe the ancient Zenko-ji Temple welcoming pilgrims, and see the charming castle town of Matsumoto. Our cameras showcase alpine scenery, traditional onsen towns, and the natural hot spring pools where Japanese macaques relax in steaming water.',
        'para3': 'Stream Nagano\'s mountains free in real-time. Check current skiing conditions, observe seasonal changes in the Japanese Alps, and plan your visit to one of Japan\'s most scenic prefectures where spiritual heritage meets outdoor adventure.'
    },
}

# Generic but varied descriptions for cities without custom content
GENERIC_TEMPLATES = [
    {
        'para1': 'Experience {city} through our live HD webcams showcasing this unique Japanese destination. Our strategically positioned cameras provide authentic real-time views of local landmarks, daily life, and the distinctive atmosphere that makes {city} a special part of Japan\'s cultural tapestry.',
        'para2': 'Watch {city} come alive throughout the day and night with continuous 24/7 streaming. Observe local residents going about their daily routines, explore the city\'s architectural character, and discover the seasonal changes that transform the landscape across spring cherry blossoms, summer festivals, autumn colors, and winter scenes.',
        'para3': 'All {city} webcam streams are completely free with no subscription required. Use our live feeds to check current weather conditions, observe crowd levels at popular locations, or simply stay connected to this fascinating Japanese city from anywhere in the world.'
    },
    {
        'para1': 'Discover {city} in real-time through our network of live streaming webcams positioned across the city. From historic temples and shrines to modern urban centers, our cameras offer an authentic window into daily life in this distinctive Japanese locale.',
        'para2': 'Our {city} live streams capture the essence of the region 24 hours a day, seven days a week. Watch as morning commuters fill the streets, observe the midday bustle of local markets and shopping districts, and see the city transform as evening lights illuminate the landscape.',
        'para3': 'Connect with {city} through free unlimited streaming. Whether you\'re planning a future visit, reminiscing about past travels, or simply curious about this Japanese destination, our webcams keep you connected to the authentic rhythm and atmosphere of {city}.'
    },
    {
        'para1': 'Watch {city} live through our continuously streaming HD webcams. This Japanese city offers its own unique character, blending local traditions with modern life. Our cameras provide real-time views that showcase what makes {city} distinctive among Japan\'s diverse cities and regions.',
        'para2': 'Stream live 24/7 from various locations throughout {city}. Our webcams capture everything from bustling urban areas to quieter neighborhood streets, showing you the authentic daily rhythm of this Japanese community as residents work, shop, and enjoy their surroundings.',
        'para3': 'Enjoy free, unlimited access to {city} live streams. Perfect for checking current conditions before visiting, observing local weather patterns, or maintaining a connection to this Japanese destination. All streams are available at no cost and can be accessed anytime from anywhere in the world.'
    }
]

def get_city_description(city_name):
    """Get unique description for a city."""
    city_key = city_name.lower()

    # Return custom description if available
    if city_key in CITY_DESCRIPTIONS:
        return CITY_DESCRIPTIONS[city_key]

    # Use hash of city name to consistently select same template for each city
    template_index = hash(city_key) % len(GENERIC_TEMPLATES)
    template = GENERIC_TEMPLATES[template_index]

    return {
        'para1': template['para1'].format(city=city_name),
        'para2': template['para2'].format(city=city_name),
        'para3': template['para3'].format(city=city_name)
    }

def update_city_description(file_path):
    """Update city page description with unique content."""
    filename = os.path.basename(file_path)
    city_slug = filename.replace('.html', '')

    print(f"Processing: {filename}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract city name from h1
    h1_match = re.search(r'<h1[^>]*>([^<]+)</h1>', content)
    if h1_match:
        city_name = h1_match.group(1).replace(' Live Webcams', '').replace(' Webcams', '').strip()
    else:
        city_name = city_slug.title()

    # Get unique description
    desc = get_city_description(city_name)

    # Find and replace the description section
    old_pattern = r'(<div class="prose prose-lg text-gray-700 space-y-4">\s*)<p>\s*Experience ' + re.escape(city_name) + r' in real-time.*?</p>\s*<p>\s*Our cameras capture the essence.*?</p>\s*<p>\s*All webcam streams are free.*?</p>'

    new_content = f'''\\1<p>
                            {desc['para1']}
                        </p>
                        <p>
                            {desc['para2']}
                        </p>
                        <p>
                            {desc['para3']}
                        </p>'''

    if re.search(old_pattern, content, re.DOTALL):
        content = re.sub(old_pattern, new_content, content, flags=re.DOTALL)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"  ✅ Updated with unique description")
        return True
    else:
        print(f"  ⚠️  Could not find description pattern")
        return False

def main():
    city_files = glob.glob('/home/user/sakuralivecams/cities/*.html')

    print(f"Found {len(city_files)} city pages to update\n")

    updated_count = 0
    skipped_count = 0

    for file_path in sorted(city_files):
        try:
            if update_city_description(file_path):
                updated_count += 1
            else:
                skipped_count += 1
        except Exception as e:
            print(f"  ❌ Error: {e}")
        print()

    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Updated: {updated_count}")
    print(f"  Skipped: {skipped_count}")
    print(f"  Total:   {len(city_files)}")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
