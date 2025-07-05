# 🤖 LevelUp Fitness – AI Pose Estimation Module

This repository contains the AI Pose Estimation script used in the **LevelUp Fitness Web Application** – a capstone project aimed at bringing personalized, AI-powered fitness training to users through posture correction and exercise feedback.

> 🧠 Built using Python, MediaPipe, and OpenCV for real-time exercise form detection and rep counting.

---

## 📌 Project Context

This module is part of the larger **LevelUp Fitness** project, where team members worked on:
- **Frontend** – User interface for workout sessions and profile tracking.
- **Backend** – Authentication, workout data management, diet plans.
- **AI Module (this repo)** – Real-time posture analysis and form feedback using pose estimation.

---

## 📽️ Features of This Module

✅ Real-time pose estimation using webcam or uploaded videos  
✅ Supports **Push-ups** and **Squats**  
✅ Auto-detects which exercise is being performed  
✅ Gives feedback on correct or incorrect posture  
✅ Reference model comparison (based on average Indian body pose structure)  
✅ Rep counter integrated for performance tracking  

---

## 🛠️ Tech Stack

| Component | Tools/Libs Used |
|----------|------------------|
| Language | Python |
| Pose Estimation | MediaPipe |
| Video Processing | OpenCV |
| Math & Logic | NumPy, math module |
| Reference Comparison | Custom Joint Angles & Positioning |
| UI Integration | Flask API (if connected with web app) |

