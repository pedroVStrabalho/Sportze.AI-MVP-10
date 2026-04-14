import streamlit as st

from training_generator_section import render_training_generator_section
from video_review_section import render_video_review_section
from physio_section import render_physio_section
from counseling_section import render_counseling_section

APP_TITLE = "Sportze.AI"
APP_SUBTITLE = "Training Generator • Video Review • Counseling • Physio"
APP_TAGLINE = "Elite sports support, modular planning, and smarter athlete guidance."

SECTIONS = [
    "Home",
    "Training Generator",
    "Video Review",
    "Counseling",
    "Physio",
]

SECTION_DESCRIPTIONS = {
    "Home": "Athlete profile, platform workflow, and high-level planning.",
    "Training Generator": "Build structured, professional training sessions with measurable prescriptions and sport-specific planning.",
    "Video Review": "Review movement, technique, and execution with a performance-oriented lens.",
    "Counseling": "Get direction on competition choices, pathway planning, and decision support.",
    "Physio": "Triage pain, manage risk, and get training-aware physical support guidance.",
}

KNOWN_TEAM_SPORTS = {
    "soccer",
    "football",
    "basketball",
    "volleyball",
    "water polo",
    "baseball",
    "softball",
    "rugby",
    "handball",
    "futsal",
    "hockey",
    "lacrosse",
    "cricket",
    "american football",
}

KNOWN_INDIVIDUAL_SPORTS = {
    "tennis",
    "running",
    "athletics",
    "track",
    "swimming",
    "gym",
    "fitness",
    "weightlifting",
    "rowing",
    "boxing",
    "judo",
    "taekwondo",
    "karate",
    "wrestling",
    "golf",
    "surfing",
    "cycling",
    "triathlon",
    "badminton",
    "table tennis",
    "skateboarding",
}


def init_state() -> None:
    defaults = {
        "active_section": "Home",
        "selected_plan": "Pro",
        "sport": "",
        "sport_type": "",
        "team_name": "",
        "athlete_name": "",
        "goal": "Improve performance",
        "level": "Advanced",
        "is_professional": "No",
        "weekly_target": 4,
        "home_notes": "",
        "profile_email": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def normalize_sport_name(text: str) -> str:
    return " ".join(text.strip().lower().split())


def detect_sport_type(sport_text: str) -> str:
    sport = normalize_sport_name(sport_text)
    if not sport:
        return ""
    if sport in KNOWN_TEAM_SPORTS:
        return "Team Sport"
    if sport in KNOWN_INDIVIDUAL_SPORTS:
        return "Individual Sport"
    return ""


def section_button(label: str, current: str) -> None:
    button_type = "primary" if current == label else "secondary"
    button_key = f"topnav_{label.lower().replace(' ', '_')}"
    if st.button(label, use_container_width=True, type=button_type, key=button_key):
        st.session_state.active_section = label


def render_top_banner() -> None:
    st.title(APP_TITLE)
    st.caption(APP_SUBTITLE)
    st.write(APP_TAGLINE)


def render_sidebar() -> None:
    with st.sidebar:
        st.markdown("## Control Panel")

        plans = ["Free", "Plus", "Pro"]
        current_plan = st.session_state.selected_plan if st.session_state.selected_plan in plans else "Pro"
        st.session_state.selected_plan = st.selectbox("Plan view", plans, index=plans.index(current_plan), key="sidebar_plan_view")

        st.markdown("### Active section")
        st.write(f"**{st.session_state.active_section}**")
        st.caption(SECTION_DESCRIPTIONS.get(st.session_state.active_section, ""))

        st.divider()

        st.markdown("### Navigation")
        for section in SECTIONS:
            if st.button(section, use_container_width=True, key=f"sidebar_{section.lower().replace(' ', '_')}"):
                st.session_state.active_section = section

        st.divider()

        st.markdown("### Profile Snapshot")
        st.write(f"Sport: {st.session_state.sport or 'Not entered'}")
        st.write(f"Sport type: {st.session_state.sport_type or 'Not defined'}")
        if st.session_state.team_name:
            st.write(f"Team: {st.session_state.team_name}")
        st.write(f"Athlete: {st.session_state.athlete_name or 'Not entered'}")
        st.write(f"Goal: {st.session_state.goal}")
        st.write(f"Level: {st.session_state.level}")
        st.write(f"Weekly frequency: {st.session_state.weekly_target}")
        if st.session_state.level in ["Advanced", "Elite"]:
            st.write(f"Professional: {st.session_state.is_professional}")

        st.divider()

        st.markdown("### Product Structure")
        st.write("- Modular build")
        st.write("- Pro-first feature structure")
        st.write("- Ready for API expansion")
        st.write("- Future-ready for organization dashboards")


def render_home() -> None:
    st.markdown("## Home")

    st.markdown("### Modules")
    st.write("Choose a module first for quick access, or fill in the athlete profile below so the Training Generator can reuse your answers automatically.")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Training Generator", use_container_width=True, key="home_training_generator_button"):
            st.session_state.active_section = "Training Generator"
        if st.button("Counseling", use_container_width=True, key="home_counseling_button"):
            st.session_state.active_section = "Counseling"
    with c2:
        if st.button("Video Review", use_container_width=True, key="home_video_review_button"):
            st.session_state.active_section = "Video Review"
        if st.button("Physio", use_container_width=True, key="home_physio_button"):
            st.session_state.active_section = "Physio"

    st.divider()

    st.markdown("### Athlete Profile")

    goals = [
        "Improve performance",
        "Build fitness",
        "Return after a break",
        "Learn how to play",
        "Injury prevention",
        "Competition preparation",
    ]
    levels = ["Beginner", "Intermediate", "Advanced", "Elite"]

    st.session_state.sport = st.text_input(
        "What sport do you play?",
        value=st.session_state.sport,
        placeholder="Type any sport in the world",
        key="home_sport_input",
    )

    detected_type = detect_sport_type(st.session_state.sport)
    if detected_type:
        st.session_state.sport_type = detected_type
        st.caption(f"Detected sport type: {detected_type}")
    elif st.session_state.sport.strip():
        st.session_state.sport_type = st.radio(
            "Is this an individual sport or a team sport?",
            ["Individual Sport", "Team Sport"],
            horizontal=True,
            index=0 if st.session_state.sport_type != "Team Sport" else 1,
            key="home_sport_type_radio",
        )
    else:
        st.session_state.sport_type = ""

    if st.session_state.sport_type == "Team Sport":
        st.session_state.team_name = st.text_input(
            "What team do you play for?",
            value=st.session_state.team_name,
            placeholder="Type your club, school, academy, or team name",
            key="home_team_name_input",
        )
        st.session_state.athlete_name = st.text_input(
            "Athlete name",
            value=st.session_state.athlete_name,
            placeholder="Type the athlete name",
            key="home_athlete_name_team_input",
        )
    elif st.session_state.sport_type == "Individual Sport":
        st.session_state.team_name = ""
        st.session_state.athlete_name = st.text_input(
            "Your name",
            value=st.session_state.athlete_name,
            placeholder="Type your name",
            key="home_athlete_name_individual_input",
        )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.session_state.goal = st.selectbox(
            "Main goal",
            goals,
            index=goals.index(st.session_state.goal) if st.session_state.goal in goals else 0,
            key="home_goal_select",
        )
    with c2:
        st.session_state.level = st.selectbox(
            "Current level",
            levels,
            index=levels.index(st.session_state.level) if st.session_state.level in levels else 2,
            key="home_level_select",
        )
    with c3:
        frequency_label = (
            "How many times do you play sports per week?"
            if st.session_state.goal == "Learn how to play" or st.session_state.level == "Beginner"
            else "How many times do you train this sport per week?"
        )
        st.session_state.weekly_target = st.slider(
            frequency_label,
            1,
            7,
            st.session_state.weekly_target,
            key="home_weekly_target_slider",
        )

    if st.session_state.level in ["Advanced", "Elite"]:
        st.session_state.is_professional = st.radio(
            "Are you professional in this sport?",
            ["No", "Yes"],
            horizontal=True,
            index=1 if st.session_state.is_professional == "Yes" else 0,
            key="home_professional_radio",
        )
    else:
        st.session_state.is_professional = "No"

    st.session_state.home_notes = st.text_area(
        "Planning notes",
        value=st.session_state.home_notes,
        placeholder="Examples: tournament next week, shoulder discomfort, wants speed emphasis, building a more elite routine...",
        height=90,
        key="home_notes_textarea",
    )

    st.divider()

    st.markdown("### System Overview")
    st.write("This platform is designed to connect training, analysis, planning, and physical support in one system.")
    st.write("The athlete profile starts from the sport first, then adapts the next questions depending on whether the sport is individual or team-based.")
    st.write("If the athlete profile is filled in here, the Training Generator reuses those answers and does not repeat the same questions.")
    st.write("If the home profile is not filled in, the Training Generator will ask those questions normally.")


def render_training_page() -> None:
    render_training_generator_section()


def render_video_page() -> None:
    render_video_review_section()


def render_counseling_page() -> None:
    render_counseling_section()


def render_physio_page() -> None:
    render_physio_section()


def main() -> None:
    init_state()
    render_sidebar()
    render_top_banner()

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        section_button("Home", st.session_state.active_section)
    with c2:
        section_button("Training Generator", st.session_state.active_section)
    with c3:
        section_button("Video Review", st.session_state.active_section)
    with c4:
        section_button("Counseling", st.session_state.active_section)
    with c5:
        section_button("Physio", st.session_state.active_section)

    st.divider()

    section = st.session_state.active_section

    if section == "Home":
        render_home()
    elif section == "Training Generator":
        render_training_page()
    elif section == "Video Review":
        render_video_page()
    elif section == "Counseling":
        render_counseling_page()
    elif section == "Physio":
        render_physio_page()
    else:
        st.warning("Unknown section selected.")


if __name__ == "__main__":
    main()
