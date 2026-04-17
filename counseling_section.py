
from __future__ import annotations

import io
import json
import re
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin

import streamlit as st

try:
    import requests
except Exception:  # pragma: no cover
    requests = None

try:
    from bs4 import BeautifulSoup
except Exception:  # pragma: no cover
    BeautifulSoup = None

try:
    from pypdf import PdfReader
except Exception:  # pragma: no cover
    PdfReader = None


# -----------------------------------------------------------------------------
# CONFIGURATION / API-READY PLACEHOLDERS
# -----------------------------------------------------------------------------
API_READY_CONFIG = {
    "enabled": False,
    "provider": None,
    "model": None,
    "reasoning_mode": None,
    "notes": "Prepared for future OpenAI / external reasoning integration, but not connected yet.",
}

HTTP_TIMEOUT = 20
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"
    )
}

OFFICIAL_TENNIS_SOURCES = {
    "ATP Tour": {
        "calendar_page": "https://www.atptour.com/en/tournaments",
        "calendar_pdf_guess": "https://www.atptour.com/-/media/files/calendar-pdfs/{year}/{year}-{next_short}-calendar.pdf",
        "fallback_pdf": "https://www.atptour.com/-/media/files/calendar-pdfs/{year}/{year}-atp-tour-calendar-december-{prev_year}.pdf",
    },
    "ATP Challenger": {
        "calendar_page": "https://www.atptour.com/en/atp-challenger-tour/calendar",
        "calendar_alt": "https://www.atptour.com/en/challenger-tour/calendar",
        "fallback_pdf": "https://www.atptour.com/-/media/files/calendar-pdfs/{year}/{year}-27-atp-challenger-calendar-as-of-11-february-{year}.pdf",
    },
    "ITF": {
        "calendar_page": "https://www.itftennis.com/en/tournament-calendar/mens-world-tennis-tour-calendar/",
    },
}

SPORT_CLASSIFICATION = {
    "Soccer": "team",
    "Football": "team",
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

DEFAULT_SPORT_OPTIONS = list(SPORT_CLASSIFICATION.keys()) + ["Other"]

TEAM_COUNTRY_HINTS = {
    "Brazil": "South America",
    "Argentina": "South America",
    "Portugal": "Europe",
    "Spain": "Europe",
    "England": "Europe",
    "Italy": "Europe",
    "Germany": "Europe",
    "France": "Europe",
    "United States": "North America",
}

TEAM_DESTINATION_OPTIONS = [
    "Brazil",
    "Portugal",
    "Spain",
    "England",
    "Italy",
    "Germany",
    "France",
    "United States",
    "Japan",
    "Saudi Arabia",
    "Qatar",
    "Other",
]

INDIVIDUAL_GOALS = [
    "Get match wins",
    "Build ranking",
    "Try a bigger event",
    "Come back with confidence",
    "Prepare for next tournament",
    "Other",
]

TENNIS_SURFACE_PROFILE: Dict[str, List[str]] = {
    "Clay": [
        "Longer rallies and more physical tolerance usually matter more.",
        "Heavy topspin and disciplined movement generally gain value.",
        "Good choice for players building resilience and match volume.",
    ],
    "Hard": [
        "Balanced surface that rewards solid first-strike patterns and all-around tennis.",
        "Usually the most transferable surface for broad development.",
        "Useful when the player wants a fair test without extreme conditions.",
    ],
    "Grass": [
        "Faster points and first-ball quality matter more.",
        "Serve, return position, reaction speed, and net comfort rise in value.",
        "Best when the player is confident in shorter-point execution.",
    ],
}

BUDGET_TO_DISTANCE = {
    "Low": "Prefer same country or short regional travel when possible.",
    "Medium": "Regional travel is realistic; one stronger option can be worth it if acceptance odds are still sensible.",
    "High": "Wider travel is possible, but recovery cost and acceptance probability should still beat prestige-only choices.",
}

OBJECTIVE_GUIDANCE = {
    "Get match wins": "Prioritize acceptance probability, manageable draw strength, and surface comfort.",
    "Try a bigger event": "Allow one ambitious option, but keep one safer backup where direct acceptance or qualifying is realistic.",
    "Build ranking": "Favor events with logical entry level, reduced travel stress, and a better chance to collect rounds.",
    "Come back with confidence": "Avoid chaotic long travel weeks and choose conditions that help rhythm and execution.",
    "Prepare for next tournament": "Choose a week that fits the next event rather than the most famous event.",
    "Other": "Use the written goal to guide the recommendation.",
}


# -----------------------------------------------------------------------------
# DATA STRUCTURES
# -----------------------------------------------------------------------------
@dataclass
class TennisTournament:
    source: str
    name: str
    city: str = ""
    country: str = ""
    category: str = ""
    surface: str = ""
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    url: str = ""
    confidence: str = "medium"
    notes: str = ""
    indoor: Optional[bool] = None


# -----------------------------------------------------------------------------
# GENERAL HELPERS
# -----------------------------------------------------------------------------
def build_future_api_payload(module_name: str, profile: Dict[str, object], context: Dict[str, object]) -> Dict[str, object]:
    return {
        "module": module_name,
        "profile": profile,
        "context": context,
        "generator_version": "counseling_v4_multi_sport_api_ready",
        "requested_output": {
            "format": "structured_counseling_recommendation",
            "needs_reasoning": True,
            "needs_live_sports_research": True,
            "needs_professional_tone": True,
            "needs_named_event_output_when_possible": True,
        },
        "api_status": "not_connected_yet",
    }


def safe_get(url: str) -> Tuple[Optional[str], Optional[bytes], Optional[str]]:
    if requests is None:
        return None, None, "requests_not_installed"
    try:
        response = requests.get(url, headers=DEFAULT_HEADERS, timeout=HTTP_TIMEOUT)
        response.raise_for_status()
        content_type = response.headers.get("Content-Type", "")
        if "application/pdf" in content_type or url.lower().endswith(".pdf"):
            return None, response.content, None
        return response.text, None, None
    except Exception as exc:
        return None, None, str(exc)


def today_local() -> date:
    return datetime.now().date()


def next_week_window(reference: Optional[date] = None) -> Tuple[date, date]:
    base = reference or today_local()
    days_until_next_monday = (7 - base.weekday()) % 7
    if days_until_next_monday == 0:
        days_until_next_monday = 7
    start = base + timedelta(days=days_until_next_monday)
    end = start + timedelta(days=6)
    return start, end


def format_date_range(start: Optional[date], end: Optional[date]) -> str:
    if start and end:
        if start == end:
            return start.strftime("%d %b %Y")
        return f"{start.strftime('%d %b %Y')} → {end.strftime('%d %b %Y')}"
    if start:
        return start.strftime("%d %b %Y")
    return "Date not confirmed"


def parse_date_flex(raw: str) -> Optional[date]:
    raw = (raw or "").strip()
    if not raw:
        return None
    patterns = [
        "%Y-%m-%d",
        "%d %b %Y",
        "%d %B %Y",
        "%b %d, %Y",
        "%B %d, %Y",
        "%d/%m/%Y",
    ]
    for fmt in patterns:
        try:
            return datetime.strptime(raw, fmt).date()
        except Exception:
            continue
    return None


def normalize_surface(raw: str) -> str:
    value = (raw or "").strip().lower()
    mapping = {
        "h": "Hard",
        "hard": "Hard",
        "ih": "Indoor Hard",
        "indoor hard": "Indoor Hard",
        "cl": "Clay",
        "clay": "Clay",
        "g": "Grass",
        "grass": "Grass",
    }
    return mapping.get(value, raw.strip().title() if raw else "")


def infer_surface_fit(preferred_surface: str, tournament_surface: str) -> str:
    if not tournament_surface:
        return "Unknown"
    p = preferred_surface.strip().lower()
    t = tournament_surface.strip().lower()
    if p in t:
        return "Strong fit"
    if p == "hard" and t in ["indoor hard", "ih", "hard"]:
        return "Strong fit"
    if p == "grass" and t in ["g", "grass"]:
        return "Strong fit"
    if p == "clay" and t in ["cl", "clay"]:
        return "Strong fit"
    return "Secondary fit"


def estimate_entry_fit(ranking: int, category: str) -> str:
    category_lower = category.lower()
    if "atp masters" in category_lower or "grand slam" in category_lower or "atp 500" in category_lower:
        return "Very ambitious unless ranking and acceptance status are already high."
    if "atp 250" in category_lower:
        if ranking <= 200:
            return "Possible depending on the week and acceptance list strength."
        if ranking <= 400:
            return "Usually ambitious; qualifying or alternate scenarios matter more."
        return "Generally unrealistic without special entry circumstances."
    if "challenger 175" in category_lower or "challenger 125" in category_lower:
        if ranking <= 220:
            return "Competitive option if form is good."
        if ranking <= 400:
            return "Possible in some weeks, but not always safe."
        return "Often aggressive unless the draw is unusually soft."
    if "challenger" in category_lower:
        if ranking <= 250:
            return "Good developmental option if the surface and travel make sense."
        if ranking <= 600:
            return "Worth checking; acceptance and qualifying remain important."
        return "Possible only in softer weeks or qualifying pathways."
    if "m25" in category_lower or "m15" in category_lower or "itf" in category_lower:
        if ranking <= 350:
            return "Usually below your strongest level unless you need confidence, matches, or a very specific schedule fit."
        if ranking <= 900:
            return "Solid level for realistic match opportunities and point building."
        return "Often the most practical level for acceptance and match volume."
    return "Check acceptance list, qualifying cutoffs, and withdrawal patterns."


def score_tournament(
    tournament: TennisTournament,
    ranking: int,
    preferred_surface: str,
    travel_budget: str,
    objective: str,
    location: str,
) -> Tuple[int, List[str]]:
    score = 50
    reasons: List[str] = []

    fit = infer_surface_fit(preferred_surface, tournament.surface)
    if fit == "Strong fit":
        score += 15
        reasons.append(f"Surface fit looks strong for a {preferred_surface}-leaning player.")
    elif fit == "Secondary fit":
        score += 5
        reasons.append("Surface is playable, but not the ideal profile match.")
    else:
        reasons.append("Surface fit is not fully confirmed yet.")

    entry_message = estimate_entry_fit(ranking, tournament.category)
    if "Good" in entry_message or "Solid" in entry_message or "Possible" in entry_message:
        score += 12
    elif "ambitious" in entry_message.lower() or "unrealistic" in entry_message.lower():
        score -= 10
    reasons.append(entry_message)

    if objective == "Get match wins":
        if "ITF" in tournament.source or "M15" in tournament.category.upper() or "M25" in tournament.category.upper() or "Challenger" in tournament.category:
            score += 8
            reasons.append("This level can be better for immediate win probability than prestige-only choices.")
    elif objective == "Try a bigger event":
        if "ATP Tour" in tournament.source or "ATP 250" in tournament.category or "Challenger 125" in tournament.category:
            score += 10
            reasons.append("This option supports an ambition-oriented week.")
    elif objective == "Build ranking":
        if "ITF" in tournament.source or "Challenger 50" in tournament.category or "Challenger 75" in tournament.category:
            score += 10
            reasons.append("This type of event can be more logical for controlled point building.")
    elif objective == "Come back with confidence":
        score += 5
        reasons.append("For a confidence week, controlled conditions matter more than maximum tournament prestige.")
    elif objective == "Prepare for next tournament":
        score += 5
        reasons.append("Preparation weeks should serve the next event, not just the biggest name on the calendar.")

    if tournament.country and location.strip():
        location_l = location.lower()
        if tournament.country.lower() in location_l:
            score += 6
            reasons.append("This event is in your current country, which improves travel simplicity.")
        elif travel_budget == "Low":
            score -= 6
            reasons.append("Low-budget mode penalizes longer travel unless the fit is clearly superior.")

    if travel_budget == "Low":
        score += 3
        reasons.append("Low-budget mode favors nearby, simpler travel plans.")
    elif travel_budget == "High":
        score += 2
        reasons.append("Higher travel budget gives flexibility, but not a free pass to choose the hardest event.")

    if tournament.confidence == "high":
        score += 5
        reasons.append("Event naming confidence is high.")
    elif tournament.confidence == "medium":
        score += 1
        reasons.append("Event was identified with medium confidence.")
    elif tournament.confidence == "low":
        score -= 8
        reasons.append("Event details were found with lower confidence and should be double-checked manually.")

    return score, reasons


def get_profile_source() -> Dict[str, object]:
    """
    Reads profile-like answers saved elsewhere in the app.
    This is intentionally broad so it can work with current or future homepage keys.
    """
    candidates = [
        "athlete_profile",
        "profile",
        "homepage_profile",
        "home_profile",
        "user_profile",
        "sportze_profile",
    ]
    for key in candidates:
        value = st.session_state.get(key)
        if isinstance(value, dict):
            return value
    return {}


def get_profile_value(*keys: str) -> Optional[object]:
    profile = get_profile_source()
    for key in keys:
        if key in profile and profile.get(key) not in [None, "", [], {}]:
            return profile.get(key)
        if key in st.session_state and st.session_state.get(key) not in [None, "", [], {}]:
            return st.session_state.get(key)
    return None


def detect_sport_type(sport_name: str) -> str:
    if not sport_name:
        return "unknown"
    return SPORT_CLASSIFICATION.get(sport_name.strip().title(), "unknown")


def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    if PdfReader is None:
        return ""
    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception:
        return ""


def _clean_event_name(name: str) -> str:
    value = re.sub(r"\s+", " ", (name or "")).strip(" -|")
    value = re.sub(r"(?i)\b(atp challenger tour|atp challenger)\b", "", value).strip(" -|")
    return value


# -----------------------------------------------------------------------------
# IMPROVED OFFICIAL TENNIS EXTRACTION
# -----------------------------------------------------------------------------
MONTHS = {
    "JAN": 1, "FEB": 2, "MAR": 3, "APR": 4, "MAY": 5, "JUN": 6,
    "JUL": 7, "AUG": 8, "SEP": 9, "OCT": 10, "NOV": 11, "DEC": 12,
}


def parse_day_month(token: str, year: int) -> Optional[date]:
    token = token.strip().upper()
    match = re.match(r"(\d{1,2})-([A-Z]{3})", token)
    if not match:
        return None
    day = int(match.group(1))
    month = MONTHS.get(match.group(2))
    if not month:
        return None
    try:
        return date(year, month, day)
    except Exception:
        return None


def discover_pdf_links_from_page(page_url: str) -> Tuple[List[str], List[str]]:
    html, _, err = safe_get(page_url)
    if err or not html:
        return [], [f"Could not load calendar page for PDF discovery: {err}"]

    pdfs = []
    for match in re.finditer(r'href="([^"]+\.pdf[^"]*)"', html, flags=re.IGNORECASE):
        candidate = urljoin(page_url, match.group(1))
        if candidate not in pdfs:
            pdfs.append(candidate)

    if not pdfs and BeautifulSoup is not None:
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup.find_all("a", href=True):
            href = tag.get("href", "")
            if ".pdf" in href.lower():
                candidate = urljoin(page_url, href)
                if candidate not in pdfs:
                    pdfs.append(candidate)

    warnings = []
    if not pdfs:
        warnings.append("The official page loaded, but no direct PDF links were exposed in the returned HTML.")
    return pdfs, warnings


def build_guess_pdf_urls(year: int) -> List[str]:
    next_short = str(year + 1)[-2:]
    return [
        OFFICIAL_TENNIS_SOURCES["ATP Tour"]["calendar_pdf_guess"].format(year=year, next_short=next_short),
        OFFICIAL_TENNIS_SOURCES["ATP Tour"]["fallback_pdf"].format(year=year, prev_year=year - 1),
        OFFICIAL_TENNIS_SOURCES["ATP Challenger"]["fallback_pdf"].format(year=year),
    ]


def _extract_named_events_from_pdf_text(text: str, source_name: str, week_start: date, week_end: date, url: str) -> List[TennisTournament]:
    tournaments: List[TennisTournament] = []
    lines = [re.sub(r"\s+", " ", line).strip() for line in text.splitlines() if line.strip()]

    atp_like = re.compile(
        r"(?P<date>\d{1,2}-[A-Z]{3})\s+(?P<city>[A-ZÀ-ÿ'.,\- ]{2,})\s+"
        r"(?P<category>ATP 250|ATP 500|ATP MASTERS 1000|GRAND SLAM|DAVIS CUP|LAVER CUP|ATP FINALS|NEXT GEN ATP FINALS)\s+"
        r"(?P<name>[A-ZÀ-ÿ0-9'&.,\- ]{4,}?)\s+(?P<surface>IH|H|CL|G)$"
    )

    challenger_like = re.compile(
        r"(?P<week>\d{1,2})\s+(?P<date>\d{1,2}-[A-Z]{3})\s+(?P<name>[A-Za-zÀ-ÿ0-9'&.\- ]{3,}?)\s+"
        r"(?P<city>[A-Za-zÀ-ÿ' .\-]+)\s+(?P<country>[A-Z]{3})\s+(?P<cat>\d{2,3})"
    )

    for line in lines:
        match = atp_like.search(line)
        if match:
            start = parse_day_month(match.group("date"), week_start.year)
            if not start or not (week_start <= start <= week_end):
                continue
            tournaments.append(
                TennisTournament(
                    source=source_name,
                    name=_clean_event_name(match.group("name").title()),
                    city=match.group("city").strip().title(),
                    category=match.group("category").strip().replace("ATP MASTERS 1000", "ATP Masters 1000"),
                    surface=normalize_surface(match.group("surface")),
                    start_date=start,
                    end_date=start + timedelta(days=6),
                    url=url,
                    confidence="high",
                    notes=f"Named event parsed from official {source_name} PDF.",
                )
            )
            continue

        match = challenger_like.search(line)
        if match:
            start = parse_day_month(match.group("date"), week_start.year)
            if not start or not (week_start <= start <= week_end):
                continue
            raw_name = _clean_event_name(match.group("name"))
            city = match.group("city").strip()
            if not raw_name or raw_name.lower() == city.lower():
                raw_name = f"ATP Challenger {city}"
            tournaments.append(
                TennisTournament(
                    source=source_name,
                    name=raw_name,
                    city=city,
                    country=match.group("country").strip(),
                    category=f"Challenger {match.group('cat').strip()}",
                    start_date=start,
                    end_date=start + timedelta(days=6),
                    url=url,
                    confidence="medium",
                    notes=f"Named event parsed from official {source_name} PDF.",
                )
            )
    return tournaments


def fetch_tennis_events_from_official_pdfs(week_start: date, week_end: date) -> Tuple[List[TennisTournament], List[str]]:
    year = week_start.year
    urls, warnings = discover_pdf_links_from_page(OFFICIAL_TENNIS_SOURCES["ATP Tour"]["calendar_page"])
    challenger_urls, challenger_warnings = discover_pdf_links_from_page(OFFICIAL_TENNIS_SOURCES["ATP Challenger"]["calendar_page"])
    warnings.extend(challenger_warnings)
    urls.extend(challenger_urls)

    for guessed in build_guess_pdf_urls(year):
        if guessed not in urls:
            urls.append(guessed)

    tournaments: List[TennisTournament] = []
    seen_urls = set()

    for url in urls:
        if not url or url in seen_urls:
            continue
        seen_urls.add(url)

        _, pdf_bytes, err = safe_get(url)
        if err or not pdf_bytes:
            continue

        text = extract_text_from_pdf_bytes(pdf_bytes)
        if not text:
            continue

        source_name = "ATP Challenger" if "challenger" in url.lower() else "ATP Tour"
        tournaments.extend(_extract_named_events_from_pdf_text(text, source_name, week_start, week_end, url))

    if not tournaments:
        warnings.append("Official PDFs were checked, but no named event for next week could be extracted from the current file text.")
    return tournaments, warnings


def fetch_itf_events_from_html(week_start: date, week_end: date) -> Tuple[List[TennisTournament], List[str]]:
    html, _, err = safe_get(OFFICIAL_TENNIS_SOURCES["ITF"]["calendar_page"])
    if err or not html:
        return [], [f"ITF calendar fetch issue: {err}"]

    warnings: List[str] = []
    tournaments: List[TennisTournament] = []

    # First pass: if official HTML exposes readable cards with M15/M25/M50 or similar.
    pattern = re.compile(
        r"\b(?P<category>M15|M25|M50|M75|M100)\s+(?P<name>[A-Za-zÀ-ÿ0-9'&.\- ]+?)(?:\s*[,\-]\s*(?P<country>[A-Za-zÀ-ÿ .\-']+))?(?=\s{2,}|<|$)"
    )
    for match in pattern.finditer(html):
        category = match.group("category").strip()
        raw_name = _clean_event_name(match.group("name"))
        country = (match.group("country") or "").strip()
        city = raw_name
        tournaments.append(
            TennisTournament(
                source="ITF",
                name=f"{category} {raw_name}",
                city=city,
                country=country,
                category=category,
                start_date=week_start,
                end_date=week_end,
                url=OFFICIAL_TENNIS_SOURCES["ITF"]["calendar_page"],
                confidence="medium",
                notes="Named event found from official ITF calendar HTML fallback.",
            )
        )

    if not tournaments and BeautifulSoup is not None:
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(" ", strip=True)
        for match in pattern.finditer(text):
            category = match.group("category").strip()
            raw_name = _clean_event_name(match.group("name"))
            country = (match.group("country") or "").strip()
            tournaments.append(
                TennisTournament(
                    source="ITF",
                    name=f"{category} {raw_name}",
                    city=raw_name,
                    country=country,
                    category=category,
                    start_date=week_start,
                    end_date=week_end,
                    url=OFFICIAL_TENNIS_SOURCES["ITF"]["calendar_page"],
                    confidence="low",
                    notes="Named event found from official ITF page text fallback.",
                )
            )

    if not tournaments:
        warnings.append("ITF official page loaded, but named tournaments were not exposed clearly enough for the current parser.")
    return tournaments, warnings


def deduplicate_tournaments(tournaments: List[TennisTournament]) -> List[TennisTournament]:
    unique: List[TennisTournament] = []
    seen = set()
    for event in tournaments:
        key = (
            event.source.lower(),
            event.name.lower().strip(),
            event.city.lower().strip(),
            event.country.lower().strip(),
            event.category.lower().strip(),
            event.start_date.isoformat() if event.start_date else "",
        )
        if key in seen:
            continue
        seen.add(key)
        unique.append(event)
    return unique


def load_next_week_tournaments(reference_date: Optional[date] = None) -> Tuple[List[TennisTournament], List[str], Tuple[date, date]]:
    week_start, week_end = next_week_window(reference_date)
    warnings: List[str] = []
    all_events: List[TennisTournament] = []

    pdf_events, pdf_warnings = fetch_tennis_events_from_official_pdfs(week_start, week_end)
    all_events.extend(pdf_events)
    warnings.extend(pdf_warnings)

    itf_events, itf_warnings = fetch_itf_events_from_html(week_start, week_end)
    all_events.extend(itf_events)
    warnings.extend(itf_warnings)

    return deduplicate_tournaments(all_events), warnings, (week_start, week_end)


# -----------------------------------------------------------------------------
# CHAT-STYLE MULTI-SPORT COUNSELING FLOW
# -----------------------------------------------------------------------------
def ensure_counseling_state() -> None:
    if "counseling_chat_answers" not in st.session_state:
        st.session_state.counseling_chat_answers = {}
    if "counseling_chat_history" not in st.session_state:
        st.session_state.counseling_chat_history = []
    if "counseling_flow_version" not in st.session_state:
        st.session_state.counseling_flow_version = "v4"


def reset_counseling_flow() -> None:
    st.session_state.counseling_chat_answers = {}
    st.session_state.counseling_chat_history = []


def push_chat(question: str, answer: str, key: str) -> None:
    st.session_state.counseling_chat_answers[key] = answer
    st.session_state.counseling_chat_history.append({"question": question, "answer": answer, "key": key})


def get_saved_or_profile_value(key: str, *profile_keys: str) -> Optional[object]:
    answers = st.session_state.get("counseling_chat_answers", {})
    if key in answers and answers.get(key) not in [None, "", [], {}]:
        return answers.get(key)
    return get_profile_value(*profile_keys)


def render_chat_history() -> None:
    history = st.session_state.get("counseling_chat_history", [])
    for item in history:
        with st.chat_message("assistant"):
            st.write(item["question"])
        with st.chat_message("user"):
            st.write(item["answer"])


def ask_chat_question(question: str, answer_key: str, profile_keys: Tuple[str, ...] = ()) -> Optional[str]:
    existing = get_saved_or_profile_value(answer_key, *profile_keys)
    if existing not in [None, "", [], {}]:
        if answer_key not in st.session_state.counseling_chat_answers:
            push_chat(question, str(existing), answer_key)
        return str(existing)

    with st.chat_message("assistant"):
        st.write(question)

    answer = st.chat_input("Type your answer and press Enter", key=f"chat_input_{answer_key}")
    if answer:
        push_chat(question, answer.strip(), answer_key)
        st.rerun()
    return None


def sport_selector_value() -> Optional[str]:
    existing = get_saved_or_profile_value("sport", "sport", "main_sport", "selected_sport")
    if existing not in [None, "", [], {}]:
        return str(existing)

    st.markdown("### Sport")
    selected = st.selectbox(
        "What sport?",
        DEFAULT_SPORT_OPTIONS,
        index=0,
        key="counseling_sport_selector",
    )
    if st.button("Confirm sport", key="confirm_counseling_sport", use_container_width=True):
        push_chat("What sport?", selected, "sport")
        st.rerun()
    return None


def professional_status_value() -> Optional[str]:
    existing = get_saved_or_profile_value("professional_status", "professional_status", "is_professional", "level")
    if existing not in [None, "", [], {}]:
        return str(existing)
    st.markdown("### Athlete level")
    selected = st.selectbox(
        "Are you professional?",
        ["No", "Semi-professional", "Yes"],
        index=0,
        key="counseling_professional_selector",
    )
    if st.button("Confirm athlete level", key="confirm_counseling_professional", use_container_width=True):
        push_chat("Are you professional?", selected, "professional_status")
        st.rerun()
    return None


def build_required_flow(sport: str, sport_type: str) -> List[Tuple[str, str, Tuple[str, ...]]]:
    flow: List[Tuple[str, str, Tuple[str, ...]]] = []

    if not get_profile_value("sport", "main_sport", "selected_sport"):
        flow.append(("What sport?", "sport", ("sport", "main_sport", "selected_sport")))

    if not get_profile_value("professional_status", "is_professional", "level"):
        flow.append(("Are you professional?", "professional_status", ("professional_status", "is_professional", "level")))

    if sport_type == "team":
        flow.extend(
            [
                ("Which team are you in now?", "current_team", ("current_team", "team", "club")),
                ("Your age?", "age", ("age",)),
                ("Where do you want to go to?", "target_country", ("target_country", "desired_country")),
            ]
        )
    elif sport_type == "individual":
        flow.extend(
            [
                ("Where are you now?", "current_location", ("current_location", "location", "country")),
                ("Your ranking?", "ranking", ("ranking", "current_ranking")),
                ("What's your goal for next week?", "goal_next_week", ("goal_next_week", "main_goal")),
            ]
        )

        if sport.strip().lower() == "tennis":
            flow.extend(
                [
                    ("Preferred surface?", "preferred_surface", ("preferred_surface",)),
                    ("Travel budget for next week?", "travel_budget", ("travel_budget",)),
                ]
            )
    else:
        flow.extend(
            [
                ("Where are you now?", "current_location", ("current_location", "location", "country")),
                ("Tell me your current level.", "current_level", ("current_level", "level")),
                ("What's your goal for next week?", "goal_next_week", ("goal_next_week", "main_goal")),
            ]
        )

    return flow


def render_special_inputs_if_needed(key: str) -> bool:
    if key == "preferred_surface":
        existing = get_saved_or_profile_value("preferred_surface", "preferred_surface")
        if existing not in [None, "", [], {}]:
            if "preferred_surface" not in st.session_state.counseling_chat_answers:
                push_chat("Preferred surface?", str(existing), "preferred_surface")
            return True

        choice = st.selectbox("Preferred surface?", list(TENNIS_SURFACE_PROFILE.keys()), key="counseling_surface_select")
        if st.button("Confirm preferred surface", key="confirm_surface", use_container_width=True):
            push_chat("Preferred surface?", choice, "preferred_surface")
            st.rerun()
        return True

    if key == "travel_budget":
        existing = get_saved_or_profile_value("travel_budget", "travel_budget")
        if existing not in [None, "", [], {}]:
            if "travel_budget" not in st.session_state.counseling_chat_answers:
                push_chat("Travel budget for next week?", str(existing), "travel_budget")
            return True

        choice = st.selectbox("Travel budget for next week?", ["Low", "Medium", "High"], key="counseling_budget_select")
        if st.button("Confirm travel budget", key="confirm_budget", use_container_width=True):
            push_chat("Travel budget for next week?", choice, "travel_budget")
            st.rerun()
        return True

    return False


def collect_counseling_answers() -> Tuple[Optional[str], str, Dict[str, object], bool]:
    ensure_counseling_state()

    render_chat_history()

    sport = sport_selector_value()
    if not sport:
        return None, "unknown", {}, False

    sport_type = detect_sport_type(sport)

    prof = professional_status_value()
    if not prof:
        return sport, sport_type, {}, False

    required = build_required_flow(sport, sport_type)
    collected: Dict[str, object] = {"sport": sport, "sport_type": sport_type, "professional_status": prof}

    for question, key, profile_keys in required:
        if key in {"sport", "professional_status"}:
            continue

        if render_special_inputs_if_needed(key):
            value = get_saved_or_profile_value(key, *profile_keys)
            if value in [None, "", [], {}]:
                return sport, sport_type, collected, False
            collected[key] = value
            continue

        answer = ask_chat_question(question, key, profile_keys)
        if answer is None:
            return sport, sport_type, collected, False
        collected[key] = answer

    return sport, sport_type, collected, True


# -----------------------------------------------------------------------------
# TENNIS COUNSELING
# -----------------------------------------------------------------------------
def build_tennis_profile(collected: Dict[str, object]) -> Dict[str, object]:
    ranking_raw = str(collected.get("ranking", "9999")).strip()
    ranking = int(re.sub(r"[^\d]", "", ranking_raw) or "9999")

    goal = str(collected.get("goal_next_week", "")).strip()
    if goal not in INDIVIDUAL_GOALS:
        mapped_goal = "Other"
    else:
        mapped_goal = goal

    return {
        "ranking": ranking,
        "location": str(collected.get("current_location", "")),
        "preferred_surface": str(collected.get("preferred_surface", "Hard")),
        "travel_budget": str(collected.get("travel_budget", "Medium")),
        "objective": mapped_goal,
        "written_goal": goal,
    }


def render_tournament_card(event: TennisTournament, ranking: int, preferred_surface: str, travel_budget: str, objective: str, location: str) -> None:
    score, reasons = score_tournament(event, ranking, preferred_surface, travel_budget, objective, location)
    title = f"{event.name} — {event.city}{', ' + event.country if event.country else ''}"
    with st.container(border=True):
        st.markdown(f"### {title}")
        cols = st.columns(4)
        cols[0].metric("Category", event.category or "TBC")
        cols[1].metric("Surface", event.surface or "TBC")
        cols[2].metric("Week", format_date_range(event.start_date, event.end_date))
        cols[3].metric("Fit score", f"{score}/100")

        st.write(f"**Source:** {event.source}")
        if event.notes:
            st.caption(event.notes)
        for reason in reasons[:5]:
            st.write(f"- {reason}")
        if event.url:
            st.markdown(f"[Official page]({event.url})")


def render_tennis_counseling_from_flow(collected: Dict[str, object]) -> None:
    tennis_profile = build_tennis_profile(collected)
    ranking = int(tennis_profile["ranking"])
    location = str(tennis_profile["location"])
    preferred_surface = str(tennis_profile["preferred_surface"])
    travel_budget = str(tennis_profile["travel_budget"])
    objective = str(tennis_profile["objective"])

    st.info(
        f"Travel framework: {BUDGET_TO_DISTANCE.get(travel_budget, BUDGET_TO_DISTANCE['Medium'])}\n\n"
        f"Objective lens: {OBJECTIVE_GUIDANCE.get(objective, OBJECTIVE_GUIDANCE['Other'])}"
    )

    with st.expander("Surface profile guidance", expanded=False):
        for line in TENNIS_SURFACE_PROFILE.get(preferred_surface, []):
            st.write(f"- {line}")

    if st.button("Get counseling advice", type="primary", use_container_width=True, key="run_tennis_counseling"):
        profile = build_tennis_profile(collected)
        context: Dict[str, object] = {"calendar_mode": "official_sources_following_week_named_events"}

        with st.spinner("Checking official ATP, Challenger, and ITF sources for next week's named tournaments..."):
            tournaments, warnings, week_range = load_next_week_tournaments()

        context["next_week_window"] = [week_range[0].isoformat(), week_range[1].isoformat()]
        context["found_tournaments"] = len(tournaments)
        future_payload = build_future_api_payload("tennis_counseling", profile, context)

        st.markdown(f"## Recommended target week: {format_date_range(week_range[0], week_range[1])}")

        if ranking <= 150:
            st.write("- You can be selective and look for stronger point opportunities, but only when the surface, travel, and draw logic still make sense.")
        elif ranking <= 600:
            st.write("- You are in a zone where event selection matters a lot: acceptance reality, first-round opportunity, and travel cost should beat pure prestige.")
        else:
            st.write("- Prioritize realistic acceptance, manageable travel, and match volume over chasing an event name that does not fit the week.")

        if tournaments:
            scored = []
            for event in tournaments:
                score, _ = score_tournament(event, ranking, preferred_surface, travel_budget, objective, location)
                scored.append((score, event))
            scored.sort(key=lambda x: x[0], reverse=True)

            best_named = scored[0][1]
            st.success(
                f"Primary named recommendation for next week: {best_named.name}"
                f"{' in ' + best_named.city if best_named.city else ''}"
                f"{', ' + best_named.country if best_named.country else ''}."
            )

            st.subheader("Top tournament suggestions for next week")
            for _, event in scored[:6]:
                render_tournament_card(event, ranking, preferred_surface, travel_budget, objective, location)
        else:
            st.warning(
                "No named tournament was confirmed from the current official source structure. "
                "The improved version now checks official ATP and Challenger PDFs plus the ITF page, "
                "but if those official structures change again, the selectors may need another adjustment."
            )

        st.subheader("Professional decision checklist")
        checklist = [
            "Check direct acceptance, qualifying cutoffs, and withdrawal patterns before committing to travel.",
            "Do not choose a harder tournament only because of the name if the realistic match value is lower.",
            "Compare surface fit, travel fatigue, and current form at the same time rather than separately.",
            "Have one primary target and one backup event when the week matters.",
        ]
        for item in checklist:
            st.write(f"- {item}")

        if warnings:
            with st.expander("Calendar fetch diagnostics", expanded=False):
                for warning in warnings[:20]:
                    st.write(f"- {warning}")

        with st.expander("Future API integration preview", expanded=False):
            st.json(future_payload)
            st.caption("Prepared for future reasoning/API implementation, but no API is connected yet.")


# -----------------------------------------------------------------------------
# GENERIC TEAM / INDIVIDUAL COUNSELING
# -----------------------------------------------------------------------------
def render_team_sport_counseling(collected: Dict[str, object]) -> None:
    sport = str(collected.get("sport", "Team sport"))
    current_team = str(collected.get("current_team", ""))
    age_raw = str(collected.get("age", "")).strip()
    target_country = str(collected.get("target_country", ""))
    professional_status = str(collected.get("professional_status", ""))

    try:
        age = int(re.sub(r"[^\d]", "", age_raw) or "0")
    except Exception:
        age = 0

    current_continent_hint = TEAM_COUNTRY_HINTS.get(target_country, "Unknown")

    profile = {
        "sport": sport,
        "sport_type": "team",
        "current_team": current_team,
        "age": age,
        "target_country": target_country,
        "professional_status": professional_status,
    }

    payload = build_future_api_payload(
        f"{sport.lower().replace(' ', '_')}_team_counseling",
        profile,
        {
            "reasoning_mode": "multi_sport_team_pathway",
            "future_api_tasks": [
                "detect current team country",
                "detect division and competition quality",
                "search realistic target markets",
                "evaluate transfer logic by age and level",
            ],
        },
    )

    st.subheader(f"{sport} counseling")
    st.success(
        f"Pathway focus: move only if the next environment improves your level, playing opportunity, and long-term pathway more than your current one."
    )

    st.write(f"- Current team: {current_team or 'Not provided'}")
    st.write(f"- Age: {age if age else 'Not confirmed'}")
    st.write(f"- Target destination: {target_country or 'Not provided'}")
    st.write(f"- Current level marker: {professional_status or 'Not provided'}")

    guidance = [
        "For team sports, the future API should identify your current club, country, competition level, and realistic next markets automatically.",
        "Age matters a lot: younger athletes should prioritize pathway, coaching quality, and minutes over club name.",
        "If the move is international, adaptation, language, registration timing, and match opportunity need to be stronger than the prestige factor.",
        "The smartest move is usually the one that improves your next move too, not only your current headline.",
    ]
    for item in guidance:
        st.write(f"- {item}")

    st.info(
        f"API-ready note: when connected, this section can detect the country and level of {current_team or 'your current team'} and compare it with target opportunities in {target_country or 'your destination market'}."
    )
    st.caption(f"Target market continent hint: {current_continent_hint}")

    with st.expander("Future API integration preview", expanded=False):
        st.json(payload)
        st.caption("Prepared for future reasoning/API implementation, but no API is connected yet.")


def render_individual_generic_counseling(collected: Dict[str, object]) -> None:
    sport = str(collected.get("sport", "Individual sport"))
    profile = {
        "sport": sport,
        "sport_type": "individual",
        "current_location": str(collected.get("current_location", "")),
        "ranking": str(collected.get("ranking", "")),
        "goal_next_week": str(collected.get("goal_next_week", "")),
        "professional_status": str(collected.get("professional_status", "")),
    }
    payload = build_future_api_payload(
        f"{sport.lower().replace(' ', '_')}_individual_counseling",
        profile,
        {
            "reasoning_mode": "multi_sport_individual_pathway",
            "future_api_tasks": [
                "search next week's relevant competitions",
                "classify event level",
                "compare event fit to athlete ranking and goal",
            ],
        },
    )

    st.subheader(f"{sport} counseling")
    st.success(
        "This flow is now prepared for future API integration: it already collects the right athlete context first, then it can later attach live event logic sport by sport."
    )

    st.write(f"- Current location: {profile['current_location'] or 'Not provided'}")
    st.write(f"- Ranking / level marker: {profile['ranking'] or 'Not provided'}")
    st.write(f"- Goal for next week: {profile['goal_next_week'] or 'Not provided'}")
    st.write(f"- Current level marker: {profile['professional_status'] or 'Not provided'}")

    for item in [
        "For individual sports, the recommendation should be based on where you are now, your current level, and what next week needs to achieve.",
        "When the API is connected, this section can search named competitions, compare event level, and suggest the smartest event instead of only giving generic advice.",
        "The next recommendation should always balance prestige, realistic entry, travel cost, recovery, and developmental value.",
    ]:
        st.write(f"- {item}")

    with st.expander("Future API integration preview", expanded=False):
        st.json(payload)
        st.caption("Prepared for future reasoning/API implementation, but no API is connected yet.")


# -----------------------------------------------------------------------------
# SECTION ROOT
# -----------------------------------------------------------------------------
def render_counseling_section() -> None:
    st.header("Counseling")
    st.write(
        "Professional multi-sport counseling with chat-style intake, homepage/profile memory support, and stronger tennis tournament naming logic."
    )

    col_a, col_b = st.columns([1, 1])
    with col_a:
        st.caption("If the homepage already collected the sport/profile, this section uses it and skips repeated questions.")
    with col_b:
        if st.button("Reset counseling flow", use_container_width=True, key="reset_counseling_flow_btn"):
            reset_counseling_flow()
            st.rerun()

    sport, sport_type, collected, is_complete = collect_counseling_answers()
    if not sport:
        return

    if not is_complete:
        st.info("Answer the remaining questions above. The full counseling result will only appear after the whole intake is finished.")
        return

    if sport.strip().lower() == "tennis":
        render_tennis_counseling_from_flow(collected)
        return

    if sport_type == "team":
        render_team_sport_counseling(collected)
    else:
        render_individual_generic_counseling(collected)
