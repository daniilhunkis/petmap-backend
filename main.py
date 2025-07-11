from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import datetime

app = FastAPI()

# Настрой CORS: укажи адрес твоего фронта для безопасности, либо ["*"] для теста
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://petmap-gray.vercel.app", "https://petmap-l1hxfum9p-daniils-projects-89f4bca3.vercel.app", "https://petmap.vercel.app", "*"],  # все адреса фронтов, которые используешь
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модели для запросов
class Metric(BaseModel):
    event: str
    time: str
    section: str = None  # если нужен раздел (или что-то ещё)
    # можно добавить другие поля при необходимости

class Feedback(BaseModel):
    name: str
    contact: str
    message: str
    time: str

@app.get("/")
def root():
    return {"status": "ok", "msg": "PetMap backend работает!"}

@app.post("/metrics")
async def metrics_endpoint(metric: Metric, request: Request):
    # Пример логирования, потом можно будет сохранять в БД
    print("METRIC:", metric.dict())
    return JSONResponse({"status": "ok"})

@app.post("/feedback")
async def feedback_endpoint(feedback: Feedback, request: Request):
    # Пример логирования, потом можно будет сохранять в БД
    print("FEEDBACK:", feedback.dict())
    return JSONResponse({"status": "ok"})
