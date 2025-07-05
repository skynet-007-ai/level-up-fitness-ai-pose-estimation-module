import cv2
import mediapipe as mp
import numpy as np
import json


def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(np.degrees(radians))

    if angle > 180.0:
        angle = 360 - angle
    return angle


# Setup
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
cap = cv2.VideoCapture("11.mp4")  # 👈 Put your video path

rep_count = 0
rep_summaries = []
current_angles = []
rep_in_progress = False

ANGLE_DOWN = 70  # bottom position
ANGLE_UP = 160  # top position

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            # Left shoulder, elbow, wrist
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

            angle = calculate_angle(shoulder, elbow, wrist)
            current_angles.append(angle)

            # Rep detection logic
            if not rep_in_progress and angle < ANGLE_DOWN:
                rep_in_progress = True
            elif rep_in_progress and angle > ANGLE_UP:
                rep_in_progress = False
                rep_count += 1

                # Rep summary
                min_angle = round(min(current_angles), 2)
                max_angle = round(max(current_angles), 2)
                avg_angle = round(sum(current_angles) / len(current_angles), 2)
                summary = {
                    "rep": rep_count,
                    "min_angle": min_angle,
                    "max_angle": max_angle,
                    "avg_angle": avg_angle,
                    "samples": len(current_angles)
                }
                rep_summaries.append(summary)
                print(f"--- Rep {rep_count} Summary ---")
                print(summary)
                current_angles = []

# Save JSON
with open("reference_pushup_data.json", "w") as f:
    json.dump(rep_summaries, f, indent=4)

cap.release()
print("✅ Reference push-up data saved to 'reference_pushup_data.json'")
