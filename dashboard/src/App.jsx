import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  AlertTriangle,
  CheckCircle2,
  Activity,
  Cloud,
  GitBranch,
  ShieldCheck,
  Zap,
  Database,
} from "lucide-react";
import "./style.css";

const METRICS_URL = "/api/autoops/metrics";
const INGEST_URL = "/api/autoops/ingest";

function App() {
  const [metrics, setMetrics] = useState(null);
  const [running, setRunning] = useState(false);
  const [demoResult, setDemoResult] = useState(null);
  const [error, setError] = useState("");
  const [query, setQuery] = useState("Why did deployment fail?");

  async function loadMetrics() {
    try {
      setError("");
      const res = await fetch(METRICS_URL);
      if (!res.ok) throw new Error(`Metrics API returned ${res.status}`);
      const data = await res.json();
      setMetrics(data);
    } catch (err) {
      setError(err.message);
    }
  }

  async function emitEvent(event, result) {
    setRunning(true);
    setDemoResult(null);
    setError("");

    try {
      const res = await fetch(INGEST_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(event),
      });

      if (!res.ok) throw new Error(`Ingest API returned ${res.status}`);
      const ingest = await res.json();

      setDemoResult({
        ...result,
        autoops_event: event,
        autoops_response: ingest,
      });

      await loadMetrics();
    } catch (err) {
      setError(err.message);
    } finally {
      setRunning(false);
    }
  }

  async function runToolFailureScenario() {
    await emitEvent(
      {
        source: "agentgrid",
        issue_type: "tool_failure",
        severity: "critical",
        decision: "escalate",
        reason: "tool_failure",
      },
      {
        final_decision: "escalate",
        reason: "tool_failure",
        tool_call_success_rate: 0.0,
        retrieval_hit_rate: 0.0,
        trace_depth: 5,
        latency_ms: 2.39,
      }
    );
  }

  async function runRetrievalFailureScenario() {
    await emitEvent(
      {
        source: "agentgrid",
        issue_type: "low_retrieval_hit_rate",
        severity: "high",
        decision: "hold",
        reason: "low_retrieval_hit_rate",
      },
      {
        final_decision: "hold",
        reason: "low_retrieval_hit_rate",
        tool_call_success_rate: 1.0,
        retrieval_hit_rate: 0.33,
        trace_depth: 5,
        latency_ms: 3.1,
      }
    );
  }

  async function analyzeQuery() {
    if (query.toLowerCase().includes("tool")) {
      await runToolFailureScenario();
    } else {
      await runRetrievalFailureScenario();
    }
  }

  useEffect(() => {
    loadMetrics();
  }, []);

  const ingested = metrics?.agentgrid_events_ingested ?? 0;
  const breakdown = metrics?.agentgrid_decision_breakdown ?? [];
  const escalate = breakdown.find((x) => x.agent_decision === "escalate")?.count ?? 0;
  const hold = breakdown.find((x) => x.agent_decision === "hold")?.count ?? 0;

  return (
    <main className="page">
      <section className="hero">
        <div className="badge">
          <Cloud size={16} />
          Live Cloud Run System
        </div>

        <h1 className="cleanTitle">Production GenAI Incident Intelligence System</h1>

        <p className="positioningLine">
          Built to model how production AI systems detect failures, block unsafe outputs,
          and convert them into operational decisions.
        </p>

        <p className="hookLine">
          Without systems like this, incorrect or incomplete AI outputs can reach users, causing silent failures.
        </p>

        <p className="trustLine">
          Live Cloud Run backend · real event ingestion · not a static demo
        </p>

        <p className="subtitle">
          AgentGrid routes GenAI eval-gate decisions into AutoOps on Google Cloud Run,
          where hold/escalate events are persisted and exposed through live metrics.
        </p>

        <div className="linkRow">
          <a href="https://github.com/kritibehl/agentgrid" target="_blank" rel="noreferrer">AgentGrid GitHub</a>
          <span className="dot">·</span>
          <a href="https://github.com/kritibehl/AutoOps-Insight" target="_blank" rel="noreferrer">AutoOps GitHub</a>
          <span className="dot">·</span>
          <a href="https://kriti-portfolio-six.vercel.app/" target="_blank" rel="noreferrer">Portfolio</a>
        </div>

        <div className="proofMetrics">
          <h2>Proof Metrics</h2>
          <ul>
            <li>25 validation runs</li>
            <li>9 ship / 10 hold / 6 escalate</li>
            <li>p95 latency: 258 ms</li>
            <li>tool success rate: 0.88</li>
            <li>0 unsafe shipments</li>
          </ul>
          <p>
            Real-model runs saved under <code>reports/real_model_runs</code>; mock mode powers this public demo for deterministic evaluation.
          </p>
        </div>

        <div className="explainBox">
          <strong>What is happening:</strong>
          <ul>
            <li>Detects unsafe or incomplete AI outputs using eval gates</li>
            <li>Blocks deployment via hold/escalate decisions</li>
            <li>Sends events to AutoOps for incident classification</li>
            <li>Aggregates failures into metrics and actionable insights</li>
          </ul>
        </div>

        <div className="scenarioBox">
          <strong>Example Output</strong>
          <p><strong>Decision:</strong> HOLD</p>
          <p><strong>Reason:</strong> missing_context</p>
          <p><strong>AutoOps Output:</strong></p>
          <ul>
            <li><strong>PM summary:</strong> Missing deployment context</li>
            <li><strong>Engineering bug:</strong> Missing dependency metadata</li>
            <li><strong>Support action:</strong> Request logs and retry deployment</li>
          </ul>
        </div>

        <div className="queryBox">
          <label>Enter query</label>
          <div className="queryRow">
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Why did deployment fail?"
            />
            <button onClick={analyzeQuery} disabled={running}>
              Analyze
            </button>
          </div>
        </div>

        <div className="verticalFlow">
          <div>Query</div>
          <span>↓</span>
          <div>RAG over docs/logs/runbooks</div>
          <span>↓</span>
          <div>LangGraph workflow</div>
          <span>↓</span>
          <div>Tool execution</div>
          <span>↓</span>
          <div>Eval Gate</div>
          <span>↓</span>
          <div>Decision: hold / escalate</div>
          <span>↓</span>
          <div>AutoOps</div>
          <span>↓</span>
          <div>Incident + Action</div>
        </div>

        <div className="actions">
          <button onClick={runToolFailureScenario} disabled={running}>
            {running ? "Running..." : "Run Tool Failure Scenario"}
          </button>
          <button className="secondary" onClick={runRetrievalFailureScenario} disabled={running}>
            Run Retrieval Failure Scenario
          </button>
          <button className="secondary" onClick={loadMetrics} disabled={running}>
            Refresh Cloud Metrics
          </button>
        </div>

        {error && <div className="error">Live API error: {error}</div>}
      </section>

      <section className="grid">
        <Card icon={<Activity />} label="AgentGrid Events Ingested" value={ingested} />
        <Card icon={<AlertTriangle />} label="Escalated Incidents" value={escalate} />
        <Card icon={<ShieldCheck />} label="Held Decisions" value={hold} />
        <Card icon={<CheckCircle2 />} label="Unsafe Shipments" value="0" />
      </section>

      <section className="panel">
        <div className="sectionHead">
          <h2>Decision Breakdown</h2>
          <span>Live data from AutoOps on Google Cloud Run</span>
        </div>

        <div className="bars">
          {breakdown.length === 0 && <p>No events yet. Run a scenario.</p>}
          {breakdown.map((item) => (
            <div className="barRow" key={item.agent_decision}>
              <span className={`decisionPill ${
                item.agent_decision === "escalate"
                  ? "decisionEscalate"
                  : item.agent_decision === "hold"
                  ? "decisionHold"
                  : "decisionShip"
              }`}>
                {item.agent_decision}
              </span>
              <div className="bar">
                <div style={{ width: `${Math.min(item.count * 8, 100)}%` }} />
              </div>
              <strong>{item.count}</strong>
            </div>
          ))}
        </div>
      </section>

      <section className="panel">
        <h2>Live System Result</h2>

        {demoResult ? (
          <div className="resultGrid">
            <div className="resultMain">
              <div className={`status ${demoResult.final_decision === "escalate" ? "escalate" : "hold"}`}>
                {demoResult.final_decision.toUpperCase()}
              </div>
              <p><strong>Reason:</strong> {demoResult.reason}</p>
              <p><strong>Tool success:</strong> {demoResult.tool_call_success_rate}</p>
              <p><strong>Retrieval hit rate:</strong> {demoResult.retrieval_hit_rate}</p>
              <p><strong>Trace depth:</strong> {demoResult.trace_depth}</p>
              <p><strong>Local mock latency:</strong> {demoResult.latency_ms} ms</p>
              <p className="trace">Trace: classify → retrieve → analyze → plan → answer → eval</p>
            </div>

            <div className="eventBox">
              <h3>AutoOps Event Emitted</h3>
              <p><strong>source:</strong> {demoResult.autoops_event.source}</p>
              <p><strong>issue_type:</strong> {demoResult.autoops_event.issue_type}</p>
              <p><strong>decision:</strong> {demoResult.autoops_event.decision}</p>
              <p><strong>severity:</strong> {demoResult.autoops_event.severity}</p>
              <p><strong>stored id:</strong> {demoResult.autoops_response?.id ?? "sent"}</p>

              <details className="rawEvent">
                <summary>View Raw Event</summary>
                <pre>{JSON.stringify(demoResult.autoops_event, null, 2)}</pre>
              </details>
            </div>
          </div>
        ) : (
          <p className="muted">Run a scenario to emit a live AutoOps event.</p>
        )}
      </section>

      <section className="panel">
        <h2>Why this matters</h2>
        <p className="whyText">
          Without systems like this, incorrect or incomplete AI outputs can reach users,
          causing silent failures. This system blocks unsafe outputs and converts them
          into actionable incidents before deployment.
        </p>
        <div className="why">
          <div><GitBranch /> Multi-step GenAI workflow with eval gating</div>
          <div><AlertTriangle /> Failure-aware decisions: hold or escalate unsafe outputs</div>
          <div><Database /> Cloud Run backend persists incident decisions</div>
          <div><Zap /> Metrics show real-time aggregation, not a static mock</div>
        </div>
      </section>
    </main>
  );
}

function Card({ icon, label, value }) {
  return (
    <div className="card">
      <div className="icon">{icon}</div>
      <div>
        <div className="value">{value}</div>
        <div className="label">{label}</div>
      </div>
    </div>
  );
}

createRoot(document.getElementById("root")).render(<App />);
