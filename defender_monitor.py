import win32evtlog

def get_defender_logs():
    server = 'localhost'
    logtype = 'Microsoft-Windows-Windows Defender/Operational'

    hand = win32evtlog.OpenEventLog(server, logtype)

    events = []
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

    total = 0

    while True:
        records = win32evtlog.ReadEventLog(hand, flags, 0)
        if not records:
            break

        for event in records:
            if total >= 20:  # limit output
                break

            try:
                event_data = {
                    "Event ID": event.EventID,
                    "Time": str(event.TimeGenerated),
                    "Source": event.SourceName,
                    "Message": str(event.StringInserts)
                }
                events.append(event_data)
                total += 1
            except:
                continue

        if total >= 20:
            break

    return events


if __name__ == "__main__":
    logs = get_defender_logs()
    for log in logs:
        print(log)