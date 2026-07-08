"""Table tennis training catalog for Sportze.AI.

This module contains table tennis workouts and exercises codified from the
Sportze.AI training catalog. The structure is import-safe and intentionally
simple so it can be consumed by the catalog manager without side effects.
"""

from __future__ import annotations

from typing import Any, Dict, List

SPORT = "table_tennis"
SPORT_NAME = "Table Tennis"


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
    return data


TABLE_TENNIS_SESSIONS: List[Dict[str, Any]] = [
    session(
        name="Learn How To Play - Training Alone",
        category="Learn How To Play",
        level="learn",
        training_type="technical",
        participants="alone",
        focus="basic solo control, wall hitting, serving, and footwork",
        exercises=[
            exercise("Forehand Counter Hits", "150 consecutive hits", "Stand 2 meters from a wall and hit forehands while keeping the ball below shoulder height."),
            exercise("Backhand Counter Hits", "150 consecutive hits", "Hit backhands against a wall without changing grip."),
            exercise("Forehand Shadow Swings", "100 reps", "Finish with the racket at eyebrow height."),
            exercise("Backhand Shadow Swings", "100 reps", "Maintain a bent-knee ready position."),
            exercise("Ready Position Footwork", "3 minutes continuously", "Move center mark to forehand corner and back, then backhand corner and back."),
            exercise("Ball Bounce Control", "300 bounces", "Bounce the ball on the forehand side of the racket without dropping it."),
            exercise("Alternate Side Bounces", "200 consecutive bounces", "Alternate forehand and backhand faces of the racket."),
            exercise("Serve Practice", "80 legal serves", "Serve into the opposite service box, aiming only to clear the net cleanly."),
            exercise("Target Forehand", "60 successful target hits", "Place three paper targets on a wall and hit each target 20 times with forehand drives."),
            exercise("Target Backhand", "60 successful target hits", "Use only backhand strokes against the same targets."),
            exercise("Split-Step Drill", "120 split steps", "Imagine an incoming ball before every movement."),
            exercise("Recovery Position", "80 imaginary rallies", "Shadow-play and return to the center after every stroke."),
        ],
    ),
    session(
        name="Learn How To Play - Hitting Partner",
        category="Learn How To Play",
        level="learn",
        training_type="technical",
        participants="with_partner",
        focus="basic partner rallies, serving, blocking, and controlled games",
        exercises=[
            exercise("Forehand-To-Forehand Rally", "100 consecutive shots"),
            exercise("Backhand-To-Backhand Rally", "100 consecutive shots"),
            exercise("Alternating Forehand Backhand Rally", "80 successful exchanges", "Alternate forehand and backhand every shot."),
            exercise("Forehand Feed And Return", "60 balls each before switching", "Player A feeds; Player B returns every ball with forehand drives."),
            exercise("Low Net Clearance Rally", "5 minutes", "Clear the net by less than 20 cm."),
            exercise("Legal Serve Practice", "60 serves each", "Partner catches every ball."),
            exercise("Short Serve To Long Push", "80 reps each before switching"),
            exercise("Forehand Attack Against Block", "50 balls", "One player blocks while the other attacks continuously."),
            exercise("Forehand Half-Table Rally", "8 minutes"),
            exercise("Backhand Half-Table Rally", "8 minutes"),
            exercise("Counter-Hit Game", "Games to 11", "Use only counter hits, no topspin."),
            exercise("Continuous Rally Challenge", "200 consecutive successful shots"),
        ],
    ),
    session(
        name="Beginner - Training Alone",
        category="Beginner",
        level="beginner",
        training_type="balanced",
        participants="alone",
        focus="beginner solo drives, serves, footwork, and topspin mechanics",
        exercises=[
            exercise("Forehand Drives", "80 balls", "Use a training robot or rebound board."),
            exercise("Backhand Drives", "80 balls", "Use a rebound board."),
            exercise("Forehand Floor Target Drives", "90 balls", "Aim to three floor targets placed 50 cm apart."),
            exercise("Alternating Shadow Swings", "150 reps", "Alternate forehand and backhand."),
            exercise("Short Serve Practice", "50 serves", "Serve short so the ball bounces twice on the opponent's side."),
            exercise("Long Fast Serve Practice", "50 serves", "Aim within 20 cm of the endline."),
            exercise("Forehand Footwork", "4 minutes", "Move between forehand and middle positions."),
            exercise("Backhand Footwork", "4 minutes", "Move between center and backhand corner."),
            exercise("Walking Racket Bounce", "5 laps around table"),
            exercise("Forehand Shadow Loops", "40 reps", "Use full body rotation."),
            exercise("Backhand Topspin Shadow Strokes", "40 reps"),
            exercise("Random Table Footwork", "10 minutes", "Move around the table without hitting a ball."),
        ],
    ),
    session(
        name="Beginner - Hitting Partner",
        category="Beginner",
        level="beginner",
        training_type="balanced",
        participants="with_partner",
        focus="beginner partner rally consistency, serves, loops, and games",
        exercises=[
            exercise("Forehand Rally", "150 consecutive balls"),
            exercise("Backhand Rally", "150 consecutive balls"),
            exercise("Alternating Forehand Backhand", "120 balls"),
            exercise("Forehand Loops Against Block", "60 balls", "Player A blocks while Player B loops."),
            exercise("Role Switch Forehand Loops", "60 balls", "Switch roles and repeat."),
            exercise("Serve Push Stop", "100 points", "Serve, receive with a push, then stop."),
            exercise("Long Serve Attack", "80 points", "Serve long; receiver attacks immediately."),
            exercise("Crosscourt Forehand Rally", "8 minutes"),
            exercise("Crosscourt Backhand Rally", "8 minutes"),
            exercise("Down-The-Line Forehand Rally", "5 minutes"),
            exercise("Down-The-Line Backhand Rally", "5 minutes"),
            exercise("Beginner Rally Games", "3 games to 11", "Focus on rallies longer than six shots."),
        ],
    ),
]


def _add_style_session(name: str, category: str, participants: str, focus: str, drills: List[tuple]) -> None:
    TABLE_TENNIS_SESSIONS.append(
        session(
            name=name,
            category=category,
            training_type="technical",
            participants=participants,
            focus=focus,
            exercises=[exercise(d[0], d[1], d[2] if len(d) > 2 else None) for d in drills],
        )
    )


_add_style_session("Forehand Attacker - Training Alone", "Forehand Attacker", "alone", "solo forehand topspin, footwork, third-ball attack, and power", [
    ("Robot Forehand Topspin", "120 strokes", "Use medium topspin feed."),
    ("Forehand Loop Shadow Swings", "80 reps", "Emphasize hip rotation."),
    ("Short Serve Third-Ball Shadow", "50 serves + shadow attacks", "Serve short backspin, then shadow the third-ball forehand attack."),
    ("Backhand-To-Forehand Shadow Attack", "60 reps", "Move from backhand corner to forehand corner and attack."),
    ("Deep Crosscourt Target Drives", "100 drives", "Aim at a 30 x 30 cm target."),
    ("Forehand Flick Shadow", "80 reps", "Attack an imaginary short ball."),
    ("Falkenberg Footwork", "6 minutes", "Without a ball."),
    ("Rebound Board Counter-Drives", "100 forehand counter-drives"),
    ("Step-Around Forehand Attacks", "50 attacks", "Attack after stepping around from the backhand corner."),
    ("Explosive Forehand Jump-Loop Shadows", "30 reps"),
])
_add_style_session("Forehand Attacker - Hitting Partner", "Forehand Attacker", "with_partner", "forehand looping, blocking pressure, third-ball attacks, and winners", [
    ("Forehand Loop Against Block", "80 consecutive attacks", None),
    ("Forehand Multiball", "120 attacks", "Partner feeds exclusively to forehand."),
    ("Short Serve Forehand Third Ball", "70 reps", "Serve short backspin; attack every long return."),
    ("Middle-Forehand Random Block", "80 balls", "Recover and attack every ball."),
    ("Forehand-Only Games", "Games to 11", None),
    ("Deep And Short Attack Recognition", "60 reps", "Attack every deep ball with topspin."),
    ("Crosscourt Forehand Loops", "6 minutes", None),
    ("Down-The-Line Forehand Loops", "6 minutes", None),
    ("Random Forehand Multiball", "150 balls", None),
    ("Forehand Winner Points", "Competitive points", "Every rally must be finished with a forehand winner."),
])
_add_style_session("Backhand Attacker - Training Alone", "Backhand Attacker", "alone", "solo backhand topspin, flicks, recovery, and punch blocks", [
    ("Rebound Board Backhand Topspin", "120 strokes", "Keep every ball below 20 cm above the net."),
    ("Backhand Topspin Shadow", "100 reps", "Use full elbow extension and recovery."),
    ("Drive-Topspin Alternation", "100 balls", "Alternate one backhand drive and one backhand topspin against robot."),
    ("Backhand Flick Shadow", "80 reps", "From an imaginary short serve."),
    ("Center-To-Backhand Attack Footwork", "80 reps", "Move laterally and attack every movement."),
    ("Crosscourt Target Backhand Drives", "100 drives", "Aim at a 30 x 30 cm target."),
    ("Short Serve Backhand Attack Recovery", "60 sequences", "Serve short backspin, recover, and shadow attack."),
    ("Step-Back Backhand Attacks", "50 attacks", "Step back half a meter and return to table."),
    ("Quick Backhand Punch Blocks", "120 blocks", "Use rebound board."),
    ("Explosive Backhand Topspin Shadows", "40 reps"),
])
_add_style_session("Backhand Attacker - Hitting Partner", "Backhand Attacker", "with_partner", "backhand topspin pressure, multiball, short-deep recognition, and attacking points", [
    ("Backhand Topspin Rally", "100 consecutive shots", None),
    ("Backhand Loops Against Block", "80 loops", None),
    ("Backhand Multiball", "150 attacks", "Partner feeds exclusively to backhand side."),
    ("Short Serve Backhand Attack", "80 reps", "Serve short, receive long to backhand, attack immediately."),
    ("Short-Deep Backhand Attack", "70 reps", "Attack every deep backhand ball."),
    ("Backhand-Only Games", "Games to 11", None),
    ("Crosscourt Backhand Loops", "8 minutes", None),
    ("Down-The-Line Backhand Attacks", "8 minutes", None),
    ("Random Block Recovery", "100 balls", "Partner blocks left and right while you recover and attack."),
    ("Backhand-Initiation Points", "Competitive points", "Every attack must begin with backhand topspin."),
])
_add_style_session("Two-Winged Looper - Training Alone", "Two-Winged Looper", "alone", "balanced forehand/backhand looping, Falkenberg footwork, and alternating attacks", [
    ("Alternating Shadow Loops", "120 reps", None),
    ("Falkenberg Footwork", "8 minutes", "Without a ball."),
    ("Alternating Rebound Drives", "150 drives", "Alternate forehand and backhand."),
    ("Step-Around To Backhand Recovery", "60 sequences", None),
    ("Alternating Topspin Shadows", "80 reps", None),
    ("Robot Alternating Topspins", "100 balls", None),
    ("Serve Recovery Alternating Attack", "60 sequences", None),
    ("Side-To-Side Footwork", "5 minutes", "One shadow stroke at every stop."),
    ("Moving Alternating Counter-Drives", "80 drives", None),
    ("Explosive Alternating Attack Shadows", "50 reps", None),
])
_add_style_session("Two-Winged Looper - Hitting Partner", "Two-Winged Looper", "with_partner", "two-wing topspin continuity, random placement, and offensive pressure", [
    ("Alternating Topspin Rally", "120 consecutive shots", None),
    ("Random Corner Attack", "100 reps", "Partner blocks randomly between both corners."),
    ("Falkenberg Drill", "8 minutes", None),
    ("Random Two-Wing Multiball", "180 attacks", None),
    ("Serve Receive Attack Rally", "80 points", None),
    ("Crosscourt Forehand-Backhand Sequence", "6 minutes", None),
    ("Placement Change Topspin Pressure", "100 balls", None),
    ("Two-Wing Requirement Points", "Competitive points", "Every rally must include at least one forehand and one backhand topspin."),
    ("Deep And Short Attacks", "70 reps", None),
    ("Topspin Pressure Games", "3 games", None),
])
_add_style_session("Defensive Chopper - Training Alone", "Defensive Chopper", "alone", "solo chop mechanics, defensive footwork, lobs, and counterattack transition", [
    ("Forehand Chop Shadows", "120 reps", None),
    ("Backhand Chop Shadows", "120 reps", None),
    ("Behind-Table Defensive Footwork", "8 minutes", "Move two meters behind the table."),
    ("Robot Topspin Chop Returns", "150 returns", None),
    ("Alternating Chops", "100 reps", None),
    ("Chop-To-Counterattack Transition", "80 shadow transitions", None),
    ("Forehand Corner Recovery", "80 reps", "Recover from forehand corner to center after every chop."),
    ("High Defensive Lobs", "100 lobs", "Use rebound board."),
    ("Chop-Float Alternation", "80 shadow strokes", None),
    ("Explosive Forehand Counterattack Shadows", "40 reps", None),
])
_add_style_session("Defensive Chopper - Hitting Partner", "Defensive Chopper", "with_partner", "chopping against loops, defensive consistency, lobs, and counterattacks", [
    ("Continuous Chop Returns", "120 consecutive chops", "Partner loops continuously."),
    ("Alternating Forehand Backhand Chops", "100 returns", None),
    ("Random Attack Defense", "8 minutes", "Defend without attempting winners."),
    ("Fifth-Ball Counterattack", "50 sequences", "Counterattack every fifth ball after four chops."),
    ("Deep Defensive Lobs", "60 returns", None),
    ("Spin Adjustment Chops", "80 balls", "Partner alternates heavy topspin and flat attacks."),
    ("Defense-Only Game", "1 game", None),
    ("Fifth Return Attack Game", "1 game", None),
    ("Topspin Multiball Defense", "150 balls", None),
    ("Continuous Defense Challenge", "200 successful returns", None),
])
_add_style_session("All-Round Player - Training Alone", "All-Round Player", "alone", "complete solo technical balance across drives, loops, serve, push, and footwork", [
    ("Complete Stroke Volume", "200 total strokes", "50 forehand drives, 50 backhand drives, 50 forehand loops, 50 backhand loops."),
    ("Serve Variation Practice", "100 serves", "Use four different spin variations."),
    ("Multidirectional Footwork", "10 minutes", None),
    ("Block-Topspin Shadow Alternation", "120 reps", None),
    ("Push Practice", "120 pushes", "60 short pushes and 60 long pushes."),
    ("Alternating Rebound Counter-Drives", "120 drives", None),
    ("Flick Shadow Practice", "100 reps", "50 forehand flicks and 50 backhand flicks."),
    ("Recovery Movement Reps", "100 recoveries", "Recover after every shadow stroke."),
    ("Four-Corner Target Hitting", "80 successful shots", None),
    ("Random Shadow Play", "5 minutes", None),
])
_add_style_session("All-Round Player - Hitting Partner", "All-Round Player", "with_partner", "complete partner play with topspin, blocks, short game, placement, and match play", [
    ("Topspin-Block Alternation", "100 rallies", None),
    ("Serve Push Topspin Rally", "80 reps", None),
    ("Placement Change Rally", "Controlled rallies", "Change placement every third shot."),
    ("Short Game Practice", "10 minutes", None),
    ("Long Game Practice", "10 minutes", None),
    ("Random Ball Stroke Selection", "120 balls", None),
    ("Placement Game", "1 game", "Emphasize placement over power."),
    ("Spin Variation Game", "1 game", None),
    ("Consistency Game", "1 game", "Aim for rallies over 15 shots."),
    ("Competitive Match Finish", "3 complete games", None),
])
_add_style_session("Serve And Receive Specialist - Training Alone", "Serve & Receive Specialist", "alone", "serve variation, target serving, and receive shadow technique", [
    ("Short Backspin Serves", "100 serves", "Ball should bounce twice on the opposite side."),
    ("Long Topspin Serves", "100 serves", "Aim to both corners."),
    ("Wide Forehand Sidespin Serves", "60 serves", None),
    ("Wide Backhand Sidespin Serves", "60 serves", None),
    ("Four-Serve Alternation", "120 total serves", None),
    ("Disguised Spin Serves", "80 serves", "Use identical motion while changing spin."),
    ("Forehand Receive Flick Shadows", "80 reps", None),
    ("Backhand Banana Flick Shadows", "80 reps", None),
    ("Short Push Receive Shadows", "80 reps", None),
    ("Six-Zone Target Serving", "120 successful serves", "Hit each of six target zones 20 times."),
])
_add_style_session("Serve And Receive Specialist - Hitting Partner", "Serve & Receive Specialist", "with_partner", "serve patterns, receiving spin, third-ball and fourth-ball development", [
    ("Short Serve Push Return", "100 reps", None),
    ("Long Serve Attack Block", "80 rallies", None),
    ("Short Serve Push Receive", "100 receives", "Use only pushes."),
    ("Forehand Flick Receive", "80 receives", None),
    ("Backhand Banana Flick Receive", "80 receives", None),
    ("Random Serve Spin Reading", "100 serves", "Identify and return changing spin."),
    ("Third-Ball Attack", "80 reps", None),
    ("Fourth-Ball Counterattack", "80 reps", None),
    ("Predetermined Serve Pattern Games", "Games to 11", None),
    ("Serve Receive Match", "1 full match", "Emphasize serve variation and receive quality."),
])

# Doubles sessions.
_add_style_session("Doubles Rotation And Positioning - Just Me", "Doubles Rotation & Positioning", "alone", "solo doubles footwork, rotation, and recovery", [
    ("Shadow Doubles Rotation", "120 cycles", None),
    ("Crossover Footwork", "100 reps", "Move around an imaginary partner."),
    ("Serve Rotate Recover", "80 sequences", None),
    ("Side-Step Recovery", "5 minutes", "Recover after every imaginary shot."),
    ("Continuous Doubles Footwork", "8 minutes", "Move around both corners."),
    ("Receive And Clear Space", "80 reps", "Shadow receiving while clearing space for partner."),
    ("Forehand Attack Rotation", "100 reps", None),
    ("Random Doubles Movement", "10 minutes", None),
])
_add_style_session("Doubles Rotation And Positioning - Pair", "Doubles Rotation & Positioning", "pair", "two-player doubles rotation and movement timing", [
    ("Alternate Hit Rotation", "100 rallies", None),
    ("Serve And Rotate", "60 points", None),
    ("Forehand Doubles Rally", "8 minutes", None),
    ("Position Switch After Attack", "80 reps", None),
    ("Receive Formations", "60 points", None),
    ("Half-Table Doubles Rally", "10 minutes", None),
    ("Emergency Wide-Shot Recovery", "50 reps", None),
    ("Movement-Only Doubles Games", "Games to 11", None),
])
_add_style_session("Doubles Rotation And Positioning - Three Players", "Doubles Rotation & Positioning", "three_players", "three-player doubles rotations with fixed opponent or feeder", [
    ("Two-Vs-One Rotation", "Rotate every 10 points", "Two players form doubles team while one remains fixed as opponent."),
    ("Rotation With Feeder", "Continuous drill", "Third player feeds balls."),
    ("Serve Receive Rotating Substitute", "Rotate every 15 rallies", None),
    ("Controlled Half-Court Rotation", "Rotate after each point", None),
    ("Attacker Role Alternation", "Every five rallies", "Third player blocks."),
    ("Rotation Cycle Drill", "100 cycles", "Third player acts as consistent opponent."),
    ("Partner Movement Recovery", "60 reps", None),
    ("Timed Doubles Points", "Rotate resting player every 5 minutes", None),
])
_add_style_session("Doubles Rotation And Positioning - Four Players", "Doubles Rotation & Positioning", "four_players", "full doubles rotation, serve patterns, and match play", [
    ("Mandatory Rotation Rallies", "10 minutes", "Rotate after every shot."),
    ("Serve Third-Ball Partner Rotation", "80 points", None),
    ("Crosscourt-Only Doubles", "8 minutes", None),
    ("Attack Block Role Alternation", "Every game to 11", None),
    ("Receive Four Serve Placements", "80 points", None),
    ("Match-Opening Serve Sequences", "3 full games", None),
    ("Fast-Transition Doubles", "Competitive points", "Every point must include at least six shots."),
    ("Best-Of-Five Doubles Match", "1 match", None),
])

_add_style_session("Doubles Attack Combination - Just Me", "Doubles Attack Combination", "alone", "solo offensive doubles rotation and finishing patterns", [
    ("Third-Ball Attack Rotation Shadow", "100 cycles", None),
    ("Fifth-Ball Attack Recovery Shadow", "80 cycles", None),
    ("Serve Attack Rotate Recover", "80 sequences", None),
    ("Coordinated Finish Footwork", "5 minutes", "Move as if creating space for a partner's winner."),
    ("Step-Around Attack Rotation", "80 reps", None),
    ("Offensive Communication Calls", "100 calls", "Call mine, yours, switch, and finish during shadow rallies."),
    ("Wide Ball Attack Recovery", "60 reps", None),
    ("Random Offensive Doubles Shadow", "10 minutes", None),
])
_add_style_session("Doubles Attack Combination - Pair", "Doubles Attack Combination", "pair", "paired third-ball attacks, fifth-ball attacks, and synchronized finishing", [
    ("Serve Third-Ball Attack", "80 points", "Server rotates, partner prepares to finish next ball."),
    ("Fifth-Ball Finishing Pattern", "70 points", None),
    ("Forehand Attack Rotation", "8 minutes", None),
    ("Backhand Open To Forehand Finish", "60 reps", None),
    ("Short Serve Long Receive Attack", "70 reps", None),
    ("Synchronized Attack Communication", "100 rallies", "Call attack direction before finishing."),
    ("Wide Attack Recovery And Finish", "50 reps", None),
    ("Attack-Only Doubles Games", "Games to 11", None),
])
_add_style_session("Doubles Attack Combination - Three Players", "Doubles Attack Combination", "three_players", "three-player doubles offensive patterns with rotating feeder/opponent", [
    ("Two-Attacker One-Blocker Rotation", "Rotate every 10 points", None),
    ("Third-Ball Attack Feed", "100 balls", "Feeder serves or feeds predictable third-ball attacks."),
    ("Fifth-Ball Attack Rotation", "80 rallies", None),
    ("Rotating Offensive Substitute", "Rotate every 15 rallies", None),
    ("One Feeder Two Attackers", "120 feeds", "Attackers coordinate finishing patterns."),
    ("Communication Cue Attacks", "60 reps", "Call who finishes before the attack."),
    ("Wide-To-Middle Attack Recovery", "60 reps", None),
    ("Timed Offensive Doubles Points", "Rotate every 5 minutes", None),
])
_add_style_session("Doubles Attack Combination - Four Players", "Doubles Attack Combination", "four_players", "full doubles offensive systems and competitive finishing", [
    ("Third-Ball Attack Games", "3 games", None),
    ("Fifth-Ball Attack Games", "3 games", None),
    ("Serve Attack Finish Pattern", "80 points", None),
    ("Crosscourt Attack Rotation", "8 minutes", None),
    ("Synchronized Forehand Finishing", "60 points", None),
    ("Offensive Communication Match", "1 game", "Point only counts when the pair communicates before attack."),
    ("Fast Offensive Transition Rally", "10 minutes", None),
    ("Best-Of-Five Attack Match", "1 match", None),
])

_add_style_session("Doubles Defense And Counterattack - Just Me", "Doubles Defense & Counterattack", "alone", "solo doubles defensive recovery, blocking, and transition footwork", [
    ("Shadow Defensive Recovery", "100 cycles", None),
    ("Wide Block Recovery Footwork", "80 reps", None),
    ("Transition Block To Counterattack", "80 shadow sequences", None),
    ("Partner-Clearance Defensive Movement", "5 minutes", None),
    ("Deep Defense Rotation", "8 minutes", None),
    ("Counterattack Opening Shadow", "80 reps", None),
    ("Emergency Recovery After Wide Ball", "60 reps", None),
    ("Random Defensive Doubles Movement", "10 minutes", None),
])
_add_style_session("Doubles Defense And Counterattack - Pair", "Doubles Defense & Counterattack", "pair", "paired blocking, counterattacking, and defensive rotation", [
    ("Alternating Blocks", "100 rallies", None),
    ("Block Counterattack Alternation", "80 rallies", None),
    ("One Blocks One Counterattacks", "8 minutes", "Switch roles halfway."),
    ("Wide Defense Recovery", "60 reps", None),
    ("Transition To Attack Pattern", "70 points", None),
    ("Defensive Communication", "100 rallies", "Call switch, block, counter, or recover."),
    ("Pressure Block Rally", "10 minutes", None),
    ("Defense-To-Counter Doubles Games", "Games to 11", None),
])
_add_style_session("Doubles Defense And Counterattack - Three Players", "Doubles Defense & Counterattack", "three_players", "one attacker versus rotating defensive pair and transition practice", [
    ("One Attacker Vs Defensive Pair", "Rotate every 10 points", None),
    ("Rotating Block Pair", "100 attacks defended", None),
    ("Counterattack Every Fourth Ball", "60 sequences", None),
    ("Defensive Pair Footwork Feed", "8 minutes", None),
    ("Rotating Defender Substitute", "Every 15 rallies", None),
    ("Pressure Defense With Feeder", "150 balls", None),
    ("Recovery After Partner Movement", "60 reps", None),
    ("Timed Defense Points", "Rotate every 5 minutes", None),
])
_add_style_session("Doubles Defense And Counterattack - Four Players", "Doubles Defense & Counterattack", "four_players", "full doubles defensive systems, counterattack transition, and match scenarios", [
    ("Full Defensive System Rally", "10 minutes", None),
    ("Block-To-Counterattack Points", "80 points", None),
    ("One Pair Attacks One Pair Defends", "3 games", "Switch roles every game."),
    ("Wide Attack Defensive Recovery", "60 points", None),
    ("Counterattack Transition Game", "1 game", "Point only counts after a successful block-to-counter transition."),
    ("Defensive Communication Match", "1 game", None),
    ("Fast Defensive Transition Rally", "10 minutes", None),
    ("Best-Of-Five Defensive Doubles Match", "1 match", None),
])


def get_sessions() -> List[Dict[str, Any]]:
    return TABLE_TENNIS_SESSIONS


def get_workouts() -> List[Dict[str, Any]]:
    return TABLE_TENNIS_SESSIONS


def get_table_tennis_sessions() -> List[Dict[str, Any]]:
    return TABLE_TENNIS_SESSIONS


def get_sessions_by_category(category: str) -> List[Dict[str, Any]]:
    return [s for s in TABLE_TENNIS_SESSIONS if s.get("category", "").lower() == category.lower()]


def get_sessions_by_participants(participants: str) -> List[Dict[str, Any]]:
    return [s for s in TABLE_TENNIS_SESSIONS if s.get("participants", "").lower() == participants.lower()]


TRAINING_SESSIONS = TABLE_TENNIS_SESSIONS
WORKOUTS = TABLE_TENNIS_SESSIONS
SESSIONS = TABLE_TENNIS_SESSIONS

__all__ = [
    "SPORT",
    "SPORT_NAME",
    "TABLE_TENNIS_SESSIONS",
    "TRAINING_SESSIONS",
    "WORKOUTS",
    "SESSIONS",
    "exercise",
    "session",
    "get_sessions",
    "get_workouts",
    "get_table_tennis_sessions",
    "get_sessions_by_category",
    "get_sessions_by_participants",
]
