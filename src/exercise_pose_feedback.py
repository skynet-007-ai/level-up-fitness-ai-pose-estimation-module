import cv2
import mediapipe as mp
import time
import math

# Initialize MediaPipe pose and drawing utils
mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

# Open video file or webcam (change path or use 0 for webcam)
cam = cv2.VideoCapture("D:\My Projects\Level-Up Fitness- AI Powered Fitness Tracking Assistant\AI_Module (AI Based Posture Correction and Tracking)\demo\squats_demo.mp4")

prevTime = 0

# Angle calculation function
def calculate_angle(a, b, c):
    ang = math.degrees(
        math.atan2(c[1] - b[1], c[0] - b[0]) -
        math.atan2(a[1] - b[1], a[0] - b[0])
    )
    ang = abs(ang)
    if ang > 180:
        ang = 360 - ang
    return ang

# Get angle from landmark indices for upper body (elbow)
def get_angle_from_ids(lm_list, ids, w, h):
    shoulder = (int(lm_list[ids[0]].x * w), int(lm_list[ids[0]].y * h))
    elbow = (int(lm_list[ids[1]].x * w), int(lm_list[ids[1]].y * h))
    wrist = (int(lm_list[ids[2]].x * w), int(lm_list[ids[2]].y * h))
    return calculate_angle(shoulder, elbow, wrist)

# Get angle from landmark indices for lower body (knee)
def get_knee_angle(lm_list, ids, w, h):
    hip = (int(lm_list[ids[0]].x * w), int(lm_list[ids[0]].y * h))
    knee = (int(lm_list[ids[1]].x * w), int(lm_list[ids[1]].y * h))
    ankle = (int(lm_list[ids[2]].x * w), int(lm_list[ids[2]].y * h))
    return calculate_angle(hip, knee, ankle)

# Landmark IDs for push-up elbows
RIGHT_ELBOW_IDS = (12, 14, 16)
LEFT_ELBOW_IDS = (11, 13, 15)

# Landmark IDs for squat knees
RIGHT_KNEE_IDS = (24, 26, 28)
LEFT_KNEE_IDS = (23, 25, 27)

# Thresholds for push-up reps
PUSHUP_DOWN_THRESHOLD = 70
PUSHUP_UP_THRESHOLD = 160

# Thresholds for squat reps
SQUAT_DOWN_THRESHOLD = 90
SQUAT_UP_THRESHOLD = 170

# Example reference average angles for Indian population (simulated)
reference_angles = {
    'pushup': {
        'down_min': 60,   # typical min elbow angle at bottom
        'up_max': 170,    # typical max elbow angle at top
    },
    'squat': {
        'down_min': 80,   # typical min knee angle at squat bottom
        'up_max': 175,    # typical max knee angle standing
    }
}

# Rep detection variables
rep_active = False
rep_angles = []
feedback = ""
rep_count = 0

# For exercise detection
angle_history_length = 30  # number of frames to analyze before deciding exercise
elbow_angles_hist = []
knee_angles_hist = []
exercise = None  # Will be 'pushup' or 'squat'

print("Analyzing exercise type... Please wait.")

while True:
    success, img = cam.read()
    if not success:
        print("End of video or cannot read frame")
        break

    img = cv2.resize(img, (640, 480))
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)

    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        lm = results.pose_landmarks.landmark
        h, w, _ = img.shape

        # Calculate right and left elbow angles
        right_elbow_angle = get_angle_from_ids(lm, RIGHT_ELBOW_IDS, w, h)
        left_elbow_angle = get_angle_from_ids(lm, LEFT_ELBOW_IDS, w, h)
        elbow_angle = min(right_elbow_angle, left_elbow_angle)

        # Calculate right and left knee angles
        right_knee_angle = get_knee_angle(lm, RIGHT_KNEE_IDS, w, h)
        left_knee_angle = get_knee_angle(lm, LEFT_KNEE_IDS, w, h)
        knee_angle = min(right_knee_angle, left_knee_angle)

        # During first few frames, record angles for exercise detection
        if exercise is None:
            elbow_angles_hist.append(elbow_angle)
            knee_angles_hist.append(knee_angle)
            if len(elbow_angles_hist) >= angle_history_length:
                elbow_range = max(elbow_angles_hist) - min(elbow_angles_hist)
                knee_range = max(knee_angles_hist) - min(knee_angles_hist)

                if elbow_range > knee_range and elbow_range > 15:
                    exercise = 'pushup'
                elif knee_range > elbow_range and knee_range > 15:
                    exercise = 'squat'
                else:
                    exercise = 'unknown'
                print(f"Detected exercise: {exercise}")

        if exercise == 'pushup' or exercise == 'squat':
            # Select active angle based on exercise
            active_angle = elbow_angle if exercise == 'pushup' else knee_angle
            label = "Elbow Angle" if exercise == 'pushup' else "Knee Angle"

            cv2.putText(img, f'{label}: {active_angle:.1f}', (30, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

            # Rep detection logic
            if not rep_active:
                if exercise == 'pushup' and active_angle < PUSHUP_DOWN_THRESHOLD:
                    rep_active = True
                    rep_angles = [active_angle]
                    print("Rep started")
                elif exercise == 'squat' and active_angle < SQUAT_DOWN_THRESHOLD:
                    rep_active = True
                    rep_angles = [active_angle]
                    print("Rep started")
            else:
                rep_angles.append(active_angle)
                if exercise == 'pushup' and active_angle > PUSHUP_UP_THRESHOLD:
                    rep_active = False
                    rep_count += 1
                    min_angle = min(rep_angles)
                    max_angle = max(rep_angles)
                    avg_angle = sum(rep_angles) / len(rep_angles)

                    # Feedback based on reference angles for push-up
                    ref_min = reference_angles['pushup']['down_min']
                    ref_max = reference_angles['pushup']['up_max']
                    if min_angle > ref_min + 15:
                        feedback = f"Rep {rep_count}: ❌ Too shallow. Lower more (min: {min_angle:.1f}°, ref: {ref_min}°)"
                    elif max_angle < ref_max - 15:
                        feedback = f"Rep {rep_count}: ❌ Didn't push up fully (max: {max_angle:.1f}°, ref: {ref_max}°)"
                    elif avg_angle < ref_min - 10 or avg_angle > ref_max + 10:
                        feedback = f"Rep {rep_count}: ⚠️ Inconsistent form (avg: {avg_angle:.1f}°)"
                    else:
                        feedback = f"Rep {rep_count}: ✅ Good push-up!"
                    print(feedback)
                    rep_angles = []

                elif exercise == 'squat' and active_angle > SQUAT_UP_THRESHOLD:
                    rep_active = False
                    rep_count += 1
                    min_angle = min(rep_angles)
                    max_angle = max(rep_angles)
                    avg_angle = sum(rep_angles) / len(rep_angles)

                    # Feedback based on reference angles for squat
                    ref_min = reference_angles['squat']['down_min']
                    ref_max = reference_angles['squat']['up_max']
                    if min_angle > ref_min + 15:
                        feedback = f"Rep {rep_count}: ❌ Not deep enough squat (min: {min_angle:.1f}°, ref: {ref_min}°)"
                    elif max_angle < ref_max - 15:
                        feedback = f"Rep {rep_count}: ❌ Didn't stand fully up (max: {max_angle:.1f}°, ref: {ref_max}°)"
                    elif avg_angle < ref_min - 10 or avg_angle > ref_max + 10:
                        feedback = f"Rep {rep_count}: ⚠️ Inconsistent form (avg: {avg_angle:.1f}°)"
                    else:
                        feedback = f"Rep {rep_count}: ✅ Good squat!"
                    print(feedback)
                    rep_angles = []

            # Draw info on frame
            cv2.putText(img, f'Exercise: {exercise.capitalize()}', (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(img, f'Reps: {rep_count}', (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(img, feedback, (30, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        else:
            cv2.putText(img, 'Analyzing exercise type...', (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        # Draw landmarks for reference
        for lm_id, landmark in enumerate(lm):
            cx, cy = int(landmark.x * w), int(landmark.y * h)
            cv2.circle(img, (cx, cy), 4, (255, 0, 0), cv2.FILLED)

    else:
        # No landmarks detected
        cv2.putText(img, 'No pose detected', (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Show FPS
    currTime = time.time()
    fps = 1 / (currTime - prevTime) if prevTime != 0 else 0
    prevTime = currTime
    cv2.putText(img, f'FPS: {int(fps)}', (500, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

    # Display frame
    cv2.imshow("Exercise Pose Feedback", img)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
