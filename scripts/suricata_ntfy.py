#!/usr/bin/env python3
import json
import time
import os
import requests

# CONFIGURATION
EVE_LOG = "/home/subzero121/services/suricata/logs/eve.json"
NTFY_URL = "https://ntfy.sh/<YOUR_PRIVATE_TOPIC>
ALERT_SEVERITIES = [1]  # Only Severity 1 (Critical / High) alerts
COOLDOWN_SECONDS = 600  # 10-minute deduplication window per (signature, src_ip)

seen_alerts = {}

def send_notification(alert_data):
    alert = alert_data.get("alert", {})
    sig = alert.get("signature", "Unknown Signature")
    cat = alert.get("category", "General Intrusion")
    src = f"{alert_data.get('src_ip', 'unknown')}:{alert_data.get('src_port', '')}"
    dest = f"{alert_data.get('dest_ip', 'unknown')}:{alert_data.get('dest_port', '')}"
    severity = alert.get("severity", 3)

    cache_key = f"{alert.get('signature_id')}_{alert_data.get('src_ip')}"
    current_time = time.time()

    if cache_key in seen_alerts and (current_time - seen_alerts[cache_key]) < COOLDOWN_SECONDS:
        return

    seen_alerts[cache_key] = current_time

    headers = {
        "Title": f"IDS ALERT [Sev {severity}]: {sig[:40]}",
        "Priority": "urgent" if severity == 1 else "default",
        "Tags": "warning,shield,skull",
        "Click": "http://evebox.lab"
    }

    body = f"Category: {cat}\nSource: {src}\nTarget: {dest}\nAction: {alert.get('action', 'allowed')}"

    try:
        requests.post(NTFY_URL, data=body.encode("utf-8"), headers=headers, timeout=5)
    except Exception:
        pass

def follow_log(filepath):
    while not os.path.exists(filepath):
        time.sleep(1)

    with open(filepath, "r") as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                if os.path.exists(filepath) and os.stat(filepath).st_size < f.tell():
                    f.close()
                    f = open(filepath, "r")
                continue

            try:
                data = json.loads(line.strip())
                if data.get("event_type") == "alert":
                    sev = data.get("alert", {}).get("severity", 3)
                    if sev in ALERT_SEVERITIES:
                        send_notification(data)
            except Exception:
                continue

if __name__ == "__main__":
    follow_log(EVE_LOG)
