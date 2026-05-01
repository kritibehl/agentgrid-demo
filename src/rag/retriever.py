from pathlib import Path
import re
from typing import List, Dict

DATA_PATHS = [
    Path("data/docs"),
    Path("data/logs"),
    Path("data/runbooks"),
]

def tokenize(text: str) -> set[str]:
    return set(re.findall(r"[a-zA-Z0-9_]+", text.lower()))

def load_chunks() -> List[Dict]:
    chunks = []

    for base_path in DATA_PATHS:
        if not base_path.exists():
            continue

        for file_path in sorted(base_path.glob("*.txt")):
            text = file_path.read_text()
            paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

            for idx, paragraph in enumerate(paragraphs):
                chunks.append({
                    "source": str(file_path),
                    "chunk_id": f"{file_path.name}:{idx}",
                    "content": paragraph,
                    "tokens": tokenize(paragraph),
                })

    return chunks

def retrieve(query: str, k: int = 3) -> List[Dict]:
    query_tokens = tokenize(query)
    chunks = load_chunks()

    scored = []
    for chunk in chunks:
        overlap = len(query_tokens.intersection(chunk["tokens"]))
        if overlap > 0:
            scored.append((overlap, chunk))

    scored.sort(key=lambda x: x[0], reverse=True)

    return [
        {
            "source": chunk["source"],
            "chunk_id": chunk["chunk_id"],
            "content": chunk["content"],
            "score": score,
        }
        for score, chunk in scored[:k]
    ]
