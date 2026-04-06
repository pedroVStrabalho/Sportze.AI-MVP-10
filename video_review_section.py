import math
import tempfile
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import numpy as np
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
    "Tennis": [
        "Split step timing",
        "Contact balance",
        "Hip-shoulder rotation",
        "Recovery footwork",
        "Lateral push-off quality",
    ],
    "Soccer": [
        "First step explosiveness",
        "Body angle when turning",
        "Knee drive",
        "Balance during striking",
        "Single-leg stability",
    ],
    "Basketball": [
        "Change of direction posture",
        "Landing mechanics",
        "Shot posture",
        "Deceleration control",
        "Single-leg stability",
    ],
    "Volleyball": [
        "Approach timing",
        "Arm swing path",
        "Landing control",
        "Block posture",
        "Jump mechanics",
    ],
    "Running": [
        "Cadence rhythm",
        "Foot strike pattern",
        "Arm swing",
        "Posture",
        "Hip-knee-ankle line",
    ],
    "General": [
        "Posture",
        "Symmetry",
        "Joint control",
        "Tempo",
        "Movement consistency",
    ],
}


LANDMARK_NAMES = {
    "nose": 0,
    "left_shoulder": 11,
    "right_shoulder": 12,
    "left_elbow": 13,
    "right_elbow": 14,
    "left_wrist": 15,
    "right_wrist": 16,
    "left_hip": 23,
    "right_hip": 24,
    "left_knee": 25,
    "right_knee": 26,
    "left_ankle": 27,
    "right_ankle": 28,
    "left_heel": 29,
    "right_heel": 30,
    "left_foot_index": 31,
    "right_foot_index": 32,
}


@dataclass
class FrameMetrics:
    timestamp: float
    left_knee_angle: Optional[float] = None
    right_knee_angle: Optional[float] = None
    left_hip_angle: Optional[float] = None
    right_hip_angle: Optional[float] = None
    left_elbow_angle: Optional[float] = None
    right_elbow_angle: Optional[float] = None
    shoulder_tilt_deg: Optional[float] = None
    hip_tilt_deg: Optional[float] = None
    trunk_lean_deg: Optional[float] = None
    knee_asymmetry_deg: Optional[float] = None
    hip_asymmetry_deg: Optional[float] = None
    ankle_distance_ratio: Optional[float] = None


def _get_pose_objects():
    if mp is None:
        return None, None, "MediaPipe is not installed in this environment."

    try:
        pose_cls = mp.solutions.pose.Pose
        drawing_utils = mp.solutions.drawing_utils
        pose_connections = mp.solutions.pose.POSE_CONNECTIONS
        return pose_cls, drawing_utils, pose_connections
    except Exception:
        try:
            from mediapipe.python.solutions.pose import Pose as PoseAlt
            from mediapipe.python.solutions import drawing_utils as drawing_utils_alt
            from mediapipe.python.solutions.pose import POSE_CONNECTIONS as pose_connections_alt
            return PoseAlt, drawing_utils_alt, pose_connections_alt
        except Exception as exc:
            return None, None, f"MediaPipe import failed: {exc}"


def _safe_point(landmarks, idx: int, visibility_threshold: float = 0.5) -> Optional[Tuple[float, float]]:
    if landmarks is None or idx >= len(landmarks):
        return None
    lm = landmarks[idx]
    vis = getattr(lm, "visibility", 1.0)
    if vis < visibility_threshold:
        return None
    return (lm.x, lm.y)


def _angle_3pt(a, b, c) -> Optional[float]:
    if a is None or b is None or c is None:
        return None

    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    c = np.array(c, dtype=float)

    ba = a - b
    bc = c - b

    norm_ba = np.linalg.norm(ba)
    norm_bc = np.linalg.norm(bc)
    if norm_ba == 0 or norm_bc == 0:
        return None

    cosine = np.dot(ba, bc) / (norm_ba * norm_bc)
    cosine = float(np.clip(cosine, -1.0, 1.0))
    angle = math.degrees(math.acos(cosine))
    return angle


def _segment_angle_deg(p1, p2) -> Optional[float]:
    if p1 is None or p2 is None:
        return None
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return math.degrees(math.atan2(dy, dx))


def _vertical_reference_angle_deg(p1, p2) -> Optional[float]:
    if p1 is None or p2 is None:
        return None
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return math.degrees(math.atan2(dx, dy))


def _distance(p1, p2) -> Optional[float]:
    if p1 is None or p2 is None:
        return None
    return float(math.dist(p1, p2))


def _mean_point(p1, p2) -> Optional[Tuple[float, float]]:
    if p1 is None or p2 is None:
        return None
    return ((p1[0] + p2[0]) / 2.0, (p1[1] + p2[1]) / 2.0)


def _extract_metrics(landmarks, timestamp: float) -> FrameMetrics:
    ls = _safe_point(landmarks, LANDMARK_NAMES["left_shoulder"])
    rs = _safe_point(landmarks, LANDMARK_NAMES["right_shoulder"])
    le = _safe_point(landmarks, LANDMARK_NAMES["left_elbow"])
    re = _safe_point(landmarks, LANDMARK_NAMES["right_elbow"])
    lw = _safe_point(landmarks, LANDMARK_NAMES["left_wrist"])
    rw = _safe_point(landmarks, LANDMARK_NAMES["right_wrist"])
    lh = _safe_point(landmarks, LANDMARK_NAMES["left_hip"])
    rh = _safe_point(landmarks, LANDMARK_NAMES["right_hip"])
    lk = _safe_point(landmarks, LANDMARK_NAMES["left_knee"])
    rk = _safe_point(landmarks, LANDMARK_NAMES["right_knee"])
    la = _safe_point(landmarks, LANDMARK_NAMES["left_ankle"])
    ra = _safe_point(landmarks, LANDMARK_NAMES["right_ankle"])

    mid_shoulders = _mean_point(ls, rs)
    mid_hips = _mean_point(lh, rh)

    left_knee_angle = _angle_3pt(lh, lk, la)
    right_knee_angle = _angle_3pt(rh, rk, ra)
    left_hip_angle = _angle_3pt(ls, lh, lk)
    right_hip_angle = _angle_3pt(rs, rh, rk)
    left_elbow_angle = _angle_3pt(ls, le, lw)
    right_elbow_angle = _angle_3pt(rs, re, rw)

    shoulder_tilt = _segment_angle_deg(ls, rs)
    hip_tilt = _segment_angle_deg(lh, rh)
    trunk_lean = _vertical_reference_angle_deg(mid_hips, mid_shoulders)

    knee_asymmetry = None
    if left_knee_angle is not None and right_knee_angle is not None:
        knee_asymmetry = abs(left_knee_angle - right_knee_angle)

    hip_asymmetry = None
    if left_hip_angle is not None and right_hip_angle is not None:
        hip_asymmetry = abs(left_hip_angle - right_hip_angle)

    ankle_distance_ratio = None
    ankle_dist = _distance(la, ra)
    hip_dist = _distance(lh, rh)
    if ankle_dist is not None and hip_dist not in (None, 0):
        ankle_distance_ratio = ankle_dist / hip_dist

    return FrameMetrics(
        timestamp=timestamp,
        left_knee_angle=left_knee_angle,
        right_knee_angle=right_knee_angle,
        left_hip_angle=left_hip_angle,
        right_hip_angle=right_hip_angle,
        left_elbow_angle=left_elbow_angle,
        right_elbow_angle=right_elbow_angle,
        shoulder_tilt_deg=shoulder_tilt,
        hip_tilt_deg=hip_tilt,
        trunk_lean_deg=trunk_lean,
        knee_asymmetry_deg=knee_asymmetry,
        hip_asymmetry_deg=hip_asymmetry,
        ankle_distance_ratio=ankle_distance_ratio,
    )


def _summarize_metric(values: List[Optional[float]]) -> Dict[str, Optional[float]]:
    clean = [float(v) for v in values if v is not None]
    if not clean:
        return {"mean": None, "min": None, "max": None, "range": None}
    return {
        "mean": float(np.mean(clean)),
        "min": float(np.min(clean)),
        "max": float(np.max(clean)),
        "range": float(np.max(clean) - np.min(clean)),
    }


def _sport_feedback(sport: str, summary: Dict[str, Dict[str, Optional[float]]]) -> List[str]:
    feedback = []

    trunk_mean = summary["trunk_lean"]["mean"]
    knee_asym = summary["knee_asymmetry"]["mean"]
    hip_asym = summary["hip_asymmetry"]["mean"]
    shoulder_tilt = summary["shoulder_tilt"]["mean"]
    knee_rom = max(
        summary["left_knee"]["range"] or 0,
        summary["right_knee"]["range"] or 0,
    )

    if trunk_mean is not None:
        if abs(trunk_mean) > 18:
            feedback.append("There is quite a lot of trunk lean. Try to keep the chest more controlled through the main action.")
        elif abs(trunk_mean) < 5:
            feedback.append("Trunk posture looks relatively controlled and centered in the sampled movement.")

    if knee_asym is not None:
        if knee_asym > 18:
            feedback.append("The left and right knee mechanics look noticeably different. That can suggest imbalance, compensation, or unstable technique.")
        elif knee_asym > 10:
            feedback.append("There is some knee asymmetry. It would be worth improving left-right consistency.")
        else:
            feedback.append("Knee mechanics look fairly symmetrical in the detected frames.")

    if hip_asym is not None and hip_asym > 15:
        feedback.append("Hip positions vary quite a lot side to side. This can reduce power transfer and movement efficiency.")

    if shoulder_tilt is not None and abs(shoulder_tilt) > 12:
        feedback.append("Shoulder line is tilted quite a bit during the action. Watch upper-body control and balance.")

    if knee_rom < 12:
        feedback.append("The movement seems a bit stiff through the knees. You may need better loading and unloading through the legs.")
    elif knee_rom > 45:
        feedback.append("There is large knee angle change, which is good for dynamic actions, but make sure it stays controlled and aligned.")

    if sport == "Tennis":
        feedback.append("For tennis, pay special attention to balance before contact, the push-off leg, and whether recovery starts immediately after the action.")
    elif sport == "Soccer":
        feedback.append("For soccer, focus on plant-foot stability, trunk position, and whether the support leg stays strong through the movement.")
    elif sport == "Basketball":
        feedback.append("For basketball, landing control and deceleration posture are key. Try to keep knees tracking cleanly over the feet.")
    elif sport == "Volleyball":
        feedback.append("For volleyball, look for good loading before takeoff and symmetrical landing mechanics.")
    elif sport == "Running":
        feedback.append("For running, look for stable posture, efficient arm-leg rhythm, and reduced side-to-side collapse.")
    else:
        feedback.append("Overall, the movement review suggests focusing on posture, symmetry, and consistency across repetitions.")

    return feedback


def analyze_video_advanced(
    video_path: str,
    sample_every_n_frames: int = 2,
    max_frames_to_analyze: int = 180,
    draw_landmarks: bool = True,
):
    if cv2 is None:
        return None, None, ["OpenCV is not installed in this environment."], None

    pose_cls, drawing_utils, pose_connections = _get_pose_objects()
    if pose_cls is None:
        return None, None, ["MediaPipe is not installed or could not be imported."], None

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None, None, ["Could not open the uploaded video."], None

    fps = cap.get(cv2.CAP_PROP_FPS)
    if not fps or fps <= 0:
        fps = 30.0

    frame_idx = 0
    analyzed_frames = 0
    detected_frames = 0
    sample_frame_rgb = None
    annotated_frame_rgb = None
    metrics: List[FrameMetrics] = []

    pose = pose_cls(
        static_image_mode=False,
        model_complexity=1,
        enable_segmentation=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )

    while cap.isOpened():
        ok, frame = cap.read()
        if not ok:
            break

        frame_idx += 1
        if frame_idx % sample_every_n_frames != 0:
            continue

        analyzed_frames += 1
        if analyzed_frames > max_frames_to_analyze:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)

        if results.pose_landmarks:
            detected_frames += 1
            timestamp = frame_idx / fps
            frame_metrics = _extract_metrics(results.pose_landmarks.landmark, timestamp=timestamp)
            metrics.append(frame_metrics)

            if sample_frame_rgb is None:
                sample_frame_rgb = rgb.copy()

            if annotated_frame_rgb is None:
                annotated = rgb.copy()
                if draw_landmarks:
                    drawing_utils.draw_landmarks(
                        annotated,
                        results.pose_landmarks,
                        pose_connections,
                    )
                annotated_frame_rgb = annotated

    cap.release()
    pose.close()

    observations = [
        f"Frames sampled: {analyzed_frames}",
        f"Frames with body landmarks detected: {detected_frames}",
    ]

    if analyzed_frames == 0:
        observations.append("No frames were analyzed from the uploaded file.")
        return None, None, observations, None

    detection_rate = detected_frames / analyzed_frames if analyzed_frames else 0.0
    observations.append(f"Detection rate: {detection_rate:.0%}")

    if detected_frames == 0:
        observations.append("No usable pose landmarks were detected. Use a brighter video, cleaner background, and keep the full body visible.")
        return sample_frame_rgb, annotated_frame_rgb, observations, None

    if detection_rate < 0.4:
        observations.append("Pose tracking was inconsistent. Try a more stable camera angle and make sure the athlete stays fully in frame.")
    elif detection_rate < 0.75:
        observations.append("Pose tracking worked moderately well, but some parts of the action may still be missed.")
    else:
        observations.append("Pose tracking worked well across the sampled frames.")

    summary = {
        "left_knee": _summarize_metric([m.left_knee_angle for m in metrics]),
        "right_knee": _summarize_metric([m.right_knee_angle for m in metrics]),
        "left_hip": _summarize_metric([m.left_hip_angle for m in metrics]),
        "right_hip": _summarize_metric([m.right_hip_angle for m in metrics]),
        "left_elbow": _summarize_metric([m.left_elbow_angle for m in metrics]),
        "right_elbow": _summarize_metric([m.right_elbow_angle for m in metrics]),
        "trunk_lean": _summarize_metric([m.trunk_lean_deg for m in metrics]),
        "shoulder_tilt": _summarize_metric([m.shoulder_tilt_deg for m in metrics]),
        "hip_tilt": _summarize_metric([m.hip_tilt_deg for m in metrics]),
        "knee_asymmetry": _summarize_metric([m.knee_asymmetry_deg for m in metrics]),
        "hip_asymmetry": _summarize_metric([m.hip_asymmetry_deg for m in metrics]),
        "stance_ratio": _summarize_metric([m.ankle_distance_ratio for m in metrics]),
    }

    return sample_frame_rgb, annotated_frame_rgb, observations, summary


def _format_metric_block(title: str, metric: Dict[str, Optional[float]], suffix: str = "°"):
    mean = metric.get("mean")
    min_v = metric.get("min")
    max_v = metric.get("max")
    range_v = metric.get("range")

    st.markdown(f"**{title}**")
    if mean is None:
        st.write("No reliable data.")
        return

    if suffix:
        st.write(f"Mean: {mean:.1f}{suffix}")
        st.write(f"Min/Max: {min_v:.1f}{suffix} / {max_v:.1f}{suffix}")
        st.write(f"Range: {range_v:.1f}{suffix}")
    else:
        st.write(f"Mean: {mean:.2f}")
        st.write(f"Min/Max: {min_v:.2f} / {max_v:.2f}")
        st.write(f"Range: {range_v:.2f}")


def render_video_review_section() -> None:
    st.header("Video Review")
    st.write("Upload a sports video and get a more real movement review using OpenCV + MediaPipe pose tracking.")

    if cv2 is None:
        st.error("OpenCV is not installed. Add opencv-python-headless to your requirements.")
    if mp is None:
        st.error("MediaPipe is not installed. Add mediapipe to your requirements.")

    sport = st.selectbox("Sport for the review", list(SPORT_MOVEMENT_KEYS.keys()))
    focus = st.multiselect(
        "What do you want to review?",
        SPORT_MOVEMENT_KEYS[sport],
        default=SPORT_MOVEMENT_KEYS[sport][:2],
    )

    angle_view = st.selectbox(
        "Video angle",
        ["Side view", "Front view", "45-degree view", "Not sure"],
        index=0,
    )

    uploaded = st.file_uploader("Upload a video", type=["mp4", "mov", "avi", "m4v"])

    st.caption(
        "Best results: full body visible, bright environment, stable camera, athlete centered in the frame, and action repeated more than once if possible."
    )

    if uploaded is None:
        return

    st.video(uploaded)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(uploaded.read())
        temp_path = tmp.name

    col1, col2 = st.columns(2)
    with col1:
        sample_every_n_frames = st.slider("Analyze every Nth frame", 1, 5, 2)
    with col2:
        max_frames_to_analyze = st.slider("Maximum sampled frames", 60, 300, 180, step=20)

    if st.button("Analyze Video", type="primary", use_container_width=True):
        sample_img, annotated_img, observations, summary = analyze_video_advanced(
            temp_path,
            sample_every_n_frames=sample_every_n_frames,
            max_frames_to_analyze=max_frames_to_analyze,
            draw_landmarks=True,
        )

        st.subheader("System observations")
        for item in observations:
            st.write(f"- {item}")

        img_col1, img_col2 = st.columns(2)
        with img_col1:
            if sample_img is not None:
                st.image(sample_img, caption="Sample frame", use_container_width=True)
        with img_col2:
            if annotated_img is not None:
                st.image(annotated_img, caption="Pose-tracked frame", use_container_width=True)

        if summary is None:
            st.warning("The system could not extract enough reliable movement data from this video.")
            return

        st.subheader("Movement metrics")
        mcol1, mcol2, mcol3 = st.columns(3)

        with mcol1:
            _format_metric_block("Left knee angle", summary["left_knee"])
            _format_metric_block("Right knee angle", summary["right_knee"])
            _format_metric_block("Knee asymmetry", summary["knee_asymmetry"])

        with mcol2:
            _format_metric_block("Left hip angle", summary["left_hip"])
            _format_metric_block("Right hip angle", summary["right_hip"])
            _format_metric_block("Hip asymmetry", summary["hip_asymmetry"])

        with mcol3:
            _format_metric_block("Trunk lean", summary["trunk_lean"])
            _format_metric_block("Shoulder tilt", summary["shoulder_tilt"])
            _format_metric_block("Stance ratio", summary["stance_ratio"], suffix="")

        st.subheader("Coach review checklist")
        for item in focus:
            st.write(f"- Check: **{item}**")

        st.subheader("Automatic movement feedback")
        feedback_items = _sport_feedback(sport, summary)

        if angle_view == "Front view":
            feedback_items.append("Front-view videos are best for left-right comparison, knee tracking, and landing symmetry.")
        elif angle_view == "Side view":
            feedback_items.append("Side-view videos are best for trunk angle, loading mechanics, and extension/flexion timing.")
        elif angle_view == "45-degree view":
            feedback_items.append("A 45-degree view can help, but some measurements may be less precise than a clean side or front view.")

        for item in feedback_items:
            st.write(f"- {item}")

        st.subheader("Important note")
        st.info(
            "This feature gives movement-quality feedback, not a medical diagnosis. It works best as a coaching and screening tool."
        )
