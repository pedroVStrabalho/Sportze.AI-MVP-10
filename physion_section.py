import streamlit as st

def run_physio():

    st.header("Physiotherapist")

    pain_area = st.selectbox("Where is the pain?", [
        "Knee", "Shoulder", "Back", "Ankle"
    ])

    pain_level = st.slider("Pain level (1-10)", 1, 10)

    if st.button("Get Advice"):

        if pain_area == "Knee":
            st.write("""
            - Ice for 20 min  
            - Quad stretching  
            - Avoid impact  
            """)

        elif pain_area == "Shoulder":
            st.write("""
            - Ice  
            - Mobility exercises  
            - Avoid overhead load  
            """)

        elif pain_area == "Back":
            st.write("""
            - Light stretching  
            - Core activation  
            - Avoid heavy lifting  
            """)

        elif pain_area == "Ankle":
            st.write("""
            - Ice  
            - Elevation  
            - Stability exercises  
            """)

        if pain_level >= 7:
            st.error("See a professional immediately.")
