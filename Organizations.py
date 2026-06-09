"""
Sportze.AI Organizations Module
--------------------------------
A coach, club, and federation dashboard for Sportze.AI.

This file is intentionally separate from app.py so the organization product can
become a real B2B/B2G product later without breaking the athlete app.

MVP features included now:
- Coach dashboard
- Test athletes section
- Add/edit athlete records
- Athlete management table
- Training compliance and workload summaries
- Injury-risk triage placeholder
- Talent identification ranking
- Club/federation command center
- Partnership readiness checklist for PAB and small Olympic committees
- Future API integration placeholders

Future API direction:
- Replace JSON persistence with database tables.
- Connect Sportze.AI training generation to each athlete profile.
- Connect video analysis outputs to technical score fields.
- Connect wearable/attendance data to workload and injury-risk estimates.
- Add role permissions for head coach, assistant coach, physio, federation admin.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
import streamlit as st


ORG_DATA_DIR = Path("data") / "organizations"
ORG_DATA_DIR.mkdir(parents=True, exist_ok=True)
ORG_FILE = ORG_DATA_DIR / "sportze_organization_demo.json"


# =============================================================================
# SAMPLE / TEST DATA
# =============================================================================
DEFAULT_TEST_ATHLETES: List[Dict[str, Any]] = [
    {
        "name": "Lucas Andrade",
        "sport": "Water Polo",
        "position": "Goalkeeper",
        "age": 15,
        "club": "PAB Test Club",
        "level": "U16 competitive",
        "goal": "Improve reaction speed and leg endurance",
        "sessions_week": 5,
        "completed_week": 4,
        "injury_status": "Healthy",
        "fatigue_1_10": 4,
        "technical_score": 78,
        "fitness_score": 74,
        "consistency_score": 80,
        "notes": "Strong reflexes. Needs more controlled eggbeater volume and shoulder prehab.",
    },
    {
        "name": "Marina Costa",
        "sport": "Water Polo",
        "position": "Attacker",
        "age": 16,
        "club": "PAB Test Club",
        "level": "U18 prospect",
        "goal": "Improve shooting power and counterattack speed",
        "sessions_week": 6,
        "completed_week": 5,
        "injury_status": "Minor shoulder discomfort",
        "fatigue_1_10": 6,
        "technical_score": 84,
        "fitness_score": 79,
        "consistency_score": 77,
        "notes": "High upside. Monitor shoulder volume before heavy shooting blocks.",
    },
    {
        "name": "Rafael Nunes",
        "sport": "Triathlon",
        "position": "Endurance athlete",
        "age": 17,
        "club": "Sportze Endurance Lab",
        "level": "Regional",
        "goal": "Build consistent bike-run transition quality",
        "sessions_week": 7,
        "completed_week": 5,
        "injury_status": "Healthy",
        "fatigue_1_10": 7,
        "technical_score": 72,
        "fitness_score": 86,
        "consistency_score": 68,
        "notes": "Great aerobic engine. Risk is fatigue accumulation and missed recovery.",
    },
    {
        "name": "Ana Beatriz Lima",
        "sport": "Swimming",
        "position": "Freestyle",
        "age": 14,
        "club": "Sportze Swim Lab",
        "level": "Development",
        "goal": "Improve 100m and 200m pacing",
        "sessions_week": 5,
        "completed_week": 5,
        "injury_status": "Healthy",
        "fatigue_1_10": 3,
        "technical_score": 75,
        "fitness_score": 70,
        "consistency_score": 90,
        "notes": "Very consistent. Good candidate for long-term development tracking.",
    },
]


PARTNERSHIP_STAGES = [
    {
        "stage": "1. Local coach pilot",
        "target_size": "5-20 athletes",
        "what_to_prove": "Athletes use the system weekly and coaches save time managing plans.",
        "offer": "Free MVP access for one training group.",
    },
    {
        "stage": "2. Small club pilot",
        "target_size": "20-75 athletes",
        "what_to_prove": "The dashboard helps compare athletes, organize workloads, and spot risk early.",
        "offer": "Low-cost club dashboard with feedback calls.",
    },
    {
        "stage": "3. PAB-style water polo pilot",
        "target_size": "50-150 athletes or 3-5 clubs",
        "what_to_prove": "Sportze can become useful for athlete registry, prospect tracking, and coach education.",
        "offer": "A formal pilot, not a huge paid contract yet.",
    },
    {
        "stage": "4. Federation beta",
        "target_size": "150-500 athletes",
        "what_to_prove": "The federation can see a national talent pipeline and standardized reports.",
        "offer": "Annual federation dashboard with support.",
    },
    {
        "stage": "5. Small Olympic committee",
        "target_size": "50-300 national athletes across sports",
        "what_to_prove": "A small country can manage elite athletes without building its own sports-science platform.",
        "offer": "National athlete development pilot for countries like Nauru.",
    },
]


# =============================================================================
# DATA HELPERS
# =============================================================================
def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def safe_load_json(path: Path, default: Dict[str, Any]) -> Dict[str, Any]:
    try:
        if not path.exists():
            return default
        loaded = json.loads(path.read_text(encoding="utf-8"))
        return loaded if isinstance(loaded, dict) else default
    except Exception:
        return default


def safe_write_json(path: Path, payload: Dict[str, Any]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)


def default_org_payload() -> Dict[str, Any]:
    return {
        "schema_version": "sportze_organizations_v1",
        "updated_at": now_iso(),
        "organization_name": "Sportze Coach Demo",
        "organization_type": "Club / Academy",
        "primary_sport": "Water Polo",
        "country": "Brazil",
        "athletes": DEFAULT_TEST_ATHLETES,
        "coach_notes": [],
        "future_api_status": {
            "training_generator_api": "Prepared placeholder",
            "video_review_api": "Prepared placeholder",
            "wearables_api": "Prepared placeholder",
            "federation_registry_api": "Prepared placeholder",
        },
    }


def get_org_state() -> Dict[str, Any]:
    if "organization_payload" not in st.session_state:
        st.session_state.organization_payload = safe_load_json(ORG_FILE, default_org_payload())
    payload = st.session_state.organization_payload
    if not isinstance(payload, dict):
        payload = default_org_payload()
        st.session_state.organization_payload = payload
    if "athletes" not in payload or not isinstance(payload["athletes"], list):
        payload["athletes"] = []
    return payload


def save_org_state() -> None:
    payload = get_org_state()
    payload["updated_at"] = now_iso()
    safe_write_json(ORG_FILE, payload)


def reset_test_data() -> None:
    st.session_state.organization_payload = default_org_payload()
    save_org_state()


def athletes_df(athletes: List[Dict[str, Any]]) -> pd.DataFrame:
    if not athletes:
        return pd.DataFrame(
            columns=[
                "name", "sport", "position", "age", "club", "level", "goal",
                "sessions_week", "completed_week", "completion_rate", "injury_status",
                "fatigue_1_10", "technical_score", "fitness_score", "consistency_score",
                "talent_score", "risk_level", "notes",
            ]
        )

    df = pd.DataFrame(athletes)
    for col in ["sessions_week", "completed_week", "fatigue_1_10", "technical_score", "fitness_score", "consistency_score"]:
        if col not in df.columns:
            df[col] = 0
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["completion_rate"] = df.apply(
        lambda row: 0 if row["sessions_week"] <= 0 else round((row["completed_week"] / row["sessions_week"]) * 100, 1),
        axis=1,
    )
    df["talent_score"] = (
        df["technical_score"] * 0.35
        + df["fitness_score"] * 0.35
        + df["consistency_score"] * 0.20
        + df["completion_rate"] * 0.10
    ).round(1)
    df["risk_level"] = df.apply(classify_risk, axis=1)
    return df


def classify_risk(row: pd.Series) -> str:
    injury = str(row.get("injury_status", "")).lower()
    fatigue = float(row.get("fatigue_1_10", 0) or 0)
    completion = float(row.get("completion_rate", 0) or 0)

    if "pain" in injury or "discomfort" in injury or "injury" in injury or fatigue >= 8:
        return "High"
    if fatigue >= 6 or completion < 65:
        return "Medium"
    return "Low"


def build_weekly_report(row: Dict[str, Any]) -> str:
    completion_rate = 0
    sessions = int(row.get("sessions_week", 0) or 0)
    completed = int(row.get("completed_week", 0) or 0)
    if sessions > 0:
        completion_rate = round((completed / sessions) * 100, 1)

    risk = classify_risk(pd.Series({**row, "completion_rate": completion_rate}))
    return f"""
Athlete report for {row.get('name', 'Unnamed athlete')}

Sport: {row.get('sport', '-')}
Position / event: {row.get('position', '-')}
Level: {row.get('level', '-')}
Goal: {row.get('goal', '-')}

This week:
- Planned sessions: {sessions}
- Completed sessions: {completed}
- Completion rate: {completion_rate}%
- Fatigue: {row.get('fatigue_1_10', '-')}/10
- Injury status: {row.get('injury_status', '-')}
- Risk level: {risk}

Coach interpretation:
{interpret_athlete(row, completion_rate, risk)}

Next-step recommendation:
{recommend_next_step(row, completion_rate, risk)}
""".strip()


def interpret_athlete(row: Dict[str, Any], completion_rate: float, risk: str) -> str:
    if risk == "High":
        return "This athlete should not simply receive more volume. The coach should review pain, fatigue, recovery, and technical load before increasing intensity."
    if completion_rate < 65:
        return "The main problem is not talent; it is training consistency. The coach should understand why sessions are being missed."
    if float(row.get("talent_score", 0) or 0) >= 80:
        return "This athlete is a strong candidate for prospect tracking and higher-level testing."
    return "This athlete is developing normally and should stay on a clear weekly plan with simple measurable targets."


def recommend_next_step(row: Dict[str, Any], completion_rate: float, risk: str) -> str:
    sport = str(row.get("sport", "sport")).lower()
    if risk == "High":
        return "Reduce load temporarily, add recovery/prehab notes, and ask for a physio-style check before harder work."
    if "water polo" in sport:
        return "Use a balanced water polo week: technical passing, shooting under fatigue, eggbeater conditioning, tactical review, and shoulder prehab."
    if "triathlon" in sport:
        return "Protect recovery while improving consistency across swim, bike, run, and brick sessions."
    if "swimming" in sport:
        return "Keep volume consistent and add pace targets for each main set."
    return "Create a simple weekly plan with one technical goal, one fitness goal, and one recovery habit."


# =============================================================================
# UI HELPERS
# =============================================================================
def metric_card(label: str, value: Any, help_text: str = "") -> None:
    st.metric(label, value, help=help_text or None)


def render_org_header(payload: Dict[str, Any]) -> None:
    st.markdown("# Organizations")
    st.caption(
        "Coach, club, and federation workspace. This is the B2B side of Sportze.AI: manage athletes, track development, prepare reports, and build toward partnerships."
    )

    with st.expander("Organization setup", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            payload["organization_name"] = st.text_input("Organization name", payload.get("organization_name", ""))
            payload["organization_type"] = st.selectbox(
                "Organization type",
                ["Club / Academy", "School", "Federation", "Olympic Committee", "Private Coach", "Other"],
                index=["Club / Academy", "School", "Federation", "Olympic Committee", "Private Coach", "Other"].index(payload.get("organization_type", "Club / Academy"))
                if payload.get("organization_type", "Club / Academy") in ["Club / Academy", "School", "Federation", "Olympic Committee", "Private Coach", "Other"] else 0,
            )
        with c2:
            payload["primary_sport"] = st.text_input("Primary sport", payload.get("primary_sport", "Water Polo"))
            payload["country"] = st.text_input("Country", payload.get("country", "Brazil"))

        if st.button("Save organization setup", type="primary"):
            save_org_state()
            st.success("Organization setup saved.")


def render_dashboard(df: pd.DataFrame) -> None:
    st.markdown("## Athlete dashboard")
    st.caption("A quick control panel for coaches: participation, workload, injury risk, and prospect tracking.")

    total = len(df)
    avg_completion = round(df["completion_rate"].mean(), 1) if total else 0
    high_risk = int((df["risk_level"] == "High").sum()) if total else 0
    top_score = round(df["talent_score"].max(), 1) if total else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Athletes", total, "Total athletes currently managed by the coach or organization.")
    with c2:
        metric_card("Avg completion", f"{avg_completion}%", "How many planned sessions athletes completed this week.")
    with c3:
        metric_card("High-risk athletes", high_risk, "Athletes needing coach attention because of pain, fatigue, or missed sessions.")
    with c4:
        metric_card("Top talent score", top_score, "MVP score combining technical, fitness, consistency, and completion data.")

    if not df.empty:
        st.markdown("### Coach attention list")
        attention = df.sort_values(["risk_level", "fatigue_1_10", "completion_rate"], ascending=[True, False, True])
        attention = attention[attention["risk_level"].isin(["High", "Medium"])]
        if attention.empty:
            st.success("No urgent athlete risks detected in this MVP dataset.")
        else:
            st.dataframe(
                attention[["name", "sport", "position", "completion_rate", "fatigue_1_10", "injury_status", "risk_level"]],
                use_container_width=True,
                hide_index=True,
            )


def render_test_athletes_section(payload: Dict[str, Any]) -> None:
    st.markdown("## Test athletes")
    st.caption(
        "Use these fake athletes to test the dashboard before real users, clubs, or federations are connected. Later, this becomes database-backed athlete creation."
    )

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Load / reset test athletes", use_container_width=True):
            reset_test_data()
            st.success("Test athletes loaded.")
            st.rerun()
    with c2:
        if st.button("Clear all athletes", use_container_width=True):
            payload["athletes"] = []
            save_org_state()
            st.warning("All athletes cleared.")
            st.rerun()


def render_add_athlete(payload: Dict[str, Any]) -> None:
    st.markdown("## Add athlete")
    st.caption("For now this saves to a local JSON file. Later, each athlete would have login, history, video data, and training-plan data.")

    with st.form("add_athlete_form", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            name = st.text_input("Athlete name")
            sport = st.text_input("Sport", value=payload.get("primary_sport", "Water Polo"))
            position = st.text_input("Position / event", value="")
            age = st.number_input("Age", min_value=5, max_value=80, value=15)
        with c2:
            club = st.text_input("Club / group", value=payload.get("organization_name", ""))
            level = st.selectbox("Level", ["Beginner", "Development", "Regional", "National", "Elite", "Professional"])
            goal = st.text_area("Main goal", value="Improve performance and consistency.")
        with c3:
            sessions_week = st.number_input("Planned sessions/week", min_value=0, max_value=20, value=5)
            completed_week = st.number_input("Completed this week", min_value=0, max_value=20, value=4)
            fatigue = st.slider("Fatigue 1-10", 1, 10, 4)
            injury_status = st.selectbox("Injury status", ["Healthy", "Minor discomfort", "Pain", "Injury recovery"])

        st.markdown("### MVP performance scores")
        s1, s2, s3 = st.columns(3)
        with s1:
            technical = st.slider("Technical score", 0, 100, 70)
        with s2:
            fitness = st.slider("Fitness score", 0, 100, 70)
        with s3:
            consistency = st.slider("Consistency score", 0, 100, 70)
        notes = st.text_area("Coach notes", value="")

        submitted = st.form_submit_button("Add athlete", type="primary")
        if submitted:
            if not name.strip():
                st.error("Add an athlete name first.")
            else:
                payload["athletes"].append(
                    {
                        "name": name.strip(),
                        "sport": sport.strip(),
                        "position": position.strip(),
                        "age": int(age),
                        "club": club.strip(),
                        "level": level,
                        "goal": goal.strip(),
                        "sessions_week": int(sessions_week),
                        "completed_week": int(completed_week),
                        "injury_status": injury_status,
                        "fatigue_1_10": int(fatigue),
                        "technical_score": int(technical),
                        "fitness_score": int(fitness),
                        "consistency_score": int(consistency),
                        "notes": notes.strip(),
                    }
                )
                save_org_state()
                st.success("Athlete added.")
                st.rerun()


def render_athlete_table(payload: Dict[str, Any], df: pd.DataFrame) -> Optional[Dict[str, Any]]:
    st.markdown("## Athlete management")
    st.caption("This table is the beginning of a real coach dashboard: one place to compare athletes and decide who needs attention.")

    if df.empty:
        st.info("No athletes yet. Load test athletes or add your own.")
        return None

    shown_cols = [
        "name", "sport", "position", "age", "club", "level", "completion_rate",
        "fatigue_1_10", "injury_status", "technical_score", "fitness_score",
        "consistency_score", "talent_score", "risk_level",
    ]
    st.dataframe(df[shown_cols].sort_values("talent_score", ascending=False), use_container_width=True, hide_index=True)

    names = df["name"].tolist()
    selected_name = st.selectbox("Open athlete profile", names)
    athlete_index = names.index(selected_name)
    athlete = payload["athletes"][athlete_index]
    return athlete


def render_selected_athlete(athlete: Optional[Dict[str, Any]]) -> None:
    if not athlete:
        return

    st.markdown("## Athlete profile")
    c1, c2 = st.columns([1.2, 1])
    with c1:
        st.markdown(f"### {athlete.get('name', 'Unnamed athlete')}")
        st.write(f"**Sport:** {athlete.get('sport', '-')}")
        st.write(f"**Position / event:** {athlete.get('position', '-')}")
        st.write(f"**Level:** {athlete.get('level', '-')}")
        st.write(f"**Goal:** {athlete.get('goal', '-')}")
        st.write(f"**Coach notes:** {athlete.get('notes', '-')}")
    with c2:
        report = build_weekly_report(athlete)
        st.text_area("Auto weekly report", report, height=360)


def render_talent_identification(df: pd.DataFrame) -> None:
    st.markdown("## Talent identification")
    st.caption(
        "This is where a federation would eventually detect prospects. For now it uses simple MVP scores; later it should use real tests, competitions, video analysis, and coach verification."
    )

    if df.empty:
        st.info("Add athletes first.")
        return

    top = df.sort_values("talent_score", ascending=False).head(10)
    st.dataframe(
        top[["name", "sport", "age", "position", "club", "talent_score", "technical_score", "fitness_score", "consistency_score", "risk_level"]],
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("### How the MVP score works")
    st.write(
        "Talent score currently combines technical score, fitness score, consistency, and weekly completion. This is deliberately simple so the dashboard is usable now, but the formula is prepared to be replaced by a future AI/API model."
    )


def render_federation_tools(payload: Dict[str, Any], df: pd.DataFrame) -> None:
    st.markdown("## Club and federation tools")
    st.caption("This section explains how the same dashboard can grow from one coach into club, PAB-style federation, and small Olympic committee products.")

    tab1, tab2, tab3 = st.tabs(["Coach tools", "Federation tools", "Partnership path"])

    with tab1:
        st.markdown("### Coach tools")
        st.write("A coach needs fewer spreadsheets and better decisions. This workspace should help with:")
        st.write("- Athlete profiles")
        st.write("- Weekly workload")
        st.write("- Training completion")
        st.write("- Injury-risk flags")
        st.write("- Simple automated reports")
        st.write("- Future training-plan assignment")

    with tab2:
        st.markdown("### Federation tools")
        st.write("A federation needs visibility over a whole sport, not just one team. This could become:")
        st.write("- National athlete registry")
        st.write("- Youth prospect pipeline")
        st.write("- Coach education portal")
        st.write("- Standardized testing and benchmarks")
        st.write("- National-team monitoring")
        st.write("- Club comparison without exposing private data unfairly")
        if not df.empty:
            sport_counts = df["sport"].value_counts().reset_index()
            sport_counts.columns = ["sport", "athletes"]
            st.dataframe(sport_counts, use_container_width=True, hide_index=True)

    with tab3:
        st.markdown("### Partnership path")
        st.caption("This is a realistic order: start small, prove usage, then approach stronger organizations.")
        st.dataframe(pd.DataFrame(PARTNERSHIP_STAGES), use_container_width=True, hide_index=True)


def render_future_api_section(payload: Dict[str, Any]) -> None:
    st.markdown("## Future API implementation")
    st.caption("These boxes do not call paid APIs yet. They show exactly where future AI/database features would connect.")

    with st.expander("Training Generator API connection", expanded=True):
        st.write("Future behavior: the coach selects athletes, chooses a weekly goal, and Sportze generates individualized plans using each athlete profile.")
        st.code(
            """# Future placeholder
# selected_athletes = get_selected_athletes()
# plans = sportze_training_api.generate_team_week(
#     athletes=selected_athletes,
#     sport=organization.primary_sport,
#     goal=coach_goal,
#     competition_calendar=calendar_data,
# )""",
            language="python",
        )

    with st.expander("Video Review API connection", expanded=False):
        st.write("Future behavior: uploaded clips update technical scores automatically, but the coach still approves final notes.")
        st.code(
            """# Future placeholder
# video_result = sportze_video_api.review(file, sport, movement_focus)
# athlete.technical_score = video_result.scores.overall
# athlete.notes += video_result.coach_summary""",
            language="python",
        )

    with st.expander("Federation registry API connection", expanded=False):
        st.write("Future behavior: clubs submit athletes into a national registry with permissions and privacy controls.")
        st.code(
            """# Future placeholder
# federation_registry.sync(
#     federation='PAB',
#     athletes=approved_club_athletes,
#     permissions=role_based_access,
# )""",
            language="python",
        )


def render_organizations_section() -> None:
    payload = get_org_state()
    render_org_header(payload)

    df = athletes_df(payload.get("athletes", []))
    if not df.empty:
        # Store derived talent score back into payload only for report interpretation.
        for idx, row in df.iterrows():
            if idx < len(payload["athletes"]):
                payload["athletes"][idx]["talent_score"] = float(row.get("talent_score", 0) or 0)

    tabs = st.tabs([
        "Dashboard",
        "Test athletes",
        "Add athlete",
        "Athletes",
        "Talent ID",
        "Club/Federation",
        "Future API",
    ])

    with tabs[0]:
        render_dashboard(df)
    with tabs[1]:
        render_test_athletes_section(payload)
    with tabs[2]:
        render_add_athlete(payload)
    with tabs[3]:
        selected = render_athlete_table(payload, df)
        render_selected_athlete(selected)
    with tabs[4]:
        render_talent_identification(df)
    with tabs[5]:
        render_federation_tools(payload, df)
    with tabs[6]:
        render_future_api_section(payload)

    save_org_state()
