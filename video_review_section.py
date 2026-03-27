import tempfile
from typing import Dict, List

import streamlit as st

try:
    import cv2
except Exception:
    cv2 = None

try:
    import mediapipe as mp
except Exception:
    mp = None


SPORT_MOVEMENT_KEYS: Dict[str, List[str]] = {
    "Tennis": ["Split step timing", "Contact point height", "Hip-shoulder rotation", "Recovery footwork"],
    "Soccer": ["First step explosiveness", "Body angle when turning", "Knee drive", "Balance during striking"],
    "Basketball": ["Change of direction posture", "Landing mechanics", "Ball protection", "Shot alignment"],
    "Volleyball": ["Approach timing", "Arm swing path", "Landing control", "Block hand position"],
    "Running": ["Cadence", "Foot strike", "Arm swing", "Posture"],
    "General": ["Posture", "Symmetry", "Joint control", "Tempo"],
}


def _get_pose_estimator():
    if mp is None:
        return None, "MediaPipe is not installed in this environment."

    # Works with modern mediapipe package layout
    pose_cls = None
    drawing_utils = None

    try:
        pose_cls = mp.solutions.pose.Pose
        drawing_utils = mp.solutions.drawing_utils
    except Exception:
        try:
            from mediapipe.python.solutions.pose import Pose as PoseAlt
            from mediapipe.python.solutions import drawing_utils as drawing_utils_alt
            pose_cls = PoseAlt
            drawing_utils = drawing_utils_alt
        except Exception as exc:
            return None, f"MediaPipe import failed: {exc}"

    return {"pose_cls": pose_cls, "drawing_utils": drawing_utils}, None



def analyze_video_basic(video_path: str, max_frames: int = 24):
    if cv2 is None:
        return None, ["OpenCV is not installed in this environment."]

    estimator, err = _get_pose_estimator()
    if err:
        return None, [err]

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None, ["Could not open the uploaded video."]

    pose = estimator["pose_cls"](static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

    frame_count = 0
    detected_frames = 0
    sample_image = None

    while cap.isOpened() and frame_count < max_frames:
        ok, frame = cap.read()
        if not ok:
            break
        frame_count += 1
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)
        if results.pose_landmarks:
            detected_frames += 1
            sample_image = rgb

    cap.release()
    pose.close()

    observations = [
        f"Frames checked: {frame_count}",
        f"Frames with pose landmarks detected: {detected_frames}",
    ]
    if detected_frames == 0:
        observations.append("No clear body landmarks were detected. Use a brighter video, full-body angle, and a more stable camera.")
    elif detected_frames < max(4, frame_count // 3):
        observations.append("Pose detection was inconsistent. Try a cleaner background and keep the whole body visible.")
    else:
        observations.append("Pose detection worked reasonably well on the sampled frames.")

    return sample_image, observations



def render_video_review_section() -> None:
    st.header("Video Review")
    st.write("Upload a video and get a basic movement review workflow with OpenCV + MediaPipe support.")

    sport = st.selectbox("Sport for the review", list(SPORT_MOVEMENT_KEYS.keys()))
    focus = st.multiselect("What do you want to review?", SPORT_MOVEMENT_KEYS[sport], default=SPORT_MOVEMENT_KEYS[sport][:2])
    uploaded = st.file_uploader("Upload a video", type=["mp4", "mov", "avi", "m4v"])

    st.caption("Best results: bright environment, stable camera, full body visible, side or front angle depending on the sport.")

    if uploaded is not None:
        st.video(uploaded)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
            tmp.write(uploaded.read())
            temp_path = tmp.name

        if st.button("Analyze Video", type="primary", use_container_width=True):
            image, observations = analyze_video_basic(temp_path)

            st.subheader("System observations")
            for item in observations:
                st.write(f"- {item}")

            if image is not None:
                st.image(image, caption="Sample detected frame", use_container_width=True)

            st.subheader("Coach review checklist")
            for item in focus:
                st.write(f"- Check: **{item}**")

            st.subheader("Practical feedback template")
            feedback = {
                "Tennis": "Look for balance before contact, spacing to the ball, and whether recovery steps start immediately after the hit.",
                "Soccer": "Check the plant foot, trunk angle, first step reaction, and whether the athlete stays balanced through the action.",
                "Basketball": "Check deceleration posture, knee alignment on landing, chest position, and whether the hips stay loaded in direction changes.",
                "Volleyball": "Look at approach rhythm, penultimate step, arm action, and landing symmetry.",
                "Running": "Review posture, cadence rhythm, overstriding signs, and arm-leg coordination.",
                "General": "Review posture, rhythm, joint control, and whether movement quality drops as fatigue rises.",
            }
            st.info(feedback[sport])

            if cv2 is None or mp is None:
                st.warning("This environment is missing either OpenCV or MediaPipe, so only partial functionality is available.")
