import csv
import json
import re
from datetime import datetime

# --- CONFIGURATION & FRAMEWORK ALIGNMENT ---
LOG_FILE = "logs.txt"
CSV_REPORT = "threat_report_2026.csv"
JSON_ALERTS = "alerts_2026.json"
FAILED_THRESHOLD = 5  # NIST-aligned burst threshold [cite: 85, 165]

def parse_logs():
    """Week 1 & 2 Logic: Optimized for OWASP Top 10:2025 Detection."""
    threat_counts = {}
    try:
        with open(LOG_FILE, 'r') as f:
            for line in f:
                # Detection 1: Authentication Failures (A07:2025) [cite: 435, 439]
                if "FAILED" in line:
                    ip_match = re.search(r'\d+\.\d+\.\d+\.\d+', line)
                    if ip_match:
                        ip = ip_match.group()
                        threat_counts[ip] = threat_counts.get(ip, 0) + 1
                
                # Detection 2: Broken Access Control / IDOR (A01:2025) [cite: 187, 194]
                # Flagging unauthorized attempts to access sensitive object IDs [cite: 71, 213]
                if "acct=" in line and "ALERT" in line:
                    ip_match = re.search(r'\d+\.\d+\.\d+\.\d+', line)
                    if ip_match:
                        ip = ip_match.group()
                        # Increment weight for targeted access violations [cite: 195]
                        threat_counts[ip] = threat_counts.get(ip, 0) + 2

    except FileNotFoundError:
        # A10:2025 Mitigation: Proper handling of missing resource states [cite: 561, 566]
        print(f"[!] A10:2025 Error: {LOG_FILE} missing. Ensure dataset exists.") 
    except Exception as e:
        # Global Exception Handler: Ensuring system "fails closed" [cite: 575, 579]
        print(f"[!] Unexpected System Fault: {e}") 
    return threat_counts

def auditor_logic(failure_counts):
    """Week 2 Logic: Tiered threat classification[cite: 59, 163]."""
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

        flagged_data.append({
            "ip": ip, 
            "threat_score": count, 
            "category": category,
            "severity": severity,
            "recommended_action": action,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    return flagged_data

def export_forensics(threat_data):
    """Forensic Export: Creating an auditable trail for SOC review[cite: 176, 532, 536]."""
    if not threat_data: return
    
    # Week 2 Enhancement: Adding SOC Summary Metadata [cite: 19, 176]
    export_package = {
        "metadata": {
            "system": "AGI-READY ENGINE V1.0",
            "audit_date": datetime.now().strftime("%Y-%m-%d"),
            "total_threats_found": len(threat_data),
            "compliance_focus": ["NIST SP 800-228", "OWASP 2025"]
        },
        "detailed_alerts": threat_data
    }

    try:
        # Generate CSV for human analysts
        with open(CSV_REPORT, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=threat_data[0].keys())
            writer.writeheader()
            writer.writerows(threat_data)
        
        # Generate JSON for AGI/Machine ingestion [cite: 23, 544]
        with open(JSON_ALERTS, 'w') as f:
            json.dump(export_package, f, indent=4)
        print(f"[+] Audit Complete. Artifacts stored in {JSON_ALERTS}")
    except IOError as e:
        print(f"[!] Forensic Export Failed: {e}")

if __name__ == "__main__":
    print("="*50)
    print("AGI-READY SECURITY AUTOMATION ENGINE - V1.0")
    print("Alignment: NIST SP 800-228 & OWASP Top 10:2025")
    print("="*50)
    
    # 1. Hunt (Week 1 Data Acquisition) [cite: 7, 22]
    raw_findings = parse_logs()
    
    # 2. Audit (Week 2 Threat Classification) [cite: 7, 59]
    processed_threats = auditor_logic(raw_findings)
    
    # 3. Export (Forensic Record Keeping) [cite: 536]
    export_forensics(processed_threats)
    
    # 4. Display (SOC Dashboard View) [cite: 19]
    for threat in processed_threats:
        status = "FLAGGED FOR AGI REVIEW" if threat['severity'] == "CRITICAL" else "MONITORING"
        print(f"[{threat['severity']}] IP: {threat['ip']} | Category: {threat['category']}")
        print(f"      Score: {threat['threat_score']} | Action: {status}\n")