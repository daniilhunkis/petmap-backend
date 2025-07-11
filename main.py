import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Настройки базы
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Модели
class Material(Base):
    __tablename__ = "materials"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    img = Column(String)
    text = Column(Text)

class Story(Base):
    __tablename__ = "stories"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    img = Column(String)
    url = Column(String)

# Создаём таблицы при первом запуске
Base.metadata.create_all(bind=engine)

# Pydantic-схемы
class MaterialIn(BaseModel):
    title: str
    img: str
    text: str

class StoryIn(BaseModel):
    title: str
    img: str
    url: str

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Можно ограничить ["https://petmap-gray.vercel.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Эндпоинты
@app.get("/api/materials")
def get_materials():
    db = SessionLocal()
    mats = db.query(Material).all()
    return [{"id": m.id, "title": m.title, "img": m.img, "text": m.text} for m in mats]

@app.post("/api/materials")
def add_material(mat: MaterialIn):
    db = SessionLocal()
    new_mat = Material(**mat.dict())
    db.add(new_mat)
    db.commit()
    db.refresh(new_mat)
    return {"id": new_mat.id, "title": new_mat.title, "img": new_mat.img, "text": new_mat.text}

@app.delete("/api/materials/{mat_id}")
def del_material(mat_id: int):
    db = SessionLocal()
    mat = db.query(Material).get(mat_id)
    if not mat:
        raise HTTPException(status_code=404)
    db.delete(mat)
    db.commit()
    return {"ok": True}

@app.get("/api/stories")
def get_stories():
    db = SessionLocal()
    st = db.query(Story).all()
    return [{"id": s.id, "title": s.title, "img": s.img, "url": s.url} for s in st]

@app.post("/api/stories")
def add_story(st: StoryIn):
    db = SessionLocal()
    new_st = Story(**st.dict())
    db.add(new_st)
    db.commit()
    db.refresh(new_st)
    return {"id": new_st.id, "title": new_st.title, "img": new_st.img, "url": new_st.url}

@app.delete("/api/stories/{story_id}")
def del_story(story_id: int):
    db = SessionLocal()
    st = db.query(Story).get(story_id)
    if not st:
        raise HTTPException(status_code=404)
    db.delete(st)
    db.commit()
    return {"ok": True}
