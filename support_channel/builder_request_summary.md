# Builder Request Summary

| Request | Category | Doc link | CLI command | Repeat? |
|---|---|---|---|---|
| br_001 | build_failed | docs/builder_onboarding.md | `pytest -q && python3 -m src.app --file data/failure_cases/tool_failure.txt` | False |
| br_002 | publishing_error | docs/troubleshooting_guide.md | `npm run build && vercel --prod` | False |
| br_003 | tool_call_failure | docs/cli_debugging_examples.md | `python3 -m src.support.diagnose --case examples/tool_failure_case.json` | False |
| br_004 | unsupported_answer | docs/common_failure_modes.md | `python3 -m src.support.diagnose --case examples/unsupported_answer_case.json` | False |
| br_005 | missing_docs_context | docs/troubleshooting_guide.md | `python3 -m src.support.diagnose --case examples/retrieval_failure_case.json` | True |
| br_006 | latency_breach | docs/common_failure_modes.md | `python3 -m src.support.diagnose --case examples/latency_breach_case.json` | False |
| br_007 | missing_docs_context | docs/troubleshooting_guide.md | `python3 -m src.support.diagnose --case examples/retrieval_failure_case.json` | True |
