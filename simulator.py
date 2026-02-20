import time
import random
from datetime import datetime

LOG_FILE = "logs.txt"

def generate_log_entry(ip, status="FAILED", account="admin"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if status == "ALERT":
        return f"{timestamp} - ALERT: acct={account} access attempt from {ip}\n"
    return f"{timestamp} - {status} login attempt from {ip}\n"

def run_simulation():
    print("[!] Starting Attack Simulation...")
    
    with open(LOG_FILE, "w") as f:
        # 1. Simulate a 'CRITICAL' Brute Force Burst (10 hits in 5 seconds)
        print("[-] Simulating Brute Force from 192.168.1.50...")
        for _ in range(10):
            f.write(generate_log_entry("192.168.1.50"))
            # No sleep = high velocity
        
        # 2. Simulate a 'HIGH' Broken Access Control (Slow and deliberate)
        print("[-] Simulating IDOR attack from 10.0.0.5...")
        f.write(generate_log_entry("10.0.0.5", status="ALERT", account="billing_root"))
        
        # 3. Simulate a 'LOW' Anomaly (Just 1 failure)
        print("[-] Simulating random failure from 172.16.0.20...")
        f.write(generate_log_entry("172.16.0.20"))

    print("[+] Simulation complete. Run main.py to audit these logs.")

if __name__ == "__main__":
    run_simulation()