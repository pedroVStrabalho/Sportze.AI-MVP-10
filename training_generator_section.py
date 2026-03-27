import random
import streamlit as st

# =========================================================
# CORE OPTIONS
# =========================================================
SPORTS = [
    "Soccer", "Basketball", "Tennis", "Water Polo", "Surfing", "Volleyball",
    "Baseball", "Running", "Gym", "Rowing", "Weightlifting", "Boxing",
]

PLAYER_LEVELS = ["Learn how to play", "Beginner", "Intermediate", "Advanced", "Elite"]
COACH_LEVELS = ["Youth / Beginner group", "Developing team", "Competitive team", "High performance team"]
COMMON_GOALS = [
    "Improve performance", "Build fitness", "Return after a break",
    "Technical development", "Competition preparation", "Injury prevention"
]
COMMON_WEAKNESSES = [
    "Consistency", "Technique", "Fitness", "Speed", "Power", "Mobility",
    "Confidence", "Decision-making"
]
SESSION_TYPES = [
    "Balanced session", "High intensity", "Technical emphasis",
    "Physical emphasis", "Tactical emphasis", "Light recovery"
]
EQUIPMENT_OPTIONS = ["Minimal equipment", "Basic equipment", "Full equipment access"]
PERIOD_PHASES = ["Off-season", "Pre-season", "In-season", "Taper / Competition week"]

SOCCER_POSITIONS = [
    "Goalkeeper", "Center Back", "Full Back", "Defensive Midfielder",
    "Central Midfielder", "Attacking Midfielder", "Winger", "Striker"
]
BASKETBALL_POSITIONS = ["Point Guard", "Shooting Guard", "Small Forward", "Power Forward", "Center"]
WATER_POLO_POSITIONS = ["Goalkeeper", "Center Forward", "Center Back", "Driver", "Wing", "Utility"]
VOLLEYBALL_POSITIONS = ["Setter", "Outside Hitter", "Opposite", "Middle Blocker", "Libero", "Defensive Specialist"]
BASEBALL_POSITIONS = [
    "Pitcher", "Catcher", "First Baseman", "Second Baseman", "Third Baseman",
    "Shortstop", "Left Fielder", "Center Fielder", "Right Fielder"
]
BOXING_POSITIONS = ["Out-boxer", "Pressure fighter", "Counterpuncher", "Southpaw specialist", "All-round boxer"]

SPORT_SPECIFIC_GOALS = {
    "Soccer": ["Improve first touch", "Improve finishing", "Improve defending", "Improve crossing and delivery", "Improve passing range", "Improve speed and agility", "Match sharpness"],
    "Basketball": ["Improve shooting", "Improve ball handling", "Improve finishing at the rim", "Improve defense", "Improve rebounding", "Improve explosiveness", "Game conditioning"],
    "Tennis": ["Improve forehand", "Improve backhand", "Improve serve", "Improve return", "Improve movement", "Build match endurance", "Competition sharpness"],
    "Water Polo": ["Improve eggbeater", "Improve shooting", "Improve passing", "Improve counterattack speed", "Improve wrestling strength", "Build swim fitness", "Game sharpness"],
    "Surfing": ["Improve pop-up", "Improve balance", "Improve paddling power", "Improve bottom turns", "Improve aerial confidence", "Improve core control", "Session readiness"],
    "Volleyball": ["Improve serve", "Improve passing", "Improve setting", "Improve blocking", "Improve hitting approach", "Improve jump power", "Match readiness"],
    "Baseball": ["Improve throwing", "Improve hitting", "Improve fielding", "Improve speed", "Improve arm care", "Improve rotational power", "Game readiness"],
    "Running": ["Improve aerobic base", "Improve speed", "Improve threshold", "Improve running economy", "Race preparation", "Return to running"],
    "Gym": ["Build muscle", "Build strength", "Lose fat", "Improve athleticism", "Improve posture", "General fitness"],
    "Rowing": ["Improve stroke efficiency", "Improve power", "Improve aerobic capacity", "Improve start sequence", "Improve mobility", "Race preparation"],
    "Weightlifting": ["Improve snatch", "Improve clean and jerk", "Improve pulling strength", "Improve front squat", "Improve overhead stability", "Competition preparation"],
    "Boxing": ["Improve jab", "Improve combinations", "Improve footwork", "Improve defense", "Improve conditioning", "Fight preparation"],
}

COACH_FOCUS_OPTIONS = {
    "Soccer": ["Team technical session", "Pressing and defensive organization", "Build-up and possession", "Transition game", "Finishing and attacking patterns", "Mixed session"],
    "Basketball": ["Team offense", "Team defense", "Transition offense and defense", "Shooting quality", "Conditioning and competition", "Mixed session"],
    "Tennis": ["Group technical development", "Serve and return emphasis", "Baseline consistency", "Movement and footwork", "Match play scenarios", "Mixed session"],
    "Water Polo": ["Team swim and conditioning", "6v5 and 5v6", "Front-court attack", "Defensive structure", "Counterattack focus", "Mixed session"],
    "Surfing": ["Dry-land technical prep", "Wave reading and timing", "Pop-up and stance mechanics", "Performance surf conditioning", "Competition surf prep", "Mixed session"],
    "Volleyball": ["Serve and pass", "Attack organization", "Blocking and defense", "Transition game", "Jump and conditioning", "Mixed session"],
    "Baseball": ["Throwing and arm care", "Hitting and timing", "Infield defense", "Outfield defense", "Game situations", "Mixed session"],
    "Running": ["Aerobic development", "Speed development", "Threshold session", "Race-week sharpening", "Return-to-run session", "Mixed session"],
    "Gym": ["Hypertrophy session", "Strength session", "Athletic performance session", "Movement quality session", "Full-body general training", "Mixed session"],
    "Rowing": ["Technique session", "Power session", "Aerobic endurance session", "Start and sprint work", "Recovery technique row", "Mixed session"],
    "Weightlifting": ["Snatch emphasis", "Clean and jerk emphasis", "Strength day", "Technique day", "Competition peak", "Mixed session"],
    "Boxing": ["Technical boxing", "Footwork and defense", "Bag and pad conditioning", "Fight-prep intensity", "Light technical recovery", "Mixed session"],
}

SPORT_TRAINING_DAYS_QUESTION = {
    "Soccer": "How many times do you train soccer per week?",
    "Basketball": "How many times do you train basketball per week?",
    "Tennis": "How many times do you train tennis per week?",
    "Water Polo": "How many times do you train water polo per week?",
    "Surfing": "How many times do you surf or train surfing-related work per week?",
    "Volleyball": "How many times do you train volleyball per week?",
    "Baseball": "How many times do you train baseball per week?",
    "Running": "How many running sessions do you do per week?",
    "Gym": "How many gym sessions do you do per week?",
    "Rowing": "How many rowing sessions do you do per week?",
    "Weightlifting": "How many weightlifting sessions do you do per week?",
    "Boxing": "How many boxing sessions do you do per week?",
}

SPORT_POSITIONS = {
    "Soccer": SOCCER_POSITIONS,
    "Basketball": BASKETBALL_POSITIONS,
    "Water Polo": WATER_POLO_POSITIONS,
    "Volleyball": VOLLEYBALL_POSITIONS,
    "Baseball": BASEBALL_POSITIONS,
    "Boxing": BOXING_POSITIONS,
}

GENERIC_COOLDOWNS = [
    "light down-regulation and breathing",
    "mobility for the main muscles used in the session",
    "easy stretching for calves, hips, glutes, and upper back",
    "short reflection: what felt sharp and what needs work next session",
]

RECOVERY_OPTIONS = [
    "easy mobility and tissue care after the session",
    "hydrate well and refuel with a proper meal",
    "walk lightly later in the day to keep the body loose",
    "sleep well to absorb the training",
]

# =========================================================
# SPORT DATA
# =========================================================
SPORT_DATA = {
    "Soccer": {
        "warmup": [
            "ball mastery and first-touch activation",
            "dynamic movement prep with skips, hips, hamstrings, groin, and ankles",
            "acceleration mechanics over 10–20 meters",
            "short passing patterns with body orientation",
        ],
        "technical": [
            "first-touch circuit under pressure",
            "short and medium passing with scanning",
            "finishing from different angles",
            "crossing and finishing pattern",
            "1v1 attacking and defending channel work",
            "receiving on the half-turn and playing forward",
        ],
        "physical": [
            "repeat sprint work",
            "agility and deceleration mechanics",
            "single-leg strength and change-of-direction control",
            "jump and landing mechanics",
            "tempo running or repeated high-speed efforts",
        ],
        "tactical": [
            "small-sided possession game",
            "transition game 4v4+targets",
            "pressing triggers and defensive shape",
            "build-up pattern play from the back",
            "final-third combination play",
        ],
        "coach": [
            "rondo progression with pressing triggers",
            "positional game with limited touches",
            "team defensive block work",
            "finishing pattern to transition wave",
            "11v11 or reduced game with a tactical rule",
        ],
    },
    "Basketball": {
        "warmup": [
            "ball-handling warm-up with both hands",
            "dynamic mobility and ankle-knee-hip prep",
            "layup footwork and rhythm entries",
            "closeout and defensive slide activation",
        ],
        "technical": [
            "stationary and dynamic ball-handling series",
            "form shooting and game-speed shooting",
            "finishing through contact at the rim",
            "pick-and-roll reads",
            "passing on the move with decision-making",
            "defensive stance and mirror drill",
        ],
        "physical": [
            "jump mechanics and landing control",
            "lateral power and slide endurance",
            "short sprint repeaters",
            "single-leg strength and trunk control",
            "court conditioning with change of pace",
        ],
        "tactical": [
            "advantage-disadvantage games",
            "transition offense and sprint-back defense",
            "half-court spacing and ball movement",
            "shell drill for team defense",
            "late-clock decision scenarios",
        ],
        "coach": [
            "team shooting block with constraints",
            "shell defense progression",
            "transition decision-making waves",
            "5v5 half-court offensive rules game",
            "end-of-game scenario competition",
        ],
    },
    "Tennis": {
        "warmup": [
            "mini tennis and hand-eye rhythm build",
            "dynamic mobility for shoulders, thoracic spine, hips, and ankles",
            "split-step and first-step movement prep",
            "shadow swings with balance and posture",
        ],
        "technical": [
            "cross-court forehand consistency",
            "backhand depth and shape drill",
            "serve rhythm and target work",
            "return position and first-strike pattern",
            "approach plus first-volley sequence",
            "directional live-ball consistency drill",
        ],
        "physical": [
            "court movement intervals",
            "reactive first-step work",
            "rotational core and medicine-ball actions",
            "single-leg strength and deceleration control",
            "tennis-specific endurance points",
        ],
        "tactical": [
            "serve plus one patterning",
            "return plus first neutral ball pattern",
            "cross then line point construction",
            "defend-to-neutral transition drill",
            "score-based match play scenarios",
        ],
        "coach": [
            "group feed with target-based consistency",
            "serve and return block",
            "movement and recovery positioning series",
            "live-ball pattern game",
            "competitive tie-break and pressure games",
        ],
    },
    "Water Polo": {
        "warmup": [
            "easy swim and shoulder prep",
            "eggbeater activation",
            "passing rhythm block",
            "mobility and scapular prep",
        ],
        "technical": [
            "passing under pressure",
            "wet shot and skip shot reps",
            "center-forward wrestling and seal work",
            "drive timing and finishing",
            "goalkeeper reaction and leg-set series",
            "counterattack passing lines",
        ],
        "physical": [
            "eggbeater intervals",
            "swim sprint repeaters",
            "tether or resisted swim work",
            "rotational power and shoulder stability",
            "upper-body endurance under fatigue",
        ],
        "tactical": [
            "6v5 execution",
            "5v6 defensive shape",
            "front-court ball movement",
            "counterattack recognition and wave work",
            "press defense and help timing",
        ],
        "coach": [
            "swim set into front-court organization",
            "6v5 and 5v6 block",
            "counterattack wave drill",
            "center-forward / center-back battle sequences",
            "scrimmage with tactical focus",
        ],
    },
    "Surfing": {
        "warmup": [
            "shoulder and thoracic mobility",
            "hip mobility and ankle prep",
            "light paddle activation",
            "pop-up rehearsal with smooth rhythm",
        ],
        "technical": [
            "pop-up technique reps",
            "stance stability on land",
            "balance-board line control",
            "bottom-turn movement pattern",
            "top-turn arm and hip sequencing",
            "aerial takeoff rehearsal on land",
        ],
        "physical": [
            "squats and split squats",
            "rotational core circuit",
            "push-up to pop-up power work",
            "single-leg balance and anti-rotation",
            "paddling strength and shoulder endurance",
        ],
        "tactical": [
            "wave selection practice",
            "timing entry and takeoff decision-making",
            "priority and heat simulation",
            "line choice on forehand vs backhand waves",
            "session planning based on conditions",
        ],
        "coach": [
            "dry-land activation to technical surf prep",
            "pop-up and stance mechanics block",
            "wave-reading discussion and drill block",
            "performance conditioning circuit",
            "water session with focused wave goals",
        ],
    },
    "Volleyball": {
        "warmup": [
            "dynamic ankle-knee-hip prep",
            "shoulder and overhead mobility",
            "approach footwork activation",
            "passing rhythm warm-up",
        ],
        "technical": [
            "serve target work",
            "serve-receive platform control",
            "setting footwork and release drill",
            "approach jump and hitting arm path",
            "blocking footwork and hand position",
            "defense and floor movement",
        ],
        "physical": [
            "jump mechanics and landing control",
            "lateral movement repeaters",
            "single-leg strength",
            "rotational core and overhead stability",
            "conditioning through repeated rally efforts",
        ],
        "tactical": [
            "serve and pass scoring game",
            "transition attack drill",
            "block-defense coordination",
            "side-out structure",
            "free-ball organization",
        ],
        "coach": [
            "serve and pass block",
            "attack pattern progression",
            "blocking system work",
            "transition competition game",
            "6v6 with scoring constraints",
        ],
    },
    "Baseball": {
        "warmup": [
            "throwing prep and shoulder care",
            "dynamic hips and thoracic mobility",
            "glove-hand quickness activation",
            "light sprint mechanics",
        ],
        "technical": [
            "throwing progression",
            "hitting tee and front-toss sequence",
            "ground-ball fielding series",
            "double-play footwork",
            "outfield route and tracking work",
            "pitching command block",
        ],
        "physical": [
            "rotational power work",
            "sprint acceleration",
            "single-leg strength",
            "arm care circuit",
            "trunk stability and anti-rotation",
        ],
        "tactical": [
            "bunt defense and coverage",
            "cutoff and relay communication",
            "first-and-third scenarios",
            "count-based hitting approach",
            "situational scrimmage",
        ],
        "coach": [
            "throwing and arm-care block",
            "defensive station rotation",
            "hitting progression",
            "situational baseball game",
            "base-running competition",
        ],
    },
    "Running": {
        "warmup": [
            "easy jog and mobility build-up",
            "drills for posture, rhythm, and ground contact",
            "strides with relaxed speed",
            "ankle and calf prep",
        ],
        "technical": [
            "cadence and rhythm drill",
            "hill stride mechanics",
            "running economy strides",
            "form-focused tempo segments",
        ],
        "physical": [
            "easy aerobic run",
            "threshold intervals",
            "short fast repetitions",
            "hill sprints",
            "strength circuit for runners",
        ],
        "tactical": [
            "pacing rehearsal",
            "negative split practice",
            "race simulation block",
            "surge and settle workout",
        ],
        "coach": [
            "structured warm-up and drills",
            "main run set with pace groups",
            "form cue reset between reps",
            "controlled cool-down and review",
        ],
    },
    "Gym": {
        "warmup": [
            "full-body mobility flow",
            "activation for glutes, trunk, and upper back",
            "movement rehearsal for the main lifts",
            "easy bike or row pulse raise",
        ],
        "technical": [
            "squat pattern practice",
            "hinge and deadlift pattern",
            "pressing mechanics",
            "pulling and scapular control",
            "tempo-based accessory work",
        ],
        "physical": [
            "compound lift block",
            "hypertrophy accessory circuit",
            "strength endurance finish",
            "carry and core stability work",
        ],
        "tactical": [
            "exercise order and rest management",
            "superset structure",
            "density block management",
        ],
        "coach": [
            "movement prep",
            "main lift block",
            "accessory hypertrophy or strength circuit",
            "conditioning finisher",
        ],
    },
    "Rowing": {
        "warmup": [
            "easy row and mobility",
            "sequencing of legs-trunk-arms",
            "hip and thoracic prep",
            "light stroke build-ups",
        ],
        "technical": [
            "catch timing drill",
            "drive sequence focus",
            "finish and recovery rhythm",
            "rate control work",
            "blade placement consistency",
        ],
        "physical": [
            "steady aerobic row",
            "power intervals",
            "start sequence repeats",
            "strength circuit for posterior chain and trunk",
        ],
        "tactical": [
            "race-rate exposure",
            "start plus settle pattern",
            "middle-500 rhythm practice",
            "sprint finish rehearsal",
        ],
        "coach": [
            "technical row with cues",
            "main interval block",
            "race-piece or power block",
            "cool-down and review",
        ],
    },
    "Weightlifting": {
        "warmup": [
            "ankle, hip, thoracic, and overhead mobility",
            "barbell movement prep",
            "speed under the bar rehearsal",
            "trunk and front-rack activation",
        ],
        "technical": [
            "snatch technique block",
            "clean and jerk technique block",
            "pull variation",
            "front squat or back squat",
            "overhead stability work",
        ],
        "physical": [
            "strength block",
            "power pulls",
            "squat volume",
            "posterior-chain accessory work",
        ],
        "tactical": [
            "attempt selection rehearsal",
            "competition rhythm practice",
            "lifting under time constraint",
        ],
        "coach": [
            "barbell warm-up flow",
            "main technical lift",
            "strength lift",
            "accessory and mobility finish",
        ],
    },
    "Boxing": {
        "warmup": [
            "rope skip and pulse raise",
            "mobility for ankles, hips, thoracic spine, and shoulders",
            "shadow boxing with rhythm",
            "reaction and footwork activation",
        ],
        "technical": [
            "jab mechanics and sharpness",
            "1-2 and 1-2-hook combinations",
            "defense slips, rolls, and blocks",
            "distance control and pivoting",
            "bag rounds with a tactical target",
            "padwork rhythm block",
        ],
        "physical": [
            "boxing conditioning rounds",
            "sprint intervals",
            "medicine-ball rotational power",
            "bodyweight strength endurance circuit",
            "neck, trunk, and shoulder resilience work",
        ],
        "tactical": [
            "countering after defense",
            "ring-cutting practice",
            "lead-hand control",
            "southpaw vs orthodox adjustment work",
            "scenario sparring constraints",
        ],
        "coach": [
            "shadow and technical cue block",
            "bag or pad rounds",
            "defense and footwork progression",
            "controlled spar or scenario rounds",
        ],
    },
}

POSITION_NOTES = {
    "Soccer": {
        "Goalkeeper": ["prioritize set position, handling, footwork, and reaction saves", "include distribution work with both short and long passing"],
        "Center Back": ["prioritize body shape, defending duels, clearances, and line leadership", "include aerial timing and longer passing into midfield"],
        "Full Back": ["prioritize repeated overlap-underlap running, crossing, and recovery speed", "include 1v1 defending in wide channels"],
        "Defensive Midfielder": ["prioritize scanning, receiving under pressure, and defensive balance", "include short passing speed and transition control"],
        "Central Midfielder": ["prioritize scanning, rhythm control, and box-to-box repeat efforts", "include receiving on the turn and forward passing choices"],
        "Attacking Midfielder": ["prioritize half-turn receiving, final pass, and shooting around the box", "include tight-space decision-making"],
        "Winger": ["prioritize 1v1 attacking, acceleration, crossing, and back-post timing", "include recovery pressing and repeated sprint ability"],
        "Striker": ["prioritize finishing, movement across defenders, and pressing from the front", "include explosive separation and first-touch finishing"],
    },
    "Basketball": {
        "Point Guard": ["prioritize handle under pressure, pace control, and decision-making", "include pick-and-roll reads and drive-kick passing"],
        "Shooting Guard": ["prioritize catch-and-shoot quality, relocation, and secondary creation", "include closeout attack and perimeter defense"],
        "Small Forward": ["prioritize two-way wing actions, finishing, and versatile defense", "include transition scoring and rebounding effort"],
        "Power Forward": ["prioritize interior finishing, screening, rebounding, and defensive switches", "include short-roll decisions and contact tolerance"],
        "Center": ["prioritize rim protection, post finishing, screening, and rebounding", "include sprint-to-rim and paint touch conditioning"],
    },
    "Water Polo": {
        "Goalkeeper": ["prioritize leg endurance, angles, hand speed, and outlet passing", "include reaction-save sequences and communication"],
        "Center Forward": ["prioritize seal position, wrestling strength, close-range finishing", "include holding water under contact"],
        "Center Back": ["prioritize body position, leverage, and fronting awareness", "include strength-endurance and foul management habits"],
        "Driver": ["prioritize explosive movement, timing, and catch-shoot quality", "include counterattack speed and passing under fatigue"],
        "Wing": ["prioritize passing angles, outside shot readiness, and quick re-locate actions", "include support movement and transition habits"],
        "Utility": ["prioritize all-round adaptability and rapid role switching", "include mixed technical reps across perimeter and inside roles"],
    },
    "Volleyball": {
        "Setter": ["prioritize footwork to the ball, release consistency, and decision speed", "include movement from imperfect passes"],
        "Outside Hitter": ["prioritize serve receive, high-ball hitting, and repeat jump quality", "include block-defense transition"],
        "Opposite": ["prioritize terminal hitting, blocking, and transition power", "include attack timing from the right side"],
        "Middle Blocker": ["prioritize first-step block movement and quick attack timing", "include landing control and repeated explosive actions"],
        "Libero": ["prioritize platform angle, reading, and low defensive posture", "include floor defense reaction work"],
        "Defensive Specialist": ["prioritize serve receive, reading, and coverage movement", "include quick platform stability under pressure"],
    },
    "Baseball": {
        "Pitcher": ["prioritize command, sequencing, lower-body force transfer, and arm care", "keep throwing volume intelligent"],
        "Catcher": ["prioritize receiving, blocking, transfer speed, and leadership", "include hip mobility and repeat squat endurance"],
        "First Baseman": ["prioritize footwork around the bag and pick timing", "include lateral range and glove presentation"],
        "Second Baseman": ["prioritize double-play footwork, quick release, and range", "include first-step quickness"],
        "Third Baseman": ["prioritize reaction speed, short-hop handling, and strong throws", "include explosive first movement"],
        "Shortstop": ["prioritize range, body control, and throw-from-different-angles skill", "include leadership and clean glove-to-hand transfer"],
        "Left Fielder": ["prioritize reads off the bat and throwing mechanics", "include route efficiency and communication"],
        "Center Fielder": ["prioritize range, leadership, and high-speed tracking", "include top-end sprint mechanics"],
        "Right Fielder": ["prioritize strong throwing and route discipline", "include reads, crow-hop timing, and boundary awareness"],
    },
    "Boxing": {
        "Out-boxer": ["prioritize range control, jab volume, and footwork", "include exit angles after scoring"],
        "Pressure fighter": ["prioritize forward balance, body work, and ring cutting", "include work-rate conditioning"],
        "Counterpuncher": ["prioritize timing, defensive reads, and response speed", "include scenario spar with deliberate counters"],
        "Southpaw specialist": ["prioritize lead-foot battle awareness and angle creation", "include matchup-specific positioning"],
        "All-round boxer": ["prioritize adaptability and role switching between lead and counter phases", "include balanced technical volume"],
    },
}

# =========================================================
# HELPERS
# =========================================================
def choose(lst, n=1):
    if not lst:
        return []
    n = min(n, len(lst))
    return random.sample(lst, n)

def format_block(title, items):
    st.markdown(f"### {title}")
    for item in items:
        st.write(f"- {item}")

def add_volume_note(level, session_type, duration):
    if level in ["Learn how to play", "Beginner"]:
        return f"Keep the session controlled. Prioritize quality over volume for this {duration}-minute session."
    if session_type == "High intensity":
        return f"This is a demanding session. Keep quality high and rest honestly between hard actions within the {duration}-minute total."
    if session_type == "Light recovery":
        return f"This session should feel smooth and controlled. The main target inside {duration} minutes is recovery and clean movement."
    return f"Manage intensity well so the session stays productive across the full {duration} minutes."

def add_phase_note(phase):
    mapping = {
        "Off-season": "Use this block to build qualities and fix weaknesses with slightly higher training load.",
        "Pre-season": "Use this block to blend physical work with more sport-specific actions and sharper intensity.",
        "In-season": "Keep the session efficient and specific. Quality matters more than adding random extra volume.",
        "Taper / Competition week": "Reduce unnecessary fatigue. Keep intensity crisp, but total volume controlled.",
    }
    return mapping.get(phase, "")

def add_equipment_note(equipment):
    mapping = {
        "Minimal equipment": "Session is shaped so it can still work with very limited equipment.",
        "Basic equipment": "Session assumes access to standard training tools and a normal practice space.",
        "Full equipment access": "Session can include the full technical and physical menu because equipment access is complete.",
    }
    return mapping.get(equipment, "")

def add_return_note(goal):
    return "Because this is a return-after-break session, start slightly below your maximum level and build back gradually." if goal == "Return after a break" else ""

def build_notes(notes):
    notes = [n for n in notes if n]
    if notes:
        format_block("Session Notes", notes)

def session_header(role, sport, level, goal, session_type):
    st.subheader("Generated Session")
    st.write(f"**Role:** {role}")
    st.write(f"**Sport:** {sport}")
    st.write(f"**Level:** {level}")
    st.write(f"**Goal:** {goal}")
    st.write(f"**Session Style:** {session_type}")

def scale_modifier(level, session_type, phase, goal):
    score = 0
    if level in ["Intermediate"]:
        score += 1
    elif level in ["Advanced", "Elite", "Competitive team", "High performance team"]:
        score += 2

    if session_type == "High intensity":
        score += 2
    elif session_type in ["Technical emphasis", "Tactical emphasis", "Physical emphasis"]:
        score += 1
    elif session_type == "Light recovery":
        score -= 2

    if phase == "Off-season":
        score += 1
    elif phase == "Taper / Competition week":
        score -= 1

    if goal in ["Competition preparation", "Improve performance", "Fight preparation", "Game conditioning", "Race preparation"]:
        score += 1
    if goal == "Return after a break":
        score -= 2

    return max(-2, min(3, score))

def bump(value, delta, minimum=1):
    return max(minimum, value + delta)

def allocate_block_minutes(duration, role):
    if role == "Coach":
        warmup = int(duration * 0.18)
        main = int(duration * 0.64)
        cooldown = int(duration * 0.10)
        review = duration - warmup - main - cooldown
    else:
        warmup = int(duration * 0.20)
        main = int(duration * 0.60)
        cooldown = int(duration * 0.10)
        review = duration - warmup - main - cooldown
    return warmup, main, cooldown, review

# =========================================================
# PRESCRIPTION ENGINE
# Every exercise gets sets / reps / minutes / distance
# =========================================================
def prescribe_exercise(name, section, sport, level, session_type, phase, duration, role="Player"):
    n = name.lower()
    mod = scale_modifier(level, session_type, phase, "")
    high = session_type == "High intensity"
    recovery = session_type == "Light recovery"

    # ---------- warm-up ----------
    if section == "warmup":
        if any(k in n for k in ["mobility", "prep", "activation", "flow", "shoulder prep", "scapular", "thoracic", "ankle", "hip"]):
            mins = bump(4, mod, 3)
            return f"{name} — {mins} min continuous"
        if any(k in n for k in ["mechanics", "shadow", "rehearsal", "footwork", "body orientation", "split-step"]):
            sets = bump(2, mod, 2)
            reps = 4 if sport in ["Soccer", "Basketball", "Volleyball", "Boxing"] else 6
            return f"{name} — {sets} sets x {reps} reps"
        if any(k in n for k in ["easy swim", "easy jog", "easy row", "pulse raise", "bike", "light paddle"]):
            mins = 5 if recovery else 6 + max(0, mod)
            return f"{name} — {mins} min"
        if any(k in n for k in ["ball mastery", "ball-handling", "mini tennis", "passing rhythm", "passing patterns"]):
            sets = 3
            sec = 60 if recovery else 75 + max(0, mod) * 15
            return f"{name} — {sets} rounds x {sec} sec"
        return f"{name} — 2 to 3 sets x 45 to 60 sec"

    # ---------- technical ----------
    if section == "technical":
        if sport == "Soccer":
            if "finishing" in n:
                reps = bump(8, mod * 2, 6)
                sets = 3 if not recovery else 2
                return f"{name} — {sets} sets x {reps} finishes"
            if "crossing" in n:
                return f"{name} — 3 sets x 6 deliveries each side"
            if "1v1" in n:
                rounds = 6 if high else 5
                return f"{name} — {rounds} rounds x 20 sec work / 40 sec rest"
            if "passing" in n or "first-touch" in n or "receiving" in n:
                return f"{name} — 3 sets x 4 min with 60 sec rest"
        elif sport == "Basketball":
            if "shooting" in n:
                makes = 25 if recovery else bump(35, mod * 5, 20)
                return f"{name} — {makes} made shots"
            if "ball-handling" in n:
                return f"{name} — 4 rounds x 45 sec each pattern"
            if "finishing" in n:
                return f"{name} — 3 sets x 10 finishes each side"
            if "pick-and-roll" in n or "passing" in n or "defensive stance" in n:
                return f"{name} — 4 sets x 3 min"
        elif sport == "Tennis":
            if "serve" in n:
                balls = 30 if recovery else bump(45, mod * 10, 20)
                return f"{name} — {balls} serves"
            if "return" in n:
                return f"{name} — 4 sets x 8 returns each side"
            if "forehand" in n or "backhand" in n:
                return f"{name} — 4 sets x 4 min live-ball"
            if "approach" in n or "directional" in n:
                return f"{name} — 3 sets x 6 points"
        elif sport == "Water Polo":
            if "passing" in n:
                return f"{name} — 4 sets x 2 min"
            if "shot" in n or "shooting" in n or "finishing" in n:
                return f"{name} — 3 sets x 8 shots"
            if "wrestling" in n or "seal work" in n:
                return f"{name} — 5 rounds x 20 sec work / 40 sec rest"
            if "goalkeeper" in n:
                return f"{name} — 4 sets x 6 reaction reps"
        elif sport == "Surfing":
            if "pop-up" in n:
                reps = bump(8, mod * 2, 6)
                return f"{name} — 3 sets x {reps} reps"
            if "balance" in n or "stance" in n:
                return f"{name} — 4 rounds x 40 sec"
            if "turn" in n or "sequencing" in n:
                return f"{name} — 3 sets x 6 reps each side"
            if "aerial" in n:
                return f"{name} — 3 sets x 5 rehearsals"
        elif sport == "Volleyball":
            if "serve" in n:
                return f"{name} — 30 serves total"
            if "passing" in n or "platform" in n:
                return f"{name} — 4 sets x 12 contacts"
            if "setting" in n:
                return f"{name} — 4 sets x 15 sets"
            if "hitting" in n or "approach" in n:
                return f"{name} — 4 sets x 6 attacks"
            if "blocking" in n:
                return f"{name} — 4 sets x 6 reps"
            if "defense" in n:
                return f"{name} — 4 rounds x 90 sec"
        elif sport == "Baseball":
            if "throwing" in n:
                return f"{name} — 25 to 35 throws"
            if "hitting" in n:
                return f"{name} — 4 rounds x 10 swings"
            if "fielding" in n:
                return f"{name} — 4 sets x 8 reps"
            if "double-play" in n:
                return f"{name} — 4 sets x 6 reps"
            if "outfield" in n:
                return f"{name} — 4 sets x 5 balls"
            if "pitching" in n:
                return f"{name} — 20 to 25 pitches"
        elif sport == "Running":
            if "cadence" in n or "rhythm" in n or "form-focused" in n:
                return f"{name} — 4 reps x 2 min"
            if "hill stride" in n:
                return f"{name} — 6 reps x 10 sec uphill"
            if "running economy" in n:
                return f"{name} — 6 strides x 80 m"
        elif sport == "Gym":
            if "squat pattern" in n or "hinge" in n or "pressing mechanics" in n or "pulling" in n:
                return f"{name} — 3 sets x 8 reps"
            if "tempo-based accessory" in n:
                return f"{name} — 3 sets x 10 reps"
        elif sport == "Rowing":
            if "drill" in n or "timing" in n or "sequence" in n or "rhythm" in n or "blade placement" in n:
                return f"{name} — 4 sets x 3 min"
        elif sport == "Weightlifting":
            if "snatch" in n:
                return f"{name} — 5 sets x 2 reps"
            if "clean and jerk" in n:
                return f"{name} — 5 sets x 1+1"
            if "pull variation" in n:
                return f"{name} — 4 sets x 3 reps"
            if "squat" in n:
                return f"{name} — 4 sets x 4 reps"
            if "overhead stability" in n:
                return f"{name} — 3 sets x 6 reps"
        elif sport == "Boxing":
            if "jab" in n or "combination" in n or "defense" in n or "distance control" in n:
                rounds = 4 if not recovery else 3
                return f"{name} — {rounds} rounds x 2 min"
            if "bag rounds" in n or "padwork" in n:
                rounds = 5 if high else 4
                return f"{name} — {rounds} rounds x 2 min"

        return f"{name} — 3 to 4 sets x 4 to 6 min"

    # ---------- physical ----------
    if section == "physical":
        if any(k in n for k in ["sprint", "repeat sprint", "repeaters"]):
            reps = 6 if recovery else bump(8, mod, 5)
            dist = "15–20 m" if sport in ["Soccer", "Basketball", "Volleyball", "Baseball"] else "25–40 m"
            return f"{name} — {reps} reps x {dist}, full walk-back recovery"
        if any(k in n for k in ["agility", "deceleration", "landing", "jump mechanics", "lateral movement"]):
            return f"{name} — 4 sets x 5 reps"
        if any(k in n for k in ["strength", "single-leg", "squats", "split squats", "compound lift", "squat volume", "strength block", "front squat", "back squat"]):
            sets = 3 if recovery else bump(4, mod, 3)
            reps = 8 if sport in ["Gym", "Surfing", "Baseball"] else 5
            return f"{name} — {sets} sets x {reps} reps"
        if any(k in n for k in ["tempo running", "high-speed efforts"]):
            return f"{name} — 6 reps x 30 sec work / 45 sec rest"
        if "easy aerobic run" in n:
            mins = 20 if recovery else 25 + max(0, mod) * 5
            return f"{name} — {mins} min"
        if "threshold intervals" in n:
            return f"{name} — 4 reps x 4 min with 90 sec jog recovery"
        if "short fast repetitions" in n:
            return f"{name} — 8 reps x 200 m with 60 sec rest"
        if "hill sprints" in n:
            return f"{name} — 8 reps x 10 sec uphill"
        if "strength circuit for runners" in n:
            return f"{name} — 3 rounds x 5 exercises x 30 sec each"
        if "court movement intervals" in n:
            return f"{name} — 6 reps x 30 sec work / 30 sec rest"
        if "reactive first-step work" in n:
            return f"{name} — 4 sets x 5 reps each side"
        if "medicine-ball" in n or "rotational power" in n:
            return f"{name} — 4 sets x 6 reps each side"
        if "eggbeater intervals" in n:
            return f"{name} — 6 reps x 30 sec work / 30 sec rest"
        if "swim sprint" in n:
            return f"{name} — 8 reps x 15 m with 20 sec rest"
        if "resisted swim" in n:
            return f"{name} — 6 reps x 12 sec"
        if "upper-body endurance" in n:
            return f"{name} — 3 rounds x 45 sec"
        if "conditioning through repeated rally efforts" in n:
            return f"{name} — 5 rounds x 75 sec work / 45 sec rest"
        if "arm care" in n:
            return f"{name} — 2 to 3 rounds x 12 reps each exercise"
        if "trunk stability" in n or "anti-rotation" in n or "core stability" in n:
            return f"{name} — 3 sets x 30 to 40 sec"
        if "steady aerobic row" in n:
            return f"{name} — 20 min continuous"
        if "power intervals" in n:
            return f"{name} — 6 reps x 1 min hard / 1 min easy"
        if "start sequence repeats" in n:
            return f"{name} — 5 reps x 20 strokes"
        if "posterior-chain accessory" in n:
            return f"{name} — 3 sets x 8 reps"
        if "power pulls" in n:
            return f"{name} — 4 sets x 3 reps"
        if "boxing conditioning rounds" in n:
            rounds = 5 if high else 4
            return f"{name} — {rounds} rounds x 2 min / 1 min rest"
        if "sprint intervals" in n and sport == "Boxing":
            return f"{name} — 8 reps x 15 sec sprint / 45 sec walk"
        if "bodyweight strength endurance circuit" in n:
            return f"{name} — 3 rounds x 5 exercises x 30 sec"
        if "neck, trunk, and shoulder resilience" in n:
            return f"{name} — 2 rounds x 12 reps each"

        return f"{name} — 3 to 4 sets x 6 to 10 reps"

    # ---------- tactical ----------
    if section == "tactical":
        if sport == "Soccer":
            return f"{name} — 4 rounds x 4 min with 90 sec rest"
        if sport == "Basketball":
            return f"{name} — 4 rounds x 3 min"
        if sport == "Tennis":
            return f"{name} — 4 sets x 6 points"
        if sport == "Water Polo":
            return f"{name} — 4 rounds x 2 min"
        if sport == "Surfing":
            return f"{name} — 3 rounds x 4 min"
        if sport == "Volleyball":
            return f"{name} — 4 rounds x 8 rallies"
        if sport == "Baseball":
            return f"{name} — 4 sets x 5 reps"
        if sport == "Running":
            if "pacing" in n or "negative split" in n:
                return f"{name} — 3 reps x 5 min"
            if "race simulation" in n:
                return f"{name} — 12 min continuous"
            return f"{name} — 4 reps x 3 min"
        if sport == "Gym":
            return f"{name} — 3 blocks x 6 min"
        if sport == "Rowing":
            return f"{name} — 4 reps x 2 min"
        if sport == "Weightlifting":
            return f"{name} — 4 sets x 1 attempt sequence"
        if sport == "Boxing":
            return f"{name} — 4 rounds x 2 min"
        return f"{name} — 3 to 4 rounds x 3 min"

    # ---------- coach ----------
    if section == "coach":
        if sport == "Soccer":
            if "11v11" in n or "reduced game" in n:
                return f"{name} — 3 games x 6 min"
            return f"{name} — 4 blocks x 4 min"
        if sport == "Basketball":
            return f"{name} — 4 blocks x 4 min"
        if sport == "Tennis":
            return f"{name} — 4 stations x 5 min"
        if sport == "Water Polo":
            return f"{name} — 4 blocks x 3 min"
        if sport == "Surfing":
            return f"{name} — 3 blocks x 6 min"
        if sport == "Volleyball":
            return f"{name} — 4 rounds x 10 rallies"
        if sport == "Baseball":
            return f"{name} — 4 stations x 6 reps"
        if sport == "Running":
            return f"{name} — 4 reps x 4 min"
        if sport == "Gym":
            return f"{name} — 4 sets x 8 reps"
        if sport == "Rowing":
            return f"{name} — 4 reps x 4 min"
        if sport == "Weightlifting":
            return f"{name} — 5 sets x 2 reps"
        if sport == "Boxing":
            return f"{name} — 4 rounds x 2 min"
        return f"{name} — 4 sets x 4 min"

    # ---------- cooldown ----------
    if section == "cooldown":
        if "breathing" in n:
            return f"{name} — 3 min"
        if "mobility" in n or "stretch" in n:
            return f"{name} — 2 rounds x 30 sec per position"
        if "reflection" in n:
            return f"{name} — 2 min"
        return f"{name} — 3 to 5 min"

    # ---------- recovery ----------
    if section == "recovery":
        if "mobility" in n or "tissue care" in n:
            return f"{name} — 8 to 10 min later in the day"
        if "hydrate" in n or "meal" in n:
            return f"{name} — within 30 to 60 min post-session"
        if "walk" in n:
            return f"{name} — 10 to 15 min easy walk"
        if "sleep" in n:
            return f"{name} — target 8+ hours"
        return f"{name} — complete after training"

    return name

def prescribe_list(items, section, sport, level, session_type, phase, duration, role="Player"):
    return [
        f"{item} — {prescribe_exercise(item, section, sport, level, session_type, phase, duration, role).split(' — ', 1)[1]}"
        if " — " in prescribe_exercise(item, section, sport, level, session_type, phase, duration, role)
        else prescribe_exercise(item, section, sport, level, session_type, phase, duration, role)
        for item in items
    ]

# =========================================================
# SESSION BUILDERS
# =========================================================
def build_player_session(sport, level, position, goal, sport_goal, weakness, session_type, equipment, phase, days_per_week, duration):
    bank = SPORT_DATA[sport]
    warmup_raw = choose(bank["warmup"], 3)
    technical_raw = choose(bank["technical"], 3)
    physical_raw = choose(bank["physical"], 2)
    tactical_raw = choose(bank["tactical"], 2)
    cooldown_raw = choose(GENERIC_COOLDOWNS, 2)
    recovery_raw = choose(RECOVERY_OPTIONS, 2)

    if session_type == "Technical emphasis":
        main_raw = technical_raw + choose(tactical_raw, 1) + choose(physical_raw, 1)
    elif session_type == "Physical emphasis":
        main_raw = physical_raw + choose(technical_raw, 2) + choose(tactical_raw, 1)
    elif session_type == "Tactical emphasis":
        main_raw = tactical_raw + choose(technical_raw, 2) + choose(physical_raw, 1)
    elif session_type == "Light recovery":
        main_raw = choose(technical_raw, 2) + ["reduced-load controlled execution"] + choose(physical_raw, 1)
    elif session_type == "High intensity":
        main_raw = choose(technical_raw, 2) + choose(physical_raw, 2) + choose(tactical_raw, 2)
    else:
        main_raw = choose(technical_raw, 2) + choose(physical_raw, 1) + choose(tactical_raw, 1)

    warmup = prescribe_list(warmup_raw, "warmup", sport, level, session_type, phase, duration, role="Player")
    main_focus = []
    for item in main_raw:
        if item in bank["technical"]:
            main_focus.append(f"{item} — {prescribe_exercise(item, 'technical', sport, level, session_type, phase, duration, 'Player').split(' — ', 1)[1]}")
        elif item in bank["physical"]:
            main_focus.append(f"{item} — {prescribe_exercise(item, 'physical', sport, level, session_type, phase, duration, 'Player').split(' — ', 1)[1]}")
        elif item in bank["tactical"]:
            main_focus.append(f"{item} — {prescribe_exercise(item, 'tactical', sport, level, session_type, phase, duration, 'Player').split(' — ', 1)[1]}")
        else:
            main_focus.append(f"{item} — 2 to 3 sets x 4 min")

    cooldown = prescribe_list(cooldown_raw, "cooldown", sport, level, session_type, phase, duration, role="Player")
    recovery = prescribe_list(recovery_raw, "recovery", sport, level, session_type, phase, duration, role="Player")

    warmup_mins, main_mins, cooldown_mins, review_mins = allocate_block_minutes(duration, "Player")

    notes = [
        add_volume_note(level, session_type, duration),
        add_phase_note(phase),
        add_equipment_note(equipment),
        add_return_note(goal),
        f"Weekly frequency context: {days_per_week} session(s) per week.",
        f"Time structure target: ~{warmup_mins} min warm-up, ~{main_mins} min main work, ~{cooldown_mins} min cool-down, ~{review_mins} min transition / review.",
        f"Main session focus selected: {sport_goal}.",
    ]
    if weakness != "None":
        notes.append(f"Extra correction priority today: {weakness.lower()}.")
    if position and sport in POSITION_NOTES and position in POSITION_NOTES[sport]:
        notes.extend(POSITION_NOTES[sport][position])

    intensity = "Moderate"
    if session_type == "High intensity":
        intensity = "High"
    elif session_type == "Light recovery":
        intensity = "Low to Moderate"
    elif level in ["Advanced", "Elite"] and goal in ["Competition preparation", "Improve performance"]:
        intensity = "Moderate to High"

    return {
        "session_name": f"{sport} {sport_goal} Session",
        "warmup": warmup,
        "main_focus": main_focus,
        "cooldown": cooldown,
        "recovery": recovery,
        "notes": notes,
        "intensity": intensity,
        "duration": duration,
    }

def build_coach_session(sport, level, focus, weakness, session_type, equipment, phase, days_per_week, duration):
    bank = SPORT_DATA[sport]
    warmup_raw = choose(bank["warmup"], 3)
    coach_menu_raw = choose(bank["coach"], 4)
    technical_raw = choose(bank["technical"], 2)
    tactical_raw = choose(bank["tactical"], 2)
    physical_raw = choose(bank["physical"], 1)
    cooldown_raw = choose(GENERIC_COOLDOWNS, 2)
    recovery_raw = choose(RECOVERY_OPTIONS, 2)

    if "technical" in focus.lower():
        main_raw = choose(technical_raw, 2) + coach_menu_raw[:2] + choose(physical_raw, 1)
    elif "defense" in focus.lower():
        main_raw = choose(tactical_raw, 2) + coach_menu_raw[:2] + choose(physical_raw, 1)
    elif any(x in focus.lower() for x in ["conditioning", "power", "endurance", "jump"]):
        main_raw = choose(physical_raw, 1) + coach_menu_raw[:3] + choose(technical_raw, 1)
    else:
        main_raw = coach_menu_raw + choose(tactical_raw, 1)

    warmup = prescribe_list(warmup_raw, "warmup", sport, level, session_type, phase, duration, role="Coach")
    main_focus = []
    for item in main_raw:
        if item in bank["coach"]:
            main_focus.append(f"{item} — {prescribe_exercise(item, 'coach', sport, level, session_type, phase, duration, 'Coach').split(' — ', 1)[1]}")
        elif item in bank["technical"]:
            main_focus.append(f"{item} — {prescribe_exercise(item, 'technical', sport, level, session_type, phase, duration, 'Coach').split(' — ', 1)[1]}")
        elif item in bank["physical"]:
            main_focus.append(f"{item} — {prescribe_exercise(item, 'physical', sport, level, session_type, phase, duration, 'Coach').split(' — ', 1)[1]}")
        elif item in bank["tactical"]:
            main_focus.append(f"{item} — {prescribe_exercise(item, 'tactical', sport, level, session_type, phase, duration, 'Coach').split(' — ', 1)[1]}")
        else:
            main_focus.append(f"{item} — 3 to 4 blocks x 4 min")

    cooldown = prescribe_list(cooldown_raw, "cooldown", sport, level, session_type, phase, duration, role="Coach")
    recovery = prescribe_list(recovery_raw, "recovery", sport, level, session_type, phase, duration, role="Coach")

    warmup_mins, main_mins, cooldown_mins, review_mins = allocate_block_minutes(duration, "Coach")

    notes = [
        f"This is a coach-led session for a {level.lower()} group.",
        f"Weekly team frequency context: {days_per_week} session(s) per week.",
        add_phase_note(phase),
        add_equipment_note(equipment),
        f"Time structure target: ~{warmup_mins} min warm-up, ~{main_mins} min main work, ~{cooldown_mins} min cool-down, ~{review_mins} min transition / review.",
        f"Team focus selected: {focus}.",
    ]
    if weakness != "None":
        notes.append(f"Team correction priority: {weakness.lower()}.")

    return {
        "session_name": f"{sport} Coach Session - {focus}",
        "warmup": warmup,
        "main_focus": main_focus,
        "cooldown": cooldown,
        "recovery": recovery,
        "notes": notes,
        "intensity": "Moderate" if session_type != "High intensity" else "Moderate to High",
        "duration": duration,
    }

# =========================================================
# RENDER
# =========================================================
def render_session_plan(session):
    st.markdown(f"## {session['session_name']}")
    st.write(f"**Estimated Duration:** {session['duration']} minutes")
    st.write(f"**Suggested Intensity:** {session['intensity']}")
    format_block("Warm-Up", session["warmup"])
    format_block("Main Session", session["main_focus"])
    format_block("Cool-Down", session["cooldown"])
    format_block("Recovery Guidance", session["recovery"])
    build_notes(session["notes"])

def render_weekly_microcycle(sport, role, level, goal, phase, days_per_week):
    st.markdown("## Weekly Training Suggestion")
    if days_per_week <= 1:
        days = [f"Day 1: Main {sport.lower()} session with technical priority and controlled physical work"]
    elif days_per_week == 2:
        days = [
            f"Day 1: Main {sport.lower()} technical and quality session",
            f"Day 2: Secondary session with conditioning, tactical execution, and controlled volume"
        ]
    elif days_per_week == 3:
        days = [
            "Day 1: High-quality technical session",
            "Day 2: Physical and tactical support session",
            "Day 3: Competition-like or sharper execution session"
        ]
    elif days_per_week == 4:
        days = [
            "Day 1: Technical emphasis",
            "Day 2: Physical emphasis",
            "Day 3: Tactical or match-play emphasis",
            "Day 4: Controlled sharpen / recovery-quality session"
        ]
    else:
        days = [
            "Day 1: Technical quality",
            "Day 2: Physical development",
            "Day 3: Tactical execution",
            "Day 4: Technical reinforcement",
            "Day 5: Competition simulation or sharper work"
        ]
        if days_per_week >= 6:
            days.append("Day 6: Light recovery, mobility, or low-load technical touch")
        if days_per_week >= 7:
            days.append("Day 7: Full recovery or very light regeneration block")

    for day in days:
        st.write(f"- {day}")
    st.caption(f"This weekly outline is adjusted to the {phase.lower()} phase for a {role.lower()} focused on {goal.lower()}.")

# =========================================================
# MAIN UI
# =========================================================
def run_training_generator():
    st.header("Training Generator")
    st.write("Generate smarter, more professional sport-specific training sessions with full reps, rounds, and time prescriptions.")

    role = st.selectbox("Are you a player or coach?", ["Player", "Coach"])
    sport = st.selectbox("Choose your sport", SPORTS)

    if role == "Player":
        level = st.selectbox("What is your level?", PLAYER_LEVELS)
        days_question = (
            "How many times do you play sports per week?"
            if level == "Learn how to play"
            else SPORT_TRAINING_DAYS_QUESTION.get(sport, "How many times do you train per week?")
        )
        days_per_week = st.slider(days_question, 1, 7, 3)

        position = st.selectbox("What is your position?", SPORT_POSITIONS[sport]) if sport in SPORT_POSITIONS else None

        goal_pool = COMMON_GOALS + SPORT_SPECIFIC_GOALS.get(sport, [])
        goal = st.selectbox("What is the goal of this training?", goal_pool)
        sport_goal = st.selectbox("Choose the main focus for this session", SPORT_SPECIFIC_GOALS.get(sport, ["General development"]))
        weakness = st.selectbox("Main weakness to improve", ["None"] + COMMON_WEAKNESSES)
        session_type = st.selectbox("Session style", SESSION_TYPES)
        duration = st.slider("Session duration (minutes)", 35, 150, 75, 5)
        equipment = st.selectbox("Equipment access", EQUIPMENT_OPTIONS)
        phase = st.selectbox("Season phase", PERIOD_PHASES)

        if st.button("Generate Training Session", key="player_generate"):
            session_header(role, sport, level, goal, session_type)
            if position:
                st.write(f"**Position:** {position}")
            session = build_player_session(
                sport, level, position, goal, sport_goal, weakness,
                session_type, equipment, phase, days_per_week, duration
            )
            render_session_plan(session)
            render_weekly_microcycle(sport, role, level, goal, phase, days_per_week)

    else:
        level = st.selectbox("What is the level of the team/group?", COACH_LEVELS)
        days_per_week = st.slider("How many times does your team play or train per week?", 1, 7, 3)
        focus = st.selectbox("What's the focus of this training?", COACH_FOCUS_OPTIONS.get(sport, ["Mixed session"]))
        weakness = st.selectbox("Main team weakness to improve", ["None"] + COMMON_WEAKNESSES)
        goal = st.selectbox("Overall goal", COMMON_GOALS)
        session_type = st.selectbox("Session style", SESSION_TYPES)
        duration = st.slider("Session duration (minutes)", 40, 180, 90, 5)
        equipment = st.selectbox("Equipment access", EQUIPMENT_OPTIONS)
        phase = st.selectbox("Season phase", PERIOD_PHASES)

        if st.button("Generate Coach Session", key="coach_generate"):
            session_header(role, sport, level, goal, session_type)
            st.write(f"**Team Focus:** {focus}")
            session = build_coach_session(
                sport, level, focus, weakness, session_type,
                equipment, phase, days_per_week, duration
            )
            render_session_plan(session)
            render_weekly_microcycle(sport, role, level, goal, phase, days_per_week)

# =========================================================
# PAGE START
# =========================================================
st.set_page_config(page_title="Sportze.AI Training Generator", layout="wide")
run_training_generator()
