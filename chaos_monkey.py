import time
import random

LOG_FILE = "logs.txt"

THREATS = [
    "CRITICAL: NIST-BURST_DETECTED // IP: 192.168.1.99 // Brute Force Attack",
    "WARNING: OWASP-A07 // Broken Authentication // Access Control Failure",
    "INFO: Unauthorized API Access // NIST-A01 // Credential Stuffing",
    "CRITICAL: SQL Injection Attempt // OWASP-A03 // Reflected Payload",
    "WARNING: Forensic Drift Detected // HMAC Signature Mismatch"
]

def unleash_chaos():
    print("[!] UNLEASHING CHAOS MONKEY...")
    for _ in range(5):
        threat = random.choice(THREATS)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        entry = f"{timestamp} - {threat}\n"
        with open(LOG_FILE, "a") as f:
            f.write(entry)
        print(f"[+] Injected: {threat}")
        time.sleep(1)

if __name__ == "__main__":
    unleash_chaos()
