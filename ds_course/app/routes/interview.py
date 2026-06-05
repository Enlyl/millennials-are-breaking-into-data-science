"""
Роут: вопросы для собеседований.
"""
from fastapi import APIRouter
from app.database import fetch_all

router = APIRouter()


@router.get("/")
def list_questions(
    category: str | None = None,
    difficulty: str | None = None,
    is_top: bool | None = None,
    limit: int = 100,
) -> list[dict]:
    sql = "SELECT * FROM interview_questions WHERE 1=1"
    params = []
    if category:
        sql += " AND category = ?"
        params.append(category)
    if difficulty:
        sql += " AND difficulty = ?"
        params.append(difficulty)
    if is_top is not None:
        sql += " AND is_top = ?"
        params.append(1 if is_top else 0)
    sql += " ORDER BY is_top DESC, id LIMIT ?"
    params.append(limit)
    return fetch_all(sql, tuple(params))


@router.get("/categories")
def categories() -> list[dict]:
    rows = fetch_all(
        """SELECT category, COUNT(*) AS count
           FROM interview_questions
           GROUP BY category
           ORDER BY category"""
    )
    return rows
