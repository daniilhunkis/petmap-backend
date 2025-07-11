import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, String, Text
import uuid

# ---- Конфигурируем БД ----
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://petmap_db_user:RXvPXSxncNoogTd8lkJsNUzHO38dlvgn@dpg-d1ojk92dbo4c73b5bba0-a:5432/petmap_db")
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# ---- Модели ----
class MaterialDB(Base):
    __tablename__ = "materials"
    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    img = Column(String, nullable=False)
    text = Column(Text, nullable=False)

class StoryDB(Base):
    __tablename__ = "stories"
    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    img = Column(String, nullable=False)
    url = Column(String, nullable=False)

class Material(BaseModel):
    id: str = ""
    title: str
    img: str
    text: str

class Story(BaseModel):
    id: str = ""
    title: str
    img: str
    url: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Инициализация базы ----
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# ---- Эндпоинты ----
@app.get("/api/materials")
async def get_materials():
    async with SessionLocal() as session:
        mats = await session.execute(
            MaterialDB.__table__.select().order_by(MaterialDB.id.desc())
        )
        return [Material(**dict(m)) for m in mats.fetchall()]

@app.post("/api/materials")
async def add_material(mat: Material):
    mat.id = str(uuid.uuid4())
    async with SessionLocal() as session:
        dbmat = MaterialDB(**mat.dict())
        session.add(dbmat)
        await session.commit()
        return mat

@app.delete("/api/materials/{mid}")
async def del_material(mid: str):
    async with SessionLocal() as session:
        await session.execute(MaterialDB.__table__.delete().where(MaterialDB.id == mid))
        await session.commit()
        return {"ok": True}

@app.get("/api/stories")
async def get_stories():
    async with SessionLocal() as session:
        sts = await session.execute(
            StoryDB.__table__.select().order_by(StoryDB.id.desc())
        )
        return [Story(**dict(s)) for s in sts.fetchall()]

@app.post("/api/stories")
async def add_story(story: Story):
    story.id = str(uuid.uuid4())
    async with SessionLocal() as session:
        dbstory = StoryDB(**story.dict())
        session.add(dbstory)
        await session.commit()
        return story

@app.delete("/api/stories/{sid}")
async def del_story(sid: str):
    async with SessionLocal() as session:
        await session.execute(StoryDB.__table__.delete().where(StoryDB.id == sid))
        await session.commit()
        return {"ok": True}

@app.get("/")
async def index():
    return {"ok": True}
