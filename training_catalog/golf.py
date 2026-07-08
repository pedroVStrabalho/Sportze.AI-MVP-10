"""
Sportze.AI Golf Training Catalog

This module codifies Golf workouts for the Training Generator.
It uses plain Python dictionaries/lists so it can be imported cleanly by
catalog_manager.py or any Sportze.AI training selector.

Structure:
- GOLF_CATALOG[category][training_mode][session_key]
- training_mode: "alone" or "with_others"
- each session contains: title, sport, category, focus, training_mode, exercises

Helper functions:
- get_golf_catalog()
- list_golf_sessions(category=None, training_mode=None)
- get_golf_session(session_key, category=None, training_mode=None)
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List, Optional

SportSession = Dict[str, Any]
SportCatalog = Dict[str, Dict[str, Dict[str, SportSession]]]

SPORT = "Golf"


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
    """Create a normalized golf session."""
    return {
        "key": key,
        "sport": SPORT,
        "title": title,
        "category": category,
        "training_mode": training_mode,
        "focus": focus,
        "exercises": exercises,
    }


def _make_session(category: str, slug: str, title: str, focus: str, items: List[tuple[str, str]]) -> SportSession:
    key = f"golf_{category}_{slug}"
    return session(
        key,
        title,
        category,
        "alone",
        focus,
        [exercise(name, prescription) for name, prescription in items],
    )


GOLF_CATALOG: SportCatalog = {
    "driving": {
        "alone": {
            "golf_driving_driver_accuracy_session": _make_session("driving", "driver_accuracy_session", "Driver Accuracy Session", "driver accuracy and tee-shot control", [("Fairway Target Drives", "Hit 50 drives aiming at a 30-meter-wide fairway target"), ("Left-Center Drives", "Hit 25 drives aiming left-center of the target"), ("Right-Center Drives", "Hit 25 drives aiming right-center of the target"), ("Slow-Motion Balance Swings", "Perform 20 slow-motion swings focusing on balance"), ("Controlled-Power Drives", "Hit 20 drives at 80% power"), ("Full-Power Drives", "Hit 20 drives at full power"), ("Finish Hold", "Hold finish position for 5 seconds after 20 swings"), ("First-Hole Pressure Drives", "Hit 10 drives simulating first-hole pressure")]),
            "golf_driving_driver_distance_session": _make_session("driving", "driver_distance_session", "Driver Distance Session", "driver distance and rotational power", [("Maximum-Speed Drives", "Hit 40 drives at maximum legal swing speed"), ("Medicine-Ball Rotational Throws", "30 throws"), ("Jump Squats", "3 x 15"), ("High-Launch Drives", "Hit 30 drives focusing on high launch angle"), ("Band Rotations", "3 x 20"), ("Overspeed Swing Training", "Hit 20 drives with overspeed swing training"), ("Plank Holds", "3 x 30 seconds"), ("Longest Drive Test", "Hit 10 longest possible drives and record distance")]),
            "golf_driving_fairway_finder_session": _make_session("driving", "fairway_finder_session", "Fairway Finder Session", "controlled tee shots and fairway percentage", [("Narrow Fairway Drives", "Hit 60 drives at a narrow target fairway"), ("Controlled Fade Drives", "Hit 20 drives with a controlled fade"), ("Controlled Draw Drives", "Hit 20 drives with a controlled draw"), ("75% Power Drives", "Hit 20 drives at 75% power"), ("85% Power Drives", "Hit 20 drives at 85% power"), ("Balance Finish", "Hold balance position after 30 swings"), ("Alignment-Stick Setup Checks", "20 checks"), ("Pressure Drives", "Hit 10 pressure drives")]),
            "golf_driving_wind_driving_session": _make_session("driving", "wind_driving_session", "Wind Driving Session", "trajectory and wind-adapted driving", [("Low-Trajectory Drives", "Hit 20 low-trajectory drives"), ("High-Trajectory Drives", "Hit 20 high-trajectory drives"), ("Headwind Drives", "Hit 20 drives into simulated headwind"), ("Tailwind Drives", "Hit 20 drives into simulated tailwind"), ("Fade Drives", "Hit 20 fade drives"), ("Draw Drives", "Hit 20 draw drives"), ("Swing-Plane Drills", "20 drills"), ("Random Target Drives", "Hit 10 random target drives")]),
            "golf_driving_competitive_driving_session": _make_session("driving", "competitive_driving_session", "Competitive Driving Session", "competitive tee-shot execution", [("Full-Round Tee Shot Simulation", "Hit 14 drives simulating a full round"), ("Recovery Drives", "Hit 14 recovery drives"), ("Pressure Drives", "Hit 14 pressure drives"), ("Controlled-Power Drives", "Hit 20 controlled-power drives"), ("Full-Power Drives", "Hit 20 full-power drives"), ("Balance Drills", "15 drills"), ("Rotational Medicine-Ball Throws", "15 throws"), ("Fairway-Target Finish", "Finish with 10 fairway-target drives")]),
            "golf_driving_shot_shaping_driving_session": _make_session("driving", "shot_shaping_driving_session", "Shot-Shaping Driving Session", "draw, fade, height, and trajectory control", [("Fade Drives", "Hit 30 fade drives"), ("Draw Drives", "Hit 30 draw drives"), ("Straight Drives", "Hit 20 straight drives"), ("Low Drives", "Hit 20 low drives"), ("High Drives", "Hit 20 high drives"), ("Alignment Drills", "20 drills"), ("Tempo Swings", "20 swings"), ("Random-Shot Drives", "Hit 10 random-shot drives")]),
            "golf_driving_driving_consistency_session": _make_session("driving", "driving_consistency_session", "Driving Consistency Session", "repeatable driver mechanics", [("Same-Target Drives", "Hit 100 drives aiming at the same target"), ("Setup Checks", "30 checks"), ("One-Dimple Focus Drives", "Hit 20 drives with eyes focused on one dimple"), ("Tempo Swings", "20 swings"), ("75% Speed Drives", "Hit 20 drives at 75% speed"), ("Full-Speed Drives", "Hit 20 drives at full speed"), ("Finish Hold", "Hold finish position after 20 swings"), ("Pressure Drives", "Hit 10 pressure drives")]),
            "golf_driving_tournament_driving_session": _make_session("driving", "tournament_driving_session", "Tournament Driving Session", "tournament tee-shot decision making", [("Tee Shot Simulation", "Simulate 18 tee shots"), ("Recovery Tee Shots", "Hit 18 recovery tee shots"), ("Narrow-Fairway Drives", "Hit 18 narrow-fairway drives"), ("Aggressive Drives", "Hit 18 aggressive drives"), ("Balance Drills", "20 drills"), ("Rotational Throws", "20 throws"), ("Full-Power Drives", "Hit 20 full-power drives"), ("Must-Hit Fairway Drives", "Finish with 10 must-hit fairway drives")]),
        }
    },
    "iron_play": {
        "alone": {
            "golf_iron_play_contact_consistency_session": _make_session("iron_play", "contact_consistency_session", "Contact Consistency Session", "clean iron contact and repeatability", [("7-Iron Contact Shots", "Hit 100 iron shots with a 7-iron"), ("100m Target Shots", "Hit 50 shots to a 100-meter target"), ("150m Target Shots", "Hit 50 shots to a 150-meter target"), ("Alignment Checks", "20 checks"), ("Half-Swings", "Hit 20 half-swings"), ("Three-Quarter Swings", "Hit 20 three-quarter swings"), ("Tempo Swings", "20 swings"), ("Pressure Shots", "Finish with 10 pressure shots")]),
            "golf_iron_play_distance_control_session": _make_session("iron_play", "distance_control_session", "Distance Control Session", "iron distance control", [("Distance Ladder", "Hit 20 shots each at 50m, 75m, 100m, 125m, and 150m"), ("Half-Swings", "20 swings"), ("Three-Quarter Swings", "20 swings"), ("Tempo Drills", "20 drills"), ("Random Distance Shots", "Hit 20 random distances"), ("Target Challenges", "Complete 10 target challenges"), ("Pressure Shots", "Hit 10 pressure shots"), ("Distance Recording", "Record all distances")]),
            "golf_iron_play_accuracy_session": _make_session("iron_play", "accuracy_session", "Accuracy Session", "green-target accuracy", [("Green Target Iron Shots", "Hit 100 iron shots at a green target"), ("Left Pin Shots", "Hit 30 shots at left pin positions"), ("Center Pin Shots", "Hit 30 shots at center pin positions"), ("Right Pin Shots", "Hit 30 shots at right pin positions"), ("Alignment Checks", "20 checks"), ("Controlled Swings", "Hit 20 controlled swings"), ("Full Swings", "Hit 20 full swings"), ("Must-Hit Targets", "Finish with 10 must-hit targets")]),
            "golf_iron_play_draw_and_fade_session": _make_session("iron_play", "draw_and_fade_session", "Draw and Fade Session", "iron shot shaping", [("Draw Shots", "Hit 30 draw shots"), ("Fade Shots", "Hit 30 fade shots"), ("Straight Shots", "Hit 20 straight shots"), ("Low Shots", "Hit 20 low shots"), ("High Shots", "Hit 20 high shots"), ("Swing-Path Drills", "20 drills"), ("Alignment Drills", "20 drills"), ("Random Targets", "Finish with 10 random targets")]),
            "golf_iron_play_long_iron_session": _make_session("iron_play", "long_iron_session", "Long Iron Session", "long iron control", [("4-Iron Shots", "Hit 50 shots with a 4-iron"), ("5-Iron Shots", "Hit 50 shots with a 5-iron"), ("Low Shots", "Hit 20 low shots"), ("High Shots", "Hit 20 high shots"), ("Tempo Drills", "20 drills"), ("Balance Drills", "20 drills"), ("Pressure Shots", "Hit 20 pressure shots"), ("Target Shots", "Finish with 10 target shots")]),
            "golf_iron_play_mid_iron_session": _make_session("iron_play", "mid_iron_session", "Mid-Iron Session", "mid-iron accuracy and trajectory", [("6-Iron Shots", "Hit 50 shots with a 6-iron"), ("7-Iron Shots", "Hit 50 shots with a 7-iron"), ("8-Iron Shots", "Hit 50 shots with an 8-iron"), ("Alignment Drills", "20 drills"), ("Low Shots", "Hit 20 low shots"), ("High Shots", "Hit 20 high shots"), ("Tempo Swings", "20 swings"), ("Pressure Shots", "Finish with 10 pressure shots")]),
            "golf_iron_play_green_hitting_session": _make_session("iron_play", "green_hitting_session", "Green-Hitting Session", "approach placement", [("Approach Shots", "Hit 100 approach shots"), ("Front Pin Shots", "Hit 30 shots to front pins"), ("Middle Pin Shots", "Hit 30 shots to middle pins"), ("Back Pin Shots", "Hit 30 shots to back pins"), ("Alignment Drills", "20 drills"), ("Tempo Swings", "20 swings"), ("Random Targets", "Hit 20 random targets"), ("Pressure Shots", "Finish with 10 pressure shots")]),
            "golf_iron_play_tournament_iron_session": _make_session("iron_play", "tournament_iron_session", "Tournament Iron Session", "tournament approach play", [("Approach Shot Simulation", "Simulate 18 approach shots"), ("Recovery Approach Simulation", "Simulate 18 recovery approaches"), ("Draw Shots", "Hit 20 draw shots"), ("Fade Shots", "Hit 20 fade shots"), ("Low Shots", "Hit 20 low shots"), ("High Shots", "Hit 20 high shots"), ("Tempo Swings", "20 swings"), ("Must-Hit Greens", "Finish with 10 must-hit greens")]),
        }
    },
    "short_game": {
        "alone": {
            "golf_short_game_basic_chipping_session": _make_session("short_game", "basic_chipping_session", "Basic Chipping Session", "basic chipping touch", [("5m Chips", "Chip 50 balls from 5 meters"), ("10m Chips", "Chip 50 balls from 10 meters"), ("15m Chips", "Chip 50 balls from 15 meters"), ("2m Circle Landing", "Land 30 chips inside a 2-meter circle"), ("1m Circle Landing", "Land 20 chips inside a 1-meter circle"), ("Uphill Chips", "Hit 20 uphill chips"), ("Downhill Chips", "Hit 20 downhill chips"), ("Pressure Chips", "Finish with 10 pressure chips")]),
            "golf_short_game_distance_chipping_session": _make_session("short_game", "distance_chipping_session", "Distance Chipping Session", "chipping distance control", [("5m Chips", "Chip 30 balls from 5 meters"), ("10m Chips", "Chip 30 balls from 10 meters"), ("15m Chips", "Chip 30 balls from 15 meters"), ("20m Chips", "Chip 30 balls from 20 meters"), ("Inside-1m Chips", "Chip 20 balls inside 1 meter"), ("Uphill Shots", "Chip 20 uphill shots"), ("Downhill Shots", "Chip 20 downhill shots"), ("Pressure Chips", "Finish with 10 pressure chips")]),
            "golf_short_game_pitching_session": _make_session("short_game", "pitching_session", "Pitching Session", "pitch distance and trajectory", [("20m Pitch Shots", "Hit 30 pitch shots from 20 meters"), ("30m Pitch Shots", "Hit 30 pitch shots from 30 meters"), ("40m Pitch Shots", "Hit 30 pitch shots from 40 meters"), ("50m Pitch Shots", "Hit 30 pitch shots from 50 meters"), ("3m Circle Landing", "Land 20 balls inside a 3-meter circle"), ("High Pitches", "Hit 20 high pitches"), ("Low Pitches", "Hit 20 low pitches"), ("Pressure Pitches", "Finish with 10 pressure pitches")]),
            "golf_short_game_bunker_session": _make_session("short_game", "bunker_session", "Bunker Session", "sand play control", [("Standard Bunker Shots", "Hit 50 bunker shots"), ("Short Bunker Shots", "Hit 20 short bunker shots"), ("Long Bunker Shots", "Hit 20 long bunker shots"), ("Uphill Bunker Shots", "Hit 20 uphill bunker shots"), ("Downhill Bunker Shots", "Hit 20 downhill bunker shots"), ("Inside-3m Bunker Shots", "Land 20 shots inside 3 meters"), ("Splash-Shot Drills", "Perform 20 splash-shot drills"), ("Pressure Bunker Shots", "Finish with 10 pressure bunker shots")]),
            "golf_short_game_up_and_down_session": _make_session("short_game", "up_and_down_session", "Up-and-Down Session", "scoring from missed greens", [("Chip and Putt Out", "Chip 30 balls then putt them out"), ("Pitch and Putt Out", "Pitch 30 balls then putt them out"), ("Bunker and Putt Out", "Hit 20 bunker shots then putt them out"), ("Up-and-Down Attempts", "Complete 20 attempts"), ("Pressure Attempts", "Complete 20 pressure attempts"), ("Uphill Chips", "Hit 20 uphill chips"), ("Downhill Chips", "Hit 20 downhill chips"), ("Must-Make Up-and-Downs", "Finish with 10 must-make up-and-downs")]),
            "golf_short_game_short_game_accuracy_session": _make_session("short_game", "short_game_accuracy_session", "Short Game Accuracy Session", "short-game landing precision", [("3m Circle Landing", "Land 50 balls inside a 3-meter circle"), ("2m Circle Landing", "Land 30 balls inside a 2-meter circle"), ("1m Circle Landing", "Land 20 balls inside a 1-meter circle"), ("Chips", "Hit 20 chips"), ("Pitches", "Hit 20 pitches"), ("Bunker Shots", "Hit 20 bunker shots"), ("Pressure Shots", "Complete 20 pressure shots"), ("Random Targets", "Finish with 10 random targets")]),
            "golf_short_game_tournament_short_game_session": _make_session("short_game", "tournament_short_game_session", "Tournament Short Game Session", "round-based short-game scoring", [("Missed Green Simulation", "Simulate 18 missed greens"), ("Up-and-Down Attempts", "Play 18 up-and-down attempts"), ("Chips", "Hit 20 chips"), ("Pitches", "Hit 20 pitches"), ("Bunker Shots", "Hit 20 bunker shots"), ("Pressure Shots", "Complete 20 pressure shots"), ("Inside-2m Landing", "Land 20 balls inside 2 meters"), ("Must-Save Pars", "Finish with 10 must-save pars")]),
            "golf_short_game_recovery_shot_session": _make_session("short_game", "recovery_shot_session", "Recovery Shot Session", "creative recovery shots", [("Flop Shots", "Hit 30 flop shots"), ("Low Runners", "Hit 30 low runners"), ("Hook Chips", "Hit 20 hook chips"), ("Slice Chips", "Hit 20 slice chips"), ("Tree-Avoidance Shots", "Hit 20 tree-avoidance shots"), ("Bunker Recoveries", "Hit 20 bunker recoveries"), ("Pressure Recoveries", "Complete 20 pressure recoveries"), ("Random Recovery Challenges", "Finish with 10 random recovery challenges")]),
        }
    },
    "putting": {"alone": {}},
    "course_management": {"alone": {}},
    "golf_fitness": {"alone": {}},
    "beginner": {"alone": {}},
}

# Putting sessions, including the five requested focus sessions from the abbreviated source.
_putting_sessions = [
    ("short_putting_session", "Short Putting Session", "short-putt consistency", [("1m Putts", "Make 100 putts from 1 meter"), ("2m Putts", "Make 50 putts from 2 meters"), ("3m Putts", "Make 30 putts from 3 meters"), ("1m Consecutive Putts", "Complete 20 consecutive putts from 1 meter"), ("2m Consecutive Putts", "Complete 10 consecutive putts from 2 meters"), ("Uphill Putts", "Hit 20 uphill putts"), ("Downhill Putts", "Hit 20 downhill putts"), ("Pressure Putts", "Finish with 10 pressure putts")]),
    ("distance_control_session", "Distance Control Session", "putting speed and distance control", [("5m Putts", "Putt 30 balls from 5 meters"), ("10m Putts", "Putt 30 balls from 10 meters"), ("15m Putts", "Putt 30 balls from 15 meters"), ("20m Putts", "Putt 30 balls from 20 meters"), ("50cm Stop Zone", "Stop 20 balls within 50 cm"), ("30cm Stop Zone", "Stop 20 balls within 30 cm"), ("Lag Putts", "Complete 20 lag putts"), ("Pressure Putts", "Finish with 10 pressure putts")]),
    ("green_reading_session", "Green Reading Session", "reading break and slope", [("Breaking Putts", "Read and putt 50 breaking putts"), ("Straight Putts", "Read and putt 50 straight putts"), ("Uphill Putts", "Read and putt 20 uphill putts"), ("Downhill Putts", "Read and putt 20 downhill putts"), ("Left-to-Right Putts", "Read and putt 20 left-to-right putts"), ("Right-to-Left Putts", "Read and putt 20 right-to-left putts"), ("Pressure Putts", "Complete 20 pressure putts"), ("Must-Make Putts", "Finish with 10 must-make putts")]),
    ("tournament_putting_session", "Tournament Putting Session", "round-based putting simulation", [("18-Hole Putting Simulation", "Simulate 18 first putts from varied distances"), ("Second-Putt Conversion", "Make 18 second putts from 1-2 meters"), ("Birdie Putts", "Hit 18 birdie putts from 3-6 meters"), ("Par-Save Putts", "Hit 18 par-save putts from 2-4 meters"), ("Uphill Tournament Putts", "Hit 20 uphill putts"), ("Downhill Tournament Putts", "Hit 20 downhill putts"), ("Breaking Tournament Putts", "Hit 20 breaking putts"), ("Final-Hole Pressure Putts", "Finish with 10 must-make putts")]),
    ("pressure_putting_session", "Pressure Putting Session", "pressure conversion", [("1m Pressure Putts", "Make 50 putts from 1 meter"), ("2m Pressure Putts", "Make 40 putts from 2 meters"), ("3m Pressure Putts", "Make 30 putts from 3 meters"), ("Consecutive Ladder", "Make 5 putts in a row from 1m, 2m, and 3m"), ("Miss-and-Reset Drill", "Restart after every miss for 20 total makes"), ("Match-Point Putts", "Hit 20 match-point putts"), ("Par-Save Putts", "Hit 20 par-save putts"), ("Must-Make Finish", "Finish with 10 consecutive putts from 1 meter")]),
    ("lag_putting_session", "Lag Putting Session", "long-distance putting and three-putt prevention", [("8m Lag Putts", "Putt 30 balls from 8 meters"), ("12m Lag Putts", "Putt 30 balls from 12 meters"), ("16m Lag Putts", "Putt 30 balls from 16 meters"), ("20m Lag Putts", "Putt 30 balls from 20 meters"), ("1m Stop Circle", "Stop 30 balls inside a 1-meter circle"), ("50cm Stop Circle", "Stop 20 balls inside a 50-cm circle"), ("Two-Putt Challenge", "Complete 18 two-putt attempts"), ("Pressure Lag Putts", "Finish with 10 pressure lag putts")]),
    ("around_the_clock_putting_session", "Around-the-Clock Putting Session", "short-putt direction control", [("1m Clock Putts", "Make 3 putts from 12 positions around the hole"), ("1.5m Clock Putts", "Make 2 putts from 12 positions around the hole"), ("2m Clock Putts", "Make 1 putt from 12 positions around the hole"), ("Uphill Clock Putts", "Hit 20 uphill putts"), ("Downhill Clock Putts", "Hit 20 downhill putts"), ("Left-Break Clock Putts", "Hit 20 left-breaking putts"), ("Right-Break Clock Putts", "Hit 20 right-breaking putts"), ("Clock Pressure Finish", "Finish with 12 consecutive 1m makes around the hole")]),
    ("competitive_putting_challenge", "Competitive Putting Challenge", "scored putting competition", [("Short-Putt Score Challenge", "Make 50 putts from 1-2 meters and record makes"), ("Medium-Putt Score Challenge", "Hit 40 putts from 3-5 meters and record makes"), ("Lag-Putt Score Challenge", "Hit 30 putts from 10-20 meters and record proximity"), ("Breaking-Putt Challenge", "Hit 30 breaking putts"), ("Uphill/Downhill Challenge", "Hit 20 uphill and 20 downhill putts"), ("Three-Putt Avoidance", "Complete 18 holes of lag putting with no three-putts"), ("Match Play Putting", "Play 18 putting holes against par"), ("Sudden-Death Finish", "Finish with 10 must-make putts")]),
]
for slug, title, focus, items in _putting_sessions:
    key = f"golf_putting_{slug}"
    GOLF_CATALOG["putting"]["alone"][key] = _make_session("putting", slug, title, focus, items)

_course_sessions = [
    ("irons_only_nine", "Irons-Only 9-Hole Session", "course strategy with irons", [("Irons-Only Holes", "Play 9 holes using only irons"), ("Fairway Center Targets", "Aim every tee shot at the fairway center"), ("Green Center Targets", "Aim every approach at the green center"), ("No Hero Shots", "Choose the safest recovery option every time"), ("Club Selection Log", "Record club choice before every shot"), ("Miss Pattern Tracking", "Track every miss left, right, short, or long"), ("Two-Putt Goal", "Try to two-putt or better on every green"), ("Score Review", "Record score and decision quality after the round")]),
    ("fairway_center_nine", "Fairway Center 9-Hole Session", "tee-shot discipline", [("Fairway Center Plan", "Play 9 holes aiming only for fairway centers"), ("Conservative Tee Clubs", "Choose the safest tee club on every hole"), ("Avoid Penalty Zones", "Plan away from water, bunkers, and out-of-bounds"), ("Middle-Green Approach", "Aim approach shots at the middle of the green"), ("Lay-Up Decision", "Lay up whenever risk is greater than reward"), ("Pre-Shot Routine", "Complete full routine before every shot"), ("Fairway Hit Tracking", "Track fairways hit and misses"), ("Post-Round Review", "Write down three tee-shot decisions to improve")]),
    ("no_pin_attack_nine", "No Pin Attack 9-Hole Session", "safe approach strategy", [("No Pin Attacks", "Play 9 holes never attacking pins"), ("Green Center Aim", "Aim every approach at the safest part of the green"), ("Avoid Short-Siding", "Plan every miss away from short-side trouble"), ("Club Up When Needed", "Take one extra club when between distances"), ("Bunker Avoidance", "Aim away from greenside bunkers"), ("Two-Putt Focus", "Prioritize leaving first putts close"), ("Miss Tracking", "Record whether each miss was safe or dangerous"), ("Strategy Score", "Rate each hole decision from 1 to 5")]),
    ("conservative_eighteen", "Conservative 18-Hole Strategy", "low-risk scoring", [("Conservative Strategy", "Play 18 holes with conservative strategy"), ("Safest Tee Club", "Choose the club most likely to keep the ball in play"), ("Center-Green Approaches", "Aim at center green on every approach"), ("Lay Up On Risky Shots", "Lay up on all low-percentage shots"), ("Avoid Big Numbers", "Take the bogey-safe option when in trouble"), ("Putt Speed Control", "Prioritize distance control on every first putt"), ("Decision Tracking", "Track every conservative decision"), ("Full Score Review", "Compare score to normal aggressive round")]),
    ("aggressive_eighteen", "Aggressive 18-Hole Strategy", "attack strategy and scoring chances", [("Aggressive Strategy", "Play 18 holes with aggressive strategy"), ("Driver Usage", "Use driver when a clear scoring advantage exists"), ("Pin Attack Selection", "Attack accessible pins with good angles"), ("Risk-Reward Log", "Record every high-risk decision before hitting"), ("Par-5 Attack", "Go for reachable par-5s when safe enough"), ("Birdie Putt Tracking", "Track birdie chances created"), ("Recovery Plan", "Choose a defined recovery strategy after aggressive misses"), ("Score Review", "Compare scoring chances versus mistakes")]),
    ("three_club_round", "Three-Club 18-Hole Session", "creativity and shot control", [("Three-Club Round", "Play 18 holes using only three clubs"), ("Shot-Shaping Requirement", "Shape shots to cover missing clubs"), ("Half-Swing Approaches", "Use half-swings for distance gaps"), ("Bump-and-Run Short Game", "Use low running shots around greens"), ("Putting With Chosen Club", "Putt with one of the three selected clubs if putter is not chosen"), ("Course Positioning", "Prioritize angles over distance"), ("Distance Adaptation Log", "Record improvised distances"), ("Creativity Review", "Write down the three best improvised shots")]),
    ("decision_tracking_round", "Decision Tracking 18-Hole Session", "course decision audit", [("Decision Tracking", "Play 18 holes tracking every decision"), ("Pre-Shot Intent", "Write or state the target before every shot"), ("Risk Rating", "Rate each shot risk as low, medium, or high"), ("Club Justification", "Record why each club was selected"), ("Miss Plan", "Identify the safest miss before every full shot"), ("Emotional Control", "Record reaction after poor shots"), ("Result Tracking", "Compare intended target to actual result"), ("Decision Review", "Review the five best and five worst decisions")]),
    ("tournament_round_simulation", "Tournament Round Simulation", "full competitive scoring", [("Full Tournament Routine", "Simulate a tournament round with full scoring"), ("Official Pre-Shot Routine", "Use the same routine before every shot"), ("Scorecard Discipline", "Record score after every hole"), ("Rule Compliance", "Follow normal golf rules exactly"), ("Pressure Tee Shots", "Treat every tee shot as tournament pressure"), ("Conservative Recovery", "Use smart recovery after every miss"), ("Putting Routine", "Use full read and routine on every putt"), ("Post-Round Debrief", "Review score, penalties, fairways, greens, and putts")]),
]
for slug, title, focus, items in _course_sessions:
    key = f"golf_course_management_{slug}"
    GOLF_CATALOG["course_management"]["alone"][key] = _make_session("course_management", slug, title, focus, items)

_fitness_sessions = [
    ("rotational_power_session", "Rotational Power Session", "rotational strength and power", [("Medicine-Ball Rotational Throws", "4 x 15"), ("Russian Twists", "4 x 12"), ("Cable Rotations", "4 x 20"), ("Jump Squats", "4 x 12"), ("Walking Lunges", "4 x 15"), ("Planks", "4 x 45 seconds"), ("Back Extensions", "4 x 15"), ("Band Rotations", "4 x 20")]),
    ("core_stability_session", "Core Stability Session", "anti-rotation and posture control", [("Front Planks", "4 x 60 seconds"), ("Side Planks", "4 x 45 seconds each side"), ("Dead Bugs", "4 x 12 each side"), ("Pallof Press", "4 x 15 each side"), ("Bird Dogs", "4 x 12 each side"), ("Glute Bridges", "4 x 15"), ("Back Extensions", "4 x 15"), ("Slow Practice Swings", "4 x 15")]),
    ("mobility_session", "Golf Mobility Session", "hip, thoracic, and shoulder mobility", [("Thoracic Rotations", "4 x 12 each side"), ("Hip Openers", "4 x 12 each side"), ("World's Greatest Stretch", "4 x 8 each side"), ("Shoulder Dislocates With Band", "4 x 15"), ("Cat-Cow Mobility", "4 x 12"), ("90/90 Hip Switches", "4 x 12"), ("Ankle Mobility Rocks", "4 x 15 each side"), ("Slow Full-Swing Rehearsals", "4 x 10")]),
    ("lower_body_power_session", "Lower Body Power Session", "leg drive for golf swing", [("Jump Squats", "5 x 10"), ("Walking Lunges", "4 x 20"), ("Split Squats", "4 x 12 each side"), ("Lateral Bounds", "4 x 12 each side"), ("Romanian Deadlifts", "4 x 12"), ("Calf Raises", "4 x 20"), ("Wall Sits", "4 x 45 seconds"), ("Rotational Step-Through Swings", "4 x 12")]),
    ("upper_body_control_session", "Upper Body Control Session", "shoulder control and swing stability", [("Band Pull-Aparts", "4 x 20"), ("Push-Ups", "4 x 15"), ("Single-Arm Cable Rows", "4 x 12 each side"), ("External Rotations", "4 x 15 each side"), ("Scapular Push-Ups", "4 x 15"), ("Medicine-Ball Chest Pass", "4 x 12"), ("Band Rotations", "4 x 20"), ("Tempo Practice Swings", "4 x 15")]),
    ("balance_session", "Golf Balance Session", "finish stability and weight transfer", [("Single-Leg Balance", "4 x 60 seconds each side"), ("Single-Leg Romanian Deadlift", "4 x 10 each side"), ("Step-Ups", "4 x 12 each side"), ("Lateral Lunges", "4 x 12 each side"), ("Balance Finish Holds", "Hold finish for 5 seconds after 30 swings"), ("Bosu Or Cushion Holds", "4 x 45 seconds each side"), ("Slow-Motion Swings", "4 x 15"), ("Eyes-Closed Balance", "4 x 30 seconds each side")]),
    ("conditioning_session", "Golf Conditioning Session", "walking endurance and repeatability", [("Brisk Walk", "30 minutes"), ("Hill Walk Intervals", "8 x 2 minutes"), ("Bodyweight Squats", "4 x 20"), ("Walking Lunges", "4 x 20"), ("Farmer Carries", "4 x 40 meters"), ("Planks", "4 x 45 seconds"), ("Practice Swings Under Fatigue", "4 x 20"), ("Cool-Down Mobility", "10 minutes")]),
    ("tournament_fitness_session", "Tournament Fitness Session", "durability for full rounds", [("Dynamic Warm-Up", "10 minutes"), ("Medicine-Ball Rotational Throws", "4 x 12"), ("Walking Lunges", "4 x 20"), ("Band Rotations", "4 x 20"), ("Farmer Carries", "4 x 50 meters"), ("Side Planks", "4 x 45 seconds each side"), ("Practice Swings Under Fatigue", "60 swings"), ("Full Mobility Cool-Down", "10 minutes")]),
]
for slug, title, focus, items in _fitness_sessions:
    key = f"golf_golf_fitness_{slug}"
    GOLF_CATALOG["golf_fitness"]["alone"][key] = _make_session("golf_fitness", slug, title, focus, items)

_beginner_sessions = [
    ("learning_the_fundamentals", "Beginner Session 1: Learning the Fundamentals", "grip, setup, contact, chipping, and putting basics", [("Practice Grip Setup", "Hold the club correctly 30 times, resetting your hands each repetition"), ("Practice Golf Stance", "Set up in the correct stance 30 times, checking foot position and posture"), ("Alignment Drill", "Aim at a target and perform 30 setup checks before swinging"), ("Half Swing Shots", "Hit 50 balls using only a half swing"), ("Short Iron Contact Drill", "Hit 50 balls with a pitching wedge or 9-iron focusing only on clean contact"), ("Basic Chipping", "Chip 50 balls from 5 meters toward a target area"), ("Short Putting", "Make 50 putts from 1 meter"), ("Distance Putting", "Putt 30 balls from 5 meters, trying to stop each ball within 50 cm of the hole")]),
    ("making_consistent_contact", "Beginner Session 2: Making Consistent Contact", "repeatable contact and first pressure finish", [("Warm-Up Swings", "Perform 30 slow practice swings"), ("7-Iron Contact Drill", "Hit 75 balls with a 7-iron"), ("Target Practice", "Hit 50 shots toward a target 75-100 meters away"), ("Tee Shot Introduction", "Hit 30 drives from a tee at 70% power"), ("Chip and Stop Drill", "Chip 40 balls and try to stop them inside a 3-meter circle"), ("Bunker Introduction", "Hit 30 bunker shots"), ("2-Meter Putting Drill", "Make 40 putts from 2 meters"), ("Pressure Finish", "Make 10 consecutive putts from 1 meter before ending the session")]),
    ("building_a_complete_game", "Beginner Session 3: Building a Complete Game", "complete beginner skill mix", [("Practice Swing Mechanics", "Perform 30 slow-motion swings"), ("Iron Shot Ladder", "Hit 20 shots each with a pitching wedge, 9-iron, 8-iron, and 7-iron"), ("Driver Introduction", "Hit 40 drives at a fairway target"), ("Short Chip Drill", "Chip 30 balls from 5 meters"), ("Long Chip Drill", "Chip 30 balls from 15 meters"), ("Pitch Shot Drill", "Hit 30 pitch shots from 20-30 meters"), ("Distance Putting", "Putt 40 balls from 8-10 meters"), ("Short Putting", "Make 30 putts from 1.5 meters")]),
    ("first_course_preparation", "Beginner Session 4: First Course Preparation", "range-to-course transition", [("Alignment Checks", "Complete 30 setup and alignment repetitions"), ("Iron Accuracy Drill", "Hit 75 shots aiming at a target green"), ("Fairway Drill", "Hit 40 drives into a designated fairway area"), ("Chip Accuracy Drill", "Land 30 chips inside a 3-meter circle"), ("Pitch Accuracy Drill", "Land 30 pitch shots inside a 5-meter circle"), ("Bunker Practice", "Hit 40 bunker shots onto the green"), ("Lag Putting", "Putt 30 balls from 10 meters"), ("Short Putting", "Make 20 consecutive putts from 1 meter")]),
    ("simulated_beginner_round", "Beginner Session 5: Simulated Beginner Round", "first complete beginner round simulation", [("Hit 20 Drives", "Aim for accuracy, not distance"), ("Hit 40 Iron Approach Shots", "Alternate between 7-iron and 9-iron"), ("Chip 30 Balls", "From varying distances around the green"), ("Pitch 30 Balls", "From 20-40 meters"), ("Hit 20 Bunker Shots", "Focus on getting out of the sand on the first attempt"), ("Putt 30 Balls from 5 Meters", "Focus on distance control"), ("Make 30 Putts from 1 Meter", "Focus on consistency"), ("Play 3 Practice Holes", "Keep score and follow normal golf rules")]),
]
for slug, title, focus, items in _beginner_sessions:
    key = f"golf_beginner_{slug}"
    GOLF_CATALOG["beginner"]["alone"][key] = _make_session("beginner", slug, title, focus, items)


def get_golf_catalog() -> SportCatalog:
    """Return a deep copy of the full Golf catalog."""
    return deepcopy(GOLF_CATALOG)


def list_golf_sessions(category: Optional[str] = None, training_mode: Optional[str] = None) -> List[SportSession]:
    """List golf sessions, optionally filtered by category and/or training mode."""
    sessions: List[SportSession] = []
    categories = [category] if category else list(GOLF_CATALOG.keys())

    for category_name in categories:
        category_data = GOLF_CATALOG.get(category_name, {})
        modes = [training_mode] if training_mode else list(category_data.keys())
        for mode in modes:
            sessions.extend(deepcopy(list(category_data.get(mode, {}).values())))

    return sessions


def get_golf_session(
    session_key: str,
    category: Optional[str] = None,
    training_mode: Optional[str] = None,
) -> Optional[SportSession]:
    """Find one golf session by key, optionally narrowing by category and mode."""
    categories = [category] if category else list(GOLF_CATALOG.keys())

    for category_name in categories:
        category_data = GOLF_CATALOG.get(category_name, {})
        modes = [training_mode] if training_mode else list(category_data.keys())
        for mode in modes:
            found = category_data.get(mode, {}).get(session_key)
            if found:
                return deepcopy(found)

    return None


ALL_GOLF_SESSIONS: List[SportSession] = list_golf_sessions()


if __name__ == "__main__":
    print(f"Loaded {len(ALL_GOLF_SESSIONS)} golf sessions.")
