"""Gymnastics training catalog for Sportze.AI.

This module codifies gymnastics workouts into a clean, implementation-ready
structure for the Training Generator catalog.
"""

SPORT = "Gymnastics"


def exercise(name: str, prescription: str) -> dict:
    """Create a normalized exercise dictionary."""
    return {"name": name, "prescription": prescription}


def session(
    name: str,
    category: str,
    level: str,
    focus: str,
    training_type: str,
    exercises: list[dict],
) -> dict:
    """Create a normalized workout/session dictionary."""
    return {
        "sport": SPORT,
        "name": name,
        "category": category,
        "level": level,
        "focus": focus,
        "training_type": training_type,
        "exercises": exercises,
    }


GYMNASTICS_WORKOUTS = [
    session(
        name="Body Control Fundamentals",
        category="Learn How to Play",
        level="learn",
        focus="body control",
        training_type="alone",
        exercises=[
            exercise("Forward Rolls", "3 x 10 rolls"),
            exercise("Backward Rolls", "3 x 10 rolls"),
            exercise("Tuck Holds", "3 x 30 seconds"),
            exercise("Hollow Body Holds", "3 x 30 seconds"),
            exercise("Arch Holds", "3 x 30 seconds"),
            exercise("Bear Crawls", "4 x 15 meters"),
            exercise("Crab Walks", "4 x 15 meters"),
            exercise("Two-Foot Stick Landings", "30 repetitions"),
        ],
    ),
    session(
        name="Balance Fundamentals",
        category="Learn How to Play",
        level="learn",
        focus="balance",
        training_type="alone",
        exercises=[
            exercise("Single-Leg Balance", "3 x 30 seconds each leg"),
            exercise("Walking Heel-to-Toe Line Drill", "10 passes"),
            exercise("Balance Beam Walk", "20 passes on low beam or line"),
            exercise("Quarter Turns on Beam or Line", "20 repetitions"),
            exercise("Single-Leg Squats to Bench", "3 x 10 each leg"),
            exercise("Arabesque Hold", "3 x 20 seconds each leg"),
            exercise("Straight Jumps with Controlled Landing", "30 repetitions"),
            exercise("180-Degree Jump Turns", "20 repetitions"),
        ],
    ),
    session(
        name="Flexibility Foundations",
        category="Learn How to Play",
        level="learn",
        focus="flexibility",
        training_type="alone",
        exercises=[
            exercise("Pike Stretch", "3 x 45 seconds"),
            exercise("Straddle Stretch", "3 x 45 seconds"),
            exercise("Butterfly Stretch", "3 x 45 seconds"),
            exercise("Bridge Holds", "5 x 20 seconds"),
            exercise("Shoulder Flexibility Stretch", "5 x 20 seconds"),
            exercise("Lunge Hip Stretch", "3 x 30 seconds each side"),
            exercise("Toe Touch Reaches", "3 x 20 reps"),
            exercise("Wall Split Progression", "5 x 20 seconds"),
        ],
    ),
    session(
        name="Jumping and Landing",
        category="Learn How to Play",
        level="learn",
        focus="jumping and landing",
        training_type="alone",
        exercises=[
            exercise("Straight Jumps", "3 x 20"),
            exercise("Tuck Jumps", "3 x 15"),
            exercise("Star Jumps", "3 x 20"),
            exercise("Broad Jumps", "3 x 10"),
            exercise("Box Step-Off Landings", "3 x 15"),
            exercise("180-Degree Jump Turns", "3 x 10"),
            exercise("Jump-to-Stick Drill", "30 reps"),
            exercise("Mini Trampoline Straight Jumps", "3 x 20"),
        ],
    ),
    session(
        name="Handstand Introduction",
        category="Learn How to Play",
        level="learn",
        focus="handstand basics",
        training_type="alone",
        exercises=[
            exercise("Wall Handstand Hold", "10 x 20 seconds"),
            exercise("Bear Position Shoulder Taps", "3 x 20"),
            exercise("Wall Walks", "5 x 5"),
            exercise("Kick-Up Handstand Attempts", "30 reps"),
            exercise("Pike Hold", "3 x 30 seconds"),
            exercise("Plank Hold", "3 x 45 seconds"),
            exercise("Hollow Body Hold", "3 x 30 seconds"),
            exercise("Handstand Line Drill", "20 reps"),
        ],
    ),
    session(
        name="Apparatus Introduction",
        category="Learn How to Play",
        level="learn",
        focus="apparatus basics",
        training_type="alone",
        exercises=[
            exercise("Low Beam Walks", "20 passes"),
            exercise("Mini Vault Runs", "20 repetitions"),
            exercise("Support Hold on Parallel Bars", "5 x 20 seconds"),
            exercise("Bar Hang", "5 x 20 seconds"),
            exercise("Ring Support Hold", "5 x 15 seconds"),
            exercise("Trampoline Straight Jumps", "50 jumps"),
            exercise("Ribbon Figure-8 Movements", "50 repetitions"),
            exercise("Ball Toss and Catch", "50 repetitions"),
        ],
    ),
    session(
        name="Combining Skills",
        category="Learn How to Play",
        level="learn",
        focus="skill combination",
        training_type="alone",
        exercises=[
            exercise("Forward Roll to Jump", "20 reps"),
            exercise("Balance Walk to Turn", "20 reps"),
            exercise("Handstand Hold", "10 x 20 seconds"),
            exercise("Cartwheel Attempts", "30 reps"),
            exercise("Jump-to-Stick Landing", "30 reps"),
            exercise("Bridge Hold", "5 x 20 seconds"),
            exercise("Bar Hang", "5 x 30 seconds"),
            exercise("Ribbon Circle Drill", "50 reps"),
        ],
    ),
    session(
        name="Mini Gymnastics Circuit",
        category="Learn How to Play",
        level="learn",
        focus="beginner circuit",
        training_type="alone",
        exercises=[
            exercise("Forward Roll", "20 reps"),
            exercise("Cartwheel Attempts", "20 reps"),
            exercise("Balance Beam Walk", "10 passes"),
            exercise("Wall Handstand Hold", "5 x 30 seconds"),
            exercise("Straight Jumps", "30 reps"),
            exercise("Bar Hang", "5 x 30 seconds"),
            exercise("Bridge Hold", "5 x 20 seconds"),
            exercise("Trampoline Straight Jumps", "50 reps"),
        ],
    ),
    session(
        name="Fundamental Gymnast Strength",
        category="Beginner",
        level="beginner",
        focus="strength",
        training_type="alone",
        exercises=[
            exercise("Push-Ups", "4 x 12"),
            exercise("Pull-Ups", "4 x 6, assisted if needed"),
            exercise("Hollow Body Holds", "4 x 30 seconds"),
            exercise("Arch Holds", "4 x 30 seconds"),
            exercise("Wall Handstand Hold", "8 x 30 seconds"),
            exercise("L-Sit Tuck Hold", "5 x 15 seconds"),
            exercise("Box Jumps", "4 x 10"),
            exercise("Bridge Holds", "5 x 20 seconds"),
        ],
    ),
    session(
        name="Cartwheel and Handstand Development",
        category="Beginner",
        level="beginner",
        focus="cartwheel and handstand",
        training_type="alone",
        exercises=[
            exercise("Cartwheels", "50 repetitions"),
            exercise("Wall Handstand Hold", "10 x 30 seconds"),
            exercise("Handstand Shoulder Taps", "5 x 10"),
            exercise("Wall Walks", "5 x 5"),
            exercise("Forward Rolls", "20 reps"),
            exercise("Backward Rolls", "20 reps"),
            exercise("Tuck Jumps", "4 x 15"),
            exercise("Hollow Body Hold", "4 x 40 seconds"),
        ],
    ),
    session(
        name="Beam and Balance",
        category="Beginner",
        level="beginner",
        focus="beam and balance",
        training_type="alone",
        exercises=[
            exercise("Beam Walks", "30 passes"),
            exercise("Single-Leg Beam Balance", "5 x 20 seconds each leg"),
            exercise("Straight Jumps on Beam", "30 reps"),
            exercise("Pivot Turns on Beam", "30 reps"),
            exercise("Arabesque Holds", "5 x 20 seconds"),
            exercise("Heel-to-Toe Walks", "20 passes"),
            exercise("Jump-to-Stick Landing", "30 reps"),
            exercise("Single-Leg Hops", "3 x 15 each leg"),
        ],
    ),
    session(
        name="Rings and Bar Foundations",
        category="Beginner",
        level="beginner",
        focus="rings and bars",
        training_type="alone",
        exercises=[
            exercise("Dead Hangs", "5 x 30 seconds"),
            exercise("Ring Support Holds", "5 x 20 seconds"),
            exercise("Pull-Ups", "5 x 5"),
            exercise("Inverted Rows", "4 x 10"),
            exercise("Knee Raises", "4 x 15"),
            exercise("Swing Drills on Bar", "30 reps"),
            exercise("Tuck Holds", "4 x 30 seconds"),
            exercise("Hollow Body Hold", "4 x 40 seconds"),
        ],
    ),
    session(
        name="Vault Foundations",
        category="Beginner",
        level="beginner",
        focus="vault",
        training_type="alone",
        exercises=[
            exercise("20-Meter Sprint Runs", "10 repetitions"),
            exercise("Broad Jumps", "4 x 10"),
            exercise("Box Jumps", "4 x 10"),
            exercise("Hurdle Steps", "30 repetitions"),
            exercise("Springboard Jumps", "30 repetitions"),
            exercise("Squat Jumps", "4 x 15"),
            exercise("Jump-to-Stick Landings", "30 reps"),
            exercise("Tuck Jumps", "4 x 15"),
        ],
    ),
    session(
        name="Rhythmic Gymnastics Basics",
        category="Beginner",
        level="beginner",
        focus="rhythmic gymnastics",
        training_type="alone",
        exercises=[
            exercise("Ribbon Circles", "50 reps"),
            exercise("Ribbon Figure-8s", "50 reps"),
            exercise("Ball Toss and Catch", "50 reps"),
            exercise("Hoop Spins", "50 reps"),
            exercise("Club Swings", "50 reps"),
            exercise("Rope Skips", "200 jumps"),
            exercise("Split Stretch", "5 x 30 seconds"),
            exercise("Balance Pose Hold", "5 x 20 seconds"),
        ],
    ),
    session(
        name="Trampoline Basics",
        category="Beginner",
        level="beginner",
        focus="trampoline",
        training_type="alone",
        exercises=[
            exercise("Straight Jumps", "100 reps"),
            exercise("Tuck Jumps", "50 reps"),
            exercise("Straddle Jumps", "50 reps"),
            exercise("Seat Drops", "30 reps"),
            exercise("Half Turns", "30 reps"),
            exercise("Full Turns", "20 reps"),
            exercise("Jump-to-Stick Landing", "30 reps"),
            exercise("Core Crunches", "4 x 20"),
        ],
    ),
    session(
        name="Complete Beginner Gymnastics Circuit",
        category="Beginner",
        level="beginner",
        focus="complete circuit",
        training_type="alone",
        exercises=[
            exercise("Forward Rolls", "20 reps"),
            exercise("Cartwheels", "30 reps"),
            exercise("Wall Handstand Hold", "5 x 30 seconds"),
            exercise("Beam Walks", "20 passes"),
            exercise("Ring Support Hold", "5 x 20 seconds"),
            exercise("Bar Hang", "5 x 30 seconds"),
            exercise("Straight Jumps", "50 reps"),
            exercise("Ribbon Figure-8s", "50 reps"),
        ],
    ),
]


def get_workouts() -> list[dict]:
    """Return all gymnastics workouts."""
    return GYMNASTICS_WORKOUTS


def get_sessions() -> list[dict]:
    """Alias used by some catalog managers."""
    return get_workouts()


def get_workouts_by_level(level: str) -> list[dict]:
    """Return workouts matching a level, such as 'learn' or 'beginner'."""
    normalized_level = level.strip().lower()
    return [workout for workout in GYMNASTICS_WORKOUTS if workout["level"] == normalized_level]


def get_workouts_by_category(category: str) -> list[dict]:
    """Return workouts matching a category."""
    normalized_category = category.strip().lower()
    return [
        workout
        for workout in GYMNASTICS_WORKOUTS
        if workout["category"].strip().lower() == normalized_category
    ]


def get_workouts_by_training_type(training_type: str) -> list[dict]:
    """Return workouts matching a training type, such as 'alone'."""
    normalized_training_type = training_type.strip().lower()
    return [
        workout
        for workout in GYMNASTICS_WORKOUTS
        if workout["training_type"] == normalized_training_type
    ]


def validate_catalog() -> bool:
    """Validate that every session has the required implementation fields."""
    required_session_keys = {
        "sport",
        "name",
        "category",
        "level",
        "focus",
        "training_type",
        "exercises",
    }
    required_exercise_keys = {"name", "prescription"}

    for workout in GYMNASTICS_WORKOUTS:
        if not required_session_keys.issubset(workout):
            return False
        if not workout["exercises"]:
            return False
        for item in workout["exercises"]:
            if not required_exercise_keys.issubset(item):
                return False
            if not item["name"] or not item["prescription"]:
                return False
    return True


if __name__ == "__main__":
    print(f"{SPORT}: {len(GYMNASTICS_WORKOUTS)} sessions loaded")
    print(f"Catalog valid: {validate_catalog()}")
