from __future__ import annotations

import json
from pathlib import Path
import sys

REQUIRED_KEYS = {
    "id",
    "company",
    "title",
    "date",
    "source_url",
    "summary",
    "failure_taxonomy",
    "system_layers",
    "detection_method",
    "detection_gap_minutes",
    "recovery_pattern",
    "customer_impact",
    "root_cause",
    "what_would_have_caught_it_earlier",
    "atlas_lessons",
    "tags",
}

def main() -> int:
    root = Path("atlas/data/postmortems")
    files = sorted(root.glob("*.json"))
    if not files:
        print("No postmortem files found.")
        return 1

    seen_ids = set()
    ok = True

    for path in files:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"[FAIL] {path}: invalid JSON: {exc}")
            ok = False
            continue

        missing = REQUIRED_KEYS - set(data.keys())
        if missing:
            print(f"[FAIL] {path}: missing keys: {sorted(missing)}")
            ok = False

        pm_id = data.get("id")
        if pm_id in seen_ids:
            print(f"[FAIL] {path}: duplicate id: {pm_id}")
            ok = False
        seen_ids.add(pm_id)

        if not isinstance(data.get("failure_taxonomy"), list):
            print(f"[FAIL] {path}: failure_taxonomy must be a list")
            ok = False
        if not isinstance(data.get("system_layers"), list):
            print(f"[FAIL] {path}: system_layers must be a list")
            ok = False
        if not isinstance(data.get("recovery_pattern"), list):
            print(f"[FAIL] {path}: recovery_pattern must be a list")
            ok = False
        if not isinstance(data.get("tags"), list):
            print(f"[FAIL] {path}: tags must be a list")
            ok = False

        print(f"[OK] {path.name}")

    return 0 if ok else 2

if __name__ == "__main__":
    raise SystemExit(main())
