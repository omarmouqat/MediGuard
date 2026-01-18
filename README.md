# 🏥 MediGuard: Intelligent Remote Health Monitoring System

![Python](https://img.shields.io/badge/Python-3.9-blue)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red)
![MQTT](https://img.shields.io/badge/Protocol-MQTT%20%2F%20CBOR-orange)
![AI](https://img.shields.io/badge/AI-Isolation%20Forest-green)

**MediGuard** is an advanced IoT solution designed to transition telemedicine from simple "Remote Monitoring" to **"Predictive Healthcare."** Unlike traditional loggers that just save numbers, MediGuard uses **Unsupervised Machine Learning (Isolation Forest)** at the edge to detect physiological anomalies in real-time. It features a bi-directional architecture where patients act as intelligent nodes and doctors use a centralized Command Center to monitor populations.

---

## 🚀 Key Features

* **🧠 AI-Powered Analysis:** Uses `scikit-learn`'s Isolation Forest to detect irregular vital signs patterns (e.g., valid HR but abnormal SpO2 correlation) without needing labeled training data.
* **📉 Bandwidth Optimization:** Implements **CBOR (Concise Binary Object Representation)** instead of JSON, reducing network payload size by ~40% for energy-efficient IoT communication.
* **👥 Multi-Tenancy:** Role-Based Access Control (RBAC) separates the "Patient View" (Simplified) from the "Doctor View" (Detailed Clinical Dashboard).
* **⚡ Real-Time Global Alerting:** A persistent "Sticky Alert" system ensures critical emergencies are visible to all medical staff immediately, regardless of which patient they are currently viewing.
* **🤖 Scalable Simulation:** Includes a multi-threaded `crowd_sim.py` tool to stress-test the system with 50+ concurrent virtual patients.

---

## 🏗️ Architecture

The system follows a microservices architecture:

1.  **Sensing Layer (Patient Portal):** * A Streamlit app acting as a "Software Defined Sensor."
    * Generates realistic physiological data (Heart Rate, Temp, SpO2) using Sine Wave algorithms (Circadian rhythms).
    * Allows manual injection of pathologies (Fever, Hypoxia) for testing.
2.  **Transport Layer:** * Uses **MQTT** (Mosquitto) for low-latency transmission.
    * Payloads are serialized in **CBOR** (Binary).
3.  **Processing Layer (Backend):** * Python script that ingests streams, runs AI models, and saves to **SQLite**.
4.  **Visualization Layer (Doctor Portal):** * A dynamic Streamlit dashboard for real-time tracking and historical analysis.

---

## 🛠️ Tech Stack

* **Language:** Python 3.9+
* **Communication:** Paho-MQTT, CBOR2
* **Frontend:** Streamlit
* **Backend/Database:** SQLite3
* **Machine Learning:** Scikit-learn (Isolation Forest)
* **Simulation:** Threading (for crowd generation)

---

## 📦 Installation

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/MediGuard.git](https://github.com/YOUR_USERNAME/MediGuard.git)
    cd MediGuard
    ```

2.  **Install Dependencies**
    ```bash
    pip install streamlit paho-mqtt cbor2 scikit-learn pandas numpy
    ```

3.  **Start the MQTT Broker**
    * *Windows:* `"C:\Program Files\mosquitto\mosquitto.exe" -v`
    * *Linux/Mac:* `mosquitto -v`
    * *(Or use a cloud broker like HiveMQ and update the `BROKER` variable in the scripts)*

---

## 🖥️ Usage Guide

To run the full system, you need to open **3 separate terminals**:

### Terminal 1: The Brain (Backend)
Starts the AI engine and database logger.
```bash
python backend.py
```

### Terminal 2: The Doctor Dashboard
Opens the Command Center for medical staff.

```Bash

streamlit run doctor_portal.py
```
### Terminal 3: The Patient Node
Opens the user app to simulate a patient.

```Bash

streamlit run patient_portal.py
```

### (Optional) Terminal 4: Stress Test
Simulate 50+ patients to test system load.

```Bash

python crowd_sim.py
```
