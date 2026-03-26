import math
import random
from datetime import datetime, timedelta

import streamlit as st

# Optional modular imports (the app is built to work with the separated files if present)
try:
    from video_review_section import run_video_review as external_video_review
except Exception:
    external_video_review = None

try:
    from counselling_section import run_counselling as external_counselling
except Exception:
    external_counselling = None

try:
    from physio_section import run_physio as external_physio
except Exception:
    external_physio = None


# =========================
# PAGE SETUP
# =========================
st.set_page_config(page_title="Sportze.AI", layout="wide")
st.title("Sportze.AI")
st.write("Generate smarter, more professional sport-specific training sessions.")

TODAY = datetime.today().date()

if "active_section" not in st.session_state:
    st.session_state.active_section = "Training Generator"


# =========================
# GLOBAL OPTIONS / TAXONOMY
# =========================
SECTION_OPTIONS = [
    "Training Generator",
    "Video Review",
    "Counselling",
    "Physio",
]

SPORTS = [
    "Gym",
    "Running",
    "Tennis",
    "Baseball",
    "Rowing",
    "Weightlifting",
    "Water Polo",
    "Soccer",
    "Boxing",
    "Volleyball",
    "Basketball",
    "Surfing",
]

ROLES = ["Player", "Coach"]
COMMON_GOALS = [
    "Improve performance",
    "Build fitness",
    "Return after a break",
    "Learn how to play",
    "Have fun / stay active",
]
SKILL_LEVELS = ["Beginner", "Intermediate", "Advanced"]
INJURY_OPTIONS = ["No", "Yes - minor limitation", "Yes - recent injury"]
TIME_OPTIONS_GENERAL = ["30 minutes", "45 minutes", "60 minutes", "75 minutes", "90 minutes", "120 minutes"]
TIME_OPTIONS_ENDURANCE = ["30 minutes", "45 minutes", "60 minutes", "75 minutes", "90 minutes", "120 minutes", "150 minutes", "180 minutes"]
AGE_BANDS = ["U8-U10", "U11-U13", "U14-U16", "U17-U19", "Senior"]

POSITION_MAP = {
    "Soccer": [
        "Goalkeeper",
        "Centre back",
        "Full back / wing back",
        "Defensive midfielder",
        "Central midfielder",
        "Attacking midfielder",
        "Winger",
        "Striker",
        "Mixed / multiple positions",
    ],
    "Water Polo": [
        "Goalkeeper",
        "Center forward / hole set",
        "Point",
        "Wing",
        "Driver / flat",
        "Utility / all-around",
    ],
    "Basketball": [
        "Point guard",
        "Shooting guard",
        "Small forward",
        "Power forward",
        "Center",
        "Combo guard / hybrid wing",
    ],
    "Volleyball": [
        "Setter",
        "Outside hitter",
        "Opposite",
        "Middle blocker",
        "Libero",
        "Defensive specialist",
        "All-around / mixed",
    ],
    "Baseball": [
        "Pitcher",
        "Catcher",
        "First base",
        "Second base",
        "Third base",
        "Shortstop",
        "Outfielder",
        "Utility",
    ],
    "Tennis": ["Singles", "Doubles", "Mixed development"],
    "Boxing": ["Orthodox", "Southpaw", "Switch / adaptable"],
}

FOCUS_MAP = {
    "Running": [
        "Short distance",
        "Medium distance",
        "Long distance",
        "Ultra long distance",
        "Mixed event conditioning",
    ],
    "Gym": [
        "General strength",
        "Sport-specific strength",
        "Return to training",
        "Power / explosiveness",
        "Hypertrophy support",
    ],
    "Tennis": [
        "Technique",
        "Match play",
        "Movement",
        "Serve / return",
        "Net play / transition",
        "Consistency under pressure",
    ],
    "Baseball": [
        "General skills",
        "Hitting",
        "Throwing",
        "Fielding",
        "Base running",
        "Game IQ / decision making",
    ],
    "Rowing": [
        "Technique",
        "Aerobic base",
        "Power",
        "Race prep",
        "Starts / rate change",
        "Race-pace endurance",
    ],
    "Weightlifting": [
        "General Olympic lifting",
        "Snatch",
        "Clean & jerk",
        "Strength support",
        "Pulls & positions",
        "Power from the floor",
    ],
    "Water Polo": [
        "General development",
        "Swimming conditioning",
        "Shooting",
        "Passing & extra-man play",
        "Defending / counterattack",
        "Leg drive & eggbeater power",
    ],
    "Soccer": [
        "General development",
        "Technical development",
        "Finishing",
        "First touch & passing",
        "1v1 attacking / defending",
        "Possession",
        "Build-up play",
        "Pressing & defending",
        "Transition",
        "Small-sided games",
        "Conditioning with the ball",
        "Set pieces",
    ],
    "Boxing": [
        "General boxing development",
        "Footwork & movement",
        "Jab & straight punches",
        "Defense & countering",
        "Combinations on bag/pads",
        "Conditioning for boxing",
        "Ring craft / tactics",
        "Inside fighting / short range work",
    ],
    "Volleyball": [
        "General volleyball development",
        "Serving & first ball pressure",
        "Serve receive / passing",
        "Setting & second contact",
        "Attacking / hitting",
        "Blocking / net defense",
        "Backcourt defense & transition",
        "Game-like rally training",
    ],
    "Basketball": [
        "General basketball development",
        "Ball handling & creation",
        "Shooting",
        "Finishing at the rim",
        "Defense & closeouts",
        "Transition & fast break",
        "Pick-and-roll reads",
        "Conditioning with game actions",
    ],
    "Surfing": [
        "General surf development",
        "Pop-up speed",
        "Paddling endurance",
        "Balance & stance control",
        "Power turns",
        "Aerial preparation",
        "Small-wave flow",
        "Big-wave preparation",
    ],
}

RUNNING_DISTANCE_MAP = {
    "Short distance": ["100m", "200m", "400m", "800m"],
    "Medium distance": ["1.5k", "3k", "5k", "10k"],
    "Long distance": ["15k", "Half marathon", "32k", "Marathon"],
    "Ultra long distance": ["50k", "100k", "100 miles"],
    "Mixed event conditioning": ["General conditioning", "Mixed race prep"],
}

GYM_TARGET_SPORTS = [
    "Running", "Tennis", "Baseball", "Rowing", "Weightlifting", "Water Polo",
    "Soccer", "Boxing", "Volleyball", "Basketball", "Surfing"
]

PHYSIO_BODY_AREAS = [
    "Knee", "Ankle / foot", "Hamstring", "Quad", "Hip / groin", "Lower back",
    "Shoulder", "Elbow / forearm", "Wrist / hand", "Neck", "Other",
]

TEAM_SPORTS = {"Soccer", "Water Polo", "Volleyball", "Basketball", "Baseball"}
POSITION_SPORTS = set(POSITION_MAP.keys())


# =========================
# HELPERS
# =========================
def parse_minutes(session_time: str) -> int:
    return int(session_time.split()[0])


def safety_message(injury_status: str, pain_score: int) -> str | None:
    if injury_status == "Yes - recent injury":
        return "You reported a recent injury. Keep intensity conservative and avoid explosive loading if pain rises."
    if pain_score >= 7:
        return "Pain is high. Do not force the session if pain changes movement quality or worsens during training."
    if injury_status == "Yes - minor limitation":
        return "You reported a minor limitation. Keep quality high and reduce volume if needed."
    return None


def pain_requires_physio(pain_score: int) -> bool:
    return pain_score >= 7


def get_group_context_text(role: str, trains_alone: str, people_training: int, age_group: str | None = None, coach_level: int | None = None) -> str:
    if role == "Coach":
        return f"Coach session | age group: {age_group or 'mixed'} | team level: {coach_level or 5}/10 | players in session: {people_training}."
    if trains_alone == "Yes":
        return "Player session | solo training setup."
    return f"Player session | group setup with about {people_training} total people."


def section(title: str, bullets: list[str]) -> str:
    body = "\n".join([f"- {b}" for b in bullets])
    return f"### {title}\n{body}\n"


def objective_line(goal: str, level: str, focus: str, context: str) -> str:
    return f"**Session objective:** {goal} | **Level:** {level} | **Focus:** {focus} | **Context:** {context}"


def choose_by_level(beginner: str, intermediate: str, advanced: str, level: str) -> str:
    if level == "Beginner":
        return beginner
    if level == "Advanced":
        return advanced
    return intermediate


def format_plan(title: str, summary: str, parts: list[str], notes: list[str]) -> str:
    note_block = "\n".join([f"- {n}" for n in notes])
    return f"## {title}\n\n{summary}\n\n" + "\n".join(parts) + f"\n### Coaching notes\n{note_block}"


# =========================
# TRAINING GENERATORS
# =========================
def generate_running_plan(role, goal, level, injury_status, pain_score, session_time, focus, distance, context, training_days=4):
    mins = parse_minutes(session_time)
    speed_bias = focus in ["Short distance", "Medium distance"]
    warmup = section("Warm-up", [
        "8-12 min easy jog or skip progression",
        "Dynamic mobility: ankle rocks, leg swings, hip openers",
        "Running drills: A-skips, straight-leg bounds, high knees, quick contacts",
        "2-4 progressive strides before the main set",
    ])

    if focus == "Short distance":
        main = section("Main set", [
            choose_by_level("6 x 60m relaxed-fast with full walkback", "2 sets of 4 x 80m at strong but clean speed", "3 sets of 3 x 120m with full quality recovery", level),
            "Add 4-6 starts from varied positions for acceleration mechanics",
            "Keep contacts quick and posture tall after the first steps",
        ])
    elif focus == "Medium distance":
        main = section("Main set", [
            choose_by_level("8 x 200m controlled with easy rest", "5 x 600m at strong rhythm", "4 x 1k around threshold / race rhythm", level),
            "Stay relaxed through the shoulders and maintain rhythm under fatigue",
            f"Distance selected: {distance}",
        ])
    elif focus == "Long distance":
        main = section("Main set", [
            choose_by_level("30-40 min steady aerobic run", "45-70 min steady with 10-15 min stronger finish", "60-90 min aerobic progression run", level),
            f"Distance selected: {distance}",
            "Cadence should stay smooth and sustainable, not forced",
        ])
    else:
        main = section("Main set", [
            choose_by_level("40-50 min easy endurance with short form resets", "60-90 min steady aerobic work", "90-120 min endurance focus with fueling practice", level),
            f"Distance selected: {distance}",
            "Use a route or track setup that allows even pacing",
        ])

    support = section("Support work", [
        "2-3 rounds: calf raises, split squat iso hold, dead bug, side plank",
        "Optional 6-10 min mobility reset after the run",
    ])
    cooldown = section("Cool-down", [
        "5-10 min walk or very easy jog",
        "Breathing downshift and light calf / hip mobility",
    ])
    notes = [
        f"Weekly frequency reference: {training_days} sessions/week.",
        "Quality days should not stack back-to-back if legs feel flat.",
        "If pain alters stride, cut volume and stop the harder reps.",
    ]
    return format_plan("Running Session", objective_line(goal, level, focus, context), [warmup, main, support, cooldown], notes)


def generate_gym_plan(role, goal, level, injury_status, pain_score, session_time, gym_style, context, gym_target_sport=None):
    strength_pair = {
        "Running": ["rear-foot elevated split squat", "Romanian deadlift", "calf raise", "core anti-rotation"],
        "Tennis": ["split squat", "single-arm row", "landmine press", "rotational med-ball work"],
        "Baseball": ["trap-bar deadlift", "single-leg strength", "scap stability", "rotational throw prep"],
        "Rowing": ["hinge pattern", "row variation", "posterior chain endurance", "bracing work"],
        "Weightlifting": ["front squat", "pull variation", "overhead stability", "jump shrug"],
        "Water Polo": ["single-leg strength", "upper-back strength", "shoulder integrity", "rotational core"],
        "Soccer": ["split squat", "Nordic support", "lateral lunge", "jump landing mechanics"],
        "Boxing": ["single-leg strength", "push-up / press", "row", "rotational med-ball"],
        "Volleyball": ["trap-bar jump", "split squat", "landing control", "shoulder stability"],
        "Basketball": ["single-leg strength", "hip hinge", "jump / landing work", "deceleration control"],
        "Surfing": ["squat variation", "hinge", "anti-rotation core", "balance / pop-up prep"],
        None: ["squat pattern", "hinge", "push", "pull"],
    }
    template = strength_pair.get(gym_target_sport, strength_pair[None])
    warmup = section("Warm-up", [
        "5-8 min pulse raise",
        "Mobility circuit: ankles, hips, thoracic spine, shoulders",
        "Activation: glutes, trunk, scapular control",
    ])
    main = section("Main lift block", [
        choose_by_level(
            f"2-3 sets each of {template[0]} and {template[1]} at controlled quality",
            f"3-4 work sets each of {template[0]} and {template[1]} with steady loading",
            f"4-5 quality work sets each of {template[0]} and {template[1]} with intent and clean mechanics",
            level,
        ),
        f"Accessory emphasis: {template[2]}",
        f"Core / transfer emphasis: {template[3]}",
    ])
    if gym_style == "Power / explosiveness":
        extra = section("Power block", [
            "3-5 sets of jumps, throws, or explosive lifts with long rest",
            "Stop sets before speed drops sharply",
        ])
    elif gym_style == "Return to training":
        extra = section("Rebuild block", [
            "Use slower eccentrics and submaximal loads",
            "Leave 2-4 reps in reserve on most sets",
            "Focus on symmetry and pain-free range",
        ])
    else:
        extra = section("Accessory block", [
            "2-4 short accessory exercises for weak links and durability",
            "Finish with trunk stability and low-level conditioning if time allows",
        ])
    cooldown = section("Cool-down", ["Light bike or walk 4-6 min", "Mobility reset for the main areas used"])
    notes = [
        f"Gym style selected: {gym_style}.",
        f"Sport-specific anchor: {gym_target_sport or 'general gym session'}.",
        "Progress load only if technique and speed stay solid.",
    ]
    return format_plan("Gym Session", objective_line(goal, level, gym_style, context), [warmup, main, extra, cooldown], notes)


def generate_tennis_plan(role, goal, level, injury_status, pain_score, session_time, focus, context, position=None):
    technical_bias = {
        "Technique": ["groundstroke patterning", "contact point discipline", "clear margin over the net"],
        "Match play": ["serve + 1", "return + first neutral ball", "score-based point play"],
        "Movement": ["split-step timing", "first step efficiency", "recovery footwork"],
        "Serve / return": ["first serve targets", "second serve shape", "return positioning"],
        "Net play / transition": ["approach ball choice", "first volley shape", "overhead recovery"],
        "Consistency under pressure": ["cross-court tolerance", "depth under fatigue", "decision making at 30-all"],
    }
    details = technical_bias[focus]
    warmup = section("Warm-up", [
        "Mini tennis and rhythm build",
        "Movement prep: split-step timing, lateral shuffle, crossover recovery",
        "Shadow swings with target intention",
    ])
    main = section("Main tennis block", [
        choose_by_level(
            f"2-3 controlled rally patterns focused on {details[0]}",
            f"4-5 focused drill blocks around {details[0]} and {details[1]}",
            f"High-quality pattern work around {details[0]}, {details[1]}, and {details[2]}",
            level,
        ),
        "Alternate feed-based quality with live-ball points when possible",
        f"Format emphasis: {position or 'singles-oriented unless you choose doubles'}",
    ])
    athletic = section("Athletic transfer", [
        "6-10 short acceleration / deceleration reps",
        "Lateral band work, trunk stability, and shoulder care",
    ])
    points = section("Competitive finish", [
        choose_by_level("Short target game to 7", "Serve-return points with a game constraint", "Pressure tie-break or score-based scenario work", level),
    ])
    notes = [
        "If training solo, use shadow patterns, self-feed targets, and wall work with a clear intention.",
        "A good tennis session should connect technique to live decision making, not just basket reps.",
        "For doubles, build more return + first volley and poaching awareness.",
    ]
    return format_plan("Tennis Session", objective_line(goal, level, focus, context), [warmup, main, athletic, points], notes)


def generate_baseball_plan(role, goal, level, injury_status, pain_score, session_time, focus, context, position=None):
    pos_text = position or "Utility"
    warmup = section("Warm-up", [
        "Dynamic movement and shoulder prep",
        "Throwing progression from short to moderate distance",
        "Reaction and glove activation work",
    ])
    specific = {
        "Pitcher": "command, rhythm, and arm care",
        "Catcher": "receiving, transfer speed, and mobility",
        "First base": "footwork around the bag and picks",
        "Second base": "double-play rhythm and first-step range",
        "Third base": "reaction speed and charging mechanics",
        "Shortstop": "lateral coverage and throwing balance",
        "Outfielder": "reads, routes, and crow-hop throws",
        "Utility": "multi-position clean fundamentals",
    }
    main = section("Skill block", [
        f"Primary role emphasis: {specific.get(pos_text, 'general baseball fundamentals')}",
        f"Focus selected: {focus}",
        choose_by_level("Short technique sets with lots of reset time", "Game-speed reps with moderate volume", "High-quality game-speed reps with stronger decision pressure", level),
    ])
    if focus == "Hitting":
        extra = section("Hitting block", ["Tee + front toss progression", "Direction and barrel control", "Situational rounds"])
    elif focus == "Throwing":
        extra = section("Throwing block", ["Gradual build-up, not max effort from rep one", "Hit a clear target line", "Finish with arm care"])
    elif focus == "Fielding":
        extra = section("Fielding block", ["Feet before hands", "Work different hop types", "Finish plays under time pressure"])
    else:
        extra = section("Game transfer", ["Short live or reactive phase", "Base-running decision work", "Communication and game IQ cues"])
    notes = [
        "Baseball sessions should preserve throwing quality; stop before mechanics break down.",
        "Position work matters a lot for baseball players, so role-specific detail is built in here.",
        "For coaches, rotate stations so players get both technical reps and game-like decisions.",
    ]
    return format_plan("Baseball Session", objective_line(goal, level, focus, context), [warmup, main, extra], notes)


def generate_rowing_plan(role, goal, level, injury_status, pain_score, session_time, focus, context):
    warmup = section("Warm-up", ["Light erg or easy row", "Hip / hamstring / thoracic mobility", "Pick drill / pause drill to connect sequence"])
    if focus == "Technique":
        main = section("Main set", ["Pause drills and ratio control", "Legs-body-arms sequencing focus", "Video one short piece if possible for feedback"])
    elif focus == "Aerobic base":
        main = section("Main set", [choose_by_level("20-30 min easy steady", "35-50 min steady aerobic", "45-75 min aerobic with brief rate lifts", level), "Keep pressure smooth and posture long"])
    elif focus == "Power":
        main = section("Main set", ["Short powerful intervals", "Strong leg drive but no yank with the arms", "Full recovery between harder reps"])
    else:
        main = section("Main set", ["Race-pace pieces or rate-change work", "Control rhythm changes cleanly", "Finish with a quality technical reset"])
    notes = ["Sequence and posture matter more than chasing numbers every session.", "If low back tightens, reduce intensity and restore clean mechanics."]
    return format_plan("Rowing Session", objective_line(goal, level, focus, context), [warmup, main], notes)


def generate_weightlifting_plan(role, goal, level, injury_status, pain_score, session_time, focus, context):
    warmup = section("Warm-up", ["Bar path drill with dowel / empty bar", "Ankle, hip, thoracic, wrist mobility", "Primer jumps or light pulls"])
    main = section("Olympic lift block", [
        choose_by_level("Technique waves at light to moderate load", "Moderate work sets with crisp speed", "Heavier quality singles/doubles while preserving bar speed", level),
        f"Primary focus: {focus}",
        "Rest enough to keep positions sharp",
    ])
    support = section("Strength support", ["Front squat or pull variation", "Posterior chain assistance", "Overhead / trunk stability"])
    notes = ["Olympic lifting sessions are ruined by sloppy fatigue. End the top work before positions collapse.", "Use the same setup routine every rep."]
    return format_plan("Weightlifting Session", objective_line(goal, level, focus, context), [warmup, main, support], notes)


def generate_water_polo_plan(role, goal, level, injury_status, pain_score, session_time, focus, context, position=None):
    pos_text = position or "Utility / all-around"
    position_emphasis = {
        "Goalkeeper": "lateral reactions, hand speed, reading release, outlet passing",
        "Center forward / hole set": "body position, sealing water, finishing under contact",
        "Point": "ball circulation, outside shot timing, directing the attack",
        "Wing": "catch-and-shoot rhythm, angle play, extra-man spacing",
        "Driver / flat": "change of speed, front-water attack, quick release",
        "Utility / all-around": "balanced attacking and defending tasks",
    }
    warmup = section("Warm-up", [
        "Easy swim and shoulder prep",
        "Eggbeater activation and vertical balance",
        "Passing rhythm from short to moderate range",
    ])
    water = section("Main water block", [
        choose_by_level("Short technical reps with many resets", "Game-speed skill blocks with moderate volume", "High-quality game-speed work plus decision pressure", level),
        f"Position emphasis: {position_emphasis.get(pos_text, 'balanced water polo fundamentals')}",
        f"Training focus: {focus}",
    ])
    if focus == "Leg drive & eggbeater power":
        extra = section("Leg-drive block", ["Vertical holds", "Explosive up-and-release actions", "Medicine-ball or partner resistance if available"])
    elif focus == "Shooting":
        extra = section("Shooting block", ["Catch high", "Get hips and legs connected to the release", "Vary angles and time pressure"])
    else:
        extra = section("Game transfer", ["Counterattack reads", "Defensive recovery", "Small tactical game or extra-man phase"])
    notes = [
        "Water polo players need both swim capacity and vertical power, not just throwing reps.",
        "Goalkeepers should still do some passing and leg-drive work, not only reaction saves.",
        "If shoulders feel overloaded, cut throw volume early.",
    ]
    return format_plan("Water Polo Session", objective_line(goal, level, focus, context), [warmup, water, extra], notes)


def generate_soccer_player_plan(goal, level, injury_status, pain_score, session_time, focus, position, context):
    pos_text = position or "Mixed / multiple positions"
    position_detail = {
        "Goalkeeper": ["set position", "handling / parrying", "footwork into dives", "distribution after the save"],
        "Centre back": ["body shape to receive", "first pass under pressure", "aerial timing", "defensive duel control"],
        "Full back / wing back": ["overlap timing", "defensive footwork", "crossing zones", "recovery runs"],
        "Defensive midfielder": ["scan before receiving", "playing out under pressure", "counter-press positioning", "cover angles"],
        "Central midfielder": ["receiving on half-turn", "tempo control", "third-man combinations", "press resistance"],
        "Attacking midfielder": ["receive between lines", "final pass choices", "turn and accelerate", "arrive to finish"],
        "Winger": ["1v1 attack", "change of pace", "cut-in / cross decision", "defensive recovery"],
        "Striker": ["movement off the shoulder", "finishing from different services", "hold-up play", "pressing the first line"],
        "Mixed / multiple positions": ["first touch", "passing rhythm", "1v1 efficiency", "small-sided game actions"],
    }
    cues = position_detail[pos_text]
    warmup = section("Warm-up", [
        "Dynamic mobility, low contacts, and ball touches",
        "Acceleration and deceleration prep",
        "Technical warm-up with scanning before every receive",
    ])
    technical = section("Technical block", [
        f"Position cues: {cues[0]}, {cues[1]}",
        choose_by_level("Unopposed or lightly opposed reps to build clean mechanics", "Opposed technical reps with clear constraints", "Game-speed technical actions under realistic pressure", level),
        f"Main soccer focus today: {focus}",
    ])
    tactical = section("Game block", [
        f"Position cues: {cues[2]}, {cues[3]}",
        "Use directional small-sided play or phase-of-play if possible",
        "Build in transition moments rather than isolated reps only",
    ])
    physical = section("Physical finish", [
        "Short sprint or repeat-action block",
        "Change of direction with quality body position",
        "Optional trunk / adductor / groin durability circuit",
    ])
    notes = [
        "Soccer sessions should connect the ball, the body, and the decision, not separate them too much.",
        "Players should not be asked position when they are coaches; that logic is handled in the UI.",
        "For solo players, use walls, cones, finishing targets, and self-fed first-touch patterns.",
    ]
    return format_plan("Soccer Player Session", objective_line(goal, level, focus, context), [warmup, technical, tactical, physical], notes)


def generate_soccer_coach_plan(goal, session_time, focus, age_group, coach_level, people_training, context):
    level_label = "foundation" if coach_level <= 3 else "development" if coach_level <= 7 else "high-performance"
    load_line = f"{people_training} players expected | team level {coach_level}/10 | {level_label} environment."
    warmup = section("Arrival + activation", [
        "Ball-based arrival activity so nobody stands still",
        "Quick movement prep linked to the topic of the session",
        "Short competitive opener to raise focus",
    ])
    block1 = section("Theme block 1", [
        f"Theme: {focus}",
        "Use a constrained practice to repeat the core action often",
        "Coach mostly through clear cues and field design, not long speeches",
    ])
    block2 = section("Theme block 2", [
        "Progress to opposed or game-like practice",
        "Add direction, scoring, and transition consequences",
        "Keep coaching points tied to one or two non-negotiables",
    ])
    game = section("Game transfer", [
        "Finish with a conditioned game",
        "Let the theme show up naturally under pressure",
        "Brief reflective close: what did the players solve well, and what still needs work?",
    ])
    notes = [
        load_line,
        f"Age band: {age_group}. Younger groups need more reps and shorter explanations; older groups can handle richer tactical detail.",
        "Coach sessions are varied by design, so the app does not ask the coach for a single player position.",
    ]
    return format_plan("Soccer Coach Session", f"**Session objective:** Improve performance | **Focus:** {focus} | **Context:** {context}", [warmup, block1, block2, game], notes)


def generate_soccer_plan(role, goal, level, injury_status, pain_score, session_time, soccer_focus, soccer_position, age_group, coach_level, people_training, context):
    if role == "Coach":
        return generate_soccer_coach_plan(goal, session_time, soccer_focus, age_group, coach_level, people_training, context)
    return generate_soccer_player_plan(goal, level, injury_status, pain_score, session_time, soccer_focus, soccer_position, context)


def generate_boxing_plan(role, goal, level, injury_status, pain_score, session_time, focus, context, position=None):
    stance = position or "Orthodox"
    warmup = section("Warm-up", ["Footwork and rhythm prep", "Shoulder / thoracic mobility", "Shadowboxing with clear technical intent"])
    technical = section("Technical block", [
        f"Stance bias: {stance}",
        f"Main focus: {focus}",
        choose_by_level("Short, clean rounds with coaching resets", "Moderate rounds with stronger pace and sharper defense", "Fight-speed rounds with high discipline and precise recovery", level),
    ])
    if focus in ["Combinations on bag/pads", "Jab & straight punches", "Inside fighting / short range work"]:
        extra = section("Impact block", ["Bag or pad rounds", "Finish combinations balanced", "Recover guard and feet after every exchange"])
    else:
        extra = section("Conditioning / tactical block", ["Reactive slips, counters, and angle exits", "Short repeat efforts with full technical discipline"])
    notes = ["Good boxing conditioning still has to look like boxing.", "If wrists, elbows, or shoulders feel off, reduce impact volume and emphasize technique / movement."]
    return format_plan("Boxing Session", objective_line(goal, level, focus, context), [warmup, technical, extra], notes)


def generate_volleyball_plan(role, goal, level, injury_status, pain_score, session_time, focus, context, position=None):
    pos = position or "All-around / mixed"
    role_map = {
        "Setter": "second-contact quality, tempo, and decision making",
        "Outside hitter": "serve receive plus attacking range",
        "Opposite": "high-ball attacking and block timing",
        "Middle blocker": "first-step block movement and quick attack timing",
        "Libero": "first-contact quality and defensive reading",
        "Defensive specialist": "passing range and transition defense",
        "All-around / mixed": "balanced first, second, and third-contact development",
    }
    warmup = section("Warm-up", ["Movement prep and shoulder care", "Ball-control rhythm", "Small partner contact progression"])
    first = section("Primary skill block", [
        f"Position emphasis: {role_map.get(pos, 'balanced development')}",
        f"Main focus: {focus}",
        choose_by_level("Simple technical repetitions", "Opposed or movement-based repetitions", "Game-speed repetitions with tactical decisions", level),
    ])
    second = section("Rally transfer", ["Build transition from first contact into attack", "Add scoring and serve pressure", "Make players solve ball quality, not just perfect feeds"])
    notes = ["Volleyball sessions should flow through first contact, second contact, and attack whenever possible.", "Even middles and liberos benefit from broad movement quality, not only one narrow skill."]
    return format_plan("Volleyball Session", objective_line(goal, level, focus, context), [warmup, first, second], notes)


def generate_basketball_plan(role, goal, level, injury_status, pain_score, session_time, focus, context, position=None):
    pos = position or "Combo guard / hybrid wing"
    position_map = {
        "Point guard": ["ball security", "pick-and-roll reads", "tempo control", "on-ball defense"],
        "Shooting guard": ["catch-and-shoot", "movement shooting", "secondary creation", "chase defense"],
        "Small forward": ["slashing", "two-way wing play", "spacing reads", "transition finishing"],
        "Power forward": ["screening", "short-roll reads", "rebounding body contact", "help defense"],
        "Center": ["rim finishing", "screen and seal", "rim protection timing", "rebounding"],
        "Combo guard / hybrid wing": ["handle under pressure", "shot creation", "versatile finishing", "switch defense"],
    }
    cues = position_map[pos]
    warmup = section("Warm-up", ["Dynamic prep and ankle / hip readiness", "Ball-handling rhythm", "Form shooting and footwork activation"])
    skill = section("Skill block", [
        f"Position cues: {cues[0]}, {cues[1]}",
        f"Main focus: {focus}",
        choose_by_level("Short technical reps with easy decisions", "Live or semi-live reps with moderate pressure", "Game-speed reps with score / clock constraints", level),
    ])
    game = section("Game application", [
        f"Position cues: {cues[2]}, {cues[3]}",
        "Use 1v1, 2v2, 3v3, or advantage situations rather than endless lines",
        "Finish with free throws or decision-pressure shots when tired",
    ])
    athletic = section("Athletic support", ["Acceleration / deceleration", "Jump and landing control", "Trunk and adductor durability"])
    notes = [
        "Basketball sessions should teach skill in space, speed, and decision-making, not only stationary drills.",
        "Coaches get a focus question instead of a position question by design.",
        "For solo training, use cones, chair defenders, wall passing, and specific shot targets.",
    ]
    return format_plan("Basketball Session", objective_line(goal, level, focus, context), [warmup, skill, game, athletic], notes)


def generate_surfing_plan(role, goal, level, injury_status, pain_score, session_time, focus, context):
    warmup = section("Warm-up", [
        "Shoulder, thoracic spine, hips, ankles",
        "2-3 min light pulse raise",
        "Pop-up movement pattern rehearsal and balance prep",
    ])
    land = section("Land-based block", [
        choose_by_level(
            "2-3 rounds of goblet squat, split squat, dead bug, side plank, and push-up to pop-up",
            "3-4 rounds of squat, hinge, anti-rotation core, single-leg balance, and explosive pop-up reps",
            "4-5 quality rounds of lower-body strength, rotational core, single-leg control, and explosive pop-up work",
            level,
        ),
        "Key surf qualities: lower-body strength, trunk control, shoulder endurance, and balance",
    ])
    water = section("Surf application", [
        "Paddle out with a clear focus instead of just free surfing",
        f"Theme on the waves: {focus}",
        "Catch waves and work on timing, take-off quality, and line choice",
        "Add maneuver intention: bottom turn, top turn, cutback, re-entry, or aerial prep depending on level and conditions",
        "If conditions allow and level fits: get waves and do aerial attempts with control and safe decision-making",
    ])
    finish = section("Finish / reset", [
        "Easy paddle or walk reset",
        "Short shoulder and hip mobility",
        "Quick note: what maneuver or wave choice improved most today?",
    ])
    notes = [
        "Surfing sessions should blend physical preparation with actual wave execution, not only gym work.",
        "On poor wave days, bias the session toward paddling quality, pop-up speed, and line choice.",
        "If the session is dry-land only, replace the water block with extra pop-up, balance, and rotational control work.",
    ]
    return format_plan("Surfing Session", objective_line(goal, level, focus, context), [warmup, land, water, finish], notes)


def generate_plan(role, sport, goal, level, injury_status, pain_score, session_time, sport_inputs, context):
    if sport == "Running":
        return generate_running_plan(role, goal, level, injury_status, pain_score, session_time, sport_inputs["running_focus"], sport_inputs["running_distance"], context, sport_inputs.get("training_days", 4))
    if sport == "Gym":
        return generate_gym_plan(role, goal, level, injury_status, pain_score, session_time, sport_inputs["gym_style"], context, sport_inputs.get("gym_target_sport"))
    if sport == "Tennis":
        return generate_tennis_plan(role, goal, level, injury_status, pain_score, session_time, sport_inputs["tennis_focus"], context, sport_inputs.get("position"))
    if sport == "Baseball":
        return generate_baseball_plan(role, goal, level, injury_status, pain_score, session_time, sport_inputs["baseball_focus"], context, sport_inputs.get("position"))
    if sport == "Rowing":
        return generate_rowing_plan(role, goal, level, injury_status, pain_score, session_time, sport_inputs["rowing_focus"], context)
    if sport == "Weightlifting":
        return generate_weightlifting_plan(role, goal, level, injury_status, pain_score, session_time, sport_inputs["wl_focus"], context)
    if sport == "Water Polo":
        return generate_water_polo_plan(role, goal, level, injury_status, pain_score, session_time, sport_inputs["wp_focus"], context, sport_inputs.get("position"))
    if sport == "Soccer":
        return generate_soccer_plan(role, goal, level, injury_status, pain_score, session_time, sport_inputs["soccer_focus"], sport_inputs.get("position"), sport_inputs.get("age_group"), sport_inputs.get("coach_level"), sport_inputs.get("people_training", 1), context)
    if sport == "Boxing":
        return generate_boxing_plan(role, goal, level, injury_status, pain_score, session_time, sport_inputs["boxing_focus"], context, sport_inputs.get("position"))
    if sport == "Volleyball":
        return generate_volleyball_plan(role, goal, level, injury_status, pain_score, session_time, sport_inputs["volleyball_focus"], context, sport_inputs.get("position"))
    if sport == "Basketball":
        return generate_basketball_plan(role, goal, level, injury_status, pain_score, session_time, sport_inputs["basketball_focus"], context, sport_inputs.get("position"))
    if sport == "Surfing":
        return generate_surfing_plan(role, goal, level, injury_status, pain_score, session_time, sport_inputs["surfing_focus"], context)
    return "Sport not supported yet."


# =========================
# INTERNAL SECTION FALLBACKS
# =========================
def internal_counselling():
    st.header("Counselling")
    counselling_sport = st.selectbox("Choose counselling mode", ["Tennis", "Soccer"])
    if counselling_sport == "Tennis":
        st.write("Manual next-week tennis recommendation mode.")
        c1, c2 = st.columns(2)
        with c1:
            ranking = st.number_input("Your ranking (ATP / ITF approx)", min_value=0, max_value=5000, value=450, step=1)
            location = st.selectbox("Where are you now?", ["South America", "North America", "Europe", "Asia", "Africa", "Oceania"])
        with c2:
            preferred_surface = st.selectbox("Preferred surface", ["Clay", "Hard", "Grass", "No preference"])
            target = st.selectbox("Target level", ["Best fit", "ITF", "Challenger", "ATP Tour"])
        st.markdown("### Manual next-week tournament pool")
        st.write("- ATP 250 level options\n- Challenger options\n- ITF M15/M25 options")
        if st.button("Generate tennis tournament advice", use_container_width=True):
            if ranking <= 120:
                st.success("Best fit: ATP qualifying / strong Challenger scheduling.")
            elif ranking <= 350:
                st.success("Best fit: Challenger main-draw or qualifying logic.")
            else:
                st.success("Best fit: ITF-heavy scheduling with selective Challenger attempts.")
            st.info(f"Surface preference: {preferred_surface} | Current region: {location} | Target level: {target}")
    else:
        st.write("Conservative soccer move recommendation mode.")
        c1, c2 = st.columns(2)
        with c1:
            current_team = st.text_input("Which team are you in now?")
            target_country = st.text_input("Target country")
        with c2:
            current_level = st.selectbox("Current level", ["School / recreational", "Academy / youth competitive", "Semi-pro / amateur senior", "2nd division / strong pro pathway", "1st division / top domestic level"])
            ambition = st.selectbox("Main objective", ["Most realistic development step", "Max minutes and development", "Best level I can still realistically compete in"])
        if st.button("Generate soccer advice", use_container_width=True):
            st.success("Conservative recommendation: choose the next step that gives minutes, fit, and a realistic competitive jump.")
            st.write(f"Current team: {current_team or 'not provided'} | Current level: {current_level} | Target country: {target_country or 'not provided'} | Objective: {ambition}")


def physio_guidance(area, pain_score, symptoms):
    red_flag = any(token in (symptoms or "").lower() for token in ["pop", "numb", "can\'t walk", "cannot walk", "major swelling", "deformity"])
    severity = "Low" if pain_score <= 3 else "Moderate" if pain_score <= 6 else "High"
    library = {
        "Knee": ("quad / calf mobility", "glute + quad activation", "ice or load reduction", "swelling, locking, instability"),
        "Ankle / foot": ("calf / ankle mobility", "single-leg balance", "compression / elevation", "instability, sharp pain with steps"),
        "Hamstring": ("gentle hamstring mobility", "bridges and isometrics", "avoid sprinting for now", "bruising, sharp pull"),
        "Quad": ("quad mobility", "controlled split squat iso", "reduce explosive work", "severe tenderness or swelling"),
        "Hip / groin": ("adductor rock-backs", "isometric squeeze + core", "reduce cutting and striking", "deep groin pain, catching"),
        "Lower back": ("hip flexor / glute mobility", "dead bug + bird dog", "avoid heavy loading", "radiating pain, numbness"),
        "Shoulder": ("thoracic and pec mobility", "scap control", "avoid high-load overhead work", "night pain, weakness, instability"),
        "Elbow / forearm": ("forearm mobility", "grip / extensor work", "reduce repetitive hitting or throwing", "sharp grip pain"),
        "Wrist / hand": ("gentle ROM", "light isometric grip", "brace / unload if needed", "swelling, loss of function"),
        "Neck": ("gentle range of motion", "posture / scap support", "avoid contact or heavy strain", "radiating symptoms, headache after trauma"),
        "Other": ("gentle mobility", "light activation", "reduce aggravating load", "worsening pain or function loss"),
    }
    stretch, mobility, support, watch = library[area]
    return {
        "severity": severity,
        "stretch": stretch,
        "mobility": mobility,
        "support": support,
        "watch": watch,
        "red_flag_found": red_flag,
    }


def internal_physio():
    st.header("Physio")
    st.write("Basic symptom-based support guidance. This is not diagnosis or treatment.")
    p1, p2 = st.columns(2)
    with p1:
        body_area = st.selectbox("Where is the pain?", PHYSIO_BODY_AREAS)
        pain_score = st.slider("Pain scale from 1 to 10", 1, 10, 3)
    with p2:
        symptoms = st.text_area("Describe symptoms", placeholder="Example: tight when I sprint, pain on stairs, slight swelling, heard no pop...")
    if st.button("Generate physio guidance", use_container_width=True):
        guidance = physio_guidance(body_area, pain_score, symptoms)
        st.subheader("Support guidance")
        st.markdown(f"""
- **Severity:** {guidance['severity']}
- **Mobility / stretch idea:** {guidance['stretch']}
- **Movement / exercise idea:** {guidance['mobility']}
- **Support action:** {guidance['support']}
- **Watch for:** {guidance['watch']}
""")
        if guidance["red_flag_found"] or pain_requires_physio(pain_score):
            st.error("There may be red flags or a higher-pain profile here. This should be checked by a qualified professional.")


def internal_video_review():
    st.header("Video Review")
    st.info("Use the separate video_review_section.py file with OpenCV + MediaPipe for the real analyzer. This fallback keeps the app running if that file is missing.")
    uploaded = st.file_uploader("Upload a video", type=["mp4", "mov", "avi", "m4v"])
    sport = st.selectbox("Sport", ["Tennis", "Soccer", "Basketball", "Surfing", "Water Polo", "General"])
    if uploaded:
        st.video(uploaded)
    if st.button("Run review", use_container_width=True):
        st.write(f"Fallback review ready for {sport}. To enable actual analysis, keep video_review_section.py in the same folder as app.py.")


# =========================
# TOP NAVIGATION
# =========================
st.session_state.active_section = st.radio(
    "Choose section",
    SECTION_OPTIONS,
    index=SECTION_OPTIONS.index(st.session_state.active_section),
    horizontal=True,
)


# =========================
# SECTION 1 — TRAINING GENERATOR
# =========================
if st.session_state.active_section == "Training Generator":
    st.header("Training Generator")
    st.markdown("### Main questions")

    role = st.selectbox("Are you a player or coach?", ROLES)
    c1, c2 = st.columns(2)

    trains_alone = "Yes"
    people_training = 1
    age_group = None
    coach_level = None

    with c1:
        if role == "Coach":
            sport = st.selectbox("What sport do you train?", SPORTS)
            goal = "Improve performance"
            level = "Intermediate"
        else:
            sport = st.selectbox("What sport do you want to train?", SPORTS)
            goal = st.selectbox("What is your goal with this sport?", COMMON_GOALS)
            level = st.selectbox("What is your level?", SKILL_LEVELS)

    with c2:
        if role == "Player":
            beginner_or_learning = (goal == "Learn how to play") or (level == "Beginner")
            training_days_label = "How many times do you play sports per week?" if beginner_or_learning else "How many times do you train this sport per week?"
            training_days_default = 3 if beginner_or_learning else 4
            training_days = st.slider(training_days_label, 1, 7, training_days_default)
            injury_status = st.selectbox("Any injury or limitation?", INJURY_OPTIONS)
            pain_score = 0
            if injury_status != "No":
                pain_score = st.slider("Pain scale from 1 to 10", 1, 10, 3)
            session_time = st.selectbox(
                "How much time do you have for this session?",
                TIME_OPTIONS_ENDURANCE if sport in ["Running", "Rowing"] else TIME_OPTIONS_GENERAL,
            )
        else:
            training_days = st.slider("How many times does your team play per week?", 1, 7, 3)
            injury_status = "No"
            pain_score = 0
            session_time = st.selectbox(
                "What's the time of this session?",
                TIME_OPTIONS_ENDURANCE if sport in ["Running", "Rowing"] else TIME_OPTIONS_GENERAL,
            )

    st.markdown("### Training context")
    tc1, tc2 = st.columns(2)
    if role == "Player":
        with tc1:
            if sport in TEAM_SPORTS:
                trains_alone = st.radio("Will this session be mostly solo or with others?", ["Yes", "No"], horizontal=True)
            else:
                trains_alone = st.radio("Will you train alone?", ["Yes", "No"], horizontal=True)
        with tc2:
            if trains_alone == "No":
                people_training = st.number_input("How many more people will train?", min_value=1, max_value=60, value=1, step=1)
            else:
                people_training = 1
    else:
        with tc1:
            age_group = st.selectbox("Age group", AGE_BANDS)
            coach_level = st.slider("Level of the team/player (1 to 10)", 1, 10, 5)
        with tc2:
            people_training = st.number_input("How many players are in the session?", min_value=1, max_value=60, value=12, step=1)

    sport_inputs = {"people_training": people_training, "training_days": training_days}

    st.markdown("### Sport-specific questions")

    # Shared rule: players can be asked position, coaches cannot.
    if role == "Player" and sport in POSITION_SPORTS:
        sport_inputs["position"] = st.selectbox("What position best describes you for this session?", POSITION_MAP[sport])
    elif role == "Coach" and sport in TEAM_SPORTS:
        st.info("For coaches, the app does not ask a player position. Coach sessions use training focus, age band, level, and player count instead.")

    if sport == "Running":
        r1, r2 = st.columns(2)
        with r1:
            sport_inputs["running_focus"] = st.selectbox("What's the focus?", FOCUS_MAP["Running"])
        with r2:
            sport_inputs["running_distance"] = st.selectbox("Choose the event / distance", RUNNING_DISTANCE_MAP[sport_inputs["running_focus"]])

    elif sport == "Gym":
        g1, g2 = st.columns(2)
        with g1:
            sport_inputs["gym_style"] = st.selectbox("What type of gym session do you want?", FOCUS_MAP["Gym"])
        with g2:
            is_specific = st.radio("Do you want this gym session to be sport specific?", ["No", "Yes"], horizontal=True) == "Yes"
            sport_inputs["gym_target_sport"] = st.selectbox("What sport?", GYM_TARGET_SPORTS) if is_specific else None

    elif sport == "Tennis":
        sport_inputs["tennis_focus"] = st.selectbox("What is the main tennis focus today?", FOCUS_MAP["Tennis"])

    elif sport == "Baseball":
        sport_inputs["baseball_focus"] = st.selectbox("What is the main baseball focus today?", FOCUS_MAP["Baseball"])

    elif sport == "Rowing":
        sport_inputs["rowing_focus"] = st.selectbox("What is the main rowing focus today?", FOCUS_MAP["Rowing"])

    elif sport == "Weightlifting":
        sport_inputs["wl_focus"] = st.selectbox("What is the main weightlifting focus today?", FOCUS_MAP["Weightlifting"])

    elif sport == "Water Polo":
        sport_inputs["wp_focus"] = st.selectbox("What is the main water polo focus today?", FOCUS_MAP["Water Polo"])

    elif sport == "Soccer":
        s1, s2 = st.columns(2)
        with s1:
            sport_inputs["soccer_focus"] = st.selectbox("What is the main soccer focus today?", FOCUS_MAP["Soccer"])
        with s2:
            if role == "Coach":
                sport_inputs["age_group"] = age_group
                sport_inputs["coach_level"] = coach_level
                st.info("Coach soccer sessions are shaped by age band, level, player count, and session focus.")
            else:
                st.info("Player soccer sessions are shaped by position, session theme, and solo/group context.")

    elif sport == "Boxing":
        sport_inputs["boxing_focus"] = st.selectbox("What is the main boxing focus today?", FOCUS_MAP["Boxing"])

    elif sport == "Volleyball":
        sport_inputs["volleyball_focus"] = st.selectbox("What is the main volleyball focus today?", FOCUS_MAP["Volleyball"])

    elif sport == "Basketball":
        sport_inputs["basketball_focus"] = st.selectbox("What is the main basketball focus today?", FOCUS_MAP["Basketball"])

    elif sport == "Surfing":
        sport_inputs["surfing_focus"] = st.selectbox("What is the main surfing focus today?", FOCUS_MAP["Surfing"])

    if st.button("Generate training session", use_container_width=True):
        safety = safety_message(injury_status, pain_score) if role == "Player" else None
        if safety:
            st.warning(safety)

        context = get_group_context_text(role, trains_alone, people_training, age_group, coach_level)
        plan = generate_plan(role, sport, goal, level, injury_status, pain_score, session_time, sport_inputs, context)

        st.subheader("Your training plan")
        st.markdown(plan)
        st.caption(
            "This planner gives general training guidance and is not medical advice. "
            "If pain is sharp, worsening, or affecting normal movement, stop and seek qualified help."
        )


# =========================
# SECTION 2 — VIDEO REVIEW
# =========================
elif st.session_state.active_section == "Video Review":
    if external_video_review is not None:
        external_video_review()
    else:
        internal_video_review()


# =========================
# SECTION 3 — COUNSELLING
# =========================
elif st.session_state.active_section == "Counselling":
    if external_counselling is not None:
        external_counselling()
    else:
        internal_counselling()


# =========================
# SECTION 4 — PHYSIO
# =========================
else:
    if external_physio is not None:
        external_physio()
    else:
        internal_physio()
