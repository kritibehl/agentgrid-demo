from __future__ import annotations

import argparse
import json
from pathlib import Path

from .graph import run_document


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the AgentGrid document triage workflow.")
    parser.add_argument("--file", required=True, help="Path to a text document.")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    text = path.read_text(encoding="utf-8")
    result = run_document(text)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
