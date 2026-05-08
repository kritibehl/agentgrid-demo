# Engineering Bug Report Examples

## Tool failure
- Signal: document search tool failed
- Impact: support workflow could not retrieve required evidence
- Expected: tool returns evidence or controlled failure state
- Actual: tool failure triggered escalation

## Low retrieval quality
- Signal: retrieval hit rate below threshold
- Impact: answer could be unsupported
- Expected: sufficient evidence coverage
- Actual: workflow returned HOLD
