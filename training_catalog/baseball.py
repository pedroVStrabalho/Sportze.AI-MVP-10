"""Baseball training catalog for Sportze.AI.

This module stores baseball exercises in a structured format so the training
program can fetch exercises cleanly by training context and position/category.

Public helpers:
- get_training_contexts()
- get_categories(context=None)
- get_exercises(category, context=None)
- get_catalog()
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List

Exercise = Dict[str, Any]
PositionCatalog = Dict[str, List[Exercise]]
Catalog = Dict[str, PositionCatalog]


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


POSITION_EXERCISES: PositionCatalog = {
    "pitcher_p": [
        _exercise("Target Fastballs", ["Throw fastballs at a strike-zone target from regulation distance."], "40 fastballs", ["pitching", "fastball accuracy"], ["baseball", "strike-zone target"]),
        _exercise("Pitch Accuracy Ladder", ["Hit the top-left, top-right, bottom-left, and bottom-right corners of the strike zone."], "10 hits per corner", ["pitching accuracy", "command"], ["baseball", "strike-zone target"]),
        _exercise("Pitch Mix Drill", ["Throw fastballs, changeups, and breaking balls in a controlled pitch mix."], "15 fastballs, 15 changeups, 15 breaking balls", ["pitch mix", "pitch control"], ["baseball"]),
        _exercise("Balance Hold Delivery", ["Hold pitching balance position for 3 seconds.", "Complete the throw after the hold."], "30 reps", ["delivery balance", "pitch mechanics"], ["baseball"]),
        _exercise("Bullpen Simulation", ["Throw pitches as if pitching an inning."], "60 pitches", ["bullpen", "game simulation"], ["baseball", "mound or throwing area"]),
        _exercise("Pitcher's Fielding Practice", ["Roll a ball 5 meters away.", "Sprint to the ball.", "Field it cleanly and throw to a target."], "20 reps", ["fielding", "pitcher defense"], ["baseball", "target"]),
    ],
    "catcher_c": [
        _exercise("Wall Receiving Drill", ["Throw a ball against a wall.", "Receive the rebound in a catcher stance."], "50 catches", ["receiving", "catcher stance"], ["baseball", "wall"]),
        _exercise("Blocking Drill", ["Throw a ball into the ground so it bounces unpredictably.", "Block it with your body."], "30 reps", ["blocking", "reaction"], ["baseball"]),
        _exercise("Pop-Up Recovery", ["Start in catcher stance.", "Stand quickly and sprint 10 meters."], "20 reps", ["recovery", "explosiveness"], []),
        _exercise("Throw to Second Base Target", ["Simulate a stolen-base throw.", "Hit a target 35-40 meters away."], "30 throws", ["throwing accuracy", "catcher pop time"], ["baseball", "target"]),
        _exercise("Framing Practice", ["Catch balls near the edge of the strike zone.", "Present each catch cleanly."], "50 catches", ["framing", "receiving"], ["baseball"]),
        _exercise("Squat Endurance", ["Hold a catcher stance with stable posture."], "5 sets of 60 seconds", ["stance endurance", "lower-body endurance"], []),
    ],
    "first_baseman_1b": [
        _exercise("Ground Ball Fielding", ["Roll the ball forward.", "Charge it, field it, and throw to a target."], "30 reps", ["ground balls", "fielding"], ["baseball", "target"]),
        _exercise("Stretch Drill", ["Place one foot on a marker.", "Practice stretching to catch throws from a wall."], "50 catches", ["first-base stretch", "catching"], ["baseball", "wall", "marker"]),
        _exercise("Short Hop Drill", ["Throw the ball against a wall so it bounces just before reaching you.", "Field the short hop cleanly."], "40 reps", ["short hops", "glove work"], ["baseball", "wall"]),
        _exercise("Bag Touch Sprint", ["Sprint to a first-base marker.", "Touch it and return."], "20 reps", ["footwork", "base coverage"], ["marker"]),
        _exercise("Backhand Pick Drill", ["Field ground balls on your glove side using a backhand pick."], "25 reps", ["backhand pick", "fielding"], ["baseball"]),
        _exercise("Forehand Pick Drill", ["Field ground balls on your throwing-hand side using a forehand pick."], "25 reps", ["forehand pick", "fielding"], ["baseball"]),
    ],
    "second_baseman_2b": [
        _exercise("Ground Ball Shuffle", ["Field a ground ball.", "Shuffle and simulate a throw to first base."], "40 reps", ["ground balls", "infield footwork"], ["baseball"]),
        _exercise("Double Play Footwork", ["Move around a base marker.", "Complete double-play footwork."], "30 reps", ["double play", "footwork"], ["marker"]),
        _exercise("Quick Transfer Drill", ["Catch the ball.", "Move it from glove to throwing hand as fast as possible."], "50 reps", ["transfer speed", "infield hands"], ["baseball", "glove"]),
        _exercise("Side-to-Side Fielding", ["Shuffle 5 meters left or right.", "Field the ball and throw to a target."], "30 reps", ["lateral movement", "fielding"], ["baseball", "target"]),
        _exercise("Bare-Hand Pickup", ["Charge slow rollers.", "Pick up the ball bare-handed with control."], "25 reps", ["slow rollers", "bare-hand pickup"], ["baseball"]),
        _exercise("Reaction Grounders", ["Throw the ball against a wall.", "Field the rebound cleanly."], "40 reps", ["reaction", "ground balls"], ["baseball", "wall"]),
    ],
    "third_baseman_3b": [
        _exercise("Hot Corner Reactions", ["Throw the ball hard against a wall.", "Field the rebounds."], "40 reps", ["reaction", "third-base fielding"], ["baseball", "wall"]),
        _exercise("Backhand Grounders", ["Field backhand ground balls with controlled glove position."], "30 reps", ["backhand", "ground balls"], ["baseball"]),
        _exercise("Charge-and-Throw", ["Charge a slow roller.", "Field it cleanly and throw to a target."], "25 reps", ["slow rollers", "throwing on the run"], ["baseball", "target"]),
        _exercise("Cross-Diamond Throws", ["Throw accurately to a first-base target across the diamond."], "40 throws", ["arm strength", "throwing accuracy"], ["baseball", "target"]),
        _exercise("Lateral Explosion Drill", ["Shuffle 5 meters.", "Field a ball and throw."], "30 reps", ["lateral power", "fielding"], ["baseball"]),
        _exercise("One-Knee Fielding", ["Field balls from one knee to improve glove control."], "25 reps", ["glove control", "fielding fundamentals"], ["baseball"]),
    ],
    "shortstop_ss": [
        _exercise("Ground Ball Repetitions", ["Field ground balls and throw each one to a target."], "50 reps", ["ground balls", "throwing accuracy"], ["baseball", "target"]),
        _exercise("Deep Backhand Drill", ["Sprint to the ball.", "Field a backhand ball.", "Throw while moving."], "25 reps", ["range", "backhand", "throwing on the run"], ["baseball"]),
        _exercise("Double Play Footwork", ["Complete double-play turns around a base marker."], "30 reps", ["double play", "footwork"], ["marker"]),
        _exercise("Range Drill", ["Sprint 10 meters left or right to field a ball."], "20 reps each side", ["range", "lateral movement"], ["baseball"]),
        _exercise("Jump Throw Drill", ["Field the ball.", "Make the throw while jumping sideways."], "20 reps", ["jump throw", "athletic throw"], ["baseball"]),
        _exercise("Reaction Wall Drill", ["Field unpredictable rebounds from a wall."], "50 reps", ["reaction", "fielding"], ["baseball", "wall"]),
    ],
    "left_fielder_lf": [
        _exercise("Fly Ball Tracking", ["Toss the ball high.", "Track and catch it before it lands."], "40 catches", ["fly balls", "tracking"], ["baseball"]),
        _exercise("Ground Ball Charge", ["Sprint forward.", "Field a rolling ball and throw to a target."], "30 reps", ["charging grounders", "outfield fielding"], ["baseball", "target"]),
        _exercise("Crow Hop Throw", ["Field the ball.", "Perform a crow hop before throwing."], "30 reps", ["crow hop", "throwing mechanics"], ["baseball"]),
        _exercise("Drop-Step Sprint", ["Turn and sprint 20 meters to simulate tracking deep fly balls."], "20 reps", ["drop step", "deep-ball tracking"], []),
        _exercise("Wall Rebound Catch", ["Throw the ball high against a wall.", "Catch the rebound."], "40 reps", ["reaction catch", "fly ball tracking"], ["baseball", "wall"]),
        _exercise("Long Throw Accuracy", ["Throw balls to a target 40-50 meters away."], "30 throws", ["long throw", "accuracy"], ["baseball", "target"]),
    ],
    "center_fielder_cf": [
        _exercise("360-Degree Fly Ball Drill", ["Toss the ball in different directions.", "Track it and catch it."], "40 catches", ["fly ball tracking", "reaction"], ["baseball"]),
        _exercise("Gap Sprint Drill", ["Sprint 25 meters left or right.", "Simulate a catch at the end of the sprint."], "20 reps", ["gap coverage", "speed"], []),
        _exercise("Drop-Step Recovery", ["Turn and sprint backward 25 meters."], "20 reps", ["drop step", "recovery speed"], []),
        _exercise("Ground Ball Fielding", ["Charge rolling balls and throw to a target."], "30 reps", ["ground balls", "outfield fielding"], ["baseball", "target"]),
        _exercise("Crow Hop Throws", ["Perform long throws after fielding using a crow hop."], "30 throws", ["crow hop", "arm strength"], ["baseball"]),
        _exercise("Reaction Catch Drill", ["Catch unpredictable rebounds off a wall."], "50 catches", ["reaction", "catching"], ["baseball", "wall"]),
    ],
    "right_fielder_rf": [
        _exercise("Long Throw Drill", ["Throw balls to a target 50 meters away."], "40 throws", ["arm strength", "throwing accuracy"], ["baseball", "target"]),
        _exercise("Fly Ball Catching", ["Catch high fly balls with controlled footwork."], "40 catches", ["fly balls", "catching"], ["baseball"]),
        _exercise("Ground Ball Recovery", ["Field ground balls and throw to a target."], "30 reps", ["ground balls", "outfield fielding"], ["baseball", "target"]),
        _exercise("Crow Hop Power Throw", ["Perform a crow hop and throw at maximum power."], "25 reps", ["crow hop", "power throw"], ["baseball"]),
        _exercise("Fence Recovery Drill", ["Sprint to a marker.", "Turn and catch a fly ball."], "20 reps", ["fence recovery", "tracking"], ["marker", "baseball"]),
        _exercise("Drop-Step Sprint", ["Turn and sprint 25 meters to simulate deep-ball tracking."], "20 reps", ["drop step", "deep-ball tracking"], []),
    ],
    "designated_hitter_dh": [
        _exercise("Tee Swings", ["Hit balls from a batting tee."], "100 swings", ["batting", "contact"], ["baseball", "bat", "batting tee"]),
        _exercise("Soft Toss Swings", ["Toss the ball to yourself and hit it."], "75 swings", ["batting", "timing"], ["baseball", "bat"]),
        _exercise("Opposite-Field Hitting", ["Hit balls intentionally toward the opposite field."], "50 hits", ["bat control", "opposite-field hitting"], ["baseball", "bat"]),
        _exercise("Pull-Side Hitting", ["Hit balls intentionally toward the pull side."], "50 hits", ["bat control", "pull-side hitting"], ["baseball", "bat"]),
        _exercise("Power Swings", ["Perform maximum-power swings with controlled mechanics."], "50 swings", ["power hitting"], ["baseball", "bat"]),
        _exercise("Strike-Zone Recognition", ["Toss balls into different zones.", "Only swing at strikes."], "100 reps", ["strike-zone recognition", "plate discipline"], ["baseball", "bat"]),
    ],
}


LEARN_BEGINNER_ALONE: List[Exercise] = [
    _exercise("Wall Throw and Catch", ["Stand 10 meters from a wall.", "Throw the baseball against the wall.", "Catch the rebound cleanly."], "100 catches", ["throwing", "catching"], ["baseball", "wall"]),
    _exercise("Ground Ball Fielding", ["Roll the ball 10 meters ahead.", "Sprint to it.", "Field it with two hands."], "30 reps", ["ground balls", "fielding fundamentals"], ["baseball"]),
    _exercise("Tee Batting Practice", ["Place the ball on a batting tee.", "Hit the ball into a target area."], "100 swings", ["batting fundamentals"], ["baseball", "bat", "batting tee", "target"]),
    _exercise("Base Running Sprint", ["Sprint 27 meters / 90 feet to simulate running to first base.", "Walk back after each rep."], "20 reps", ["base running", "speed"], ["base marker"]),
    _exercise("Fly Ball Tracking", ["Toss the ball high into the air.", "Move underneath it and catch it."], "40 catches", ["fly balls", "tracking"], ["baseball"]),
    _exercise("Throw Accuracy Drill", ["Place a target 15 meters away.", "Throw balls attempting to hit the target."], "50 throws", ["throwing accuracy"], ["baseball", "target"]),
    _exercise("Field-and-Throw Drill", ["Roll the ball forward.", "Field it cleanly.", "Throw immediately to a target."], "30 reps", ["fielding", "throwing transition"], ["baseball", "target"]),
    _exercise("Bat Control Drill", ["Take slow practice swings.", "Focus on making contact with the center of the bat."], "50 swings", ["bat control", "swing mechanics"], ["bat"]),
    _exercise("Reaction Wall Drill", ["Throw the ball hard against a wall.", "React to the rebound and catch it."], "50 catches", ["reaction", "catching"], ["baseball", "wall"]),
    _exercise("Home Run Circuit", ["Hit a ball from a tee.", "Sprint a full lap around four markers representing the bases."], "10 reps", ["batting", "base running"], ["baseball", "bat", "batting tee", "markers"]),
]


LEARN_BEGINNER_GROUP: List[Exercise] = [
    _exercise("Partner Catch", ["Stand 15 meters apart.", "Throw and catch continuously."], "100 catches each", ["throwing", "catching"], ["baseball"]),
    _exercise("Soft Toss Hitting", ["One player tosses balls underhand.", "One player hits them."], "50 hits each", ["batting", "timing"], ["baseball", "bat"]),
    _exercise("Ground Ball Fielding", ["One player rolls ground balls.", "One player fields and throws back."], "40 reps", ["fielding", "throwing"], ["baseball"]),
    _exercise("Fly Ball Catching", ["One player throws high fly balls.", "One player catches them."], "40 catches", ["fly balls", "catching"], ["baseball"]),
    _exercise("Throw-and-Run Drill", ["Throw the ball to a partner.", "Immediately sprint to a first-base marker."], "20 reps", ["throwing", "base running"], ["baseball", "base marker"]),
    _exercise("Hit-and-Run Drill", ["One player hits the ball.", "Immediately sprint to first base."], "30 reps", ["batting", "base running"], ["baseball", "bat", "base marker"]),
    _exercise("Mini Infield Drill", ["One player hits ground balls.", "Another player fields and throws to first base."], "30 reps", ["infield fielding", "throwing"], ["baseball", "bat", "base marker"]),
    _exercise("Relay Throw Drill", ["Three players stand 20 meters apart.", "Throw the ball down the line and back."], "20 cycles", ["relay throwing", "team coordination"], ["baseball"]),
    _exercise("Base Running Circuit", ["One player hits the ball.", "Runner advances around all bases."], "15 reps", ["base running", "batting"], ["baseball", "bat", "bases or markers"]),
    _exercise("Beginner Mini Game", ["Play a simplified game.", "Pitch underhand.", "Use no strikeouts.", "Every hit puts the ball in play."], "3 innings", ["game understanding", "team play"], ["baseball", "bat", "bases or markers"]),
]


BASEBALL_CATALOG: Catalog = {
    "training_alone": {
        **POSITION_EXERCISES,
        "learn_how_to_play_beginner": LEARN_BEGINNER_ALONE,
    },
    "training_2_or_more_people": {
        **POSITION_EXERCISES,
        "learn_how_to_play_beginner": LEARN_BEGINNER_GROUP,
    },
}


def get_training_contexts() -> List[str]:
    """Return available training contexts."""
    return list(BASEBALL_CATALOG.keys())


def get_categories(context: str | None = None) -> List[str]:
    """Return category keys.

    If context is provided, return categories only for that context.
    """
    if context is not None:
        if context not in BASEBALL_CATALOG:
            raise KeyError(f"Unknown baseball training context: {context}")
        return list(BASEBALL_CATALOG[context].keys())

    categories: List[str] = []
    for context_catalog in BASEBALL_CATALOG.values():
        for category in context_catalog:
            if category not in categories:
                categories.append(category)
    return categories


def get_exercises(category: str, context: str | None = None) -> List[Exercise]:
    """Return exercises for a category.

    If context is omitted, the function searches all contexts and returns the
    first matching category. Use context for deterministic selection when a
    category exists in both solo and group training.
    """
    if context is not None:
        if context not in BASEBALL_CATALOG:
            raise KeyError(f"Unknown baseball training context: {context}")
        if category not in BASEBALL_CATALOG[context]:
            raise KeyError(f"Unknown baseball category for {context}: {category}")
        return deepcopy(BASEBALL_CATALOG[context][category])

    for context_catalog in BASEBALL_CATALOG.values():
        if category in context_catalog:
            return deepcopy(context_catalog[category])
    raise KeyError(f"Unknown baseball category: {category}")


def get_catalog() -> Catalog:
    """Return a deep copy of the full baseball catalog."""
    return deepcopy(BASEBALL_CATALOG)


__all__ = [
    "BASEBALL_CATALOG",
    "get_training_contexts",
    "get_categories",
    "get_exercises",
    "get_catalog",
]
