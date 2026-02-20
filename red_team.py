import os

# Path to your logs
LOG_FILE = "logs.txt"

def tamper_logs():
    if not os.path.exists(LOG_FILE):
        print("[-] Error: logs.txt not found. Run main.py first to generate logs.")
        return

    with open(LOG_FILE, "r") as f:
        lines = f.readlines()

    if len(lines) < 2:
        print("[-] Not enough log data to tamper with.")
        return

    print("[!] Initiating Red Team Tamper...")
    
    # Let's modify the last log entry to hide a threat or change a timestamp
    # We are changing the content but NOT the signature.
    original_line = lines[-1]
    tampered_line = original_line.replace("CRITICAL", "INFO").replace("Brute Force", "Authorized Login")
    
    lines[-1] = tampered_line

    with open(LOG_FILE, "w") as f:
        f.writelines(lines)

    print(f"[+] Tamper Complete: Changed 'CRITICAL' to 'INFO' in the last entry.")
    print("[!] The HMAC signature is now invalid. Run main.py to see if the Auditor catches it.")

if __name__ == "__main__":
    tamper_logs()
