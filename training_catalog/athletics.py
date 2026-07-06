"""Athletics training catalog for Sportze.AI.

This module stores athletics exercises in a structured format so the training
program can fetch exercises cleanly by event group/category.

Public helpers:
- get_categories()
- get_exercises(category)
- get_catalog()
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List

Exercise = Dict[str, Any]
Catalog = Dict[str, List[Exercise]]


def _exercise(
    name: str,
    instructions: List[str],
    volume: str,
    focus: List[str] | None = None,
    equipment: List[str] | None = None,
) -> Exercise:
    return {
        "name": name,
        "instructions": instructions,
        "volume": volume,
        "focus": focus or [],
        "equipment": equipment or [],
    }


ATHLETICS_CATALOG: Catalog = {
    "sprinting_100m_200m": [
        _exercise("30m Maximum Speed Sprint", ["Sprint 30 meters at maximum speed."], "8 reps", ["speed", "acceleration"]),
        _exercise("60m Sprint at 95%", ["Sprint 60 meters at 95% effort."], "6 reps", ["speed", "sprint endurance"]),
        _exercise("20m Acceleration + 20m Sprint", ["Accelerate for 20 meters.", "Then sprint 20 meters at full speed."], "8 reps", ["acceleration", "top speed"]),
        _exercise("120m Speed Endurance Run", ["Run 120 meters at 90% effort."], "5 reps", ["speed endurance"]),
        _exercise("Standing Broad Jumps", ["Perform standing broad jumps with a controlled landing."], "4 sets of 10 jumps", ["power", "horizontal jump"]),
        _exercise("40m Uphill Sprint", ["Sprint uphill for 40 meters."], "6 reps", ["power", "acceleration"]),
        _exercise("5-10-5 Shuttle Run", ["Complete a 5-10-5 shuttle run with sharp changes of direction."], "8 reps", ["agility", "acceleration"]),
        _exercise("80m Block Start Sprint", ["Sprint 80 meters from starting blocks."], "6 reps", ["block start", "speed"], ["starting blocks"]),
    ],
    "long_sprint_400m": [
        _exercise("300m Race-Pace Run", ["Run 300 meters at race pace."], "4 reps", ["400m pace", "speed endurance"]),
        _exercise("200m Run at 90%", ["Run 200 meters at 90% effort."], "6 reps", ["speed endurance"]),
        _exercise("500m Controlled Run", ["Run 500 meters at a controlled pace."], "3 reps", ["lactate tolerance", "endurance"]),
        _exercise("150m Maximum Sprint", ["Sprint 150 meters at maximum effort."], "6 reps", ["speed", "speed endurance"]),
        _exercise("4 x 100m Short-Rest Runs", ["Run 100 meters.", "Rest 30 seconds between reps."], "4 reps", ["repeat sprint ability"]),
        _exercise("350m Race-Pace Run", ["Run 350 meters at race pace."], "3 reps", ["400m pace", "lactate tolerance"]),
        _exercise("60m Uphill Sprint", ["Sprint uphill for 60 meters."], "6 reps", ["power", "drive phase"]),
        _exercise("600m Steady Run", ["Run 600 meters at a steady pace."], "2 reps", ["endurance", "400m conditioning"]),
    ],
    "hurdles": [
        _exercise("5-Hurdle Race-Spacing Sprint", ["Sprint over 5 hurdles at race spacing."], "8 reps", ["hurdle rhythm", "speed"], ["hurdles"]),
        _exercise("Lead-Leg Hurdle Drill", ["Perform lead-leg drills over 10 low hurdles."], "4 sets", ["lead leg", "technique"], ["low hurdles"]),
        _exercise("Trail-Leg Hurdle Drill", ["Perform trail-leg drills over 10 low hurdles."], "4 sets", ["trail leg", "technique"], ["low hurdles"]),
        _exercise("30m Sprint + 3 Hurdles", ["Sprint 30 meters.", "Clear 3 hurdles after the sprint."], "8 reps", ["approach", "hurdle rhythm"], ["hurdles"]),
        _exercise("Quick-Step Hurdle Runs", ["Perform quick-step runs between 5 hurdles."], "8 reps", ["cadence", "rhythm"], ["hurdles"]),
        _exercise("150m Hurdle Rhythm Sprint", ["Sprint 150 meters with hurdles at race rhythm."], "4 reps", ["race rhythm", "speed endurance"], ["hurdles"]),
        _exercise("8-Hurdle Run at 85%", ["Run over 8 hurdles at 85% speed."], "5 reps", ["controlled rhythm", "technique"], ["hurdles"]),
        _exercise("Full Hurdles Race Simulation", ["Complete a full race simulation over hurdles."], "3 reps", ["race simulation"], ["hurdles"]),
    ],
    "middle_distance_800m_1500m": [
        _exercise("400m Race-Pace Repeats", ["Run 400 meters at race pace."], "6 reps", ["race pace", "middle distance"]),
        _exercise("800m Controlled Repeats", ["Run 800 meters at a controlled pace."], "4 reps", ["endurance", "pace control"]),
        _exercise("200m Fast Repeats", ["Run 200 meters fast."], "10 reps", ["speed", "finishing kick"]),
        _exercise("1200m Tempo Repeats", ["Run 1200 meters at tempo pace."], "3 reps", ["tempo", "aerobic endurance"]),
        _exercise("6 x 300m Race-Pace Runs", ["Run 300 meters at race pace."], "6 reps", ["race pace", "speed endurance"]),
        _exercise("5km Easy Run", ["Run 5 kilometers at an easy pace."], "1 run", ["aerobic base"]),
        _exercise("Lap Sprint Finish Drill", ["Run 400-meter laps.", "Sprint 100 meters after every 400-meter lap."], "6 laps", ["finishing kick", "pace change"]),
        _exercise("1500m Race Simulation", ["Run a full 1500-meter race simulation."], "1 simulation", ["race simulation"]),
    ],
    "long_distance_5000m_10000m": [
        _exercise("5km Race-Pace Run", ["Run 5 kilometers at race pace."], "1 run", ["race pace", "5k"]),
        _exercise("8 x 800m Race-Pace Repeats", ["Run 800 meters at race pace."], "8 reps", ["race pace", "endurance"]),
        _exercise("10km Steady Run", ["Run 10 kilometers at a steady pace."], "1 run", ["aerobic endurance"]),
        _exercise("12 x 400m Fast Repeats", ["Run 400 meters fast."], "12 reps", ["speed endurance"]),
        _exercise("15km Easy Run", ["Run 15 kilometers at an easy pace."], "1 run", ["aerobic base"]),
        _exercise("3km Tempo Repeats", ["Run 3 kilometers at tempo pace."], "3 reps", ["tempo", "threshold"]),
        _exercise("6 x 1km Race-Pace Repeats", ["Run 1 kilometer at race pace."], "6 reps", ["race pace", "threshold"]),
        _exercise("10km Race Simulation", ["Complete a 10-kilometer race simulation."], "1 simulation", ["race simulation"]),
    ],
    "marathon": [
        _exercise("25km Easy Run", ["Run 25 kilometers at an easy pace."], "1 run", ["aerobic endurance"]),
        _exercise("15km Marathon-Pace Run", ["Run 15 kilometers at marathon pace."], "1 run", ["marathon pace"]),
        _exercise("35km Long Run", ["Run 35 kilometers at long-run pace."], "1 run", ["long run", "endurance"]),
        _exercise("10 x 1km Marathon-Pace Repeats", ["Run 1 kilometer at marathon pace."], "10 reps", ["marathon pace", "pace control"]),
        _exercise("20km Progression Run", ["Run 20 kilometers, gradually increasing pace throughout the run."], "1 run", ["progression", "endurance"]),
        _exercise("8km Recovery Run", ["Run 8 kilometers at recovery pace."], "1 run", ["recovery"]),
        _exercise("5km Tempo Repeats", ["Run 5 kilometers at tempo pace."], "3 reps", ["tempo", "threshold"]),
        _exercise("30km Race Simulation", ["Complete a 30-kilometer race simulation."], "1 simulation", ["race simulation", "marathon preparation"]),
    ],
    "steeplechase": [
        _exercise("400m Barrier Lap Repeats", ["Run 400 meters while clearing barriers each lap."], "6 reps", ["barriers", "race rhythm"], ["steeplechase barriers"]),
        _exercise("100m + 3 Barriers", ["Run 100 meters.", "Clear 3 barriers."], "10 reps", ["barrier technique"], ["steeplechase barriers"]),
        _exercise("Water Jump Practice", ["Practice water jumps with safe landings."], "20 jumps", ["water jump"], ["water jump pit"]),
        _exercise("2000m With Barriers", ["Run 2000 meters including barriers."], "1 run", ["race endurance", "barriers"], ["steeplechase barriers"]),
        _exercise("Hurdle + Water Jump Combination", ["Complete hurdle-and-water-jump combinations."], "8 combinations", ["barrier transition", "water jump"], ["steeplechase barriers", "water jump pit"]),
        _exercise("5 x 600m Steeplechase Pace", ["Run 600 meters at steeplechase pace."], "5 reps", ["race pace"]),
        _exercise("3000m Steady With Barriers", ["Run 3000 meters at a steady pace with barriers."], "1 run", ["endurance", "barrier rhythm"], ["steeplechase barriers"]),
        _exercise("Full Steeplechase Race Simulation", ["Complete a full steeplechase race simulation."], "1 simulation", ["race simulation"], ["steeplechase barriers", "water jump pit"]),
    ],
    "race_walking": [
        _exercise("5km Legal Technique Walk", ["Walk 5 kilometers while maintaining legal race-walking technique."], "1 walk", ["technique", "endurance"]),
        _exercise("10 x 400m Race-Pace Walks", ["Walk 400 meters at race pace."], "10 reps", ["race pace"]),
        _exercise("10km Steady Walk", ["Walk 10 kilometers at a steady pace."], "1 walk", ["endurance"]),
        _exercise("2km Fast Walk Repeats", ["Walk 2 kilometers fast."], "4 reps", ["speed endurance"]),
        _exercise("15km Endurance Walk", ["Walk 15 kilometers at endurance pace."], "1 walk", ["endurance"]),
        _exercise("1km Uphill Walk Repeats", ["Walk uphill for 1 kilometer."], "5 reps", ["strength endurance"]),
        _exercise("20 x 200m Race-Pace Walks", ["Walk 200 meters at race pace."], "20 reps", ["race pace", "cadence"]),
        _exercise("20km Race Walk Simulation", ["Complete a 20-kilometer race simulation."], "1 simulation", ["race simulation"]),
    ],
    "high_jump": [
        _exercise("Approach Runs Without Jump", ["Perform approach runs without jumping."], "20 reps", ["approach rhythm"]),
        _exercise("Low-Bar Fosbury Jumps", ["Jump over a low bar using Fosbury technique."], "15 reps", ["technique"], ["high jump bar"]),
        _exercise("Single-Leg Takeoff Jumps", ["Perform single-leg takeoff jumps."], "15 reps", ["takeoff", "power"]),
        _exercise("Box Jumps", ["Complete box jumps with controlled landings."], "20 reps", ["power"], ["box"]),
        _exercise("Full-Height Jump Attempts", ["Perform full-height high jump attempts."], "10 reps", ["competition technique"], ["high jump bar"]),
        _exercise("Curved Approach + Jump", ["Run a curved approach.", "Then complete the jump."], "8 reps", ["approach", "takeoff"], ["high jump bar"]),
        _exercise("Depth Jumps", ["Perform depth jumps with quick ground contact."], "15 reps", ["reactive power"], ["box"]),
        _exercise("High Jump Competition Simulation", ["Complete a competition simulation."], "10 attempts", ["race simulation", "competition practice"], ["high jump bar"]),
    ],
    "long_jump_triple_jump": [
        _exercise("Full Approach Runs", ["Perform full approach runs without jumping."], "20 reps", ["approach rhythm"]),
        _exercise("Long Jump Takeoffs", ["Complete long jump takeoffs from the board area."], "15 reps", ["takeoff"]),
        _exercise("Hop-Step-Jump Sequences", ["Perform triple-jump hop-step-jump sequences."], "15 reps", ["triple jump technique"]),
        _exercise("30m Bounding Runs", ["Execute bounding runs over 30 meters."], "20 reps", ["power", "rhythm"]),
        _exercise("Standing Long Jumps", ["Perform standing long jumps with stable landings."], "15 reps", ["horizontal power"]),
        _exercise("40m Sprint + Jump", ["Sprint 40 meters.", "Then perform a jump."], "12 reps", ["speed into takeoff"]),
        _exercise("Single-Leg Hops", ["Complete single-leg hops with controlled landings."], "20 reps", ["single-leg power"]),
        _exercise("Full Competition Jumps", ["Perform full competition jumps."], "10 jumps", ["competition practice"]),
    ],
    "pole_vault": [
        _exercise("Pole Carry Runs", ["Complete pole carry runs with controlled posture."], "20 reps", ["approach", "pole control"], ["vaulting pole"]),
        _exercise("Plant Drills", ["Perform plant drills without jumping."], "15 reps", ["plant technique"], ["vaulting pole"]),
        _exercise("Swing-Up Drills", ["Execute swing-up drills."], "10 reps", ["swing mechanics"], ["vaulting pole"]),
        _exercise("Short-Run Vaults", ["Perform short-run vaults."], "15 reps", ["vault technique"], ["vaulting pole"]),
        _exercise("Takeoff Jumps", ["Complete pole vault takeoff jumps."], "20 reps", ["takeoff"], ["vaulting pole"]),
        _exercise("Full Vault Attempts", ["Execute full vault attempts."], "10 reps", ["competition technique"], ["vaulting pole"]),
        _exercise("High-Bar Swing Drills", ["Perform high-bar swing drills."], "15 reps", ["swing strength"], ["high bar"]),
        _exercise("Pole Vault Competition Simulation", ["Complete a competition simulation."], "10 vaults", ["competition practice"], ["vaulting pole"]),
    ],
    "shot_put": [
        _exercise("Standing Shot Put Throws", ["Throw the shot put from a standing position."], "20 throws", ["throwing technique"], ["shot put"]),
        _exercise("Glide Throws", ["Perform glide throws."], "15 throws", ["glide technique"], ["shot put"]),
        _exercise("Rotational Throws", ["Complete rotational throws."], "15 throws", ["rotational technique"], ["shot put"]),
        _exercise("Maximum-Distance Shot Throws", ["Throw for maximum distance."], "10 reps", ["power"], ["shot put"]),
        _exercise("Medicine-Ball Chest Throws", ["Perform medicine-ball chest throws."], "20 throws", ["upper-body power"], ["medicine ball"]),
        _exercise("Explosive Squat Jumps", ["Complete explosive squat jumps."], "15 reps", ["lower-body power"]),
        _exercise("Power-Position Throws", ["Throw from power position."], "20 reps", ["power position"], ["shot put"]),
        _exercise("Shot Put Competition Throws", ["Perform competition-style shot put throws."], "10 throws", ["competition practice"], ["shot put"]),
    ],
    "discus_throw": [
        _exercise("Standing Discus Throws", ["Throw discus from a standing position."], "20 reps", ["release", "standing throw"], ["discus"]),
        _exercise("Half-Turn Throws", ["Perform half-turn throws."], "15 throws", ["rotation technique"], ["discus"]),
        _exercise("Full Rotational Throws", ["Complete full rotational throws."], "15 throws", ["full throw technique"], ["discus"]),
        _exercise("Maximum-Distance Discus Throws", ["Throw for maximum distance."], "10 reps", ["power"], ["discus"]),
        _exercise("Medicine-Ball Rotational Throws", ["Perform medicine-ball rotational throws."], "20 throws", ["rotational power"], ["medicine ball"]),
        _exercise("Balance Turns", ["Complete balance turns with controlled footwork."], "20 reps", ["balance", "rotation"]),
        _exercise("Release-Angle Drills", ["Perform release-angle drills."], "15 reps", ["release angle"], ["discus"]),
        _exercise("Discus Competition Throws", ["Complete competition-style discus throws."], "10 throws", ["competition practice"], ["discus"]),
    ],
    "hammer_throw": [
        _exercise("Hammer Winds", ["Perform hammer winds."], "20 reps", ["rhythm", "hammer control"], ["hammer"]),
        _exercise("One-Turn Throws", ["Complete one-turn throws."], "15 throws", ["rotation technique"], ["hammer"]),
        _exercise("Two-Turn Throws", ["Perform two-turn throws."], "15 throws", ["rotation technique"], ["hammer"]),
        _exercise("Full Hammer Throws", ["Complete full throws."], "15 throws", ["full throw technique"], ["hammer"]),
        _exercise("Rotational Medicine-Ball Throws", ["Perform rotational medicine-ball throws."], "20 throws", ["rotational power"], ["medicine ball"]),
        _exercise("Balance-Turn Drills", ["Complete balance-turn drills."], "20 reps", ["balance", "turning rhythm"]),
        _exercise("Maximum-Distance Hammer Throws", ["Throw for maximum distance."], "10 reps", ["power"], ["hammer"]),
        _exercise("Hammer Competition Throws", ["Complete competition-style hammer throws."], "10 throws", ["competition practice"], ["hammer"]),
    ],
    "javelin_throw": [
        _exercise("Standing Javelin Throws", ["Throw javelin from a standing position."], "20 reps", ["release", "throwing mechanics"], ["javelin"]),
        _exercise("Three-Step Throws", ["Perform three-step throws."], "15 throws", ["approach rhythm"], ["javelin"]),
        _exercise("Full Approach Throws", ["Complete full approach throws."], "15 throws", ["full throw technique"], ["javelin"]),
        _exercise("Crossover-Step Drills", ["Perform crossover-step drills."], "20 reps", ["approach mechanics"]),
        _exercise("Maximum-Distance Javelin Throws", ["Throw for maximum distance."], "10 reps", ["power"], ["javelin"]),
        _exercise("Medicine-Ball Overhead Throws", ["Complete medicine-ball overhead throws."], "20 throws", ["overhead power"], ["medicine ball"]),
        _exercise("Release-Angle Drills", ["Perform release-angle drills."], "15 reps", ["release angle"], ["javelin"]),
        _exercise("Javelin Competition Throws", ["Complete competition-style javelin throws."], "10 throws", ["competition practice"], ["javelin"]),
    ],
    "beginner_sprinting": [
        _exercise("30m Acceleration Run", ["Start standing still.", "Sprint 30 meters at 80% effort."], "8 reps", ["beginner", "acceleration"]),
        _exercise("High Knees Run", ["Run 20 meters while lifting knees to waist height."], "10 reps", ["running form"]),
        _exercise("Fast Feet Drill", ["Run in place as quickly as possible for 20 seconds."], "6 rounds", ["cadence"]),
        _exercise("60m Controlled Sprint", ["Sprint 60 meters at 75% effort."], "6 reps", ["controlled speed"]),
        _exercise("Shuttle Sprint", ["Sprint 10 meters forward and back."], "10 reps", ["agility", "acceleration"]),
        _exercise("Sprint Technique Run", ["Run 40 meters focusing on arm drive and posture."], "8 reps", ["technique"]),
    ],
    "beginner_jumping": [
        _exercise("Standing Long Jump", ["Jump forward from a standing position."], "15 jumps", ["beginner", "horizontal power"]),
        _exercise("Single-Leg Hops", ["Hop forward on one leg for 10 meters."], "5 reps per leg", ["single-leg power"]),
        _exercise("Box Step Jumps", ["Jump onto a low platform or step."], "20 reps", ["jump mechanics"], ["low platform"]),
        _exercise("Approach Run and Jump", ["Run 10 meters.", "Perform a long jump."], "15 reps", ["approach", "jumping"]),
        _exercise("Vertical Jump Reach", ["Jump straight up and touch the highest point possible."], "20 jumps", ["vertical power"]),
        _exercise("Bounding Drill", ["Take long running jumps for 30 meters."], "6 reps", ["bounding", "rhythm"]),
    ],
    "beginner_throwing": [
        _exercise("Medicine Ball Chest Throw", ["Throw a medicine ball forward from chest height."], "20 throws", ["throwing power"], ["medicine ball"]),
        _exercise("Overhead Throw", ["Throw a ball overhead for distance."], "20 throws", ["overhead throwing"]),
        _exercise("Standing Target Throw", ["Throw a ball at a target 10 meters away."], "30 throws", ["accuracy"]),
        _exercise("Rotational Throw", ["Rotate your hips and throw a ball sideways."], "15 throws per side", ["rotation"]),
        _exercise("Kneeling Throw", ["Kneel on one knee and throw a ball forward."], "20 throws", ["upper-body mechanics"]),
        _exercise("Distance Throw Challenge", ["Throw a ball as far as possible."], "15 throws", ["distance throwing"]),
    ],
    "beginner_middle_distance_800m_1500m": [
        _exercise("400m Easy Run", ["Run 400 meters at a comfortable pace."], "4 reps", ["beginner endurance"]),
        _exercise("200m Tempo Run", ["Run 200 meters at moderate effort."], "8 reps", ["tempo"]),
        _exercise("1km Continuous Run", ["Run 1 kilometer without stopping."], "1 rep", ["continuous running"]),
        _exercise("Run-Walk Intervals", ["Run 200 meters.", "Walk 100 meters."], "6 rounds", ["run-walk endurance"]),
        _exercise("600m Pace Run", ["Run 600 meters at a steady pace."], "3 reps", ["pace control"]),
        _exercise("Finishing Sprint Drill", ["Run 300 meters easy.", "Sprint the final 100 meters."], "5 reps", ["finishing kick"]),
    ],
    "beginner_long_distance_5000m_plus": [
        _exercise("2km Continuous Run", ["Run 2 kilometers at an easy pace."], "1 run", ["beginner endurance"]),
        _exercise("Run-Walk Endurance", ["Run 500 meters.", "Walk 100 meters."], "6 rounds", ["run-walk endurance"]),
        _exercise("3km Steady Run", ["Run 3 kilometers at a comfortable pace."], "1 run", ["steady endurance"]),
        _exercise("Long Easy Run", ["Run continuously for 20 minutes."], "1 run", ["aerobic base"]),
        _exercise("Hill Endurance Run", ["Run uphill for 100 meters.", "Walk back down."], "10 reps", ["hill endurance"]),
        _exercise("Negative Split Run", ["Run 2 kilometers.", "Complete the second kilometer faster than the first."], "1 run", ["pace control"]),
    ],
    "learn_how_to_play": [
        _exercise("Run 100 Meters", ["Run 100 meters at a comfortable pace."], "5 reps", ["first session", "running"]),
        _exercise("Standing Long Jump", ["Jump forward from a standing position."], "15 jumps", ["first session", "jumping"]),
        _exercise("Throw a Ball for Distance", ["Throw a ball as far as possible."], "20 throws", ["first session", "throwing"]),
        _exercise("Run Around a Track", ["Run continuously for 5 minutes."], "1 run", ["first session", "endurance"]),
        _exercise("Sprint and Stop", ["Sprint 20 meters.", "Stop under control."], "10 reps", ["first session", "control"]),
        _exercise("Athletics Circuit", ["Run 50 meters.", "Perform 1 standing long jump.", "Throw a ball 1 time.", "Repeat the sequence."], "10 rounds", ["first session", "general athletics"]),
    ],
}


CATEGORY_ALIASES: Dict[str, str] = {
    "100m": "sprinting_100m_200m",
    "200m": "sprinting_100m_200m",
    "sprint": "sprinting_100m_200m",
    "sprinting": "sprinting_100m_200m",
    "400m": "long_sprint_400m",
    "long sprint": "long_sprint_400m",
    "800m": "middle_distance_800m_1500m",
    "1500m": "middle_distance_800m_1500m",
    "middle distance": "middle_distance_800m_1500m",
    "5000m": "long_distance_5000m_10000m",
    "5k": "long_distance_5000m_10000m",
    "10000m": "long_distance_5000m_10000m",
    "10k": "long_distance_5000m_10000m",
    "long distance": "long_distance_5000m_10000m",
    "beginner sprint": "beginner_sprinting",
    "beginner jumping": "beginner_jumping",
    "beginner throwing": "beginner_throwing",
    "learn": "learn_how_to_play",
    "learn how to play": "learn_how_to_play",
}


def normalize_category(category: str) -> str:
    """Return the canonical category key for a category or alias."""
    key = category.strip().lower().replace("-", " ").replace("_", " ")
    if key in CATEGORY_ALIASES:
        return CATEGORY_ALIASES[key]

    canonical = key.replace(" ", "_")
    if canonical in ATHLETICS_CATALOG:
        return canonical

    raise KeyError(f"Unknown athletics category: {category}")


def get_categories() -> List[str]:
    """Return all canonical athletics category keys."""
    return list(ATHLETICS_CATALOG.keys())


def get_exercises(category: str) -> List[Exercise]:
    """Return a copy of all exercises for a category or alias."""
    canonical = normalize_category(category)
    return deepcopy(ATHLETICS_CATALOG[canonical])


def get_catalog() -> Catalog:
    """Return a copy of the full athletics catalog."""
    return deepcopy(ATHLETICS_CATALOG)


__all__ = [
    "ATHLETICS_CATALOG",
    "CATEGORY_ALIASES",
    "get_catalog",
    "get_categories",
    "get_exercises",
    "normalize_category",
]
