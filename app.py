import streamlit as st

st.title("🛡️ Microsoft Defender Monitoring Dashboard")

st.write("Cybersecurity Threat Monitoring System")

# Try importing Windows-specific module
try:
    import win32evtlog
    WINDOWS = True
except:
    WINDOWS = False


def get_fake_logs():
    return [
        {
            "Event ID": 1116,
            "Time": "2026-04-01 08:30",
            "Source": "Windows Defender",
            "Message": "Malware detected: EICAR Test File"
        },
        {
            "Event ID": 1117,
            "Time": "2026-04-01 08:32",
            "Source": "Windows Defender",
            "Message": "Threat quarantined successfully"
        }
    ]


def get_real_logs():
    import win32evtlog

    server = 'localhost'
    logtype = 'Microsoft-Windows-Windows Defender/Operational'
    hand = win32evtlog.OpenEventLog(server, logtype)

    logs = []
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

    events = win32evtlog.ReadEventLog(hand, flags, 0)

    for event in events[:10]:
        logs.append({
            "Event ID": event.EventID,
            "Time": str(event.TimeGenerated),
            "Source": event.SourceName,
            "Message": str(event.StringInserts)
        })

    return logs


if st.button("Fetch Logs"):

    if WINDOWS:
        st.success("Running in LOCAL mode (Real Defender Logs)")
        logs = get_real_logs()
    else:
        st.warning("Running in CLOUD mode (Simulated Logs)")
        logs = get_fake_logs()

    for log in logs:
        st.subheader("Threat Event")
        st.write(f"**Event ID:** {log['Event ID']}")
        st.write(f"**Time:** {log['Time']}")
        st.write(f"**Source:** {log['Source']}")
        st.write(f"**Details:** {log['Message']}")
        st.write("---")