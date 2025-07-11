from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid, json, os

app = FastAPI()

# CORS для фронта (разрешить все, для MVP)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== ХЕЛПЕРЫ =====
def load_json(filename, fallback=[]):
    if not os.path.exists(filename):
        with open(filename, "w") as f: json.dump(fallback, f)
    with open(filename, "r") as f:
        try:
            return json.load(f)
        except Exception:
            return fallback

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ===== МОДЕЛИ =====
class Material(BaseModel):
    id: str = None
    title: str
    img: str
    text: str

class Story(BaseModel):
    id: str = None
    title: str
    img: str
    url: str

# ===== API МАТЕРИАЛОВ =====
MATERIALS_FILE = "materials.json"

@app.get("/api/materials")
def get_materials():
    return load_json(MATERIALS_FILE, [])

@app.post("/api/materials")
def add_material(mat: Material):
    mats = load_json(MATERIALS_FILE, [])
    mat.id = str(uuid.uuid4())
    mats.insert(0, mat.dict())
    save_json(MATERIALS_FILE, mats)
    return mat

@app.delete("/api/materials/{id}")
def del_material(id: str):
    mats = load_json(MATERIALS_FILE, [])
    mats2 = [m for m in mats if m["id"] != id]
    if len(mats2) == len(mats): raise HTTPException(status_code=404)
    save_json(MATERIALS_FILE, mats2)
    return {"ok": True}

# ===== API СТОРИС =====
STORIES_FILE = "stories.json"

@app.get("/api/stories")
def get_stories():
    return load_json(STORIES_FILE, [])

@app.post("/api/stories")
def add_story(story: Story):
    sts = load_json(STORIES_FILE, [])
    story.id = str(uuid.uuid4())
    sts.insert(0, story.dict())
    save_json(STORIES_FILE, sts)
    return story

@app.delete("/api/stories/{id}")
def del_story(id: str):
    sts = load_json(STORIES_FILE, [])
    sts2 = [s for s in sts if s["id"] != id]
    if len(sts2) == len(sts): raise HTTPException(status_code=404)
    save_json(STORIES_FILE, sts2)
    return {"ok": True}
