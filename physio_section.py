from typing import Dict, List

import streamlit as st


BODY_AREAS = {
    "Knee": {
        "common_issues": ["Overuse from jumping/running", "Poor landing mechanics", "Load spike"],
        "suggestions": [
            "Reduce explosive load for 48-72 hours if pain is rising.",
            "Ice 15-20 minutes after heavier activity if it helps symptoms.",
            "Try quad, calf, and hip mobility work.",
            "Use controlled split squats or wall sits only if pain stays tolerable.",
        ],
    },
    "Shoulder": {
        "common_issues": ["Throwing/serving overload", "Poor scapular control", "Contact irritation"],
        "suggestions": [
            "Reduce volume of serves, spikes, or throws for a few sessions.",
            "Do band external rotations and scapular retraction work.",
            "Avoid painful overhead ranges until symptoms settle.",
            "Ice can help after high-load sessions if it feels soothing.",
        ],
    },
    "Ankle": {
        "common_issues": ["Landing/twist episode", "Stiffness after sprinting", "Reactive soreness"],
        "suggestions": [
            "Use gentle ankle circles and calf mobility.",
            "Reduce cutting/jumping if pain is increasing.",
            "Single-leg balance drills can help if tolerated.",
            "Seek urgent assessment if swelling is major or weight-bearing is hard.",
        ],
    },
    "Lower Back": {
        "common_issues": ["Load management issue", "Technique fatigue", "Rotation/extension irritation"],
        "suggestions": [
            "Temporarily reduce heavy spinal loading.",
            "Use easy walking and light mobility if it feels better, not worse.",
            "Try dead bugs, bird dogs, and controlled core work.",
            "Stop and get checked if pain shoots down the leg or causes numbness.",
        ],
    },
    "Hip/Groin": {
        "common_issues": ["Direction-change overload", "Adductor tightness", "Sprint-related irritation"],
        "suggestions": [
            "Reduce max sprinting for a short period.",
            "Use adductor squeezes and controlled groin warm-up drills.",
            "Do gentle hip mobility without forcing range.",
            "Get checked if sharp pain appears during acceleration or kicking.",
        ],
    },
}

RED_FLAGS = [
    "Pain above 8/10",
    "Visible deformity",
    "Unable to bear weight",
    "Loss of strength or numbness",
    "Major swelling right away",
    "Fever or signs of infection",
]



def render_physio_section() -> None:
    st.header("Physio")
    st.write("A basic sports triage and self-care support tool. It does not replace a doctor or physiotherapist.")

    area = st.selectbox("Where does it hurt?", list(BODY_AREAS.keys()))
    pain = st.slider("Pain scale", 0, 10, 4)
    onset = st.selectbox("When did it start?", ["Today", "1-3 days ago", "This week", "More than a week ago"])
    pain_type = st.selectbox("What type of pain is it?", ["Sharp", "Dull", "Tightness", "Burning", "Stiffness", "Other"])
    swelling = st.radio("Is there swelling?", ["No", "A little", "A lot"], horizontal=True)
    mechanism = st.text_area("What happened?", placeholder="Example: landed awkwardly, after serves, after a match, after leg day...")

    st.subheader("Red flags")
    selected_red_flags = st.multiselect("Select any that are happening", RED_FLAGS)

    if st.button("Evaluate", type="primary", use_container_width=True):
        info = BODY_AREAS[area]

        st.subheader("Initial impression")
        if pain >= 8 or swelling == "A lot" or selected_red_flags:
            st.error(
                "This looks like a stronger warning sign pattern. You should get a proper in-person medical or physio assessment as soon as possible."
            )
        elif pain >= 6:
            st.warning(
                "Moderate symptoms. Reduce training load, avoid painful movements, and monitor closely over the next 24-72 hours."
            )
        else:
            st.success(
                "This sounds more compatible with a milder overload or irritation pattern, assuming there was no major trauma."
            )

        st.write("**Common possibilities to consider:**")
        for item in info["common_issues"]:
            st.write(f"- {item}")

        st.write("**Immediate care ideas:**")
        for item in info["suggestions"]:
            st.write(f"- {item}")

        st.write("**Training decision today:**")
        if pain <= 3:
            st.write("- You may do modified training if movement quality stays good and symptoms do not rise during the session.")
        elif pain <= 5:
            st.write("- Keep training light and technical, and remove high-impact or high-force actions.")
        else:
            st.write("- Avoid normal full training today. Prioritize recovery and assessment.")

        if mechanism.strip():
            st.info(f"Mechanism noted: {mechanism}")

        st.caption("This is educational guidance only, not a diagnosis.")
