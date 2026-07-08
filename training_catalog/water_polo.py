"""Water polo training catalog for Sportze.AI.

This module contains water polo workouts and exercises codified from the
Sportze.AI training catalog. It includes solo fundamentals, swimming, ball
control, goalkeeper and center-forward sessions, plus 2+ people tactical,
position-specific, match, and resistance sessions.
"""

from __future__ import annotations

from typing import Any, Dict, List

SPORT = "water_polo"
SPORT_NAME = "Water Polo"


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
    if role:
        data["role"] = role
    return data


WATER_POLO_SESSIONS: List[Dict[str, Any]] = [
    session(
        name="Learn How To Play Water Polo",
        category="Learn How To Play",
        level="learn",
        training_type="technical",
        participants="alone",
        focus="basic floating, ball handling, passing, shooting, and swimming",
        exercises=[
            exercise("Basic Floating & Eggbeater", "10 x 30 seconds", "Eggbeater continuously for 30 seconds. Rest 30 seconds."),
            exercise("Basic Ball Pickup", "30 repetitions", "Throw the ball 2-3 meters away, swim to it, and pick it up with one hand."),
            exercise("Wall Passing", "100 one-hand passes", "Stand 3 meters from a wall. Throw and catch with one hand."),
            exercise("Basic Water Dribbling", "8 x 25m", "Swim while pushing the ball in front."),
            exercise("Catch & Lift", "50 repetitions", "Toss the ball upward, catch with one hand, and raise immediately into shooting position."),
            exercise("High Elbow Shooting Mechanics", "60 slow motions", "Perform slow shooting motions without shooting."),
            exercise("Vertical Ball Control", "8 x 45 seconds", "Eggbeater while moving the ball around your body."),
            exercise("Swim & Turn", "10 repetitions", "Swim 25m, perform one quick body rotation, then continue swimming."),
            exercise("Crossbar Accuracy", "50 throws from 5 meters", "Throw at the crossbar."),
            exercise("Ball Protection", "3 minutes", "Hold the ball away from your body while eggbeatering. Alternate sides every 10 seconds."),
            exercise("Fast Pickup", "20 repetitions", "Place ball floating, sprint 10m, pick it up, and shoot."),
            exercise("Mini Time Trial", "3 x 100m", "Rest 2 minutes between repeats."),
        ],
    ),
    session(
        name="Beginner Water Polo",
        category="Beginner",
        level="beginner",
        training_type="balanced",
        participants="alone",
        focus="beginner swim, eggbeater, passing, shooting, and ball control",
        exercises=[
            exercise("Easy Crawl", "6 x 50m"),
            exercise("Crawl With Ball", "8 x 25m"),
            exercise("Wall Passes", "40 passes"),
            exercise("Stationary Shots", "30 shots"),
            exercise("Eggbeater Intervals", "10 x 20 seconds"),
            exercise("Sprint Swim", "6 x 25m"),
            exercise("Fake Shots", "50 fakes"),
            exercise("Pickups", "25 pickups"),
            exercise("One-Hand Ball Carry Swim", "8 x 15m"),
            exercise("One-Hand Catches", "50 catches"),
            exercise("Alternating Ball Rotations", "100 forehand/backhand rotations"),
            exercise("Continuous Swim With Ball", "200m"),
        ],
    ),
    session(
        name="Sprint Swimming",
        category="Sprint Swimming",
        training_type="conditioning",
        participants="alone",
        focus="water polo sprint speed and race pace swimming",
        exercises=[
            exercise("Maximal Sprint 25s", "8 x 25m @ 22 seconds"),
            exercise("Maximal Sprint 25s", "10 x 25m @ 20 seconds"),
            exercise("100m Pace Set", "8 x 100m @ 1:45"),
            exercise("50m Pace Set", "6 x 50m @ 45 seconds"),
            exercise("100m Time Trial", "3 repetitions"),
            exercise("Explosive Starts", "12 x 15m"),
            exercise("Butterfly-To-Crawl Sprint", "8 x 25m", "Butterfly to halfway, crawl finish."),
            exercise("Explosive Starts With Max Strokes", "10 starts", "First 8 strokes maximal."),
            exercise("Threshold 75s", "8 x 75m"),
            exercise("Descending 50s", "10 x 50m"),
            exercise("Broken 100s", "4 x (4 x 25m)"),
            exercise("Dive Or Wall Push Sprint", "8 x 25m"),
        ],
    ),
    session(
        name="Swimming With Ball",
        category="Swimming With Ball",
        training_type="technical_conditioning",
        participants="alone",
        focus="ball-carry swimming endurance and speed",
        exercises=[
            exercise("Continuous Crawl With Ball", "400m"),
            exercise("Carrying Ball", "500m"),
            exercise("One-Hand Ball Hold", "500m"),
            exercise("Crawl With Ball", "10 x 100m"),
            exercise("Kick-And-Stroke Ball Swim", "6 x 100m", "Alternate 12.5m kick only and 12.5m full stroke."),
            exercise("Ball Carry Medley", "200m"),
            exercise("Accelerating Ball Swim", "8 x 50m", "Accelerate every fourth stroke."),
            exercise("Backstroke With Ball", "8 x 25m"),
            exercise("Backward Recovery To Forward Explosion", "8 x 25m", "Move backward with ball then explode forward."),
            exercise("Timed Ball Swim", "4 x 100m"),
            exercise("Maximal Sprint With Ball", "10 x 50m"),
            exercise("Continuous Ball Swim", "600m"),
        ],
    ),
    session(
        name="Endurance Swimming",
        category="Endurance Swimming",
        training_type="conditioning",
        participants="alone",
        focus="aerobic and threshold water polo swim base",
        exercises=[
            exercise("Breathing 6/1 Set", "5 x 200m"),
            exercise("Strong/Easy 200s", "10 x 200m alternating strong/easy"),
            exercise("Aerobic 100s", "10 x 100m"),
            exercise("Pace 100s", "6 x 3 x 100m @ 1:35"),
            exercise("Threshold 75s", "20 x 75m"),
            exercise("Threshold 50s", "20 x 50m"),
            exercise("Medley Swim", "400m"),
            exercise("Continuous Swim", "600m"),
            exercise("Breathing Every 6 Strokes", "400m"),
            exercise("Breathing Every 8 Strokes", "400m"),
            exercise("Negative Split Swim", "800m"),
            exercise("Continuous Swim", "1000m"),
        ],
    ),
    session(
        name="Eggbeater Power",
        category="Eggbeater Power",
        training_type="strength",
        participants="alone",
        focus="vertical leg power and water polo elevation",
        exercises=[
            exercise("Eggbeater Intervals", "12 x 30 seconds"),
            exercise("Ball Overhead Eggbeater", "8 x 30 seconds"),
            exercise("Maximal Vertical Jumps", "50 jumps"),
            exercise("Diagonal Jumps", "40 jumps"),
            exercise("Lateral Jumps", "40 jumps"),
            exercise("Crossbar Touches", "30 touches"),
            exercise("Jump Then Simulate Shot", "40 repetitions"),
            exercise("Weighted-Ball Jumps", "30 repetitions"),
            exercise("Elastic Resistance Eggbeater", "1 drill", "Eggbeater while holding elastic resistance."),
            exercise("Jump-Catch-Shoot", "40 repetitions"),
            exercise("Continuous Eggbeater", "10 x 1 minute"),
            exercise("Uninterrupted Eggbeater", "5 minutes"),
        ],
    ),
    session(
        name="Shooting",
        category="Shooting",
        training_type="technical",
        participants="alone",
        focus="water polo shooting variations",
        exercises=[
            exercise("High-Corner Shots", "100 shots"),
            exercise("Leaning Shots", "80 shots"),
            exercise("Back-Floating Shots", "60 shots"),
            exercise("Reverse Shots", "80 shots"),
            exercise("Shot Fakes Then Finish", "100 repetitions"),
            exercise("One-Leg Receive-And-Shoot", "80 repetitions"),
            exercise("Three-Shot Combinations", "50 combinations"),
            exercise("Catch-And-Shoot", "80 shots"),
            exercise("Moving Shots", "60 shots"),
            exercise("Off-Balance Shots", "50 shots"),
            exercise("Sprint Then Shoot", "50 repetitions"),
            exercise("Jump Then Shoot", "40 repetitions"),
        ],
    ),
    session(
        name="Ball Control",
        category="Ball Control",
        training_type="technical",
        participants="alone",
        focus="water polo ball handling",
        exercises=[
            exercise("Dribbling", "400m"),
            exercise("Ball Locked In One Hand", "400m"),
            exercise("Continuous Hand Dribbles", "100 dribbles"),
            exercise("Figure-Eight Rotations", "100 rotations"),
            exercise("Rotations Each Direction", "100 each direction"),
            exercise("Overhead Carries", "100 carries"),
            exercise("Weighted-Ball Transfers", "50 transfers"),
            exercise("One-Hand Pickups", "100 pickups"),
            exercise("Fake Pickups", "50 pickups"),
            exercise("Ball Circles Around Body", "100 circles"),
            exercise("Alternating Hand Transfers", "100 transfers"),
            exercise("Nonstop Ball Handling", "5 minutes"),
        ],
    ),
    session(
        name="Goalkeeper Solo",
        category="Goalkeeper",
        training_type="position_specific",
        participants="alone",
        role="goalkeeper",
        focus="goalkeeper elevation, reactions, saves, and outlet passing",
        exercises=[
            exercise("Explosive Crossbar Touches", "60 touches"),
            exercise("Lateral Goal-Line Jumps", "80 jumps"),
            exercise("High-Ball Catches", "100 catches"),
            exercise("Low-Ball Saves", "80 saves"),
            exercise("One-Hand Tip Saves", "50 saves"),
            exercise("Double-Save Simulations", "40 simulations"),
            exercise("Explosive Recoveries From Floating", "50 recoveries"),
            exercise("Medicine-Ball Overhead Throws", "40 throws"),
            exercise("Elastic Jump Resistance", "8 x 30 seconds"),
            exercise("Reaction Catches Off Wall", "60 catches"),
            exercise("Outlet Passes To Halfway", "50 passes"),
            exercise("Continuous Goalkeeper Movement", "10 x 1 minute"),
        ],
    ),
    session(
        name="Center Forward Solo",
        category="Center Forward",
        training_type="position_specific",
        participants="alone",
        role="center_forward",
        focus="center-forward receiving, protection, spins, and finishing",
        exercises=[
            exercise("Ball-Protection Holds", "100 holds"),
            exercise("Reverse-Spin Movements", "80 movements"),
            exercise("Front-Spin Movements", "80 movements"),
            exercise("Catch-Turn-Shoot", "100 repetitions"),
            exercise("Quick Releases", "80 releases"),
            exercise("One-Hand Catches Under Pressure Simulation", "100 catches"),
            exercise("High-Point Catches", "60 catches"),
            exercise("Fake-Spin Then Finish", "80 repetitions"),
            exercise("Eggbeater Power Catches", "100 catches"),
            exercise("Inside-Water Pickups", "80 pickups"),
            exercise("Immediate Backhand Finishes", "60 finishes"),
            exercise("Complete Center-Forward Sequences", "50 sequences", "Receive, protect, spin, and shoot."),
        ],
    ),
    session(
        name="Learn How To Play Water Polo With Teammates",
        category="Learn How To Play",
        level="learn",
        training_type="technical",
        participants="2+ people",
        focus="passing, movement, shooting, contact, and mini-game basics",
        exercises=[
            exercise("Partner One-Hand Passing", "100 passes", "Partners stand 4 meters apart without dropping the ball."),
            exercise("Swimming Passes", "8 x 25m", "Partners pass every five strokes without stopping."),
            exercise("Triangle Passing", "150 passes", "Groups of three rotate clockwise after every 25 passes."),
            exercise("Catch-Lift-Return", "60 repetitions each", "Catch with one hand, raise into shooting position, and return the pass."),
            exercise("2v1 Possession", "10 consecutive passes before switching", "Play in a 10 x 10m area."),
            exercise("Catch-And-Shoot Line", "20 repetitions each from 5 meters"),
            exercise("Ball Race And Shoot", "15 repetitions each", "Two players race 15m to a floating ball; winner picks up and shoots."),
            exercise("Moving Square Passing", "5 continuous minutes", "Four players pass around a 6 x 6m area."),
            exercise("3v3 Possession", "6 x 2-minute rounds", "Every player must touch the ball before a shot."),
            exercise("Controlled Shoulder Contact", "10 x 20 seconds", "Partners maintain eggbeater while practicing controlled shoulder contact."),
            exercise("Goalkeeper Outlet Passing", "15 throws to each teammate"),
            exercise("Controlled 4v4 Mini Game", "10 minutes", "Emphasize passing over shooting."),
        ],
    ),
    session(
        name="Beginner Water Polo With Teammates",
        category="Beginner",
        level="beginner",
        training_type="balanced",
        participants="2+ people",
        focus="beginner team play, counterattack, finishing, pressure, and scrimmage",
        exercises=[
            exercise("Moving Partner Passes", "150 passes", "Partners swim side by side."),
            exercise("3v2 Counterattack", "15 repetitions", "Rotate every attack."),
            exercise("Fake And Finish", "40 repetitions each", "Attacker receives, fake shoots once, then finishes."),
            exercise("4v4 Three-Pass Game", "10 minutes", "Maximum of three passes before shooting."),
            exercise("Front-Water Pickups Under Pressure", "30 pickups"),
            exercise("Shoulder-To-Shoulder Entries", "20 entries, then switch"),
            exercise("High Passing With Jump", "100 passes", "Both players jump before every catch."),
            exercise("Continuous 2v2", "12 minutes", "Change opponents every two minutes."),
            exercise("Goalkeeper Distribution After Saves", "40 repetitions"),
            exercise("5v4 Spacing", "10 minutes"),
            exercise("Center Fronting Defense", "20 repetitions each"),
            exercise("Controlled Scrimmage", "10 minutes", "Use standard rules."),
        ],
    ),
    session(
        name="General Player Team Session",
        category="General Player",
        training_type="team_tactical",
        participants="2+ people",
        focus="general field player perimeter, counterattack, defense, and scrimmage",
        exercises=[
            exercise("Moving Perimeter Passes", "200 continuous passes"),
            exercise("Sprint-Receive-Shoot-Defend", "25 repetitions", "Sprint 20m, receive, shoot, then defend counterattack."),
            exercise("4v4 Half-Court Pressure", "12 minutes"),
            exercise("Perimeter Shots While Moving", "40 shots"),
            exercise("3v2 Counterattacks", "15 minutes"),
            exercise("6v6 Press Defense", "8 possessions"),
            exercise("Catch-Fake-Shoot", "50 combinations"),
            exercise("Turnover Recovery Transitions", "20 full-pool transitions"),
            exercise("Nonstop Possession Game", "5 minutes", "No player may stop moving."),
            exercise("Offense-Defense Whistle Alternation", "15 minutes"),
            exercise("Defensive Blocks Against Perimeter Shots", "20 blocks"),
            exercise("Full Scrimmage", "20 minutes"),
        ],
    ),
    session(
        name="Goalkeeper Team Session",
        category="Goalkeeper",
        training_type="position_specific",
        participants="2+ people",
        role="goalkeeper",
        focus="live shots, outlet passing, game management, and scrimmage goalkeeping",
        exercises=[
            exercise("Perimeter Shot Saves", "100 shots from alternating sides"),
            exercise("Close-Range Center Shots", "50 shots"),
            exercise("Cross-Cage Outlet Passes", "60 passes"),
            exercise("Skip Shot Reactions", "40 shots"),
            exercise("Lob Shot Defense", "30 shots"),
            exercise("Penalty Saves", "40 saves"),
            exercise("Goalkeeper Vs Counterattack", "20 repetitions"),
            exercise("Crossbar Touches Between Saves", "50 touches"),
            exercise("Extra-Man Shot Defense", "40 shots"),
            exercise("Blocked-Shot Recoveries", "30 recoveries"),
            exercise("Defensive Direction", "20 live possessions"),
            exercise("Goalkeeper Scrimmage", "20 minutes"),
        ],
    ),
    session(
        name="Center Forward Team Session",
        category="Center Forward",
        training_type="position_specific",
        participants="2+ people",
        role="center_forward",
        focus="center-forward contact receiving, finishing, sealing, and live play",
        exercises=[
            exercise("Receive-Protect-Turn-Shoot", "50 repetitions"),
            exercise("Backhand Finishes", "40 finishes"),
            exercise("Front-Spin Shots", "50 shots"),
            exercise("Reverse-Spin Shots", "50 shots"),
            exercise("Inside-Water Battles", "20 x 30-second rounds"),
            exercise("Two-Second Receive And Shoot", "40 repetitions"),
            exercise("Seal Defender Before Pass", "50 repetitions"),
            exercise("2v2 Center Battles", "15 minutes"),
            exercise("Double-Team Receive And Pass Out", "40 repetitions"),
            exercise("One-Hand Catches Under Contact", "40 catches"),
            exercise("Exclusion-Drawing Attempts", "30 attempts"),
            exercise("Live Center Scrimmage", "20 minutes"),
        ],
    ),
    session(
        name="Passing Team Session",
        category="Passing",
        training_type="technical",
        participants="2+ people",
        focus="water polo passing variations",
        exercises=[
            exercise("One-Hand Passes", "200 passes"),
            exercise("Wet Passes", "100 passes"),
            exercise("Dry Passes", "100 passes"),
            exercise("Skip Passes", "100 passes"),
            exercise("Cross-Pool Passes", "100 passes"),
            exercise("Moving Passes", "100 passes"),
            exercise("Quick-Release Passes", "100 passes"),
            exercise("Two-Hand Passes", "100 passes"),
            exercise("Long Outlet Passes", "100 passes"),
            exercise("One-Touch Passes", "100 passes"),
            exercise("Triangle Passes", "150 passes"),
            exercise("Square Passing Rotations", "150 rotations"),
        ],
    ),
    session(
        name="Wrestling Contact Session",
        category="Wrestling",
        training_type="contact",
        participants="2+ people",
        focus="luta, body position, center battles, and contact pressure",
        exercises=[
            exercise("Shoulder-To-Shoulder Battle", "10 x 20 seconds"),
            exercise("Center Wrestling", "8 x 30 seconds"),
            exercise("Front-To-Front Battles", "20 battles"),
            exercise("Back-To-Back Battles", "20 battles"),
            exercise("Ball-Protection Battles", "20 battles"),
            exercise("Spin Escapes", "20 escapes"),
            exercise("Counter-Spin Escapes", "20 escapes"),
            exercise("Inside-Water Battles", "20 battles"),
            exercise("Entry Battles", "20 battles"),
            exercise("Whistle Breakouts After Wrestling", "20 breakouts"),
            exercise("Center-Defense Battles", "20 battles"),
            exercise("Continuous Wrestling Rounds", "10 x 1 minute"),
        ],
    ),
    session(
        name="Fencing Hand-Fighting Session",
        category="Fencing",
        training_type="contact_technical",
        participants="2+ people",
        focus="esgrima, hand fighting, lane denial, and recoveries",
        exercises=[
            exercise("Hand Fighting", "10 x 30 seconds"),
            exercise("Ball Fencing", "10 x 30 seconds"),
            exercise("Reach Battles", "50 battles"),
            exercise("Wrist-Control Battles", "50 battles"),
            exercise("Passing-Lane Denial", "40 drills"),
            exercise("Offensive Hand-Fighting", "40 drills"),
            exercise("Defensive Hand-Fighting", "40 drills"),
            exercise("Recover-And-Pass", "30 repetitions"),
            exercise("Recover-And-Shoot", "30 repetitions"),
            exercise("Live Perimeter Fencing", "20 drills"),
            exercise("Center-Entry Fencing", "20 drills"),
            exercise("Continuous Fencing Games", "10 x 2 minutes"),
        ],
    ),
    session(
        name="Counterattack Team Session",
        category="Counterattack",
        training_type="tactical_conditioning",
        participants="2+ people",
        focus="transition speed, numbers-up attack, and defensive recovery",
        exercises=[
            exercise("3v2 Fast Break", "20 repetitions"),
            exercise("4v3 Fast Break", "15 repetitions"),
            exercise("6v5 Transition", "15 repetitions"),
            exercise("Full-Pool Counterattack", "20 repetitions"),
            exercise("Goalkeeper Outlet To Finish", "20 repetitions"),
            exercise("Defensive Recovery Sprint", "20 repetitions"),
            exercise("Three-Wave Counterattack", "15 repetitions"),
            exercise("Continuous Transition Game", "15 minutes"),
            exercise("Steal Then Counter", "20 repetitions"),
            exercise("Counterattack After Blocked Shot", "20 repetitions"),
            exercise("Counterattack After Exclusion", "20 repetitions"),
            exercise("Timed Transition Possessions", "20 x 30 seconds"),
        ],
    ),
    session(
        name="Extra Man 6v5 Session",
        category="Extra Man",
        training_type="tactical",
        participants="2+ people",
        focus="6v5 extra-man offense and recovery",
        exercises=[
            exercise("Standard 6v5 Possessions", "40 possessions"),
            exercise("Quick-Release Possessions", "40 possessions"),
            exercise("Cross-Pass Finishes", "40 finishes"),
            exercise("Inside-Feed Finishes", "40 finishes"),
            exercise("Weak-Side Finishes", "40 finishes"),
            exercise("Skip-Pass Finishes", "40 finishes"),
            exercise("Five-Second Shot-Clock Possessions", "30 possessions"),
            exercise("Rotating Perimeter Possessions", "30 possessions"),
            exercise("Double-Post Possessions", "30 possessions"),
            exercise("Fake-Then-Shoot Possessions", "30 possessions"),
            exercise("Recovery After Turnover", "30 repetitions"),
            exercise("Live 6v5 vs 5v6", "20 possessions"),
        ],
    ),
    session(
        name="Tactical Match Session",
        category="Tactical Match",
        training_type="match_simulation",
        participants="2+ people",
        focus="scrimmage constraints, tactical scenarios, and official match simulation",
        exercises=[
            exercise("Full 6v6 Scrimmage", "20 minutes"),
            exercise("Press-Defense Scrimmage", "15 minutes"),
            exercise("Zone-Defense Scrimmage", "15 minutes"),
            exercise("Counterattack-Only Scrimmage", "15 minutes"),
            exercise("Center-Focused Offense", "15 minutes"),
            exercise("Extra-Man Focused Game", "15 minutes"),
            exercise("Shot-Clock Game", "10 minutes", "Use a 20-second clock."),
            exercise("No-Foul Scrimmage", "10 minutes"),
            exercise("One-Pass Maximum Game", "10 minutes"),
            exercise("Exclusion Simulation Game", "10 minutes"),
            exercise("Final-Minute Scenario Practice", "10 minutes"),
            exercise("Official Match Simulation", "30 minutes"),
        ],
    ),
    session(
        name="Resistance Training",
        category="Resistance Training",
        training_type="strength_conditioning",
        participants="2+ people",
        focus="weighted ball, elastic, resisted swimming, and contact conditioning",
        exercises=[
            exercise("Weighted-Ball Partner Passes", "100 passes"),
            exercise("Weighted-Ball Shots", "50 shots"),
            exercise("Resistance Belt Swim", "8 x 25m"),
            exercise("Resisted Eggbeater Jumps", "50 jumps", "Partner provides downward resistance with an elastic band."),
            exercise("Resisted Sprints", "6 x 20m", "Partner holds a resistance cord."),
            exercise("Elastic Resisted One-Hand Passes", "60 passes", "Elastic band attached to the throwing arm."),
            exercise("Goalkeeper Resisted Vertical Jumps", "40 jumps"),
            exercise("Resisted Center-Forward Turns", "30 turns", "Defender applies constant body pressure."),
            exercise("Parachute Or Drag Bucket Swim", "6 x 50m + 25m sprint", "Release drag and immediately sprint 25m free."),
            exercise("Resistance Wrestling To Catch-And-Shoot", "40 repetitions", "Perform catch-and-shoot immediately after 20 seconds of partner resistance wrestling."),
            exercise("Resisted Ball-Protection", "10 x 30 seconds", "Defender attempts to strip the ball continuously."),
            exercise("Resistance Finisher", "8 rounds", "20 seconds resisted swimming, 20 seconds wrestling, 20 seconds max-speed counterattack sprint."),
        ],
    ),
]


def get_sessions() -> List[Dict[str, Any]]:
    """Return every water polo session in the catalog."""
    return WATER_POLO_SESSIONS


def get_workouts() -> List[Dict[str, Any]]:
    """Backward-compatible alias for get_sessions."""
    return get_sessions()


def get_sessions_by_category(category: str) -> List[Dict[str, Any]]:
    """Return all sessions matching a category."""
    target = category.lower()
    return [s for s in WATER_POLO_SESSIONS if s.get("category", "").lower() == target]


def get_sessions_by_participants(participants: str) -> List[Dict[str, Any]]:
    """Return sessions matching a participant mode such as 'alone' or '2+ people'."""
    target = participants.lower()
    return [s for s in WATER_POLO_SESSIONS if s.get("participants", "").lower() == target]


def get_sessions_by_role(role: str) -> List[Dict[str, Any]]:
    """Return role-specific sessions."""
    target = role.lower().replace(" ", "_")
    return [s for s in WATER_POLO_SESSIONS if s.get("role", "").lower() == target]


def get_session_names() -> List[str]:
    """Return only the session names."""
    return [s["name"] for s in WATER_POLO_SESSIONS]


__all__ = [
    "SPORT",
    "SPORT_NAME",
    "WATER_POLO_SESSIONS",
    "exercise",
    "session",
    "get_sessions",
    "get_workouts",
    "get_sessions_by_category",
    "get_sessions_by_participants",
    "get_sessions_by_role",
    "get_session_names",
]
