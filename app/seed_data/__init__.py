"""
Пакет seed-данных: orchestrator.
Импортирует уроки всех блоков из модулей, содержит метаданные, проекты,
достижения, вопросы.
"""
import json
from app.seed_helpers import ex, lesson, theory, analogy, example
from app.seed_block1_part1 import LESSONS as B1_P1
from app.seed_block1_part2 import LESSONS as B1_P2
from app.seed_block1_part3 import LESSONS as B1_P3
from app.seed_block2_part1 import LESSONS as B2_P1
from app.seed_block2_part2 import LESSONS as B2_P2
from app.seed_block3 import LESSONS as B3
from app.seed_block4 import LESSONS as B4
from app.seed_block5 import LESSONS as B5
from app.seed_block6 import LESSONS as B6
from app.seed_block7 import LESSONS as B7
from app.seed_block8 import LESSONS as B8
from app.seed_block9 import LESSONS as B9
from app.seed_block10 import LESSONS as B10
from app.seed_meta import (
    BLOCKS_META,
    PROJECTS,
    ACHIEVEMENTS,
    INTERVIEW_QUESTIONS,
)
from app.seed_capstone import FINAL_PROJECTS
from app.seed_sql_extra import EXTRA_EXERCISES

# Блоки с реальным контентом (1-10).
REAL_BLOCKS = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}


def _stub_lesson(block_num: int, lesson_num: str, title: str) -> dict:
    """Заглушка урока для блоков 3-10 (без полного контента)."""
    return lesson(
        lesson_num, title, "mixed", [
            theory(f"Урок '{title}' появится в следующих обновлениях. "
                   f"Это часть Блока {block_num}. Содержимое в разработке."),
            analogy("Этот блок пока в режиме preview.", "Контент готовится."),
            example(
                "Демонстрационное упражнение-заглушка.",
                "Выведи сообщение, что урок готовится.",
                "print(f'Урок {title} скоро появится!')",
                "Урок ... скоро появится!",
                "Простой print для демонстрации."
            ),
        ],
        exercises=[
            ex(1, "python",
               f"Демо-задание для урока '{title}'. Выведи строку 'OK'.",
               "# Выведи 'OK'\n",
               "print('OK')",
               [{"check": "'OK' in _printed_output", "msg": "Должно быть выведено 'OK'"}],
               ["print()"], 1),
        ],
        minutes=20, difficulty=1,
    )


def _stub_block_lessons(block_num: int, titles: list) -> list:
    """Генерирует список заглушек уроков для блока."""
    return [_stub_lesson(block_num, f"{block_num}.{i+1}", t)
            for i, t in enumerate(titles)]


def _all_lessons() -> list:
    lessons = []
    for src in [B1_P1, B1_P2, B1_P3, B2_P1, B2_P2, B3, B4, B5, B6, B7, B8, B9, B10]:
        for fn in src:
            lessons.append(fn())
    # Заглушки оставшихся блоков (если такие есть в BLOCKS_META)
    for block in BLOCKS_META:
        bn = block["number"]
        if bn in REAL_BLOCKS:
            continue
        if block["lessons_meta"]:
            lessons.extend(_stub_block_lessons(bn, block["lessons_meta"]))
    # Добавляем дополнительные упражнения для уроков SQL (блок 2)
    for lesson_data in lessons:
        ln = lesson_data["number"]
        extra = EXTRA_EXERCISES.get(ln)
        if extra:
            lesson_data["exercises"].extend(extra)
    return lessons


def _seed_blocks(conn) -> None:
    conn.execute("DELETE FROM blocks")
    for b in BLOCKS_META:
        conn.execute(
            "INSERT INTO blocks (number, title, description, theme) VALUES (?, ?, ?, ?)",
            (b["number"], b["title"], b["description"], b["theme"]),
        )


def _seed_lessons(conn) -> None:
    conn.execute("DELETE FROM lessons")
    for lesson_data in _all_lessons():
        cur = conn.execute("SELECT id FROM blocks WHERE number = ?", (lesson_data["number"].split(".")[0],))
        row = cur.fetchone()
        if not row:
            continue
        block_id = row["id"]
        content = {
            "theme": lesson_data["theme"],
            "sections": lesson_data["sections_json"],
        }
        # sections_json уже сериализован, но в lesson_dict — это строка JSON
        # В базе храним весь набор секций + meta
        content_payload = {
            "sections": json.loads(lesson_data["sections_json"]),
            "minutes": lesson_data.get("estimated_minutes", 45),
        }
        conn.execute(
            """INSERT INTO lessons (block_id, number, title, content_json, difficulty, estimated_minutes, order_idx)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (block_id, lesson_data["number"], lesson_data["title"],
             json.dumps(content_payload, ensure_ascii=False),
             lesson_data.get("difficulty", 2),
             lesson_data.get("estimated_minutes", 45),
             int(lesson_data["number"].split(".")[1]) - 1),
        )


def _seed_exercises(conn) -> None:
    conn.execute("DELETE FROM exercises")
    all_lessons = _all_lessons()
    for lesson_data in all_lessons:
        cur = conn.execute("SELECT id FROM lessons WHERE number = ?", (lesson_data["number"],))
        row = cur.fetchone()
        if not row:
            continue
        lesson_id = row["id"]
        for ex_data in lesson_data["exercises"]:
            conn.execute(
                """INSERT INTO exercises
                   (lesson_id, number, type, prompt, starter_code, solution_code,
                    test_cases_json, hints_json, difficulty, expected_result_json)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (lesson_id, ex_data["number"], ex_data["type"], ex_data["prompt"],
                 ex_data["starter_code"], ex_data["solution_code"],
                 ex_data["test_cases_json"], ex_data["hints_json"],
                 ex_data["difficulty"], ex_data.get("expected_result_json")),
            )


def _seed_projects(conn) -> None:
    conn.execute("DELETE FROM projects")
    for p in PROJECTS:
        cur = conn.execute("SELECT id FROM blocks WHERE number = ?", (p["block"],))
        row = cur.fetchone()
        block_id = row["id"] if row else None
        conn.execute(
            """INSERT INTO projects
               (block_id, title, description, theme, difficulty, template_code, solution_code, dataset_json)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (block_id, p["title"], p["description"], p.get("theme", "mixed"),
             p.get("difficulty", 3), p.get("template_code", ""),
             p.get("solution_code", ""),
             json.dumps(p.get("dataset", {}), ensure_ascii=False)),
        )


def _seed_achievements(conn) -> None:
    conn.execute("DELETE FROM achievements")
    conn.execute("DELETE FROM user_achievements")
    for a in ACHIEVEMENTS:
        conn.execute(
            """INSERT INTO achievements (key, title, description, icon, condition_json)
               VALUES (?, ?, ?, ?, ?)""",
            (a["key"], a["title"], a["description"], a.get("icon", "🏆"),
             json.dumps(a.get("condition", {}), ensure_ascii=False)),
        )


def _seed_interview_questions(conn) -> None:
    conn.execute("DELETE FROM interview_questions")
    for q in INTERVIEW_QUESTIONS:
        conn.execute(
            """INSERT INTO interview_questions
               (category, difficulty, question, answer, explanation, common_mistakes, tags_json, is_top)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (q["category"], q.get("difficulty", "junior"), q["question"], q["answer"],
             q.get("explanation", ""), q.get("common_mistakes", ""),
             json.dumps(q.get("tags", []), ensure_ascii=False),
             1 if q.get("is_top") else 0),
        )


def _seed_final_projects(conn) -> None:
    conn.execute("DELETE FROM final_projects")
    for fp in FINAL_PROJECTS:
        conn.execute(
            """INSERT INTO final_projects
               (theme, title, description, steps_json, dataset_json, template_code, solution_code)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (fp["theme"], fp["title"], fp["description"],
             json.dumps(fp["steps_json"], ensure_ascii=False),
             json.dumps(fp["dataset_json"], ensure_ascii=False),
             fp["template_code"], fp["solution_code"]),
        )


def seed_all(conn) -> None:
    """Главная точка: заполняет всю БД."""
    _seed_blocks(conn)
    _seed_lessons(conn)
    _seed_exercises(conn)
    _seed_projects(conn)
    _seed_achievements(conn)
    _seed_interview_questions(conn)
    _seed_final_projects(conn)
