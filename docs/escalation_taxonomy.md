# AgentGrid Escalation Taxonomy

| Failure signal | Decision | Owner | Support action |
|---|---|---|---|
| Missing context | HOLD | Support reviewer | Request missing source/log/runbook |
| Conflicting evidence | ESCALATE | Product/support reviewer | Route for manual review |
| Tool failure | ESCALATE | Engineering | Investigate tool/runtime failure |
| Latency breach | HOLD | Platform/infra | Hold response until latency stabilizes |
| Unsupported answer | HOLD | Reviewer | Block unsupported output |
| Low retrieval quality | HOLD | Support/retrieval owner | Request better evidence |
