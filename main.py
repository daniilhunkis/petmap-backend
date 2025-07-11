from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import csv
import io

app = FastAPI()

# CORS для фронта на Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://petmap-gray.vercel.app", "https://petmap-l1hxfum9p-daniils-projects-89f4bca3.vercel.app", "https://petmap.vercel.app", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модели
class Metric(BaseModel):
    event: str
    time: str
    section: str = None

class Feedback(BaseModel):
    name: str
    contact: str
    message: str
    time: str

class Story(BaseModel):
    id: int
    title: str
    content: str
    time: str

# Хранилища
metrics_store: List[dict] = []
feedback_store: List[dict] = []
stories_store: List[dict] = []

@app.get("/")
def root():
    return {"status": "ok", "msg": "PetMap backend работает!"}

# Метрики
@app.post("/metrics")
async def metrics_endpoint(metric: Metric):
    metrics_store.append(metric.dict())
    return {"status": "ok"}

@app.get("/metrics")
def get_metrics():
    return metrics_store[-100:]  # последние 100

@app.get("/metrics_csv")
def get_metrics_csv():
    si = io.StringIO()
    writer = csv.DictWriter(si, fieldnames=["event", "time", "section"])
    writer.writeheader()
    for m in metrics_store[-100:]:
        writer.writerow(m)
    output = si.getvalue()
    return JSONResponse(content={"csv": output})

# Обратная связь
@app.post("/feedback")
async def feedback_endpoint(feedback: Feedback):
    feedback_store.append(feedback.dict())
    return {"status": "ok"}

@app.get("/feedback")
def get_feedback():
    return feedback_store[-100:]

@app.get("/feedback_csv")
def get_feedback_csv():
    si = io.StringIO()
    writer = csv.DictWriter(si, fieldnames=["name", "contact", "message", "time"])
    writer.writeheader()
    for f in feedback_store[-100:]:
        writer.writerow(f)
    output = si.getvalue()
    return JSONResponse(content={"csv": output})

# Stories
@app.get("/stories")
def get_stories():
    return stories_store

@app.post("/stories")
async def add_story(story: Story):
    story.id = len(stories_store) + 1
    stories_store.append(story.dict())
    return {"status": "ok"}

@app.delete("/stories/{story_id}")
def delete_story(story_id: int):
    global stories_store
    stories_store = [s for s in stories_store if s["id"] != story_id]
    return {"status": "deleted"}

# Краткая аналитика
@app.get("/admin_stats")
def admin_stats():
    return {
        "metrics": len(metrics_store),
        "feedback": len(feedback_store),
        "stories": len(stories_store),
    }
