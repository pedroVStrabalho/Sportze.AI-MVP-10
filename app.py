import json
import re
from pathlib import Path
from typing import Any, Dict

import streamlit as st

from training_generator_section import render_training_generator_section
from video_review_section import render_video_review_section
from physio_section import render_physio_section
from counseling_section import render_counseling_section

APP_TITLE = "Sportze.AI"
APP_SUBTITLE = "Training Generator • Video Review • Counseling • Physio"
APP_TAGLINE = "Elite sports support, modular planning, and smarter athlete guidance."

SECTIONS = [
    "Training Generator",
    "Video Review",
    "Counseling",
    "Physio",
]

SECTION_DESCRIPTIONS = {
    "Training Generator": "Unified onboarding + training chat interface with session logging.",
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

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
USERS_DIR = DATA_DIR / "users"
USERS_DIR.mkdir(exist_ok=True)


def init_state() -> None:
    defaults = {
        "active_section": "Training Generator",
        "selected_plan": "Pro",
        "sport": "",
        "sport_type": "",
        "team_name": "",
        "athlete_name": "",
        "goal": "",
        "level": "",
        "is_professional": "No",
        "weekly_target": None,
        "home_notes": "",
        "profile_email": "",
        "profile_loaded": False,
        "auth_message": "",
        "user_training_logs": [],
        "saved_training_sessions": [],
        "generator_chat_messages": [],
        "training_chat_started": False,
        "training_question_index": 0,
        "training_chat_complete": False,
        "training_profile": {},
        "latest_training_payload": None,
        "latest_training_summary": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def normalize_sport_name(text: str) -> str:
    return " ".join(str(text).strip().lower().split())


def detect_sport_type(sport_text: str) -> str:
    sport = normalize_sport_name(sport_text)
    if not sport:
        return ""
    if sport in KNOWN_TEAM_SPORTS:
        return "Team Sport"
    if sport in KNOWN_INDIVIDUAL_SPORTS:
        return "Individual Sport"
    return ""


def sanitize_email(email: str) -> str:
    return re.sub(r"[^a-zA-Z0-9._-]", "_", email.strip().lower())


def user_file_path(email: str) -> Path:
    return USERS_DIR / f"{sanitize_email(email)}.json"


def build_user_payload() -> Dict[str, Any]:
    return {
        "profile_email": st.session_state.get("profile_email", ""),
        "sport": st.session_state.get("sport", ""),
        "sport_type": st.session_state.get("sport_type", ""),
        "team_name": st.session_state.get("team_name", ""),
        "athlete_name": st.session_state.get("athlete_name", ""),
        "goal": st.session_state.get("goal", ""),
        "level": st.session_state.get("level", ""),
        "is_professional": st.session_state.get("is_professional", "No"),
        "weekly_target": st.session_state.get("weekly_target", None),
        "home_notes": st.session_state.get("home_notes", ""),
        "saved_training_sessions": st.session_state.get("saved_training_sessions", []),
        "user_training_logs": st.session_state.get("user_training_logs", []),
    }


def apply_user_payload(payload: Dict[str, Any]) -> None:
    for key in [
        "profile_email",
        "sport",
        "sport_type",
        "team_name",
        "athlete_name",
        "goal",
        "level",
        "is_professional",
        "weekly_target",
        "home_notes",
        "saved_training_sessions",
        "user_training_logs",
    ]:
        if key in payload:
            st.session_state[key] = payload[key]


def save_user_profile() -> None:
    email = st.session_state.get("profile_email", "").strip().lower()
    if not email:
        return
    with user_file_path(email).open("w", encoding="utf-8") as f:
        json.dump(build_user_payload(), f, ensure_ascii=False, indent=2)


def load_user_profile(email: str) -> bool:
    path = user_file_path(email)
    if not path.exists():
        return False
    with path.open("r", encoding="utf-8") as f:
        payload = json.load(f)
    apply_user_payload(payload)
    st.session_state.profile_loaded = True
    return True


def create_user_profile(email: str, name: str = "") -> None:
    st.session_state.profile_email = email.strip().lower()
    if name.strip() and not st.session_state.get("athlete_name"):
        st.session_state.athlete_name = name.strip()
    st.session_state.profile_loaded = True
    save_user_profile()


def clear_session_profile() -> None:
    preserved = {
        "active_section": st.session_state.get("active_section", "Training Generator"),
        "selected_plan": st.session_state.get("selected_plan", "Pro"),
    }
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    init_state()
    for key, value in preserved.items():
        st.session_state[key] = value


def section_button(label: str, current: str) -> None:
    button_type = "primary" if current == label else "secondary"
    button_key = f"topnav_{label.lower().replace(' ', '_')}"
    if st.button(label, use_container_width=True, type=button_type, key=button_key):
        st.session_state.active_section = label
        st.rerun()


def render_top_banner() -> None:
    st.title(APP_TITLE)
    st.caption(APP_SUBTITLE)
    st.write(APP_TAGLINE)


def render_auth_block() -> None:
    with st.sidebar:
        st.markdown("## Email Login")
        email_input = st.text_input(
            "Email",
            value=st.session_state.get("profile_email", ""),
            placeholder="name@email.com",
            key="auth_email_input",
        ).strip().lower()
        name_input = st.text_input(
            "Name (optional for first login)",
            value=st.session_state.get("athlete_name", ""),
            key="auth_name_input",
        ).strip()

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Log in", use_container_width=True, key="auth_login_button"):
                if email_input:
                    st.session_state.profile_email = email_input
                    if load_user_profile(email_input):
                        st.session_state.auth_message = "Existing email profile loaded."
                    else:
                        create_user_profile(email_input, name_input)
                        st.session_state.auth_message = "New email profile created and ready to save progress."
                    st.rerun()
        with c2:
            if st.button("Log out", use_container_width=True, key="auth_logout_button"):
                clear_session_profile()
                st.session_state.auth_message = "You logged out of the saved email profile."
                st.rerun()

        if st.session_state.get("auth_message"):
            st.caption(st.session_state.auth_message)

        if st.session_state.get("profile_email"):
            st.success(f"Logged profile: {st.session_state.profile_email}")
            st.caption("Training history, profile answers, and gym summaries are saved for this email on this app deployment.")
        else:
            st.info("You can use the app without logging in, but training history will only stay for the current session.")

        st.divider()


def render_sidebar() -> None:
    render_auth_block()

    with st.sidebar:
        plans = ["Free", "Plus", "Pro"]
        current_plan = st.session_state.selected_plan if st.session_state.selected_plan in plans else "Pro"
        st.session_state.selected_plan = st.selectbox(
            "Plan view",
            plans,
            index=plans.index(current_plan),
            key="sidebar_plan_view",
        )

        st.markdown("### Active section")
        st.write(f"**{st.session_state.active_section}**")
        st.caption(SECTION_DESCRIPTIONS.get(st.session_state.active_section, ""))

        st.divider()
        st.markdown("### Navigation")
        for section in SECTIONS:
            if st.button(section, use_container_width=True, key=f"sidebar_{section.lower().replace(' ', '_')}"):
                st.session_state.active_section = section
                st.rerun()

        st.divider()
        st.markdown("### Profile Snapshot")
        st.write(f"Sport: {st.session_state.sport or 'Not entered'}")
        st.write(f"Sport type: {st.session_state.sport_type or 'Not defined'}")
        if st.session_state.team_name:
            st.write(f"Team: {st.session_state.team_name}")
        st.write(f"Athlete: {st.session_state.athlete_name or 'Not entered'}")
        st.write(f"Goal: {st.session_state.goal or 'Not entered'}")
        st.write(f"Level: {st.session_state.level or 'Not entered'}")
        st.write(f"Weekly frequency: {st.session_state.weekly_target or 'Not entered'}")
        if st.session_state.level in ["Advanced", "Elite"]:
            st.write(f"Professional: {st.session_state.is_professional}")
        if st.session_state.saved_training_sessions:
            st.write(f"Saved generated sessions: {len(st.session_state.saved_training_sessions)}")
        if st.session_state.user_training_logs:
            st.write(f"Logged gym summaries: {len(st.session_state.user_training_logs)}")

        st.divider()
        st.markdown("### Product Structure")
        st.write("- Homepage removed")
        st.write("- Training Generator opens by default")
        st.write("- Email-based saved profile")
        st.write("- Chat onboarding for every sport")
        st.write("- Gym training summary + calorie comparison")


def persist_if_logged_in() -> None:
    if st.session_state.get("profile_email"):
        save_user_profile()


def render_training_page() -> None:
    render_training_generator_section(on_persist=persist_if_logged_in)


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

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        section_button("Training Generator", st.session_state.active_section)
    with c2:
        section_button("Video Review", st.session_state.active_section)
    with c3:
        section_button("Counseling", st.session_state.active_section)
    with c4:
        section_button("Physio", st.session_state.active_section)

    st.divider()

    section = st.session_state.active_section
    if section == "Training Generator":
        render_training_page()
    elif section == "Video Review":
        render_video_page()
    elif section == "Counseling":
        render_counseling_page()
    elif section == "Physio":
        render_physio_page()
    else:
        st.warning("Unknown section selected.")

    persist_if_logged_in()


if __name__ == "__main__":
    main()
