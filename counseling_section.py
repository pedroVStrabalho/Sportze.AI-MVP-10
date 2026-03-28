from __future__ import annotations

import io
import json
import re
from dataclasses import dataclass, asdict
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional, Tuple

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
        "calendar_pdf": "https://www.atptour.com/-/media/files/calendar-pdfs/{year}/{year}-atp-tour-calendar-december-{prev_year}.pdf",
        "news_page": "https://www.atptour.com/en/news/what-is-the-{year}-atp-tour-calendar",
        "tournaments": "https://www.atptour.com/en/tournaments",
    },
    "ATP Challenger": {
        "calendar_html": "https://www.atptour.com/en/atp-challenger-tour/calendar",
        "calendar_alt": "https://www.atptour.com/en/challenger-tour/calendar",
        "calendar_pdf": "https://www.atptour.com/-/media/files/calendar-pdfs/{year}/{year}-27-atp-challenger-calendar-as-of-11-february-{year}.pdf",
    },
    "ITF": {
        "calendar_html": "https://www.itftennis.com/en/tournament-calendar/mens-world-tennis-tour-calendar/",
        "tour_home": "https://www.itftennis.com/en/itf-tours/mens-world-tennis-tour/",
    },
}

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

BUDGET_TO_DISTANCE = {
    "Low": "Prefer same country or short regional travel when possible.",
    "Medium": "Regional travel is realistic; one stronger option can be worth it if acceptance odds are still sensible.",
    "High": "Wider travel is possible, but recovery cost and acceptance probability should still beat prestige-only choices.",
}

OBJECTIVE_GUIDANCE = {
    "Get match wins": "Prioritize acceptance probability, manageable draw strength, and surface comfort.",
    "Try a bigger event": "Allow one ambitious option, but keep one safer backup where direct acceptance or qualifying is realistic.",
    "Build points safely": "Favor events with a logical entry level, reduced travel stress, and a better chance to collect rounds.",
    "Come back with confidence": "Avoid chaotic long travel weeks and choose conditions that help rhythm and execution.",
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


# -----------------------------------------------------------------------------
# GENERAL HELPERS
# -----------------------------------------------------------------------------
def build_future_api_payload(module_name: str, profile: Dict[str, object], context: Dict[str, object]) -> Dict[str, object]:
    return {
        "module": module_name,
        "profile": profile,
        "context": context,
        "generator_version": "counseling_v2_api_ready",
        "requested_output": {
            "format": "structured_counseling_recommendation",
            "needs_reasoning": True,
            "needs_live_sports_research": True,
            "needs_professional_tone": True,
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
    elif objective == "Build points safely":
        if "ITF" in tournament.source or "Challenger 50" in tournament.category or "Challenger 75" in tournament.category:
            score += 10
            reasons.append("This type of event can be more logical for controlled point building.")
    elif objective == "Come back with confidence":
        score += 5
        reasons.append("For a confidence week, controlled conditions matter more than maximum tournament prestige.")

    if location.strip():
        reasons.append(f"Current location noted: {location}. Travel should be checked against budget and recovery." )
    if travel_budget == "Low":
        score += 3
        reasons.append("Low-budget mode favors nearby, simpler travel plans.")
    elif travel_budget == "High":
        score += 2
        reasons.append("Higher travel budget gives flexibility, but not a free pass to choose the hardest event.")

    if tournament.confidence == "high":
        score += 3
    elif tournament.confidence == "low":
        score -= 5
        reasons.append("Event details were found with lower confidence and should be double-checked manually.")

    return score, reasons


# -----------------------------------------------------------------------------
# OFFICIAL CALENDAR FETCHERS
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


def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    if PdfReader is None:
        return ""
    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception:
        return ""


def fetch_atp_main_from_pdf(year: int, week_start: date, week_end: date) -> Tuple[List[TennisTournament], List[str]]:
    urls = [
        OFFICIAL_TENNIS_SOURCES["ATP Tour"]["calendar_pdf"].format(year=year, prev_year=year - 1),
        f"https://www.atptour.com/-/media/files/calendar-pdfs/{year}/2026-atp-tour-calendar-december-2025.pdf" if year == 2026 else "",
    ]
    urls = [u for u in urls if u]
    warnings: List[str] = []
    tournaments: List[TennisTournament] = []

    for url in urls:
        _, pdf_bytes, err = safe_get(url)
        if err or not pdf_bytes:
            warnings.append(f"ATP Tour PDF fetch issue: {err}")
            continue
        text = extract_text_from_pdf_bytes(pdf_bytes)
        if not text:
            warnings.append("ATP Tour PDF was downloaded but could not be parsed. Install pypdf if needed.")
            continue

        # Broad regex strategy: capture date + city + category + tournament name + surface on same line where possible.
        pattern = re.compile(
            r"(?P<week>\d{1,2})\s+(?P<date>\d{2}-[A-Z]{3})\s+(?P<city>[A-ZÀ-ÿ'.,\- ]{2,})\s+(?P<category>ATP 250|ATP 500|ATP MASTERS 1000|GRAND SLAM|DAVIS CUP|LAVER CUP|ATP FINALS|NEXT GEN ATP FINALS)\s+(?P<name>[A-ZÀ-ÿ0-9'&.,\- ]{4,})\s+(?P<surface>IH|H|CL|G)"
        )
        found_any = False
        for match in pattern.finditer(text):
            start = parse_day_month(match.group("date"), year)
            if not start or not (week_start <= start <= week_end):
                continue
            found_any = True
            surface_map = {"IH": "Indoor Hard", "H": "Hard", "CL": "Clay", "G": "Grass"}
            tournaments.append(
                TennisTournament(
                    source="ATP Tour",
                    name=match.group("name").strip().title(),
                    city=match.group("city").strip().title(),
                    category=match.group("category").strip(),
                    surface=surface_map.get(match.group("surface"), match.group("surface")),
                    start_date=start,
                    end_date=start + timedelta(days=6),
                    url=OFFICIAL_TENNIS_SOURCES["ATP Tour"]["tournaments"],
                    confidence="high",
                    notes="Parsed from official ATP Tour calendar PDF.",
                )
            )
        if found_any:
            break
    return tournaments, warnings


def fetch_challenger_from_html(week_start: date, week_end: date) -> Tuple[List[TennisTournament], List[str]]:
    warnings: List[str] = []
    urls = [
        OFFICIAL_TENNIS_SOURCES["ATP Challenger"]["calendar_html"],
        OFFICIAL_TENNIS_SOURCES["ATP Challenger"]["calendar_alt"],
    ]
    tournaments: List[TennisTournament] = []

    for url in urls:
        html, _, err = safe_get(url)
        if err or not html:
            warnings.append(f"Challenger calendar fetch issue: {err}")
            continue
        if BeautifulSoup is None:
            warnings.append("BeautifulSoup is not installed; Challenger HTML parsing unavailable.")
            continue
        soup = BeautifulSoup(html, "html.parser")

        # The live page structure changes. We therefore scan the page text aggressively.
        page_text = soup.get_text(" ", strip=True)
        month_name = week_start.strftime("%B")
        if month_name.lower() not in page_text.lower() and week_end.strftime("%B").lower() not in page_text.lower():
            warnings.append("Challenger page loaded, but the expected month was not easy to find in the HTML text.")

        # Parse visible event snippets like “Challenger Tour-75. City, Country”
        snippet_pattern = re.compile(r"Challenger Tour-(\d{2,3})\.\s+([^·]+?),\s+([A-Za-zÀ-ÿ .\-']+)")
        seen = set()
        for cat, city, country in snippet_pattern.findall(page_text):
            key = (cat, city.strip(), country.strip())
            if key in seen:
                continue
            seen.add(key)
            tournaments.append(
                TennisTournament(
                    source="ATP Challenger",
                    name=f"ATP Challenger {cat}",
                    city=city.strip(),
                    country=country.strip(),
                    category=f"Challenger {cat}",
                    start_date=week_start,
                    end_date=week_end,
                    url=url,
                    confidence="medium",
                    notes="Found on official ATP Challenger calendar page. Confirm exact event name manually if needed.",
                )
            )
        if tournaments:
            break
    return tournaments, warnings


def fetch_challenger_from_pdf(year: int, week_start: date, week_end: date) -> Tuple[List[TennisTournament], List[str]]:
    url = OFFICIAL_TENNIS_SOURCES["ATP Challenger"]["calendar_pdf"].format(year=year)
    _, pdf_bytes, err = safe_get(url)
    if err or not pdf_bytes:
        return [], [f"Challenger PDF fetch issue: {err}"]
    text = extract_text_from_pdf_bytes(pdf_bytes)
    if not text:
        return [], ["Challenger PDF downloaded but could not be parsed. Install pypdf if needed."]

    tournaments: List[TennisTournament] = []
    warnings: List[str] = []
    current_month = ""
    for raw_line in text.splitlines():
        line = re.sub(r"\s+", " ", raw_line).strip()
        if line.upper() in MONTHS:
            current_month = line.upper()
            continue
        if not line:
            continue

        date_match = re.search(r"(\d{1,2})\s+(\d{1,2}-[A-Z]{3})\s+([A-Za-zÀ-ÿ' .\-]+)\s+([A-Z]{3})\s+(\d{2,3})", line)
        if not date_match:
            continue
        start = parse_day_month(date_match.group(2), year)
        if not start or not (week_start <= start <= week_end):
            continue

        city = date_match.group(3).strip()
        country = date_match.group(4).strip()
        category_num = date_match.group(5).strip()
        tournaments.append(
            TennisTournament(
                source="ATP Challenger",
                name=f"ATP Challenger {category_num}",
                city=city,
                country=country,
                category=f"Challenger {category_num}",
                start_date=start,
                end_date=start + timedelta(days=6),
                url=url,
                confidence="medium",
                notes="Parsed from official ATP Challenger calendar PDF. Exact tournament title may need manual confirmation.",
            )
        )
    return tournaments, warnings


def fetch_itf_events(week_start: date, week_end: date) -> Tuple[List[TennisTournament], List[str]]:
    warnings: List[str] = []
    url = OFFICIAL_TENNIS_SOURCES["ITF"]["calendar_html"]
    html, _, err = safe_get(url)
    if err or not html:
        return [], [f"ITF calendar fetch issue: {err}"]
    if BeautifulSoup is None:
        return [], ["BeautifulSoup is not installed; ITF HTML parsing unavailable."]

    soup = BeautifulSoup(html, "html.parser")
    page_text = soup.get_text(" ", strip=True)
    tournaments: List[TennisTournament] = []

    # ITF pages often embed event cards inconsistently, so we use broad pattern matching.
    # Examples targeted: M15 Antalya, Turkey / M25 Sao Paulo, Brazil
    event_pattern = re.compile(r"\b(M15|M25)\s+([A-Za-zÀ-ÿ0-9' .\-]+?),\s+([A-Za-zÀ-ÿ .\-']+)\b")
    seen = set()
    for category, city, country in event_pattern.findall(page_text):
        key = (category, city.strip(), country.strip())
        if key in seen:
            continue
        seen.add(key)
        tournaments.append(
            TennisTournament(
                source="ITF",
                name=f"ITF {category}",
                city=city.strip(),
                country=country.strip(),
                category=category,
                start_date=week_start,
                end_date=week_end,
                url=url,
                confidence="medium",
                notes="Found on official ITF calendar page. Exact acceptance details must still be checked.",
            )
        )
    if not tournaments:
        warnings.append("ITF official calendar page loaded, but event cards were not easy to parse with the current page structure.")
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
    year = week_start.year
    all_events: List[TennisTournament] = []
    warnings: List[str] = []

    atp_main, warn = fetch_atp_main_from_pdf(year, week_start, week_end)
    all_events.extend(atp_main)
    warnings.extend(warn)

    challenger_html, warn = fetch_challenger_from_html(week_start, week_end)
    all_events.extend(challenger_html)
    warnings.extend(warn)

    if not challenger_html:
        challenger_pdf, warn = fetch_challenger_from_pdf(year, week_start, week_end)
        all_events.extend(challenger_pdf)
        warnings.extend(warn)

    itf_events, warn = fetch_itf_events(week_start, week_end)
    all_events.extend(itf_events)
    warnings.extend(warn)

    return deduplicate_tournaments(all_events), warnings, (week_start, week_end)


# -----------------------------------------------------------------------------
# TENNIS COUNSELING
# -----------------------------------------------------------------------------
def build_tennis_profile(
    ranking: int,
    location: str,
    preferred_surface: str,
    travel_budget: str,
    objective: str,
) -> Dict[str, object]:
    return {
        "ranking": ranking,
        "location": location,
        "preferred_surface": preferred_surface,
        "travel_budget": travel_budget,
        "objective": objective,
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
        for reason in reasons[:4]:
            st.write(f"- {reason}")
        if event.url:
            st.markdown(f"[Official page]({event.url})")


def render_tennis_counseling() -> None:
    st.subheader("Tennis Tournament Counseling")
    st.write(
        "Professional tournament guidance using the next week's official ATP Tour, ATP Challenger, and ITF calendars when available. "
        "This section is also prepared for future API reasoning integration."
    )

    col1, col2 = st.columns(2)
    with col1:
        ranking = st.number_input("Current ATP ranking", min_value=1, max_value=5000, value=850)
        location = st.text_input("Where are you now?", placeholder="Example: São Paulo, Brazil")
        preferred_surface = st.selectbox("Preferred surface", list(TENNIS_SURFACE_PROFILE.keys()))
    with col2:
        travel_budget = st.selectbox("Travel budget for next week", ["Low", "Medium", "High"])
        objective = st.selectbox(
            "Main objective",
            ["Get match wins", "Try a bigger event", "Build points safely", "Come back with confidence"],
        )
        refresh_live = st.checkbox("Refresh official calendar data now", value=True)

    st.info(
        f"Travel framework: {BUDGET_TO_DISTANCE[travel_budget]}\n\n"
        f"Objective lens: {OBJECTIVE_GUIDANCE[objective]}"
    )

    with st.expander("Surface profile guidance", expanded=False):
        for line in TENNIS_SURFACE_PROFILE[preferred_surface]:
            st.write(f"- {line}")

    if st.button("Get Tennis Advice", type="primary", use_container_width=True):
        profile = build_tennis_profile(ranking, location, preferred_surface, travel_budget, objective)
        context: Dict[str, object] = {"calendar_mode": "official_sources_next_week"}

        if refresh_live:
            with st.spinner("Checking official ATP / Challenger / ITF calendar sources..."):
                tournaments, warnings, week_range = load_next_week_tournaments()
        else:
            tournaments, warnings, week_range = [], ["Live fetch disabled by user toggle."], next_week_window()

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

            st.subheader("Top tournament suggestions for next week")
            for _, event in scored[:6]:
                render_tournament_card(event, ranking, preferred_surface, travel_budget, objective, location)
        else:
            st.warning(
                "No tournament cards could be confirmed from the official pages with the current parser. "
                "The code is still structured to fetch the next week automatically, but you may need to install or update parsing dependencies or adjust selectors if the site structure changed."
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
# SOCCER COUNSELING
# -----------------------------------------------------------------------------
def suggest_soccer_path(current_level: str, continent: str, country: str, offers: str) -> Tuple[str, List[str]]:
    reasons: List[str] = []
    if current_level in ["Local / amateur", "Semi-pro"]:
        recommendation = f"Target a stable development move in {country} rather than a prestige leap."
        reasons.extend([
            "Minutes, coaching quality, and a realistic competitive jump matter more than the badge name.",
            "A consistent bridge step usually creates better next moves than one oversized jump that leads to no playing time.",
        ])
    elif current_level == "Lower professional":
        recommendation = f"Look for a better-structured league or second-tier pathway in {country}."
        reasons.extend([
            "You are at a stage where structure, tactical education, and visibility can all matter at once.",
            "A slightly stronger league with a real development plan can outperform a random bigger-club gamble.",
        ])
    else:
        recommendation = f"You can consider stronger opportunities in {country}, but only when the tactical fit and route to minutes are real."
        reasons.extend([
            "At higher levels, the wrong move is often a pathway problem, not a talent problem.",
            "Exposure matters, but role clarity and coach trust still decide whether the move actually helps.",
        ])

    if offers.strip():
        reasons.append("Existing offers should be ranked by likely playing time, tactical fit, contract safety, and exposure value.")
    else:
        reasons.append("With no concrete offers, priority should be environments where your profile clearly solves a need.")

    return recommendation, reasons


def render_soccer_counseling() -> None:
    st.subheader("Soccer Career Counseling")
    st.write("A more structured and professional counseling flow, also prepared for future API reasoning integration.")

    col1, col2 = st.columns(2)
    with col1:
        current_team = st.text_input("Which team are you in now?", placeholder="Example: Derry City, Santos U20, local academy...")
        current_level = st.selectbox("Current team level", TEAM_LEVEL_GUIDE)
    with col2:
        continent = st.selectbox("Which continent do you want to go to?", list(SOCCER_CONTINENTS.keys()))
        country = st.selectbox("What country inside that continent?", SOCCER_CONTINENTS[continent])

    offers = st.text_area(
        "What contract offers do you have today?",
        placeholder="Write current options, trials, salary level, loan ideas, or no offers yet.",
    )

    if st.button("Get Soccer Advice", type="primary", use_container_width=True):
        profile = {
            "current_team": current_team,
            "current_level": current_level,
            "target_continent": continent,
            "target_country": country,
            "offers": offers,
        }
        future_payload = build_future_api_payload("soccer_counseling", profile, {"mode": "career_pathway"})

        recommendation, reasons = suggest_soccer_path(current_level, continent, country, offers)

        st.markdown("## Recommended pathway")
        st.success(recommendation)

        st.markdown("### Why this is the smarter move")
        for reason in reasons:
            st.write(f"- {reason}")

        st.markdown("### Smart decision filters")
        filters = [
            "Will you realistically play meaningful minutes?",
            "Is the league a logical next step from your current level?",
            "Does the club's style suit your strongest qualities?",
            "Is the contract financially and legally safe?",
            "Will this move improve your next move, not only your current headline?",
        ]
        for f in filters:
            st.write(f"- {f}")

        if current_team:
            st.info(f"Based on '{current_team}', avoid unrealistic giant-club jumps unless your level, data, and pathway clearly support them.")
        if offers.strip():
            st.caption(f"Offers noted: {offers}")

        with st.expander("Future API integration preview", expanded=False):
            st.json(future_payload)
            st.caption("Prepared for future reasoning/API implementation, but no API is connected yet.")


# -----------------------------------------------------------------------------
# SECTION ROOT
# -----------------------------------------------------------------------------
def render_counseling_section() -> None:
    st.header("Counseling")
    st.write(
        "Professional counseling with improved structure, future API-ready architecture, and live-calendar support hooks for tennis."
    )
    mode = st.radio("Choose counseling mode", ["Tennis", "Soccer"], horizontal=True)

    if mode == "Tennis":
        render_tennis_counseling()
    else:
        render_soccer_counseling()
