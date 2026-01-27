import sys
import re
import json
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path

# --- Configuration ---
# This ensures the script knows exactly where the "prey" is located
LOG_PATH_DEFAULT = Path(r"C:\Users\Daniel\Documents\security-log-analyzer\logs.txt")

# This Regex pattern must perfectly match your logs.txt format 
LINE_RE = re.compile(r"^(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+(?P<status>\w+)\s+-\s+User:\s*(?P<user>[^ ]+)\s+-\s+IP:\s*(?P<ip>\d+\.\d+\.\d+\.\d+)$")

def export_threats(failures_by_ip, output_path="alerts.json"):
    """Automates the export of detected threats for audit compliance."""
    # Structure the data for SIEM ingestion
    threats = [
        {"ip": ip, "failures": count, "status": "FLAGGED"}
        for ip, count in failures_by_ip.items() if count >= 3
    ]
    
    if threats:
        alert_data = {
            "alert_type": "Brute Force Detection",
            "severity": "HIGH",
            "generated_at": datetime.now().isoformat(),
            "detected_threats": threats
        }
        with open(output_path, "w") as f:
            json.dump(alert_data, f, indent=4)
        print(f"[!] Audit Alert Generated: {output_path}")

def parse_log(path):
    total, success, failed = 0, 0, 0
    failures_by_ip = Counter()
    failures_by_user = Counter()
    fail_times_by_ip = defaultdict(list)

    if not path.exists():
        print(f"[!] Error: Target file not found at {path}")
        return

    # Step 2 & 3: Read file and apply Threat Logic
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line: continue
            m = LINE_RE.match(line)
            total += 1
            if not m: continue
            
            status = m.group("status").upper()
            ip = m.group("ip")
            user = m.group("user")

            if status == "SUCCESS":
                success += 1
            elif status == "FAILED":
                failed += 1
                failures_by_ip[ip] += 1
                failures_by_user[user] += 1

    # Step 4: The Security Dashboard Output
    print("\n" + "="*45)
    print(" [!] INTERNAL SECURITY ANALYST THREAT REPORT")
    print("="*45)
    print(f"[*] LOG ENTRIES PROCESSED: {total}")
    print(f"[+] SUCCESSFUL AUTHENTICATIONS: {success}")
    print(f"[-] FAILED LOGIN ATTEMPTS: {failed}")
    
    if failures_by_ip:
        print("\n[!] SUSPICIOUS ACTIVITY DETECTED:")
        for ip, count in failures_by_ip.most_common():
            risk = "HIGH RISK" if count >= 3 else "LOW RISK"
            print(f"    -> {ip}: {count} failures ({risk})")
    print("="*45 + "\n")

    # Call the new Export function
    export_threats(failures_by_ip)

def main():
    # Use provided path or default
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else LOG_PATH_DEFAULT
    parse_log(path)

if __name__ == "__main__":
    main()