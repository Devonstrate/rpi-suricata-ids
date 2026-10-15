# Threat Emulation & Alert Validation Record

## Test Signature Execution
* **Source Host:** Main Workstation (`192.168.20.x`)
* **Target:** External Internet HTTP Ingress
* **Vector:** Malicious User-Agent string simulation (`BlackSun`)
* **Command:** `curl -s -A "BlackSun" [http://testmyids.com](http://testmyids.com) > /dev/null`

## Alert Telemetry (`eve.json` Record)
```json
{
  "timestamp": "2026-10-15T18:38:12.194821+0000",
  "flow_id": 1493028472918471,
  "in_iface": "eth0",
  "event_type": "alert",
  "src_ip": "192.168.20.45",
  "src_port": 54210,
  "dest_ip": "104.21.5.192",
  "dest_port": 80,
  "proto": "TCP",
  "alert": {
    "action": "allowed",
    "gid": 1,
    "signature_id": 2008983,
    "rev": 13,
    "signature": "ET USER_AGENTS Suspicious User-Agent (BlackSun)",
    "category": "A Network Trojan was detected",
    "severity": 1
  }
}
