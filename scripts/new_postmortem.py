from __future__ import annotations

import json
import re
import sys
from pathlib import Path

TEMPLATE = {
    "id": "",
    "company": "",
    "title": "",
    "date": "",
    "source_url": "",
    "summary": "",
    "failure_taxonomy": [],
    "system_layers": [],
    "detection_method": "",
    "detection_gap_minutes": 0,
    "recovery_pattern": [],
    "customer_impact": "",
    "root_cause": "",
    "what_would_have_caught_it_earlier": [],
    "atlas_lessons": "",
    "tags": []
}

def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")

def main() -> int:
    if len(sys.argv) < 4:
        print("Usage: python3 scripts/new_postmortem.py <company> <date:YYYY-MM-DD> <title>")
        return 1

    company = sys.argv[1].strip()
    date = sys.argv[2].strip()
    title = " ".join(sys.argv[3:]).strip()

    pm = dict(TEMPLATE)
    pm["company"] = company
    pm["date"] = date
    pm["title"] = title
    pm["id"] = f"{slugify(company)}-{date}"
    pm["tags"] = [slugify(company)]

    out = Path("atlas/data/postmortems") / f"{pm['id']}.json"
    out.write_text(json.dumps(pm, indent=2) + "\n", encoding="utf-8")
    print(f"Created {out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
