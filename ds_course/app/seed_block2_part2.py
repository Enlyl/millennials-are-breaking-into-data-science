"""
Блок 2, часть 2: SQL — уроки 2.8-2.14
"""
from app.seed_helpers import (
    ex, lesson, theory, analogy, visual, example,
    common_mistakes, interview_questions, knowledge_checklist,
)


def _2_8():
    return lesson(
        "2.8", "Подзапросы", "gaming", [
            theory(
                "**Подзапрос** — запрос внутри другого запроса.\n\n"
                "```sql\nSELECT name\n"
                "FROM players\n"
                "WHERE score > (SELECT AVG(score) FROM players);\n```\n\n"
                "Подзапросы бывают:\n"
                "- В WHERE: `WHERE col > (SELECT ...)`\n"
                "- В FROM: `FROM (SELECT ...) AS sub`\n"
                "- В SELECT: `SELECT (SELECT ...) AS x`"
            ),
            analogy(
                "Подзапрос — это вложенный вопрос: 'Покажи игроков с очками выше среднего'. Сначала считаем среднее, потом сравниваем.",
                "Найти игроков, у которых score = max: подзапрос в WHERE."
            ),
            visual(
                "Подзапрос в WHERE: внешний запрос ссылается на результат внутреннего, который выполняется первым.",
                r'''   Внешний запрос (SELECT name FROM players WHERE score > ?)
   ┌─────────────────────────────────────────────────────────────┐
   │  SELECT name                                                │
   │  FROM   players                                             │
   │  WHERE  score >  (результат внутреннего)                    │
   │              ▲                                              │
   │              │ результат:  966.67  (одно число)              │
   │              │                                              │
   └──────────────┼──────────────────────────────────────────────┘
                  │
                  │ Подзапрос (внутренний, выполняется ПЕРВЫМ)
                  ▼
   ┌─────────────────────────────────────────────────────────────┐
   │  SELECT AVG(score)                                          │
   │  FROM   players                                             │
   │  ───────────                                                │
   │  результат:  966.67                                         │
   └─────────────────────────────────────────────────────────────┘

   Другие места подзапросов:
   • WHERE col IN (SELECT ...)     — подзапрос возвращает набор
   • FROM   (SELECT ...) AS sub    — подзапрос как таблица
   • SELECT (SELECT ...) AS x      — скалярный подзапрос'''
            ),
            example(
                "Найди игроков со score выше среднего.",
                "WHERE score > (подзапрос с AVG).",
                "SELECT name, score\n"
                "FROM players\n"
                "WHERE score > (SELECT AVG(score) FROM players);",
                "| name    | score |\n|---------|-------|\n| Alice   | 1500  |",
                "Подзапрос вернул среднее 966.66. Игроки с score > 966.66 — только Alice (1500)."
            ),
            common_mistakes([
                {"mistake": "Подзапрос возвращает > 1 строки в WHERE col = (sub)", "why_bad": "Ошибка или непредсказуемо", "fix": "Используй IN или ANY/ALL"},
                {"mistake": "Забыл алиас для подзапроса в FROM", "why_bad": "Синтаксическая ошибка", "fix": "FROM (SELECT ...) AS sub"},
            ]),
            interview_questions([
                {"q": "Коррелированный vs обычный подзапрос?",
                 "a": "Коррелированный ссылается на внешний запрос (выполняется для каждой строки). Обычный — независимый."},
                {"q": "EXISTS vs IN?",
                 "a": "EXISTS проверяет факт наличия строки, IN — равенство. EXISTS быстрее для больших подзапросов."},
            ]),
            knowledge_checklist([
                "Подзапрос в WHERE",
                "Подзапрос в FROM с алиасом",
                "Понимаю IN, EXISTS, ANY",
            ]),
        ],
        exercises=[
            ex(1, "sql", "Найди игроков с score выше среднего.",
               "SELECT name FROM players WHERE score > (SELECT ?(score) FROM players);\n",
               "SELECT name FROM players WHERE score > (SELECT AVG(score) FROM players);",
               [{"check": "len(result) == 1 and result[0]['name'] == 'Alice'", "msg": "Только Alice (1500 > 966)"}],
               ["WHERE > (SELECT AVG...)"], 2),
            ex(2, "sql", "Найди игроков, у которых team_id соответствует Red.",
               "SELECT name FROM players WHERE team_id = (SELECT id FROM teams WHERE team_name = 'Red');\n",
               "SELECT name FROM players WHERE team_id = (SELECT id FROM teams WHERE team_name = 'Red');",
               [{"check": "len(result) == 2", "msg": "2 игрока в Red"}],
               ["WHERE = (SELECT id ...)"], 2),
            ex(3, "sql", "Найди игрока с максимальным score через подзапрос.",
               "SELECT name FROM players WHERE score = (SELECT ?(score) FROM players);\n",
               "SELECT name FROM players WHERE score = (SELECT MAX(score) FROM players);",
               [{"check": "result[0]['name'] == 'Alice'", "msg": "Alice с 1500"}],
               ["WHERE = (SELECT MAX ...)"], 2),
        ],
        minutes=30, difficulty=2,
    )


def _2_9():
    return lesson(
        "2.9", "CTE (Common Table Expressions)", "gaming", [
            theory(
                "**CTE** — именованный подзапрос через WITH. Делает запрос читабельнее.\n\n"
                "```sql\nWITH high_scorers AS (\n"
                "  SELECT name, score FROM players WHERE score > 1000\n"
                ")\n"
                "SELECT * FROM high_scorers WHERE name LIKE 'A%';\n```\n\n"
                "Можно несколько CTE через запятую."
            ),
            analogy(
                "CTE — переменная с подзапросом: 'вычисли это один раз, потом используй'. Как sub в математике.",
                "Сначала определи 'high_scorers', потом работай с ними."
            ),
            visual(
                "CTE через WITH: именованный промежуточный результат вычисляется один раз и подаётся в основной запрос.",
                r'''   ┌──────────────────────────────────────────────────────────┐
   │  WITH avg_score AS (                                        │
   │       SELECT AVG(score) AS a FROM players                   │
   │  )                                                          │
   │  ──── определили «переменную» avg_score ────                │
   │                                                             │
   │  SELECT name, score                                         │
   │  FROM   players, avg_score                                  │
   │  WHERE  players.score > avg_score.a                         │
   └──────────────────────────────────────────────────────────┘
                       │
                       │ материализуется
                       ▼
   ┌───────────────────────┐         ┌─────────────────────────┐
   │  avg_score (CTE)      │         │  players                │
   │  ┌─────────────┐      │  JOIN   │  name   │ score         │
   │  │     a       │      │  по     │  ───────┼──────         │
   │  │   966.67    │      │ условию │  Alice  │  1500         │
   │  └─────────────┘      │   │     │  Bob    │   800         │
   │  временная «таблица»  │   │     │  Diana  │  2200         │
   └───────────────────────┘   ▼     └─────────┬───────────────┘
                                              │
                                              ▼
                                ┌────────────────────────┐
                                │ name    │ score        │  ← результат
                                │ Alice   │ 1500 (>966)  │
                                │ Diana   │ 2200 (>966)  │
                                └────────────────────────┘'''
            ),
            example(
                "Используя CTE, найди игроков со score выше среднего.",
                "WITH avg_score AS (SELECT AVG(score) AS a FROM players).",
                "WITH avg_score AS (\n"
                "  SELECT AVG(score) AS a FROM players\n"
                ")\n"
                "SELECT name, score\n"
                "FROM players, avg_score\n"
                "WHERE players.score > avg_score.a;",
                "name: Alice, score: 1500",
                "CTE avg_score материализует подзапрос, потом используем в WHERE."
            ),
            common_mistakes([
                {"mistake": "WITH без AS", "why_bad": "Синтаксическая ошибка", "fix": "WITH name AS (SELECT ...)"},
                {"mistake": "Использовать CTE до его определения", "why_bad": "Неизвестно", "fix": "Определяй CTE выше использования"},
            ]),
            interview_questions([
                {"q": "CTE vs подзапрос?",
                 "a": "CTE читабельнее, можно переиспользовать, рекурсивные CTE для иерархий. Подзапрос — для простых случаев."},
                {"q": "Рекурсивный CTE — для чего?",
                 "a": "Для деревьев и графов: оргструктура, иерархия комментариев, обход графа."},
            ]),
            knowledge_checklist([
                "Создаю CTE через WITH ... AS",
                "Использую CTE вместо подзапросов для читаемости",
            ]),
        ],
        exercises=[
            ex(1, "sql", "Создай CTE `top_players` с score > 1000, выведи всех из него.",
               "WITH top_players AS (SELECT * FROM players WHERE score > 1000) SELECT * FROM top_players;\n",
               "WITH top_players AS (SELECT * FROM players WHERE score > 1000) SELECT * FROM top_players;",
               [{"check": "len(result) == 1 and result[0]['name'] == 'Alice'", "msg": "Только Alice"}],
               ["WITH name AS (SELECT ...)"], 2),
            ex(2, "sql", "Создай CTE `red_players` для команды Red, выведи имена.",
               "WITH red_players AS (SELECT * FROM players WHERE team_id = 1) SELECT name FROM red_players;\n",
               "WITH red_players AS (SELECT * FROM players WHERE team_id = 1) SELECT name FROM red_players;",
               [{"check": "len(result) == 2", "msg": "2 игрока в Red"}],
               ["WITH ... AS ... SELECT"], 2),
        ],
        minutes=25, difficulty=2,
    )


def _2_10():
    return lesson(
        "2.10", "Оконные функции: ROW_NUMBER, RANK, DENSE_RANK", "gaming", [
            theory(
                "**Оконные функции** считают по 'окну' строк, не схлопывая результат (как GROUP BY).\n\n"
                "```sql\nSELECT name, score,\n"
                "  ROW_NUMBER() OVER (ORDER BY score DESC) AS rn,\n"
                "  RANK() OVER (ORDER BY score DESC) AS rnk,\n"
                "  DENSE_RANK() OVER (ORDER BY score DESC) AS drnk\n"
                "FROM players;\n```\n\n"
                "- `ROW_NUMBER()` — уникальный номер (1, 2, 3, ...)\n"
                "- `RANK()` — ранг с пропусками (1, 1, 3, 4)\n"
                "- `DENSE_RANK()` — ранг без пропусков (1, 1, 2, 3)"
            ),
            analogy(
                "ROW_NUMBER — места в очереди. RANK — как в спорте: два первых, третий сразу третий. DENSE_RANK — последовательно: 1, 1, 2.",
                "Топ-N в каждой команде: ROW_NUMBER() OVER (PARTITION BY team ORDER BY score DESC)."
            ),
            visual(
                "Сравнение ROW_NUMBER, RANK, DENSE_RANK на одних и тех же данных: разница в обработке одинаковых значений.",
                r'''   Исходные строки (отсортированы по score DESC):
   ┌─────────┬───────┐
   │ name    │ score │
   │ ────────┼───────│
   │ Alice   │  1500 │
   │ Bob     │  1500 │  ← дубль!
   │ Charlie │  1000 │
   │ Diana   │  1000 │  ← дубль!
   │ Eve     │   500 │
   └─────────┴───────┘
             │
             │  ORDER BY score DESC
             ▼
   ┌─────────┬───────┬─────────┬───────┬─────────────┐
   │ name    │ score │ ROW_NUM │ RANK  │ DENSE_RANK  │
   │ ────────┼───────┼─────────┼───────┼─────────────│
   │ Alice   │  1500 │    1    │   1   │     1       │
   │ Bob     │  1500 │    2    │   1   │     1       │  ← одинаковые
   │ Charlie │  1000 │    3    │   3   │     2       │  ← пропуск в RANK
   │ Diana   │  1000 │    4    │   3   │     2       │
   │ Eve     │   500 │    5    │   5   │     3       │
   └─────────┴───────┴─────────┴───────┴─────────────┘
       ↑                ↑        ↑         ↑
   уникальные 1..N    с       1,1,3,3,5  1,1,2,2,3
   номера              пропусками
                      после дублей'''
            ),
            example(
                "Ранжируй игроков по score.",
                "ROW_NUMBER / RANK / DENSE_RANK.",
                "SELECT name, score,\n"
                "  ROW_NUMBER() OVER (ORDER BY score DESC) AS rn,\n"
                "  RANK() OVER (ORDER BY score DESC) AS rnk\n"
                "FROM players;",
                "Alice rn=1 rnk=1, Bob rn=2 rnk=2, Charlie rn=3 rnk=3",
                "ROW_NUMBER даёт уникальные номера. RANK пропускает места при равных."
            ),
            common_mistakes([
                {"mistake": "Забыл OVER (...)", "why_bad": "Синтаксическая ошибка", "fix": "ROW_NUMBER() OVER (ORDER BY ...)"},
                {"mistake": "PARTITION BY в скобках", "why_bad": "Ошибка", "fix": "PARTITION BY col — внутри OVER"},
            ]),
            interview_questions([
                {"q": "RANK vs DENSE_RANK?",
                 "a": "RANK пропускает: 1,1,3. DENSE_RANK не пропускает: 1,1,2."},
                {"q": "PARTITION BY vs GROUP BY?",
                 "a": "PARTITION BY — для окон (не схлопывает), GROUP BY — для агрегации (схлопывает)."},
            ]),
            knowledge_checklist([
                "Использую ROW_NUMBER, RANK, DENSE_RANK",
                "Указываю ORDER BY внутри OVER",
                "Знаю разницу между ними",
            ]),
        ],
        exercises=[
            ex(1, "sql", "Пронумеруй игроков по убыванию score.",
               "SELECT name, ROW_NUMBER() OVER (ORDER BY score DESC) AS rn FROM players;\n",
               "SELECT name, ROW_NUMBER() OVER (ORDER BY score DESC) AS rn FROM players;",
               [{"check": "result[0]['name'] == 'Alice' and result[0]['rn'] == 1", "msg": "Alice под номером 1"}],
               ["ROW_NUMBER() OVER (ORDER BY score DESC)"], 2),
            ex(2, "sql", "Присвой ранг (RANK) по score DESC.",
               "SELECT name, RANK() OVER (ORDER BY score DESC) AS rnk FROM players;\n",
               "SELECT name, RANK() OVER (ORDER BY score DESC) AS rnk FROM players;",
               [{"check": "result[0]['rnk'] == 1", "msg": "Alice — ранг 1"}],
               ["RANK() OVER ..."], 2),
            ex(3, "sql", "Пронумеруй игроков внутри каждой команды (PARTITION BY team_id).",
               "SELECT name, ROW_NUMBER() OVER (PARTITION BY team_id ORDER BY score DESC) AS rn FROM players;\n",
               "SELECT name, ROW_NUMBER() OVER (PARTITION BY team_id ORDER BY score DESC) AS rn FROM players;",
               [{"check": "len(result) == 3", "msg": "3 строки"}],
               ["PARTITION BY team_id", "ROW_NUMBER OVER"], 3),
        ],
        minutes=35, difficulty=3,
    )


def _2_11():
    return lesson(
        "2.11", "Оконные функции: LAG, LEAD, SUM OVER, AVG OVER", "gaming", [
            theory(
                "**LAG(col, n)** — значение столбца n строк назад.\n"
                "**LEAD(col, n)** — значение n строк вперёд.\n"
                "**SUM/AVG OVER (...)** — накопительная сумма/среднее.\n\n"
                "```sql\nSELECT name, score,\n"
                "  LAG(score) OVER (ORDER BY score DESC) AS prev,\n"
                "  SUM(score) OVER (ORDER BY score DESC) AS cumsum\n"
                "FROM players;\n```"
            ),
            analogy(
                "LAG — посмотреть назад, LEAD — вперёд. SUM OVER — растущий итог.",
                "Разница с предыдущим днём: LAG(value) в оконной функции."
            ),
            visual(
                "Оконные функции LAG, LEAD и SUM OVER: показано, как из текущей строки «подглядывают» в соседние и считают накопительный итог.",
                r'''   Данные по дням (matches):
   ┌──────────┬────────┬────────┬────────┬──────────────┐
   │ day      │ score  │ LAG(1) │ LEAD(1)│ SUM OVER     │
   │          │        │ (prev) │ (next) │ (running tot)│
   │ ──────── ┼────────┼────────┼────────┼──────────────│
   │  1       │  10    │  NULL  │   20   │   10         │
   │  2       │  20    │   10   │   30   │   30         │  ← 10+20
   │  3       │  30    │   20   │   40   │   60         │  ← +30
   │  4       │  40    │   30   │  NULL  │  100         │  ← +40
   └──────────┴────────┴────────┴────────┴──────────────┘
                  ▲        ▲        ▲          ▲
                  │        │        │          │
                LAG(s,1) LEAD(s,1)   окно растёт →
                «назад»  «вперёд»   SUM OVER (ORDER BY day)

   Синтаксис:
   LAG(score)  OVER (ORDER BY day)
   LEAD(score) OVER (ORDER BY day)
   SUM(score)  OVER (ORDER BY day
                     ROWS BETWEEN UNBOUNDED PRECEDING
                              AND CURRENT ROW)'''
            ),
            example(
                "Накопительная сумма score.",
                "SUM(score) OVER (ORDER BY score DESC).",
                "SELECT name, score,\n"
                "  SUM(score) OVER (ORDER BY score DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumsum\n"
                "FROM players;",
                "Alice cumsum=1500, Bob cumsum=2300, Charlie cumsum=2900",
                "ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW — окно от начала до текущей."
            ),
            common_mistakes([
                {"mistake": "LAG без ORDER BY", "why_bad": "Неопределённый порядок", "fix": "OVER (ORDER BY ...)"},
            ]),
            interview_questions([
                {"q": "Что возвращает LAG на первой строке?",
                 "a": "NULL, потому что предыдущей нет. Можно задать дефолт: LAG(col, 1, 0)."},
                {"q": "Когда использовать SUM OVER вместо GROUP BY?",
                 "a": "Когда нужны детальные строки + агрегат: накопительная сумма, скользящее среднее."},
            ]),
            knowledge_checklist([
                "LAG/LEAD для доступа к соседним строкам",
                "SUM OVER для накопительных",
                "AVG OVER для скользящих средних",
            ]),
        ],
        exercises=[
            ex(1, "sql", "Покажи score и score предыдущего игрока (по убыванию).",
               "SELECT name, score, LAG(score) OVER (ORDER BY score DESC) AS prev FROM players;\n",
               "SELECT name, score, LAG(score) OVER (ORDER BY score DESC) AS prev FROM players;",
               [{"check": "result[1]['prev'] == 1500", "msg": "Bob prev=1500 (Alice)"}],
               ["LAG(score) OVER (ORDER BY ...)"], 2),
            ex(2, "sql", "Покажи score и следующий score (по возрастанию).",
               "SELECT name, score, LEAD(score) OVER (ORDER BY score ASC) AS next FROM players;\n",
               "SELECT name, score, LEAD(score) OVER (ORDER BY score ASC) AS next FROM players;",
               [{"check": "result[0]['next'] == 800", "msg": "Alice next=800 (Bob)"}],
               ["LEAD(score) OVER ..."], 2),
            ex(3, "sql", "Накопительная сумма score.",
               "SELECT name, SUM(score) OVER (ORDER BY score DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cs FROM players;\n",
               "SELECT name, SUM(score) OVER (ORDER BY score DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cs FROM players;",
               [{"check": "result[-1]['cs'] == 2900", "msg": "Итоговая сумма = 2900"}],
               ["SUM OVER ... ROWS BETWEEN ..."], 3),
        ],
        minutes=30, difficulty=3,
    )


def _2_12():
    return lesson(
        "2.12", "Продвинутые оконные функции: NTILE, PERCENT_RANK", "gaming", [
            theory(
                "**NTILE(n)** — делит строки на n групп одинакового размера.\n"
                "**PERCENT_RANK()** — относительный ранг (0..1).\n"
                "**CUME_DIST()** — кумулятивное распределение.\n\n"
                "```sql\nSELECT name, score,\n"
                "  NTILE(2) OVER (ORDER BY score DESC) AS half,\n"
                "  PERCENT_RANK() OVER (ORDER BY score) AS pr\n"
                "FROM players;\n```"
            ),
            analogy(
                "NTILE — разбить на N корзин: топ-25%, топ-50%. PERCENT_RANK — позиция в процентах.",
                "Разделить игроков на 4 квартиля по skill: NTILE(4)."
            ),
            visual(
                "NTILE(4) разбивает 8 строк на 4 бакеты по 2 строки, PERCENT_RANK считает относительную позицию от 0 до 1.",
                r'''   8 игроков (отсортированы по score DESC):
   ┌─────────┬───────┬─────────┬─────────────┐
   │ name    │ score │ NTILE(4)│ PERCENT_RANK│
   │ ────────┼───────┼─────────┼─────────────│
   │ Alice   │  2400 │   1     │   0.000     │  ← top
   │ Bob     │  2100 │   1     │   0.143     │
   │ Charlie │  1900 │   2     │   0.286     │
   │ Diana   │  1700 │   2     │   0.429     │
   │ Eve     │  1400 │   3     │   0.571     │
   │ Frank   │  1100 │   3     │   0.714     │
   │ Grace   │   800 │   4     │   0.857     │
   │ Henry   │   300 │   4     │   1.000     │  ← bottom
   └─────────┴───────┴─────────┴─────────────┘

   NTILE(4) — 4 «корзины» по ~2 строки:
   ┌──────┬──────┬──────┬──────┐
   │ top  │      │      │ bot  │
   │ 25%  │      │      │ 25%  │
   │ ██   │ ██   │ ██   │ ██   │
   │ ██   │ ██   │ ██   │ ██   │
   └──────┴──────┴──────┴──────┘

   PERCENT_RANK = (rank − 1) / (N − 1)   ∈ [0, 1]'''
            ),
            example(
                "Раздели игроков на 2 группы по score.",
                "NTILE(2).",
                "SELECT name, score,\n"
                "  NTILE(2) OVER (ORDER BY score DESC) AS half\n"
                "FROM players;",
                "Alice half=1, Bob half=1, Charlie half=2",
                "NTILE(2) — 2 группы, по убыванию. 3 строки → группа 1 (Alice, Bob), группа 2 (Charlie)."
            ),
            common_mistakes([
                {"mistake": "Ожидать ровно n в каждой группе", "why_bad": "При нечётком делении — разные", "fix": "NTILE старается, но ±1 разница возможна"},
            ]),
            interview_questions([
                {"q": "PERCENT_RANK vs CUME_DIST?",
                 "a": "PERCENT_RANK: (rank-1)/(N-1). CUME_DIST: кол-во <= текущего / N."},
            ]),
            knowledge_checklist([
                "NTILE для квантилей",
                "PERCENT_RANK для процентилей",
            ]),
        ],
        exercises=[
            ex(1, "sql", "Раздели игроков на 2 группы по score (NTILE).",
               "SELECT name, NTILE(2) OVER (ORDER BY score DESC) AS grp FROM players;\n",
               "SELECT name, NTILE(2) OVER (ORDER BY score DESC) AS grp FROM players;",
               [{"check": "max(r['grp'] for r in result) == 2", "msg": "2 группы"}],
               ["NTILE(2) OVER"], 2),
            ex(2, "sql", "Посчитай percent_rank по score.",
               "SELECT name, PERCENT_RANK() OVER (ORDER BY score) AS pr FROM players;\n",
               "SELECT name, PERCENT_RANK() OVER (ORDER BY score) AS pr FROM players;",
               [{"check": "len(result) == 3", "msg": "3 строки"}],
               ["PERCENT_RANK() OVER"], 3),
        ],
        minutes=25, difficulty=3,
    )


def _2_13():
    return lesson(
        "2.13", "Индексы и оптимизация запросов", "gaming", [
            theory(
                "**Индекс** — структура для быстрого поиска (аналог оглавления в книге).\n\n"
                "```sql\nCREATE INDEX idx_player_score ON players(score);\n"
                "DROP INDEX idx_player_score;\n```\n\n"
                "**Советы по оптимизации:**\n"
                "- Индексируй столбцы в WHERE, JOIN, ORDER BY\n"
                "- Избегай SELECT * в продакшне\n"
                "- Используй EXPLAIN для анализа"
            ),
            analogy(
                "Индекс — оглавление книги. Без него перелистываешь все страницы. С ним — сразу к нужной.",
                "CREATE INDEX на players.score ускоряет WHERE score > 1000."
            ),
            visual(
                "B-tree индекс как сбалансированное дерево: корневой узел → промежуточные → листья со значениями и указателями на строки.",
                r'''                Без индекса (full scan):
   ┌──────────────────────────────────┐    SELECT * FROM players
   │  1 Alice  1500  red  ░░░░░░░░    │    WHERE score > 1000;
   │  2 Bob     800  red  ░░░░░░░░    │    нужно прочитать ВСЕ строки
   │  3 Charlie 600 blue ░░░░░░░░    │    O(N) — медленно
   │  4 Diana  2200 blue ░░░░░░░░    │
   │  ...                             │
   └──────────────────────────────────┘

                С B-tree индексом по score:
                          ┌─────────┐
                          │  [1500] │ ← корень
                          └────┬────┘
                  ┌────────────┴────────────┐
              ┌───┴───┐                ┌────┴────┐
              │[<1500]│                │[>= 1500]│
              └───┬───┘                └────┬────┘
              ┌───┴───┐                ┌────┴────┐
              ▼       ▼                ▼         ▼
           [600]   [800..1400]    [1500,2200]   [...]
            ↓        ↓               ↓
         строки   строки         строки → WHERE score>1000
         (листья)                находит за O(log N)

   Стоимость: индекс замедляет INSERT/UPDATE (обновлять дерево)
   Выгода:    SELECT по индексированному столбцу — на порядки быстрее'''
            ),
            example(
                "Создай индекс на столбец score, проверь EXPLAIN.",
                "CREATE INDEX ... ON ...;",
                "CREATE INDEX idx_players_score ON players(score);\n\n"
                "EXPLAIN QUERY PLAN\n"
                "SELECT * FROM players WHERE score > 1000;",
                "Использует индекс idx_players_score",
                "EXPLAIN показывает план запроса: какие индексы использованы, как сканируется таблица."
            ),
            common_mistakes([
                {"mistake": "Индексировать всё подряд", "why_bad": "Замедляет INSERT/UPDATE", "fix": "Только часто используемые в WHERE/JOIN"},
                {"mistake": "SELECT * в больших таблицах", "why_bad": "Тянет ненужные данные", "fix": "Указывай конкретные столбцы"},
            ]),
            interview_questions([
                {"q": "B-tree vs Hash индекс?",
                 "a": "B-tree — диапазоны (>, <, BETWEEN), сортировка. Hash — только равенство (=)."},
                {"q": "Что такое композитный индекс?",
                 "a": "Индекс по нескольким столбцам: CREATE INDEX ON players(team_id, score). Порядок важен."},
            ]),
            knowledge_checklist([
                "Создаю индекс через CREATE INDEX",
                "Использую EXPLAIN для анализа",
                "Понимаю trade-off: индексы ускоряют SELECT, замедляют запись",
            ]),
        ],
        exercises=[
            ex(1, "sql", "Создай индекс на score в таблице players.",
               "CREATE INDEX idx_score ON ?(score);\n",
               "CREATE INDEX idx_score ON players(score);",
               [{"check": "'CREATE INDEX' in query.upper() and 'players' in query and 'score' in query", "msg": "CREATE INDEX на players(score)"}],
               ["CREATE INDEX name ON table(col)"], 2),
            ex(2, "sql", "Проверь план запроса SELECT * FROM players WHERE score > 1000 через EXPLAIN.",
               "EXPLAIN QUERY PLAN SELECT * FROM players WHERE score > 1000;\n",
               "EXPLAIN QUERY PLAN SELECT * FROM players WHERE score > 1000;",
               [{"check": "'EXPLAIN' in query.upper()", "msg": "EXPLAIN"}],
               ["EXPLAIN QUERY PLAN"], 2),
        ],
        minutes=30, difficulty=3,
    )


def _2_14():
    return lesson(
        "2.14", "Мини-проект: Аналитика игровой платформы", "gaming", [
            theory(
                "В этом мини-проекте ты применишь все знания SQL на реальной аналитической задаче.\n\n"
                "**Дано:** база данных игровой платформы с таблицами:\n"
                "- `players` (id, name, registration_date)\n"
                "- `sessions` (id, player_id, game_id, start_time, duration_minutes)\n"
                "- `purchases` (id, player_id, amount, purchase_date)\n"
                "- `matches` (id, game_id, winner_id, loser_id, match_date)\n\n"
                "**Задачи:**\n"
                "1. Топ-10 игроков по сумме покупок\n"
                "2. Средний чек покупки\n"
                "3. Retention (вернулись ли на 7 день)\n"
                "4. Самые популярные игры"
            ),
            analogy(
                "Аналитик игровой платформы — то же, что Data Analyst в любой компании: данные → запросы → инсайты для продукта.",
                "Wargaming, Valve, Riot — все используют SQL для аналитики."
            ),
            visual(
                "End-to-end SQL-конвейер аналитики игровой платформы: несколько таблиц JOIN → группировка → метрики → инсайты.",
                r'''   ┌──────────┐  ┌──────────┐  ┌────────────┐  ┌──────────┐
   │ players  │  │ sessions │  │ purchases  │  │ matches  │
   │ id,name  │  │ id,pid,  │  │ id,pid,    │  │ id,wid,  │
   │ reg_date │  │ game,    │  │ amount,    │  │ lid,date │
   │          │  │ dur,time │  │ date       │  │          │
   └────┬─────┘  └────┬─────┘  └─────┬──────┘  └────┬─────┘
        │             │              │              │
        └──────┬──────┴──────┬───────┴──────┬───────┘
               │             │              │
               ▼             ▼              ▼
         ┌──────────────────────────────────────┐
         │  JOIN по player_id, game_id          │  CTE / подзапросы
         │  WHERE date BETWEEN ... AND ...      │  фильтры по дате
         └──────────────┬──────────────────────┘
                        │  сырые объединённые строки
                        ▼
         ┌──────────────────────────────────────┐
         │  GROUP BY player / game / team       │  агрегация
         │  SUM, COUNT, AVG, COUNT(DISTINCT)    │
         └──────────────┬──────────────────────┘
                        │  метрики
                        ▼
         ┌──────────────────────────────────────┐
         │  HAVING / ORDER BY / LIMIT           │  топ-N, пороги
         └──────────────┬──────────────────────┘
                        │  результат
                        ▼
         ┌──────────────────────────────────────┐
         │  📊 Инсайты:                         │
         │  • Топ-10 покупателей (LTV)           │
         │  • Retention day-7                    │
         │  • Самые популярные игры             │
         │  • Средний чек / ARPU                │
         └──────────────────────────────────────┘'''
            ),
            example(
                "Решение: топ-10 покупателей.",
                "JOIN + GROUP BY + ORDER BY + LIMIT.",
                "SELECT p.name, SUM(pu.amount) AS total\n"
                "FROM players p\n"
                "JOIN purchases pu ON p.id = pu.player_id\n"
                "GROUP BY p.id, p.name\n"
                "ORDER BY total DESC\n"
                "LIMIT 10;",
                "Топ-10 покупателей с суммами",
                "JOIN связывает players и purchases. GROUP BY + SUM считает сумму по игроку. ORDER BY + LIMIT — топ."
            ),
            common_mistakes([
                {"mistake": "Забыл GROUP BY по тому же столбцу, что и в SELECT", "why_bad": "Не сгруппирует правильно", "fix": "Все столбцы в SELECT — либо в GROUP BY, либо в агрегате"},
                {"mistake": "JOIN без ON", "why_bad": "Декартово произведение", "fix": "Указывай ON"},
            ]),
            interview_questions([
                {"q": "Что такое retention и как его считать в SQL?",
                 "a": "Доля пользователей, вернувшихся через N дней. Считается через JOIN сессий с самими собой или оконные функции."},
                {"q": "LTV в SQL?",
                 "a": "LTV = сумма покупок за всё время. SELECT player_id, SUM(amount) FROM purchases GROUP BY player_id."},
            ]),
            knowledge_checklist([
                "Соединяю 3+ таблиц",
                "Группирую и фильтрую",
                "Сортирую и лимитирую",
                "Считаю retention и LTV",
            ]),
        ],
        exercises=[
            ex(1, "sql", "Найди топ-2 игроков по сумме покупок (JOIN players + purchases, GROUP BY, ORDER BY DESC, LIMIT 2).",
               "SELECT p.name, SUM(pu.amount) AS total FROM players p JOIN purchases pu ON p.id = pu.player_id GROUP BY p.id ORDER BY total DESC LIMIT 2;\n",
               "SELECT p.name, SUM(pu.amount) AS total FROM players p JOIN purchases pu ON p.id = pu.player_id GROUP BY p.id ORDER BY total DESC LIMIT 2;",
               [{"check": "len(result) == 2 and result[0]['total'] >= result[1]['total']", "msg": "2 игрока, по убыванию"}],
               ["JOIN ... ON", "GROUP BY p.id", "ORDER BY total DESC", "LIMIT 2"], 3),
            ex(2, "sql", "Посчитай общее количество сессий.",
               "SELECT ?(*) FROM sessions;\n",
               "SELECT COUNT(*) FROM sessions;",
               [{"check": "result[0]['COUNT(*)'] >= 0", "msg": "Любое неотрицательное"}],
               ["COUNT(*)"], 1),
            ex(3, "sql", "Средняя продолжительность сессии в минутах.",
               "SELECT ?(duration_minutes) FROM sessions;\n",
               "SELECT AVG(duration_minutes) FROM sessions;",
               [{"check": "isinstance(result[0]['AVG(duration_minutes)'], (int, float))", "msg": "Среднее — число"}],
               ["AVG(column)"], 2),
        ],
        minutes=90, difficulty=4,
    )


LESSONS = [_2_8, _2_9, _2_10, _2_11, _2_12, _2_13, _2_14]
