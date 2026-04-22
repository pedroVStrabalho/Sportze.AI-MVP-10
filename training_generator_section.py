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
SESSION_TYPES = ["Balanced Session", "Technical Priority", "Physical Priority", "Competition Week"]
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


def detect_sport_type(sport_text: str) -> str:
    sport = normalize_lower(sport_text)
    if not sport:
        return ""
    if sport in KNOWN_TEAM_SPORTS:
        return "Team Sport"
    if sport in KNOWN_INDIVIDUAL_SPORTS:
        return "Individual Sport"
    return ""


def match_supported_sport(sport_text: str) -> Optional[str]:
    normalized = normalize_lower(sport_text)
    aliases = {
        "football": "Soccer",
        "soccer": "Soccer",
        "water polo": "Water Polo",
        "waterpolo": "Water Polo",
        "gym": "Gym",
        "fitness": "Gym",
    }
    if normalized in aliases:
        return aliases[normalized]
    for sport_name in SPORT_POSITIONS:
        if normalize_lower(sport_name) == normalized:
            return sport_name
    return None


def get_frequency_prompt(goal: str, level: str) -> str:
    if goal == "Learn how to play" or level == "Beginner":
        return "How many times do you play sports per week?"
    return "How many times do you train this sport per week?"


def get_question_flow(profile: Dict[str, str]) -> List[Dict[str, object]]:
    sport = profile.get("sport", "")
    sport_type = profile.get("sport_type", "") or detect_sport_type(sport)
    supported_sport = match_supported_sport(sport)
    positions = SPORT_POSITIONS.get(supported_sport, ["General Profile"])

    logged_in = bool(st.session_state.get("profile_email", "").strip())
    saved_name = normalize_text(str(st.session_state.get("athlete_name", "") or profile.get("athlete_name", "")))
    is_professional_value = profile.get("is_professional", False)
    is_professional = bool(is_professional_value is True or str(is_professional_value).strip().lower() in {"yes", "true", "1"})
    should_ask_name = (not logged_in) and (not saved_name) and is_professional

    flow = [
        {"key": "sport", "prompt": "What physical activity/sport do you play?", "type": "text"},
        {
            "key": "sport_type",
            "prompt": "Is this an individual sport or a team sport? You can answer: Individual Sport or Team Sport.",
            "type": "select",
            "options": ["Individual Sport", "Team Sport"],
            "skip_if_detected": True,
        },
    ]

    if sport_type == "Team Sport":
        flow.append({"key": "team_name", "prompt": "What team do you play for?", "type": "text"})

    flow.extend([
        {"key": "goal", "prompt": "What is your main goal?", "type": "select", "options": GOALS},
        {"key": "level", "prompt": "What is your current level?", "type": "select", "options": LEVELS},
        {"key": "weekly_target", "prompt": get_frequency_prompt(profile.get("goal", ""), profile.get("level", "")), "type": "int", "min": 1, "max": 7},
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

    if profile.get("level") in ["Advanced", "Elite"]:
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
        if not re.fullmatch(r"\d+", answer):
            return False, None, "Please answer with a number."
        value = int(answer)
        min_v = int(question.get("min", 0))
        max_v = int(question.get("max", 999))
        if value < min_v or value > max_v:
            return False, None, f"Please answer with a number between {min_v} and {max_v}."
        return True, value, None

    if q_type == "bool":
        lowered = normalize_lower(answer)
        if lowered in {"yes", "y", "true"}:
            return True, True, None
        if lowered in {"no", "n", "false"}:
            return True, False, None
        return False, None, "Please answer Yes or No."

    if q_type == "select":
        options = question.get("options", [])
        option_map = {normalize_lower(str(opt)): opt for opt in options}
        lowered = normalize_lower(answer)
        if lowered in option_map:
            return True, option_map[lowered], None
        return False, None, "Please answer using one of the shown options."

    if q_type == "select_or_text":
        options = question.get("options", [])
        option_map = {normalize_lower(str(opt)): opt for opt in options}
        lowered = normalize_lower(answer)
        if lowered in option_map:
            return True, option_map[lowered], None
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
    duration = int(profile.get("duration", 75))
    readiness = str(profile.get("readiness", "Moderate"))
    goal = str(profile.get("goal", "Improve performance"))
    level = str(profile.get("level", "Intermediate"))
    season_phase = str(profile.get("season_phase", "In-Season"))
    primary_focus = str(profile.get("primary_focus", "Technical Quality"))
    position = str(profile.get("position", "General Profile"))

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

    st.divider()
    render_history_panel()


if __name__ == "__main__":
    render_training_generator_section()
