"""
SQLite database: schema, connection helpers, and initialization.
"""
import sqlite3
import json
import threading
from pathlib import Path
from contextlib import contextmanager

ROOT = Path(__file__).parent.parent.resolve()
DB_PATH = ROOT / "course.db"

_lock = threading.Lock()


SCHEMA = """
CREATE TABLE IF NOT EXISTS blocks (
    id INTEGER PRIMARY KEY,
    number INTEGER NOT NULL UNIQUE,
    title TEXT NOT NULL,
    description TEXT,
    theme TEXT CHECK(theme IN ('space', 'gaming', 'mixed', 'neutral'))
);

CREATE TABLE IF NOT EXISTS lessons (
    id INTEGER PRIMARY KEY,
    block_id INTEGER REFERENCES blocks(id),
    number TEXT NOT NULL,
    title TEXT NOT NULL,
    content_json TEXT NOT NULL,
    difficulty INTEGER CHECK(difficulty BETWEEN 1 AND 5),
    estimated_minutes INTEGER,
    order_idx INTEGER DEFAULT 0,
    UNIQUE(block_id, number)
);

CREATE TABLE IF NOT EXISTS exercises (
    id INTEGER PRIMARY KEY,
    lesson_id INTEGER REFERENCES lessons(id),
    number INTEGER NOT NULL,
    type TEXT CHECK(type IN ('python', 'sql', 'quiz', 'theory')),
    prompt TEXT NOT NULL,
    starter_code TEXT,
    solution_code TEXT NOT NULL,
    test_cases_json TEXT,
    hints_json TEXT,
    difficulty INTEGER CHECK(difficulty BETWEEN 1 AND 5),
    expected_result_json TEXT
);

CREATE TABLE IF NOT EXISTS user_progress (
    id INTEGER PRIMARY KEY,
    lesson_id INTEGER REFERENCES lessons(id) UNIQUE,
    completed BOOLEAN DEFAULT FALSE,
    score INTEGER DEFAULT 0,
    attempts INTEGER DEFAULT 0,
    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS exercise_attempts (
    id INTEGER PRIMARY KEY,
    exercise_id INTEGER REFERENCES exercises(id),
    user_code TEXT,
    passed BOOLEAN,
    score INTEGER,
    attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY,
    block_id INTEGER REFERENCES blocks(id),
    title TEXT NOT NULL,
    description TEXT,
    theme TEXT CHECK(theme IN ('space', 'gaming', 'mixed', 'neutral')),
    difficulty INTEGER,
    template_code TEXT,
    solution_code TEXT,
    dataset_json TEXT
);

CREATE TABLE IF NOT EXISTS interview_questions (
    id INTEGER PRIMARY KEY,
    category TEXT CHECK(category IN ('python', 'sql', 'statistics', 'ml', 'ds_general')),
    difficulty TEXT CHECK(difficulty IN ('junior', 'middle')),
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    explanation TEXT,
    common_mistakes TEXT,
    tags_json TEXT,
    is_top INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS achievements (
    id INTEGER PRIMARY KEY,
    key TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    icon TEXT,
    condition_json TEXT
);

CREATE TABLE IF NOT EXISTS user_achievements (
    id INTEGER PRIMARY KEY,
    achievement_id INTEGER REFERENCES achievements(id) UNIQUE,
    earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS final_projects (
    id INTEGER PRIMARY KEY,
    theme TEXT NOT NULL CHECK(theme IN ('space', 'gaming')),
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    steps_json TEXT NOT NULL,
    dataset_json TEXT NOT NULL,
    template_code TEXT NOT NULL,
    solution_code TEXT NOT NULL,
    characters_json TEXT NOT NULL DEFAULT '[]'
);
"""


@contextmanager
def get_conn():
    conn = sqlite3.connect(str(DB_PATH), timeout=10.0, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    """Создаёт схему и заполняет контентом при первом запуске."""
    DB_PATH.touch()
    with _lock, get_conn() as conn:
        conn.executescript(SCHEMA)
    _seed_if_empty()
    # Всегда перезаливаем капстоны (могли измениться шаги/персонажи)
    from app.seed_data import reseed_final_projects
    with get_conn() as conn:
        reseed_final_projects(conn)


def _seed_if_empty() -> None:
    from app.seed_data import seed_all
    with get_conn() as conn:
        cur = conn.execute("SELECT COUNT(*) AS c FROM blocks")
        if cur.fetchone()["c"] == 0:
            seed_all(conn)


def row_to_dict(row) -> dict:
    if row is None:
        return None
    d = dict(row)
    for k, v in d.items():
        if isinstance(v, str) and v.startswith(("{", "[")):
            try:
                d[k] = json.loads(v)
            except Exception:
                pass
    return d


def fetch_one(sql: str, params=()) -> dict | None:
    with get_conn() as conn:
        cur = conn.execute(sql, params)
        row = cur.fetchone()
        return row_to_dict(row) if row else None


def fetch_all(sql: str, params=()) -> list[dict]:
    with get_conn() as conn:
        cur = conn.execute(sql, params)
        return [row_to_dict(r) for r in cur.fetchall()]


def execute(sql: str, params=()) -> int:
    with _lock, get_conn() as conn:
        cur = conn.execute(sql, params)
        return cur.lastrowid
