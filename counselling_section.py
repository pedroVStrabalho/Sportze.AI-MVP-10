import streamlit as st

def run_counselling():

    st.header("Counselling")

    sport = st.selectbox("Choose sport", ["Tennis"])

    if sport == "Tennis":

        ranking = st.number_input("Your ranking (ATP/ITF approx)", value=500)
        location = st.text_input("Where are you now?")

        st.subheader("Next Week Tournaments (Manual)")

        st.write("""
        ATP 250:
        - Houston
        - Marrakech
        - Bucharest

        Challenger:
        - São Leopoldo
        - Mexico City

        ITF:
        - Multiple M15/M25 events worldwide
        """)

        if st.button("Get Recommendation"):

            if ranking < 150:
                st.success("Play ATP 250 level")

            elif ranking < 400:
                st.success("Play Challenger level")

            else:
                st.success("Play ITF M15/M25 level")
