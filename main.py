import sys
import os
import re
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# --- Security Initialization ---
# Safely pulls secrets for future AGI integration [cite: 31, 50]
load_dotenv()
AI_API_KEY = os.getenv("AI_API_KEY")

# --- Configuration ---
LOG_PATH_DEFAULT = Path(__file__).parent / "logs.txt"

# Week 2: Threat Intelligence Watchlist [cite: 7, 43, 45]
# Flagging IPs that match known malicious ranges or high-risk actors
WATCHLIST_IPS = ["10.0.0.50", "172.16.0.5"] 

# Enhanced Regex: Captures timestamps, status, user, IP, and optional Path telemetry [cite: 14, 16, 17]
LINE_RE = re.compile(
    r"^(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+"
    r"(?P<status>\w+)\s+-\s+User:\s*(?P<user>[^ ]+)\s+-\s+IP:\s*"
    r"(?P<ip>\d+\.\d+\.\d+\.\d+)"
    r"(?:\s+-\s+Path:\s*(?P<path>.*))?$"
)

def generate_ai_summary(alert_data):
    """Prepares structured data for AGI-based natural language summarization[cite: 7, 31, 46]."""
    if not alert_data:
        return "No threats detected."
    
    status_msg = "[+] SECURE MODE: AI API Key loaded successfully." if AI_API_KEY else "[!] SECURE MODE: API Key hidden (local only)."

    prompt = f"""
    SYSTEM: You are a Lead Cybersecurity Analyst.
    DATA: {json.dumps(alert_data, indent=2)}
    TASK: Generate an executive-level summary of the threat.
    """
    
    print("\n" + "-"*50)
    print(f"{status_msg}")
    print("[!] AGI INTEGRATION: THREAT BRIEFING PREPARED")
    print("-" * 50)
    print(prompt)
    return prompt

def export_threats(failures_by_ip, targeted_paths, output_path="alerts.json"):
    """Automates threat data export for audit compliance and SIEM ingestion[cite: 7, 176]."""
    threats = []
    
    # Week 2 Logic: Risk-based scoring and Watchlist cross-referencing [cite: 7, 41]
    for ip, count in failures_by_ip.items():
        is_on_watchlist = ip in WATCHLIST_IPS
        
        # Threshold: Flag if failures >= 3 OR if the IP is on the watchlist [cite: 11, 39, 165]
        if count >= 3 or is_on_watchlist:
            threats.append({
                "ip": ip, 
                "failures": count, 
                "status": "FLAGGED",
                "risk_level": "CRITICAL" if is_on_watchlist else "HIGH", # Scoring based on intel
                "targeted_endpoints": list(targeted_paths[ip])
            })
    
    if threats:
        alert_data = {
            "alert_type": "Brute Force Detection",
            "severity": "CRITICAL" if any(t["risk_level"] == "CRITICAL" for t in threats) else "HIGH",
            "generated_at": datetime.now().isoformat(),
            "detected_threats": threats
        }
        with open(output_path, "w") as f:
            json.dump(alert_data, f, indent=4)
        return alert_data
    return None

def print_soc_dashboard(total, failed, alert_data):
    """Displays a clean, professional SOC summary to the terminal[cite: 18, 19]."""
    print("\n" + "="*55)
    print(" [!] INTERNAL SECURITY ANALYST THREAT REPORT")
    print("="*55)
    print(f"[*] LOG ENTRIES PROCESSED: {total}")
    print(f"[-] FAILED LOGIN ATTEMPTS: {failed}")
    print("-" * 55)
    
    if alert_data:
        print(f"{'IP ADDRESS':<15} | {'FAILURES':<10} | {'RISK':<10}")
        print("-" * 55)
        for threat in alert_data["detected_threats"]:
            print(f"{threat['ip']:<15} | {threat['failures']:<10} | {threat['risk_level']:<10}")
        print(f"\n[!] Audit Alert Generated: alerts.json")
    else:
        print("[+] SYSTEM STATUS: NO HIGH-RISK THREATS DETECTED")
    print("="*55 + "\n")

def parse_log(path):
    """Core engine to ingest and parse local log files for indicators of compromise[cite: 7, 14, 15]."""
    total, success, failed = 0, 0, 0
    failures_by_ip = Counter()
    targeted_paths = defaultdict(set) 

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
            
            ip = m.group("ip")
            status = m.group("status").upper()
            path_hit = m.group("path") if m.group("path") else "unknown"

            if status == "FAILED":
                failed += 1
                failures_by_ip[ip] += 1
                targeted_paths[ip].add(path_hit)
            else:
                success += 1

    # Execute Export Logic [cite: 7, 176]
    alert_data = export_threats(failures_by_ip, targeted_paths)
    
    # Display Dashboard [cite: 19]
    print_soc_dashboard(total, failed, alert_data)
    
    # Trigger AGI Briefing Prep [cite: 7, 31]
    if alert_data:
        generate_ai_summary(alert_data)

def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else LOG_PATH_DEFAULT
    parse_log(path)

if __name__ == "__main__":
    main()