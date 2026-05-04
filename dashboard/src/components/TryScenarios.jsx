const scenarios = [
  {
    label: "Missing context → HOLD",
    query: "Why did the deployment fail if the logs are incomplete?",
    reason: "Missing retrieval context",
    autoops: "AutoOps Event: Sent"
  },
  {
    label: "Conflicting evidence → ESCALATE",
    query: "One runbook says rollback, another says retry. What should we do?",
    reason: "Evidence conflicts across sources",
    autoops: "AutoOps Event: Sent"
  },
  {
    label: "Tool failure → ESCALATE",
    query: "Analyze the incident but the log parser is unavailable.",
    reason: "Required support tool failed",
    autoops: "AutoOps Event: Sent"
  },
  {
    label: "Latency breach → HOLD",
    query: "The model answered but response latency breached the support budget.",
    reason: "Latency exceeded support threshold",
    autoops: "AutoOps Event: Sent"
  },
  {
    label: "Normal answer → SHIP",
    query: "Why did deployment fail due to a DB timeout retry storm?",
    reason: "Evidence-backed answer with supported action plan",
    autoops: "AutoOps Event: Not required"
  }
];

export default function TryScenarios({ onSelect }) {
  return (
    <section className="try-scenarios">
      <div className="try-scenarios-header">
        <p className="eyebrow">Try these scenarios</p>
        <h2>Live GenAI support gate</h2>
        <p>
          Each scenario shows when AgentGrid should answer, hold, or escalate into AutoOps.
        </p>
      </div>

      <div className="scenario-grid">
        {scenarios.map((scenario) => (
          <button
            key={scenario.label}
            type="button"
            onClick={() => onSelect?.(scenario.query)}
            className="scenario-card"
          >
            <strong>{scenario.label}</strong>
            <span>{scenario.reason}</span>
            <small>{scenario.autoops}</small>
          </button>
        ))}
      </div>

      <div className="live-status">
        <strong>Live System Status:</strong> 102 events ingested · 51 escalations · 10 holds · 0 unsafe shipments
      </div>
    </section>
  );
}
