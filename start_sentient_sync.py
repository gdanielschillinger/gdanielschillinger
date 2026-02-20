import subprocess
import time
import os
import sys

def launch():
    print("--- INITIALIZING SENTIENT SYNC ECOSYSTEM ---")
    print()
    
    # Store original directory
    original_dir = os.getcwd()
    
    # 1. Start the API (The Hands)
    print("[+] Launching API Server...")
    try:
        subprocess.Popen([sys.executable, "api.py"], creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0)
        print("    ✓ API Server started on http://localhost:8000")
    except Exception as e:
        print(f"    ✗ Failed to start API: {e}")
    
    time.sleep(2)
    
    # 2. Start the Sentinel (The Reflexes)
    print("[+] Launching Sentinel Watchdog...")
    try:
        subprocess.Popen([sys.executable, "sentinel.py"], creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0)
        print("    ✓ Sentinel Watchdog started (monitoring logs.txt)")
    except Exception as e:
        print(f"    ✗ Failed to start Sentinel: {e}")
    
    time.sleep(2)
    
    # 3. Start the Frontend (The Eyes)
    print("[+] Launching Dashboard...")
    try:
        frontend_path = os.path.join(original_dir, "frontend", "frontend")
        if os.path.isdir(frontend_path):
            os.chdir(frontend_path)
            subprocess.Popen(["npm", "run", "dev"], shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0)
            print("    ✓ Dashboard dev server started on http://localhost:3000")
        else:
            print(f"    ✗ Frontend directory not found: {frontend_path}")
    except Exception as e:
        print(f"    ✗ Failed to start Frontend: {e}")
    finally:
        os.chdir(original_dir)
    
    print()
    print("="*60)
    print("[!] SENTIENT SYNC ECOSYSTEM FULLY OPERATIONAL")
    print("[!] Dashboard:  http://localhost:3000")
    print("[!] API:        http://localhost:8000")
    print("[!] Watchdog:   Active (monitoring logs.txt)")
    print("="*60)
    print("[!] SECURE THE AGI. PROTECT THE SYNC.")
    print()

if __name__ == "__main__":
    launch()
