
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
    "Home": "High-level athlete dashboard, quick guidance, workflow, and platform overview.",
    "Training Generator": "Build structured, professional training sessions with measurable prescriptions and sport-specific planning.",
    "Video Review": "Review movement, technique, and execution with a performance-oriented lens.",
    "Counseling": "Get direction on competition choices, pathway planning, and decision support.",
    "Physio": "Triage pain, manage risk, and get training-aware physical support guidance.",
}


def init_state() -> None:
    defaults = {
        "active_section": "Home",
        "selected_plan": "Pro",
        "athlete_name": "",
        "sport": "Tennis",
        "goal": "Improve performance",
        "level": "Advanced",
        "weekly_target": 4,
        "home_notes": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def section_button(label: str, current: str) -> None:
    button_type = "primary" if current == label else "secondary"
    if st.button(label, use_container_width=True, type=button_type):
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
        st.session_state.selected_plan = st.selectbox("Plan view", plans, index=plans.index(current_plan))

        st.markdown("### Active section")
        st.write(f"**{st.session_state.active_section}**")
        st.caption(SECTION_DESCRIPTIONS.get(st.session_state.active_section, ""))

        st.divider()

        st.markdown("### Navigation")
        for section in SECTIONS:
            if st.button(section, use_container_width=True, key=f"sidebar_{section}"):
                st.session_state.active_section = section

        st.divider()

        st.markdown("### Profile")
        st.write(f"Sport: {st.session_state.sport}")
        st.write(f"Goal: {st.session_state.goal}")
        st.write(f"Level: {st.session_state.level}")
        st.write(f"Weekly target: {st.session_state.weekly_target}")


def render_home() -> None:
    st.markdown("## Home")

    st.markdown("### Athlete Profile")

    sports = ["Soccer", "Basketball", "Tennis", "Volleyball", "Water Polo", "Baseball", "Running", "Gym", "Weightlifting", "Rowing"]
    goals = [
        "Improve performance",
        "Build fitness",
        "Return after a break",
        "Learn how to play",
        "Injury prevention",
        "Competition preparation",
    ]
    levels = ["Beginner", "Intermediate", "Advanced", "Elite"]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.session_state.athlete_name = st.text_input("Athlete / Team", value=st.session_state.athlete_name)
    with c2:
        st.session_state.sport = st.selectbox("Sport", sports)
    with c3:
        st.session_state.goal = st.selectbox("Goal", goals)
    with c4:
        st.session_state.level = st.selectbox("Level", levels)

    st.session_state.weekly_target = st.slider("Weekly training frequency", 1, 7, st.session_state.weekly_target)

    st.session_state.home_notes = st.text_area(
        "Planning notes",
        value=st.session_state.home_notes,
        height=80,
    )

    st.divider()

    st.markdown("### Modules")

    c1, c2 = st.columns(2)

    with c1:
        if st.button("Training Generator", use_container_width=True):
            st.session_state.active_section = "Training Generator"
        if st.button("Counseling", use_container_width=True):
            st.session_state.active_section = "Counseling"

    with c2:
        if st.button("Video Review", use_container_width=True):
            st.session_state.active_section = "Video Review"
        if st.button("Physio", use_container_width=True):
            st.session_state.active_section = "Physio"

    st.divider()

    st.markdown("### System Overview")
    st.write("This platform is designed to connect training, analysis, planning, and physical support in one system.")
    st.write("Each section works independently but contributes to the same performance workflow.")


def render_training_page() -> None:
    st.markdown("## Training Generator")
    render_training_generator_section()


def render_video_page() -> None:
    st.markdown("## Video Review")
    render_video_review_section()


def render_counseling_page() -> None:
    st.markdown("## Counseling")
    render_counseling_section()


def render_physio_page() -> None:
    st.markdown("## Physio")
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
