import sys
import os
import re
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

# --- Configuration ---
LOG_PATH_DEFAULT = Path(r"C:\Users\Daniel\Documents\security-log-analyzer\logs.txt")
# High-precision Regex for telemetry extraction
LINE_RE = re.compile(r"^(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+(?P<status>\w+)\s+-\s+User:\s*(?P<user>[^ ]+)\s+-\s+IP:\s*(?P<ip>\d+\.\d+\.\d+\.\d+)$")

def generate_ai_summary(alert_data):
    """Prepares the structured data for AGI-based natural language summarization."""
    if not alert_data:
        return "No threats detected for summarization."
    
    # This structured prompt will serve as the input for our LLM integration
    prompt = f"""
    SYSTEM: You are a Lead Cybersecurity Analyst.
    DATA: {json.dumps(alert_data, indent=2)}
    TASK: Generate an executive-level summary of the threat. 
    Focus on the attacking IP, failure volume, and required remediation steps.
    """
    
    print("\n" + "-"*45)
    print("[!] AGI INTEGRATION: THREAT BRIEFING PREPARED")
    print("-"*45)
    print(prompt)
    return prompt

def export_threats(failures_by_ip, output_path="alerts.json"):
    """Automates threat data export for audit compliance and SIEM ingestion."""
    threats = [{"ip": ip, "failures": count, "status": "FLAGGED"} 
               for ip, count in failures_by_ip.items() if count >= 3]
    
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
        return alert_data
    return None

def parse_log(path):
    total, success, failed = 0, 0, 0
    failures_by_ip = Counter()

    if not path.exists():
        print(f"[!] Error: Target file not found at {path}")
        return

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line: continue
            m = LINE_RE.match(line)
            total += 1
            if not m: continue
            
            if m.group("status").upper() == "FAILED":
                failed += 1
                failures_by_ip[m.group("ip")] += 1
            else:
                success += 1

    # Terminal Dashboard Output
    print("\n" + "="*45)
    print(" [!] INTERNAL SECURITY ANALYST THREAT REPORT")
    print("="*45)
    print(f"[*] LOG ENTRIES PROCESSED: {total}")
    print(f"[-] FAILED LOGIN ATTEMPTS: {failed}")
    
    # Automated Auditor Logic
    alert_data = export_threats(failures_by_ip)
    
    # AGI Framework Trigger [New for Week 3!]
    if alert_data:
        generate_ai_summary(alert_data)

def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else LOG_PATH_DEFAULT
    parse_log(path)

if __name__ == "__main__":
    main()