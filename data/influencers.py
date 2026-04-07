"""55 hand-crafted influencer profiles with realistic, internally consistent data."""

from __future__ import annotations

from schema import Influencer

# Pre-written recommendation blurbs for top-scored influencers (fallback when no API key)
RECOMMENDATION_BLURBS: dict[str, str] = {
    "@mayafitlife": (
        "Maya's fitness content consistently drives 5.2% engagement, well above the Instagram "
        "fitness average of 2.8%. Her audience skews 22-34 female, aligning closely with our "
        "target demographic. Previous Nike and Lululemon partnerships signal brand-tier alignment "
        "without direct competitor overlap."
    ),
    "@deshawntech": (
        "DeShawn's long-form tech reviews on YouTube average 320K views with an unusually high "
        "watch-through rate. His audience trusts his product recommendations -- affiliate "
        "conversion data from his Audible partnership shows 4.2x industry average click-through."
    ),
    "@priyacooks": (
        "Priya's recipe content generates exceptional save rates on Instagram, indicating high "
        "purchase intent from her audience. Her HelloFresh collaboration drove measurable "
        "subscription lifts. Estimated CPM is 40% below comparable food creators at her tier."
    ),
    "@alexlifestyle": (
        "Alex bridges lifestyle and wellness in a way that resonates with our core 25-34 demo. "
        "His engagement-to-follower ratio is in the top 5% for mid-tier lifestyle creators. "
        "Clean aesthetic and brand-safe content history reduce partnership risk."
    ),
    "@jennabeauty": (
        "Jenna's beauty tutorials drive high engagement and her audience overlaps 78% with our "
        "target customer profile. Her previous Glossier and Fenty campaigns delivered strong "
        "UGC that brands repurposed across paid channels -- dual value from one partnership."
    ),
    "@marcusfitpro": (
        "Marcus has built a highly engaged male fitness community that's underserved by most "
        "brand partnerships. His supplement and gear recommendations convert at 3.8x the "
        "category average. Strong candidate for our men's wellness vertical."
    ),
    "@sophiatravels": (
        "Sophia's travel content has an aspirational quality that drives high save-and-share "
        "rates. Her audience is affluent (est. HHI $95K+) and skews toward experience-driven "
        "purchases. She's a strong fit for premium product positioning."
    ),
    "@tikitoktara": (
        "Tara's TikTok content has gone viral 6 times in the past quarter, generating 12M+ "
        "organic impressions. Her comedic approach to fashion resonates with Gen Z audiences "
        "and her content style lends itself well to native brand integrations."
    ),
    "@chloefashion": (
        "Chloe's fashion content demonstrates sophisticated styling that attracts an older, "
        "higher-spending audience compared to typical fashion influencers. Her audience "
        "conversion rate on affiliate links is 2.3x the fashion category benchmark."
    ),
    "@ryanplayz": (
        "Ryan's gaming streams draw a loyal audience with above-average disposable income. "
        "His tech-adjacent content creates natural crossover opportunities. Past partnerships "
        "with Razer and HyperX show strong brand integration capabilities."
    ),
}


def _make(
    name, handle, platform, niche, followers, engagement, aud_fit, brand_fit,
    cost, location, status, bio, partnerships, revenue=0.0,
) -> dict:
    """Helper to build an influencer dict with computed fields."""
    avg_likes = int(followers * engagement / 100)
    avg_comments = int(avg_likes * 0.04)
    blurb = RECOMMENDATION_BLURBS.get(handle, "")
    return dict(
        name=name, handle=handle, platform=platform, niche=niche,
        followers=followers, engagement_rate=engagement,
        audience_fit_score=aud_fit, brand_fit_score=brand_fit,
        estimated_cost=cost, location=location, status=status,
        bio=bio, past_partnerships=partnerships,
        avg_likes=avg_likes, avg_comments=avg_comments,
        recommendation_blurb=blurb, revenue_generated=revenue,
    )


_RAW = [
    # ── Fitness (7) ───────────────────────────────────────────────────────
    _make("Maya Chen", "@mayafitlife", "Instagram", "Fitness", 285000, 5.2, 94, 88,
          3200, "Los Angeles, CA", "Qualified",
          "NASM-certified trainer sharing daily workouts and meal prep. 285K strong.",
          ["Nike", "Lululemon", "MyProtein"]),
    _make("Marcus Johnson", "@marcusfitpro", "YouTube", "Fitness", 520000, 3.8, 91, 85,
          6500, "Atlanta, GA", "Discovered",
          "Strength coach and supplement reviewer. Honest reviews, no BS.",
          ["Gymshark", "Optimum Nutrition"]),
    _make("Aisha Rahman", "@aabornefit", "TikTok", "Fitness", 145000, 6.1, 82, 79,
          1400, "Toronto, Canada", "Contacted",
          "Yoga and mobility flows. Making flexibility fun since 2021.",
          ["Alo Yoga", "Manduka"]),
    _make("Jake Torres", "@jaketorresfit", "Instagram", "Fitness", 92000, 4.8, 76, 72,
          900, "Miami, FL", "Contacted",
          "Calisthenics and bodyweight training. Park workout king.",
          ["TRX", "Rogue Fitness"]),
    _make("Samantha Lee", "@samleefitness", "YouTube", "Fitness", 1800000, 1.4, 70, 68,
          22000, "Sydney, Australia", "Discovered",
          "Full-body HIIT and challenges. 1.8M subscribers and counting.",
          ["Adidas", "Women's Best", "Fitbit"]),
    _make("Carlos Mendez", "@carlosfitmx", "TikTok", "Fitness", 340000, 5.5, 78, 74,
          2800, "Mexico City, Mexico", "Signed",
          "Functional fitness and boxing. Bilingual content creator.",
          ["Under Armour", "Everlast"], revenue=0.0),
    _make("Brittany Owens", "@brittfitjourney", "Instagram", "Fitness", 67000, 6.8, 72, 65,
          650, "Austin, TX", "Discovered",
          "Postpartum fitness recovery advocate. Real stories, real results.",
          ["Kindred Bravely"]),

    # ── Beauty (7) ────────────────────────────────────────────────────────
    _make("Jenna Park", "@jennabeauty", "Instagram", "Beauty", 410000, 4.6, 92, 90,
          4800, "New York, NY", "Qualified",
          "Clean beauty advocate and licensed esthetician. Ingredient deep-dives.",
          ["Glossier", "Fenty Beauty", "The Ordinary"]),
    _make("Destiny Williams", "@destinyglowup", "TikTok", "Beauty", 890000, 3.2, 80, 76,
          8500, "Houston, TX", "Converted",
          "Drugstore dupes and transformation videos. 890K followers love her energy.",
          ["e.l.f. Cosmetics", "Maybelline", "CeraVe"], revenue=34200.0),
    _make("Mei Lin Wu", "@meilinbeauty", "YouTube", "Beauty", 215000, 4.1, 85, 82,
          2600, "San Francisco, CA", "Contacted",
          "Asian beauty routines and skincare science. Bilingual EN/ZH content.",
          ["Tatcha", "COSRX", "Shiseido"]),
    _make("Olivia Russo", "@oliviarussobeauty", "Instagram", "Beauty", 178000, 3.9, 74, 80,
          2000, "Milan, Italy", "Discovered",
          "European luxury beauty and fragrance. Minimalist aesthetic.",
          ["Chanel", "Dior Beauty"]),
    _make("Tasha Brown", "@tashabeautytalks", "TikTok", "Beauty", 56000, 7.2, 68, 65,
          550, "Chicago, IL", "Discovered",
          "Textured hair care and inclusive beauty. Raw, honest reviews.",
          ["SheaMoisture", "Pattern Beauty"]),
    _make("Luna Kim", "@lunaskinlab", "Instagram", "Beauty", 325000, 4.3, 86, 84,
          3600, "Seoul, South Korea", "Negotiating",
          "K-beauty expert and product formulator. Science-first approach.",
          ["Laneige", "Sulwhasoo", "Drunk Elephant"]),
    _make("Rachel Green", "@rachelglam", "YouTube", "Beauty", 1200000, 1.8, 71, 69,
          15000, "London, UK", "Contacted",
          "Luxury hauls and red carpet recreations. 1.2M glamour enthusiasts.",
          ["Charlotte Tilbury", "MAC", "NARS"]),

    # ── Tech (7) ──────────────────────────────────────────────────────────
    _make("DeShawn Torres", "@deshawntech", "YouTube", "Tech", 680000, 3.6, 93, 87,
          8200, "San Jose, CA", "Qualified",
          "In-depth tech reviews and teardowns. Former Apple engineer.",
          ["Audible", "Dbrand", "NordVPN"]),
    _make("Ananya Patel", "@ananyatechie", "Twitter", "Tech", 125000, 2.4, 88, 83,
          1200, "Bangalore, India", "Contacted",
          "AI/ML thought leader and startup advisor. Sharp takes on emerging tech.",
          ["Google Cloud", "Notion"]),
    _make("Tyler Brooks", "@tylerbreaks", "TikTok", "Tech", 420000, 4.5, 79, 75,
          3800, "Seattle, WA", "Replied",
          "Making tech accessible. Gadget unboxings in 60 seconds or less.",
          ["Samsung", "Anker", "Peak Design"]),
    _make("Nina Volkov", "@ninavtech", "YouTube", "Tech", 95000, 5.1, 84, 78,
          1100, "Berlin, Germany", "Discovered",
          "Privacy and security focused tech reviewer. No sponsored compromises.",
          ["ProtonMail", "Framework Laptop"]),
    _make("James O'Brien", "@jtechio", "Twitter", "Tech", 210000, 2.1, 75, 71,
          1800, "Dublin, Ireland", "Contacted",
          "SaaS and developer tools commentary. CTO turned creator.",
          ["Linear", "Vercel", "Raycast"]),
    _make("Kevin Nguyen", "@kevinbuilds", "YouTube", "Tech", 3200000, 0.9, 65, 62,
          45000, "Austin, TX", "Discovered",
          "PC builds and gaming setups. 3.2M subscribers. Mr. Beast of tech.",
          ["Intel", "Corsair", "LG", "ASUS"]),
    _make("Sara Mitchell", "@saramitchtech", "Instagram", "Tech", 48000, 5.8, 80, 76,
          480, "Portland, OR", "Qualified",
          "Minimalist desk setups and productivity tools. Apple ecosystem focused.",
          ["Apple", "Bellroy"]),

    # ── Food (7) ──────────────────────────────────────────────────────────
    _make("Priya Sharma", "@priyacooks", "Instagram", "Food", 365000, 5.4, 95, 91,
          4000, "Mumbai, India", "Qualified",
          "Home cooking made beautiful. Indian fusion recipes with modern plating.",
          ["HelloFresh", "Le Creuset", "KitchenAid"]),
    _make("Marco DiNapoli", "@marcoeats", "TikTok", "Food", 720000, 4.2, 81, 78,
          7000, "New York, NY", "Signed",
          "NYC street food explorer and restaurant reviewer. First-bite reactions.",
          ["Uber Eats", "DoorDash", "Yelp"], revenue=0.0),
    _make("Emma Johansson", "@emmabakes", "YouTube", "Food", 195000, 4.7, 83, 80,
          2200, "Stockholm, Sweden", "Replied",
          "Sourdough obsessed. Nordic baking traditions with a modern twist.",
          ["KitchenAid", "Bob's Red Mill"]),
    _make("David Park", "@davidgrills", "Instagram", "Food", 110000, 3.8, 70, 73,
          1000, "Dallas, TX", "Contacted",
          "Weekend BBQ warrior. Brisket rankings and smoke ring science.",
          ["Traeger", "Meat Church"]),
    _make("Zara Okafor", "@zaracookslagos", "TikTok", "Food", 82000, 6.5, 74, 68,
          750, "Lagos, Nigeria", "Discovered",
          "West African cuisine for the world. Jollof rice diplomacy.",
          ["Knorr"]),
    _make("Amy Chen", "@amyeatsla", "Instagram", "Food", 440000, 3.6, 77, 75,
          4500, "Los Angeles, CA", "Converted",
          "LA food scene authority. Restaurant reviews and hidden gem finder.",
          ["American Express", "Resy", "Wine.com"], revenue=22500.0),
    _make("Thomas Weber", "@thomascooks", "YouTube", "Food", 58000, 5.9, 69, 66,
          580, "Munich, Germany", "Discovered",
          "German home cooking with a health twist. Farm-to-table advocate.",
          ["HelloFresh"]),

    # ── Lifestyle (7) ────────────────────────────────────────────────────
    _make("Alex Rivera", "@alexlifestyle", "Instagram", "Lifestyle", 310000, 4.9, 96, 89,
          3400, "Denver, CO", "Qualified",
          "Wellness, mindfulness, and everyday aesthetics. Clean living advocate.",
          ["Headspace", "Away Luggage", "Brooklinen"]),
    _make("Jessica Tran", "@jesstranlife", "TikTok", "Lifestyle", 540000, 4.1, 80, 77,
          5200, "Vancouver, Canada", "Negotiating",
          "Day-in-my-life content that makes productivity look effortless.",
          ["Notion", "Athletic Greens"]),
    _make("Daniel Kim", "@dankimlife", "YouTube", "Lifestyle", 870000, 2.6, 73, 70,
          9500, "Los Angeles, CA", "Contacted",
          "Vlogger, entrepreneur, and gear reviewer. The aspirational everyday.",
          ["Tesla", "Ridge Wallet", "Keeps"]),
    _make("Mia Thompson", "@miathompsonliving", "Instagram", "Lifestyle", 155000, 5.3, 85, 81,
          1800, "Nashville, TN", "Replied",
          "Southern living with modern style. Interior design meets daily routines.",
          ["West Elm", "Anthropologie"]),
    _make("Chris Walker", "@chriswalksdaily", "Twitter", "Lifestyle", 78000, 3.2, 66, 63,
          700, "London, UK", "Discovered",
          "Urban exploration and minimalist living. Walks through cities, talks about life.",
          ["Allbirds"]),
    _make("Lena Muller", "@lenamlife", "Instagram", "Lifestyle", 42000, 7.1, 71, 68,
          420, "Zurich, Switzerland", "Discovered",
          "Slow living and sustainability. Quality over quantity, always.",
          ["Patagonia"]),
    _make("Omar Hassan", "@omarliveswell", "TikTok", "Lifestyle", 260000, 4.4, 79, 76,
          2400, "Dubai, UAE", "Signed",
          "Luxury meets practical. Dubai lifestyle without the cringe.",
          ["Emirates", "Montblanc"], revenue=0.0),

    # ── Fashion (7) ───────────────────────────────────────────────────────
    _make("Chloe Dubois", "@chloefashion", "Instagram", "Fashion", 495000, 3.7, 90, 92,
          5500, "Paris, France", "Qualified",
          "Parisian street style and capsule wardrobe philosophy. Less is more.",
          ["Sezane", "Jacquemus", "The Frankie Shop"]),
    _make("Tara Singh", "@tikitoktara", "TikTok", "Fashion", 1500000, 2.2, 88, 86,
          18000, "Los Angeles, CA", "Negotiating",
          "Thrift flips and outfit challenges that go viral. 1.5M fashionistas.",
          ["SHEIN", "Zara", "Depop"]),
    _make("Nathan Brooks", "@nathanstreetwear", "Instagram", "Fashion", 230000, 3.4, 76, 79,
          2500, "London, UK", "Contacted",
          "Streetwear and sneaker culture. Drop alerts and fit checks.",
          ["Nike", "New Balance", "StockX"]),
    _make("Isabella Moreno", "@isabellamoreno", "YouTube", "Fashion", 165000, 4.0, 82, 84,
          1900, "Madrid, Spain", "Replied",
          "Sustainable fashion advocate. Ethical brand spotlights and styling tips.",
          ["Reformation", "Everlane", "Veja"]),
    _make("Kai Tanaka", "@kaitanakastyle", "Instagram", "Fashion", 88000, 4.6, 73, 77,
          850, "Tokyo, Japan", "Discovered",
          "Japanese minimalist fashion and avant-garde designers. East meets West.",
          ["Uniqlo", "Comme des Garcons"]),
    _make("Ashley Williams", "@ashwilliamsfashion", "TikTok", "Fashion", 375000, 3.9, 78, 75,
          3200, "New York, NY", "Content Posted",
          "NYC fashion week insider. Behind-the-scenes and trend forecasting.",
          ["Revolve", "Nordstrom", "Rent the Runway"], revenue=16800.0),
    _make("Leo Zhang", "@leostyled", "Instagram", "Fashion", 52000, 5.5, 67, 70,
          520, "Shanghai, China", "Discovered",
          "Menswear essentials and tailoring tips. Making suits cool for Gen Z.",
          ["Suitsupply"]),

    # ── Gaming (7) ────────────────────────────────────────────────────────
    _make("Ryan Park", "@ryanplayz", "YouTube", "Gaming", 950000, 2.8, 87, 83,
          11000, "Chicago, IL", "Qualified",
          "Competitive FPS streamer and tech reviewer. 950K loyal gamers.",
          ["Razer", "HyperX", "G Fuel"]),
    _make("Aria Chen", "@ariachengg", "TikTok", "Gaming", 620000, 3.5, 79, 74,
          6000, "San Francisco, CA", "Replied",
          "Cozy gaming and aesthetic setups. Making gaming wholesome since 2022.",
          ["Nintendo", "Secretlab"]),
    _make("Brandon White", "@brandonplayz", "YouTube", "Gaming", 2400000, 1.1, 64, 60,
          32000, "Dallas, TX", "Discovered",
          "Minecraft and Roblox content for younger audiences. 2.4M subscribers.",
          ["Epic Games", "Discord"]),
    _make("Yuki Sato", "@yukisatogames", "TikTok", "Gaming", 180000, 4.8, 75, 71,
          1700, "Tokyo, Japan", "Contacted",
          "JRPG specialist and retro gaming collector. Nostalgia with a modern twist.",
          ["Square Enix", "Analogue"]),
    _make("Sarah McDonald", "@sarahplaysit", "YouTube", "Gaming", 135000, 3.6, 80, 77,
          1500, "Dublin, Ireland", "Negotiating",
          "Indie game spotlight and developer interviews. The thinking gamer's channel.",
          ["Steam", "Humble Bundle"]),
    _make("Diego Ramirez", "@diegoRGG", "TikTok", "Gaming", 310000, 4.2, 72, 68,
          2800, "Buenos Aires, Argentina", "Content Posted",
          "Mobile gaming reviews and esports commentary. Bilingual EN/ES.",
          ["Riot Games", "HoYoverse"], revenue=14000.0),
    _make("Emily Watson", "@emilywgaming", "Twitter", "Gaming", 45000, 3.1, 63, 61,
          450, "Seattle, WA", "Discovered",
          "Game design commentary and industry analysis. Thoughtful takes.",
          ["Unity"]),

    # ── Travel (6) ────────────────────────────────────────────────────────
    _make("Sophia Laurent", "@sophiatravels", "Instagram", "Travel", 480000, 4.0, 93, 88,
          5200, "Barcelona, Spain", "Qualified",
          "Luxury and boutique travel with a conscience. 480K wanderlusters.",
          ["Marriott Bonvoy", "Away", "Airbnb"]),
    _make("Andre Jackson", "@andrejexplores", "YouTube", "Travel", 340000, 3.3, 78, 74,
          3600, "Cape Town, South Africa", "Signed",
          "Adventure travel and African tourism spotlight. Authentic cultural immersion.",
          ["National Geographic", "GoPro"], revenue=0.0),
    _make("Hannah Müller", "@hannahtravels", "TikTok", "Travel", 290000, 4.6, 81, 79,
          2600, "Vienna, Austria", "Replied",
          "Budget Europe travel tips and hidden gem spotlights. Travel smart, not expensive.",
          ["Hostelworld", "Skyscanner"]),
    _make("Raj Krishnan", "@rajwanders", "Instagram", "Travel", 155000, 3.7, 76, 72,
          1600, "Chennai, India", "Contacted",
          "South Asian travel and heritage sites. Photography-first storytelling.",
          ["Canon", "Lonely Planet"]),
    _make("Lily Chang", "@lilygoesglobal", "YouTube", "Travel", 720000, 2.5, 74, 70,
          7800, "Singapore", "Converted",
          "Southeast Asian food and travel series. 720K subscribers hungry for adventure.",
          ["Singapore Airlines", "Klook", "Agoda"], revenue=39000.0),
    _make("Tom Anderson", "@tomandersentravel", "Instagram", "Travel", 38000, 6.2, 68, 64,
          380, "Denver, CO", "Discovered",
          "National parks and van life. The great American road trip, documented.",
          ["REI"]),
]


def get_influencers() -> list[Influencer]:
    """Return all 55 influencer profiles as validated Pydantic objects."""
    return [Influencer(**d) for d in _RAW]
