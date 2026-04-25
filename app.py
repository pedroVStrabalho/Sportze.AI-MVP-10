import base64
import hashlib
import hmac
import json
import os
import re
import secrets
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlencode

import streamlit as st

try:
    import requests
except Exception:  # pragma: no cover
    requests = None

from training_generator_section import render_training_generator_section
from video_review_section import render_video_review_section
from physio_section import render_physio_section
from counseling_section import render_counseling_section


# =============================================================================
# SPORTZE.AI APP SHELL
# =============================================================================
# What changed in this version:
# - Training Generator is the default and opens immediately.
# - No homepage explanatory paragraph.
# - Sidebar no longer contains module navigation, product structure, or profile snapshot.
# - Login is now in the top-right of the main screen.
# - Google OAuth is supported through Streamlit secrets.
# - A local email fallback remains available for testing without Google credentials.
# - Profile persistence remains JSON-based for MVP deployment.
# - The app shell is prepared for future database/auth migration without changing modules.
#
# Google OAuth setup for Render / Streamlit:
# 1. Create OAuth credentials in Google Cloud Console.
# 2. Authorized redirect URI should match:
#      https://YOUR-RENDER-APP.onrender.com
#    or local:
#      http://localhost:8501
# 3. Add these secrets in Streamlit/Render environment:
#      GOOGLE_CLIENT_ID = "..."
#      GOOGLE_CLIENT_SECRET = "..."
#      GOOGLE_REDIRECT_URI = "https://YOUR-RENDER-APP.onrender.com"
#
# Optional:
#      AUTH_ALLOW_EMAIL_FALLBACK = true
#
# This file intentionally does not require Authlib. It uses Google's OAuth
# endpoints directly through requests so deployment stays simple.
# =============================================================================


# =============================================================================
# BASIC CONFIG
# =============================================================================
APP_TITLE = "Sportze.AI"
DEFAULT_SECTION = "Training Generator"

SECTIONS = [
    "Training Generator",
    "Video Review",
    "Counseling",
    "Physio",
]

# No emojis in module labels. Keep this as a dict so .get() is always safe.
SECTION_ICONS: Dict[str, str] = {
    "Training Generator": "",
    "Video Review": "",
    "Counseling": "",
    "Physio": "",
}

SECTION_ROUTES = {
    "Training Generator": "training",
    "Video Review": "video",
    "Counseling": "counseling",
    "Physio": "physio",
}

ROUTE_TO_SECTION = {value: key for key, value in SECTION_ROUTES.items()}

PLAN_LIMITS = {
    "Free": {
        "training_generations_per_day": 5,
        "physio_sessions_per_day": 3,
        "video_reviews_per_day": 0,
        "counseling_sessions_per_day": 9999,
    },
    "Plus": {
        "training_generations_per_day": 9999,
        "physio_sessions_per_day": 10,
        "video_reviews_per_day": 1,
        "counseling_sessions_per_day": 9999,
    },
    "Pro": {
        "training_generations_per_day": 9999,
        "physio_sessions_per_day": 9999,
        "video_reviews_per_day": 9999,
        "counseling_sessions_per_day": 9999,
    },
}

PLAN_LIMIT_LABELS = {
    "training_generations_per_day": "training generations/day",
    "physio_sessions_per_day": "physio sections/day",
    "video_reviews_per_day": "video reviews/day",
    "counseling_sessions_per_day": "counseling sessions/day",
}

UNLIMITED_LIMIT = 9999

KNOWN_TEAM_SPORTS = {
    "soccer",
    "football",
    "basketball",
    "volleyball",
    "water polo",
    "baseball",
    "softball",
    "rugby",
    "handball",
    "futsal",
    "hockey",
    "lacrosse",
    "cricket",
    "american football",
    "field hockey",
    "ice hockey",
    "netball",
}

KNOWN_INDIVIDUAL_SPORTS = {
    "tennis",
    "running",
    "athletics",
    "track",
    "track and field",
    "swimming",
    "gym",
    "fitness",
    "weightlifting",
    "powerlifting",
    "bodybuilding",
    "rowing",
    "boxing",
    "judo",
    "taekwondo",
    "karate",
    "wrestling",
    "golf",
    "surfing",
    "surf",
    "cycling",
    "triathlon",
    "badminton",
    "table tennis",
    "skateboarding",
    "climbing",
    "bouldering",
    "skiing",
    "snowboarding",
    "gymnastics",
    "crossfit",
}

DATA_DIR = Path("data")
USERS_DIR = DATA_DIR / "users"
AUDIT_DIR = DATA_DIR / "audit"
for _path in [DATA_DIR, USERS_DIR, AUDIT_DIR]:
    _path.mkdir(exist_ok=True)


# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="S",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =============================================================================
# DATA STRUCTURES
# =============================================================================
@dataclass
class AuthUser:
    email: str = ""
    name: str = ""
    picture: str = ""
    provider: str = ""
    logged_in: bool = False
    login_time: str = ""


@dataclass
class ProfileSnapshot:
    profile_email: str = ""
    athlete_name: str = ""
    sport: str = ""
    sport_type: str = ""
    team_name: str = ""
    goal: str = ""
    level: str = ""
    is_professional: str = "No"
    weekly_target: Optional[int] = None
    selected_plan: str = "Pro"


# =============================================================================
# SMALL HELPERS
# =============================================================================
def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def get_secret(name: str, default: Any = None) -> Any:
    try:
        if name in st.secrets:
            return st.secrets[name]
    except Exception:
        pass
    return os.environ.get(name, default)


def bool_secret(name: str, default: bool = False) -> bool:
    value = get_secret(name, default)
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y", "on"}


def normalize_text(text: Any) -> str:
    return " ".join(str(text or "").strip().split())


def normalize_sport_name(text: str) -> str:
    return normalize_text(text).lower()


def detect_sport_type(sport_text: str) -> str:
    sport = normalize_sport_name(sport_text)
    if not sport:
        return ""
    if sport in KNOWN_TEAM_SPORTS:
        return "Team Sport"
    if sport in KNOWN_INDIVIDUAL_SPORTS:
        return "Individual Sport"
    return ""


def sanitize_email(email: str) -> str:
    return re.sub(r"[^a-zA-Z0-9._-]", "_", normalize_text(email).lower())


def user_file_path(email: str) -> Path:
    cleaned = sanitize_email(email)
    if not cleaned:
        cleaned = "anonymous"
    return USERS_DIR / f"{cleaned}.json"


def audit_file_path(email: str) -> Path:
    cleaned = sanitize_email(email) or "anonymous"
    return AUDIT_DIR / f"{cleaned}.jsonl"


def safe_json_load(path: Path, default: Any) -> Any:
    try:
        if not path.exists():
            return default
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def safe_json_write(path: Path, payload: Any) -> None:
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp_path.replace(path)


def add_audit_event(action: str, details: Optional[Dict[str, Any]] = None) -> None:
    email = st.session_state.get("profile_email", "") or st.session_state.get("auth_user", {}).get("email", "")
    row = {
        "time": now_iso(),
        "action": action,
        "section": st.session_state.get("active_section", DEFAULT_SECTION),
        "email": email,
        "details": details or {},
    }
    try:
        with audit_file_path(email).open("a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    except Exception:
        pass


def stable_hash(text: str) -> str:
    salt = str(get_secret("SPORTZE_LOCAL_HASH_SECRET", "sportze-ai-local-mvp-secret"))
    return hmac.new(salt.encode("utf-8"), text.encode("utf-8"), hashlib.sha256).hexdigest()


def set_query_route(section: str) -> None:
    route = SECTION_ROUTES.get(section, "training")
    try:
        st.query_params["section"] = route
    except Exception:
        pass


def read_query_route() -> Optional[str]:
    try:
        route = st.query_params.get("section")
        if isinstance(route, list):
            route = route[0] if route else None
        if route in ROUTE_TO_SECTION:
            return ROUTE_TO_SECTION[route]
    except Exception:
        return None
    return None


def clear_oauth_query_params() -> None:
    try:
        params = dict(st.query_params)
        for key in ["code", "state", "scope", "authuser", "prompt"]:
            if key in params:
                del st.query_params[key]
    except Exception:
        pass


# =============================================================================
# SESSION STATE
# =============================================================================
def init_state() -> None:
    defaults: Dict[str, Any] = {
        "active_section": DEFAULT_SECTION,
        "selected_plan": "Pro",
        "sport": "",
        "sport_type": "",
        "team_name": "",
        "athlete_name": "",
        "goal": "",
        "level": "",
        "is_professional": "No",
        "weekly_target": None,
        "home_notes": "",
        "profile_email": "",
        "profile_loaded": False,
        "auth_message": "",
        "auth_error": "",
        "auth_user": asdict(AuthUser()),
        "oauth_state": "",
        "oauth_nonce": "",
        "oauth_started_at": 0,
        "user_training_logs": [],
        "saved_training_sessions": [],
        "generator_chat_messages": [],
        "training_chat_started": False,
        "training_question_index": 0,
        "training_chat_complete": False,
        "training_profile": {},
        "latest_training_payload": None,
        "latest_training_summary": None,
        "usage_counters": {
            "training_generations": 0,
            "video_reviews": 0,
            "physio_sessions": 0,
            "counseling_sessions": 0,
        },
        "daily_usage": {
            "date": datetime.now(timezone.utc).date().isoformat(),
            "training_generations": 0,
            "video_reviews": 0,
            "physio_sessions": 0,
            "counseling_sessions": 0,
        },
        "active_visit_counter": 0,
        "section_visit_counted": {},
        "last_counted_training_signature": "",
        "last_saved_at": "",
        "ui_compact_mode": True,
        "show_local_email_login": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    query_section = read_query_route()
    if query_section and query_section in SECTIONS:
        st.session_state.active_section = query_section


def current_auth_user() -> AuthUser:
    raw = st.session_state.get("auth_user", {})
    if not isinstance(raw, dict):
        raw = {}
    return AuthUser(
        email=str(raw.get("email", "")),
        name=str(raw.get("name", "")),
        picture=str(raw.get("picture", "")),
        provider=str(raw.get("provider", "")),
        logged_in=bool(raw.get("logged_in", False)),
        login_time=str(raw.get("login_time", "")),
    )


def set_auth_user(user: AuthUser) -> None:
    st.session_state.auth_user = asdict(user)
    st.session_state.profile_email = user.email
    if user.name and not st.session_state.get("athlete_name"):
        st.session_state.athlete_name = user.name


# =============================================================================
# PROFILE PERSISTENCE
# =============================================================================
def build_user_payload() -> Dict[str, Any]:
    return {
        "schema_version": "sportze_user_profile_v2",
        "updated_at": now_iso(),
        "profile_email": st.session_state.get("profile_email", ""),
        "auth_user": st.session_state.get("auth_user", asdict(AuthUser())),
        "sport": st.session_state.get("sport", ""),
        "sport_type": st.session_state.get("sport_type", ""),
        "team_name": st.session_state.get("team_name", ""),
        "athlete_name": st.session_state.get("athlete_name", ""),
        "goal": st.session_state.get("goal", ""),
        "level": st.session_state.get("level", ""),
        "is_professional": st.session_state.get("is_professional", "No"),
        "weekly_target": st.session_state.get("weekly_target", None),
        "home_notes": st.session_state.get("home_notes", ""),
        "selected_plan": st.session_state.get("selected_plan", "Pro"),
        "saved_training_sessions": st.session_state.get("saved_training_sessions", []),
        "user_training_logs": st.session_state.get("user_training_logs", []),
        "usage_counters": st.session_state.get("usage_counters", {}),
        "daily_usage": st.session_state.get("daily_usage", {}),
        "last_counted_training_signature": st.session_state.get("last_counted_training_signature", ""),
        "training_profile": st.session_state.get("training_profile", {}),
    }


def apply_user_payload(payload: Dict[str, Any]) -> None:
    allowed = [
        "profile_email",
        "auth_user",
        "sport",
        "sport_type",
        "team_name",
        "athlete_name",
        "goal",
        "level",
        "is_professional",
        "weekly_target",
        "home_notes",
        "selected_plan",
        "saved_training_sessions",
        "user_training_logs",
        "usage_counters",
        "daily_usage",
        "last_counted_training_signature",
        "training_profile",
    ]
    for key in allowed:
        if key in payload:
            st.session_state[key] = payload[key]

    if not st.session_state.get("sport_type") and st.session_state.get("sport"):
        st.session_state.sport_type = detect_sport_type(st.session_state.sport)

    st.session_state.profile_loaded = True


def save_user_profile() -> None:
    email = st.session_state.get("profile_email", "").strip().lower()
    if not email:
        return
    payload = build_user_payload()
    safe_json_write(user_file_path(email), payload)
    st.session_state.last_saved_at = now_iso()


def load_user_profile(email: str) -> bool:
    email = normalize_text(email).lower()
    if not email:
        return False
    path = user_file_path(email)
    if not path.exists():
        return False
    payload = safe_json_load(path, {})
    if not isinstance(payload, dict):
        return False
    apply_user_payload(payload)
    st.session_state.profile_loaded = True
    return True


def create_user_profile(email: str, name: str = "", provider: str = "email") -> None:
    email = normalize_text(email).lower()
    name = normalize_text(name)
    user = AuthUser(
        email=email,
        name=name,
        provider=provider,
        logged_in=True,
        login_time=now_iso(),
    )
    set_auth_user(user)
    st.session_state.profile_loaded = True
    save_user_profile()
    add_audit_event("profile_created", {"provider": provider})


def clear_session_profile() -> None:
    preserved = {
        "active_section": st.session_state.get("active_section", DEFAULT_SECTION),
        "selected_plan": st.session_state.get("selected_plan", "Pro"),
    }
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    init_state()
    for key, value in preserved.items():
        st.session_state[key] = value
    add_audit_event("logout")


def persist_if_logged_in() -> None:
    user = current_auth_user()
    if user.logged_in and user.email:
        save_user_profile()
    elif st.session_state.get("profile_email"):
        save_user_profile()


# =============================================================================
# GOOGLE OAUTH
# =============================================================================
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"


def google_auth_configured() -> bool:
    return bool(get_secret("GOOGLE_CLIENT_ID")) and bool(get_secret("GOOGLE_CLIENT_SECRET")) and bool(get_google_redirect_uri())


def get_google_redirect_uri() -> str:
    explicit = get_secret("GOOGLE_REDIRECT_URI", "")
    if explicit:
        return str(explicit)

    # Local dev fallback. In production, set GOOGLE_REDIRECT_URI explicitly.
    return "http://localhost:8501"


def create_oauth_state() -> str:
    value = secrets.token_urlsafe(32)
    st.session_state.oauth_state = value
    st.session_state.oauth_nonce = secrets.token_urlsafe(32)
    st.session_state.oauth_started_at = int(time.time())
    return value


def build_google_login_url() -> str:
    client_id = str(get_secret("GOOGLE_CLIENT_ID", ""))
    redirect_uri = get_google_redirect_uri()
    state = create_oauth_state()

    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "state": state,
        "nonce": st.session_state.oauth_nonce,
        "access_type": "online",
        "prompt": "select_account",
    }
    return f"{GOOGLE_AUTH_URL}?{urlencode(params)}"


def exchange_google_code_for_token(code: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    if requests is None:
        return None, "The requests package is not installed."

    client_id = str(get_secret("GOOGLE_CLIENT_ID", ""))
    client_secret = str(get_secret("GOOGLE_CLIENT_SECRET", ""))
    redirect_uri = get_google_redirect_uri()

    try:
        response = requests.post(
            GOOGLE_TOKEN_URL,
            data={
                "code": code,
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code",
            },
            timeout=20,
        )
        if response.status_code >= 400:
            return None, f"Google token exchange failed: {response.text[:500]}"
        return response.json(), None
    except Exception as exc:
        return None, str(exc)


def fetch_google_userinfo(access_token: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    if requests is None:
        return None, "The requests package is not installed."

    try:
        response = requests.get(
            GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=20,
        )
        if response.status_code >= 400:
            return None, f"Google userinfo failed: {response.text[:500]}"
        return response.json(), None
    except Exception as exc:
        return None, str(exc)


def process_google_oauth_callback() -> None:
    try:
        code = st.query_params.get("code")
        state = st.query_params.get("state")
        if isinstance(code, list):
            code = code[0] if code else None
        if isinstance(state, list):
            state = state[0] if state else None
    except Exception:
        return

    if not code:
        return

    expected_state = st.session_state.get("oauth_state", "")
    if expected_state and state != expected_state:
        st.session_state.auth_error = "Google login security check failed. Please try again."
        clear_oauth_query_params()
        return

    token_payload, err = exchange_google_code_for_token(str(code))
    if err or not token_payload:
        st.session_state.auth_error = err or "Google login failed."
        clear_oauth_query_params()
        return

    access_token = token_payload.get("access_token", "")
    if not access_token:
        st.session_state.auth_error = "Google login did not return an access token."
        clear_oauth_query_params()
        return

    info, err = fetch_google_userinfo(access_token)
    if err or not info:
        st.session_state.auth_error = err or "Could not read Google profile."
        clear_oauth_query_params()
        return

    email = normalize_text(info.get("email", "")).lower()
    name = normalize_text(info.get("name", ""))
    picture = normalize_text(info.get("picture", ""))

    if not email:
        st.session_state.auth_error = "Google did not return an email address."
        clear_oauth_query_params()
        return

    user = AuthUser(
        email=email,
        name=name,
        picture=picture,
        provider="google",
        logged_in=True,
        login_time=now_iso(),
    )
    set_auth_user(user)

    if load_user_profile(email):
        existing_user = current_auth_user()
        existing_user.provider = "google"
        existing_user.logged_in = True
        existing_user.login_time = now_iso()
        if picture:
            existing_user.picture = picture
        if name and not existing_user.name:
            existing_user.name = name
        set_auth_user(existing_user)
        st.session_state.auth_message = "Google login successful. Saved profile loaded."
        add_audit_event("google_login_existing")
    else:
        create_user_profile(email=email, name=name, provider="google")
        current = current_auth_user()
        current.picture = picture
        set_auth_user(current)
        st.session_state.auth_message = "Google login successful. New Sportze.AI profile created."
        add_audit_event("google_login_new")

    st.session_state.auth_error = ""
    clear_oauth_query_params()
    st.rerun()


# =============================================================================
# UI STYLES
# =============================================================================
def inject_css() -> None:
    st.markdown(
        """
<style>
    :root {
        --sportze-bg: #050816;
        --sportze-card: rgba(255,255,255,0.055);
        --sportze-card-strong: rgba(255,255,255,0.09);
        --sportze-border: rgba(255,255,255,0.13);
        --sportze-text-soft: rgba(255,255,255,0.72);
    }

    .block-container {
        padding-top: 1.4rem;
        padding-bottom: 4rem;
        max-width: 1280px;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stSidebar"] {
        display: none;
    }

    .sportze-topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        margin-bottom: 0.8rem;
        padding: 0.75rem 0.85rem;
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 22px;
        background: linear-gradient(135deg, rgba(255,255,255,0.07), rgba(255,255,255,0.025));
        backdrop-filter: blur(10px);
    }

    .sportze-brand {
        display: flex;
        align-items: center;
        gap: 0.7rem;
        min-width: 220px;
    }

    .sportze-logo {
        width: 38px;
        height: 38px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 900;
        background: radial-gradient(circle at top left, #6ee7ff, #5b5cff 48%, #17172c);
        color: white;
        box-shadow: 0 10px 30px rgba(55, 120, 255, 0.25);
    }

    .sportze-brand-title {
        font-size: 1.05rem;
        font-weight: 800;
        line-height: 1.1;
    }

    .sportze-brand-subtitle {
        font-size: 0.76rem;
        opacity: 0.72;
        margin-top: 0.1rem;
    }

    .sportze-auth-box {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        gap: 0.65rem;
        text-align: right;
    }

    .sportze-user-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.45rem 0.65rem;
        border: 1px solid rgba(255,255,255,0.14);
        border-radius: 999px;
        background: rgba(255,255,255,0.06);
        font-size: 0.82rem;
        white-space: nowrap;
    }

    .sportze-avatar {
        width: 28px;
        height: 28px;
        border-radius: 999px;
        object-fit: cover;
        background: rgba(255,255,255,0.12);
    }

    .sportze-tabs {
        margin-top: 0.4rem;
        margin-bottom: 1.3rem;
    }

    .sportze-page-title {
        margin-top: 0.15rem;
        margin-bottom: 1.0rem;
    }

    .sportze-page-title h1 {
        font-size: clamp(2rem, 4vw, 3.2rem);
        line-height: 1.0;
        margin-bottom: 0.2rem;
        letter-spacing: -0.055em;
    }

    .sportze-page-title p {
        margin: 0;
        opacity: 0.68;
        font-size: 0.98rem;
    }

    .sportze-login-card {
        border: 1px solid rgba(255,255,255,0.13);
        border-radius: 22px;
        padding: 1.0rem;
        background: rgba(255,255,255,0.045);
        margin-bottom: 1rem;
    }

    .sportze-compact-note {
        opacity: 0.68;
        font-size: 0.82rem;
    }

    .stButton > button {
        border-radius: 999px;
    }

    div[data-testid="stTextInput"] input {
        border-radius: 999px;
    }

    div[data-testid="stSelectbox"] div {
        border-radius: 18px;
    }

    .sportze-hidden {
        display: none !important;
    }

    .sportze-main-hero {
        margin-top: 2.0rem;
        margin-bottom: 1.8rem;
    }

    .sportze-main-hero h1 {
        font-size: clamp(3.2rem, 7vw, 5.2rem);
        line-height: 0.95;
        letter-spacing: -0.065em;
        margin: 0 0 0.55rem 0;
        font-weight: 900;
    }

    .sportze-main-hero h2 {
        font-size: clamp(1.25rem, 2.4vw, 1.95rem);
        line-height: 1.18;
        margin: 0;
        font-weight: 750;
        letter-spacing: -0.025em;
    }

    .sportze-topbar-row {
        margin-bottom: 1.2rem;
    }

</style>
        """,
        unsafe_allow_html=True,
    )


# =============================================================================
# TOP-RIGHT LOGIN
# =============================================================================
def render_google_login_button() -> None:
    if google_auth_configured():
        login_url = build_google_login_url()
        st.link_button("Continue with Google", login_url, use_container_width=True, type="primary")
        st.caption("Opens Google login in a new tab/window, then returns to Sportze.AI.")
    else:
        st.warning("Google login is not configured yet.")
        with st.expander("Google login setup needed", expanded=False):
            st.code(
                """527430452650-a1udlafdtn8jp51f8t1jfnq9reknvntb.apps.googleusercontent.com="..."
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="..."
GOOGLE_REDIRECT_URI="https://your-render-app.onrender.com"
AUTH_ALLOW_EMAIL_FALLBACK=true""",
                language="toml",
            )


def render_email_fallback_login() -> None:
    allow_fallback = bool_secret("AUTH_ALLOW_EMAIL_FALLBACK", True)
    if not allow_fallback:
        return

    st.caption("Local testing fallback")
    email_input = st.text_input(
        "Email",
        value=st.session_state.get("profile_email", ""),
        placeholder="name@email.com",
        key="top_email_login_input",
        label_visibility="collapsed",
    ).strip().lower()

    name_input = st.text_input(
        "Name",
        value=st.session_state.get("athlete_name", ""),
        placeholder="Name (optional)",
        key="top_name_login_input",
        label_visibility="collapsed",
    ).strip()

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Email login", use_container_width=True, key="top_email_login_btn"):
            if not email_input or "@" not in email_input:
                st.session_state.auth_error = "Enter a valid email."
            else:
                if load_user_profile(email_input):
                    user = AuthUser(
                        email=email_input,
                        name=st.session_state.get("athlete_name", name_input),
                        provider="email",
                        logged_in=True,
                        login_time=now_iso(),
                    )
                    set_auth_user(user)
                    st.session_state.auth_message = "Email profile loaded."
                    add_audit_event("email_login_existing")
                else:
                    create_user_profile(email_input, name_input, provider="email")
                    st.session_state.auth_message = "New email profile created."
                st.session_state.auth_error = ""
                st.rerun()
    with c2:
        if st.button("Cancel", use_container_width=True, key="cancel_email_login_btn"):
            st.session_state.show_local_email_login = False
            st.rerun()


def render_login_popover() -> None:
    user = current_auth_user()

    if user.logged_in:
        label = user.name or user.email or "Account"
        with st.popover(f"Account", use_container_width=True):
            st.markdown("### Signed in")
            if user.picture:
                st.image(user.picture, width=56)
            st.write(label)
            st.caption(user.email)
            st.caption(f"Provider: {user.provider or 'unknown'}")
            if st.session_state.get("last_saved_at"):
                st.caption(f"Last saved: {st.session_state.last_saved_at}")
            if st.button("Log out", use_container_width=True, key="top_logout_btn"):
                clear_session_profile()
                st.rerun()
        return

    with st.popover("Log in", use_container_width=True):
        st.markdown("### Log in to Sportze.AI")
        render_google_login_button()
        st.divider()
        if st.button("Use email fallback", use_container_width=True, key="show_email_fallback_btn"):
            st.session_state.show_local_email_login = not st.session_state.get("show_local_email_login", False)
        if st.session_state.get("show_local_email_login"):
            render_email_fallback_login()

        if st.session_state.get("auth_error"):
            st.error(st.session_state.auth_error)
        elif st.session_state.get("auth_message"):
            st.success(st.session_state.auth_message)


def render_topbar() -> None:
    user = current_auth_user()
    left, middle, right = st.columns([1.35, 2.2, 1.2], vertical_alignment="center")

    with left:
        st.markdown(
            """
<div class="sportze-brand">
    <div class="sportze-logo">S</div>
    <div>
        <div class="sportze-brand-title">Sportze.AI</div>
        <div class="sportze-brand-subtitle">World-class athlete intelligence</div>
    </div>
</div>
            """,
            unsafe_allow_html=True,
        )

    with middle:
        render_top_navigation()

    with right:
        render_login_popover()


# =============================================================================
# NAVIGATION
# =============================================================================
def set_active_section(section: str) -> None:
    if section not in SECTIONS:
        section = DEFAULT_SECTION
    previous = st.session_state.get("active_section", DEFAULT_SECTION)
    st.session_state.active_section = section
    if previous != section:
        st.session_state.active_visit_counter = int(st.session_state.get("active_visit_counter", 0) or 0) + 1
        st.session_state.section_visit_counted = {}
    set_query_route(section)
    add_audit_event("section_changed", {"section": section})


def render_top_navigation() -> None:
    current = st.session_state.get("active_section", DEFAULT_SECTION)

    cols = st.columns(len(SECTIONS))
    for idx, section in enumerate(SECTIONS):
        icons = SECTION_ICONS if isinstance(SECTION_ICONS, dict) else {}
        icon = icons.get(section, "")
        label = f"{icon} {section}".strip()
        button_type = "primary" if current == section else "secondary"
        with cols[idx]:
            if st.button(label, use_container_width=True, type=button_type, key=f"topnav_{SECTION_ROUTES[section]}"):
                set_active_section(section)
                st.rerun()


# =============================================================================
# HERO / PAGE TITLE
# =============================================================================
def render_default_training_hero() -> None:
    """
    Default opening view requested by the user.
    The actual module title comes from the Training Generator module itself, so
    this hero avoids duplicating the section title.
    """
    if st.session_state.get("active_section", DEFAULT_SECTION) != "Training Generator":
        return

    st.markdown(
        """
<div class="sportze-main-hero">
    <h1>Sportze.AI</h1>
    <h2>Your intelligent personal trainer/coach for any sport in the world</h2>
</div>
        """,
        unsafe_allow_html=True,
    )


def should_suppress_module_text(value: Any) -> bool:
    """Remove old explanatory homepage text without touching module files."""
    if not isinstance(value, str):
        return False
    cleaned = value.strip().lower()
    blocked_fragments = [
        "this section now starts as the default interface",
        "it unites the old homepage profile collection",
        "for non-cataloged sports, the chat still works",
        "future api can interpret those sports dynamically",
    ]
    return any(fragment in cleaned for fragment in blocked_fragments)


class SuppressOldTrainingCopy:
    """
    Context manager that suppresses only the old text the user asked to remove.
    It does not interfere with the actual chat, buttons, or generated plans.
    """

    def __enter__(self):
        self._old_write = st.write
        self._old_markdown = st.markdown

        def filtered_write(*args, **kwargs):
            if len(args) == 1 and should_suppress_module_text(args[0]):
                return None
            return self._old_write(*args, **kwargs)

        def filtered_markdown(body, *args, **kwargs):
            if should_suppress_module_text(body):
                return None
            return self._old_markdown(body, *args, **kwargs)

        st.write = filtered_write
        st.markdown = filtered_markdown
        return self

    def __exit__(self, exc_type, exc, tb):
        st.write = self._old_write
        st.markdown = self._old_markdown
        return False


# =============================================================================
# USAGE / PLAN HELPERS
# =============================================================================
def today_key() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def reset_daily_usage_if_needed() -> None:
    usage = st.session_state.get("daily_usage", {})
    if not isinstance(usage, dict) or usage.get("date") != today_key():
        st.session_state.daily_usage = {
            "date": today_key(),
            "training_generations": 0,
            "video_reviews": 0,
            "physio_sessions": 0,
            "counseling_sessions": 0,
        }
        st.session_state.section_visit_counted = {}


def get_plan() -> str:
    plan = st.session_state.get("selected_plan", "Pro")
    if plan not in PLAN_LIMITS:
        plan = "Pro"
    return plan


def get_plan_limit(limit_name: str) -> int:
    return int(PLAN_LIMITS.get(get_plan(), PLAN_LIMITS["Pro"]).get(limit_name, UNLIMITED_LIMIT))


def get_daily_used(counter_name: str) -> int:
    reset_daily_usage_if_needed()
    usage = st.session_state.get("daily_usage", {})
    return int(usage.get(counter_name, 0) or 0)


def increment_usage(counter_name: str) -> None:
    reset_daily_usage_if_needed()

    daily = st.session_state.get("daily_usage", {})
    daily[counter_name] = int(daily.get(counter_name, 0) or 0) + 1
    daily["date"] = today_key()
    st.session_state.daily_usage = daily

    counters = st.session_state.get("usage_counters", {})
    counters[counter_name] = int(counters.get(counter_name, 0) or 0) + 1
    st.session_state.usage_counters = counters

    add_audit_event("usage_incremented", {"counter": counter_name, "daily_used": daily[counter_name], "plan": get_plan()})


def can_use(counter_name: str, limit_name: str) -> bool:
    return get_daily_used(counter_name) < get_plan_limit(limit_name)


def usage_text(counter_name: str, limit_name: str) -> str:
    used = get_daily_used(counter_name)
    limit = get_plan_limit(limit_name)
    label = PLAN_LIMIT_LABELS.get(limit_name, limit_name)
    if limit >= UNLIMITED_LIMIT:
        return f"{label}: unlimited"
    return f"{label}: {used}/{limit} used today"


def render_limit_reached(counter_name: str, limit_name: str, module_name: str) -> None:
    used = get_daily_used(counter_name)
    limit = get_plan_limit(limit_name)
    st.warning(f"{module_name} limit reached for the {get_plan()} plan: {used}/{limit} today.")
    st.caption("Because monetization is not active yet, you can change the Plan dropdown at the top-right to test another tier.")


def render_usage_caption(counter_name: str, limit_name: str) -> None:
    text = usage_text(counter_name, limit_name)
    st.caption(text)


def count_section_visit_once(counter_name: str, limit_name: str, module_key: str, module_name: str) -> bool:
    """
    Counts a module use once per visit, not on every Streamlit rerun.
    Used for Physio and Video Review until those modules expose explicit callbacks.
    """
    reset_daily_usage_if_needed()
    visit_id = int(st.session_state.get("active_visit_counter", 0) or 0)
    counted = st.session_state.get("section_visit_counted", {})
    if not isinstance(counted, dict):
        counted = {}

    visit_key = f"{module_key}:{visit_id}:{today_key()}"
    if counted.get(visit_key):
        return True

    if not can_use(counter_name, limit_name):
        render_limit_reached(counter_name, limit_name, module_name)
        return False

    increment_usage(counter_name)
    counted[visit_key] = True
    st.session_state.section_visit_counted = counted
    return True


def training_generation_signature() -> str:
    latest_summary = st.session_state.get("latest_training_summary")
    latest_payload = st.session_state.get("latest_training_payload")
    saved_sessions = st.session_state.get("saved_training_sessions", [])
    raw = json.dumps(
        {
            "summary": latest_summary,
            "payload": latest_payload,
            "saved_count": len(saved_sessions) if isinstance(saved_sessions, list) else 0,
        },
        sort_keys=True,
        default=str,
    )
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def maybe_count_training_generation(before_signature: str) -> None:
    after_signature = training_generation_signature()
    last_counted = st.session_state.get("last_counted_training_signature", "")

    latest_exists = bool(st.session_state.get("latest_training_summary") or st.session_state.get("latest_training_payload"))
    if not latest_exists:
        return

    if after_signature == before_signature:
        return

    if after_signature == last_counted:
        return

    increment_usage("training_generations")
    st.session_state.last_counted_training_signature = after_signature


def render_plan_popover() -> None:
    with st.popover("Plan", use_container_width=True):
        plans = ["Free", "Plus", "Pro"]
        current = get_plan()
        selected = st.selectbox("Plan view", plans, index=plans.index(current), key="top_plan_select")
        st.session_state.selected_plan = selected
        reset_daily_usage_if_needed()

        st.caption("MVP plan preview. You can switch manually until monetization is connected.")

        limits = PLAN_LIMITS[selected]
        st.markdown("**Daily limits**")
        for limit_name, value in limits.items():
            label = PLAN_LIMIT_LABELS.get(limit_name, limit_name)
            shown = "Unlimited" if int(value) >= UNLIMITED_LIMIT else str(value)
            st.write(f"- {label}: {shown}")

        st.markdown("**Used today**")
        st.write(f"- Training generations: {get_daily_used('training_generations')}")
        st.write(f"- Physio sections: {get_daily_used('physio_sessions')}")
        st.write(f"- Video reviews: {get_daily_used('video_reviews')}")


# =============================================================================
# MODULE RENDERERS
# =============================================================================
def render_training_page() -> None:
    render_usage_caption("training_generations", "training_generations_per_day")
    if not can_use("training_generations", "training_generations_per_day"):
        render_limit_reached("training_generations", "training_generations_per_day", "Training Generator")
        return

    before_signature = training_generation_signature()
    with SuppressOldTrainingCopy():
        try:
            render_training_generator_section(on_persist=persist_if_logged_in)
        except TypeError:
            render_training_generator_section()
    maybe_count_training_generation(before_signature)


def render_video_page() -> None:
    render_usage_caption("video_reviews", "video_reviews_per_day")
    if not count_section_visit_once("video_reviews", "video_reviews_per_day", "video", "Video Review"):
        return
    render_video_review_section()


def render_counseling_page() -> None:
    # Counseling is intentionally generous while the product is still pre-monetization.
    if can_use("counseling_sessions", "counseling_sessions_per_day"):
        render_counseling_section()
    else:
        render_limit_reached("counseling_sessions", "counseling_sessions_per_day", "Counseling")


def render_physio_page() -> None:
    render_usage_caption("physio_sessions", "physio_sessions_per_day")
    if not count_section_visit_once("physio_sessions", "physio_sessions_per_day", "physio", "Physio"):
        return
    render_physio_section()


def render_active_section() -> None:
    section = st.session_state.get("active_section", DEFAULT_SECTION)

    if section == "Training Generator":
        render_training_page()
    elif section == "Video Review":
        render_video_page()
    elif section == "Counseling":
        render_counseling_page()
    elif section == "Physio":
        render_physio_page()
    else:
        st.warning("Unknown section selected.")
        set_active_section(DEFAULT_SECTION)


# =============================================================================
# PROFILE BRIDGE FOR MODULES
# =============================================================================
def expose_profile_for_modules() -> None:
    """
    Keeps compatibility with current and future module keys.
    The training generator, counseling, physio, and video review modules can read
    these values without needing to know whether the profile came from Google,
    email fallback, the old homepage, or chat onboarding.
    """
    profile = {
        "profile_email": st.session_state.get("profile_email", ""),
        "athlete_name": st.session_state.get("athlete_name", ""),
        "sport": st.session_state.get("sport", ""),
        "sport_type": st.session_state.get("sport_type", ""),
        "team_name": st.session_state.get("team_name", ""),
        "goal": st.session_state.get("goal", ""),
        "level": st.session_state.get("level", ""),
        "is_professional": st.session_state.get("is_professional", "No"),
        "weekly_target": st.session_state.get("weekly_target"),
        "selected_plan": st.session_state.get("selected_plan", "Pro"),
        "logged_in": current_auth_user().logged_in,
        "auth_provider": current_auth_user().provider,
    }

    # Common names used by older module versions.
    st.session_state.athlete_profile = profile
    st.session_state.profile = profile
    st.session_state.homepage_profile = profile
    st.session_state.home_profile = profile
    st.session_state.user_profile = profile
    st.session_state.sportze_profile = profile

    if st.session_state.get("sport") and not st.session_state.get("sport_type"):
        st.session_state.sport_type = detect_sport_type(st.session_state.sport)


# =============================================================================
# CLEAN SIDEBAR
# =============================================================================
def render_minimal_sidebar_escape_hatch() -> None:
    """
    The user asked to remove the sidebar clutter. The sidebar is hidden by CSS.
    This function keeps a developer/debug escape hatch only if explicitly enabled.
    """
    show_debug = bool_secret("SPORTZE_SHOW_DEBUG_SIDEBAR", False)
    if not show_debug:
        return

    with st.sidebar:
        st.markdown("### Debug")
        st.json(
            {
                "active_section": st.session_state.get("active_section"),
                "logged_in": current_auth_user().logged_in,
                "email": st.session_state.get("profile_email"),
                "profile_loaded": st.session_state.get("profile_loaded"),
                "last_saved_at": st.session_state.get("last_saved_at"),
            }
        )


# =============================================================================
# STATUS MESSAGES
# =============================================================================
def render_auth_status_message() -> None:
    if st.session_state.get("auth_error"):
        st.error(st.session_state.auth_error)
    elif st.session_state.get("auth_message"):
        st.toast(st.session_state.auth_message)


# =============================================================================
# MAIN
# =============================================================================
def main() -> None:
    init_state()
    reset_daily_usage_if_needed()
    inject_css()
    process_google_oauth_callback()
    expose_profile_for_modules()
    render_minimal_sidebar_escape_hatch()

    render_topbar()

    extra_left, extra_right = st.columns([5, 1], vertical_alignment="center")
    with extra_right:
        render_plan_popover()

    render_default_training_hero()
    render_auth_status_message()

    render_active_section()

    expose_profile_for_modules()
    persist_if_logged_in()


if __name__ == "__main__":
    main()
