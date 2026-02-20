import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class LogHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith("logs.txt") or event.src_path.endswith("\\logs.txt"):
            print(f"\n[!] LOG_MODIFIED: Triggering Sentient_Sync_Logic...")
            # Automatically runs the auditor, graph, and UI update
            subprocess.run(["python", "main.py"])

if __name__ == "__main__":
    print("--- SENTINEL WATCHDOG: ACTIVE ---")
    print("[+] Monitoring logs.txt for real-time forensic drift...")
    
    event_handler = LogHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
