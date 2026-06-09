"""
Sportze.AI training_catalog.py

This file is intentionally a clean starter catalog hook.

The current training_generator_updated.py imports get_catalog_session(profile, meta).
For now, this file does NOT override the existing generator output. Later, you can
fill TRAINING_CATALOG with the 18-sport, 43-session-per-sport database:
- 3 Learn the Sport sessions
- 10 Beginner sessions
- 10 Intermediate sessions
- 10 Advanced sessions
- 10 Elite sessions

Each session can also include solo/group compatibility.
"""

from typing import Dict, List, Optional, Any


SUPPORTED_18_SPORTS: List[str] = [
    "Soccer",
    "Tennis",
    "Basketball",
    "Volleyball",
    "Swimming",
    "Running",
    "Cycling",
    "Cricket",
    "Baseball",
    "Golf",
    "Rugby",
    "Badminton",
    "Table Tennis",
    "Martial Arts",
    "Field Hockey",
    "Handball",
    "Water Polo",
    "Triathlon",
]

TEAM_SPORTS = {
    "Soccer",
    "Basketball",
    "Volleyball",
    "Cricket",
    "Baseball",
    "Rugby",
    "Field Hockey",
    "Handball",
    "Water Polo",
}

INDIVIDUAL_SPORTS = set(SUPPORTED_18_SPORTS) - TEAM_SPORTS

LEVELS = ["Beginner", "Intermediate", "Advanced", "Elite"]
LEARN_THE_SPORT_LEVEL = "Never Played Before"

# Future shape:
#
# TRAINING_CATALOG = {
#     "Soccer": {
#         "Learn the Sport": [session_1, session_2, session_3],
#         "Beginner": [10 session dicts],
#         "Intermediate": [10 session dicts],
#         "Advanced": [10 session dicts],
#         "Elite": [10 session dicts],
#     },
# }
#
# A session dict should look like:
#
# {
#     "title": "Beginner Solo Ball Mastery",
#     "level": "Beginner",
#     "format": "solo",  # "solo", "group", or "both"
#     "min_people": 1,
#     "max_people": 1,
#     "duration_minutes": 60,
#     "goal_tags": ["Technical Priority", "Improve performance"],
#     "exercises": [
#         {
#             "name": "Dynamic warm-up",
#             "category": "Warm-Up",
#             "prescription": "8 minutes",
#             "purpose": "Prepare movement quality.",
#             "coaching_points": ["Stay smooth.", "Increase speed gradually."],
#             "planned_block_minutes": 8,
#             "planned_sets": None,
#             "planned_reps": None,
#         }
#     ],
# }

TRAINING_CATALOG: Dict[str, Dict[str, List[Dict[str, Any]]]] = {}


def normalize_sport_name(sport: str) -> str:
    text = " ".join(str(sport or "").strip().split()).lower()
    aliases = {
        "football": "Soccer",
        "futebol": "Soccer",
        "waterpolo": "Water Polo",
        "water polo": "Water Polo",
        "table tennis": "Table Tennis",
        "ping pong": "Table Tennis",
        "track": "Running",
        "athletics": "Running",
        "martial arts": "Martial Arts",
        "mma": "Martial Arts",
    }
    if text in aliases:
        return aliases[text]
    for sport_name in SUPPORTED_18_SPORTS:
        if sport_name.lower() == text:
            return sport_name
    return str(sport or "").strip()


def detect_catalog_sport_type(sport: str) -> str:
    sport_name = normalize_sport_name(sport)
    if sport_name in TEAM_SPORTS:
        return "Team Sport"
    if sport_name in INDIVIDUAL_SPORTS:
        return "Individual Sport"
    return ""


def session_matches_training_format(session: Dict[str, Any], training_alone: bool, partners_count: int) -> bool:
    session_format = str(session.get("format", "both")).lower()
    total_people = 1 if training_alone else 1 + int(partners_count or 0)

    if session_format == "solo" and not training_alone:
        return False
    if session_format == "group" and training_alone:
        return False

    min_people = int(session.get("min_people", 1) or 1)
    max_people = session.get("max_people", 999)
    max_people = 999 if max_people is None else int(max_people)

    return min_people <= total_people <= max_people


def get_catalog_session(profile: Dict[str, Any], meta: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """Return a catalog session override when the future catalog is filled.

    Returning None tells the main generator to keep its current generated session.
    """
    sport = normalize_sport_name(str(profile.get("sport", "")))
    level = str(profile.get("level", "Beginner"))
    goal = str(profile.get("goal", ""))
    session_type = str(profile.get("session_type", ""))
    training_alone = bool(profile.get("training_alone", True))
    partners_count = int(profile.get("training_partners_count", 0) or 0)

    sport_catalog = TRAINING_CATALOG.get(sport)
    if not sport_catalog:
        return None

    if goal == "Learn how to play":
        candidate_sessions = sport_catalog.get("Learn the Sport", [])
    else:
        candidate_sessions = sport_catalog.get(level, [])

    for session in candidate_sessions:
        if not session_matches_training_format(session, training_alone, partners_count):
            continue

        goal_tags = session.get("goal_tags", [])
        if goal_tags and goal not in goal_tags and session_type not in goal_tags:
            continue

        return {
            "title": session.get("title"),
            "exercises": session.get("exercises"),
            "meta": {
                "catalog_matched": True,
                "catalog_sport": sport,
                "catalog_level": level,
                "catalog_training_format": "solo" if training_alone else "group",
            },
            "source": "training_catalog.py",
        }

    return None
