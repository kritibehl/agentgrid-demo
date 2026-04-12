const POSTMORTEMS = [
  {
    "id": "cloudflare-2020-07-17",
    "company": "Cloudflare",
    "title": "Global outage triggered by router configuration deployment",
    "date": "2020-07-17",
    "source_url": "PASTE_PUBLIC_POSTMORTEM_URL_HERE",
    "summary": "A broad service outage caused by a bad network/router configuration rollout.",
    "failure_taxonomy": [
      "config_change",
      "network_partition",
      "deploy_regression"
    ],
    "system_layers": [
      "network",
      "edge",
      "control_plane"
    ],
    "detection_method": "internal_alert",
    "detection_gap_minutes": 3,
    "recovery_pattern": [
      "rollback",
      "manual_mitigation"
    ],
    "customer_impact": "Broad availability degradation across multiple services.",
    "root_cause": "Configuration deployment introduced invalid routing behavior.",
    "what_would_have_caught_it_earlier": [
      "staged rollout with blast-radius guardrails",
      "control-plane config validation",
      "network path canary checks"
    ],
    "atlas_lessons": "A KubePulse-style topology validation layer would have caught path health degradation before broad rollout. A Faultline-style gated change path could have limited propagation of unsafe config state.",
    "tags": [
      "network",
      "routing",
      "rollback",
      "canary"
    ]
  },
  {
    "id": "github-actions-2023-01-30",
    "company": "GitHub",
    "title": "Actions incident affecting workflow execution",
    "date": "2023-01-30",
    "source_url": "PASTE_PUBLIC_POSTMORTEM_URL_HERE",
    "summary": "Workflow execution and related developer automation were degraded.",
    "failure_taxonomy": [
      "dependency_outage",
      "control_plane_failure",
      "cascading_timeout"
    ],
    "system_layers": [
      "application",
      "control_plane",
      "database"
    ],
    "detection_method": "internal_alert",
    "detection_gap_minutes": 8,
    "recovery_pattern": [
      "restart",
      "manual_mitigation",
      "traffic_shift"
    ],
    "customer_impact": "Delayed or failed CI workflow execution.",
    "root_cause": "Control-plane instability propagated into job orchestration failures.",
    "what_would_have_caught_it_earlier": [
      "queue-depth anomaly alerts",
      "control-plane health invariants",
      "dependency timeout-chain tracing"
    ],
    "atlas_lessons": "This maps directly to reliability validation. DetTrace-style causal reconstruction would help isolate where queueing drift became operator-visible. AutoOps-style failure categorization could surface recurrence patterns faster.",
    "tags": [
      "ci",
      "control-plane",
      "workflow",
      "timeout"
    ]
  },
  {
    "id": "stripe-api-incident-example",
    "company": "Stripe",
    "title": "API availability degradation example",
    "date": "2022-01-01",
    "source_url": "PASTE_PUBLIC_POSTMORTEM_URL_HERE",
    "summary": "Template entry. Replace with a real public Stripe postmortem.",
    "failure_taxonomy": [
      "dependency_outage"
    ],
    "system_layers": [
      "application",
      "database"
    ],
    "detection_method": "customer_report",
    "detection_gap_minutes": 15,
    "recovery_pattern": [
      "manual_mitigation"
    ],
    "customer_impact": "Template entry.",
    "root_cause": "Template entry.",
    "what_would_have_caught_it_earlier": [
      "synthetic checks"
    ],
    "atlas_lessons": "Replace with a real lesson tied to your validation framework.",
    "tags": [
      "template"
    ]
  }
];