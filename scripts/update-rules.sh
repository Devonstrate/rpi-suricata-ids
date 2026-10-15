#!/usr/bin/env bash
set -euo pipefail

echo "[*] Updating Suricata Emerging Threats ruleset..."
docker exec suricata suricata-update --no-test

echo "[*] Reloading Suricata detection engine..."
docker kill --signal=USR2 suricata

echo "[+] Rules updated and live engine reloaded without packet drop."
