# AgentGrid GenAI Text Workflow Quality Review

## Purpose

This artifact extends AgentGrid's support-workflow framing to common GenAI text-generation tasks:

- rewriting
- summarization
- support reply generation
- unsupported-answer handling

Retrieval is optional in these scenarios. The main focus is whether the generation step follows instructions and avoids unsafe or unsupported content.

## Evaluation Gate Checks

| Check | Purpose |
|---|---|
| instruction_adherence | Confirms the model followed task constraints |
| unsupported_detail | Detects invented facts or unsupported fixes |
| missing_required_content | Detects omitted required information |
| concise_reply_quality | Checks whether the response is appropriately brief and useful |

## Scenario Coverage

| Scenario | Task | Key risk |
|---|---|---|
| rewrite_clarity_001 | rewrite | hallucinated root cause |
| summarize_incident_001 | summarization | missing remediation action |
| support_reply_001 | support reply | missing diagnostic next step |
| unsupported_reply_001 | support reply | unsupported confident fix |

## Why This Matters

Many production GenAI support failures are not only retrieval failures. They also occur when a model:

- ignores formatting constraints
- invents unsupported details
- omits required support context
- writes overly long or unclear replies
- claims resolution without evidence

AgentGrid's eval-gate framing can be applied to these text workflows by checking whether generated outputs are safe, concise, supported, and instruction-following.

## Resume-Safe Summary

Added controlled GenAI text-workflow scenarios for rewrite, summarization, and support reply-generation tasks, with evaluation checks for instruction adherence, unsupported details, missing required content, and concise reply quality.
