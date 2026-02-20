from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from evidence_locker import seal_evidence
import requests

def emit_thought(thought):
    """Emit an AI thought to the thought buffer via API."""
    try:
        requests.post("http://localhost:8000/system/post-thought", json={"thought": thought}, timeout=1)
    except Exception:
        pass

# 1. Define the "State" (What the AI remembers)
class AgentState(TypedDict):
    logs: List[str]
    integrity_status: str
    threat_level: str
    action_taken: str

# 2. Define the Nodes (The AI's "Organs")
def audit_integrity_node(state: AgentState):
    print("--- NODE: AUDITING INTEGRITY ---")
    emit_thought(">> INITIALIZING INTEGRITY AUDIT...")
    # This is where your HMAC logic lives
    if state["integrity_status"] == "COMPROMISED":
        emit_thought(">> CRITICAL: LOG INTEGRITY COMPROMISED")
        return {"threat_level": "CRITICAL", "action_taken": "LOCKDOWN_UI"}
    emit_thought(">> INTEGRITY CHECK: PASSED")
    return {"threat_level": "STABLE", "action_taken": "MONITORING"}

def triage_threat_node(state: AgentState):
    print("--- NODE: DEEP FORENSIC TRIAGE ---")
    emit_thought(">> INITIALIZING NIST-CSF-2.0 TRIAGE SEQUENCE...")
    actions = []
    location = "UNKNOWN"

    for log in state["logs"]:
        if "Prompt" in log or "Injection" in log:
            # Addressing the #1 AGI threat of 2026
            actions.append("OWASP-LLM01:2026-Direct_Injection")
            emit_thought(">> THREAT_VECTOR: DIRECT_PROMPT_INJECTION_DETECTED")
        elif "Authentication" in log:
            actions.append("OWASP-A01:2026-Broken_Access")
            emit_thought(">> THREAT_VECTOR: AUTHENTICATION_FAILURE_ESCALATION")
        elif "Brute Force" in log:
            # NIST CSF 2.0 Detect Category
            actions.append("NIST-CSF-2.0:DE.AE-Anomaly")
            emit_thought(">> THREAT_VECTOR: BRUTE_FORCE_ATTACK_PATTERN")
            
    # Join thoughts for the UI to display
    thought = " // ".join(actions) if actions else "NIST-ID.AM:2026_Steady_State"
    emit_thought(f">> TRIAGE_COMPLETE: {thought}")
    return {"threat_level": "ANALYZED", "action_taken": thought}

# 3. Build the Graph
workflow = StateGraph(AgentState)

# Add our nodes
workflow.add_node("auditor", audit_integrity_node)
workflow.add_node("triager", triage_threat_node)
# Add responder node placeholder (will archive evidence when flagged)

def responder_node(state: AgentState):
    print("--- NODE: EXECUTING RESPONSE ---")
    emit_thought(">> INITIATING_RESPONSE_PROTOCOL...")
    action = state.get("action_taken", "")
    # Be robust: also inspect logs for forensic indicators
    try:
        logs = state.get("logs", [])
        last_log = logs[-1] if logs else ""
        # If triage flagged an OWASP or critical pattern, archive
        if isinstance(action, str) and ("CRITICAL" in action or "FLAGGED" in action):
            emit_thought(f">> ARCHIVING_EVIDENCE: {action}")
            file_saved = seal_evidence(last_log, action)
            emit_thought(f">> EVIDENCE_SEALED: {file_saved}")
            # NEW: Log to persistent API counter
            try:
                requests.post("http://localhost:8000/system/log-neutralization", json={"vector": action}, timeout=1)
            except Exception:
                pass
            return {"action_taken": f"ARCHIVED_TO_LOCKER: {file_saved}"}

        for log in logs:
            if "Authentication Failure" in log or "Access Control" in log or "Brute Force" in log or "ALERT" in log:
                emit_thought(">> AUTO_FLAGGED_THREAT_DETECTED")
                file_saved = seal_evidence(last_log, "AUTO_FLAGGED")
                emit_thought(f">> EVIDENCE_AUTO_ARCHIVED: {file_saved}")
                try:
                    requests.post("http://localhost:8000/system/log-neutralization", json={"vector": "AUTO_FLAGGED"}, timeout=1)
                except Exception:
                    pass
                return {"action_taken": f"ARCHIVED_TO_LOCKER: {file_saved}"}
    except Exception:
        emit_thought(">> RESPONSE_EXECUTION_ERROR")
        pass
    emit_thought(">> RESPONSE_COMPLETE | MONITORING_RESUMED")
    return {"action_taken": action}

def collusion_check_node(state: AgentState):
    print("--- NODE: COLLUSION_DETECTION ---")
    emit_thought(">> EXECUTING MULTI-VECTOR COLLUSION_SCAN...")
    # If the last 5 logs show 3+ different IP/Locations, it's a coordinated attack
    logs = state.get("logs", [])
    if len(logs) > 5:
        # crude heuristic: count distinct tokens that look like IPs or city names
        distinct = set()
        for l in logs[-5:]:
            import re
            m = re.findall(r"\d+\.\d+\.\d+\.\d+", l)
            if m:
                distinct.update(m)
            else:
                if "Berlin" in l: distinct.add("Berlin")
                if "Tokyo" in l: distinct.add("Tokyo")
                if "London" in l: distinct.add("London")
        if len(distinct) >= 3:
            emit_thought(">> SPATIAL_CORRELATION: POSITIVE | ATTACK_PATTERN: COORDINATED")
            return {"action_taken": "ALERT: COORDINATED_COLLUSION_DETECTED"}
        else:
            emit_thought(">> SPATIAL_CORRELATION: NEGATIVE | SINGLE_VECTOR_ATTACK")
    else:
        emit_thought(">> LOG_BUFFER_INSUFFICIENT | COLLUSION_CHECK_SKIPPED")
    return {"action_taken": state.get("action_taken")}

# Define the edges (The "Nerves")
workflow.set_entry_point("auditor")
workflow.add_edge("auditor", "triager")
# Route: triager -> collusion check -> responder -> END
workflow.add_node("collusion", collusion_check_node)
workflow.add_node("responder", responder_node)
workflow.add_edge("triager", "collusion")
workflow.add_edge("collusion", "responder")
workflow.add_edge("responder", END)

# Compile the Brain
sentient_ai = workflow.compile()

print("[+] Sentient Nervous System: ONLINE")
