
from __future__ import annotations

import io
import json
import re
from dataclasses import dataclass
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
        "calendar_page": "https://www.atptour.com/en/tournaments",
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

SOCCER_DIVISION_GUIDE = {
    "Brazil": [
        "Academy / U15-U17",
        "Academy / U20",
        "State league / amateur",
        "Semi-pro",
        "Serie D / equivalent",
        "Serie C / equivalent",
        "Serie B / equivalent",
        "Serie A / top-flight equivalent",
    ],
    "England": [
        "Academy / U18",
        "Academy / U21",
        "Non-League",
        "League Two equivalent",
        "League One equivalent",
        "Championship equivalent",
        "Premier League equivalent",
    ],
    "Portugal": [
        "Academy / U17",
        "Academy / U19",
        "Campeonato de Portugal / amateur bridge",
        "Liga 3 equivalent",
        "Liga Portugal 2 equivalent",
        "Liga Portugal equivalent",
    ],
    "Spain": [
        "Academy / Juvenil",
        "Reserve / B team level",
        "Tercera / amateur bridge",
        "Segunda Federación equivalent",
        "Primera Federación equivalent",
        "LaLiga Hypermotion equivalent",
        "LaLiga equivalent",
    ],
    "Default": [
        "Academy",
        "Amateur",
        "Semi-pro",
        "Lower professional",
        "Second division equivalent",
        "Top-flight equivalent",
    ],
}

AGE_DEVELOPMENT_NOTES = {
    "under_15": "Development, coaching quality, and patience matter much more than exposure hype.",
    "15_to_17": "This is a formation stage, so pathway logic and game minutes beat prestige-only moves.",
    "18_to_21": "This is a sensitive bridge stage where first-team minutes and contract clarity matter a lot.",
    "22_plus": "Role fit, stability, and level progression matter more than vague promises.",
}

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
    indoor: Optional[bool] = None


# -----------------------------------------------------------------------------
# GENERAL HELPERS
# -----------------------------------------------------------------------------
def build_future_api_payload(module_name: str, profile: Dict[str, object], context: Dict[str, object]) -> Dict[str, object]:
    return {
        "module": module_name,
        "profile": profile,
        "context": context,
        "generator_version": "counseling_v3_api_ready",
        "requested_output": {
            "format": "structured_counseling_recommendation",
            "needs_reasoning": True,
            "needs_live_sports_research": True,
            "needs_professional_tone": True,
            "needs_named_event_output": True,
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
    raw = raw.strip()
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
    elif objective == "Build points safely":
        if "ITF" in tournament.source or "Challenger 50" in tournament.category or "Challenger 75" in tournament.category:
            score += 10
            reasons.append("This type of event can be more logical for controlled point building.")
    elif objective == "Come back with confidence":
        score += 5
        reasons.append("For a confidence week, controlled conditions matter more than maximum tournament prestige.")

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


def _clean_event_name(name: str) -> str:
    value = re.sub(r"\s+", " ", (name or "")).strip(" -|")
    value = re.sub(r"(?i)\b(atp challenger tour|atp challenger)\b", "", value).strip(" -|")
    return value


def _event_from_json_blob(blob: object, source_name: str, default_url: str, week_start: date, week_end: date) -> List[TennisTournament]:
    events: List[TennisTournament] = []
    if isinstance(blob, dict):
        candidates = [blob]
        for key in ["events", "items", "results", "tournaments", "data", "calendar"]:
            value = blob.get(key)
            if isinstance(value, list):
                candidates.extend(value)
    elif isinstance(blob, list):
        candidates = blob
    else:
        candidates = []

    for item in candidates:
        if not isinstance(item, dict):
            continue

        raw_name = (
            item.get("name")
            or item.get("title")
            or item.get("tournamentName")
            or item.get("eventName")
            or item.get("displayName")
            or ""
        )
        if not raw_name:
            continue

        raw_city = item.get("city") or item.get("location") or item.get("venueCity") or ""
        raw_country = item.get("country") or item.get("nation") or item.get("venueCountry") or ""
        raw_category = item.get("category") or item.get("level") or item.get("drawCategory") or item.get("grade") or ""
        raw_surface = item.get("surface") or item.get("courtSurface") or ""
        raw_url = item.get("url") or item.get("link") or default_url

        raw_start = (
            item.get("startDate")
            or item.get("start_date")
            or item.get("date")
            or item.get("weekStart")
            or ""
        )
        raw_end = item.get("endDate") or item.get("end_date") or item.get("weekEnd") or ""

        start_date = None
        end_date = None

        if isinstance(raw_start, str) and raw_start:
            start_date = parse_date_flex(raw_start[:10] if "T" in raw_start else raw_start)
        if isinstance(raw_end, str) and raw_end:
            end_date = parse_date_flex(raw_end[:10] if "T" in raw_end else raw_end)

        if start_date and not end_date:
            end_date = start_date + timedelta(days=6)

        if start_date and (start_date > week_end or start_date < week_start):
            continue

        if not start_date:
            start_date = week_start
            end_date = week_end

        events.append(
            TennisTournament(
                source=source_name,
                name=_clean_event_name(raw_name),
                city=str(raw_city).strip(),
                country=str(raw_country).strip(),
                category=str(raw_category).strip() or source_name,
                surface=normalize_surface(str(raw_surface)),
                start_date=start_date,
                end_date=end_date or (start_date + timedelta(days=6)),
                url=str(raw_url).strip(),
                confidence="high",
                notes=f"Named event found through structured data on the official {source_name} source.",
            )
        )
    return events


def _extract_json_candidates_from_html(html: str) -> List[object]:
    blobs: List[object] = []
    script_patterns = [
        r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',
        r'<script[^>]*type="application/json"[^>]*>(.*?)</script>',
        r'window\.__INITIAL_STATE__\s*=\s*({.*?});',
        r'window\.__NEXT_DATA__\s*=\s*({.*?})</script>',
        r'__NUXT__\s*=\s*({.*?});',
    ]
    for pattern in script_patterns:
        for match in re.finditer(pattern, html, flags=re.DOTALL | re.IGNORECASE):
            raw = match.group(1).strip()
            if not raw:
                continue
            try:
                blobs.append(json.loads(raw))
            except Exception:
                cleaned = raw.replace("&quot;", '"')
                try:
                    blobs.append(json.loads(cleaned))
                except Exception:
                    continue
    return blobs


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

        lines = [re.sub(r"\s+", " ", line).strip() for line in text.splitlines() if line.strip()]
        broad_pattern = re.compile(
            r"(?P<date>\d{2}-[A-Z]{3})\s+(?P<city>[A-ZÀ-ÿ'.,\- ]{2,})\s+"
            r"(?P<category>ATP 250|ATP 500|ATP MASTERS 1000|GRAND SLAM|DAVIS CUP|LAVER CUP|ATP FINALS|NEXT GEN ATP FINALS)\s+"
            r"(?P<name>[A-ZÀ-ÿ0-9'&.,\- ]{4,}?)\s+(?P<surface>IH|H|CL|G)$"
        )

        found_any = False
        for line in lines:
            match = broad_pattern.search(line)
            if not match:
                continue
            start = parse_day_month(match.group("date"), year)
            if not start or not (week_start <= start <= week_end):
                continue
            found_any = True
            tournaments.append(
                TennisTournament(
                    source="ATP Tour",
                    name=_clean_event_name(match.group("name").title()),
                    city=match.group("city").strip().title(),
                    category=match.group("category").strip().replace("ATP MASTERS 1000", "ATP Masters 1000"),
                    surface=normalize_surface(match.group("surface")),
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


def fetch_named_events_from_structured_html(url: str, source_name: str, week_start: date, week_end: date) -> Tuple[List[TennisTournament], List[str]]:
    html, _, err = safe_get(url)
    if err or not html:
        return [], [f"{source_name} HTML fetch issue: {err}"]
    warnings: List[str] = []
    events: List[TennisTournament] = []

    for blob in _extract_json_candidates_from_html(html):
        events.extend(_event_from_json_blob(blob, source_name, url, week_start, week_end))

    if not events and BeautifulSoup is not None:
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(" ", strip=True)

        atp_patterns = [
            re.compile(
                r"(?P<name>[A-Z][A-Za-z0-9'&.\- ]{3,}?)\s+(?P<city>[A-Za-zÀ-ÿ' .\-]+),\s*(?P<country>[A-Za-zÀ-ÿ' .\-]+)\s+"
                r"(?P<category>ATP 250|ATP 500|ATP Masters 1000|Grand Slam)\s+(?P<surface>Hard|Clay|Grass|Indoor Hard)?",
                re.IGNORECASE,
            ),
            re.compile(
                r"(?P<name>Challenger [A-Za-z0-9'&.\- ]+?)\s+(?P<city>[A-Za-zÀ-ÿ' .\-]+),\s*(?P<country>[A-Za-zÀ-ÿ' .\-]+)",
                re.IGNORECASE,
            ),
            re.compile(
                r"(?P<name>M15 [A-Za-z0-9'&.\- ]+|M25 [A-Za-z0-9'&.\- ]+)\s+(?P<city>[A-Za-zÀ-ÿ' .\-]+),\s*(?P<country>[A-Za-zÀ-ÿ' .\-]+)",
                re.IGNORECASE,
            ),
        ]

        for pattern in atp_patterns:
            for match in pattern.finditer(text):
                name = _clean_event_name(match.group("name"))
                city = (match.groupdict().get("city") or "").strip()
                country = (match.groupdict().get("country") or "").strip()
                category = (match.groupdict().get("category") or source_name).strip()
                surface = normalize_surface((match.groupdict().get("surface") or "").strip())
                if len(name) < 4:
                    continue
                events.append(
                    TennisTournament(
                        source=source_name,
                        name=name,
                        city=city,
                        country=country,
                        category=category,
                        surface=surface,
                        start_date=week_start,
                        end_date=week_end,
                        url=url,
                        confidence="medium",
                        notes=f"Named event found from official {source_name} HTML text fallback.",
                    )
                )

    if not events:
        warnings.append(f"{source_name} official page loaded, but named events could not be extracted with the current parser.")
    return events, warnings


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
    lines = [re.sub(r"\s+", " ", line).strip() for line in text.splitlines() if line.strip()]
    pattern = re.compile(
        r"(?P<week>\d{1,2})\s+(?P<date>\d{1,2}-[A-Z]{3})\s+(?P<name>[A-Za-zÀ-ÿ0-9'&.\- ]{3,}?)\s+"
        r"(?P<city>[A-Za-zÀ-ÿ' .\-]+)\s+(?P<country>[A-Z]{3})\s+(?P<cat>\d{2,3})"
    )

    for line in lines:
        match = pattern.search(line)
        if not match:
            continue
        start = parse_day_month(match.group("date"), year)
        if not start or not (week_start <= start <= week_end):
            continue

        raw_name = _clean_event_name(match.group("name"))
        city = match.group("city").strip()
        country = match.group("country").strip()
        category_num = match.group("cat").strip()

        if not raw_name or raw_name.lower() == city.lower():
            raw_name = f"ATP Challenger {city}"

        tournaments.append(
            TennisTournament(
                source="ATP Challenger",
                name=raw_name,
                city=city,
                country=country,
                category=f"Challenger {category_num}",
                start_date=start,
                end_date=start + timedelta(days=6),
                url=url,
                confidence="medium",
                notes="Parsed from official ATP Challenger calendar PDF.",
            )
        )
    if not tournaments:
        warnings.append("Challenger PDF was parsed, but no named tournament matching next week was found.")
    return tournaments, warnings


def fetch_itf_events(week_start: date, week_end: date) -> Tuple[List[TennisTournament], List[str]]:
    named_events, warnings = fetch_named_events_from_structured_html(
        OFFICIAL_TENNIS_SOURCES["ITF"]["calendar_html"], "ITF", week_start, week_end
    )
    if named_events:
        return named_events, warnings

    html, _, err = safe_get(OFFICIAL_TENNIS_SOURCES["ITF"]["calendar_html"])
    if err or not html:
        return [], [f"ITF calendar fetch issue: {err}"]

    tournaments: List[TennisTournament] = []
    page_text = html
    pattern = re.compile(
        r"\b(?P<category>M15|M25)\s+(?P<name>[A-Za-zÀ-ÿ0-9'&.\- ]+?)\s*[,\-]\s*(?P<country>[A-Za-zÀ-ÿ .\-']+)\b"
    )
    for match in pattern.finditer(page_text):
        category = match.group("category").strip()
        raw_name = _clean_event_name(match.group("name"))
        country = match.group("country").strip()
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
                url=OFFICIAL_TENNIS_SOURCES["ITF"]["calendar_html"],
                confidence="medium",
                notes="Found on official ITF calendar page with a broad fallback parser.",
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

    atp_main_pdf, warn = fetch_atp_main_from_pdf(year, week_start, week_end)
    all_events.extend(atp_main_pdf)
    warnings.extend(warn)

    atp_main_html, warn = fetch_named_events_from_structured_html(
        OFFICIAL_TENNIS_SOURCES["ATP Tour"]["calendar_page"], "ATP Tour", week_start, week_end
    )
    all_events.extend(atp_main_html)
    warnings.extend(warn)

    challenger_html, warn = fetch_named_events_from_structured_html(
        OFFICIAL_TENNIS_SOURCES["ATP Challenger"]["calendar_html"], "ATP Challenger", week_start, week_end
    )
    all_events.extend(challenger_html)
    warnings.extend(warn)

    if not challenger_html:
        challenger_alt, warn = fetch_named_events_from_structured_html(
            OFFICIAL_TENNIS_SOURCES["ATP Challenger"]["calendar_alt"], "ATP Challenger", week_start, week_end
        )
        all_events.extend(challenger_alt)
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
        for reason in reasons[:5]:
            st.write(f"- {reason}")
        if event.url:
            st.markdown(f"[Official page]({event.url})")


def render_tennis_counseling() -> None:
    st.subheader("Tennis Tournament Counseling")
    st.write(
        "Professional tournament guidance using the following week's official ATP Tour, ATP Challenger, and ITF calendars. "
        "This version is focused on naming actual tournaments, not only showing the week window, and it remains ready for future API integration."
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
        context: Dict[str, object] = {"calendar_mode": "official_sources_following_week_named_events"}

        if refresh_live:
            with st.spinner("Checking official ATP / Challenger / ITF calendar sources for next week's named tournaments..."):
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
                "No named tournament cards could be confirmed from the official pages with the current parser. "
                "The structure is ready and still checks the following week automatically, but the source selectors may need adjustment if the official site structure changes."
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
def age_bucket(age: int) -> str:
    if age < 15:
        return "under_15"
    if age <= 17:
        return "15_to_17"
    if age <= 21:
        return "18_to_21"
    return "22_plus"


def get_division_examples(country: str, age: int) -> List[str]:
    base = SOCCER_DIVISION_GUIDE.get(country, SOCCER_DIVISION_GUIDE["Default"]).copy()
    if age <= 20:
        return base
    return [entry for entry in base if "Academy" not in entry]


def suggest_soccer_path(
    age: int,
    current_country: str,
    current_division: str,
    target_continent: str,
    target_country: str,
    details: str,
) -> Tuple[str, List[str], List[str]]:
    reasons: List[str] = []
    filters: List[str] = []

    bucket = age_bucket(age)
    age_note = AGE_DEVELOPMENT_NOTES[bucket]
    reasons.append(age_note)

    division_lower = current_division.lower()
    target_country_clean = target_country.strip() or "the target country"

    if "academy" in division_lower or "u" in division_lower:
        recommendation = f"Prioritize a development-first move to {target_country_clean}, only if coaching quality, pathway, and minutes are clearly better than your current environment."
        reasons.extend([
            "At academy stage, the wrong badge is less important than the wrong pathway.",
            "A better developmental structure is more valuable than a club that only sounds bigger.",
        ])
    elif "amateur" in division_lower or "semi" in division_lower:
        recommendation = f"Look for a realistic bridge move to {target_country_clean} where you can actually play, adapt, and earn the next step."
        reasons.extend([
            "From amateur or semi-pro level, stability and game minutes usually matter more than prestige.",
            "Your best move is often one level above your current reality, not three levels above it.",
        ])
    elif "second" in division_lower or "serie b" in division_lower or "championship" in division_lower or "liga portugal 2" in division_lower:
        recommendation = f"Target a competitive move to {target_country_clean} only if it improves level, exposure, or tactical fit without reducing your role too much."
        reasons.extend([
            "At this level, a move should improve both sporting level and career visibility.",
            "A stronger but tactically wrong move can still slow your progression.",
        ])
    elif "top-flight" in division_lower or "serie a" in division_lower or "premier league" in division_lower or "laliga" in division_lower:
        recommendation = f"Only move to {target_country_clean} if the role, tactical fit, and exposure value are clearly stronger than your current situation."
        reasons.extend([
            "At a high level, the issue is usually role quality, not only league name.",
            "You should optimize the next contract and the next two years, not only the next headline.",
        ])
    else:
        recommendation = f"Build a pathway to {target_country_clean} that matches your age, current division, and likelihood of meaningful minutes."
        reasons.extend([
            "Your next move should be structurally logical, not only emotionally exciting.",
            "The best pathway is the one that improves the next move after this one as well.",
        ])

    if current_country.strip().lower() == target_country.strip().lower() and target_country.strip():
        reasons.append("Because the current and target country are the same, the decision should focus even more on division quality, minutes, and coach fit.")
    else:
        reasons.append("Because this may involve international adaptation, language, style of play, and legal/registration timing also matter.")

    if details.strip():
        reasons.append("The personal details you added should be weighed against contract safety, pathway clarity, and real playing opportunity.")
    else:
        reasons.append("Without extra details, the safest advice is to prioritize pathway clarity over brand name.")

    filters.extend([
        "Will you realistically play meaningful minutes there?",
        "Is the target division a logical next step from your current division?",
        "Does the move improve your development profile for your age?",
        "Is the club's style a fit for your strongest qualities?",
        "Is the contract or trial situation safe and clearly structured?",
        "Will this move improve your next move, not only your current headline?",
    ])

    if bucket in {"under_15", "15_to_17"}:
        filters.append("For your age, is the coaching and development environment clearly better?")
    if target_continent.strip():
        filters.append(f"Is {target_continent} really the right football market for your current stage, or only the most attractive name?")

    return recommendation, reasons, filters


def render_soccer_counseling() -> None:
    st.subheader("Soccer Career Counseling")
    st.write(
        "A more professional funnel focused on age, current country, current division, destination, and pathway logic. "
        "This version removes the old team-name-first flow and remains API ready."
    )

    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("What's your age?", min_value=8, max_value=45, value=17, step=1)
        current_country = st.text_input("What country are you now?", placeholder="Example: Brazil")
        current_division = st.text_input(
            "Which division are you in now?",
            placeholder="Example: Academy / U20, Semi-pro, Serie D, Liga 3, Championship...",
        )
    with col2:
        target_continent = st.selectbox("Which continent do you want to go to?", list(SOCCER_CONTINENTS.keys()))
        target_country = st.selectbox("What country inside that continent?", SOCCER_CONTINENTS[target_continent])
        division_examples = get_division_examples(current_country.strip() or "Default", int(age))

    if current_country or age:
        with st.expander("Division examples for this stage", expanded=False):
            st.write("These are example labels to help the user answer the division question more precisely:")
            for item in division_examples:
                st.write(f"- {item}")

    details = st.text_area(
        "Tell some important details",
        placeholder=(
            "Write position, level, recent minutes, passport situation, trials, injuries, dominant foot, "
            "physical profile, goals, or anything important about your situation."
        ),
    )

    if st.button("Get Soccer Advice", type="primary", use_container_width=True):
        profile = {
            "age": int(age),
            "current_country": current_country,
            "current_division": current_division,
            "target_continent": target_continent,
            "target_country": target_country,
            "details": details,
        }
        future_payload = build_future_api_payload(
            "soccer_counseling",
            profile,
            {
                "mode": "career_pathway",
                "funnel": [
                    "age",
                    "current_country",
                    "current_division",
                    "target_continent",
                    "target_country",
                    "details",
                ],
            },
        )

        recommendation, reasons, filters = suggest_soccer_path(
            int(age),
            current_country,
            current_division,
            target_continent,
            target_country,
            details,
        )

        st.markdown("## Recommended pathway")
        st.success(recommendation)

        st.markdown("### Why this is the smarter move")
        for reason in reasons:
            st.write(f"- {reason}")

        st.markdown("### Smart decision filters")
        for f in filters:
            st.write(f"- {f}")

        if current_country.strip():
            st.info(
                f"Current country noted: {current_country}. The advice is being shaped first by age, country, division, and destination rather than by a team-name shortcut."
            )
        if current_division.strip():
            st.caption(f"Current division noted: {current_division}")
        if details.strip():
            st.caption(f"Additional details noted: {details}")

        with st.expander("Future API integration preview", expanded=False):
            st.json(future_payload)
            st.caption("Prepared for future reasoning/API implementation, but no API is connected yet.")


# -----------------------------------------------------------------------------
# SECTION ROOT
# -----------------------------------------------------------------------------
def render_counseling_section() -> None:
    st.header("Counseling")
    st.write(
        "Professional counseling with improved structure, API-ready architecture, and live-calendar support hooks for tennis."
    )
    mode = st.radio("Choose counseling mode", ["Tennis", "Soccer"], horizontal=True)

    if mode == "Tennis":
        render_tennis_counseling()
    else:
        render_soccer_counseling()
