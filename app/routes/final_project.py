"""
Роут: финальный проект (capstone).
"""
import json
from fastapi import APIRouter, HTTPException
from app.database import fetch_one

router = APIRouter()


@router.get("/{theme}")
def get_final_project(theme: str) -> dict:
    if theme not in ("space", "gaming"):
        raise HTTPException(404, "Theme must be 'space' or 'gaming'")
    fp = fetch_one(
        "SELECT * FROM final_projects WHERE theme = ?", (theme,)
    )
    if not fp:
        raise HTTPException(404, "Final project not found for this theme")
    # Парсим JSON-поля, если они строками
    for field in ("steps_json", "dataset_json", "characters_json"):
        val = fp.get(field)
        if isinstance(val, str):
            try:
                fp[field] = json.loads(val)
            except Exception:
                pass
    return fp
