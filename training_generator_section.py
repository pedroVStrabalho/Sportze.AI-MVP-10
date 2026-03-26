import streamlit as st
import random

def run_training_generator():

    st.header("Training Generator")

    role = st.selectbox("Are you a player or a coach?", ["Player", "Coach"])

    sport = st.selectbox("Choose your sport", [
        "Soccer", "Basketball", "Tennis", "Water Polo", "Surfing"
    ])

    # =========================
    # PLAYER FLOW
    # =========================
    if role == "Player":

        position = None

        if sport == "Soccer":
            position = st.selectbox("Position", [
                "Striker", "Winger", "Midfielder", "Defender", "Full Back", "Goalkeeper"
            ])

        elif sport == "Basketball":
            position = st.selectbox("Position", [
                "Point Guard", "Shooting Guard", "Small Forward", "Power Forward", "Center"
            ])

        elif sport == "Water Polo":
            position = st.selectbox("Position", [
                "Goalkeeper", "Center Forward", "Driver", "Winger"
            ])

        goal = st.selectbox("Goal", [
            "Improve performance", "Build fitness", "Learn how to play"
        ])

    # =========================
    # COACH FLOW
    # =========================
    else:
        focus = st.selectbox("What is the focus of this training?", [
            "Technical", "Tactical", "Physical", "Mixed"
        ])

    # =========================
    # GENERATE SESSION
    # =========================
    if st.button("Generate Training"):

        st.subheader("Your Session")

        if sport == "Surfing":
            st.write("""
            - Warm-up: mobility + shoulders
            - Strength: squats, split squats, core circuit
            - Pop-up drills: 3x10 explosive reps
            - Balance work: BOSU / single-leg stability
            - Water session:
                - Catch waves focusing on timing
                - Practice bottom turns + cutbacks
                - Attempt 3–5 aerials
            """)

        elif sport == "Soccer":
            st.write(f"""
            - Warm-up + dynamic stretches  
            - Passing drills (short + long)  
            - Position work: {position}  
            - Small-sided game (high intensity)  
            - Conditioning: sprints + agility  
            """)

        elif sport == "Basketball":
            st.write(f"""
            - Ball handling warm-up  
            - Shooting drills  
            - Position work: {position}  
            - 1v1 / 3v3 game  
            - Conditioning: suicides  
            """)

        elif sport == "Water Polo":
            st.write(f"""
            - Swim warm-up  
            - Passing drills  
            - Position work: {position}  
            - Shooting drills  
            - Game simulation  
            """)

        elif sport == "Tennis":
            st.write("""
            - Warm-up + mini tennis  
            - Groundstroke consistency  
            - Serve practice  
            - Point play  
            """)

        if role == "Coach":
            st.write(f"\nFocus: {focus}")
