# 🤖 AI Integration Module – LevelUp Fitness

This folder contains the integration setup between the AI-based pose estimation model and the frontend web interface.

It includes:
- A **Flask backend (`ai_service.py`)** that accepts video files (recorded or uploaded) and analyzes push-up posture using MediaPipe.
- An **HTML frontend (`ai-fitness.html`)** that allows users to:
  - Record or upload workout videos
  - Send the video to the backend for analysis
  - View rep count, posture feedback, and angle metrics
  - Download a CSV report

---

## 📂 File Breakdown

### `ai_service.py` (⚙️ Flask API)
- Runs a server on `localhost:5001`
- Accepts POST requests with a video file
- Processes the video frame-by-frame using MediaPipe
- Detects reps and provides real-time feedback (✅ Good form, ❌ Incorrect form)
- Returns:
  - Total reps
  - Feedback for each rep
  - Min/Max/Avg elbow angles per rep

### `ai-fitness.html` (🧑‍💻 Frontend Interface)
- Has two options:
  - Record video using webcam
  - Upload a pre-recorded workout video
- Sends video to `/analyze` endpoint of `ai_service.py`
- Displays:
  - Detected exercise
  - Total reps performed
  - Feedback list
  - Angle breakdown
- CSV download of the report is supported

---

## 🔧 How to Run This

1. Open terminal in this folder.
2. Start the Flask backend:
   ```bash
   python ai_service.py
