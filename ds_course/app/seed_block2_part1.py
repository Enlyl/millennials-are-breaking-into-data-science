"""
Блок 2, часть 1: SQL — уроки 2.1-2.7
"""
from app.seed_helpers import (
    ex, lesson, theory, analogy, visual, example,
    common_mistakes, interview_questions, knowledge_checklist,
)


def _2_1():
    return lesson(
        "2.1", "SELECT, FROM, WHERE", "gaming", [
            theory(
                "**SELECT** — основная команда SQL для выборки данных.\n\n"
                "```sql\nSELECT column1, column2\n"
                "FROM table_name\n"
                "WHERE condition;\n```\n\n"
                "**SELECT \\*** — выбрать все столбцы.\n"
                "**WHERE** — фильтрация строк по условию.\n"
                "**Операторы сравнения:** `=`, `!=`, `>`, `<`, `>=`, `<=`\n"
                "**Логика:** `AND`, `OR`, `NOT`"
            ),
            analogy(
                "SELECT — это как заказ в ресторане: ты просишь конкретные блюда (столбцы) из меню (таблицы), с возможностью указать 'без острого' (WHERE).",
                "Выбрать имена всех игроков с рейтингом выше 2000: SELECT name FROM players WHERE rating > 2000;"
            ),
            example(
                "Выбрать имена и очки всех игроков с очками > 1000.",
                "SELECT имя_столбца FROM таблица WHERE условие.",
                "SELECT name, score\n"
                "FROM players\n"
                "WHERE score > 1000;",
                "| name      | score |\n|-----------|-------|\n| DragonSlayer | 1500 |\n| ShadowHunter | 1200 |",
                "WHERE отфильтровал только тех, у кого score > 1000."
            ),
            common_mistakes([
                {"mistake": "WHERE score = 1000 (строковое сравнение)", "why_bad": "Если score — число, нужно без кавычек", "fix": "WHERE score = 1000 (без кавычек)"},
                {"mistake": "SELECT Name vs name", "why_bad": "Зависит от регистра в схеме", "fix": "Проверяй реальные имена столбцов"},
            ]),
            interview_questions([
                {"q": "В чём разница между WHERE и HAVING?",
                 "a": "WHERE фильтрует строки ДО группировки. HAVING — ПОСЛЕ группировки (используется с GROUP BY)."},
                {"q": "Что вернёт SELECT без FROM?",
                 "a": "В большинстве СУБД — ошибка. В MySQL/PostgreSQL — вычислимое выражение: SELECT 1+1 вернёт 2."},
            ]),
            knowledge_checklist([
                "Пишу SELECT, FROM, WHERE",
                "Фильтрую через операторы сравнения",
                "Использую AND/OR/NOT",
                "Понимаю разницу между * и конкретными столбцами",
            ]),
        ],
        exercises=[
            ex(1, "sql", "Выбрать все столбцы из таблицы `players`.",
               "-- Твой запрос\n",
               "SELECT * FROM players;",
               [{"check": "result == [{'id': 1, 'name': 'Alice', 'score': 1500}, {'id': 2, 'name': 'Bob', 'score': 800}]", "msg": "Все строки и столбцы"}],
               ["SELECT * — все столбцы", "FROM указывает таблицу"], 1),
            ex(2, "sql", "Выбрать только `name` и `score` из `players`.",
               "-- Выбрать name и score\n",
               "SELECT name, score FROM players;",
               [{"check": "result == [{'name': 'Alice', 'score': 1500}, {'name': 'Bob', 'score': 800}]", "msg": "Только name и score"}],
               ["SELECT столбец1, столбец2", "FROM таблица"], 1),
            ex(3, "sql", "Выбрать игроков с score > 1000.",
               "SELECT * FROM players WHERE score > 1000;\n",
               "SELECT * FROM players WHERE score > 1000;",
               [{"check": "len(result) == 1 and result[0]['name'] == 'Alice'", "msg": "Только Alice (1500)"}],
               ["WHERE score > 1000"], 1),
            ex(4, "sql", "Выбрать игроков с score между 500 и 1000 (включительно).",
               "SELECT * FROM players WHERE score BETWEEN ? AND ?;\n",
               "SELECT * FROM players WHERE score BETWEEN 500 AND 1000;",
               [{"check": "len(result) == 1 and result[0]['name'] == 'Bob'", "msg": "Bob со score 800"}],
               ["BETWEEN ... AND ...", "Включительно"], 2),
            ex(5, "sql", "Выбрать игроков с name = 'Alice'.",
               "SELECT * FROM players WHERE name = ?;\n",
               "SELECT * FROM players WHERE name = 'Alice';",
               [{"check": "len(result) == 1 and result[0]['name'] == 'Alice'", "msg": "Только Alice"}],
               ["WHERE name = 'значение'", "Строки в одинарных кавычках"], 1),
            ex(6, "sql", "Выбрать игроков, у которых score != 1500.",
               "SELECT * FROM players WHERE score != ?;\n",
               "SELECT * FROM players WHERE score != 1500;",
               [{"check": "len(result) == 1 and result[0]['name'] == 'Bob'", "msg": "Только Bob"}],
               ["!= или <>", "Не равно"], 2),
            ex(7, "sql", "Выбрать игроков с score > 1000 ИЛИ name = 'Bob'.",
               "SELECT * FROM players WHERE score > 1000 OR name = ?;\n",
               "SELECT * FROM players WHERE score > 1000 OR name = 'Bob';",
               [{"check": "len(result) == 2", "msg": "Оба игрока"}],
               ["OR — хотя бы одно", "AND — оба"], 2),
            ex(8, "sql", "Выбрать игроков, у которых score > 500 И score < 1500.",
               "SELECT * FROM players WHERE score > 500 AND score < 1500;\n",
               "SELECT * FROM players WHERE score > 500 AND score < 1500;",
               [{"check": "len(result) == 1 and result[0]['name'] == 'Bob'", "msg": "Только Bob (800)"}],
               ["AND для диапазона", "score > 500 AND score < 1500"], 2),
        ],
        minutes=40, difficulty=1,
    )


def _2_2():
    return lesson(
        "2.2", "ORDER BY, LIMIT, DISTINCT", "gaming", [
            theory(
                "**ORDER BY** — сортировка результатов.\n"
                "**LIMIT n** — первые n строк.\n"
                "**DISTINCT** — уникальные значения.\n\n"
                "```sql\nSELECT name, score\n"
                "FROM players\n"
                "ORDER BY score DESC\n"
                "LIMIT 5;\n```\n\n"
                "**ASC** — по возрастанию (default), **DESC** — по убыванию."
            ),
            analogy(
                "ORDER BY — сортировка в Excel (А→Я, по убыванию). LIMIT — топ-N строк. DISTINCT — убрать дубликаты.",
                "Топ-10 игроков по рейтингу: ORDER BY rating DESC LIMIT 10."
            ),
            example(
                "Выбрать топ-3 игрока по очкам (по убыванию).",
                "ORDER BY ... DESC LIMIT 3.",
                "SELECT name, score\n"
                "FROM players\n"
                "ORDER BY score DESC\n"
                "LIMIT 3;",
                "| name      | score |\n|-----------|-------|\n| Alice     | 1500  |\n| Bob       | 800   |\n| Charlie   | 600   |",
                "DESC — по убыванию, LIMIT 3 — первые 3 строки."
            ),
            common_mistakes([
                {"mistake": "ORDER BY без указания ASC/DESC", "why_bad": "По умолчанию ASC — может не совпасть с ожиданием", "fix": "Явно указывай ASC или DESC"},
                {"mistake": "LIMIT без ORDER BY", "why_bad": "Результат непредсказуем", "fix": "Всегда используй ORDER BY с LIMIT"},
            ]),
            interview_questions([
                {"q": "Можно ли использовать ORDER BY по нескольким столбцам?",
                 "a": "Да: ORDER BY score DESC, name ASC — сначала по score, потом по name при равных score."},
                {"q": "DISTINCT применяется ко всем столбцам или к одному?",
                 "a": "Ко всем в SELECT. SELECT DISTINCT a, b — уникальные КОМБИНАЦИИ a и b."},
            ]),
            knowledge_checklist([
                "Сортирую через ORDER BY ASC/DESC",
                "Ограничиваю результат через LIMIT",
                "Использую DISTINCT для уникальности",
                "Сортирую по нескольким столбцам",
            ]),
        ],
        exercises=[
            ex(1, "sql", "Выбрать всех игроков, отсортированных по score по убыванию.",
               "SELECT * FROM players ORDER BY ? DESC;\n",
               "SELECT * FROM players ORDER BY score DESC;",
               [{"check": "result[0]['name'] == 'Alice' and result[1]['name'] == 'Bob'", "msg": "Сначала Alice (1500), потом Bob (800)"}],
               ["ORDER BY score DESC"], 1),
            ex(2, "sql", "Выбрать топ-1 игрока (с наивысшим score).",
               "SELECT * FROM players ORDER BY score DESC LIMIT ?;\n",
               "SELECT * FROM players ORDER BY score DESC LIMIT 1;",
               [{"check": "len(result) == 1 and result[0]['name'] == 'Alice'", "msg": "Только Alice"}],
               ["ORDER BY ... DESC LIMIT 1", "Топ-1"], 1),
            ex(3, "sql", "Выбрать уникальные значения score (без дубликатов).",
               "SELECT ? score FROM players;\n",
               "SELECT DISTINCT score FROM players;",
               [{"check": "len(result) == 2", "msg": "2 уникальных score: 1500 и 800"}],
               ["DISTINCT убирает дубли"], 2),
            ex(4, "sql", "Выбрать всех игроков, отсортированных по name (А-Я).",
               "SELECT * FROM players ORDER BY name ?;\n",
               "SELECT * FROM players ORDER BY name ASC;",
               [{"check": "result[0]['name'] == 'Alice' and result[1]['name'] == 'Bob'", "msg": "Алфавитный порядок"}],
               ["ORDER BY name ASC", "ASC по возрастанию"], 1),
            ex(5, "sql", "Выбрать 2 игроков с наименьшим score.",
               "SELECT * FROM players ORDER BY score ASC LIMIT ?;\n",
               "SELECT * FROM players ORDER BY score ASC LIMIT 2;",
               [{"check": "len(result) == 2", "msg": "2 игрока с мин. score"}],
               ["ORDER BY ASC + LIMIT"], 1),
            ex(6, "sql", "Выбрать уникальные комбинации name и score.",
               "SELECT ? name, score FROM players;\n",
               "SELECT DISTINCT name, score FROM players;",
               [{"check": "len(result) == 2", "msg": "Уникальные пары"}],
               ["DISTINCT к комбинации столбцов"], 2),
            ex(7, "sql", "Выбрать игроков, отсортированных по score DESC, потом по name ASC.",
               "SELECT * FROM players ORDER BY score ?, name ?;\n",
               "SELECT * FROM players ORDER BY score DESC, name ASC;",
               [{"check": "result[0]['score'] == 1500", "msg": "По убыванию score"}],
               ["ORDER BY col1 DESC, col2 ASC"], 3),
        ],
        minutes=30, difficulty=1,
    )


def _2_3():
    return lesson(
        "2.3", "Агрегатные функции: COUNT, SUM, AVG, MIN, MAX", "gaming", [
            theory(
                "**Агрегатные функции** считают по столбцу:\n\n"
                "- `COUNT(col)` — кол-во не-NULL значений\n"
                "- `SUM(col)` — сумма\n"
                "- `AVG(col)` — среднее\n"
                "- `MIN(col)` — минимум\n"
                "- `MAX(col)` — максимум\n\n"
                "```sql\nSELECT COUNT(*), AVG(score), MAX(score)\n"
                "FROM players;\n```\n\n"
                "`COUNT(*)` считает все строки, включая NULL."
            ),
            analogy(
                "Агрегатные функции — итоги в спорте: COUNT — сколько матчей, SUM — всего очков, AVG — в среднем за матч.",
                "Сколько игроков в базе: SELECT COUNT(*) FROM players;."
            ),
            example(
                "Вычисли статистику по таблице players.",
                "Агрегаты без GROUP BY дают одну строку.",
                "SELECT\n"
                "  COUNT(*) AS total,\n"
                "  AVG(score) AS avg_score,\n"
                "  MAX(score) AS best,\n"
                "  MIN(score) AS worst\n"
                "FROM players;",
                "| total | avg_score | best | worst |\n|-------|-----------|------|-------|\n| 3     | 966.66    | 1500 | 600   |",
                "AS задаёт алиас (имя столбца в результате)."
            ),
            common_mistakes([
                {"mistake": "AVG(name) для строкового столбца", "why_bad": "Ошибка или 0", "fix": "Применяй только к числовым"},
                {"mistake": "COUNT(col) vs COUNT(*)", "why_bad": "COUNT(col) не считает NULL", "fix": "COUNT(*) — все строки"},
            ]),
            interview_questions([
                {"q": "Чем COUNT(col) отличается от COUNT(*)?",
                 "a": "COUNT(col) не считает NULL в col. COUNT(*) считает все строки."},
                {"q": "NULL — это 0 для AVG?",
                 "a": "Нет. NULL игнорируется и в числителе (SUM), и в знаменателе (COUNT)."},
            ]),
            knowledge_checklist([
                "Использую COUNT, SUM, AVG, MIN, MAX",
                "Понимаю разницу COUNT(*) vs COUNT(col)",
                "Задаю алиасы через AS",
            ]),
        ],
        exercises=[
            ex(1, "sql", "Посчитай общее количество игроков.",
               "SELECT ?(*) FROM players;\n",
               "SELECT COUNT(*) FROM players;",
               [{"check": "result[0]['COUNT(*)'] == 3", "msg": "3 игрока"}],
               ["COUNT(*) считает все строки"], 1),
            ex(2, "sql", "Найди средний score всех игроков.",
               "SELECT ?(score) FROM players;\n",
               "SELECT AVG(score) FROM players;",
               [{"check": "abs(result[0]['AVG(score)'] - 966.66) < 1", "msg": "≈ 966.67"}],
               ["AVG(столбец)"], 1),
            ex(3, "sql", "Найди максимальный score.",
               "SELECT ?(score) FROM players;\n",
               "SELECT MAX(score) FROM players;",
               [{"check": "result[0]['MAX(score)'] == 1500", "msg": "1500"}],
               ["MAX(столбец)"], 1),
            ex(4, "sql", "Найди минимальный score.",
               "SELECT MIN(score) FROM players;\n",
               "SELECT MIN(score) FROM players;",
               [{"check": "result[0]['MIN(score)'] == 600", "msg": "600"}],
               ["MIN(столбец)"], 1),
            ex(5, "sql", "Посчитай сумму всех score.",
               "SELECT SUM(score) FROM players;\n",
               "SELECT SUM(score) FROM players;",
               [{"check": "result[0]['SUM(score)'] == 2900", "msg": "2900"}],
               ["SUM(столбец)"], 1),
            ex(6, "sql", "Посчитай количество игроков с score > 1000.",
               "SELECT COUNT(*) FROM players WHERE score > ?;\n",
               "SELECT COUNT(*) FROM players WHERE score > 1000;",
               [{"check": "result[0]['COUNT(*)'] == 1", "msg": "1 игрок (Alice)"}],
               ["COUNT + WHERE"], 2),
            ex(7, "sql", "Найди максимальный и минимальный score одной строкой.",
               "SELECT MAX(score), ?(score) FROM players;\n",
               "SELECT MAX(score), MIN(score) FROM players;",
               [{"check": "result[0]['MAX(score)'] == 1500 and result[0]['MIN(score)'] == 600", "msg": "1500 и 600"}],
               ["MAX, MIN в одном SELECT"], 2),
        ],
        minutes=35, difficulty=2,
    )


def _2_4():
    return lesson(
        "2.4", "GROUP BY и HAVING", "gaming", [
            theory(
                "**GROUP BY** группирует строки по значениям столбца, агрегат считается для каждой группы.\n\n"
                "```sql\nSELECT team, COUNT(*) AS players_count\n"
                "FROM players\n"
                "GROUP BY team;\n```\n\n"
                "**HAVING** — фильтр ПОСЛЕ группировки (аналог WHERE, но для групп):\n\n"
                "```sql\nSELECT team, AVG(score) AS avg_score\n"
                "FROM players\n"
                "GROUP BY team\n"
                "HAVING AVG(score) > 800;\n```"
            ),
            analogy(
                "GROUP BY — это как сортировка по полкам: все яблоки вместе, все груши вместе. HAVING — фильтр для полок ('только полки с >10 яблоками').",
                "Сколько игроков в каждой команде: SELECT team, COUNT(*) FROM players GROUP BY team."
            ),
            example(
                "Сколько игроков в каждой команде?",
                "GROUP BY team + COUNT(*).",
                "SELECT team, COUNT(*) AS cnt\n"
                "FROM players\n"
                "GROUP BY team;",
                "| team | cnt |\n|------|-----|\n| red  | 2   |\n| blue | 1   |",
                "GROUP BY team разбил на 2 группы. COUNT(*) для каждой."
            ),
            common_mistakes([
                {"mistake": "WHERE с агрегатом", "why_bad": "WHERE фильтрует строки, не группы", "fix": "Используй HAVING для агрегатов"},
                {"mistake": "SELECT без агрегата и без GROUP BY столбца", "why_bad": "Неоднозначный результат в строгих СУБД", "fix": "Все столбцы в SELECT — либо в GROUP BY, либо в агрегате"},
            ]),
            interview_questions([
                {"q": "Порядок выполнения SELECT?",
                 "a": "FROM → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT."},
                {"q": "Можно ли WHERE и HAVING в одном запросе?",
                 "a": "Да. WHERE — до группировки, HAVING — после. Пример: WHERE active=1 GROUP BY team HAVING COUNT > 5."},
            ]),
            knowledge_checklist([
                "Группирую через GROUP BY",
                "Фильтрую группы через HAVING",
                "Помню порядок: WHERE → GROUP BY → HAVING",
            ]),
        ],
        exercises=[
            ex(1, "sql", "Посчитай количество игроков в каждой команде.",
               "SELECT team, COUNT(*) FROM players GROUP BY ?;\n",
               "SELECT team, COUNT(*) FROM players GROUP BY team;",
               [{"check": "len(result) == 2", "msg": "2 команды"}],
               ["GROUP BY team"], 1),
            ex(2, "sql", "Средний score по командам.",
               "SELECT team, AVG(score) FROM players GROUP BY ?;\n",
               "SELECT team, AVG(score) FROM players GROUP BY team;",
               [{"check": "len(result) == 2", "msg": "2 команды"}],
               ["AVG + GROUP BY"], 2),
            ex(3, "sql", "Покажи команды, у которых средний score > 1000.",
               "SELECT team, AVG(score) AS a FROM players GROUP BY team HAVING ? > 1000;\n",
               "SELECT team, AVG(score) AS a FROM players GROUP BY team HAVING AVG(score) > 1000;",
               [{"check": "len(result) == 1 and result[0]['team'] == 'red'", "msg": "Только red (Alice 1500, Charlie 1000)"}],
               ["HAVING с агрегатом"], 2),
            ex(4, "sql", "Максимальный score по командам.",
               "SELECT team, MAX(score) FROM players GROUP BY ?;\n",
               "SELECT team, MAX(score) FROM players GROUP BY team;",
               [{"check": "len(result) == 2", "msg": "2 команды"}],
               ["MAX + GROUP BY"], 2),
            ex(5, "sql", "Команды с более чем 1 игроком.",
               "SELECT team FROM players GROUP BY team HAVING COUNT(*) > ?;\n",
               "SELECT team FROM players GROUP BY team HAVING COUNT(*) > 1;",
               [{"check": "len(result) == 1 and result[0]['team'] == 'red'", "msg": "Только red (2 игрока)"}],
               ["HAVING COUNT(*) > 1"], 2),
        ],
        minutes=40, difficulty=2,
    )


def _2_5():
    return lesson(
        "2.5", "CASE WHEN", "gaming", [
            theory(
                "**CASE WHEN** — аналог if/else в SQL.\n\n"
                "```sql\nSELECT name,\n"
                "  CASE\n"
                "    WHEN score >= 1500 THEN 'Про'\n"
                "    WHEN score >= 1000 THEN 'Средний'\n"
                "    ELSE 'Новичок'\n"
                "  END AS rank\n"
                "FROM players;\n```"
            ),
            analogy(
                "CASE WHEN — это if/elif/else, только в SQL.",
                "Ранг игрока по очкам: pro, средний, новичок."
            ),
            example(
                "Категоризируй игроков по score: >=1500 — 'Pro', >=800 — 'Average', иначе 'Rookie'.",
                "CASE WHEN возвращает значение на основе условий.",
                "SELECT name,\n"
                "  CASE\n"
                "    WHEN score >= 1500 THEN 'Pro'\n"
                "    WHEN score >= 800 THEN 'Average'\n"
                "    ELSE 'Rookie'\n"
                "  END AS rank\n"
                "FROM players;",
                "| name    | rank    |\n|---------|---------|\n| Alice   | Pro     |\n| Bob     | Average |\n| Charlie | Rookie  |",
                "CASE проверяет условия по порядку. Первое совпавшее — результат."
            ),
            common_mistakes([
                {"mistake": "Забыл END", "why_bad": "SyntaxError", "fix": "Всегда закрывай CASE через END"},
                {"mistake": "WHEN без THEN", "why_bad": "Синтаксическая ошибка", "fix": "WHEN условие THEN значение"},
            ]),
            interview_questions([
                {"q": "Можно ли CASE WHEN использовать в WHERE?",
                 "a": "Нет, в WHERE только условия. Для трансформации — SELECT или HAVING."},
                {"q": "CASE vs COALESCE?",
                 "a": "COALESCE(a, b) — первое не-NULL из списка. CASE WHEN — условная логика."},
            ]),
            knowledge_checklist([
                "Пишу CASE WHEN ... THEN ... ELSE ... END",
                "Использую для категоризации",
                "Помню про END",
            ]),
        ],
        exercises=[
            ex(1, "sql", "Добавь столбец `level`: 'high' если score > 1000, иначе 'low'.",
               "SELECT name, CASE WHEN score > 1000 THEN 'high' ELSE '?' END AS level FROM players;\n",
               "SELECT name, CASE WHEN score > 1000 THEN 'high' ELSE 'low' END AS level FROM players;",
               [{"check": "result[0]['level'] == 'high' and result[1]['level'] == 'low'", "msg": "Alice high, Bob low"}],
               ["CASE WHEN ... THEN ... ELSE", "END обязателен"], 2),
            ex(2, "sql", "Категоризируй: 'A' если score>=1500, 'B' если >=1000, иначе 'C'.",
               "SELECT name, CASE WHEN score>=1500 THEN 'A' WHEN score>=1000 THEN 'B' ELSE 'C' END AS grade FROM players;\n",
               "SELECT name, CASE WHEN score>=1500 THEN 'A' WHEN score>=1000 THEN 'B' ELSE 'C' END AS grade FROM players;",
               [{"check": "result[0]['grade'] == 'A' and result[2]['grade'] == 'C'", "msg": "Alice A, Charlie C"}],
               ["WHEN ... THEN", "ELSE"], 2),
            ex(3, "sql", "Выведи name и status: 'winner' для score=1500, иначе 'other'.",
               "SELECT name, CASE WHEN score = 1500 THEN 'winner' ELSE 'other' END AS status FROM players;\n",
               "SELECT name, CASE WHEN score = 1500 THEN 'winner' ELSE 'other' END AS status FROM players;",
               [{"check": "result[0]['status'] == 'winner' and result[1]['status'] == 'other'", "msg": "Alice winner, Bob other"}],
               ["CASE ... ELSE"], 2),
        ],
        minutes=30, difficulty=2,
    )


def _2_6():
    return lesson(
        "2.6", "INNER JOIN, LEFT JOIN", "gaming", [
            theory(
                "**JOIN** соединяет строки из двух таблиц по условию.\n\n"
                "**INNER JOIN** — только совпадающие строки:\n"
                "```sql\nSELECT p.name, t.team_name\n"
                "FROM players p\n"
                "INNER JOIN teams t ON p.team_id = t.id;\n```\n\n"
                "**LEFT JOIN** — все из левой + совпадения из правой (если нет — NULL):\n"
                "```sql\nSELECT p.name, t.team_name\n"
                "FROM players p\n"
                "LEFT JOIN teams t ON p.team_id = t.id;\n```"
            ),
            analogy(
                "INNER JOIN — пересечение двух списков (только общие друзья). LEFT JOIN — все из списка A, к ним добавь друзей из B (если есть).",
                "Соединить игроков с их командами: INNER JOIN players + teams."
            ),
            example(
                "Покажи имена игроков и названия их команд.",
                "INNER JOIN + ON.",
                "SELECT p.name, t.team_name\n"
                "FROM players p\n"
                "INNER JOIN teams t ON p.team_id = t.id;",
                "| name    | team_name |\n|---------|-----------|\n| Alice   | Red       |\n| Bob     | Red       |\n| Charlie | Blue      |",
                "INNER JOIN берёт только тех, у кого есть совпадение в teams."
            ),
            common_mistakes([
                {"mistake": "JOIN без ON", "why_bad": "Декартово произведение — строки × строки", "fix": "Всегда указывай ON"},
                {"mistake": "Путать LEFT и INNER", "why_bad": "LEFT даст NULL, INNER — нет", "fix": "LEFT — все из левой, INNER — только совпадения"},
            ]),
            interview_questions([
                {"q": "В чём разница INNER и LEFT JOIN?",
                 "a": "INNER — только совпадающие строки в обеих таблицах. LEFT — все из левой + NULL для несовпавших правых."},
                {"q": "Что такое CROSS JOIN?",
                 "a": "Декартово произведение: каждая строка левой с каждой строкой правой. Без ON."},
            ]),
            knowledge_checklist([
                "INNER JOIN для совпадений",
                "LEFT JOIN для всех из левой",
                "Указываю ON",
            ]),
        ],
        exercises=[
            ex(1, "sql", "Покажи имена игроков и названия команд (INNER JOIN).",
               "SELECT p.name, t.team_name FROM players p INNER JOIN teams t ON p.team_id = t.id;\n",
               "SELECT p.name, t.team_name FROM players p INNER JOIN teams t ON p.team_id = t.id;",
               [{"check": "len(result) == 3", "msg": "3 совпадения"}],
               ["INNER JOIN ... ON ..."], 1),
            ex(2, "sql", "Покажи всех игроков и их команды (LEFT JOIN). Если команды нет — должно быть в результате.",
               "SELECT p.name, t.team_name FROM players p LEFT JOIN teams t ON p.team_id = t.id;\n",
               "SELECT p.name, t.team_name FROM players p LEFT JOIN teams t ON p.team_id = t.id;",
               [{"check": "len(result) == 3", "msg": "Все игроки"}],
               ["LEFT JOIN ... ON ..."], 2),
            ex(3, "sql", "Выведи name игрока и team_name, где team_name = 'Red'.",
               "SELECT p.name, t.team_name FROM players p INNER JOIN teams t ON p.team_id = t.id WHERE t.team_name = 'Red';\n",
               "SELECT p.name, t.team_name FROM players p INNER JOIN teams t ON p.team_id = t.id WHERE t.team_name = 'Red';",
               [{"check": "len(result) == 2", "msg": "2 игрока в Red"}],
               ["INNER JOIN + WHERE"], 2),
        ],
        minutes=35, difficulty=2,
    )


def _2_7():
    return lesson(
        "2.7", "RIGHT JOIN, FULL JOIN, CROSS JOIN", "gaming", [
            theory(
                "**RIGHT JOIN** — все из правой + совпадения из левой.\n"
                "**FULL OUTER JOIN** — все из обеих (нет в SQLite, но есть в PostgreSQL).\n"
                "**CROSS JOIN** — каждая с каждой (декартово произведение).\n\n"
                "```sql\n-- RIGHT JOIN\n"
                "SELECT * FROM a RIGHT JOIN b ON a.id = b.a_id;\n\n"
                "-- FULL OUTER (не все СУБД)\n"
                "SELECT * FROM a FULL OUTER JOIN b ON a.id = b.a_id;\n\n"
                "-- CROSS JOIN\n"
                "SELECT * FROM a CROSS JOIN b;\n```"
            ),
            analogy(
                "RIGHT JOIN — зеркало LEFT JOIN. FULL OUTER — объединение INNER + LEFT + RIGHT.",
                "Все команды, даже без игроков: RIGHT JOIN teams ← players."
            ),
            example(
                "CROSS JOIN: все комбинации игроков и игр.",
                "Каждый с каждым — без условия.",
                "SELECT p.name AS player, g.name AS game\n"
                "FROM players p\n"
                "CROSS JOIN games g;",
                "Все комбинации player × game",
                "CROSS JOIN = декартово произведение. 3 игрока × 2 игры = 6 строк."
            ),
            common_mistakes([
                {"mistake": "Использовать FULL OUTER JOIN в SQLite", "why_bad": "SQLite не поддерживает", "fix": "UNION двух запросов LEFT+RIGHT"},
            ]),
            interview_questions([
                {"q": "Почему CROSS JOIN опасен?",
                 "a": "Может вернуть огромный результат: 1М × 1М = 10^12 строк. Использовать осознанно."},
                {"q": "Заменяет ли FULL OUTER комбинацию LEFT+RIGHT?",
                 "a": "Да, FULL OUTER = LEFT JOIN ∪ RIGHT JOIN, без дубликатов."},
            ]),
            knowledge_checklist([
                "Понимаю разницу между типами JOIN",
                "Использую CROSS JOIN осознанно",
            ]),
        ],
        exercises=[
            ex(1, "sql", "Верни все комбинации игроков и команд (CROSS JOIN).",
               "SELECT p.name, t.team_name FROM players p CROSS JOIN teams t;\n",
               "SELECT p.name, t.team_name FROM players p CROSS JOIN teams t;",
               [{"check": "len(result) == 6", "msg": "3 игрока × 2 команды = 6"}],
               ["CROSS JOIN без ON"], 1),
            ex(2, "sql", "Покажи команды и игроков через LEFT JOIN teams (все команды + игроки, если есть).",
               "SELECT t.team_name, p.name FROM teams t LEFT JOIN players p ON t.id = p.team_id;\n",
               "SELECT t.team_name, p.name FROM teams t LEFT JOIN players p ON t.id = p.team_id;",
               [{"check": "len(result) >= 3", "msg": "Все команды"}],
               ["teams слева, players справа", "LEFT JOIN"], 2),
        ],
        minutes=25, difficulty=2,
    )


LESSONS = [_2_1, _2_2, _2_3, _2_4, _2_5, _2_6, _2_7]
