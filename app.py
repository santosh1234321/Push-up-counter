import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import tempfile
import time

st.set_page_config(page_title="Push-Up Counter", layout="centered")
st.title("Push-Up Counter from Video")

def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = abs(radians * 180 / np.pi)
    return 360 - angle if angle > 180 else angle

uploaded_file = st.file_uploader("Upload your push-up video", type=["mp4", "mov", "avi"])
if uploaded_file:
    temp_input = tempfile.NamedTemporaryFile(delete=False)
    temp_input.write(uploaded_file.read())
    input_path = temp_input.name

    output_path = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False).name

    cap = cv2.VideoCapture(input_path)
    width, height = int(cap.get(3)), int(cap.get(4))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    pushup_count = 0
    direction = 0

    progress_bar = st.progress(0)
    progress_text = st.empty()
    st.info("Processing your video...")

    start_time = time.time()
    frame_counter = 0

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            try:
                landmarks = results.pose_landmarks.landmark
                shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                angle = calculate_angle(shoulder, elbow, wrist)

                if angle > 160 and direction == 1:
                    pushup_count += 1
                    direction = 0
                elif angle < 90 and direction == 0:
                    direction = 1

                # Draw angle text with background rectangle in bright red text and black bg
                angle_text = f'Angle: {int(angle)}'
                font = cv2.FONT_HERSHEY_SIMPLEX
                text_size = cv2.getTextSize(angle_text, font, 1, 3)[0]
                text_x, text_y = width - 320, 80
                cv2.rectangle(image,
                              (text_x - 10, text_y - text_size[1] - 10),
                              (text_x + text_size[0] + 10, text_y + 10),
                              (0, 0, 0),  # black background
                              cv2.FILLED)
                cv2.putText(image, angle_text, (text_x, text_y),
                            font, 1, (0, 0, 255), 3)  # bright red text
            except:
                pass

            # Draw pose landmarks with customized style (blue points, yellow connections)
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=3),  # Blue points
                    mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=2, circle_radius=2)  # Yellow connections
                )

            # Draw push-up count text with blue bg and white text
            pushup_text = f'Push-Ups: {pushup_count}'
            font = cv2.FONT_HERSHEY_SIMPLEX
            text_size = cv2.getTextSize(pushup_text, font, 1, 4)[0]
            text_x, text_y = width - 320, 50
            cv2.rectangle(image,
                          (text_x - 10, text_y - text_size[1] - 10),
                          (text_x + text_size[0] + 10, text_y + 10),
                          (255, 0, 0),  # blue background
                          cv2.FILLED)
            cv2.putText(image, pushup_text, (text_x, text_y),
                        font, 1, (255, 255, 255), 4)  # white text

            writer.write(image)
            frame_counter += 1

            progress = frame_counter / total_frames
            progress_bar.progress(min(progress, 1.0))
            elapsed = time.time() - start_time
            avg_time_per_frame = elapsed / frame_counter if frame_counter else 0
            eta = (total_frames - frame_counter) * avg_time_per_frame
            progress_text.markdown(
                f"Processed {frame_counter}/{total_frames} frames "
                f"Elapsed: {elapsed:.1f}s | ETA: {eta:.1f}s"
            )

    cap.release()
    writer.release()

    st.success(f"Done! Total push-ups detected: {pushup_count}")

    with open(output_path, 'rb') as video_file:
        video_bytes = video_file.read()
        st.video(video_bytes)
        st.download_button("Download H.264 Video (.mp4)", video_bytes,
                           file_name="pushups_h264.mp4", mime="video/mp4")
