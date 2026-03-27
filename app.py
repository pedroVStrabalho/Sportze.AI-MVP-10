import streamlit as st

from training_generator_section import render_training_generator_section
from video_review_section import render_video_review_section
from physio_section import render_physio_section
from counseling_section import render_counseling_section

APP_TITLE = "Sportze.AI"
APP_SUBTITLE = "Training Generator • Video Review • Counseling • Physio"


def init_state() -> None:
    defaults = {
        "active_section": "Training Generator",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def section_button(label: str, current: str) -> None:
    if st.button(label, use_container_width=True, type="primary" if current == label else "secondary"):
        st.session_state.active_section = label


init_state()

st.title(APP_TITLE)
st.caption(APP_SUBTITLE)
st.write(
    "A modular Streamlit version built around separate sections, with no `st.set_page_config()` inside any file."
)

with st.container():
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
    render_training_generator_section()
elif section == "Video Review":
    render_video_review_section()
elif section == "Counseling":
    render_counseling_section()
elif section == "Physio":
    render_physio_section()
else:
    st.warning("Unknown section selected.")
