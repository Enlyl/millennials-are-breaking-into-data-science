"""
Роут: проекты.
"""
from fastapi import APIRouter
from app.database import fetch_one, fetch_all

router = APIRouter()


@router.get("/")
def list_projects() -> list[dict]:
    return fetch_all(
        """SELECT p.*, b.title AS block_title, b.number AS block_number
           FROM projects p
           LEFT JOIN blocks b ON p.block_id = b.id
           ORDER BY p.id"""
    )


@router.get("/{project_id}")
def get_project(project_id: int) -> dict:
    project = fetch_one(
        """SELECT p.*, b.title AS block_title
           FROM projects p
           LEFT JOIN blocks b ON p.block_id = b.id
           WHERE p.id = ?""",
        (project_id,),
    )
    if not project:
        from fastapi import HTTPException
        raise HTTPException(404, "Project not found")
    return project
