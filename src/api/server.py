from fastapi import FastAPI
from src.agent.graph import run_agent

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/run")
def run(input: str):
    return run_agent(input)
