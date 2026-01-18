import streamlit as st
import pandas as pd
import sqlite3
import time

st.set_page_config(page_title="Doctor Dashboard", layout="wide", page_icon="👨‍⚕️")


def get_all_data():
    try:
        conn = sqlite3.connect('vitals.db')
        query = "SELECT * FROM measurements ORDER BY timestamp DESC LIMIT 100"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except:
        return pd.DataFrame()

df = get_all_data()

st.sidebar.title("👨‍⚕️ Dr. Console")
st.sidebar.write("Active Patients")

if df.empty:
    st.sidebar.info("No active patients.")
    st.info("Waiting for patient data stream...")
else:
    alert_patients = df[df['alert_msg'].str.contains("CRITICAL|AI|Irregular", regex=True, na=False)][
        'patient_id'].unique()

    if len(alert_patients) > 0:
        for p in alert_patients:
            p_alerts = df[
                (df['patient_id'] == p) & (df['alert_msg'].str.contains("CRITICAL|AI|Irregular", regex=True, na=False))]

            if not p_alerts.empty:
                last_msg = p_alerts.iloc[0]['alert_msg']

                if "CRITICAL" in last_msg:
                    st.error(f"🚨 URGENT: Patient **{p}** - {last_msg}")


    active_patients = sorted(df['patient_id'].unique())

    index = 0
    if 'selected_patient_id' in st.session_state:
        if st.session_state.selected_patient_id in active_patients:
            index = active_patients.index(st.session_state.selected_patient_id)

    selected_patient = st.sidebar.radio(
        "Select Patient to Monitor",
        active_patients,
        index=index,
        key="patient_radio"
    )

    st.session_state.selected_patient_id = selected_patient

    if selected_patient:
        st.header(f"Patient File: {selected_patient}")

        pat_df = df[df['patient_id'] == selected_patient].sort_values(by="timestamp")

        if not pat_df.empty:
            latest = pat_df.iloc[-1]

            msg = latest['alert_msg']

            if "CRITICAL" in msg:
                st.error(f"🚨 DANGER: {msg}")  # Red Box
            elif "AI" in msg or "Irregular" in msg:
                st.warning(f"⚠️ AI WARNING: {msg}")  # Yellow Box
            else:
                st.success("✅ Status: Stable")  # Green Box

            c1, c2, c3 = st.columns(3)
            c1.metric("Heart Rate", f"{latest['hr']} BPM")
            c2.metric("Temperature", f"{latest['temp']} °C")
            c3.metric("SpO2", f"{latest['spo2']} %")

            col_chart1, col_chart2 = st.columns(2)
            with col_chart1:
                st.caption("Heart Rate History")
                st.line_chart(pat_df.set_index("timestamp")['hr'])
            with col_chart2:
                st.caption("Temperature History")
                st.line_chart(pat_df.set_index("timestamp")['temp'])

time.sleep(1)
st.rerun()