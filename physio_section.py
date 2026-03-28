from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Tuple

import streamlit as st


# ==========================================================
# ADVANCED SPORTS PHYSIO / TRIAGE SECTION
# - Keeps the original spirit of the current version
# - Adds a much larger anatomical catalog
# - Adds chat-style free-text "where does it hurt?"
# - Adds optional image upload dropbox for pain-area review
# - Adds sport-aware advice, stop rules, and load guidance
# - Ready to be connected to APIs later, but works now offline
# ==========================================================


SPORT_OPTIONS = [
    "Water Polo",
    "Soccer",
    "Tennis",
    "Basketball",
    "Volleyball",
    "Swimming",
    "Running",
    "Track & Field",
    "Rugby",
    "American Football",
    "Baseball",
    "Softball",
    "Handball",
    "Futsal",
    "Cycling",
    "Gym / Strength Training",
    "Martial Arts",
    "Other",
]

PAIN_TYPES = [
    "Sharp",
    "Dull",
    "Tightness",
    "Burning",
    "Stiffness",
    "Throbbing",
    "Aching",
    "Pins and needles",
    "Cramping",
    "Instability / giving way",
    "Other",
]

ONSET_OPTIONS = [
    "Today",
    "1-3 days ago",
    "This week",
    "1-3 weeks ago",
    "More than a month ago",
]

SEVERITY_DECISION = {
    "continue": "You may continue only modified activity if pain stays stable and movement quality remains good.",
    "reduce": "Reduce load, avoid painful ranges and explosive actions, and re-check symptoms over the next 24-72 hours.",
    "stop": "Stop the session today and switch to recovery and in-person medical/physio assessment if symptoms are strong.",
}

RED_FLAGS = [
    "Pain above 8/10",
    "Visible deformity",
    "Unable to bear weight",
    "Loss of strength or numbness",
    "Major swelling right away",
    "Fever or signs of infection",
    "Night pain that feels severe or unusual",
    "Loss of bladder or bowel control",
    "Pain after a major collision or fall",
    "Severe headache / neck trauma",
]


ANATOMY_ZONES: Dict[str, Dict[str, Any]] = {
    "head_neck": {
        "label": "Head / Neck",
        "keywords": [
            "head", "jaw", "tmj", "face", "eye", "ear", "neck", "cervical", "c-spine",
            "trapezius", "upper trap", "sternocleidomastoid", "scm", "scalene", "occipital",
        ],
        "common_issues": [
            "Neck muscle spasm or overload",
            "Postural neck irritation",
            "Impact-related neck symptoms",
            "Jaw clenching / TMJ tension",
        ],
        "mobility": [
            "Gentle neck rotations within pain-free range - 1 to 2 minutes",
            "Chin tucks - 2 sets of 8 slow reps",
            "Upper trap stretch - 2 x 20-30 seconds per side",
            "Thoracic extension over chair or foam roller - 1 to 2 minutes",
        ],
        "strength": [
            "Scapular retractions - 2 to 3 sets of 10 reps",
            "Isometric neck holds with hand resistance - 3 x 10 seconds each direction",
        ],
        "urgent_clues": [
            "Dizziness after trauma",
            "Concussion symptoms",
            "Numbness down the arm",
            "Severe headache after impact",
        ],
    },
    "shoulder": {
        "label": "Shoulder / Clavicle / Scapula",
        "keywords": [
            "shoulder", "rotator cuff", "supraspinatus", "infraspinatus", "teres minor", "subscapularis",
            "deltoid", "clavicle", "ac joint", "scapula", "shoulder blade", "labrum", "biceps tendon",
            "pec", "pectoralis", "lat", "lats",
        ],
        "common_issues": [
            "Overhead load irritation",
            "Scapular control issue",
            "Rotator cuff overload",
            "Throwing, serving, or contact-related irritation",
        ],
        "mobility": [
            "Pendulum swings - 1 to 2 minutes",
            "Thoracic rotation openers - 2 sets of 6 per side",
            "Wall slides in pain-free range - 2 sets of 8 reps",
            "Pec doorway stretch - 2 x 20-30 seconds",
        ],
        "strength": [
            "Band external rotations - 2 to 3 sets of 10 reps",
            "Scapular setting / retraction - 2 to 3 sets of 10 reps",
            "Serratus wall slide or reach - 2 sets of 8 reps",
        ],
        "urgent_clues": [
            "Obvious deformity",
            "Sudden pop with major weakness",
            "Cannot raise the arm after trauma",
        ],
    },
    "elbow_forearm": {
        "label": "Elbow / Forearm",
        "keywords": [
            "elbow", "forearm", "biceps", "triceps", "brachialis", "brachioradialis", "ulna", "radius",
            "tennis elbow", "golfer's elbow", "lateral elbow", "medial elbow", "extensor", "flexor",
        ],
        "common_issues": [
            "Grip or throwing overload",
            "Flexor/extensor tendon irritation",
            "Reactive soreness after high volume",
        ],
        "mobility": [
            "Wrist flexor stretch - 2 x 20 seconds",
            "Wrist extensor stretch - 2 x 20 seconds",
            "Pronation/supination gentle rotations - 2 sets of 10 reps",
        ],
        "strength": [
            "Light wrist extension eccentrics - 2 sets of 10 reps",
            "Isometric grip holds - 3 x 10 seconds",
            "Hammer pronation/supination control - 2 sets of 8 reps",
        ],
        "urgent_clues": [
            "Rapid swelling",
            "Cannot grip or extend the elbow after trauma",
        ],
    },
    "wrist_hand": {
        "label": "Wrist / Hand / Fingers",
        "keywords": [
            "wrist", "hand", "thumb", "finger", "metacarpal", "phalanges", "scaphoid", "carpal",
            "palm", "knuckle", "index", "middle finger", "ring finger", "pinky",
        ],
        "common_issues": [
            "Impact or fall-on-hand irritation",
            "Grip overload",
            "Wrist mobility restriction",
        ],
        "mobility": [
            "Wrist circles - 1 minute",
            "Finger tendon glides - 2 sets of 8 reps",
            "Gentle prayer stretch - 2 x 20 seconds",
        ],
        "strength": [
            "Soft ball squeeze - 2 sets of 10 reps",
            "Rubber band finger extension - 2 sets of 12 reps",
        ],
        "urgent_clues": [
            "Marked swelling after a fall",
            "Snuffbox pain / possible scaphoid issue",
            "Finger deformity",
        ],
    },
    "thoracic_back_ribs": {
        "label": "Upper Back / Thoracic / Ribs / Chest",
        "keywords": [
            "upper back", "thoracic", "t-spine", "rib", "ribs", "intercostal", "chest", "sternum",
            "pec", "pectoralis", "mid back", "rhomboid",
        ],
        "common_issues": [
            "Thoracic stiffness",
            "Rib/intercostal irritation",
            "Postural overload",
            "Breathing-related muscular pain",
        ],
        "mobility": [
            "Thoracic rotations - 2 sets of 6 per side",
            "Cat-camel - 1 to 2 minutes",
            "Open book drill - 2 sets of 6 per side",
        ],
        "strength": [
            "Band rows - 2 to 3 sets of 10 reps",
            "Prone Y/T low-load raises - 2 sets of 8 reps",
        ],
        "urgent_clues": [
            "Shortness of breath",
            "Chest pressure",
            "Severe pain after collision",
        ],
    },
    "lower_back": {
        "label": "Lower Back / Lumbar / SI Joint",
        "keywords": [
            "lower back", "back", "lumbar", "l-spine", "si joint", "sacroiliac", "ql", "quadratus lumborum",
            "erector spinae", "paraspinal", "spine",
        ],
        "common_issues": [
            "Load management issue",
            "Technique fatigue",
            "Rotation or extension irritation",
            "Muscle spasm or stiffness",
        ],
        "mobility": [
            "Cat-camel - 1 to 2 minutes",
            "Child's pose rock-back - 2 sets of 6 reps if comfortable",
            "Knee-to-chest gentle mobility - 2 sets of 6 per side",
            "Walking for 5-10 minutes if it eases symptoms",
        ],
        "strength": [
            "Dead bug - 2 sets of 6 per side",
            "Bird dog - 2 sets of 6 per side",
            "Glute bridge - 2 sets of 10 reps",
        ],
        "urgent_clues": [
            "Pain shooting below the knee",
            "Numbness or weakness",
            "Loss of bladder or bowel control",
        ],
    },
    "hip_groin_glute": {
        "label": "Hip / Groin / Glute",
        "keywords": [
            "hip", "groin", "glute", "glutes", "adductor", "abductor", "hamstring origin", "hip flexor",
            "psoas", "iliacus", "glute med", "glute max", "piriformis", "pelvis", "acetabulum",
        ],
        "common_issues": [
            "Direction-change overload",
            "Adductor tightness or reactive soreness",
            "Sprint-related hip flexor irritation",
            "Glute weakness or pelvic control issue",
        ],
        "mobility": [
            "90/90 hip switches - 2 sets of 6 per side",
            "Adductor rock-backs - 2 sets of 8 reps",
            "Hip flexor stretch - 2 x 20-30 seconds per side",
            "Figure-4 stretch - 2 x 20 seconds if comfortable",
        ],
        "strength": [
            "Adductor squeeze - 3 x 10 seconds",
            "Glute bridge - 2 sets of 10 reps",
            "Side-lying hip abduction - 2 sets of 10 reps",
            "Mini-band lateral walk - 2 x 8 steps each side",
        ],
        "urgent_clues": [
            "Sharp groin pain with kicking or acceleration",
            "Unable to push off normally",
            "Pain after a big twist or split position",
        ],
    },
    "thigh_quad_hamstring": {
        "label": "Thigh / Quad / Hamstring",
        "keywords": [
            "quad", "quadriceps", "hamstring", "thigh", "vastus", "rectus femoris", "biceps femoris",
            "semitendinosus", "semimembranosus", "it band", "iliotibial band",
        ],
        "common_issues": [
            "Sprint or acceleration overload",
            "Delayed soreness after hard sessions",
            "Strain-type symptoms",
        ],
        "mobility": [
            "Heel-to-glute quad stretch - 2 x 20 seconds",
            "Hamstring flossing - 2 sets of 8 reps",
            "Leg swings gentle - 1 minute",
        ],
        "strength": [
            "Bridge march - 2 sets of 8 reps",
            "Hamstring isometric heel digs - 3 x 10 seconds",
            "Split squat partial range - 2 sets of 8 reps if tolerable",
        ],
        "urgent_clues": [
            "Sudden pop or tearing feeling",
            "Large bruise",
            "Cannot jog or push off",
        ],
    },
    "knee": {
        "label": "Knee / Patella / Tendon",
        "keywords": [
            "knee", "kneecap", "patella", "patellar tendon", "acl", "pcl", "mcl", "lcl", "meniscus",
            "joint line", "quad tendon", "tibia", "fibula",
        ],
        "common_issues": [
            "Overuse from jumping or running",
            "Poor landing mechanics",
            "Load spike",
            "Patellar or tendon irritation",
        ],
        "mobility": [
            "Heel slides - 2 sets of 8 reps",
            "Calf stretch - 2 x 20-30 seconds",
            "Quad stretch - 2 x 20 seconds",
            "Ankle dorsiflexion mobility - 2 sets of 8 reps",
        ],
        "strength": [
            "Wall sit - 3 x 20-30 seconds if tolerable",
            "Spanish squat or band-supported squat hold - 3 x 20 seconds if available",
            "Straight-leg raise - 2 sets of 10 reps",
            "Glute bridge - 2 sets of 10 reps",
        ],
        "urgent_clues": [
            "Immediate swelling after twist",
            "Locking",
            "Giving way",
            "Cannot fully bear weight",
        ],
    },
    "shin_calf_achilles": {
        "label": "Shin / Calf / Achilles",
        "keywords": [
            "shin", "calf", "gastroc", "gastrocnemius", "soleus", "achilles", "tibia", "compartment",
            "lower leg", "shin splints",
        ],
        "common_issues": [
            "Running load spike",
            "Calf strain or tightness",
            "Achilles reactive soreness",
            "Shin stress irritation",
        ],
        "mobility": [
            "Ankle circles - 1 minute",
            "Bent-knee calf stretch - 2 x 20 seconds",
            "Straight-knee calf stretch - 2 x 20 seconds",
        ],
        "strength": [
            "Double-leg calf raise - 2 sets of 12 reps if tolerable",
            "Isometric calf hold at top - 3 x 10 seconds",
            "Tibialis raises against wall - 2 sets of 12 reps",
        ],
        "urgent_clues": [
            "Sudden snap in Achilles area",
            "Marked tenderness on bone",
            "Pain worsening with daily walking",
        ],
    },
    "ankle_foot": {
        "label": "Ankle / Foot / Toes",
        "keywords": [
            "ankle", "foot", "heel", "arch", "plantar fascia", "toes", "toe", "metatarsal", "navicular",
            "talus", "calcaneus", "peroneal", "posterior tibial", "achilles insertion",
        ],
        "common_issues": [
            "Landing or twist episode",
            "Stiffness after sprinting",
            "Reactive soreness",
            "Foot loading issue",
        ],
        "mobility": [
            "Ankle circles - 1 minute",
            "Alphabet with ankle - 1 set",
            "Calf mobility against wall - 2 sets of 8 reps",
            "Toe yoga / toe spread - 2 sets of 8 reps",
        ],
        "strength": [
            "Single-leg balance - 3 x 20 seconds if safe",
            "Band ankle inversion/eversion - 2 sets of 10 reps",
            "Short-foot arch activation - 2 sets of 8 reps",
        ],
        "urgent_clues": [
            "Large swelling",
            "Cannot bear weight",
            "Bone tenderness after twist or fall",
        ],
    },
}


SPORT_LOAD_GUIDANCE: Dict[str, Dict[str, List[str]]] = {
    "Water Polo": {
        "high_risk": ["Shoulder / Clavicle / Scapula", "Elbow / Forearm", "Lower Back / Lumbar / SI Joint", "Hip / Groin / Glute"],
        "notes": [
            "Throwing volume, contact, eggbeater kicking, and repeated overhead motion matter a lot.",
            "Pain during shots, blocking, wrestling, or eggbeater usually means load should be modified.",
        ],
    },
    "Tennis": {
        "high_risk": ["Shoulder / Clavicle / Scapula", "Elbow / Forearm", "Wrist / Hand / Fingers", "Knee / Patella / Tendon", "Hip / Groin / Glute"],
        "notes": [
            "Serve volume, forehand/backhand repetition, and hard court load can drive symptoms.",
            "Pain that rises with serving or deceleration should not be ignored.",
        ],
    },
    "Soccer": {
        "high_risk": ["Hip / Groin / Glute", "Thigh / Quad / Hamstring", "Knee / Patella / Tendon", "Shin / Calf / Achilles", "Ankle / Foot / Toes"],
        "notes": [
            "Acceleration, deceleration, kicking, and change of direction are major drivers.",
            "Sharp groin or hamstring pain should shift training immediately.",
        ],
    },
    "Basketball": {
        "high_risk": ["Knee / Patella / Tendon", "Ankle / Foot / Toes", "Shin / Calf / Achilles", "Lower Back / Lumbar / SI Joint"],
        "notes": [
            "Jumping, landing, repeated cutting, and total court load are key contributors.",
        ],
    },
    "Volleyball": {
        "high_risk": ["Shoulder / Clavicle / Scapula", "Knee / Patella / Tendon", "Ankle / Foot / Toes", "Lower Back / Lumbar / SI Joint"],
        "notes": [
            "Serving, spiking, blocking, and jumping load often shape symptoms.",
        ],
    },
    "Running": {
        "high_risk": ["Hip / Groin / Glute", "Knee / Patella / Tendon", "Shin / Calf / Achilles", "Ankle / Foot / Toes"],
        "notes": [
            "Mileage spikes, speed work, and hard surfaces are common load triggers.",
        ],
    },
    "Gym / Strength Training": {
        "high_risk": ["Shoulder / Clavicle / Scapula", "Lower Back / Lumbar / SI Joint", "Hip / Groin / Glute", "Knee / Patella / Tendon"],
        "notes": [
            "Load progression, technique fatigue, and depth/range choices matter.",
        ],
    },
}


GENERIC_SEARCH_TERMS = {
    "back": "Lower Back / Lumbar / SI Joint",
    "low back": "Lower Back / Lumbar / SI Joint",
    "lower back": "Lower Back / Lumbar / SI Joint",
    "upper back": "Upper Back / Thoracic / Ribs / Chest",
    "mid back": "Upper Back / Thoracic / Ribs / Chest",
    "groin": "Hip / Groin / Glute",
    "hip": "Hip / Groin / Glute",
    "glute": "Hip / Groin / Glute",
    "butt": "Hip / Groin / Glute",
    "hamstring": "Thigh / Quad / Hamstring",
    "quad": "Thigh / Quad / Hamstring",
    "thigh": "Thigh / Quad / Hamstring",
    "knee": "Knee / Patella / Tendon",
    "ankle": "Ankle / Foot / Toes",
    "foot": "Ankle / Foot / Toes",
    "toe": "Ankle / Foot / Toes",
    "heel": "Ankle / Foot / Toes",
    "calf": "Shin / Calf / Achilles",
    "shin": "Shin / Calf / Achilles",
    "achilles": "Shin / Calf / Achilles",
    "shoulder": "Shoulder / Clavicle / Scapula",
    "clavicle": "Shoulder / Clavicle / Scapula",
    "scapula": "Shoulder / Clavicle / Scapula",
    "elbow": "Elbow / Forearm",
    "forearm": "Elbow / Forearm",
    "wrist": "Wrist / Hand / Fingers",
    "hand": "Wrist / Hand / Fingers",
    "finger": "Wrist / Hand / Fingers",
    "neck": "Head / Neck",
    "head": "Head / Neck",
    "jaw": "Head / Neck",
    "rib": "Upper Back / Thoracic / Ribs / Chest",
    "chest": "Upper Back / Thoracic / Ribs / Chest",
}


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def infer_zone_from_text(text: str) -> Tuple[Optional[str], List[str]]:
    text_n = normalize_text(text)
    hits: List[Tuple[str, int, List[str]]] = []

    for zone_id, zone_info in ANATOMY_ZONES.items():
        matched_terms = [kw for kw in zone_info["keywords"] if kw.lower() in text_n]
        if matched_terms:
            hits.append((zone_id, len(matched_terms), matched_terms))

    for generic_term, mapped_label in GENERIC_SEARCH_TERMS.items():
        if generic_term in text_n:
            for zone_id, zone_info in ANATOMY_ZONES.items():
                if zone_info["label"] == mapped_label:
                    hits.append((zone_id, 1, [generic_term]))
                    break

    if not hits:
        return None, []

    hits.sort(key=lambda x: x[1], reverse=True)
    best_zone_id, _, matched = hits[0]
    return best_zone_id, sorted(set(matched))


def get_sport_notes(sport: str, zone_label: str) -> List[str]:
    data = SPORT_LOAD_GUIDANCE.get(sport, {})
    notes = list(data.get("notes", []))
    if zone_label in data.get("high_risk", []):
        notes.append(f"For {sport}, this area is commonly stressed, so training volume and intensity should be adjusted carefully.")
    return notes


def build_stop_recommendation(pain: int, swelling: str, red_flags: List[str], pain_type: str, can_train: str) -> Tuple[str, str]:
    if red_flags or pain >= 8 or swelling == "A lot" or can_train == "No":
        return "stop", SEVERITY_DECISION["stop"]
    if pain >= 6 or swelling == "A little" or pain_type in ["Sharp", "Burning", "Instability / giving way", "Pins and needles"]:
        return "reduce", SEVERITY_DECISION["reduce"]
    return "continue", SEVERITY_DECISION["continue"]


def get_time_based_guidance(onset: str) -> List[str]:
    mapping = {
        "Today": [
            "Keep the next 24-48 hours calm and monitor whether pain is rising, stable, or easing.",
            "Do not chase pain with hard stretching or explosive drills today.",
        ],
        "1-3 days ago": [
            "If symptoms are already trending down, gradual mobility and low-load work may help.",
            "If symptoms are rising each day, get it checked sooner.",
        ],
        "This week": [
            "Look for a clear load trigger such as matches, serving, throwing, sprinting, jumping, or gym spikes.",
            "If it is not improving by the end of the week, in-person evaluation becomes more important.",
        ],
        "1-3 weeks ago": [
            "Persistent symptoms beyond 1-3 weeks deserve a more structured return-to-sport plan.",
            "If you keep modifying activity but pain does not improve, seek a physio or sports medicine professional.",
        ],
        "More than a month ago": [
            "Chronic or recurring pain should not just be managed with random stretching.",
            "A professional assessment is strongly recommended to look at mechanics, strength deficits, and training load.",
        ],
    }
    return mapping.get(onset, [])


def get_burning_specific_guidance(pain_type: str) -> List[str]:
    if pain_type != "Burning":
        return []
    return [
        "Burning pain can sometimes reflect irritated tissue, overload, or occasionally nerve-related symptoms.",
        "Avoid aggressive stretching into burning pain.",
        "If burning spreads, tingles, or feels electrical, seek professional assessment more quickly.",
    ]


def render_zone_summary(zone: Dict[str, Any]) -> None:
    st.write("**Common possibilities to consider:**")
    for item in zone["common_issues"]:
        st.write(f"- {item}")

    st.write("**Mobility ideas:**")
    for item in zone["mobility"]:
        st.write(f"- {item}")

    st.write("**Early low-load strength / control ideas:**")
    for item in zone["strength"]:
        st.write(f"- {item}")


def render_uploaded_image_panel(uploaded_file) -> None:
    st.subheader("Visual pain-area upload")
    if uploaded_file is None:
        st.caption("Optional: upload an image so the athlete can visually indicate the painful area. This version stores and previews the file, and is ready for future API-based image analysis.")
        return

    st.image(uploaded_file, caption="Uploaded area image", use_container_width=True)
    st.info(
        "Image received. In this offline version, the program previews the uploaded image and uses your written description for triage. "
        "The structure is already ready for future API/vision integration so the image can later be analyzed automatically."
    )


def render_professional_escalation(onset: str, pain: int, red_flags: List[str], pain_type: str) -> None:
    st.write("**When to stop and get professional help:**")
    escalation_points = [
        "Stop immediately if pain becomes sharp, unstable, causes limping, or changes your movement a lot.",
        "Book a sports physio or doctor sooner if pain is persisting, recurring, or interfering with normal training.",
        "Seek urgent in-person care if there is major swelling, visible deformity, numbness, severe weakness, or inability to bear weight.",
    ]

    if onset in ["1-3 weeks ago", "More than a month ago"]:
        escalation_points.append("Because the issue has been going on for a while, a structured assessment is more strongly recommended.")
    if pain >= 7:
        escalation_points.append("Because the pain level is high, do not try to push through normal sport today.")
    if red_flags:
        escalation_points.append("Red flags were selected, so this should be treated more seriously and assessed in person.")
    if pain_type in ["Burning", "Pins and needles"]:
        escalation_points.append("Because symptoms may be irritable or nerve-related, professional assessment is more important if this persists.")

    for point in escalation_points:
        st.write(f"- {point}")


def render_physio_section() -> None:
    st.header("Physio")
    st.write(
        "A more advanced sports triage and self-care support tool. It does not diagnose injuries and does not replace a doctor or physiotherapist. "
        "It is built to be smarter, more sport-specific, and ready for future API upgrades."
    )

    st.subheader("Athlete profile")
    col1, col2 = st.columns(2)
    with col1:
        sport = st.selectbox("What sport do you practise?", SPORT_OPTIONS)
        pain = st.slider("Pain scale", 0, 10, 4)
        onset = st.selectbox("When did it start?", ONSET_OPTIONS)
        pain_type = st.selectbox("What type of pain is it?", PAIN_TYPES)
    with col2:
        swelling = st.radio("Is there swelling?", ["No", "A little", "A lot"], horizontal=True)
        can_train = st.radio("Can you still train normally right now?", ["Yes", "A little", "No"], horizontal=True)
        after_impact = st.radio("Did it start after a collision, fall, twist, or bad landing?", ["No", "Yes"], horizontal=True)
        side = st.selectbox("Which side?", ["Not sure / central", "Left", "Right", "Both"])

    st.subheader("Where does it hurt?")
    manual_area = st.selectbox(
        "Quick anatomical selector",
        [zone["label"] for zone in ANATOMY_ZONES.values()],
        index=7,
    )
    where_chat = st.text_area(
        "Write where it hurts in your own words",
        placeholder=(
            "Examples: burning pain in the front of my right knee below the kneecap after jumps...\n"
            "tightness in my left groin when I sprint...\n"
            "my back hurts after water polo shots..."
        ),
        height=120,
    )
    mechanism = st.text_area(
        "What happened?",
        placeholder="Example: landed awkwardly, after serves, after a match, after gym squats, after eggbeater, after sprinting...",
        height=100,
    )

    st.subheader("Upload visual pain-area reference")
    uploaded_file = st.file_uploader(
        "Optional: upload an image of the painful area or where the athlete marked the pain",
        type=["png", "jpg", "jpeg", "webp"],
        help="This adds the dropbox/upload step you asked for. The current version previews the image now and is ready for future vision API analysis.",
    )

    st.subheader("Red flags")
    selected_red_flags = st.multiselect("Select any that are happening", RED_FLAGS)

    if st.button("Evaluate", type="primary", use_container_width=True):
        inferred_zone_id, matched_terms = infer_zone_from_text(where_chat)

        selected_zone_id = None
        for zone_id, zone in ANATOMY_ZONES.items():
            if zone["label"] == manual_area:
                selected_zone_id = zone_id
                break

        final_zone_id = inferred_zone_id or selected_zone_id
        zone = ANATOMY_ZONES[final_zone_id]
        zone_label = zone["label"]

        decision_key, decision_text = build_stop_recommendation(
            pain=pain,
            swelling=swelling,
            red_flags=selected_red_flags,
            pain_type=pain_type,
            can_train=can_train,
        )

        st.subheader("Initial impression")
        if decision_key == "stop":
            st.error(decision_text)
        elif decision_key == "reduce":
            st.warning(decision_text)
        else:
            st.success(decision_text)

        st.write(f"**Best matched body area:** {zone_label}")
        if matched_terms:
            st.caption(f"Detected from your description: {', '.join(matched_terms)}")

        if after_impact == "Yes":
            st.warning("Because this started after trauma or a bad movement event, treat it more cautiously than a simple soreness pattern.")

        render_zone_summary(zone)

        st.write("**Sport-specific context:**")
        sport_notes = get_sport_notes(sport, zone_label)
        if sport_notes:
            for item in sport_notes:
                st.write(f"- {item}")
        else:
            st.write("- General rule: reduce the movements that directly reproduce pain and keep technique quality high.")

        st.write("**Time-based guidance:**")
        for item in get_time_based_guidance(onset):
            st.write(f"- {item}")

        burning_notes = get_burning_specific_guidance(pain_type)
        if burning_notes:
            st.write("**Burning-pain guidance:**")
            for item in burning_notes:
                st.write(f"- {item}")

        st.write("**Training decision today:**")
        if decision_key == "continue":
            st.write("- You may do modified technical work, lighter volume, and controlled movement only if symptoms do not rise during the session.")
        elif decision_key == "reduce":
            st.write("- Keep training light or partial. Remove sprinting, jumping, heavy lifting, maximal throwing/serving, or painful ranges depending on the body area.")
        else:
            st.write("- Avoid normal full training today. Prioritize recovery and arrange in-person assessment.")

        if where_chat.strip():
            st.info(f"Your pain description: {where_chat.strip()}")
        if mechanism.strip():
            st.info(f"Mechanism noted: {mechanism.strip()}")

        render_uploaded_image_panel(uploaded_file)
        render_professional_escalation(onset, pain, selected_red_flags, pain_type)

        st.write("**Urgent clues specific to this area:**")
        for item in zone["urgent_clues"]:
            st.write(f"- {item}")

        st.caption(
            "Educational support only, not a diagnosis. This version already includes the image-upload dropbox and the large anatomical catalog, "
            "and it is structured so you can later connect AI/API image review without rebuilding the section."
        )
