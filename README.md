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

---

## Team Members and Their Roles

### 1. Harsh Kumar (ME, 24A12RES271) – AI/ML Lead & Project Coordinator  
**Responsibilities:**  
- Led overall planning, architecture, and team coordination  
- Developed AI-based posture correction using MediaPipe and OpenCV  
- Designed logic for personalized workout recommendations  
- Integrated AI modules with frontend/backend flow  

**Skills Applied/Learned:**  
- Machine Learning, Computer Vision  
- YOLOv8n (Ultralytics), OpenCV, MediaPipe  
- Object Detection Model Training and Custom Dataset Handling  
- AI Workflow Planning and Real-time Integration  

---

### 2. Hanshraj Kumar (24A12RES260) – Frontend Developer & UI Designer  
**Responsibilities:**  
- Developed frontend using HTML, CSS, and JavaScript  
- Built secure login interface for user authentication  
- Designed UI sections: Yoga, Meditation, Bodyweight Training, Diet  
- Created responsive navbar and “To-Do List” feature  
- Developed a static “Contact Us” section with developer info  

**Skills Applied/Learned:**  
- UI design, responsive layout (HTML/CSS)  
- Modular component structuring  
- Web navigation and content flow  

---

### 3. Harsh Kumar (24A12RES268) – Backend Developer & UX Designer  
**Responsibilities:**  
- Built backend using Node.js and Express.js  
- Implemented JWT-based login and registration  
- Managed MongoDB Atlas for storing user and profile data  
- Developed logic for diet plan generation and PDF download  
- Enabled secure logout, YouTube video embedding, and API routing  

**Skills Applied/Learned:**  
- Node.js, Express.js, MongoDB  
- JWT authentication and REST API  
- Secure backend logic and database handling  
