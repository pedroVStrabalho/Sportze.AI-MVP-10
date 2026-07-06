"""Basketball training catalog for Sportze.AI.

This module stores basketball exercises in a structured format so the training
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


POSITION_EXERCISES_ALONE: PositionCatalog = {
    "point_guard_pg": [
        _exercise("Cone Dribble Layup Series", ["Dribble through 10 cones.", "Finish with a layup after the final cone."], "30 reps", ["ball handling", "finishing"], ["basketball", "10 cones"]),
        _exercise("Moving Crossovers", ["Move up and down the court while performing crossovers."], "200 crossovers", ["ball handling", "change of direction"], ["basketball"]),
        _exercise("Wall Passing From 5 Distances", ["Pass against a wall from 5 different distances."], "200 total passes", ["passing accuracy", "touch"], ["basketball", "wall"]),
        _exercise("Top-of-Key Pull-Up Jumpers", ["Dribble into a pull-up jump shot from the top of the key."], "100 shots", ["pull-up shooting", "guard scoring"], ["basketball", "hoop"]),
        _exercise("Full-Court Speed Dribbles", ["Speed dribble from one baseline to the other under control."], "50 runs", ["transition speed", "ball control"], ["basketball", "court"]),
        _exercise("Behind-the-Back Direction Changes", ["Perform behind-the-back dribble changes while moving."], "100 reps", ["ball handling", "direction change"], ["basketball"]),
        _exercise("Paint Floaters", ["Attack the paint and shoot a controlled floater."], "75 makes", ["floater", "paint scoring"], ["basketball", "hoop"]),
        _exercise("Two-Ball Dribbling", ["Dribble two balls simultaneously with control."], "20 minutes", ["coordination", "ball handling"], ["2 basketballs"]),
    ],
    "shooting_guard_sg": [
        _exercise("5-Spot Three-Point Shooting", ["Shoot three-pointers from 5 spots around the arc."], "100 shots", ["three-point shooting"], ["basketball", "hoop"]),
        _exercise("One-Dribble Mid-Range Jumpers", ["Take one dribble into a mid-range jump shot."], "75 makes", ["mid-range shooting", "shot creation"], ["basketball", "hoop"]),
        _exercise("Wing Catch-and-Shoot Simulation", ["Simulate catching on the wing and shoot immediately."], "50 reps from each wing", ["catch-and-shoot", "wing shooting"], ["basketball", "hoop"]),
        _exercise("Both-Hand Layups", ["Make layups with each hand."], "50 makes per hand", ["finishing", "weak-hand development"], ["basketball", "hoop"]),
        _exercise("Jab-Step and Shoot", ["Use a jab step, create space, and shoot."], "100 reps", ["triple threat", "shooting footwork"], ["basketball", "hoop"]),
        _exercise("Step-Back Jump Shots", ["Create separation with a step-back and shoot."], "50 shots", ["shot creation", "footwork"], ["basketball", "hoop"]),
        _exercise("10-Spot Shooting Circuit", ["Shoot from 10 spots around the court."], "1 full circuit", ["shooting variety", "conditioning"], ["basketball", "hoop"]),
        _exercise("Consecutive Free-Throw Sets", ["Make 25 consecutive free throws."], "5 sets", ["free throws", "focus"], ["basketball", "hoop"]),
    ],
    "small_forward_sf": [
        _exercise("Three-Level Scoring Circuit", ["Alternate between layups, mid-range shots, and three-pointers."], "150 total shots", ["three-level scoring"], ["basketball", "hoop"]),
        _exercise("Full-Court Dribble and Finish", ["Dribble full court and finish at the basket."], "50 runs", ["transition finishing", "ball handling"], ["basketball", "court", "hoop"]),
        _exercise("Cone Triple-Threat Attacks", ["Attack a cone from triple-threat position."], "100 reps", ["triple threat", "driving"], ["basketball", "cone"]),
        _exercise("Self-Rebound and Finish", ["Throw or shoot the ball, grab your own rebound, and finish immediately."], "100 reps", ["rebounding", "put-back finishing"], ["basketball", "hoop"]),
        _exercise("Angle Pull-Up Jumpers", ["Shoot pull-up jump shots from different court angles."], "50 makes", ["pull-up shooting", "shot versatility"], ["basketball", "hoop"]),
        _exercise("Spin-Move Finishes", ["Attack the basket and finish after a spin move."], "50 reps", ["finishing", "footwork"], ["basketball", "hoop"]),
        _exercise("Defensive Slide Intervals", ["Perform defensive slides with low stance and active hands."], "20 minutes", ["defense", "lateral movement"], []),
        _exercise("Contact Finishes", ["Finish through contact using a pad or resistance band."], "30 finishes", ["contact finishing", "strength"], ["basketball", "pad or resistance band"]),
    ],
    "power_forward_pf": [
        _exercise("Drop-Step Finishes", ["Catch or self-toss in the post and finish with a drop step."], "100 reps", ["post scoring", "footwork"], ["basketball", "hoop"]),
        _exercise("Close-Range Bank Shots", ["Shoot bank shots from close range."], "75 makes", ["touch", "inside scoring"], ["basketball", "hoop"]),
        _exercise("Self-Toss Rebounds", ["Toss the ball off the backboard or rim and rebound it."], "100 rebounds", ["rebounding", "timing"], ["basketball", "hoop"]),
        _exercise("Up-and-Under Finishes", ["Use an up-and-under move and finish under control."], "50 reps", ["post moves", "finishing"], ["basketball", "hoop"]),
        _exercise("Both-Hand Hook Shots", ["Shoot hook shots with each hand."], "50 makes per hand", ["hook shot", "ambidextrous finishing"], ["basketball", "hoop"]),
        _exercise("Baseline-to-Baseline Finish Runs", ["Sprint baseline to baseline and finish at the rim."], "40 reps", ["conditioning", "finishing"], ["basketball", "court", "hoop"]),
        _exercise("Power Layups Through Contact", ["Attack the rim and finish a power layup through contact."], "75 reps", ["power finishing", "contact"], ["basketball", "pad or resistance band"]),
        _exercise("Post Footwork Around Cones", ["Move around cones using post pivots and footwork patterns."], "20 minutes", ["post footwork", "agility"], ["cones"]),
    ],
    "center_c": [
        _exercise("Paint Hook Shots", ["Shoot hook shots in the paint."], "100 makes", ["hook shot", "inside scoring"], ["basketball", "hoop"]),
        _exercise("Under-Basket Drop-Steps", ["Perform drop-step finishes under the basket."], "100 reps", ["post footwork", "finishing"], ["basketball", "hoop"]),
        _exercise("Self-Toss Rebounding", ["Toss the ball off the backboard or rim and rebound it."], "150 rebounds", ["rebounding", "positioning"], ["basketball", "hoop"]),
        _exercise("Backboard Shot-Block Jumps", ["Jump toward a backboard target as if blocking a shot."], "50 jumps", ["rim protection", "vertical power"], ["backboard target"]),
        _exercise("Direct Rim Power Finishes", ["Finish powerfully at the rim from close range."], "75 makes", ["power finishing", "inside scoring"], ["basketball", "hoop"]),
        _exercise("Reverse Layups From Both Sides", ["Perform reverse layups from both sides of the rim."], "50 reps", ["finishing angles", "body control"], ["basketball", "hoop"]),
        _exercise("Defensive Slides and Closeouts", ["Alternate defensive slides with closeouts to a target."], "20 minutes", ["defense", "mobility"], ["cone or target"]),
        _exercise("Rim-to-Half-Court Sprints", ["Sprint from the rim to half court and back."], "40 reps", ["conditioning", "big-man mobility"], ["court"]),
    ],
}


POSITION_EXERCISES_GROUP: PositionCatalog = {
    "point_guard_pg": [
        _exercise("Partner Chest and Bounce Passing", ["Complete chest passes and bounce passes with a partner."], "200 passes", ["passing", "accuracy"], ["basketball"]),
        _exercise("Pick-and-Roll Repetitions", ["Run pick-and-roll actions with a screener."], "50 reps", ["playmaking", "pick and roll"], ["basketball", "screener"]),
        _exercise("Full-Court Pressure Ball Handling", ["Handle the ball against full-court pressure."], "20 minutes", ["pressure handling", "decision making"], ["basketball"]),
        _exercise("Drive-and-Kick Passing", ["Drive into the paint and kick the ball out to shooters."], "100 passes", ["drive and kick", "playmaking"], ["basketball"]),
        _exercise("Fast-Break Leadership", ["Lead fast-break situations from half court."], "30 reps", ["transition offense", "decision making"], ["basketball"]),
        _exercise("Perimeter One-on-One", ["Play one-on-one starting from the perimeter."], "first to 21", ["scoring", "defense"], ["basketball", "hoop"]),
        _exercise("3-on-2 Transition Drill", ["Complete 3-on-2 transition possessions."], "30 reps", ["transition offense", "passing"], ["basketball"]),
        _exercise("Turnover-Free Team Sets", ["Run team offensive sets without turnovers."], "20 minutes", ["team offense", "execution"], ["basketball"]),
    ],
    "shooting_guard_sg": [
        _exercise("Partner Pass Shooting", ["Receive passes from a partner and shoot."], "200 shots", ["catch-and-shoot", "shooting volume"], ["basketball", "hoop"]),
        _exercise("Catch-and-Shoot Threes", ["Catch and shoot three-pointers."], "100 makes", ["three-point shooting"], ["basketball", "hoop"]),
        _exercise("Scoring One-on-One", ["Play one-on-one possessions focused on scoring."], "25 possessions", ["shot creation", "finishing"], ["basketball", "hoop"]),
        _exercise("Shots Off Screens", ["Use screens and shoot off movement."], "100 shots", ["off-ball movement", "shooting"], ["basketball", "screeners", "hoop"]),
        _exercise("Fast-Break Finishes", ["Finish fast-break opportunities at the rim."], "50 reps", ["transition finishing"], ["basketball", "hoop"]),
        _exercise("First-to-50 Made Shots Challenge", ["Compete to be first to 50 made shots."], "1 challenge", ["competitive shooting"], ["basketball", "hoop"]),
        _exercise("Curl-Cut and Shoot", ["Curl cut off a screen or marker and shoot."], "100 reps", ["movement shooting", "footwork"], ["basketball", "hoop"]),
        _exercise("Continuous 3-on-3 Off-Ball Game", ["Play continuous 3-on-3 focused on off-ball movement."], "1 game block", ["off-ball movement", "team offense"], ["basketball"]),
    ],
    "small_forward_sf": [
        _exercise("Multi-Area One-on-One", ["Play one-on-one possessions from different court areas."], "30 possessions", ["versatile scoring", "defense"], ["basketball", "hoop"]),
        _exercise("Rebound-and-Outlet", ["Secure the rebound and make an outlet pass."], "100 sequences", ["rebounding", "outlet passing"], ["basketball"]),
        _exercise("Transition Finishes With Teammates", ["Run transition lanes and finish with teammates."], "50 reps", ["transition", "finishing"], ["basketball", "hoop"]),
        _exercise("Defended Triple-Threat Attacks", ["Attack from triple-threat position against a defender."], "50 reps", ["triple threat", "scoring"], ["basketball"]),
        _exercise("Multi-Position Defense", ["Guard multiple positions in live or guided possessions."], "20 minutes", ["defense", "versatility"], ["basketball"]),
        _exercise("Mixed Finishes Around the Basket", ["Complete a variety of finishes around the basket."], "100 finishes", ["finishing package"], ["basketball", "hoop"]),
        _exercise("Continuous 2-on-2", ["Play continuous 2-on-2."], "20 minutes", ["spacing", "two-way play"], ["basketball"]),
        _exercise("Full-Court Two-Way Conditioning Game", ["Compete in a full-court game emphasizing offense and defense."], "1 game block", ["conditioning", "two-way play"], ["basketball"]),
    ],
    "power_forward_pf": [
        _exercise("Defended Post-Ups", ["Post up against a defender and finish or pass."], "50 reps", ["post scoring", "physicality"], ["basketball", "hoop"]),
        _exercise("Pick-and-Roll Set and Roll", ["Set the screen and roll to the basket."], "75 plays", ["screening", "rolling"], ["basketball"]),
        _exercise("Live Rebounding Battle", ["Compete for live rebounds."], "100 rebounds", ["rebounding", "physicality"], ["basketball", "hoop"]),
        _exercise("High-Low Passing", ["Complete high-low passing sequences."], "50 sequences", ["passing", "frontcourt chemistry"], ["basketball"]),
        _exercise("Low-Post One-on-One", ["Play low-post one-on-one possessions."], "25 possessions", ["post offense", "post defense"], ["basketball", "hoop"]),
        _exercise("Put-Back Finishes", ["Finish immediately after offensive rebounds."], "75 finishes", ["put-backs", "rebounding"], ["basketball", "hoop"]),
        _exercise("Post-Up Defense", ["Defend post-up attempts."], "50 attempts", ["post defense", "positioning"], ["basketball"]),
        _exercise("Interior 3-on-3", ["Play 3-on-3 focused on interior scoring."], "1 game block", ["interior scoring", "team play"], ["basketball"]),
    ],
    "center_c": [
        _exercise("Post-Up Battles", ["Battle for position and play post-up possessions under the basket."], "50 reps", ["post play", "physicality"], ["basketball", "hoop"]),
        _exercise("Rim Shot Contests", ["Contest shots around the rim without fouling."], "100 contests", ["rim protection", "defense"], ["basketball", "hoop"]),
        _exercise("Live Rebounding", ["Compete for live rebounds."], "150 rebounds", ["rebounding", "positioning"], ["basketball", "hoop"]),
        _exercise("Pick-and-Roll Finishes", ["Catch pick-and-roll passes and finish at the rim."], "75 finishes", ["roll finishing", "hands"], ["basketball", "hoop"]),
        _exercise("Low-Post First-to-15", ["Play low-post one-on-one."], "first to 15", ["post scoring", "post defense"], ["basketball", "hoop"]),
        _exercise("Shot-Block Attempts", ["Attempt shot blocks during defensive drills."], "50 attempts", ["shot blocking", "timing"], ["basketball", "hoop"]),
        _exercise("Rebound Outlet Passes", ["Rebound and immediately throw an outlet pass."], "100 passes", ["rebounding", "outlet passing"], ["basketball"]),
        _exercise("Rim Protection 3-on-3", ["Play 3-on-3 focused on rim protection and interior scoring."], "1 game block", ["rim protection", "interior scoring"], ["basketball"]),
    ],
}


LEARN_HOW_TO_PLAY_ALONE: List[Exercise] = [
    _exercise("Dominant-Hand Dribble", ["Dribble the ball with your dominant hand without stopping."], "10 minutes", ["basic ball handling"], ["basketball"]),
    _exercise("Non-Dominant-Hand Dribble", ["Dribble the ball with your non-dominant hand without stopping."], "10 minutes", ["weak-hand ball handling"], ["basketball"]),
    _exercise("Stationary Crossovers", ["Perform stationary crossovers with control."], "100 reps", ["crossover", "ball control"], ["basketball"]),
    _exercise("Dominant-Hand Layups", ["Make layups with your dominant hand."], "50 makes", ["finishing fundamentals"], ["basketball", "hoop"]),
    _exercise("Non-Dominant-Hand Layups", ["Make layups with your non-dominant hand."], "50 makes", ["weak-hand finishing"], ["basketball", "hoop"]),
    _exercise("Close-Range Paint Shots", ["Shoot close-range shots from inside the paint."], "100 shots", ["touch", "shooting basics"], ["basketball", "hoop"]),
    _exercise("Basic Free Throws", ["Shoot free throws with consistent routine."], "50 makes", ["free throws"], ["basketball", "hoop"]),
    _exercise("Wall Passing With Both Hands", ["Pass against a wall using both hands."], "200 passes", ["passing basics"], ["basketball", "wall"]),
    _exercise("Baseline-to-Baseline Dribble", ["Dribble from baseline to baseline under control."], "30 runs", ["movement dribbling"], ["basketball", "court"]),
    _exercise("Jump Stops and Pivots", ["Perform jump stops and pivot turns."], "50 reps", ["footwork", "balance"], ["basketball"]),
    _exercise("5-Spot Shooting", ["Shoot from 5 court spots.", "Make 10 shots at each spot."], "50 makes", ["shooting basics"], ["basketball", "hoop"]),
    _exercise("Basic Cone Ball-Handling Circuit", ["Complete a basic ball-handling circuit around 10 cones."], "1 circuit", ["ball handling", "coordination"], ["basketball", "10 cones"]),
]


LEARN_HOW_TO_PLAY_GROUP: List[Exercise] = [
    _exercise("Partner Chest Passes", ["Complete chest passes with a partner."], "200 passes", ["passing basics"], ["basketball"]),
    _exercise("Partner Bounce Passes", ["Complete bounce passes with a partner."], "200 passes", ["passing basics"], ["basketball"]),
    _exercise("Give-and-Go Passing", ["Practice give-and-go passes with a partner."], "50 reps", ["passing", "movement"], ["basketball"]),
    _exercise("No-Dribble Passing", ["Play passing-only basketball without dribbling."], "15 minutes", ["passing", "spacing"], ["basketball"]),
    _exercise("Partner-Pass Layups", ["Receive a partner pass and finish a layup."], "50 layups", ["finishing", "timing"], ["basketball", "hoop"]),
    _exercise("Near-Basket One-on-One", ["Play one-on-one starting near the basket."], "20 minutes", ["finishing", "defense"], ["basketball", "hoop"]),
    _exercise("Partner Defensive Slides", ["Practice defensive slides against a partner."], "15 minutes", ["defense", "footwork"], ["basketball"]),
    _exercise("Partner Fast-Break Layups", ["Complete fast-break layups with a partner."], "50 layups", ["transition", "finishing"], ["basketball", "hoop"]),
    _exercise("Keep-Away Passing", ["Play keep-away using passing only."], "15 minutes", ["passing", "decision making"], ["basketball"]),
    _exercise("First-to-25 Made Shots", ["Compete in a shooting challenge."], "first to 25 makes", ["shooting", "competition"], ["basketball", "hoop"]),
    _exercise("2-on-2 Half-Court", ["Play 2-on-2 half-court basketball."], "20 minutes", ["basic team play", "spacing"], ["basketball"]),
    _exercise("Controlled 3-on-3 Basic Rules", ["Play a controlled 3-on-3 game focusing on basic rules."], "1 game block", ["game understanding", "team play"], ["basketball"]),
]


BEGINNER_ALONE: List[Exercise] = [
    _exercise("Alternating-Hand Layups", ["Make layups while alternating hands every attempt."], "100 makes", ["finishing", "coordination"], ["basketball", "hoop"]),
    _exercise("Walking Crossovers", ["Perform crossovers while walking the court."], "200 crossovers", ["ball handling"], ["basketball"]),
    _exercise("Mid-Range Jump Shots", ["Shoot mid-range jump shots."], "75 shots", ["mid-range shooting"], ["basketball", "hoop"]),
    _exercise("Timed Free Throws", ["Make free throws in under 15 minutes."], "50 makes", ["free throws", "focus"], ["basketball", "hoop"]),
    _exercise("Cone Direction Changes", ["Dribble around cones and change direction."], "100 reps", ["ball handling", "change of direction"], ["basketball", "cones"]),
    _exercise("Euro-Step Finishes", ["Attack the basket and finish with a Euro step."], "50 reps", ["finishing", "footwork"], ["basketball", "hoop"]),
    _exercise("Angle Bank Shots", ["Shoot bank shots from different angles."], "50 shots", ["touch", "finishing angles"], ["basketball", "hoop"]),
    _exercise("Full-Court Dribble Layups", ["Dribble full court and finish with a layup."], "40 reps", ["transition", "finishing"], ["basketball", "court", "hoop"]),
    _exercise("10-Spot Shooting Circuit", ["Complete a 10-spot shooting circuit around the court."], "1 circuit", ["shooting variety"], ["basketball", "hoop"]),
    _exercise("Defensive Slides and Closeouts", ["Perform defensive slides and closeouts."], "20 minutes", ["defense", "footwork"], ["cone or target"]),
    _exercise("Consecutive Spot Makes", ["Make 25 consecutive shots from three different spots."], "3 spots", ["shooting consistency"], ["basketball", "hoop"]),
    _exercise("Dribble-Move Layup Alternation", ["Alternate between dribble moves and layups."], "20 minutes", ["ball handling", "finishing"], ["basketball", "hoop"]),
]


BEGINNER_GROUP: List[Exercise] = [
    _exercise("Turnover-Free Partner Passing", ["Complete passes with a partner without a turnover."], "300 passes", ["passing", "catching"], ["basketball"]),
    _exercise("Wing One-on-One", ["Play one-on-one possessions from the wing."], "25 possessions", ["scoring", "defense"], ["basketball", "hoop"]),
    _exercise("Partner Catch-and-Shoot", ["Shoot from partner passes."], "100 reps", ["catch-and-shoot"], ["basketball", "hoop"]),
    _exercise("Give-and-Go Attacks", ["Run give-and-go attacks to the basket."], "50 reps", ["passing", "cutting"], ["basketball", "hoop"]),
    _exercise("Continuous Fast-Break Layups", ["Run continuous fast-break layup drills."], "15 minutes", ["transition", "finishing"], ["basketball", "hoop"]),
    _exercise("Rebounding Battle", ["Compete for rebounds."], "first to 50 rebounds", ["rebounding", "competition"], ["basketball", "hoop"]),
    _exercise("Defensive Containment", ["Defend a ball handler and keep them in front."], "20 minutes", ["defense", "containment"], ["basketball"]),
    _exercise("2-on-2 Spacing and Passing", ["Play 2-on-2 focused on spacing and passing."], "1 game block", ["spacing", "team play"], ["basketball"]),
    _exercise("Pick-and-Roll Repetitions", ["Run pick-and-roll actions."], "50 reps", ["screening", "decision making"], ["basketball"]),
    _exercise("Team Shooting Challenge", ["Compete in a team shooting challenge."], "first to 100 made shots", ["shooting", "competition"], ["basketball", "hoop"]),
    _exercise("3-on-3 Half-Court", ["Play 3-on-3 half-court basketball."], "30 minutes", ["team play", "spacing"], ["basketball"]),
    _exercise("Controlled Full-Court Scrimmage", ["Play a controlled full-court scrimmage focusing on fundamentals."], "1 scrimmage", ["fundamentals", "game play"], ["basketball"]),
]


BASKETBALL_CATALOG: Catalog = {
    "training_alone": {
        **POSITION_EXERCISES_ALONE,
        "learn_how_to_play": LEARN_HOW_TO_PLAY_ALONE,
        "beginner": BEGINNER_ALONE,
    },
    "training_2_or_more_people": {
        **POSITION_EXERCISES_GROUP,
        "learn_how_to_play": LEARN_HOW_TO_PLAY_GROUP,
        "beginner": BEGINNER_GROUP,
    },
}


def get_training_contexts() -> List[str]:
    """Return available training contexts."""
    return list(BASKETBALL_CATALOG.keys())


def get_categories(context: str | None = None) -> List[str]:
    """Return category keys.

    If context is provided, return categories only for that context.
    """
    if context is not None:
        if context not in BASKETBALL_CATALOG:
            raise KeyError(f"Unknown basketball training context: {context}")
        return list(BASKETBALL_CATALOG[context].keys())

    categories: List[str] = []
    for context_catalog in BASKETBALL_CATALOG.values():
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
        if context not in BASKETBALL_CATALOG:
            raise KeyError(f"Unknown basketball training context: {context}")
        if category not in BASKETBALL_CATALOG[context]:
            raise KeyError(f"Unknown basketball category for {context}: {category}")
        return deepcopy(BASKETBALL_CATALOG[context][category])

    for context_catalog in BASKETBALL_CATALOG.values():
        if category in context_catalog:
            return deepcopy(context_catalog[category])
    raise KeyError(f"Unknown basketball category: {category}")


def get_catalog() -> Catalog:
    """Return a deep copy of the full basketball catalog."""
    return deepcopy(BASKETBALL_CATALOG)


__all__ = [
    "BASKETBALL_CATALOG",
    "get_training_contexts",
    "get_categories",
    "get_exercises",
    "get_catalog",
]
