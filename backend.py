
import cbor2
import sqlite3
import paho.mqtt.client as mqtt
from sklearn.ensemble import IsolationForest


conn = sqlite3.connect('vitals.db', check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS measurements 
             (timestamp REAL, patient_id TEXT, hr REAL, temp REAL, spo2 REAL, anomaly_score REAL, alert_msg TEXT)''')
conn.commit()

patient_buffers = {}


def analyze_data(patient_id, data):
    alert = "None"
    is_anomaly = 0


    if patient_id not in patient_buffers:
        patient_buffers[patient_id] = []


    current_vector = [data['heart_rate'], data['spo2']]
    patient_buffers[patient_id].append(current_vector)


    if len(patient_buffers[patient_id]) > 50:
        patient_buffers[patient_id].pop(0)


    if len(patient_buffers[patient_id]) > 10:
        clf = IsolationForest(contamination=0.2, random_state=42)
        clf.fit(patient_buffers[patient_id])
        pred = clf.predict([current_vector])
        if pred[0] == -1:
            is_anomaly = 1
            if alert == "None": alert = "AI: Irregular Pattern"


    if data['temperature'] > 39.0:
        alert = "CRITICAL: High Fever"
    elif data['spo2'] < 90:
        alert = "CRITICAL: Low Oxygen"

    return is_anomaly, alert


def on_message(client, userdata, msg):
    try:

        topic_parts = msg.topic.split("/")
        patient_id = topic_parts[1]

        payload = cbor2.loads(msg.payload)


        anomaly, alert_msg = analyze_data(patient_id, payload)


        c.execute("INSERT INTO measurements VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (payload['timestamp'], patient_id, payload['heart_rate'], payload['temperature'],
                   payload['spo2'], anomaly, alert_msg))
        conn.commit()

        print(f"[{patient_id}] HR: {payload['heart_rate']} | Alert: {alert_msg}")

    except Exception as e:
        print(f"Error: {e}")


client = mqtt.Client()
client.connect("localhost", 1883, 60)

client.subscribe("health/+/vitals")
print("Backend Listening for ALL patients...")
client.on_message = on_message
client.loop_forever()