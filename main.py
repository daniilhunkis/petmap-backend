from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Пример заглушки на корень
@app.get("/")
def root():
    return {"status": "Backend works!"}

# Пример модели для обратной связи
class Feedback(BaseModel):
    name: str
    message: str

# Пример хранения сообщений (in-memory)
feedback_list: List[Feedback] = []

@app.post("/feedback")
def send_feedback(feedback: Feedback):
    feedback_list.append(feedback)
    return {"success": True, "msg": "Спасибо за обратную связь!"}

@app.get("/feedback")
def get_feedback():
    return feedback_list

# Пример эндпоинта для метрик
class Metric(BaseModel):
    event: str
    info: dict

metrics: List[Metric] = []

@app.post("/metrics")
def collect_metric(metric: Metric):
    metrics.append(metric)
    return {"success": True}

@app.get("/metrics")
def get_metrics():
    return metrics

# Можно добавить другие роуты по аналогии
