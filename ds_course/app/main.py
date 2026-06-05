"""
FastAPI application: инициализация + подключение роутов.
"""
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.routes import lessons, progress, projects, interview, achievements

ROOT = Path(__file__).parent.parent.resolve()
FRONTEND = ROOT / "frontend"

app = FastAPI(title="Data Science Course", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def _startup() -> None:
    init_db()


# Роуты API
app.include_router(lessons.router, prefix="/api/lessons", tags=["lessons"])
app.include_router(progress.router, prefix="/api/progress", tags=["progress"])
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
app.include_router(interview.router, prefix="/api/interview", tags=["interview"])
app.include_router(achievements.router, prefix="/api/achievements", tags=["achievements"])


# Health
@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


# Статика
app.mount("/static", StaticFiles(directory=str(FRONTEND)), name="static")
app.mount("/vendor", StaticFiles(directory=str(FRONTEND / "vendor")), name="vendor")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(str(FRONTEND / "index.html"))


@app.get("/favicon.ico")
def favicon() -> FileResponse:
    fav = FRONTEND / "favicon.ico"
    if fav.exists():
        return FileResponse(str(fav))
    return FileResponse(str(FRONTEND / "index.html"))
