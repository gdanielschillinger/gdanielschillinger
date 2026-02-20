import os
import json
import hashlib
from datetime import datetime

EVIDENCE_DIR = "forensic_evidence"

def seal_evidence(log_entry, threat_type):
    if not os.path.exists(EVIDENCE_DIR):
        os.makedirs(EVIDENCE_DIR)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    evidence_id = hashlib.md5(log_entry.encode()).hexdigest()[:8]
    filename = f"{EVIDENCE_DIR}/case_{timestamp}_{evidence_id}.json"

    artifact = {
        "case_id": f"SR-{evidence_id}",
        "captured_at": str(datetime.now()),
        "threat_classification": threat_type,
        "raw_log": log_entry,
        "chain_of_custody": "Sentient_Sync_Automated_Agent",
        "integrity_hash": hashlib.sha256(log_entry.encode()).hexdigest()
    }

    with open(filename, "w") as f:
        json.dump(artifact, f, indent=4)
    
    return filename

print("[+] Forensic Evidence Locker: ONLINE")
