# Builder Onboarding

AgentGrid is a GenAI support operations platform for validating AI workflow safety.

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
Run API:

uvicorn src.api.server:app --reload

Run dashboard:

cd dashboard
npm install
npm run dev

Run validation workflow:

python3 -m src.app --file data/failure_cases/tool_failure.txt
What AgentGrid does
validates retrieval quality
validates tool execution
blocks unsupported outputs
generates ship/hold/escalate decisions
emits support incidents into AutoOps
Recommended learning path
run local validation scenarios
inspect trace IDs
inspect eval-gate decisions
inspect AutoOps ingestion
inspect Redis worker flows
