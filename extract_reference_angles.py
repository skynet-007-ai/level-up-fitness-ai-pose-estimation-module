import os
import cv2
import numpy as np
import mediapipe as mp
from collections import defaultdict

# Set your dataset folder name
VIDEO_FOLDER = "Gym Video Dataset"  # <-- your dataset folder name

# Initialize MediaPipe pose detection
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
angle_data = defaultdict(list)  # Dictionary to store all angle data

# Helper: Calculate angle between three points
def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    return 360 - angle if angle > 180.0 else angle

# Loop through each video in the folder
for file in os.listdir(VIDEO_FOLDER):
    if not file.endswith('.mp4'):
        continue

    filepath = os.path.join(VIDEO_FOLDER, file)
    cap = cv2.VideoCapture(filepath)

    print(f"Processing: {file}")
    exercise_type = "pushups" if "pushups" in file.lower() else "squats"

    elbow_angles, shoulder_angles, knee_angles, hip_angles = [], [], [], []

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        # Convert frame to RGB and process with MediaPipe
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = pose.process(frame_rgb)

        if result.pose_landmarks:
            lm = result.pose_landmarks.landmark
            h, w, _ = frame.shape

            # Get key landmarks (RIGHT side only)
            shoulder = [lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x * w,
                        lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y * h]
            elbow = [lm[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x * w,
                     lm[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y * h]
            wrist = [lm[mp_pose.PoseLandmark.RIGHT_WRIST.value].x * w,
                     lm[mp_pose.PoseLandmark.RIGHT_WRIST.value].y * h]
            hip = [lm[mp_pose.PoseLandmark.RIGHT_HIP.value].x * w,
                   lm[mp_pose.PoseLandmark.RIGHT_HIP.value].y * h]
            knee = [lm[mp_pose.PoseLandmark.RIGHT_KNEE.value].x * w,
                    lm[mp_pose.PoseLandmark.RIGHT_KNEE.value].y * h]
            ankle = [lm[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x * w,
                     lm[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y * h]

            # Store angles for pushups or squats
            if exercise_type == "pushups":
                elbow_angles.append(calculate_angle(shoulder, elbow, wrist))
                shoulder_angles.append(calculate_angle(hip, shoulder, elbow))
            else:  # squats
                knee_angles.append(calculate_angle(hip, knee, ankle))
                hip_angles.append(calculate_angle(shoulder, hip, knee))

    cap.release()

    # Store average angles per video
    if exercise_type == "pushups":
        if elbow_angles:
            angle_data["pushup_elbow"].append(np.mean(elbow_angles))
        if shoulder_angles:
            angle_data["pushup_shoulder"].append(np.mean(shoulder_angles))
    else:
        if knee_angles:
            angle_data["squat_knee"].append(np.mean(knee_angles))
        if hip_angles:
            angle_data["squat_hip"].append(np.mean(hip_angles))

# Print final reference angles for each exercise
print("\n✅ Final Reference Angles for Real-Time Pose Correction:")
for key, values in angle_data.items():
    print(f"{key}: {np.mean(values):.2f}°")
