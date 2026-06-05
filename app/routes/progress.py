"""
Роут: прогресс пользователя.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from app.database import fetch_one, fetch_all, execute

router = APIRouter()


class ProgressUpdate(BaseModel):
    lesson_id: int
    completed: bool = False
    score: int = 0
    notes: str | None = None


class AttemptLog(BaseModel):
    exercise_id: int
    user_code: str
    passed: bool
    score: int = 0


@router.get("/")
def get_progress() -> list[dict]:
    return fetch_all(
        """SELECT p.*, l.title, l.number
           FROM user_progress p
           JOIN lessons l ON p.lesson_id = l.id
           ORDER BY p.last_accessed DESC"""
    )


@router.get("/summary")
def summary() -> dict:
    total = fetch_one("SELECT COUNT(*) AS c FROM lessons")
    done = fetch_one("SELECT COUNT(*) AS c FROM user_progress WHERE completed = 1")
    total_ex = fetch_one("SELECT COUNT(*) AS c FROM exercises")
    solved = fetch_one("SELECT COUNT(*) AS c FROM exercise_attempts WHERE passed = 1")
    return {
        "lessons_total": total["c"] if total else 0,
        "lessons_done": done["c"] if done else 0,
        "exercises_total": total_ex["c"] if total_ex else 0,
        "exercises_solved": solved["c"] if solved else 0,
    }


@router.post("/update")
def update_progress(update: ProgressUpdate) -> dict:
    existing = fetch_one("SELECT id, attempts FROM user_progress WHERE lesson_id = ?", (update.lesson_id,))
    if existing:
        execute(
            """UPDATE user_progress
               SET completed = ?, score = ?, notes = ?,
                   last_accessed = CURRENT_TIMESTAMP, attempts = attempts + 1
               WHERE lesson_id = ?""",
            (update.completed, update.score, update.notes, update.lesson_id),
        )
        return {"status": "updated", "id": existing["id"]}
    new_id = execute(
        """INSERT INTO user_progress (lesson_id, completed, score, notes, last_accessed, attempts)
           VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, 1)""",
        (update.lesson_id, update.completed, update.score, update.notes),
    )
    return {"status": "created", "id": new_id}


@router.post("/attempt")
def log_attempt(attempt: AttemptLog) -> dict:
    new_id = execute(
        """INSERT INTO exercise_attempts (exercise_id, user_code, passed, score)
           VALUES (?, ?, ?, ?)""",
        (attempt.exercise_id, attempt.user_code, attempt.passed, attempt.score),
    )
    return {"status": "logged", "id": new_id, "passed": attempt.passed}


@router.post("/reset")
def reset_progress() -> dict:
    execute("DELETE FROM user_progress")
    execute("DELETE FROM exercise_attempts")
    execute("DELETE FROM user_achievements")
    return {"status": "reset"}
