# standard libs
import csv
import json
import re
import hmac
import hashlib
import os
import glob
import shutil
from datetime import datetime
# Import the brain we just built
from sentient_graph import sentient_ai

# --- CONFIGURATION & FRAMEWORK ALIGNMENT ---
LOG_FILE = "logs.txt"
CSV_REPORT = "threat_report_2026.csv"
JSON_ALERTS = "alerts_2026.json"
# Updated path for the nested structure
UI_PULSE = "frontend/frontend/public/pulse.json"
FAILED_THRESHOLD = 5  # NIST-aligned burst threshold

# SECURITY KEY: In a real app, move this to a .env file
SECRET_KEY = b"SentientSync_Daniel_2026_SecureKey"

def generate_integrity_hash(data_payload: str) -> str:
    """Generates a keyed-hash to ensure the log hasn't been tampered with."""
    return hmac.new(SECRET_KEY, data_payload.encode(), hashlib.sha256).hexdigest()

def parse_logs():
    """Week 1 & 2 Logic: Optimized for OWASP Top 10:2025 Detection."""
    threat_counts = {}
    try:
        with open(LOG_FILE, 'r') as f:
            for line in f:
                # Detection 1: Authentication Failures (A07:2025)
                if "FAILED" in line:
                    ip_match = re.search(r'\d+\.\d+\.\d+\.\d+', line)
                    if ip_match:
                        ip = ip_match.group()
                        threat_counts[ip] = threat_counts.get(ip, 0) + 1
                
                # Detection 2: Broken Access Control / IDOR (A01:2025)
                if "acct=" in line and "ALERT" in line:
                    ip_match = re.search(r'\d+\.\d+\.\d+\.\d+', line)
                    if ip_match:
                        ip = ip_match.group()
                        # Increment weight for targeted access violations
                        threat_counts[ip] = threat_counts.get(ip, 0) + 2

    except FileNotFoundError:
        print(f"[!] A10:2025 Error: {LOG_FILE} missing. Creating dummy log for demo...")
        with open(LOG_FILE, 'w') as f:
            f.write(f"{datetime.now()} - FAILED login attempt from 192.168.1.50\n")
            f.write(f"{datetime.now()} - ALERT: acct=admin access from 192.168.1.99\n")
        return parse_logs()
    except Exception as e:
        print(f"[!] Unexpected System Fault: {e}") 
    return threat_counts

def auditor_logic(failure_counts):
    """Week 2 Logic: Tiered threat classification with Cryptographic Integrity."""
    flagged_data = []
    for ip, count in failure_counts.items():
        if count >= FAILED_THRESHOLD:
            category = "A07:2025-Authentication Failure"
            severity = "CRITICAL"
            action = "IP_BLOCKLIST_REQUIRED"
        elif count >= 2:
            category = "A01:2025-Broken Access Control"
            severity = "MEDIUM"
            action = "MANUAL_LOG_REVIEW"
        else:
            category = "Low-Level Anomaly"
            severity = "LOW"
            action = "MONITORING"

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # --- NEW: INTEGRITY SIGNING ---
        # We create a unique signature based on the threat data
        payload = f"{ip}|{count}|{severity}|{timestamp}"
        integrity_sig = generate_integrity_hash(payload)

        flagged_data.append({
            "ip": ip, 
            "threat_score": count, 
            "category": category,
            "severity": severity,
            "recommended_action": action,
            "timestamp": timestamp,
            "integrity_signature": integrity_sig # This proves the data hasn't been modified
        })
    return flagged_data


def run_sentient_logic(logs, integrity_status):
    # Prepare the "State" for the AI
    initial_state = {
        "logs": [l.strip() for l in logs],
        "integrity_status": integrity_status,
        "threat_level": "UNKNOWN",
        "action_taken": "INITIALIZING"
    }
    # Run the graph (The thinking process)
    try:
        final_output = sentient_ai.invoke(initial_state)
    except Exception:
        final_output = {"threat_level": "UNKNOWN", "action_taken": "PASSIVE"}
    return final_output


def export_evidence_manifest():
    evidence_files = glob.glob("forensic_evidence/*.json")
    manifest = []
    # Get the 5 most recent evidence files
    latest_files = sorted(evidence_files, key=os.path.getmtime, reverse=True)[:5]
    for file_path in latest_files:
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
                manifest.append({
                    "id": data.get("case_id"),
                    "type": data.get("threat_classification"),
                    "time": data.get("captured_at", "").split(".")[0],
                    "file": f"/evidence_vault/{os.path.basename(file_path)}"
                })
        except Exception:
            continue
    try:
        UI_EVIDENCE_PATH = "frontend/frontend/public/evidence_vault"
        os.makedirs(UI_EVIDENCE_PATH, exist_ok=True)
        # Copy files into the public evidence vault
        for file_path in latest_files:
            try:
                shutil.copy(file_path, UI_EVIDENCE_PATH)
            except Exception:
                pass

        os.makedirs("frontend/frontend/public", exist_ok=True)
        with open("frontend/frontend/public/evidence_list.json", "w") as f:
            json.dump(manifest, f, indent=4)
    except Exception as e:
        print(f"[!] Evidence manifest export failed: {e}")

def export_forensics(threat_data):
    """Forensic Export: Creating an auditable trail for SOC review."""
    if not threat_data: 
        print("[!] No threats detected. Export skipped.")
        return
    
    export_package = {
        "metadata": {
            "system": "SENTIENT-SYNC ENGINE V1.1",
            "audit_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_threats_found": len(threat_data),
            "compliance_focus": ["NIST SP 800-228", "OWASP 2025"],
            "integrity_mode": "HMAC-SHA256"
        },
        "detailed_alerts": threat_data
    }

    try:
        # 1. Generate CSV for human analysts
        with open(CSV_REPORT, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=threat_data[0].keys())
            writer.writeheader()
            writer.writerows(threat_data)
        
        # 2. Generate JSON for Machine ingestion
        with open(JSON_ALERTS, 'w') as f:
            json.dump(export_package, f, indent=4)

        # 3. Read recent logs (used by both terminal feed and AI)
        try:
            with open(LOG_FILE, 'r') as lf:
                lines = lf.readlines()
        except Exception:
            lines = []

        # Determine a simple integrity status for the AI
        integrity_status = "COMPROMISED" if any(t['severity'] == "CRITICAL" for t in threat_data) else "OK"

        # Run the Sentient Graph to get AI thought/action
        try:
            ai_result = run_sentient_logic(lines, integrity_status)
            ai_action = ai_result.get("action_taken") if isinstance(ai_result, dict) else str(ai_result)
            # If the sentient graph provided a location, push it to the API for map visualization
            try:
                location_tag = None
                if isinstance(ai_result, dict):
                    location_tag = ai_result.get("location")
                if location_tag and location_tag != "UNKNOWN":
                    # Map simple location tags to city payloads
                    LOCATION_MAP = {
                        "BERLIN": {"name": "Berlin", "lat": "52.52", "lon": "13.40"},
                        "TOKYO": {"name": "Tokyo", "lat": "35.67", "lon": "139.65"},
                        "MIAMI": {"name": "Miami", "lat": "25.76", "lon": "-80.19"},
                        "LONDON": {"name": "London", "lat": "51.50", "lon": "-0.12"}
                    }
                    city = LOCATION_MAP.get(location_tag.upper()) or None
                    if city:
                        try:
                            import urllib.request as _ur
                            import json as _json
                            payload = _json.dumps(city).encode('utf-8')
                            req = _ur.Request('http://localhost:8000/system/override-origin', data=payload, headers={'Content-Type': 'application/json'})
                            _ur.urlopen(req, timeout=1)
                            # Also trigger the Neural Link visualization
                            link_payload = _json.dumps({"origin": city}).encode('utf-8')
                            link_req = _ur.Request('http://localhost:8000/system/trigger-link', data=link_payload, headers={'Content-Type': 'application/json'})
                            _ur.urlopen(link_req, timeout=1)
                        except Exception:
                            pass
            except Exception:
                pass
        except Exception:
            ai_action = "PASSIVE"

        # 4. Generate UI Pulse for React Bento Box (including AI thought)
        with open(UI_PULSE, 'w') as f:
            pulse = {
                "last_update": datetime.now().strftime("%H:%M:%S"),
                "status": "ALERT" if any(t['severity'] == "CRITICAL" for t in threat_data) else "SECURE",
                "active_threats": len(threat_data),
                "latest_hash": threat_data[0]['integrity_signature'][:10],
                "ai_thought": ai_action
            }
            json.dump(pulse, f, indent=4)

        # 5. Create a simple terminal feed for the React TerminalModule
        terminal_data = {
            "logs": [l.strip() for l in lines[-10:]]
        }
        try:
            with open("frontend/frontend/public/terminal_feed.json", 'w') as tf:
                json.dump(terminal_data, tf, indent=4)
        except IOError as e:
            print(f"[!] Terminal Feed Export Failed: {e}")

        # Export evidence manifest for UI
        try:
            export_evidence_manifest()
        except Exception:
            pass

        print(f"[+] Audit Complete. Artifacts: {JSON_ALERTS}, {CSV_REPORT}, and {UI_PULSE}")
    except IOError as e:
        print(f"[!] Forensic Export Failed: {e}")

if __name__ == "__main__":
    print("\n" + "="*50)
    print("SENTIENT SYNC: SECURITY AUTOMATION ENGINE - V1.1")
    print("Alignment: NIST SP 800-228 & OWASP Top 10:2025")
    print("Developer: Daniel Schillinger")
    print("="*50 + "\n")
    
    # 1. Data Acquisition
    raw_findings = parse_logs()
    
    # 2. Threat Classification & Cryptographic Signing
    processed_threats = auditor_logic(raw_findings)
    
    # 3. Forensic Record Keeping & UI Bridge
    export_forensics(processed_threats)
    
    # 4. Display Summary
    for threat in processed_threats:
        status = "FLAGGED FOR AGI REVIEW" if threat['severity'] == "CRITICAL" else "MONITORING"
        print(f"[{threat['severity']}] IP: {threat['ip']} | Category: {threat['category']}")
        print(f"    Integrity Hash: {threat['integrity_signature'][:16]}...")
        print(f"    Action: {status}\n")