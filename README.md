# 🏛️ CivicProof: AI-Driven Micro-Accountability Engine

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.103.0-009688.svg?logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-1.27.0-FF4B4B.svg?logo=streamlit)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8.0-5C3EE8.svg?logo=opencv)
![YOLOv8](https://img.shields.io/badge/YOLO-v8-yellow.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

> **Bridging the Trust Deficit between Government Promises and Ground Reality.**

CivicProof is an AI-powered governance platform designed to automate the verification of hyper-local civic works (such as streetlight repairs and pothole filling). It forces transparency by requiring field workers to upload visual proof, which is then audited by a Computer Vision AI before marking a task as "Complete" and notifying local citizens.

---

## 🛑 The Problem: "Ghost Work"
Local municipalities spend millions on last-mile infrastructure, but face a massive "Trust Deficit." 
* **Lack of Verification:** Authorities cannot physically inspect thousands of daily micro-tasks.
* **Fake Reporting:** Contractors often mark jobs as "Complete" without actually doing the work.
* **Citizen Disconnect:** Residents see broken infrastructure, report it, but never receive transparent updates.

## 💡 The Solution: Visual Proof Protocol
CivicProof replaces manual checks with an **Automated Trust Loop**:
1. **Assign:** A task (e.g., "Fix Streetlight") is assigned to a local booth.
2. **Execute & Upload:** The worker finishes the job and uploads a photo to the portal.
3. **AI Audit:** The YOLOv8 + OpenCV engine analyzes the image for context (is it a street?) and execution (is the light actually glowing?).
4. **Notify:** Once verified, the system automatically sends an SMS notification to the specific voters registered in that booth area.

---

## ✨ Key Features
* **Smart Glare Detection (Computer Vision):** Custom blob-detection algorithms distinguish between a working lightbulb and a bright daytime sky, preventing "false positive" verifications.
* **Geospatial War Room:** A real-time Streamlit dashboard providing authorities with a heat map of pending vs. verified complaints.
* **Automated Citizen Loop:** Closes the feedback loop by linking verified tasks directly to the voter registry database for localized SMS updates.
* **Fraud Prevention:** Automatically rejects dark, blurry, or context-inaccurate photos.

---

## 📸 System Previews

### 1. The Command Center Dashboard
*Real-time metrics, geospatial booth mapping, and task tracking.*
![CivicProof Dashboard](Screenshot%202026-02-16%20134807.png)

### 2. Live Activity Map & Status Updates
*Monitoring task statuses (Pending, Verified, Rejected) across different city zones.*
![Activity Map](Screenshot%202026-02-16%20134822.png)

### 3. AI Verification Override 
*Testing the AI engine directly from the portal.*
![Verification Override](Screenshot%202026-02-15%20211826.png)

---

## 🛠️ Technology Stack
* **Backend:** Python, FastAPI, Uvicorn
* **AI/Machine Learning:** Ultralytics YOLOv8 (Object Detection), OpenCV (Luminosity/Blob Analysis), NumPy
* **Database:** SQLite & SQLAlchemy (Knowledge Graph modeling of Voters ↔ Booths ↔ Tasks)
* **Frontend:** Streamlit, Pandas

---

## 🚀 Quick Start Guide (Local Deployment)

### Prerequisites
* Python 3.9+
* Git

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/CivicProof.git](https://github.com/yourusername/CivicProof.git)
   cd CivicProof
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize and Seed the Database:**
   *This creates a local SQLite database and populates it with dummy booths, voters, and tasks.*
   ```bash
   python seed.py
   ```

4. **Start the FastAPI Backend:**
   ```bash
   uvicorn main:app --reload
   ```
   *The API will be live at `http://127.0.0.1:8000` (Access the Swagger UI at `/docs`).*

5. **Launch the Streamlit Dashboard:**
   *Open a new terminal window and run:*
   ```bash
   streamlit run dashboard.py
   ```
   *The dashboard will automatically open in your browser.*

---

## 🤝 Open for Collaboration
This project is open-source and looking for contributors! Areas where we need help:
* **Frontend Polish:** Enhancing the Streamlit UI with custom CSS and better Map integrations (Folium).
* **AI Expansion:** Training custom YOLO models to detect specific civic issues like garbage dumps, potholes, and waterlogging.
* **Security:** Implementing EXIF GPS data extraction to ensure uploaded photos match the task coordinates.

If you are interested, please fork the repository and submit a Pull Request!

---
*Developed for robust, transparent, and hyper-local governance.*
