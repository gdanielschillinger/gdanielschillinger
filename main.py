import sys
import re
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path

# --- Configuration ---
# This ensures the script knows exactly where the "prey" is located [cite: 10, 11]
LOG_PATH_DEFAULT = Path(r"C:\Users\Daniel\Documents\security-log-analyzer\logs.txt")

# This Regex pattern must perfectly match your logs.txt format 
LINE_RE = re.compile(r"^(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+(?P<status>\w+)\s+-\s+User:\s*(?P<user>[^ ]+)\s+-\s+IP:\s*(?P<ip>\d+\.\d+\.\d+\.\d+)$")

def parse_log(path):
    total = 0
    success = 0
    failed = 0
    failures_by_ip = Counter()
    failures_by_user = Counter()
    fail_times_by_ip = defaultdict(list)

    if not path.exists():
        print(f"[!] Error: Target file not found at {path}")
        return None

    # Step 2 & 3: Read file and apply Threat Logic [cite: 14, 15]
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            m = LINE_RE.match(line)
            total += 1
            if not m:
                continue
            
            ts = datetime.strptime(m.group("ts"), "%Y-%m-%d %H:%M:%S")
            status = m.group("status").upper()
            user = m.group("user")
            ip = m.group("ip")

            if status == "SUCCESS":
                success += 1
            elif status == "FAILED":
                failed += 1
                failures_by_ip[ip] += 1
                failures_by_user[user] += 1
                fail_times_by_ip[ip].append(ts)

    # Step 4: The Security Dashboard Output [cite: 18, 19]
    print("\n" + "="*45)
    print(" [!] INTERNAL SECURITY ANALYST THREAT REPORT")
    print("="*45)
    print(f"[*] SOURCE DATA: {path.name}")
    print(f"[*] LOG ENTRIES PROCESSED: {total}")
    print(f"[+] SUCCESSFUL AUTHENTICATIONS: {success}")
    print(f"[-] FAILED LOGIN ATTEMPTS: {failed}")
    
    if failures_by_ip:
        print("\n[!] SUSPICIOUS ACTIVITY DETECTED:")
        for ip, count in failures_by_ip.most_common():
            risk = "HIGH RISK" if count >= 3 else "LOW RISK"
            print(f"    -> {ip}: {count} failures ({risk})")
    print("="*45 + "\n")
    
    return True

def main():
    # Use provided path or default [cite: 13, 14]
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else LOG_PATH_DEFAULT
    parse_log(path)

if __name__ == "__main__":
    main()