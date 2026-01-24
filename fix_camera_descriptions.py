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

    def handle_starttag(self, tag, attrs):
        if tag == 'h1':
            self.in_h1 = True
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
            if not data.startswith('View All'):
                self.city = data.replace(', Japan', '')

def get_location_type(camera_name_lower):
    """Determine the type of location based on camera name."""
    if any(word in camera_name_lower for word in ['crossing', 'scramble', 'intersection']):
        return 'crossing'
    elif any(word in camera_name_lower for word in ['station', 'terminal', 'railway', 'jr', 'shinkansen']):
        return 'station'
    elif any(word in camera_name_lower for word in ['temple', 'shrine', 'sensoji', 'fushimi']):
        return 'temple'
    elif any(word in camera_name_lower for word in ['tower', 'skytree', 'dome']):
        return 'tower'
    elif any(word in camera_name_lower for word in ['market', 'street', 'shopping']):
        return 'market'
    elif any(word in camera_name_lower for word in ['castle', 'palace']):
        return 'castle'
    elif any(word in camera_name_lower for word in ['beach', 'bay', 'harbor', 'port', 'ocean', 'sea']):
        return 'coastal'
    elif any(word in camera_name_lower for word in ['mountain', 'mount', 'volcano', 'fuji', 'sakurajima']):
        return 'mountain'
    elif any(word in camera_name_lower for word in ['park', 'garden']):
        return 'park'
    elif any(word in camera_name_lower for word in ['airport']):
        return 'airport'
    elif any(word in camera_name_lower for word in ['bridge']):
        return 'bridge'
    elif any(word in camera_name_lower for word in ['onsen', 'hot spring']):
        return 'onsen'
    elif any(word in camera_name_lower for word in ['river', 'lake']):
        return 'water'
    elif any(word in camera_name_lower for word in ['skyline', 'panoramic', 'view']):
        return 'panoramic'
    elif any(word in camera_name_lower for word in ['district', 'town', 'village']):
        return 'district'
    else:
        return 'general'

def create_unique_description(camera_name, city, location_type):
    """Create a unique description based on location type."""

    descriptions = {
        'crossing': [
            f'Watch the dynamic energy of <strong class="text-white">{camera_name}</strong> through this live HD webcam. This bustling intersection in {city} showcases the constant flow of pedestrian traffic that epitomizes urban Japanese life, where thousands cross simultaneously in synchronized chaos.',
            f'Our cameras capture the mesmerizing choreography of {city}\'s pedestrians at this iconic crossing point. Experience the wave-like patterns as crowds surge across {camera_name}, a quintessentially Japanese urban phenomenon that attracts visitors from around the world.',
            f'This live stream offers front-row seats to the organized chaos that defines modern Japanese city crossings. From dawn commuters to late-night revelers, witness the perpetual motion at one of {city}\'s most dynamic intersection points.',
        ],
        'station': [
            f'Experience the heartbeat of {city}\'s transportation network through our live camera at <strong class="text-white">{camera_name}</strong>. Watch as Japan\'s legendary punctual trains arrive and depart, while commuters navigate this bustling hub with characteristic efficiency and order.',
            f'This real-time view captures the impressive architecture and constant activity of one of {city}\'s vital transportation centers. From the sleek bullet trains to local commuters, observe the seamless choreography of Japanese rail travel at {camera_name}.',
            f'Stream live from {camera_name}, where modern engineering meets daily Japanese life. Watch the precision of train operations, the flow of thousands of passengers, and the architectural grandeur that makes this station a landmark in {city}.',
        ],
        'temple': [
            f'Discover spiritual tranquility through our live webcam at <strong class="text-white">{camera_name}</strong>. This sacred site in {city} offers a peaceful contrast to urban bustle, where traditional architecture and devotional practices have endured for centuries.',
            f'Experience the timeless beauty of Japanese spirituality at {camera_name}. Our camera captures visitors paying respects, seasonal festivals, and the serene atmosphere of this historic {city} temple where ancient traditions continue to thrive.',
            f'Watch live as this revered temple in {city} welcomes worshippers and tourists alike. From morning prayers to evening rituals, {camera_name} provides an authentic window into Japan\'s living spiritual heritage and architectural splendor.',
        ],
        'tower': [
            f'<strong class="text-white">{camera_name}</strong> rises majestically above {city} in this live HD stream. Watch this iconic landmark transform from day to night, when illumination creates a spectacular display against the city skyline, visible for miles around.',
            f'Our camera captures the commanding presence of {camera_name}, a symbol of {city}\'s modern identity. Observe changing weather patterns, the interplay of light and shadow, and the urban landscape spreading out below this architectural marvel.',
            f'Experience {city} from a unique perspective with views of {camera_name}. This live stream showcases the tower\'s striking appearance throughout the day, its role as a communications hub, and its status as one of the region\'s most recognizable structures.',
        ],
        'market': [
            f'Immerse yourself in the vibrant commerce of <strong class="text-white">{camera_name}</strong> through this live webcam. Watch vendors displaying fresh seafood, local shoppers seeking ingredients, and the authentic energy of {city}\'s traditional market culture.',
            f'This live feed captures the colorful chaos and culinary treasures of {camera_name} in {city}. From early morning deliveries to the bustle of midday shoppers, experience Japan\'s food culture and merchant traditions in real-time.',
            f'Stream the authentic atmosphere of {city}\'s marketplace at {camera_name}. Watch as locals browse seasonal produce, street food vendors prepare traditional dishes, and the market pulses with the energy that has defined Japanese commerce for generations.',
        ],
        'castle': [
            f'<strong class="text-white">{camera_name}</strong> stands as a testament to Japan\'s feudal past, its imposing architecture dominating the {city} skyline. Our live camera captures this historic fortress through all seasons, from cherry blossom framing to autumn foliage.',
            f'Watch centuries of history come alive at {camera_name} in {city}. This live stream showcases the castle\'s magnificent defensive walls, traditional architecture, and the surrounding grounds that have witnessed pivotal moments in Japanese history.',
            f'Experience the grandeur of feudal Japan through our camera at {camera_name}. From its strategic position in {city}, this castle offers a window into samurai-era architecture, historical significance, and the preservation efforts that keep this heritage alive.',
        ],
        'coastal': [
            f'Discover the serene beauty of Japan\'s coastline at <strong class="text-white">{camera_name}</strong>. This live ocean view from {city} captures rolling waves, changing tides, and the interplay of light on water that makes coastal Japan so captivating.',
            f'Our camera streams the dynamic coastal landscape at {camera_name} in {city}. Watch boats navigating the waters, beachgoers enjoying the shore, and stunning sunsets painting the sky over the ocean in brilliant colors.',
            f'Experience {city}\'s maritime character through this live coastal webcam at {camera_name}. From peaceful morning seas to dramatic weather patterns, this stream captures the ever-changing moods of Japan\'s beautiful waterfront.',
        ],
        'mountain': [
            f'<strong class="text-white">{camera_name}</strong> showcases Japan\'s dramatic volcanic landscape in real-time. Watch this majestic peak from {city}, observing changing weather patterns, seasonal transformations, and the raw natural power that shapes the Japanese archipelago.',
            f'This live stream captures the awe-inspiring presence of {camera_name} near {city}. From snow-capped peaks to morning mist, witness the mountain\'s many moods and understand why these heights hold such spiritual significance in Japanese culture.',
            f'Experience the natural grandeur of {camera_name} through our live webcam. Whether shrouded in clouds or standing crystal clear against blue skies, this {city} landmark demonstrates nature\'s timeless beauty and power.',
        ],
        'park': [
            f'Find tranquility in urban {city} through our live view of <strong class="text-white">{camera_name}</strong>. Watch as visitors enjoy cherry blossoms in spring, lush greenery in summer, brilliant foliage in autumn, and serene snow in winter.',
            f'This live camera captures the peaceful atmosphere of {camera_name} in {city}. Observe families picnicking, couples strolling, and locals finding respite from urban life in this carefully maintained green space.',
            f'Experience the seasonal beauty of Japanese gardens and parks at {camera_name}. Our {city} webcam streams the changing landscape, traditional design elements, and the important role these spaces play in Japanese urban life.',
        ],
        'airport': [
            f'Watch Japan\'s aviation excellence in action at <strong class="text-white">{camera_name}</strong>. This live view of {city}\'s gateway captures aircraft movements, the efficient choreography of ground operations, and the constant flow of international travel.',
            f'Our camera streams the dynamic activity at {camera_name} in {city}. From take-offs and landings to the architectural design of this modern terminal, witness the precision that makes Japanese airports world-renowned.',
            f'Experience the hub of international connectivity at {camera_name}. This {city} airport webcam shows real-time operations, the scale of modern aviation, and Japan\'s reputation for punctuality and service excellence.',
        ],
        'bridge': [
            f'<strong class="text-white">{camera_name}</strong> spans majestically across {city}\'s waterways in this live stream. Watch vehicles and pedestrians cross this architectural landmark, especially stunning when illuminated after dark.',
            f'Our camera captures the elegant engineering of {camera_name} in {city}. This iconic structure serves as both vital infrastructure and beautiful landmark, showcasing Japanese design excellence.',
            f'Experience the graceful lines of {camera_name} through our live webcam. From its structural beauty to its role connecting {city}, this bridge represents Japanese engineering and aesthetic sensibilities.',
        ],
        'onsen': [
            f'Discover Japan\'s famous hot spring culture at <strong class="text-white">{camera_name}</strong> in {city}. Watch steam rising from natural thermal waters, a tradition that has relaxed and healed visitors for centuries.',
            f'This live view captures the peaceful atmosphere of {camera_name}, one of {city}\'s treasured onsen destinations. Observe the steam, traditional architecture, and the enduring appeal of Japan\'s hot spring culture.',
            f'Experience the volcanic legacy of Japan at {camera_name} in {city}. Our camera streams this geothermal wonder where locals and travelers have sought relaxation and rejuvenation for generations.',
        ],
        'water': [
            f'Watch the flowing beauty of <strong class="text-white">{camera_name}</strong> in {city}. This live stream captures reflections, seasonal water levels, and the important role this waterway plays in the local landscape and ecosystem.',
            f'Our camera showcases the natural beauty of {camera_name} near {city}. From calm morning reflections to dramatic weather conditions, observe how this body of water changes character throughout the day.',
            f'Experience the serene presence of {camera_name} through our live webcam. This {city} waterway offers peaceful views, wildlife sightings, and demonstrates the harmony between urban development and natural features.',
        ],
        'panoramic': [
            f'<strong class="text-white">{camera_name}</strong> offers sweeping views across {city}\'s urban landscape. This elevated perspective captures the vast scale of the metropolis, from towering skyscrapers to distant mountains.',
            f'Our camera provides a bird\'s-eye view of {city} from {camera_name}. Watch the city pulse with life, observe weather systems rolling through, and appreciate the stunning contrast between urban density and natural surroundings.',
            f'Experience {city} from above through this panoramic webcam at {camera_name}. From sunrise illuminating the cityscape to the glittering lights of evening, witness the full majesty of this Japanese metropolis.',
        ],
        'district': [
            f'Explore the unique character of <strong class="text-white">{camera_name}</strong> through this live {city} webcam. This neighborhood showcases local architecture, street life, and the distinctive atmosphere that defines different areas of Japanese cities.',
            f'Our camera captures the authentic daily rhythm of {camera_name} in {city}. Watch residents going about their routines, local shops opening and closing, and the community interactions that give this district its special character.',
            f'Experience {city}\'s diverse neighborhoods through our view of {camera_name}. From morning commutes to evening activities, this live stream reveals the layered complexity of urban Japanese life.',
        ],
        'general': [
            f'Discover <strong class="text-white">{camera_name}</strong> through our live HD webcam in {city}. This real-time view captures the authentic atmosphere of this notable location, where Japanese culture and daily life unfold naturally before the camera.',
            f'Our camera brings you live to {camera_name} in {city}, offering continuous views of this distinctive locale. Watch as the area transforms throughout the day, revealing different aspects of its character and appeal.',
            f'Experience {camera_name} in real-time from anywhere in the world. This {city} location streams 24/7, providing an unfiltered window into Japanese life, architecture, and the rhythms that define this unique place.',
        ]
    }

    # Select description based on hash for consistency
    desc_list = descriptions.get(location_type, descriptions['general'])
    desc_index = hash(camera_name) % len(desc_list)
    para1 = desc_list[desc_index]

    # Create varied second and third paragraphs
    para2_templates = [
        f'This live feed operates 24/7, capturing {camera_name} through all hours and weather conditions. From early morning calm to bustling midday activity and atmospheric evening scenes, witness the full cycle of life at this {city} location.',
        f'Stream continuous views of {camera_name} around the clock. Our high-definition camera captures this {city} landmark in all its moods - sunrise lighting, afternoon crowds, sunset colors, and nighttime illumination.',
        f'Watch {camera_name} throughout the day and night with our always-on live stream. This {city} webcam never sleeps, offering authentic views during quiet early hours, busy daytime periods, and magical evening transformations.',
    ]

    para3_templates = [
        f'<strong class="text-white">What makes this special:</strong> The camera angle provides excellent perspective on {camera_name}, capturing both close-up details and surrounding context. Perfect for checking current conditions, observing local weather, or simply enjoying virtual tourism to {city}.',
        f'<strong class="text-white">Viewing highlights:</strong> This webcam offers clear views of {camera_name} and its surroundings. Whether planning a visit to {city}, monitoring weather patterns, or satisfying curiosity about Japanese locations, the stream provides valuable real-time information.',
        f'<strong class="text-white">Why watch:</strong> This live camera at {camera_name} serves multiple purposes - trip planning, weather monitoring, or pure enjoyment of {city} from afar. The high-quality stream reveals details that photos and recorded video cannot capture.',
    ]

    para4_templates = [
        f'<strong class="text-white">Best viewing times:</strong> Early morning (6:00-8:00 JST) for serene atmosphere and soft lighting, midday (11:00-14:00 JST) for maximum activity, golden hour (17:00-19:00 JST) for beautiful light, and evening (19:00-23:00 JST) for illuminated scenes and nightlife.',
        f'<strong class="text-white">Recommended times:</strong> Dawn (5:30-7:00 JST) to see the day awakening, peak hours (12:00-15:00 JST) for bustling activity, sunset period (17:00-18:30 JST) for dramatic colors, and night hours (20:00-24:00 JST) when artificial lighting creates atmosphere.',
        f'<strong class="text-white">Optimal viewing:</strong> Morning rush (7:00-9:00 JST) for commuter activity, afternoon (13:00-16:00 JST) for casual exploration, pre-evening (16:30-18:30 JST) for transitional lighting, and late night (21:00-01:00 JST) for a different perspective on {city}.',
    ]

    # Use hash to consistently select same templates for each camera
    para2 = para2_templates[hash(camera_name + '2') % len(para2_templates)]
    para3 = para3_templates[hash(camera_name + '3') % len(para3_templates)]
    para4 = para4_templates[hash(camera_name + '4') % len(para4_templates)]

    description = f'''                    <div class="text-gray-300 space-y-3 mb-4">
                        <p>{para1}</p>

                        <p>{para2}</p>

                        <p>{para3}</p>

                        <p>{para4}</p>
                    </div>'''

    return description

def update_camera_description(file_path):
    """Update a camera page with unique description."""
    filename = os.path.basename(file_path)

    # Skip tokyo-tower.html as it already has custom description
    if filename == 'tokyo-tower.html':
        return False, "already custom"

    print(f"Processing: {filename}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract camera info
    extractor = CameraInfoExtractor()
    extractor.feed(content)

    if not extractor.camera_name or not extractor.city:
        print(f"  ⚠️  Could not extract name/city")
        return False, "parse error"

    camera_name = extractor.camera_name
    city = extractor.city
    location_type = get_location_type(camera_name.lower())

    # Check if already has custom description (not the template)
    if 'Experience the vibrant atmosphere of' not in content:
        print(f"  ⏭️  Already has custom description")
        return False, "already custom"

    # Create unique description
    new_desc = create_unique_description(camera_name, city, location_type)

    # Find and replace the old description
    old_pattern = r'<div class="text-gray-300 space-y-3 mb-4">.*?</div>'

    match = re.search(old_pattern, content, re.DOTALL)
    if not match:
        print(f"  ⚠️  Could not find description block")
        return False, "no match"

    content = re.sub(old_pattern, new_desc, content, count=1, flags=re.DOTALL)

    # Write updated content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  ✅ Updated ({location_type} type)")
    return True, location_type

def main():
    camera_files = glob.glob('/home/user/sakuralivecams/cameras/*.html')
    camera_files = [f for f in camera_files if not os.path.basename(f).startswith('index')]

    print(f"Found {len(camera_files)} camera pages\n")

    updated_count = 0
    skipped_count = 0
    type_counts = {}

    for file_path in sorted(camera_files):
        try:
            success, result = update_camera_description(file_path)
            if success:
                updated_count += 1
                type_counts[result] = type_counts.get(result, 0) + 1
            else:
                skipped_count += 1
        except Exception as e:
            print(f"  ❌ Error: {e}")
            skipped_count += 1
        print()

    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Updated: {updated_count}")
    print(f"  Skipped: {skipped_count}")
    print(f"  Total:   {len(camera_files)}")
    print(f"\nLocation Types:")
    for loc_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {loc_type}: {count}")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
