from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import psutil
import platform
import random
import sqlite3
import time
import hashlib
import requests

CITIES = [
    {"name": "Berlin", "lat": "52.52", "lon": "13.40"},
    {"name": "Miami", "lat": "25.76", "lon": "-80.19"},
    {"name": "Tokyo", "lat": "35.67", "lon": "139.65"},
    {"name": "London", "lat": "51.50", "lon": "-0.12"}
]

# Runtime override for demo: main.py can post detected origin here
CURRENT_ORIGIN = None

# Neural Link state for visualization
CURRENT_PATH = {"active": False, "origin": None, "target": "LOCKER_01"}

# Thought buffer for AI internal monologue
THOUGHT_BUFFER = []

# Event history for forensic timeline
EVENT_HISTORY = []

# Merkle-style hash chain for immutable audit trail
PREVIOUS_HASH = "SENTIENT_GENESIS_BLOCK"

DB_PATH = "sentient_sync.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS stats 
                 (id INTEGER PRIMARY KEY, total_neutralized INTEGER, last_vector TEXT)''')
    c.execute("INSERT OR IGNORE INTO stats (id, total_neutralized, last_vector) VALUES (1, 0, 'NONE')")
    conn.commit()
    conn.close()

init_db()

app = FastAPI()

# Allow your React dashboard to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/system/status")
def get_status():
    return {"status": "ONLINE", "mode": "AUTONOMOUS", "node": "MIAMI_NODE_01"}


@app.post("/system/clear-vault")
def clear_vault():
    # Deletes current evidence files (for demo resets)
    folder = 'forensic_evidence'
    ui_vault = 'frontend/frontend/public/evidence_vault'
    try:
        if os.path.isdir(folder):
            for f in os.listdir(folder):
                try:
                    os.remove(os.path.join(folder, f))
                except Exception:
                    pass
        if os.path.isdir(ui_vault):
            for f in os.listdir(ui_vault):
                try:
                    os.remove(os.path.join(ui_vault, f))
                except Exception:
                    pass
    except Exception as e:
        return {"message": f"Error purging vault: {e}"}
    return {"message": "Forensic Vault Purged"}


@app.get("/system/vitals")
def get_vitals():
    try:
        cpu = f"{psutil.cpu_percent()}%"
        mem = f"{psutil.virtual_memory().percent}%"
    except Exception:
        cpu = "N/A"
        mem = "N/A"
    origin = CURRENT_ORIGIN if CURRENT_ORIGIN is not None else random.choice(CITIES)
    # Read lifetime neutralized stats from DB
    total_neutralized = 0
    last_vector = 'NONE'
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT total_neutralized, last_vector FROM stats WHERE id = 1")
        row = c.fetchone()
        if row:
            total_neutralized = row[0]
            last_vector = row[1]
        conn.close()
    except Exception:
        pass
    
    # Entropy is based on threat activity (simplified: 20% chance of HIGH_ENTROPY)
    entropy = "STABLE" if random.random() > 0.2 else "HIGH_ENTROPY"

    return {
        "node": "MIAMI_NODE_01",
        "cpu_load": cpu,
        "memory": mem,
        "os": platform.system(),
        "status": "OPERATIONAL",
        "agent": "SENTIENT_v1.0.4",
        "active_threat_origin": origin,
        "total_neutralized": total_neutralized,
        "last_vector": last_vector,
        "neural_link": CURRENT_PATH,
        "entropy": entropy
    }


@app.post("/system/override-origin")
def override_origin(origin: dict):
    """Demo endpoint: accept a JSON object with name/lat/lon to pin the map ping."""
    global CURRENT_ORIGIN
    try:
        # Basic validation: ensure keys present
        if not origin or not all(k in origin for k in ("name", "lat", "lon")):
            return {"message": "Invalid origin payload"}
        CURRENT_ORIGIN = origin
        return {"message": "Origin overridden", "origin": CURRENT_ORIGIN}
    except Exception as e:
        return {"message": f"Error setting origin: {e}"}


@app.post("/system/log-neutralization")
def log_neutralization(data: dict):
    vector = data.get("vector", "UNKNOWN")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE stats SET total_neutralized = total_neutralized + 1, last_vector = ? WHERE id = 1", (vector,))
    conn.commit()
    conn.close()
    return {"status": "STAT_LOGGED"}


@app.post("/system/trigger-link")
def trigger_link(data: dict):
    """Trigger the Neural Link visualization by setting the active path."""
    global CURRENT_PATH
    origin = data.get("origin", {"name": "UNKNOWN", "lat": "0", "lon": "0"})
    CURRENT_PATH = {"active": True, "origin": origin, "target": "LOCKER_01"}
    return {"status": "LINK_ILLUMINATED"}


@app.post("/system/post-thought")
def post_thought(data: dict):
    """Record an AI thought to the internal monologue buffer."""
    global THOUGHT_BUFFER
    thought = data.get("thought", "")
    if thought:
        THOUGHT_BUFFER.append(thought)
        # Keep only last 20 thoughts
        THOUGHT_BUFFER = THOUGHT_BUFFER[-20:]
    return {"status": "THOUGHT_RECORDED"}


@app.get("/system/thoughts")
def get_thoughts():
    """Return the AI's thought buffer."""
    return {"thoughts": THOUGHT_BUFFER}


@app.post("/system/log-event")
def log_event(data: dict):
    """Log an event to the forensic timeline with cryptographic hash chain."""
    global EVENT_HISTORY, PREVIOUS_HASH
    msg = data.get("msg")
    current_hash = hashlib.sha256(f"{PREVIOUS_HASH}{msg}".encode()).hexdigest()
    
    event = {
        "time": time.strftime("%H:%M:%S"),
        "msg": msg,
        "hash": current_hash[:16],  # Show truncated hash for UI
        "type": data.get("type", "INFO")
    }
    PREVIOUS_HASH = current_hash
    EVENT_HISTORY.append(event)
    EVENT_HISTORY = EVENT_HISTORY[-50:]
    return {"status": "EVENT_RECORDED"}


@app.get("/system/history")
def get_history():
    """Return the forensic event history."""
    return {"history": EVENT_HISTORY}


@app.post("/system/query")
async def query_sentient(data: dict):
    """Process natural language commands from the Sentinel Shell."""
    user_input = data.get("command")
    # This would eventually pipe into your LangGraph's 'human_in_the_loop' node
    # For now, we simulate the AI reasoning
    response = f"SENTIENT_SYNC >> Executing analysis on '{user_input}'... No lateral movement detected in SQLite history."
    
    # Log the interaction to our Forensic Chronicle
    try:
        requests.post("http://localhost:8000/system/log-event", 
                      json={"msg": f"USER_QUERY: {user_input}", "type": "INFO"})
    except Exception:
        pass
    
    return {"response": response}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
