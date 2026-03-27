import streamlit as st

# MUST be the first Streamlit command in the whole app
st.set_page_config(page_title="Sportze.AI", layout="wide")

from training_generator_section import run_training_generator
from video_review_section import run_video_review
from physio_section import run_physio

st.title("Sportze.AI")

section = st.sidebar.radio(
    "Choose a section",
    ["Training Generator", "Video Review", "Physio"]
)

if section == "Training Generator":
    run_training_generator()
elif section == "Video Review":
    run_video_review()
elif section == "Physio":
    run_physio()
