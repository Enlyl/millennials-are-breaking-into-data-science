"""
Роут: уроки — список, по id, по номеру, упражнения.
"""
from fastapi import APIRouter, HTTPException
from app.database import fetch_one, fetch_all

router = APIRouter()


@router.get("/blocks")
def list_blocks() -> list[dict]:
    return fetch_all("SELECT * FROM blocks ORDER BY number")


@router.get("/block/{number}")
def get_block(number: int) -> dict:
    block = fetch_one("SELECT * FROM blocks WHERE number = ?", (number,))
    if not block:
        raise HTTPException(404, "Block not found")
    lessons = fetch_all(
        "SELECT id, number, title, difficulty, estimated_minutes FROM lessons WHERE block_id = ? ORDER BY order_idx",
        (block["id"],),
    )
    block["lessons"] = lessons
    return block


@router.get("/")
def list_lessons(block_id: int | None = None) -> list[dict]:
    if block_id is not None:
        return fetch_all(
            "SELECT id, number, title, difficulty, estimated_minutes FROM lessons WHERE block_id = ? ORDER BY order_idx",
            (block_id,),
        )
    return fetch_all(
        "SELECT id, block_id, number, title, difficulty, estimated_minutes FROM lessons ORDER BY block_id, order_idx"
    )


@router.get("/{number}")
def get_lesson(number: str) -> dict:
    lesson = fetch_one(
        "SELECT * FROM lessons WHERE number = ?",
        (number,),
    )
    if not lesson:
        raise HTTPException(404, "Lesson not found")
    block = fetch_one("SELECT number, title, theme FROM blocks WHERE id = ?", (lesson["block_id"],))
    lesson["block"] = block
    exercises = fetch_all(
        """SELECT id, number, type, prompt, starter_code, solution_code,
                  test_cases_json, hints_json, difficulty, expected_result_json
           FROM exercises WHERE lesson_id = ? ORDER BY number""",
        (lesson["id"],),
    )
    lesson["exercises"] = exercises
    return lesson


@router.get("/{number}/solution/{exercise_number}")
def get_solution(number: str, exercise_number: int) -> dict:
    lesson = fetch_one("SELECT id FROM lessons WHERE number = ?", (number,))
    if not lesson:
        raise HTTPException(404, "Lesson not found")
    ex = fetch_one(
        "SELECT solution_code FROM exercises WHERE lesson_id = ? AND number = ?",
        (lesson["id"], exercise_number),
    )
    if not ex:
        raise HTTPException(404, "Exercise not found")
    return {"solution": ex["solution_code"]}
