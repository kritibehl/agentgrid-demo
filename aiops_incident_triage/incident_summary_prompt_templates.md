# Incident Summary Prompt Templates

## Grounded Incident Summary Template

Use only the provided logs, telemetry, and runbook context.

Required sections:

1. Incident summary
2. Probable-cause hypothesis
3. Evidence used
4. Missing evidence
5. Recommended support actions
6. Escalation recommendation

## Guardrails

- Do not state root cause as certain unless evidence is conclusive.
- Frame root cause as a hypothesis.
- Cite logs, telemetry, or runbook context.
- Do not invent missing dependencies.
- If runbook context is missing, mark the summary as evidence-limited.
- Include next diagnostic steps.
