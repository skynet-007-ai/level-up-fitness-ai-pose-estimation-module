# 🤖 LevelUp Fitness – AI Pose Estimation Module

This repository contains the **AI module** for the *LevelUp Fitness* capstone project.  
The system uses **computer vision and pose estimation** to analyze exercise posture, detect repetitions, and provide feedback on exercise form.

The module currently supports **push-up and squat detection** using joint angle analysis.

---

## 🧠 Overview

The system uses **MediaPipe Pose Estimation** to track human body landmarks and calculate joint angles.  
These angles are used to:

- Detect the type of exercise being performed
- Count repetitions
- Provide posture feedback based on reference joint angle data

---

## 📽️ Demo

The screenshots below show the system detecting exercise posture,
counting repetitions, and displaying feedback in real time.

### Push-up Detection

Example output showing push-up detection and rep counting.

![Push-up Detection](demo/output_example_pushups.png)

### Squat Detection

Example output showing squat detection and posture analysis.

![Squat Detection](demo/output_example_squats.png)

---

## ✨ Features

- Real-time pose estimation using MediaPipe
- Automatic exercise detection (Push-ups / Squats)
- Rep counting using joint angle thresholds
- Posture feedback based on reference joint angles
- Supports both webcam input and pre-recorded video

---

## 📂 Project Structure

```
AI_Module
│
├── src
│   ├── exercise_pose_feedback.py
│   ├── pose_estimation_demo.py
│   ├── pose_landmark_extractor.py
│   └── generate_reference_dataset.py
│
├── demo
│   ├── pushup_demo.mp4
│   ├── squats_demo.mp4
│   ├── output_example_pushups.png
│   └── output_example_squats.png
│
├── reference_data
│   └── reference_pushup_data.json
│
├── dataset_sample
│
├── requirements.txt
├── README.md
└── LICENSE
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/skynet-007-ai/Level-Up-Fitness-Webapp-AI-Based-Fitness-Coaching-Assistant.git
cd Level-Up-Fitness-Webapp-AI-Based-Fitness-Coaching-Assistant

```

Install dependencies:

```bash
pip install -r requirements.txt

```
---

## ▶️ Running the Project


Run the main pose detection and feedback script:

```bash
python src/exercise_pose_feedback.py

```
Press **q** to exit the program.

---

## 🛠️ Tech Stack

| Component            | Technology |
| -------------------- | ---------- |
| Language             | Python     |
| Pose Estimation      | MediaPipe  |
| Video Processing     | OpenCV     |
| Numerical Processing | NumPy      |

---

## 🚀 Future Improvements

Possible improvements to the system:

1. Support more exercises (lunges, planks, pull-ups)

2. Improve posture classification accuracy

3. Add real-time voice feedback

4. Deploy as a web or mobile fitness assistant

---

## 👨‍💻 Author

**Harsh Kumar**
AI/ML Lead - Level-Up Fitness Capstone Project
Indian Institute of Technology Patna


This repository contains the AI module contribution to the LevelUp Fitness project. The full system includes additional frontend and backend modules developed by the team.