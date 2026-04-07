
import random
import re
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional

import streamlit as st


# =============================================================================
# ELITE / PRO TRAINING GENERATOR
# - Built from the user's original architecture
# - Same core idea preserved: structured sport library + dynamic session builder
# - Expanded for a more elite feel, deeper profiling, readiness, intensity,
#   progression, weekly planning, coaching notes, and better UI output
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

INTENSITY_MODES = ["Controlled", "Standard", "High", "Peak"]
READINESS_OPTIONS = ["Low", "Moderate", "High"]
PRIMARY_FOCUS_OPTIONS = ["Speed", "Power", "Technical Quality", "Conditioning", "Strength", "Movement Quality", "Match Rhythm"]
SEASON_PHASES = ["Off-Season", "Pre-Season", "In-Season", "Competition Block", "Return-to-Play Support"]


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


def build_future_api_payload(profile: Dict[str, object]) -> Dict[str, object]:
    return {
        "athlete_profile": profile,
        "generator_version": "training_generator_pro_v1_api_ready",
        "requested_output": {
            "format": "structured_elite_training_session",
            "needs_reasoning": True,
            "needs_professional_tone": True,
            "needs_measurable_prescriptions": True,
            "needs_sport_specific_progression": True,
            "needs_dynamic_time_allocation": True,
            "needs_readiness_adjustment": True,
            "needs_phase_context": True,
        },
        "future_modules": ["training_generation", "counseling", "video_review", "physio_support", "analytics_dashboard"],
        "api_status": "not_connected_yet",
    }


# -----------------------------------------------------------------------------
# TRAINING LIBRARY
# -----------------------------------------------------------------------------
SPORT_LIBRARY: Dict[str, Dict[str, List[Exercise]]] = {
    "Soccer": {
        "Warm-Up": [
            Exercise(
                "Jog + mobility flow", "Warm-Up", "6 minutes easy jog + 6 mobility reps each movement",
                "Raise body temperature and open hips/ankles.",
                ["Bodyweight", "Open space"], ["Low"], ["Movement Quality"], ["All"], ["Beginner", "Intermediate", "Advanced", "Elite"],
                ["Off-Season", "Pre-Season", "In-Season", "Competition Block"], 1.1,
                ["Stay tall through the trunk", "Increase range progressively"], ["Add skips between mobility drills"], ["Reduce ROM if stiff today"], []
            ),
            Exercise(
                "Dynamic activation", "Warm-Up", "2 rounds of 20m each: high knees, butt kicks, side shuffles",
                "Prepare sprint mechanics.",
                ["Open space"], ["Low", "Moderate"], ["Speed"], ["All"], ["Beginner", "Intermediate", "Advanced", "Elite"],
                ["Pre-Season", "In-Season", "Competition Block"], 0.9,
                ["Fast contacts, relaxed shoulders", "Finish each line with quality posture"], ["Add build-up accelerations"], ["Reduce total distance if fatigued"], []
            ),
            Exercise(
                "Acceleration prep runs", "Warm-Up", "4 reps x 12m progressive build-up",
                "Prime the nervous system before speed work.",
                ["Open space"], ["Moderate"], ["Speed"], ["Winger", "Striker", "Full Back", "Wing Back"], ["Intermediate", "Advanced", "Elite"],
                ["Pre-Season", "Competition Block"], 0.9,
                ["Start smooth, finish sharp", "Full intent without overreaching"], ["Add one more rep for advanced athletes"], ["Use 8m distance on low-readiness days"], []
            ),
        ],
        "Technical": [
            Exercise(
                "First-touch passing circuit", "Technical", "4 rounds x 3 minutes, 45 seconds rest",
                "Improve control and passing rhythm.",
                ["Ball", "Open space"], ["Moderate"], ["Technical Quality"], ["All"], ["Beginner", "Intermediate", "Advanced", "Elite"],
                ["Off-Season", "Pre-Season", "In-Season"], 1.0,
                ["Open body before reception", "Scan before first touch"], ["Limit touches", "Use weaker foot emphasis"], ["Increase space between reps"], []
            ),
            Exercise(
                "Dribble slalom + exit sprint", "Technical", "6 reps x 20m, walk-back recovery",
                "Tight control under speed.",
                ["Ball", "Cones"], ["Moderate", "High"], ["Speed", "Technical Quality"], ["Winger", "Striker", "Attacking Midfielder", "Full Back"], ["Intermediate", "Advanced", "Elite"],
                ["Pre-Season", "In-Season"], 0.85,
                ["Last touch sets up the sprint", "Keep center of mass under control"], ["Finish with shot or pass"], ["Shorten slalom distance"], []
            ),
            Exercise(
                "Crossing and finishing", "Technical", "5 reps each side + 10 finishes",
                "Wide delivery and box timing.",
                ["Ball", "Goal", "Field"], ["Moderate"], ["Technical Quality", "Match Rhythm"], ["Winger", "Full Back", "Wing Back", "Striker"], ["Intermediate", "Advanced", "Elite"],
                ["In-Season", "Competition Block"], 1.15,
                ["Attack the box with speed", "Quality over volume on delivery"], ["Add passive defender"], ["Reduce finishing volume"], []
            ),
            Exercise(
                "Short combination patterns", "Technical", "5 rounds x 90 seconds",
                "Improve one-touch rhythm and support angles.",
                ["Ball", "Cones"], ["Moderate"], ["Technical Quality"], ["Central Midfielder", "Attacking Midfielder", "Defensive Midfielder"], ["Intermediate", "Advanced", "Elite"],
                ["In-Season", "Competition Block"], 0.9,
                ["Third-man run timing matters", "Receive side-on when possible"], ["Add a pressing trigger"], ["Allow extra touch"], []
            ),
        ],
        "Physical": [
            Exercise(
                "Acceleration sprints", "Physical", "8 reps x 15m, 40 seconds rest",
                "Explosive first steps.",
                ["Open space"], ["High"], ["Speed"], ["All"], ["Intermediate", "Advanced", "Elite"],
                ["Pre-Season", "In-Season", "Competition Block"], 0.85,
                ["Win the first three steps", "Push, do not pop up early"], ["Add resisted starts"], ["Reduce to 6 reps"], ["Stop if hamstring tightness rises"]
            ),
            Exercise(
                "Repeated sprint block", "Physical", "2 sets of 6 x 20m, 20 seconds rest between reps, 2 minutes between sets",
                "Match-like repeatability.",
                ["Open space"], ["High"], ["Conditioning", "Speed"], ["All"], ["Advanced", "Elite"],
                ["Pre-Season", "In-Season"], 1.0,
                ["Keep mechanics even when tired", "Do not chase volume if speed collapses"], ["Add change of direction"], ["Reduce one rep per set"], ["Monitor heavy leg fatigue"]
            ),
            Exercise(
                "Split squats", "Physical", "3 sets x 8 reps each leg",
                "Single-leg strength.",
                ["Bodyweight", "Dumbbells"], ["Moderate"], ["Strength"], ["All"], ["Beginner", "Intermediate", "Advanced", "Elite"],
                ["Off-Season", "Pre-Season", "In-Season"], 0.9,
                ["Front foot rooted", "Control the bottom position"], ["Load heavier or pause 2 seconds"], ["Use bodyweight only"], []
            ),
            Exercise(
                "Nordic hamstring support", "Physical", "2-3 sets x 4-6 reps",
                "Posterior-chain resilience and sprint protection.",
                ["Bodyweight", "Partner"], ["Moderate", "High"], ["Strength", "Injury Prevention"], ["All"], ["Intermediate", "Advanced", "Elite"],
                ["Pre-Season", "In-Season"], 0.8,
                ["Control the lowering phase", "Quality beats max range"], ["Add one rep per set"], ["Shorter range"], ["Avoid if acute hamstring pain exists"]
            ),
        ],
        "Tactical": [
            Exercise(
                "Small-sided game", "Tactical", "4 rounds x 4 minutes, 2 minutes rest",
                "Decision-making under pressure.",
                ["Ball", "Field"], ["High"], ["Match Rhythm", "Conditioning"], ["All"], ["Intermediate", "Advanced", "Elite"],
                ["Pre-Season", "In-Season"], 1.3,
                ["Coach transitions aggressively", "Manipulate space to target the objective"], ["Touch limits or overload side"], ["Reduce pitch size and work time"], []
            ),
            Exercise(
                "Pressing shape rehearsal", "Tactical", "5 rounds x 2 minutes",
                "Team organization and triggers.",
                ["Ball", "Field"], ["Moderate"], ["Technical Quality", "Match Rhythm"], ["All"], ["Intermediate", "Advanced", "Elite"],
                ["In-Season", "Competition Block"], 0.95,
                ["First presser sets the cue", "Back line must stay connected"], ["Add directional target"], ["Walk-through intensity"], []
            ),
        ],
        "Recovery": [
            Exercise(
                "Breathing walk + stretch", "Recovery", "6 minutes walk + 30 seconds per stretch",
                "Downregulate and improve recovery.",
                ["Bodyweight"], ["Low"], ["Movement Quality"], ["All"], ["Beginner", "Intermediate", "Advanced", "Elite"],
                ["Off-Season", "Pre-Season", "In-Season", "Competition Block"], 0.8,
                ["Long exhale, slow nasal inhale", "Stretch what feels most loaded today"], ["Add light foam roll"], ["Reduce total hold time"], []
            ),
        ],
    },

    "Basketball": {
        "Warm-Up": [
            Exercise("Court movement warm-up", "Warm-Up", "2 rounds of 4 minutes", "Prepare hips, calves, shoulders.", ["Court"], ["Low"], ["Movement Quality"], ["All"], ["Beginner", "Intermediate", "Advanced", "Elite"], ["All"], 1.0),
            Exercise("Ball-handling activation", "Warm-Up", "3 minutes continuous", "Wake up handle and coordination.", ["Ball"], ["Low"], ["Technical Quality"], ["Guard", "Point Guard", "Shooting Guard"], ["Beginner", "Intermediate", "Advanced", "Elite"], ["All"], 0.8),
            Exercise("Landing prep series", "Warm-Up", "2 sets x 5 snap-downs + 2 sets x 5 pogo jumps", "Prime safe landing mechanics.", ["Court"], ["Low", "Moderate"], ["Power", "Movement Quality"], ["All"], ["Intermediate", "Advanced", "Elite"], ["All"], 0.85),
        ],
        "Technical": [
            Exercise("Form shooting", "Technical", "25 made shots", "Shooting mechanics.", ["Ball", "Court"], ["Low", "Moderate"], ["Technical Quality"], ["All"], ["Beginner", "Intermediate", "Advanced", "Elite"], ["All"], 0.95),
            Exercise("Cone change-of-direction dribble", "Technical", "6 reps each side", "Ball control and footwork.", ["Ball", "Cones"], ["Moderate"], ["Speed", "Technical Quality"], ["Point Guard", "Shooting Guard", "Small Forward"], ["Intermediate", "Advanced", "Elite"], ["All"], 0.85),
            Exercise("Pick-and-roll reads", "Technical", "4 rounds x 3 minutes", "Game reads.", ["Ball", "Court"], ["Moderate"], ["Technical Quality", "Match Rhythm"], ["Point Guard", "Center", "Power Forward"], ["Intermediate", "Advanced", "Elite"], ["In-Season", "Competition Block"], 1.1),
            Exercise("Closeout to contest drill", "Technical", "5 rounds x 4 reps", "Defensive footwork and control.", ["Court", "Ball"], ["Moderate"], ["Movement Quality", "Technical Quality"], ["All"], ["Intermediate", "Advanced", "Elite"], ["All"], 0.9),
        ],
        "Physical": [
            Exercise("Countermovement jumps", "Physical", "4 sets x 5 reps", "Vertical power.", ["Bodyweight"], ["High"], ["Power"], ["All"], ["Intermediate", "Advanced", "Elite"], ["Off-Season", "Pre-Season", "In-Season"], 0.8),
            Exercise("Defensive slide intervals", "Physical", "6 reps x 20 seconds, 40 seconds rest", "Lateral conditioning.", ["Court"], ["High"], ["Conditioning", "Movement Quality"], ["All"], ["Intermediate", "Advanced", "Elite"], ["Pre-Season", "In-Season"], 0.9),
            Exercise("Push-ups", "Physical", "3 sets x 10-15 reps", "Upper-body strength.", ["Bodyweight"], ["Moderate"], ["Strength"], ["All"], ["Beginner", "Intermediate", "Advanced"], ["Off-Season", "Pre-Season", "In-Season"], 0.8),
            Exercise("Rear-foot elevated split squat", "Physical", "3 sets x 8 reps each leg", "Single-leg strength and deceleration support.", ["Bench", "Dumbbells"], ["Moderate"], ["Strength"], ["All"], ["Intermediate", "Advanced", "Elite"], ["Off-Season", "Pre-Season", "In-Season"], 0.95),
        ],
        "Tactical": [
            Exercise("Advantage game", "Tactical", "5 rounds x 3 minutes", "Transition decisions.", ["Ball", "Court"], ["High"], ["Match Rhythm"], ["All"], ["Intermediate", "Advanced", "Elite"], ["In-Season", "Competition Block"], 1.15),
        ],
        "Recovery": [
            Exercise("Light mobility", "Recovery", "8 minutes", "Joint recovery.", ["Bodyweight"], ["Low"], ["Movement Quality"], ["All"], ["Beginner", "Intermediate", "Advanced", "Elite"], ["All"], 0.8),
        ],
    },

    "Tennis": {
        "Warm-Up": [
            Exercise("Mini tennis + mobility", "Warm-Up", "8 minutes total", "Feel and footwork.", ["Racket", "Ball", "Court"], ["Low"], ["Technical Quality", "Movement Quality"], ["All"], ["Beginner", "Intermediate", "Advanced", "Elite"], ["All"], 1.1),
            Exercise("Split-step reaction drill", "Warm-Up", "3 sets x 45 seconds", "Timing and readiness.", ["Court"], ["Moderate"], ["Speed"], ["All"], ["Intermediate", "Advanced", "Elite"], ["All"], 0.75),
            Exercise("Serve shoulder prep", "Warm-Up", "2 sets x 8 reps each movement", "Prepare the shoulder complex for serving volume.", ["Bands", "Bodyweight"], ["Low"], ["Movement Quality"], ["Singles Player", "Doubles Specialist", "Serve-and-Volley Player"], ["Intermediate", "Advanced", "Elite"], ["All"], 0.8),
        ],
        "Technical": [
            Exercise("Crosscourt consistency", "Technical", "4 rounds x 4 minutes", "Rally tolerance.", ["Racket", "Ball", "Court"], ["Moderate"], ["Technical Quality", "Conditioning"], ["Baseline Player", "All-Court Player", "Singles Player"], ["Intermediate", "Advanced", "Elite"], ["All"], 1.2),
            Exercise("Serve targets", "Technical", "30 first serves + 20 second serves", "Placement and confidence.", ["Racket", "Ball", "Court"], ["Moderate"], ["Technical Quality"], ["Serve-and-Volley Player", "Singles Player", "Doubles Specialist"], ["Intermediate", "Advanced", "Elite"], ["All"], 1.0),
            Exercise("Approach + volley sequence", "Technical", "12 reps each side", "Net transition.", ["Racket", "Ball", "Court"], ["Moderate"], ["Technical Quality", "Match Rhythm"], ["Serve-and-Volley Player", "All-Court Player", "Doubles Specialist"], ["Intermediate", "Advanced", "Elite"], ["In-Season", "Competition Block"], 0.9),
            Exercise("Backhand pattern under pressure", "Technical", "5 rounds x 6 balls", "Stabilize the weaker wing under speed and direction change.", ["Racket", "Ball", "Court"], ["Moderate", "High"], ["Technical Quality"], ["Singles Player", "Baseline Player", "All-Court Player"], ["Intermediate", "Advanced", "Elite"], ["All"], 0.95),
        ],
        "Physical": [
            Exercise("Lateral shuffle intervals", "Physical", "6 reps x 20 seconds, 40 seconds rest", "Court movement endurance.", ["Court"], ["High"], ["Conditioning", "Movement Quality"], ["All"], ["Intermediate", "Advanced", "Elite"], ["Pre-Season", "In-Season"], 0.85),
            Exercise("Medicine ball rotations", "Physical", "3 sets x 10 reps each side", "Rotational power.", ["Medicine ball"], ["Moderate"], ["Power"], ["All"], ["Intermediate", "Advanced", "Elite"], ["Off-Season", "Pre-Season", "In-Season"], 0.85),
            Exercise("Reverse lunges", "Physical", "3 sets x 8 reps each leg", "Lower-body control.", ["Bodyweight", "Dumbbells"], ["Moderate"], ["Strength"], ["All"], ["Beginner", "Intermediate", "Advanced", "Elite"], ["All"], 0.85),
            Exercise("Reactive first-step drill", "Physical", "8 reps x 5-8 seconds", "Explosive response to directional cues.", ["Court", "Cones"], ["High"], ["Speed"], ["All"], ["Intermediate", "Advanced", "Elite"], ["Pre-Season", "Competition Block"], 0.8),
        ],
        "Tactical": [
            Exercise("Pattern play", "Tactical", "5 rounds x 3 points per pattern", "Build point construction.", ["Racket", "Ball", "Court"], ["Moderate"], ["Match Rhythm", "Technical Quality"], ["All"], ["Intermediate", "Advanced", "Elite"], ["In-Season", "Competition Block"], 1.0),
            Exercise("Scoreboard pressure game", "Tactical", "4 rounds starting at 30-30", "Decision-making under pressure.", ["Racket", "Ball", "Court"], ["High"], ["Match Rhythm"], ["All"], ["Advanced", "Elite"], ["Competition Block"], 0.9),
        ],
        "Recovery": [
            Exercise("Forearm/hip mobility", "Recovery", "6 minutes", "Reduce stiffness.", ["Bodyweight"], ["Low"], ["Movement Quality"], ["All"], ["Beginner", "Intermediate", "Advanced", "Elite"], ["All"], 0.75),
        ],
    },

    "Volleyball": {
        "Warm-Up": [
            Exercise("Dynamic court warm-up", "Warm-Up", "7 minutes", "General readiness.", ["Court"], ["Low"], ["Movement Quality"], ["All"], ["All"], ["All"], 1.0),
            Exercise("Arm swing activation", "Warm-Up", "2 sets x 12 reps", "Shoulder prep.", ["Bands", "Bodyweight"], ["Low"], ["Movement Quality"], ["All"], ["All"], ["All"], 0.75),
            Exercise("Landing mechanics primer", "Warm-Up", "2 sets x 5 jumps with stick landing", "Jump-readiness and safe deceleration.", ["Court"], ["Low", "Moderate"], ["Power", "Movement Quality"], ["All"], ["Intermediate", "Advanced", "Elite"], ["All"], 0.8),
        ],
        "Technical": [
            Exercise("Serve receive reps", "Technical", "20 quality passes", "Platform control.", ["Ball", "Court"], ["Moderate"], ["Technical Quality"], ["Libero", "Defensive Specialist", "Outside Hitter"], ["All"], ["All"], 0.95),
            Exercise("Setting accuracy", "Technical", "4 rounds x 2 minutes", "Tempo and placement.", ["Ball", "Court"], ["Moderate"], ["Technical Quality"], ["Setter"], ["All"], ["All"], 0.9),
            Exercise("Approach jump spikes", "Technical", "5 sets x 4 reps", "Timing and hitting mechanics.", ["Ball", "Court"], ["Moderate", "High"], ["Technical Quality", "Power"], ["Outside Hitter", "Opposite", "Middle Blocker"], ["Intermediate", "Advanced", "Elite"], ["All"], 1.0),
            Exercise("Block footwork sequence", "Technical", "5 rounds x 4 reps", "Improve shuffle and cross-over to block.", ["Court"], ["Moderate"], ["Technical Quality", "Movement Quality"], ["Middle Blocker", "Opposite", "Outside Hitter"], ["Intermediate", "Advanced", "Elite"], ["All"], 0.85),
        ],
        "Physical": [
            Exercise("Block jumps", "Physical", "4 sets x 5 reps", "Explosive jumping.", ["Court"], ["High"], ["Power"], ["Middle Blocker", "Opposite", "Outside Hitter"], ["Intermediate", "Advanced", "Elite"], ["Pre-Season", "In-Season"], 0.85),
            Exercise("Band external rotations", "Physical", "3 sets x 12 reps", "Shoulder integrity.", ["Bands"], ["Low", "Moderate"], ["Injury Prevention"], ["All"], ["All"], ["All"], 0.75),
            Exercise("Tempo squats", "Physical", "3 sets x 8 reps", "Leg strength.", ["Bodyweight", "Dumbbells", "Barbell"], ["Moderate"], ["Strength"], ["All"], ["Intermediate", "Advanced", "Elite"], ["Off-Season", "Pre-Season", "In-Season"], 0.95),
            Exercise("Lateral shuffle-to-drop step", "Physical", "6 reps each side", "Fast defensive movement patterns.", ["Court"], ["High"], ["Speed"], ["Libero", "Defensive Specialist", "Setter"], ["Intermediate", "Advanced", "Elite"], ["Pre-Season", "In-Season"], 0.8),
        ],
        "Tactical": [
            Exercise("6v6 situational play", "Tactical", "4 rounds x 5 minutes", "Rotation and decision-making.", ["Ball", "Court"], ["High"], ["Match Rhythm"], ["All"], ["Intermediate", "Advanced", "Elite"], ["In-Season", "Competition Block"], 1.2),
        ],
        "Recovery": [
            Exercise("Shoulder and calf stretch", "Recovery", "6 minutes", "Restore range of motion.", ["Bodyweight"], ["Low"], ["Movement Quality"], ["All"], ["All"], ["All"], 0.75),
        ],
    },

    "Water Polo": {
        "Warm-Up": [
            Exercise("Swim + eggbeater prep", "Warm-Up", "200m easy swim + 3 x 30 seconds eggbeater", "Pool readiness.", ["Pool"], ["Low"], ["Movement Quality"], ["All"], ["All"], ["All"], 1.1),
            Exercise("Shoulder mobility", "Warm-Up", "2 sets x 10 reps", "Throwing prep.", ["Bodyweight", "Bands"], ["Low"], ["Movement Quality"], ["All"], ["All"], ["All"], 0.75),
            Exercise("Reaction swim starts", "Warm-Up", "6 reps x 6-8m", "Prime fast first movement in the water.", ["Pool"], ["Moderate"], ["Speed"], ["Goalkeeper", "Driver", "Wing", "Point"], ["Intermediate", "Advanced", "Elite"], ["In-Season", "Competition Block"], 0.8),
        ],
        "Technical": [
            Exercise("Passing on the move", "Technical", "4 rounds x 3 minutes", "Ball speed and accuracy.", ["Pool", "Ball"], ["Moderate"], ["Technical Quality"], ["All"], ["All"], ["All"], 1.0),
            Exercise("Shooting corners", "Technical", "20 shots total", "Finishing.", ["Pool", "Ball", "Goal"], ["Moderate"], ["Technical Quality"], ["Wing", "Point", "Driver", "Center Forward"], ["Intermediate", "Advanced", "Elite"], ["All"], 0.95),
            Exercise("Center battle positioning", "Technical", "6 reps x 20 seconds", "Body position under contact.", ["Pool", "Ball"], ["High"], ["Strength", "Technical Quality"], ["Center Forward", "Center Back"], ["Intermediate", "Advanced", "Elite"], ["In-Season"], 0.9),
            Exercise("Goalkeeper angle set drill", "Technical", "5 rounds x 5 reps", "Line, angle and explosive reaction.", ["Pool", "Ball", "Goal"], ["Moderate"], ["Technical Quality", "Speed"], ["Goalkeeper"], ["Intermediate", "Advanced", "Elite"], ["All"], 0.9),
        ],
        "Physical": [
            Exercise("Sprint swims", "Physical", "8 reps x 15m, 30 seconds rest", "Explosive swimming.", ["Pool"], ["High"], ["Speed"], ["All"], ["Intermediate", "Advanced", "Elite"], ["Pre-Season", "In-Season"], 0.9),
            Exercise("Eggbeater hold", "Physical", "4 reps x 40 seconds", "Leg endurance.", ["Pool"], ["High"], ["Conditioning", "Strength"], ["All"], ["Intermediate", "Advanced", "Elite"], ["All"], 0.85),
            Exercise("Pull-ups or band pulls", "Physical", "3 sets x 6-10 reps", "Upper-body strength.", ["Pull-up bar", "Bands"], ["Moderate"], ["Strength"], ["All"], ["Beginner", "Intermediate", "Advanced", "Elite"], ["All"], 0.85),
            Exercise("Medicine ball overhead throw", "Physical", "3 sets x 6 reps", "Throwing power transfer.", ["Medicine ball"], ["Moderate", "High"], ["Power"], ["Point", "Wing", "Driver"], ["Intermediate", "Advanced", "Elite"], ["Off-Season", "Pre-Season"], 0.8),
        ],
        "Tactical": [
            Exercise("6-on-5 execution", "Tactical", "5 rounds x 90 seconds", "Special situation organization.", ["Pool", "Ball"], ["Moderate", "High"], ["Match Rhythm"], ["All"], ["Intermediate", "Advanced", "Elite"], ["In-Season", "Competition Block"], 1.0),
        ],
        "Recovery": [
            Exercise("Easy backstroke + stretch", "Recovery", "5 minutes swim + 5 minutes stretch", "Recovery.", ["Pool"], ["Low"], ["Movement Quality"], ["All"], ["All"], ["All"], 0.9),
        ],
    },

    "Baseball": {
        "Warm-Up": [
            Exercise("Throwing prep warm-up", "Warm-Up", "8 minutes", "Arm and hip readiness.", ["Ball", "Open space"], ["Low"], ["Movement Quality"], ["All"], ["All"], ["All"], 1.0),
            Exercise("Scap activation series", "Warm-Up", "2 sets x 10 reps", "Shoulder blade control before throwing or hitting.", ["Bands"], ["Low"], ["Movement Quality"], ["All"], ["All"], ["All"], 0.75),
        ],
        "Technical": [
            Exercise("Fielding fundamentals", "Technical", "4 rounds x 8 reps", "Clean glove work.", ["Ball", "Field"], ["Moderate"], ["Technical Quality"], ["All"], ["All"], ["All"], 1.0),
            Exercise("Bat speed tee work", "Technical", "5 rounds x 6 swings", "Quality contact.", ["Bat", "Ball", "Field"], ["Moderate"], ["Technical Quality", "Power"], ["All"], ["Intermediate", "Advanced", "Elite"], ["All"], 0.95),
            Exercise("Long toss progression", "Technical", "10 minutes", "Throwing capacity.", ["Ball", "Field"], ["Moderate"], ["Technical Quality", "Strength"], ["Pitcher", "Catcher", "Outfielder"], ["Intermediate", "Advanced", "Elite"], ["All"], 1.05),
            Exercise("Pitch command sequence", "Technical", "4 rounds x 8 pitches", "Zone feel and repeatable mechanics.", ["Ball", "Field"], ["Moderate"], ["Technical Quality"], ["Pitcher"], ["Intermediate", "Advanced", "Elite"], ["In-Season", "Competition Block"], 1.0),
        ],
        "Physical": [
            Exercise("Rotational med-ball throws", "Physical", "3 sets x 8 reps each side", "Power transfer.", ["Medicine ball"], ["Moderate", "High"], ["Power"], ["All"], ["Intermediate", "Advanced", "Elite"], ["Off-Season", "Pre-Season"], 0.85),
            Exercise("Broad jumps", "Physical", "4 sets x 4 reps", "Lower-body power.", ["Bodyweight"], ["High"], ["Power"], ["All"], ["Intermediate", "Advanced", "Elite"], ["Off-Season", "Pre-Season"], 0.8),
            Exercise("Rear-foot elevated split squat", "Physical", "3 sets x 8 reps each leg", "Single-leg strength.", ["Bench", "Dumbbells"], ["Moderate"], ["Strength"], ["All"], ["Intermediate", "Advanced", "Elite"], ["All"], 0.9),
            Exercise("Farmer carry", "Physical", "4 reps x 20-30m", "Grip, trunk and postural strength.", ["Dumbbells", "Kettlebells"], ["Moderate"], ["Strength"], ["All"], ["Intermediate", "Advanced", "Elite"], ["All"], 0.8),
        ],
        "Tactical": [
            Exercise("Situational defense", "Tactical", "4 rounds x 3 minutes", "Game IQ.", ["Field", "Ball"], ["Moderate"], ["Match Rhythm"], ["All"], ["Intermediate", "Advanced", "Elite"], ["In-Season", "Competition Block"], 1.0),
        ],
        "Recovery": [
            Exercise("Posterior shoulder care", "Recovery", "6 minutes", "Arm recovery.", ["Bands", "Bodyweight"], ["Low"], ["Movement Quality", "Injury Prevention"], ["All"], ["All"], ["All"], 0.8),
        ],
    },

    "Running": {
        "Warm-Up": [
            Exercise("Run warm-up", "Warm-Up", "8 minutes easy + drills", "Prepare gait and tissue stiffness.", ["Open space"], ["Low"], ["Movement Quality"], ["All"], ["All"], ["All"], 1.0),
            Exercise("Ankling and A-skip series", "Warm-Up", "2 rounds x 20m each", "Improve ground contact quality.", ["Track", "Road", "Open space"], ["Low", "Moderate"], ["Speed", "Movement Quality"], ["Sprinter", "Middle Distance"], ["Intermediate", "Advanced", "Elite"], ["All"], 0.8),
        ],
        "Technical": [
            Exercise("Strides", "Technical", "6 reps x 80m", "Running form at speed.", ["Track", "Road", "Open space"], ["Moderate"], ["Speed"], ["All"], ["Intermediate", "Advanced", "Elite"], ["All"], 0.85),
            Exercise("Hill mechanics", "Technical", "6 reps x 12 seconds", "Drive and posture.", ["Hill", "Open space"], ["High"], ["Speed", "Power"], ["Sprinter", "Middle Distance", "Trail Runner"], ["Intermediate", "Advanced", "Elite"], ["Pre-Season", "Off-Season"], 0.8),
            Exercise("Cadence control block", "Technical", "4 rounds x 2 minutes", "Economy and rhythm awareness.", ["Track", "Road"], ["Moderate"], ["Technical Quality", "Conditioning"], ["Long Distance", "Middle Distance"], ["Intermediate", "Advanced", "Elite"], ["In-Season", "Competition Block"], 0.9),
        ],
        "Physical": [
            Exercise("Main aerobic set", "Physical", "20-45 minutes depending on level", "Aerobic development.", ["Track", "Road", "Trail"], ["Moderate", "High"], ["Conditioning"], ["Middle Distance", "Long Distance", "Trail Runner"], ["Beginner", "Intermediate", "Advanced", "Elite"], ["All"], 2.2),
            Exercise("Calf raises", "Physical", "3 sets x 15 reps", "Lower-leg resilience.", ["Bodyweight", "Dumbbells"], ["Moderate"], ["Strength", "Injury Prevention"], ["All"], ["All"], ["All"], 0.7),
            Exercise("Dead bugs", "Physical", "3 sets x 10 reps each side", "Core stability.", ["Bodyweight"], ["Low", "Moderate"], ["Strength"], ["All"], ["All"], ["All"], 0.7),
            Exercise("Sprint build-up reps", "Physical", "6 reps x 60m progressive", "Speed exposure without full maxing out.", ["Track", "Open space"], ["High"], ["Speed"], ["Sprinter", "Middle Distance"], ["Intermediate", "Advanced", "Elite"], ["Pre-Season", "Competition Block"], 0.9),
        ],
        "Tactical": [
            Exercise("Pacing rehearsal", "Tactical", "3 rounds x 5 minutes", "Race awareness.", ["Track", "Road"], ["Moderate"], ["Match Rhythm"], ["Middle Distance", "Long Distance", "Trail Runner"], ["Intermediate", "Advanced", "Elite"], ["In-Season", "Competition Block"], 1.1),
        ],
        "Recovery": [
            Exercise("Walk + mobility", "Recovery", "10 minutes", "Bring heart rate down.", ["Bodyweight"], ["Low"], ["Movement Quality"], ["All"], ["All"], ["All"], 0.9),
        ],
    },

    "Gym": {
        "Warm-Up": [
            Exercise("Cardio primer + mobility", "Warm-Up", "6 minutes cardio + 6 reps per mobility drill", "General prep.", ["Cardio machine", "Bodyweight"], ["Low"], ["Movement Quality"], ["All"], ["All"], ["All"], 1.0),
            Exercise("Bracing and hinge prep", "Warm-Up", "2 rounds x 5 reps each", "Prime safer lifting mechanics.", ["Bodyweight", "Bands"], ["Low"], ["Movement Quality"], ["Athletic Performance", "Hypertrophy", "General Fitness"], ["All"], ["All"], 0.8),
        ],
        "Technical": [
            Exercise("Movement pattern rehearsal", "Technical", "2 light sets per lift", "Safer lifting.", ["Barbell", "Dumbbells", "Machines"], ["Low"], ["Technical Quality"], ["All"], ["All"], ["All"], 0.7),
            Exercise("Tempo skill set", "Technical", "2 sets x 5 reps at controlled tempo", "Improve position awareness.", ["Barbell", "Dumbbells"], ["Low", "Moderate"], ["Technical Quality"], ["All"], ["All"], ["All"], 0.75),
        ],
        "Physical": [
            Exercise("Squat or leg press", "Physical", "4 sets x 6-10 reps", "Lower-body strength.", ["Barbell", "Machine"], ["Moderate", "High"], ["Strength"], ["Hypertrophy", "Athletic Performance", "General Fitness"], ["Intermediate", "Advanced", "Elite"], ["Off-Season", "Pre-Season", "In-Season"], 1.2),
            Exercise("Bench or push variation", "Physical", "4 sets x 6-10 reps", "Upper-body pushing.", ["Barbell", "Dumbbells", "Machine"], ["Moderate", "High"], ["Strength"], ["All"], ["Intermediate", "Advanced", "Elite"], ["All"], 1.05),
            Exercise("Row or pull variation", "Physical", "4 sets x 8-12 reps", "Upper-body pulling.", ["Barbell", "Dumbbells", "Machine"], ["Moderate", "High"], ["Strength"], ["All"], ["Intermediate", "Advanced", "Elite"], ["All"], 1.05),
            Exercise("Conditioning finisher", "Physical", "8-12 minutes", "Work capacity.", ["Cardio machine", "Bodyweight"], ["High"], ["Conditioning"], ["Fat Loss", "General Fitness", "Athletic Performance"], ["Intermediate", "Advanced", "Elite"], ["Off-Season", "Pre-Season", "In-Season"], 1.0),
            Exercise("Trap bar jump or med-ball throw", "Physical", "4 sets x 3-5 reps", "Fast force development.", ["Trap bar", "Medicine ball"], ["High"], ["Power"], ["Athletic Performance"], ["Advanced", "Elite"], ["Off-Season", "Pre-Season"], 0.8),
        ],
        "Tactical": [
            Exercise("Tempo control", "Tactical", "Apply 2-0-2 tempo on first 2 exercises", "Technique discipline.", ["Barbell", "Dumbbells", "Machine"], ["Low"], ["Technical Quality"], ["All"], ["All"], ["All"], 0.6),
        ],
        "Recovery": [
            Exercise("Cooldown stretch", "Recovery", "6 minutes", "Recovery.", ["Bodyweight"], ["Low"], ["Movement Quality"], ["All"], ["All"], ["All"], 0.75),
        ],
    },

    "Weightlifting": {
        "Warm-Up": [
            Exercise("Barbell prep sequence", "Warm-Up", "8 minutes", "Mobility and groove.", ["Barbell", "Open space"], ["Low"], ["Movement Quality"], ["All"], ["All"], ["All"], 1.0),
            Exercise("Overhead position primer", "Warm-Up", "2 sets x 5 reps", "Open thoracic and overhead mechanics.", ["PVC", "Barbell"], ["Low"], ["Movement Quality"], ["Snatch Focus", "General Weightlifting"], ["Intermediate", "Advanced", "Elite"], ["All"], 0.8),
        ],
        "Technical": [
            Exercise("Snatch technique", "Technical", "6 sets x 2 reps", "Bar path and speed.", ["Barbell"], ["Moderate", "High"], ["Technical Quality", "Power"], ["Snatch Focus", "General Weightlifting"], ["Intermediate", "Advanced", "Elite"], ["All"], 1.25),
            Exercise("Clean and jerk technique", "Technical", "5 sets x 2 reps", "Coordination.", ["Barbell"], ["Moderate", "High"], ["Technical Quality", "Power"], ["Clean and Jerk Focus", "General Weightlifting"], ["Intermediate", "Advanced", "Elite"], ["All"], 1.2),
            Exercise("Segment lift practice", "Technical", "4 sets x 2 reps", "Strengthen precision in the weakest phase.", ["Barbell"], ["Moderate"], ["Technical Quality"], ["All"], ["Intermediate", "Advanced", "Elite"], ["All"], 1.0),
        ],
        "Physical": [
            Exercise("Front squat", "Physical", "4 sets x 3-5 reps", "Strength for receiving positions.", ["Barbell"], ["High"], ["Strength"], ["All"], ["Intermediate", "Advanced", "Elite"], ["All"], 1.0),
            Exercise("Pulls", "Physical", "4 sets x 3 reps", "Explosive extension.", ["Barbell"], ["High"], ["Power"], ["All"], ["Intermediate", "Advanced", "Elite"], ["All"], 0.95),
            Exercise("Core holds", "Physical", "3 sets x 30-45 seconds", "Trunk stiffness.", ["Bodyweight"], ["Moderate"], ["Strength"], ["All"], ["Beginner", "Intermediate", "Advanced", "Elite"], ["All"], 0.75),
            Exercise("Push press", "Physical", "4 sets x 3 reps", "Overhead power transfer.", ["Barbell"], ["High"], ["Power"], ["Clean and Jerk Focus", "General Weightlifting"], ["Intermediate", "Advanced", "Elite"], ["Off-Season", "Pre-Season"], 0.85),
        ],
        "Tactical": [
            Exercise("Attempt selection practice", "Tactical", "3 mock waves", "Meet strategy.", ["Barbell"], ["Moderate"], ["Match Rhythm"], ["All"], ["Intermediate", "Advanced", "Elite"], ["Competition Block"], 0.7),
        ],
        "Recovery": [
            Exercise("Thoracic/ankle mobility", "Recovery", "8 minutes", "Position restoration.", ["Bodyweight"], ["Low"], ["Movement Quality"], ["All"], ["All"], ["All"], 0.8),
        ],
    },

    "Rowing": {
        "Warm-Up": [
            Exercise("Erg + mobility prep", "Warm-Up", "5 minutes erg + 5 minutes mobility", "Stroke prep.", ["Rowing erg", "Bodyweight"], ["Low"], ["Movement Quality"], ["All"], ["All"], ["All"], 1.0),
            Exercise("Stroke pick drill", "Warm-Up", "2 rounds x 2 minutes", "Reconnect rhythm from arms-only to full stroke.", ["Boat", "Erg"], ["Low"], ["Technical Quality"], ["Sweep Rower", "Sculler", "Indoor Rower"], ["Beginner", "Intermediate", "Advanced", "Elite"], ["All"], 0.85),
        ],
        "Technical": [
            Exercise("Pause drill", "Technical", "4 rounds x 3 minutes", "Sequencing.", ["Boat", "Erg"], ["Moderate"], ["Technical Quality"], ["Sweep Rower", "Sculler", "Indoor Rower"], ["All"], ["All"], 1.0),
            Exercise("Rate ladder", "Technical", "3 rounds x 4 minutes", "Control at different rates.", ["Boat", "Erg"], ["Moderate", "High"], ["Technical Quality", "Conditioning"], ["Sweep Rower", "Sculler", "Indoor Rower"], ["Intermediate", "Advanced", "Elite"], ["All"], 1.05),
            Exercise("Catch timing set", "Technical", "5 rounds x 90 seconds", "Sharper placement and front-end timing.", ["Boat", "Erg"], ["Moderate"], ["Technical Quality"], ["Sweep Rower", "Sculler"], ["Intermediate", "Advanced", "Elite"], ["All"], 0.9),
        ],
        "Physical": [
            Exercise("Main erg piece", "Physical", "3 x 8 minutes, 2 minutes rest", "Aerobic power.", ["Rowing erg"], ["High"], ["Conditioning"], ["Indoor Rower", "Sweep Rower", "Sculler"], ["Intermediate", "Advanced", "Elite"], ["Pre-Season", "In-Season"], 1.6),
            Exercise("Romanian deadlift", "Physical", "3 sets x 8 reps", "Posterior chain.", ["Barbell", "Dumbbells"], ["Moderate"], ["Strength"], ["All"], ["Intermediate", "Advanced", "Elite"], ["All"], 0.9),
            Exercise("Plank", "Physical", "3 reps x 40 seconds", "Core endurance.", ["Bodyweight"], ["Moderate"], ["Strength"], ["All"], ["All"], ["All"], 0.7),
            Exercise("Leg drive intervals", "Physical", "5 reps x 45 seconds", "Specific power endurance for the drive phase.", ["Erg"], ["High"], ["Power", "Conditioning"], ["Indoor Rower", "Sweep Rower", "Sculler"], ["Intermediate", "Advanced", "Elite"], ["Pre-Season", "In-Season"], 0.85),
        ],
        "Tactical": [
            Exercise("Race rhythm simulation", "Tactical", "2 rounds x 6 minutes", "Pacing.", ["Boat", "Erg"], ["Moderate", "High"], ["Match Rhythm"], ["Sweep Rower", "Sculler", "Indoor Rower"], ["Intermediate", "Advanced", "Elite"], ["Competition Block"], 1.0),
        ],
        "Recovery": [
            Exercise("Easy paddle or walk", "Recovery", "8 minutes", "Recovery.", ["Boat", "Bodyweight"], ["Low"], ["Movement Quality"], ["All"], ["All"], ["All"], 0.8),
        ],
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
        "Balanced Session": {"Warm-Up": 2, "Technical": 2, "Physical": 2, "Tactical": 1, "Recovery": 1},
        "Technical Priority": {"Warm-Up": 2, "Technical": 3, "Physical": 1, "Tactical": 1, "Recovery": 1},
        "Physical Priority": {"Warm-Up": 2, "Technical": 1, "Physical": 3, "Tactical": 0, "Recovery": 1},
        "Competition Week": {"Warm-Up": 2, "Technical": 2, "Physical": 1, "Tactical": 1, "Recovery": 1},
    },
    "Running": {
        "Balanced Session": {"Warm-Up": 1, "Technical": 1, "Physical": 2, "Tactical": 1, "Recovery": 1},
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

READINESS_MULTIPLIERS = {
    "Low": 0.88,
    "Moderate": 1.0,
    "High": 1.08,
}

INTENSITY_NOTES = {
    "Controlled": "Keep quality-first pacing. Leave reserve in the tank and avoid chasing fatigue.",
    "Standard": "Normal productive training intensity. Strong quality, but not an all-out day.",
    "High": "High-output day. Prioritize sharp execution, full recoveries on speed work, and stop if mechanics fade.",
    "Peak": "Very high intent. Use only when readiness is truly high and the athlete is not carrying pain or excessive fatigue.",
}

GOAL_PRIORITIES = {
    "Improve performance": ["Technical", "Physical", "Tactical"],
    "Build fitness": ["Physical", "Technical", "Recovery"],
    "Return after a break": ["Warm-Up", "Technical", "Recovery"],
    "Learn how to play": ["Warm-Up", "Technical", "Recovery"],
    "Injury prevention": ["Warm-Up", "Physical", "Recovery"],
    "Competition preparation": ["Technical", "Tactical", "Physical"],
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


def category_share_map(session_type: str, goal: str) -> Dict[str, float]:
    shares = dict(CATEGORY_BASE_SHARES)
    adjustments = SESSION_TYPE_CATEGORY_ADJUSTMENTS.get(session_type, {})
    for key, mult in adjustments.items():
        shares[key] = shares.get(key, 0.0) * mult

    priorities = GOAL_PRIORITIES.get(goal, [])
    for cat in priorities:
        shares[cat] = shares.get(cat, 0.0) * 1.08

    total = sum(shares.values())
    return {k: v / total for k, v in shares.items()}


def position_matches(ex: Exercise, position: str) -> bool:
    if not ex.position_tags or "All" in ex.position_tags:
        return True
    return position in ex.position_tags


def level_matches(ex: Exercise, level: str) -> bool:
    if not ex.level_tags:
        return True
    return level in ex.level_tags or "All" in ex.level_tags


def phase_matches(ex: Exercise, season_phase: str) -> bool:
    if not ex.phase_tags:
        return True
    return season_phase in ex.phase_tags or "All" in ex.phase_tags


def focus_matches(ex: Exercise, primary_focus: str) -> bool:
    if not ex.focus_tags:
        return False
    return primary_focus in ex.focus_tags


def choose_exercises_for_category(
    library_items: List[Exercise],
    requested_count: int,
    position: str,
    level: str,
    season_phase: str,
    primary_focus: str,
) -> List[Exercise]:
    if not library_items or requested_count <= 0:
        return []

    scored: List[Tuple[float, Exercise]] = []
    for ex in library_items:
        score = 1.0
        if position_matches(ex, position):
            score += 1.2
        if level_matches(ex, level):
            score += 0.6
        if phase_matches(ex, season_phase):
            score += 0.6
        if focus_matches(ex, primary_focus):
            score += 0.8
        score += random.uniform(0.0, 0.25)
        scored.append((score, ex))

    scored.sort(key=lambda x: x[0], reverse=True)
    pool = [ex for _, ex in scored]

    selected = []
    seen_names = set()
    for ex in pool:
        if ex.name not in seen_names:
            selected.append(ex)
            seen_names.add(ex.name)
        if len(selected) >= requested_count:
            break

    if len(selected) < requested_count:
        leftovers = [ex for ex in library_items if ex.name not in seen_names]
        random.shuffle(leftovers)
        selected.extend(leftovers[: max(0, requested_count - len(selected))])

    return selected[:requested_count]


def adapt_session_for_equipment(session: List[Exercise], equipment_level: str, sport: str) -> List[Exercise]:
    normalized = normalize_equipment_level(equipment_level)

    if normalized in ["Competitive", "Elite"]:
        return session

    adjusted: List[Exercise] = []
    for ex in session:
        heavy_tags = {"Barbell", "Machine", "Medicine ball", "Rowing erg", "Pool", "Boat", "Trap bar"}
        if normalized == "Minimal":
            if any(tag in heavy_tags for tag in ex.equipment_tags):
                adjusted.append(
                    Exercise(
                        name=f"Adapted version of {ex.name}",
                        category=ex.category,
                        prescription=ex.prescription,
                        purpose=f"Low-equipment adaptation: {ex.purpose}",
                        equipment_tags=["Bodyweight", "Open space"],
                        intensity_tags=ex.intensity_tags,
                        focus_tags=ex.focus_tags,
                        position_tags=ex.position_tags,
                        level_tags=ex.level_tags,
                        phase_tags=ex.phase_tags,
                        time_weight=ex.time_weight,
                        coaching_points=ex.coaching_points,
                        progressions=ex.progressions,
                        regressions=ex.regressions,
                        risk_notes=ex.risk_notes,
                    )
                )
            else:
                adjusted.append(ex)
        elif normalized == "Basic":
            if any(tag in {"Barbell", "Machine", "Boat", "Trap bar"} for tag in ex.equipment_tags):
                adjusted.append(
                    Exercise(
                        name=f"Basic setup adaptation - {ex.name}",
                        category=ex.category,
                        prescription=ex.prescription,
                        purpose=f"Adapted for a simpler training environment. {ex.purpose}",
                        equipment_tags=["Bodyweight", "Cones", "Bands", "Balls"],
                        intensity_tags=ex.intensity_tags,
                        focus_tags=ex.focus_tags,
                        position_tags=ex.position_tags,
                        level_tags=ex.level_tags,
                        phase_tags=ex.phase_tags,
                        time_weight=ex.time_weight,
                        coaching_points=ex.coaching_points,
                        progressions=ex.progressions,
                        regressions=ex.regressions,
                        risk_notes=ex.risk_notes,
                    )
                )
            else:
                adjusted.append(ex)
        else:
            adjusted.append(ex)

    return adjusted


def adjust_duration_for_readiness(duration: int, readiness: str, goal: str, session_type: str) -> int:
    multiplier = READINESS_MULTIPLIERS.get(readiness, 1.0)
    adjusted = round(duration * multiplier)

    if goal in ["Return after a break", "Injury prevention"]:
        adjusted = min(adjusted, duration)

    if session_type == "Competition Week":
        adjusted = min(adjusted, duration)

    return max(30, adjusted)


def allocate_block_minutes(
    session: List[Exercise],
    duration: int,
    session_type: str,
    goal: str,
) -> List[int]:
    explicit_minutes: List[Optional[int]] = [parse_prescription_minutes(ex.prescription) for ex in session]
    fixed_total = sum(m for m in explicit_minutes if m is not None)
    remaining = max(0, duration - fixed_total)

    shares = category_share_map(session_type, goal)
    unresolved_indices = [idx for idx, value in enumerate(explicit_minutes) if value is None]

    if unresolved_indices:
        category_weights: Dict[int, float] = {}
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


def build_session(
    sport: str,
    position: str,
    level: str,
    session_type: str,
    equipment_level: str,
    duration: int,
    season_phase: str,
    primary_focus: str,
) -> List[Exercise]:
    lib = SPORT_LIBRARY[sport]
    blueprint = get_blueprint(sport, session_type)
    blueprint = trim_blueprint_to_target(blueprint, target_exercise_count(sport, duration))

    session: List[Exercise] = []
    for category, requested_count in blueprint.items():
        library_items = lib.get(category, [])
        chosen = choose_exercises_for_category(
            library_items=library_items,
            requested_count=requested_count,
            position=position,
            level=level,
            season_phase=season_phase,
            primary_focus=primary_focus,
        )
        session.extend(chosen)

    return adapt_session_for_equipment(session, equipment_level, sport)


def weekly_focus(days: int, goal: str, season_phase: str) -> List[str]:
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
    if season_phase == "Competition Block":
        base[1] = "Day 2: Sharp but lower-volume technical session"
        base[5] = "Day 6: Recovery emphasis or light activation"
    return base[:max(1, min(days, 7))]


def generate_session_objectives(goal: str, session_type: str, primary_focus: str, readiness: str) -> List[str]:
    objectives = [
        f"Primary aim: {goal.lower()}.",
        f"Session emphasis: {session_type.lower()}.",
        f"Performance focus today: {primary_focus.lower()}.",
    ]
    if readiness == "Low":
        objectives.append("Manage load intelligently and protect technical quality.")
    elif readiness == "High":
        objectives.append("Use high readiness to push quality and intent where appropriate.")
    return objectives


def build_profile_summary(
    role: str,
    sport: str,
    position: str,
    goal: str,
    level: str,
    weekly_frequency: int,
    duration: int,
    adjusted_duration: int,
    session_type: str,
    equipment_level: str,
    readiness: str,
    intensity_mode: str,
    season_phase: str,
    primary_focus: str,
) -> Dict[str, object]:
    return {
        "role": role,
        "sport": sport,
        "position": position,
        "goal": goal,
        "level": level,
        "weekly_frequency": weekly_frequency,
        "duration_minutes_requested": duration,
        "duration_minutes_adjusted": adjusted_duration,
        "session_type": session_type,
        "equipment_level": equipment_level,
        "readiness": readiness,
        "intensity_mode": intensity_mode,
        "season_phase": season_phase,
        "primary_focus": primary_focus,
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


def estimate_session_load(level: str, readiness: str, intensity_mode: str, duration: int) -> str:
    score = 0
    score += {"Beginner": 1, "Intermediate": 2, "Advanced": 3, "Elite": 4}[level]
    score += {"Low": 0, "Moderate": 1, "High": 2}[readiness]
    score += {"Controlled": 0, "Standard": 1, "High": 2, "Peak": 3}[intensity_mode]
    score += 1 if duration >= 75 else 0
    score += 1 if duration >= 105 else 0

    if score <= 3:
        return "Low to Moderate"
    if score <= 6:
        return "Moderate"
    if score <= 8:
        return "Moderate to High"
    return "High"


def extract_progression_tip(ex: Exercise, level: str, readiness: str) -> str:
    if readiness == "Low" and ex.regressions:
        return ex.regressions[0]
    if level in ["Advanced", "Elite"] and ex.progressions:
        return ex.progressions[0]
    if ex.progressions:
        return ex.progressions[0]
    if ex.regressions:
        return ex.regressions[0]
    return "Keep execution quality high before adding complexity."


def build_coach_summary(
    sport: str,
    position: str,
    goal: str,
    session_type: str,
    primary_focus: str,
    readiness: str,
    intensity_mode: str,
    season_phase: str,
) -> List[str]:
    return [
        f"{sport} profile selected with position emphasis on {position}.",
        f"The plan is designed around {goal.lower()} with a {session_type.lower()} structure.",
        f"The generator prioritized {primary_focus.lower()} and adjusted for {readiness.lower()} readiness.",
        f"Season context considered: {season_phase.lower()}.",
        INTENSITY_NOTES[intensity_mode],
    ]


def build_microcycle_example(
    weekly_frequency: int,
    session_type: str,
    goal: str,
    season_phase: str,
    primary_focus: str,
) -> List[str]:
    base = weekly_focus(weekly_frequency, goal, season_phase)
    detailed = []
    for i, item in enumerate(base, start=1):
        if i == 1:
            detailed.append(f"{item} | Main emphasis: {session_type} | Priority: {primary_focus}")
        elif i == 2:
            detailed.append(f"{item} | Lower stress than Day 1, quality technical execution")
        elif i == 3:
            detailed.append(f"{item} | High neural output if athlete is fresh")
        elif i == 4:
            detailed.append(f"{item} | Restore freshness and sharpen movement quality")
        elif i == 5:
            detailed.append(f"{item} | Competitive rhythm and decision quality")
        elif i == 6:
            detailed.append(f"{item} | Supportive physical work without unnecessary fatigue")
        else:
            detailed.append(f"{item} | Full recovery, mobility, sleep and hydration focus")
    return detailed


def render_metric_cards(adjusted_duration: int, estimated_load: str, intensity_mode: str, readiness: str) -> None:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Planned minutes", adjusted_duration)
    c2.metric("Estimated load", estimated_load)
    c3.metric("Intensity mode", intensity_mode)
    c4.metric("Readiness", readiness)


# -----------------------------------------------------------------------------
# STREAMLIT SECTION
# -----------------------------------------------------------------------------
def render_training_generator_section() -> None:
    st.header("Training Generator Pro")
    st.write(
        "Generate elite-level sessions with exact reps, sets, and time prescriptions, plus readiness adjustment, "
        "season context, position-specific emphasis, coaching points, progressions, and a more professional planning layer."
    )

    role = st.radio("Are you a player or coach?", ["Player", "Coach"], horizontal=True)

    c1, c2 = st.columns(2)
    with c1:
        sport = st.selectbox("Choose the sport", list(SPORT_POSITIONS.keys()))
        position = st.selectbox("Choose the position / profile", SPORT_POSITIONS[sport])
        goal = st.selectbox("Main goal", GOALS)
        level = st.selectbox("Current level", LEVELS)
        primary_focus = st.selectbox("Primary focus today", PRIMARY_FOCUS_OPTIONS)
    with c2:
        weekly_frequency = st.slider(get_frequency_prompt(goal, level), 1, 7, 4)
        session_type = st.selectbox("Session type", SESSION_TYPES)
        duration = st.slider("Requested session duration (minutes)", 30, 180, 75, step=5)
        equipment_level = st.selectbox(
            "Level of equipment available",
            EQUIPMENT_LEVELS,
            index=2,
            help="Choose the overall quality of the equipment and training environment available.",
        )
        season_phase = st.selectbox("Season phase", SEASON_PHASES)

    c3, c4 = st.columns(2)
    with c3:
        readiness = st.select_slider("Current readiness", options=READINESS_OPTIONS, value="Moderate")
        intensity_mode = st.select_slider("Desired intensity mode", options=INTENSITY_MODES, value="Standard")
    with c4:
        pain_flag = st.checkbox("There is some pain / discomfort today")
        competition_soon = st.checkbox("Competition or match in the next 3 days")
        needs_low_impact = st.checkbox("Prefer lower-impact loading today")

    render_equipment_level_box(equipment_level)

    notes = st.text_area(
        "Extra notes",
        placeholder="Examples: match in 3 days, shoulder fatigue, focus on speed, beginner team, small training space, heavy legs, needs serve emphasis...",
        height=110,
    )

    st.caption(
        "Pro architecture included: structured athlete profile, future payload builder, dynamic session blueprint logic, "
        "position-aware exercise selection, readiness/load adjustment, and modular timing functions. No API has been connected yet."
    )

    if st.button("Generate Pro Training Session", type="primary", use_container_width=True):
        adjusted_duration = adjust_duration_for_readiness(duration, readiness, goal, session_type)

        if competition_soon:
            adjusted_duration = min(adjusted_duration, duration)
            if session_type == "Physical Priority":
                session_type = "Competition Week"

        if pain_flag or needs_low_impact:
            adjusted_duration = max(30, adjusted_duration - 5)

        session = build_session(
            sport=sport,
            position=position,
            level=level,
            session_type=session_type,
            equipment_level=equipment_level,
            duration=adjusted_duration,
            season_phase=season_phase,
            primary_focus=primary_focus,
        )
        block_minutes = allocate_block_minutes(session, adjusted_duration, session_type, goal)

        profile_summary = build_profile_summary(
            role=role,
            sport=sport,
            position=position,
            goal=goal,
            level=level,
            weekly_frequency=weekly_frequency,
            duration=duration,
            adjusted_duration=adjusted_duration,
            session_type=session_type,
            equipment_level=equipment_level,
            readiness=readiness,
            intensity_mode=intensity_mode,
            season_phase=season_phase,
            primary_focus=primary_focus,
        )
        future_payload = build_future_api_payload(profile_summary)
        estimated_load = estimate_session_load(level, readiness, intensity_mode, adjusted_duration)

        st.subheader(f"{sport} Pro Session Plan")
        st.write(
            f"**Profile:** {role} | **Position:** {position} | **Goal:** {goal} | **Level:** {level} | "
            f"**Weekly frequency:** {weekly_frequency} | **Requested duration:** {duration} min | **Planned duration:** {adjusted_duration} min"
        )
        st.caption(f"Equipment level selected: {equipment_level} | Season phase: {season_phase} | Primary focus: {primary_focus}")
        st.caption(build_session_summary_line(session, block_minutes, adjusted_duration))

        render_metric_cards(adjusted_duration, estimated_load, intensity_mode, readiness)

        if notes.strip():
            st.info(f"Context notes considered: {notes}")

        if pain_flag:
            st.warning("Pain/discomfort flagged: keep technical quality high, reduce aggressive loading if symptoms change mechanics, and escalate to the Physio section if needed.")
        if competition_soon:
            st.warning("Competition proximity flagged: session logic shifted toward freshness and sharpness rather than accumulating fatigue.")

        st.subheader("Session objectives")
        for item in generate_session_objectives(goal, session_type, primary_focus, readiness):
            st.write(f"- {item}")

        st.subheader("Coach overview")
        for item in build_coach_summary(sport, position, goal, session_type, primary_focus, readiness, intensity_mode, season_phase):
            st.write(f"- {item}")

        st.subheader("Training blocks")
        for idx, (ex, planned_minutes) in enumerate(zip(session, block_minutes), start=1):
            with st.expander(f"{idx}. {ex.name}", expanded=True if idx <= 3 else False):
                st.markdown(f"**Category:** {ex.category}")
                st.markdown(f"**Prescription:** {ex.prescription}")
                st.markdown(f"**Purpose:** {ex.purpose}")
                st.markdown(f"**Planned block duration in this session:** ~{planned_minutes} minutes")
                if ex.equipment_tags:
                    st.markdown(f"**Typical equipment for this drill:** {', '.join(ex.equipment_tags)}")
                if ex.focus_tags:
                    st.markdown(f"**Key training qualities:** {', '.join(ex.focus_tags)}")
                if ex.coaching_points:
                    st.markdown("**Elite coaching points:**")
                    for point in ex.coaching_points:
                        st.write(f"- {point}")
                st.markdown(f"**Progression / regression tip:** {extract_progression_tip(ex, level, readiness)}")
                if ex.risk_notes:
                    st.markdown("**Risk note:**")
                    for note in ex.risk_notes:
                        st.write(f"- {note}")

        st.subheader("Weekly structure suggestion")
        for item in build_microcycle_example(weekly_frequency, session_type, goal, season_phase, primary_focus):
            st.write(f"- {item}")

        st.subheader("Professional coaching reminders")
        reminders = [
            "Different drills should not always carry the same time load. Longer pattern work or main-set work should naturally take more room than short primers.",
            "Use the planned block durations as the session architecture, while the prescription remains the coaching instruction.",
            "Stop or modify a drill when execution clearly drops or movement quality breaks down.",
            "Record key outputs such as sprint quality, serve percentage, shot quality, jump height feel, split times, stroke rate, bar speed, or session RPE.",
            "On low-readiness days, protect quality first. On high-readiness days, push only the right parts of the session.",
            "A professional session is not only hard — it is precise, realistic, and appropriate for the athlete’s environment and current condition.",
        ]
        if role == "Coach":
            reminders.append("For teams, use the generated plan as a core structure, then split work:rest or constraints depending on starters, reserves, and rehab profiles.")
        if pain_flag:
            reminders.append("Pain was flagged. Reduce intensity immediately if mechanics change, symptoms worsen, or compensations appear.")
        for item in reminders:
            st.write(f"- {item}")

        with st.expander("Future API integration preview", expanded=False):
            st.json(future_payload)
            st.caption("This is only a preview of the structure prepared for future reasoning/API implementation.")


if __name__ == "__main__":
    render_training_generator_section()
