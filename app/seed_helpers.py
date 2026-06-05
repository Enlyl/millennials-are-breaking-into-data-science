"""
Helpers для генерации seed-данных уроков и упражнений.
Используем Python-dict (не JSON-литералы) для читаемости.
В БД пишем через json.dumps.
"""
import json
from typing import Any


def ex(num, etype, prompt, starter, solution, tests=None, hints=None,
       difficulty=2, expected=None) -> dict:
    return {
        "number": num,
        "type": etype,
        "prompt": prompt,
        "starter_code": starter,
        "solution_code": solution,
        "test_cases_json": json.dumps(tests or [], ensure_ascii=False),
        "hints_json": json.dumps(hints or [], ensure_ascii=False),
        "difficulty": difficulty,
        "expected_result_json": json.dumps(expected, ensure_ascii=False) if expected else None,
    }


def lesson(number, title, theme, sections, exercises, difficulty=2, minutes=45) -> dict:
    return {
        "number": number,
        "title": title,
        "theme": theme,
        "difficulty": difficulty,
        "estimated_minutes": minutes,
        "sections_json": json.dumps(sections, ensure_ascii=False),
        "exercises": exercises,
    }


def theory(content: str) -> dict:
    return {"type": "theory", "content": content}


def analogy(real_world: str, domain_example: str) -> dict:
    return {"type": "analogy", "real_world": real_world, "domain_example": domain_example}


def visual(description: str, ascii_diagram: str = "") -> dict:
    return {"type": "visual", "description": description, "ascii_diagram": ascii_diagram}


def example(problem: str, solution_explanation: str, code: str,
            output: str, output_explanation: str) -> dict:
    return {
        "type": "example",
        "problem": problem,
        "solution_explanation": solution_explanation,
        "code": code,
        "output": output,
        "output_explanation": output_explanation,
    }


def common_mistakes(items: list) -> dict:
    return {"type": "common_mistakes", "items": items}


def interview_questions(items: list) -> dict:
    return {"type": "interview_questions", "items": items}


def knowledge_checklist(items: list) -> dict:
    return {"type": "knowledge_checklist", "items": items}
