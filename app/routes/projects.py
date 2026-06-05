"""
Роут: проекты.
"""
import json
from fastapi import APIRouter
from app.database import fetch_one, fetch_all

router = APIRouter()


@router.get("/")
def list_projects(include_datasets: bool = False) -> list[dict]:
    """Список проектов. По умолчанию БЕЗ dataset (быстрый ответ).
    Чтобы получить все данные (с dataset), передайте ?include_datasets=true.
    """
    if include_datasets:
        rows = fetch_all(
            """SELECT p.*, b.title AS block_title, b.number AS block_number
               FROM projects p
               LEFT JOIN blocks b ON p.block_id = b.id
               ORDER BY p.id"""
        )
        for r in rows:
            ds = r.get("dataset_json")
            if ds:
                try:
                    parsed = json.loads(ds) if isinstance(ds, str) else ds
                    r["dataset_summary"] = f"{len(parsed)} записей" if isinstance(parsed, list) else "объект"
                except Exception:
                    r["dataset_summary"] = "объект"
            else:
                r["dataset_summary"] = "—"
        return rows
    # Лёгкий вариант — без dataset_json (может быть 50-5000 записей)
    rows = fetch_all(
        """SELECT p.id, p.block_id, p.title, p.difficulty,
                  p.description, p.template_code, p.dataset_json,
                  b.title AS block_title, b.number AS block_number
           FROM projects p
           LEFT JOIN blocks b ON p.block_id = b.id
           ORDER BY p.id"""
    )
    for r in rows:
        ds = r.get("dataset_json")
        if ds:
            try:
                parsed = json.loads(ds) if isinstance(ds, str) else ds
                r["dataset_summary"] = f"{len(parsed)} записей" if isinstance(parsed, list) else "объект"
            except Exception:
                r["dataset_summary"] = "объект"
        else:
            r["dataset_summary"] = "—"
        r.pop("dataset_json", None)
    return rows


@router.get("/{project_id}")
def get_project(project_id: int, include_dataset: bool = True) -> dict:
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
    if not include_dataset and "dataset_json" in project:
        project["dataset_json"] = None
    return project
