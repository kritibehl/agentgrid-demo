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

const AUTOOPS_API = import.meta.env.VITE_AUTOOPS_API_URL || "/api";

function App() {
  const [metrics, setMetrics] = useState(null);
  const [running, setRunning] = useState(false);
  const [demoResult, setDemoResult] = useState(null);
  const [error, setError] = useState("");

  async function loadMetrics() {
    try {
      setError("");
      const res = await fetch(`${AUTOOPS_API}/support/metrics`);
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
      const res = await fetch(`${AUTOOPS_API}/support/ingest`, {
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

  async function runToolFailureDemo() {
    const event = {
      source: "agentgrid",
      issue_type: "tool_failure",
      severity: "critical",
      decision: "escalate",
      reason: "tool_failure",
    };

    await emitEvent(event, {
      final_decision: "escalate",
      reason: "tool_failure",
      tool_call_success_rate: 0.0,
      retrieval_hit_rate: 0.0,
      trace_depth: 5,
      latency_ms: 2.39,
    });
  }

  async function runLowRetrievalDemo() {
    const event = {
      source: "agentgrid",
      issue_type: "low_retrieval_hit_rate",
      severity: "high",
      decision: "hold",
      reason: "low_retrieval_hit_rate",
    };

    await emitEvent(event, {
      final_decision: "hold",
      reason: "low_retrieval_hit_rate",
      tool_call_success_rate: 1.0,
      retrieval_hit_rate: 0.33,
      trace_depth: 5,
      latency_ms: 3.1,
    });
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
          Live Cloud Run Demo
        </div>

        <h1>AI Incident Intelligence Pipeline</h1>

        <p className="subtitle">
          AgentGrid routes GenAI eval-gate decisions into AutoOps on Google Cloud Run,
          where hold/escalate events are persisted and exposed through live metrics.
        </p>

        <div className="proofLine">
          Validated across <strong>25 GenAI failure scenarios</strong> →{" "}
          <strong>9 ship</strong> / <strong>10 hold</strong> / <strong>6 escalate</strong> ·{" "}
          <strong>258.02 ms p95</strong> · <strong>0.88 tool-call success rate</strong> ·{" "}
          <strong>0 unsafe shipments</strong>
        </div>

        <div className="flow">
          <span>Query</span>
          <span>RAG</span>
          <span>LangGraph</span>
          <span>MCP Tools</span>
          <span>Eval Gate</span>
          <span>AutoOps</span>
        </div>

        <div className="actions">
          <button onClick={runToolFailureDemo} disabled={running}>
            {running ? "Running live demo..." : "Run Tool Failure Demo"}
          </button>
          <button className="secondary" onClick={runLowRetrievalDemo} disabled={running}>
            Run Low Retrieval Demo
          </button>
          <button className="secondary" onClick={loadMetrics} disabled={running}>
            Refresh Live Metrics
          </button>
        </div>

        <p className="hint">
          Demo simulates eval-gate failures → AutoOps stores hold/escalate incidents.
        </p>

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
          {breakdown.length === 0 && <p>No events yet. Run the demo.</p>}
          {breakdown.map((item) => (
            <div className="barRow" key={item.agent_decision}>
              <span>{item.agent_decision}</span>
              <div className="bar">
                <div style={{ width: `${Math.min(item.count * 8, 100)}%` }} />
              </div>
              <strong>{item.count}</strong>
            </div>
          ))}
        </div>
      </section>

      <section className="panel">
        <h2>Live Demo Result</h2>

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
              <p className="trace">
                Trace: classify → retrieve → analyze → plan → answer → eval
              </p>
            </div>

            <div className="eventBox">
              <h3>AutoOps Event Emitted</h3>
              <p><strong>source:</strong> {demoResult.autoops_event.source}</p>
              <p><strong>issue_type:</strong> {demoResult.autoops_event.issue_type}</p>
              <p><strong>decision:</strong> {demoResult.autoops_event.decision}</p>
              <p><strong>severity:</strong> {demoResult.autoops_event.severity}</p>
              <p><strong>stored id:</strong> {demoResult.autoops_response?.id ?? "sent"}</p>
            </div>
          </div>
        ) : (
          <p className="muted">Click a demo button to emit a live AutoOps event.</p>
        )}
      </section>

      <section className="panel">
        <h2>Why this matters</h2>
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
