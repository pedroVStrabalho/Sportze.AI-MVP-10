import random
from dataclasses import dataclass
from typing import Dict, List

import streamlit as st


@dataclass
class Exercise:
    name: str
    category: str
    prescription: str
    purpose: str


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

SPORT_LIBRARY: Dict[str, Dict[str, List[Exercise]]] = {
    "Soccer": {
        "Warm-Up": [
            Exercise("Jog + mobility flow", "Warm-Up", "6 minutes easy jog + 6 mobility reps each movement", "Raise body temperature and open hips/ankles."),
            Exercise("Dynamic activation", "Warm-Up", "2 rounds of 20m each: high knees, butt kicks, side shuffles", "Prepare sprint mechanics."),
        ],
        "Technical": [
            Exercise("First-touch passing circuit", "Technical", "4 rounds x 3 minutes, 45 seconds rest", "Improve control and passing rhythm."),
            Exercise("Dribble slalom + exit sprint", "Technical", "6 reps x 20m, walk-back recovery", "Tight control under speed."),
            Exercise("Crossing and finishing", "Technical", "5 reps each side + 10 finishes", "Wide delivery and box timing."),
        ],
        "Physical": [
            Exercise("Acceleration sprints", "Physical", "8 reps x 15m, 40 seconds rest", "Explosive first steps."),
            Exercise("Repeated sprint block", "Physical", "2 sets of 6 x 20m, 20 seconds rest between reps, 2 minutes between sets", "Match-like repeatability."),
            Exercise("Split squats", "Physical", "3 sets x 8 reps each leg", "Single-leg strength."),
        ],
        "Tactical": [
            Exercise("Small-sided game", "Tactical", "4 rounds x 4 minutes, 2 minutes rest", "Decision-making under pressure."),
            Exercise("Pressing shape rehearsal", "Tactical", "5 rounds x 2 minutes", "Team organization and triggers."),
        ],
        "Recovery": [
            Exercise("Breathing walk + stretch", "Recovery", "6 minutes walk + 30 seconds per stretch", "Downregulate and improve recovery."),
        ],
    },
    "Basketball": {
        "Warm-Up": [
            Exercise("Court movement warm-up", "Warm-Up", "2 rounds of 4 minutes", "Prepare hips, calves, shoulders."),
            Exercise("Ball-handling activation", "Warm-Up", "3 minutes continuous", "Wake up handle and coordination."),
        ],
        "Technical": [
            Exercise("Form shooting", "Technical", "25 made shots", "Shooting mechanics."),
            Exercise("Cone change-of-direction dribble", "Technical", "6 reps each side", "Ball control and footwork."),
            Exercise("Pick-and-roll reads", "Technical", "4 rounds x 3 minutes", "Game reads."),
        ],
        "Physical": [
            Exercise("Countermovement jumps", "Physical", "4 sets x 5 reps", "Vertical power."),
            Exercise("Defensive slide intervals", "Physical", "6 reps x 20 seconds, 40 seconds rest", "Lateral conditioning."),
            Exercise("Push-ups", "Physical", "3 sets x 10-15 reps", "Upper-body strength."),
        ],
        "Tactical": [
            Exercise("Advantage game", "Tactical", "5 rounds x 3 minutes", "Transition decisions."),
        ],
        "Recovery": [Exercise("Light mobility", "Recovery", "8 minutes", "Joint recovery.")],
    },
    "Tennis": {
        "Warm-Up": [
            Exercise("Mini tennis + mobility", "Warm-Up", "8 minutes total", "Feel and footwork."),
            Exercise("Split-step reaction drill", "Warm-Up", "3 sets x 45 seconds", "Timing and readiness."),
        ],
        "Technical": [
            Exercise("Crosscourt consistency", "Technical", "4 rounds x 4 minutes", "Rally tolerance."),
            Exercise("Serve targets", "Technical", "30 first serves + 20 second serves", "Placement and confidence."),
            Exercise("Approach + volley sequence", "Technical", "12 reps each side", "Net transition."),
        ],
        "Physical": [
            Exercise("Lateral shuffle intervals", "Physical", "6 reps x 20 seconds, 40 seconds rest", "Court movement endurance."),
            Exercise("Medicine ball rotations", "Physical", "3 sets x 10 reps each side", "Rotational power."),
            Exercise("Reverse lunges", "Physical", "3 sets x 8 reps each leg", "Lower-body control."),
        ],
        "Tactical": [Exercise("Pattern play", "Tactical", "5 rounds x 3 points per pattern", "Build point construction.")],
        "Recovery": [Exercise("Forearm/hip mobility", "Recovery", "6 minutes", "Reduce stiffness.")],
    },
    "Volleyball": {
        "Warm-Up": [
            Exercise("Dynamic court warm-up", "Warm-Up", "7 minutes", "General readiness."),
            Exercise("Arm swing activation", "Warm-Up", "2 sets x 12 reps", "Shoulder prep."),
        ],
        "Technical": [
            Exercise("Serve receive reps", "Technical", "20 quality passes", "Platform control."),
            Exercise("Setting accuracy", "Technical", "4 rounds x 2 minutes", "Tempo and placement."),
            Exercise("Approach jump spikes", "Technical", "5 sets x 4 reps", "Timing and hitting mechanics."),
        ],
        "Physical": [
            Exercise("Block jumps", "Physical", "4 sets x 5 reps", "Explosive jumping."),
            Exercise("Band external rotations", "Physical", "3 sets x 12 reps", "Shoulder integrity."),
            Exercise("Tempo squats", "Physical", "3 sets x 8 reps", "Leg strength."),
        ],
        "Tactical": [Exercise("6v6 situational play", "Tactical", "4 rounds x 5 minutes", "Rotation and decision-making.")],
        "Recovery": [Exercise("Shoulder and calf stretch", "Recovery", "6 minutes", "Restore range of motion.")],
    },
    "Water Polo": {
        "Warm-Up": [
            Exercise("Swim + eggbeater prep", "Warm-Up", "200m easy swim + 3 x 30 seconds eggbeater", "Pool readiness."),
            Exercise("Shoulder mobility", "Warm-Up", "2 sets x 10 reps", "Throwing prep."),
        ],
        "Technical": [
            Exercise("Passing on the move", "Technical", "4 rounds x 3 minutes", "Ball speed and accuracy."),
            Exercise("Shooting corners", "Technical", "20 shots total", "Finishing."),
            Exercise("Center battle positioning", "Technical", "6 reps x 20 seconds", "Body position under contact."),
        ],
        "Physical": [
            Exercise("Sprint swims", "Physical", "8 reps x 15m, 30 seconds rest", "Explosive swimming."),
            Exercise("Eggbeater hold", "Physical", "4 reps x 40 seconds", "Leg endurance."),
            Exercise("Pull-ups or band pulls", "Physical", "3 sets x 6-10 reps", "Upper-body strength."),
        ],
        "Tactical": [Exercise("6-on-5 execution", "Tactical", "5 rounds x 90 seconds", "Special situation organization.")],
        "Recovery": [Exercise("Easy backstroke + stretch", "Recovery", "5 minutes swim + 5 minutes stretch", "Recovery.")],
    },
    "Baseball": {
        "Warm-Up": [Exercise("Throwing prep warm-up", "Warm-Up", "8 minutes", "Arm and hip readiness.")],
        "Technical": [
            Exercise("Fielding fundamentals", "Technical", "4 rounds x 8 reps", "Clean glove work."),
            Exercise("Bat speed tee work", "Technical", "5 rounds x 6 swings", "Quality contact."),
            Exercise("Long toss progression", "Technical", "10 minutes", "Throwing capacity."),
        ],
        "Physical": [
            Exercise("Rotational med-ball throws", "Physical", "3 sets x 8 reps each side", "Power transfer."),
            Exercise("Broad jumps", "Physical", "4 sets x 4 reps", "Lower-body power."),
            Exercise("Rear-foot elevated split squat", "Physical", "3 sets x 8 reps each leg", "Single-leg strength."),
        ],
        "Tactical": [Exercise("Situational defense", "Tactical", "4 rounds x 3 minutes", "Game IQ.")],
        "Recovery": [Exercise("Posterior shoulder care", "Recovery", "6 minutes", "Arm recovery.")],
    },
    "Running": {
        "Warm-Up": [Exercise("Run warm-up", "Warm-Up", "8 minutes easy + drills", "Prepare gait and tissue stiffness.")],
        "Technical": [
            Exercise("Strides", "Technical", "6 reps x 80m", "Running form at speed."),
            Exercise("Hill mechanics", "Technical", "6 reps x 12 seconds", "Drive and posture."),
        ],
        "Physical": [
            Exercise("Main aerobic set", "Physical", "20-45 minutes depending on level", "Aerobic development."),
            Exercise("Calf raises", "Physical", "3 sets x 15 reps", "Lower-leg resilience."),
            Exercise("Dead bugs", "Physical", "3 sets x 10 reps each side", "Core stability."),
        ],
        "Tactical": [Exercise("Pacing rehearsal", "Tactical", "3 rounds x 5 minutes", "Race awareness.")],
        "Recovery": [Exercise("Walk + mobility", "Recovery", "10 minutes", "Bring heart rate down.")],
    },
    "Gym": {
        "Warm-Up": [Exercise("Cardio primer + mobility", "Warm-Up", "6 minutes cardio + 6 reps per mobility drill", "General prep.")],
        "Technical": [Exercise("Movement pattern rehearsal", "Technical", "2 light sets per lift", "Safer lifting.")],
        "Physical": [
            Exercise("Squat or leg press", "Physical", "4 sets x 6-10 reps", "Lower-body strength."),
            Exercise("Bench or push variation", "Physical", "4 sets x 6-10 reps", "Upper-body pushing."),
            Exercise("Row or pull variation", "Physical", "4 sets x 8-12 reps", "Upper-body pulling."),
            Exercise("Conditioning finisher", "Physical", "8-12 minutes", "Work capacity."),
        ],
        "Tactical": [Exercise("Tempo control", "Tactical", "Apply 2-0-2 tempo on first 2 exercises", "Technique discipline.")],
        "Recovery": [Exercise("Cooldown stretch", "Recovery", "6 minutes", "Recovery.")],
    },
    "Weightlifting": {
        "Warm-Up": [Exercise("Barbell prep sequence", "Warm-Up", "8 minutes", "Mobility and groove.")],
        "Technical": [
            Exercise("Snatch technique", "Technical", "6 sets x 2 reps", "Bar path and speed."),
            Exercise("Clean and jerk technique", "Technical", "5 sets x 2 reps", "Coordination."),
        ],
        "Physical": [
            Exercise("Front squat", "Physical", "4 sets x 3-5 reps", "Strength for receiving positions."),
            Exercise("Pulls", "Physical", "4 sets x 3 reps", "Explosive extension."),
            Exercise("Core holds", "Physical", "3 sets x 30-45 seconds", "Trunk stiffness."),
        ],
        "Tactical": [Exercise("Attempt selection practice", "Tactical", "3 mock waves", "Meet strategy.")],
        "Recovery": [Exercise("Thoracic/ankle mobility", "Recovery", "8 minutes", "Position restoration.")],
    },
    "Rowing": {
        "Warm-Up": [Exercise("Erg + mobility prep", "Warm-Up", "5 minutes erg + 5 minutes mobility", "Stroke prep.")],
        "Technical": [
            Exercise("Pause drill", "Technical", "4 rounds x 3 minutes", "Sequencing."),
            Exercise("Rate ladder", "Technical", "3 rounds x 4 minutes", "Control at different rates."),
        ],
        "Physical": [
            Exercise("Main erg piece", "Physical", "3 x 8 minutes, 2 minutes rest", "Aerobic power."),
            Exercise("Romanian deadlift", "Physical", "3 sets x 8 reps", "Posterior chain."),
            Exercise("Plank", "Physical", "3 reps x 40 seconds", "Core endurance."),
        ],
        "Tactical": [Exercise("Race rhythm simulation", "Tactical", "2 rounds x 6 minutes", "Pacing." )],
        "Recovery": [Exercise("Easy paddle or walk", "Recovery", "8 minutes", "Recovery.")],
    },
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


def get_frequency_prompt(goal: str, level: str) -> str:
    if goal == "Learn how to play" or level == "Beginner":
        return "How many times do you play sports per week?"
    return "How many times do you train this sport per week?"



def build_session(sport: str, session_type: str) -> List[Exercise]:
    lib = SPORT_LIBRARY[sport]
    session: List[Exercise] = []
    session.extend(random.sample(lib["Warm-Up"], k=min(2, len(lib["Warm-Up"]))))

    if session_type == "Technical Priority":
        session.extend(random.sample(lib["Technical"], k=min(3, len(lib["Technical"]))))
        session.extend(random.sample(lib["Physical"], k=min(2, len(lib["Physical"]))))
    elif session_type == "Physical Priority":
        session.extend(random.sample(lib["Physical"], k=min(3, len(lib["Physical"]))))
        session.extend(random.sample(lib["Technical"], k=min(2, len(lib["Technical"]))))
    elif session_type == "Competition Week":
        session.extend(random.sample(lib["Technical"], k=min(2, len(lib["Technical"]))))
        session.extend(random.sample(lib["Tactical"], k=min(1, len(lib["Tactical"]))))
        session.extend(random.sample(lib["Physical"], k=min(1, len(lib["Physical"]))))
    else:
        session.extend(random.sample(lib["Technical"], k=min(2, len(lib["Technical"]))))
        session.extend(random.sample(lib["Physical"], k=min(2, len(lib["Physical"]))))
        session.extend(random.sample(lib["Tactical"], k=min(1, len(lib["Tactical"]))))

    session.extend(random.sample(lib["Recovery"], k=min(1, len(lib["Recovery"]))))
    return session



def weekly_focus(days: int, goal: str) -> List[str]:
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
    return base[:max(1, min(days, 7))]



def render_training_generator_section() -> None:
    st.header("Training Generator")
    st.write("Generate sessions with exercise names, exact reps, sets, and time prescriptions for every sport.")

    role = st.radio("Are you a player or coach?", ["Player", "Coach"], horizontal=True)

    c1, c2 = st.columns(2)
    with c1:
        sport = st.selectbox("Choose the sport", list(SPORT_POSITIONS.keys()))
        position = st.selectbox("Choose the position / profile", SPORT_POSITIONS[sport])
        goal = st.selectbox("Main goal", GOALS)
        level = st.selectbox("Current level", LEVELS)
    with c2:
        weekly_frequency = st.slider(get_frequency_prompt(goal, level), 1, 14, 4)
        session_type = st.selectbox("Session type", SESSION_TYPES)
        duration = st.slider("Session duration (minutes)", 30, 180, 75, step=5)
        available_equipment = st.multiselect(
            "Available equipment",
            ["Cones", "Balls", "Resistance Bands", "Dumbbells", "Barbell", "Medicine Ball", "Pool", "Court", "Gym", "Rowing Erg"],
            default=["Cones", "Balls"] if sport in ["Soccer", "Basketball", "Tennis", "Volleyball", "Water Polo", "Baseball"] else ["Gym"],
        )

    notes = st.text_area(
        "Extra notes",
        placeholder="Examples: match in 3 days, shoulder fatigue, focus on speed, beginner team, small training space...",
    )

    if st.button("Generate Training Session", type="primary", use_container_width=True):
        session = build_session(sport, session_type)

        st.subheader(f"{sport} Session Plan")
        st.write(
            f"**Profile:** {role} | **Position:** {position} | **Goal:** {goal} | **Level:** {level} | "
            f"**Weekly frequency:** {weekly_frequency} | **Duration target:** {duration} minutes"
        )

        if available_equipment:
            st.caption("Available equipment: " + ", ".join(available_equipment))
        if notes.strip():
            st.info(f"Coach notes considered: {notes}")

        total_blocks = len(session)
        approx_block_minutes = max(4, duration // max(1, total_blocks))

        for idx, ex in enumerate(session, start=1):
            with st.expander(f"{idx}. {ex.name}", expanded=True if idx <= 3 else False):
                st.markdown(f"**Category:** {ex.category}")
                st.markdown(f"**Prescription:** {ex.prescription}")
                st.markdown(f"**Purpose:** {ex.purpose}")
                st.markdown(f"**Estimated block time:** ~{approx_block_minutes} minutes")

        st.subheader("Weekly structure suggestion")
        for item in weekly_focus(weekly_frequency, goal):
            st.write(f"- {item}")

        st.subheader("Professional coaching reminders")
        reminders = [
            "Progress intensity gradually across the week instead of stacking every hard stimulus together.",
            "Keep quality high: stop technical drills when execution clearly drops.",
            "Record key outputs like sprint times, shot quality, serve percentage, or RPE after the session.",
            "If pain appears and changes movement mechanics, reduce load and use the Physio section for a basic triage workflow.",
        ]
        if role == "Coach":
            reminders.append("For team sessions, adapt work:rest ratios so starters and reserves are both challenged appropriately.")
        for item in reminders:
            st.write(f"- {item}")
