import streamlit as st


# =============================================================================
# SPORTZE.AI EXPLORE SECTION
# =============================================================================
# This module is intentionally self-contained so it can be imported by app.py
# without changing the Training Generator, Video Review, Counseling, or Physio
# modules. It follows the same Streamlit rendering pattern used by the existing
# Sportze.AI sections: one public render_* function, helper data, and clean UI.
# =============================================================================

SPORTS = {
    "Water Polo": {
        "emoji": "🤽",
        "tagline": "Explosive swimming, contact, strategy, and team execution in one sport.",
        "overview": (
            "Water polo is a high-intensity team sport played in a pool, where athletes combine "
            "elite swimming endurance, fast passing, tactical positioning, shooting accuracy, and "
            "physical strength. Each team tries to score by throwing the ball into the opponent's goal "
            "while constantly swimming, defending, blocking, and creating space. Because players cannot "
            "stand on the bottom, the sport demands exceptional conditioning, leg strength through eggbeater "
            "kicking, shoulder power, reaction speed, and game intelligence."
        ),
        "why_it_matters": [
            "Develops full-body endurance, especially through repeated sprint swimming and constant treading.",
            "Builds shoulder, core, hip, and leg strength through shooting, blocking, wrestling, and eggbeater work.",
            "Improves tactical awareness because players must read defenses, identify space, and react quickly.",
            "Creates strong team communication, since success depends on coordinated drives, picks, passes, and rotations.",
        ],
        "sportze_angle": (
            "Sportze.AI can support water polo athletes by generating swim conditioning sets, dryland strength plans, "
            "mobility routines, recovery suggestions, position-specific drills, and tactical development goals. The AI can "
            "help a center, driver, goalkeeper, or utility player train differently according to their role."
        ),
        "main_body": "World Aquatics",
        "link": "https://www.worldaquatics.com/",
    },
    "Triathlon": {
        "emoji": "🏊‍♂️🚴‍♂️🏃‍♂️",
        "tagline": "A complete endurance challenge combining swimming, cycling, and running.",
        "overview": (
            "Triathlon is an endurance sport made of three disciplines completed in sequence: swimming, cycling, "
            "and running. Athletes race against the clock while managing pacing, transitions, nutrition, hydration, "
            "equipment, fatigue, and mental control. Distances can range from short sprint events to long-distance races, "
            "including the famous Ironman format. Because triathlon combines three sports into one, successful athletes "
            "need aerobic capacity, muscular endurance, efficient technique, smart recovery, and excellent planning."
        ),
        "why_it_matters": [
            "Builds one of the most complete cardiovascular bases in sport because training is spread across three disciplines.",
            "Reduces repetitive overload compared with only running, since swim and bike sessions add lower-impact volume.",
            "Requires intelligent pacing, nutrition, and race strategy instead of only raw speed.",
            "Teaches long-term discipline because improvement depends on consistency across many training zones and skills.",
        ],
        "sportze_angle": (
            "Sportze.AI can help triathletes balance weekly swim, bike, run, strength, mobility, and recovery sessions. It can "
            "separate easy aerobic work from threshold sessions, suggest brick workouts, organize taper weeks, and adapt training "
            "around soreness, limited time, or upcoming races."
        ),
        "main_body": "IRONMAN",
        "link": "https://www.ironman.com/",
    },
    "Karate": {
        "emoji": "🥋",
        "tagline": "Precision, discipline, speed, control, and combat intelligence.",
        "overview": (
            "Karate is a martial art built around striking techniques, defensive movement, body control, timing, and discipline. "
            "Training commonly includes kihon, which means fundamental techniques; kata, which are structured movement patterns; "
            "and kumite, which is sparring or controlled combat. Karate develops speed, coordination, balance, flexibility, "
            "explosive power, focus, and respect. At competitive levels, athletes must combine technical accuracy with fast decision-making, "
            "distance control, reaction time, and mental composure under pressure."
        ),
        "why_it_matters": [
            "Improves coordination, balance, mobility, and body awareness through repeated technical practice.",
            "Builds explosive power and reaction speed through strikes, footwork, and controlled sparring.",
            "Develops discipline and focus because technique quality matters as much as strength or aggression.",
            "Strengthens mental control, especially in competition where timing, patience, and precision decide points.",
        ],
        "sportze_angle": (
            "Sportze.AI can support karate athletes with mobility routines, explosive strength plans, reaction drills, conditioning blocks, "
            "injury-prevention work, and structured weekly plans that separate technical training, sparring preparation, strength, and recovery."
        ),
        "main_body": "World Karate Federation",
        "link": "https://www.wkf.net/",
    },
}


def _card(title: str, body: str) -> None:
    st.markdown(
        f"""
<div class="explore-card">
    <h3>{title}</h3>
    <p>{body}</p>
</div>
        """,
        unsafe_allow_html=True,
    )


def _inject_explore_css() -> None:
    st.markdown(
        """
<style>
    .explore-hero {
        padding: 1.25rem 1.35rem;
        border: 1px solid rgba(255,255,255,0.13);
        border-radius: 28px;
        background: linear-gradient(135deg, rgba(91,92,255,0.18), rgba(110,231,255,0.08), rgba(255,255,255,0.035));
        margin-bottom: 1.25rem;
    }

    .explore-hero h1 {
        margin: 0 0 0.35rem 0;
        font-size: clamp(2.1rem, 4.8vw, 3.7rem);
        line-height: 0.95;
        letter-spacing: -0.055em;
        font-weight: 900;
    }

    .explore-hero p {
        margin: 0;
        font-size: 1.02rem;
        line-height: 1.58;
        color: rgba(255,255,255,0.76);
        max-width: 920px;
    }

    .explore-card {
        border: 1px solid rgba(255,255,255,0.13);
        border-radius: 24px;
        padding: 1.05rem 1.1rem;
        background: rgba(255,255,255,0.052);
        margin-bottom: 0.85rem;
    }

    .explore-card h3 {
        margin: 0 0 0.35rem 0;
        font-size: 1.02rem;
        font-weight: 800;
        letter-spacing: -0.02em;
    }

    .explore-card p, .explore-card li {
        color: rgba(255,255,255,0.74);
        line-height: 1.55;
    }

    .explore-sport-title {
        font-size: clamp(1.8rem, 3.5vw, 2.65rem);
        line-height: 1.0;
        letter-spacing: -0.045em;
        font-weight: 900;
        margin-bottom: 0.2rem;
    }

    .explore-tagline {
        color: rgba(255,255,255,0.72);
        font-size: 1rem;
        margin-bottom: 1rem;
    }

    .explore-link-box {
        border: 1px solid rgba(110,231,255,0.26);
        background: rgba(110,231,255,0.07);
        border-radius: 22px;
        padding: 1rem;
        margin-top: 0.7rem;
    }
</style>
        """,
        unsafe_allow_html=True,
    )


def render_explore_section() -> None:
    """Render the Explore page for Sportze.AI."""
    _inject_explore_css()

    st.markdown(
        """
<div class="explore-hero">
    <h1>Explore Sportze.AI</h1>
    <p>
        Sportze.AI is an intelligent sports performance platform designed to help athletes excel in their sport,
        improve their fitness, understand their training, and make smarter decisions about performance, recovery,
        injury prevention, and long-term development. It combines AI-guided training, sport-specific insights,
        video review, counseling, and physical preparation so each athlete can train with more structure and purpose.
    </p>
</div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([0.95, 2.05], gap="large")

    with left:
        st.markdown("## Discover")
        st.caption("Choose a sport to see how it works, why it matters, and where its global platform lives.")

        sport_names = list(SPORTS.keys())
        if "explore_selected_sport" not in st.session_state:
            st.session_state.explore_selected_sport = sport_names[0]

        for sport_name in sport_names:
            sport = SPORTS[sport_name]
            is_active = st.session_state.explore_selected_sport == sport_name
            label = f"{sport['emoji']}  {sport_name}"
            if st.button(label, use_container_width=True, type="primary" if is_active else "secondary", key=f"explore_{sport_name.lower().replace(' ', '_')}"):
                st.session_state.explore_selected_sport = sport_name
                st.rerun()

    with right:
        selected_name = st.session_state.get("explore_selected_sport", "Water Polo")
        selected = SPORTS.get(selected_name, SPORTS["Water Polo"])

        st.markdown(f"<div class='explore-sport-title'>{selected['emoji']} {selected_name}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='explore-tagline'>{selected['tagline']}</div>", unsafe_allow_html=True)

        _card("Quick overview", selected["overview"])

        st.markdown("### Why athletes train it")
        for point in selected["why_it_matters"]:
            st.markdown(f"- {point}")

        _card("How Sportze.AI can help", selected["sportze_angle"])

        st.markdown(
            f"""
<div class="explore-link-box">
    <strong>Main global platform:</strong> {selected['main_body']}<br>
    <span style="color: rgba(255,255,255,0.72);">Use this as the official reference point for news, events, rules, rankings, and the global structure of the sport.</span>
</div>
            """,
            unsafe_allow_html=True,
        )
        st.link_button(f"Open {selected['main_body']}", selected["link"], use_container_width=False)

    st.divider()
    st.markdown("### What Explore can become next")
    c1, c2, c3 = st.columns(3)
    with c1:
        _card("Sport libraries", "Add more sports with rules, training demands, athlete profiles, and official bodies.")
    with c2:
        _card("Smart discovery", "Recommend a sport based on body type, goals, schedule, injury history, and interests.")
    with c3:
        _card("Pathways", "Show beginner-to-advanced development paths, competitions, equipment, and training milestones.")
