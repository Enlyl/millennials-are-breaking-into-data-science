"""
Роут: достижения.
"""
from fastapi import APIRouter
from app.database import fetch_all, fetch_one, execute

router = APIRouter()


@router.get("/")
def list_achievements() -> list[dict]:
    all_ach = fetch_all("SELECT * FROM achievements ORDER BY id")
    earned = {r["achievement_id"] for r in fetch_all("SELECT achievement_id FROM user_achievements")}
    for a in all_ach:
        a["earned"] = a["id"] in earned
    return all_ach


@router.post("/earn/{key}")
def earn_achievement(key: str) -> dict:
    ach = fetch_one("SELECT id FROM achievements WHERE key = ?", (key,))
    if not ach:
        return {"status": "not_found"}
    existing = fetch_one("SELECT id FROM user_achievements WHERE achievement_id = ?", (ach["id"],))
    if existing:
        return {"status": "already_earned"}
    execute("INSERT INTO user_achievements (achievement_id) VALUES (?)", (ach["id"],))
    return {"status": "earned", "key": key}
