from typing import TypedDict, List
import json

# Define the shared state that agents will pass around
class AgentState(TypedDict):
    raw_logs: str
    threat_data: List[dict]
    integrity_verified: bool
    status: str

# Node 1: The Collector (Wraps your parse_logs logic)
def collector_node(state: AgentState):
    print("--- COLLECTING LOGS ---")
    # In Phase 2, this will call your actual parse_logs()
    return {"status": "Logs Collected"}

# Node 2: The Auditor (The core brain)
def auditor_node(state: AgentState):
    print("--- AUDITING FOR COLLUSION ---")
    # This is where Claude will eventually reason over the data
    return {"integrity_verified": True, "status": "Audit Complete"}

# Node 3: The UI Bridge (Updates your pulse.json)
def ui_update_node(state: AgentState):
    print("--- UPDATING DASHBOARD ---")
    # This pushes the data to your Bento Box website
    return {"status": "Active"}
