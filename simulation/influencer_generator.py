"""Procedural generation of synthetic influencer profiles."""

from __future__ import annotations

import math
import random as _random
from typing import Any

from config import NICHES, PLATFORMS

# ── Name data ────────────────────────────────────────────────────────────

FIRST_NAMES = [
    # Western
    "Emma", "Liam", "Olivia", "Noah", "Ava", "Ethan", "Sophia", "Mason",
    "Isabella", "Logan", "Mia", "Lucas", "Charlotte", "Aiden", "Amelia",
    "Jackson", "Harper", "Sebastian", "Evelyn", "Mateo", "Abigail", "Jack",
    "Emily", "Owen", "Ella", "Alexander", "Scarlett", "Daniel", "Grace",
    "Henry", "Chloe", "Michael", "Zoey", "Benjamin", "Lily", "James",
    "Hannah", "Elijah", "Nora", "William", "Riley", "Caleb", "Aria",
    "Nathan", "Luna", "Ryan", "Stella", "Dylan", "Hazel", "Leo",
    # Hispanic/Latin
    "Sofia", "Diego", "Valentina", "Carlos", "Camila", "Miguel", "Lucia",
    "Alejandro", "Gabriela", "Rafael", "Mariana", "Andres", "Daniela",
    "Santiago", "Isabella", "Matias", "Renata", "Pablo", "Fernanda", "Javier",
    # Asian
    "Yuki", "Haruto", "Sakura", "Kai", "Mei", "Riku", "Hana", "Sora",
    "Jin", "Min", "Seo", "Hyun", "Joon", "Yuna", "Tae",
    "Priya", "Arjun", "Ananya", "Rohan", "Diya", "Vivaan", "Aisha",
    "Wei", "Xin", "Lian", "Jing", "Chen", "Rui", "Zara",
    # African / Middle Eastern
    "Amara", "Kwame", "Nia", "Jabari", "Zuri", "Kofi", "Aaliyah",
    "Omari", "Imani", "Tariq", "Fatima", "Hassan", "Leila", "Omar",
    "Amira", "Malik", "Kaia", "Idris", "Nadia", "Rashid",
    # Mixed / Modern
    "Jordan", "Taylor", "Morgan", "Casey", "Quinn", "Avery", "Sage",
    "Blake", "Reese", "Parker", "Skyler", "Rowan", "Finley", "River",
    "Emery", "Lennox", "Harley", "Phoenix", "Kai", "Briar",
    # Additional diversity
    "Ingrid", "Lars", "Freya", "Sven", "Astrid", "Erik", "Bianca",
    "Marco", "Chiara", "Luca", "Elena", "Nikolai", "Anya", "Dmitri",
    "Katya", "Pierre", "Celine", "Hugo", "Isla", "Declan",
    "Sienna", "Callum", "Ivy", "Theo", "Maren", "Felix", "Clara",
    "Oscar", "Violet", "Ezra", "Iris", "Jasper", "Wren", "Atlas",
    "Ember", "Orion", "Nova", "Bodhi", "Juniper", "Cruz",
    "Talia", "Remy", "Elise", "Knox", "Margot", "Brooks", "Sloane",
    "Barrett", "Gemma", "Hayes", "Colette", "Sterling", "Blythe", "Crew",
]

LAST_NAMES = [
    # English
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Anderson", "Taylor", "Thomas",
    "Wilson", "Moore", "Jackson", "Martin", "Lee", "Thompson", "White",
    "Harris", "Clark", "Lewis", "Robinson", "Walker", "Young", "Allen",
    "King", "Wright", "Scott", "Hill", "Green", "Adams", "Baker",
    "Nelson", "Carter", "Mitchell", "Perez", "Roberts", "Turner",
    # Hispanic
    "Hernandez", "Lopez", "Gonzalez", "Rivera", "Ramirez", "Torres",
    "Flores", "Gomez", "Sanchez", "Morales", "Castillo", "Reyes",
    "Ortiz", "Delgado", "Vargas", "Mendoza", "Guerrero", "Silva",
    # Asian
    "Kim", "Nguyen", "Chen", "Wang", "Li", "Zhang", "Liu", "Huang",
    "Park", "Choi", "Tanaka", "Yamamoto", "Sato", "Nakamura", "Suzuki",
    "Patel", "Singh", "Kumar", "Shah", "Gupta", "Sharma",
    # African / Middle Eastern
    "Ibrahim", "Mohammed", "Ali", "Hassan", "Ahmed", "Okafor", "Mensah",
    "Diallo", "Osei", "Achebe", "Mbeki", "Okeke",
    # European
    "Mueller", "Schmidt", "Fischer", "Weber", "Larsson", "Johansson",
    "Rossi", "Bianchi", "Dubois", "Bernard", "Moreau", "Petrov",
    "Novak", "Kowalski", "Andersson", "Hansen", "Olsen",
    # Modern / compound-style
    "Bell", "Fox", "Cole", "Reed", "Stone", "Chase", "Blake", "Frost",
    "Cross", "Quinn", "Steele", "Wolfe", "Vance", "Lane", "Brooks",
    "Hayes", "Drake", "Vaughn", "Hale", "Dunn", "Marsh", "Dale",
    "West", "Holt", "Sage", "Wren", "Blair", "Kent", "Royce", "Vale",
]

# ── Niche-specific data ──────────────────────────────────────────────────

NICHE_HANDLE_WORDS = {
    "Fitness": ["fit", "gains", "strong", "flex", "grind", "sweat", "lift", "active", "health", "gym"],
    "Beauty": ["glam", "glow", "beauty", "skin", "lash", "style", "pretty", "radiant", "luxe", "bloom"],
    "Tech": ["tech", "dev", "code", "byte", "pixel", "hack", "geek", "digital", "cyber", "data"],
    "Food": ["eats", "chef", "taste", "yum", "cook", "bites", "flavor", "foodie", "kitchen", "feast"],
    "Lifestyle": ["life", "vibe", "daily", "living", "moments", "bliss", "chill", "soul", "zen", "flow"],
    "Fashion": ["style", "chic", "trend", "drip", "wear", "luxe", "mode", "haute", "threads", "look"],
    "Gaming": ["game", "play", "gg", "stream", "quest", "level", "pixel", "loot", "apex", "pro"],
    "Travel": ["travel", "roam", "wander", "explore", "globe", "nomad", "journey", "trek", "drift", "voyage"],
}

NICHE_BIO_TEMPLATES = {
    "Fitness": [
        "{cert}-certified trainer. {specialty} enthusiast. Helping {audience} get stronger.",
        "Personal trainer & {specialty} coach. {followers_m}+ community. Let's build together.",
        "Fitness creator sharing {specialty} tips & real results. {location} based.",
        "{specialty} | Nutrition | Mindset. Documenting the journey to my best self.",
        "Former athlete turned {specialty} coach. Real workouts, no shortcuts.",
        "Daily {specialty} content. Trainer to {followers_m}+ strong. DM for coaching.",
        "{specialty} lover. Plant-based athlete. Proving consistency > perfection.",
        "Movement is medicine. {specialty} routines, meal prep, & lifestyle.",
        "Building bodies and confidence through {specialty}. Collab inquiries: DM.",
        "Your favorite {specialty} creator. {cert} certified. Let's get after it.",
    ],
    "Beauty": [
        "Beauty obsessed. {specialty} tutorials & honest reviews. {location}.",
        "Licensed esthetician sharing {specialty} secrets. Skin first, makeup second.",
        "{specialty} creator. {followers_m}+ besties learning together.",
        "Clean beauty advocate. {specialty} tips for real people. Cruelty-free always.",
        "MUA & {specialty} enthusiast. Transformations are my love language.",
        "Your go-to for {specialty}. PR-friendly. Collabs: email in bio.",
        "Skincare nerd. {specialty} routines that actually work. No filters needed.",
        "{specialty} content daily. From drugstore to luxury. {location} based.",
        "Self-taught MUA. {specialty} tutorials & product hauls. {followers_m}+ fam.",
        "Helping you glow from the inside out. {specialty} & wellness tips.",
    ],
    "Tech": [
        "{specialty} reviewer & tech enthusiast. Honest takes on the latest gear.",
        "Software engineer by day, {specialty} creator by night. {location}.",
        "Breaking down {specialty} for everyone. {followers_m}+ nerds and counting.",
        "Tech journalist covering {specialty}. Hot takes & deep dives.",
        "{specialty} content creator. Unboxings, reviews, and tutorials.",
        "Making {specialty} accessible. No jargon, just clarity. {location} based.",
        "Full-time {specialty} creator. Building the future one video at a time.",
        "AI, {specialty}, and everything in between. The future is now.",
        "Your {specialty} sherpa. Reviews, comparisons, and real-world testing.",
        "Obsessed with {specialty}. {cert} background. Content that matters.",
    ],
    "Food": [
        "{specialty} recipes for busy people. {location} food scene explorer.",
        "Home cook turned {specialty} creator. {followers_m}+ foodies strong.",
        "{specialty} content daily. Restaurant reviews & recipes. {location}.",
        "Culinary school grad sharing {specialty} magic. Simple ingredients, big flavor.",
        "{specialty} creator. Eating my way through {location} one bite at a time.",
        "Recipe developer & {specialty} photographer. Cookbooks coming soon.",
        "Making {specialty} approachable. 30-minute meals that actually taste good.",
        "Food blogger. {specialty} recipes with a twist. PR-friendly.",
        "{specialty} & culture. Sharing stories through food. {location}.",
        "Self-taught chef. {specialty} videos that make you hungry. {followers_m}+ fam.",
    ],
    "Lifestyle": [
        "Living intentionally. {specialty}, wellness, and everyday joy. {location}.",
        "{specialty} & daily inspo. Creating a life I love. {followers_m}+ along for the ride.",
        "Content creator sharing {specialty}, home, and real talk. {location} based.",
        "Millennial navigating {specialty}, adulting, and everything in between.",
        "{specialty} creator. Morning routines, productivity, and good vibes only.",
        "Documenting life's little moments. {specialty} & honest conversations.",
        "{specialty} | Wellness | Growth. Building my dream life publicly.",
        "Your digital neighbor sharing {specialty} tips. Keeping it real since day one.",
        "Lifestyle curator. {specialty}, organization, and aesthetic living.",
        "{specialty} content for people who want more out of life. {location}.",
    ],
    "Fashion": [
        "Personal stylist & {specialty} creator. Looks for every budget. {location}.",
        "{specialty} content daily. Thrift finds to designer picks. {followers_m}+ fashionistas.",
        "Fashion buyer turned {specialty} creator. Industry insider tips.",
        "{specialty} & sustainable fashion advocate. Style doesn't have to cost the earth.",
        "Your {specialty} bestie. OOTDs, hauls, and try-ons. {location} based.",
        "Menswear / {specialty} creator. Elevating everyday style.",
        "{specialty} content. Street style meets high fashion. {location}.",
        "Closet minimalist. {specialty} capsule wardrobes & styling hacks.",
        "Fashion illustrator & {specialty} creator. Art meets style.",
        "{specialty} influencer. Runway to real way. Collabs welcome.",
    ],
    "Gaming": [
        "{specialty} streamer. Competitive & casual. Building a community.",
        "Full-time {specialty} content creator. {followers_m}+ gamers strong.",
        "{specialty} gameplay, reviews, and hot takes. GG only.",
        "Pro {specialty} player turned content creator. Tips & streams daily.",
        "Indie {specialty} enthusiast. Highlighting hidden gems you need to play.",
        "{specialty} & esports commentary. The plays that matter.",
        "Variety {specialty} streamer. Chill vibes, good games. {location}.",
        "Retro {specialty} collector & modern gamer. Best of both worlds.",
        "{specialty} tutorials, tier lists, and community events. Join the squad.",
        "Gaming creator covering {specialty}. News, reviews, and first looks.",
    ],
    "Travel": [
        "Exploring the world one {specialty} trip at a time. {location} home base.",
        "{specialty} travel creator. {followers_m}+ adventurers following along.",
        "Full-time traveler. {specialty} itineraries & hidden gems.",
        "Travel photographer capturing {specialty} moments. Currently in {location}.",
        "{specialty} travel on any budget. Tips, guides, and real experiences.",
        "Digital nomad. {specialty} content from wherever I wake up.",
        "Couple traveling the world. {specialty} adventures documented daily.",
        "{specialty} travel & culture. Going beyond the tourist trail.",
        "Adventure seeker. {specialty} destinations & outdoor exploration.",
        "Solo {specialty} traveler sharing honest guides. {followers_m}+ explorers.",
    ],
}

NICHE_SPECIALTIES = {
    "Fitness": ["HIIT", "yoga", "strength training", "calisthenics", "CrossFit",
                "running", "powerlifting", "Pilates", "martial arts", "bodybuilding",
                "functional fitness", "mobility", "cycling", "swimming"],
    "Beauty": ["skincare", "makeup", "haircare", "nail art", "fragrance",
               "anti-aging", "acne care", "K-beauty", "natural beauty", "brow styling",
               "lip art", "contouring", "color theory"],
    "Tech": ["smartphones", "laptops", "AI tools", "smart home", "PC building",
             "cameras", "wearables", "audio gear", "EVs", "drones",
             "VR/AR", "cybersecurity", "productivity apps"],
    "Food": ["vegan", "baking", "grilling", "meal prep", "street food",
             "Italian", "Asian fusion", "comfort food", "healthy eating", "desserts",
             "fermentation", "cocktails", "brunch"],
    "Lifestyle": ["minimalism", "productivity", "self-care", "home decor", "journaling",
                  "wellness", "mindfulness", "organization", "morning routines", "budgeting",
                  "plant care", "reading", "slow living"],
    "Fashion": ["streetwear", "vintage", "minimalist", "Y2K", "luxury",
                "athleisure", "workwear", "bohemian", "preppy", "avant-garde",
                "denim", "accessories", "sustainable fashion"],
    "Gaming": ["FPS", "RPG", "MOBA", "battle royale", "indie games",
               "retro gaming", "strategy", "simulation", "horror", "speedrunning",
               "MMO", "fighting games", "sandbox"],
    "Travel": ["budget", "luxury", "solo", "adventure", "cultural",
               "backpacking", "road trip", "island hopping", "city breaks", "eco-tourism",
               "food tourism", "photography", "van life"],
}

NICHE_CERTS = {
    "Fitness": ["NASM", "ACE", "ISSA", "NSCA", "ACSM", "CrossFit L2"],
    "Beauty": ["Licensed esthetician", "Cosmetology grad", "Dermatology researcher"],
    "Tech": ["CS degree", "AWS certified", "Ex-FAANG", "Engineering"],
    "Food": ["Culinary school", "Food science", "Nutrition certified", "Chef trained"],
    "Lifestyle": ["Psychology", "Certified coach", "Wellness certified"],
    "Fashion": ["FIT grad", "Fashion design", "Retail buyer", "Stylist certified"],
    "Gaming": ["Esports veteran", "Game dev", "Competitive ranked"],
    "Travel": ["Travel writer", "Tourism certified", "Hospitality background"],
}

NICHE_PARTNERSHIPS = {
    "Fitness": ["Nike", "Lululemon", "Gymshark", "Under Armour", "MyProtein",
                "Fitbit", "Peloton", "Reebok", "Adidas", "Hydro Flask",
                "Whoop", "Huel", "Optimum Nutrition", "Alo Yoga", "NOBULL"],
    "Beauty": ["Sephora", "Glossier", "Fenty Beauty", "Charlotte Tilbury", "NARS",
               "Drunk Elephant", "The Ordinary", "MAC", "Rare Beauty", "Tatcha",
               "CeraVe", "La Mer", "Olaplex", "Benefit", "Urban Decay"],
    "Tech": ["Samsung", "Apple", "Google", "Sony", "Logitech",
             "Razer", "Dell", "HP", "OnePlus", "Anker",
             "Nvidia", "AMD", "Bose", "JBL", "DJI"],
    "Food": ["HelloFresh", "Blue Apron", "KitchenAid", "Le Creuset", "Whole Foods",
             "Trader Joe's", "Vitamix", "Lodge", "Bob's Red Mill", "Oatly",
             "Beyond Meat", "Nespresso", "Instacart", "DoorDash"],
    "Lifestyle": ["Target", "IKEA", "Amazon", "Notion", "Calm",
                  "Headspace", "Canva", "Papier", "Muji", "The Container Store",
                  "Brooklinen", "Casper", "Dyson", "Rifle Paper Co."],
    "Fashion": ["Zara", "H&M", "ASOS", "Revolve", "Nordstrom",
                "Everlane", "Reformation", "Gucci", "Prada", "Nike",
                "Adidas", "Uniqlo", "Mango", "COS", "& Other Stories"],
    "Gaming": ["Razer", "SteelSeries", "HyperX", "Corsair", "Elgato",
               "Xbox", "PlayStation", "Nintendo", "Epic Games", "Steam",
               "Secretlab", "NZXT", "MSI", "ASUS ROG", "Logitech G"],
    "Travel": ["Airbnb", "Booking.com", "Expedia", "Away", "Samsonite",
               "GoPro", "DJI", "Lonely Planet", "Marriott", "Hilton",
               "Delta", "United", "National Geographic", "REI", "Osprey"],
}

LOCATIONS = [
    "Los Angeles, CA", "New York, NY", "Miami, FL", "Austin, TX",
    "Chicago, IL", "San Francisco, CA", "Seattle, WA", "Nashville, TN",
    "Denver, CO", "Atlanta, GA", "Portland, OR", "Dallas, TX",
    "San Diego, CA", "Boston, MA", "Phoenix, AZ", "Minneapolis, MN",
    "Detroit, MI", "Philadelphia, PA", "Las Vegas, NV", "Honolulu, HI",
    "London, UK", "Toronto, CA", "Vancouver, CA", "Sydney, AU",
    "Melbourne, AU", "Berlin, DE", "Paris, FR", "Amsterdam, NL",
    "Barcelona, ES", "Tokyo, JP", "Seoul, KR", "Singapore, SG",
    "Dubai, UAE", "Mumbai, IN", "Sao Paulo, BR", "Mexico City, MX",
    "Lagos, NG", "Cape Town, ZA", "Stockholm, SE", "Lisbon, PT",
]

# ── Handle patterns ──────────────────────────────────────────────────────

def _make_handle(first: str, last: str, niche: str, rng: _random.Random) -> str:
    """Generate a realistic social media handle."""
    niche_word = rng.choice(NICHE_HANDLE_WORDS.get(niche, ["creator"]))
    first_l = first.lower()
    last_l = last.lower()
    patterns = [
        f"@{first_l}{niche_word}",
        f"@{first_l}.{niche_word}",
        f"@{first_l}_{last_l}",
        f"@{first_l}{last_l[:3]}",
        f"@the{first_l}{niche_word}",
        f"@{first_l}.{last_l}",
        f"@{niche_word}{first_l}",
        f"@{first_l}{rng.randint(1, 99):02d}",
        f"@just{first_l}",
        f"@{first_l}.creates",
    ]
    return rng.choice(patterns)


def _make_bio(niche: str, specialty: str, location: str, followers: int, rng: _random.Random) -> str:
    """Generate a realistic bio from templates."""
    templates = NICHE_BIO_TEMPLATES.get(niche, NICHE_BIO_TEMPLATES["Lifestyle"])
    template = rng.choice(templates)
    cert = rng.choice(NICHE_CERTS.get(niche, ["Certified"]))
    followers_m = f"{followers / 1000:.0f}K" if followers < 1_000_000 else f"{followers / 1_000_000:.1f}M"
    return template.format(
        specialty=specialty,
        cert=cert,
        location=location,
        followers_m=followers_m,
        audience="people",
    )


# ── Main generator ───────────────────────────────────────────────────────

def generate_pool(n: int = 750, seed: int = 42) -> list[dict]:
    """Generate n synthetic influencer profiles as dicts.

    All influencers start with status='Pool' (undiscovered).
    Returns plain dicts for easy session-state storage.
    """
    rng = _random.Random(seed)
    pool: list[dict] = []
    used_handles: set[str] = set()

    for i in range(n):
        first = rng.choice(FIRST_NAMES)
        last = rng.choice(LAST_NAMES)
        niche = rng.choice(NICHES)
        platform = rng.choice(PLATFORMS)
        location = rng.choice(LOCATIONS)

        # Generate unique handle
        handle = _make_handle(first, last, niche, rng)
        attempt = 0
        while handle in used_handles and attempt < 10:
            handle = _make_handle(first, last, niche, rng)
            attempt += 1
        if handle in used_handles:
            handle = f"@{first.lower()}{last.lower()}{i}"
        used_handles.add(handle)

        # Follower count: log-normal distribution
        followers = int(10 ** rng.gauss(4.8, 0.6))
        followers = max(5_000, min(5_000_000, followers))

        # Engagement rate: inversely correlated with followers
        base_eng = 7.0 - 0.8 * math.log10(max(followers, 1))
        engagement_rate = round(max(0.5, min(8.0, base_eng + rng.gauss(0, 0.8))), 1)

        # Fit scores: normal distribution, correlated
        audience_fit = int(max(20, min(98, rng.gauss(62, 16))))
        brand_fit = int(max(20, min(98, audience_fit * 0.7 + rng.gauss(0, 10) + 20)))

        # Cost: function of followers and engagement
        cost_base = followers / 100 * (1 + engagement_rate / 5)
        estimated_cost = int(max(200, cost_base * rng.uniform(0.7, 1.3)))

        # Specialty and bio
        specialty = rng.choice(NICHE_SPECIALTIES.get(niche, ["general"]))
        bio = _make_bio(niche, specialty, location, followers, rng)

        # Past partnerships (0-4)
        all_brands = NICHE_PARTNERSHIPS.get(niche, [])
        n_partnerships = rng.choices([0, 1, 2, 3, 4], weights=[30, 25, 25, 15, 5])[0]
        partnerships = rng.sample(all_brands, min(n_partnerships, len(all_brands)))

        # Derived stats
        avg_likes = int(followers * engagement_rate / 100 * rng.uniform(0.6, 1.0))
        avg_comments = int(avg_likes * rng.uniform(0.02, 0.08))

        name = f"{first} {last}"

        pool.append({
            "name": name,
            "handle": handle,
            "platform": platform,
            "niche": niche,
            "followers": followers,
            "engagement_rate": engagement_rate,
            "audience_fit_score": audience_fit,
            "brand_fit_score": brand_fit,
            "estimated_cost": estimated_cost,
            "location": location,
            "status": "Pool",
            "bio": bio,
            "past_partnerships": partnerships,
            "avg_likes": avg_likes,
            "avg_comments": avg_comments,
            "recommendation_blurb": "",
            "revenue_generated": 0.0,
            "stage_entered_day": 0,
            "deal_value": 0.0,
            "content_posted_day": None,
            "discovered_day": None,
            "_pool_index": i,
        })

    return pool
