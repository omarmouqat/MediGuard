import streamlit as st
import time
#import json
import cbor2
import random
import math
import paho.mqtt.client as mqtt

st.set_page_config(page_title="My Health Portal", page_icon="💓")

st.title("Patient Vitals Monitor")

if 'monitoring' not in st.session_state:
    st.session_state.monitoring = False

name = st.text_input("Enter your Name to start monitoring:", placeholder="e.g. Omar")

st.sidebar.header("Simulation Controls")
sim_mode = st.sidebar.radio("Current Condition", ["Healthy", "Fever", "Critical SpO2"])

if name:
    col1, col2 = st.columns(2)
    if col1.button("Start Sending Data"):
        st.session_state.monitoring = True
    if col2.button("Stop"):
        st.session_state.monitoring = False

    if st.session_state.monitoring:
        st.success(f"Monitoring Active for: **{name}**")
        placeholder = st.empty()

        client = mqtt.Client()
        try:
            client.connect("localhost", 1883, 60)
        except:
            st.error("Could not connect to MQTT Broker!")
            st.stop()

        tick = 0
        while st.session_state.monitoring:
            base_hr = 75
            base_temp = 36.6
            base_spo2 = 98

            if sim_mode == "Fever":
                base_temp = 39.5 + random.uniform(-0.2, 0.2)
                base_hr += 20
            elif sim_mode == "Critical SpO2":
                base_spo2 = 85 + random.uniform(-2, 2)
                base_hr += 40
            else:
                base_hr += 5 * math.sin(tick * 0.2)

            data = {
                "timestamp": time.time(),
                "heart_rate": round(base_hr, 1),
                "temperature": round(base_temp, 1),
                "spo2": round(base_spo2, 1)
            }

            topic = f"health/{name}/vitals"
            client.publish(topic, cbor2.dumps(data))

            with placeholder.container():
                m1, m2, m3 = st.columns(3)
                m1.metric("Heart Rate", f"{data['heart_rate']} bpm")
                m2.metric("Temp", f"{data['temperature']} °C")
                m3.metric("SpO2", f"{data['spo2']} %")
                st.caption("Sending data to hospital server...")

            time.sleep(1)
            tick += 1