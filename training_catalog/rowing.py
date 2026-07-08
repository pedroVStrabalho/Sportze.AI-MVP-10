"""Rowing training catalog for Sportze.AI.

This module contains rowing workouts and exercises codified from the Sportze.AI
training catalog. The structure is intentionally simple and import-safe so it can
be consumed by the catalog manager without side effects.
"""

from __future__ import annotations

from typing import Dict, List, Any

SPORT = "rowing"
SPORT_NAME = "Rowing"


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


ROWING_SESSIONS: List[Dict[str, Any]] = [
    session(
        name="Learn How To Row",
        category="Learn How To Row",
        level="learn",
        training_type="technical",
        participants="alone",
        focus="rowing fundamentals",
        exercises=[
            exercise("Legs Body Arms Stroke Sequence", "50 strokes at 18 strokes/minute", "Sit on a rowing machine and focus only on the sequence: Legs → Body → Arms."),
            exercise("Slow Recovery Sequence", "5 sets x 20 stroke recoveries", "Move Arms → Body → Legs very slowly."),
            exercise("Horizontal Chain Row", "500 meters continuously", "Keep the chain perfectly horizontal."),
            exercise("Legs-Only Strokes", "30 strokes", "Use the rowing machine and isolate the leg drive."),
            exercise("Arms-Only Strokes", "30 strokes", "Use the rowing machine and isolate the arm pull."),
            exercise("Body-Swing-Only Strokes", "30 strokes", "Use the rowing machine and isolate body swing."),
            exercise("Light Technical Intervals", "4 x 250 meters", "Row at light intensity."),
            exercise("Catch Position Hold", "5 x 20 seconds, 20 seconds rest", "Hold the catch position with control."),
            exercise("Finish Position Hold", "5 x 20 seconds, 20 seconds rest", "Hold the finish position with control."),
            exercise("Exact Rate Row", "100 strokes at exactly 20 strokes/minute"),
            exercise("First Continuous Row", "1000 meters continuously without stopping"),
            exercise("Smooth Rhythm Intervals", "3 x 500 meters", "Focus on smooth rhythm."),
        ],
    ),
    session(
        name="Beginner Rowing",
        category="Beginner",
        level="beginner",
        training_type="balanced",
        participants="alone",
        focus="beginner rowing fitness and technique",
        exercises=[
            exercise("Continuous Beginner Row", "2000 meters continuously"),
            exercise("Short Interval Row", "6 x 250 meters, 1-minute rest"),
            exercise("Rate Control Row", "100 strokes at 22 strokes/minute"),
            exercise("High Leg Drive Intervals", "5 x 1 minute"),
            exercise("Medium Interval Row", "4 x 500 meters"),
            exercise("Leg Drive Emphasis", "50 strokes", "Emphasize leg drive only."),
            exercise("Consistent Split Row", "1500 meters", "Maintain consistent split times."),
            exercise("Rowing Sprints", "10 x 30 seconds"),
            exercise("Steady Beginner Row", "3000 meters at steady pace"),
            exercise("Longer Intervals", "4 x 750 meters"),
            exercise("Maximum Precision Row", "500 meters", "Use maximum technical precision."),
            exercise("Consecutive Stroke Challenge", "200 consecutive strokes without interruption"),
        ],
    ),
    session(
        name="Sculling Technical Session",
        category="Sculling",
        training_type="technical",
        participants="alone",
        focus="sculling balance and handle control",
        exercises=[
            exercise("Equal Handle Pressure Row", "3000 meters", "Maintain equal pressure on both handles."),
            exercise("Technical Sculling Intervals", "8 x 250 meters"),
            exercise("Level Hands Recovery", "100 strokes", "Keep hands level throughout recovery."),
            exercise("Balance-Focused Intervals", "5 x 500 meters"),
            exercise("Low-Rate Sculling Row", "2000 meters at 20 strokes/minute"),
            exercise("Power Start Repeats", "10 starts x 10 powerful strokes"),
            exercise("Identical Handle Height Row", "1500 meters", "Maintain identical handle heights."),
            exercise("Race-Pace Sculling Intervals", "4 x 750 meters"),
        ],
    ),
    session(
        name="Sprint Rowing Session",
        category="Sprint Rowing",
        training_type="intense",
        participants="alone",
        focus="sprint rowing speed",
        exercises=[
            exercise("Maximum 100m Sprints", "12 x 100 meters at maximum effort"),
            exercise("Race Pace 250s", "8 x 250 meters at race pace"),
            exercise("Explosive Race Starts", "10 starts x 15 explosive strokes"),
            exercise("High Effort 500s", "6 x 500 meters at 90% effort"),
            exercise("Thirty-Second Sprint Intervals", "20 x 30 seconds"),
            exercise("Competition Pace Row", "1000 meters at competition pace"),
            exercise("Race Effort 750s", "5 x 750 meters, 2-minute recovery"),
            exercise("High Stroke Rate Challenge", "200 strokes above 30 strokes/minute"),
        ],
    ),
    session(
        name="Endurance Rowing Session",
        category="Endurance Rowing",
        training_type="endurance",
        participants="alone",
        focus="aerobic rowing capacity",
        exercises=[
            exercise("Continuous 5K Row", "5000 meters continuously"),
            exercise("Continuous 8K Row", "8000 meters continuously"),
            exercise("Long Distance Intervals", "3 x 3000 meters"),
            exercise("Conversational 10K Row", "10,000 meters at conversational pace"),
            exercise("One-Hour Row", "60 minutes uninterrupted"),
            exercise("Long Repeats", "4 x 2500 meters"),
            exercise("Ninety-Minute Steady State", "90 minutes steady-state rowing"),
            exercise("Continuous 15K Row", "15,000 meters continuously"),
        ],
    ),
    session(
        name="Strength and Power Rowing Session",
        category="Strength & Power",
        training_type="physical",
        participants="alone",
        focus="rowing power and strength",
        exercises=[
            exercise("Maximal Power Strokes", "10 x 20 maximal-power strokes"),
            exercise("Maximum Leg Drive Intervals", "8 x 250 meters"),
            exercise("Power 500s", "5 x 500-meter power intervals"),
            exercise("Barbell Squats", "5 sets x 20 reps"),
            exercise("Romanian Deadlifts", "5 sets x 15 reps"),
            exercise("Walking Lunges", "5 sets x 20 reps per leg"),
            exercise("Bent-Over Rows", "5 sets x 15 reps"),
            exercise("Highest Watt 1000m", "1000 meters", "Maintain the highest possible watt output."),
        ],
    ),
    session(
        name="Double Scull 2x Session",
        category="Double Scull 2x",
        training_type="technical",
        participants="2 people",
        focus="double scull synchronization",
        exercises=[
            exercise("Timing Match Row", "3000 meters", "Match stroke timing exactly."),
            exercise("Synchronized 250s", "8 x 250-meter synchronized intervals"),
            exercise("Double Race Starts", "10 starts x 15 strokes"),
            exercise("Low Rate Double Row", "2000 meters at 22 strokes/minute"),
            exercise("Race Pace 500s", "6 x 500 meters at race pace"),
            exercise("Synchronized Stroke Challenge", "100 consecutive synchronized strokes"),
            exercise("Double 750s", "4 x 750-meter intervals"),
            exercise("Continuous Double Row", "5000 meters continuously"),
        ],
    ),
    session(
        name="Quad Scull 4x Session",
        category="Quad Scull 4x",
        training_type="technical",
        participants="4 people",
        focus="quad scull crew rhythm",
        exercises=[
            exercise("Crew Rhythm 5K", "5000 meters", "Maintain perfect crew rhythm."),
            exercise("Explosive Quad Starts", "10 starts x 10 explosive strokes"),
            exercise("Quad Race 250s", "8 x 250-meter race intervals"),
            exercise("Technical Quad Row", "3000 meters at technical pace"),
            exercise("Race Pace Quad 500s", "6 x 500 meters at race pace"),
            exercise("Synchronized Stroke Challenge", "200 synchronized strokes"),
            exercise("Quad 1000s", "4 x 1000 meters"),
            exercise("Continuous Quad Row", "6000 meters continuously"),
        ],
    ),
    session(
        name="Pair 2- Session",
        category="Pair 2-",
        training_type="technical",
        participants="2 people",
        focus="pair blade timing",
        exercises=[
            exercise("Blade Entry Timing Row", "3000 meters", "Match blade entry timing."),
            exercise("Pair 250s", "8 x 250-meter intervals"),
            exercise("Pair Race Starts", "10 starts x 15 strokes"),
            exercise("Pair Synchronization Challenge", "150 synchronized strokes"),
            exercise("Pair Race Efforts", "5 x 500 meters"),
            exercise("Low Rate Pair Row", "2000 meters at low stroke rate"),
            exercise("Pair 750s", "4 x 750 meters"),
            exercise("Continuous Pair Row", "5000 meters continuously"),
        ],
    ),
    session(
        name="Four 4- Session",
        category="Four 4-",
        training_type="balanced",
        participants="4 people",
        focus="sweep four synchronization",
        exercises=[
            exercise("Continuous Four Row", "6000 meters continuously"),
            exercise("Explosive Four Starts", "10 explosive starts"),
            exercise("Four 250s", "8 x 250-meter intervals"),
            exercise("Four Synchronization Challenge", "250 synchronized strokes"),
            exercise("Race Pace Four 500s", "6 x 500 meters at race pace"),
            exercise("Technical Four Row", "3000 meters technical rowing"),
            exercise("Four 1000s", "4 x 1000 meters"),
            exercise("Long Four Row", "7500 meters continuously"),
        ],
    ),
    session(
        name="Eight 8+ Session",
        category="Eight 8+",
        training_type="balanced",
        participants="8+ people",
        focus="eight crew rhythm and race preparation",
        exercises=[
            exercise("Continuous Eight Row", "8000 meters continuously"),
            exercise("Eight Race Starts", "10 starts x 20 strokes"),
            exercise("Eight Race 500s", "8 x 500-meter race intervals"),
            exercise("Eight Synchronization Challenge", "300 synchronized strokes"),
            exercise("Eight 1000s", "5 x 1000 meters"),
            exercise("Technical Eight Row", "4000 meters technical rowing"),
            exercise("Eight Race 750s", "6 x 750-meter race efforts"),
            exercise("Continuous 10K Eight Row", "10,000 meters continuously"),
        ],
    ),
    session(
        name="Coxswain Training Session",
        category="Coxswain Training",
        training_type="technical",
        participants="crew",
        focus="coxswain calls, steering, tactics, and feedback",
        exercises=[
            exercise("Stroke Rate Change Calls", "20-minute row", "Call stroke-rate changes every 30 seconds."),
            exercise("Buoy Turn Steering", "20 buoy turns"),
            exercise("Race Start Leadership", "Lead 10 race-start sequences"),
            exercise("Timing Error-Free Direction", "5000 meters", "Direct a crew without timing errors."),
            exercise("Tactical Move Calls", "8 x 250-meter intervals", "Call tactical moves during the intervals."),
            exercise("Full 2000m Race Simulation", "1 full 2000-meter race simulation"),
            exercise("Emergency Stop Procedures", "10 practice stops"),
            exercise("Endurance Row Feedback", "10,000 meters", "Continuously give technical feedback."),
        ],
    ),
    session(
        name="Crew Sprint Training Session",
        category="Crew Sprint Training",
        training_type="intense",
        participants="crew",
        focus="crew sprint speed and race pace",
        exercises=[
            exercise("All-Out Crew Sprints", "12 x 100 meters"),
            exercise("Crew Race Starts", "10 starts x 20 strokes"),
            exercise("Crew Race 250s", "8 x 250 meters at race pace"),
            exercise("High Effort Crew 500s", "6 x 500 meters at 95% effort"),
            exercise("Full Competition Pace 1000m", "1000 meters at full competition pace"),
            exercise("Crew Thirty-Second Sprints", "20 x 30-second sprint intervals"),
            exercise("Crew Race 750s", "5 x 750-meter race efforts"),
            exercise("Full 2000m Race Simulation", "1 complete 2000-meter race simulation"),
        ],
    ),
]

TRAINING_CATALOG = ROWING_SESSIONS
WORKOUTS = ROWING_SESSIONS


def get_sessions() -> List[Dict[str, Any]]:
    return ROWING_SESSIONS


def get_workouts() -> List[Dict[str, Any]]:
    return ROWING_SESSIONS


def get_sessions_by_category(category: str) -> List[Dict[str, Any]]:
    category_key = category.lower().strip()
    return [s for s in ROWING_SESSIONS if s.get("category", "").lower() == category_key]


def get_sessions_by_participants(participants: str) -> List[Dict[str, Any]]:
    participants_key = participants.lower().strip()
    return [s for s in ROWING_SESSIONS if s.get("participants", "").lower() == participants_key]


def get_alone_sessions() -> List[Dict[str, Any]]:
    return [s for s in ROWING_SESSIONS if s.get("participants") == "alone"]


def get_group_sessions() -> List[Dict[str, Any]]:
    return [s for s in ROWING_SESSIONS if s.get("participants") != "alone"]


def get_session_names() -> List[str]:
    return [s["name"] for s in ROWING_SESSIONS]


if __name__ == "__main__":
    total_exercises = sum(len(s["exercises"]) for s in ROWING_SESSIONS)
    print(f"{SPORT_NAME}: {len(ROWING_SESSIONS)} sessions, {total_exercises} exercises")
