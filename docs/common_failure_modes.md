# Common Failure Modes

| Failure mode | Typical cause | Decision |
|---|---|---|
| missing_context | insufficient retrieval evidence | HOLD |
| conflicting_docs | inconsistent evidence | ESCALATE |
| tool_failure | retrieval/tool execution failed | ESCALATE |
| latency_breach | slow validation workflow | HOLD |
| unsupported_answer | unsupported output detected | HOLD |
| low_retrieval_hit_rate | weak evidence retrieval | HOLD |
