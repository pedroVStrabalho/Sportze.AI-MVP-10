from typing import Dict, List

import streamlit as st


TENNIS_SURFACE_PROFILE: Dict[str, List[str]] = {
    "Clay": ["Longer rallies", "Helps grinders and movers", "More physical tolerance needed"],
    "Hard": ["Balanced all-around test", "Rewards solid first strike tennis", "Most transferable surface"],
    "Grass": ["Faster points", "Rewards serve and first ball", "Comfort at net matters more"],
}

SOCCER_CONTINENTS = {
    "Europe": ["England", "Spain", "Portugal", "Italy", "Germany", "France", "Netherlands", "Belgium", "Scotland", "Ireland"],
    "South America": ["Brazil", "Argentina", "Uruguay", "Chile", "Colombia", "Peru", "Paraguay"],
    "North America": ["United States", "Mexico", "Canada"],
    "Asia": ["Japan", "South Korea", "Saudi Arabia", "UAE", "Qatar"],
}

TEAM_LEVEL_GUIDE = [
    "Local / amateur",
    "Semi-pro",
    "Lower professional",
    "Strong professional",
    "Top-flight high level",
]



def render_tennis_counseling() -> None:
    st.subheader("Tennis Tournament Counseling")
    ranking = st.number_input("Current ranking", min_value=1, max_value=5000, value=850)
    location = st.text_input("Where are you now?", placeholder="Example: São Paulo, Brazil")
    preferred_surface = st.selectbox("Preferred surface", list(TENNIS_SURFACE_PROFILE.keys()))
    travel_budget = st.selectbox("Travel budget for next week", ["Low", "Medium", "High"])
    objective = st.selectbox("Main objective", ["Get match wins", "Try a bigger event", "Build points safely", "Come back with confidence"])

    if st.button("Get Tennis Advice", type="primary", use_container_width=True):
        st.write("**Recommendation logic:**")
        if ranking <= 150:
            st.write("- You can be more selective and look for stronger point opportunities, but still avoid unnecessary long travel if form is unstable.")
        elif ranking <= 600:
            st.write("- Focus on events where the cut is realistic and the draw gives winnable first rounds.")
        else:
            st.write("- Prioritize lower-tier events or local/regional opportunities where travel cost is lower and match volume is more realistic.")

        for line in TENNIS_SURFACE_PROFILE[preferred_surface]:
            st.write(f"- {line}")

        if travel_budget == "Low":
            st.info("Best approach: stay regional, reduce cost, and maximize match probability rather than prestige.")
        elif travel_budget == "Medium":
            st.info("Best approach: mix one stronger try with one safer tournament plan if scheduling allows.")
        else:
            st.info("Best approach: widen options, but still value acceptance probability and recovery time between events.")

        st.write("**Practical next-step checklist:**")
        st.write("- Check acceptance list strength and qualifying cutoffs.")
        st.write("- Compare travel stress against your current physical freshness.")
        st.write("- Prefer tournaments where your game style fits the surface and conditions.")
        if location:
            st.caption(f"Current location noted: {location}")



def render_soccer_counseling() -> None:
    st.subheader("Soccer Career Counseling")
    current_team = st.text_input("Which team are you in now?", placeholder="Example: Derry City, Santos U20, local academy...")
    current_level = st.selectbox("Current team level", TEAM_LEVEL_GUIDE)
    continent = st.selectbox("Which continent do you want to go to?", list(SOCCER_CONTINENTS.keys()))
    country = st.selectbox("What country inside that continent?", SOCCER_CONTINENTS[continent])
    offers = st.text_area("What contract offers do you have today?", placeholder="Write current options, trials, salary level, loan ideas, or no offers yet.")

    if st.button("Get Soccer Advice", type="primary", use_container_width=True):
        st.write("**Fit analysis:**")
        if current_level in ["Local / amateur", "Semi-pro"]:
            st.write("- The smartest move is usually a step up, not a giant leap. Look for stable minutes, not only club name.")
        elif current_level == "Lower professional":
            st.write("- A stronger developmental league or a better-structured second division can be an excellent bridge move.")
        else:
            st.write("- Now you can consider leagues with more visibility, but the tactical fit and pathway to minutes still matter most.")

        st.write(f"- Target geography selected: **{continent} → {country}**")

        if offers.strip():
            st.write("- Existing offers matter a lot. Compare playing time, coaching quality, contract stability, and exposure.")
            st.caption(f"Offers noted: {offers}")
        else:
            st.write("- With no current offers, prioritize showcase environments, agents with proven placement history, and clubs where your profile clearly solves a need.")

        st.write("**Smart decision filters:**")
        filters = [
            "Will you realistically play?",
            "Is the club level a logical next step from your current level?",
            "Does the league help future moves?",
            "Is the contract financially and legally safe?",
            "Does the style of play suit your strongest qualities?",
        ]
        for f in filters:
            st.write(f"- {f}")

        if current_team:
            st.info(
                f"Based on '{current_team}', avoid unrealistic giant-club jumps unless your current level and performance data clearly support that level."
            )



def render_counseling_section() -> None:
    st.header("Counseling")
    mode = st.radio("Choose counseling mode", ["Tennis", "Soccer"], horizontal=True)

    if mode == "Tennis":
        render_tennis_counseling()
    else:
        render_soccer_counseling()
