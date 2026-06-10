import hashlib
import random
import re
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Callable, Dict, List, Optional, Tuple

import streamlit as st

try:
    from training_catalog import get_catalog_session
except Exception:
    get_catalog_session = None


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
# SPORTZE.AI EXPANDED SPORT CATALOG + SESSION LIBRARY
# Added from the two Sportze.AI PDFs:
# - 31 core sport templates with 10 normal sessions + 7 adapted gym sessions each
# - Sports 32-200 similarity map, so unknown / less common sports can borrow the
#   closest high-quality template instead of falling back to a generic plan.
# -----------------------------------------------------------------------------
CORE_SPORT_TEMPLATE_INFO: Dict[str, str] = {'American Football': 'explosive starts, acceleration, contact strength, position-specific power, repeat efforts',
 'Badminton': 'split-step speed, lunging strength, overhead power, repeated rally endurance, agility',
 'Baseball': 'rotational power, throwing velocity, sprint speed, hip-shoulder separation, shoulder care',
 'Basketball': 'vertical power, deceleration, lateral defense, finishing, repeated high-intensity efforts',
 'Boxing': 'footwork, rotational power, shoulder endurance, reaction, repeated high-intensity rounds',
 'Cricket': 'rotational power, sprint between wickets, throwing, shoulder resilience, batting reaction',
 'Cycling': 'leg endurance, cadence control, aerobic power, hip stability, repeat intervals',
 'Esports': 'reaction, focus, posture, hand/wrist durability, cognitive endurance',
 'Field Hockey': 'low body position, stick speed, acceleration, repeated sprints, change of direction',
 'Fitness Training': 'general fitness, mobility, full-body strength, conditioning',
 'Golf': 'rotational power, trunk stability, hip mobility, posture endurance, controlled speed',
 'Gymnastics': 'bodyweight strength, mobility, landing control, core tension, shoulder stability',
 'Handball': 'jump throw power, shoulder resilience, change of direction, contact balance, sprint repeats',
 'Ice Hockey': 'skating power, adductor strength, lateral speed, repeated shifts, trunk rotation',
 'Lacrosse': 'sprint speed, stick-handling under fatigue, rotational shooting power, agility',
 'MMA': 'hip mobility, grip strength, power endurance, level changes, trunk stiffness',
 'Netball': 'landing control, passing speed, short acceleration, court agility, repeat efforts',
 'Rowing': 'leg drive, posterior chain strength, aerobic power, rhythm, trunk endurance',
 'Rugby': 'collision tolerance, acceleration, repeated sprint ability, grip strength, total-body power',
 'Running': 'aerobic base, stride mechanics, elastic strength, threshold capacity, injury resilience',
 'Skateboarding': 'balance, landing tolerance, ankle control, reactive strength, rotational control',
 'Skiing': 'eccentric leg strength, edge control, trunk stiffness, balance, leg endurance',
 'Soccer': 'acceleration, repeated sprints, change of direction, first touch, finishing, aerobic base',
 'Softball': 'rotational hitting power, throwing durability, sprint starts, fielding reaction',
 'Squash': 'lunge endurance, court speed, racket control, repeated short bursts, hip mobility',
 'Surfing': 'paddle endurance, pop-up speed, balance, hip mobility, trunk rotation',
 'Swimming': 'pull strength, core control, shoulder endurance, kick power, aerobic capacity',
 'Table Tennis': 'reaction speed, footwork, trunk rotation, wrist/forearm control, repeated short bursts',
 'Tennis': 'serve power, first-step speed, lateral recovery, rotational strength, repeat point endurance',
 'Track & Field': 'speed mechanics, elastic power, event-specific endurance, rhythm, mobility',
 'Volleyball': 'jump power, landing control, shoulder durability, approach speed, reaction',
 'Water Polo': 'eggbeater strength, swim sprint repeats, shoulder durability, rotational throwing power, contact '
               'balance',
 'Weightlifting': 'maximal strength, bar speed, explosive strength, trunk bracing',
 'Wrestling': 'grip strength, neck/trunk strength, hip drive, anaerobic endurance, positional control'}

SPORTZE_NORMAL_SESSION_TEMPLATES: List[Tuple[str, str, List[Tuple[str, str]]]] = [('Technical Base Builder',
  'Build clean sport skills under low-to-medium fatigue.',
  [('Dynamic warm-up + movement prep', '8 min'),
   ('Skill pattern block: fundamentals at smooth speed', '4 x 4 min'),
   ('Main technical drill with decision cue', '5 x 3 min'),
   ('Conditioned small-game or rally block', '4 x 5 min'),
   ('Cooldown + mobility', '6 min')]),
 ('Speed and First-Step Session',
  'Improve acceleration, reaction, and first movement quality.',
  [('Warm-up: skips, mobility, build-ups', '10 min'),
   ('Reaction starts', '8 x 5-10 sec'),
   ('Short accelerations', '10 x 10-20 m'),
   ('Sport-specific chase/recovery drill', '6 x 20 sec'),
   ('Easy technical reps', '10 min')]),
 ('Agility and Change-of-Direction Session',
  'Train braking, re-acceleration, and body control.',
  [('Movement prep', '8 min'),
   ('Deceleration mechanics', '5 x 3 reps/side'),
   ('COD drill: planned angles', '6 x 20 sec'),
   ('Reactive agility drill', '8 x 15 sec'),
   ('Sport skill under COD fatigue', '4 x 4 min')]),
 ('Power Technique Session',
  'Transfer speed and force into sport skill.',
  [('Warm-up + activation', '10 min'),
   ('Explosive med-ball or jump prep', '5 x 3 reps'),
   ('High-quality sport power reps', '8 x 3 reps'),
   ('Power skill into live decision', '6 x 60 sec'),
   ('Mobility reset', '6 min')]),
 ('Endurance Skills Session',
  'Hold technique while fatigue rises.',
  [('Progressive warm-up', '8 min'),
   ('Tempo skill intervals', '6 x 3 min'),
   ('Sport-specific repeated efforts', '8 x 45 sec'),
   ('Technical recovery reps', '5 x 90 sec'),
   ('Breathing cooldown', '5 min')]),
 ('Small-Sided Competition Session',
  'Create game-like pressure with controlled volume.',
  [('Warm-up + ball/object feel', '8 min'),
   ('Rules-based mini-games', '5 x 4 min'),
   ('Constraint challenge', '4 x 3 min'),
   ('Score-pressure finisher', '6 x 45 sec'),
   ('Cooldown', '5 min')]),
 ('Reaction and Decision Session',
  'Improve perception, timing, and choices.',
  [('Warm-up with visual cue', '8 min'),
   ('Partner reaction drill', '8 x 20 sec'),
   ('Decision-tree technical reps', '6 x 2 min'),
   ('Live cue game', '5 x 3 min'),
   ('Review: 3 key decisions', '3 min')]),
 ('Strength-Endurance Sport Session',
  'Repeat sport actions without losing posture.',
  [('Warm-up', '8 min'),
   ('Bodyweight strength circuit', '3 rounds'),
   ('Sport technique circuit', '4 rounds x 5 min'),
   ('Fatigue skill test', '5 x 60 sec'),
   ('Mobility', '6 min')]),
 ('Match Simulation Session',
  'Prepare for realistic competition rhythm.',
  [('Warm-up routine', '10 min'),
   ('Phase 1: controlled tempo', '8 min'),
   ('Phase 2: high-pressure scenarios', '6 x 2 min'),
   ('Phase 3: final-score simulation', '8 min'),
   ('Cooldown and notes', '5 min')]),
 ('Recovery Skill Session',
  'Keep quality high while reducing load.',
  [('Easy warm-up', '6 min'),
   ('Mobility + tissue prep', '8 min'),
   ('Low-intensity technical reps', '20 min'),
   ('Coordination game', '10 min'),
   ('Cooldown breathing', '5 min')])]

SPORTZE_GYM_SESSION_TEMPLATES: List[Tuple[str, List[Tuple[str, str]]]] = [('Gym Session 1 - Lower-Body Power',
  [('Trap-bar jump or jump squat', '4 x 3'),
   ('Front squat', '4 x 5'),
   ('Split squat', '3 x 6/side'),
   ('Calf/ankle stiffness hops', '3 x 20 sec'),
   ('Core anti-rotation press', '3 x 10/side')]),
 ('Gym Session 2 - Upper-Body Power and Shoulder Care',
  [('Med-ball rotational throw', '5 x 4/side'),
   ('Pull-up or pulldown', '4 x 6-8'),
   ('Landmine press', '3 x 6/side'),
   ('Cable row', '3 x 10'),
   ('External rotation + scap push-up', '3 x 12 each')]),
 ('Gym Session 3 - Acceleration and Strength',
  [('Sled push or resisted sprint', '6 x 10-15 m'),
   ('Deadlift variation', '4 x 4'),
   ('Step-up', '3 x 6/side'),
   ('Hamstring curl or Nordic regression', '3 x 6-8'),
   ('Farmer carry', '4 x 25 m')]),
 ('Gym Session 4 - Agility, Braking, and Core',
  [('Lateral bounds', '4 x 5/side'),
   ('Copenhagen plank', '3 x 20 sec/side'),
   ('Lateral lunge', '3 x 8/side'),
   ('Pallof walkout', '3 x 6/side'),
   ('Landing mechanics', '5 x 3 reps')]),
 ('Gym Session 5 - Hypertrophy and Durability',
  [('Goblet squat', '3 x 10'),
   ('DB bench press', '3 x 8-10'),
   ('Single-arm row', '3 x 10/side'),
   ('Romanian deadlift', '3 x 8'),
   ('Loaded carry', '3 x 30 m')]),
 ('Gym Session 6 - Conditioning Circuit',
  [('Bike/row/ski erg interval', '8 x 30 sec hard / 60 sec easy'),
   ('Kettlebell swing', '4 x 12'),
   ('Push-up', '4 x 10-15'),
   ('Walking lunge', '4 x 12/side'),
   ('Dead bug', '3 x 10/side')]),
 ('Gym Session 7 - Mobility, Prehab, and Recovery Strength',
  [('Hip mobility flow', '8 min'),
   ('Thoracic rotation', '3 x 8/side'),
   ('Tempo split squat', '3 x 8/side'),
   ('Face pull', '3 x 15'),
   ('Breathing reset', '5 min')])]

SPORT_SIMILARITY_MAP: Dict[str, Dict[str, str]] = {
    'Netball': {'template': 'Basketball', 'why': 'court spacing, pivots, jumping, passing lanes', 'adaptation': 'basketball court movement + volleyball-style landing control'},
    'Futsal': {'template': 'Soccer', 'why': 'small-sided football, repeated accelerations', 'adaptation': 'soccer plan with tighter spaces and more change-of-direction'},
    'Beach Soccer': {'template': 'Soccer', 'why': 'football skills on unstable sand', 'adaptation': 'soccer plan with sand endurance and ankle/calf load'},
    'Beach Volleyball': {'template': 'Volleyball', 'why': 'same net rules, lower player count, sand movement', 'adaptation': 'volleyball plan with sand power and shoulder endurance'},
    'Padel': {'template': 'Tennis', 'why': 'racket sport, short sprints, volleys, walls', 'adaptation': 'tennis plan with more reactive footwork and trunk rotation'},
    'Squash': {'template': 'Tennis', 'why': 'racket skill, repeated lunges, tight court', 'adaptation': 'tennis plan with higher repeated-sprint density'},
    'Racquetball': {'template': 'Tennis', 'why': 'racket striking, wall rebound, accelerations', 'adaptation': 'tennis plan with wall-reaction and shoulder care'},
    'Pickleball': {'template': 'Tennis', 'why': 'racket/net court with lower running volume', 'adaptation': 'tennis plan with quicker hands and deceleration'},
    'Lacrosse': {'template': 'Field Hockey', 'why': 'stick handling, dodging, team invasion patterns', 'adaptation': 'field hockey plan with more contact and upper-body power'},
    'Floorball': {'template': 'Field Hockey', 'why': 'stick-and-ball, fast indoor transitions', 'adaptation': 'field hockey plan with indoor sprint repeats'},
    'Bandy': {'template': 'Ice Hockey', 'why': 'stick/puck-ball on ice, endurance skating', 'adaptation': 'ice hockey plan with longer aerobic skating blocks'},
    'Ringette': {'template': 'Ice Hockey', 'why': 'ice skating, team invasion, quick passing', 'adaptation': 'ice hockey plan with passing speed and skating agility'},
    'Inline Hockey': {'template': 'Ice Hockey', 'why': 'hockey pattern without ice surface', 'adaptation': 'ice hockey plan adapted to roller mechanics'},
    'Roller Hockey': {'template': 'Field Hockey', 'why': 'stick sport on wheels, agility and passing', 'adaptation': 'field hockey plan with skating/roller conditioning'},
    'Australian Rules Football': {'template': 'Rugby', 'why': 'contact, kicking, repeated running, aerial contests', 'adaptation': 'rugby plan with longer running and jump-catch work'},
    'Gaelic Football': {'template': 'Rugby', 'why': 'contact running, kicking, catching, transitions', 'adaptation': 'rugby-like plan with soccer kicking and repeated carries'},
    'Hurling': {'template': 'Field Hockey', 'why': 'stick-ball, sprinting, striking, aerial skill', 'adaptation': 'field hockey plan with more overhead striking power'},
    'Camogie': {'template': 'Field Hockey', 'why': 'hurling-style stick-ball demands', 'adaptation': 'field hockey plan with overhead striking and sprinting'},
    'Rugby League': {'template': 'Rugby', 'why': 'contact collision, repeated defensive lines', 'adaptation': 'rugby plan with shorter high-intensity intervals'},
    'Rugby Sevens': {'template': 'Rugby', 'why': 'open-field sprinting and contact', 'adaptation': 'rugby plan with more speed endurance'},
    'Touch Rugby': {'template': 'Rugby', 'why': 'rugby spacing without tackling', 'adaptation': 'rugby plan with agility and aerobic speed'},
    'Flag Football': {'template': 'American Football', 'why': 'routes, acceleration, evasive running', 'adaptation': 'American football plan with less contact and more agility'},
    'Ultimate Frisbee': {'template': 'Soccer', 'why': 'field invasion, repeated running, cutting', 'adaptation': 'soccer plan with shoulder throwing and jump timing'},
    'Handball Beach': {'template': 'Handball', 'why': 'same throwing patterns, sand movement', 'adaptation': 'handball plan with sand power and landing work'},
    'Dodgeball': {'template': 'Handball', 'why': 'throwing power, agility, reaction', 'adaptation': 'handball plan with more evasive agility'},
    'Sepak Takraw': {'template': 'Volleyball', 'why': 'net sport, acrobatic kicking, jumping', 'adaptation': 'volleyball plan with mobility and hip power'},
    'Footvolley': {'template': 'Volleyball', 'why': 'net sport with soccer touches on sand', 'adaptation': 'volleyball plan with soccer coordination and sand work'},
    'Bossaball': {'template': 'Volleyball', 'why': 'volleyball with acrobatics/trampoline', 'adaptation': 'volleyball plan with gymnastics landing and core control'},
    'Kabaddi': {'template': 'Rugby', 'why': 'contact, wrestling strength, repeated raids', 'adaptation': 'rugby plan with wrestling strength and breath-control intervals'},
    'Kho Kho': {'template': 'Running', 'why': 'tag, chasing, turning, speed endurance', 'adaptation': 'running plan with agility, acceleration and reactive turns'},
    'Softball': {'template': 'Baseball', 'why': 'bat-and-ball, throwing, sprint starts', 'adaptation': 'baseball plan with slightly higher fielding volume'},
    'Rounders': {'template': 'Baseball', 'why': 'bat-and-ball, bases, fielding', 'adaptation': 'baseball plan with simple sprint/throw emphasis'},
    'Kickball': {'template': 'Baseball', 'why': 'base-running game with kicking', 'adaptation': 'baseball plan with soccer-style kicking and sprinting'},
    'Pesapallo': {'template': 'Baseball', 'why': 'bat-and-ball with sprinting and throwing', 'adaptation': 'baseball plan with more acceleration and directional running'},
    'Tee-ball': {'template': 'Baseball', 'why': 'introductory bat-and-ball mechanics', 'adaptation': 'baseball beginner plan with basic coordination'},
    'Wiffle Ball': {'template': 'Baseball', 'why': 'bat-and-ball hitting/fielding in small space', 'adaptation': 'baseball plan with lighter throwing load'},
    'Curling': {'template': 'Golf', 'why': 'precision, balance, tactical shot execution', 'adaptation': 'golf-like precision plan with mobility and low-intensity conditioning'},
    'Bowling': {'template': 'Golf', 'why': 'precision skill, repeatable mechanics', 'adaptation': 'golf plan with shoulder/core stability and unilateral balance'},
    'Ten-pin Bowling': {'template': 'Golf', 'why': 'repeatable precision release', 'adaptation': 'golf plan with wrist/shoulder durability'},
    'Bocce': {'template': 'Golf', 'why': 'precision target sport', 'adaptation': 'golf plan with balance, coordination, light strength'},
    'Petanque': {'template': 'Golf', 'why': 'precision throwing and posture', 'adaptation': 'golf plan with shoulder mobility and trunk control'},
    'Darts': {'template': 'Golf', 'why': 'fine motor precision under pressure', 'adaptation': 'golf plan reduced to posture, core, shoulder endurance'},
    'Billiards / Pool': {'template': 'Golf', 'why': 'precision, stance, concentration', 'adaptation': 'golf plan reduced to mobility and posture endurance'},
    'Snooker': {'template': 'Golf', 'why': 'precision, stance, calm execution', 'adaptation': 'golf plan with low fatigue and mental routine'},
    'Archery': {'template': 'Golf', 'why': 'precision, posture, shoulder stability', 'adaptation': 'golf-like precision plan with scapular endurance'},
    'Shooting Sport': {'template': 'Golf', 'why': 'precision, breath control, postural stability', 'adaptation': 'golf-like plan with isometrics and breathing control'},
    'Equestrian Jumping': {'template': 'Gymnastics', 'why': 'balance, rhythm, core control', 'adaptation': 'gymnastics plan with lower-body stability and posture'},
    'Dressage': {'template': 'Gymnastics', 'why': 'posture, control, balance, rhythm', 'adaptation': 'gymnastics plan with core, hip mobility, isometrics'},
    'Rodeo': {'template': 'Rugby', 'why': 'contact resilience, grip, trunk control', 'adaptation': 'rugby plan with grip, core, neck and hip durability'},
    'Polo': {'template': 'Field Hockey', 'why': 'stick striking, team tactics, rotation', 'adaptation': 'field hockey plan with posture and rotational power'},
    'Canoe Sprint': {'template': 'Rowing', 'why': 'paddle endurance and upper-body power', 'adaptation': 'rowing plan with unilateral trunk rotation'},
    'Kayaking': {'template': 'Rowing', 'why': 'paddle endurance, trunk rotation', 'adaptation': 'rowing plan with shoulder care and torso power'},
    'Canoe Slalom': {'template': 'Rowing', 'why': 'paddle power plus agility/control', 'adaptation': 'rowing plan with reactive core and balance'},
    'Dragon Boat': {'template': 'Rowing', 'why': 'team paddling rhythm, high repeat power', 'adaptation': 'rowing plan with synchronized power endurance'},
    'Sailing': {'template': 'Rowing', 'why': 'core, grip, balance, endurance', 'adaptation': 'rowing plan with balance and isometric strength'},
    'Windsurfing': {'template': 'Surfing', 'why': 'board balance, wind control, core endurance', 'adaptation': 'surfing plan with grip and shoulder endurance'},
    'Kitesurfing': {'template': 'Surfing', 'why': 'board balance, pulling force, core', 'adaptation': 'surfing plan with more grip and anti-rotation'},
    'Wakeboarding': {'template': 'Snowboarding', 'why': 'board stance, balance, pulling force', 'adaptation': 'snowboarding plan with water-start and grip strength'},
    'Waterskiing': {'template': 'Skiing', 'why': 'ski stance, rope pull, balance', 'adaptation': 'skiing plan with grip and posterior-chain strength'},
    'Diving': {'template': 'Gymnastics', 'why': 'aerial control, takeoff, mobility', 'adaptation': 'gymnastics plan with landing mechanics and shoulder mobility'},
    'Artistic Swimming': {'template': 'Swimming', 'why': 'aquatic endurance, flexibility, core', 'adaptation': 'swimming plan with gymnastics mobility and breath control'},
    'Open Water Swimming': {'template': 'Swimming', 'why': 'aerobic endurance, pacing, shoulder durability', 'adaptation': 'swimming plan with longer continuous endurance'},
    'Lifesaving Sport': {'template': 'Swimming', 'why': 'swim speed, rescue carries, mixed endurance', 'adaptation': 'swimming plan with loaded carries and beach sprinting'},
    'Triathlon': {'template': 'Running', 'why': 'endurance base with swim/bike/run', 'adaptation': 'running plan with cycling and swimming cross-training'},
    'Duathlon': {'template': 'Running', 'why': 'run-bike-run endurance', 'adaptation': 'running plan with cycling bricks'},
    'Aquathlon': {'template': 'Swimming', 'why': 'swim-run transitions', 'adaptation': 'swimming plan with running intervals'},
    'Race Walking': {'template': 'Running', 'why': 'endurance gait under technical rules', 'adaptation': 'running plan with lower impact and hip endurance'},
    'Trail Running': {'template': 'Running', 'why': 'running with terrain, climbs, stability', 'adaptation': 'running plan with hill strength and ankle stability'},
    'Cross Country Running': {'template': 'Running', 'why': 'running endurance and uneven terrain', 'adaptation': 'running plan with aerobic intervals and hills'},
    'Marathon': {'template': 'Running', 'why': 'long aerobic endurance', 'adaptation': 'running plan with longer steady volume'},
    'Sprint Running': {'template': 'Track & Field', 'why': 'max velocity, power, starts', 'adaptation': 'track plan with acceleration and strength-power'},
    'Hurdles': {'template': 'Track & Field', 'why': 'sprinting plus rhythm and mobility', 'adaptation': 'track plan with plyometrics and hip mobility'},
    'Long Jump': {'template': 'Track & Field', 'why': 'sprint approach and explosive takeoff', 'adaptation': 'track plan with jump power and landing mechanics'},
    'High Jump': {'template': 'Track & Field', 'why': 'jump power, curve approach, mobility', 'adaptation': 'track plan with plyos and core control'},
    'Pole Vault': {'template': 'Gymnastics', 'why': 'sprint, plant, aerial body control', 'adaptation': 'gymnastics/track hybrid with upper-body power'},
    'Javelin': {'template': 'Track & Field', 'why': 'throwing power and runway speed', 'adaptation': 'track plan with shoulder care and rotational power'},
    'Shot Put': {'template': 'Weightlifting', 'why': 'explosive strength and power transfer', 'adaptation': 'weightlifting plan with throws and trunk power'},
    'Discus': {'template': 'Track & Field', 'why': 'rotational throwing power', 'adaptation': 'track plan with rotational strength'},
    'Hammer Throw': {'template': 'Weightlifting', 'why': 'rotational power and heavy strength', 'adaptation': 'weightlifting plan with rotation and grip'},
    'Powerlifting': {'template': 'Weightlifting', 'why': 'max strength squat/bench/deadlift', 'adaptation': 'weightlifting plan focused on maximal strength'},
    'Olympic Weightlifting': {'template': 'Weightlifting', 'why': 'snatch/clean/jerk power', 'adaptation': 'weightlifting plan with speed-strength technique'},
    'Strongman': {'template': 'Weightlifting', 'why': 'loaded carries, heavy odd objects', 'adaptation': 'weightlifting plan with grip and conditioning'},
    'CrossFit': {'template': 'Weightlifting', 'why': 'mixed strength and conditioning', 'adaptation': 'weightlifting plan with more metabolic circuits'},
    'Calisthenics': {'template': 'Gymnastics', 'why': 'bodyweight strength and control', 'adaptation': 'gymnastics plan with progressive bodyweight strength'},
    'Parkour': {'template': 'Gymnastics', 'why': 'jumping, landing, vaulting, agility', 'adaptation': 'gymnastics plan with movement skill and landing durability'},
    'Trampoline': {'template': 'Gymnastics', 'why': 'aerial rhythm and landing control', 'adaptation': 'gymnastics plan with plyometrics and body control'},
    'Cheerleading': {'template': 'Gymnastics', 'why': 'stunts, jumps, tumbling, teamwork', 'adaptation': 'gymnastics plan with partner stability and power'},
    'DanceSport': {'template': 'Gymnastics', 'why': 'rhythm, agility, posture, endurance', 'adaptation': 'gymnastics plan with footwork and mobility'},
    'Breakdancing': {'template': 'Gymnastics', 'why': 'floor power, mobility, rhythm', 'adaptation': 'gymnastics plan with upper-body strength and hip mobility'},
    'Climbing': {'template': 'Gymnastics', 'why': 'grip strength, body tension, pulling', 'adaptation': 'gymnastics plan with pulling and forearm endurance'},
    'Bouldering': {'template': 'Gymnastics', 'why': 'explosive grip and body control', 'adaptation': 'gymnastics plan with power grip and mobility'},
    'Mountaineering': {'template': 'Skiing', 'why': 'endurance, load carriage, altitude tolerance', 'adaptation': 'skiing plan with hiking endurance and strength'},
    'Orienteering': {'template': 'Running', 'why': 'running plus navigation under fatigue', 'adaptation': 'running plan with intervals and decision-making'},
    'Adventure Racing': {'template': 'Running', 'why': 'multi-discipline endurance and navigation', 'adaptation': 'running plan with mixed endurance circuits'},
    'Biathlon': {'template': 'Skiing', 'why': 'ski endurance plus shooting calm', 'adaptation': 'skiing plan with breath-control precision'},
    'Cross-country Skiing': {'template': 'Skiing', 'why': 'high aerobic endurance and poles', 'adaptation': 'skiing plan with long intervals'},
    'Alpine Skiing': {'template': 'Skiing', 'why': 'leg power, edges, eccentric control', 'adaptation': 'skiing plan with power and knee stability'},
    'Freestyle Skiing': {'template': 'Skiing', 'why': 'skiing with aerial/park skills', 'adaptation': 'skiing plan with gymnastics landing control'},
    'Ski Jumping': {'template': 'Skiing', 'why': 'takeoff power and aerial control', 'adaptation': 'skiing plan with plyometrics and landing'},
    'Nordic Combined': {'template': 'Skiing', 'why': 'ski jump plus cross-country endurance', 'adaptation': 'skiing plan with power plus aerobic volume'},
    'Speed Skating': {'template': 'Ice Hockey', 'why': 'skating power, speed endurance', 'adaptation': 'ice hockey plan with more straight-line speed'},
    'Figure Skating': {'template': 'Gymnastics', 'why': 'aerial control, edges, balance', 'adaptation': 'gymnastics plan with skating-specific strength'},
    'Short Track Speed Skating': {'template': 'Ice Hockey', 'why': 'ice sprinting, turns, contact risk', 'adaptation': 'ice hockey plan with cornering and repeated sprints'},
    'Inline Speed Skating': {'template': 'Cycling', 'why': 'cyclical leg power and speed endurance', 'adaptation': 'cycling plan with skating mechanics'},
    'BMX Racing': {'template': 'Cycling', 'why': 'bike sprints, jumps, power', 'adaptation': 'cycling plan with explosive starts and landing'},
    'BMX Freestyle': {'template': 'Skateboarding', 'why': 'tricks, balance, aerial control', 'adaptation': 'skateboarding plan with bike-specific strength'},
    'Mountain Biking': {'template': 'Cycling', 'why': 'bike endurance, terrain control', 'adaptation': 'cycling plan with upper-body stability'},
    'Road Cycling': {'template': 'Cycling', 'why': 'aerobic endurance and pacing', 'adaptation': 'cycling plan with long steady intervals'},
    'Track Cycling': {'template': 'Cycling', 'why': 'sprint power or sustained pace', 'adaptation': 'cycling plan with velodrome power intervals'},
    'Cyclocross': {'template': 'Cycling', 'why': 'bike handling, running carries, mud', 'adaptation': 'cycling plan with repeated dismount intervals'},
    'Motocross': {'template': 'Cycling', 'why': 'riding endurance, grip, impact tolerance', 'adaptation': 'cycling-like plan with more grip/neck/core strength'},
    'Skateboard Vert': {'template': 'Skateboarding', 'why': 'board balance, aerial tricks', 'adaptation': 'skateboarding plan with landing and hip mobility'},
    'Scootering': {'template': 'Skateboarding', 'why': 'park tricks, jumps, landings', 'adaptation': 'skateboarding plan with handlebar grip and landings'},
    'Roller Derby': {'template': 'Ice Hockey', 'why': 'skating, contact, team tactics', 'adaptation': 'ice hockey plan with roller and contact conditioning'},
    'Speed Climbing': {'template': 'Gymnastics', 'why': 'explosive vertical sprint and grip', 'adaptation': 'gymnastics plan with speed-power pulls'},
    'Sumo': {'template': 'Wrestling', 'why': 'grappling force, balance, pushing', 'adaptation': 'wrestling plan with heavy lower-body strength'},
    'Judo': {'template': 'Martial Arts', 'why': 'throws, grip fighting, falls', 'adaptation': 'martial arts plan with wrestling and landing skills'},
    'Brazilian Jiu-Jitsu': {'template': 'Martial Arts', 'why': 'ground grappling, isometric strength', 'adaptation': 'martial arts plan with wrestling endurance'},
    'Sambo': {'template': 'Martial Arts', 'why': 'judo/wrestling hybrid', 'adaptation': 'martial arts plan with throws and grappling strength'},
    'Aikido': {'template': 'Martial Arts', 'why': 'movement, balance, joint control', 'adaptation': 'martial arts plan with mobility and control'},
    'Karate': {'template': 'Martial Arts', 'why': 'striking speed, footwork, reaction', 'adaptation': 'martial arts plan with explosive striking intervals'},
    'Taekwondo': {'template': 'Martial Arts', 'why': 'kicking speed, mobility, reaction', 'adaptation': 'martial arts plan with hip mobility and kick power'},
    'Muay Thai': {'template': 'MMA', 'why': 'striking, clinch, conditioning', 'adaptation': 'MMA plan with striking volume and shin/hip durability'},
    'Kickboxing': {'template': 'Boxing', 'why': 'boxing plus kicks and footwork', 'adaptation': 'boxing plan with lower-body kick power'},
    'Savate': {'template': 'Kickboxing', 'why': 'boxing/kicking with footwork', 'adaptation': 'boxing plan with kick mobility and agility'},
    'Fencing': {'template': 'Martial Arts', 'why': 'combat footwork, reaction, lunges', 'adaptation': 'martial arts plan with lunge speed and precision'},
    'Kendo': {'template': 'Martial Arts', 'why': 'weapon striking, footwork, reaction', 'adaptation': 'martial arts plan with shoulder endurance'},
    'Wushu': {'template': 'Martial Arts', 'why': 'forms, kicks, acrobatics', 'adaptation': 'martial arts plan with gymnastics mobility'},
    'Capoeira': {'template': 'Martial Arts', 'why': 'kicks, rhythm, acrobatics', 'adaptation': 'martial arts plan with gymnastics and mobility'},
    'Lethwei': {'template': 'MMA', 'why': 'full-contact striking and clinch', 'adaptation': 'MMA plan with striking and neck/core work'},
    'Greco-Roman Wrestling': {'template': 'Wrestling', 'why': 'upper-body throws and clinch control', 'adaptation': 'wrestling plan with trunk and grip emphasis'},
    'Freestyle Wrestling': {'template': 'Wrestling', 'why': 'takedowns, scrambles, mat control', 'adaptation': 'wrestling plan with repeated shots and sprawls'},
    'Arm Wrestling': {'template': 'Wrestling', 'why': 'grip, wrist, elbow force', 'adaptation': 'wrestling plan reduced to grip/forearm strength'},
    'Tug of War': {'template': 'Rowing', 'why': 'team pulling force and grip endurance', 'adaptation': 'rowing plan with maximal pulls and coordination'},
    'Bodybuilding': {'template': 'Weightlifting', 'why': 'hypertrophy and muscle isolation', 'adaptation': 'weightlifting plan with bodybuilding volume'},
    'Fitness Training': {'template': 'Weightlifting', 'why': 'general strength and conditioning', 'adaptation': 'weightlifting plan with balanced full-body work'},
    'Aerobics': {'template': 'Running', 'why': 'rhythmic cardio endurance', 'adaptation': 'running plan with low-impact circuits'},
    'Pilates': {'template': 'Gymnastics', 'why': 'core control, mobility, posture', 'adaptation': 'gymnastics plan reduced to core and alignment'},
    'Yoga Sport': {'template': 'Gymnastics', 'why': 'mobility, balance, isometric control', 'adaptation': 'gymnastics plan with mobility and breath control'},
    'Rowing Indoor / Erg': {'template': 'Rowing', 'why': 'same pattern without boat balance', 'adaptation': 'rowing plan with erg intervals'},
    'Coastal Rowing': {'template': 'Rowing', 'why': 'rowing with waves and beach starts', 'adaptation': 'rowing plan with stability and beach sprinting'},
    'Canoe Polo': {'template': 'Water Polo', 'why': 'water invasion game plus paddling', 'adaptation': 'water polo plan with kayak/paddle upper-body load'},
    'Underwater Hockey': {'template': 'Water Polo', 'why': 'aquatic invasion, breath control, puck skill', 'adaptation': 'water polo plan with apnea and fin work'},
    'Underwater Rugby': {'template': 'Water Polo', 'why': 'aquatic contact and breath control', 'adaptation': 'water polo plan with more wrestling strength'},
    'Finswimming': {'template': 'Swimming', 'why': 'swim speed with fins and dolphin kick', 'adaptation': 'swimming plan with core and ankle mobility'},
    'Freediving': {'template': 'Swimming', 'why': 'breath control and water efficiency', 'adaptation': 'swimming plan reduced to safety-first apnea conditioning'},
    'Water Ski Racing': {'template': 'Skiing', 'why': 'ski stance, water speed, grip', 'adaptation': 'skiing plan with grip and core bracing'},
    'Rafting': {'template': 'Rowing', 'why': 'team paddling, trunk endurance', 'adaptation': 'rowing plan with reactive core'},
    'Stand-up Paddleboarding': {'template': 'Rowing', 'why': 'paddling plus balance', 'adaptation': 'rowing plan with unilateral balance and trunk rotation'},
    'Dragon Surf Ski': {'template': 'Rowing', 'why': 'paddle endurance on open water', 'adaptation': 'rowing plan with ocean stability'},
    'Bodyboarding': {'template': 'Surfing', 'why': 'wave timing, paddling, core', 'adaptation': 'surfing plan with prone paddling and hip mobility'},
    'Skimboarding': {'template': 'Surfing', 'why': 'beach sprint, board balance', 'adaptation': 'surfing plan with sprint starts and landings'},
    'Longboarding Surf': {'template': 'Surfing', 'why': 'board balance, wave control', 'adaptation': 'surfing plan with low-stance endurance'},
    'Snowshoe Running': {'template': 'Running', 'why': 'endurance on snow resistance', 'adaptation': 'running plan with hip flexor and calf endurance'},
    'Sled Hockey': {'template': 'Ice Hockey', 'why': 'upper-body propulsion on ice', 'adaptation': 'ice hockey plan adapted to upper-body power'},
    'Luge': {'template': 'Skiing', 'why': 'high-speed sled, neck/core isometrics', 'adaptation': 'skiing plan reduced to neck/core and reaction'},
    'Skeleton': {'template': 'Skiing', 'why': 'sprint start plus sled control', 'adaptation': 'skiing plan with start sprint and neck strength'},
    'Bobsleigh': {'template': 'Track & Field', 'why': 'explosive push start and speed', 'adaptation': 'track plan with sprint/power emphasis'},
    'Dog Agility': {'template': 'Running', 'why': 'handler sprinting and reaction', 'adaptation': 'running plan with agility and commands'},
    'Disc Golf': {'template': 'Golf', 'why': 'throwing precision and walking', 'adaptation': 'golf plan with rotational throwing mobility'},
    'Teqball': {'template': 'Soccer', 'why': 'soccer touches on curved table', 'adaptation': 'soccer plan with coordination and mobility'},
    'Footgolf': {'template': 'Golf', 'why': 'golf course strategy with football kicking', 'adaptation': 'golf plan with soccer kicking mechanics'},
    'Chess Boxing': {'template': 'Boxing', 'why': 'boxing rounds plus cognitive recovery', 'adaptation': 'boxing plan with controlled intensity'},
    'E-Soccer / Football Gaming': {'template': 'Esports', 'why': 'gaming skill, football decision models', 'adaptation': 'esports plan with posture + soccer tactical awareness'},
    'Sim Racing': {'template': 'Esports', 'why': 'reaction, focus, neck/forearm endurance', 'adaptation': 'esports plan with neck, grip, posture endurance'},
    'Drone Racing': {'template': 'Esports', 'why': 'reaction, fine motor, visual tracking', 'adaptation': 'esports plan with posture and reaction drills'},
    'Speedcubing': {'template': 'Esports', 'why': 'fine motor speed and focus', 'adaptation': 'esports plan with hand/wrist care'},
    'Mind Sports / Chess': {'template': 'Esports', 'why': 'cognitive endurance and focus', 'adaptation': 'esports plan with posture, mobility, recovery'},
    'Go': {'template': 'Esports', 'why': 'cognitive endurance and planning', 'adaptation': 'esports plan with posture and concentration blocks'},
}


SPORT_TEMPLATE_ALIASES: Dict[str, str] = {
    "football": "Soccer", "soccer": "Soccer", "futebol": "Soccer", "futbol": "Soccer",
    "aussie rules": "Rugby", "australian rules": "Rugby",
    "polo aquatico": "Water Polo", "polo aquático": "Water Polo", "waterpolo": "Water Polo",
    "track": "Track & Field", "athletics": "Track & Field", "track and field": "Track & Field",
    "mma": "MMA", "mixed martial arts": "MMA", "martial arts": "MMA",
    "gym": "Gym", "fitness": "Gym", "academia": "Gym", "musculacao": "Gym", "musculação": "Gym",
    "bodybuilding": "Weightlifting", "weight training": "Gym", "lifting": "Weightlifting",
    "gaming": "Esports", "e sports": "Esports", "esport": "Esports", "esports": "Esports",
}

TEAM_TEMPLATE_SPORTS = {
    "Soccer", "Cricket", "Basketball", "Field Hockey", "Volleyball", "Baseball", "Rugby", "American Football",
    "Ice Hockey", "Handball", "Netball", "Lacrosse", "Softball", "Water Polo"
}

INDIVIDUAL_TEMPLATE_SPORTS = set(CORE_SPORT_TEMPLATE_INFO.keys()) - TEAM_TEMPLATE_SPORTS - {"Gym"}


def _session_focus_from_emphasis(emphasis: str, fallback: str = "Technical Quality") -> str:
    text = canonical_compact(emphasis)
    if any(x in text for x in ["speed", "sprint", "acceleration"]):
        return "Speed"
    if any(x in text for x in ["power", "jump", "throw", "explosive"]):
        return "Power"
    if any(x in text for x in ["endurance", "aerobic", "conditioning", "stamina"]):
        return "Conditioning"
    if any(x in text for x in ["strength", "grip", "posterior", "collision"]):
        return "Strength"
    return fallback


def _parse_template_sets_reps(prescription: str) -> str:
    # Keep original PDF prescription, but make it generator-friendly.
    return str(prescription).replace("x", "x").strip()


def make_core_sport_library(sport_name: str, emphasis: str) -> Dict[str, List[Exercise]]:
    """Builds a reusable library from the PDF session templates.
    Each core sport receives the 10 normal sport templates converted into category blocks.
    """
    focus = _session_focus_from_emphasis(emphasis)
    library = {"Warm-Up": [], "Technical": [], "Physical": [], "Tactical": [], "Recovery": []}
    for idx, (session_title, purpose, blocks) in enumerate(SPORTZE_NORMAL_SESSION_TEMPLATES, start=1):
        for block_name, prescription in blocks:
            lower = canonical_compact(block_name)
            if "warm" in lower or "prep" in lower:
                category = "Warm-Up"
            elif "cool" in lower or "breath" in lower or "mobility" in lower or "review" in lower:
                category = "Recovery"
            elif any(word in lower for word in ["game", "simulation", "decision", "scenario", "live", "score", "rules", "constraint"]):
                category = "Tactical"
            elif any(word in lower for word in ["sprint", "acceleration", "agility", "cod", "strength", "circuit", "interval", "power", "bodyweight", "reaction"]):
                category = "Physical"
            else:
                category = "Technical"
            library[category].append(
                Exercise(
                    name=f"{sport_name} - {session_title}: {block_name}",
                    category=category,
                    prescription=_parse_template_sets_reps(prescription),
                    purpose=f"{purpose} Sport emphasis: {emphasis}.",
                    equipment_tags=["Sport equipment if available", "Open space", "Cones"],
                    intensity_tags=["Low", "Moderate", "High"],
                    focus_tags=[focus, "Technical Quality", "Conditioning", "Match Rhythm"],
                    position_tags=["All"], level_tags=["All"], phase_tags=["All"],
                    time_weight=1.0 + (0.04 * (idx % 4)),
                    coaching_points=[
                        f"Keep the drill specific to {sport_name}: {emphasis}.",
                        "Quality comes before fatigue; stop the rep if mechanics break.",
                    ],
                )
            )
    return library


def make_sport_focused_gym_library(template_sport: str, emphasis: str) -> Dict[str, List[Exercise]]:
    """Uses the 7 adapted gym sessions from the PDF for sport-focused gym mode."""
    focus = _session_focus_from_emphasis(emphasis, "Strength")
    library = {"Warm-Up": [], "Technical": [], "Physical": [], "Tactical": [], "Recovery": []}
    library["Warm-Up"].append(Exercise(
        f"{template_sport} gym warm-up: mobility + activation", "Warm-Up", "6-10 minutes progressive prep",
        f"Prepare the body for a gym session that supports {template_sport}: {emphasis}.",
        ["Bodyweight", "Bands", "Open space"], ["Low"], ["Movement Quality", focus], ["All"], ["All"], ["All"], 1.0,
    ))
    library["Technical"].append(Exercise(
        f"{template_sport} gym technique ramp", "Technical", "2-3 lighter ramp sets before main work",
        "Practice positions and tempo before loading.",
        ["Bodyweight", "Dumbbells", "Barbell", "Machine"], ["Low", "Moderate"], ["Technical Quality", focus], ["All"], ["All"], ["All"], 0.8,
    ))
    for idx, (session_title, blocks) in enumerate(SPORTZE_GYM_SESSION_TEMPLATES, start=1):
        for movement, prescription in blocks:
            lower = canonical_compact(movement)
            category = "Recovery" if any(w in lower for w in ["breathing", "mobility", "rotation"] ) and idx == 7 else "Physical"
            library[category].append(Exercise(
                name=f"{template_sport} adapted gym - {session_title}: {movement}",
                category=category,
                prescription=prescription,
                purpose=f"Gym transfer for {template_sport}. Emphasis: {emphasis}.",
                equipment_tags=["Bodyweight", "Bands", "Dumbbells", "Barbell", "Machine", "Medicine ball"],
                intensity_tags=["Low", "Moderate", "High"],
                focus_tags=[focus, "Strength", "Power", "Conditioning", "Movement Quality"],
                position_tags=["All"], level_tags=["All"], phase_tags=["All"],
                time_weight=1.05,
                coaching_points=[
                    f"Use gym work to improve {template_sport} performance, not just random fatigue.",
                    "Keep reps fast and clean when the goal is athletic performance.",
                ],
            ))
    library["Recovery"].append(Exercise(
        f"{template_sport} cooldown and tissue reset", "Recovery", "5-8 minutes easy cooldown + mobility",
        "Reduce stiffness and finish ready for the next sport session.",
        ["Bodyweight"], ["Low"], ["Movement Quality"], ["All"], ["All"], ["All"], 0.75,
    ))
    return library


def resolve_sport_template(sport_text: str) -> Tuple[Optional[str], str, Optional[Dict[str, str]]]:
    """Returns: (template_sport, display_sport, similarity_info)."""
    raw = normalize_text(sport_text)
    compact = canonical_compact(raw)
    if not compact:
        return None, raw, None
    if compact in {canonical_compact(x) for x in GYM_ALIASES}:
        return "Gym", "Gym", None
    alias = SPORT_TEMPLATE_ALIASES.get(compact)
    if alias:
        return alias, raw or alias, None
    for sport_name in list(CORE_SPORT_TEMPLATE_INFO.keys()) + list(SPORT_LIBRARY.keys()) + list(SPORT_POSITIONS.keys()):
        if canonical_compact(sport_name) == compact:
            return sport_name, sport_name, None
    for mapped_sport, info in SPORT_SIMILARITY_MAP.items():
        if canonical_compact(mapped_sport) == compact:
            return info["template"], raw or mapped_sport, info
    # Soft matching for typos / partial names
    try:
        import difflib
        keys = [canonical_compact(s) for s in list(CORE_SPORT_TEMPLATE_INFO.keys()) + list(SPORT_SIMILARITY_MAP.keys()) + list(SPORT_TEMPLATE_ALIASES.keys())]
        close = difflib.get_close_matches(compact, keys, n=1, cutoff=0.78)
        if close:
            key = close[0]
            for sport_name in CORE_SPORT_TEMPLATE_INFO:
                if canonical_compact(sport_name) == key:
                    return sport_name, raw or sport_name, None
            for mapped_sport, info in SPORT_SIMILARITY_MAP.items():
                if canonical_compact(mapped_sport) == key:
                    return info["template"], raw or mapped_sport, info
            if key in SPORT_TEMPLATE_ALIASES:
                return SPORT_TEMPLATE_ALIASES[key], raw, None
    except Exception:
        pass
    # Intelligent unknown fallback: infer by movement words.
    if any(w in compact for w in ["gaelic", "contact", "tackle", "league", "union"]):
        return "Rugby", raw, {"template": "Rugby", "why": "contact field invasion sport", "adaptation": "rugby-like contact, sprint, and power session"}
    if any(w in compact for w in ["racket", "racquet", "paddle"]):
        return "Tennis", raw, {"template": "Tennis", "why": "racket/paddle reaction sport", "adaptation": "tennis-like footwork, rotation, and reaction session"}
    if any(w in compact for w in ["fight", "combat", "kick", "karate", "jitsu"]):
        return "MMA", raw, {"template": "MMA", "why": "combat sport movement profile", "adaptation": "martial-arts conditioning and mobility session"}
    if any(w in compact for w in ["swim", "water", "aquatic"]):
        return "Swimming", raw, {"template": "Swimming", "why": "aquatic endurance and shoulder demand", "adaptation": "swimming-like conditioning and shoulder care"}
    return "Soccer", raw, {"template": "Soccer", "why": "general field/court athletic fallback", "adaptation": "general agility, speed, technical-quality session"}


def expand_sportze_libraries() -> None:
    for sport_name, emphasis in CORE_SPORT_TEMPLATE_INFO.items():
        if sport_name == "Gym":
            continue
        if sport_name not in SPORT_LIBRARY:
            SPORT_LIBRARY[sport_name] = make_core_sport_library(sport_name, emphasis)
        if sport_name not in SPORT_DURATION_STYLE:
            SPORT_DURATION_STYLE[sport_name] = {"short": 6, "standard": 7, "long": 8}
        if sport_name not in SPORT_BLUEPRINTS:
            SPORT_BLUEPRINTS[sport_name] = DEFAULT_BLUEPRINTS
    # Precompute sport-focused gym libraries under virtual names.
    for sport_name, emphasis in CORE_SPORT_TEMPLATE_INFO.items():
        if sport_name == "Gym":
            continue
        SPORT_LIBRARY[f"Gym for {sport_name}"] = make_sport_focused_gym_library(sport_name, emphasis)


_SPORTZE_LIBRARIES_EXPANDED = False

def ensure_sportze_libraries_expanded() -> None:
    global _SPORTZE_LIBRARIES_EXPANDED
    if not _SPORTZE_LIBRARIES_EXPANDED:
        expand_sportze_libraries()
        _SPORTZE_LIBRARIES_EXPANDED = True


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
        "training_entry_mode": None,
        "description_mode_waiting": False,
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
    template, _, _ = resolve_sport_template(sport_text) if "resolve_sport_template" in globals() else (None, sport_text, None)
    if template == "Gym" or is_gym_sport(sport_text):
        return "Individual Sport"
    if template in TEAM_TEMPLATE_SPORTS or sport in {canonical_compact(x) for x in KNOWN_TEAM_SPORTS}:
        return "Team Sport"
    if template in INDIVIDUAL_TEMPLATE_SPORTS or sport in {canonical_compact(x) for x in KNOWN_INDIVIDUAL_SPORTS}:
        return "Individual Sport"
    return ""


def match_supported_sport(sport_text: str) -> Optional[str]:
    template, _, _ = resolve_sport_template(sport_text) if "resolve_sport_template" in globals() else (None, sport_text, None)
    return template


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


def is_competitive_level(level: object) -> bool:
    return str(level).strip() in {"Advanced", "Elite", "Experienced"}


def is_short_yes_answer(value: object) -> bool:
    return canonical_compact(str(value)) in {canonical_compact(x) for x in COMMON_BOOL_YES}


def is_short_no_answer(value: object) -> bool:
    return canonical_compact(str(value)) in {canonical_compact(x) for x in COMMON_BOOL_NO} | {"none", "nothing", "no notes", "n/a", "na"}


def get_question_flow(profile: Dict[str, str]) -> List[Dict[str, object]]:
    sport = profile.get("sport", "")
    sport_type = profile.get("sport_type", "") or detect_sport_type(sport)
    supported_sport = match_supported_sport(sport)
    gym_mode = bool(supported_sport == "Gym" or is_gym_sport(sport))
    level = str(profile.get("level", ""))
    competitive_level = is_competitive_level(level)

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
        flow.append({"key": "gym_sport_focus_flag", "prompt": "Do you want this gym session to be focused on another sport? Answer Yes or No.", "type": "bool"})
        if bool(profile.get("gym_sport_focus_flag", False)):
            flow.append({"key": "gym_focus_sport", "prompt": "Which sport should this gym session support?", "type": "text"})
        flow.extend([
            {"key": "goal", "prompt": "What is your main gym goal?", "type": "select", "options": GYM_GOALS},
            {"key": "level", "prompt": "What is your current gym level?", "type": "select", "options": GYM_LEVELS},
            {"key": "training_alone", "prompt": "Will you train alone? Answer Yes or No.", "type": "bool"},
        ])
        if profile.get("training_alone") is False:
            flow.append({"key": "training_partners_count", "prompt": "How many other people will train with you?", "type": "int", "min": 1, "max": 99})
        flow.extend([
            {"key": "weekly_target", "prompt": get_frequency_prompt(profile.get("goal", ""), profile.get("level", ""), sport), "type": "int", "min": 1, "max": 7},
            {"key": "session_type", "prompt": "What kind of gym session do you want today?", "type": "select", "options": GYM_SESSION_TYPES},
            {"key": "duration", "prompt": "How many minutes should this gym session last?", "type": "int", "min": 30, "max": 180},
            {"key": "equipment_level", "prompt": "What is your level of equipment available?", "type": "select", "options": EQUIPMENT_LEVELS},
            {"key": "pain_flag", "prompt": "Is there pain or discomfort today? Answer Yes or No.", "type": "bool"},
        ])
    else:
        flow.extend([
            {"key": "goal", "prompt": "What is your main goal?", "type": "select", "options": GOALS},
            {"key": "level", "prompt": "What is your current level?", "type": "select", "options": LEVELS},
            {"key": "training_alone", "prompt": "Will you train alone? Answer Yes or No.", "type": "bool"},
        ])
        if profile.get("training_alone") is False:
            flow.append({"key": "training_partners_count", "prompt": "How many other people will train with you?", "type": "int", "min": 1, "max": 99})
        flow.extend([
            {"key": "weekly_target", "prompt": get_frequency_prompt(profile.get("goal", ""), profile.get("level", ""), sport), "type": "int", "min": 1, "max": 7},
            {"key": "session_type", "prompt": "What kind of session do you want today?", "type": "select", "options": SESSION_TYPES},
            {"key": "duration", "prompt": "How many minutes should this session last?", "type": "int", "min": 30, "max": 180},
            {"key": "equipment_level", "prompt": "What is your level of equipment available?", "type": "select", "options": EQUIPMENT_LEVELS},
        ])
        if competitive_level:
            flow.append({"key": "season_phase", "prompt": "What season phase are you in?", "type": "select", "options": SEASON_PHASES})
        flow.append({"key": "pain_flag", "prompt": "Is there pain or discomfort today? Answer Yes or No.", "type": "bool"})

    if bool(profile.get("pain_flag", False)):
        flow.extend([
            {"key": "pain_location", "prompt": "Where does it hurt?", "type": "text"},
            {"key": "pain_scale", "prompt": "On a scale from 1 to 10, how much does it hurt?", "type": "int", "min": 1, "max": 10},
        ])

    flow.append({"key": "needs_low_impact", "prompt": "Do you prefer lower-impact loading today? Answer Yes or No.", "type": "bool"})

    if competitive_level and not gym_mode:
        flow.append({"key": "competition_soon", "prompt": "Do you have a competition or match in the next 3 days? Answer Yes or No.", "type": "bool"})

    flow.append({"key": "notes", "prompt": "Any extra notes?", "type": "text"})
    if bool(profile.get("notes_pending", False)):
        flow.append({"key": "notes_detail", "prompt": "What notes?", "type": "text"})

    if (not gym_mode) and competitive_level:
        insert_idx = 5 if sport_type == "Team Sport" else 4
        flow.insert(insert_idx, {"key": "is_professional", "prompt": "Are you professional in this sport? Answer Yes or No.", "type": "bool"})

    if should_ask_name:
        name_prompt = "What is your name?"
        insert_idx = 6 if sport_type == "Team Sport" else 5
        flow.insert(insert_idx, {"key": "athlete_name", "prompt": name_prompt, "type": "text"})

    cleaned_flow = []
    seen_keys = set()
    for q in flow:
        if q.get("key") == "sport_type" and q.get("skip_if_detected") and detect_sport_type(profile.get("sport", "")):
            continue
        if q.get("key") in seen_keys:
            continue
        seen_keys.add(q.get("key"))
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
    st.session_state.training_entry_mode = None
    st.session_state.description_mode_waiting = False


def start_training_chat(entry_mode: str = "guided") -> None:
    reset_training_chat()
    st.session_state.training_chat_started = True
    st.session_state.training_entry_mode = entry_mode
    if entry_mode == "describe":
        st.session_state.description_mode_waiting = True
        append_bot_message("Describe exactly what kind of training session you want: sport, focus, main goal, duration, equipment, level, pain notes, etc.")
        return
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
    if key == "notes":
        if is_short_no_answer(value):
            st.session_state.training_profile["notes"] = ""
            st.session_state.training_profile["notes_pending"] = False
            st.session_state.home_notes = ""
            return
        if is_short_yes_answer(value):
            st.session_state.training_profile["notes"] = ""
            st.session_state.training_profile["notes_pending"] = True
            return
        st.session_state.training_profile["notes"] = str(value).strip()
        st.session_state.training_profile["notes_pending"] = False
        st.session_state.home_notes = str(value).strip()
        return

    if key == "notes_detail":
        st.session_state.training_profile["notes"] = "" if is_short_no_answer(value) else str(value).strip()
        st.session_state.training_profile["notes_pending"] = False
        st.session_state.home_notes = st.session_state.training_profile["notes"]
        return

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
    if key == "sport_type":
        st.session_state.sport_type = value
    if key == "is_professional":
        st.session_state.is_professional = "Yes" if value else "No"
    if key == "pain_location":
        st.session_state.pain_location = value
    if key == "pain_scale":
        st.session_state.pain_scale = value
    if key == "gym_focus_sport":
        st.session_state.gym_focus_sport = value
    if key == "gym_sport_focus_flag":
        st.session_state.gym_sport_focus_flag = value
    if key == "training_alone":
        st.session_state.training_alone = value
    if key == "training_partners_count":
        st.session_state.training_partners_count = value


def parse_free_description_to_profile(description: str) -> Dict[str, object]:
    text = normalize_text(description)
    compact = canonical_compact(text)
    profile: Dict[str, object] = {"notes": text}

    # Sport detection: choose the first catalog sport/alias mentioned. Fallback uses resolver.
    detected_sport = ""
    sport_candidates = list(CORE_SPORT_TEMPLATE_INFO.keys()) + list(SPORT_SIMILARITY_MAP.keys()) + list(SPORT_TEMPLATE_ALIASES.keys())
    sport_candidates = sorted(sport_candidates, key=lambda s: len(str(s)), reverse=True)
    for candidate in sport_candidates:
        c = canonical_compact(candidate)
        if c and (f" {c} " in f" {compact} " or compact.startswith(c + " ") or compact.endswith(" " + c)):
            detected_sport = candidate
            break
    if not detected_sport:
        detected_sport = text.split(" ")[0] if text else "General"
    template, display_sport, similarity = resolve_sport_template(detected_sport)
    profile["sport"] = display_sport or detected_sport
    if template == "Gym":
        profile["sport"] = "Gym"
    profile["sport_type"] = detect_sport_type(profile["sport"]) or "Individual Sport"

    # Duration
    duration_match = re.search(r"(\d{2,3})\s*(min|mins|minutes|minute|m)\b", compact)
    if not duration_match:
        duration_match = re.search(r"\b(30|35|40|45|50|55|60|70|75|80|90|100|105|120|150|180)\b", compact)
    profile["duration"] = int(duration_match.group(1)) if duration_match else 75
    profile["duration"] = max(30, min(180, int(profile["duration"])))

    # Goal/session type
    if any(w in compact for w in ["hypertrophy", "hypertrofia", "muscle", "massa", "bulk"]):
        profile["goal"] = "Hypertrophy" if template == "Gym" else "Build fitness"
    elif any(w in compact for w in ["fat loss", "lose fat", "weight loss", "emagrecer", "cut", "cardio"]):
        profile["goal"] = "Fat Loss" if template == "Gym" else "Build fitness"
    elif any(w in compact for w in ["injury", "prehab", "prevent", "pain"]):
        profile["goal"] = "Injury prevention"
    elif any(w in compact for w in ["competition", "match", "tournament", "game prep"]):
        profile["goal"] = "Competition preparation"
    elif any(w in compact for w in ["learn", "beginner", "new"]):
        profile["goal"] = "Learn how to play"
    elif template == "Gym":
        profile["goal"] = "Athletic Performance" if any(w in compact for w in ["sport", "athletic", "performance", "explosive"] ) else "General Fitness"
    else:
        profile["goal"] = "Improve performance"

    if any(w in compact for w in ["technical", "technique", "skill", "skills"]):
        profile["session_type"] = "Technical Priority"
    elif any(w in compact for w in ["physical", "conditioning", "strength", "power", "speed", "explosive", "hard", "intense"]):
        profile["session_type"] = "Intense Session" if template == "Gym" and "intense" in compact else "Physical Priority"
    elif any(w in compact for w in ["competition week", "match prep", "tournament prep"]):
        profile["session_type"] = "Competition Week"
    else:
        profile["session_type"] = "Balanced Session"

    if any(w in compact for w in ["beginner", "iniciante", "new"]):
        profile["level"] = "Beginner"
    elif any(w in compact for w in ["advanced", "elite", "pro", "experienced", "avancado"]):
        profile["level"] = "Experienced" if template == "Gym" else "Advanced"
    else:
        profile["level"] = "Intermediate"

    if any(w in compact for w in ["no equipment", "bodyweight", "minimal", "home"]):
        profile["equipment_level"] = "Minimal"
    elif any(w in compact for w in ["full gym", "elite", "complete"]):
        profile["equipment_level"] = "Elite"
    elif any(w in compact for w in ["gym", "barbell", "machine", "dumbbell"]):
        profile["equipment_level"] = "Competitive"
    else:
        profile["equipment_level"] = "Medium"

    freq_match = re.search(r"(\d+)\s*(x|times|days)\s*(per|a)?\s*week", compact)
    profile["weekly_target"] = max(1, min(7, int(freq_match.group(1)))) if freq_match else 3
    profile["pain_flag"] = any(w in compact for w in ["pain", "hurt", "injury", "discomfort", "dor"])
    if profile["pain_flag"]:
        profile["pain_location"] = "Mentioned in free description"
        profile["pain_scale"] = 3
    profile["needs_low_impact"] = any(w in compact for w in ["low impact", "easy on joints", "return", "recovery"])

    if any(w in compact for w in ["alone", "solo", "by myself", "sozinho", "sozinha"]):
        profile["training_alone"] = True
    elif any(w in compact for w in ["with friends", "with teammates", "group", "team training", "partner", "duo", "small group"]):
        profile["training_alone"] = False
        people_match = re.search(r"(?:with|plus|and)\s+(\d+)\s+(?:people|friends|teammates|partners|players)", compact)
        profile["training_partners_count"] = int(people_match.group(1)) if people_match else 1
    else:
        profile["training_alone"] = True

    # Gym focused on another sport: detect "gym for water polo", "gym focused on soccer", etc.
    if template == "Gym":
        focus_match = re.search(r"(?:for|focused on|support|to improve)\s+([a-zA-Z\s]{3,40})", text, flags=re.I)
        if focus_match:
            focus_text = normalize_text(focus_match.group(1))
            if focus_text and not is_gym_sport(focus_text):
                profile["gym_sport_focus_flag"] = True
                profile["gym_focus_sport"] = focus_text
    return profile


def handle_description_reply(user_text: str) -> None:
    append_user_message(user_text)
    profile = parse_free_description_to_profile(user_text)
    st.session_state.training_profile = profile
    st.session_state.training_chat_complete = True
    st.session_state.description_mode_waiting = False
    append_bot_message("Great. I understood your description and I am generating your session now.")
    generate_training_from_chat_profile()

def handle_chat_reply(user_text: str) -> None:
    if st.session_state.get("training_entry_mode") == "describe":
        handle_description_reply(user_text)
        return
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


def infer_primary_focus(goal: str, session_type: str, sport: str) -> str:
    if match_supported_sport(sport) == "Gym" or is_gym_sport(sport):
        if goal == "Hypertrophy":
            return "Strength"
        if goal == "Fat Loss":
            return "Conditioning"
        if goal == "Athletic Performance":
            return "Power"
        return "Movement Quality"
    if session_type == "Technical Priority":
        return "Technical Quality"
    if session_type == "Physical Priority":
        return "Conditioning"
    if goal == "Injury prevention":
        return "Movement Quality"
    if goal == "Build fitness":
        return "Conditioning"
    if goal == "Competition preparation":
        return "Match Rhythm"
    return "Technical Quality"


def pain_adjustment_minutes(pain_scale: object) -> int:
    try:
        score = int(pain_scale)
    except Exception:
        return 5
    if score >= 8:
        return 15
    if score >= 5:
        return 10
    if score >= 1:
        return 5
    return 0


def build_session(profile: Dict[str, object]) -> Tuple[List[Exercise], List[int], Dict[str, object]]:
    ensure_sportze_libraries_expanded()
    raw_sport = str(profile.get("sport", "")).strip()
    template_sport, display_sport, similarity_info = resolve_sport_template(raw_sport)
    supported_sport = template_sport
    sport_for_engine = supported_sport or "General"

    gym_focus_template = None
    gym_focus_display = ""
    if supported_sport == "Gym" and bool(profile.get("gym_sport_focus_flag", False)):
        gym_focus_display = str(profile.get("gym_focus_sport", "")).strip()
        gym_focus_template, _, similarity_info = resolve_sport_template(gym_focus_display)
        if gym_focus_template and gym_focus_template != "Gym":
            sport_for_engine = f"Gym for {gym_focus_template}"
            library = SPORT_LIBRARY.get(f"Gym for {gym_focus_template}", SPORT_LIBRARY.get("Gym", DEFAULT_GENERAL_LIBRARY))
        else:
            library = SPORT_LIBRARY.get("Gym", DEFAULT_GENERAL_LIBRARY)
    else:
        library = SPORT_LIBRARY.get(supported_sport, DEFAULT_GENERAL_LIBRARY)

    session_type = str(profile.get("session_type", "Balanced Session"))
    requested_session_type = session_type
    if session_type == "Intense Session":
        session_type = "Physical Priority"
    duration = int(profile.get("duration", 75))
    goal = str(profile.get("goal", "Improve performance"))
    level = str(profile.get("level", "Intermediate"))
    if level == "Experienced":
        level = "Advanced"
    season_phase = str(profile.get("season_phase", "All" if supported_sport == "Gym" else "General Training"))
    primary_focus = infer_primary_focus(goal, session_type, raw_sport)
    position = str(profile.get("goal", "General Fitness") if supported_sport == "Gym" else "General Profile")

    adjusted_duration = duration
    if bool(profile.get("competition_soon", False)) and is_competitive_level(level):
        adjusted_duration = min(adjusted_duration, duration)
        if session_type == "Physical Priority":
            session_type = "Competition Week"
    if bool(profile.get("pain_flag", False)) or bool(profile.get("needs_low_impact", False)):
        adjusted_duration = max(30, adjusted_duration - pain_adjustment_minutes(profile.get("pain_scale", 3)))

    blueprint_key = "Gym" if supported_sport == "Gym" else (supported_sport or "default")
    blueprint = get_blueprint(blueprint_key, session_type)
    blueprint = trim_blueprint_to_target(blueprint, target_exercise_count(blueprint_key, adjusted_duration))

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

    if not session:
        library = DEFAULT_GENERAL_LIBRARY
        for category, count in blueprint.items():
            session.extend(choose_exercises_for_category(library.get(category, []), count, position, level, season_phase, primary_focus))

    block_minutes = allocate_block_minutes(session, adjusted_duration, session_type, goal)

    meta = {
        "supported_sport": supported_sport,
        "display_sport": display_sport or raw_sport,
        "sport_for_engine": sport_for_engine,
        "similarity_template_used": similarity_info.get("template") if similarity_info else None,
        "similarity_reason": similarity_info.get("why") if similarity_info else None,
        "similarity_adaptation": similarity_info.get("adaptation") if similarity_info else None,
        "gym_focus_sport": gym_focus_display,
        "gym_focus_template": gym_focus_template,
        "adjusted_duration": adjusted_duration,
        "session_type": requested_session_type if requested_session_type == "Intense Session" else session_type,
        "engine_session_type": session_type,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "gym_summary_enabled": bool(supported_sport == "Gym"),
        "primary_focus_inferred": primary_focus,
        "season_phase_used": season_phase,
        "training_alone": bool(profile.get("training_alone", True)),
        "training_partners_count": int(profile.get("training_partners_count", 0) or 0),
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


def estimate_session_load(level: str, duration: int, pain_flag: bool = False, low_impact: bool = False) -> str:
    score = 0
    score += {"Beginner": 1, "Intermediate": 2, "Advanced": 3, "Experienced": 3, "Elite": 4}.get(level, 2)
    score += 1 if duration >= 75 else 0
    score += 1 if duration >= 105 else 0
    if pain_flag or low_impact:
        score = max(0, score - 1)
    if score <= 2:
        return "Low to Moderate"
    if score <= 4:
        return "Moderate"
    if score <= 5:
        return "Moderate to High"
    return "High"

def extract_planned_reps_from_prescription(prescription: str, goal: str) -> int:
    text = prescription.lower()
    ranges = re.findall(r"(\d+)\s*[-–]\s*(\d+)\s*reps", text)
    if ranges:
        low, high = map(int, ranges[0])
        if goal == "Hypertrophy":
            return min(high, max(low, 10))
        if goal == "Fat Loss":
            return min(high, max(low, 12))
        if goal == "Athletic Performance":
            return min(high, max(low, 6))
        return round((low + high) / 2)
    single = re.findall(r"(\d+)\s*reps", text)
    if single:
        return int(single[0])
    if "interval" in text or "conditioning" in text:
        return 8
    if "cooldown" in text or "mobility" in text or "warm" in text:
        return 6
    return 10


def gym_exact_prescription(ex: Exercise, goal: str) -> Tuple[str, int, int]:
    # Gym mode deliberately uses an exact 3-set prescription for every block so the summary logger
    # can pre-fill a clear planned target and compare what the athlete actually completed.
    planned_sets = 3
    planned_reps = extract_planned_reps_from_prescription(ex.prescription, goal)
    prescription = f"Do {planned_sets} sets of {planned_reps} reps. {ex.prescription}"
    return prescription, planned_sets, planned_reps

def build_session_payload(profile: Dict[str, object], session: List[Exercise], block_minutes: List[int], meta: Dict[str, object]) -> Dict[str, object]:
    safe_profile = dict(profile)
    safe_profile["generated_at"] = meta["generated_at"]
    is_gym = bool(meta.get("gym_summary_enabled", False))
    goal = str(profile.get("goal", "General Fitness"))
    exercise_rows = []
    for ex, minutes in zip(session, block_minutes):
        prescription = ex.prescription
        planned_sets = None
        planned_reps = None
        if is_gym:
            prescription, planned_sets, planned_reps = gym_exact_prescription(ex, goal)
        exercise_rows.append({
            "name": ex.name,
            "category": ex.category,
            "prescription": prescription,
            "purpose": ex.purpose,
            "coaching_points": ex.coaching_points,
            "planned_block_minutes": minutes,
            "planned_sets": planned_sets,
            "planned_reps": planned_reps,
        })
    payload = {
        "session_id": build_session_hash(safe_profile, session),
        "title": build_session_title(profile),
        "profile": safe_profile,
        "meta": meta,
        "exercises": exercise_rows,
    }
    return payload

def persist_generated_session(payload: Dict[str, object], on_persist: Optional[Callable[[], None]]) -> None:
    saved = st.session_state.get("saved_training_sessions", [])
    saved = [s for s in saved if s.get("session_id") != payload.get("session_id")]
    saved.insert(0, payload)
    st.session_state.saved_training_sessions = saved[:50]
    if on_persist:
        on_persist()



def apply_training_catalog_session_if_available(payload: Dict[str, object]) -> Dict[str, object]:
    """Optional hook for the future training_catalog.py file.

    The current generator still works exactly as before. When training_catalog.py is
    expanded later, get_catalog_session(profile, meta) may return a dict with:
    - "title" optional
    - "exercises" optional list of exercise dictionaries
    - "meta" optional extra metadata
    - "source" optional catalog source label

    If the catalog is missing or returns None, this function leaves the payload unchanged.
    """
    if get_catalog_session is None:
        return payload

    try:
        catalog_result = get_catalog_session(
            profile=payload.get("profile", {}),
            meta=payload.get("meta", {}),
        )
    except Exception as exc:
        payload.setdefault("meta", {})["catalog_error"] = str(exc)
        return payload

    if not catalog_result:
        return payload

    if isinstance(catalog_result, dict):
        if catalog_result.get("title"):
            payload["title"] = str(catalog_result["title"])
        if isinstance(catalog_result.get("exercises"), list) and catalog_result["exercises"]:
            payload["exercises"] = catalog_result["exercises"]
        if isinstance(catalog_result.get("meta"), dict):
            payload.setdefault("meta", {}).update(catalog_result["meta"])
        payload.setdefault("meta", {})["catalog_source"] = catalog_result.get("source", "training_catalog.py")
    return payload


def generate_training_from_chat_profile() -> None:
    profile = dict(st.session_state.training_profile)
    session, block_minutes, meta = build_session(profile)
    payload = build_session_payload(profile, session, block_minutes, meta)
    payload = apply_training_catalog_session_if_available(payload)
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
            ex["name"]: {"done": True, "reps": ex.get("planned_reps"), "sets": ex.get("planned_sets"), "weight": None}
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
    exercises = payload.get("exercises", [])

    st.subheader(payload.get("title", "Training session"))
    st.markdown("### Session")

    if not exercises:
        st.info("No exercises were generated for this session.")
        return

    for idx, ex in enumerate(exercises, start=1):
        name = str(ex.get("name", f"Exercise {idx}")).strip() or f"Exercise {idx}"
        prescription = str(ex.get("prescription", "")).strip()

        if not prescription:
            sets = ex.get("planned_sets")
            reps = ex.get("planned_reps")
            if sets and reps:
                prescription = f"{sets}x{reps} reps"
            else:
                prescription = "Follow the planned reps/time for this block."

        st.markdown(f"**{idx}. {name}**")
        st.markdown(f"- {prescription}")

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
                    "Number of reps completed",
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
    ensure_sportze_libraries_expanded()
    st.session_state["_training_on_persist"] = on_persist

    st.header("Training Generator")

    if not st.session_state.training_chat_started and not st.session_state.get("latest_training_payload"):
        left, right = st.columns(2)
        with left:
            with st.container(border=True):
                st.subheader("Answer some questions")
                st.write("answer our questions for the best possible training session for yourself.")
                if st.button("Start training chat", type="primary", use_container_width=True, key="start_guided_training_chat_btn"):
                    start_training_chat("guided")
                    st.rerun()
        with right:
            with st.container(border=True):
                st.subheader("Describe your training session")
                st.write("describe exactly what kind of training session you want (sport, focus, main goal, duration, etc.) and I'll generate it for you.")
                if st.button("Start training chat", type="primary", use_container_width=True, key="start_describe_training_chat_btn"):
                    start_training_chat("describe")
                    st.rerun()

        st.caption("Sportze.AI now supports the 31 core sport libraries plus a 32-200 sport similarity map, so uncommon sports can adapt from the closest template instead of receiving a generic plan.")
        return

    top1, top2 = st.columns([1, 1])
    with top1:
        if st.button("Restart training chat", use_container_width=True, key="restart_training_chat_btn"):
            reset_training_chat()
            st.rerun()
    with top2:
        if st.session_state.get("training_entry_mode") == "describe":
            st.caption("Mode: Describe your training session")
        else:
            st.caption("Mode: Answer some questions")

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
# Clean human grammar aliases.
# These are real typing mistakes, slang, English/Portuguese variants, and short answers.
# No fake numbered aliases.
# -----------------------------------------------------------------------------
EXTRA_COMMON_ANSWER_ALIASES = {
    "performace": "Improve performance", "perfomance": "Improve performance", "preformance": "Improve performance",
    "imrpove performance": "Improve performance", "improve performace": "Improve performance", "improve my game": "Improve performance",
    "get better": "Improve performance", "better at sport": "Improve performance", "melhorar": "Improve performance",
    "build fitnes": "Build fitness", "build fitnesss": "Build fitness", "get fit": "Build fitness", "get in shape": "Build fitness",
    "stamina": "Build fitness", "endurance": "Build fitness", "cardio": "Build fitness", "condicionamento": "Build fitness",
    "return": "Return after a break", "after break": "Return after a break", "comeback": "Return after a break", "voltar": "Return after a break",
    "retorno": "Return after a break", "back from injury": "Return after a break",
    "learn": "Learn how to play", "learn sport": "Learn how to play", "new sport": "Learn how to play", "aprender": "Learn how to play",
    "injury prev": "Injury prevention", "avoid injury": "Injury prevention", "prevent injuries": "Injury prevention", "prevencao": "Injury prevention",
    "comp": "Competition preparation", "game prep": "Competition preparation", "match prep": "Competition preparation", "tournament prep": "Competition preparation",
    "hypertrofy": "Hypertrophy", "hipertrofia": "Hypertrophy", "hypertrofia": "Hypertrophy", "gain muscle": "Hypertrophy",
    "muscle gain": "Hypertrophy", "muscle mass": "Hypertrophy", "massa muscular": "Hypertrophy", "bulk": "Hypertrophy",
    "fatloss": "Fat Loss", "fat lose": "Fat Loss", "lose fat": "Fat Loss", "lose weight": "Fat Loss", "loose weight": "Fat Loss",
    "weightloss": "Fat Loss", "emagrecer": "Fat Loss", "perder gordura": "Fat Loss", "cutting": "Fat Loss",
    "ath perf": "Athletic Performance", "athletic perf": "Athletic Performance", "sport specific": "Athletic Performance",
    "explosive": "Athletic Performance", "explosiveness": "Athletic Performance",
    "begginer": "Beginner", "beginer": "Beginner", "starter": "Beginner", "starting": "Beginner", "iniciante": "Beginner",
    "intermidiate": "Intermediate", "intermed": "Intermediate", "mid": "Intermediate", "medio": "Intermediate", "médio": "Intermediate",
    "advnaced": "Advanced", "avanced": "Advanced", "avançado": "Advanced", "serious": "Advanced",
    "exp": "Experienced", "experiente": "Experienced", "very experienced": "Experienced",
    "bal": "Balanced Session", "mix": "Balanced Session", "mixed": "Balanced Session", "normal session": "Balanced Session",
    "technique": "Technical Priority", "skills": "Technical Priority", "tecnica": "Technical Priority", "técnica": "Technical Priority",
    "physic": "Physical Priority", "physical session": "Physical Priority", "conditioning session": "Physical Priority", "fisico": "Physical Priority", "físico": "Physical Priority",
    "intensive": "Intense Session", "hard session": "Intense Session", "puxado": "Intense Session", "pesado": "Intense Session",
    "min": "Minimal", "minimal equipment": "Minimal", "no equipment": "Minimal", "home": "Minimal",
    "basico": "Basic", "básico": "Basic", "some equipment": "Basic",
    "med": "Medium", "normal equipment": "Medium", "medio equipment": "Medium", "médio equipment": "Medium",
    "club": "Competitive", "club level": "Competitive", "complete": "Elite", "full gym": "Elite", "full equipment": "Elite",
    "individual": "Individual Sport", "solo": "Individual Sport", "alone": "Individual Sport",
    "team": "Team Sport", "team sport": "Team Sport", "collective": "Team Sport", "time": "Team Sport",
}
COMMON_ANSWER_ALIASES.update({canonical_compact(k): v for k, v in EXTRA_COMMON_ANSWER_ALIASES.items()})

# Curated human typing aliases: short slang, spelling errors, Portuguese/English mix, and fast answers.
CURATED_GRAMMAR_ALIASES = {
    "perfomance": "Improve performance", "preformance": "Improve performance", "perform": "Improve performance", "better performance": "Improve performance",
    "improve perf": "Improve performance", "improve my game": "Improve performance", "get better": "Improve performance",
    "build fit": "Build fitness", "build fitnesss": "Build fitness", "get in shape": "Build fitness", "shape": "Build fitness",
    "cardio": "Build fitness", "stamina": "Build fitness", "endurance": "Build fitness", "condicionamento": "Build fitness",
    "back after break": "Return after a break", "after break": "Return after a break", "voltar": "Return after a break", "retorno": "Return after a break",
    "learn sport": "Learn how to play", "new sport": "Learn how to play", "begin learning": "Learn how to play", "aprender": "Learn how to play",
    "injury prev": "Injury prevention", "injury prevent": "Injury prevention", "avoid injury": "Injury prevention", "prevent injuries": "Injury prevention",
    "comp": "Competition preparation", "tournament": "Competition preparation", "game prep": "Competition preparation", "prepare match": "Competition preparation",
    "hypertrofia": "Hypertrophy", "hipertrofia": "Hypertrophy", "hipertrophy": "Hypertrophy", "gain muscle": "Hypertrophy",
    "muscle mass": "Hypertrophy", "massa": "Hypertrophy", "massa muscular": "Hypertrophy", "size": "Hypertrophy",
    "lose weight": "Fat Loss", "loose weight": "Fat Loss", "weightloss": "Fat Loss", "emagrecer": "Fat Loss", "perder gordura": "Fat Loss",
    "definition": "Fat Loss", "cutting": "Fat Loss", "dry": "Fat Loss", "leaning": "Fat Loss",
    "ath perf": "Athletic Performance", "explosive": "Athletic Performance", "explosiveness": "Athletic Performance", "sport specific": "Athletic Performance",
    "general fit": "General Fitness", "healthy": "General Fitness", "health fitness": "General Fitness", "overall": "General Fitness",
    "beggin": "Beginner", "begginers": "Beginner", "starter": "Beginner", "starting": "Beginner", "iniciante": "Beginner",
    "intermed": "Intermediate", "mid": "Intermediate", "medio": "Intermediate", "médio": "Intermediate",
    "advnaced": "Advanced", "avanced": "Advanced", "good": "Advanced", "serious": "Advanced", "avançado": "Advanced",
    "exp": "Experienced", "experiente": "Experienced", "very experienced": "Experienced",
    "bal": "Balanced Session", "balanced session": "Balanced Session", "mix": "Balanced Session", "mixed": "Balanced Session",
    "technique": "Technical Priority", "skills": "Technical Priority", "skill": "Technical Priority", "tecnica": "Technical Priority", "técnica": "Technical Priority",
    "physic": "Physical Priority", "physical session": "Physical Priority", "conditioning session": "Physical Priority", "fisico": "Physical Priority", "físico": "Physical Priority",
    "intensive": "Intense Session", "hard session": "Intense Session", "hardcore": "Intense Session", "puxado": "Intense Session", "pesado": "Intense Session",
    "min": "Minimal", "mínimo": "Minimal", "minimal equipment": "Minimal", "no equipment": "Minimal",
    "basico": "Basic", "básico": "Basic", "some equipment": "Basic", "normal equipment": "Medium",
    "medium": "Medium", "med": "Medium", "medio equipment": "Medium", "médio equipment": "Medium",
    "club": "Competitive", "club level": "Competitive", "competition equipment": "Competitive",
    "complete": "Elite", "full gym": "Elite", "full equipment": "Elite", "elite equipment": "Elite",
    "individual": "Individual Sport", "individual sport": "Individual Sport", "alone": "Individual Sport", "solo": "Individual Sport",
    "team": "Team Sport", "team sport": "Team Sport", "collective": "Team Sport", "time": "Team Sport",
}
COMMON_ANSWER_ALIASES.update({canonical_compact(k): v for k, v in CURATED_GRAMMAR_ALIASES.items()})

EXTRA_GYM_EXERCISES = [
    Exercise("Goblet squat", "Physical", "3-4 sets of 8-12 reps", "Lower-body strength with simple setup.", ["Dumbbell", "Kettlebell"], ["Moderate"], ["Strength"], ["All"], ["All"], ["All"], 1.05),
    Exercise("Romanian deadlift", "Physical", "3-4 sets of 6-10 reps", "Posterior chain strength for running, jumping, swimming, and field sports.", ["Dumbbells", "Barbell"], ["Moderate", "High"], ["Strength"], ["All"], ["Intermediate", "Advanced", "Experienced", "Elite"], ["All"], 1.1),
    Exercise("Trap bar deadlift", "Physical", "3-5 sets of 3-6 reps", "Total-body strength with athletic transfer.", ["Trap bar"], ["High"], ["Strength", "Power"], ["Athletic Performance"], ["Advanced", "Experienced", "Elite"], ["All"], 1.15),
    Exercise("Dumbbell bench press", "Physical", "3-4 sets of 8-12 reps", "Upper-body pushing strength.", ["Dumbbells", "Bench"], ["Moderate"], ["Strength"], ["All"], ["All"], ["All"], 1.0),
    Exercise("Pull-up or lat pulldown", "Physical", "3-4 sets of 6-12 reps", "Upper-body pulling strength and shoulder support.", ["Pull-up bar", "Machine"], ["Moderate", "High"], ["Strength"], ["All"], ["All"], ["All"], 1.0),
    Exercise("Split squat", "Physical", "3 sets of 8-10 reps each side", "Single-leg control for field, court, and water sports.", ["Bodyweight", "Dumbbells"], ["Moderate"], ["Strength", "Movement Quality"], ["All"], ["All"], ["All"], 1.05),
    Exercise("Lateral lunge", "Physical", "3 sets of 6-10 reps each side", "Adductor strength and lateral control.", ["Bodyweight", "Dumbbells"], ["Moderate"], ["Movement Quality", "Strength"], ["All"], ["All"], ["All"], 0.95),
    Exercise("Medicine ball rotational throw", "Physical", "4-6 sets of 3-5 throws each side", "Rotational power for throwing, hitting, striking, and serving sports.", ["Medicine ball", "Wall"], ["High"], ["Power"], ["Athletic Performance"], ["Intermediate", "Advanced", "Experienced", "Elite"], ["All"], 0.9),
    Exercise("Box jump or broad jump", "Physical", "4-6 sets of 2-4 reps", "Explosive lower-body power.", ["Box", "Open space"], ["High"], ["Power"], ["Athletic Performance"], ["Intermediate", "Advanced", "Experienced", "Elite"], ["All"], 0.85),
    Exercise("Sled push or bike sprint", "Physical", "6-10 short efforts of 8-20 seconds", "Repeated high-intensity conditioning.", ["Sled", "Bike", "Open space"], ["High"], ["Conditioning", "Power"], ["Fat Loss", "Athletic Performance"], ["All"], ["All"], 1.0),
    Exercise("Pallof press", "Physical", "3 sets of 8-12 reps each side", "Anti-rotation core strength.", ["Cable", "Band"], ["Low", "Moderate"], ["Movement Quality", "Strength"], ["All"], ["All"], ["All"], 0.75),
    Exercise("Shoulder external rotation", "Recovery", "2-3 sets of 12-15 reps", "Shoulder durability for throwing, swimming, racket, and contact sports.", ["Band", "Cable"], ["Low"], ["Movement Quality"], ["All"], ["All"], ["All"], 0.7),
    Exercise("Hip mobility reset", "Recovery", "5-8 minutes controlled mobility", "Restore hip positions after strength or field/court work.", ["Bodyweight"], ["Low"], ["Movement Quality"], ["All"], ["All"], ["All"], 0.7),
]
for _exercise in EXTRA_GYM_EXERCISES:
    SPORT_LIBRARY.setdefault("Gym", {}).setdefault(_exercise.category, []).append(_exercise)


# Materialized PDF session-library index: every core sport has exactly 17 selectable
# session options available to the generator/UI or a future API layer.
def build_full_session_library_index() -> Dict[str, Dict[str, List[Dict[str, object]]]]:
    index: Dict[str, Dict[str, List[Dict[str, object]]]] = {}
    for sport_name, emphasis in CORE_SPORT_TEMPLATE_INFO.items():
        if sport_name == "Gym":
            continue
        normal_sessions = []
        for session_title, purpose, blocks in SPORTZE_NORMAL_SESSION_TEMPLATES:
            normal_sessions.append({
                "title": session_title,
                "type": "normal sport session",
                "purpose": purpose,
                "sport_emphasis": emphasis,
                "blocks": [{"name": name, "prescription": prescription} for name, prescription in blocks],
            })
        gym_sessions = []
        for session_title, blocks in SPORTZE_GYM_SESSION_TEMPLATES:
            gym_sessions.append({
                "title": session_title,
                "type": "adapted gym session",
                "purpose": f"Gym transfer session for {sport_name}: {emphasis}.",
                "sport_emphasis": emphasis,
                "blocks": [{"name": name, "prescription": prescription} for name, prescription in blocks],
            })
        index[sport_name] = {"normal_sessions": normal_sessions, "adapted_gym_sessions": gym_sessions}
    return index

SPORTZE_FULL_SESSION_LIBRARY_INDEX = build_full_session_library_index()


def get_all_session_options_for_sport(sport_text: str) -> Dict[str, object]:
    template, display_sport, similarity_info = resolve_sport_template(sport_text)
    if template == "Gym":
        return {"sport": display_sport or "Gym", "template": "Gym", "normal_sessions": [], "adapted_gym_sessions": []}
    if template not in SPORTZE_FULL_SESSION_LIBRARY_INDEX:
        template = "Soccer"
        similarity_info = similarity_info or {"template": "Soccer", "why": "general sport fallback", "adaptation": "general athletic session"}
    result = dict(SPORTZE_FULL_SESSION_LIBRARY_INDEX.get(template, {}))
    result.update({"sport": display_sport or sport_text, "template": template, "similarity_info": similarity_info})
    return result


if __name__ == "__main__":
    render_training_generator_section()
