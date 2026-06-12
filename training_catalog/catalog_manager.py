# =============================================================================
# SPORTZE.AI - TRAINING CATALOG MANAGER
# =============================================================================
# Put this file inside:
# training_catalog/catalog_manager.py
#
# Purpose:
# - Connects all individual sport catalog files inside training_catalog/
# - Looks up the correct sport catalog
# - Selects sessions by level, solo/group, goal, and session type
# - Falls back to universal_sport_system.py for sports not yet fully cataloged
#
# Expected folder:
# training_catalog/
#   __init__.py
#   catalog_manager.py
#   universal_sport_system.py
#   soccer.py
#   basketball.py
#   ...
# =============================================================================

from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
from typing import Any, Dict, List, Optional, Tuple
import random
import re


# -------------------------------------------------------------------------
# SPORTS YOU HAVE AS REAL CATALOG FILES
# -------------------------------------------------------------------------
# Key = normalized user sport name.
# Value = Python module filename inside training_catalog, without ".py".
#
# Example:
# "water polo" -> training_catalog/water_polo.py
# -------------------------------------------------------------------------

CATALOG_MODULES: Dict[str, str] = {
    "american football": "american_football",
    "football": "american_football",
    "gridiron": "american_football",

    "athletics": "athletics",
    "track and field": "athletics",
    "track": "athletics",
    "field": "athletics",
    "running": "athletics",
    "sprinting": "athletics",
    "marathon": "athletics",

    "baseball": "baseball",
    "basketball": "basketball",

    "box": "box",
    "boxing": "box",

    "calisthenics": "calisthenics",
    "bodyweight training": "calisthenics",

    "cricket": "cricket",
    "cycling": "cycling",
    "biking": "cycling",

    "golf": "golf",
    "gymnastics": "gymnastics",

    "hockey": "hockey",
    "field hockey": "hockey",
    "ice hockey": "hockey",

    "martial arts": "martial_arts",
    "karate": "martial_arts",
    "judo": "martial_arts",
    "taekwondo": "martial_arts",
    "mma": "martial_arts",
    "brazilian jiu jitsu": "martial_arts",
    "bjj": "martial_arts",

    "rowing": "rowing",
    "rugby": "rugby",

    "soccer": "soccer",
    "football soccer": "soccer",
    "futsal": "soccer",

    "swimming": "swimming",
    "table tennis": "table_tennis",
    "ping pong": "table_tennis",

    "tennis": "tennis",
    "triathlon": "triathlon",

    "volleyball": "volleyball",
    "beach volleyball": "volleyball",

    "water polo": "water_polo",
    "weightlifting": "weightlifting",
    "olympic weightlifting": "weightlifting",
}


LEVEL_ALIASES: Dict[str, str] = {
    "never played": "Never Played Before",
    "never played before": "Never Played Before",
    "learn": "Never Played Before",
    "learn how to play": "Never Played Before",
    "new": "Never Played Before",
    "beginner": "Beginner",
    "intermediate": "Intermediate",
    "advanced": "Advanced",
    "elite": "Elite",
}


SESSION_TYPE_KEYWORDS: Dict[str, List[str]] = {
    "balanced": ["technical", "base", "competition", "recovery", "tactical"],
    "technical": ["technical", "skill", "base", "pattern"],
    "physical": ["speed", "power", "strength", "endurance", "agility"],
    "intense": ["competition", "simulation", "speed", "power", "endurance"],
    "recovery": ["recovery", "low-intensity", "mobility"],
    "tactical": ["tactical", "decision", "reaction", "pattern"],
}


@dataclass
class CatalogResult:
    source: str
    sport_requested: str
    sport_used: str
    is_exact_catalog: bool
    session: Dict[str, Any]
    similar_sports: List[str]


def normalize_text(value: str) -> str:
    """Normalize user text so lookup is forgiving."""
    value = (value or "").strip().lower()
    value = value.replace("_", " ").replace("-", " ")
    value = re.sub(r"[^a-z0-9\s]", "", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def normalize_level(level: Optional[str], goal: Optional[str] = None) -> str:
    """Return one of the catalog level names."""
    combined = normalize_text(f"{level or ''} {goal or ''}")

    if "learn how to play" in combined or "never played" in combined:
        return "Never Played Before"

    for key, fixed in LEVEL_ALIASES.items():
        if key in combined:
            return fixed

    return "Beginner"


def normalize_training_alone(value: Optional[Any]) -> Optional[bool]:
    """Convert user answer about solo/group training into True/False/None."""
    if value is None:
        return None

    if isinstance(value, bool):
        return value

    text = normalize_text(str(value))

    if text in {"yes", "y", "alone", "solo", "by myself", "true", "1"}:
        return True

    if text in {"no", "n", "group", "team", "with others", "with a team", "false", "0"}:
        return False

    return None


def get_module_name_for_sport(sport: str) -> Optional[str]:
    """Return the module name for a sport if Sportze has a fixed catalog for it."""
    normalized = normalize_text(sport)

    if normalized in CATALOG_MODULES:
        return CATALOG_MODULES[normalized]

    # light fuzzy matching: allows "I want soccer training"
    for key, module in CATALOG_MODULES.items():
        if key in normalized or normalized in key:
            return module

    return None


def import_sport_module(module_name: str):
    """
    Import a sport module from training_catalog.

    This supports both:
    - running inside the package: training_catalog.soccer
    - direct local testing from the folder: soccer
    """
    try:
        return import_module(f"training_catalog.{module_name}")
    except ModuleNotFoundError:
        return import_module(module_name)


def extract_catalog_from_module(module: Any) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Sport files can expose data in different simple formats.

    Supported:
    1. TRAINING_CATALOG = {"Soccer": [sessions...]}
    2. TRAINING_CATALOG = [sessions...]
    3. SOCCER_SESSIONS = [sessions...]
    4. SESSIONS = [sessions...]
    5. SPORT_METADATA = {...}
    """

    metadata = getattr(module, "SPORT_METADATA", {}) or {}

    if hasattr(module, "TRAINING_CATALOG"):
        catalog = getattr(module, "TRAINING_CATALOG")

        if isinstance(catalog, dict):
            all_sessions: List[Dict[str, Any]] = []
            for value in catalog.values():
                if isinstance(value, list):
                    all_sessions.extend(value)
            return all_sessions, metadata

        if isinstance(catalog, list):
            return catalog, metadata

    if hasattr(module, "SESSIONS"):
        sessions = getattr(module, "SESSIONS")
        if isinstance(sessions, list):
            return sessions, metadata

    for name in dir(module):
        if name.endswith("_SESSIONS"):
            sessions = getattr(module, name)
            if isinstance(sessions, list):
                return sessions, metadata

    return [], metadata


def filter_sessions(
    sessions: List[Dict[str, Any]],
    level: str,
    training_alone: Optional[bool],
    session_type: Optional[str],
) -> List[Dict[str, Any]]:
    """Filter sessions using level, solo/group preference, and session type."""
    if not sessions:
        return []

    level_matches = [
        s for s in sessions
        if normalize_text(str(s.get("level", ""))) == normalize_text(level)
    ]

    candidates = level_matches or sessions

    if training_alone is not None:
        if training_alone:
            solo_matches = [
                s for s in candidates
                if s.get("solo_allowed") is True or normalize_text(str(s.get("format", ""))) in {"solo", "both", "flexible"}
            ]
            if solo_matches:
                candidates = solo_matches
        else:
            group_matches = [
                s for s in candidates
                if s.get("group_allowed") is True or normalize_text(str(s.get("format", ""))) in {"group", "both", "flexible"}
            ]
            if group_matches:
                candidates = group_matches

    session_type_norm = normalize_text(session_type or "balanced")
    keywords = SESSION_TYPE_KEYWORDS.get(session_type_norm, SESSION_TYPE_KEYWORDS["balanced"])

    keyword_matches = []
    for session in candidates:
        searchable = normalize_text(
            " ".join([
                str(session.get("title", "")),
                str(session.get("objective", "")),
                " ".join(map(str, session.get("training_blocks", []))) if isinstance(session.get("training_blocks", []), list) else "",
            ])
        )
        if any(keyword in searchable for keyword in keywords):
            keyword_matches.append(session)

    return keyword_matches or candidates


def choose_session(
    sessions: List[Dict[str, Any]],
    level: str = "Beginner",
    training_alone: Optional[Any] = None,
    session_type: Optional[str] = "balanced",
    seed: Optional[int] = None,
) -> Optional[Dict[str, Any]]:
    """Choose one clean matching session."""
    if not sessions:
        return None

    alone = normalize_training_alone(training_alone)
    candidates = filter_sessions(sessions, level, alone, session_type)

    rng = random.Random(seed)
    return rng.choice(candidates) if candidates else None


def get_catalog_sessions(sport: str) -> List[Dict[str, Any]]:
    """Return all fixed catalog sessions for a sport, or an empty list."""
    module_name = get_module_name_for_sport(sport)
    if not module_name:
        return []

    module = import_sport_module(module_name)
    sessions, _metadata = extract_catalog_from_module(module)
    return sessions


def get_training_session(
    sport: str,
    goal: Optional[str] = None,
    level: Optional[str] = None,
    training_alone: Optional[Any] = None,
    session_type: Optional[str] = "balanced",
    seed: Optional[int] = None,
) -> CatalogResult:
    """
    Main function for the training generator.

    Use this from your main training generator:
        from training_catalog.catalog_manager import get_training_session

        result = get_training_session(
            sport=user_sport,
            goal=user_goal,
            level=user_level,
            training_alone=user_training_alone,
            session_type=user_session_type,
        )

        session = result.session
    """

    requested = sport or "unknown sport"
    fixed_level = normalize_level(level, goal)
    module_name = get_module_name_for_sport(requested)

    if module_name:
        try:
            module = import_sport_module(module_name)
            sessions, metadata = extract_catalog_from_module(module)
            selected = choose_session(
                sessions=sessions,
                level=fixed_level,
                training_alone=training_alone,
                session_type=session_type,
                seed=seed,
            )

            if selected:
                sport_used = str(selected.get("sport") or requested).strip()
                return CatalogResult(
                    source="fixed_catalog",
                    sport_requested=requested,
                    sport_used=sport_used,
                    is_exact_catalog=True,
                    session=selected,
                    similar_sports=[],
                )
        except Exception as error:
            # If a sport file has a temporary syntax/import problem,
            # the system still works through the universal fallback.
            fallback_reason = f"fixed catalog import failed: {error}"
        else:
            fallback_reason = "fixed catalog exists but no session was found"
    else:
        fallback_reason = "sport is not in fixed catalog"

    # Universal fallback for any other sport.
    try:
        try:
            universal = import_module("training_catalog.universal_sport_system")
        except ModuleNotFoundError:
            universal = import_module("universal_sport_system")

        universal_session = universal.generate_universal_session(
            sport=requested,
            goal=goal,
            level=fixed_level,
            training_alone=training_alone,
            session_type=session_type,
            seed=seed,
        )

        profile = universal.get_universal_sport_profile(requested)

        universal_session["fallback_reason"] = fallback_reason

        return CatalogResult(
            source="universal_sport_system",
            sport_requested=requested,
            sport_used=profile["sport"],
            is_exact_catalog=False,
            session=universal_session,
            similar_sports=profile.get("nearest_catalog_sports", []),
        )

    except Exception as error:
        # Final emergency fallback so the app never fully crashes.
        return CatalogResult(
            source="emergency_fallback",
            sport_requested=requested,
            sport_used=requested,
            is_exact_catalog=False,
            similar_sports=["athletics", "calisthenics"],
            session={
                "id": "emergency_fallback_session",
                "sport": requested,
                "sport_type": "Unknown",
                "level": fixed_level,
                "format": "solo" if normalize_training_alone(training_alone) is not False else "group",
                "title": f"{requested.title()} General Athletic Session",
                "objective": "Create a safe basic session when no catalog could be loaded.",
                "equipment": "open space, cones optional",
                "people": "1 athlete or group",
                "training_blocks": [
                    "1. Warm-up: 10 min light movement and mobility.",
                    "2. Skill block: 15 min easy basic technique practice.",
                    "3. Physical block: 3 rounds of squats, lunges, push-ups, planks, and short accelerations.",
                    "4. Sport block: 15 min simple repeated sport movement.",
                    "5. Cooldown: 5 min stretching and breathing.",
                ],
                "coach_cues": [
                    "Keep technique safe.",
                    "Stop if pain appears.",
                    "Increase speed only after control is good.",
                ],
                "progression": "Add complexity first, then speed, then fatigue.",
                "error": str(error),
            },
        )


def get_available_fixed_sports() -> List[str]:
    """Return the main fixed catalog sports."""
    return sorted(set(CATALOG_MODULES.keys()))


def format_session_simple(session: Dict[str, Any]) -> str:
    """
    Optional display helper.

    It keeps the output simple for the user:
    bold exercise/block name and the dose underneath.
    """
    title = session.get("title", "Training Session")
    blocks = session.get("training_blocks", [])

    lines = [f"### {title}", ""]

    for block in blocks:
        block = str(block).strip()
        if not block:
            continue

        cleaned = re.sub(r"^\d+\.\s*", "", block)

        if ":" in cleaned:
            name, details = cleaned.split(":", 1)
            lines.append(f"**{name.strip()}**")
            lines.append(f"- {details.strip()}")
        else:
            lines.append(f"**{cleaned}**")
            lines.append("- Complete with clean technique.")

        lines.append("")

    return "\n".join(lines).strip()
