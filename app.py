
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


SECTION_ICONS = {
    "Home",
    "Training Generator",
    "Video Review",
    "Counseling",
    "Physio" ,
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
        "last_generated_session_score": None,
        "home_notes": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def section_button(label: str, current: str) -> None:
    button_type = "primary" if current == label else "secondary"
    if st.button(f"{SECTION_ICONS.get(label, '')} {label}", use_container_width=True, type=button_type):
        st.session_state.active_section = label


def render_top_banner() -> None:
    st.title(APP_TITLE)
    st.caption(APP_SUBTITLE)
    st.write(APP_TAGLINE)


def render_platform_overview() -> None:
    st.markdown("### Platform overview")
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Core sections", "4")
        st.caption("Training, video, counseling, and physio")
    with c2:
        st.metric("App style", "Modular")
        st.caption("Each section can scale independently")
    with c3:
        st.metric("User level", st.session_state.level)
        st.caption("Current athlete profile reference")
    with c4:
        st.metric("Plan mode", st.session_state.selected_plan)
        st.caption("Pro-first structure for easier future limitations")

    st.info(
        "This upgraded app keeps the same main idea of Sportze.AI — a modular athlete platform — "
        "while improving structure, navigation, identity, and readiness for more elite workflows."
    )


def render_quick_profile_box() -> None:
    st.markdown("### Quick athlete profile")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.session_state.athlete_name = st.text_input("Athlete / team name", value=st.session_state.athlete_name, placeholder="Optional")
    with c2:
        st.session_state.sport = st.selectbox(
            "Main sport",
            ["Soccer", "Basketball", "Tennis", "Volleyball", "Water Polo", "Baseball", "Running", "Gym", "Weightlifting", "Rowing"],
            index=["Soccer", "Basketball", "Tennis", "Volleyball", "Water Polo", "Baseball", "Running", "Gym", "Weightlifting", "Rowing"].index(st.session_state.sport)
            if st.session_state.sport in ["Soccer", "Basketball", "Tennis", "Volleyball", "Water Polo", "Baseball", "Running", "Gym", "Weightlifting", "Rowing"]
            else 2,
        )
    with c3:
        st.session_state.goal = st.selectbox(
            "Main goal",
            [
                "Improve performance",
                "Build fitness",
                "Return after a break",
                "Learn how to play",
                "Injury prevention",
                "Competition preparation",
            ],
            index=[
                "Improve performance",
                "Build fitness",
                "Return after a break",
                "Learn how to play",
                "Injury prevention",
                "Competition preparation",
            ].index(st.session_state.goal)
            if st.session_state.goal in [
                "Improve performance",
                "Build fitness",
                "Return after a break",
                "Learn how to play",
                "Injury prevention",
                "Competition preparation",
            ]
            else 0,
        )
    with c4:
        st.session_state.level = st.selectbox(
            "Current level",
            ["Beginner", "Intermediate", "Advanced", "Elite"],
            index=["Beginner", "Intermediate", "Advanced", "Elite"].index(st.session_state.level)
            if st.session_state.level in ["Beginner", "Intermediate", "Advanced", "Elite"]
            else 2,
        )

    st.session_state.weekly_target = st.slider("Weekly training target", 1, 7, st.session_state.weekly_target)
    st.session_state.home_notes = st.text_area(
        "High-level planning notes",
        value=st.session_state.home_notes,
        placeholder="Examples: tournament next week, shoulder discomfort, wants speed emphasis, building a more elite routine...",
        height=90,
    )


def render_section_cards() -> None:
    st.markdown("### Main modules")
    c1, c2 = st.columns(2)

    with c1:
        with st.container():
            st.markdown("#### Training Generator")
            st.write("Generate pro-level sessions with better structure, progression logic, and more measurable prescriptions.")
            if st.button("Open Training Generator", use_container_width=True, key="open_training_home"):
                st.session_state.active_section = "Training Generator"

        with st.container():
            st.markdown("#### Counseling")
            st.write("Guide athlete decisions, pathway planning, tournament thinking, and strategic development choices.")
            if st.button("Open Counseling", use_container_width=True, key="open_counseling_home"):
                st.session_state.active_section = "Counseling"

    with c2:
        with st.container():
            st.markdown("#### Video Review")
            st.write("Review movement and technique with a more performance-oriented workflow.")
            if st.button("Open Video Review", use_container_width=True, key="open_video_home"):
                st.session_state.active_section = "Video Review"

        with st.container():
            st.markdown("#### Physio")
            st.write("Handle pain-related guidance, risk awareness, and support before problems get worse.")
            if st.button("Open Physio", use_container_width=True, key="open_physio_home"):
                st.session_state.active_section = "Physio"


def render_pro_plan_box() -> None:
    st.markdown("### Plan structure")
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("#### Free")
        st.write("- Limited generations")
        st.write("- Basic access")
        st.write("- Entry point for adoption")

    with c2:
        st.markdown("#### Plus")
        st.write("- Unlimited core generation")
        st.write("- Better access to physio")
        st.write("- Controlled video review access")

    with c3:
        st.markdown("#### Pro")
        st.write("- Full generation power")
        st.write("- Strongest workflow for serious athletes")
        st.write("- Best base for elite personalization")

    st.success(
        "This app version is built with a Pro-first mindset, so later it is easier to limit features for Free and Plus "
        "than to rebuild the high-end experience from scratch."
    )


def render_home_workflow() -> None:
    st.markdown("### Recommended workflow")
    workflow_steps = [
        "1. Use Training Generator to build the main session.",
        "2. Use Video Review to check movement, execution, or technique.",
        "3. Use Counseling for direction, planning, and competition-related support.",
        "4. Use Physio if pain, discomfort, or movement limitations appear.",
    ]
    for step in workflow_steps:
        st.write(f"- {step}")


def render_home_performance_panel() -> None:
    st.markdown("### Elite performance principles")
    principles = [
        "Professional training is not just harder — it is more precise.",
        "Different drills should carry different time and intensity demands.",
        "A strong system connects training, technique review, planning, and body management.",
        "Athletes improve faster when the program feels realistic for their actual environment.",
        "The platform should support both individual users and future organization dashboards.",
    ]
    for item in principles:
        st.write(f"- {item}")


def render_sidebar() -> None:
    with st.sidebar:
        st.markdown("## Sportze.AI Control Panel")
        st.session_state.selected_plan = st.selectbox("Plan view", ["Free", "Plus", "Pro"], index=["Free", "Plus", "Pro"].index(st.session_state.selected_plan))

        st.markdown("### Active section")
        st.write(f"**{SECTION_ICONS.get(st.session_state.active_section, '')} {st.session_state.active_section}**")
        st.caption(SECTION_DESCRIPTIONS.get(st.session_state.active_section, ""))

        st.divider()

        st.markdown("### Quick navigation")
        for section in SECTIONS:
            if st.button(f"Go to {section}", use_container_width=True, key=f"sidebar_{section}"):
                st.session_state.active_section = section

        st.divider()

        st.markdown("### Current profile snapshot")
        st.write(f"**Sport:** {st.session_state.sport}")
        st.write(f"**Goal:** {st.session_state.goal}")
        st.write(f"**Level:** {st.session_state.level}")
        st.write(f"**Weekly target:** {st.session_state.weekly_target}")

        st.divider()

        st.markdown("### Product direction")
        st.write("- Modular build")
        st.write("- Pro-first feature structure")
        st.write("- Ready to grow into organization dashboards")
        st.write("- Keeps separate files and avoids `st.set_page_config()` inside modules")


def render_section_header(section: str) -> None:
    st.markdown(f"## {SECTION_ICONS.get(section, '')} {section}")
    st.caption(SECTION_DESCRIPTIONS.get(section, ""))


def render_home() -> None:
    render_section_header("Home")
    render_platform_overview()
    st.divider()
    render_quick_profile_box()
    st.divider()
    render_section_cards()
    st.divider()

    left, right = st.columns([1.2, 1.0])
    with left:
        render_pro_plan_box()
    with right:
        render_home_workflow()

    st.divider()
    render_home_performance_panel()

    if st.session_state.athlete_name:
        st.info(
            f"Current profile loaded for **{st.session_state.athlete_name}** — "
            f"{st.session_state.sport}, {st.session_state.level}, goal: {st.session_state.goal.lower()}."
        )


def render_training_page() -> None:
    render_section_header("Training Generator")
    st.write(
        "This section is the main performance engine of Sportze.AI. "
        "It should feel professional, measurable, and realistic for serious athletes."
    )
    render_training_generator_section()


def render_video_page() -> None:
    render_section_header("Video Review")
    st.write(
        "Use this area to analyze technique, body positioning, execution quality, and movement patterns."
    )
    render_video_review_section()


def render_counseling_page() -> None:
    render_section_header("Counseling")
    st.write(
        "This section should guide decisions more intelligently, helping athletes choose better next steps and opportunities."
    )
    render_counseling_section()


def render_physio_page() -> None:
    render_section_header("Physio")
    st.write(
        "This section supports training-aware body management, pain triage, and risk-aware guidance."
    )
    render_physio_section()


def main() -> None:
    init_state()
    render_sidebar()
    render_top_banner()

    with st.container():
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
