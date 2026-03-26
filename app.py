import streamlit as st

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Sportze.AI", layout="wide")

st.title("Sportze.AI")
st.write("AI-powered sports training, analysis and guidance.")

# =========================
# SAFE IMPORTS (VERY IMPORTANT)
# =========================
def safe_import(module_name, function_name):
    try:
        module = __import__(module_name)
        return getattr(module, function_name)
    except Exception as e:
        st.warning(f"{module_name} failed to load: {e}")
        return None

run_training_generator = safe_import("training_generator_section", "run_training_generator")
run_video_review = safe_import("video_review_section", "run_video_review")
run_counselling = safe_import("counselling_section", "run_counselling")
run_physio = safe_import("physio_section", "run_physio")

# =========================
# NAVIGATION
# =========================
section = st.sidebar.selectbox("Choose Section", [
    "Training Generator",
    "Video Review",
    "Counselling",
    "Physio"
])

# =========================
# ROUTING
# =========================
if section == "Training Generator":

    if run_training_generator:
        run_training_generator()
    else:
        st.error("Training Generator failed to load.")

elif section == "Video Review":

    if run_video_review:
        run_video_review()
    else:
        st.error("Video Review failed to load.")

elif section == "Counselling":

    if run_counselling:
        run_counselling()
    else:
        st.error("Counselling failed to load.")

elif section == "Physio":

    if run_physio:
        run_physio()
    else:
        st.error("Physio failed to load.")
