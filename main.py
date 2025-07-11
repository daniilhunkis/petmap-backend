from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from fastapi.responses import FileResponse
import os

app = FastAPI()

# Разрешаем доступ с фронта
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Для разработки можно *, на проде — только свой домен
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Metric(BaseModel):
    event: str
    time: str
    section: Optional[str] = None
    title: Optional[str] = None

class Feedback(BaseModel):
    name: str
    contact: str
    message: str
    time: str

metrics_db: List[Metric] = []
feedback_db: List[Feedback] = []

@app.post("/api/metrics")
async def save_metric(metric: Metric):
    metrics_db.append(metric)
    return {"status": "ok"}

@app.post("/api/feedback")
async def save_feedback(feedback: Feedback):
    feedback_db.append(feedback)
    return {"status": "ok"}

@app.get("/api/metrics")
async def get_metrics():
    return metrics_db

@app.get("/api/feedbacks")
async def get_feedbacks():
    return feedback_db

@app.get("/admin")
async def admin_panel():
    path = os.path.join(os.path.dirname(__file__), "admin.html")
    return FileResponse(path)
