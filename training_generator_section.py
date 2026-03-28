
import random
import re
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional

import streamlit as st


@dataclass
class Exercise:
    name: str
    category: str
    prescription: str
    purpose: str
    equipment_tags: List[str] = field(default_factory=list)
    intensity_tags: List[str] = field(default_factory=list)
    time_weight: float = 1.0


# -----------------------------------------------------------------------------
# SPORT CONFIGURATION
# -----------------------------------------------------------------------------
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


EQUIPMENT_LEVEL_DETAILS: Dict[str, Dict[str, List[str] | str]] = {
    "Minimal": {
        "label": "Minimal",
        "description": "Very limited setup. Mostly bodyweight, open space, and basic self-organized work.",
        "includes": ["Bodyweight", "Open space", "Wall or target", "Floor or grass area"],
    },
    "Basic": {
        "label": "Basic",
        "description": "Simple field or court access plus a few standard tools.",
        "includes": ["Balls or sport implement", "Cones", "Bands", "Basic court/field access"],
    },
    "Medium": {
        "label": "Medium",
        "description": "Good general training setup for most athletes.",
        "includes": ["Cones", "Balls", "Resistance bands", "Dumbbells", "Medicine ball", "Court/field/pool access"],
    },
    "Competitive": {
        "label": "Competitive",
        "description": "Strong club-level training environment with quality support resources.",
        "includes": ["Full court/field/pool setup", "Gym access", "Strength equipment", "Agility equipment", "Recovery tools"],
    },
    "Elite": {
        "label": "Elite",
        "description": "High-performance environment with broad equipment and support capacity.",
        "includes": ["Complete sport facility", "Full gym", "Specialized tools", "Monitoring resources", "Recovery resources"],
    },
}


# -----------------------------------------------------------------------------
# FUTURE API-READY STRUCTURES (PLACEHOLDERS ONLY - NO API YET)
# -----------------------------------------------------------------------------
API_READY_CONFIG = {
    "enabled": False,
    "provider": None,
    "model": None,
    "reasoning_mode": None,
    "research_mode": None,
}


def build_future_api_payload(profile: Dict[str, str | int | List[str]]) -> Dict[str, object]:
    """
    Placeholder helper to keep the generator organized for future API integration.
    This is intentionally not used yet.
    """
    return {
        "athlete_profile": profile,
        "generator_version": "training_generator_v4_api_ready",
        "requested_output": {
            "format": "structured_training_session",
            "needs_reasoning": True,
            "needs_professional_tone": True,
            "needs_measurable_prescriptions": True,
            "needs_sport_specific_progression": True,
            "needs_dynamic_time_allocation": True,
        },
        "future_modules": ["training_generation", "counseling", "video_review", "physio_support"],
        "api_status": "not_connected_yet",
    }


# -----------------------------------------------------------------------------
# TRAINING LIBRARY
# -----------------------------------------------------------------------------
SPORT_LIBRARY: Dict[str, Dict[str, List[Exercise]]] = {
    "Soccer": {
        "Warm-Up": [
            Exercise("Jog + mobility flow", "Warm-Up", "6 minutes easy jog + 6 mobility reps each movement", "Raise body temperature and open hips/ankles.", ["Bodyweight", "Open space"], time_weight=1.1),
            Exercise("Dynamic activation", "Warm-Up", "2 rounds of 20m each: high knees, butt kicks, side shuffles", "Prepare sprint mechanics.", ["Open space"], time_weight=0.9),
        ],
        "Technical": [
            Exercise("First-touch passing circuit", "Technical", "4 rounds x 3 minutes, 45 seconds rest", "Improve control and passing rhythm.", ["Ball", "Open space"], time_weight=1.0),
            Exercise("Dribble slalom + exit sprint", "Technical", "6 reps x 20m, walk-back recovery", "Tight control under speed.", ["Ball", "Cones"], time_weight=0.85),
            Exercise("Crossing and finishing", "Technical", "5 reps each side + 10 finishes", "Wide delivery and box timing.", ["Ball", "Goal", "Field"], time_weight=1.15),
        ],
        "Physical": [
            Exercise("Acceleration sprints", "Physical", "8 reps x 15m, 40 seconds rest", "Explosive first steps.", ["Open space"], time_weight=0.85),
            Exercise("Repeated sprint block", "Physical", "2 sets of 6 x 20m, 20 seconds rest between reps, 2 minutes between sets", "Match-like repeatability.", ["Open space"], time_weight=1.0),
            Exercise("Split squats", "Physical", "3 sets x 8 reps each leg", "Single-leg strength.", ["Bodyweight", "Dumbbells"], time_weight=0.9),
        ],
        "Tactical": [
            Exercise("Small-sided game", "Tactical", "4 rounds x 4 minutes, 2 minutes rest", "Decision-making under pressure.", ["Ball", "Field"], time_weight=1.3),
            Exercise("Pressing shape rehearsal", "Tactical", "5 rounds x 2 minutes", "Team organization and triggers.", ["Ball", "Field"], time_weight=0.95),
        ],
        "Recovery": [
            Exercise("Breathing walk + stretch", "Recovery", "6 minutes walk + 30 seconds per stretch", "Downregulate and improve recovery.", ["Bodyweight"], time_weight=0.8),
        ],
    },
    "Basketball": {
        "Warm-Up": [
            Exercise("Court movement warm-up", "Warm-Up", "2 rounds of 4 minutes", "Prepare hips, calves, shoulders.", ["Court"], time_weight=1.0),
            Exercise("Ball-handling activation", "Warm-Up", "3 minutes continuous", "Wake up handle and coordination.", ["Ball"], time_weight=0.8),
        ],
        "Technical": [
            Exercise("Form shooting", "Technical", "25 made shots", "Shooting mechanics.", ["Ball", "Court"], time_weight=0.95),
            Exercise("Cone change-of-direction dribble", "Technical", "6 reps each side", "Ball control and footwork.", ["Ball", "Cones"], time_weight=0.85),
            Exercise("Pick-and-roll reads", "Technical", "4 rounds x 3 minutes", "Game reads.", ["Ball", "Court"], time_weight=1.1),
        ],
        "Physical": [
            Exercise("Countermovement jumps", "Physical", "4 sets x 5 reps", "Vertical power.", ["Bodyweight"], time_weight=0.8),
            Exercise("Defensive slide intervals", "Physical", "6 reps x 20 seconds, 40 seconds rest", "Lateral conditioning.", ["Court"], time_weight=0.9),
            Exercise("Push-ups", "Physical", "3 sets x 10-15 reps", "Upper-body strength.", ["Bodyweight"], time_weight=0.8),
        ],
        "Tactical": [Exercise("Advantage game", "Tactical", "5 rounds x 3 minutes", "Transition decisions.", ["Ball", "Court"], time_weight=1.15)],
        "Recovery": [Exercise("Light mobility", "Recovery", "8 minutes", "Joint recovery.", ["Bodyweight"], time_weight=0.8)],
    },
    "Tennis": {
        "Warm-Up": [
            Exercise("Mini tennis + mobility", "Warm-Up", "8 minutes total", "Feel and footwork.", ["Racket", "Ball", "Court"], time_weight=1.1),
            Exercise("Split-step reaction drill", "Warm-Up", "3 sets x 45 seconds", "Timing and readiness.", ["Court"], time_weight=0.75),
        ],
        "Technical": [
            Exercise("Crosscourt consistency", "Technical", "4 rounds x 4 minutes", "Rally tolerance.", ["Racket", "Ball", "Court"], time_weight=1.2),
            Exercise("Serve targets", "Technical", "30 first serves + 20 second serves", "Placement and confidence.", ["Racket", "Ball", "Court"], time_weight=1.0),
            Exercise("Approach + volley sequence", "Technical", "12 reps each side", "Net transition.", ["Racket", "Ball", "Court"], time_weight=0.9),
        ],
        "Physical": [
            Exercise("Lateral shuffle intervals", "Physical", "6 reps x 20 seconds, 40 seconds rest", "Court movement endurance.", ["Court"], time_weight=0.85),
            Exercise("Medicine ball rotations", "Physical", "3 sets x 10 reps each side", "Rotational power.", ["Medicine ball"], time_weight=0.85),
            Exercise("Reverse lunges", "Physical", "3 sets x 8 reps each leg", "Lower-body control.", ["Bodyweight", "Dumbbells"], time_weight=0.85),
        ],
        "Tactical": [Exercise("Pattern play", "Tactical", "5 rounds x 3 points per pattern", "Build point construction.", ["Racket", "Ball", "Court"], time_weight=1.0)],
        "Recovery": [Exercise("Forearm/hip mobility", "Recovery", "6 minutes", "Reduce stiffness.", ["Bodyweight"], time_weight=0.75)],
    },
    "Volleyball": {
        "Warm-Up": [
            Exercise("Dynamic court warm-up", "Warm-Up", "7 minutes", "General readiness.", ["Court"], time_weight=1.0),
            Exercise("Arm swing activation", "Warm-Up", "2 sets x 12 reps", "Shoulder prep.", ["Bands", "Bodyweight"], time_weight=0.75),
        ],
        "Technical": [
            Exercise("Serve receive reps", "Technical", "20 quality passes", "Platform control.", ["Ball", "Court"], time_weight=0.95),
            Exercise("Setting accuracy", "Technical", "4 rounds x 2 minutes", "Tempo and placement.", ["Ball", "Court"], time_weight=0.9),
            Exercise("Approach jump spikes", "Technical", "5 sets x 4 reps", "Timing and hitting mechanics.", ["Ball", "Court"], time_weight=1.0),
        ],
        "Physical": [
            Exercise("Block jumps", "Physical", "4 sets x 5 reps", "Explosive jumping.", ["Court"], time_weight=0.85),
            Exercise("Band external rotations", "Physical", "3 sets x 12 reps", "Shoulder integrity.", ["Bands"], time_weight=0.75),
            Exercise("Tempo squats", "Physical", "3 sets x 8 reps", "Leg strength.", ["Bodyweight", "Dumbbells", "Barbell"], time_weight=0.95),
        ],
        "Tactical": [Exercise("6v6 situational play", "Tactical", "4 rounds x 5 minutes", "Rotation and decision-making.", ["Ball", "Court"], time_weight=1.2)],
        "Recovery": [Exercise("Shoulder and calf stretch", "Recovery", "6 minutes", "Restore range of motion.", ["Bodyweight"], time_weight=0.75)],
    },
    "Water Polo": {
        "Warm-Up": [
            Exercise("Swim + eggbeater prep", "Warm-Up", "200m easy swim + 3 x 30 seconds eggbeater", "Pool readiness.", ["Pool"], time_weight=1.1),
            Exercise("Shoulder mobility", "Warm-Up", "2 sets x 10 reps", "Throwing prep.", ["Bodyweight", "Bands"], time_weight=0.75),
        ],
        "Technical": [
            Exercise("Passing on the move", "Technical", "4 rounds x 3 minutes", "Ball speed and accuracy.", ["Pool", "Ball"], time_weight=1.0),
            Exercise("Shooting corners", "Technical", "20 shots total", "Finishing.", ["Pool", "Ball", "Goal"], time_weight=0.95),
            Exercise("Center battle positioning", "Technical", "6 reps x 20 seconds", "Body position under contact.", ["Pool", "Ball"], time_weight=0.9),
        ],
        "Physical": [
            Exercise("Sprint swims", "Physical", "8 reps x 15m, 30 seconds rest", "Explosive swimming.", ["Pool"], time_weight=0.9),
            Exercise("Eggbeater hold", "Physical", "4 reps x 40 seconds", "Leg endurance.", ["Pool"], time_weight=0.85),
            Exercise("Pull-ups or band pulls", "Physical", "3 sets x 6-10 reps", "Upper-body strength.", ["Pull-up bar", "Bands"], time_weight=0.85),
        ],
        "Tactical": [Exercise("6-on-5 execution", "Tactical", "5 rounds x 90 seconds", "Special situation organization.", ["Pool", "Ball"], time_weight=1.0)],
        "Recovery": [Exercise("Easy backstroke + stretch", "Recovery", "5 minutes swim + 5 minutes stretch", "Recovery.", ["Pool"], time_weight=0.9)],
    },
    "Baseball": {
        "Warm-Up": [Exercise("Throwing prep warm-up", "Warm-Up", "8 minutes", "Arm and hip readiness.", ["Ball", "Open space"], time_weight=1.0)],
        "Technical": [
            Exercise("Fielding fundamentals", "Technical", "4 rounds x 8 reps", "Clean glove work.", ["Ball", "Field"], time_weight=1.0),
            Exercise("Bat speed tee work", "Technical", "5 rounds x 6 swings", "Quality contact.", ["Bat", "Ball", "Field"], time_weight=0.95),
            Exercise("Long toss progression", "Technical", "10 minutes", "Throwing capacity.", ["Ball", "Field"], time_weight=1.05),
        ],
        "Physical": [
            Exercise("Rotational med-ball throws", "Physical", "3 sets x 8 reps each side", "Power transfer.", ["Medicine ball"], time_weight=0.85),
            Exercise("Broad jumps", "Physical", "4 sets x 4 reps", "Lower-body power.", ["Bodyweight"], time_weight=0.8),
            Exercise("Rear-foot elevated split squat", "Physical", "3 sets x 8 reps each leg", "Single-leg strength.", ["Bench", "Dumbbells"], time_weight=0.9),
        ],
        "Tactical": [Exercise("Situational defense", "Tactical", "4 rounds x 3 minutes", "Game IQ.", ["Field", "Ball"], time_weight=1.0)],
        "Recovery": [Exercise("Posterior shoulder care", "Recovery", "6 minutes", "Arm recovery.", ["Bands", "Bodyweight"], time_weight=0.8)],
    },
    "Running": {
        "Warm-Up": [Exercise("Run warm-up", "Warm-Up", "8 minutes easy + drills", "Prepare gait and tissue stiffness.", ["Open space"], time_weight=1.0)],
        "Technical": [
            Exercise("Strides", "Technical", "6 reps x 80m", "Running form at speed.", ["Track", "Road", "Open space"], time_weight=0.85),
            Exercise("Hill mechanics", "Technical", "6 reps x 12 seconds", "Drive and posture.", ["Hill", "Open space"], time_weight=0.8),
        ],
        "Physical": [
            Exercise("Main aerobic set", "Physical", "20-45 minutes depending on level", "Aerobic development.", ["Track", "Road", "Trail"], time_weight=2.2),
            Exercise("Calf raises", "Physical", "3 sets x 15 reps", "Lower-leg resilience.", ["Bodyweight", "Dumbbells"], time_weight=0.7),
            Exercise("Dead bugs", "Physical", "3 sets x 10 reps each side", "Core stability.", ["Bodyweight"], time_weight=0.7),
        ],
        "Tactical": [Exercise("Pacing rehearsal", "Tactical", "3 rounds x 5 minutes", "Race awareness.", ["Track", "Road"], time_weight=1.1)],
        "Recovery": [Exercise("Walk + mobility", "Recovery", "10 minutes", "Bring heart rate down.", ["Bodyweight"], time_weight=0.9)],
    },
    "Gym": {
        "Warm-Up": [Exercise("Cardio primer + mobility", "Warm-Up", "6 minutes cardio + 6 reps per mobility drill", "General prep.", ["Cardio machine", "Bodyweight"], time_weight=1.0)],
        "Technical": [Exercise("Movement pattern rehearsal", "Technical", "2 light sets per lift", "Safer lifting.", ["Barbell", "Dumbbells", "Machines"], time_weight=0.7)],
        "Physical": [
            Exercise("Squat or leg press", "Physical", "4 sets x 6-10 reps", "Lower-body strength.", ["Barbell", "Machine"], time_weight=1.2),
            Exercise("Bench or push variation", "Physical", "4 sets x 6-10 reps", "Upper-body pushing.", ["Barbell", "Dumbbells", "Machine"], time_weight=1.05),
            Exercise("Row or pull variation", "Physical", "4 sets x 8-12 reps", "Upper-body pulling.", ["Barbell", "Dumbbells", "Machine"], time_weight=1.05),
            Exercise("Conditioning finisher", "Physical", "8-12 minutes", "Work capacity.", ["Cardio machine", "Bodyweight"], time_weight=1.0),
        ],
        "Tactical": [Exercise("Tempo control", "Tactical", "Apply 2-0-2 tempo on first 2 exercises", "Technique discipline.", ["Barbell", "Dumbbells", "Machine"], time_weight=0.6)],
        "Recovery": [Exercise("Cooldown stretch", "Recovery", "6 minutes", "Recovery.", ["Bodyweight"], time_weight=0.75)],
    },
    "Weightlifting": {
        "Warm-Up": [Exercise("Barbell prep sequence", "Warm-Up", "8 minutes", "Mobility and groove.", ["Barbell", "Open space"], time_weight=1.0)],
        "Technical": [
            Exercise("Snatch technique", "Technical", "6 sets x 2 reps", "Bar path and speed.", ["Barbell"], time_weight=1.25),
            Exercise("Clean and jerk technique", "Technical", "5 sets x 2 reps", "Coordination.", ["Barbell"], time_weight=1.2),
        ],
        "Physical": [
            Exercise("Front squat", "Physical", "4 sets x 3-5 reps", "Strength for receiving positions.", ["Barbell"], time_weight=1.0),
            Exercise("Pulls", "Physical", "4 sets x 3 reps", "Explosive extension.", ["Barbell"], time_weight=0.95),
            Exercise("Core holds", "Physical", "3 sets x 30-45 seconds", "Trunk stiffness.", ["Bodyweight"], time_weight=0.75),
        ],
        "Tactical": [Exercise("Attempt selection practice", "Tactical", "3 mock waves", "Meet strategy.", ["Barbell"], time_weight=0.7)],
        "Recovery": [Exercise("Thoracic/ankle mobility", "Recovery", "8 minutes", "Position restoration.", ["Bodyweight"], time_weight=0.8)],
    },
    "Rowing": {
        "Warm-Up": [Exercise("Erg + mobility prep", "Warm-Up", "5 minutes erg + 5 minutes mobility", "Stroke prep.", ["Rowing erg", "Bodyweight"], time_weight=1.0)],
        "Technical": [
            Exercise("Pause drill", "Technical", "4 rounds x 3 minutes", "Sequencing.", ["Boat", "Erg"], time_weight=1.0),
            Exercise("Rate ladder", "Technical", "3 rounds x 4 minutes", "Control at different rates.", ["Boat", "Erg"], time_weight=1.05),
        ],
        "Physical": [
            Exercise("Main erg piece", "Physical", "3 x 8 minutes, 2 minutes rest", "Aerobic power.", ["Rowing erg"], time_weight=1.6),
            Exercise("Romanian deadlift", "Physical", "3 sets x 8 reps", "Posterior chain.", ["Barbell", "Dumbbells"], time_weight=0.9),
            Exercise("Plank", "Physical", "3 reps x 40 seconds", "Core endurance.", ["Bodyweight"], time_weight=0.7),
        ],
        "Tactical": [Exercise("Race rhythm simulation", "Tactical", "2 rounds x 6 minutes", "Pacing.", ["Boat", "Erg"], time_weight=1.0)],
        "Recovery": [Exercise("Easy paddle or walk", "Recovery", "8 minutes", "Recovery.", ["Boat", "Bodyweight"], time_weight=0.8)],
    },
}

SPORT_DURATION_STYLE: Dict[str, Dict[str, int]] = {
    "Soccer": {"short": 6, "standard": 7, "long": 8},
    "Basketball": {"short": 6, "standard": 7, "long": 8},
    "Tennis": {"short": 5, "standard": 6, "long": 7},
    "Volleyball": {"short": 6, "standard": 7, "long": 8},
    "Water Polo": {"short": 6, "standard": 7, "long": 8},
    "Baseball": {"short": 5, "standard": 6, "long": 7},
    "Running": {"short": 4, "standard": 5, "long": 6},
    "Gym": {"short": 5, "standard": 6, "long": 7},
    "Weightlifting": {"short": 5, "standard": 6, "long": 7},
    "Rowing": {"short": 5, "standard": 6, "long": 7},
}

SPORT_BLUEPRINTS: Dict[str, Dict[str, Dict[str, int]]] = {
    "Soccer": {
        "Balanced Session": {"Warm-Up": 2, "Technical": 2, "Physical": 2, "Tactical": 1, "Recovery": 1},
        "Technical Priority": {"Warm-Up": 2, "Technical": 3, "Physical": 1, "Tactical": 1, "Recovery": 1},
        "Physical Priority": {"Warm-Up": 2, "Technical": 1, "Physical": 3, "Tactical": 1, "Recovery": 1},
        "Competition Week": {"Warm-Up": 2, "Technical": 2, "Physical": 1, "Tactical": 1, "Recovery": 1},
    },
    "Tennis": {
        "Balanced Session": {"Warm-Up": 2, "Technical": 2, "Physical": 2, "Tactical": 0, "Recovery": 1},
        "Technical Priority": {"Warm-Up": 2, "Technical": 3, "Physical": 1, "Tactical": 0, "Recovery": 1},
        "Physical Priority": {"Warm-Up": 2, "Technical": 1, "Physical": 3, "Tactical": 0, "Recovery": 1},
        "Competition Week": {"Warm-Up": 2, "Technical": 2, "Physical": 1, "Tactical": 0, "Recovery": 1},
    },
    "Running": {
        "Balanced Session": {"Warm-Up": 1, "Technical": 1, "Physical": 2, "Tactical": 0, "Recovery": 1},
        "Technical Priority": {"Warm-Up": 1, "Technical": 2, "Physical": 1, "Tactical": 0, "Recovery": 1},
        "Physical Priority": {"Warm-Up": 1, "Technical": 1, "Physical": 3, "Tactical": 0, "Recovery": 1},
        "Competition Week": {"Warm-Up": 1, "Technical": 1, "Physical": 1, "Tactical": 1, "Recovery": 1},
    },
    "Gym": {
        "Balanced Session": {"Warm-Up": 1, "Technical": 1, "Physical": 3, "Tactical": 0, "Recovery": 1},
        "Technical Priority": {"Warm-Up": 1, "Technical": 1, "Physical": 3, "Tactical": 0, "Recovery": 1},
        "Physical Priority": {"Warm-Up": 1, "Technical": 0, "Physical": 4, "Tactical": 0, "Recovery": 1},
        "Competition Week": {"Warm-Up": 1, "Technical": 1, "Physical": 2, "Tactical": 0, "Recovery": 1},
    },
    "Weightlifting": {
        "Balanced Session": {"Warm-Up": 1, "Technical": 2, "Physical": 2, "Tactical": 0, "Recovery": 1},
        "Technical Priority": {"Warm-Up": 1, "Technical": 2, "Physical": 1, "Tactical": 1, "Recovery": 1},
        "Physical Priority": {"Warm-Up": 1, "Technical": 1, "Physical": 3, "Tactical": 0, "Recovery": 1},
        "Competition Week": {"Warm-Up": 1, "Technical": 2, "Physical": 1, "Tactical": 1, "Recovery": 1},
    },
    "Rowing": {
        "Balanced Session": {"Warm-Up": 1, "Technical": 2, "Physical": 2, "Tactical": 0, "Recovery": 1},
        "Technical Priority": {"Warm-Up": 1, "Technical": 2, "Physical": 1, "Tactical": 1, "Recovery": 1},
        "Physical Priority": {"Warm-Up": 1, "Technical": 1, "Physical": 3, "Tactical": 0, "Recovery": 1},
        "Competition Week": {"Warm-Up": 1, "Technical": 1, "Physical": 1, "Tactical": 1, "Recovery": 1},
    },
}

DEFAULT_BLUEPRINTS = {
    "Balanced Session": {"Warm-Up": 2, "Technical": 2, "Physical": 2, "Tactical": 1, "Recovery": 1},
    "Technical Priority": {"Warm-Up": 2, "Technical": 3, "Physical": 1, "Tactical": 1, "Recovery": 1},
    "Physical Priority": {"Warm-Up": 2, "Technical": 1, "Physical": 3, "Tactical": 1, "Recovery": 1},
    "Competition Week": {"Warm-Up": 2, "Technical": 2, "Physical": 1, "Tactical": 1, "Recovery": 1},
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


# -----------------------------------------------------------------------------
# GENERATOR HELPERS
# -----------------------------------------------------------------------------
def get_frequency_prompt(goal: str, level: str) -> str:
    if goal == "Learn how to play" or level == "Beginner":
        return "How many times do you play sports per week?"
    return "How many times do you train this sport per week?"


def get_equipment_guidance(level: str) -> Dict[str, List[str] | str]:
    return EQUIPMENT_LEVEL_DETAILS.get(level, EQUIPMENT_LEVEL_DETAILS["Basic"])


def normalize_equipment_level(level: str) -> str:
    return level.strip().title()


def duration_bucket(duration: int) -> str:
    if duration <= 55:
        return "short"
    if duration <= 95:
        return "standard"
    return "long"


def target_exercise_count(sport: str, duration: int) -> int:
    style = SPORT_DURATION_STYLE.get(sport, {"short": 6, "standard": 7, "long": 8})
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


def adapt_session_for_equipment(session: List[Exercise], equipment_level: str, sport: str) -> List[Exercise]:
    """
    Current version keeps the core library intact while adding equipment-level adaptations.
    This makes the section ready for future API enhancement without changing core ideas.
    """
    normalized = normalize_equipment_level(equipment_level)

    if normalized in ["Competitive", "Elite"]:
        return session

    adjusted: List[Exercise] = []
    for ex in session:
        if normalized == "Minimal":
            if any(tag in ex.equipment_tags for tag in ["Barbell", "Machine", "Medicine ball", "Rowing erg", "Pool", "Boat"]):
                adjusted.append(
                    Exercise(
                        name=f"Adapted version of {ex.name}",
                        category=ex.category,
                        prescription=ex.prescription,
                        purpose=f"Low-equipment adaptation: {ex.purpose}",
                        equipment_tags=["Bodyweight", "Open space"],
                        time_weight=ex.time_weight,
                    )
                )
            else:
                adjusted.append(ex)
        elif normalized == "Basic":
            if any(tag in ex.equipment_tags for tag in ["Barbell", "Machine", "Boat"]):
                adjusted.append(
                    Exercise(
                        name=f"Basic setup adaptation - {ex.name}",
                        category=ex.category,
                        prescription=ex.prescription,
                        purpose=f"Adapted for a simpler training environment. {ex.purpose}",
                        equipment_tags=["Bodyweight", "Cones", "Bands", "Balls"],
                        time_weight=ex.time_weight,
                    )
                )
            else:
                adjusted.append(ex)
        else:
            adjusted.append(ex)

    return adjusted


def parse_prescription_minutes(prescription: str) -> Optional[int]:
    text = prescription.lower().replace("~", "").strip()

    m = re.search(r"(\d+)\s*(?:x|rounds? x|sets? x)\s*(\d+)\s*minutes?", text)
    if m:
        return int(m.group(1)) * int(m.group(2))

    m = re.search(r"(\d+)\s*rounds?\s*x\s*(\d+)\s*minutes?", text)
    if m:
        return int(m.group(1)) * int(m.group(2))

    if "minutes total" in text:
        m = re.search(r"(\d+)\s*minutes? total", text)
        if m:
            return int(m.group(1))

    if "minutes easy" in text:
        m = re.search(r"(\d+)\s*minutes? easy", text)
        if m:
            return int(m.group(1)) + 4

    if "minutes erg + " in text:
        nums = [int(n) for n in re.findall(r"(\d+)\s*minutes?", text)]
        if nums:
            return sum(nums)

    nums = [int(n) for n in re.findall(r"(\d+)\s*minutes?", text)]
    if len(nums) == 1:
        return nums[0]

    if "20-45 minutes" in text:
        return 30
    if "8-12 minutes" in text:
        return 10

    if "shots total" in text:
        return 10
    if "made shots" in text:
        return 10
    if "quality passes" in text:
        return 10
    if "mock waves" in text:
        return 9
    if "light sets per lift" in text:
        return 8

    if "x" in text and "seconds" in text:
        sec_nums = [int(n) for n in re.findall(r"(\d+)\s*seconds?", text)]
        rep_nums = [int(n) for n in re.findall(r"(\d+)\s*x", text)]
        if sec_nums and rep_nums:
            total_seconds = rep_nums[0] * sec_nums[0]
            rest_match = re.search(r"(\d+)\s*seconds? rest", text)
            if rest_match:
                total_seconds += max(0, rep_nums[0] - 1) * int(rest_match.group(1))
            return max(4, round(total_seconds / 60))

    if "sets x" in text and "reps" in text:
        sets_match = re.search(r"(\d+)\s*sets?", text)
        if sets_match:
            sets = int(sets_match.group(1))
            return max(6, sets * 3)

    return None


def category_share_map(session_type: str) -> Dict[str, float]:
    shares = dict(CATEGORY_BASE_SHARES)
    adjustments = SESSION_TYPE_CATEGORY_ADJUSTMENTS.get(session_type, {})
    for key, mult in adjustments.items():
        shares[key] = shares.get(key, 0.0) * mult
    total = sum(shares.values())
    return {k: v / total for k, v in shares.items()}


def allocate_block_minutes(session: List[Exercise], duration: int, session_type: str) -> List[int]:
    explicit_minutes: List[Optional[int]] = [parse_prescription_minutes(ex.prescription) for ex in session]
    fixed_total = sum(m for m in explicit_minutes if m is not None)
    remaining = max(0, duration - fixed_total)

    shares = category_share_map(session_type)
    unresolved_indices = [idx for idx, value in enumerate(explicit_minutes) if value is None]

    if unresolved_indices:
        category_weights: Dict[str, float] = {}
        for idx in unresolved_indices:
            ex = session[idx]
            category_weights[idx] = shares.get(ex.category, 0.1) * max(0.5, ex.time_weight)

        total_weight = sum(category_weights.values()) or 1.0
        allocations = {}
        for idx in unresolved_indices:
            raw = remaining * (category_weights[idx] / total_weight)
            allocations[idx] = max(5, round(raw))

        current_sum = sum(allocations.values())
        diff = remaining - current_sum
        ordered_indices = sorted(unresolved_indices, key=lambda i: category_weights[i], reverse=True)

        pointer = 0
        while diff != 0 and ordered_indices:
            i = ordered_indices[pointer % len(ordered_indices)]
            if diff > 0:
                allocations[i] += 1
                diff -= 1
            elif allocations[i] > 5:
                allocations[i] -= 1
                diff += 1
            pointer += 1

        for idx in unresolved_indices:
            explicit_minutes[idx] = allocations[idx]

    return [int(value or 0) for value in explicit_minutes]


def build_session(sport: str, session_type: str, equipment_level: str, duration: int) -> List[Exercise]:
    lib = SPORT_LIBRARY[sport]
    blueprint = get_blueprint(sport, session_type)
    blueprint = trim_blueprint_to_target(blueprint, target_exercise_count(sport, duration))

    session: List[Exercise] = []
    for category, requested_count in blueprint.items():
        if requested_count <= 0:
            continue
        library_items = lib.get(category, [])
        if not library_items:
            continue
        if requested_count >= len(library_items):
            session.extend(random.sample(library_items, k=len(library_items)))
        else:
            session.extend(random.sample(library_items, k=requested_count))

    return adapt_session_for_equipment(session, equipment_level, sport)


def weekly_focus(days: int, goal: str) -> List[str]:
    base = [
        "Day 1: Main development session",
        "Day 2: Technical efficiency session",
        "Day 3: Speed / power / intensity session",
        "Day 4: Recovery or light skill session",
        "Day 5: Tactical or match simulation",
        "Day 6: Strength / conditioning support",
        "Day 7: Full recovery",
    ]
    if goal == "Return after a break":
        base[0] = "Day 1: Controlled re-entry session"
        base[2] = "Day 3: Moderate intensity exposure"
    elif goal == "Competition preparation":
        base[4] = "Day 5: Competition simulation"
    return base[:max(1, min(days, 7))]


def build_profile_summary(
    role: str,
    sport: str,
    position: str,
    goal: str,
    level: str,
    weekly_frequency: int,
    duration: int,
    session_type: str,
    equipment_level: str,
) -> Dict[str, object]:
    return {
        "role": role,
        "sport": sport,
        "position": position,
        "goal": goal,
        "level": level,
        "weekly_frequency": weekly_frequency,
        "duration_minutes": duration,
        "session_type": session_type,
        "equipment_level": equipment_level,
    }


def render_equipment_level_box(equipment_level: str) -> None:
    info = get_equipment_guidance(equipment_level)
    st.info(
        f"**Equipment level: {info['label']}**\n\n"
        f"{info['description']}\n\n"
        f"Typical setup: {', '.join(info['includes'])}"
    )


def build_session_summary_line(session: List[Exercise], block_minutes: List[int], duration: int) -> str:
    counts_by_category: Dict[str, int] = {}
    for ex in session:
        counts_by_category[ex.category] = counts_by_category.get(ex.category, 0) + 1
    category_bits = [f"{cat}: {count}" for cat, count in counts_by_category.items()]
    return f"{len(session)} training blocks | Planned duration: ~{sum(block_minutes)} of {duration} minutes | " + " | ".join(category_bits)


# -----------------------------------------------------------------------------
# STREAMLIT SECTION
# -----------------------------------------------------------------------------
def render_training_generator_section() -> None:
    st.header("Training Generator")
    st.write(
        "Generate sessions with exercise names, exact reps, sets, and time prescriptions for every sport. "
        "This version also fixes the old issue of equally divided drill times by using sport-specific session structure and dynamic block planning."
    )

    role = st.radio("Are you a player or coach?", ["Player", "Coach"], horizontal=True)

    c1, c2 = st.columns(2)
    with c1:
        sport = st.selectbox("Choose the sport", list(SPORT_POSITIONS.keys()))
        position = st.selectbox("Choose the position / profile", SPORT_POSITIONS[sport])
        goal = st.selectbox("Main goal", GOALS)
        level = st.selectbox("Current level", LEVELS)
    with c2:
        weekly_frequency = st.slider(get_frequency_prompt(goal, level), 1, 7, 4)
        session_type = st.selectbox("Session type", SESSION_TYPES)
        duration = st.slider("Session duration (minutes)", 30, 180, 75, step=5)
        equipment_level = st.selectbox(
            "Level of equipment available",
            EQUIPMENT_LEVELS,
            index=1,
            help="Choose the overall quality of the equipment and training environment available.",
        )

    render_equipment_level_box(equipment_level)

    notes = st.text_area(
        "Extra notes",
        placeholder="Examples: match in 3 days, shoulder fatigue, focus on speed, beginner team, small training space...",
    )

    st.caption(
        "API-ready foundation included: structured athlete profile, future payload builder, dynamic session blueprint logic, and modular timing functions. "
        "No API has been connected yet."
    )

    if st.button("Generate Training Session", type="primary", use_container_width=True):
        session = build_session(sport, session_type, equipment_level, duration)
        block_minutes = allocate_block_minutes(session, duration, session_type)

        profile_summary = build_profile_summary(
            role=role,
            sport=sport,
            position=position,
            goal=goal,
            level=level,
            weekly_frequency=weekly_frequency,
            duration=duration,
            session_type=session_type,
            equipment_level=equipment_level,
        )
        future_payload = build_future_api_payload(profile_summary)

        st.subheader(f"{sport} Session Plan")
        st.write(
            f"**Profile:** {role} | **Position:** {position} | **Goal:** {goal} | **Level:** {level} | "
            f"**Weekly frequency:** {weekly_frequency} | **Duration target:** {duration} minutes"
        )
        st.caption(f"Equipment level selected: {equipment_level}")
        st.caption(build_session_summary_line(session, block_minutes, duration))

        if notes.strip():
            st.info(f"Coach notes considered: {notes}")

        for idx, (ex, planned_minutes) in enumerate(zip(session, block_minutes), start=1):
            with st.expander(f"{idx}. {ex.name}", expanded=True if idx <= 3 else False):
                st.markdown(f"**Category:** {ex.category}")
                st.markdown(f"**Prescription:** {ex.prescription}")
                st.markdown(f"**Purpose:** {ex.purpose}")
                st.markdown(f"**Planned block duration in this session:** ~{planned_minutes} minutes")
                if ex.equipment_tags:
                    st.markdown(f"**Typical equipment for this drill:** {', '.join(ex.equipment_tags)}")

        st.subheader("Weekly structure suggestion")
        for item in weekly_focus(weekly_frequency, goal):
            st.write(f"- {item}")

        st.subheader("Professional coaching reminders")
        reminders = [
            "Different drills should not always carry the same time load. Longer pattern or main-set work should naturally take more room than short primers.",
            "Use the planned block durations as a session structure guide, while the prescription stays as the technical coaching instruction.",
            "Keep quality high: stop technical drills when execution clearly drops.",
            "Record key outputs like sprint times, shot quality, serve percentage, split times, or RPE after the session.",
            "If pain appears and changes movement mechanics, reduce load and use the Physio section for a basic triage workflow.",
            "Use the equipment level as a realism filter: the session should feel professional but still possible in the athlete's environment.",
        ]
        if role == "Coach":
            reminders.append("For team sessions, adapt work:rest ratios so starters and reserves are both challenged appropriately.")
        for item in reminders:
            st.write(f"- {item}")

        with st.expander("Future API integration preview", expanded=False):
            st.json(future_payload)
            st.caption("This is only a preview of the structure prepared for future reasoning/API implementation.")
