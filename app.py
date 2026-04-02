import streamlit as st
import time
import pandas as pd
import random
from datetime import datetime

st.set_page_config(page_title="IoT SOC Dashboard", layout="wide")

# 🎨 DARK UI
st.markdown("""
<style>
body { background-color: #0e1117; color: white; }
.stMetric { background-color: #1c1f26; padding: 10px; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# Detect Windows
try:
    import win32evtlog
    WINDOWS = True
except:
    WINDOWS = False


# 🔹 IoT Device Simulation
devices = ["Camera-01", "Sensor-02", "Thermostat-03", "DoorLock-04"]

def simulate_iot_attack():
    device = random.choice(devices)
    threat = random.choice([
        "Unauthorized Access Attempt",
        "Malware Injection",
        "Suspicious Data Spike",
        "Remote Command Execution"
    ])
    severity = random.choice(["High", "Medium", "Low"])
    
    return {
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Device": device,
        "Threat": threat,
        "Severity": severity
    }


# 🔹 AI Explanation
def ai_explain(threat, severity):
    if severity == "High":
        return "Critical threat detected. Immediate action required to prevent system compromise."
    elif severity == "Medium":
        return "Potential threat observed. Monitor system behavior closely."
    else:
        return "Low-risk activity. No immediate action required."


# 🔹 Defender Logs (local)
def get_real_logs():
    logs = []
    try:
        server = 'localhost'
        logtype = 'Microsoft-Windows-Windows Defender/Operational'
        import win32evtlog
        hand = win32evtlog.OpenEventLog(server, logtype)

        flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
        events = win32evtlog.ReadEventLog(hand, flags, 0)

        for event in events[:5]:
            logs.append({
                "Time": str(event.TimeGenerated),
                "Device": "Host System",
                "Threat": str(event.StringInserts),
                "Severity": "High" if event.EventID == 1116 else "Medium"
            })
    except:
        pass

    return logs


# 🔥 HEADER
st.title("🛡️ IoT Cybersecurity SOC Dashboard")
st.markdown("Real-Time Threat Monitoring + AI Analysis")

refresh = st.sidebar.slider("Refresh Rate (sec)", 5, 60, 10)

# Mode
if WINDOWS:
    st.sidebar.success("LOCAL MODE (Real Defender + IoT)")
    logs = get_real_logs()
else:
    st.sidebar.warning("CLOUD MODE (Simulated IoT)")
    logs = []

# Add IoT simulation
for _ in range(3):
    logs.append(simulate_iot_attack())

df = pd.DataFrame(logs)

# 📊 METRICS
col1, col2, col3 = st.columns(3)
col1.metric("Total Events", len(df))
col2.metric("High Threats", len(df[df["Severity"] == "High"]))
col3.metric("Devices Active", len(set(df["Device"])))

# 📈 GRAPH
st.subheader("📊 Threat Activity")
df["Count"] = 1
timeline = df.groupby("Time").count()["Count"]
st.line_chart(timeline)

# 📋 TABLE
st.subheader("📋 Threat Logs")
st.dataframe(df, use_container_width=True)

# 🚨 ALERTS + AI
st.subheader("🚨 Live Alerts with AI Insight")

for _, row in df.iterrows():
    explanation = ai_explain(row["Threat"], row["Severity"])

    if row["Severity"] == "High":
        st.error(f"[{row['Device']}] {row['Threat']} → {explanation}")
    elif row["Severity"] == "Medium":
        st.warning(f"[{row['Device']}] {row['Threat']} → {explanation}")
    else:
        st.info(f"[{row['Device']}] {row['Threat']} → {explanation}")

# 📁 DOWNLOAD
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("Download Logs", csv, "iot_security_logs.csv", "text/csv")

# 🔄 REFRESH
time.sleep(refresh)
st.rerun()