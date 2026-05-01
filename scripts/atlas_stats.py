from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

POSTMORTEM_DIR = Path("atlas/data/postmortems")

def main() -> int:
    items = []
    for path in sorted(POSTMORTEM_DIR.glob("*.json")):
        items.append(json.loads(path.read_text(encoding="utf-8")))

    failure_counter = Counter()
    layer_counter = Counter()
    detection_counter = Counter()
    recovery_counter = Counter()
    company_counter = Counter()

    for item in items:
        company_counter[item.get("company", "")] += 1
        detection_counter[item.get("detection_method", "")] += 1
        for x in item.get("failure_taxonomy", []):
            failure_counter[x] += 1
        for x in item.get("system_layers", []):
            layer_counter[x] += 1
        for x in item.get("recovery_pattern", []):
            recovery_counter[x] += 1

    print("=== Postmortem Atlas Stats ===")
    print(f"Total postmortems: {len(items)}")
    print(f"Companies covered: {len([k for k in company_counter if k])}")
    print(f"Top failure types: {failure_counter.most_common(10)}")
    print(f"Top system layers: {layer_counter.most_common(10)}")
    print(f"Detection methods: {detection_counter.most_common(10)}")
    print(f"Recovery patterns: {recovery_counter.most_common(10)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
