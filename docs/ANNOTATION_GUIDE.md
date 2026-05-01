# Postmortem Atlas Annotation Guide

Each entry should normalize a public postmortem into a comparable reliability record.

## Required fields

- failure_taxonomy: classify the dominant technical failure modes
- system_layers: identify where the failure primarily manifested
- detection_method: how the incident was first detected
- detection_gap_minutes: minutes between fault onset and reliable operator awareness
- recovery_pattern: primary mitigation or restoration actions
- what_would_have_caught_it_earlier: earlier monitoring, validation, or release controls
- atlas_lessons: one paragraph connecting the incident to resilience validation

## Annotation rules

1. Prefer the earliest reliable public timestamp when estimating detection gap.
2. Use 1–3 dominant failure types, not every possible label.
3. Separate root cause from customer-visible impact.
4. Tie lessons back to proactive reliability validation, not generic advice.
5. Preserve source fidelity; do not invent details not supported by the postmortem.

## Reliability framing

The atlas should answer four questions for every outage:

1. What failed?
2. How long did detection take?
3. How was recovery achieved?
4. What validation or monitoring would have caught it sooner?
