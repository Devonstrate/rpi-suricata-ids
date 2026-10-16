# Enterprise-Grade Perimeter Defense & Monitoring Pipeline
**Raspberry Pi IDS/IPS with GL.iNet Hardware Gateway Integration**

## 1. Executive Summary
This project implements an enterprise-aligned network detection and prevention architecture designed to monitor multi-VLAN residential/lab traffic under resource-constrained conditions. By combining hardware-level DNS threat sinkholing with host-based deep packet inspection (DPI), the pipeline eliminates unwanted noise and surfaces genuine indicators of compromise (IoCs).

---

## 2. Network Topology & Traffic Flow
```text
                       [ WAN / Internet ]
                               |
                   +-----------v-----------+
                   |  GL.iNet Flint 3      |
                   |  Gateway / Router     |
                   |  - AdGuard Home (DoH) |
                   |  - Network Segments   |
                   +-----+-----------+-----+
                         |           |
            [Main / PC VLAN]       [IoT VLAN (PS5, Vizio, Apple TV)]
            192.168.20.0/24         192.168.30.0/24
                         |
           +-------------v-------------+
           | Raspberry Pi Host         |
           | 192.168.50.115 (eth0)     |
           |                           |
           | +-----------------------+ |
           | | Suricata 8.0 Engine   | |
           | | (SYSTEM / AF-PACKET)  | |
           | +-----------+-----------+ |
           |             | eve.json    |
           | +-----------v-----------+ |
           | | EveBox SQLite Ingestion| |
           | +-----------+-----------+ |
           |             | port 5636   |
           | +-----------v-----------+ |
           | | Nginx Proxy Manager   | |
           | | ([http://evebox.lab](http://evebox.lab))   | |
           | +-----------------------+ |
           |                           |
           | Out-of-Band: WireGuard    |
           | (wg0: 10.44.5.1/24)       |
           +---------------------------+
---

## 5. Operations & Continuous Intelligence
* **Automated Threat Intelligence:** A daily cron job (`30 3 * * *`) executes `scripts/update-rules.sh`, pulling the latest Emerging Threats Open ruleset and sending a `SIGUSR2` hot-reload signal to the running engine without dropping active inspection flows.
* **Detailed Triage Record:** See [`architecture/DETECTION_EVAL.md`](architecture/DETECTION_EVAL.md) for the full synthetic test payload, raw `eve.json` event schema, and ingestion verification.



* **Real-Time Critical Alert Forwarding (`scripts/suricata_ntfy.py`):**
  * Monitors `eve.json` in real time via a dedicated systemd service (`suricata-ntfy.service`).
  * Implements strict Severity 1 gating to eliminate false positives and alert fatigue.
  * Incorporates a 10-minute signature/IP deduplication cache.
  * Dispatches urgent push notifications via `ntfy` with direct deep-links to the local EveBox triage console.
