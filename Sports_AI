"""
Sports AI section for Sportze.AI.

This is the default landing/search screen for the app. It is intentionally built
so the MVP works without an API, while keeping a clean handoff structure for the
future API layer.

Future API behavior:
- Replace classify_sports_ai_message() with an LLM/router call.
- Keep the same handoff keys in st.session_state so other modules do not need
  to change.
- The receiving modules can read sportze_intake_context / training_prefill and
  skip questions that were already answered by the user's first message.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from typing import Any, Callable, Dict, List, Optional, Tuple

import streamlit as st


SPORTS_AI_PUNS = [
    "Ask anything. We will take a shot at it.",
    "Your sports questions, no warm-up needed.",
    "From rules to results, we keep the ball rolling.",
    "One question can kick off everything.",
]

KNOWN_SPORTS = [
    "soccer", "football", "futsal", "basketball", "volleyball", "water polo",
    "tennis", "table tennis", "badminton", "baseball", "softball", "rugby",
    "american football", "cricket", "hockey", "field hockey", "ice hockey",
    "handball", "lacrosse", "netball", "running", "athletics", "track and field",
    "swimming", "cycling", "triathlon", "rowing", "gym", "fitness",
    "weightlifting", "powerlifting", "bodybuilding", "calisthenics", "boxing",
    "martial arts", "judo", "taekwondo", "karate", "wrestling", "golf",
    "surfing", "skateboarding", "climbing", "bouldering", "skiing",
    "snowboarding", "gymnastics", "crossfit",
]

TEAM_SPORTS = {
    "soccer", "football", "futsal", "basketball", "volleyball", "water polo",
    "baseball", "softball", "rugby", "american football", "cricket", "hockey",
    "field hockey", "ice hockey", "handball", "lacrosse", "netball",
}

TRAINING_TERMS = {
    "train", "training", "practice", "practise", "workout", "exercise", "session",
    "drill", "drills", "fitness", "conditioning", "improve", "get better",
    "learn to play", "learn how to play", "start playing", "begin", "beginner",
}

LEARN_TERMS = {
    "learn to play", "learn how to play", "start playing", "never played",
    "new sport", "beginner", "from zero", "from scratch", "how do i start",
}

PHYSIO_TERMS = {
    "pain", "hurts", "hurt", "injury", "injured", "sore", "sprain", "strain",
    "knee", "ankle", "shoulder", "elbow", "wrist", "back", "neck", "hip",
    "hamstring", "calf", "groin", "physio", "rehab", "rehabilitation",
}

COUNSELING_TERMS = {
    "confidence", "nervous", "anxious", "pressure", "motivation", "mindset",
    "mental", "counseling", "counselling", "scared", "fear", "focus",
    "burnout", "stress", "coach problem", "team problem", "sports psychology",
}

VIDEO_TERMS = {
    "video review", "analyze my video", "analyse my video", "form check",
    "technique review", "movement review", "upload video", "review my technique",
    "check my form", "look at my video",
}

YES_TERMS = {"yes", "yeah", "yep", "sure", "please", "i do", "i want", "train", "practice"}
NO_TERMS = {"no", "nope", "nah", "not", "do not", "don't", "dont"}

LEVEL_PATTERNS = [
    ("Elite/Pro", r"\b(elite|pro|professional|national team|national level|world class)\b"),
    ("Advanced", r"\b(advanced|very good|competitive|federated|club level)\b"),
    ("Intermediate", r"\b(intermediate|okay|decent|some experience|already play)\b"),
    ("Beginner", r"\b(beginner|new|never played|from zero|from scratch|start)\b"),
]

GOAL_PATTERNS = [
    ("Learn how to play", r"\b(learn to play|learn how to play|start playing|from zero|from scratch|never played|new sport)\b"),
    ("Improve technique", r"\b(technique|technical|skills|skill|shooting|passing|dribbling|serve|stroke)\b"),
    ("Improve fitness", r"\b(fitness|conditioning|physical|stamina|endurance|speed|strength|agility)\b"),
    ("Compete better", r"\b(compete|competition|match|game|tournament|race|performance)\b"),
]


@dataclass
class SportsAIIntent:
    target_section: str = "Sports AI"
    confidence: str = "low"
    needs_confirmation: bool = False
    sport: str = ""
    goal: str = ""
    level: str = ""
    sport_type: str = ""
    original_message: str = ""
    reason: str = ""


def _clean(text: Any) -> str:
    return " ".join(str(text or "").strip().split())


def _lower(text: Any) -> str:
    return _clean(text).lower()


def _contains_any(text: str, terms: set[str]) -> bool:
    return any(term in text for term in terms)


def detect_sport(text: str) -> str:
    lowered = _lower(text)
    # Longest first so "american football" wins before "football".
    for sport in sorted(KNOWN_SPORTS, key=len, reverse=True):
        if re.search(rf"(?<![a-z]){re.escape(sport)}(?![a-z])", lowered):
            # Normalize common ambiguity: if the user writes football and also says NFL/American,
            # keep American football. Otherwise football is treated as soccer for a world app.
            if sport == "football" and re.search(r"\b(nfl|american football|quarterback|touchdown)\b", lowered):
                return "american football"
            if sport == "football":
                return "soccer"
            return sport
    return ""


def detect_sport_type(sport: str) -> str:
    if not sport:
        return ""
    return "Team Sport" if sport in TEAM_SPORTS else "Individual Sport"


def detect_goal_and_level(text: str) -> Tuple[str, str]:
    lowered = _lower(text)
    goal = ""
    level = ""

    for detected_goal, pattern in GOAL_PATTERNS:
        if re.search(pattern, lowered):
            goal = detected_goal
            break

    for detected_level, pattern in LEVEL_PATTERNS:
        if re.search(pattern, lowered):
            level = detected_level
            break

    if goal == "Learn how to play":
        level = "Beginner"

    return goal, level


def classify_sports_ai_message(message: str) -> SportsAIIntent:
    lowered = _lower(message)
    sport = detect_sport(lowered)
    goal, level = detect_goal_and_level(lowered)
    sport_type = detect_sport_type(sport)

    if _contains_any(lowered, PHYSIO_TERMS):
        return SportsAIIntent(
            target_section="Physio",
            confidence="high",
            sport=sport,
            goal=goal,
            level=level,
            sport_type=sport_type,
            original_message=message,
            reason="The message mentions pain, injury, rehab, or a body area that should go to Physio.",
        )

    if _contains_any(lowered, VIDEO_TERMS):
        return SportsAIIntent(
            target_section="Video Review",
            confidence="high",
            sport=sport,
            goal=goal,
            level=level,
            sport_type=sport_type,
            original_message=message,
            reason="The message asks for video, form, movement, or technique review.",
        )

    if _contains_any(lowered, COUNSELING_TERMS):
        return SportsAIIntent(
            target_section="Counseling",
            confidence="high",
            sport=sport,
            goal=goal,
            level=level,
            sport_type=sport_type,
            original_message=message,
            reason="The message mentions mindset, motivation, confidence, stress, or sports counseling.",
        )

    clearly_training = _contains_any(lowered, TRAINING_TERMS)
    clearly_learning = _contains_any(lowered, LEARN_TERMS)

    if sport and (clearly_training or clearly_learning):
        if clearly_learning and not goal:
            goal = "Learn how to play"
            level = "Beginner"
        return SportsAIIntent(
            target_section="Training Generator",
            confidence="high",
            sport=sport,
            goal=goal or "Improve at this sport",
            level=level or "",
            sport_type=sport_type,
            original_message=message,
            reason="The user clearly asked to train, practice, improve, or learn a sport.",
        )

    if sport and not clearly_training:
        return SportsAIIntent(
            target_section="Training Generator",
            confidence="medium",
            needs_confirmation=True,
            sport=sport,
            goal=goal,
            level=level,
            sport_type=sport_type,
            original_message=message,
            reason="A sport was detected, but it is not totally clear whether the user wants to train it.",
        )

    if clearly_training or clearly_learning:
        return SportsAIIntent(
            target_section="Training Generator",
            confidence="medium",
            needs_confirmation=True,
            sport=sport,
            goal=goal or ("Learn how to play" if clearly_learning else ""),
            level=level or ("Beginner" if clearly_learning else ""),
            sport_type=sport_type,
            original_message=message,
            reason="Training intent was detected, but the sport may still need to be clarified.",
        )

    return SportsAIIntent(
        target_section="Sports AI",
        confidence="low",
        sport=sport,
        goal=goal,
        level=level,
        sport_type=sport_type,
        original_message=message,
        reason="The message looks like a general sports question for the future API answer mode.",
    )


def build_training_prefill(intent: SportsAIIntent) -> Dict[str, Any]:
    skip_questions: List[str] = []

    if intent.sport:
        skip_questions.append("sport")
    if intent.goal:
        skip_questions.append("goal")
    if intent.level:
        skip_questions.append("level")

    if intent.goal == "Learn how to play":
        skip_questions.extend(["goal", "level"])

    # Deduplicate while preserving order.
    deduped_skip_questions = list(dict.fromkeys(skip_questions))

    return {
        "source": "Sports AI",
        "original_message": intent.original_message,
        "sport": intent.sport,
        "sport_type": intent.sport_type,
        "goal": intent.goal,
        "level": intent.level,
        "skip_questions": deduped_skip_questions,
        "api_ready_notes": (
            "Future API should extract sport, goal, level, injury status, module intent, "
            "training style, available time, solo/group preference, frequency, fatigue, "
            "and then skip any repeated questions in the receiving module."
        ),
    }


def apply_handoff(intent: SportsAIIntent) -> None:
    handoff = {
        "source": "Sports AI",
        "target_section": intent.target_section,
        "confidence": intent.confidence,
        "sport": intent.sport,
        "sport_type": intent.sport_type,
        "goal": intent.goal,
        "level": intent.level,
        "original_message": intent.original_message,
        "reason": intent.reason,
    }
    st.session_state.sportze_intake_context = handoff
    st.session_state.last_sports_ai_intent = asdict(intent)

    if intent.sport:
        st.session_state.sport = intent.sport
        st.session_state.sport_type = intent.sport_type
    if intent.goal:
        st.session_state.goal = intent.goal
    if intent.level:
        st.session_state.level = intent.level

    if intent.target_section == "Training Generator":
        training_prefill = build_training_prefill(intent)
        st.session_state.training_prefill = training_prefill
        st.session_state.training_profile = {
            **st.session_state.get("training_profile", {}),
            **{k: v for k, v in training_prefill.items() if v},
        }
        st.session_state.training_skip_questions = training_prefill["skip_questions"]
        st.session_state.training_chat_started = False
        st.session_state.training_question_index = 0
        st.session_state.training_chat_complete = False
        st.session_state.generator_chat_messages = []

    if intent.target_section == "Physio":
        st.session_state.physio_prefill = handoff
    elif intent.target_section == "Counseling":
        st.session_state.counseling_prefill = handoff
    elif intent.target_section == "Video Review":
        st.session_state.video_review_prefill = handoff


def render_future_api_answer(message: str) -> None:
    st.info(
        "API answer mode placeholder: once the API is connected, Sports AI will search and answer this sports question directly here."
    )
    st.write(f"For now, I saved your question: **{message}**")


def handle_confirmation_response(response: str, navigate_to: Callable[[str], None]) -> None:
    lowered = _lower(response)
    pending = st.session_state.get("sports_ai_pending_intent", {})
    if not pending:
        return

    if any(term == lowered or term in lowered for term in YES_TERMS):
        intent = SportsAIIntent(**pending)
        intent.needs_confirmation = False
        intent.confidence = "high"
        apply_handoff(intent)
        st.session_state.sports_ai_pending_intent = {}
        navigate_to(intent.target_section)
        st.rerun()

    if any(term == lowered or term in lowered for term in NO_TERMS):
        st.session_state.sports_ai_pending_intent = {}
        st.session_state.sports_ai_messages.append({"role": "assistant", "content": "Ok, sorry. Carry on."})
        st.rerun()

    st.session_state.sports_ai_messages.append(
        {"role": "assistant", "content": "Just answer yes or no: do you want to practice/train this sport?"}
    )
    st.rerun()


def render_sports_ai_section(navigate_to: Optional[Callable[[str], None]] = None) -> None:
    """
    Render the Sports AI landing section.

    navigate_to(section_name) should be supplied by app.py so this section can
    redirect users into Training Generator, Physio, Counseling, or Video Review.
    """
    if navigate_to is None:
        navigate_to = lambda section_name: st.session_state.__setitem__("active_section", section_name)

    if "sports_ai_messages" not in st.session_state:
        st.session_state.sports_ai_messages = []
    if "sports_ai_pending_intent" not in st.session_state:
        st.session_state.sports_ai_pending_intent = {}

    st.markdown(
        """
<style>
    .sports-ai-wrap {
        max-width: 940px;
        margin: 3.4rem auto 1.6rem auto;
        text-align: center;
    }
    .sports-ai-pun {
        font-size: clamp(2.6rem, 5.5vw, 5.1rem);
        line-height: 0.96;
        letter-spacing: -0.065em;
        font-weight: 950;
        margin-bottom: 0.95rem;
    }
    .sports-ai-subtitle {
        max-width: 780px;
        margin: 0 auto 1.4rem auto;
        opacity: 0.78;
        font-size: clamp(1.0rem, 1.6vw, 1.18rem);
        line-height: 1.45;
    }
    .sports-ai-panel {
        max-width: 880px;
        margin: 0 auto 1.3rem auto;
        padding: 1rem;
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 28px;
        background: linear-gradient(145deg, rgba(255,255,255,0.075), rgba(255,255,255,0.03));
    }
</style>
<div class="sports-ai-wrap">
    <div class="sports-ai-pun">Ask anything. We will take a shot at it.</div>
    <div class="sports-ai-subtitle">
        Whatever you want to know in the sports world, news, results, learn about a new sport,
        rules, positions, and much more, all in one place. What's your question?
    </div>
</div>
        """,
        unsafe_allow_html=True,
    )

    with st.container():
        st.markdown('<div class="sports-ai-panel">', unsafe_allow_html=True)

        for msg in st.session_state.sports_ai_messages[-8:]:
            with st.chat_message(msg.get("role", "assistant")):
                st.write(msg.get("content", ""))

        question = st.chat_input("Ask Sports AI anything...")
        if question:
            st.session_state.sports_ai_messages.append({"role": "user", "content": question})

            if st.session_state.get("sports_ai_pending_intent"):
                handle_confirmation_response(question, navigate_to)
                return

            intent = classify_sports_ai_message(question)

            if intent.needs_confirmation:
                st.session_state.sports_ai_pending_intent = asdict(intent)
                st.session_state.sports_ai_messages.append(
                    {"role": "assistant", "content": "Do you want to practice/train this sport?"}
                )
                st.rerun()

            if intent.target_section in {"Training Generator", "Physio", "Counseling", "Video Review"} and intent.confidence == "high":
                apply_handoff(intent)
                navigate_to(intent.target_section)
                st.rerun()

            st.session_state.sports_ai_messages.append(
                {
                    "role": "assistant",
                    "content": (
                        "API answer mode placeholder: once the API is connected, I will search the sports world "
                        "and answer this directly here. For now, this question was saved."
                    ),
                }
            )
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    with st.expander("Developer handoff notes", expanded=False):
        st.write("The section writes these API-ready keys for other modules:")
        st.code(
            "sportze_intake_context\ntraining_prefill\ntraining_skip_questions\nphysio_prefill\ncounseling_prefill\nvideo_review_prefill",
            language="text",
        )
        if st.session_state.get("sportze_intake_context"):
            st.json(st.session_state.sportze_intake_context)
