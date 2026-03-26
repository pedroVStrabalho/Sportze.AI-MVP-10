import os
import cv2
import math
import time
import tempfile
import statistics
import streamlit as st
import mediapipe as mp

# =========================
# MEDIAPIPE SETUP
# =========================
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils


def _calculate_angle(a, b, c):
    """
    Calculate angle ABC in degrees.
    a, b, c = (x, y)
    """
    ax, ay = a
    bx, by = b
    cx, cy = c

    ba = (ax - bx, ay - by)
    bc = (cx - bx, cy - by)

    dot = ba[0] * bc[0] + ba[1] * bc[1]
    mag_ba = math.sqrt(ba[0] ** 2 + ba[1] ** 2)
    mag_bc = math.sqrt(bc[0] ** 2 + bc[1] ** 2)

    if mag_ba == 0 or mag_bc == 0:
        return None

    cos_angle = max(-1.0, min(1.0, dot / (mag_ba * mag_bc)))
    angle = math.degrees(math.acos(cos_angle))
    return angle


def _landmark_xy(landmarks, idx, width, height):
    lm = landmarks[idx]
    return (int(lm.x * width), int(lm.y * height))


def _safe_visibility(landmarks, idx, threshold=0.50):
    return landmarks[idx].visibility >= threshold


def _analyze_frame_pose(landmarks, width, height):
    """
    Extract simple biomechanical indicators from one frame.
    Returns dict with angles if available.
    """
    L = mp_pose.PoseLandmark

    needed = [
        L.LEFT_SHOULDER.value,
        L.RIGHT_SHOULDER.value,
        L.LEFT_ELBOW.value,
        L.RIGHT_ELBOW.value,
        L.LEFT_WRIST.value,
        L.RIGHT_WRIST.value,
        L.LEFT_HIP.value,
        L.RIGHT_HIP.value,
        L.LEFT_KNEE.value,
        L.RIGHT_KNEE.value,
        L.LEFT_ANKLE.value,
        L.RIGHT_ANKLE.value,
    ]

    for idx in needed:
        if not _safe_visibility(landmarks, idx):
            return {}

    left_shoulder = _landmark_xy(landmarks, L.LEFT_SHOULDER.value, width, height)
    right_shoulder = _landmark_xy(landmarks, L.RIGHT_SHOULDER.value, width, height)
    left_elbow = _landmark_xy(landmarks, L.LEFT_ELBOW.value, width, height)
    right_elbow = _landmark_xy(landmarks, L.RIGHT_ELBOW.value, width, height)
    left_wrist = _landmark_xy(landmarks, L.LEFT_WRIST.value, width, height)
    right_wrist = _landmark_xy(landmarks, L.RIGHT_WRIST.value, width, height)
    left_hip = _landmark_xy(landmarks, L.LEFT_HIP.value, width, height)
    right_hip = _landmark_xy(landmarks, L.RIGHT_HIP.value, width, height)
    left_knee = _landmark_xy(landmarks, L.LEFT_KNEE.value, width, height)
    right_knee = _landmark_xy(landmarks, L.RIGHT_KNEE.value, width, height)
    left_ankle = _landmark_xy(landmarks, L.LEFT_ANKLE.value, width, height)
    right_ankle = _landmark_xy(landmarks, L.RIGHT_ANKLE.value, width, height)

    data = {}

    # Elbow angles
    data["left_elbow_angle"] = _calculate_angle(left_shoulder, left_elbow, left_wrist)
    data["right_elbow_angle"] = _calculate_angle(right_shoulder, right_elbow, right_wrist)

    # Knee angles
    data["left_knee_angle"] = _calculate_angle(left_hip, left_knee, left_ankle)
    data["right_knee_angle"] = _calculate_angle(right_hip, right_knee, right_ankle)

    # Hip angles
    data["left_hip_angle"] = _calculate_angle(left_shoulder, left_hip, left_knee)
    data["right_hip_angle"] = _calculate_angle(right_shoulder, right_hip, right_knee)

    # Shoulder line balance
    shoulder_diff = abs(left_shoulder[1] - right_shoulder[1])
    data["shoulder_balance_px"] = shoulder_diff

    # Hip line balance
    hip_diff = abs(left_hip[1] - right_hip[1])
    data["hip_balance_px"] = hip_diff

    return data


def _summarize_metrics(all_metrics, sport):
    """
    Simple coaching summary from collected frame metrics.
    """
    if not all_metrics:
        return {
            "summary": "No reliable body landmarks were detected often enough to produce feedback.",
            "tips": [
                "Upload a brighter video.",
                "Use a side or front angle with the full body visible.",
                "Avoid heavy occlusion.",
            ],
        }

    def avg(key):
        vals = [m[key] for m in all_metrics if key in m and m[key] is not None]
        return round(statistics.mean(vals), 1) if vals else None

    left_knee = avg("left_knee_angle")
    right_knee = avg("right_knee_angle")
    left_hip = avg("left_hip_angle")
    right_hip = avg("right_hip_angle")
    shoulder_balance = avg("shoulder_balance_px")
    hip_balance = avg("hip_balance_px")

    tips = []

    if shoulder_balance is not None and shoulder_balance > 25:
        tips.append("Upper body looks uneven at times. Try to keep shoulders more level through the movement.")

    if hip_balance is not None and hip_balance > 25:
        tips.append("Hip line shifts noticeably. Focus on balance and trunk control.")

    if left_knee is not None and left_knee < 135:
        tips.append("Left knee bend is relatively deep. Make sure the movement stays controlled and stable.")

    if right_knee is not None and right_knee < 135:
        tips.append("Right knee bend is relatively deep. Keep knee tracking aligned over the foot.")

    if left_hip is not None and left_hip < 130:
        tips.append("Left hip angle suggests a lower loaded position. Maintain core tension to avoid collapsing.")

    if right_hip is not None and right_hip < 130:
        tips.append("Right hip angle suggests a lower loaded position. Keep posture strong through the trunk.")

    if sport == "Tennis":
        tips.append("For tennis, try recording from the side on serves and from behind on groundstrokes for better review.")
    elif sport == "Soccer":
        tips.append("For soccer, use clips with full-body shooting, sprinting, or change-of-direction actions.")
    elif sport == "Basketball":
        tips.append("For basketball, lateral defense and jump-stop clips usually give cleaner movement feedback.")
    elif sport == "Surfing":
        tips.append("For surfing, pop-up and stance clips on land are easier to analyze than water footage.")
    elif sport == "Water Polo":
        tips.append("Water polo is harder for pose tracking because of water occlusion, so dry-land movement clips work better.")

    if not tips:
        tips = [
            "Movement looked generally stable in the sampled frames.",
            "Try a closer angle or a more specific action clip for more useful feedback.",
        ]

    summary = (
        f"Processed movement successfully. "
        f"Avg shoulder imbalance: {shoulder_balance}px, "
        f"avg hip imbalance: {hip_balance}px, "
        f"avg knee angles: L {left_knee}°, R {right_knee}°."
    )

    return {
        "summary": summary,
        "tips": tips,
    }


def run_video_review():
    st.header("Video Review")

    st.write("Upload a sports video and get basic pose-based feedback.")

    sport = st.selectbox(
        "Which sport is this clip for?",
        ["Tennis", "Soccer", "Basketball", "Water Polo", "Surfing", "General"]
    )

    uploaded_video = st.file_uploader("Upload your video", type=["mp4", "mov", "avi", "m4v"])

    sample_every_n_frames = st.slider("Analyze every Nth frame", 1, 5, 2)
    draw_landmarks = st.checkbox("Draw pose landmarks on output video", value=True)

    if uploaded_video is not None:
        st.video(uploaded_video)

    if uploaded_video is not None and st.button("Run Video Analysis"):
        with st.spinner("Processing video with OpenCV + MediaPipe..."):
            input_temp_path = None
            output_temp_path = None

            try:
                # Save uploaded file to temp file
                suffix = os.path.splitext(uploaded_video.name)[1] or ".mp4"
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_in:
                    tmp_in.write(uploaded_video.read())
                    input_temp_path = tmp_in.name

                cap = cv2.VideoCapture(input_temp_path)
                if not cap.isOpened():
                    st.error("Could not open the uploaded video.")
                    return

                fps = cap.get(cv2.CAP_PROP_FPS)
                if fps <= 0:
                    fps = 25.0

                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

                # Output video path
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_out:
                    output_temp_path = tmp_out.name

                fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                writer = cv2.VideoWriter(output_temp_path, fourcc, fps, (width, height))

                all_metrics = []
                frame_idx = 0
                analyzed_frames = 0
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                progress = st.progress(0)

                start_time = time.time()

                with mp_pose.Pose(
                    static_image_mode=False,
                    model_complexity=1,
                    smooth_landmarks=True,
                    enable_segmentation=False,
                    min_detection_confidence=0.5,
                    min_tracking_confidence=0.5,
                ) as pose:

                    while True:
                        ret, frame = cap.read()
                        if not ret:
                            break

                        frame_idx += 1
                        output_frame = frame.copy()

                        if frame_idx % sample_every_n_frames == 0:
                            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                            results = pose.process(rgb)

                            if results.pose_landmarks:
                                analyzed_frames += 1

                                metrics = _analyze_frame_pose(
                                    results.pose_landmarks.landmark,
                                    width,
                                    height
                                )
                                if metrics:
                                    all_metrics.append(metrics)

                                if draw_landmarks:
                                    mp_drawing.draw_landmarks(
                                        output_frame,
                                        results.pose_landmarks,
                                        mp_pose.POSE_CONNECTIONS
                                    )

                        writer.write(output_frame)

                        if total_frames > 0:
                            progress.progress(min(frame_idx / total_frames, 1.0))

                cap.release()
                writer.release()

                elapsed = round(time.time() - start_time, 2)

                summary = _summarize_metrics(all_metrics, sport)

                st.success(f"Analysis complete in {elapsed}s.")
                st.write(f"Frames read: {frame_idx}")
                st.write(f"Frames analyzed: {analyzed_frames}")
                st.write(f"Useful metric frames: {len(all_metrics)}")

                st.subheader("Feedback Summary")
                st.write(summary["summary"])

                st.subheader("Coaching Tips")
                for tip in summary["tips"]:
                    st.write(f"- {tip}")

                st.subheader("Annotated Video")
                with open(output_temp_path, "rb") as f:
                    st.video(f.read())

                st.caption(
                    "This is a basic pose-based review. It is useful for movement screening, "
                    "but it is not yet a full sport-specific biomechanics engine."
                )

            except Exception as e:
                st.error(f"Video analysis failed: {e}")

            finally:
                if input_temp_path and os.path.exists(input_temp_path):
                    try:
                        os.remove(input_temp_path)
                    except Exception:
                        pass

                if output_temp_path and os.path.exists(output_temp_path):
                    # Keep file during session if Streamlit still needs it
                    pass
