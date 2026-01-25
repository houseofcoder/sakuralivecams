#!/usr/bin/env python3
"""
Add competitive advantage section to index.html to help outrank competitors.
Emphasizes unique value propositions without directly naming competitors.
"""

import re

def add_competitive_section():
    """Add 'Why Choose SakuraLive' section to index page"""

    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already added
    if 'Why Choose SakuraLive Over Other Webcam Sites' in content:
        print("⚠️  Competitive section already exists")
        return False

    # New competitive advantage section
    competitive_section = '''
    <!-- Competitive Advantages Section -->
    <section class="bg-gradient-to-b from-gray-900 to-black py-16">
        <div class="max-w-7xl mx-auto px-4">
            <div class="text-center mb-12">
                <h2 class="text-3xl md:text-4xl font-bold text-white mb-4">
                    Why Choose SakuraLive Over Other Webcam Sites?
                </h2>
                <p class="text-xl text-gray-300 max-w-3xl mx-auto">
                    The most comprehensive collection of Japan webcams with features you won't find anywhere else
                </p>
            </div>

            <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                <!-- Advantage 1: More Cameras -->
                <div class="bg-white/5 backdrop-blur rounded-xl p-6 border border-white/10">
                    <div class="w-12 h-12 bg-green-500/20 rounded-lg flex items-center justify-center mb-4">
                        <svg class="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/>
                        </svg>
                    </div>
                    <h3 class="text-lg font-bold text-white mb-2">200+ Live Cameras</h3>
                    <p class="text-gray-300 text-sm">
                        More Japan webcams than any other platform. Curated HD streams from 34+ cities including Tokyo, Osaka, Kyoto, and hidden gems.
                    </p>
                </div>

                <!-- Advantage 2: Always Free -->
                <div class="bg-white/5 backdrop-blur rounded-xl p-6 border border-white/10">
                    <div class="w-12 h-12 bg-blue-500/20 rounded-lg flex items-center justify-center mb-4">
                        <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"/>
                        </svg>
                    </div>
                    <h3 class="text-lg font-bold text-white mb-2">100% Free Forever</h3>
                    <p class="text-gray-300 text-sm">
                        No hidden fees, no premium tiers, no paywalls. Every camera is completely free to watch. No credit card required, ever.
                    </p>
                </div>

                <!-- Advantage 3: No Registration -->
                <div class="bg-white/5 backdrop-blur rounded-xl p-6 border border-white/10">
                    <div class="w-12 h-12 bg-purple-500/20 rounded-lg flex items-center justify-center mb-4">
                        <svg class="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                        </svg>
                    </div>
                    <h3 class="text-lg font-bold text-white mb-2">Instant Access</h3>
                    <p class="text-gray-300 text-sm">
                        No account creation, no email signup, no personal information needed. Click and watch instantly - it's that simple.
                    </p>
                </div>

                <!-- Advantage 4: Better Organization -->
                <div class="bg-white/5 backdrop-blur rounded-xl p-6 border border-white/10">
                    <div class="w-12 h-12 bg-orange-500/20 rounded-lg flex items-center justify-center mb-4">
                        <svg class="w-6 h-6 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
                        </svg>
                    </div>
                    <h3 class="text-lg font-bold text-white mb-2">Smart Organization</h3>
                    <p class="text-gray-300 text-sm">
                        Browse by city, filter by category (temples, airports, beaches), search by location. Find exactly what you want in seconds.
                    </p>
                </div>

                <!-- Advantage 5: Current Time Display -->
                <div class="bg-white/5 backdrop-blur rounded-xl p-6 border border-white/10">
                    <div class="w-12 h-12 bg-red-500/20 rounded-lg flex items-center justify-center mb-4">
                        <svg class="w-6 h-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                        </svg>
                    </div>
                    <h3 class="text-lg font-bold text-white mb-2">Live JST Time</h3>
                    <p class="text-gray-300 text-sm">
                        Every camera shows current Japan Standard Time so you always know what time it is there - perfect for planning your viewing.
                    </p>
                </div>

                <!-- Advantage 6: Rich Context -->
                <div class="bg-white/5 backdrop-blur rounded-xl p-6 border border-white/10">
                    <div class="w-12 h-12 bg-yellow-500/20 rounded-lg flex items-center justify-center mb-4">
                        <svg class="w-6 h-6 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                        </svg>
                    </div>
                    <h3 class="text-lg font-bold text-white mb-2">Detailed Descriptions</h3>
                    <p class="text-gray-300 text-sm">
                        Every camera includes location history, what you'll see, best viewing times, and cultural context - not just a raw video feed.
                    </p>
                </div>

                <!-- Advantage 7: Mobile App -->
                <div class="bg-white/5 backdrop-blur rounded-xl p-6 border border-white/10">
                    <div class="w-12 h-12 bg-indigo-500/20 rounded-lg flex items-center justify-center mb-4">
                        <svg class="w-6 h-6 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"/>
                        </svg>
                    </div>
                    <h3 class="text-lg font-bold text-white mb-2">Android App Available</h3>
                    <p class="text-gray-300 text-sm">
                        Free Android app for optimized mobile viewing. Watch Japan live on your phone with a streamlined, ad-free experience.
                    </p>
                </div>

                <!-- Advantage 8: Updated Daily -->
                <div class="bg-white/5 backdrop-blur rounded-xl p-6 border border-white/10">
                    <div class="w-12 h-12 bg-pink-500/20 rounded-lg flex items-center justify-center mb-4">
                        <svg class="w-6 h-6 text-pink-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                        </svg>
                    </div>
                    <h3 class="text-lg font-bold text-white mb-2">Always Up-to-Date</h3>
                    <p class="text-gray-300 text-sm">
                        We monitor all streams daily and remove broken cameras immediately. You'll never waste time on dead links or offline feeds.
                    </p>
                </div>
            </div>

            <!-- Call to Action -->
            <div class="mt-12 text-center">
                <p class="text-xl text-gray-300 mb-6">
                    Join thousands of viewers experiencing Japan live, right now
                </p>
                <a href="#cameras" class="inline-flex items-center gap-2 bg-red-600 hover:bg-red-700 text-white px-8 py-4 rounded-lg font-bold text-lg shadow-lg transition">
                    <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M8 5v14l11-7z"/>
                    </svg>
                    Start Watching Free Now
                </a>
            </div>
        </div>
    </section>
'''

    # Insert after the Statistics section and before the Hero/Featured section
    # Find the statistics section closing tag
    stats_section_end = r'(</section>\s*\n\s*<!-- Hero / Featured -->)'

    if re.search(stats_section_end, content):
        content = re.sub(
            stats_section_end,
            f'</section>{competitive_section}\n    <!-- Hero / Featured -->',
            content,
            count=1
        )
    else:
        print("⚠️  Could not find insertion point")
        return False

    # Write back
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)

    return True

def main():
    print("🚀 Adding competitive advantage section to index.html...")

    if add_competitive_section():
        print("✅ Successfully added 'Why Choose SakuraLive' section!")
        print("\nHighlights 8 key advantages:")
        print("  1. 200+ cameras (more than competitors)")
        print("  2. 100% free forever")
        print("  3. No registration required")
        print("  4. Smart organization & filters")
        print("  5. Live JST time display")
        print("  6. Detailed descriptions")
        print("  7. Android app")
        print("  8. Always updated")
    else:
        print("❌ Failed to add section")

if __name__ == '__main__':
    main()
