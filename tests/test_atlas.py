from pathlib import Path
import json

def test_postmortem_files_exist() -> None:
    files = sorted(Path("atlas/data/postmortems").glob("*.json"))
    assert len(files) >= 3

def test_postmortem_schema_fields_present() -> None:
    path = sorted(Path("atlas/data/postmortems").glob("*.json"))[0]
    data = json.loads(path.read_text(encoding="utf-8"))
    assert "id" in data
    assert "company" in data
    assert "failure_taxonomy" in data
    assert "atlas_lessons" in data
