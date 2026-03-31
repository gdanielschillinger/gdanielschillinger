import re
import os
import json
import hmac
import hashlib
import ipaddress
import logging
from collections import Counter
from typing import TypedDict, List, Optional

import requests
from langgraph.graph import StateGraph, END
from google import genai

from evidence_locker import seal_evidence

LOGGER = logging.getLogger(__name__)

# Gemini client — loaded once at module init
_GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
_gemini_client = genai.Client(api_key=_GEMINI_API_KEY) if _GEMINI_API_KEY else None
_GEMINI_MODEL = "gemini-2.5-pro-exp-03-25"

# HMAC key for signing LLM output (reuses same env var as main.py)
_HMAC_KEY = os.environ.get("SENTIENT_HMAC_KEY", "")

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
    location: str
    evidence_file: Optional[str]
    collusion_score: int
    llm_analysis: Optional[str]       # Structured threat reasoning from Gemini
    llm_analysis_signature: Optional[str]  # HMAC-SHA256 signature of the LLM output

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

def triage_threat_node(state: AgentState) -> dict:
    """Classify threats from logs into OWASP/NIST categories and extract origin location."""
    print("--- NODE: DEEP FORENSIC TRIAGE ---")
    emit_thought(">> INITIALIZING NIST-CSF-2.0 TRIAGE SEQUENCE...")
    actions = []
    location = "UNKNOWN"

    # Location extraction pattern
    _location_pattern = re.compile(r"(Berlin|Tokyo|London|Miami|Moscow|Sydney|Toronto)", re.IGNORECASE)

    for log in state["logs"]:
        # LLM01: Prompt Injection
        if "Prompt" in log or "Injection" in log:
            actions.append("OWASP-LLM01:2025-Direct_Injection")
            emit_thought(">> THREAT_VECTOR: DIRECT_PROMPT_INJECTION_DETECTED")
        # A07: Authentication Failures
        elif "Authentication" in log:
            actions.append("OWASP-A07:2025-Authentication_Failure")
            emit_thought(">> THREAT_VECTOR: AUTHENTICATION_FAILURE_ESCALATION")
        # DE.AE: Brute Force Anomaly
        elif "Brute Force" in log:
            actions.append("NIST-CSF-2.0:DE.AE-Brute_Force_Anomaly")
            emit_thought(">> THREAT_VECTOR: BRUTE_FORCE_ATTACK_PATTERN")
        # XSS
        elif "XSS" in log or "<script" in log.lower():
            actions.append("OWASP-A03:2025-XSS_Injection")
            emit_thought(">> THREAT_VECTOR: CROSS_SITE_SCRIPTING_DETECTED")
        # SQL Injection
        elif "SQL" in log or "OR 1=1" in log:
            actions.append("OWASP-A03:2025-SQL_Injection")
            emit_thought(">> THREAT_VECTOR: SQL_INJECTION_DETECTED")

        # Extract origin location from log line
        loc_match = _location_pattern.search(log)
        if loc_match:
            location = loc_match.group().upper()

    thought = " // ".join(actions) if actions else "NIST-ID.AM:2025_Steady_State"
    emit_thought(f">> TRIAGE_COMPLETE: {thought}")
    return {"threat_level": "ANALYZED", "action_taken": thought, "location": location}

def llm_analysis_node(state: AgentState) -> dict:
    """Send flagged log lines to Gemini for structured LLM threat analysis.

    Only activates when triage has flagged at least one OWASP/NIST threat vector.
    Passes a structured prompt asking Gemini to reason over the flagged logs,
    identify the most likely attack pattern, assess severity, and recommend
    a response aligned to NIST CSF 2.0.

    The LLM output is HMAC-SHA256 signed before being stored in state,
    ensuring the analysis cannot be tampered with after generation.
    Falls back gracefully if Gemini is unavailable (no API key or network error).
    """
    print("--- NODE: LLM THREAT ANALYSIS ---")
    emit_thought(">> DISPATCHING TO GEMINI: STRUCTURED THREAT REASONING...")

    action = state.get("action_taken", "")
    logs = state.get("logs", [])

    # Only invoke LLM when triage has flagged a real threat
    if not action or "Steady_State" in action or "MONITORING" in action:
        emit_thought(">> LLM_ANALYSIS: SKIPPED | NO ACTIVE THREAT VECTORS")
        return {"llm_analysis": None, "llm_analysis_signature": None}

    if not _gemini_client:
        LOGGER.warning("GEMINI_API_KEY not set — LLM analysis node skipped.")
        emit_thought(">> LLM_ANALYSIS: SKIPPED | GEMINI_API_KEY NOT CONFIGURED")
        return {"llm_analysis": None, "llm_analysis_signature": None}

    # Build structured prompt — deterministic, auditable input
    flagged_logs = "\n".join(f"  [{i+1}] {line}" for i, line in enumerate(logs[-10:]))
    prompt = (
        "You are a cybersecurity threat analyst operating inside the Sentient Sync Engine, "
        "an AGI security framework aligned to NIST CSF 2.0 and OWASP LLM Top 10:2025.\n\n"
        f"Triage has flagged the following threat vectors: {action}\n\n"
        f"Relevant log entries:\n{flagged_logs}\n\n"
        "Respond in valid JSON only. Do not include markdown. Use this exact schema:\n"
        "{\n"
        '  "attack_pattern": "<most likely attack pattern>",\n'
        '  "owasp_vector": "<primary OWASP LLM Top 10 or OWASP Top 10 category>",\n'
        '  "severity": "LOW | MEDIUM | HIGH | CRITICAL",\n'
        '  "reasoning": "<2-3 sentence technical explanation>",\n'
        '  "nist_response": "<recommended NIST CSF 2.0 Respond action>",\n'
        '  "confidence": <integer 0-100>\n'
        "}"
    )

    try:
        response = _gemini_client.models.generate_content(
            model=_GEMINI_MODEL,
            contents=prompt,
        )
        raw_output = response.text.strip()

        # Validate the response is parseable JSON before accepting it
        parsed = json.loads(raw_output)
        analysis_json = json.dumps(parsed, separators=(",", ":"))

        # HMAC-SHA256 sign the LLM output — proves it has not been altered post-generation
        signature = "UNSIGNED"
        if _HMAC_KEY:
            signature = hmac.new(
                bytes.fromhex(_HMAC_KEY),
                analysis_json.encode("utf-8"),
                hashlib.sha256,
            ).hexdigest()

        severity = parsed.get("severity", "UNKNOWN")
        confidence = parsed.get("confidence", 0)
        emit_thought(
            f">> LLM_ANALYSIS: {severity} | confidence={confidence}% "
            f"| sig={signature[:12]}..."
        )
        LOGGER.info("LLM analysis complete: severity=%s confidence=%s", severity, confidence)

        return {
            "llm_analysis": analysis_json,
            "llm_analysis_signature": signature,
        }

    except json.JSONDecodeError as exc:
        LOGGER.warning("Gemini returned non-JSON output: %s", exc)
        emit_thought(">> LLM_ANALYSIS: FAILED | INVALID JSON RESPONSE")
        return {"llm_analysis": None, "llm_analysis_signature": None}
    except Exception as exc:
        LOGGER.warning("LLM analysis node error: %s", exc)
        emit_thought(">> LLM_ANALYSIS: FAILED | API ERROR")
        return {"llm_analysis": None, "llm_analysis_signature": None}


# 3. Build the Graph
workflow = StateGraph(AgentState)

# Add our nodes
workflow.add_node("auditor", audit_integrity_node)
workflow.add_node("triager", triage_threat_node)
workflow.add_node("llm_analyzer", llm_analysis_node)

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

def collusion_check_node(state: AgentState) -> dict:
    """Detect coordinated multi-source attacks using spatial correlation and confidence scoring.

    Analyzes the last 20 log entries for distinct source IPs across distinct /24 subnets.
    Returns a confidence score (0-100) rather than a boolean flag.
    Score >= 60 triggers a collusion alert with supporting evidence.
    """
    print("--- NODE: COLLUSION_DETECTION ---")
    emit_thought(">> EXECUTING MULTI-VECTOR COLLUSION_SCAN...")

    logs = state.get("logs", [])
    if len(logs) < 3:
        emit_thought(">> LOG_BUFFER_INSUFFICIENT | COLLUSION_CHECK_SKIPPED")
        return {"action_taken": state.get("action_taken"), "collusion_score": 0}

    # Extract and validate IPs from the last 20 log entries
    ip_pattern = re.compile(r"\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b")
    valid_ips: list[str] = []

    for log_line in logs[-20:]:
        for ip_str in ip_pattern.findall(log_line):
            try:
                ipaddress.IPv4Address(ip_str)
                valid_ips.append(ip_str)
            except ipaddress.AddressValueError:
                continue

    unique_ips = set(valid_ips)

    # Subnet-level deduplication — same /24 = likely same actor
    unique_subnets: set[ipaddress.IPv4Network] = set()
    for ip in unique_ips:
        try:
            subnet = ipaddress.IPv4Network(f"{ip}/24", strict=False)
            unique_subnets.add(subnet)
        except ValueError:
            continue

    # Confidence scoring (0-100)
    score = 0
    if len(unique_subnets) >= 3:
        score += 40  # Attacks from 3+ distinct /24 networks
    if len(unique_ips) >= 5:
        score += 30  # High source IP diversity
    if len(valid_ips) > 0 and len(valid_ips) / max(len(unique_ips), 1) < 2:
        score += 30  # Low repetition per IP = coordinated probing pattern

    if score >= 60:
        evidence = f"IPs:{len(unique_ips)} | Subnets:{len(unique_subnets)} | Confidence:{score}%"
        emit_thought(f">> SPATIAL_CORRELATION: POSITIVE | {evidence}")
        return {
            "action_taken": f"ALERT: COORDINATED_COLLUSION_DETECTED [{evidence}]",
            "collusion_score": score,
        }

    emit_thought(f">> SPATIAL_CORRELATION: NEGATIVE | Subnets:{len(unique_subnets)} | Score:{score}%")
    return {"action_taken": state.get("action_taken"), "collusion_score": score}

# Define the edges (The "Nerves")
workflow.set_entry_point("auditor")
workflow.add_edge("auditor", "triager")
# Route: triager -> collusion check -> responder -> END
workflow.add_node("collusion", collusion_check_node)
workflow.add_node("responder", responder_node)
workflow.add_edge("triager", "llm_analyzer")
workflow.add_edge("llm_analyzer", "collusion")
workflow.add_edge("collusion", "responder")
workflow.add_edge("responder", END)

# Compile the Brain
sentient_ai = workflow.compile()

print("[+] Sentient Nervous System: ONLINE")
