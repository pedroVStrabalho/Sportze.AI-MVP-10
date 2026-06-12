# =============================================================================
# SPORTZE.AI - UNIVERSAL SPORT SYSTEM
# =============================================================================
# Put this file inside:
# training_catalog/universal_sport_system.py
#
# Purpose:
# - Covers sports that do not yet have a full Sportze fixed catalog file.
# - Contains 400 popular / commonly practiced sports and sport-like disciplines.
# - Labels each one as individual, team, combat, hybrid, or mind/precision.
# - Maps each one to the nearest Sportze fixed catalog sports.
#
# Later API upgrade:
# - The API can use "nearest_catalog_sports" as inspiration.
# - It can research the requested sport and then create a specific session.
# =============================================================================

from __future__ import annotations

from typing import Any, Dict, List, Optional
import random
import re


FIXED_CATALOG_SPORTS: List[str] = [
    "american football",
    "athletics",
    "baseball",
    "basketball",
    "box",
    "calisthenics",
    "cricket",
    "cycling",
    "golf",
    "gymnastics",
    "hockey",
    "martial arts",
    "rowing",
    "rugby",
    "soccer",
    "swimming",
    "table tennis",
    "tennis",
    "triathlon",
    "volleyball",
    "water polo",
    "weightlifting",
]


SPORT_NAMES: List[str] = ['Soccer', 'Cricket', 'Basketball', 'Tennis', 'Volleyball', 'Table Tennis', 'Baseball', 'Golf', 'American Football', 'Rugby Union', 'Rugby League', 'Badminton', 'Swimming', 'Athletics', 'Running', 'Cycling', 'Boxing', 'Martial Arts', 'Mixed Martial Arts', 'Karate', 'Taekwondo', 'Judo', 'Brazilian Jiu Jitsu', 'Wrestling', 'Kickboxing', 'Muay Thai', 'Fencing', 'Weightlifting', 'Powerlifting', 'Bodybuilding', 'Calisthenics', 'Gymnastics', 'Artistic Gymnastics', 'Rhythmic Gymnastics', 'Trampoline Gymnastics', 'Parkour', 'Rowing', 'Canoeing', 'Kayaking', 'Dragon Boat', 'Water Polo', 'Triathlon', 'Duathlon', 'Aquathlon', 'Modern Pentathlon', 'Handball', 'Field Hockey', 'Ice Hockey', 'Inline Hockey', 'Lacrosse', 'Softball', 'Rounders', 'Netball', 'Futsal', 'Beach Soccer', 'Beach Volleyball', 'Squash', 'Racquetball', 'Padel', 'Pickleball', 'Platform Tennis', 'Real Tennis', 'Polo', 'Equestrian', 'Dressage', 'Show Jumping', 'Eventing', 'Horse Racing', 'Archery', 'Shooting', 'Biathlon', 'Cross Country Skiing', 'Alpine Skiing', 'Freestyle Skiing', 'Ski Jumping', 'Nordic Combined', 'Snowboarding', 'Speed Skating', 'Short Track Speed Skating', 'Figure Skating', 'Curling', 'Bobsleigh', 'Skeleton', 'Luge', 'Surfing', 'Bodyboarding', 'Windsurfing', 'Kitesurfing', 'Sailing', 'Yachting', 'Stand Up Paddleboarding', 'Diving', 'Synchronized Swimming', 'Open Water Swimming', 'Freediving', 'Scuba Sport', 'Snorkeling', 'Underwater Hockey', 'Underwater Rugby', 'Fin Swimming', 'Skateboarding', 'Longboarding', 'Roller Skating', 'Inline Skating', 'BMX Racing', 'BMX Freestyle', 'Mountain Biking', 'Road Cycling', 'Track Cycling', 'Cyclocross', 'Gravel Cycling', 'Billiards', 'Snooker', 'Pool', 'Bowling', 'Ten Pin Bowling', 'Lawn Bowls', 'Bocce', 'Petanque', 'Darts', 'Chess Boxing', 'Esports', 'Ultimate Frisbee', 'Disc Golf', 'Flying Disc', 'Orienteering', 'Trail Running', 'Cross Country Running', 'Race Walking', 'Hurdles', 'Long Jump', 'High Jump', 'Triple Jump', 'Pole Vault', 'Shot Put', 'Discus Throw', 'Hammer Throw', 'Javelin Throw', 'Decathlon', 'Heptathlon', 'Sprint Canoe', 'Slalom Canoe', 'Surf Ski', 'Rafting', 'Sport Climbing', 'Bouldering', 'Lead Climbing', 'Speed Climbing', 'Mountaineering', 'Rock Climbing', 'Ice Climbing', 'Caving', 'Adventure Racing', 'Obstacle Course Racing', 'Spartan Race', 'Tough Mudder', 'CrossFit', 'Functional Fitness', 'Aerobics', 'Pilates', 'Yoga Sport', 'Cheerleading', 'DanceSport', 'Breaking', 'Ballet Fitness', 'Capoeira', 'Aikido', 'Kendo', 'Kenjutsu', 'Iaido', 'Kung Fu', 'Wushu', 'Sambo', 'Savate', 'Sumo', 'Greco Roman Wrestling', 'Freestyle Wrestling', 'Grappling', 'Submission Wrestling', 'Arm Wrestling', 'Strongman', 'Highland Games', 'Tug of War', 'Kabaddi', 'Kho Kho', 'Sepak Takraw', 'Teqball', 'Footvolley', 'Bossaball', 'Footbag', 'Gaelic Football', 'Hurling', 'Camogie', 'Australian Rules Football', 'Aussie Rules', 'Canadian Football', 'Flag Football', 'Touch Rugby', 'Tag Rugby', 'Rugby Sevens', 'Wheelchair Rugby', 'Wheelchair Basketball', 'Wheelchair Tennis', 'Wheelchair Racing', 'Para Swimming', 'Goalball', 'Boccia', 'Sitting Volleyball', 'Blind Football', 'Para Powerlifting', 'Climbing Para', 'Handcycling', 'Para Triathlon', 'Para Badminton', 'Para Table Tennis', 'Water Skiing', 'Wakeboarding', 'Barefoot Skiing', 'Jet Ski Racing', 'Powerboating', 'Rowing Coastal', 'Beach Sprint Rowing', 'Indoor Rowing', 'Erg Rowing', 'Indoor Cycling', 'Spin Cycling', 'Track Running', 'Road Running', 'Ultra Running', 'Mountain Running', 'Skyrunning', 'Fell Running', 'Snowshoe Running', 'Canicross', 'Dog Agility', 'Mushing', 'Sled Dog Racing', 'Equestrian Vaulting', 'Reining', 'Endurance Riding', 'Rodeo', 'Bull Riding', 'Barrel Racing', 'Tent Pegging', 'Mounted Games', 'Polo Crosse', 'Cycle Polo', 'Bike Polo', 'Canoe Polo', 'Elephant Polo', 'Pesapallo', 'Bandy', 'Floorball', 'Broomball', 'Ringette', 'Rink Hockey', 'Roller Hockey', 'Street Hockey', 'Shinty', 'Hurling Handball', 'Basque Pelota', 'Jai Alai', 'Pelota Mixteca', 'Frontenis', 'Tamburello', 'Tchoukball', 'Korfball', 'Kin Ball', 'Gateball', 'Croquet', 'Minigolf', 'Footgolf', 'Speed Golf', 'Urban Golf', 'Frisbee Golf', 'SlamBall', '3x3 Basketball', 'Streetball', 'Dodgeball', 'Paintball', 'Airsoft Sport', 'Laser Tag Sport', 'Capture the Flag Sport', 'Tag', 'Chase Tag', 'World Chase Tag', 'Freerunning', 'Stunt Tricking', 'Tricking', 'Acrobatics', 'Circus Arts', 'Aerial Silks', 'Aerial Hoop', 'Pole Sport', 'Slacklining', 'Highlining', 'Juggling Sport', 'Boomerang Throwing', 'Axe Throwing', 'Knife Throwing Sport', 'Sport Fishing', 'Fly Fishing', 'Casting Sport', 'Spearfishing', 'Competitive Lifesaving', 'Surf Lifesaving', 'Beach Flags', 'Oceanman', 'Swimrun', 'Aquabike', 'Canoe Marathon', 'Outrigger Canoeing', "Va'a", 'Paddle Tennis', 'Beach Tennis', 'Soft Tennis', 'Speed Badminton', 'Crossminton', 'Shuttleball', 'Matkot', 'Hand Tennis', 'Wallball', 'One Wall Handball', 'Four Wall Handball', 'Gaelic Handball', 'American Handball', 'Beach Handball', 'Wheelchair Handball', 'Indoor Soccer', 'Arena Football', 'Minifootball', 'Walking Football', 'Powerchair Football', 'Freestyle Football', 'Football Tennis', 'Footpool', 'Subbuteo', 'Table Football', 'Foosball', 'Air Hockey', 'Table Hockey', 'Table Shuffleboard', 'Shuffleboard', 'Carrom', 'Novuss', 'Crokinole', 'Go', 'Xiangqi', 'Shogi', 'Checkers', 'Bridge Sport', 'Poker Sport', 'Backgammon', 'Memory Sport', 'Speedcubing', 'Sport Stacking', "Rubik's Cube", 'Competitive Programming', 'Robot Soccer', 'Drone Racing', 'FPV Drone Racing', 'Model Aircraft Racing', 'RC Car Racing', 'Karting', 'Auto Racing', 'Formula Racing', 'Rally Racing', 'Drifting', 'Motorcycle Racing', 'Motocross', 'Supercross', 'Enduro', 'Trials', 'Speedway Motorcycle', 'Flat Track Racing', 'ATV Racing', 'Snowmobile Racing', 'Kart Slalom', 'Autocross', 'Hill Climb Racing', 'Powerlifting Bench Press', 'Deadlifting', 'Squat Competition', 'Olympic Lifting', 'Kettlebell Sport', 'Girevoy Sport', 'Stone Lifting', 'Mas Wrestling', 'Mace Sport', 'Club Swinging', 'Fitness Racing', 'Hyrox', 'Tri Fitness', 'Natural Movement', 'Animal Flow', 'Street Workout', 'Plank Sport', 'Push Up Contest', 'Pull Up Contest', 'Rope Climbing']


TEAM_KEYWORDS = [
    "soccer", "football", "basketball", "volleyball", "baseball", "softball",
    "rugby", "cricket", "hockey", "handball", "polo", "lacrosse", "netball",
    "kabaddi", "korfball", "tchoukball", "floorball", "bandy", "curling",
    "dodgeball", "ultimate", "quadball", "goalball", "sitting volleyball",
]

COMBAT_KEYWORDS = [
    "boxing", "box", "martial", "karate", "judo", "taekwondo", "jiu jitsu",
    "bjj", "wrestling", "mma", "kickboxing", "muay thai", "fencing", "sambo",
    "sumo", "grappling", "combat", "pankration", "silat", "arnis", "kendo",
]

PRECISION_OR_MIND_KEYWORDS = [
    "golf", "archery", "shooting", "darts", "billiards", "snooker", "pool",
    "bowling", "chess", "go", "shogi", "bridge", "poker", "backgammon",
    "memory", "speedcubing", "stacking", "carrom", "crokinole",
]

WATER_KEYWORDS = [
    "swimming", "water", "surf", "diving", "canoe", "kayak", "rowing",
    "paddle", "sailing", "wakeboarding", "freediving", "snorkeling",
    "lifesaving", "ocean", "aquathlon", "aquabike", "swimrun",
]

RACKET_KEYWORDS = [
    "tennis", "badminton", "squash", "racquet", "padel", "pickleball",
    "table tennis", "ping pong", "pelota", "frontenis", "crossminton",
]

CYCLING_KEYWORDS = [
    "cycling", "biking", "bike", "bmx", "cyclocross", "handcycling",
]

GYMNASTIC_KEYWORDS = [
    "gymnastics", "trampoline", "parkour", "freerunning", "acrobatics",
    "aerial", "cheer", "dance", "breaking", "tricking", "tumbling",
]

STRENGTH_KEYWORDS = [
    "weightlifting", "powerlifting", "bodybuilding", "strongman", "kettlebell",
    "crossfit", "fitness", "hyrox", "calisthenics", "street workout",
    "push up", "pull up", "deadlifting", "squat", "bench",
]

ENDURANCE_KEYWORDS = [
    "running", "athletics", "triathlon", "duathlon", "marathon", "trail",
    "cross country", "race walking", "skyrunning", "orienteering",
]


def normalize_text(value: str) -> str:
    value = (value or "").strip().lower()
    value = value.replace("_", " ").replace("-", " ")
    value = re.sub(r"[^a-z0-9\s]", "", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def _contains_any(text: str, keywords: List[str]) -> bool:
    return any(keyword in text for keyword in keywords)


def classify_sport_type(sport: str) -> str:
    text = normalize_text(sport)

    if _contains_any(text, COMBAT_KEYWORDS):
        return "Combat Sport"

    if _contains_any(text, TEAM_KEYWORDS):
        return "Team Sport"

    if _contains_any(text, PRECISION_OR_MIND_KEYWORDS):
        return "Precision / Mind Sport"

    if any(word in text for word in ["relay", "team", "doubles", "mixed"]):
        return "Hybrid Sport"

    return "Individual Sport"


def nearest_catalog_sports(sport: str) -> List[str]:
    text = normalize_text(sport)
    nearest: List[str] = []

    def add(*sports: str) -> None:
        for item in sports:
            if item not in nearest:
                nearest.append(item)

    if _contains_any(text, RACKET_KEYWORDS):
        if "table" in text or "ping" in text:
            add("table tennis", "tennis")
        else:
            add("tennis", "table tennis")

    if _contains_any(text, TEAM_KEYWORDS):
        if "basket" in text:
            add("basketball", "volleyball")
        elif "volley" in text:
            add("volleyball", "basketball")
        elif "base" in text or "softball" in text or "cricket" in text:
            add("baseball", "cricket")
        elif "rugby" in text or "football" in text or "gridiron" in text:
            add("rugby", "american football", "soccer")
        elif "hockey" in text:
            add("hockey", "soccer")
        elif "water polo" in text or "polo" in text:
            add("water polo", "swimming", "rugby")
        else:
            add("soccer", "basketball", "rugby")

    if _contains_any(text, WATER_KEYWORDS):
        if "rowing" in text or "canoe" in text or "kayak" in text or "paddle" in text:
            add("rowing", "swimming")
        elif "water polo" in text:
            add("water polo", "swimming")
        else:
            add("swimming", "triathlon")

    if _contains_any(text, CYCLING_KEYWORDS):
        add("cycling", "triathlon")

    if _contains_any(text, GYMNASTIC_KEYWORDS):
        add("gymnastics", "calisthenics")

    if _contains_any(text, STRENGTH_KEYWORDS):
        if "bodyweight" in text or "calisthenics" in text or "street workout" in text:
            add("calisthenics", "gymnastics")
        else:
            add("weightlifting", "calisthenics")

    if _contains_any(text, ENDURANCE_KEYWORDS):
        if "triathlon" in text or "duathlon" in text or "aquathlon" in text:
            add("triathlon", "cycling", "swimming", "athletics")
        else:
            add("athletics", "triathlon", "cycling")

    if _contains_any(text, COMBAT_KEYWORDS):
        if "box" in text:
            add("box", "martial arts")
        else:
            add("martial arts", "box", "calisthenics")

    if _contains_any(text, PRECISION_OR_MIND_KEYWORDS):
        if "golf" in text:
            add("golf", "calisthenics")
        elif "bowling" in text or "darts" in text or "archery" in text or "shooting" in text:
            add("golf", "table tennis", "calisthenics")
        else:
            add("table tennis", "golf")

    if not nearest:
        add("athletics", "calisthenics", "gymnastics")

    return nearest[:5]


def build_sport_database() -> Dict[str, Dict[str, Any]]:
    database: Dict[str, Dict[str, Any]] = {}

    for sport in SPORT_NAMES:
        normalized = normalize_text(sport)
        database[normalized] = {
            "sport": sport,
            "sport_type": classify_sport_type(sport),
            "nearest_catalog_sports": nearest_catalog_sports(sport),
        }

    return database


UNIVERSAL_SPORT_DATABASE: Dict[str, Dict[str, Any]] = build_sport_database()


ALIASES: Dict[str, str] = {
    "ping pong": "table tennis",
    "football": "soccer",
    "american football": "american football",
    "gridiron": "american football",
    "bjj": "brazilian jiu jitsu",
    "mma": "mixed martial arts",
    "bike": "cycling",
    "biking": "cycling",
    "run": "running",
    "jogging": "running",
    "boxing": "boxing",
    "box": "boxing",
}


def get_universal_sport_profile(sport: str) -> Dict[str, Any]:
    requested = normalize_text(sport)

    if requested in ALIASES:
        requested = normalize_text(ALIASES[requested])

    if requested in UNIVERSAL_SPORT_DATABASE:
        return UNIVERSAL_SPORT_DATABASE[requested]

    # fuzzy lookup
    for key, profile in UNIVERSAL_SPORT_DATABASE.items():
        if requested in key or key in requested:
            return profile

    # unknown sport: still return a usable profile
    return {
        "sport": sport.strip().title() if sport else "Unknown Sport",
        "sport_type": classify_sport_type(sport),
        "nearest_catalog_sports": nearest_catalog_sports(sport),
    }


def normalize_level(level: Optional[str], goal: Optional[str] = None) -> str:
    text = normalize_text(f"{level or ''} {goal or ''}")

    if "learn how to play" in text or "never played" in text or "start" in text:
        return "Never Played Before"
    if "elite" in text:
        return "Elite"
    if "advanced" in text:
        return "Advanced"
    if "intermediate" in text:
        return "Intermediate"
    return "Beginner"


def normalize_training_alone(value: Optional[Any]) -> bool:
    if isinstance(value, bool):
        return value

    text = normalize_text(str(value or ""))

    if text in {"no", "group", "team", "with others", "with a team", "false", "0"}:
        return False

    return True


def _session_duration(level: str, session_type: Optional[str]) -> int:
    base = {
        "Never Played Before": 40,
        "Beginner": 55,
        "Intermediate": 70,
        "Advanced": 85,
        "Elite": 100,
    }.get(level, 55)

    if normalize_text(session_type or "") == "recovery":
        base -= 10
    if normalize_text(session_type or "") == "intense":
        base += 10

    return max(35, base)


def _primary_focus(session_type: Optional[str]) -> str:
    text = normalize_text(session_type or "balanced")

    if text == "technical":
        return "technical quality, clean repetitions, and control"
    if text == "physical":
        return "strength, speed, endurance, and movement quality"
    if text == "intense":
        return "high-intensity sport actions under fatigue"
    if text == "tactical":
        return "decision-making, timing, positioning, and game understanding"
    if text == "recovery":
        return "low-load movement, mobility, and technique quality"

    return "balanced technical and physical development"


def generate_universal_session(
    sport: str,
    goal: Optional[str] = None,
    level: Optional[str] = None,
    training_alone: Optional[Any] = None,
    session_type: Optional[str] = "balanced",
    seed: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Create a safe fallback session for any sport.

    This is not meant to replace the full researched catalog.
    It keeps Sportze working until the API can research the sport deeply.
    """

    profile = get_universal_sport_profile(sport)
    fixed_level = normalize_level(level, goal)
    alone = normalize_training_alone(training_alone)
    duration = _session_duration(fixed_level, session_type)
    focus = _primary_focus(session_type)
    similar = profile["nearest_catalog_sports"]
    sport_type = profile["sport_type"]

    rng = random.Random(seed)

    if sport_type == "Team Sport":
        tactical_block = "Sport block: 4 x 5 min repeated game-like actions: movement, pass/receive timing, spacing, and defensive recovery."
        people = "1 athlete with targets, or 2+ athletes if available"
    elif sport_type == "Combat Sport":
        tactical_block = "Sport block: 6 x 2 min controlled rounds of stance, footwork, guard, entry, exit, and basic combinations."
        people = "1 athlete shadow work, or partner/coach if available"
    elif sport_type == "Precision / Mind Sport":
        tactical_block = "Sport block: 6 rounds of target practice, routine rehearsal, focus reset, and accuracy under light fatigue."
        people = "1 athlete"
    else:
        tactical_block = "Sport block: 5 x 4 min repeated sport-specific movement patterns with clean technique and controlled effort."
        people = "1 athlete or group"

    if not alone and sport_type != "Individual Sport":
        format_value = "group"
    elif not alone:
        format_value = "flexible"
    else:
        format_value = "solo"

    session_variation = rng.choice(["base", "control", "performance"])

    return {
        "id": f"universal_{normalize_text(profile['sport']).replace(' ', '_')}_{session_variation}",
        "sport": profile["sport"],
        "sport_type": sport_type,
        "level": fixed_level,
        "format": format_value,
        "solo_allowed": True,
        "group_allowed": sport_type in {"Team Sport", "Combat Sport", "Hybrid Sport"},
        "training_alone_default": alone,
        "duration_min": duration,
        "title": f"{profile['sport']} Universal {fixed_level} {(session_type or 'Balanced').title()} Session",
        "objective": f"Build {focus} using inspiration from: {', '.join(similar)}.",
        "equipment": "sport equipment if available, open space, cones/markers, timer, water bottle",
        "people": people,
        "nearest_catalog_sports": similar,
        "api_future_note": "Future API can research this sport and generate a more specific session using the nearest catalog sports as inspiration.",
        "training_blocks": [
            "Warm-up: 10 min light cardio, mobility, joint preparation, and easy sport movements.",
            "Technique block: 4 rounds of 6-10 clean repetitions of the safest basic skill pattern for this sport.",
            "Movement block: 4 rounds of agility, balance, coordination, acceleration, deceleration, or rhythm work.",
            tactical_block,
            "Conditioning block: 3 rounds of 30 sec work + 30 sec rest using sport-like movements.",
            "Cooldown: 5-8 min easy movement, stretching, breathing, and notes on what improved.",
        ],
        "coach_cues": [
            "Start with control before speed.",
            "Keep the movements pain-free.",
            "Use the nearest catalog sports as training inspiration, not as exact copies.",
            "Increase complexity first, then speed, then fatigue.",
        ],
        "progression": "When the athlete can complete the session with clean technique, increase decision pressure or sport specificity before increasing intensity.",
    }


def get_all_universal_sports() -> List[str]:
    return [profile["sport"] for profile in UNIVERSAL_SPORT_DATABASE.values()]


def search_universal_sports(query: str, limit: int = 20) -> List[Dict[str, Any]]:
    q = normalize_text(query)
    results = []

    for key, profile in UNIVERSAL_SPORT_DATABASE.items():
        if q in key or key in q:
            results.append(profile)

    return results[:limit]


def get_sports_by_type(sport_type: str) -> List[Dict[str, Any]]:
    target = normalize_text(sport_type)
    return [
        profile
        for profile in UNIVERSAL_SPORT_DATABASE.values()
        if normalize_text(profile["sport_type"]) == target
    ]
