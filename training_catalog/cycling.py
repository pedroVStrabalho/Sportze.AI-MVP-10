"""
Sportze.AI Cycling Training Catalog

This module codifies Cycling workouts for the Training Generator.
It uses plain Python dictionaries/lists so it can be imported cleanly by
catalog_manager.py or any Sportze.AI training selector.

Structure:
- CYCLING_CATALOG[category][training_mode][session_key]
- training_mode: "alone" or "with_others"
- each session contains: title, sport, category, focus, training_mode, exercises

Helper functions:
- get_cycling_catalog()
- list_cycling_sessions(category=None, training_mode=None)
- get_cycling_session(session_key, category=None, training_mode=None)
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List, Optional

SportSession = Dict[str, Any]
SportCatalog = Dict[str, Dict[str, Dict[str, SportSession]]]

SPORT = "Cycling"


def exercise(name: str, prescription: str, notes: str = "") -> Dict[str, str]:
    """Create a normalized exercise object for Sportze.AI catalogs."""
    item = {"name": name, "prescription": prescription}
    if notes:
        item["notes"] = notes
    return item


def session(
    key: str,
    title: str,
    category: str,
    training_mode: str,
    focus: str,
    exercises: List[Dict[str, str]],
) -> SportSession:
    """Create a normalized cycling session."""
    return {
        "key": key,
        "sport": SPORT,
        "title": title,
        "category": category,
        "training_mode": training_mode,
        "focus": focus,
        "exercises": exercises,
    }


CYCLING_CATALOG: SportCatalog = {
    "mountain_bike_beginner": {
        "alone": {
            "cycling_mtb_beginner_trail_ride": session(
                "cycling_mtb_beginner_trail_ride",
                "Trail Ride",
                "mountain_bike_beginner",
                "alone",
                "easy trail handling and beginner endurance",
                [exercise("Easy Trail Ride", "Ride 5 km on easy trail")],
            ),
            "cycling_mtb_beginner_climbing_session": session(
                "cycling_mtb_beginner_climbing_session",
                "Climbing Session",
                "mountain_bike_beginner",
                "alone",
                "beginner climbing strength",
                [exercise("Short Trail Climbs", "Complete 5 climbs of 200m")],
            ),
            "cycling_mtb_beginner_endurance_trail_ride": session(
                "cycling_mtb_beginner_endurance_trail_ride",
                "Endurance Trail Ride",
                "mountain_bike_beginner",
                "alone",
                "continuous trail endurance",
                [exercise("Continuous Trail Ride", "Ride 10 km continuously")],
            ),
            "cycling_mtb_beginner_technical_ride": session(
                "cycling_mtb_beginner_technical_ride",
                "Technical Ride",
                "mountain_bike_beginner",
                "alone",
                "basic technical trail control",
                [exercise("Technical Trail Ride", "Complete 3 km technical trail")],
            ),
            "cycling_mtb_beginner_long_trail_ride": session(
                "cycling_mtb_beginner_long_trail_ride",
                "Long Trail Ride",
                "mountain_bike_beginner",
                "alone",
                "longer beginner trail endurance",
                [exercise("Long Continuous Trail Ride", "Ride 15 km continuously")],
            ),
            "cycling_mtb_beginner_xc_simulation": session(
                "cycling_mtb_beginner_xc_simulation",
                "XC Simulation",
                "mountain_bike_beginner",
                "alone",
                "beginner cross-country mixed terrain",
                [exercise("Mixed Terrain XC Ride", "Ride 20 km mixed terrain")],
            ),
        },
        "with_others": {},
    },
    "xc_intermediate": {
        "alone": {
            "cycling_xc_intermediate_endurance_ride": session(
                "cycling_xc_intermediate_endurance_ride",
                "Endurance Ride",
                "xc_intermediate",
                "alone",
                "cross-country endurance",
                [exercise("Continuous XC Ride", "Ride 25 km continuously")],
            ),
            "cycling_xc_intermediate_climbing_session": session(
                "cycling_xc_intermediate_climbing_session",
                "Climbing Session",
                "xc_intermediate",
                "alone",
                "cross-country climbing capacity",
                [exercise("XC Climb Repeats", "Complete 10 climbs of 300m")],
            ),
            "cycling_xc_intermediate_technical_session": session(
                "cycling_xc_intermediate_technical_session",
                "Technical Session",
                "xc_intermediate",
                "alone",
                "technical trail endurance",
                [exercise("Technical XC Trail Ride", "Ride 10 km technical trail")],
            ),
            "cycling_xc_intermediate_race_pace": session(
                "cycling_xc_intermediate_race_pace",
                "XC Race Pace",
                "xc_intermediate",
                "alone",
                "race-pace conditioning",
                [exercise("Race-Pace XC Ride", "Ride 15 km at race pace")],
            ),
            "cycling_xc_intermediate_long_xc_ride": session(
                "cycling_xc_intermediate_long_xc_ride",
                "Long XC Ride",
                "xc_intermediate",
                "alone",
                "long cross-country endurance",
                [exercise("Long Continuous XC Ride", "Ride 35 km continuously")],
            ),
            "cycling_xc_intermediate_xc_simulation": session(
                "cycling_xc_intermediate_xc_simulation",
                "XC Simulation",
                "xc_intermediate",
                "alone",
                "full cross-country simulation",
                [exercise("Mixed Terrain XC Simulation", "Ride 40 km mixed terrain")],
            ),
        },
        "with_others": {},
    },
    "road_cycling_beginner": {
        "alone": {
            "cycling_road_beginner_easy_ride": session(
                "cycling_road_beginner_easy_ride",
                "Easy Ride",
                "road_cycling_beginner",
                "alone",
                "entry-level road endurance",
                [exercise("Easy Road Ride", "Ride 10 km continuously")],
            ),
            "cycling_road_beginner_cadence_ride": session(
                "cycling_road_beginner_cadence_ride",
                "Cadence Ride",
                "road_cycling_beginner",
                "alone",
                "pedaling rhythm and cadence consistency",
                [exercise("Continuous Cadence Ride", "Ride 15 km continuously")],
            ),
            "cycling_road_beginner_endurance_ride": session(
                "cycling_road_beginner_endurance_ride",
                "Endurance Ride",
                "road_cycling_beginner",
                "alone",
                "beginner road endurance",
                [exercise("Continuous Road Ride", "Ride 20 km continuously")],
            ),
            "cycling_road_beginner_sprint_ride": session(
                "cycling_road_beginner_sprint_ride",
                "Sprint Ride",
                "road_cycling_beginner",
                "alone",
                "introductory sprint work",
                [exercise("Road Ride With Sprints", "Ride 15 km with 5 sprints")],
            ),
            "cycling_road_beginner_long_ride": session(
                "cycling_road_beginner_long_ride",
                "Long Ride",
                "road_cycling_beginner",
                "alone",
                "long beginner road endurance",
                [exercise("Long Continuous Road Ride", "Ride 25 km continuously")],
            ),
            "cycling_road_beginner_recovery_ride": session(
                "cycling_road_beginner_recovery_ride",
                "Recovery Ride",
                "road_cycling_beginner",
                "alone",
                "active recovery and easy aerobic riding",
                [exercise("Easy Recovery Ride", "Ride 10 km at easy pace")],
            ),
        },
        "with_others": {},
    },
    "road_cycling_intermediate": {
        "alone": {
            "cycling_road_intermediate_endurance_ride": session(
                "cycling_road_intermediate_endurance_ride",
                "Endurance Ride",
                "road_cycling_intermediate",
                "alone",
                "intermediate road endurance",
                [exercise("Continuous Road Endurance Ride", "Ride 40 km continuously")],
            ),
            "cycling_road_intermediate_sprint_session": session(
                "cycling_road_intermediate_sprint_session",
                "Sprint Session",
                "road_cycling_intermediate",
                "alone",
                "road sprint repeat conditioning",
                [exercise("Road Ride With Sprint Repeats", "Ride 30 km with 10 sprints")],
            ),
            "cycling_road_intermediate_climbing_session": session(
                "cycling_road_intermediate_climbing_session",
                "Climbing Session",
                "road_cycling_intermediate",
                "alone",
                "hill climbing endurance",
                [exercise("Hill Road Ride", "Ride 25 km including hills")],
            ),
            "cycling_road_intermediate_tempo_ride": session(
                "cycling_road_intermediate_tempo_ride",
                "Tempo Ride",
                "road_cycling_intermediate",
                "alone",
                "steady tempo pacing",
                [exercise("Steady Tempo Road Ride", "Ride 35 km at steady pace")],
            ),
            "cycling_road_intermediate_long_ride": session(
                "cycling_road_intermediate_long_ride",
                "Long Ride",
                "road_cycling_intermediate",
                "alone",
                "long intermediate road endurance",
                [exercise("Long Continuous Road Ride", "Ride 50 km continuously")],
            ),
            "cycling_road_intermediate_group_ride": session(
                "cycling_road_intermediate_group_ride",
                "Group Ride",
                "road_cycling_intermediate",
                "alone",
                "sustained road riding volume",
                [exercise("Continuous Road Ride", "Ride 40 km continuously")],
                
            ),
        },
        "with_others": {
            "cycling_road_intermediate_group_ride_with_others": session(
                "cycling_road_intermediate_group_ride_with_others",
                "Group Ride",
                "road_cycling_intermediate",
                "with_others",
                "group riding endurance",
                [exercise("Group Road Ride", "Ride 40 km continuously")],
            ),
        },
    },
    "road_cycling_advanced": {
        "alone": {
            "cycling_road_advanced_endurance_ride": session(
                "cycling_road_advanced_endurance_ride",
                "Endurance Ride",
                "road_cycling_advanced",
                "alone",
                "advanced road endurance",
                [exercise("Continuous Road Endurance Ride", "Ride 70 km continuously")],
            ),
            "cycling_road_advanced_sprint_session": session(
                "cycling_road_advanced_sprint_session",
                "Sprint Session",
                "road_cycling_advanced",
                "alone",
                "advanced sprint repeat conditioning",
                [exercise("Road Ride With Sprint Repeats", "Ride 50 km with 15 sprints")],
            ),
            "cycling_road_advanced_climbing_session": session(
                "cycling_road_advanced_climbing_session",
                "Climbing Session",
                "road_cycling_advanced",
                "alone",
                "advanced climbing endurance",
                [exercise("Hill Road Ride", "Ride 60 km with hills")],
            ),
            "cycling_road_advanced_tempo_ride": session(
                "cycling_road_advanced_tempo_ride",
                "Tempo Ride",
                "road_cycling_advanced",
                "alone",
                "advanced tempo endurance",
                [exercise("Continuous Tempo Road Ride", "Ride 60 km continuously")],
            ),
            "cycling_road_advanced_long_ride": session(
                "cycling_road_advanced_long_ride",
                "Long Ride",
                "road_cycling_advanced",
                "alone",
                "long advanced road endurance",
                [exercise("Long Continuous Road Ride", "Ride 90 km continuously")],
            ),
            "cycling_road_advanced_race_simulation": session(
                "cycling_road_advanced_race_simulation",
                "Race Simulation",
                "road_cycling_advanced",
                "alone",
                "advanced race simulation",
                [exercise("Road Race Simulation", "Ride 100 km")],
            ),
        },
        "with_others": {},
    },
    "tour_de_france_elite": {
        "alone": {
            "cycling_elite_endurance_ride": session(
                "cycling_elite_endurance_ride",
                "Endurance Ride",
                "tour_de_france_elite",
                "alone",
                "elite endurance volume",
                [exercise("Elite Continuous Road Ride", "Ride 120 km continuously")],
            ),
            "cycling_elite_mountain_ride": session(
                "cycling_elite_mountain_ride",
                "Mountain Ride",
                "tour_de_france_elite",
                "alone",
                "elite mountain climbing",
                [exercise("Mountain Road Ride", "Ride 100 km with major climbs")],
            ),
            "cycling_elite_sprint_stage_simulation": session(
                "cycling_elite_sprint_stage_simulation",
                "Sprint Stage Simulation",
                "tour_de_france_elite",
                "alone",
                "elite sprint-stage finishing",
                [exercise("Sprint Stage Ride", "Ride 140 km with 20 final sprints")],
            ),
            "cycling_elite_time_trial_simulation": session(
                "cycling_elite_time_trial_simulation",
                "Time Trial Simulation",
                "tour_de_france_elite",
                "alone",
                "maximum sustainable time-trial pacing",
                [exercise("Time Trial Effort", "Ride 40 km at maximum sustainable pace")],
            ),
            "cycling_elite_queen_stage_simulation": session(
                "cycling_elite_queen_stage_simulation",
                "Queen Stage Simulation",
                "tour_de_france_elite",
                "alone",
                "elite multi-climb stage simulation",
                [exercise("Queen Stage Ride", "Ride 160 km with multiple climbs")],
            ),
            "cycling_elite_grand_tour_stage": session(
                "cycling_elite_grand_tour_stage",
                "Grand Tour Stage",
                "tour_de_france_elite",
                "alone",
                "grand tour stage endurance",
                [exercise("Grand Tour Stage Ride", "Ride 180 km continuously")],
            ),
        },
        "with_others": {},
    },
}


CYCLING_SESSION_BANK: List[SportSession] = [
    workout
    for category_data in CYCLING_CATALOG.values()
    for mode_data in category_data.values()
    for workout in mode_data.values()
]


CYCLING_CATEGORIES = list(CYCLING_CATALOG.keys())
CYCLING_TRAINING_MODES = ["alone", "with_others"]


CYCLING_CATEGORY_ALIASES = {
    "mountain bike beginner": "mountain_bike_beginner",
    "mtb beginner": "mountain_bike_beginner",
    "mountain bike": "mountain_bike_beginner",
    "mtb": "mountain_bike_beginner",
    "xc intermediate": "xc_intermediate",
    "cross country intermediate": "xc_intermediate",
    "cross-country intermediate": "xc_intermediate",
    "xc": "xc_intermediate",
    "road cycling beginner": "road_cycling_beginner",
    "road beginner": "road_cycling_beginner",
    "beginner road": "road_cycling_beginner",
    "beginner": "road_cycling_beginner",
    "road cycling intermediate": "road_cycling_intermediate",
    "road intermediate": "road_cycling_intermediate",
    "intermediate": "road_cycling_intermediate",
    "road cycling advanced": "road_cycling_advanced",
    "road advanced": "road_cycling_advanced",
    "advanced": "road_cycling_advanced",
    "tour de france": "tour_de_france_elite",
    "tour de france elite": "tour_de_france_elite",
    "elite": "tour_de_france_elite",
    "elite level": "tour_de_france_elite",
    "grand tour": "tour_de_france_elite",
}


CYCLING_MODE_ALIASES = {
    "solo": "alone",
    "alone": "alone",
    "individual": "alone",
    "training alone": "alone",
    "group": "with_others",
    "partner": "with_others",
    "with others": "with_others",
    "2+ people": "with_others",
    "two or more": "with_others",
}


def normalize_cycling_category(category: Optional[str]) -> Optional[str]:
    """Normalize a category string to a catalog key."""
    if category is None:
        return None
    key = category.strip().lower().replace("_", " ")
    return CYCLING_CATEGORY_ALIASES.get(key, key.replace(" ", "_"))


def normalize_cycling_training_mode(training_mode: Optional[str]) -> Optional[str]:
    """Normalize a training mode string to 'alone' or 'with_others'."""
    if training_mode is None:
        return None
    key = training_mode.strip().lower().replace("_", " ")
    return CYCLING_MODE_ALIASES.get(key, key.replace(" ", "_"))


def get_cycling_catalog() -> SportCatalog:
    """Return a deep copy of the full cycling catalog."""
    return deepcopy(CYCLING_CATALOG)


def list_cycling_sessions(
    category: Optional[str] = None,
    training_mode: Optional[str] = None,
) -> List[SportSession]:
    """List cycling sessions, optionally filtered by category and training mode."""
    normalized_category = normalize_cycling_category(category)
    normalized_mode = normalize_cycling_training_mode(training_mode)

    sessions: List[SportSession] = []
    for category_key, category_data in CYCLING_CATALOG.items():
        if normalized_category and category_key != normalized_category:
            continue
        for mode_key, mode_data in category_data.items():
            if normalized_mode and mode_key != normalized_mode:
                continue
            sessions.extend(mode_data.values())
    return deepcopy(sessions)


def get_cycling_session(
    session_key: str,
    category: Optional[str] = None,
    training_mode: Optional[str] = None,
) -> Optional[SportSession]:
    """Find one cycling session by key, optionally inside a category/training mode."""
    for item in list_cycling_sessions(category=category, training_mode=training_mode):
        if item["key"] == session_key:
            return item
    return None


# Generic names that catalog_manager.py can use if it expects standard exports.
CATALOG = CYCLING_CATALOG
SESSION_BANK = CYCLING_SESSION_BANK
CATEGORIES = CYCLING_CATEGORIES
TRAINING_MODES = CYCLING_TRAINING_MODES


if __name__ == "__main__":
    print(f"{SPORT} catalog loaded: {len(CYCLING_SESSION_BANK)} sessions")
    for category_name in CYCLING_CATEGORIES:
        count = len(list_cycling_sessions(category=category_name))
        print(f"- {category_name}: {count} sessions")
