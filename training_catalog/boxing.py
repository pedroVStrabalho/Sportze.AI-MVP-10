"""
Boxing training catalog for Sportze.AI.

Structure:
- learn_how_to_box
- beginner
- intermediate
- advanced
- elite_pro

Each level contains:
- training_alone
- training_2_plus_people

Each exercise/session item has:
- name
- instructions
"""

SPORT = "Boxing"

BOXING_CATALOG = {
    "learn_how_to_box": {
        "training_alone": [
            {
                "name": "Basic Stance Walk",
                "instructions": [
                    "Hold boxing stance for 5 minutes.",
                    "Move forward 50 times.",
                    "Move backward 50 times.",
                    "Move left 50 times.",
                    "Move right 50 times.",
                ],
            },
            {
                "name": "Jab Repetitions",
                "instructions": [
                    "Complete 10 sets of 20 jabs.",
                    "Return guard after every punch.",
                ],
            },
            {
                "name": "Cross Repetitions",
                "instructions": [
                    "Complete 10 sets of 20 crosses.",
                    "Rotate hips fully on every punch.",
                ],
            },
            {
                "name": "Jab-Cross Shadowboxing",
                "instructions": [
                    "Complete 10 rounds of 1 minute.",
                    "Use continuous jab-cross combinations.",
                ],
            },
            {
                "name": "Defensive Slips",
                "instructions": [
                    "Complete 5 sets of 50 slips left.",
                    "Complete 5 sets of 50 slips right.",
                ],
            },
            {
                "name": "Shadowboxing Fundamentals",
                "instructions": [
                    "Complete 6 rounds of 2 minutes.",
                    "Use only jab, cross, and footwork.",
                ],
            },
            {
                "name": "Mirror Technique Drill",
                "instructions": [
                    "Complete 5 rounds of 2 minutes.",
                    "Watch guard position constantly.",
                ],
            },
            {
                "name": "Straight Punch Accuracy",
                "instructions": [
                    "Pick a target on a wall.",
                    "Complete 200 straight punches.",
                ],
            },
            {
                "name": "Footwork Ladder",
                "instructions": [
                    "Move continuously for 10 minutes.",
                    "Never cross your feet.",
                ],
            },
            {
                "name": "Full Beginner Shadowboxing",
                "instructions": [
                    "Complete 8 rounds of 2 minutes.",
                    "Mix punches, movement, and defense.",
                ],
            },
        ],
        "training_2_plus_people": [
            {"name": "Jab Accuracy Partner Drill", "instructions": ["Complete 10 sets of 20 jabs each."]},
            {"name": "Jab-Cross Pad Work", "instructions": ["Complete 10 rounds of 1 minute."]},
            {"name": "Mirror Footwork", "instructions": ["Follow partner movements for 5 rounds of 2 minutes."]},
            {"name": "Defense Recognition", "instructions": ["Partner throws slow punches.", "Defend 100 punches."]},
            {"name": "Distance Management Drill", "instructions": ["Complete 10 rounds of 1 minute."]},
            {"name": "Controlled Touch Sparring", "instructions": ["Complete 5 rounds of 2 minutes."]},
            {"name": "Partner Reaction Drill", "instructions": ["Complete 200 punch-call reactions."]},
            {"name": "Body Shot Pad Drill", "instructions": ["Complete 10 sets of 20 punches."]},
            {"name": "Combination Calling", "instructions": ["Partner calls combinations.", "Complete 100 executions."]},
            {"name": "Beginner Technical Sparring", "instructions": ["Complete 6 rounds of 2 minutes."]},
        ],
    },
    "beginner": {
        "training_alone": [
            {"name": "Jab Marathon", "instructions": ["Complete 500 jabs."]},
            {"name": "Cross Marathon", "instructions": ["Complete 500 crosses."]},
            {"name": "Jab-Cross Repetitions", "instructions": ["Complete 300 jab-cross combinations."]},
            {"name": "Slip and Counter", "instructions": ["Complete 200 slips.", "Complete 200 crosses."]},
            {"name": "Ducking Drill", "instructions": ["Complete 200 ducks."]},
            {"name": "Shadowboxing Endurance", "instructions": ["Complete 10 rounds of 2 minutes."]},
            {"name": "Four-Punch Combination Drill", "instructions": ["Complete 200 combinations."]},
            {"name": "Footwork Circuits", "instructions": ["Move continuously for 15 minutes."]},
            {"name": "Defensive Shadowboxing", "instructions": ["Complete 8 rounds of 2 minutes."]},
            {"name": "Heavy Shadowboxing", "instructions": ["Complete 12 rounds of 2 minutes."]},
        ],
        "training_2_plus_people": [
            {"name": "Focus Mitt Fundamentals", "instructions": ["Complete 10 rounds of 2 minutes."]},
            {"name": "Jab Sparring", "instructions": ["Complete 6 rounds of 2 minutes."]},
            {"name": "Distance Sparring", "instructions": ["Complete 6 rounds of 2 minutes."]},
            {"name": "Defense Drill", "instructions": ["Defend 200 punches."]},
            {"name": "Counter Drill", "instructions": ["Complete 200 counters."]},
            {"name": "Body Shot Pad Work", "instructions": ["Complete 300 punches."]},
            {"name": "Combination Pad Work", "instructions": ["Complete 10 rounds of 2 minutes."]},
            {"name": "Controlled Sparring", "instructions": ["Complete 8 rounds of 2 minutes."]},
            {"name": "Pressure Drill", "instructions": ["Complete 10 rounds of 1 minute."]},
            {"name": "Reaction Drill", "instructions": ["Complete 300 coach commands."]},
        ],
    },
    "intermediate": {
        "training_alone": [
            {"name": "Triple Combination Drill", "instructions": ["Complete 300 combinations."]},
            {"name": "Shadowboxing With Angles", "instructions": ["Complete 10 rounds of 3 minutes."]},
            {"name": "Slip-Counter Series", "instructions": ["Complete 300 repetitions."]},
            {"name": "Defensive Movement Drill", "instructions": ["Move defensively for 15 minutes."]},
            {"name": "Advanced Footwork", "instructions": ["Complete 20 minutes of advanced footwork."]},
            {"name": "High Pace Shadowboxing", "instructions": ["Complete 12 rounds of 3 minutes."]},
            {"name": "Body-Head Combinations", "instructions": ["Complete 250 combinations."]},
            {"name": "Counter Shadowboxing", "instructions": ["Complete 10 rounds of 3 minutes."]},
            {"name": "Fight Simulation", "instructions": ["Complete 6 rounds of 3 minutes."]},
            {"name": "Technical Shadowboxing", "instructions": ["Complete 15 rounds of 2 minutes."]},
        ],
        "training_2_plus_people": [
            {"name": "Mitt Combination Training", "instructions": ["Complete 12 rounds of 3 minutes."]},
            {"name": "Technical Sparring", "instructions": ["Complete 10 rounds of 3 minutes."]},
            {"name": "Counter Sparring", "instructions": ["Complete 8 rounds of 3 minutes."]},
            {"name": "Pressure Sparring", "instructions": ["Complete 8 rounds of 3 minutes."]},
            {"name": "Defensive Sparring", "instructions": ["Complete 8 rounds of 3 minutes."]},
            {"name": "Partner Reaction Drill", "instructions": ["Complete 400 reactions."]},
            {"name": "Body Shot Drill", "instructions": ["Complete 400 punches."]},
            {"name": "Angle Creation Drill", "instructions": ["Complete 10 rounds of 2 minutes."]},
            {"name": "Combination Recognition", "instructions": ["Complete 10 rounds of 2 minutes."]},
            {"name": "Match Simulation", "instructions": ["Complete 8 rounds of 3 minutes."]},
        ],
    },
    "advanced": {
        "training_alone": [
            {"name": "Professional Shadowboxing", "instructions": ["Complete 15 rounds of 3 minutes."]},
            {"name": "High-Speed Combinations", "instructions": ["Complete 500 combinations."]},
            {"name": "Defensive Mastery Drill", "instructions": ["Complete 500 defensive movements."]},
            {"name": "Counter Mastery Drill", "instructions": ["Complete 400 counters."]},
            {"name": "Ring Movement Session", "instructions": ["Move around the ring for 20 minutes."]},
            {"name": "Fight Pace Intervals", "instructions": ["Complete 15 rounds of 3 minutes."]},
            {"name": "Tactical Shadowboxing", "instructions": ["Complete 12 rounds of 3 minutes."]},
            {"name": "Pressure Fighter Simulation", "instructions": ["Complete 10 rounds of 3 minutes."]},
            {"name": "Out-Boxer Simulation", "instructions": ["Complete 10 rounds of 3 minutes."]},
            {"name": "Championship Simulation", "instructions": ["Complete 12 rounds of 3 minutes."]},
        ],
        "training_2_plus_people": [
            {"name": "Elite Mitt Work", "instructions": ["Complete 15 rounds of 3 minutes."]},
            {"name": "Tactical Sparring", "instructions": ["Complete 12 rounds of 3 minutes."]},
            {"name": "Counter-Fighting Sparring", "instructions": ["Complete 10 rounds of 3 minutes."]},
            {"name": "Pressure Sparring", "instructions": ["Complete 10 rounds of 3 minutes."]},
            {"name": "Defensive Sparring", "instructions": ["Complete 10 rounds of 3 minutes."]},
            {"name": "Open Sparring", "instructions": ["Complete 12 rounds of 3 minutes."]},
            {"name": "Body Attack Drill", "instructions": ["Complete 500 punches."]},
            {"name": "Ring Control Drill", "instructions": ["Complete 10 rounds of 3 minutes."]},
            {"name": "Coach Command Drill", "instructions": ["Complete 500 commands."]},
            {"name": "Fight Simulation", "instructions": ["Complete 12 rounds of 3 minutes."]},
        ],
    },
    "elite_pro": {
        "training_alone": [
            {"name": "Elite Shadowboxing", "instructions": ["Complete 20 rounds of 3 minutes."]},
            {"name": "Championship Pace Session", "instructions": ["Complete 15 rounds of 3 minutes."]},
            {"name": "Counter-Punch Specialist Drill", "instructions": ["Complete 600 repetitions."]},
            {"name": "Defensive Specialist Drill", "instructions": ["Complete 600 repetitions."]},
            {"name": "Tactical Session", "instructions": ["Complete 15 rounds of 3 minutes."]},
            {"name": "Footwork Specialist Session", "instructions": ["Complete 30 minutes of footwork."]},
            {"name": "Combination Specialist Session", "instructions": ["Complete 700 combinations."]},
            {"name": "Fight Camp Simulation", "instructions": ["Complete 18 rounds of 3 minutes."]},
            {"name": "Opponent Study Simulation", "instructions": ["Complete 12 rounds of 3 minutes."]},
            {"name": "Professional Match Preparation", "instructions": ["Complete 12 rounds of 3 minutes."]},
        ],
        "training_2_plus_people": [
            {"name": "Championship Mitt Work", "instructions": ["Complete 20 rounds of 3 minutes."]},
            {"name": "Professional Sparring", "instructions": ["Complete 12 rounds of 3 minutes."]},
            {"name": "Tactical Sparring", "instructions": ["Complete 12 rounds of 3 minutes."]},
            {"name": "Opponent-Specific Sparring", "instructions": ["Complete 12 rounds of 3 minutes."]},
            {"name": "Pressure Fighter Sparring", "instructions": ["Complete 10 rounds of 3 minutes."]},
            {"name": "Out-Boxer Sparring", "instructions": ["Complete 10 rounds of 3 minutes."]},
            {"name": "Counter-Fighter Sparring", "instructions": ["Complete 10 rounds of 3 minutes."]},
            {"name": "Elite Reaction Drill", "instructions": ["Complete 600 reactions."]},
            {"name": "Full Fight Simulation", "instructions": ["Complete 12 rounds of 3 minutes."]},
            {"name": "Title Fight Simulation", "instructions": ["Complete 15 rounds of 3 minutes."]},
        ],
    },
}


def get_catalog():
    """Return the complete boxing catalog."""
    return BOXING_CATALOG


def get_levels():
    """Return all available boxing levels."""
    return list(BOXING_CATALOG.keys())


def get_training_modes(level):
    """Return available training modes for a given level."""
    return list(BOXING_CATALOG.get(level, {}).keys())


def get_exercises(level, training_mode):
    """
    Return exercises for a specific boxing level and training mode.

    Args:
        level: Example: "beginner", "advanced", "elite_pro".
        training_mode: "training_alone" or "training_2_plus_people".
    """
    return BOXING_CATALOG.get(level, {}).get(training_mode, [])


def get_all_exercises_flat():
    """Return every boxing exercise as a flat list with level and mode metadata."""
    exercises = []
    for level, modes in BOXING_CATALOG.items():
        for training_mode, items in modes.items():
            for item in items:
                exercises.append({
                    "sport": SPORT,
                    "level": level,
                    "training_mode": training_mode,
                    **item,
                })
    return exercises
