import streamlit as st

def run_physio():
    st.header("Physio Section")
    st.write("Basic recovery and pain-guidance assistant.")

    pain_area = st.selectbox(
        "Where does it hurt?",
        [
            "Neck", "Shoulder", "Elbow", "Wrist",
            "Upper back", "Lower back", "Hip",
            "Knee", "Ankle", "Foot"
        ]
    )

    pain_scale = st.slider("Pain level (0-10)", 0, 10, 3)
    swelling = st.selectbox("Do you have swelling?", ["No", "A little", "Yes"])
    recent_injury = st.selectbox("Did this start after a recent injury?", ["No", "Yes"])

    if st.button("Evaluate"):
        st.subheader("Guidance")

        if pain_scale >= 8 or swelling == "Yes" or recent_injury == "Yes":
            st.error(
                "This may need professional evaluation. Avoid forcing training and consider a doctor or physiotherapist."
            )

        if pain_area == "Knee":
            st.write("- Reduce impact for 24-72 hours.")
            st.write("- Ice for 15-20 minutes.")
            st.write("- Gentle quad and hamstring mobility.")
            st.write("- Avoid deep painful bending.")
        elif pain_area == "Shoulder":
            st.write("- Reduce overhead load.")
            st.write("- Ice for 15-20 minutes if irritated.")
            st.write("- Light mobility only in pain-free range.")
            st.write("- Avoid explosive pressing or throwing if painful.")
        elif pain_area == "Lower back":
            st.write("- Avoid heavy loading for now.")
            st.write("- Gentle walking for 10-15 minutes.")
            st.write("- Light trunk mobility and controlled breathing.")
            st.write("- Stop if pain radiates or worsens.")
        else:
            st.write("- Reduce painful activity temporarily.")
            st.write("- Ice 15-20 minutes if irritated.")
            st.write("- Do gentle mobility in pain-free range.")
            st.write("- Progress back only when symptoms calm down.")

        st.info("This section is guidance only and does not replace a real medical assessment.")
