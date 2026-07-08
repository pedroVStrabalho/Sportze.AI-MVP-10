"""Rugby training catalog for Sportze.AI.

This module contains rugby workouts and exercises codified from the Sportze.AI
training catalog. It includes learn/beginner sessions, Rugby Union 15s roles,
Rugby Sevens roles, and 2+ people tactical sessions.
"""

from __future__ import annotations

from typing import Any, Dict, List

SPORT = "rugby"
SPORT_NAME = "Rugby"


def exercise(name: str, prescription: str, notes: str | None = None) -> Dict[str, Any]:
    item: Dict[str, Any] = {"name": name, "prescription": prescription}
    if notes:
        item["notes"] = notes
    return item


def session(
    name: str,
    category: str,
    training_type: str,
    exercises: List[Dict[str, Any]],
    level: str | None = None,
    participants: str = "alone",
    focus: str | None = None,
    rugby_format: str | None = None,
    role: str | None = None,
) -> Dict[str, Any]:
    data: Dict[str, Any] = {
        "sport": SPORT,
        "name": name,
        "category": category,
        "training_type": training_type,
        "participants": participants,
        "exercises": exercises,
    }
    if level:
        data["level"] = level
    if focus:
        data["focus"] = focus
    if rugby_format:
        data["rugby_format"] = rugby_format
    if role:
        data["role"] = role
    return data


RUGBY_SESSIONS: List[Dict[str, Any]] = [
    session(
        name="Learn How To Play Rugby",
        category="Learn How To Play",
        level="learn",
        training_type="technical",
        participants="alone",
        focus="rugby fundamentals",
        exercises=[
            exercise("Right-Hand Wall Passing", "100 throws from 5 meters", "Throw a rugby ball against a wall right-handed."),
            exercise("Left-Hand Wall Passing", "100 throws from 5 meters", "Throw a rugby ball against a wall left-handed."),
            exercise("Two-Hand Ball Carry Runs", "20 x 20-meter runs", "Carry the ball in two hands."),
            exercise("Ball-Carrying Slalom", "15 slalom runs", "Place 6 cones in a zig-zag and carry the ball through them."),
            exercise("Running Ground Pickups", "50 pickups", "Pick up the rugby ball from the ground while running."),
            exercise("Ground Kicking To Target", "50 kicks", "Kick the ball off the ground toward a target area."),
            exercise("Ball-Carrying Sprints", "15 x 30 meters"),
            exercise("Side-Step Cone Runs", "20 runs"),
            exercise("Support Line Runs", "10 runs", "Sprint 20m, cut inward, then sprint another 20m."),
            exercise("Spin Passes Against Wall", "100 passes"),
            exercise("100m Shuttle Runs", "10 x 100 meters"),
            exercise("Continuous Direction-Change Carry", "15 minutes", "Run continuously with the ball and change direction every 20 seconds."),
        ],
    ),
    session(
        name="Learn How To Play Rugby With Teammates",
        category="Learn How To Play",
        level="learn",
        training_type="technical",
        participants="2+ people",
        focus="basic passing, support, and non-contact play",
        exercises=[
            exercise("Partner Passing", "200 passes"),
            exercise("Jogging Catch-And-Pass", "50 repetitions"),
            exercise("Support-Line Drills", "20 drills"),
            exercise("Two-On-One Attack", "30 situations"),
            exercise("Lateral Passing Sequences", "50 sequences"),
            exercise("Kick-And-Chase", "20 repetitions"),
            exercise("No-Drop Passing Chains", "15 chains x 10 passes"),
            exercise("Touch Rugby", "10 minutes"),
            exercise("Overlap Attack Drills", "20 drills"),
            exercise("Small-Sided Touch Rugby", "15 minutes"),
            exercise("Defensive Line Movement", "20 movements"),
            exercise("Non-Contact Rugby", "20 minutes"),
        ],
    ),
    session(
        name="Beginner Rugby",
        category="Beginner",
        level="beginner",
        training_type="balanced",
        participants="alone",
        focus="beginner ball carrying, passing, kicking, and conditioning",
        exercises=[
            exercise("Ball-Carrying Sprints", "20 x 40 meters"),
            exercise("Alternating Wall Passes", "200 passes"),
            exercise("Cone-Weave Carries", "20 runs"),
            exercise("Straight Sprints", "10 x 60 meters"),
            exercise("Target Zone Kicks", "75 kicks"),
            exercise("Speed Ground-Ball Pickups", "50 pickups"),
            exercise("100m Shuttle Runs", "10 shuttles"),
            exercise("400m Runs", "5 x 400 meters"),
            exercise("Lying Acceleration Runs", "20 starts"),
            exercise("Change-Of-Direction Runs", "30 runs"),
            exercise("Spin Passes Each Side", "100 each side"),
            exercise("Continuous Ball Carry", "20 minutes"),
        ],
    ),
    session(
        name="Beginner Rugby With Teammates",
        category="Beginner",
        level="beginner",
        training_type="balanced",
        participants="2+ people",
        focus="beginner team attack, defense, ruck entry, and modified play",
        exercises=[
            exercise("Teammate Passing", "300 passes"),
            exercise("Draw-And-Pass", "50 drills"),
            exercise("Two-On-One Attacks", "30 attacks"),
            exercise("Three-On-Two Attacks", "30 attacks"),
            exercise("Kick-And-Recover", "50 drills"),
            exercise("Tackle-Entry Technique", "30 repetitions", "Use tackle bags."),
            exercise("Ruck-Entry Drills", "20 drills"),
            exercise("Touch Rugby", "20 minutes"),
            exercise("Defensive Drift-Line Drills", "20 drills"),
            exercise("Overlap Attack Drills", "15 drills"),
            exercise("Support-Running Circuits", "15 circuits"),
            exercise("Modified Rugby", "30 minutes"),
        ],
    ),
]


def _add_role_session(name: str, category: str, rugby_format: str, role: str, participants: str, focus: str, items: List[tuple[str, str, str | None]], training_type: str = "position_specific") -> None:
    RUGBY_SESSIONS.append(session(name=name, category=category, training_type=training_type, participants=participants, focus=focus, rugby_format=rugby_format, role=role, exercises=[exercise(n, p, notes) for n, p, notes in items]))


# Rugby Union 15s roles
_UNION_ROLES: Dict[str, List[tuple[str, str, str | None]]] = {
    "Prop": [("Scrum Machine Push", "10 x 15 meters", None), ("Tackle Bag Carry", "10 x 20 meters", None), ("Pick-And-Go Carries", "15 carries", None), ("Power Sprints", "10 x 30 meters", None), ("Ruck Cleanouts", "30 cleanouts", None), ("Tackle-Bag Hits", "15 hits", None), ("Scrum Drives", "5 x 1 minute", None), ("Contact Pad Ball Carries", "20 x 15 meters", None)],
    "Hooker": [("Lineout Throws To Target", "100 throws", None), ("Lineout Throw-And-Follow", "30 drills", None), ("Ruck Entries", "20 entries", None), ("Tackle-Bag Hits", "20 hits", None), ("Short Carries", "10 x 30 meters", None), ("Pick-And-Go Drills", "15 drills", None), ("Moving-Target Lineouts", "50 throws", None), ("Scrum Engagements", "10 repetitions", None)],
    "Lock": [("Jump And Catch", "50 catches", None), ("Lineout-Lift Simulations", "20 simulations", None), ("Carries", "10 x 40 meters", None), ("Tackle-Bag Collisions", "20 collisions", None), ("Ruck Entries", "20 entries", None), ("Jump-And-Catch Sequences", "10 sequences", None), ("100m Runs", "8 x 100 meters", None), ("Maul-Drive Efforts", "15 efforts", None)],
    "Flanker": [("Tackle-Bag Hits", "30 hits", None), ("Ruck Contests", "30 contests", None), ("40m Sprints", "15 x 40 meters", None), ("Ball-Steal Drills", "20 drills", None), ("Support-Line Runs", "20 runs", None), ("Pick-And-Go Carries", "20 carries", None), ("400m Runs", "5 x 400 meters", None), ("Defensive Pressure Circuits", "15 circuits", None)],
    "Number 8": [("Pick-And-Go Carries", "20 carries", None), ("Tackle-Bag Collisions", "15 collisions", None), ("Power Carries", "10 x 50 meters", None), ("Support-Line Drills", "20 drills", None), ("Ruck Entries", "20 entries", None), ("100m Runs", "8 x 100 meters", None), ("Offload Drills", "15 drills", None), ("Defensive Transition Circuits", "10 circuits", None)],
    "Scrum-Half": [("Ground Passes", "300 passes", None), ("Box Kicks", "50 kicks", None), ("Pass-Sprint-Pass", "30 sequences", None), ("Acceleration Sprints", "15 x 20 meters", None), ("Directional Passing", "100 passes each direction", None), ("Decision-Making Passing", "20 drills", None), ("Tactical Kicks", "50 kicks", None), ("300m Runs", "5 x 300 meters", None)],
    "Fly-Half": [("Tactical Kicks", "100 kicks", None), ("Spin Passes", "200 passes", None), ("Grubber Kicks", "50 kicks", None), ("Cross-Field Kicks", "50 kicks", None), ("Attacking-Line Drills", "20 drills", None), ("Goal-Kick Attempts", "50 attempts", None), ("Pass-Kick Combinations", "20 combinations", None), ("400m Runs", "6 x 400 meters", None)],
    "Center": [("Hard Running Lines", "20 lines", None), ("Side-Step Attacks", "20 attacks", None), ("Contact Carries", "15 carries", None), ("40m Sprints", "15 x 40 meters", None), ("Draw-And-Pass Drills", "50 drills", None), ("Defensive Line Drills", "20 drills", None), ("Support-Line Circuits", "10 circuits", None), ("Tackle-Bag Hits", "20 hits", None)],
    "Wing": [("60m Sprints", "20 x 60 meters", None), ("Kick-Chase Efforts", "20 efforts", None), ("Corner Finishing Runs", "15 runs", None), ("Side-Step Attacks", "20 attacks", None), ("100m Sprints", "10 x 100 meters", None), ("Aerial-Ball Catches", "20 catches", None), ("Support-Line Runs", "15 runs", None), ("Acceleration Starts", "20 starts", None)],
    "Fullback": [("High-Ball Catches", "100 catches", None), ("Tactical Kicks", "50 kicks", None), ("Counterattack Lines", "15 lines", None), ("50m Sprints", "15 x 50 meters", None), ("Kick-Return Drills", "30 drills", None), ("Support-Line Runs", "20 runs", None), ("Moving-Kick Catches", "50 catches", None), ("400m Runs", "5 x 400 meters", None)],
}
for _role, _items in _UNION_ROLES.items():
    _add_role_session(f"Rugby Union 15s {_role}", "Rugby Union 15s", "15s", _role, "2+ people", f"Rugby Union {_role.lower()} position work", _items)

# Rugby Sevens roles and special sessions
_SEVENS: Dict[str, tuple[str, str, str, List[tuple[str, str, str | None]]]] = {
    "Front Row Forward": ("Front Row Forward", "2+ people", "restarts, contact situations, ball carrying, breakdown work, and physical dominance", [("Accelerating Ball Carries", "20 x 40 meters", "Accelerate through the final 15 meters."), ("Tackle-Bag Collisions", "30 collisions", "Get back to your feet immediately after each hit."), ("Ruck-Entry Drills", "20 drills", "Use a tackle bag."), ("Ball-Carrying Sprints", "15 x 50 meters", None), ("Pick-And-Go Carries", "20 x 15 meters", None), ("Restart-Kick Receptions", "50 jump-and-catches", None), ("100m Shuttle Runs", "10 x 100 meters", None), ("Support-Line Circuits", "15 circuits", "Sprint 30m, change angle, then sprint another 30m.")]),
    "Mobile Forward": ("Mobile Forward", "2+ people", "tackling, defensive coverage, support play, and ball carrying in space", [("40m Sprints", "20 x 40 meters", None), ("Tackle-Bag Hits", "25 hits", None), ("Breakdown-Entry Drills", "20 drills", None), ("Support-Line Circuits", "15 x 60 meters", None), ("Ball-Carrying Slalom Runs", "20 runs", None), ("Game-Pace 200m Runs", "10 x 200 meters", None), ("Defensive Recovery Runs", "20 runs", "Sprint 30m, turn, and sprint back."), ("High-Intensity 500m Runs", "5 x 500 meters", None)]),
    "Playmaker": ("Playmaker", "alone", "distribution, creating space, decision making, and tempo control", [("Wall Spin Passes", "300 passes", None), ("Lateral Moving Passes", "100 passes", None), ("Long Passes", "50 passes of at least 15 meters", None), ("Draw-And-Pass Around Cones", "20 drills", None), ("Grubber Kicks", "50 kicks", None), ("Kick-Pass Combinations", "30 combinations", None), ("Sprint And Pass", "15 x 40 meters", "Deliver a pass immediately at the end of each sprint."), ("Match-Pace 300m Runs", "8 x 300 meters", None)]),
    "Finisher": ("Finisher", "alone", "scoring tries, speed, support running, and one-on-one attacking", [("60m Sprints", "20 x 60 meters", None), ("Side-Step Cone Attacks", "30 attacks", None), ("Try-Finishing Runs", "20 runs", "Dive over a marked try line."), ("80m Sprints", "15 x 80 meters", None), ("Kick-Chase Efforts", "20 efforts", None), ("Support-Line Circuits", "15 circuits", None), ("Maximum 100m Sprints", "10 x 100 meters", None), ("Lying Acceleration Starts", "20 starts", None)]),
    "Speed & Acceleration": ("Speed & Acceleration", "alone", "pure speed, first-step explosiveness, and chase speed", [("20m Sprints", "15 x 20 meters", None), ("40m Sprints", "15 x 40 meters", None), ("60m Sprints", "10 x 60 meters", None), ("Falling Starts", "20 x 20 meters", None), ("Reaction Sprints", "15 starts", "Use random starting signals."), ("Hill Sprints", "10 x 30 meters", None), ("Change-Of-Direction Sprints", "20 sprints", "Use cones."), ("150m Sprints", "5 x 150 meters", None)]),
    "Conditioning & Repeat Sprint Ability": ("Conditioning & Repeat Sprint Ability", "alone", "Rugby 7s match fitness, recovery between efforts, and late-game speed", [("Repeated 100m Sprints", "20 x 100 meters, 20 seconds rest", None), ("Game-Pace 200m Runs", "10 x 200 meters", None), ("300m Repeats", "8 x 300 meters, 45 seconds rest", None), ("High-Intensity 500m Runs", "5 x 500 meters", None), ("150m Shuttle Runs", "10 shuttles", None), ("Continuous Acceleration Run", "25 minutes", "Accelerate every minute."), ("Sprint-Repeat Intervals", "15 x 50 meters", None), ("2 km Time Trial", "maximum sustainable pace", None)]),
    "Open Field Attack": ("Open Field Attack", "2+ people", "creating overlaps, passing under pressure, and exploiting space", [("Two-On-One Attacks", "50 situations", None), ("Three-On-Two Attacks", "30 situations", None), ("Full-Width Passing Attacks", "20 attacks", None), ("Support-Line Attack Sequences", "20 sequences", None), ("Offload Through Contact Pads", "20 drills", None), ("Three-Pass Touch Rugby", "15 minutes", "Maximum of 3 passes before scoring."), ("Overlap Attack Drills", "20 drills", None), ("Conditioned 7s Attack Scenarios", "20 minutes", None)]),
    "Open Field Defense": ("Open Field Defense", "2+ people", "one-on-one tackling, defensive spacing, and recovery defense", [("One-On-One Tackling", "30 drills", None), ("Drift-Defense Repetitions", "20 reps", None), ("Scramble-Defense Recoveries", "20 recoveries", None), ("Defensive Line-Speed Drills", "20 drills", None), ("Full-Field Recovery Chases", "15 chases", None), ("Tackle-And-Reload", "20 drills", "Make a tackle, get up, and immediately defend again."), ("Defense-Only Touch Rugby", "15 minutes", "Attackers have numerical superiority."), ("Conditioned Defensive Scenarios", "20 minutes", "Use 7-player teams.")]),
}
for _name, (_role, _participants, _focus, _items) in _SEVENS.items():
    _add_role_session(f"Rugby Sevens {_name}", "Rugby Sevens", "7s", _role, _participants, _focus, _items, training_type="sevens_specific")


def get_sessions() -> List[Dict[str, Any]]:
    return RUGBY_SESSIONS


def get_workouts() -> List[Dict[str, Any]]:
    return RUGBY_SESSIONS


def get_sessions_by_level(level: str) -> List[Dict[str, Any]]:
    normalized = level.lower().strip()
    return [s for s in RUGBY_SESSIONS if s.get("level", "").lower() == normalized]


def get_sessions_by_participants(participants: str) -> List[Dict[str, Any]]:
    normalized = participants.lower().strip()
    return [s for s in RUGBY_SESSIONS if s.get("participants", "").lower() == normalized]


def get_sessions_by_format(rugby_format: str) -> List[Dict[str, Any]]:
    normalized = rugby_format.lower().strip()
    return [s for s in RUGBY_SESSIONS if s.get("rugby_format", "").lower() == normalized]


def get_sessions_by_role(role: str) -> List[Dict[str, Any]]:
    normalized = role.lower().strip()
    return [s for s in RUGBY_SESSIONS if s.get("role", "").lower() == normalized]


WORKOUTS = RUGBY_SESSIONS
SESSIONS = RUGBY_SESSIONS
TRAINING_CATALOG = RUGBY_SESSIONS

__all__ = [
    "SPORT",
    "SPORT_NAME",
    "RUGBY_SESSIONS",
    "WORKOUTS",
    "SESSIONS",
    "TRAINING_CATALOG",
    "get_sessions",
    "get_workouts",
    "get_sessions_by_level",
    "get_sessions_by_participants",
    "get_sessions_by_format",
    "get_sessions_by_role",
]
