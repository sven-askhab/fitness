from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from app.database import create_database
from app.routes import router

# создаём приложение
app = FastAPI()

# создаём базу данных при запуске
create_database()

# путь к статике
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

# подключаем API маршруты
app.include_router(router)

# раздача статических файлов (css, js)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# ---------- HTML страницы ----------

@app.get("/")
def index():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/login")
def login_page():
    return FileResponse(STATIC_DIR / "login.html")


@app.get("/register")
def register_page():
    return FileResponse(STATIC_DIR / "register.html")


@app.get("/workouts")
def workouts_page():
    return FileResponse(STATIC_DIR / "workouts.html")


@app.get("/workouts/{workout_id}")
def workout_detail_page(workout_id: int):
    return FileResponse(STATIC_DIR / "workout_detail.html")


@app.get("/stats")
def stats_page():
    return FileResponse(STATIC_DIR / "stats.html")
