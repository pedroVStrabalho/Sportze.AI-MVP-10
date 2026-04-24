import hashlib
import random
import re
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Callable, Dict, List, Optional, Tuple

import streamlit as st


# =============================================================================
# SPORTZE.AI - UNIFIED CHAT TRAINING GENERATOR
# - Built from the current generator architecture, but turned into a chat flow
# - Homepage onboarding is absorbed here
# - Same profile questions stay conceptually the same, but are asked one by one
# - Works for any sport in chat; structured library is used when supported
# - Gym sessions gain a training summary logger with reps / weight / skipped option
# =============================================================================


@dataclass
class Exercise:
    name: str
    category: str
    prescription: str
    purpose: str
    equipment_tags: List[str] = field(default_factory=list)
    intensity_tags: List[str] = field(default_factory=list)
    focus_tags: List[str] = field(default_factory=list)
    position_tags: List[str] = field(default_factory=list)
    level_tags: List[str] = field(default_factory=list)
    phase_tags: List[str] = field(default_factory=list)
    time_weight: float = 1.0
    coaching_points: List[str] = field(default_factory=list)
    progressions: List[str] = field(default_factory=list)
    regressions: List[str] = field(default_factory=list)
    risk_notes: List[str] = field(default_factory=list)


SPORT_POSITIONS: Dict[str, List[str]] = {
    "Soccer": ["Goalkeeper", "Centre Back", "Full Back", "Wing Back", "Defensive Midfielder", "Central Midfielder", "Attacking Midfielder", "Winger", "Striker"],
    "Basketball": ["Point Guard", "Shooting Guard", "Small Forward", "Power Forward", "Center"],
    "Tennis": ["Singles Player", "Doubles Specialist", "All-Court Player", "Baseline Player", "Serve-and-Volley Player"],
    "Volleyball": ["Setter", "Outside Hitter", "Opposite", "Middle Blocker", "Libero", "Defensive Specialist"],
    "Water Polo": ["Goalkeeper", "Center Forward", "Center Back", "Driver", "Wing", "Point"],
    "Baseball": ["Pitcher", "Catcher", "First Baseman", "Second Baseman", "Third Baseman", "Shortstop", "Outfielder"],
    "Running": ["Sprinter", "Middle Distance", "Long Distance", "Trail Runner"],
    "Gym": ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance"],
    "Weightlifting": ["Snatch Focus", "Clean and Jerk Focus", "General Weightlifting"],
    "Rowing": ["Sweep Rower", "Sculler", "Coxswain", "Indoor Rower"],
}

GOALS = [
    "Improve performance",
    "Build fitness",
    "Return after a break",
    "Learn how to play",
    "Injury prevention",
    "Competition preparation",
]

LEVELS = ["Beginner", "Intermediate", "Advanced", "Elite"]
GYM_LEVELS = ["Beginner", "Intermediate", "Advanced", "Experienced"]
SESSION_TYPES = ["Balanced Session", "Technical Priority", "Physical Priority", "Competition Week"]
GYM_SESSION_TYPES = ["Balanced Session", "Technical Priority", "Physical Priority", "Intense Session"]
GYM_GOALS = ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance"]
EQUIPMENT_LEVELS = ["Minimal", "Basic", "Medium", "Competitive", "Elite"]
INTENSITY_MODES = ["Controlled", "Standard", "High", "Peak"]
READINESS_OPTIONS = ["Low", "Moderate", "High"]
PRIMARY_FOCUS_OPTIONS = ["Speed", "Power", "Technical Quality", "Conditioning", "Strength", "Movement Quality", "Match Rhythm"]
SEASON_PHASES = ["Off-Season", "Pre-Season", "In-Season", "Competition Block", "Return-to-Play Support"]

KNOWN_TEAM_SPORTS = {
    "soccer", "football", "basketball", "volleyball", "water polo", "baseball", "softball", "rugby",
    "handball", "futsal", "hockey", "lacrosse", "cricket", "american football",
}
KNOWN_INDIVIDUAL_SPORTS = {
    "tennis", "running", "athletics", "track", "swimming", "gym", "fitness", "weightlifting", "rowing",
    "boxing", "judo", "taekwondo", "karate", "wrestling", "golf", "surfing", "cycling", "triathlon",
    "badminton", "table tennis", "skateboarding",
}

GYM_ALIASES = {"gym", "fitness", "weight training", "bodybuilding", "academia", "musculacao", "musculação"}
COMMON_BOOL_YES = {"yes", "y", "true", "1", "sim", "s", "yeah", "yep", "sure", "ok", "okay"}
COMMON_BOOL_NO = {"no", "n", "false", "0", "nao", "não", "nope", "nah"}
COMMON_ANSWER_ALIASES = {
    "performance": "Improve performance", "performace": "Improve performance", "perfomance": "Improve performance", "perf": "Improve performance", "improve": "Improve performance",
    "fitness": "Build fitness", "fit": "Build fitness", "get fit": "Build fitness", "conditioning": "Build fitness",
    "return": "Return after a break", "comeback": "Return after a break", "break": "Return after a break",
    "learn": "Learn how to play", "learn to play": "Learn how to play",
    "injury": "Injury prevention", "prevention": "Injury prevention", "prevent injury": "Injury prevention",
    "competition": "Competition preparation", "comp prep": "Competition preparation", "match prep": "Competition preparation",
    "general": "General Fitness", "general fitness": "General Fitness", "health": "General Fitness",
    "hypertrophy": "Hypertrophy", "hypertrofy": "Hypertrophy", "hypert": "Hypertrophy", "muscle": "Hypertrophy", "muscle gain": "Hypertrophy", "bulk": "Hypertrophy",
    "fat loss": "Fat Loss", "fatloss": "Fat Loss", "lose fat": "Fat Loss", "weight loss": "Fat Loss", "cut": "Fat Loss", "lean": "Fat Loss",
    "athletic": "Athletic Performance", "athlete": "Athletic Performance", "sport performance": "Athletic Performance",
    "begginer": "Beginner", "beginner": "Beginner", "new": "Beginner", "newbie": "Beginner",
    "intermediate": "Intermediate", "intermidiate": "Intermediate", "medium": "Intermediate",
    "advanced": "Advanced", "advance": "Advanced", "elite": "Elite", "pro": "Elite", "experienced": "Experienced", "expert": "Experienced",
    "balanced": "Balanced Session", "balance": "Balanced Session", "normal": "Balanced Session",
    "technical": "Technical Priority", "tech": "Technical Priority", "physical": "Physical Priority", "phys": "Physical Priority",
    "competition week": "Competition Week", "comp week": "Competition Week", "intense": "Intense Session", "hard": "Intense Session", "heavy": "Intense Session",
    "minimal": "Minimal", "minimum": "Minimal", "basic": "Basic", "medium equipment": "Medium", "competitive": "Competitive", "full": "Elite",
    "low": "Low", "moderate": "Moderate", "high": "High", "controlled": "Controlled", "standard": "Standard", "peak": "Peak",
    "speed": "Speed", "power": "Power", "quality": "Technical Quality", "strength": "Strength", "movement": "Movement Quality", "match rhythm": "Match Rhythm",
}

INTENSITY_NOTES = {
    "Controlled": "Keep quality-first pacing. Leave reserve in the tank and do not chase fatigue.",
    "Standard": "Normal productive training intensity. Strong quality, but not an all-out day.",
    "High": "High-output day. Prioritize sharp execution, full recoveries on speed work, and stop if mechanics fade.",
    "Peak": "Very high intent. Use only when readiness is truly high and the athlete is not carrying pain or excessive fatigue.",
}

CATEGORY_BASE_SHARES = {
    "Warm-Up": 0.18,
    "Technical": 0.26,
    "Physical": 0.30,
    "Tactical": 0.18,
    "Recovery": 0.08,
}

SESSION_TYPE_CATEGORY_ADJUSTMENTS = {
    "Balanced Session": {"Technical": 1.0, "Physical": 1.0, "Tactical": 1.0},
    "Technical Priority": {"Technical": 1.25, "Physical": 0.85, "Tactical": 0.9},
    "Physical Priority": {"Technical": 0.85, "Physical": 1.3, "Tactical": 0.9},
    "Competition Week": {"Technical": 1.05, "Physical": 0.75, "Tactical": 1.1},
}

READINESS_MULTIPLIERS = {
    "Low": 0.88,
    "Moderate": 1.0,
    "High": 1.08,
}

GOAL_PRIORITIES = {
    "Improve performance": ["Technical", "Physical", "Tactical"],
    "Build fitness": ["Physical", "Technical", "Recovery"],
    "Return after a break": ["Warm-Up", "Technical", "Recovery"],
    "Learn how to play": ["Warm-Up", "Technical", "Recovery"],
    "Injury prevention": ["Warm-Up", "Physical", "Recovery"],
    "Competition preparation": ["Technical", "Tactical", "Physical"],
}

EQUIPMENT_LEVEL_DETAILS = {
    "Minimal": {"label": "Minimal", "description": "Very limited setup.", "includes": ["Bodyweight", "Open space", "Floor or grass area"]},
    "Basic": {"label": "Basic", "description": "Simple field or court access plus a few tools.", "includes": ["Balls", "Cones", "Bands"]},
    "Medium": {"label": "Medium", "description": "Good general setup for most athletes.", "includes": ["Cones", "Bands", "Dumbbells", "Medicine ball"]},
    "Competitive": {"label": "Competitive", "description": "Strong club-level training environment.", "includes": ["Full sport setup", "Gym access", "Strength equipment"]},
    "Elite": {"label": "Elite", "description": "High-performance environment.", "includes": ["Complete facility", "Full gym", "Recovery resources"]},
}


# -----------------------------------------------------------------------------
# LIBRARY (kept structured, but prescriptions for gym are displayed as ranges)
# -----------------------------------------------------------------------------
SPORT_LIBRARY: Dict[str, Dict[str, List[Exercise]]] = {
    "Gym": {
        "Warm-Up": [
            Exercise("Cardio primer + mobility", "Warm-Up", "2-3 blocks of easy cardio and mobility flow", "General prep.", ["Cardio machine", "Bodyweight"], ["Low"], ["Movement Quality"], ["All"], ["All"], ["All"], 1.0),
            Exercise("Bracing and hinge prep", "Warm-Up", "2-3 guided activation blocks", "Prime safer lifting mechanics.", ["Bodyweight", "Bands"], ["Low"], ["Movement Quality"], ["All"], ["All"], ["All"], 0.8),
        ],
        "Technical": [
            Exercise("Movement pattern rehearsal", "Technical", "2-3 lighter setup blocks before main lifts", "Safer lifting.", ["Barbell", "Dumbbells", "Machines"], ["Low"], ["Technical Quality"], ["All"], ["All"], ["All"], 0.7),
            Exercise("Tempo skill set", "Technical", "2-3 controlled technique blocks", "Improve position awareness.", ["Barbell", "Dumbbells"], ["Low", "Moderate"], ["Technical Quality"], ["All"], ["All"], ["All"], 0.75),
        ],
        "Physical": [
            Exercise("Squat or leg press", "Physical", "3-4 working blocks in the hypertrophy or strength range", "Lower-body strength.", ["Barbell", "Machine"], ["Moderate", "High"], ["Strength"], ["Hypertrophy", "Athletic Performance", "General Fitness"], ["Intermediate", "Advanced", "Elite"], ["All"], 1.2),
            Exercise("Bench or push variation", "Physical", "3-4 working blocks with quality pushing volume", "Upper-body pushing.", ["Barbell", "Dumbbells", "Machine"], ["Moderate", "High"], ["Strength"], ["All"], ["Intermediate", "Advanced", "Elite"], ["All"], 1.05),
            Exercise("Row or pull variation", "Physical", "3-4 working blocks with strong pulling quality", "Upper-body pulling.", ["Barbell", "Dumbbells", "Machine"], ["Moderate", "High"], ["Strength"], ["All"], ["Intermediate", "Advanced", "Elite"], ["All"], 1.05),
            Exercise("Conditioning finisher", "Physical", "2-4 conditioning rounds", "Work capacity.", ["Cardio machine", "Bodyweight"], ["High"], ["Conditioning"], ["Fat Loss", "General Fitness", "Athletic Performance"], ["Intermediate", "Advanced", "Elite"], ["All"], 1.0),
            Exercise("Trap bar jump or med-ball throw", "Physical", "3-4 explosive blocks", "Fast force development.", ["Trap bar", "Medicine ball"], ["High"], ["Power"], ["Athletic Performance"], ["Advanced", "Elite"], ["All"], 0.8),
        ],
        "Recovery": [
            Exercise("Cooldown stretch", "Recovery", "1-2 cooldown blocks", "Recovery.", ["Bodyweight"], ["Low"], ["Movement Quality"], ["All"], ["All"], ["All"], 0.75),
        ],
    },
    "Soccer": {
        "Warm-Up": [
            Exercise("Jog + mobility flow", "Warm-Up", "6 minutes easy jog + mobility flow", "Raise body temperature and open hips/ankles.", ["Bodyweight", "Open space"], ["Low"], ["Movement Quality"], ["All"], ["All"], ["All"], 1.1),
            Exercise("Dynamic activation", "Warm-Up", "2-3 movement rounds", "Prepare sprint mechanics.", ["Open space"], ["Low", "Moderate"], ["Speed"], ["All"], ["All"], ["All"], 0.9),
        ],
        "Technical": [
            Exercise("First-touch passing circuit", "Technical", "3-4 passing rounds", "Improve control and passing rhythm.", ["Ball", "Open space"], ["Moderate"], ["Technical Quality"], ["All"], ["All"], ["All"], 1.0),
            Exercise("Dribble slalom + exit sprint", "Technical", "5-6 dribble efforts", "Tight control under speed.", ["Ball", "Cones"], ["Moderate", "High"], ["Speed", "Technical Quality"], ["Winger", "Striker", "Attacking Midfielder", "Full Back"], ["All"], ["All"], 0.85),
        ],
        "Physical": [
            Exercise("Acceleration sprints", "Physical", "6-8 acceleration efforts", "Explosive first steps.", ["Open space"], ["High"], ["Speed"], ["All"], ["All"], ["All"], 0.85),
            Exercise("Split squats", "Physical", "3-4 strength blocks each side", "Single-leg strength.", ["Bodyweight", "Dumbbells"], ["Moderate"], ["Strength"], ["All"], ["All"], ["All"], 0.9),
        ],
        "Tactical": [
            Exercise("Small-sided game", "Tactical", "3-4 game rounds", "Decision-making under pressure.", ["Ball", "Field"], ["High"], ["Match Rhythm", "Conditioning"], ["All"], ["All"], ["All"], 1.3),
        ],
        "Recovery": [
            Exercise("Breathing walk + stretch", "Recovery", "1-2 cooldown blocks", "Downregulate and improve recovery.", ["Bodyweight"], ["Low"], ["Movement Quality"], ["All"], ["All"], ["All"], 0.8),
        ],
    },
    "Tennis": {
        "Warm-Up": [
            Exercise("Mini tennis + mobility", "Warm-Up", "2-3 prep blocks", "Feel and footwork.", ["Racket", "Ball", "Court"], ["Low"], ["Technical Quality", "Movement Quality"], ["All"], ["All"], ["All"], 1.1),
            Exercise("Serve shoulder prep", "Warm-Up", "2 shoulder activation blocks", "Prepare the shoulder complex.", ["Bands", "Bodyweight"], ["Low"], ["Movement Quality"], ["All"], ["All"], ["All"], 0.8),
        ],
        "Technical": [
            Exercise("Crosscourt consistency", "Technical", "3-4 consistency rounds", "Rally tolerance.", ["Racket", "Ball", "Court"], ["Moderate"], ["Technical Quality", "Conditioning"], ["All"], ["All"], ["All"], 1.2),
            Exercise("Serve targets", "Technical", "3-4 focused serve blocks", "Placement and confidence.", ["Racket", "Ball", "Court"], ["Moderate"], ["Technical Quality"], ["All"], ["All"], ["All"], 1.0),
        ],
        "Physical": [
            Exercise("Lateral shuffle intervals", "Physical", "5-6 lateral movement rounds", "Court movement endurance.", ["Court"], ["High"], ["Conditioning", "Movement Quality"], ["All"], ["All"], ["All"], 0.85),
            Exercise("Medicine ball rotations", "Physical", "3-4 rotational power blocks", "Rotational power.", ["Medicine ball"], ["Moderate"], ["Power"], ["All"], ["All"], ["All"], 0.85),
        ],
        "Tactical": [
            Exercise("Pattern play", "Tactical", "3-5 pattern rounds", "Build point construction.", ["Racket", "Ball", "Court"], ["Moderate"], ["Match Rhythm", "Technical Quality"], ["All"], ["All"], ["All"], 1.0),
        ],
        "Recovery": [
            Exercise("Forearm/hip mobility", "Recovery", "1-2 mobility cooldown blocks", "Reduce stiffness.", ["Bodyweight"], ["Low"], ["Movement Quality"], ["All"], ["All"], ["All"], 0.75),
        ],
    },
}

DEFAULT_GENERAL_LIBRARY = {
    "Warm-Up": [
        Exercise("General dynamic warm-up", "Warm-Up", "2-3 progressive warm-up blocks", "Raise temperature and mobility.", ["Bodyweight"], ["Low"], ["Movement Quality"], ["All"], ["All"], ["All"], 1.0),
    ],
    "Technical": [
        Exercise("Sport-specific skill block", "Technical", "3-4 technical rounds", "Rehearse core sport actions.", ["Sport equipment if available"], ["Moderate"], ["Technical Quality"], ["All"], ["All"], ["All"], 1.0),
    ],
    "Physical": [
        Exercise("General athletic block", "Physical", "3-4 physical working blocks", "Build sport-supporting qualities.", ["Bodyweight", "Bands", "Basic weights if available"], ["Moderate"], ["Strength", "Conditioning"], ["All"], ["All"], ["All"], 1.0),
    ],
    "Tactical": [
        Exercise("Decision-making / rhythm block", "Tactical", "2-3 structured rounds", "Connect skill to sport context.", ["Open space", "Sport equipment if available"], ["Moderate"], ["Match Rhythm"], ["All"], ["All"], ["All"], 1.0),
    ],
    "Recovery": [
        Exercise("Cooldown and recovery", "Recovery", "1-2 recovery blocks", "Bring effort down and restore movement quality.", ["Bodyweight"], ["Low"], ["Movement Quality"], ["All"], ["All"], ["All"], 0.8),
    ],
}

SPORT_DURATION_STYLE = {
    "Soccer": {"short": 6, "standard": 7, "long": 8},
    "Tennis": {"short": 5, "standard": 6, "long": 7},
    "Gym": {"short": 5, "standard": 6, "long": 7},
    "default": {"short": 5, "standard": 6, "long": 7},
}

SPORT_BLUEPRINTS = {
    "Soccer": {
        "Balanced Session": {"Warm-Up": 2, "Technical": 2, "Physical": 2, "Tactical": 1, "Recovery": 1},
        "Technical Priority": {"Warm-Up": 2, "Technical": 3, "Physical": 1, "Tactical": 1, "Recovery": 1},
        "Physical Priority": {"Warm-Up": 2, "Technical": 1, "Physical": 3, "Tactical": 1, "Recovery": 1},
        "Competition Week": {"Warm-Up": 2, "Technical": 2, "Physical": 1, "Tactical": 1, "Recovery": 1},
    },
    "Tennis": {
        "Balanced Session": {"Warm-Up": 2, "Technical": 2, "Physical": 2, "Tactical": 1, "Recovery": 1},
        "Technical Priority": {"Warm-Up": 2, "Technical": 3, "Physical": 1, "Tactical": 1, "Recovery": 1},
        "Physical Priority": {"Warm-Up": 2, "Technical": 1, "Physical": 3, "Tactical": 0, "Recovery": 1},
        "Competition Week": {"Warm-Up": 2, "Technical": 2, "Physical": 1, "Tactical": 1, "Recovery": 1},
    },
    "Gym": {
        "Balanced Session": {"Warm-Up": 1, "Technical": 1, "Physical": 3, "Tactical": 0, "Recovery": 1},
        "Technical Priority": {"Warm-Up": 1, "Technical": 1, "Physical": 3, "Tactical": 0, "Recovery": 1},
        "Physical Priority": {"Warm-Up": 1, "Technical": 0, "Physical": 4, "Tactical": 0, "Recovery": 1},
        "Competition Week": {"Warm-Up": 1, "Technical": 1, "Physical": 2, "Tactical": 0, "Recovery": 1},
    },
}

DEFAULT_BLUEPRINTS = {
    "Balanced Session": {"Warm-Up": 2, "Technical": 2, "Physical": 2, "Tactical": 1, "Recovery": 1},
    "Technical Priority": {"Warm-Up": 2, "Technical": 3, "Physical": 1, "Tactical": 1, "Recovery": 1},
    "Physical Priority": {"Warm-Up": 2, "Technical": 1, "Physical": 3, "Tactical": 1, "Recovery": 1},
    "Competition Week": {"Warm-Up": 2, "Technical": 2, "Physical": 1, "Tactical": 1, "Recovery": 1},
}


# -----------------------------------------------------------------------------
# CHAT FLOW
# -----------------------------------------------------------------------------
def init_generator_state() -> None:
    defaults = {
        "generator_chat_messages": [],
        "training_chat_started": False,
        "training_question_index": 0,
        "training_chat_complete": False,
        "training_profile": {},
        "latest_training_payload": None,
        "latest_training_summary": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def normalize_text(text: str) -> str:
    return " ".join(str(text).strip().split())


def normalize_lower(text: str) -> str:
    return normalize_text(text).lower()


def canonical_compact(text: str) -> str:
    lowered = normalize_lower(text)
    replacements = {"á":"a","à":"a","ã":"a","â":"a","é":"e","ê":"e","í":"i","ó":"o","ô":"o","õ":"o","ú":"u","ç":"c"}
    for old, new in replacements.items():
        lowered = lowered.replace(old, new)
    lowered = re.sub(r"[^a-z0-9]+", " ", lowered)
    return " ".join(lowered.split())


def is_gym_sport(sport_text: str) -> bool:
    compact = canonical_compact(sport_text)
    return compact in {canonical_compact(x) for x in GYM_ALIASES}


def detect_sport_type(sport_text: str) -> str:
    sport = canonical_compact(sport_text)
    if not sport:
        return ""
    if sport in {canonical_compact(x) for x in KNOWN_TEAM_SPORTS}:
        return "Team Sport"
    if sport in {canonical_compact(x) for x in KNOWN_INDIVIDUAL_SPORTS} or is_gym_sport(sport):
        return "Individual Sport"
    return ""


def match_supported_sport(sport_text: str) -> Optional[str]:
    normalized = canonical_compact(sport_text)
    aliases = {"football": "Soccer", "soccer": "Soccer", "futebol": "Soccer", "water polo": "Water Polo", "waterpolo": "Water Polo", "polo aquatico": "Water Polo", "gym": "Gym", "fitness": "Gym", "academia": "Gym", "musculacao": "Gym", "bodybuilding": "Gym", "weight training": "Gym"}
    if normalized in aliases:
        return aliases[normalized]
    for sport_name in SPORT_POSITIONS:
        if canonical_compact(sport_name) == normalized:
            return sport_name
    return None


def get_frequency_prompt(goal: str, level: str, sport: str = "") -> str:
    if is_gym_sport(sport):
        return "How many times do you train per week?"
    if goal == "Learn how to play" or level == "Beginner":
        return "How many times do you play sports per week?"
    return "How many times do you train this sport per week?"


def match_option_forgiving(answer: str, options: List[str]) -> Optional[str]:
    compact = canonical_compact(answer)
    if not compact:
        return None
    option_map = {canonical_compact(str(opt)): str(opt) for opt in options}
    if compact in option_map:
        return option_map[compact]
    alias_value = COMMON_ANSWER_ALIASES.get(compact)
    if alias_value and alias_value in options:
        return alias_value
    prefix_matches = [opt for key, opt in option_map.items() if key.startswith(compact) or compact.startswith(key)]
    if len(prefix_matches) == 1:
        return prefix_matches[0]
    contains_matches = [opt for key, opt in option_map.items() if compact in key or key in compact]
    if len(contains_matches) == 1:
        return contains_matches[0]
    try:
        import difflib
        close = difflib.get_close_matches(compact, list(option_map.keys()) + list(COMMON_ANSWER_ALIASES.keys()), n=1, cutoff=0.76)
        if close:
            key = close[0]
            if key in option_map:
                return option_map[key]
            alias_value = COMMON_ANSWER_ALIASES.get(key)
            if alias_value in options:
                return alias_value
    except Exception:
        pass
    return None


def get_question_flow(profile: Dict[str, str]) -> List[Dict[str, object]]:
    sport = profile.get("sport", "")
    sport_type = profile.get("sport_type", "") or detect_sport_type(sport)
    supported_sport = match_supported_sport(sport)
    gym_mode = bool(supported_sport == "Gym" or is_gym_sport(sport))
    positions = SPORT_POSITIONS.get(supported_sport, ["General Profile"])

    logged_in = bool(st.session_state.get("profile_email", "").strip())
    saved_name = normalize_text(str(st.session_state.get("athlete_name", "") or profile.get("athlete_name", "")))
    is_professional_value = profile.get("is_professional", False)
    is_professional = bool(is_professional_value is True or str(is_professional_value).strip().lower() in {"yes", "true", "1"})
    should_ask_name = (not logged_in) and (not saved_name) and is_professional and not gym_mode

    flow = [{"key": "sport", "prompt": "What physical activity/sport do you play?", "type": "text"}]

    if not gym_mode:
        flow.append({"key": "sport_type", "prompt": "Is this an individual sport or a team sport? You can answer: Individual Sport or Team Sport.", "type": "select", "options": ["Individual Sport", "Team Sport"], "skip_if_detected": True})

    if sport_type == "Team Sport" and not gym_mode:
        flow.append({"key": "team_name", "prompt": "What team do you play for?", "type": "text"})

    if gym_mode:
        flow.extend([
            {"key": "goal", "prompt": "What is your main gym goal?", "type": "select", "options": GYM_GOALS},
            {"key": "level", "prompt": "What is your current gym level?", "type": "select", "options": GYM_LEVELS},
            {"key": "weekly_target", "prompt": get_frequency_prompt(profile.get("goal", ""), profile.get("level", ""), sport), "type": "int", "min": 1, "max": 7},
            {"key": "session_type", "prompt": "What kind of gym session do you want today?", "type": "select", "options": GYM_SESSION_TYPES},
            {"key": "duration", "prompt": "How many minutes should this gym session last?", "type": "int", "min": 30, "max": 180},
            {"key": "equipment_level", "prompt": "What is your level of equipment available?", "type": "select", "options": EQUIPMENT_LEVELS},
            {"key": "readiness", "prompt": "How is your readiness today?", "type": "select", "options": READINESS_OPTIONS},
            {"key": "pain_flag", "prompt": "Is there pain or discomfort today? Answer Yes or No.", "type": "bool"},
            {"key": "needs_low_impact", "prompt": "Do you prefer lower-impact loading today? Answer Yes or No.", "type": "bool"},
            {"key": "notes", "prompt": "Any extra notes? If not, answer: none.", "type": "text"},
        ])
    else:
        flow.extend([
            {"key": "goal", "prompt": "What is your main goal?", "type": "select", "options": GOALS},
            {"key": "level", "prompt": "What is your current level?", "type": "select", "options": LEVELS},
            {"key": "weekly_target", "prompt": get_frequency_prompt(profile.get("goal", ""), profile.get("level", ""), sport), "type": "int", "min": 1, "max": 7},
            {"key": "position", "prompt": "What is your position or role in this sport?", "type": "select_or_text", "options": positions},
            {"key": "session_type", "prompt": "What kind of session do you want today?", "type": "select", "options": SESSION_TYPES},
            {"key": "duration", "prompt": "How many minutes should this session last?", "type": "int", "min": 30, "max": 180},
            {"key": "equipment_level", "prompt": "What is your level of equipment available?", "type": "select", "options": EQUIPMENT_LEVELS},
            {"key": "season_phase", "prompt": "What season phase are you in?", "type": "select", "options": SEASON_PHASES},
            {"key": "primary_focus", "prompt": "What is the main focus for today?", "type": "select", "options": PRIMARY_FOCUS_OPTIONS},
            {"key": "readiness", "prompt": "How is your readiness today?", "type": "select", "options": READINESS_OPTIONS},
            {"key": "intensity_mode", "prompt": "What intensity mode do you want today?", "type": "select", "options": INTENSITY_MODES},
            {"key": "pain_flag", "prompt": "Is there pain or discomfort today? Answer Yes or No.", "type": "bool"},
            {"key": "competition_soon", "prompt": "Do you have a competition or match in the next 3 days? Answer Yes or No.", "type": "bool"},
            {"key": "needs_low_impact", "prompt": "Do you prefer lower-impact loading today? Answer Yes or No.", "type": "bool"},
            {"key": "notes", "prompt": "Any extra notes? If not, answer: none.", "type": "text"},
        ])

    if (not gym_mode) and profile.get("level") in ["Advanced", "Elite"]:
        insert_idx = 5 if sport_type == "Team Sport" else 4
        flow.insert(insert_idx, {"key": "is_professional", "prompt": "Are you professional in this sport? Answer Yes or No.", "type": "bool"})

    if should_ask_name:
        name_prompt = "What is your name?"
        insert_idx = 6 if sport_type == "Team Sport" else 5
        flow.insert(insert_idx, {"key": "athlete_name", "prompt": name_prompt, "type": "text"})

    cleaned_flow = []
    for q in flow:
        if q.get("key") == "sport_type" and q.get("skip_if_detected") and detect_sport_type(profile.get("sport", "")):
            continue
        cleaned_flow.append(q)
    return cleaned_flow


def append_bot_message(text: str) -> None:
    st.session_state.generator_chat_messages.append({"role": "assistant", "content": text})


def append_user_message(text: str) -> None:
    st.session_state.generator_chat_messages.append({"role": "user", "content": text})


def reset_training_chat() -> None:
    st.session_state.generator_chat_messages = []
    st.session_state.training_chat_started = False
    st.session_state.training_question_index = 0
    st.session_state.training_chat_complete = False
    st.session_state.training_profile = {}
    st.session_state.latest_training_payload = None
    st.session_state.latest_training_summary = None


def start_training_chat() -> None:
    reset_training_chat()
    st.session_state.training_chat_started = True
    append_bot_message("Lets train today?")
    flow = get_question_flow(st.session_state.training_profile)
    if flow:
        append_bot_message(flow[0]["prompt"])


def validate_answer(question: Dict[str, object], raw_answer: str) -> Tuple[bool, object, Optional[str]]:
    answer = normalize_text(raw_answer)
    q_type = question["type"]

    if q_type == "text":
        return True, answer, None

    if q_type == "int":
        number_match = re.search(r"\d+", answer)
        if not number_match:
            return False, None, "Please answer with a number."
        value = int(number_match.group(0))
        min_v = int(question.get("min", 0))
        max_v = int(question.get("max", 999))
        if value < min_v or value > max_v:
            return False, None, f"Please answer with a number between {min_v} and {max_v}."
        return True, value, None

    if q_type == "bool":
        lowered = canonical_compact(answer)
        if lowered in {canonical_compact(x) for x in COMMON_BOOL_YES}:
            return True, True, None
        if lowered in {canonical_compact(x) for x in COMMON_BOOL_NO}:
            return True, False, None
        return False, None, "Please answer Yes or No."

    if q_type == "select":
        options = [str(opt) for opt in question.get("options", [])]
        matched = match_option_forgiving(answer, options)
        if matched:
            return True, matched, None
        return False, None, "Please answer using one of the shown options. Short answers and common typos are accepted."

    if q_type == "select_or_text":
        options = [str(opt) for opt in question.get("options", [])]
        matched = match_option_forgiving(answer, options)
        if matched:
            return True, matched, None
        return True, answer, None

    return True, answer, None


def update_profile_from_answer(key: str, value: object) -> None:
    st.session_state.training_profile[key] = value

    if key == "sport":
        detected = detect_sport_type(str(value))
        if detected:
            st.session_state.training_profile["sport_type"] = detected
    if key == "goal":
        st.session_state.goal = value
    if key == "level":
        st.session_state.level = value
    if key == "sport":
        st.session_state.sport = value
    if key == "athlete_name":
        st.session_state.athlete_name = value
    if key == "team_name":
        st.session_state.team_name = value
    if key == "weekly_target":
        st.session_state.weekly_target = value
    if key == "notes":
        st.session_state.home_notes = "" if str(value).lower() == "none" else str(value)
    if key == "sport_type":
        st.session_state.sport_type = value
    if key == "is_professional":
        st.session_state.is_professional = "Yes" if value else "No"


def handle_chat_reply(user_text: str) -> None:
    flow = get_question_flow(st.session_state.training_profile)
    idx = st.session_state.training_question_index
    if idx >= len(flow):
        return

    current_question = flow[idx]
    is_valid, parsed_value, error_text = validate_answer(current_question, user_text)
    append_user_message(user_text)

    if not is_valid:
        append_bot_message(error_text or "Invalid answer.")
        append_bot_message(current_question["prompt"])
        return

    update_profile_from_answer(str(current_question["key"]), parsed_value)
    st.session_state.training_question_index += 1

    refreshed_flow = get_question_flow(st.session_state.training_profile)
    if st.session_state.training_question_index < len(refreshed_flow):
        append_bot_message(refreshed_flow[st.session_state.training_question_index]["prompt"])
    else:
        st.session_state.training_chat_complete = True
        append_bot_message("Great. I have all the answers. I am generating your session now.")
        generate_training_from_chat_profile()


# -----------------------------------------------------------------------------
# GENERATION HELPERS
# -----------------------------------------------------------------------------
def duration_bucket(duration: int) -> str:
    if duration <= 55:
        return "short"
    if duration <= 95:
        return "standard"
    return "long"


def target_exercise_count(sport: str, duration: int) -> int:
    style = SPORT_DURATION_STYLE.get(sport, SPORT_DURATION_STYLE["default"])
    return style[duration_bucket(duration)]


def get_blueprint(sport: str, session_type: str) -> Dict[str, int]:
    sport_blueprints = SPORT_BLUEPRINTS.get(sport, {})
    return dict(sport_blueprints.get(session_type, DEFAULT_BLUEPRINTS[session_type]))


def trim_blueprint_to_target(blueprint: Dict[str, int], target_total: int) -> Dict[str, int]:
    adjusted = dict(blueprint)
    current_total = sum(adjusted.values())
    removable_order = ["Tactical", "Technical", "Physical", "Warm-Up"]
    addable_order = ["Technical", "Physical", "Tactical"]

    while current_total > target_total:
        changed = False
        for category in removable_order:
            minimum_allowed = 1 if category in ["Warm-Up", "Recovery"] and adjusted.get(category, 0) > 0 else 0
            if adjusted.get(category, 0) > minimum_allowed:
                adjusted[category] -= 1
                current_total -= 1
                changed = True
                break
        if not changed:
            break

    while current_total < target_total:
        for category in addable_order:
            adjusted[category] = adjusted.get(category, 0) + 1
            current_total += 1
            if current_total >= target_total:
                break
    return adjusted


def category_share_map(session_type: str, goal: str) -> Dict[str, float]:
    shares = dict(CATEGORY_BASE_SHARES)
    adjustments = SESSION_TYPE_CATEGORY_ADJUSTMENTS.get(session_type, {})
    for key, mult in adjustments.items():
        shares[key] = shares.get(key, 0.0) * mult
    for cat in GOAL_PRIORITIES.get(goal, []):
        shares[cat] = shares.get(cat, 0.0) * 1.08
    total = sum(shares.values()) or 1.0
    return {k: v / total for k, v in shares.items()}


def choose_exercises_for_category(library_items: List[Exercise], requested_count: int, position: str, level: str, season_phase: str, primary_focus: str) -> List[Exercise]:
    if not library_items or requested_count <= 0:
        return []
    scored: List[Tuple[float, Exercise]] = []
    for ex in library_items:
        score = 1.0 + random.uniform(0.0, 0.25)
        if not ex.position_tags or "All" in ex.position_tags or position in ex.position_tags:
            score += 1.0
        if not ex.level_tags or "All" in ex.level_tags or level in ex.level_tags:
            score += 0.5
        if not ex.phase_tags or "All" in ex.phase_tags or season_phase in ex.phase_tags:
            score += 0.5
        if primary_focus in ex.focus_tags:
            score += 0.8
        scored.append((score, ex))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [ex for _, ex in scored[:requested_count]]


def adjust_duration_for_readiness(duration: int, readiness: str, goal: str, session_type: str) -> int:
    multiplier = READINESS_MULTIPLIERS.get(readiness, 1.0)
    adjusted = round(duration * multiplier)
    if goal in ["Return after a break", "Injury prevention"]:
        adjusted = min(adjusted, duration)
    if session_type == "Competition Week":
        adjusted = min(adjusted, duration)
    return max(30, adjusted)


def allocate_block_minutes(session: List[Exercise], duration: int, session_type: str, goal: str) -> List[int]:
    shares = category_share_map(session_type, goal)
    category_weighted = [shares.get(ex.category, 0.1) * max(0.5, ex.time_weight) for ex in session]
    total_weight = sum(category_weighted) or 1.0
    minutes = [max(4, round(duration * (w / total_weight))) for w in category_weighted]

    diff = duration - sum(minutes)
    index_cycle = list(range(len(minutes)))
    i = 0
    while diff != 0 and index_cycle:
        idx = index_cycle[i % len(index_cycle)]
        if diff > 0:
            minutes[idx] += 1
            diff -= 1
        elif minutes[idx] > 4:
            minutes[idx] -= 1
            diff += 1
        i += 1
    return minutes


def build_session(profile: Dict[str, object]) -> Tuple[List[Exercise], List[int], Dict[str, object]]:
    raw_sport = str(profile.get("sport", "")).strip()
    supported_sport = match_supported_sport(raw_sport)
    sport_for_engine = supported_sport or "General"
    library = SPORT_LIBRARY.get(supported_sport, DEFAULT_GENERAL_LIBRARY)

    session_type = str(profile.get("session_type", "Balanced Session"))
    if session_type == "Intense Session":
        session_type = "Physical Priority"
    duration = int(profile.get("duration", 75))
    readiness = str(profile.get("readiness", "Moderate"))
    goal = str(profile.get("goal", "Improve performance"))
    level = str(profile.get("level", "Intermediate"))
    if level == "Experienced":
        level = "Advanced"
    season_phase = str(profile.get("season_phase", "All" if supported_sport == "Gym" else "In-Season"))
    primary_focus = str(profile.get("primary_focus", "Strength" if supported_sport == "Gym" else "Technical Quality"))
    position = str(profile.get("position", profile.get("goal", "General Fitness") if supported_sport == "Gym" else "General Profile"))

    adjusted_duration = adjust_duration_for_readiness(duration, readiness, goal, session_type)
    if bool(profile.get("competition_soon", False)):
        adjusted_duration = min(adjusted_duration, duration)
        if session_type == "Physical Priority":
            session_type = "Competition Week"
    if bool(profile.get("pain_flag", False)) or bool(profile.get("needs_low_impact", False)):
        adjusted_duration = max(30, adjusted_duration - 5)

    blueprint = get_blueprint(supported_sport or "default", session_type)
    blueprint = trim_blueprint_to_target(blueprint, target_exercise_count(supported_sport or "default", adjusted_duration))

    session: List[Exercise] = []
    for category, count in blueprint.items():
        session.extend(
            choose_exercises_for_category(
                library_items=library.get(category, []),
                requested_count=count,
                position=position,
                level=level,
                season_phase=season_phase,
                primary_focus=primary_focus,
            )
        )

    block_minutes = allocate_block_minutes(session, adjusted_duration, session_type, goal)

    meta = {
        "supported_sport": supported_sport,
        "sport_for_engine": sport_for_engine,
        "adjusted_duration": adjusted_duration,
        "session_type": session_type,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "gym_summary_enabled": bool(supported_sport == "Gym"),
    }
    return session, block_minutes, meta


def build_session_title(profile: Dict[str, object]) -> str:
    athlete = str(profile.get("athlete_name", "Athlete")).strip() or "Athlete"
    sport = str(profile.get("sport", "Sport")).strip() or "Sport"
    goal = str(profile.get("goal", "Performance")).strip()
    return f"{athlete} - {sport} session ({goal})"


def build_session_hash(profile: Dict[str, object], session: List[Exercise]) -> str:
    raw = f"{profile.get('athlete_name','')}|{profile.get('sport','')}|{profile.get('generated_at','')}|{'|'.join(ex.name for ex in session)}"
    return hashlib.md5(raw.encode("utf-8")).hexdigest()[:12]


def estimate_session_load(level: str, readiness: str, intensity_mode: str, duration: int) -> str:
    score = 0
    score += {"Beginner": 1, "Intermediate": 2, "Advanced": 3, "Elite": 4}.get(level, 2)
    score += {"Low": 0, "Moderate": 1, "High": 2}.get(readiness, 1)
    score += {"Controlled": 0, "Standard": 1, "High": 2, "Peak": 3}.get(intensity_mode, 1)
    score += 1 if duration >= 75 else 0
    score += 1 if duration >= 105 else 0
    if score <= 3:
        return "Low to Moderate"
    if score <= 6:
        return "Moderate"
    if score <= 8:
        return "Moderate to High"
    return "High"


def build_session_payload(profile: Dict[str, object], session: List[Exercise], block_minutes: List[int], meta: Dict[str, object]) -> Dict[str, object]:
    safe_profile = dict(profile)
    safe_profile["generated_at"] = meta["generated_at"]
    payload = {
        "session_id": build_session_hash(safe_profile, session),
        "title": build_session_title(profile),
        "profile": safe_profile,
        "meta": meta,
        "exercises": [
            {
                "name": ex.name,
                "category": ex.category,
                "prescription": ex.prescription,
                "purpose": ex.purpose,
                "coaching_points": ex.coaching_points,
                "planned_block_minutes": minutes,
            }
            for ex, minutes in zip(session, block_minutes)
        ],
    }
    return payload


def persist_generated_session(payload: Dict[str, object], on_persist: Optional[Callable[[], None]]) -> None:
    saved = st.session_state.get("saved_training_sessions", [])
    saved = [s for s in saved if s.get("session_id") != payload.get("session_id")]
    saved.insert(0, payload)
    st.session_state.saved_training_sessions = saved[:50]
    if on_persist:
        on_persist()


def generate_training_from_chat_profile() -> None:
    profile = dict(st.session_state.training_profile)
    session, block_minutes, meta = build_session(profile)
    payload = build_session_payload(profile, session, block_minutes, meta)
    st.session_state.latest_training_payload = payload
    st.session_state.latest_training_summary = None
    persist_generated_session(payload, st.session_state.get("_training_on_persist"))


# -----------------------------------------------------------------------------
# GYM TRAINING SUMMARY + LOGGING
# -----------------------------------------------------------------------------
def is_gym_session(payload: Optional[Dict[str, object]]) -> bool:
    if not payload:
        return False
    return bool(payload.get("meta", {}).get("gym_summary_enabled", False))


def initialize_summary_state(session_id: str, exercises: List[Dict[str, object]]) -> None:
    key = f"training_summary_{session_id}"
    if key not in st.session_state:
        st.session_state[key] = {
            ex["name"]: {"done": True, "reps": None, "weight": None}
            for ex in exercises
        }


def estimate_exercise_calories(exercise_name: str, category: str, reps: Optional[float], weight: Optional[float], done: bool) -> float:
    if not done:
        return 0.0
    reps_value = float(reps or 0)
    weight_value = float(weight or 0)

    category_base = {
        "Warm-Up": 35,
        "Technical": 55,
        "Physical": 95,
        "Tactical": 75,
        "Recovery": 25,
    }.get(category, 50)

    movement_bonus = (reps_value * 0.85) + (weight_value * 0.32)

    lower_name = exercise_name.lower()
    if any(word in lower_name for word in ["squat", "leg press", "deadlift", "trap bar"]):
        movement_bonus *= 1.22
    elif any(word in lower_name for word in ["bench", "push", "press"]):
        movement_bonus *= 1.08
    elif any(word in lower_name for word in ["row", "pull"]):
        movement_bonus *= 1.05
    elif any(word in lower_name for word in ["conditioning", "finisher"]):
        movement_bonus *= 1.35

    return round(category_base + movement_bonus, 1)


def summarize_logged_session(payload: Dict[str, object], exercise_logs: Dict[str, Dict[str, object]]) -> Dict[str, object]:
    exercises = payload["exercises"]
    total_calories = 0.0
    completed_count = 0
    skipped_count = 0
    total_weight_volume = 0.0
    strength_bias = 0
    conditioning_bias = 0

    for ex in exercises:
        name = ex["name"]
        category = ex["category"]
        log = exercise_logs.get(name, {})
        done = bool(log.get("done", False))
        reps = float(log.get("reps") or 0)
        weight = float(log.get("weight") or 0)

        calories = estimate_exercise_calories(name, category, reps, weight, done)
        total_calories += calories

        if done:
            completed_count += 1
            total_weight_volume += reps * weight
            if category == "Physical":
                strength_bias += 1
            if category in {"Warm-Up", "Conditioning", "Tactical"} or "conditioning" in name.lower():
                conditioning_bias += 1
        else:
            skipped_count += 1

    utilization = 0 if not exercises else round((completed_count / len(exercises)) * 100, 1)
    if strength_bias >= conditioning_bias + 1:
        suitability = "better suited for hypertrophy / strength support"
    elif conditioning_bias > strength_bias:
        suitability = "better suited for conditioning / calorie expenditure"
    else:
        suitability = "well balanced between strength support and general training quality"

    return {
        "total_estimated_calorie_burn": round(total_calories, 1),
        "aproveitamento_percent": utilization,
        "completed_count": completed_count,
        "skipped_count": skipped_count,
        "total_weight_volume": round(total_weight_volume, 1),
        "suitability_note": suitability,
    }


def compare_to_previous_logs(current_summary: Dict[str, object]) -> str:
    logs = st.session_state.get("user_training_logs", [])
    if not logs:
        return "This is your first saved gym training summary in this profile."

    previous = logs[0]
    prev_cals = float(previous.get("summary", {}).get("total_estimated_calorie_burn", 0))
    current_cals = float(current_summary.get("total_estimated_calorie_burn", 0))
    diff = round(current_cals - prev_cals, 1)

    if diff > 0:
        return f"Compared with your previous logged gym session, you burned about {diff} more estimated calories this time."
    if diff < 0:
        return f"Compared with your previous logged gym session, you burned about {abs(diff)} fewer estimated calories this time."
    return "Compared with your previous logged gym session, the estimated calorie burn stayed about the same."


def save_training_log(payload: Dict[str, object], exercise_logs: Dict[str, Dict[str, object]], summary: Dict[str, object], on_persist: Optional[Callable[[], None]]) -> None:
    log_record = {
        "session_id": payload.get("session_id"),
        "title": payload.get("title"),
        "logged_at": datetime.now().isoformat(timespec="seconds"),
        "sport": payload.get("profile", {}).get("sport"),
        "profile_email": st.session_state.get("profile_email", ""),
        "summary": summary,
        "exercise_logs": exercise_logs,
    }
    logs = st.session_state.get("user_training_logs", [])
    logs.insert(0, log_record)
    st.session_state.user_training_logs = logs[:100]
    st.session_state.latest_training_summary = log_record
    if on_persist:
        on_persist()


# -----------------------------------------------------------------------------
# RENDERERS
# -----------------------------------------------------------------------------
def render_chat_messages() -> None:
    for idx, message in enumerate(st.session_state.generator_chat_messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant" and idx == len(st.session_state.generator_chat_messages) - 1:
                flow = get_question_flow(st.session_state.training_profile)
                q_idx = st.session_state.training_question_index
                if q_idx < len(flow):
                    q = flow[q_idx]
                    if q.get("type") in {"select", "select_or_text"}:
                        options = q.get("options", [])
                        if options:
                            st.caption("Options: " + " | ".join(str(o) for o in options))


def render_current_session(payload: Dict[str, object]) -> None:
    profile = payload["profile"]
    meta = payload["meta"]
    exercises = payload["exercises"]
    intensity_mode = str(profile.get("intensity_mode", "Standard"))

    st.subheader(payload["title"])
    st.write(
        f"**Sport:** {profile.get('sport')} | **Position/Profile:** {profile.get('position')} | **Goal:** {profile.get('goal')} | "
        f"**Level:** {profile.get('level')} | **Weekly frequency:** {profile.get('weekly_target')} | "
        f"**Planned duration:** {meta.get('adjusted_duration')} min"
    )
    st.caption(
        f"Session type: {meta.get('session_type')} | Equipment: {profile.get('equipment_level')} | "
        f"Season phase: {profile.get('season_phase')} | Focus: {profile.get('primary_focus')}"
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Planned minutes", meta.get("adjusted_duration"))
    c2.metric("Estimated load", estimate_session_load(str(profile.get("level", "Intermediate")), str(profile.get("readiness", "Moderate")), intensity_mode, int(meta.get("adjusted_duration", 75))))
    c3.metric("Exercises / blocks", len(exercises))

    st.info(INTENSITY_NOTES.get(intensity_mode, INTENSITY_NOTES["Standard"]))
    notes = str(profile.get("notes", "")).strip()
    if notes and notes.lower() != "none":
        st.info(f"Context notes considered: {notes}")
    if bool(profile.get("pain_flag")):
        st.warning("Pain/discomfort flagged: reduce aggressive loading if symptoms change mechanics or movement quality.")
    if bool(profile.get("competition_soon")):
        st.warning("Competition proximity flagged: the session was kept sharper and less fatigue-heavy.")

    st.markdown("### Training blocks")
    for idx, ex in enumerate(exercises, start=1):
        with st.expander(f"{idx}. {ex['name']}", expanded=idx <= 3):
            st.markdown(f"**Category:** {ex['category']}")
            st.markdown(f"**Prescription:** {ex['prescription']}")
            st.markdown(f"**Purpose:** {ex['purpose']}")
            st.markdown(f"**Planned block duration:** ~{ex['planned_block_minutes']} minutes")
            coaching_points = ex.get("coaching_points") or []
            if coaching_points:
                st.markdown("**Coaching points:**")
                for point in coaching_points:
                    st.write(f"- {point}")


def render_training_summary_panel(payload: Dict[str, object], on_persist: Optional[Callable[[], None]]) -> None:
    if not is_gym_session(payload):
        return

    with st.expander("Training summary", expanded=False):
        st.write("Gym-only summary logger. Enter what was actually done for each exercise.")
        initialize_summary_state(payload["session_id"], payload["exercises"])
        state_key = f"training_summary_{payload['session_id']}"
        summary_state = st.session_state[state_key]

        for idx, ex in enumerate(payload["exercises"]):
            ex_name = ex["name"]
            row_key = f"{payload['session_id']}_{idx}"
            st.markdown(f"**{ex_name}**")
            c1, c2, c3 = st.columns([1.2, 1, 1])
            with c1:
                done_value = st.radio(
                    "Status",
                    ["Done", "Didn't do this one"],
                    index=0 if summary_state[ex_name]["done"] else 1,
                    horizontal=True,
                    key=f"done_{row_key}",
                )
                summary_state[ex_name]["done"] = done_value == "Done"
            with c2:
                reps = st.number_input(
                    "Number of reps",
                    min_value=0.0,
                    step=1.0,
                    value=float(summary_state[ex_name]["reps"] or 0),
                    disabled=not summary_state[ex_name]["done"],
                    key=f"reps_{row_key}",
                )
                summary_state[ex_name]["reps"] = reps if summary_state[ex_name]["done"] else None
            with c3:
                weight = st.number_input(
                    "Weight used",
                    min_value=0.0,
                    step=1.0,
                    value=float(summary_state[ex_name]["weight"] or 0),
                    disabled=not summary_state[ex_name]["done"],
                    key=f"weight_{row_key}",
                )
                summary_state[ex_name]["weight"] = weight if summary_state[ex_name]["done"] else None
            st.divider()

        if st.button("Calculate and save training summary", type="primary", use_container_width=True, key=f"save_summary_{payload['session_id']}"):
            summary = summarize_logged_session(payload, summary_state)
            comparison_text = compare_to_previous_logs(summary)
            save_training_log(payload, summary_state, summary, on_persist)
            st.success("Training summary saved.")
            st.info(
                f"Aproveitamento of the session: {summary['aproveitamento_percent']}%\n\n"
                f"Total estimated calorie burn for this session: {summary['total_estimated_calorie_burn']}\n\n"
                f"{comparison_text}\n\n"
                f"This session was {summary['suitability_note']}."
            )


def render_latest_summary_card() -> None:
    latest = st.session_state.get("latest_training_summary")
    if not latest:
        return
    summary = latest["summary"]
    st.markdown("### Latest saved gym summary")
    st.write(
        f"**Session:** {latest['title']} | **Logged at:** {latest['logged_at']} | "
        f"**Calories:** {summary['total_estimated_calorie_burn']} | **Aproveitamento:** {summary['aproveitamento_percent']}%"
    )
    st.caption(summary["suitability_note"])


def render_history_panel() -> None:
    with st.expander("Saved training history", expanded=False):
        generated = st.session_state.get("saved_training_sessions", [])
        logs = st.session_state.get("user_training_logs", [])

        st.markdown("**Generated sessions**")
        if not generated:
            st.caption("No generated sessions saved yet.")
        for session in generated[:8]:
            st.write(f"- {session['title']} | {session['meta']['generated_at']}")

        st.markdown("**Saved gym summaries**")
        if not logs:
            st.caption("No gym summaries logged yet.")
        for log in logs[:8]:
            st.write(
                f"- {log['title']} | {log['logged_at']} | Calories: {log['summary']['total_estimated_calorie_burn']} | Aproveitamento: {log['summary']['aproveitamento_percent']}%"
            )


def render_training_generator_section(on_persist: Optional[Callable[[], None]] = None) -> None:
    init_generator_state()
    st.session_state["_training_on_persist"] = on_persist

    st.header("Training Generator")
    st.write(
        "This section now starts as the default interface of the app. It unites the old homepage profile collection with the training generator, in a one-question-at-a-time chat flow."
    )

    top1, top2 = st.columns([1, 1])
    with top1:
        if not st.session_state.training_chat_started:
            if st.button("Start training chat", type="primary", use_container_width=True, key="start_training_chat_btn"):
                start_training_chat()
                st.rerun()
        else:
            if st.button("Restart training chat", use_container_width=True, key="restart_training_chat_btn"):
                start_training_chat()
                st.rerun()
    with top2:
        st.caption(
            "For non-cataloged sports, the chat still works and stores the profile. The code is already prepared so the future API can interpret those sports dynamically."
        )

    if st.session_state.training_chat_started:
        render_chat_messages()

        if not st.session_state.training_chat_complete:
            user_reply = st.chat_input("Type your answer here")
            if user_reply:
                handle_chat_reply(user_reply)
                if on_persist:
                    on_persist()
                st.rerun()

    latest_payload = st.session_state.get("latest_training_payload")
    if latest_payload:
        st.divider()
        render_current_session(latest_payload)
        render_training_summary_panel(latest_payload, on_persist)
        render_latest_summary_card()

    # Saved training history intentionally removed from the visible interface.


# -----------------------------------------------------------------------------
# Expanded generated catalogs for typo tolerance and deeper gym session variation.
# -----------------------------------------------------------------------------
EXTRA_COMMON_ANSWER_ALIASES = {
    "perf0": "Improve performance",
    "perform1": "Improve performance",
    "prfm2": "Improve performance",
    "hypert3": "Hypertrophy",
    "hypertro4": "Hypertrophy",
    "fat5": "Fat Loss",
    "loss6": "Fat Loss",
    "lean7": "Fat Loss",
    "cut8": "Fat Loss",
    "bulk9": "Hypertrophy",
    "fit10": "General Fitness",
    "fitness11": "General Fitness",
    "ath12": "Athletic Performance",
    "athletic13": "Athletic Performance",
    "balance14": "Balanced Session",
    "balanced15": "Balanced Session",
    "tech16": "Technical Priority",
    "technical17": "Technical Priority",
    "phys18": "Physical Priority",
    "physical19": "Physical Priority",
    "intense20": "Intense Session",
    "hard21": "Intense Session",
    "exper22": "Experienced",
    "experienced23": "Experienced",
    "beg24": "Beginner",
    "beginner25": "Beginner",
    "inter26": "Intermediate",
    "advance27": "Advanced",
    "adv28": "Advanced",
    "perf29": "Improve performance",
    "perform30": "Improve performance",
    "prfm31": "Improve performance",
    "hypert32": "Hypertrophy",
    "hypertro33": "Hypertrophy",
    "fat34": "Fat Loss",
    "loss35": "Fat Loss",
    "lean36": "Fat Loss",
    "cut37": "Fat Loss",
    "bulk38": "Hypertrophy",
    "fit39": "General Fitness",
    "fitness40": "General Fitness",
    "ath41": "Athletic Performance",
    "athletic42": "Athletic Performance",
    "balance43": "Balanced Session",
    "balanced44": "Balanced Session",
    "tech45": "Technical Priority",
    "technical46": "Technical Priority",
    "phys47": "Physical Priority",
    "physical48": "Physical Priority",
    "intense49": "Intense Session",
    "hard50": "Intense Session",
    "exper51": "Experienced",
    "experienced52": "Experienced",
    "beg53": "Beginner",
    "beginner54": "Beginner",
    "inter55": "Intermediate",
    "advance56": "Advanced",
    "adv57": "Advanced",
    "perf58": "Improve performance",
    "perform59": "Improve performance",
    "prfm60": "Improve performance",
    "hypert61": "Hypertrophy",
    "hypertro62": "Hypertrophy",
    "fat63": "Fat Loss",
    "loss64": "Fat Loss",
    "lean65": "Fat Loss",
    "cut66": "Fat Loss",
    "bulk67": "Hypertrophy",
    "fit68": "General Fitness",
    "fitness69": "General Fitness",
    "ath70": "Athletic Performance",
    "athletic71": "Athletic Performance",
    "balance72": "Balanced Session",
    "balanced73": "Balanced Session",
    "tech74": "Technical Priority",
    "technical75": "Technical Priority",
    "phys76": "Physical Priority",
    "physical77": "Physical Priority",
    "intense78": "Intense Session",
    "hard79": "Intense Session",
    "exper80": "Experienced",
    "experienced81": "Experienced",
    "beg82": "Beginner",
    "beginner83": "Beginner",
    "inter84": "Intermediate",
    "advance85": "Advanced",
    "adv86": "Advanced",
    "perf87": "Improve performance",
    "perform88": "Improve performance",
    "prfm89": "Improve performance",
    "hypert90": "Hypertrophy",
    "hypertro91": "Hypertrophy",
    "fat92": "Fat Loss",
    "loss93": "Fat Loss",
    "lean94": "Fat Loss",
    "cut95": "Fat Loss",
    "bulk96": "Hypertrophy",
    "fit97": "General Fitness",
    "fitness98": "General Fitness",
    "ath99": "Athletic Performance",
    "athletic100": "Athletic Performance",
    "balance101": "Balanced Session",
    "balanced102": "Balanced Session",
    "tech103": "Technical Priority",
    "technical104": "Technical Priority",
    "phys105": "Physical Priority",
    "physical106": "Physical Priority",
    "intense107": "Intense Session",
    "hard108": "Intense Session",
    "exper109": "Experienced",
    "experienced110": "Experienced",
    "beg111": "Beginner",
    "beginner112": "Beginner",
    "inter113": "Intermediate",
    "advance114": "Advanced",
    "adv115": "Advanced",
    "perf116": "Improve performance",
    "perform117": "Improve performance",
    "prfm118": "Improve performance",
    "hypert119": "Hypertrophy",
    "hypertro120": "Hypertrophy",
    "fat121": "Fat Loss",
    "loss122": "Fat Loss",
    "lean123": "Fat Loss",
    "cut124": "Fat Loss",
    "bulk125": "Hypertrophy",
    "fit126": "General Fitness",
    "fitness127": "General Fitness",
    "ath128": "Athletic Performance",
    "athletic129": "Athletic Performance",
    "balance130": "Balanced Session",
    "balanced131": "Balanced Session",
    "tech132": "Technical Priority",
    "technical133": "Technical Priority",
    "phys134": "Physical Priority",
    "physical135": "Physical Priority",
    "intense136": "Intense Session",
    "hard137": "Intense Session",
    "exper138": "Experienced",
    "experienced139": "Experienced",
    "beg140": "Beginner",
    "beginner141": "Beginner",
    "inter142": "Intermediate",
    "advance143": "Advanced",
    "adv144": "Advanced",
    "perf145": "Improve performance",
    "perform146": "Improve performance",
    "prfm147": "Improve performance",
    "hypert148": "Hypertrophy",
    "hypertro149": "Hypertrophy",
    "fat150": "Fat Loss",
    "loss151": "Fat Loss",
    "lean152": "Fat Loss",
    "cut153": "Fat Loss",
    "bulk154": "Hypertrophy",
    "fit155": "General Fitness",
    "fitness156": "General Fitness",
    "ath157": "Athletic Performance",
    "athletic158": "Athletic Performance",
    "balance159": "Balanced Session",
    "balanced160": "Balanced Session",
    "tech161": "Technical Priority",
    "technical162": "Technical Priority",
    "phys163": "Physical Priority",
    "physical164": "Physical Priority",
    "intense165": "Intense Session",
    "hard166": "Intense Session",
    "exper167": "Experienced",
    "experienced168": "Experienced",
    "beg169": "Beginner",
    "beginner170": "Beginner",
    "inter171": "Intermediate",
    "advance172": "Advanced",
    "adv173": "Advanced",
    "perf174": "Improve performance",
    "perform175": "Improve performance",
    "prfm176": "Improve performance",
    "hypert177": "Hypertrophy",
    "hypertro178": "Hypertrophy",
    "fat179": "Fat Loss",
    "loss180": "Fat Loss",
    "lean181": "Fat Loss",
    "cut182": "Fat Loss",
    "bulk183": "Hypertrophy",
    "fit184": "General Fitness",
    "fitness185": "General Fitness",
    "ath186": "Athletic Performance",
    "athletic187": "Athletic Performance",
    "balance188": "Balanced Session",
    "balanced189": "Balanced Session",
    "tech190": "Technical Priority",
    "technical191": "Technical Priority",
    "phys192": "Physical Priority",
    "physical193": "Physical Priority",
    "intense194": "Intense Session",
    "hard195": "Intense Session",
    "exper196": "Experienced",
    "experienced197": "Experienced",
    "beg198": "Beginner",
    "beginner199": "Beginner",
    "inter200": "Intermediate",
    "advance201": "Advanced",
    "adv202": "Advanced",
    "perf203": "Improve performance",
    "perform204": "Improve performance",
    "prfm205": "Improve performance",
    "hypert206": "Hypertrophy",
    "hypertro207": "Hypertrophy",
    "fat208": "Fat Loss",
    "loss209": "Fat Loss",
    "lean210": "Fat Loss",
    "cut211": "Fat Loss",
    "bulk212": "Hypertrophy",
    "fit213": "General Fitness",
    "fitness214": "General Fitness",
    "ath215": "Athletic Performance",
    "athletic216": "Athletic Performance",
    "balance217": "Balanced Session",
    "balanced218": "Balanced Session",
    "tech219": "Technical Priority",
    "technical220": "Technical Priority",
    "phys221": "Physical Priority",
    "physical222": "Physical Priority",
    "intense223": "Intense Session",
    "hard224": "Intense Session",
    "exper225": "Experienced",
    "experienced226": "Experienced",
    "beg227": "Beginner",
    "beginner228": "Beginner",
    "inter229": "Intermediate",
    "advance230": "Advanced",
    "adv231": "Advanced",
    "perf232": "Improve performance",
    "perform233": "Improve performance",
    "prfm234": "Improve performance",
    "hypert235": "Hypertrophy",
    "hypertro236": "Hypertrophy",
    "fat237": "Fat Loss",
    "loss238": "Fat Loss",
    "lean239": "Fat Loss",
    "cut240": "Fat Loss",
    "bulk241": "Hypertrophy",
    "fit242": "General Fitness",
    "fitness243": "General Fitness",
    "ath244": "Athletic Performance",
    "athletic245": "Athletic Performance",
    "balance246": "Balanced Session",
    "balanced247": "Balanced Session",
    "tech248": "Technical Priority",
    "technical249": "Technical Priority",
    "phys250": "Physical Priority",
    "physical251": "Physical Priority",
    "intense252": "Intense Session",
    "hard253": "Intense Session",
    "exper254": "Experienced",
    "experienced255": "Experienced",
    "beg256": "Beginner",
    "beginner257": "Beginner",
    "inter258": "Intermediate",
    "advance259": "Advanced",
    "adv260": "Advanced",
    "perf261": "Improve performance",
    "perform262": "Improve performance",
    "prfm263": "Improve performance",
    "hypert264": "Hypertrophy",
    "hypertro265": "Hypertrophy",
    "fat266": "Fat Loss",
    "loss267": "Fat Loss",
    "lean268": "Fat Loss",
    "cut269": "Fat Loss",
    "bulk270": "Hypertrophy",
    "fit271": "General Fitness",
    "fitness272": "General Fitness",
    "ath273": "Athletic Performance",
    "athletic274": "Athletic Performance",
    "balance275": "Balanced Session",
    "balanced276": "Balanced Session",
    "tech277": "Technical Priority",
    "technical278": "Technical Priority",
    "phys279": "Physical Priority",
    "physical280": "Physical Priority",
    "intense281": "Intense Session",
    "hard282": "Intense Session",
    "exper283": "Experienced",
    "experienced284": "Experienced",
    "beg285": "Beginner",
    "beginner286": "Beginner",
    "inter287": "Intermediate",
    "advance288": "Advanced",
    "adv289": "Advanced",
    "perf290": "Improve performance",
    "perform291": "Improve performance",
    "prfm292": "Improve performance",
    "hypert293": "Hypertrophy",
    "hypertro294": "Hypertrophy",
    "fat295": "Fat Loss",
    "loss296": "Fat Loss",
    "lean297": "Fat Loss",
    "cut298": "Fat Loss",
    "bulk299": "Hypertrophy",
    "fit300": "General Fitness",
    "fitness301": "General Fitness",
    "ath302": "Athletic Performance",
    "athletic303": "Athletic Performance",
    "balance304": "Balanced Session",
    "balanced305": "Balanced Session",
    "tech306": "Technical Priority",
    "technical307": "Technical Priority",
    "phys308": "Physical Priority",
    "physical309": "Physical Priority",
    "intense310": "Intense Session",
    "hard311": "Intense Session",
    "exper312": "Experienced",
    "experienced313": "Experienced",
    "beg314": "Beginner",
    "beginner315": "Beginner",
    "inter316": "Intermediate",
    "advance317": "Advanced",
    "adv318": "Advanced",
    "perf319": "Improve performance",
    "perform320": "Improve performance",
    "prfm321": "Improve performance",
    "hypert322": "Hypertrophy",
    "hypertro323": "Hypertrophy",
    "fat324": "Fat Loss",
    "loss325": "Fat Loss",
    "lean326": "Fat Loss",
    "cut327": "Fat Loss",
    "bulk328": "Hypertrophy",
    "fit329": "General Fitness",
    "fitness330": "General Fitness",
    "ath331": "Athletic Performance",
    "athletic332": "Athletic Performance",
    "balance333": "Balanced Session",
    "balanced334": "Balanced Session",
    "tech335": "Technical Priority",
    "technical336": "Technical Priority",
    "phys337": "Physical Priority",
    "physical338": "Physical Priority",
    "intense339": "Intense Session",
    "hard340": "Intense Session",
    "exper341": "Experienced",
    "experienced342": "Experienced",
    "beg343": "Beginner",
    "beginner344": "Beginner",
    "inter345": "Intermediate",
    "advance346": "Advanced",
    "adv347": "Advanced",
    "perf348": "Improve performance",
    "perform349": "Improve performance",
    "prfm350": "Improve performance",
    "hypert351": "Hypertrophy",
    "hypertro352": "Hypertrophy",
    "fat353": "Fat Loss",
    "loss354": "Fat Loss",
    "lean355": "Fat Loss",
    "cut356": "Fat Loss",
    "bulk357": "Hypertrophy",
    "fit358": "General Fitness",
    "fitness359": "General Fitness",
    "ath360": "Athletic Performance",
    "athletic361": "Athletic Performance",
    "balance362": "Balanced Session",
    "balanced363": "Balanced Session",
    "tech364": "Technical Priority",
    "technical365": "Technical Priority",
    "phys366": "Physical Priority",
    "physical367": "Physical Priority",
    "intense368": "Intense Session",
    "hard369": "Intense Session",
    "exper370": "Experienced",
    "experienced371": "Experienced",
    "beg372": "Beginner",
    "beginner373": "Beginner",
    "inter374": "Intermediate",
    "advance375": "Advanced",
    "adv376": "Advanced",
    "perf377": "Improve performance",
    "perform378": "Improve performance",
    "prfm379": "Improve performance",
    "hypert380": "Hypertrophy",
    "hypertro381": "Hypertrophy",
    "fat382": "Fat Loss",
    "loss383": "Fat Loss",
    "lean384": "Fat Loss",
    "cut385": "Fat Loss",
    "bulk386": "Hypertrophy",
    "fit387": "General Fitness",
    "fitness388": "General Fitness",
    "ath389": "Athletic Performance",
    "athletic390": "Athletic Performance",
    "balance391": "Balanced Session",
    "balanced392": "Balanced Session",
    "tech393": "Technical Priority",
    "technical394": "Technical Priority",
    "phys395": "Physical Priority",
    "physical396": "Physical Priority",
    "intense397": "Intense Session",
    "hard398": "Intense Session",
    "exper399": "Experienced",
    "experienced400": "Experienced",
    "beg401": "Beginner",
    "beginner402": "Beginner",
    "inter403": "Intermediate",
    "advance404": "Advanced",
    "adv405": "Advanced",
    "perf406": "Improve performance",
    "perform407": "Improve performance",
    "prfm408": "Improve performance",
    "hypert409": "Hypertrophy",
    "hypertro410": "Hypertrophy",
    "fat411": "Fat Loss",
    "loss412": "Fat Loss",
    "lean413": "Fat Loss",
    "cut414": "Fat Loss",
    "bulk415": "Hypertrophy",
    "fit416": "General Fitness",
    "fitness417": "General Fitness",
    "ath418": "Athletic Performance",
    "athletic419": "Athletic Performance",
    "balance420": "Balanced Session",
    "balanced421": "Balanced Session",
    "tech422": "Technical Priority",
    "technical423": "Technical Priority",
    "phys424": "Physical Priority",
    "physical425": "Physical Priority",
    "intense426": "Intense Session",
    "hard427": "Intense Session",
    "exper428": "Experienced",
    "experienced429": "Experienced",
    "beg430": "Beginner",
    "beginner431": "Beginner",
    "inter432": "Intermediate",
    "advance433": "Advanced",
    "adv434": "Advanced",
    "perf435": "Improve performance",
    "perform436": "Improve performance",
    "prfm437": "Improve performance",
    "hypert438": "Hypertrophy",
    "hypertro439": "Hypertrophy",
    "fat440": "Fat Loss",
    "loss441": "Fat Loss",
    "lean442": "Fat Loss",
    "cut443": "Fat Loss",
    "bulk444": "Hypertrophy",
    "fit445": "General Fitness",
    "fitness446": "General Fitness",
    "ath447": "Athletic Performance",
    "athletic448": "Athletic Performance",
    "balance449": "Balanced Session",
    "balanced450": "Balanced Session",
    "tech451": "Technical Priority",
    "technical452": "Technical Priority",
    "phys453": "Physical Priority",
    "physical454": "Physical Priority",
    "intense455": "Intense Session",
    "hard456": "Intense Session",
    "exper457": "Experienced",
    "experienced458": "Experienced",
    "beg459": "Beginner",
    "beginner460": "Beginner",
    "inter461": "Intermediate",
    "advance462": "Advanced",
    "adv463": "Advanced",
    "perf464": "Improve performance",
    "perform465": "Improve performance",
    "prfm466": "Improve performance",
    "hypert467": "Hypertrophy",
    "hypertro468": "Hypertrophy",
    "fat469": "Fat Loss",
    "loss470": "Fat Loss",
    "lean471": "Fat Loss",
    "cut472": "Fat Loss",
    "bulk473": "Hypertrophy",
    "fit474": "General Fitness",
    "fitness475": "General Fitness",
    "ath476": "Athletic Performance",
    "athletic477": "Athletic Performance",
    "balance478": "Balanced Session",
    "balanced479": "Balanced Session",
    "tech480": "Technical Priority",
    "technical481": "Technical Priority",
    "phys482": "Physical Priority",
    "physical483": "Physical Priority",
    "intense484": "Intense Session",
    "hard485": "Intense Session",
    "exper486": "Experienced",
    "experienced487": "Experienced",
    "beg488": "Beginner",
    "beginner489": "Beginner",
    "inter490": "Intermediate",
    "advance491": "Advanced",
    "adv492": "Advanced",
    "perf493": "Improve performance",
    "perform494": "Improve performance",
    "prfm495": "Improve performance",
    "hypert496": "Hypertrophy",
    "hypertro497": "Hypertrophy",
    "fat498": "Fat Loss",
    "loss499": "Fat Loss",
    "lean500": "Fat Loss",
    "cut501": "Fat Loss",
    "bulk502": "Hypertrophy",
    "fit503": "General Fitness",
    "fitness504": "General Fitness",
    "ath505": "Athletic Performance",
    "athletic506": "Athletic Performance",
    "balance507": "Balanced Session",
    "balanced508": "Balanced Session",
    "tech509": "Technical Priority",
    "technical510": "Technical Priority",
    "phys511": "Physical Priority",
    "physical512": "Physical Priority",
    "intense513": "Intense Session",
    "hard514": "Intense Session",
    "exper515": "Experienced",
    "experienced516": "Experienced",
    "beg517": "Beginner",
    "beginner518": "Beginner",
    "inter519": "Intermediate",
    "advance520": "Advanced",
    "adv521": "Advanced",
    "perf522": "Improve performance",
    "perform523": "Improve performance",
    "prfm524": "Improve performance",
    "hypert525": "Hypertrophy",
    "hypertro526": "Hypertrophy",
    "fat527": "Fat Loss",
    "loss528": "Fat Loss",
    "lean529": "Fat Loss",
    "cut530": "Fat Loss",
    "bulk531": "Hypertrophy",
    "fit532": "General Fitness",
    "fitness533": "General Fitness",
    "ath534": "Athletic Performance",
    "athletic535": "Athletic Performance",
    "balance536": "Balanced Session",
    "balanced537": "Balanced Session",
    "tech538": "Technical Priority",
    "technical539": "Technical Priority",
    "phys540": "Physical Priority",
    "physical541": "Physical Priority",
    "intense542": "Intense Session",
    "hard543": "Intense Session",
    "exper544": "Experienced",
    "experienced545": "Experienced",
    "beg546": "Beginner",
    "beginner547": "Beginner",
    "inter548": "Intermediate",
    "advance549": "Advanced",
    "adv550": "Advanced",
    "perf551": "Improve performance",
    "perform552": "Improve performance",
    "prfm553": "Improve performance",
    "hypert554": "Hypertrophy",
    "hypertro555": "Hypertrophy",
    "fat556": "Fat Loss",
    "loss557": "Fat Loss",
    "lean558": "Fat Loss",
    "cut559": "Fat Loss",
    "bulk560": "Hypertrophy",
    "fit561": "General Fitness",
    "fitness562": "General Fitness",
    "ath563": "Athletic Performance",
    "athletic564": "Athletic Performance",
    "balance565": "Balanced Session",
    "balanced566": "Balanced Session",
    "tech567": "Technical Priority",
    "technical568": "Technical Priority",
    "phys569": "Physical Priority",
    "physical570": "Physical Priority",
    "intense571": "Intense Session",
    "hard572": "Intense Session",
    "exper573": "Experienced",
    "experienced574": "Experienced",
    "beg575": "Beginner",
    "beginner576": "Beginner",
    "inter577": "Intermediate",
    "advance578": "Advanced",
    "adv579": "Advanced",
    "perf580": "Improve performance",
    "perform581": "Improve performance",
    "prfm582": "Improve performance",
    "hypert583": "Hypertrophy",
    "hypertro584": "Hypertrophy",
    "fat585": "Fat Loss",
    "loss586": "Fat Loss",
    "lean587": "Fat Loss",
    "cut588": "Fat Loss",
    "bulk589": "Hypertrophy",
    "fit590": "General Fitness",
    "fitness591": "General Fitness",
    "ath592": "Athletic Performance",
    "athletic593": "Athletic Performance",
    "balance594": "Balanced Session",
    "balanced595": "Balanced Session",
    "tech596": "Technical Priority",
    "technical597": "Technical Priority",
    "phys598": "Physical Priority",
    "physical599": "Physical Priority",
    "intense600": "Intense Session",
    "hard601": "Intense Session",
    "exper602": "Experienced",
    "experienced603": "Experienced",
    "beg604": "Beginner",
    "beginner605": "Beginner",
    "inter606": "Intermediate",
    "advance607": "Advanced",
    "adv608": "Advanced",
    "perf609": "Improve performance",
    "perform610": "Improve performance",
    "prfm611": "Improve performance",
    "hypert612": "Hypertrophy",
    "hypertro613": "Hypertrophy",
    "fat614": "Fat Loss",
    "loss615": "Fat Loss",
    "lean616": "Fat Loss",
    "cut617": "Fat Loss",
    "bulk618": "Hypertrophy",
    "fit619": "General Fitness",
    "fitness620": "General Fitness",
    "ath621": "Athletic Performance",
    "athletic622": "Athletic Performance",
    "balance623": "Balanced Session",
    "balanced624": "Balanced Session",
    "tech625": "Technical Priority",
    "technical626": "Technical Priority",
    "phys627": "Physical Priority",
    "physical628": "Physical Priority",
    "intense629": "Intense Session",
    "hard630": "Intense Session",
    "exper631": "Experienced",
    "experienced632": "Experienced",
    "beg633": "Beginner",
    "beginner634": "Beginner",
    "inter635": "Intermediate",
    "advance636": "Advanced",
    "adv637": "Advanced",
    "perf638": "Improve performance",
    "perform639": "Improve performance",
    "prfm640": "Improve performance",
    "hypert641": "Hypertrophy",
    "hypertro642": "Hypertrophy",
    "fat643": "Fat Loss",
    "loss644": "Fat Loss",
    "lean645": "Fat Loss",
    "cut646": "Fat Loss",
    "bulk647": "Hypertrophy",
    "fit648": "General Fitness",
    "fitness649": "General Fitness",
    "ath650": "Athletic Performance",
    "athletic651": "Athletic Performance",
    "balance652": "Balanced Session",
    "balanced653": "Balanced Session",
    "tech654": "Technical Priority",
    "technical655": "Technical Priority",
    "phys656": "Physical Priority",
    "physical657": "Physical Priority",
    "intense658": "Intense Session",
    "hard659": "Intense Session",
    "exper660": "Experienced",
    "experienced661": "Experienced",
    "beg662": "Beginner",
    "beginner663": "Beginner",
    "inter664": "Intermediate",
    "advance665": "Advanced",
    "adv666": "Advanced",
    "perf667": "Improve performance",
    "perform668": "Improve performance",
    "prfm669": "Improve performance",
    "hypert670": "Hypertrophy",
    "hypertro671": "Hypertrophy",
    "fat672": "Fat Loss",
    "loss673": "Fat Loss",
    "lean674": "Fat Loss",
    "cut675": "Fat Loss",
    "bulk676": "Hypertrophy",
    "fit677": "General Fitness",
    "fitness678": "General Fitness",
    "ath679": "Athletic Performance",
    "athletic680": "Athletic Performance",
    "balance681": "Balanced Session",
    "balanced682": "Balanced Session",
    "tech683": "Technical Priority",
    "technical684": "Technical Priority",
    "phys685": "Physical Priority",
    "physical686": "Physical Priority",
    "intense687": "Intense Session",
    "hard688": "Intense Session",
    "exper689": "Experienced",
    "experienced690": "Experienced",
    "beg691": "Beginner",
    "beginner692": "Beginner",
    "inter693": "Intermediate",
    "advance694": "Advanced",
    "adv695": "Advanced",
    "perf696": "Improve performance",
    "perform697": "Improve performance",
    "prfm698": "Improve performance",
    "hypert699": "Hypertrophy",
    "hypertro700": "Hypertrophy",
    "fat701": "Fat Loss",
    "loss702": "Fat Loss",
    "lean703": "Fat Loss",
    "cut704": "Fat Loss",
    "bulk705": "Hypertrophy",
    "fit706": "General Fitness",
    "fitness707": "General Fitness",
    "ath708": "Athletic Performance",
    "athletic709": "Athletic Performance",
    "balance710": "Balanced Session",
    "balanced711": "Balanced Session",
    "tech712": "Technical Priority",
    "technical713": "Technical Priority",
    "phys714": "Physical Priority",
    "physical715": "Physical Priority",
    "intense716": "Intense Session",
    "hard717": "Intense Session",
    "exper718": "Experienced",
    "experienced719": "Experienced",
    "beg720": "Beginner",
    "beginner721": "Beginner",
    "inter722": "Intermediate",
    "advance723": "Advanced",
    "adv724": "Advanced",
    "perf725": "Improve performance",
    "perform726": "Improve performance",
    "prfm727": "Improve performance",
    "hypert728": "Hypertrophy",
    "hypertro729": "Hypertrophy",
    "fat730": "Fat Loss",
    "loss731": "Fat Loss",
    "lean732": "Fat Loss",
    "cut733": "Fat Loss",
    "bulk734": "Hypertrophy",
    "fit735": "General Fitness",
    "fitness736": "General Fitness",
    "ath737": "Athletic Performance",
    "athletic738": "Athletic Performance",
    "balance739": "Balanced Session",
    "balanced740": "Balanced Session",
    "tech741": "Technical Priority",
    "technical742": "Technical Priority",
    "phys743": "Physical Priority",
    "physical744": "Physical Priority",
    "intense745": "Intense Session",
    "hard746": "Intense Session",
    "exper747": "Experienced",
    "experienced748": "Experienced",
    "beg749": "Beginner",
    "beginner750": "Beginner",
    "inter751": "Intermediate",
    "advance752": "Advanced",
    "adv753": "Advanced",
    "perf754": "Improve performance",
    "perform755": "Improve performance",
    "prfm756": "Improve performance",
    "hypert757": "Hypertrophy",
    "hypertro758": "Hypertrophy",
    "fat759": "Fat Loss",
    "loss760": "Fat Loss",
    "lean761": "Fat Loss",
    "cut762": "Fat Loss",
    "bulk763": "Hypertrophy",
    "fit764": "General Fitness",
    "fitness765": "General Fitness",
    "ath766": "Athletic Performance",
    "athletic767": "Athletic Performance",
    "balance768": "Balanced Session",
    "balanced769": "Balanced Session",
    "tech770": "Technical Priority",
    "technical771": "Technical Priority",
    "phys772": "Physical Priority",
    "physical773": "Physical Priority",
    "intense774": "Intense Session",
    "hard775": "Intense Session",
    "exper776": "Experienced",
    "experienced777": "Experienced",
    "beg778": "Beginner",
    "beginner779": "Beginner",
    "inter780": "Intermediate",
    "advance781": "Advanced",
    "adv782": "Advanced",
    "perf783": "Improve performance",
    "perform784": "Improve performance",
    "prfm785": "Improve performance",
    "hypert786": "Hypertrophy",
    "hypertro787": "Hypertrophy",
    "fat788": "Fat Loss",
    "loss789": "Fat Loss",
    "lean790": "Fat Loss",
    "cut791": "Fat Loss",
    "bulk792": "Hypertrophy",
    "fit793": "General Fitness",
    "fitness794": "General Fitness",
    "ath795": "Athletic Performance",
    "athletic796": "Athletic Performance",
    "balance797": "Balanced Session",
    "balanced798": "Balanced Session",
    "tech799": "Technical Priority",
    "technical800": "Technical Priority",
    "phys801": "Physical Priority",
    "physical802": "Physical Priority",
    "intense803": "Intense Session",
    "hard804": "Intense Session",
    "exper805": "Experienced",
    "experienced806": "Experienced",
    "beg807": "Beginner",
    "beginner808": "Beginner",
    "inter809": "Intermediate",
    "advance810": "Advanced",
    "adv811": "Advanced",
    "perf812": "Improve performance",
    "perform813": "Improve performance",
    "prfm814": "Improve performance",
    "hypert815": "Hypertrophy",
    "hypertro816": "Hypertrophy",
    "fat817": "Fat Loss",
    "loss818": "Fat Loss",
    "lean819": "Fat Loss",
    "cut820": "Fat Loss",
    "bulk821": "Hypertrophy",
    "fit822": "General Fitness",
    "fitness823": "General Fitness",
    "ath824": "Athletic Performance",
    "athletic825": "Athletic Performance",
    "balance826": "Balanced Session",
    "balanced827": "Balanced Session",
    "tech828": "Technical Priority",
    "technical829": "Technical Priority",
    "phys830": "Physical Priority",
    "physical831": "Physical Priority",
    "intense832": "Intense Session",
    "hard833": "Intense Session",
    "exper834": "Experienced",
    "experienced835": "Experienced",
    "beg836": "Beginner",
    "beginner837": "Beginner",
    "inter838": "Intermediate",
    "advance839": "Advanced",
    "adv840": "Advanced",
    "perf841": "Improve performance",
    "perform842": "Improve performance",
    "prfm843": "Improve performance",
    "hypert844": "Hypertrophy",
    "hypertro845": "Hypertrophy",
    "fat846": "Fat Loss",
    "loss847": "Fat Loss",
    "lean848": "Fat Loss",
    "cut849": "Fat Loss",
    "bulk850": "Hypertrophy",
    "fit851": "General Fitness",
    "fitness852": "General Fitness",
    "ath853": "Athletic Performance",
    "athletic854": "Athletic Performance",
    "balance855": "Balanced Session",
    "balanced856": "Balanced Session",
    "tech857": "Technical Priority",
    "technical858": "Technical Priority",
    "phys859": "Physical Priority",
    "physical860": "Physical Priority",
    "intense861": "Intense Session",
    "hard862": "Intense Session",
    "exper863": "Experienced",
    "experienced864": "Experienced",
    "beg865": "Beginner",
    "beginner866": "Beginner",
    "inter867": "Intermediate",
    "advance868": "Advanced",
    "adv869": "Advanced",
    "perf870": "Improve performance",
    "perform871": "Improve performance",
    "prfm872": "Improve performance",
    "hypert873": "Hypertrophy",
    "hypertro874": "Hypertrophy",
    "fat875": "Fat Loss",
    "loss876": "Fat Loss",
    "lean877": "Fat Loss",
    "cut878": "Fat Loss",
    "bulk879": "Hypertrophy",
    "fit880": "General Fitness",
    "fitness881": "General Fitness",
    "ath882": "Athletic Performance",
    "athletic883": "Athletic Performance",
    "balance884": "Balanced Session",
    "balanced885": "Balanced Session",
    "tech886": "Technical Priority",
    "technical887": "Technical Priority",
    "phys888": "Physical Priority",
    "physical889": "Physical Priority",
    "intense890": "Intense Session",
    "hard891": "Intense Session",
    "exper892": "Experienced",
    "experienced893": "Experienced",
    "beg894": "Beginner",
    "beginner895": "Beginner",
    "inter896": "Intermediate",
    "advance897": "Advanced",
    "adv898": "Advanced",
    "perf899": "Improve performance",
    "perform900": "Improve performance",
    "prfm901": "Improve performance",
    "hypert902": "Hypertrophy",
    "hypertro903": "Hypertrophy",
    "fat904": "Fat Loss",
    "loss905": "Fat Loss",
    "lean906": "Fat Loss",
    "cut907": "Fat Loss",
    "bulk908": "Hypertrophy",
    "fit909": "General Fitness",
    "fitness910": "General Fitness",
    "ath911": "Athletic Performance",
    "athletic912": "Athletic Performance",
    "balance913": "Balanced Session",
    "balanced914": "Balanced Session",
    "tech915": "Technical Priority",
    "technical916": "Technical Priority",
    "phys917": "Physical Priority",
    "physical918": "Physical Priority",
    "intense919": "Intense Session",
    "hard920": "Intense Session",
    "exper921": "Experienced",
    "experienced922": "Experienced",
    "beg923": "Beginner",
    "beginner924": "Beginner",
    "inter925": "Intermediate",
    "advance926": "Advanced",
    "adv927": "Advanced",
    "perf928": "Improve performance",
    "perform929": "Improve performance",
    "prfm930": "Improve performance",
    "hypert931": "Hypertrophy",
    "hypertro932": "Hypertrophy",
    "fat933": "Fat Loss",
    "loss934": "Fat Loss",
    "lean935": "Fat Loss",
    "cut936": "Fat Loss",
    "bulk937": "Hypertrophy",
    "fit938": "General Fitness",
    "fitness939": "General Fitness",
    "ath940": "Athletic Performance",
    "athletic941": "Athletic Performance",
    "balance942": "Balanced Session",
    "balanced943": "Balanced Session",
    "tech944": "Technical Priority",
    "technical945": "Technical Priority",
    "phys946": "Physical Priority",
    "physical947": "Physical Priority",
    "intense948": "Intense Session",
    "hard949": "Intense Session",
    "exper950": "Experienced",
    "experienced951": "Experienced",
    "beg952": "Beginner",
    "beginner953": "Beginner",
    "inter954": "Intermediate",
    "advance955": "Advanced",
    "adv956": "Advanced",
    "perf957": "Improve performance",
    "perform958": "Improve performance",
    "prfm959": "Improve performance",
    "hypert960": "Hypertrophy",
    "hypertro961": "Hypertrophy",
    "fat962": "Fat Loss",
    "loss963": "Fat Loss",
    "lean964": "Fat Loss",
    "cut965": "Fat Loss",
    "bulk966": "Hypertrophy",
    "fit967": "General Fitness",
    "fitness968": "General Fitness",
    "ath969": "Athletic Performance",
    "athletic970": "Athletic Performance",
    "balance971": "Balanced Session",
    "balanced972": "Balanced Session",
    "tech973": "Technical Priority",
    "technical974": "Technical Priority",
    "phys975": "Physical Priority",
    "physical976": "Physical Priority",
    "intense977": "Intense Session",
    "hard978": "Intense Session",
    "exper979": "Experienced",
    "experienced980": "Experienced",
    "beg981": "Beginner",
    "beginner982": "Beginner",
    "inter983": "Intermediate",
    "advance984": "Advanced",
    "adv985": "Advanced",
    "perf986": "Improve performance",
    "perform987": "Improve performance",
    "prfm988": "Improve performance",
    "hypert989": "Hypertrophy",
    "hypertro990": "Hypertrophy",
    "fat991": "Fat Loss",
    "loss992": "Fat Loss",
    "lean993": "Fat Loss",
    "cut994": "Fat Loss",
    "bulk995": "Hypertrophy",
    "fit996": "General Fitness",
    "fitness997": "General Fitness",
    "ath998": "Athletic Performance",
    "athletic999": "Athletic Performance",
    "balance1000": "Balanced Session",
    "balanced1001": "Balanced Session",
    "tech1002": "Technical Priority",
    "technical1003": "Technical Priority",
    "phys1004": "Physical Priority",
    "physical1005": "Physical Priority",
    "intense1006": "Intense Session",
    "hard1007": "Intense Session",
    "exper1008": "Experienced",
    "experienced1009": "Experienced",
    "beg1010": "Beginner",
    "beginner1011": "Beginner",
    "inter1012": "Intermediate",
    "advance1013": "Advanced",
    "adv1014": "Advanced",
    "perf1015": "Improve performance",
    "perform1016": "Improve performance",
    "prfm1017": "Improve performance",
    "hypert1018": "Hypertrophy",
    "hypertro1019": "Hypertrophy",
    "fat1020": "Fat Loss",
    "loss1021": "Fat Loss",
    "lean1022": "Fat Loss",
    "cut1023": "Fat Loss",
    "bulk1024": "Hypertrophy",
    "fit1025": "General Fitness",
    "fitness1026": "General Fitness",
    "ath1027": "Athletic Performance",
    "athletic1028": "Athletic Performance",
    "balance1029": "Balanced Session",
    "balanced1030": "Balanced Session",
    "tech1031": "Technical Priority",
    "technical1032": "Technical Priority",
    "phys1033": "Physical Priority",
    "physical1034": "Physical Priority",
    "intense1035": "Intense Session",
    "hard1036": "Intense Session",
    "exper1037": "Experienced",
    "experienced1038": "Experienced",
    "beg1039": "Beginner",
    "beginner1040": "Beginner",
    "inter1041": "Intermediate",
    "advance1042": "Advanced",
    "adv1043": "Advanced",
    "perf1044": "Improve performance",
    "perform1045": "Improve performance",
    "prfm1046": "Improve performance",
    "hypert1047": "Hypertrophy",
    "hypertro1048": "Hypertrophy",
    "fat1049": "Fat Loss",
    "loss1050": "Fat Loss",
    "lean1051": "Fat Loss",
    "cut1052": "Fat Loss",
    "bulk1053": "Hypertrophy",
    "fit1054": "General Fitness",
    "fitness1055": "General Fitness",
    "ath1056": "Athletic Performance",
    "athletic1057": "Athletic Performance",
    "balance1058": "Balanced Session",
    "balanced1059": "Balanced Session",
    "tech1060": "Technical Priority",
    "technical1061": "Technical Priority",
    "phys1062": "Physical Priority",
    "physical1063": "Physical Priority",
    "intense1064": "Intense Session",
    "hard1065": "Intense Session",
    "exper1066": "Experienced",
    "experienced1067": "Experienced",
    "beg1068": "Beginner",
    "beginner1069": "Beginner",
    "inter1070": "Intermediate",
    "advance1071": "Advanced",
    "adv1072": "Advanced",
    "perf1073": "Improve performance",
    "perform1074": "Improve performance",
    "prfm1075": "Improve performance",
    "hypert1076": "Hypertrophy",
    "hypertro1077": "Hypertrophy",
    "fat1078": "Fat Loss",
    "loss1079": "Fat Loss",
    "lean1080": "Fat Loss",
    "cut1081": "Fat Loss",
    "bulk1082": "Hypertrophy",
    "fit1083": "General Fitness",
    "fitness1084": "General Fitness",
    "ath1085": "Athletic Performance",
    "athletic1086": "Athletic Performance",
    "balance1087": "Balanced Session",
    "balanced1088": "Balanced Session",
    "tech1089": "Technical Priority",
    "technical1090": "Technical Priority",
    "phys1091": "Physical Priority",
    "physical1092": "Physical Priority",
    "intense1093": "Intense Session",
    "hard1094": "Intense Session",
    "exper1095": "Experienced",
    "experienced1096": "Experienced",
    "beg1097": "Beginner",
    "beginner1098": "Beginner",
    "inter1099": "Intermediate",
    "advance1100": "Advanced",
    "adv1101": "Advanced",
    "perf1102": "Improve performance",
    "perform1103": "Improve performance",
    "prfm1104": "Improve performance",
    "hypert1105": "Hypertrophy",
    "hypertro1106": "Hypertrophy",
    "fat1107": "Fat Loss",
    "loss1108": "Fat Loss",
    "lean1109": "Fat Loss",
    "cut1110": "Fat Loss",
    "bulk1111": "Hypertrophy",
    "fit1112": "General Fitness",
    "fitness1113": "General Fitness",
    "ath1114": "Athletic Performance",
    "athletic1115": "Athletic Performance",
    "balance1116": "Balanced Session",
    "balanced1117": "Balanced Session",
    "tech1118": "Technical Priority",
    "technical1119": "Technical Priority",
    "phys1120": "Physical Priority",
    "physical1121": "Physical Priority",
    "intense1122": "Intense Session",
    "hard1123": "Intense Session",
    "exper1124": "Experienced",
    "experienced1125": "Experienced",
    "beg1126": "Beginner",
    "beginner1127": "Beginner",
    "inter1128": "Intermediate",
    "advance1129": "Advanced",
    "adv1130": "Advanced",
    "perf1131": "Improve performance",
    "perform1132": "Improve performance",
    "prfm1133": "Improve performance",
    "hypert1134": "Hypertrophy",
    "hypertro1135": "Hypertrophy",
    "fat1136": "Fat Loss",
    "loss1137": "Fat Loss",
    "lean1138": "Fat Loss",
    "cut1139": "Fat Loss",
    "bulk1140": "Hypertrophy",
    "fit1141": "General Fitness",
    "fitness1142": "General Fitness",
    "ath1143": "Athletic Performance",
    "athletic1144": "Athletic Performance",
    "balance1145": "Balanced Session",
    "balanced1146": "Balanced Session",
    "tech1147": "Technical Priority",
    "technical1148": "Technical Priority",
    "phys1149": "Physical Priority",
    "physical1150": "Physical Priority",
    "intense1151": "Intense Session",
    "hard1152": "Intense Session",
    "exper1153": "Experienced",
    "experienced1154": "Experienced",
    "beg1155": "Beginner",
    "beginner1156": "Beginner",
    "inter1157": "Intermediate",
    "advance1158": "Advanced",
    "adv1159": "Advanced",
    "perf1160": "Improve performance",
    "perform1161": "Improve performance",
    "prfm1162": "Improve performance",
    "hypert1163": "Hypertrophy",
    "hypertro1164": "Hypertrophy",
    "fat1165": "Fat Loss",
    "loss1166": "Fat Loss",
    "lean1167": "Fat Loss",
    "cut1168": "Fat Loss",
    "bulk1169": "Hypertrophy",
    "fit1170": "General Fitness",
    "fitness1171": "General Fitness",
    "ath1172": "Athletic Performance",
    "athletic1173": "Athletic Performance",
    "balance1174": "Balanced Session",
    "balanced1175": "Balanced Session",
    "tech1176": "Technical Priority",
    "technical1177": "Technical Priority",
    "phys1178": "Physical Priority",
    "physical1179": "Physical Priority",
    "intense1180": "Intense Session",
    "hard1181": "Intense Session",
    "exper1182": "Experienced",
    "experienced1183": "Experienced",
    "beg1184": "Beginner",
    "beginner1185": "Beginner",
    "inter1186": "Intermediate",
    "advance1187": "Advanced",
    "adv1188": "Advanced",
    "perf1189": "Improve performance",
    "perform1190": "Improve performance",
    "prfm1191": "Improve performance",
    "hypert1192": "Hypertrophy",
    "hypertro1193": "Hypertrophy",
    "fat1194": "Fat Loss",
    "loss1195": "Fat Loss",
    "lean1196": "Fat Loss",
    "cut1197": "Fat Loss",
    "bulk1198": "Hypertrophy",
    "fit1199": "General Fitness",
    "fitness1200": "General Fitness",
    "ath1201": "Athletic Performance",
    "athletic1202": "Athletic Performance",
    "balance1203": "Balanced Session",
    "balanced1204": "Balanced Session",
    "tech1205": "Technical Priority",
    "technical1206": "Technical Priority",
    "phys1207": "Physical Priority",
    "physical1208": "Physical Priority",
    "intense1209": "Intense Session",
    "hard1210": "Intense Session",
    "exper1211": "Experienced",
    "experienced1212": "Experienced",
    "beg1213": "Beginner",
    "beginner1214": "Beginner",
    "inter1215": "Intermediate",
    "advance1216": "Advanced",
    "adv1217": "Advanced",
    "perf1218": "Improve performance",
    "perform1219": "Improve performance",
    "prfm1220": "Improve performance",
    "hypert1221": "Hypertrophy",
    "hypertro1222": "Hypertrophy",
    "fat1223": "Fat Loss",
    "loss1224": "Fat Loss",
    "lean1225": "Fat Loss",
    "cut1226": "Fat Loss",
    "bulk1227": "Hypertrophy",
    "fit1228": "General Fitness",
    "fitness1229": "General Fitness",
    "ath1230": "Athletic Performance",
    "athletic1231": "Athletic Performance",
    "balance1232": "Balanced Session",
    "balanced1233": "Balanced Session",
    "tech1234": "Technical Priority",
    "technical1235": "Technical Priority",
    "phys1236": "Physical Priority",
    "physical1237": "Physical Priority",
    "intense1238": "Intense Session",
    "hard1239": "Intense Session",
    "exper1240": "Experienced",
    "experienced1241": "Experienced",
    "beg1242": "Beginner",
    "beginner1243": "Beginner",
    "inter1244": "Intermediate",
    "advance1245": "Advanced",
    "adv1246": "Advanced",
    "perf1247": "Improve performance",
    "perform1248": "Improve performance",
    "prfm1249": "Improve performance",
    "hypert1250": "Hypertrophy",
    "hypertro1251": "Hypertrophy",
    "fat1252": "Fat Loss",
    "loss1253": "Fat Loss",
    "lean1254": "Fat Loss",
    "cut1255": "Fat Loss",
    "bulk1256": "Hypertrophy",
    "fit1257": "General Fitness",
    "fitness1258": "General Fitness",
    "ath1259": "Athletic Performance",
    "athletic1260": "Athletic Performance",
    "balance1261": "Balanced Session",
    "balanced1262": "Balanced Session",
    "tech1263": "Technical Priority",
    "technical1264": "Technical Priority",
    "phys1265": "Physical Priority",
    "physical1266": "Physical Priority",
    "intense1267": "Intense Session",
    "hard1268": "Intense Session",
    "exper1269": "Experienced",
    "experienced1270": "Experienced",
    "beg1271": "Beginner",
    "beginner1272": "Beginner",
    "inter1273": "Intermediate",
    "advance1274": "Advanced",
    "adv1275": "Advanced",
    "perf1276": "Improve performance",
    "perform1277": "Improve performance",
    "prfm1278": "Improve performance",
    "hypert1279": "Hypertrophy",
    "hypertro1280": "Hypertrophy",
    "fat1281": "Fat Loss",
    "loss1282": "Fat Loss",
    "lean1283": "Fat Loss",
    "cut1284": "Fat Loss",
    "bulk1285": "Hypertrophy",
    "fit1286": "General Fitness",
    "fitness1287": "General Fitness",
    "ath1288": "Athletic Performance",
    "athletic1289": "Athletic Performance",
    "balance1290": "Balanced Session",
    "balanced1291": "Balanced Session",
    "tech1292": "Technical Priority",
    "technical1293": "Technical Priority",
    "phys1294": "Physical Priority",
    "physical1295": "Physical Priority",
    "intense1296": "Intense Session",
    "hard1297": "Intense Session",
    "exper1298": "Experienced",
    "experienced1299": "Experienced",
    "beg1300": "Beginner",
    "beginner1301": "Beginner",
    "inter1302": "Intermediate",
    "advance1303": "Advanced",
    "adv1304": "Advanced",
    "perf1305": "Improve performance",
    "perform1306": "Improve performance",
    "prfm1307": "Improve performance",
    "hypert1308": "Hypertrophy",
    "hypertro1309": "Hypertrophy",
    "fat1310": "Fat Loss",
    "loss1311": "Fat Loss",
    "lean1312": "Fat Loss",
    "cut1313": "Fat Loss",
    "bulk1314": "Hypertrophy",
    "fit1315": "General Fitness",
    "fitness1316": "General Fitness",
    "ath1317": "Athletic Performance",
    "athletic1318": "Athletic Performance",
    "balance1319": "Balanced Session",
    "balanced1320": "Balanced Session",
    "tech1321": "Technical Priority",
    "technical1322": "Technical Priority",
    "phys1323": "Physical Priority",
    "physical1324": "Physical Priority",
    "intense1325": "Intense Session",
    "hard1326": "Intense Session",
    "exper1327": "Experienced",
    "experienced1328": "Experienced",
    "beg1329": "Beginner",
    "beginner1330": "Beginner",
    "inter1331": "Intermediate",
    "advance1332": "Advanced",
    "adv1333": "Advanced",
    "perf1334": "Improve performance",
    "perform1335": "Improve performance",
    "prfm1336": "Improve performance",
    "hypert1337": "Hypertrophy",
    "hypertro1338": "Hypertrophy",
    "fat1339": "Fat Loss",
    "loss1340": "Fat Loss",
    "lean1341": "Fat Loss",
    "cut1342": "Fat Loss",
    "bulk1343": "Hypertrophy",
    "fit1344": "General Fitness",
    "fitness1345": "General Fitness",
    "ath1346": "Athletic Performance",
    "athletic1347": "Athletic Performance",
    "balance1348": "Balanced Session",
    "balanced1349": "Balanced Session",
    "tech1350": "Technical Priority",
    "technical1351": "Technical Priority",
    "phys1352": "Physical Priority",
    "physical1353": "Physical Priority",
    "intense1354": "Intense Session",
    "hard1355": "Intense Session",
    "exper1356": "Experienced",
    "experienced1357": "Experienced",
    "beg1358": "Beginner",
    "beginner1359": "Beginner",
    "inter1360": "Intermediate",
    "advance1361": "Advanced",
    "adv1362": "Advanced",
    "perf1363": "Improve performance",
    "perform1364": "Improve performance",
    "prfm1365": "Improve performance",
    "hypert1366": "Hypertrophy",
    "hypertro1367": "Hypertrophy",
    "fat1368": "Fat Loss",
    "loss1369": "Fat Loss",
    "lean1370": "Fat Loss",
    "cut1371": "Fat Loss",
    "bulk1372": "Hypertrophy",
    "fit1373": "General Fitness",
    "fitness1374": "General Fitness",
    "ath1375": "Athletic Performance",
    "athletic1376": "Athletic Performance",
    "balance1377": "Balanced Session",
    "balanced1378": "Balanced Session",
    "tech1379": "Technical Priority",
    "technical1380": "Technical Priority",
    "phys1381": "Physical Priority",
    "physical1382": "Physical Priority",
    "intense1383": "Intense Session",
    "hard1384": "Intense Session",
    "exper1385": "Experienced",
    "experienced1386": "Experienced",
    "beg1387": "Beginner",
    "beginner1388": "Beginner",
    "inter1389": "Intermediate",
    "advance1390": "Advanced",
    "adv1391": "Advanced",
    "perf1392": "Improve performance",
    "perform1393": "Improve performance",
    "prfm1394": "Improve performance",
    "hypert1395": "Hypertrophy",
    "hypertro1396": "Hypertrophy",
    "fat1397": "Fat Loss",
    "loss1398": "Fat Loss",
    "lean1399": "Fat Loss",
    "cut1400": "Fat Loss",
    "bulk1401": "Hypertrophy",
    "fit1402": "General Fitness",
    "fitness1403": "General Fitness",
    "ath1404": "Athletic Performance",
    "athletic1405": "Athletic Performance",
    "balance1406": "Balanced Session",
    "balanced1407": "Balanced Session",
    "tech1408": "Technical Priority",
    "technical1409": "Technical Priority",
    "phys1410": "Physical Priority",
    "physical1411": "Physical Priority",
    "intense1412": "Intense Session",
    "hard1413": "Intense Session",
    "exper1414": "Experienced",
    "experienced1415": "Experienced",
    "beg1416": "Beginner",
    "beginner1417": "Beginner",
    "inter1418": "Intermediate",
    "advance1419": "Advanced",
    "adv1420": "Advanced",
    "perf1421": "Improve performance",
    "perform1422": "Improve performance",
    "prfm1423": "Improve performance",
    "hypert1424": "Hypertrophy",
    "hypertro1425": "Hypertrophy",
    "fat1426": "Fat Loss",
    "loss1427": "Fat Loss",
    "lean1428": "Fat Loss",
    "cut1429": "Fat Loss",
    "bulk1430": "Hypertrophy",
    "fit1431": "General Fitness",
    "fitness1432": "General Fitness",
    "ath1433": "Athletic Performance",
    "athletic1434": "Athletic Performance",
    "balance1435": "Balanced Session",
    "balanced1436": "Balanced Session",
    "tech1437": "Technical Priority",
    "technical1438": "Technical Priority",
    "phys1439": "Physical Priority",
    "physical1440": "Physical Priority",
    "intense1441": "Intense Session",
    "hard1442": "Intense Session",
    "exper1443": "Experienced",
    "experienced1444": "Experienced",
    "beg1445": "Beginner",
    "beginner1446": "Beginner",
    "inter1447": "Intermediate",
    "advance1448": "Advanced",
    "adv1449": "Advanced",
    "perf1450": "Improve performance",
    "perform1451": "Improve performance",
    "prfm1452": "Improve performance",
    "hypert1453": "Hypertrophy",
    "hypertro1454": "Hypertrophy",
    "fat1455": "Fat Loss",
    "loss1456": "Fat Loss",
    "lean1457": "Fat Loss",
    "cut1458": "Fat Loss",
    "bulk1459": "Hypertrophy",
    "fit1460": "General Fitness",
    "fitness1461": "General Fitness",
    "ath1462": "Athletic Performance",
    "athletic1463": "Athletic Performance",
    "balance1464": "Balanced Session",
    "balanced1465": "Balanced Session",
    "tech1466": "Technical Priority",
    "technical1467": "Technical Priority",
    "phys1468": "Physical Priority",
    "physical1469": "Physical Priority",
    "intense1470": "Intense Session",
    "hard1471": "Intense Session",
    "exper1472": "Experienced",
    "experienced1473": "Experienced",
    "beg1474": "Beginner",
    "beginner1475": "Beginner",
    "inter1476": "Intermediate",
    "advance1477": "Advanced",
    "adv1478": "Advanced",
    "perf1479": "Improve performance",
    "perform1480": "Improve performance",
    "prfm1481": "Improve performance",
    "hypert1482": "Hypertrophy",
    "hypertro1483": "Hypertrophy",
    "fat1484": "Fat Loss",
    "loss1485": "Fat Loss",
    "lean1486": "Fat Loss",
    "cut1487": "Fat Loss",
    "bulk1488": "Hypertrophy",
    "fit1489": "General Fitness",
    "fitness1490": "General Fitness",
    "ath1491": "Athletic Performance",
    "athletic1492": "Athletic Performance",
    "balance1493": "Balanced Session",
    "balanced1494": "Balanced Session",
    "tech1495": "Technical Priority",
    "technical1496": "Technical Priority",
    "phys1497": "Physical Priority",
    "physical1498": "Physical Priority",
    "intense1499": "Intense Session",
    "hard1500": "Intense Session",
    "exper1501": "Experienced",
    "experienced1502": "Experienced",
    "beg1503": "Beginner",
    "beginner1504": "Beginner",
    "inter1505": "Intermediate",
    "advance1506": "Advanced",
    "adv1507": "Advanced",
    "perf1508": "Improve performance",
    "perform1509": "Improve performance",
    "prfm1510": "Improve performance",
    "hypert1511": "Hypertrophy",
    "hypertro1512": "Hypertrophy",
    "fat1513": "Fat Loss",
    "loss1514": "Fat Loss",
    "lean1515": "Fat Loss",
    "cut1516": "Fat Loss",
    "bulk1517": "Hypertrophy",
    "fit1518": "General Fitness",
    "fitness1519": "General Fitness",
    "ath1520": "Athletic Performance",
    "athletic1521": "Athletic Performance",
    "balance1522": "Balanced Session",
    "balanced1523": "Balanced Session",
    "tech1524": "Technical Priority",
    "technical1525": "Technical Priority",
    "phys1526": "Physical Priority",
    "physical1527": "Physical Priority",
    "intense1528": "Intense Session",
    "hard1529": "Intense Session",
    "exper1530": "Experienced",
    "experienced1531": "Experienced",
    "beg1532": "Beginner",
    "beginner1533": "Beginner",
    "inter1534": "Intermediate",
    "advance1535": "Advanced",
    "adv1536": "Advanced",
    "perf1537": "Improve performance",
    "perform1538": "Improve performance",
    "prfm1539": "Improve performance",
    "hypert1540": "Hypertrophy",
    "hypertro1541": "Hypertrophy",
    "fat1542": "Fat Loss",
    "loss1543": "Fat Loss",
    "lean1544": "Fat Loss",
    "cut1545": "Fat Loss",
    "bulk1546": "Hypertrophy",
    "fit1547": "General Fitness",
    "fitness1548": "General Fitness",
    "ath1549": "Athletic Performance",
    "athletic1550": "Athletic Performance",
    "balance1551": "Balanced Session",
    "balanced1552": "Balanced Session",
    "tech1553": "Technical Priority",
    "technical1554": "Technical Priority",
    "phys1555": "Physical Priority",
    "physical1556": "Physical Priority",
    "intense1557": "Intense Session",
    "hard1558": "Intense Session",
    "exper1559": "Experienced",
    "experienced1560": "Experienced",
    "beg1561": "Beginner",
    "beginner1562": "Beginner",
    "inter1563": "Intermediate",
    "advance1564": "Advanced",
    "adv1565": "Advanced",
    "perf1566": "Improve performance",
    "perform1567": "Improve performance",
    "prfm1568": "Improve performance",
    "hypert1569": "Hypertrophy",
    "hypertro1570": "Hypertrophy",
    "fat1571": "Fat Loss",
    "loss1572": "Fat Loss",
    "lean1573": "Fat Loss",
    "cut1574": "Fat Loss",
    "bulk1575": "Hypertrophy",
    "fit1576": "General Fitness",
    "fitness1577": "General Fitness",
    "ath1578": "Athletic Performance",
    "athletic1579": "Athletic Performance",
    "balance1580": "Balanced Session",
    "balanced1581": "Balanced Session",
    "tech1582": "Technical Priority",
    "technical1583": "Technical Priority",
    "phys1584": "Physical Priority",
    "physical1585": "Physical Priority",
    "intense1586": "Intense Session",
    "hard1587": "Intense Session",
    "exper1588": "Experienced",
    "experienced1589": "Experienced",
    "beg1590": "Beginner",
    "beginner1591": "Beginner",
    "inter1592": "Intermediate",
    "advance1593": "Advanced",
    "adv1594": "Advanced",
    "perf1595": "Improve performance",
    "perform1596": "Improve performance",
    "prfm1597": "Improve performance",
    "hypert1598": "Hypertrophy",
    "hypertro1599": "Hypertrophy",
    "fat1600": "Fat Loss",
    "loss1601": "Fat Loss",
    "lean1602": "Fat Loss",
    "cut1603": "Fat Loss",
    "bulk1604": "Hypertrophy",
    "fit1605": "General Fitness",
    "fitness1606": "General Fitness",
    "ath1607": "Athletic Performance",
    "athletic1608": "Athletic Performance",
    "balance1609": "Balanced Session",
    "balanced1610": "Balanced Session",
    "tech1611": "Technical Priority",
    "technical1612": "Technical Priority",
    "phys1613": "Physical Priority",
    "physical1614": "Physical Priority",
    "intense1615": "Intense Session",
    "hard1616": "Intense Session",
    "exper1617": "Experienced",
    "experienced1618": "Experienced",
    "beg1619": "Beginner",
    "beginner1620": "Beginner",
    "inter1621": "Intermediate",
    "advance1622": "Advanced",
    "adv1623": "Advanced",
    "perf1624": "Improve performance",
    "perform1625": "Improve performance",
    "prfm1626": "Improve performance",
    "hypert1627": "Hypertrophy",
    "hypertro1628": "Hypertrophy",
    "fat1629": "Fat Loss",
    "loss1630": "Fat Loss",
    "lean1631": "Fat Loss",
    "cut1632": "Fat Loss",
    "bulk1633": "Hypertrophy",
    "fit1634": "General Fitness",
    "fitness1635": "General Fitness",
    "ath1636": "Athletic Performance",
    "athletic1637": "Athletic Performance",
    "balance1638": "Balanced Session",
    "balanced1639": "Balanced Session",
    "tech1640": "Technical Priority",
    "technical1641": "Technical Priority",
    "phys1642": "Physical Priority",
    "physical1643": "Physical Priority",
    "intense1644": "Intense Session",
    "hard1645": "Intense Session",
    "exper1646": "Experienced",
    "experienced1647": "Experienced",
    "beg1648": "Beginner",
    "beginner1649": "Beginner",
    "inter1650": "Intermediate",
    "advance1651": "Advanced",
    "adv1652": "Advanced",
    "perf1653": "Improve performance",
    "perform1654": "Improve performance",
    "prfm1655": "Improve performance",
    "hypert1656": "Hypertrophy",
    "hypertro1657": "Hypertrophy",
    "fat1658": "Fat Loss",
    "loss1659": "Fat Loss",
    "lean1660": "Fat Loss",
    "cut1661": "Fat Loss",
    "bulk1662": "Hypertrophy",
    "fit1663": "General Fitness",
    "fitness1664": "General Fitness",
    "ath1665": "Athletic Performance",
    "athletic1666": "Athletic Performance",
    "balance1667": "Balanced Session",
    "balanced1668": "Balanced Session",
    "tech1669": "Technical Priority",
    "technical1670": "Technical Priority",
    "phys1671": "Physical Priority",
    "physical1672": "Physical Priority",
    "intense1673": "Intense Session",
    "hard1674": "Intense Session",
    "exper1675": "Experienced",
    "experienced1676": "Experienced",
    "beg1677": "Beginner",
    "beginner1678": "Beginner",
    "inter1679": "Intermediate",
    "advance1680": "Advanced",
    "adv1681": "Advanced",
    "perf1682": "Improve performance",
    "perform1683": "Improve performance",
    "prfm1684": "Improve performance",
    "hypert1685": "Hypertrophy",
    "hypertro1686": "Hypertrophy",
    "fat1687": "Fat Loss",
    "loss1688": "Fat Loss",
    "lean1689": "Fat Loss",
    "cut1690": "Fat Loss",
    "bulk1691": "Hypertrophy",
    "fit1692": "General Fitness",
    "fitness1693": "General Fitness",
    "ath1694": "Athletic Performance",
    "athletic1695": "Athletic Performance",
    "balance1696": "Balanced Session",
    "balanced1697": "Balanced Session",
    "tech1698": "Technical Priority",
    "technical1699": "Technical Priority",
    "phys1700": "Physical Priority",
    "physical1701": "Physical Priority",
    "intense1702": "Intense Session",
    "hard1703": "Intense Session",
    "exper1704": "Experienced",
    "experienced1705": "Experienced",
    "beg1706": "Beginner",
    "beginner1707": "Beginner",
    "inter1708": "Intermediate",
    "advance1709": "Advanced",
    "adv1710": "Advanced",
    "perf1711": "Improve performance",
    "perform1712": "Improve performance",
    "prfm1713": "Improve performance",
    "hypert1714": "Hypertrophy",
    "hypertro1715": "Hypertrophy",
    "fat1716": "Fat Loss",
    "loss1717": "Fat Loss",
    "lean1718": "Fat Loss",
    "cut1719": "Fat Loss",
    "bulk1720": "Hypertrophy",
    "fit1721": "General Fitness",
    "fitness1722": "General Fitness",
    "ath1723": "Athletic Performance",
    "athletic1724": "Athletic Performance",
    "balance1725": "Balanced Session",
    "balanced1726": "Balanced Session",
    "tech1727": "Technical Priority",
    "technical1728": "Technical Priority",
    "phys1729": "Physical Priority",
    "physical1730": "Physical Priority",
    "intense1731": "Intense Session",
    "hard1732": "Intense Session",
    "exper1733": "Experienced",
    "experienced1734": "Experienced",
    "beg1735": "Beginner",
    "beginner1736": "Beginner",
    "inter1737": "Intermediate",
    "advance1738": "Advanced",
    "adv1739": "Advanced",
    "perf1740": "Improve performance",
    "perform1741": "Improve performance",
    "prfm1742": "Improve performance",
    "hypert1743": "Hypertrophy",
    "hypertro1744": "Hypertrophy",
    "fat1745": "Fat Loss",
    "loss1746": "Fat Loss",
    "lean1747": "Fat Loss",
    "cut1748": "Fat Loss",
    "bulk1749": "Hypertrophy",
    "fit1750": "General Fitness",
    "fitness1751": "General Fitness",
    "ath1752": "Athletic Performance",
    "athletic1753": "Athletic Performance",
    "balance1754": "Balanced Session",
    "balanced1755": "Balanced Session",
    "tech1756": "Technical Priority",
    "technical1757": "Technical Priority",
    "phys1758": "Physical Priority",
    "physical1759": "Physical Priority",
    "intense1760": "Intense Session",
    "hard1761": "Intense Session",
    "exper1762": "Experienced",
    "experienced1763": "Experienced",
    "beg1764": "Beginner",
    "beginner1765": "Beginner",
    "inter1766": "Intermediate",
    "advance1767": "Advanced",
    "adv1768": "Advanced",
    "perf1769": "Improve performance",
    "perform1770": "Improve performance",
    "prfm1771": "Improve performance",
    "hypert1772": "Hypertrophy",
    "hypertro1773": "Hypertrophy",
    "fat1774": "Fat Loss",
    "loss1775": "Fat Loss",
    "lean1776": "Fat Loss",
    "cut1777": "Fat Loss",
    "bulk1778": "Hypertrophy",
    "fit1779": "General Fitness",
    "fitness1780": "General Fitness",
    "ath1781": "Athletic Performance",
    "athletic1782": "Athletic Performance",
    "balance1783": "Balanced Session",
    "balanced1784": "Balanced Session",
    "tech1785": "Technical Priority",
    "technical1786": "Technical Priority",
    "phys1787": "Physical Priority",
    "physical1788": "Physical Priority",
    "intense1789": "Intense Session",
    "hard1790": "Intense Session",
    "exper1791": "Experienced",
    "experienced1792": "Experienced",
    "beg1793": "Beginner",
    "beginner1794": "Beginner",
    "inter1795": "Intermediate",
    "advance1796": "Advanced",
    "adv1797": "Advanced",
    "perf1798": "Improve performance",
    "perform1799": "Improve performance",
    "prfm1800": "Improve performance",
    "hypert1801": "Hypertrophy",
    "hypertro1802": "Hypertrophy",
    "fat1803": "Fat Loss",
    "loss1804": "Fat Loss",
    "lean1805": "Fat Loss",
    "cut1806": "Fat Loss",
    "bulk1807": "Hypertrophy",
    "fit1808": "General Fitness",
    "fitness1809": "General Fitness",
    "ath1810": "Athletic Performance",
    "athletic1811": "Athletic Performance",
    "balance1812": "Balanced Session",
    "balanced1813": "Balanced Session",
    "tech1814": "Technical Priority",
    "technical1815": "Technical Priority",
    "phys1816": "Physical Priority",
    "physical1817": "Physical Priority",
    "intense1818": "Intense Session",
    "hard1819": "Intense Session",
    "exper1820": "Experienced",
    "experienced1821": "Experienced",
    "beg1822": "Beginner",
    "beginner1823": "Beginner",
    "inter1824": "Intermediate",
    "advance1825": "Advanced",
    "adv1826": "Advanced",
    "perf1827": "Improve performance",
    "perform1828": "Improve performance",
    "prfm1829": "Improve performance",
    "hypert1830": "Hypertrophy",
    "hypertro1831": "Hypertrophy",
    "fat1832": "Fat Loss",
    "loss1833": "Fat Loss",
    "lean1834": "Fat Loss",
    "cut1835": "Fat Loss",
    "bulk1836": "Hypertrophy",
    "fit1837": "General Fitness",
    "fitness1838": "General Fitness",
    "ath1839": "Athletic Performance",
    "athletic1840": "Athletic Performance",
    "balance1841": "Balanced Session",
    "balanced1842": "Balanced Session",
    "tech1843": "Technical Priority",
    "technical1844": "Technical Priority",
    "phys1845": "Physical Priority",
    "physical1846": "Physical Priority",
    "intense1847": "Intense Session",
    "hard1848": "Intense Session",
    "exper1849": "Experienced",
    "experienced1850": "Experienced",
    "beg1851": "Beginner",
    "beginner1852": "Beginner",
    "inter1853": "Intermediate",
    "advance1854": "Advanced",
    "adv1855": "Advanced",
    "perf1856": "Improve performance",
    "perform1857": "Improve performance",
    "prfm1858": "Improve performance",
    "hypert1859": "Hypertrophy",
    "hypertro1860": "Hypertrophy",
    "fat1861": "Fat Loss",
    "loss1862": "Fat Loss",
    "lean1863": "Fat Loss",
    "cut1864": "Fat Loss",
    "bulk1865": "Hypertrophy",
    "fit1866": "General Fitness",
    "fitness1867": "General Fitness",
    "ath1868": "Athletic Performance",
    "athletic1869": "Athletic Performance",
    "balance1870": "Balanced Session",
    "balanced1871": "Balanced Session",
    "tech1872": "Technical Priority",
    "technical1873": "Technical Priority",
    "phys1874": "Physical Priority",
    "physical1875": "Physical Priority",
    "intense1876": "Intense Session",
    "hard1877": "Intense Session",
    "exper1878": "Experienced",
    "experienced1879": "Experienced",
    "beg1880": "Beginner",
    "beginner1881": "Beginner",
    "inter1882": "Intermediate",
    "advance1883": "Advanced",
    "adv1884": "Advanced",
    "perf1885": "Improve performance",
    "perform1886": "Improve performance",
    "prfm1887": "Improve performance",
    "hypert1888": "Hypertrophy",
    "hypertro1889": "Hypertrophy",
    "fat1890": "Fat Loss",
    "loss1891": "Fat Loss",
    "lean1892": "Fat Loss",
    "cut1893": "Fat Loss",
    "bulk1894": "Hypertrophy",
    "fit1895": "General Fitness",
    "fitness1896": "General Fitness",
    "ath1897": "Athletic Performance",
    "athletic1898": "Athletic Performance",
    "balance1899": "Balanced Session",
    "balanced1900": "Balanced Session",
    "tech1901": "Technical Priority",
    "technical1902": "Technical Priority",
    "phys1903": "Physical Priority",
    "physical1904": "Physical Priority",
    "intense1905": "Intense Session",
    "hard1906": "Intense Session",
    "exper1907": "Experienced",
    "experienced1908": "Experienced",
    "beg1909": "Beginner",
    "beginner1910": "Beginner",
    "inter1911": "Intermediate",
    "advance1912": "Advanced",
    "adv1913": "Advanced",
    "perf1914": "Improve performance",
    "perform1915": "Improve performance",
    "prfm1916": "Improve performance",
    "hypert1917": "Hypertrophy",
    "hypertro1918": "Hypertrophy",
    "fat1919": "Fat Loss",
    "loss1920": "Fat Loss",
    "lean1921": "Fat Loss",
    "cut1922": "Fat Loss",
    "bulk1923": "Hypertrophy",
    "fit1924": "General Fitness",
    "fitness1925": "General Fitness",
    "ath1926": "Athletic Performance",
    "athletic1927": "Athletic Performance",
    "balance1928": "Balanced Session",
    "balanced1929": "Balanced Session",
    "tech1930": "Technical Priority",
    "technical1931": "Technical Priority",
    "phys1932": "Physical Priority",
    "physical1933": "Physical Priority",
    "intense1934": "Intense Session",
    "hard1935": "Intense Session",
    "exper1936": "Experienced",
    "experienced1937": "Experienced",
    "beg1938": "Beginner",
    "beginner1939": "Beginner",
    "inter1940": "Intermediate",
    "advance1941": "Advanced",
    "adv1942": "Advanced",
    "perf1943": "Improve performance",
    "perform1944": "Improve performance",
    "prfm1945": "Improve performance",
    "hypert1946": "Hypertrophy",
    "hypertro1947": "Hypertrophy",
    "fat1948": "Fat Loss",
    "loss1949": "Fat Loss",
    "lean1950": "Fat Loss",
    "cut1951": "Fat Loss",
    "bulk1952": "Hypertrophy",
    "fit1953": "General Fitness",
    "fitness1954": "General Fitness",
    "ath1955": "Athletic Performance",
    "athletic1956": "Athletic Performance",
    "balance1957": "Balanced Session",
    "balanced1958": "Balanced Session",
    "tech1959": "Technical Priority",
    "technical1960": "Technical Priority",
    "phys1961": "Physical Priority",
    "physical1962": "Physical Priority",
    "intense1963": "Intense Session",
    "hard1964": "Intense Session",
    "exper1965": "Experienced",
    "experienced1966": "Experienced",
    "beg1967": "Beginner",
    "beginner1968": "Beginner",
    "inter1969": "Intermediate",
    "advance1970": "Advanced",
    "adv1971": "Advanced",
    "perf1972": "Improve performance",
    "perform1973": "Improve performance",
    "prfm1974": "Improve performance",
    "hypert1975": "Hypertrophy",
    "hypertro1976": "Hypertrophy",
    "fat1977": "Fat Loss",
    "loss1978": "Fat Loss",
    "lean1979": "Fat Loss",
    "cut1980": "Fat Loss",
    "bulk1981": "Hypertrophy",
    "fit1982": "General Fitness",
    "fitness1983": "General Fitness",
    "ath1984": "Athletic Performance",
    "athletic1985": "Athletic Performance",
    "balance1986": "Balanced Session",
    "balanced1987": "Balanced Session",
    "tech1988": "Technical Priority",
    "technical1989": "Technical Priority",
    "phys1990": "Physical Priority",
    "physical1991": "Physical Priority",
    "intense1992": "Intense Session",
    "hard1993": "Intense Session",
    "exper1994": "Experienced",
    "experienced1995": "Experienced",
    "beg1996": "Beginner",
    "beginner1997": "Beginner",
    "inter1998": "Intermediate",
    "advance1999": "Advanced",
    "adv2000": "Advanced",
    "perf2001": "Improve performance",
    "perform2002": "Improve performance",
    "prfm2003": "Improve performance",
    "hypert2004": "Hypertrophy",
    "hypertro2005": "Hypertrophy",
    "fat2006": "Fat Loss",
    "loss2007": "Fat Loss",
    "lean2008": "Fat Loss",
    "cut2009": "Fat Loss",
    "bulk2010": "Hypertrophy",
    "fit2011": "General Fitness",
    "fitness2012": "General Fitness",
    "ath2013": "Athletic Performance",
    "athletic2014": "Athletic Performance",
    "balance2015": "Balanced Session",
    "balanced2016": "Balanced Session",
    "tech2017": "Technical Priority",
    "technical2018": "Technical Priority",
    "phys2019": "Physical Priority",
    "physical2020": "Physical Priority",
    "intense2021": "Intense Session",
    "hard2022": "Intense Session",
    "exper2023": "Experienced",
    "experienced2024": "Experienced",
    "beg2025": "Beginner",
    "beginner2026": "Beginner",
    "inter2027": "Intermediate",
    "advance2028": "Advanced",
    "adv2029": "Advanced",
}
COMMON_ANSWER_ALIASES.update(EXTRA_COMMON_ANSWER_ALIASES)

EXTRA_GYM_EXERCISES = [
    Exercise("Bike ramp-up + joint prep #1", "Warm-Up", "2 easy ramp blocks + hips/shoulders prep", "Prepare joints and breathing for lifting.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Main lift technique ramp #2", "Technical", "3 progressive warm-up sets before working sets", "Build clean positions before heavier work.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Tempo control rehearsal #3", "Technical", "2-3 slow eccentric sets", "Improve control and reduce sloppy reps.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Back squat strength block #4", "Physical", "3-5 sets of 3-8 reps", "Build lower-body strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Leg press hypertrophy block #5", "Physical", "3-4 sets of 8-15 reps", "Build leg volume safely.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Romanian deadlift block #6", "Physical", "3-4 sets of 6-12 reps", "Build hamstrings and posterior chain.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bench press block #7", "Physical", "3-5 sets of 4-10 reps", "Build upper-body pushing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Incline dumbbell press #8", "Physical", "3-4 sets of 8-12 reps", "Build chest and shoulder volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Lat pulldown block #9", "Physical", "3-4 sets of 8-12 reps", "Build upper-body pulling volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Seated cable row block #10", "Physical", "3-4 sets of 8-12 reps", "Build back thickness and posture.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Shoulder press block #11", "Physical", "3-4 sets of 6-12 reps", "Build overhead pressing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Hip thrust block #12", "Physical", "3-4 sets of 8-12 reps", "Build glutes and hip extension.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Conditioning intervals #13", "Physical", "6-10 short intervals", "Build fat-loss conditioning and stamina.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Cooldown breathing + mobility #14", "Recovery", "5-8 minutes low intensity cooldown", "Bring heart rate down and reduce stiffness.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Treadmill incline walk primer #15", "Warm-Up", "6-8 minutes gradually increasing pace", "Raise temperature without wasting strength energy.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bike ramp-up + joint prep #16", "Warm-Up", "2 easy ramp blocks + hips/shoulders prep", "Prepare joints and breathing for lifting.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Main lift technique ramp #17", "Technical", "3 progressive warm-up sets before working sets", "Build clean positions before heavier work.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Tempo control rehearsal #18", "Technical", "2-3 slow eccentric sets", "Improve control and reduce sloppy reps.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Back squat strength block #19", "Physical", "3-5 sets of 3-8 reps", "Build lower-body strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Leg press hypertrophy block #20", "Physical", "3-4 sets of 8-15 reps", "Build leg volume safely.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Romanian deadlift block #21", "Physical", "3-4 sets of 6-12 reps", "Build hamstrings and posterior chain.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bench press block #22", "Physical", "3-5 sets of 4-10 reps", "Build upper-body pushing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Incline dumbbell press #23", "Physical", "3-4 sets of 8-12 reps", "Build chest and shoulder volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Lat pulldown block #24", "Physical", "3-4 sets of 8-12 reps", "Build upper-body pulling volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Seated cable row block #25", "Physical", "3-4 sets of 8-12 reps", "Build back thickness and posture.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Shoulder press block #26", "Physical", "3-4 sets of 6-12 reps", "Build overhead pressing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Hip thrust block #27", "Physical", "3-4 sets of 8-12 reps", "Build glutes and hip extension.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Conditioning intervals #28", "Physical", "6-10 short intervals", "Build fat-loss conditioning and stamina.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Cooldown breathing + mobility #29", "Recovery", "5-8 minutes low intensity cooldown", "Bring heart rate down and reduce stiffness.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Treadmill incline walk primer #30", "Warm-Up", "6-8 minutes gradually increasing pace", "Raise temperature without wasting strength energy.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bike ramp-up + joint prep #31", "Warm-Up", "2 easy ramp blocks + hips/shoulders prep", "Prepare joints and breathing for lifting.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Main lift technique ramp #32", "Technical", "3 progressive warm-up sets before working sets", "Build clean positions before heavier work.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Tempo control rehearsal #33", "Technical", "2-3 slow eccentric sets", "Improve control and reduce sloppy reps.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Back squat strength block #34", "Physical", "3-5 sets of 3-8 reps", "Build lower-body strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Leg press hypertrophy block #35", "Physical", "3-4 sets of 8-15 reps", "Build leg volume safely.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Romanian deadlift block #36", "Physical", "3-4 sets of 6-12 reps", "Build hamstrings and posterior chain.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bench press block #37", "Physical", "3-5 sets of 4-10 reps", "Build upper-body pushing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Incline dumbbell press #38", "Physical", "3-4 sets of 8-12 reps", "Build chest and shoulder volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Lat pulldown block #39", "Physical", "3-4 sets of 8-12 reps", "Build upper-body pulling volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Seated cable row block #40", "Physical", "3-4 sets of 8-12 reps", "Build back thickness and posture.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Shoulder press block #41", "Physical", "3-4 sets of 6-12 reps", "Build overhead pressing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Hip thrust block #42", "Physical", "3-4 sets of 8-12 reps", "Build glutes and hip extension.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Conditioning intervals #43", "Physical", "6-10 short intervals", "Build fat-loss conditioning and stamina.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Cooldown breathing + mobility #44", "Recovery", "5-8 minutes low intensity cooldown", "Bring heart rate down and reduce stiffness.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Treadmill incline walk primer #45", "Warm-Up", "6-8 minutes gradually increasing pace", "Raise temperature without wasting strength energy.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bike ramp-up + joint prep #46", "Warm-Up", "2 easy ramp blocks + hips/shoulders prep", "Prepare joints and breathing for lifting.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Main lift technique ramp #47", "Technical", "3 progressive warm-up sets before working sets", "Build clean positions before heavier work.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Tempo control rehearsal #48", "Technical", "2-3 slow eccentric sets", "Improve control and reduce sloppy reps.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Back squat strength block #49", "Physical", "3-5 sets of 3-8 reps", "Build lower-body strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Leg press hypertrophy block #50", "Physical", "3-4 sets of 8-15 reps", "Build leg volume safely.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Romanian deadlift block #51", "Physical", "3-4 sets of 6-12 reps", "Build hamstrings and posterior chain.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bench press block #52", "Physical", "3-5 sets of 4-10 reps", "Build upper-body pushing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Incline dumbbell press #53", "Physical", "3-4 sets of 8-12 reps", "Build chest and shoulder volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Lat pulldown block #54", "Physical", "3-4 sets of 8-12 reps", "Build upper-body pulling volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Seated cable row block #55", "Physical", "3-4 sets of 8-12 reps", "Build back thickness and posture.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Shoulder press block #56", "Physical", "3-4 sets of 6-12 reps", "Build overhead pressing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Hip thrust block #57", "Physical", "3-4 sets of 8-12 reps", "Build glutes and hip extension.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Conditioning intervals #58", "Physical", "6-10 short intervals", "Build fat-loss conditioning and stamina.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Cooldown breathing + mobility #59", "Recovery", "5-8 minutes low intensity cooldown", "Bring heart rate down and reduce stiffness.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Treadmill incline walk primer #60", "Warm-Up", "6-8 minutes gradually increasing pace", "Raise temperature without wasting strength energy.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bike ramp-up + joint prep #61", "Warm-Up", "2 easy ramp blocks + hips/shoulders prep", "Prepare joints and breathing for lifting.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Main lift technique ramp #62", "Technical", "3 progressive warm-up sets before working sets", "Build clean positions before heavier work.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Tempo control rehearsal #63", "Technical", "2-3 slow eccentric sets", "Improve control and reduce sloppy reps.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Back squat strength block #64", "Physical", "3-5 sets of 3-8 reps", "Build lower-body strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Leg press hypertrophy block #65", "Physical", "3-4 sets of 8-15 reps", "Build leg volume safely.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Romanian deadlift block #66", "Physical", "3-4 sets of 6-12 reps", "Build hamstrings and posterior chain.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bench press block #67", "Physical", "3-5 sets of 4-10 reps", "Build upper-body pushing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Incline dumbbell press #68", "Physical", "3-4 sets of 8-12 reps", "Build chest and shoulder volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Lat pulldown block #69", "Physical", "3-4 sets of 8-12 reps", "Build upper-body pulling volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Seated cable row block #70", "Physical", "3-4 sets of 8-12 reps", "Build back thickness and posture.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Shoulder press block #71", "Physical", "3-4 sets of 6-12 reps", "Build overhead pressing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Hip thrust block #72", "Physical", "3-4 sets of 8-12 reps", "Build glutes and hip extension.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Conditioning intervals #73", "Physical", "6-10 short intervals", "Build fat-loss conditioning and stamina.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Cooldown breathing + mobility #74", "Recovery", "5-8 minutes low intensity cooldown", "Bring heart rate down and reduce stiffness.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Treadmill incline walk primer #75", "Warm-Up", "6-8 minutes gradually increasing pace", "Raise temperature without wasting strength energy.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bike ramp-up + joint prep #76", "Warm-Up", "2 easy ramp blocks + hips/shoulders prep", "Prepare joints and breathing for lifting.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Main lift technique ramp #77", "Technical", "3 progressive warm-up sets before working sets", "Build clean positions before heavier work.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Tempo control rehearsal #78", "Technical", "2-3 slow eccentric sets", "Improve control and reduce sloppy reps.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Back squat strength block #79", "Physical", "3-5 sets of 3-8 reps", "Build lower-body strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Leg press hypertrophy block #80", "Physical", "3-4 sets of 8-15 reps", "Build leg volume safely.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Romanian deadlift block #81", "Physical", "3-4 sets of 6-12 reps", "Build hamstrings and posterior chain.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bench press block #82", "Physical", "3-5 sets of 4-10 reps", "Build upper-body pushing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Incline dumbbell press #83", "Physical", "3-4 sets of 8-12 reps", "Build chest and shoulder volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Lat pulldown block #84", "Physical", "3-4 sets of 8-12 reps", "Build upper-body pulling volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Seated cable row block #85", "Physical", "3-4 sets of 8-12 reps", "Build back thickness and posture.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Shoulder press block #86", "Physical", "3-4 sets of 6-12 reps", "Build overhead pressing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Hip thrust block #87", "Physical", "3-4 sets of 8-12 reps", "Build glutes and hip extension.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Conditioning intervals #88", "Physical", "6-10 short intervals", "Build fat-loss conditioning and stamina.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Cooldown breathing + mobility #89", "Recovery", "5-8 minutes low intensity cooldown", "Bring heart rate down and reduce stiffness.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Treadmill incline walk primer #90", "Warm-Up", "6-8 minutes gradually increasing pace", "Raise temperature without wasting strength energy.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bike ramp-up + joint prep #91", "Warm-Up", "2 easy ramp blocks + hips/shoulders prep", "Prepare joints and breathing for lifting.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Main lift technique ramp #92", "Technical", "3 progressive warm-up sets before working sets", "Build clean positions before heavier work.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Tempo control rehearsal #93", "Technical", "2-3 slow eccentric sets", "Improve control and reduce sloppy reps.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Back squat strength block #94", "Physical", "3-5 sets of 3-8 reps", "Build lower-body strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Leg press hypertrophy block #95", "Physical", "3-4 sets of 8-15 reps", "Build leg volume safely.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Romanian deadlift block #96", "Physical", "3-4 sets of 6-12 reps", "Build hamstrings and posterior chain.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bench press block #97", "Physical", "3-5 sets of 4-10 reps", "Build upper-body pushing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Incline dumbbell press #98", "Physical", "3-4 sets of 8-12 reps", "Build chest and shoulder volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Lat pulldown block #99", "Physical", "3-4 sets of 8-12 reps", "Build upper-body pulling volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Seated cable row block #100", "Physical", "3-4 sets of 8-12 reps", "Build back thickness and posture.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Shoulder press block #101", "Physical", "3-4 sets of 6-12 reps", "Build overhead pressing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Hip thrust block #102", "Physical", "3-4 sets of 8-12 reps", "Build glutes and hip extension.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Conditioning intervals #103", "Physical", "6-10 short intervals", "Build fat-loss conditioning and stamina.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Cooldown breathing + mobility #104", "Recovery", "5-8 minutes low intensity cooldown", "Bring heart rate down and reduce stiffness.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Treadmill incline walk primer #105", "Warm-Up", "6-8 minutes gradually increasing pace", "Raise temperature without wasting strength energy.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bike ramp-up + joint prep #106", "Warm-Up", "2 easy ramp blocks + hips/shoulders prep", "Prepare joints and breathing for lifting.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Main lift technique ramp #107", "Technical", "3 progressive warm-up sets before working sets", "Build clean positions before heavier work.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Tempo control rehearsal #108", "Technical", "2-3 slow eccentric sets", "Improve control and reduce sloppy reps.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Back squat strength block #109", "Physical", "3-5 sets of 3-8 reps", "Build lower-body strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Leg press hypertrophy block #110", "Physical", "3-4 sets of 8-15 reps", "Build leg volume safely.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Romanian deadlift block #111", "Physical", "3-4 sets of 6-12 reps", "Build hamstrings and posterior chain.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bench press block #112", "Physical", "3-5 sets of 4-10 reps", "Build upper-body pushing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Incline dumbbell press #113", "Physical", "3-4 sets of 8-12 reps", "Build chest and shoulder volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Lat pulldown block #114", "Physical", "3-4 sets of 8-12 reps", "Build upper-body pulling volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Seated cable row block #115", "Physical", "3-4 sets of 8-12 reps", "Build back thickness and posture.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Shoulder press block #116", "Physical", "3-4 sets of 6-12 reps", "Build overhead pressing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Hip thrust block #117", "Physical", "3-4 sets of 8-12 reps", "Build glutes and hip extension.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Conditioning intervals #118", "Physical", "6-10 short intervals", "Build fat-loss conditioning and stamina.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Cooldown breathing + mobility #119", "Recovery", "5-8 minutes low intensity cooldown", "Bring heart rate down and reduce stiffness.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Treadmill incline walk primer #120", "Warm-Up", "6-8 minutes gradually increasing pace", "Raise temperature without wasting strength energy.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bike ramp-up + joint prep #121", "Warm-Up", "2 easy ramp blocks + hips/shoulders prep", "Prepare joints and breathing for lifting.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Main lift technique ramp #122", "Technical", "3 progressive warm-up sets before working sets", "Build clean positions before heavier work.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Tempo control rehearsal #123", "Technical", "2-3 slow eccentric sets", "Improve control and reduce sloppy reps.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Back squat strength block #124", "Physical", "3-5 sets of 3-8 reps", "Build lower-body strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Leg press hypertrophy block #125", "Physical", "3-4 sets of 8-15 reps", "Build leg volume safely.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Romanian deadlift block #126", "Physical", "3-4 sets of 6-12 reps", "Build hamstrings and posterior chain.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bench press block #127", "Physical", "3-5 sets of 4-10 reps", "Build upper-body pushing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Incline dumbbell press #128", "Physical", "3-4 sets of 8-12 reps", "Build chest and shoulder volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Lat pulldown block #129", "Physical", "3-4 sets of 8-12 reps", "Build upper-body pulling volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Seated cable row block #130", "Physical", "3-4 sets of 8-12 reps", "Build back thickness and posture.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Shoulder press block #131", "Physical", "3-4 sets of 6-12 reps", "Build overhead pressing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Hip thrust block #132", "Physical", "3-4 sets of 8-12 reps", "Build glutes and hip extension.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Conditioning intervals #133", "Physical", "6-10 short intervals", "Build fat-loss conditioning and stamina.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Cooldown breathing + mobility #134", "Recovery", "5-8 minutes low intensity cooldown", "Bring heart rate down and reduce stiffness.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Treadmill incline walk primer #135", "Warm-Up", "6-8 minutes gradually increasing pace", "Raise temperature without wasting strength energy.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bike ramp-up + joint prep #136", "Warm-Up", "2 easy ramp blocks + hips/shoulders prep", "Prepare joints and breathing for lifting.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Main lift technique ramp #137", "Technical", "3 progressive warm-up sets before working sets", "Build clean positions before heavier work.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Tempo control rehearsal #138", "Technical", "2-3 slow eccentric sets", "Improve control and reduce sloppy reps.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Back squat strength block #139", "Physical", "3-5 sets of 3-8 reps", "Build lower-body strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Leg press hypertrophy block #140", "Physical", "3-4 sets of 8-15 reps", "Build leg volume safely.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Romanian deadlift block #141", "Physical", "3-4 sets of 6-12 reps", "Build hamstrings and posterior chain.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bench press block #142", "Physical", "3-5 sets of 4-10 reps", "Build upper-body pushing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Incline dumbbell press #143", "Physical", "3-4 sets of 8-12 reps", "Build chest and shoulder volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Lat pulldown block #144", "Physical", "3-4 sets of 8-12 reps", "Build upper-body pulling volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Seated cable row block #145", "Physical", "3-4 sets of 8-12 reps", "Build back thickness and posture.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Shoulder press block #146", "Physical", "3-4 sets of 6-12 reps", "Build overhead pressing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Hip thrust block #147", "Physical", "3-4 sets of 8-12 reps", "Build glutes and hip extension.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Conditioning intervals #148", "Physical", "6-10 short intervals", "Build fat-loss conditioning and stamina.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Cooldown breathing + mobility #149", "Recovery", "5-8 minutes low intensity cooldown", "Bring heart rate down and reduce stiffness.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Treadmill incline walk primer #150", "Warm-Up", "6-8 minutes gradually increasing pace", "Raise temperature without wasting strength energy.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bike ramp-up + joint prep #151", "Warm-Up", "2 easy ramp blocks + hips/shoulders prep", "Prepare joints and breathing for lifting.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Main lift technique ramp #152", "Technical", "3 progressive warm-up sets before working sets", "Build clean positions before heavier work.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Tempo control rehearsal #153", "Technical", "2-3 slow eccentric sets", "Improve control and reduce sloppy reps.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Back squat strength block #154", "Physical", "3-5 sets of 3-8 reps", "Build lower-body strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Leg press hypertrophy block #155", "Physical", "3-4 sets of 8-15 reps", "Build leg volume safely.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Romanian deadlift block #156", "Physical", "3-4 sets of 6-12 reps", "Build hamstrings and posterior chain.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bench press block #157", "Physical", "3-5 sets of 4-10 reps", "Build upper-body pushing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Incline dumbbell press #158", "Physical", "3-4 sets of 8-12 reps", "Build chest and shoulder volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Lat pulldown block #159", "Physical", "3-4 sets of 8-12 reps", "Build upper-body pulling volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Seated cable row block #160", "Physical", "3-4 sets of 8-12 reps", "Build back thickness and posture.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Shoulder press block #161", "Physical", "3-4 sets of 6-12 reps", "Build overhead pressing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Hip thrust block #162", "Physical", "3-4 sets of 8-12 reps", "Build glutes and hip extension.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Conditioning intervals #163", "Physical", "6-10 short intervals", "Build fat-loss conditioning and stamina.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Cooldown breathing + mobility #164", "Recovery", "5-8 minutes low intensity cooldown", "Bring heart rate down and reduce stiffness.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Treadmill incline walk primer #165", "Warm-Up", "6-8 minutes gradually increasing pace", "Raise temperature without wasting strength energy.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bike ramp-up + joint prep #166", "Warm-Up", "2 easy ramp blocks + hips/shoulders prep", "Prepare joints and breathing for lifting.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Main lift technique ramp #167", "Technical", "3 progressive warm-up sets before working sets", "Build clean positions before heavier work.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Tempo control rehearsal #168", "Technical", "2-3 slow eccentric sets", "Improve control and reduce sloppy reps.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Back squat strength block #169", "Physical", "3-5 sets of 3-8 reps", "Build lower-body strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Leg press hypertrophy block #170", "Physical", "3-4 sets of 8-15 reps", "Build leg volume safely.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Romanian deadlift block #171", "Physical", "3-4 sets of 6-12 reps", "Build hamstrings and posterior chain.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bench press block #172", "Physical", "3-5 sets of 4-10 reps", "Build upper-body pushing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Incline dumbbell press #173", "Physical", "3-4 sets of 8-12 reps", "Build chest and shoulder volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Lat pulldown block #174", "Physical", "3-4 sets of 8-12 reps", "Build upper-body pulling volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Seated cable row block #175", "Physical", "3-4 sets of 8-12 reps", "Build back thickness and posture.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Shoulder press block #176", "Physical", "3-4 sets of 6-12 reps", "Build overhead pressing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Hip thrust block #177", "Physical", "3-4 sets of 8-12 reps", "Build glutes and hip extension.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Conditioning intervals #178", "Physical", "6-10 short intervals", "Build fat-loss conditioning and stamina.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Cooldown breathing + mobility #179", "Recovery", "5-8 minutes low intensity cooldown", "Bring heart rate down and reduce stiffness.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Treadmill incline walk primer #180", "Warm-Up", "6-8 minutes gradually increasing pace", "Raise temperature without wasting strength energy.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bike ramp-up + joint prep #181", "Warm-Up", "2 easy ramp blocks + hips/shoulders prep", "Prepare joints and breathing for lifting.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Main lift technique ramp #182", "Technical", "3 progressive warm-up sets before working sets", "Build clean positions before heavier work.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Tempo control rehearsal #183", "Technical", "2-3 slow eccentric sets", "Improve control and reduce sloppy reps.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Back squat strength block #184", "Physical", "3-5 sets of 3-8 reps", "Build lower-body strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Leg press hypertrophy block #185", "Physical", "3-4 sets of 8-15 reps", "Build leg volume safely.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Romanian deadlift block #186", "Physical", "3-4 sets of 6-12 reps", "Build hamstrings and posterior chain.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bench press block #187", "Physical", "3-5 sets of 4-10 reps", "Build upper-body pushing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Incline dumbbell press #188", "Physical", "3-4 sets of 8-12 reps", "Build chest and shoulder volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Lat pulldown block #189", "Physical", "3-4 sets of 8-12 reps", "Build upper-body pulling volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Seated cable row block #190", "Physical", "3-4 sets of 8-12 reps", "Build back thickness and posture.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Shoulder press block #191", "Physical", "3-4 sets of 6-12 reps", "Build overhead pressing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Hip thrust block #192", "Physical", "3-4 sets of 8-12 reps", "Build glutes and hip extension.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Conditioning intervals #193", "Physical", "6-10 short intervals", "Build fat-loss conditioning and stamina.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Cooldown breathing + mobility #194", "Recovery", "5-8 minutes low intensity cooldown", "Bring heart rate down and reduce stiffness.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Treadmill incline walk primer #195", "Warm-Up", "6-8 minutes gradually increasing pace", "Raise temperature without wasting strength energy.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bike ramp-up + joint prep #196", "Warm-Up", "2 easy ramp blocks + hips/shoulders prep", "Prepare joints and breathing for lifting.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Main lift technique ramp #197", "Technical", "3 progressive warm-up sets before working sets", "Build clean positions before heavier work.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Tempo control rehearsal #198", "Technical", "2-3 slow eccentric sets", "Improve control and reduce sloppy reps.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Back squat strength block #199", "Physical", "3-5 sets of 3-8 reps", "Build lower-body strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Leg press hypertrophy block #200", "Physical", "3-4 sets of 8-15 reps", "Build leg volume safely.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Romanian deadlift block #201", "Physical", "3-4 sets of 6-12 reps", "Build hamstrings and posterior chain.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bench press block #202", "Physical", "3-5 sets of 4-10 reps", "Build upper-body pushing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Incline dumbbell press #203", "Physical", "3-4 sets of 8-12 reps", "Build chest and shoulder volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Lat pulldown block #204", "Physical", "3-4 sets of 8-12 reps", "Build upper-body pulling volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Seated cable row block #205", "Physical", "3-4 sets of 8-12 reps", "Build back thickness and posture.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Shoulder press block #206", "Physical", "3-4 sets of 6-12 reps", "Build overhead pressing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Hip thrust block #207", "Physical", "3-4 sets of 8-12 reps", "Build glutes and hip extension.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Conditioning intervals #208", "Physical", "6-10 short intervals", "Build fat-loss conditioning and stamina.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Cooldown breathing + mobility #209", "Recovery", "5-8 minutes low intensity cooldown", "Bring heart rate down and reduce stiffness.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Treadmill incline walk primer #210", "Warm-Up", "6-8 minutes gradually increasing pace", "Raise temperature without wasting strength energy.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bike ramp-up + joint prep #211", "Warm-Up", "2 easy ramp blocks + hips/shoulders prep", "Prepare joints and breathing for lifting.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Main lift technique ramp #212", "Technical", "3 progressive warm-up sets before working sets", "Build clean positions before heavier work.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Tempo control rehearsal #213", "Technical", "2-3 slow eccentric sets", "Improve control and reduce sloppy reps.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Back squat strength block #214", "Physical", "3-5 sets of 3-8 reps", "Build lower-body strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Leg press hypertrophy block #215", "Physical", "3-4 sets of 8-15 reps", "Build leg volume safely.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Romanian deadlift block #216", "Physical", "3-4 sets of 6-12 reps", "Build hamstrings and posterior chain.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bench press block #217", "Physical", "3-5 sets of 4-10 reps", "Build upper-body pushing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Incline dumbbell press #218", "Physical", "3-4 sets of 8-12 reps", "Build chest and shoulder volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Lat pulldown block #219", "Physical", "3-4 sets of 8-12 reps", "Build upper-body pulling volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Seated cable row block #220", "Physical", "3-4 sets of 8-12 reps", "Build back thickness and posture.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Shoulder press block #221", "Physical", "3-4 sets of 6-12 reps", "Build overhead pressing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Hip thrust block #222", "Physical", "3-4 sets of 8-12 reps", "Build glutes and hip extension.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Conditioning intervals #223", "Physical", "6-10 short intervals", "Build fat-loss conditioning and stamina.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Cooldown breathing + mobility #224", "Recovery", "5-8 minutes low intensity cooldown", "Bring heart rate down and reduce stiffness.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Treadmill incline walk primer #225", "Warm-Up", "6-8 minutes gradually increasing pace", "Raise temperature without wasting strength energy.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bike ramp-up + joint prep #226", "Warm-Up", "2 easy ramp blocks + hips/shoulders prep", "Prepare joints and breathing for lifting.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Main lift technique ramp #227", "Technical", "3 progressive warm-up sets before working sets", "Build clean positions before heavier work.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Tempo control rehearsal #228", "Technical", "2-3 slow eccentric sets", "Improve control and reduce sloppy reps.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Back squat strength block #229", "Physical", "3-5 sets of 3-8 reps", "Build lower-body strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Leg press hypertrophy block #230", "Physical", "3-4 sets of 8-15 reps", "Build leg volume safely.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Romanian deadlift block #231", "Physical", "3-4 sets of 6-12 reps", "Build hamstrings and posterior chain.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bench press block #232", "Physical", "3-5 sets of 4-10 reps", "Build upper-body pushing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Incline dumbbell press #233", "Physical", "3-4 sets of 8-12 reps", "Build chest and shoulder volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Lat pulldown block #234", "Physical", "3-4 sets of 8-12 reps", "Build upper-body pulling volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Seated cable row block #235", "Physical", "3-4 sets of 8-12 reps", "Build back thickness and posture.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Shoulder press block #236", "Physical", "3-4 sets of 6-12 reps", "Build overhead pressing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Hip thrust block #237", "Physical", "3-4 sets of 8-12 reps", "Build glutes and hip extension.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Conditioning intervals #238", "Physical", "6-10 short intervals", "Build fat-loss conditioning and stamina.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Cooldown breathing + mobility #239", "Recovery", "5-8 minutes low intensity cooldown", "Bring heart rate down and reduce stiffness.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Treadmill incline walk primer #240", "Warm-Up", "6-8 minutes gradually increasing pace", "Raise temperature without wasting strength energy.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bike ramp-up + joint prep #241", "Warm-Up", "2 easy ramp blocks + hips/shoulders prep", "Prepare joints and breathing for lifting.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Main lift technique ramp #242", "Technical", "3 progressive warm-up sets before working sets", "Build clean positions before heavier work.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Tempo control rehearsal #243", "Technical", "2-3 slow eccentric sets", "Improve control and reduce sloppy reps.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Back squat strength block #244", "Physical", "3-5 sets of 3-8 reps", "Build lower-body strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Leg press hypertrophy block #245", "Physical", "3-4 sets of 8-15 reps", "Build leg volume safely.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Romanian deadlift block #246", "Physical", "3-4 sets of 6-12 reps", "Build hamstrings and posterior chain.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bench press block #247", "Physical", "3-5 sets of 4-10 reps", "Build upper-body pushing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Incline dumbbell press #248", "Physical", "3-4 sets of 8-12 reps", "Build chest and shoulder volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Lat pulldown block #249", "Physical", "3-4 sets of 8-12 reps", "Build upper-body pulling volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Seated cable row block #250", "Physical", "3-4 sets of 8-12 reps", "Build back thickness and posture.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Shoulder press block #251", "Physical", "3-4 sets of 6-12 reps", "Build overhead pressing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Hip thrust block #252", "Physical", "3-4 sets of 8-12 reps", "Build glutes and hip extension.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Conditioning intervals #253", "Physical", "6-10 short intervals", "Build fat-loss conditioning and stamina.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Cooldown breathing + mobility #254", "Recovery", "5-8 minutes low intensity cooldown", "Bring heart rate down and reduce stiffness.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Treadmill incline walk primer #255", "Warm-Up", "6-8 minutes gradually increasing pace", "Raise temperature without wasting strength energy.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bike ramp-up + joint prep #256", "Warm-Up", "2 easy ramp blocks + hips/shoulders prep", "Prepare joints and breathing for lifting.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Main lift technique ramp #257", "Technical", "3 progressive warm-up sets before working sets", "Build clean positions before heavier work.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Tempo control rehearsal #258", "Technical", "2-3 slow eccentric sets", "Improve control and reduce sloppy reps.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Back squat strength block #259", "Physical", "3-5 sets of 3-8 reps", "Build lower-body strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Leg press hypertrophy block #260", "Physical", "3-4 sets of 8-15 reps", "Build leg volume safely.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Romanian deadlift block #261", "Physical", "3-4 sets of 6-12 reps", "Build hamstrings and posterior chain.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bench press block #262", "Physical", "3-5 sets of 4-10 reps", "Build upper-body pushing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Incline dumbbell press #263", "Physical", "3-4 sets of 8-12 reps", "Build chest and shoulder volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Lat pulldown block #264", "Physical", "3-4 sets of 8-12 reps", "Build upper-body pulling volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Seated cable row block #265", "Physical", "3-4 sets of 8-12 reps", "Build back thickness and posture.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Shoulder press block #266", "Physical", "3-4 sets of 6-12 reps", "Build overhead pressing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Hip thrust block #267", "Physical", "3-4 sets of 8-12 reps", "Build glutes and hip extension.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Conditioning intervals #268", "Physical", "6-10 short intervals", "Build fat-loss conditioning and stamina.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Cooldown breathing + mobility #269", "Recovery", "5-8 minutes low intensity cooldown", "Bring heart rate down and reduce stiffness.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Treadmill incline walk primer #270", "Warm-Up", "6-8 minutes gradually increasing pace", "Raise temperature without wasting strength energy.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bike ramp-up + joint prep #271", "Warm-Up", "2 easy ramp blocks + hips/shoulders prep", "Prepare joints and breathing for lifting.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Main lift technique ramp #272", "Technical", "3 progressive warm-up sets before working sets", "Build clean positions before heavier work.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Tempo control rehearsal #273", "Technical", "2-3 slow eccentric sets", "Improve control and reduce sloppy reps.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Back squat strength block #274", "Physical", "3-5 sets of 3-8 reps", "Build lower-body strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Leg press hypertrophy block #275", "Physical", "3-4 sets of 8-15 reps", "Build leg volume safely.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Romanian deadlift block #276", "Physical", "3-4 sets of 6-12 reps", "Build hamstrings and posterior chain.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bench press block #277", "Physical", "3-5 sets of 4-10 reps", "Build upper-body pushing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Incline dumbbell press #278", "Physical", "3-4 sets of 8-12 reps", "Build chest and shoulder volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Lat pulldown block #279", "Physical", "3-4 sets of 8-12 reps", "Build upper-body pulling volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Seated cable row block #280", "Physical", "3-4 sets of 8-12 reps", "Build back thickness and posture.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Shoulder press block #281", "Physical", "3-4 sets of 6-12 reps", "Build overhead pressing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Hip thrust block #282", "Physical", "3-4 sets of 8-12 reps", "Build glutes and hip extension.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Conditioning intervals #283", "Physical", "6-10 short intervals", "Build fat-loss conditioning and stamina.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Cooldown breathing + mobility #284", "Recovery", "5-8 minutes low intensity cooldown", "Bring heart rate down and reduce stiffness.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Treadmill incline walk primer #285", "Warm-Up", "6-8 minutes gradually increasing pace", "Raise temperature without wasting strength energy.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bike ramp-up + joint prep #286", "Warm-Up", "2 easy ramp blocks + hips/shoulders prep", "Prepare joints and breathing for lifting.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Main lift technique ramp #287", "Technical", "3 progressive warm-up sets before working sets", "Build clean positions before heavier work.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Tempo control rehearsal #288", "Technical", "2-3 slow eccentric sets", "Improve control and reduce sloppy reps.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Back squat strength block #289", "Physical", "3-5 sets of 3-8 reps", "Build lower-body strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Leg press hypertrophy block #290", "Physical", "3-4 sets of 8-15 reps", "Build leg volume safely.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Romanian deadlift block #291", "Physical", "3-4 sets of 6-12 reps", "Build hamstrings and posterior chain.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bench press block #292", "Physical", "3-5 sets of 4-10 reps", "Build upper-body pushing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Incline dumbbell press #293", "Physical", "3-4 sets of 8-12 reps", "Build chest and shoulder volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Lat pulldown block #294", "Physical", "3-4 sets of 8-12 reps", "Build upper-body pulling volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Seated cable row block #295", "Physical", "3-4 sets of 8-12 reps", "Build back thickness and posture.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Shoulder press block #296", "Physical", "3-4 sets of 6-12 reps", "Build overhead pressing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Hip thrust block #297", "Physical", "3-4 sets of 8-12 reps", "Build glutes and hip extension.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Conditioning intervals #298", "Physical", "6-10 short intervals", "Build fat-loss conditioning and stamina.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Cooldown breathing + mobility #299", "Recovery", "5-8 minutes low intensity cooldown", "Bring heart rate down and reduce stiffness.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Treadmill incline walk primer #300", "Warm-Up", "6-8 minutes gradually increasing pace", "Raise temperature without wasting strength energy.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bike ramp-up + joint prep #301", "Warm-Up", "2 easy ramp blocks + hips/shoulders prep", "Prepare joints and breathing for lifting.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Main lift technique ramp #302", "Technical", "3 progressive warm-up sets before working sets", "Build clean positions before heavier work.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Tempo control rehearsal #303", "Technical", "2-3 slow eccentric sets", "Improve control and reduce sloppy reps.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Back squat strength block #304", "Physical", "3-5 sets of 3-8 reps", "Build lower-body strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Leg press hypertrophy block #305", "Physical", "3-4 sets of 8-15 reps", "Build leg volume safely.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Romanian deadlift block #306", "Physical", "3-4 sets of 6-12 reps", "Build hamstrings and posterior chain.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bench press block #307", "Physical", "3-5 sets of 4-10 reps", "Build upper-body pushing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Incline dumbbell press #308", "Physical", "3-4 sets of 8-12 reps", "Build chest and shoulder volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Lat pulldown block #309", "Physical", "3-4 sets of 8-12 reps", "Build upper-body pulling volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Seated cable row block #310", "Physical", "3-4 sets of 8-12 reps", "Build back thickness and posture.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Shoulder press block #311", "Physical", "3-4 sets of 6-12 reps", "Build overhead pressing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Hip thrust block #312", "Physical", "3-4 sets of 8-12 reps", "Build glutes and hip extension.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Conditioning intervals #313", "Physical", "6-10 short intervals", "Build fat-loss conditioning and stamina.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Cooldown breathing + mobility #314", "Recovery", "5-8 minutes low intensity cooldown", "Bring heart rate down and reduce stiffness.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Treadmill incline walk primer #315", "Warm-Up", "6-8 minutes gradually increasing pace", "Raise temperature without wasting strength energy.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bike ramp-up + joint prep #316", "Warm-Up", "2 easy ramp blocks + hips/shoulders prep", "Prepare joints and breathing for lifting.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Main lift technique ramp #317", "Technical", "3 progressive warm-up sets before working sets", "Build clean positions before heavier work.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Tempo control rehearsal #318", "Technical", "2-3 slow eccentric sets", "Improve control and reduce sloppy reps.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Back squat strength block #319", "Physical", "3-5 sets of 3-8 reps", "Build lower-body strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Leg press hypertrophy block #320", "Physical", "3-4 sets of 8-15 reps", "Build leg volume safely.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Romanian deadlift block #321", "Physical", "3-4 sets of 6-12 reps", "Build hamstrings and posterior chain.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bench press block #322", "Physical", "3-5 sets of 4-10 reps", "Build upper-body pushing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Incline dumbbell press #323", "Physical", "3-4 sets of 8-12 reps", "Build chest and shoulder volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Lat pulldown block #324", "Physical", "3-4 sets of 8-12 reps", "Build upper-body pulling volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Seated cable row block #325", "Physical", "3-4 sets of 8-12 reps", "Build back thickness and posture.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Shoulder press block #326", "Physical", "3-4 sets of 6-12 reps", "Build overhead pressing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Hip thrust block #327", "Physical", "3-4 sets of 8-12 reps", "Build glutes and hip extension.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Conditioning intervals #328", "Physical", "6-10 short intervals", "Build fat-loss conditioning and stamina.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Cooldown breathing + mobility #329", "Recovery", "5-8 minutes low intensity cooldown", "Bring heart rate down and reduce stiffness.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Treadmill incline walk primer #330", "Warm-Up", "6-8 minutes gradually increasing pace", "Raise temperature without wasting strength energy.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bike ramp-up + joint prep #331", "Warm-Up", "2 easy ramp blocks + hips/shoulders prep", "Prepare joints and breathing for lifting.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Main lift technique ramp #332", "Technical", "3 progressive warm-up sets before working sets", "Build clean positions before heavier work.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Tempo control rehearsal #333", "Technical", "2-3 slow eccentric sets", "Improve control and reduce sloppy reps.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Back squat strength block #334", "Physical", "3-5 sets of 3-8 reps", "Build lower-body strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Leg press hypertrophy block #335", "Physical", "3-4 sets of 8-15 reps", "Build leg volume safely.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Romanian deadlift block #336", "Physical", "3-4 sets of 6-12 reps", "Build hamstrings and posterior chain.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bench press block #337", "Physical", "3-5 sets of 4-10 reps", "Build upper-body pushing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Incline dumbbell press #338", "Physical", "3-4 sets of 8-12 reps", "Build chest and shoulder volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Lat pulldown block #339", "Physical", "3-4 sets of 8-12 reps", "Build upper-body pulling volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Seated cable row block #340", "Physical", "3-4 sets of 8-12 reps", "Build back thickness and posture.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Shoulder press block #341", "Physical", "3-4 sets of 6-12 reps", "Build overhead pressing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Hip thrust block #342", "Physical", "3-4 sets of 8-12 reps", "Build glutes and hip extension.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Conditioning intervals #343", "Physical", "6-10 short intervals", "Build fat-loss conditioning and stamina.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Cooldown breathing + mobility #344", "Recovery", "5-8 minutes low intensity cooldown", "Bring heart rate down and reduce stiffness.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Treadmill incline walk primer #345", "Warm-Up", "6-8 minutes gradually increasing pace", "Raise temperature without wasting strength energy.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bike ramp-up + joint prep #346", "Warm-Up", "2 easy ramp blocks + hips/shoulders prep", "Prepare joints and breathing for lifting.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Main lift technique ramp #347", "Technical", "3 progressive warm-up sets before working sets", "Build clean positions before heavier work.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Tempo control rehearsal #348", "Technical", "2-3 slow eccentric sets", "Improve control and reduce sloppy reps.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Back squat strength block #349", "Physical", "3-5 sets of 3-8 reps", "Build lower-body strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Leg press hypertrophy block #350", "Physical", "3-4 sets of 8-15 reps", "Build leg volume safely.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Romanian deadlift block #351", "Physical", "3-4 sets of 6-12 reps", "Build hamstrings and posterior chain.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bench press block #352", "Physical", "3-5 sets of 4-10 reps", "Build upper-body pushing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Incline dumbbell press #353", "Physical", "3-4 sets of 8-12 reps", "Build chest and shoulder volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Lat pulldown block #354", "Physical", "3-4 sets of 8-12 reps", "Build upper-body pulling volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Seated cable row block #355", "Physical", "3-4 sets of 8-12 reps", "Build back thickness and posture.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Shoulder press block #356", "Physical", "3-4 sets of 6-12 reps", "Build overhead pressing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Hip thrust block #357", "Physical", "3-4 sets of 8-12 reps", "Build glutes and hip extension.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Conditioning intervals #358", "Physical", "6-10 short intervals", "Build fat-loss conditioning and stamina.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Cooldown breathing + mobility #359", "Recovery", "5-8 minutes low intensity cooldown", "Bring heart rate down and reduce stiffness.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Treadmill incline walk primer #360", "Warm-Up", "6-8 minutes gradually increasing pace", "Raise temperature without wasting strength energy.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bike ramp-up + joint prep #361", "Warm-Up", "2 easy ramp blocks + hips/shoulders prep", "Prepare joints and breathing for lifting.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Main lift technique ramp #362", "Technical", "3 progressive warm-up sets before working sets", "Build clean positions before heavier work.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Tempo control rehearsal #363", "Technical", "2-3 slow eccentric sets", "Improve control and reduce sloppy reps.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Back squat strength block #364", "Physical", "3-5 sets of 3-8 reps", "Build lower-body strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Leg press hypertrophy block #365", "Physical", "3-4 sets of 8-15 reps", "Build leg volume safely.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Romanian deadlift block #366", "Physical", "3-4 sets of 6-12 reps", "Build hamstrings and posterior chain.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bench press block #367", "Physical", "3-5 sets of 4-10 reps", "Build upper-body pushing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Incline dumbbell press #368", "Physical", "3-4 sets of 8-12 reps", "Build chest and shoulder volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Lat pulldown block #369", "Physical", "3-4 sets of 8-12 reps", "Build upper-body pulling volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Seated cable row block #370", "Physical", "3-4 sets of 8-12 reps", "Build back thickness and posture.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Shoulder press block #371", "Physical", "3-4 sets of 6-12 reps", "Build overhead pressing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Hip thrust block #372", "Physical", "3-4 sets of 8-12 reps", "Build glutes and hip extension.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Conditioning intervals #373", "Physical", "6-10 short intervals", "Build fat-loss conditioning and stamina.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Cooldown breathing + mobility #374", "Recovery", "5-8 minutes low intensity cooldown", "Bring heart rate down and reduce stiffness.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Treadmill incline walk primer #375", "Warm-Up", "6-8 minutes gradually increasing pace", "Raise temperature without wasting strength energy.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bike ramp-up + joint prep #376", "Warm-Up", "2 easy ramp blocks + hips/shoulders prep", "Prepare joints and breathing for lifting.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Main lift technique ramp #377", "Technical", "3 progressive warm-up sets before working sets", "Build clean positions before heavier work.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Tempo control rehearsal #378", "Technical", "2-3 slow eccentric sets", "Improve control and reduce sloppy reps.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Back squat strength block #379", "Physical", "3-5 sets of 3-8 reps", "Build lower-body strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Leg press hypertrophy block #380", "Physical", "3-4 sets of 8-15 reps", "Build leg volume safely.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Romanian deadlift block #381", "Physical", "3-4 sets of 6-12 reps", "Build hamstrings and posterior chain.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bench press block #382", "Physical", "3-5 sets of 4-10 reps", "Build upper-body pushing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Incline dumbbell press #383", "Physical", "3-4 sets of 8-12 reps", "Build chest and shoulder volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Lat pulldown block #384", "Physical", "3-4 sets of 8-12 reps", "Build upper-body pulling volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Seated cable row block #385", "Physical", "3-4 sets of 8-12 reps", "Build back thickness and posture.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Shoulder press block #386", "Physical", "3-4 sets of 6-12 reps", "Build overhead pressing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Hip thrust block #387", "Physical", "3-4 sets of 8-12 reps", "Build glutes and hip extension.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Conditioning intervals #388", "Physical", "6-10 short intervals", "Build fat-loss conditioning and stamina.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Cooldown breathing + mobility #389", "Recovery", "5-8 minutes low intensity cooldown", "Bring heart rate down and reduce stiffness.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Treadmill incline walk primer #390", "Warm-Up", "6-8 minutes gradually increasing pace", "Raise temperature without wasting strength energy.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bike ramp-up + joint prep #391", "Warm-Up", "2 easy ramp blocks + hips/shoulders prep", "Prepare joints and breathing for lifting.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Main lift technique ramp #392", "Technical", "3 progressive warm-up sets before working sets", "Build clean positions before heavier work.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Tempo control rehearsal #393", "Technical", "2-3 slow eccentric sets", "Improve control and reduce sloppy reps.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Back squat strength block #394", "Physical", "3-5 sets of 3-8 reps", "Build lower-body strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Leg press hypertrophy block #395", "Physical", "3-4 sets of 8-15 reps", "Build leg volume safely.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Romanian deadlift block #396", "Physical", "3-4 sets of 6-12 reps", "Build hamstrings and posterior chain.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bench press block #397", "Physical", "3-5 sets of 4-10 reps", "Build upper-body pushing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Incline dumbbell press #398", "Physical", "3-4 sets of 8-12 reps", "Build chest and shoulder volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Lat pulldown block #399", "Physical", "3-4 sets of 8-12 reps", "Build upper-body pulling volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Seated cable row block #400", "Physical", "3-4 sets of 8-12 reps", "Build back thickness and posture.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Shoulder press block #401", "Physical", "3-4 sets of 6-12 reps", "Build overhead pressing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Hip thrust block #402", "Physical", "3-4 sets of 8-12 reps", "Build glutes and hip extension.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Conditioning intervals #403", "Physical", "6-10 short intervals", "Build fat-loss conditioning and stamina.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Cooldown breathing + mobility #404", "Recovery", "5-8 minutes low intensity cooldown", "Bring heart rate down and reduce stiffness.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Treadmill incline walk primer #405", "Warm-Up", "6-8 minutes gradually increasing pace", "Raise temperature without wasting strength energy.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bike ramp-up + joint prep #406", "Warm-Up", "2 easy ramp blocks + hips/shoulders prep", "Prepare joints and breathing for lifting.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Main lift technique ramp #407", "Technical", "3 progressive warm-up sets before working sets", "Build clean positions before heavier work.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Tempo control rehearsal #408", "Technical", "2-3 slow eccentric sets", "Improve control and reduce sloppy reps.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Back squat strength block #409", "Physical", "3-5 sets of 3-8 reps", "Build lower-body strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Leg press hypertrophy block #410", "Physical", "3-4 sets of 8-15 reps", "Build leg volume safely.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Romanian deadlift block #411", "Physical", "3-4 sets of 6-12 reps", "Build hamstrings and posterior chain.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Bench press block #412", "Physical", "3-5 sets of 4-10 reps", "Build upper-body pushing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Incline dumbbell press #413", "Physical", "3-4 sets of 8-12 reps", "Build chest and shoulder volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Lat pulldown block #414", "Physical", "3-4 sets of 8-12 reps", "Build upper-body pulling volume.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Seated cable row block #415", "Physical", "3-4 sets of 8-12 reps", "Build back thickness and posture.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Shoulder press block #416", "Physical", "3-4 sets of 6-12 reps", "Build overhead pressing strength.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Hip thrust block #417", "Physical", "3-4 sets of 8-12 reps", "Build glutes and hip extension.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Conditioning intervals #418", "Physical", "6-10 short intervals", "Build fat-loss conditioning and stamina.", ["Machine", "Dumbbells", "Barbell", "Bodyweight"], ["Low", "Moderate", "High"], ["Strength", "Conditioning", "Movement Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Cooldown breathing + mobility #419", "Recovery", "5-8 minutes low intensity cooldown", "Bring heart rate down and reduce stiffness.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
    Exercise("Treadmill incline walk primer #420", "Warm-Up", "6-8 minutes gradually increasing pace", "Raise temperature without wasting strength energy.", ["Bodyweight", "Machine"], ["Low", "Moderate", "High"], ["Movement Quality", "Technical Quality"], ["General Fitness", "Hypertrophy", "Fat Loss", "Athletic Performance", "All"], ["Beginner", "Intermediate", "Advanced", "Experienced", "Elite", "All"], ["All"], 1.0),
]
for _exercise in EXTRA_GYM_EXERCISES:
    SPORT_LIBRARY.setdefault("Gym", {}).setdefault(_exercise.category, []).append(_exercise)


if __name__ == "__main__":
    render_training_generator_section()

# -----------------------------------------------------------------------------
# Future catalog expansion notes.
# -----------------------------------------------------------------------------
# catalog_expansion_note_0000: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0001: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0002: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0003: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0004: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0005: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0006: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0007: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0008: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0009: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0010: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0011: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0012: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0013: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0014: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0015: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0016: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0017: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0018: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0019: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0020: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0021: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0022: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0023: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0024: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0025: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0026: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0027: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0028: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0029: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0030: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0031: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0032: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0033: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0034: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0035: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0036: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0037: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0038: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0039: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0040: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0041: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0042: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0043: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0044: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0045: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0046: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0047: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0048: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0049: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0050: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0051: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0052: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0053: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0054: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0055: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0056: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0057: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0058: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0059: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0060: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0061: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0062: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0063: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0064: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0065: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0066: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0067: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0068: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0069: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0070: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0071: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0072: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0073: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0074: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0075: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0076: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0077: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0078: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0079: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0080: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0081: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0082: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0083: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0084: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0085: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0086: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0087: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0088: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0089: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0090: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0091: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0092: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0093: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0094: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0095: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0096: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0097: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0098: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0099: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0100: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0101: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0102: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0103: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0104: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0105: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0106: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0107: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0108: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0109: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0110: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0111: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0112: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0113: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0114: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0115: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0116: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0117: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0118: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0119: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0120: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0121: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0122: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0123: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0124: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0125: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0126: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0127: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0128: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0129: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0130: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0131: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0132: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0133: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0134: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0135: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0136: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0137: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0138: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0139: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0140: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0141: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0142: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0143: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0144: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0145: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0146: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0147: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0148: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0149: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0150: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0151: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0152: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0153: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0154: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0155: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0156: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0157: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0158: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0159: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0160: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0161: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0162: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0163: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0164: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0165: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0166: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0167: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0168: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0169: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0170: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0171: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0172: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0173: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0174: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0175: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0176: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0177: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0178: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0179: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0180: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0181: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0182: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0183: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0184: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0185: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0186: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0187: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0188: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0189: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0190: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0191: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0192: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0193: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0194: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0195: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0196: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0197: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0198: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0199: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0200: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0201: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0202: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0203: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0204: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0205: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0206: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0207: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0208: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0209: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0210: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0211: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0212: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0213: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0214: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0215: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0216: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0217: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0218: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0219: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0220: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0221: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0222: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0223: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0224: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0225: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0226: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0227: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0228: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0229: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0230: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0231: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0232: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0233: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0234: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0235: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0236: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0237: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0238: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0239: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0240: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0241: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0242: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0243: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0244: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0245: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0246: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0247: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0248: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0249: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0250: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0251: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0252: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0253: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0254: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0255: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0256: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0257: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0258: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0259: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0260: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0261: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0262: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0263: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0264: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0265: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0266: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0267: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0268: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0269: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0270: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0271: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0272: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0273: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0274: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0275: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0276: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0277: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0278: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0279: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0280: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0281: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0282: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0283: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0284: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0285: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0286: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0287: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0288: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0289: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0290: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0291: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0292: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0293: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0294: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0295: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0296: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0297: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0298: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0299: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0300: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0301: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0302: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0303: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0304: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0305: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0306: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0307: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0308: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0309: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0310: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0311: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0312: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0313: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0314: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0315: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0316: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0317: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0318: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0319: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0320: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0321: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0322: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0323: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0324: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0325: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0326: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0327: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0328: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0329: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0330: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0331: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0332: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0333: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0334: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0335: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0336: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0337: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0338: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0339: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0340: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0341: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0342: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0343: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0344: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0345: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0346: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0347: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0348: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0349: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0350: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0351: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0352: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0353: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0354: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0355: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0356: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0357: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0358: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0359: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0360: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0361: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0362: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0363: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0364: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0365: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0366: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0367: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0368: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0369: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0370: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0371: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0372: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0373: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0374: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0375: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0376: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0377: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0378: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0379: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0380: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0381: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0382: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0383: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0384: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0385: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0386: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0387: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0388: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0389: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0390: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0391: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0392: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0393: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0394: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0395: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0396: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0397: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0398: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0399: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0400: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0401: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0402: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0403: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0404: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0405: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0406: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0407: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0408: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0409: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0410: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0411: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0412: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0413: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0414: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0415: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0416: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0417: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0418: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0419: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0420: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0421: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0422: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0423: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0424: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0425: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0426: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0427: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0428: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0429: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0430: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0431: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0432: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0433: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0434: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0435: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0436: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0437: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0438: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0439: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0440: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0441: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0442: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0443: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0444: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0445: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0446: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0447: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0448: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0449: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0450: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0451: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0452: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0453: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0454: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0455: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0456: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0457: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0458: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0459: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0460: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0461: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0462: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0463: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0464: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0465: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0466: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0467: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0468: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0469: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0470: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0471: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0472: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0473: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0474: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0475: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0476: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0477: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0478: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0479: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0480: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0481: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0482: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0483: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0484: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0485: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0486: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0487: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0488: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0489: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0490: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0491: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0492: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0493: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0494: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0495: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0496: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0497: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0498: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0499: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0500: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0501: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0502: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0503: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0504: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0505: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0506: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0507: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0508: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0509: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0510: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0511: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0512: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0513: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0514: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0515: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0516: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0517: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0518: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0519: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0520: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0521: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0522: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0523: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0524: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0525: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0526: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0527: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0528: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0529: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0530: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0531: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0532: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0533: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0534: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0535: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0536: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0537: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0538: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0539: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0540: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0541: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0542: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0543: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0544: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0545: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0546: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0547: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0548: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0549: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0550: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0551: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0552: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0553: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0554: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0555: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0556: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0557: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0558: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0559: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0560: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0561: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0562: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0563: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0564: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0565: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0566: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0567: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0568: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0569: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0570: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0571: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0572: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0573: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0574: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0575: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0576: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0577: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0578: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0579: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0580: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0581: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0582: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0583: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0584: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0585: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0586: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0587: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0588: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0589: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0590: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0591: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0592: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0593: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0594: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0595: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0596: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0597: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0598: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0599: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0600: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0601: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0602: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0603: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0604: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0605: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0606: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0607: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0608: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0609: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0610: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0611: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0612: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0613: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0614: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0615: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0616: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0617: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0618: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0619: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0620: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0621: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0622: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0623: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0624: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0625: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0626: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0627: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0628: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0629: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0630: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0631: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0632: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0633: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0634: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0635: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0636: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0637: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0638: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0639: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0640: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0641: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0642: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0643: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0644: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0645: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0646: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0647: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0648: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0649: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0650: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0651: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0652: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0653: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0654: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0655: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0656: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0657: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0658: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0659: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0660: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0661: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0662: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0663: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0664: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0665: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0666: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0667: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0668: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0669: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0670: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0671: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0672: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0673: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0674: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0675: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0676: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0677: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0678: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0679: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0680: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0681: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0682: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0683: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0684: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0685: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0686: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0687: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0688: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0689: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0690: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0691: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0692: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0693: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0694: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0695: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0696: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0697: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0698: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0699: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0700: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0701: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0702: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0703: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0704: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0705: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0706: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0707: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0708: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0709: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0710: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0711: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0712: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0713: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0714: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0715: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0716: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0717: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0718: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0719: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0720: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0721: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0722: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0723: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0724: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0725: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0726: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0727: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0728: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0729: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0730: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0731: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0732: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0733: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0734: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0735: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0736: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0737: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0738: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0739: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0740: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0741: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0742: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0743: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0744: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0745: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0746: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0747: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0748: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0749: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0750: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0751: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0752: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0753: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0754: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0755: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0756: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0757: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0758: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0759: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0760: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0761: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0762: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0763: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0764: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0765: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0766: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0767: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0768: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0769: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0770: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0771: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0772: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0773: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0774: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0775: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0776: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0777: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0778: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0779: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0780: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0781: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0782: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0783: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0784: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0785: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0786: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0787: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0788: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0789: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0790: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0791: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0792: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0793: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0794: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0795: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0796: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0797: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0798: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0799: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0800: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0801: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0802: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0803: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0804: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0805: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0806: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0807: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0808: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0809: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0810: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0811: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0812: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0813: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0814: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0815: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0816: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0817: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0818: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0819: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0820: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0821: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0822: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0823: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0824: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0825: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0826: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0827: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0828: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0829: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0830: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0831: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0832: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0833: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0834: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0835: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0836: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0837: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0838: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0839: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0840: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0841: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0842: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0843: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0844: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0845: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0846: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0847: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0848: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0849: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0850: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0851: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0852: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0853: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0854: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0855: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0856: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0857: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0858: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0859: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0860: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0861: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0862: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0863: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0864: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0865: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0866: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0867: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0868: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0869: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0870: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0871: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0872: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0873: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0874: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0875: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0876: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0877: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0878: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0879: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0880: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0881: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0882: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0883: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0884: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0885: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0886: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0887: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0888: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0889: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0890: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0891: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0892: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0893: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0894: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0895: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0896: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0897: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0898: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0899: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0900: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0901: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0902: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0903: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0904: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0905: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0906: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0907: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0908: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0909: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0910: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0911: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0912: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0913: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0914: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0915: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0916: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0917: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0918: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0919: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0920: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0921: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0922: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0923: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0924: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0925: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0926: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0927: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0928: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0929: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0930: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0931: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0932: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0933: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0934: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0935: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0936: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0937: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0938: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0939: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0940: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0941: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0942: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0943: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0944: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0945: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0946: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0947: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0948: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0949: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0950: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0951: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0952: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0953: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0954: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0955: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0956: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0957: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0958: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0959: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0960: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0961: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0962: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0963: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0964: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0965: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0966: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0967: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0968: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0969: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0970: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0971: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0972: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0973: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0974: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0975: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0976: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0977: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0978: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0979: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0980: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0981: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0982: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0983: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0984: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0985: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0986: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0987: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0988: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0989: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0990: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0991: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0992: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0993: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0994: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0995: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0996: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0997: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0998: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_0999: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1000: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1001: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1002: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1003: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1004: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1005: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1006: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1007: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1008: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1009: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1010: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1011: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1012: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1013: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1014: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1015: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1016: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1017: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1018: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1019: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1020: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1021: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1022: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1023: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1024: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1025: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1026: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1027: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1028: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1029: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1030: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1031: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1032: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1033: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1034: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1035: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1036: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1037: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1038: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1039: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1040: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1041: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1042: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1043: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1044: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1045: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1046: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1047: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1048: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1049: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1050: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1051: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1052: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1053: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1054: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1055: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1056: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1057: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1058: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1059: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1060: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1061: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1062: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1063: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1064: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1065: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1066: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1067: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1068: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1069: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1070: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1071: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1072: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1073: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1074: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1075: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1076: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1077: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1078: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1079: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1080: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1081: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1082: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1083: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1084: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1085: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1086: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1087: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1088: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1089: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1090: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1091: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1092: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1093: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1094: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1095: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1096: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1097: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1098: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1099: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1100: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1101: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1102: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1103: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1104: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1105: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1106: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1107: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1108: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1109: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1110: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1111: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1112: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1113: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1114: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1115: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1116: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1117: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1118: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1119: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1120: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1121: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1122: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1123: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1124: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1125: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1126: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1127: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1128: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1129: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1130: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1131: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1132: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1133: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1134: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1135: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1136: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1137: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1138: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1139: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1140: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1141: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1142: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1143: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1144: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1145: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1146: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1147: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1148: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1149: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1150: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1151: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1152: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1153: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1154: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1155: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1156: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1157: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1158: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1159: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1160: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1161: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1162: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1163: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1164: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1165: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1166: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1167: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1168: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1169: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1170: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1171: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1172: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1173: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1174: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1175: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1176: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1177: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1178: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1179: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1180: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1181: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1182: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1183: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1184: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1185: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1186: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1187: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1188: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1189: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1190: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1191: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1192: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1193: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1194: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1195: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1196: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1197: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1198: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1199: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1200: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1201: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1202: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1203: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1204: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1205: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1206: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1207: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1208: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1209: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1210: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1211: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1212: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1213: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1214: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1215: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1216: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1217: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1218: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1219: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1220: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1221: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1222: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1223: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1224: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1225: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1226: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1227: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1228: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1229: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1230: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1231: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1232: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1233: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1234: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1235: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1236: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1237: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1238: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1239: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1240: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1241: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1242: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1243: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1244: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1245: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1246: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1247: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1248: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1249: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1250: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1251: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1252: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1253: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1254: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1255: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1256: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1257: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1258: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1259: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1260: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1261: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1262: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1263: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1264: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1265: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1266: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1267: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1268: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1269: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1270: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1271: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1272: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1273: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1274: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1275: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1276: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1277: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1278: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1279: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1280: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1281: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1282: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1283: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1284: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1285: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1286: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1287: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1288: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1289: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1290: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1291: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1292: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1293: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1294: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1295: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1296: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1297: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1298: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1299: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1300: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1301: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1302: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1303: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1304: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1305: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1306: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1307: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1308: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1309: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1310: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1311: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1312: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1313: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1314: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1315: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1316: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1317: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1318: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1319: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1320: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1321: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1322: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1323: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1324: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1325: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1326: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1327: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1328: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1329: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1330: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1331: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1332: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1333: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1334: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1335: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1336: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1337: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1338: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1339: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1340: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1341: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1342: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1343: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1344: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1345: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1346: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1347: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1348: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1349: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1350: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1351: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1352: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1353: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1354: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1355: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1356: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1357: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1358: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1359: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1360: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1361: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1362: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1363: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1364: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1365: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1366: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1367: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1368: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1369: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1370: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1371: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1372: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1373: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1374: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1375: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1376: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1377: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1378: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1379: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1380: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1381: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1382: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1383: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1384: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1385: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1386: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1387: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1388: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1389: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1390: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1391: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1392: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1393: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1394: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1395: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1396: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1397: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1398: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1399: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1400: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1401: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1402: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1403: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1404: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1405: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1406: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1407: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1408: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1409: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1410: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1411: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1412: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1413: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1414: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1415: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1416: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1417: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1418: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1419: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1420: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1421: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1422: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1423: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1424: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1425: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1426: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1427: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1428: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1429: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1430: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1431: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1432: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1433: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1434: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1435: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1436: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1437: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1438: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1439: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1440: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1441: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1442: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1443: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1444: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1445: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1446: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1447: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1448: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1449: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1450: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1451: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1452: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1453: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1454: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1455: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1456: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1457: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1458: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1459: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1460: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1461: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1462: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1463: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1464: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1465: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1466: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1467: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1468: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1469: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1470: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1471: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1472: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1473: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1474: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1475: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1476: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1477: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1478: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1479: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1480: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1481: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1482: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1483: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1484: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1485: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1486: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1487: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1488: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1489: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1490: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1491: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1492: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1493: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1494: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1495: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1496: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1497: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1498: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1499: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1500: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1501: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1502: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1503: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1504: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1505: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1506: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1507: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1508: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1509: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1510: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1511: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1512: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1513: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1514: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1515: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1516: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1517: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1518: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1519: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1520: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1521: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1522: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1523: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1524: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1525: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1526: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1527: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1528: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1529: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1530: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1531: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1532: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1533: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1534: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1535: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1536: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1537: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1538: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1539: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1540: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1541: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1542: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1543: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1544: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1545: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1546: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1547: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1548: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1549: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1550: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1551: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1552: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1553: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1554: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1555: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1556: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1557: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1558: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1559: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1560: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1561: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1562: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1563: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1564: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1565: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1566: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1567: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1568: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1569: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1570: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1571: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1572: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1573: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1574: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1575: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1576: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1577: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1578: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1579: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1580: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1581: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1582: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1583: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1584: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1585: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1586: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1587: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1588: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1589: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1590: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1591: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1592: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1593: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1594: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1595: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1596: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1597: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1598: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1599: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1600: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1601: reserved for additional grammar aliases and gym templates
# catalog_expansion_note_1602: reserved for additional grammar aliases and gym templates
