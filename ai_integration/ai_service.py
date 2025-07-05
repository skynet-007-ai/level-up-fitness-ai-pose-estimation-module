from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import cv2
import mediapipe as mp
import math
import tempfile

app = Flask(__name__)
CORS(app)

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils

# Helper functions
def calculate_angle(a, b, c):
    ang = math.degrees(
        math.atan2(c[1] - b[1], c[0] - b[0]) -
        math.atan2(a[1] - b[1], a[0] - b[0])
    )
    ang = abs(ang)
    if ang > 180:
        ang = 360 - ang
    return ang

def get_angle_from_ids(lm_list, ids, w, h):
    shoulder = (int(lm_list[ids[0]].x * w), int(lm_list[ids[0]].y * h))
    elbow = (int(lm_list[ids[1]].x * w), int(lm_list[ids[1]].y * h))
    wrist = (int(lm_list[ids[2]].x * w), int(lm_list[ids[2]].y * h))
    return calculate_angle(shoulder, elbow, wrist)

@app.route('/analyze', methods=['POST'])
def analyze_video():
    if 'video' not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    video_file = request.files['video']
    temp_path = os.path.join(tempfile.gettempdir(), "session.mp4")
    video_file.save(temp_path)

    cap = cv2.VideoCapture(temp_path)

    rep_active = False
    rep_angles = []
    feedback = []
    rep_count = 0
    all_angle_data = []

    RIGHT_IDS = (12, 14, 16)
    LEFT_IDS = (11, 13, 15)
    DOWN_ANGLE = 70
    UP_ANGLE = 160

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.resize(frame, (640, 480))
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)

        if results.pose_landmarks:
            lm = results.pose_landmarks.landmark
            h, w, _ = frame.shape
            right_angle = get_angle_from_ids(lm, RIGHT_IDS, w, h)
            left_angle = get_angle_from_ids(lm, LEFT_IDS, w, h)
            elbow_angle = min(right_angle, left_angle)

            if not rep_active:
                if elbow_angle < DOWN_ANGLE:
                    rep_active = True
                    rep_angles = [elbow_angle]
            else:
                rep_angles.append(elbow_angle)
                if elbow_angle > UP_ANGLE:
                    rep_active = False
                    rep_count += 1

                    min_angle = min(rep_angles)
                    max_angle = max(rep_angles)
                    avg_angle = sum(rep_angles) / len(rep_angles)
                    all_angle_data.append({
                        "rep": rep_count,
                        "min": round(min_angle, 2),
                        "max": round(max_angle, 2),
                        "avg": round(avg_angle, 2)
                    })

                    if min_angle > 80:
                        feedback.append(f"Rep {rep_count}: ❌ Too shallow. Lower more")
                    elif max_angle < 140:
                        feedback.append(f"Rep {rep_count}: ❌ Didn't push up fully")
                    elif avg_angle < 75 or avg_angle > 135:
                        feedback.append(f"Rep {rep_count}: ⚠️ Inconsistent form")
                    else:
                        feedback.append(f"Rep {rep_count}: ✅ Good push-up")

                    rep_angles = []

    cap.release()
    return jsonify({
        "exercise": "Push-ups",
        "reps": rep_count,
        "angles": all_angle_data,
        "feedback": feedback
    })

if __name__ == "__main__":
    app.run(port=5001)
