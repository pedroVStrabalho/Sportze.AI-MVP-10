import random
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

import streamlit as st


@dataclass
class Exercise:
    name: str
    category: str
    prescription: str
    purpose: str
    equipment_tags: List[str] = field(default_factory=list)
    intensity_tags: List[str] = field(default_factory=list)


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
}


def build_future_api_payload(profile: Dict[str, str | int | List[str]]) -> Dict[str, object]:
    """
    Placeholder helper to keep the generator organized for future API integration.
    This is intentionally not used yet.
    """
    return {
        "athlete_profile": profile,
        "generator_version": "training_generator_v2_api_ready",
        "requested_output": {
            "format": "structured_training_session",
            "needs_reasoning": True,
            "needs_professional_tone": True,
            "needs_measurable_prescriptions": True,
        },
        "api_status": "not_connected_yet",
    }


# -----------------------------------------------------------------------------
# TRAINING LIBRARY
# -----------------------------------------------------------------------------
SPORT_LIBRARY: Dict[str, Dict[str, List[Exercise]]] = {
    "Soccer": {
        "Warm-Up": [
            Exercise("Jog + mobility flow", "Warm-Up", "6 minutes easy jog + 6 mobility reps each movement", "Raise body temperature and open hips/ankles.", ["Bodyweight", "Open space"]),
            Exercise("Dynamic activation", "Warm-Up", "2 rounds of 20m each: high knees, butt kicks, side shuffles", "Prepare sprint mechanics.", ["Open space"]),
        ],
        "Technical": [
            Exercise("First-touch passing circuit", "Technical", "4 rounds x 3 minutes, 45 seconds rest", "Improve control and passing rhythm.", ["Ball", "Open space"]),
            Exercise("Dribble slalom + exit sprint", "Technical", "6 reps x 20m, walk-back recovery", "Tight control under speed.", ["Ball", "Cones"]),
            Exercise("Crossing and finishing", "Technical", "5 reps each side + 10 finishes", "Wide delivery and box timing.", ["Ball", "Goal", "Field"]),
        ],
        "Physical": [
            Exercise("Acceleration sprints", "Physical", "8 reps x 15m, 40 seconds rest", "Explosive first steps.", ["Open space"]),
            Exercise("Repeated sprint block", "Physical", "2 sets of 6 x 20m, 20 seconds rest between reps, 2 minutes between sets", "Match-like repeatability.", ["Open space"]),
            Exercise("Split squats", "Physical", "3 sets x 8 reps each leg", "Single-leg strength.", ["Bodyweight", "Dumbbells"]),
        ],
        "Tactical": [
            Exercise("Small-sided game", "Tactical", "4 rounds x 4 minutes, 2 minutes rest", "Decision-making under pressure.", ["Ball", "Field"]),
            Exercise("Pressing shape rehearsal", "Tactical", "5 rounds x 2 minutes", "Team organization and triggers.", ["Ball", "Field"]),
        ],
        "Recovery": [
            Exercise("Breathing walk + stretch", "Recovery", "6 minutes walk + 30 seconds per stretch", "Downregulate and improve recovery.", ["Bodyweight"]),
        ],
    },
    "Basketball": {
        "Warm-Up": [
            Exercise("Court movement warm-up", "Warm-Up", "2 rounds of 4 minutes", "Prepare hips, calves, shoulders.", ["Court"]),
            Exercise("Ball-handling activation", "Warm-Up", "3 minutes continuous", "Wake up handle and coordination.", ["Ball"]),
        ],
        "Technical": [
            Exercise("Form shooting", "Technical", "25 made shots", "Shooting mechanics.", ["Ball", "Court"]),
            Exercise("Cone change-of-direction dribble", "Technical", "6 reps each side", "Ball control and footwork.", ["Ball", "Cones"]),
            Exercise("Pick-and-roll reads", "Technical", "4 rounds x 3 minutes", "Game reads.", ["Ball", "Court"]),
        ],
        "Physical": [
            Exercise("Countermovement jumps", "Physical", "4 sets x 5 reps", "Vertical power.", ["Bodyweight"]),
            Exercise("Defensive slide intervals", "Physical", "6 reps x 20 seconds, 40 seconds rest", "Lateral conditioning.", ["Court"]),
            Exercise("Push-ups", "Physical", "3 sets x 10-15 reps", "Upper-body strength.", ["Bodyweight"]),
        ],
        "Tactical": [Exercise("Advantage game", "Tactical", "5 rounds x 3 minutes", "Transition decisions.", ["Ball", "Court"])],
        "Recovery": [Exercise("Light mobility", "Recovery", "8 minutes", "Joint recovery.", ["Bodyweight"])],
    },
    "Tennis": {
        "Warm-Up": [
            Exercise("Mini tennis + mobility", "Warm-Up", "8 minutes total", "Feel and footwork.", ["Racket", "Ball", "Court"]),
            Exercise("Split-step reaction drill", "Warm-Up", "3 sets x 45 seconds", "Timing and readiness.", ["Court"]),
        ],
        "Technical": [
            Exercise("Crosscourt consistency", "Technical", "4 rounds x 4 minutes", "Rally tolerance.", ["Racket", "Ball", "Court"]),
            Exercise("Serve targets", "Technical", "30 first serves + 20 second serves", "Placement and confidence.", ["Racket", "Ball", "Court"]),
            Exercise("Approach + volley sequence", "Technical", "12 reps each side", "Net transition.", ["Racket", "Ball", "Court"]),
        ],
        "Physical": [
            Exercise("Lateral shuffle intervals", "Physical", "6 reps x 20 seconds, 40 seconds rest", "Court movement endurance.", ["Court"]),
            Exercise("Medicine ball rotations", "Physical", "3 sets x 10 reps each side", "Rotational power.", ["Medicine ball"]),
            Exercise("Reverse lunges", "Physical", "3 sets x 8 reps each leg", "Lower-body control.", ["Bodyweight", "Dumbbells"]),
        ],
        "Tactical": [Exercise("Pattern play", "Tactical", "5 rounds x 3 points per pattern", "Build point construction.", ["Racket", "Ball", "Court"])],
        "Recovery": [Exercise("Forearm/hip mobility", "Recovery", "6 minutes", "Reduce stiffness.", ["Bodyweight"])],
    },
    "Volleyball": {
        "Warm-Up": [
            Exercise("Dynamic court warm-up", "Warm-Up", "7 minutes", "General readiness.", ["Court"]),
            Exercise("Arm swing activation", "Warm-Up", "2 sets x 12 reps", "Shoulder prep.", ["Bands", "Bodyweight"]),
        ],
        "Technical": [
            Exercise("Serve receive reps", "Technical", "20 quality passes", "Platform control.", ["Ball", "Court"]),
            Exercise("Setting accuracy", "Technical", "4 rounds x 2 minutes", "Tempo and placement.", ["Ball", "Court"]),
            Exercise("Approach jump spikes", "Technical", "5 sets x 4 reps", "Timing and hitting mechanics.", ["Ball", "Court"]),
        ],
        "Physical": [
            Exercise("Block jumps", "Physical", "4 sets x 5 reps", "Explosive jumping.", ["Court"]),
            Exercise("Band external rotations", "Physical", "3 sets x 12 reps", "Shoulder integrity.", ["Bands"]),
            Exercise("Tempo squats", "Physical", "3 sets x 8 reps", "Leg strength.", ["Bodyweight", "Dumbbells", "Barbell"]),
        ],
        "Tactical": [Exercise("6v6 situational play", "Tactical", "4 rounds x 5 minutes", "Rotation and decision-making.", ["Ball", "Court"])],
        "Recovery": [Exercise("Shoulder and calf stretch", "Recovery", "6 minutes", "Restore range of motion.", ["Bodyweight"])],
    },
    "Water Polo": {
        "Warm-Up": [
            Exercise("Swim + eggbeater prep", "Warm-Up", "200m easy swim + 3 x 30 seconds eggbeater", "Pool readiness.", ["Pool"]),
            Exercise("Shoulder mobility", "Warm-Up", "2 sets x 10 reps", "Throwing prep.", ["Bodyweight", "Bands"]),
        ],
        "Technical": [
            Exercise("Passing on the move", "Technical", "4 rounds x 3 minutes", "Ball speed and accuracy.", ["Pool", "Ball"]),
            Exercise("Shooting corners", "Technical", "20 shots total", "Finishing.", ["Pool", "Ball", "Goal"]),
            Exercise("Center battle positioning", "Technical", "6 reps x 20 seconds", "Body position under contact.", ["Pool", "Ball"]),
        ],
        "Physical": [
            Exercise("Sprint swims", "Physical", "8 reps x 15m, 30 seconds rest", "Explosive swimming.", ["Pool"]),
            Exercise("Eggbeater hold", "Physical", "4 reps x 40 seconds", "Leg endurance.", ["Pool"]),
            Exercise("Pull-ups or band pulls", "Physical", "3 sets x 6-10 reps", "Upper-body strength.", ["Pull-up bar", "Bands"]),
        ],
        "Tactical": [Exercise("6-on-5 execution", "Tactical", "5 rounds x 90 seconds", "Special situation organization.", ["Pool", "Ball"])],
        "Recovery": [Exercise("Easy backstroke + stretch", "Recovery", "5 minutes swim + 5 minutes stretch", "Recovery.", ["Pool"])],
    },
    "Baseball": {
        "Warm-Up": [Exercise("Throwing prep warm-up", "Warm-Up", "8 minutes", "Arm and hip readiness.", ["Ball", "Open space"])],
        "Technical": [
            Exercise("Fielding fundamentals", "Technical", "4 rounds x 8 reps", "Clean glove work.", ["Ball", "Field"]),
            Exercise("Bat speed tee work", "Technical", "5 rounds x 6 swings", "Quality contact.", ["Bat", "Ball", "Field"]),
            Exercise("Long toss progression", "Technical", "10 minutes", "Throwing capacity.", ["Ball", "Field"]),
        ],
        "Physical": [
            Exercise("Rotational med-ball throws", "Physical", "3 sets x 8 reps each side", "Power transfer.", ["Medicine ball"]),
            Exercise("Broad jumps", "Physical", "4 sets x 4 reps", "Lower-body power.", ["Bodyweight"]),
            Exercise("Rear-foot elevated split squat", "Physical", "3 sets x 8 reps each leg", "Single-leg strength.", ["Bench", "Dumbbells"]),
        ],
        "Tactical": [Exercise("Situational defense", "Tactical", "4 rounds x 3 minutes", "Game IQ.", ["Field", "Ball"])],
        "Recovery": [Exercise("Posterior shoulder care", "Recovery", "6 minutes", "Arm recovery.", ["Bands", "Bodyweight"])],
    },
    "Running": {
        "Warm-Up": [Exercise("Run warm-up", "Warm-Up", "8 minutes easy + drills", "Prepare gait and tissue stiffness.", ["Open space"])],
        "Technical": [
            Exercise("Strides", "Technical", "6 reps x 80m", "Running form at speed.", ["Track", "Road", "Open space"]),
            Exercise("Hill mechanics", "Technical", "6 reps x 12 seconds", "Drive and posture.", ["Hill", "Open space"]),
        ],
        "Physical": [
            Exercise("Main aerobic set", "Physical", "20-45 minutes depending on level", "Aerobic development.", ["Track", "Road", "Trail"]),
            Exercise("Calf raises", "Physical", "3 sets x 15 reps", "Lower-leg resilience.", ["Bodyweight", "Dumbbells"]),
            Exercise("Dead bugs", "Physical", "3 sets x 10 reps each side", "Core stability.", ["Bodyweight"]),
        ],
        "Tactical": [Exercise("Pacing rehearsal", "Tactical", "3 rounds x 5 minutes", "Race awareness.", ["Track", "Road"])],
        "Recovery": [Exercise("Walk + mobility", "Recovery", "10 minutes", "Bring heart rate down.", ["Bodyweight"])],
    },
    "Gym": {
        "Warm-Up": [Exercise("Cardio primer + mobility", "Warm-Up", "6 minutes cardio + 6 reps per mobility drill", "General prep.", ["Cardio machine", "Bodyweight"])],
        "Technical": [Exercise("Movement pattern rehearsal", "Technical", "2 light sets per lift", "Safer lifting.", ["Barbell", "Dumbbells", "Machines"])],
        "Physical": [
            Exercise("Squat or leg press", "Physical", "4 sets x 6-10 reps", "Lower-body strength.", ["Barbell", "Machine"]),
            Exercise("Bench or push variation", "Physical", "4 sets x 6-10 reps", "Upper-body pushing.", ["Barbell", "Dumbbells", "Machine"]),
            Exercise("Row or pull variation", "Physical", "4 sets x 8-12 reps", "Upper-body pulling.", ["Barbell", "Dumbbells", "Machine"]),
            Exercise("Conditioning finisher", "Physical", "8-12 minutes", "Work capacity.", ["Cardio machine", "Bodyweight"]),
        ],
        "Tactical": [Exercise("Tempo control", "Tactical", "Apply 2-0-2 tempo on first 2 exercises", "Technique discipline.", ["Barbell", "Dumbbells", "Machine"])],
        "Recovery": [Exercise("Cooldown stretch", "Recovery", "6 minutes", "Recovery.", ["Bodyweight"])],
    },
    "Weightlifting": {
        "Warm-Up": [Exercise("Barbell prep sequence", "Warm-Up", "8 minutes", "Mobility and groove.", ["Barbell", "Open space"])],
        "Technical": [
            Exercise("Snatch technique", "Technical", "6 sets x 2 reps", "Bar path and speed.", ["Barbell"]),
            Exercise("Clean and jerk technique", "Technical", "5 sets x 2 reps", "Coordination.", ["Barbell"]),
        ],
        "Physical": [
            Exercise("Front squat", "Physical", "4 sets x 3-5 reps", "Strength for receiving positions.", ["Barbell"]),
            Exercise("Pulls", "Physical", "4 sets x 3 reps", "Explosive extension.", ["Barbell"]),
            Exercise("Core holds", "Physical", "3 sets x 30-45 seconds", "Trunk stiffness.", ["Bodyweight"]),
        ],
        "Tactical": [Exercise("Attempt selection practice", "Tactical", "3 mock waves", "Meet strategy.", ["Barbell"])],
        "Recovery": [Exercise("Thoracic/ankle mobility", "Recovery", "8 minutes", "Position restoration.", ["Bodyweight"])],
    },
    "Rowing": {
        "Warm-Up": [Exercise("Erg + mobility prep", "Warm-Up", "5 minutes erg + 5 minutes mobility", "Stroke prep.", ["Rowing erg", "Bodyweight"])],
        "Technical": [
            Exercise("Pause drill", "Technical", "4 rounds x 3 minutes", "Sequencing.", ["Boat", "Erg"]),
            Exercise("Rate ladder", "Technical", "3 rounds x 4 minutes", "Control at different rates.", ["Boat", "Erg"]),
        ],
        "Physical": [
            Exercise("Main erg piece", "Physical", "3 x 8 minutes, 2 minutes rest", "Aerobic power.", ["Rowing erg"]),
            Exercise("Romanian deadlift", "Physical", "3 sets x 8 reps", "Posterior chain.", ["Barbell", "Dumbbells"]),
            Exercise("Plank", "Physical", "3 reps x 40 seconds", "Core endurance.", ["Bodyweight"]),
        ],
        "Tactical": [Exercise("Race rhythm simulation", "Tactical", "2 rounds x 6 minutes", "Pacing.", ["Boat", "Erg"])],
        "Recovery": [Exercise("Easy paddle or walk", "Recovery", "8 minutes", "Recovery.", ["Boat", "Bodyweight"])],
    },
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



def session_mix_for_type(session_type: str) -> Tuple[int, int, int]:
    if session_type == "Technical Priority":
        return (3, 2, 0)
    if session_type == "Physical Priority":
        return (2, 3, 0)
    if session_type == "Competition Week":
        return (2, 1, 1)
    return (2, 2, 1)



def adapt_session_for_equipment(session: List[Exercise], equipment_level: str, sport: str) -> List[Exercise]:
    """
    Current version keeps the core library intact while adding equipment-level notes.
    This makes the section ready for future API enhancement without changing core ideas.
    """
    normalized = normalize_equipment_level(equipment_level)

    if normalized in ["Competitive", "Elite"]:
        return session

    adjusted: List[Exercise] = []
    for ex in session:
        if normalized == "Minimal":
            if any(tag in ex.equipment_tags for tag in ["Barbell", "Machine", "Medicine ball", "Rowing erg", "Pool", "Boat"]):
                adjusted.append(
                    Exercise(
                        name=f"Adapted version of {ex.name}",
                        category=ex.category,
                        prescription=ex.prescription,
                        purpose=f"Low-equipment adaptation: {ex.purpose}",
                        equipment_tags=["Bodyweight", "Open space"],
                    )
                )
            else:
                adjusted.append(ex)
        elif normalized == "Basic":
            if any(tag in ex.equipment_tags for tag in ["Barbell", "Machine", "Boat"]):
                adjusted.append(
                    Exercise(
                        name=f"Basic setup adaptation - {ex.name}",
                        category=ex.category,
                        prescription=ex.prescription,
                        purpose=f"Adapted for a simpler training environment. {ex.purpose}",
                        equipment_tags=["Bodyweight", "Cones", "Bands", "Balls"],
                    )
                )
            else:
                adjusted.append(ex)
        else:
            adjusted.append(ex)

    # Keep the sport identity visible in adapted sessions.
    return adjusted



def build_session(sport: str, session_type: str, equipment_level: str) -> List[Exercise]:
    lib = SPORT_LIBRARY[sport]
    session: List[Exercise] = []
    session.extend(random.sample(lib["Warm-Up"], k=min(2, len(lib["Warm-Up"]))))

    technical_k, physical_k, tactical_k = session_mix_for_type(session_type)

    if technical_k > 0:
        session.extend(random.sample(lib["Technical"], k=min(technical_k, len(lib["Technical"]))))
    if physical_k > 0:
        session.extend(random.sample(lib["Physical"], k=min(physical_k, len(lib["Physical"]))))
    if tactical_k > 0:
        session.extend(random.sample(lib["Tactical"], k=min(tactical_k, len(lib["Tactical"]))))

    session.extend(random.sample(lib["Recovery"], k=min(1, len(lib["Recovery"]))))
    return adapt_session_for_equipment(session, equipment_level, sport)



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



def build_profile_summary(
    role: str,
    sport: str,
    position: str,
    goal: str,
    level: str,
    weekly_frequency: int,
    duration: int,
    session_type: str,
    equipment_level: str,
) -> Dict[str, object]:
    return {
        "role": role,
        "sport": sport,
        "position": position,
        "goal": goal,
        "level": level,
        "weekly_frequency": weekly_frequency,
        "duration_minutes": duration,
        "session_type": session_type,
        "equipment_level": equipment_level,
    }



def render_equipment_level_box(equipment_level: str) -> None:
    info = get_equipment_guidance(equipment_level)
    st.info(
        f"**Equipment level: {info['label']}**\n\n"
        f"{info['description']}\n\n"
        f"Typical setup: {', '.join(info['includes'])}"
    )


# -----------------------------------------------------------------------------
# STREAMLIT SECTION
# -----------------------------------------------------------------------------
def render_training_generator_section() -> None:
    st.header("Training Generator")
    st.write(
        "Generate sessions with exercise names, exact reps, sets, and time prescriptions for every sport. "
        "This version is also structured to be ready for future API reasoning integration."
    )

    role = st.radio("Are you a player or coach?", ["Player", "Coach"], horizontal=True)

    c1, c2 = st.columns(2)
    with c1:
        sport = st.selectbox("Choose the sport", list(SPORT_POSITIONS.keys()))
        position = st.selectbox("Choose the position / profile", SPORT_POSITIONS[sport])
        goal = st.selectbox("Main goal", GOALS)
        level = st.selectbox("Current level", LEVELS)
    with c2:
        weekly_frequency = st.slider(get_frequency_prompt(goal, level), 1, 7, 4)
        session_type = st.selectbox("Session type", SESSION_TYPES)
        duration = st.slider("Session duration (minutes)", 30, 180, 75, step=5)
        equipment_level = st.selectbox(
            "Level of equipment available",
            EQUIPMENT_LEVELS,
            index=1,
            help="Choose the overall quality of the equipment and training environment available.",
        )

    render_equipment_level_box(equipment_level)

    notes = st.text_area(
        "Extra notes",
        placeholder="Examples: match in 3 days, shoulder fatigue, focus on speed, beginner team, small training space...",
    )

    st.caption(
        "API-ready foundation included: structured athlete profile, future payload builder, and cleaner generator logic. "
        "No API has been connected yet."
    )

    if st.button("Generate Training Session", type="primary", use_container_width=True):
        session = build_session(sport, session_type, equipment_level)
        profile_summary = build_profile_summary(
            role=role,
            sport=sport,
            position=position,
            goal=goal,
            level=level,
            weekly_frequency=weekly_frequency,
            duration=duration,
            session_type=session_type,
            equipment_level=equipment_level,
        )
        future_payload = build_future_api_payload(profile_summary)

        st.subheader(f"{sport} Session Plan")
        st.write(
            f"**Profile:** {role} | **Position:** {position} | **Goal:** {goal} | **Level:** {level} | "
            f"**Weekly frequency:** {weekly_frequency} | **Duration target:** {duration} minutes"
        )
        st.caption(f"Equipment level selected: {equipment_level}")

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
                if ex.equipment_tags:
                    st.markdown(f"**Typical equipment for this drill:** {', '.join(ex.equipment_tags)}")

        st.subheader("Weekly structure suggestion")
        for item in weekly_focus(weekly_frequency, goal):
            st.write(f"- {item}")

        st.subheader("Professional coaching reminders")
        reminders = [
            "Progress intensity gradually across the week instead of stacking every hard stimulus together.",
            "Keep quality high: stop technical drills when execution clearly drops.",
            "Record key outputs like sprint times, shot quality, serve percentage, or RPE after the session.",
            "If pain appears and changes movement mechanics, reduce load and use the Physio section for a basic triage workflow.",
            "Use the equipment level as a realism filter: the session should feel professional but still possible in the athlete's environment.",
        ]
        if role == "Coach":
            reminders.append("For team sessions, adapt work:rest ratios so starters and reserves are both challenged appropriately.")
        for item in reminders:
            st.write(f"- {item}")

        with st.expander("Future API integration preview", expanded=False):
            st.json(future_payload)
            st.caption("This is only a preview of the structure prepared for future reasoning/API implementation.")
