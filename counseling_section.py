from __future__ import annotations

import re
from typing import Dict, List, Tuple

import streamlit as st

# -----------------------------------------------------------------------------
# STANDALONE COUNSELLING MODULE SETUP
# -----------------------------------------------------------------------------
# This file is meant to be imported from app.py, for example:
# from counselling_section import render_counseling_section
# Then call render_counseling_section() where your Counseling page is rendered.

SPORT_CLASSIFICATION: Dict[str, str] = {
    "Soccer": "team",
    "American Football": "team",
    "Futsal": "team",
    "Basketball": "team",
    "Volleyball": "team",
    "Water Polo": "team",
    "Handball": "team",
    "Rugby": "team",
    "Hockey": "team",
    "Baseball": "team",
    "Softball": "team",
    "Cricket": "team",
    "Tennis": "individual",
    "Padel": "individual",
    "Beach Tennis": "individual",
    "Table Tennis": "individual",
    "Badminton": "individual",
    "Squash": "individual",
    "Golf": "individual",
    "Athletics": "individual",
    "Swimming": "individual",
    "Triathlon": "individual",
    "Boxing": "individual",
    "Judo": "individual",
    "Wrestling": "individual",
    "Gymnastics": "individual",
    "Cycling": "individual",
    "Surf": "individual",
}

SPORT_ALIASES: Dict[str, str] = {
    "football": "Soccer", "futebol": "Soccer", "futbol": "Soccer", "socer": "Soccer", "socker": "Soccer",
    "american footbal": "American Football", "nfl": "American Football", "gridiron": "American Football",
    "futsall": "Futsal", "indoor soccer": "Futsal",
    "basket": "Basketball", "bball": "Basketball", "bascketball": "Basketball", "basketbal": "Basketball",
    "volei": "Volleyball", "vôlei": "Volleyball", "volley": "Volleyball", "voley": "Volleyball", "vollyball": "Volleyball",
    "waterpolo": "Water Polo", "water pollo": "Water Polo", "waterpoolo": "Water Polo", "polo aquatico": "Water Polo", "polo aquático": "Water Polo",
    "hand ball": "Handball", "handebol": "Handball", "handbal": "Handball",
    "rugbi": "Rugby", "rugby union": "Rugby", "rugby sevens": "Rugby", "rugy": "Rugby",
    "field hockey": "Hockey", "ice hockey": "Hockey", "hoquei": "Hockey", "hocky": "Hockey",
    "beisebol": "Baseball", "base ball": "Baseball", "basebal": "Baseball",
    "softbol": "Softball", "soft ball": "Softball", "softbal": "Softball",
    "criquete": "Cricket", "criket": "Cricket",
    "tenis": "Tennis", "tênis": "Tennis", "tennnis": "Tennis", "tennisfs": "Tennis", "tennisz": "Tennis",
    "pádel": "Padel", "paddle": "Padel", "padle": "Padel", "paddel": "Padel",
    "beachtennis": "Beach Tennis", "beach tenis": "Beach Tennis", "tenis de praia": "Beach Tennis", "tênis de praia": "Beach Tennis",
    "ping pong": "Table Tennis", "ping-pong": "Table Tennis", "tenis de mesa": "Table Tennis", "tênis de mesa": "Table Tennis",
    "badmington": "Badminton", "badmintom": "Badminton", "badmiton": "Badminton",
    "squashh": "Squash", "squashs": "Squash",
    "golfe": "Golf", "glof": "Golf",
    "track and field": "Athletics", "atletismo": "Athletics", "running": "Athletics", "sprint": "Athletics", "athletcs": "Athletics",
    "natacao": "Swimming", "natação": "Swimming", "swim": "Swimming", "swiming": "Swimming", "swimmng": "Swimming",
    "triatlo": "Triathlon", "triathalon": "Triathlon", "triathlete": "Triathlon",
    "boxe": "Boxing", "box": "Boxing", "boxxing": "Boxing",
    "judô": "Judo", "judoo": "Judo",
    "luta olimpica": "Wrestling", "luta olímpica": "Wrestling", "wrestlin": "Wrestling",
    "ginastica": "Gymnastics", "ginástica": "Gymnastics", "artistic gymnastics": "Gymnastics", "gymnastic": "Gymnastics",
    "ciclismo": "Cycling", "bike": "Cycling", "biking": "Cycling", "road cycling": "Cycling", "mtb": "Cycling",
    "surfing": "Surf", "surfe": "Surf", "surfista": "Surf", "surffing": "Surf",
    "karate": "Karate", "karaté": "Karate", "karatê": "Karate", "karatee": "Karate",
    "rowing": "Rowing", "remo": "Rowing", "row": "Rowing",
    "weight lifting": "Weightlifting", "olympic lifting": "Weightlifting", "levantamento de peso": "Weightlifting", "weightlifitng": "Weightlifting",
}

# Keep these names because older code may reference them.
COMMON_SPORT_INPUT_ERRORS: Dict[str, str] = dict(SPORT_ALIASES)
EXTENDED_SPORT_ERROR_CATALOG: Dict[str, str] = dict(SPORT_ALIASES)


def normalize_text_for_match(value: str) -> str:
    value = (value or "").strip().lower()
    replacements = {"á": "a", "à": "a", "ã": "a", "â": "a", "é": "e", "ê": "e", "í": "i", "ó": "o", "õ": "o", "ô": "o", "ú": "u", "ç": "c"}
    for old, new in replacements.items():
        value = value.replace(old, new)
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def normalize_sport_name(raw_sport: str) -> Tuple[str, str, str]:
    raw = (raw_sport or "").strip()
    if not raw:
        return "", "unknown", "empty"

    direct = SPORT_CLASSIFICATION.get(raw.title()) or SPORT_CLASSIFICATION.get(raw)
    if direct:
        return raw.title(), direct, "exact_catalog_match"

    norm = normalize_text_for_match(raw)
    merged_aliases: Dict[str, str] = {}
    for source in [SPORT_ALIASES, COMMON_SPORT_INPUT_ERRORS, EXTENDED_SPORT_ERROR_CATALOG]:
        for alias, canonical in source.items():
            merged_aliases[normalize_text_for_match(alias)] = canonical

    if norm in merged_aliases:
        canonical = merged_aliases[norm]
        return canonical, SPORT_CLASSIFICATION.get(canonical, "unknown"), "alias_or_typo_match"

    compact = norm.replace(" ", "")
    for alias_norm, canonical in merged_aliases.items():
        if compact == alias_norm.replace(" ", ""):
            return canonical, SPORT_CLASSIFICATION.get(canonical, "unknown"), "compact_alias_match"

    # simple fuzzy-ish containment fallback for common typo phrases
    for alias_norm, canonical in merged_aliases.items():
        if len(alias_norm) >= 4 and alias_norm in norm:
            return canonical, SPORT_CLASSIFICATION.get(canonical, "unknown"), "contained_alias_match"

    return raw.title(), "unknown", "custom_sport_not_in_catalog"

# -----------------------------------------------------------------------------
# AI-READY ELITE SPORTS COUNSELING CHAT
# -----------------------------------------------------------------------------
# This section intentionally removes the old questionnaire intake.
# The app now asks one open question, stores the chat, and prepares a rich
# API payload for future OpenAI / external reasoning implementation.

SUPPLEMENTAL_COUNSELING_SPORTS: Dict[str, str] = {
    "Karate": "individual",
    "Rowing": "team",
    "Weightlifting": "individual",
}
SPORT_CLASSIFICATION.update(SUPPLEMENTAL_COUNSELING_SPORTS)
DEFAULT_SPORT_OPTIONS = list(dict.fromkeys(list(SPORT_CLASSIFICATION.keys()) + ["Other"]))

SPORT_COUNSELING_KNOWLEDGE: Dict[str, Dict[str, object]] = {
    "Soccer": {
        "type": "team",
        "major_leagues": ["Premier League", "La Liga", "Bundesliga", "Serie A", "Ligue 1", "MLS", "UEFA Champions League"],
        "knowledge": "Soccer counseling should evaluate club level, minutes, academy pathway, agent quality, tactical role, passport/registration restrictions, and whether a move improves the next transfer. Elite advice must separate prestige from development value.",
    },
    "American Football": {
        "type": "team",
        "major_leagues": ["NFL", "NCAA FBS", "NCAA FCS", "UFL", "CFL", "High School Football", "International Federation of American Football"],
        "knowledge": "American football pathways are heavily combine-driven. Counseling should consider position, measurable traits, film, academic eligibility, camp exposure, scholarship routes, and whether the athlete fits NCAA or professional development timelines.",
    },
    "Futsal": {
        "type": "team",
        "major_leagues": ["FIFA Futsal World Cup", "UEFA Futsal Champions League", "Liga Nacional de Futsal", "Spanish Primera Division Futsal", "Portuguese Liga Placard", "AFC Futsal Asian Cup", "CONMEBOL Libertadores Futsal"],
        "knowledge": "Futsal counseling should track technical speed, small-space decision making, tactical role, national federation competitions, professional club visibility, and whether the athlete is pursuing futsal only or using futsal as a soccer accelerator.",
    },
    "Basketball": {
        "type": "team",
        "major_leagues": ["NBA", "NBA G League", "NCAA Basketball", "EuroLeague", "Liga ACB", "Basketball Champions League", "FIBA World Cup"],
        "knowledge": "Basketball counseling must compare size, position, skill translation, exposure tournaments, AAU or club context, NCAA eligibility, professional overseas options, and whether the athlete needs minutes, physical development, or higher competition.",
    },
    "Volleyball": {
        "type": "team",
        "major_leagues": ["FIVB Volleyball Nations League", "Olympic Games", "CEV Champions League", "Brazilian Superliga", "Italian SuperLega", "Polish PlusLiga", "NCAA Volleyball"],
        "knowledge": "Volleyball counseling should consider position, height, jump metrics, serve/receive profile, club level, national team pathway, NCAA route, and whether the athlete needs reps, technical specialization, or stronger tactical systems.",
    },
    "Water Polo": {
        "type": "team",
        "major_leagues": ["World Aquatics", "Olympic Games", "World Aquatics Championships", "World Aquatics World Cup", "LEN Champions League", "NCAA Water Polo", "European Championships"],
        "knowledge": "Water polo counseling should analyze national-team route, club strength, NCAA options, left/right handed role, center/driver/goalkeeper profile, swimming base, tactical IQ, and the European professional pathway. For Brazil, advice should also compare domestic development with Europe or NCAA exposure.",
    },
    "Handball": {
        "type": "team",
        "major_leagues": ["EHF Champions League", "IHF World Championship", "Olympic Games", "German Bundesliga", "French Starligue", "Spanish Liga ASOBAL", "EHF European League"],
        "knowledge": "Handball counseling should evaluate position, physical profile, club country, tactical role, youth national-team visibility, European market fit, and whether a transfer improves minutes and coaching quality.",
    },
    "Rugby": {
        "type": "team",
        "major_leagues": ["Rugby World Cup", "Six Nations", "The Rugby Championship", "United Rugby Championship", "Premiership Rugby", "Top 14", "Super Rugby Pacific"],
        "knowledge": "Rugby counseling should separate union and sevens, evaluate position-specific physical demands, academy exposure, school pathway, national eligibility, injury risk, and whether the athlete is targeting club professionalism or Olympic sevens.",
    },
    "Hockey": {
        "type": "team",
        "major_leagues": ["NHL", "AHL", "KHL", "IIHF World Championship", "Olympic Hockey", "Euro Hockey League", "FIH Hockey Pro League"],
        "knowledge": "Hockey can mean ice or field hockey, so the AI must clarify from context. Counseling should analyze league pathway, skating or stick skill, position, school/club route, draft exposure, and national federation opportunities.",
    },
    "Baseball": {
        "type": "team",
        "major_leagues": ["MLB", "MiLB", "NCAA Baseball", "NPB", "KBO", "World Baseball Classic", "Little League / Youth Federation Pathway"],
        "knowledge": "Baseball counseling should evaluate position, velocity, bat speed, defensive value, showcase data, scholarship route, draft eligibility, Latin American academy pathways, and whether the athlete needs exposure or technical refinement first.",
    },
    "Softball": {
        "type": "team",
        "major_leagues": ["NCAA Softball", "Women's Professional Fastpitch", "WBSC Softball World Cup", "Olympic Softball", "National Pro Fastpitch legacy pathway", "European Softball Cups", "Pan American Softball Championship"],
        "knowledge": "Softball counseling should consider pitching/hitting profile, travel-team exposure, NCAA fit, national federation events, tournament schedule, recruiting video, and position-specific development.",
    },
    "Cricket": {
        "type": "team",
        "major_leagues": ["ICC Cricket World Cup", "ICC T20 World Cup", "Indian Premier League", "Big Bash League", "The Hundred", "County Championship", "Pakistan Super League"],
        "knowledge": "Cricket counseling should identify format, role, domestic structure, academy pathway, franchise potential, national eligibility, batting/bowling specialization, and whether the athlete should chase match volume or higher-level exposure.",
    },
    "Tennis": {
        "type": "individual",
        "major_leagues": ["ATP Tour", "ATP Challenger Tour", "ITF World Tennis Tour", "Grand Slams", "Davis Cup", "United Cup", "Next Gen ATP Finals"],
        "knowledge": "Tennis counseling must connect ranking, calendar, surface, acceptance lists, travel load, age, UTR/ITF/ATP level, and progression from ITF Juniors to M15/M25, Challenger 50/75/100/125/175, then ATP 250/500/Masters/Grand Slams. Elite advice should choose events by expected match value, not only prestige.",
    },
    "Padel": {
        "type": "individual",
        "major_leagues": ["Premier Padel", "FIP Tour", "FIP Platinum", "FIP Gold", "FIP Rise", "FIP Promotion", "National Padel Federations"],
        "knowledge": "Padel counseling should evaluate partner quality, side preference, FIP ranking, event level, travel, national federation calendar, and whether the athlete needs match wins or stronger international exposure.",
    },
    "Beach Tennis": {
        "type": "individual",
        "major_leagues": ["ITF Beach Tennis World Tour", "BT400", "BT200", "BT100", "BT50", "World Championships", "National Beach Tennis Circuits"],
        "knowledge": "Beach tennis counseling should compare ITF event level, partner chemistry, surface/weather conditions, ranking-points value, national circuit strength, and whether a higher BT event is realistic or too aggressive.",
    },
    "Table Tennis": {
        "type": "individual",
        "major_leagues": ["World Table Tennis", "WTT Champions", "WTT Star Contender", "WTT Contender", "WTT Feeder", "ITTF World Championships", "Olympic Table Tennis"],
        "knowledge": "Table tennis counseling should analyze world ranking, national ranking, style matchup, youth pathway, WTT event level, continental circuits, and whether the athlete should prioritize ranking points or tactical development.",
    },
    "Badminton": {
        "type": "individual",
        "major_leagues": ["BWF World Tour Finals", "BWF Super 1000", "BWF Super 750", "BWF Super 500", "BWF Super 300", "BWF International Challenge", "BWF Future Series"],
        "knowledge": "Badminton counseling should compare singles/doubles route, BWF ranking, continental events, travel budget, draw strength, federation support, and whether the next event gives realistic points or only prestige.",
    },
    "Squash": {
        "type": "individual",
        "major_leagues": ["PSA World Tour", "PSA World Championships", "PSA Platinum", "PSA Gold", "PSA Silver", "PSA Bronze", "PSA Challenger Tour"],
        "knowledge": "Squash counseling should evaluate PSA ranking, Challenger level, draw strength, physical durability, technical style, travel clusters, and whether to target points, experience, or confidence.",
    },
    "Golf": {
        "type": "individual",
        "major_leagues": ["PGA Tour", "DP World Tour", "Korn Ferry Tour", "LIV Golf", "Challenge Tour", "World Amateur Golf Ranking", "NCAA Golf"],
        "knowledge": "Golf counseling should evaluate scoring average, handicap, tournament results, course fit, WAGR/NCAA route, qualifiers, mental consistency, and whether the athlete needs amateur ranking, college exposure, or pro qualifying attempts.",
    },
    "Athletics": {
        "type": "individual",
        "major_leagues": ["World Athletics Diamond League", "World Athletics Championships", "Olympic Games", "Continental Tour Gold", "Continental Tour Silver", "Continental Tour Bronze", "National Championships"],
        "knowledge": "Athletics counseling must be event-specific. It should analyze PB/SB, qualifying standards, event timing, peaking cycle, wind/altitude, travel fatigue, and whether the next meet is for ranking, qualification, or performance development.",
    },
    "Swimming": {
        "type": "individual",
        "major_leagues": ["World Aquatics Championships", "Olympic Games", "World Aquatics Swimming World Cup", "National Trials", "NCAA Swimming", "Mare Nostrum Swim Tour", "Continental Championships"],
        "knowledge": "Swimming counseling should consider event profile, PB/SB, qualifying cuts, taper phase, pool type, relay pathway, technical limiters, and whether the meet should be used for qualification, race rhythm, or training validation.",
    },
    "Triathlon": {
        "type": "individual",
        "major_leagues": ["World Triathlon Championship Series", "World Triathlon Cup", "Continental Cups", "Ironman World Championship", "Ironman 70.3 World Championship", "Challenge Family", "Supertri"],
        "knowledge": "Triathlon counseling should separate draft-legal Olympic route from Ironman route. It must analyze swim-bike-run splits, transition skills, ranking points, climate, travel, recovery, and race selection by development phase.",
    },
    "Boxing": {
        "type": "individual",
        "major_leagues": ["Olympic Boxing", "World Boxing Championships", "IBA / World Boxing events", "Golden Gloves", "WBC", "WBA", "IBF", "WBO"],
        "knowledge": "Boxing counseling should distinguish amateur and professional goals, weight class, record quality, opponent selection, federation route, safety, coaching, sparring level, and whether a bout improves development or creates unnecessary risk.",
    },
    "Judo": {
        "type": "individual",
        "major_leagues": ["IJF World Tour", "IJF Grand Slam", "IJF Grand Prix", "IJF World Championships", "Olympic Games", "Continental Opens", "National Ranking Events"],
        "knowledge": "Judo counseling should evaluate weight class, IJF ranking, continental route, grip style, travel clusters, recovery, national-team selection, and whether the event has ranking value or tactical development value.",
    },
    "Wrestling": {
        "type": "individual",
        "major_leagues": ["United World Wrestling", "World Wrestling Championships", "Olympic Games", "Continental Championships", "Ranking Series", "NCAA Wrestling", "National Trials"],
        "knowledge": "Wrestling counseling should distinguish freestyle, Greco-Roman, and folkstyle, then analyze weight class, ranking events, national trials, NCAA route, peaking cycle, and whether cutting weight harms performance.",
    },
    "Gymnastics": {
        "type": "individual",
        "major_leagues": ["FIG World Championships", "Olympic Games", "FIG World Cup", "Continental Championships", "NCAA Gymnastics", "National Championships", "Junior World Championships"],
        "knowledge": "Gymnastics counseling should consider apparatus profile, difficulty score, execution consistency, injury risk, age pathway, national-team selection, and whether the next competition is for routine validation or selection pressure.",
    },
    "Cycling": {
        "type": "individual",
        "major_leagues": ["UCI WorldTour", "UCI ProSeries", "UCI Continental Circuits", "Tour de France", "Giro d'Italia", "Vuelta a España", "Olympic Cycling"],
        "knowledge": "Cycling counseling should separate road, track, MTB, BMX, and time trial. It must analyze power profile, team role, race category, UCI points, course fit, recovery, and whether the event supports long-term specialization.",
    },
    "Surf": {
        "type": "individual",
        "major_leagues": ["World Surf League Championship Tour", "WSL Challenger Series", "WSL Qualifying Series", "ISA World Surfing Games", "Olympic Surfing", "Junior Pro Events", "National Surf Circuits"],
        "knowledge": "Surf counseling should evaluate heat strategy, wave type, ranking pathway, QS/Challenger selection, travel, board setup, national-team route, and whether the contest conditions fit the athlete's strengths.",
    },
    "Karate": {
        "type": "individual",
        "major_leagues": ["World Karate Federation", "Karate 1 Premier League", "Karate 1 Series A", "Karate 1 Youth League", "World Karate Championships", "Continental Championships", "National Karate Championships"],
        "knowledge": "Karate counseling should separate kumite and kata, evaluate weight/category, WKF ranking, national-team pathway, continental events, technical profile, tactical scoring patterns, and whether the athlete needs ranking points or championship preparation.",
    },
    "Rowing": {
        "type": "team",
        "major_leagues": ["World Rowing Championships", "Olympic Rowing", "World Rowing Cups", "U23 World Championships", "Junior World Championships", "NCAA Rowing", "Henley Royal Regatta"],
        "knowledge": "Rowing counseling should analyze boat class, erg scores, crew role, technical efficiency, national-team route, NCAA recruiting, regatta calendar, and whether the athlete should prioritize crew placement, erg improvement, or selection events.",
    },
    "Weightlifting": {
        "type": "individual",
        "major_leagues": ["IWF World Championships", "Olympic Weightlifting", "IWF World Cup", "Continental Championships", "Junior World Championships", "National Championships", "University Weightlifting Championships"],
        "knowledge": "Weightlifting counseling should evaluate snatch/clean and jerk totals, weight class, qualification standards, technical consistency, injury management, competition timing, and whether changing weight class helps or hurts qualification odds.",
    },
}

COUNSELING_SYSTEM_PROMPT = """
You are Sportze.AI Elite Sports Counseling.
Your job is to give high-level, practical, accurate sports career guidance.
Use the athlete's written question as the main source of truth.
Infer the sport even if the user writes with typo errors, mixed language, lowercase, or abbreviations.
Always consider: age, country, current team/club, ranking, level, budget, calendar, realistic pathway, competition level, selection rules, exposure, development value, health, and long-term career impact.
Do not recommend prestige-only moves. Recommend the option that best improves the athlete's next step.
When live API/search is connected, verify calendars, rankings, entry lists, league quality, federation rules, and current deadlines before final advice.
""".strip()


def ensure_counseling_state() -> None:
    if "counseling_messages" not in st.session_state:
        st.session_state.counseling_messages = []
    if "counseling_api_payloads" not in st.session_state:
        st.session_state.counseling_api_payloads = []


def reset_counseling_flow() -> None:
    st.session_state.counseling_messages = []
    st.session_state.counseling_api_payloads = []


def infer_sports_from_counseling_text(text: str) -> List[str]:
    detected: List[str] = []
    normalized_question = normalize_text_for_match(text)

    for sport in SPORT_COUNSELING_KNOWLEDGE.keys():
        if normalize_text_for_match(sport) in normalized_question:
            detected.append(sport)

    for token in re.findall(r"[A-Za-zÀ-ÿ0-9\- ]{3,}", text or ""):
        canonical, _, _ = normalize_sport_name(token)
        if canonical in SPORT_COUNSELING_KNOWLEDGE and canonical not in detected:
            detected.append(canonical)

    for alias, canonical in {**SPORT_ALIASES, **COMMON_SPORT_INPUT_ERRORS, **EXTENDED_SPORT_ERROR_CATALOG}.items():
        if normalize_text_for_match(alias) and normalize_text_for_match(alias) in normalized_question:
            if canonical in SPORT_COUNSELING_KNOWLEDGE and canonical not in detected:
                detected.append(canonical)

    return detected[:4]


def build_counseling_api_payload(user_question: str, detected_sports: List[str]) -> Dict[str, object]:
    relevant_knowledge = {
        sport: SPORT_COUNSELING_KNOWLEDGE[sport]
        for sport in detected_sports
        if sport in SPORT_COUNSELING_KNOWLEDGE
    }
    if not relevant_knowledge:
        relevant_knowledge = {"General": {"knowledge": "Sport not confidently detected. Ask the API to infer the sport and apply the closest federation / league / pathway model."}}

    return {
        "module": "sports_counseling_chat",
        "generator_version": "counseling_v5_elite_api_ready_chat_only",
        "api_status": "not_connected_yet",
        "system_prompt": COUNSELING_SYSTEM_PROMPT,
        "user_question": user_question,
        "detected_sports": detected_sports,
        "sport_knowledge": relevant_knowledge,
        "requested_output": {
            "format": "elite_structured_sports_counseling_answer",
            "tone": "clear, direct, intelligent, athlete-first",
            "depth": "elite",
            "must_include": [
                "direct answer",
                "sport pathway analysis",
                "competition / league / calendar logic",
                "realistic next steps",
                "risks and tradeoffs",
                "what must be verified live before acting",
            ],
            "live_research_needed_when_api_is_connected": True,
        },
    }


def render_detected_sport_knowledge(detected_sports: List[str]) -> None:
    if not detected_sports:
        st.info("Sportze.AI will infer the sport from the question when the AI API is connected.")
        return

    st.markdown("#### Detected sport knowledge base")
    for sport in detected_sports:
        data = SPORT_COUNSELING_KNOWLEDGE.get(sport, {})
        leagues = data.get("major_leagues", [])
        knowledge = data.get("knowledge", "")
        with st.expander(f"{sport} intelligence layer", expanded=len(detected_sports) == 1):
            if leagues:
                st.write("Major leagues / circuits / pathways:")
                st.write(", ".join(str(item) for item in leagues[:7]))
            if knowledge:
                st.write(str(knowledge))


def build_placeholder_counseling_response(user_question: str, detected_sports: List[str]) -> str:
    sport_label = ", ".join(detected_sports) if detected_sports else "the sport you described"
    return (
        f"I understood your counseling request about {sport_label}. The AI API is not connected yet, "
        "so this is not the final generated counseling answer. When connected, Sportze.AI will use the question, "
        "the sport knowledge base, live calendars/rankings where needed, and the elite counseling prompt to return "
        "a complete recommendation with pathway, competition logic, risks, tradeoffs, and next steps."
    )


def render_counseling_section() -> None:
    ensure_counseling_state()

    st.header("Sports Counseling")
    st.write("Elite AI-ready sports counseling. Ask one detailed question and the future API will generate the full answer.")

    col_a, col_b = st.columns([3, 1])
    with col_a:
        st.caption("Question: What sports counseling do you want today?")
    with col_b:
        if st.button("Reset chat", use_container_width=True, key="reset_counseling_chat_btn"):
            reset_counseling_flow()
            st.rerun()

    for message in st.session_state.counseling_messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_question = st.chat_input("What sports counseling do you want today?")

    if user_question:
        clean_question = user_question.strip()
        detected_sports = infer_sports_from_counseling_text(clean_question)
        payload = build_counseling_api_payload(clean_question, detected_sports)
        placeholder = build_placeholder_counseling_response(clean_question, detected_sports)

        st.session_state.counseling_messages.append({"role": "user", "content": clean_question})
        st.session_state.counseling_messages.append({"role": "assistant", "content": placeholder})
        st.session_state.counseling_api_payloads.append(payload)
        st.rerun()

    if not st.session_state.counseling_messages:
        st.markdown("### What sports counseling do you want today?")
        st.write(
            "Describe anything: tournament choice, professional pathway, college recruiting, Olympic route, "
            "league comparison, next career move, rankings, calendar strategy, or how to develop in your sport."
        )
        st.text_area(
            "Example style",
            value="I am a 14-year-old water polo player in Brazil. What pathway should I follow to reach NCAA, Europe, or the Olympics?",
            height=90,
            disabled=True,
        )

    latest_payload = st.session_state.counseling_api_payloads[-1] if st.session_state.counseling_api_payloads else None
    latest_sports = latest_payload.get("detected_sports", []) if latest_payload else []
    render_detected_sport_knowledge(list(latest_sports))

    with st.expander("Future API implementation payload", expanded=False):
        if latest_payload:
            st.json(latest_payload)
        else:
            st.json(
                {
                    "module": "sports_counseling_chat",
                    "api_status": "not_connected_yet",
                    "system_prompt": COUNSELING_SYSTEM_PROMPT,
                    "sports_available": list(SPORT_COUNSELING_KNOWLEDGE.keys()),
                    "note": "Once an API key/model is connected, send the user's question plus this knowledge base to the model.",
                }
            )
