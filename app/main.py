"""
FastAPI application: инициализация + подключение роутов + статика с кешированием.
"""
import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.database import init_db
from app.routes import lessons, progress, projects, interview, achievements, final_project

ROOT = Path(__file__).parent.parent.resolve()
FRONTEND = ROOT / "frontend"

app = FastAPI(title="Data Science Course", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=512)


@app.on_event("startup")
def _startup() -> None:
    init_db()


# Роуты API
app.include_router(lessons.router, prefix="/api/lessons", tags=["lessons"])
app.include_router(progress.router, prefix="/api/progress", tags=["progress"])
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
app.include_router(interview.router, prefix="/api/interview", tags=["interview"])
app.include_router(achievements.router, prefix="/api/achievements", tags=["achievements"])
app.include_router(final_project.router, prefix="/api/final-project", tags=["final_project"])


# Health
@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


# ============================================================================
# Статика с долгим кешированием для vendor (Pyodide/sql.js wheels)
# ============================================================================
class CachedStaticFiles(StaticFiles):
    """StaticFiles с агрессивным кешированием. .whl/.wasm/.zip/.asm.js
    получают Cache-Control: max-age=31536000 (1 год)."""

    async def get_response(self, path: str, scope: dict) -> Response:
        response = await super().get_response(path, scope)
        if response.status_code == 200:
            # Только для бинарных вендор-файлов
            if any(path.endswith(ext) for ext in (".whl", ".wasm", ".zip", ".asm.js")):
                response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
        return response


class ShortCachedStaticFiles(StaticFiles):
    """HTML/JS/CSS — короткий кеш (5 минут)."""

    async def get_response(self, path: str, scope: dict) -> Response:
        response = await super().get_response(path, scope)
        if response.status_code == 200:
            if any(path.endswith(ext) for ext in (".html", ".js", ".css", ".json")):
                response.headers["Cache-Control"] = "public, max-age=300"
        return response


# Вендор (Pyodide + sql.js) — кешируется 1 год
app.mount("/vendor", CachedStaticFiles(directory=str(FRONTEND / "vendor")), name="vendor")
# index.html / css / js — кешируются 5 минут
app.mount("/static", ShortCachedStaticFiles(directory=str(FRONTEND)), name="static")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(str(FRONTEND / "index.html"))


@app.get("/favicon.ico")
def favicon() -> FileResponse:
    fav = FRONTEND / "favicon.ico"
    if fav.exists():
        return FileResponse(str(fav))
    return FileResponse(str(FRONTEND / "index.html"))
