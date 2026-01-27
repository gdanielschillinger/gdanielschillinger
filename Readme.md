# Security Log Analyzer & Automated Auditor

A Python-based security automation engine designed for log ingestion, regex-based telemetry extraction, and automated threat triage. This tool identifies brute-force patterns and generates standardized JSON alerts for security operations.

## Milestone: Internal SOC Readiness
The core engine is fully operational. It successfully parses raw server telemetry and identifies High-Risk Indicators of Compromise (IoCs).

### SOC Analyst Threat Report
* **Dataset**: `logs.txt` (Synthetic Production Simulation)
* **Total Entries Processed**: 5
* **Identified Authentication Failures**: 3
* **System Status**: HIGH RISK ACTIVITY DETECTED

### Threat Vector Summary
| Indicator (IP) | Failures | Risk Level | Mitigation Action |
| :--- | :--- | :--- | :--- |
| 10.0.0.50 | 3 | HIGH | Logged to alerts.json for SIEM Ingestion |

---

## Technical Architecture
* **Telemetry Extraction**: Custom Regex patterns extract ISO-8601 timestamps, status codes, and IP addresses.
* **Automated Triage**: Threshold-based logic identifies brute-force attempts (Threshold: 3 failures).
* **Audit Compliance**: Standardized JSON export ensures interoperability with modern SIEM/SOAR platforms.

## Project Roadmap
- [x] **Week 1: Data Ingestion** (Regex Parsing & File Handling)
- [x] **Week 2: Automated Auditing** (Threshold Triage & JSON Export)
- [ ] **Week 3: AGI Integration** (LLM-based Threat Summarization)
- [ ] **Week 4: Deployment & Portfolio Validation**