
from fastapi import FastAPI
from pydantic import BaseModel

from src.log_analyzer import analyze_log

app = FastAPI(
    title="PipelinePilot AI",
    description="An API for analyzing CI/CD pipeline failures.",
    version="0.1.0",
)


class LogRequest(BaseModel):
    log_text: str


@app.get("/")
def health_check():
    return {
        "status": "running",
        "message": "PipelinePilot AI API is ready",
    }


@app.post("/analyze")
def analyze_pipeline_log(request: LogRequest):
    return analyze_log(request.log_text)
