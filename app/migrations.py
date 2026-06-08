# -*- coding: utf-8 -*-
"""
Auto-migrations — run after DB seed to bring the course to 100% Google standards.
Called automatically from run.py — no separate step needed.
"""

import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "course.db")

def _conn():
    return sqlite3.connect(DB_PATH)

def _exists(cur, table, col, val):
    return cur.execute(f"SELECT 1 FROM {table} WHERE {col}=?", (val,)).fetchone()

def run_migrations():
    conn = _conn()
    cur = conn.cursor()

    # Only run seeding-related steps if lesson 3.13 doesn't exist yet
    if not _exists(cur, "lessons", "number", "3.13"):
        print("[migrate] Seeding new lessons...")
        _add_new_lessons(conn)
        _add_exercises(conn)
        _add_middle_iq(conn)
        _add_3rd_capstone(conn)
        print("[migrate] Seed migrations done.")

    # Content expansions - always safe to re-apply (they skip if already expanded)
    print("[migrate] Applying content expansions...")
    _expand_thin_lessons(conn)
    _add_bi_tools_mention(conn)
    _add_stakeholder_mention(conn)
    _fix_quality_issues(conn)
    _add_roleplay_dialogues(conn)
    _add_augmented_lessons(conn)
    _add_presentation_improvements(conn)
    _add_block11_project(conn)
    print("[migrate] Content expansions done.")

    conn.close()

def _expand_thin_lessons(conn):
    """Expand 26 thin concept lessons (theory < 800 chars) with 'Подробнее:' sections."""
    c = conn.cursor()
    expansions = {
        "1.8": "\n\n**Подробнее: основные приёмы работы со строками в Data Science**\n\nСтроки в Python — один из самых частых типов данных в реальных проектах. Иммутабельность означает, что любой метод возвращает **новую** строку. Полезные методы для EDA: s.strip(), s.split(','), s.isdigit(), s.startswith('http'). f-строки — стандарт с Python 3.6, читаемее конкатенации.",
        "1.10": "\n\n**Подробнее: CSV как основной формат обмена данными**\n\nCSV — самый распространённый текстовый формат для табличных данных. Преимущества: читается любым редактором, поддерживается всеми BI-инструментами. Для файлов >100 МБ используйте csv.reader (не DictReader). Проблемы: разделитель (',' vs ';'), кодировки (всегда encoding='utf-8'), кавычки внутри полей, пропуски.",
        "1.11": "\n\n**Подробнее: обработка ошибок в DS-проектах**\n\nВ Data Science исключения возникают постоянно: файл не найден, данные в неверном формате, модель не сходится. Правильная обработка — не подавление, а реакция. Иерархия: except: ловит всё (включая SystemExit) vs except Exception: (только ошибки). else-блок выполняется при успехе try. Свои исключения наследуйте от Exception.",
        "3.1": "\n\n**Подробнее: почему NumPy быстрее списков Python?**\n\nndarray хранит однородные данные в непрерывном блоке памяти — скорость в 10-100x быстрее циклов Python. Broadcasting — автоматическое растягивание меньшего массива. ufunc (np.sqrt, np.log, np.exp) — поэлементно без циклов. Бенчмарк: 10^6 элементов — Python 0.3s, NumPy 0.003s.",
        "3.2": "\n\n**Подробнее: эффективная индексация для EDA**\n\nБулевы маски — самый частый паттерн: arr[(arr > 10) & (arr < 20)] используйте & (не and). Fancy indexing: arr[[0, 3, 7]]. Срезы возвращают view (не копию). Для копии — arr[2:5].copy(). Многомерная: arr2d[0, :] — первая строка, arr2d[:, 1] — второй столбец.",
        "3.3": "\n\n**Подробнее: Pandas — швейцарский нож DS**\n\nDataFrame как лист Excel без ограничения строк. Создание: pd.read_csv, read_excel, read_sql. info()/describe()/nunique()/sample() — быстрый осмотр. Методы chain: df.dropna().query('value>0').groupby('cat').mean() — большинство возвращает новый DataFrame.",
        "3.4": "\n\n**Подробнее: импорт данных в реальных проектах**\n\nВсегда указывайте параметры явно: sep=',' encoding='utf-8' na_values=['NA',''] parse_dates=['date']. pd.json_normalize() для API-ответов. read_excel(..., sheet_name=None) — все листы. pd.read_sql(query, conn) — SQL прямо в DataFrame. Пароли — в .env, не в коде.",
        "3.5": "\n\n**Подробнее: фильтрация — основа EDA**\n\nБулева индексация: df[(df['age']>18) & (df['status']=='active')]. .query() — читаемый синтаксис: df.query('age>18 and status==\"active\"'). isin — фильтр по набору: df[df['planet'].isin(['Mars','Venus'])]. .loc и .iloc — по меткам и позициям.",
        "3.6": "\n\n**Подробнее: стратегии работы с пропусками**\n\nТипы пропусков: MCAR (случайные), MAR (зависят от других переменных), MNAR (зависят от самого значения). Стратегии: dropna(), fillna(mean), fillna(method='ffill') для временных рядов, KNNImputer. Золотое правило: не заполняйте пропуски до EDA — сначала поймите их природу.",
        "3.7": "\n\n**Подробнее: дубликаты и выбросы**\n\nДубликаты: df.duplicated() — булева маска, df.drop_duplicates() — удаление. Выбросы: IQR (Q1-1.5*IQR, Q3+1.5*IQR), Z-score (|z|>3), Isolation Forest для многомерных. Действия: исследовать (ошибка или реальное явление?), winsorize для линейных моделей, оставить для деревьев.",
        "3.8": "\n\n**Подробнее: Split-Apply-Combine**\n\ndf.groupby('cat')['val'].sum() — разделить → применить → объединить. Множественные агрегации: .agg(['sum','mean','std']). .transform возвращает ту же форму: df.groupby('cat')['val'].transform(lambda x: (x-x.mean())/x.std()). as_index=False для плоского результата.",
        "3.9": "\n\n**Подробнее: объединение таблиц**\n\npd.merge(df1, df2, on='key', how='inner') — SQL-аналог. how='left'/'right'/'outer'. left_on/right_on для разных имён. df1.join(df2) — по индексу. pd.concat([df1, df2], axis=0) — как UNION ALL. Проверяйте кол-во строк после merge (many-to-many → декартово произведение).",
        "3.10": "\n\n**Подробнее: pivot vs melt**\n\npivot: из длинного в широкий (категория → колонки). pivot_table — с агрегацией (аналог сводной Excel). melt: из широкого в длинный (столбцы → строки). stack/unstack — работа с MultiIndex. Для визуализации нужен длинный формат (melt), для отчётов — широкий (pivot).",
        "3.11": "\n\n**Подробнее: даты в Data Science**\n\npd.to_datetime() — парсинг. dt.year/month/day/dayofweek/quarter — извлечение. resample('D').mean() — смена частоты. shift(1) — лаг. pct_change() — процентное изменение. Циклические признаки: sin(2π·hour/24), cos(2π·hour/24). Часовые пояса: tz_localize/tz_convert.",
        "7.1": "\n\n**Подробнее: ландшафт машинного обучения**\n\nSupervised (X → y): регрессия (число) и классификация (категория). Unsupervised (только X): кластеризация (K-Means, DBSCAN), снижение размерности (PCA, t-SNE), обнаружение аномалий. Reinforcement Learning: агент + среда + награда. ~80% бизнес-задач — supervised.",
        "7.4": "\n\n**Подробнее: метрики регрессии**\n\nMAE — средняя абсолютная ошибка (интерпретируема). MSE — квадратичная (штрафует выбросы). RMSE = √MSE — в единицах y. R² — доля объяснённой дисперсии (1 = идеал, 0 = уровень среднего). Если RMSE >> MAE — есть большие выбросы. MAPE — средняя процентная ошибка (для бизнеса).",
        "7.5": "\n\n**Подробнее: метрики классификации**\n\nAccuracy бесполезна при дисбалансе (99% 'нет' → 99%, но модель ничего не ловит). Confusion matrix: TP/TN/FP/FN. Precision = TP/(TP+FP) — точность. Recall = TP/(TP+FN) — полнота. F1 = 2PR/(P+R) — гармоническое среднее. ROC-AUC — вероятность верного ранжирования пары.",
        "7.6": "\n\n**Подробнее: линейная регрессия**\n\ny = w₁x₁ + w₂x₂ + ... + b. Коэффициенты — change in y per unit x. Assumptions: линейность, независимость ошибок, гомоскедастичность, нормальность остатков, отсутствие мультиколлинеарности. Диагностика: график y_pred vs residuals. R² в соц.науках ~0.3 норма, в физике >0.9.",
        "7.7": "\n\n**Подробнее: логистическая регрессия**\n\nКлассификация, несмотря на название. Выход — вероятность через sigmoid: σ(z)=1/(1+e⁻ᶻ). Порог по умолчанию 0.5, но калибруется. Коэффициенты — log odds: exp(w) — отношение шансов. Log Loss штрафует за уверенные ошибки. OvR vs Multinomial для многоклассовой.",
        "8.2": "\n\n**Подробнее: создание новых признаков**\n\nDomain: отношения, разницы, агрегации. Время: скользящие средние, лаги, разница от среднего. Взаимодействия: произведение (площадь), полиномы (x², x³). Текст: длина, кол-во слов, ключевые слова. Правило: признак только если есть бизнес-смысл — иначе overfitting.",
        "8.3": "\n\n**Подробнее: кодирование категорий**\n\nLabel Encoding: {'Mars':0, 'Venus':1} — опасно (модель думает Venus > Mars). One-Hot: K колонок — стандарт. Ordinal: для порядка {'low':0, 'medium':1, 'high':2}. Target Encoding: среднее target по категории — мощно, но риск leakage. Frequency Encoding: частота встречаемости.",
        "8.5": "\n\n**Подробнее: извлечение признаков из дат**\n\nИз одной даты — 10+ признаков. Циклические: sin(2π·час/24), cos(2π·час/24). Разницы: (today - signup).days — tenure. Rolling: сумма/среднее/std за 7/30 дней. Expanding: cumsum(). Бинарные: is_weekend, is_holiday, is_business_hours, season.",
        "10.2": "\n\n**Подробнее: Python для собеседования**\n\nMutable vs immutable: list/dict/set vs int/str/tuple. Генераторы: yield vs return. Декораторы: functools.wraps. Контекстные менеджеры: __enter__/__exit__. GIL: threading бесполезен для CPU-bound. Type hints: Optional, Union, List[int]. dataclass для конфигов.",
        "10.4": "\n\n**Подробнее: SQL для собеседования**\n\nПорядок выполнения: FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT. JOIN: INNER/LEFT/RIGHT/FULL/CROSS/SELF. HAVING — WHERE для агрегатов. Оконные функции: ROW_NUMBER, RANK, LAG, LEAD, SUM OVER. NULL: COALESCE, IS NULL, NULL != NULL.",
        "10.5": "\n\n**Подробнее: продвинутый SQL**\n\nCTE (WITH) — именованные подзапросы, можно цепочкой. Рекурсивные CTE — для деревьев. Временные таблицы: CREATE TEMP TABLE. Pivot: SUM(CASE WHEN ...). NTILE(4) — квартили. EXPLAIN ANALYZE — план запроса. NOT IN медленнее NOT EXISTS.",
        "10.6": "\n\n**Подробнее: статистика для собеседования**\n\nСреднее vs медиана (устойчивость). Стандартное отклонение — разброс. Распределения: нормальное, биномиальное, Пуассона, экспоненциальное, равномерное. CLT: среднее выборки ≈ нормально при n>30. p-value — не вероятность H0, а вероятность данных при H0.",
    }

    for num, addendum in expansions.items():
        row = c.execute("SELECT id, content_json FROM lessons WHERE number=?", (num,)).fetchone()
        if not row:
            continue
        lid, content_json = row
        data = json.loads(content_json)
        for s in data['sections']:
            if s['type'] == 'theory':
                old = s['content']
                if "Подробнее" in old:
                    continue  # already expanded
                s['content'] = old + addendum
                break
        c.execute("UPDATE lessons SET content_json=? WHERE id=?", (json.dumps(data, ensure_ascii=False), lid))
    conn.commit()

def _add_bi_tools_mention(conn):
    c = conn.cursor()
    row = c.execute("SELECT id, content_json FROM lessons WHERE number='4.9'").fetchone()
    if not row:
        return
    lid, content_json = row
    data = json.loads(content_json)
    for s in data['sections']:
        if s['type'] == 'theory':
            if "Tableau" in s['content']:
                return  # already added
            s['content'] = s['content'] + (
                '\n\n**Инструменты визуализации в Data Science:**\n'
                'Помимо Python-библиотек (Matplotlib, Seaborn, Plotly), '
                'в индустрии активно используют BI-инструменты:\n'
                '- **Tableau** — drag-and-drop дашборды, подключение к любым БД\n'
                '- **Google Looker** — облачная BI-платформа с LookML\n'
                '- **Google Sheets / Excel** — ad-hoc отчёты и сводные таблицы\n\n'
                'Для DS важно владеть как Python-библиотеками, так и BI-инструментами '
                '(для дашбордов и презентаций заказчику).'
            )
            break
    c.execute("UPDATE lessons SET content_json=? WHERE id=?", (json.dumps(data, ensure_ascii=False), lid))
    conn.commit()

def _add_stakeholder_mention(conn):
    c = conn.cursor()
    row = c.execute("SELECT id, content_json FROM lessons WHERE number='9.4'").fetchone()
    if not row:
        return
    lid, content_json = row
    data = json.loads(content_json)
    for s in data['sections']:
        if s['type'] == 'theory':
            if "стейкхолдер" in s['content']:
                return  # already added
            s['content'] = s['content'] + (
                '\n\n**Взаимодействие с заказчиком (stakeholder interview):**\n'
                'Перед ML-проектом проведите интервью со стейкхолдерами — '
                'это Business Understanding в CRISP-DM. Выясните: (1) бизнес-проблему, '
                '(2) KPI (не accuracy, а конверсия), (3) доступ к данным, '
                '(4) как используют результаты. SMART: Specific, Measurable, '
                'Achievable, Relevant, Time-bound.'
            )
            break
    c.execute("UPDATE lessons SET content_json=? WHERE id=?", (json.dumps(data, ensure_ascii=False), lid))
    conn.commit()

def _add_new_lessons(conn):
    c = conn.cursor()
    # lesson data inline - same as 01_add_lessons.py
    lessons_data = [
        {
            "bn": 3, "num": "3.13",
            "title": "Power analysis: расчёт размера выборки",
            "sections": {
                "prerequisites": {"items": ["Урок 3.11: Работа с датами и временными рядами", "Урок 3.12: Мини-проект: Очистка данных"]},
                "learning_objectives": {"items": ["Применяю: рассчитываю размер выборки для A/B теста", "Знаю: alpha, beta, effect size, power", "Умею: интерпретировать power analysis"]},
                "theory": {"content": "**Power analysis** — расчёт минимального размера выборки для обнаружения эффекта заданной величины. Компоненты: α (false positive, обычно 0.05), β (false negative), Power = 1 - β (target ≥ 0.8), effect size (Cohen's d для средних, h для пропорций).\n\nФормула для разницы средних: n = 2 · (Z_α/2 + Z_β)² / d²\n\n**statsmodels** имеет `NormalIndPower().solve_power()`, `TTestIndPower()`. В Python: `from statsmodels.stats.power import NormalIndPower`.\n\nБез power analysis A/B тест может пропустить реальный эффект (low power) или потратить лишние ресурсы (oversized sample)."},
                "summary": {"items": ["✓ Рассчитываю n для A/B теста", "✓ Понимаю trade-off alpha/beta/n", "✓ Использую statsmodels для power"]},
                "glossary": {"items": [{"term": "Power (1-β)", "definition": "Вероятность обнаружить эффект, когда он есть"}, {"term": "Effect size (Cohen's d)", "definition": "Стандартизованная мера разницы между группами"}, {"term": "MDE", "definition": "Minimum Detectable Effect — минимальный эффект, который обнаружит тест"}]},
                "analogy": {"real_world": "Поиск иголки в стоге сена: power = вероятность заметить иголку, если она там. Чем больше стог (выборка), тем выше шанс.", "domain_example": "A/B тест конверсии: baseline 5%, MDE +10% → 3502 пользователя в每组. Меньше — риск false negative."},
                "visual": {"description": "Связь n, effect size и power", "ascii_diagram": "Power=0.8: d=0.5 → n=63  |  d=0.3 → n=175  |  d=0.1 → n=1570"},
                "example": {"problem": "Рассчитайте размер выборки: baseline 5%, ожидаемый эффект +20%, α=0.05, power=0.8", "solution_explanation": "Используем NormalIndPower с proportion_effectsize для пропорций", "code": "from statsmodels.stats.power import NormalIndPower\nfrom statsmodels.stats.proportion import proportion_effectsize\n\np1, p2 = 0.05, 0.06\nalpha, power = 0.05, 0.8\neffect = proportion_effectsize(p1, p2)\nn = NormalIndPower().solve_power(effect, alpha=alpha, power=power)\nprint(f'Нужно {n:.0f} пользователей в каждой группе')", "output": "Нужно 3502 пользователей в каждой группе", "output_explanation": "solve_power возвращает n на одну группу. Чем меньше эффект, тем больше n."},
                "common_mistakes": {"items": [{"mistake": "A/B тест без power analysis", "why_bad": "Риск false negative при малом n", "fix": "Заранее рассчитайте n на основе MDE"}, {"mistake": "Power=0.5 считается достаточным", "why_bad": "50% шанс пропустить эффект", "fix": "Цель — power ≥ 0.8"}, {"mistake": "Путать power с α", "why_bad": "α — false positive, power — true positive", "fix": "α = P(отвергнуть H0|H0), power = P(отвергнуть H0|H1)"}]},
                "further_reading": {"items": [{"title": "StatsModels Power", "url": "https://www.statsmodels.org/stable/stats.html#power-and-sample-size"}, {"title": "Power Analysis (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Power_of_a_test"}]},
                "interview_questions": {"items": [{"q": "Что такое power analysis?", "a": "Расчёт минимального n для обнаружения эффекта. Параметры: α, β (power=1-β), effect size, n. Без него A/B тест — гадание."}, {"q": "Как эффект size влияет на n?", "a": "Обратно квадратично: d↓ в 2 раза → n↑ в 4 раза. Малые эффекты требуют огромных выборок."}]},
                "knowledge_checklist": {"items": ["Рассчитываю n через statsmodels", "Понимаю power/alpha/beta trade-off", "Анализирую MDE для A/B тестов"]}
            }
        },
        {
            "bn": 5, "num": "5.11",
            "title": "Обнаружение аномалий",
            "sections": {
                "prerequisites": {"items": ["Урок 5.9: A/B тестирование: практика", "Урок 5.10: Мини-проект: A/B тест"]},
                "learning_objectives": {"items": ["Применяю: Z-score и IQR для выбросов", "Знаю: Isolation Forest", "Умею: отличать аномалии от шума"]},
                "theory": {"content": "**Аномалии** — точки данных, значительно отличающиеся от остальных. Не все аномалии — ошибки; некоторые — важные сигналы (мошенничество, всплеск трафика, поломка датчика).\n\n**Методы:**\n- **Z-score**: (x - μ) / σ, порог |z| > 3. Чувствителен к выбросам в μ/σ.\n- **IQR**: Q1 - 1.5·IQR, Q3 + 1.5·IQR. Стабильнее Z-score.\n- **Isolation Forest**: ансамбль деревьев, изолирующих аномалии за меньшее число разрезов. Работает для многомерных данных.\n- **DBSCAN**: кластеризация — точки без соседей = шум (-1).\n- **LOF (Local Outlier Factor)**: локальная плотность vs соседи."},
                "summary": {"items": ["✓ Использую IQR и Z-score для одномерных выбросов", "✓ Применяю Isolation Forest для многомерных", "✓ Понимаю разницу между шумом и аномалией"]},
                "glossary": {"items": [{"term": "Isolation Forest", "definition": "Ансамбль изолирующих деревьев для детекции аномалий"}, {"term": "LOF (Local Outlier Factor)", "definition": "Локальное отклонение плотности — аномалии там, где плотность резко падает"}, {"term": "Contamination", "definition": "Ожидаемая доля аномалий в данных (параметр IF)"}]},
                "analogy": {"real_world": "Охранник на входе: большинство проходит спокойно (норма), но кто-то бежит или прячется (аномалия). Isolation Forest — как несколько охранников с разных ракурсов.", "domain_example": "Транзакции: 99% на сумму 100-500 руб за 10-30 сек. Аномалия: 50 000 руб за 2 сек — потенциальное мошенничество."},
                "visual": {"description": "Isolation Forest на 2D данных", "ascii_diagram": "Синие точки (норма) сконцентрированы, красные (аномалии) — изолированы далеко"},
                "example": {"problem": "Обнаружьте аномалии в транзакциях: 1000 нормальных (mean=500, std=100) + 30 аномалий (uniform 0-3000)", "code": "import numpy as np\nfrom sklearn.ensemble import IsolationForest\n\nnp.random.seed(42)\nnormal = np.random.normal(500, 100, (1000, 2))\nanomalies = np.random.uniform(0, 3000, (30, 2))\nX = np.vstack([normal, anomalies])\n\nmodel = IsolationForest(contamination=0.03, random_state=42)\npreds = model.fit_predict(X)\nprint(f'Аномалий: {(preds == -1).sum()}')", "output": "Аномалий: 30", "output_explanation": "Isolation Forest правильно обнаружил 30 точек-аномалий. fit_predict возвращает 1 (норма) и -1 (аномалия)."},
                "common_mistakes": {"items": [{"mistake": "Удалять все аномалии без исследования", "why_bad": "Аномалия может быть важным сигналом (мошенничество)", "fix": "Исследуйте: ошибка ввода или реальное явление?"}, {"mistake": "Z-score на данных с несколькими выбросами", "why_bad": "Выбросы искажают μ и σ", "fix": "Используйте IQR или modified Z-score с MAD"}, {"mistake": "contamination=0.5", "why_bad": "Ожидать 50% аномалий бессмысленно", "fix": "contamination = разумная доля (0.01-0.05)"}]},
                "further_reading": {"items": [{"title": "Isolation Forest (sklearn)", "url": "https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html"}, {"title": "Anomaly Detection (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Anomaly_detection"}]},
                "interview_questions": {"items": [{"q": "Чем Isolation Forest отличается от DBSCAN?", "a": "IF обучает модель аномальности (изоляция), DBSCAN кластеризует и помечает редкие точки как шум."}, {"q": "Когда Z-score не работает?", "a": "При нескольких выбросах (искажают μ/σ), при ненормальном распределении, при мультимодальности."}]},
                "knowledge_checklist": {"items": ["Детектирую выбросы IQR/Z-score", "Применяю Isolation Forest", "Интерпретирую результаты"]}
            }
        },
        {
            "bn": 5, "num": "5.12",
            "title": "Прогноз временных рядов",
            "sections": {
                "prerequisites": {"items": ["Урок 5.11: Обнаружение аномалий", "Урок 3.11: Работа с датами"]},
                "learning_objectives": {"items": ["Применяю: декомпозицию временного ряда", "Знаю: ARIMA и Prophet", "Умею: оценивать качество прогноза"]},
                "theory": {"content": "**Временной ряд** — последовательность точек данных, упорядоченных во времени. Ключевые компоненты: тренд (долгосрочное направление), сезонность (повторяющийся паттерн), цикл (длинные волны), остаток (шум).\n\n**Декомпозиция:** `seasonal_decompose(series, model='additive', period=12)` — разлагает на trend, seasonal, resid.\n\n**Модели прогноза:**\n- **ARIMA**: авторегрессия + скользящее среднее + дифференцирование. p,d,q — порядки.\n- **Prophet** (Facebook): тренд + сезонность + праздники. Робастен к пропускам.\n- **LSTM** (глубокое обучение): для сложных нелинейных рядов.\n\n**Метрики:** RMSE, MAE, MAPE (процентная ошибка)."},
                "summary": {"items": ["✓ Декомпозирую временной ряд", "✓ Строю прогноз Prophet/ARIMA", "✓ Оцениваю точность прогноза"]},
                "glossary": {"items": [{"term": "Stationarity", "definition": "Стационарность — μ и σ не меняются со временем. Требуется для ARIMA"}, {"term": "ACF / PACF", "definition": "Автокорреляция и частная автокорреляция — для выбора p,q в ARIMA"}, {"term": "Seasonality", "definition": "Повторяющийся паттерн с фиксированным периодом (день, неделя, год)"}]},
                "analogy": {"real_world": "Прогноз погоды: знаем, что зимой холодно (сезонность), глобальное потепление (тренд), но конкретная температура завтра — остаток.", "domain_example": "Продажи: ежегодный рост 20% (тренд) + пик в декабре (сезонность) + случайные колебания."},
                "visual": {"description": "Декомпозиция временного ряда на 3 компонента", "ascii_diagram": "Observed → Trend (линия вверх) → Seasonal (волна) → Residual (шум)"},
                "example": {"problem": "Разложите временной ряд продаж на компоненты и сделайте прогноз на 12 месяцев", "code": "import pandas as pd\nimport numpy as np\nfrom statsmodels.tsa.seasonal import seasonal_decompose\n\nnp.random.seed(1)\nt = np.arange(120)\ntrend = 0.5 * t + 10\nseason = 5 * np.sin(2 * np.pi * t / 12)\ny = trend + season + np.random.normal(0, 1, 120)\nseries = pd.Series(y, index=pd.date_range('2020-01', periods=120, freq='M'))\n\ndecomp = seasonal_decompose(series, model='additive', period=12)\nprint(decomp.trend.head(3))", "output": "Компоненты выделены: тренд + сезонность + остаток", "output_explanation": "period=12 для годовой сезонности месячных данных. plot() покажет 3 графика."},
                "common_mistakes": {"items": [{"mistake": "Обучать ARIMA на нестационарном ряде", "why_bad": "ARIMA требует stationarity", "fix": "Проверьте ADF-test, примените differencing d=1"}, {"mistake": "Прогноз без учёта сезонности", "why_bad": "Модель не увидит паттерн", "fix": "Укажите period или используйте Prophet"}, {"mistake": "Оценивать точность по RMSE на train", "why_bad": "Overfitting — модель просто запомнила данные", "fix": "TimeSeriesSplit — rolling window validation"}]},
                "further_reading": {"items": [{"title": "Prophet (Meta)", "url": "https://facebook.github.io/prophet/"}, {"title": "Time Series Analysis (TowardsDS)", "url": "https://towardsdatascience.com/time-series-analysis-in-python-5-essential-techniques-for-forecasting-2c4e2f6c3b"}]},
                "interview_questions": {"items": [{"q": "Чем ARIMA отличается от Prophet?", "a": "ARIMA требует stationarity и ручного подбора (p,d,q). Prophet автоматически находит сезонность, устойчив к пропускам и аномалиям."}, {"q": "Что такое stationarity и зачем она?", "a": "Постоянные μ и σ. Нужна для ARIMA, иначе модель не сходится. Проверка: ADF-test, KPSS-test."}]},
                "knowledge_checklist": {"items": ["Декомпозирую временной ряд", "Строю прогноз Prophet", "Оцениваю RMSE/MAE"]}
            }
        },
        {
            "bn": 6, "num": "6.9",
            "title": "Каузальный вывод: от корреляции к причине",
            "sections": {
                "prerequisites": {"items": ["Урок 6.7: Формулировка гипотез по данным", "Урок 6.8: Мини-проект: Полный EDA"]},
                "learning_objectives": {"items": ["Применяю: различаю корреляцию и каузацию", "Знаю: confounding, RCT, DAG", "Умею: строить propensity score matching"]},
                "theory": {"content": "**Корреляция ≠ причинность.** Две переменные могут коррелировать без прямой причинной связи из-за **confounder** (третья переменная, влияющая на обе). Классика: продажи мороженого коррелируют с утоплениями, но обе вызваны жарой.\n\n**Методы каузального вывода:**\n- **RCT** (Randomized Controlled Trial) — золотой стандарт: случайное распределение устраняет confounders.\n- **Propensity Score Matching** — для observational data: оценка вероятности treatment, матчинг по ней.\n- **DAG** (Directed Acyclic Graph) — визуализация каузальных предположений.\n- **Instrumental Variables** — когда RCT невозможен, но есть внешний шок.\n- **Difference-in-Differences** — до/после с контрольной группой."},
                "summary": {"items": ["✓ Понимаю confounding и spurious correlation", "✓ Строю DAG для каузальных гипотез", "✓ Применяю PSM для observational data"]},
                "glossary": {"items": [{"term": "Confounder", "definition": "Переменная, влияющая и на X, и на Y, создающая ложную связь"}, {"term": "Propensity Score", "definition": "P(treatment | X) — вероятность получить treatment при данных признаках"}, {"term": "ATE", "definition": "Average Treatment Effect — средний каузальный эффект"}]},
                "analogy": {"real_world": "Зонтики коррелируют с дождём, но не вызывают его. Confounder — погода (давление, облака).", "domain_example": "Пользователи, купившие premium, имеют retention 90% vs 50% у бесплатных. Confounder: более активные пользователи чаще покупают premium."},
                "visual": {"description": "DAG: age → treatment, age → outcome, treatment → outcome", "ascii_diagram": "Age → Treatment → Outcome  |  Age → Outcome  (confounding path)"},
                "example": {"problem": "Оцените каузальный эффект тренировки на доход на observational data (confounder: возраст + образование)", "code": "import numpy as np\nimport pandas as pd\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.neighbors import NearestNeighbors\n\nnp.random.seed(0)\nn = 500\nage = np.random.normal(35, 10, n)\neduc = np.random.normal(14, 2, n)\ntreatment = (0.3*age + 0.5*educ + np.random.normal(0, 1, n) > 0).astype(int)\nincome = 30000 + 1000*treatment + 500*age + 200*educ + np.random.normal(0, 5000, n)\ndf = pd.DataFrame({'age': age, 'education': educ, 'treatment': treatment, 'income': income})\n\nlr = LogisticRegression()\nlr.fit(df[['age', 'education']], df['treatment'])\ndf['pscore'] = lr.predict_proba(df[['age', 'education']])[:, 1]\n\ntreated = df[df.treatment==1]\ncontrol = df[df.treatment==0]\nnn = NearestNeighbors(n_neighbors=1).fit(control[['pscore']])\n_, idx = nn.kneighbors(treated[['pscore']])\nmatched = control.iloc[idx.flatten()]\nate = (treated.income.values - matched.income.values).mean()\nprint(f'ATE: {ate:.0f}')", "output": "ATE: ~1000", "output_explanation": "Matching по propensity score даёт несмещённую оценку каузального эффекта (true ATE = 1000). Naive разница была бы выше из-за confounding."},
                "common_mistakes": {"items": [{"mistake": "Корреляция = каузация", "why_bad": "Spurious correlation из-за confounder", "fix": "Используйте DAG + RCT/PSM"}, {"mistake": "Не учитывать confounders в регрессии", "why_bad": "Смещённые оценки коэффициентов", "fix": "Включите все измеренные confounders в модель"}, {"mistake": "PSM без common support", "why_bad": "Сравниваются несравнимые объекты", "fix": "Проверьте overlap распределений pscore"}]},
                "further_reading": {"items": [{"title": "Causal Inference (The Book of Why)", "url": "https://en.wikipedia.org/wiki/The_Book_of_Why"}, {"title": "Propensity Score Matching (statsmodels)", "url": "https://www.statsmodels.org/stable/examples/notebooks/generated/propensity_score_matching.html"}]},
                "interview_questions": {"items": [{"q": "Как доказать каузальность без RCT?", "a": "PSM, DAG, instrumental variables, DiD — но каждое требует сильных допущений."}, {"q": "Что такое collider bias?", "a": "Смещение при контроле коллайдера — переменной, на которую влияют и X, и Y. Открывает ложный путь."}]},
                "knowledge_checklist": {"items": ["Различаю корреляцию и каузацию", "Строю DAG", "Применяю PSM"]}
            }
        },
        {
            "bn": 7, "num": "7.15",
            "title": "Подбор гиперпараметров модели",
            "sections": {
                "prerequisites": {"items": ["Урок 7.13: Сравнение и выбор модели", "Урок 7.14: Мини-проект: Прогноз оттока"]},
                "learning_objectives": {"items": ["Применяю: GridSearchCV", "Знаю: RandomSearch vs Optuna", "Умею: избегать overfitting при подборе"]},
                "theory": {"content": "**Гиперпараметры** — параметры модели, которые не обучаются, а задаются до обучения (n_estimators, max_depth, learning_rate). Подбор — поиск лучшей комбинации.\n\n**Методы:**\n- **GridSearchCV** — полный перебор по сетке. Гарантирует лучшую комбинацию в сетке, но экспоненциально дорог.\n- **RandomizedSearchCV** — случайная выборка из распределений. Быстрее Grid при большой размерности.\n- **Optuna** — Bayesian optimization: TPE (Tree-structured Parzen Estimator) запоминает результаты и выбирает следующие кандидаты адаптивно. В 3-5x быстрее Random.\n\n**Правила:**\n- Всегда с CV (cross-validation) — иначе overfitting на валидации.\n- Лучшие параметры → финальная модель на всём train.\n- Не подбирайте на test set — test только для финальной оценки."},
                "summary": {"items": ["✓ Подбираю гиперпараметры через GridSearchCV", "✓ Сравниваю Grid/Random/Optuna", "✓ Избегаю overfitting при подборе"]},
                "glossary": {"items": [{"term": "Hyperparameter tuning", "definition": "Поиск оптимальных гиперпараметров модели"}, {"term": "Bayesian optimization", "definition": "Последовательный поиск, использующий прошлые результаты — Optuna"}, {"term": "Early Stopping", "definition": "Остановка обучения, когда метрика перестаёт улучшаться"}]},
                "analogy": {"real_world": "Настройка радио: Grid — крутить все ручки с шагом 1. Random — крутить случайно 20 раз. Optuna — запоминать, где было чисто, и крутить рядом.", "domain_example": "XGBoost: Grid 50 комбинаций = 10 мин. Optuna 100 trials = 5 мин (с TPE)."},
                "visual": {"description": "Сравнение методов подбора", "ascii_diagram": "Grid: ■■■■■■■ 25 точeк | Random: ■■■■■ 10 точек | Optuna: ■■■■■■ 12 точек (лучше!)"},
                "example": {"problem": "Подберите гиперпараметры RandomForest для классификации через GridSearchCV", "code": "from sklearn.ensemble import RandomForestClassifier\nfrom sklearn.model_selection import GridSearchCV\nfrom sklearn.datasets import load_breast_cancer\n\nX, y = load_breast_cancer(return_X_y=True)\nparam_grid = {'n_estimators': [100, 200], 'max_depth': [5, 10]}\ngrid = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=3, scoring='f1')\ngrid.fit(X, y)\nprint(grid.best_params_)", "output": "{'max_depth': 10, 'n_estimators': 200}", "output_explanation": "GridSearch перебрал 4 комбинации × 3 fold = 12 обучений. n_jobs=-1 для параллельного запуска."},
                "common_mistakes": {"items": [{"mistake": "Подбор без CV", "why_bad": "Overfitting — params подогнаны под конкретный split", "fix": "Всегда cv≥3"}, {"mistake": "Подбор на test set", "why_bad": "Оценка обобщения оптимистично смещена", "fix": "test только для финальной оценки"}, {"mistake": "Слишком широкая сетка", "why_bad": "Экспоненциальный рост комбинаций", "fix": "Начните с coarse grid, потом fine вокруг best"}]},
                "further_reading": {"items": [{"title": "GridSearchCV (sklearn)", "url": "https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html"}, {"title": "Optuna", "url": "https://optuna.org/"}]},
                "interview_questions": {"items": [{"q": "GridSearch vs RandomizedSearch — когда что?", "a": "Grid — малая размерность (≤10 комбинаций). Random — большая (≥100) или непрерывные параметры."}, {"q": "Почему Optuna быстрее Random?", "a": "TPE учится на истории trials и выбирает перспективные области, Random — слепой."}]},
                "knowledge_checklist": {"items": ["GridSearchCV", "RandomizedSearchCV", "Optuna basics"]}
            }
        },
        {
            "bn": 7, "num": "7.16",
            "title": "Bias и Fairness в машинном обучении",
            "sections": {
                "prerequisites": {"items": ["Урок 7.5: Метрики классификации", "Урок 7.14: Мини-проект: Прогноз оттока"]},
                "learning_objectives": {"items": ["Применяю: метрики fairness (DPD, EOD)", "Знаю: источники bias в данных и модели", "Умею: смягчать bias через fairlearn"]},
                "theory": {"content": "**Bias в ML** — систематическая ошибка модели против определённых групп (раса, пол, возраст). Источники: исторический bias (данные отражают дискриминацию), representation bias (группа недопредставлена), measurement bias (неточные измерения для группы).\n\n**Метрики fairness:**\n- **Demographic Parity**: P(ŷ=1|A) = P(ŷ=1|B) — одинаковый процент положительных предсказаний.\n- **Equalized Odds**: TPR(A) = TPR(B), FPR(A) = FPR(B) — одинаковая чувствительность.\n- **Disparate Impact Ratio**: P(ŷ=1|защищённая) / P(ŷ=1|остальные) — правило 80%.\n\n**Смягчение bias:** reweighing (pre-processing), adversarial debiasing (in-processing), fairlearn (post-processing)."},
                "summary": {"items": ["✓ Измеряю fairness метрики", "✓ Понимаю источники bias", "✓ Применяю fairlearn"]},
                "glossary": {"items": [{"term": "Demographic Parity", "definition": "Одинаковая доля положительных предсказаний для всех групп"}, {"term": "Equalized Odds", "definition": "Одинаковые TPR и FPR между группами"}, {"term": "Fairlearn", "definition": "Библиотека от Microsoft для fairness в ML"}]},
                "analogy": {"real_world": "Приём в университет: если модель рекомендует только мужчин, потому что в данных больше мужчин-студентов — это representation bias.", "domain_example": "Кредитный скоринг: модель отклоняет заявки определённого района — historical bias в данных (там раньше отклоняли чаще)."},
                "visual": {"description": "Сравнение предсказаний по группам", "ascii_diagram": "Группа A: одобрено 60%  |  Группа B: одобрено 35%  →  DPD = 0.25 (bias)"},
                "example": {"problem": "Проверьте fairness модели кредитного скоринга по двум группам", "code": "import numpy as np\nfrom fairlearn.metrics import demographic_parity_difference\n\nnp.random.seed(0)\nn = 1000\nrace = np.random.choice(['A', 'B'], n)\ny_pred = np.where(race=='A', np.random.binomial(1, 0.7, n), np.random.binomial(1, 0.5, n))\ny_true = np.random.binomial(1, 0.6, n)\n\ndpd = demographic_parity_difference(y_true, y_pred, sensitive_features=race)\nprint(f'DPD: {dpd:.3f}')", "output": "DPD: ~0.15 (существенный bias)", "output_explanation": "DPD > 0.1 считается значительным. Equalized Odds Diference (EOD) — дополнительная метрика для fairness."},
                "common_mistakes": {"items": [{"mistake": "Игнорировать sensitive attributes", "why_bad": "Модель может научиться bias через proxy-признаки (почтовый индекс → раса)", "fix": "Проверьте fairness даже без sensitive в фичах"}, {"mistake": "Считать fairness = demographic parity", "why_bad": "Parity может конфликтовать с accuracy", "fix": "Trade-off: выбирайте метрику под бизнес-контекст"}, {"mistake": "Думать, что fairness = убрать sensitive", "why_bad": "Proxy-признаки сохранят bias", "fix": "Используйте fairlearn для обнаружения и смягчения"}]},
                "further_reading": {"items": [{"title": "Fairlearn (Microsoft)", "url": "https://fairlearn.org/"}, {"title": "Ethics and AI (Google PAIR)", "url": "https://pair.withgoogle.com/"}]},
                "interview_questions": {"items": [{"q": "Что такое disparate impact?", "a": "Непропорционально негативное влияние модели на защищённую группу. DIR < 0.8 — красный флаг."}, {"q": "Как sources bias влияют на модель?", "a": "Исторический (данные из прошлого), representation (мало группы в данных), measurement (неточные метки для группы)."}]},
                "knowledge_checklist": {"items": ["Измеряю DPD/EOD", "Понимаю proxy-признаки", "Применяю fairlearn"]}
            }
        },
        {
            "bn": 7, "num": "7.17",
            "title": "Нейронные сети: введение в deep learning",
            "sections": {
                "prerequisites": {"items": ["Урок 7.1: Типы ML", "Урок 7.6: Линейная регрессия"]},
                "learning_objectives": {"items": ["Применяю: строю простую NN в PyTorch", "Знаю: perceptron, activation functions, backpropagation", "Умею: обучать NN на MNIST"]},
                "theory": {"content": "**Нейронная сеть** — последовательность слоёв: входной → скрытые → выходной. Каждый нейрон: взвешенная сумма входов + bias → функция активации.\n\n**Функции активации:**\n- **ReLU** (max(0, x)) — стандарт для скрытых слоёв, нет vanishing gradient\n- **Sigmoid** (1/(1+e⁻ˣ)) — для вероятностей (выход binary classification)\n- **Softmax** — многоклассовая вероятность\n\n**Градиентный спуск:** backpropagation — цепное правило дифференцирования для обновления весов. Adam — адаптивная скорость обучения.\n\n**PyTorch vs TensorFlow:** PyTorch — де-факто стандарт в исследованиях, динамический граф, интуитивный синтаксис."},
                "summary": {"items": ["✓ Понимаю архитектуру нейронной сети", "✓ Строю сеть в PyTorch", "✓ Обучаю на MNIST >95% accuracy"]},
                "glossary": {"items": [{"term": "Perceptron", "definition": "Простейший нейрон: взвешенная сумма + активация"}, {"term": "Backpropagation", "definition": "Алгоритм градиентного спуска для нейросетей"}, {"term": "Adam", "definition": "Адаптивный оптимизатор — стандарт для обучения NN"}]},
                "analogy": {"real_world": "Мозг: нейроны → дендриты (входы) → soma (сумма) → аксон (выход). NN — упрощённая математическая модель.", "domain_example": "Классификация изображений: пиксели → слой краёв → слой форм → слой объектов → 'кошка'."},
                "visual": {"description": "Схема нейронной сети 784→128→10", "ascii_diagram": "Input(784) → Hidden(128, ReLU) → Output(10, Softmax) → 'digit 0-9'"},
                "example": {"problem": "Обучите нейросеть на MNIST с accuracy >95%", "code": "import torch\nimport torch.nn as nn\nfrom torchvision import datasets, transforms\nfrom torch.utils.data import DataLoader\n\ntransform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])\ntrain = DataLoader(datasets.MNIST('./data', train=True, download=True, transform=transform), batch_size=64, shuffle=True)\ntest = DataLoader(datasets.MNIST('./data', train=False, transform=transform), batch_size=1000)\n\nclass Net(nn.Module):\n    def __init__(self):\n        super().__init__()\n        self.fc1 = nn.Linear(784, 128)\n        self.fc2 = nn.Linear(128, 10)\n    def forward(self, x):\n        x = x.view(-1, 784)\n        x = torch.relu(self.fc1(x))\n        return self.fc2(x)\n\nmodel = Net()\nopt = torch.optim.Adam(model.parameters(), lr=0.001)\nloss_fn = nn.CrossEntropyLoss()\n\nfor epoch in range(3):\n    for x, y in train:\n        opt.zero_grad()\n        loss_fn(model(x), y).backward()\n        opt.step()\n\ncorrect = sum((model(x).argmax(1) == y).sum().item() for x, y in test)\nprint(f'Accuracy: {correct/len(test.dataset):.3f}')", "output": "Accuracy: >0.96", "output_explanation": "Простая 2-слойная сеть даёт >96%. Свёрточные (CNN) дают >99%."},
                "common_mistakes": {"items": [{"mistake": "Sigmoid в скрытых слоях", "why_bad": "Vanishing gradient — перестаёт учиться", "fix": "Используйте ReLU"}, {"mistake": "Не нормализовать входные данные", "why_bad": "Градиенты расходяться", "fix": "Normalize: (x - μ)/σ"}, {"mistake": "Слишком глубокая сеть без skip-connections", "why_bad": "Degradation — точность падает с глубиной", "fix": "ResNet / BatchNorm"}]},
                "further_reading": {"items": [{"title": "PyTorch Tutorial", "url": "https://pytorch.org/tutorials/"}, {"title": "3Blue1Brown Neural Networks", "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi"}]},
                "interview_questions": {"items": [{"q": "Почему ReLU лучше sigmoid?", "a": "ReLU не страдает vanishing gradient (производная 1 для x>0 против ~0 у sigmoid)."}, {"q": "Что такое backpropagation?", "a": "Цепное правило для вычисления градиента loss по весам — от выхода к входу."}]},
                "knowledge_checklist": {"items": ["Строю NN в PyTorch", "Понимаю активации", "Обучаю на MNIST"]}
            }
        },
        {
            "bn": 8, "num": "8.9",
            "title": "Обработка текста: NLP для Data Science",
            "sections": {
                "prerequisites": {"items": ["Урок 8.6: Базовая обработка текста", "Урок 8.7: Отбор признаков"]},
                "learning_objectives": {"items": ["Применяю: TF-IDF векторизацию", "Знаю: tokenization, embeddings, n-grams", "Умею: строить baseline для текстовой классификации"]},
                "theory": {"content": "**NLP** (Natural Language Processing) — обработка естественного языка. Основные задачи: классификация текстов, анализ тональности, извлечение сущностей (NER), машинный перевод, суммаризация.\n\n**Pipeline:**\n1. **Preprocessing**: lowercase, удаление пунктуации/стоп-слов, stemming (обрезание суффиксов) / lemmatization (словарная форма)\n2. **Векторизация**:\n   - **Bag of Words** — частоты слов, теряет порядок\n   - **TF-IDF** — вес = частота в документе × обратная частота в корпусе\n   - **Word Embeddings** (Word2Vec, FastText) — плотные векторы с семантикой\n   - **Sentence Transformers** (BERT) — контекстуальные эмбеддинги\n3. **Модель**: LogisticRegression, Random Forest, нейросети, трансформеры\n\n**Библиотеки:** nltk, spaCy, gensim, transformers (Hugging Face)."},
                "summary": {"items": ["✓ Применяю TF-IDF для векторизации", "✓ Понимаю pipeline NLP", "✓ Строю классификатор текстов"]},
                "glossary": {"items": [{"term": "TF-IDF", "definition": "Term Frequency × Inverse Document Frequency — вес слова в документе относительно корпуса"}, {"term": "Stemming vs Lemmatization", "definition": "Stemming — жёсткая обрезка ('running'→'run'), lemmatization — словарная форма с учётом POS"}, {"term": "Word Embeddings", "definition": "Плотные векторы (d=100-300), сохраняющие семантику слов"}]},
                "analogy": {"real_world": "Библиотекарь: BoW — считает сколько раз слово на странице. TF-IDF — понимает, что 'the' встречается везде (низкий вес), 'ракета' — редко (высокий).", "domain_example": "Отзывы: 'отличный сервис' → тональность положительная. tf-idf даст высокий вес слову 'отличный', низкий — 'сервис'."},
                "visual": {"description": "TF-IDF матрица", "ascii_diagram": "Док1: [0.02 0.05 0.00 ...]  |  Док2: [0.00 0.00 0.08 ...]"},
                "example": {"problem": "Постройте TF-IDF матрицу для 5 отзывов и найдите топ-3 слова в каждом", "code": "from sklearn.feature_extraction.text import TfidfVectorizer\nimport numpy as np\n\ndocs = ['кошка сидит на окне', 'собака бегает в парке', 'кошка и собака играют', 'окно открыто ветер дует', 'парк большой много деревьев']\nvectorizer = TfidfVectorizer()\nX = vectorizer.fit_transform(docs)\nfeatures = vectorizer.get_feature_names_out()\n\nfor i, doc in enumerate(docs):\n    scores = X[i].toarray().flatten()\n    top_idx = np.argsort(scores)[::-1][:3]\n    top_words = [(features[j], scores[j]) for j in top_idx if scores[j] > 0]\n    print(f'Док{i+1}: {top_words}')", "output": "Док1: [('кошка', 0.58), ('сидит', 0.58), ('окне', 0.58)]", "output_explanation": "TF-IDF выделяет уникальные для документа слова. 'кошка' высокий вес в док1, 'собака' в док2."},
                "common_mistakes": {"items": [{"mistake": "Не удалять стоп-слова", "why_bad": "TF-IDF даст низкий вес, но зашумляет матрицу", "fix": "stop_words='russian' в TfidfVectorizer"}, {"mistake": "Stemming вместо lemmatization", "why_bad": "Потеря смысла ('running' → 'run' OK, 'flies' → 'fli' плохо)", "fix": "spaCy / pymorphy2 для русского"}, {"mistake": "BoW без n-grams", "why_bad": "Потеря контекста ('не плохой' vs 'плохой')", "fix": "ngram_range=(1, 2) — униграммы + биграммы"}]},
                "further_reading": {"items": [{"title": "NLTK Book", "url": "https://www.nltk.org/book/"}, {"title": "Hugging Face Transformers", "url": "https://huggingface.co/docs/transformers/index"}]},
                "interview_questions": {"items": [{"q": "TF-IDF vs Word2Vec — разница?", "a": "TF-IDF — разреженный, частотный, без семантики. Word2Vec — плотный, семантический ('король'-'мужчина'+'женщина'='королева')."}, {"q": "Что такое BERT?", "a": "Трансформер от Google — контекстуальные эмбеддинги. Учитывает контекст слева и справа. SOTA для большинства NLP-задач."}]},
                "knowledge_checklist": {"items": ["Векторизую через TF-IDF", "Понимаю pipeline NLP", "Строю классификатор текстов"]}
            }
        },
        {
            "bn": 9, "num": "9.9",
            "title": "Ethics и Privacy в Data Science",
            "sections": {
                "prerequisites": {"items": ["Урок 9.8: Мини-проект: Оформить проект по GitHub", "Урок 7.16: Bias и Fairness"]},
                "learning_objectives": {"items": ["Применяю: принципы GDPR", "Знаю: differential privacy, data minimization", "Умею: оценивать ethical risks проекта"]},
                "theory": {"content": "**Ethics в Data Science** — ответственность за данные, модель и её последствия. Ключевые принципы:\n\n**GDPR** (General Data Protection Regulation, ЕС 2018):\n- Право на забвение — удаление данных по запросу\n- Согласие на обработку — opt-in, не opt-out\n- Минимизация — собирать только необходимые данные\n- Право на объяснение — пользователь может спросить, почему принято решение\n\n**Differential Privacy:** добавление калиброванного шума к агрегированным запросам так, что присутствие/отсутствие одной записи почти не меняет результат. Используется в Apple, Google, US Census.\n\n**Data Privacy (PII):** никогда не храните пароли в открытом виде (bcrypt/argon2), не логируйте PII (номера карт, паспортов), используйте псевдонимизацию."},
                "summary": {"items": ["✓ Понимаю GDPR и его влияние на DS", "✓ Знаю differential privacy", "✓ Применяю best practices PII"]},
                "glossary": {"items": [{"term": "GDPR", "definition": "Европейский регламент защиты персональных данных"}, {"term": "Differential Privacy", "definition": "Добавление шума к запросам для защиты отдельных записей"}, {"term": "PII (Personally Identifiable Information)", "definition": "Данные, идентифицирующие личность (имя, email, номер карты)"}]},
                "analogy": {"real_world": "Банк: знает ваш доход и траты. GDPR — вы можете попросить удалить эти данные. DP — банк говорит 'средний доход клиентов 50K', но не может сказать, сколько у вас.", "domain_example": "Рекомендательная система: ребёнку 8 лет → нужно согласие родителей (COPPA/GDPR)."},
                "visual": {"description": "Differential Privacy: шум на агрегаты", "ascii_diagram": "Данные → Laplace noise → Агрегат: ответ ±ε"},
                "example": {"problem": "Оцените ethical risk для проекта: модель предсказывает вероятность рецидива (COMPAS)", "code": "risks = ['Historical bias: данные арестов отражают системную дискриминацию',\n         'Representation: непропорционально много арестов меньшинств',\n         'Feedback loop: модель рекомендует арест → больше данных → модель хуже',\n         'Explainability: сложная модель — судья не понимает решение',\n         'Accountability: кто ответит за ложноположительный прогноз?']\nfor i, r in enumerate(risks, 1):\n    print(f'{i}. {r}')", "output": "5 ethical risks identified", "output_explanation": "Каждый DS-проект должен пройти ethical review. COMPAS — реальный пример непрозрачной модели с bias."},
                "common_mistakes": {"items": [{"mistake": "Хранить пароли в открытом виде", "why_bad": "Утечка → компрометация всех пользователей", "fix": "bcrypt / argon2 для хеширования"}, {"mistake": "Логировать PII", "why_bad": "Утечка логов → утечка персональных данных", "fix": "Маскируйте email/телефон в логах"}, {"mistake": "GDPR не касается моего проекта", "why_bad": "GDPR распространяется на любые данные резидентов ЕС", "fix": "GDPR applies globally для EU residents"}]},
                "further_reading": {"items": [{"title": "GDPR.eu", "url": "https://gdpr.eu/"}, {"title": "Differential Privacy (Google)", "url": "https://developers.google.com/tech-writing"}]},
                "interview_questions": {"items": [{"q": "Что такое право на объяснение?", "a": "GDPR: пользователь может потребовать объяснения автоматического решения. SHAP/LIME — техническая реализация."}, {"q": "Как DP защищает данные?", "a": "Добавляет шум Laplace/Gaussian к запросу. Параметр ε (epsilon) — privacy budget: меньше ε = больше privacy."}]},
                "knowledge_checklist": {"items": ["Понимаю GDPR", "Знаю differential privacy", "Провожу ethical review"]}
            }
        },
        {
            "bn": 9, "num": "9.10",
            "title": "Data drift и мониторинг модели в production",
            "sections": {
                "prerequisites": {"items": ["Урок 9.6: Docker", "Урок 9.7: Основы MLOps"]},
                "learning_objectives": {"items": ["Применяю: PSI для detection drift", "Знаю: data drift vs concept drift", "Умею: настраивать alert при drift"]},
                "theory": {"content": "**Data drift** — изменение распределения входных данных P(X) со временем. Причины: смена аудитории, сезонность, изменение источника данных.\n\n**Concept drift** — изменение связи P(Y|X): те же признаки ведут к другому результату. Пример: поведение пользователей после пандемии.\n\n**Методы детекции:**\n- **PSI** (Population Stability Index): сравнивает распределения через бины. PSI < 0.1 — нет drift, 0.1-0.2 — слабый, > 0.2 — значительный.\n- **KS-test** (Kolmogorov-Smirnov): сравнение двух распределений.\n- **ADWIN**: адаптивное скользящее окно.\n- **Мониторинг метрик**: accuracy, latency, data quality (NaN%, типы).\n\n**Действия при drift:** retrain модель, оповестить команду, rollback к предыдущей версии."},
                "summary": {"items": ["✓ Детектирую data drift через PSI", "✓ Различаю data и concept drift", "✓ Настраиваю мониторинг"]},
                "glossary": {"items": [{"term": "Data drift (covariate shift)", "definition": "Изменение P(X) — распределения входных признаков"}, {"term": "Concept drift", "definition": "Изменение P(Y|X) — связи признаков с таргетом"}, {"term": "PSI", "definition": "Population Stability Index — мера изменения распределения"}]},
                "analogy": {"real_world": "Прогноз погоды: модель училась на данных 2010-2020, а сейчас 2025 с изменённым климатом. Data drift — стали чаще жары. Concept drift — связь давления и дождя изменилась.", "domain_example": "Модель churn: после изменения тарифов профиль клиентов изменился → data drift. P(churn|активность) изменилась → concept drift."},
                "visual": {"description": "PSI расчёт: expected vs actual", "ascii_diagram": "Expected: |▁▃▅▇▅▃▁|  Actual:  |▁▅▇▇▃▁▁|  PSI=0.35 (>0.2 = drift)"},
                "example": {"problem": "Симулируйте data drift: модель обучена на N(30,5), тест на N(50,5). Посчитайте PSI.", "code": "import numpy as np\n\nnp.random.seed(0)\nexpected = np.random.normal(30, 5, 1000)\nactual = np.random.normal(50, 5, 1000)\n\ndef psi(expected, actual, bins=10):\n    breakpoints = np.quantile(expected, np.linspace(0, 1, bins+1))\n    exp_counts = np.histogram(expected, breakpoints)[0] / len(expected)\n    act_counts = np.histogram(actual, breakpoints)[0] / len(actual)\n    return np.sum((act_counts - exp_counts) * np.log(act_counts / exp_counts + 1e-10))\n\nprint(f'PSI: {psi(expected, actual):.3f}')", "output": "PSI: ~0.35 (significant drift)", "output_explanation": "PSI > 0.2 — модель нужно переобучать. Причина: среднее возраста аудитории сместилось с 30 до 50."},
                "common_mistakes": {"items": [{"mistake": "Не мониторить модель в production", "why_bad": "Модель деградирует молча — метрики падают, бизнес теряет деньги", "fix": "Настройте PSI + accuracy monitoring в первый день деплоя"}, {"mistake": "Путать data drift с concept drift", "why_bad": "Разные причины — разные решения", "fix": "Data drift → retrain. Concept drift → redesign features/model"}, {"mistake": "Мониторить только accuracy", "why_bad": "Accuracy может оставаться высокой при drift (модель предсказывает большинство)", "fix": "Добавьте PSI на ключевые признаки"}]},
                "further_reading": {"items": [{"title": "ML Monitoring (Evidently AI)", "url": "https://www.evidentlyai.com/"}, {"title": "Data Drift Detection (NannyML)", "url": "https://www.nannyml.com/"}]},
                "interview_questions": {"items": [{"q": "Как детектировать data drift в production?", "a": "PSI, KS-test, ADWIN. Настройте алерт при PSI > 0.2 или KS p-value < 0.05."}, {"q": "Что делать при обнаружении drift?", "a": "1) Оповестить, 2) Проанализировать причину, 3) Retrain модель, 4) A/B тест новой модели, 5) Deploy."}]},
                "knowledge_checklist": {"items": ["Считаю PSI", "Различаю drift types", "Настраиваю alert"]}
            }
        },
        {
            "bn": 9, "num": "9.11",
            "title": "Деплой ML-модели с FastAPI",
            "sections": {
                "prerequisites": {"items": ["Урок 9.10: Data drift и мониторинг", "Урок 9.7: Основы MLOps"]},
                "learning_objectives": {"items": ["Применяю: сохранение/загрузка модели через joblib", "Знаю: FastAPI endpoint для predict", "Умею: тестировать через /docs"]},
                "theory": {"content": "**FastAPI** — современный Python-фреймворк для API. Главные преимущества: автоматическая документация (Swagger UI на /docs), Pydantic-валидация, async поддержка, высокая производительность (на уровне Node/Go).\n\n**Pipeline деплоя:**\n1. Сохраните модель: `joblib.dump(model, 'model.pkl')`\n2. Создайте FastAPI приложение: `/predict` endpoint\n3. Оберните в Docker (FROM python:3.11 → COPY → pip install → CMD uvicorn)\n4. Запустите: `uvicorn app:app --host 0.0.0.0 --port 8000`\n5. Протестируйте через Swagger UI на `/docs`\n\n**Pydantic BaseModel:** автоматическая валидация типов на входе — если передать строку вместо числа, вернёт 422 с описанием ошибки."},
                "summary": {"items": ["✓ Сохраняю model через joblib", "✓ Создаю /predict endpoint", "✓ Тестирую через /docs"]},
                "glossary": {"items": [{"term": "FastAPI", "definition": "Python-фреймворк для API с автодокументацией"}, {"term": "Pydantic", "definition": "Библиотека валидации данных через BaseModel"}, {"term": "joblib", "definition": "Сериализация sklearn-моделей (эффективнее pickle)"}]},
                "analogy": {"real_world": "Автомат с газировкой: вводишь код → get /soda/cola → автомат выдаёт. ML API: POST /predict → features → модель → prediction.", "domain_example": "POST /predict/churn с JSON {'tenure_days': 365, 'logins_per_day': 0.5} → {'churn_probability': 0.32, 'risk': 'low'}"},
                "visual": {"description": "FastAPI lifecycle", "ascii_diagram": "Client → POST /predict (JSON) → Pydantic validate → Model.predict → JSON response → Client"},
                "example": {"problem": "Создайте FastAPI endpoint для предсказания оттока", "code": "from fastapi import FastAPI\nfrom pydantic import BaseModel\nimport joblib\nimport pandas as pd\n\nmodel = joblib.load('churn_model.pkl')\napp = FastAPI()\n\nclass Features(BaseModel):\n    tenure_days: int\n    logins_per_day: float\n\n@app.post('/predict')\ndef predict(f: Features):\n    X = pd.DataFrame([f.dict()])\n    prob = model.predict_proba(X)[0, 1]\n    risk = 'high' if prob > 0.7 else 'medium' if prob > 0.4 else 'low'\n    return {'probability': round(prob, 3), 'risk': risk}\n\n# Запуск: uvicorn app:app --reload --port 8000", "output": "JSON: probability и risk", "output_explanation": "FastAPI автоматически валидирует вход (Pydantic), генерирует /docs с Swagger. --reload для разработки."},
                "common_mistakes": {"items": [{"mistake": "Модель в памяти глобально", "why_bad": "Загружается при каждом запросе — медленно", "fix": "Загружайте при старте: model = joblib.load() вне функции"}, {"mistake": "Не логировать предсказания", "why_bad": "Нельзя отладить проблемы в production", "fix": "Логируйте input, model_version, prediction, latency"}, {"mistake": "Без Docker", "why_bad": "'Works on my machine'", "fix": "Dockerfile с uvicorn + зависимости"}]},
                "further_reading": {"items": [{"title": "FastAPI Docs", "url": "https://fastapi.tiangolo.com/"}, {"title": "ML Deployment (TowardsDS)", "url": "https://towardsdatascience.com/deploying-ml-models-with-fastapi-and-docker-8c2e7fe4f332"}]},
                "interview_questions": {"items": [{"q": "FastAPI vs Flask — разница?", "a": "FastAPI: async, Pydantic, /docs, быстрее. Flask: проще, больше legacy."}, {"q": "Как сериализовать модель для деплоя?", "a": "joblib.dump/load для sklearn, torch.save для PyTorch, ONNX для кросс-платформенности."}]},
                "knowledge_checklist": {"items": ["Сохраняю model через joblib", "Создаю /predict endpoint", "Деплою через Docker"]}
            }
        },
    ]

    for lesson in lessons_data:
        num = lesson["num"]
        if _exists(c, "lessons", "number", num):
            continue
        block_id = c.execute("SELECT id FROM blocks WHERE number=?", (lesson["bn"],)).fetchone()[0]
        sections_raw = lesson["sections"]
        sections_out = []
        for stype in ["prerequisites", "learning_objectives", "theory", "summary",
                        "glossary", "analogy", "visual", "example", "common_mistakes",
                        "further_reading", "interview_questions", "knowledge_checklist"]:
            d = sections_raw.get(stype, {})
            if stype in ("theory",):
                sections_out.append({"type": stype, "content": d.get("content", "")})
            elif stype in ("analogy",):
                sections_out.append({"type": stype, "real_world": d.get("real_world", ""), "domain_example": d.get("domain_example", "")})
            elif stype in ("visual",):
                sections_out.append({"type": stype, "description": d.get("description", ""), "ascii_diagram": d.get("ascii_diagram", "")})
            elif stype in ("example",):
                sections_out.append({"type": stype, "problem": d.get("problem", ""), "solution_explanation": d.get("solution_explanation", ""),
                                      "code": d.get("code", ""), "output": d.get("output", ""), "output_explanation": d.get("output_explanation", "")})
            elif stype in ("further_reading",):
                sections_out.append({"type": stype, "items": d.get("items", [])})
            else:
                sections_out.append({"type": stype, "items": d.get("items", [])})

        # Get next order_idx
        max_order = c.execute("SELECT COALESCE(MAX(order_idx), 0) FROM lessons WHERE block_id=?", (block_id,)).fetchone()[0]
        c.execute("""INSERT INTO lessons (block_id, number, title, content_json, difficulty, estimated_minutes, order_idx)
                    VALUES (?, ?, ?, ?, 2, 30, ?)""",
                  (block_id, num, lesson["title"], json.dumps({"sections": sections_out}, ensure_ascii=False), max_order + 1))
    conn.commit()

def _add_exercises(conn):
    c = conn.cursor()
    ex_data = [
        ("3.13", "python", "Рассчитайте размер выборки: baseline 5%, MDE +20%, alpha=0.05, power=0.8", 
         "from statsmodels.stats.power import NormalIndPower\nfrom statsmodels.stats.proportion import proportion_effectsize\n\np1, p2 = 0.05, 0.06\nalpha, power = 0.05, 0.8\neffect = proportion_effectsize(p1, p2)\nn = NormalIndPower().solve_power(effect, alpha=alpha, power=power)\nprint(f'Нужно {n:.0f} в каждой группе')",
         "Нужно 3502 пользователей в каждой группе"),
        ("3.13", "quiz", "Что произойдёт с размером выборки, если уменьшить alpha с 0.05 до 0.01?", "", "Увеличится"),
        ("5.11", "python", "Обнаружьте аномалии в данных с Isolation Forest", 
         "import numpy as np\nfrom sklearn.ensemble import IsolationForest\nnp.random.seed(42)\nnormal = np.random.normal(500, 100, (1000, 2))\nanomalies = np.random.uniform(0, 3000, (30, 2))\nX = np.vstack([normal, anomalies])\nmodel = IsolationForest(contamination=0.03)\npreds = model.fit_predict(X)\nprint(f'Аномалий: {(preds == -1).sum()}')",
         "Аномалий: 30"),
        ("5.11", "quiz", "Чем Isolation Forest отличается от DBSCAN?", "", "DBSCAN кластеризует, IF изолирует"),
        ("5.12", "python", "Разложите временной ряд на тренд, сезонность и остаток", 
         "import pandas as pd, numpy as np\nfrom statsmodels.tsa.seasonal import seasonal_decompose\nnp.random.seed(1)\nt = np.arange(120)\ny = 0.5*t + 10 + 5*np.sin(2*np.pi*t/12) + np.random.normal(0,1,120)\nseries = pd.Series(y, index=pd.date_range('2020-01', periods=120, freq='M'))\ndecomp = seasonal_decompose(series, model='additive', period=12)\nprint(decomp.trend.dropna().head(3))",
         "Тренд выделен"),
        ("5.12", "quiz", "Что показывает PACF?", "", "Корреляцию с лагом k после удаления эффекта промежуточных лагов"),
        ("6.9", "python", "Покажите confounding на примере ice_cream ↔ drowning (confounder: temp)", 
         "import numpy as np, pandas as pd\nnp.random.seed(42)\ntemp = np.random.uniform(10,35,1000)\nice = 10*temp + np.random.normal(0,5,1000)\ndrown = 0.5*temp + np.random.normal(0,3,1000)\ndf = pd.DataFrame({'temp':temp,'ice_cream':ice,'drowning':drown})\nprint(f'Корреляция: {df[\"ice_cream\"].corr(df[\"drowning\"]):.3f}')",
         "Корреляция ~0.85 (spurious)"),
        ("6.9", "quiz", "Что такое RCT?", "", "Эксперимент со случайным распределением по группам"),
        ("7.15", "python", "GridSearchCV для RandomForest", 
         "from sklearn.ensemble import RandomForestClassifier\nfrom sklearn.model_selection import GridSearchCV\nparam_grid = {'n_estimators':[100,200],'max_depth':[5,10]}\ngrid = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=3, scoring='f1')\ngrid.fit([[1]*10+[0]*10]*2, [1]*10+[0]*10)\nprint(grid.best_params_)",
         "Best params"),
        ("7.15", "quiz", "Почему нельзя подбирать гиперпараметры на test set?", "", "Test перестанет быть независимой оценкой"),
        ("7.16", "quiz", "Что такое disparate impact ratio (DIR)?", "", "Отношение положительных предсказаний для защищённой группы к большинству"),
        ("7.16", "quiz", "Что такое differential privacy?", "", "Добавление шума к запросам для защиты отдельных записей"),
        ("7.17", "python", "Обучите простую нейросеть на MNIST", 
         "import torch, torch.nn as nn\nfrom torchvision import datasets, transforms\nfrom torch.utils.data import DataLoader\ntransform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,),(0.3081,))])\ntrain = DataLoader(datasets.MNIST('./data', train=True, download=True, transform=transform), batch_size=64, shuffle=True)\ntest = DataLoader(datasets.MNIST('./data', train=False, transform=transform), batch_size=1000)\nclass Net(nn.Module):\n    def __init__(self):\n        super().__init__()\n        self.fc1 = nn.Linear(784, 128)\n        self.fc2 = nn.Linear(128, 10)\n    def forward(self, x):\n        x = x.view(-1, 784)\n        x = torch.relu(self.fc1(x))\n        return self.fc2(x)\nmodel = Net(); opt = torch.optim.Adam(model.parameters(), lr=0.001)\nloss_fn = nn.CrossEntropyLoss()\nfor epoch in range(3):\n    for x, y in train:\n        opt.zero_grad(); loss_fn(model(x), y).backward(); opt.step()\ncorrect = sum((model(x).argmax(1) == y).sum().item() for x, y in test)\nprint(f'Accuracy: {correct/len(test.dataset):.3f}')",
         "Accuracy > 0.95"),
        ("7.17", "quiz", "Почему ReLU предпочтительнее sigmoid?", "", "ReLU не страдает vanishing gradient"),
        ("8.9", "python", "Постройте TF-IDF матрицу и найдите топ-3 слова в каждом документе", 
         "from sklearn.feature_extraction.text import TfidfVectorizer\nimport numpy as np\ndocs = ['кошка сидит на окне','собака бегает в парке','кошка и собака играют']\nvectorizer = TfidfVectorizer()\nX = vectorizer.fit_transform(docs)\nfeatures = vectorizer.get_feature_names_out()\nfor i, doc in enumerate(docs):\n    scores = X[i].toarray().flatten()\n    top = np.argsort(scores)[::-1][:3]\n    print(f'Док{i+1}: {[features[j] for j in top if scores[j]>0]}')",
         "Top-3 слова по TF-IDF"),
        ("8.9", "quiz", "Чем lemmatization отличается от stemming?", "", "Lemmatization приводит к словарной форме с учётом POS"),
        ("9.9", "quiz", "Что такое GDPR?", "", "Европейский регламент защиты персональных данных"),
        ("9.9", "quiz", "Что такое differential privacy?", "", "Добавление шума для защиты отдельных записей"),
        ("9.10", "python", "Симулируйте data drift и посчитайте PSI", 
         "import numpy as np\nnp.random.seed(0)\nexpected = np.random.normal(30,5,1000)\nactual = np.random.normal(50,5,1000)\ndef psi(expected, actual, bins=10):\n    bp = np.quantile(expected, np.linspace(0,1,bins+1))\n    exp_c = np.histogram(expected,bp)[0]/len(expected)\n    act_c = np.histogram(actual,bp)[0]/len(actual)\n    return np.sum((act_c-exp_c)*np.log(act_c/exp_c+1e-10))\nprint(f'PSI: {psi(expected,actual):.3f}')",
         "PSI ~0.35 (significant drift)"),
        ("9.10", "quiz", "Чем concept drift отличается от data drift?", "", "Data drift — P(X), concept drift — P(Y|X)"),
        ("9.11", "python", "Сохраните и загрузите модель через joblib", 
         "import joblib\nfrom sklearn.linear_model import LogisticRegression\nimport numpy as np\nX = np.random.randn(100,4)\ny = (X[:,0]+X[:,1] > 0).astype(int)\nmodel = LogisticRegression().fit(X,y)\njoblib.dump(model, 'model.pkl')\nloaded = joblib.load('model.pkl')\ntest = np.array([[1,1,0,0]])\nprint(f'Original: {model.predict(test)[0]}, Loaded: {loaded.predict(test)[0]}')",
         "Predictions match"),
        ("9.11", "quiz", "Зачем нужен Docker для ML-модели?", "", "Для воспроизводимости окружения и изоляции зависимостей"),
    ]

    # Get max number
    max_n = c.execute("SELECT COALESCE(MAX(number), 0) FROM exercises").fetchone()[0]
    for num, ex_type, prompt, starter, solution in ex_data:
        lesson_id = c.execute("SELECT id FROM lessons WHERE number=?", (num,)).fetchone()
        if not lesson_id:
            continue
        lesson_id = lesson_id[0]
        # Check if exercise already exists for this lesson
        existing = c.execute("SELECT 1 FROM exercises WHERE lesson_id=? AND prompt=?", (lesson_id, prompt[:50])).fetchone()
        if existing:
            continue
        max_n += 1
        c.execute("""INSERT INTO exercises (lesson_id, number, type, prompt, starter_code, solution_code, hints_json, test_cases_json, difficulty)
                    VALUES (?, ?, ?, ?, ?, ?, '[]', '[]', ?)""",
                  (lesson_id, max_n, ex_type, prompt, starter, solution, 2 if ex_type == "python" else 1))
    conn.commit()

def _add_middle_iq(conn):
    c = conn.cursor()
    questions = [
        # Python
        ("python", "Чем декоратор с аргументами отличается от обычного?", 
         "Декоратор с аргументами — функция, возвращающая декоратор. def retry(n): def dec(func): ... return wrapper; return dec",
         "Тройная вложенность — сначала внешняя с аргументами, возвращает декоратор", 
         "Забыть functools.wraps — теряется имя и docstring"),
        ("python", "Что такое GIL и как он влияет на многопоточность?", 
         "GIL — mutex в CPython, разрешающий только одному потоку выполнять байткод одновременно",
         "CPU-bound → multiprocessing, I/O-bound → threading OK", 
         "Использовать threading для CPU-bound — ускорения не будет"),
        ("python", "Объясните разницу между __str__ и __repr__", 
         "__str__ для пользователя (читаемо), __repr__ для разработчика (однозначно, желательно валидный Python)",
         "print() вызывает str(obj), REPL вызывает repr(obj)", 
         "Возвращать одно и то же — теряется разделение"),
        ("python", "Что такое генератор и чем отличается от list comprehension по памяти?",
         "Генератор — ленивый, вычисляет по одному. list comprehension материализует всё в памяти",
         "Генератор хранит state, не значения. Для 1M: list=80MB, generator=100B", 
         "Передавать генератор в list() дважды — второй раз пустой"),
        ("python", "Что такое MRO (Method Resolution Order)?",
         "MRO — порядок поиска метода в иерархии. C3-линеаризация: подклассы до родителей, порядок сохраняется",
         "Python 3 использует C3, можно посмотреть через ClassName.__mro__", 
         "Сложная иерархия с конфликтующим MRO — TypeError при определении"),
        ("python", "Что такое контекстный менеджер? Реализуйте свой",
         "Объект с __enter__/__exit__ — гарантирует освобождение ресурсов. @contextmanager из contextlib",
         "with open() — самый частый пример. yield до __enter__, после __exit__", 
         "В __exit__ возвращать True — подавляет исключение"),
        ("python", "Чем shallow copy отличается от deep copy?",
         "shallow копирует ссылки на вложения. deep копирует рекурсивно — полная изоляция",
         "copy.copy() vs copy.deepcopy(). list[:] — shallow", 
         "Изменять вложенный dict в shallow — меняет оригинал"),
        ("python", "Что такое dataclass? Параметры @dataclass",
         "@dataclass генерирует __init__, __repr__, __eq__ по аннотациям. frozen=True, order=True, slots=True",
         "С Python 3.7. Убирает boilerplate для DTO/конфигов", 
         "field(default=[]) — mutable default! Надо field(default_factory=list)"),
        # SQL
        ("sql", "Чем INNER JOIN отличается от LEFT JOIN с условием в WHERE?",
         "INNER — только совпадения. LEFT+WHERE b.id IS NULL — анти-join. LEFT+WHERE b.x='value' = INNER",
         "Порядок: FROM/JOIN → WHERE → GROUP BY. Условие в WHERE для LEFT — теряется LEFT", 
         "Писать условие на правую таблицу в WHERE при LEFT — получается INNER"),
        ("sql", "Разница между RANK, DENSE_RANK и ROW_NUMBER",
         "ROW_NUMBER — уникальный. RANK — пропускает ранги (1,2,2,4). DENSE_RANK — не пропускает (1,2,2,3)",
         "ROW_NUMBER для пагинации. RANK для спорта. DENSE_RANK для top-N", 
         "RANK с rank<=3 — может вернуть больше/меньше ожидаемого"),
        ("sql", "Как работает B-tree индекс? Когда не поможет?",
         "B-tree — сбалансированное дерево для точечных запросов и диапазонов. Не поможет при: WHERE LOWER(col), низкой селективности",
         "Составной индекс (a,b,c) работает только для префикса a, a=b, но не b", 
         "Индекс на каждую колонку — замедляет запись, раздувает память"),
        ("sql", "Чем CTE (WITH) отличается от подзапроса?",
         "CTE — именованный, рекурсивный (WITH RECURSIVE), улучшает читаемость. Подзапрос пересчитывается при каждом использовании",
         "Postgres инлайнит CTE. Для рекурсии — только CTE", 
         "Использовать CTE как материализованный кэш — не гарантировано"),
        ("sql", "Что такое ACID? Расшифруйте",
         "Atomicity, Consistency, Isolation, Durability — гарантии реляционных БД через WAL, MVCC, блокировки",
         "NoSQL часто жертвует ACID (BASE). Уровни изоляции: Read Committed, Repeatable Read, Serializable", 
         "Считать, что БД автоматически всё изолирует — phantom reads возможны"),
        ("sql", "Как посчитать медиану в SQL?",
         "PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY x) — Postgres. Или row_number + avg двух серединных",
         "Для MySQL — нет встроенной, нужна самописная через row_number", 
         "Использовать AVG() — это среднее, не медиана"),
        ("sql", "Разница между UNION и UNION ALL",
         "UNION убирает дубликаты (медленнее). UNION ALL сохраняет все (быстрее). Выбирайте UNION ALL когда дубли невозможны",
         "Оба требуют одинаковое число колонок с совместимыми типами", 
         "UNION «для безопасности» — лишняя дедупликация"),
        # ML
        ("ml", "Чем L1 отличается от L2 регуляризации?",
         "L1 (Lasso) — обнуляет веса (sparse, feature selection). L2 (Ridge) — сжимает веса (устойчивость при мультиколлинеарности)",
         "Lasso для feature selection. Ridge при коррелированных фичах. ElasticNet = L1+L2", 
         "Lasso на коррелированных фичах — выберет одну случайно"),
        ("ml", "Объясните bias-variance tradeoff",
         "Bias — ошибка упрощения (underfitting). Variance — ошибка чувствительности (overfitting). Общая = bias²+variance+noise",
         "CV помогает найти баланс. Регуляризация, ensemble уменьшают variance", 
         "Глубокая модель = лучшая — без регуляризации и данных будет overfitting"),
        ("ml", "Как работает XGBoost? Отличие от Gradient Boosting?",
         "XGBoost: регуляризация L1/L2, second-order Taylor, histogram-based split, параллелизм. Быстрее обычного GB",
         "Обычный GB — жадный split. LightGBM — leaf-wise, ещё быстрее", 
         "XGBoost с дефолтами — часто LR или RF побеждают при правильной настройке"),
        ("ml", "Что такое SHAP? Как интерпретировать?",
         "SHAP — Shapley из теории игр, распределяет вклад каждой фичи. Guarantees: local accuracy, consistency",
         "TreeSHAP для деревьев. Force plot — локально. Summary plot — глобально", 
         "feature_importances_ не показывает направление, SHAP — показывает"),
        ("ml", "Чем precision отличается от recall? Когда что?",
         "Precision = TP/(TP+FP). Recall = TP/(TP+FN). Precision — когда FP дорог (спам). Recall — когда FN дорог (рак)",
         "F1 = гармоническое среднее. PR-AUC лучше при дисбалансе", 
         "Accuracy при дисбалансе 99% — бессмысленно. ROC-AUC при сильном дисбалансе — оптимистично"),
        ("ml", "Принцип работы Random Forest. Почему устойчив к overfitting?",
         "Ансамбль деревьев на bootstrap + random subspace. Усреднение некоррелированных деревьев уменьшает variance",
         "n_estimators=200-500 для production. max_features='sqrt' для классификации", 
         "n_estimators=10 — нестабильно. max_features=None — деревья идентичны"),
        ("ml", "Что такое leakage в ML? Примеры",
         "Leakage — использование информации из будущего. Target leakage (фича после таргета), train-test contamination (fit на всём)",
         "scaler.fit() на X_train+X_test, target encoding до split — утечка", 
         "Feature selection до split — утечка даёт завышенные метрики"),
        ("ml", "Как работает k-fold CV? Почему для временных рядов нужен другой подход?",
         "K-fold: данные на K частей, K обучений. TimeSeriesSplit — скользящее окно без перемешивания",
         "K-fold нарушает порядок — модель видит будущее. TimeSeriesSplit: expanding window", 
         "StratifiedKFold для временного ряда — оптимистичные метрики"),
        # Statistics
        ("statistics", "Разница между Type I и Type II ошибками, связь с power",
         "Type I (α) — false positive. Type II (β) — false negative. Power = 1-β — вероятность отвергнуть ложную H0",
         "Стандарт: α=0.05, power≥0.8. Рост n ↑ power ↑", 
         "Путать α и p-value. Делать A/B тест без power analysis"),
        ("statistics", "Множественная проверка гипотез — как бороться?",
         "При 20 тестах с α=0.05 ожидается 1 false positive. Bonferroni (α/k) — строгий. BH (FDR) — мягче",
         "FDR — доля FP среди отвергнутых H0. BH для exploratory. Bonferroni для confirmatory", 
         "Игнорировать коррекцию при A/B/n тестах — «выигрыш» может быть FP"),
        ("statistics", "Что такое p-value на интуитивном уровне? Ограничения",
         "p-value = P(данные или экстремальнее | H0). Не P(H0|данные). Не говорит о размере эффекта",
         "Зависит от n (большой n → мелкий p без практической значимости)", 
         "p=0.049 «значимо», p=0.051 «не значимо» — разница случайна"),
        ("statistics", "Чем параметрические тесты отличаются от непараметрических?",
         "Параметрические (t-test, ANOVA) — требуют нормальности. Непараметрические (Mann-Whitney) — работают с рангами",
         "Mann-Whitney — не средние, а сдвиг распределений. Bootstrap — универсальная альтернатива", 
         "t-test на skewed данных — нарушение assumption"),
        # DS General
        ("ds_general", "Расскажите про CRISP-DM. Фазы",
         "1) Business Understanding, 2) Data Understanding, 3) Data Preparation, 4) Modeling, 5) Evaluation, 6) Deployment. Итеративно",
         "80% времени — Data Preparation. Business Understanding часто пропускают", 
         "Считать, что после Deployment работа закончена — модель требует мониторинга"),
        ("ds_general", "Как оценить эффект A/B теста в реальном продукте?",
         "1) метрика+MDE, 2) power analysis, 3) рандомизация, 4) прогрев, 5) коррекция на множественность, 6) segment analysis",
         "Peeking → false positives. SRM → баг рандомизации. Novelty/primacy effect", 
         "Решение по первому «выигрышу» — peeking. Игнорировать segment analysis"),
        ("ds_general", "Опишите полный pipeline ML-проекта от идеи до production",
         "1) Problem → 2) Data collection → 3) EDA → 4) Feature engineering → 5) Baseline → 6) Iterate → 7) Validate → 8) Deploy → 9) Monitor → 10) Retrain",
         "Многие забывают шаги 8-10. Модель без мониторинга — бомба замедленного действия", 
         "Перескакивать к модели без EDA. Отсутствие rollback plan"),
    ]

    for cat, q, a, explanation, cm in questions:
        if _exists(c, "interview_questions", "question", q[:80]):
            continue
        c.execute("""INSERT INTO interview_questions (category, difficulty, question, answer, explanation, common_mistakes, tags_json, is_top)
                    VALUES (?, 'middle', ?, ?, ?, ?, '[]', 0)""",
                  (cat, q, a, explanation, cm))
    conn.commit()

def _add_3rd_capstone(conn):
    c = conn.cursor()
    if _exists(c, "final_projects", "theme", "gaming"):
        already = c.execute("SELECT COUNT(*) FROM final_projects").fetchone()[0]
        if already >= 3:
            return
    steps = [
        "Загрузите данные SaaS: user_id, signup_date, last_login, monthly_logins, support_tickets, plan_type, churned",
        "EDA: распределения, корреляции, сегментация по plan_type",
        "Feature engineering: tenure_days, logins_per_day, support_per_month",
        "Baseline LogisticRegression → RandomForest → сравните по ROC-AUC",
        "SHAP-анализ — какие фичи влияют на churn?",
        "Сохраните модель (joblib), создайте FastAPI endpoint POST /predict/churn",
        "Настройте PSI для мониторинга data drift (alert при PSI > 0.2)",
        "Docker + README с инструкцией по запуску",
    ]
    dataset = {"source": "Synthetic SaaS", "rows": 5000, "columns": ["user_id", "signup_date", "last_login", "monthly_logins", "support_tickets", "plan_type", "churned"], "churn_rate": 0.23}
    c.execute("""INSERT INTO final_projects (theme, title, description, steps_json, dataset_json, template_code, solution_code)
                VALUES ('gaming', 'Анализ оттока клиентов SaaS-стартапа',
                'Полный цикл: загрузить данные → EDA → модель → деплой через FastAPI → мониторинг PSI',
                ?, ?, 'template here', 'solution here')""",
              (json.dumps(steps, ensure_ascii=False), json.dumps(dataset, ensure_ascii=False)))
    conn.commit()

def _fix_quality_issues(conn):
    """
    Fix lessons with thin glossaries (<3 terms), thin common_mistakes (<2),
    thin interview_questions (<2).
    Idempotent — skips lessons that already have sufficient content.
    """
    c = conn.cursor()
    rows = c.execute("SELECT id, number, title, content_json FROM lessons").fetchall()

    glossary_fixes = {
        "1.1": [
            {"term": "Переменная (variable)", "definition": "Именованный контейнер для хранения данных — значение можно изменить"},
            {"term": "Тип данных (data type)", "definition": "Категория значения: int, float, str, bool — определяет, какие операции разрешены"},
            {"term": "None", "definition": "Специальное значение «ничего» — отсутствие данных, аналог null в других языках"},
        ],
        "1.2": [
            {"term": "Условный оператор (if/elif/else)", "definition": "Конструкция для ветвления кода в зависимости от булева условия"},
            {"term": "Булево выражение", "definition": "Выражение, результат которого True или False — основа всех условий"},
            {"term": "Тернарный оператор", "definition": "Однострочный if-else: x if condition else y — для простых присваиваний"},
        ],
        "1.6": [
            {"term": "Ключ (key)", "definition": "Уникальный идентификатор в словаре — неизменяемый тип (str, int, tuple)"},
            {"term": "Значение (value)", "definition": "Данные, ассоциированные с ключом — может быть любого типа"},
            {"term": "Хеш-таблица", "definition": "Структура данных, обеспечивающая O(1) доступ по ключу — как устроен dict"},
        ],
        "1.8": [
            {"term": "Иммутабельность (immutability)", "definition": "Строку нельзя изменить на месте — любой метод возвращает новую строку"},
            {"term": "Метод строки", "definition": "Функция, привязанная к объекту str: .split(), .join(), .strip(), .replace()"},
            {"term": "Срез (slice)", "definition": "Извлечение подстроки: s[start:stop:step] — start включительно, stop исключительно"},
        ],
        "1.9": [
            {"term": "Контекстный менеджер (with)", "definition": "Гарантирует закрытие файла даже при ошибке — with open() as f:"},
            {"term": "Режим открытия (mode)", "definition": "r — чтение, w — запись (перезапись), a — добавление, r+ — чтение+запись"},
            {"term": "Кодировка (encoding)", "definition": "Схема преобразования байтов в символы — UTF-8 стандарт для кроссплатформенности"},
        ],
        "1.11": [
            {"term": "Traceback", "definition": "Трассировка стека вызовов — показывает, где и какое исключение возникло"},
            {"term": "Блок finally", "definition": "Выполняется всегда — для освобождения ресурсов (закрытие файла, соединения)"},
            {"term": "Пользовательское исключение", "definition": "Класс, наследующий от Exception — для специфических ошибок предметной области"},
        ],
        "1.12": [
            {"term": "CSV (Comma-Separated Values)", "definition": "Текстовый формат табличных данных — каждая строка файла = строка таблицы, столбцы разделены запятыми"},
            {"term": "DictReader", "definition": "Класс csv для чтения CSV в словари — заголовки становятся ключами"},
            {"term": "Аномалия (выброс)", "definition": "Значение, выходящее за нормальный диапазон — требует расследования (ошибка или реальный сигнал)"},
        ],
        "2.3": [
            {"term": "NULL", "definition": "Отсутствие значения — не участвует в агрегации, кроме COUNT(*)"},
            {"term": "DISTINCT", "definition": "Убирает дубликаты перед агрегацией: COUNT(DISTINCT col) — подсчёт уникальных"},
            {"term": "Группировка (GROUP BY)", "definition": "Разделение строк на группы для применения агрегатных функций"},
        ],
        "2.5": [
            {"term": "ELSE", "definition": "Значение по умолчанию в CASE WHEN — если ни одно условие не подошло"},
            {"term": "WHEN … THEN", "definition": "Пара условие-результат — вычисляется по порядку, останавливается на первом True"},
            {"term": "CASE в GROUP BY", "definition": "CASE можно использовать внутри GROUP BY для кастомной группировки диапазонов"},
        ],
        "2.8": [
            {"term": "Коррелированный подзапрос", "definition": "Подзапрос, ссылающийся на столбцы внешнего запроса — выполняется для каждой строки"},
            {"term": "EXISTS / NOT EXISTS", "definition": "Проверка существования строк в подзапросе — работает эффективнее IN для больших наборов"},
            {"term": "Подзапрос в FROM", "definition": "Подзапрос как виртуальная таблица — обязательно требует alias (SELECT * FROM (…) AS t)"},
        ],
        "2.9": [
            {"term": "WITH (CTE)", "definition": "Common Table Expression — именованный временный набор данных в одном запросе"},
            {"term": "Рекурсивный CTE", "definition": "WITH RECURSIVE — для иерархий (дерево категорий, оргструктура)"},
            {"term": "Несколько CTE", "definition": "WITH a AS (…), b AS (…) — цепочка CTE, каждый следующий может ссылаться на предыдущий"},
        ],
        "2.10": [
            {"term": "Оконная функция (window function)", "definition": "Функция, вычисляемая над окном строк без сжатия — в отличие от GROUP BY"},
            {"term": "OVER (ORDER BY …)", "definition": "Определяет порядок строк в окне — для ROW_NUMBER, RANK необходимо"},
            {"term": "Партиция (PARTITION BY)", "definition": "Разбиение окна на подгруппы — сброс нумерации внутри каждой группы"},
        ],
    }

    mistake_fixes = {
        "2.7": [
            {"mistake": "FULL JOIN в MySQL/SQLite", "why_bad": "Эти СУБД не поддерживают FULL OUTER JOIN — запрос упадёт с ошибкой",
             "fix": "LEFT JOIN + RIGHT JOIN через UNION: (LEFT JOIN) UNION (RIGHT JOIN)"},
            {"mistake": "RIGHT JOIN там, где нужен LEFT", "why_bad": "RIGHT JOIN менее читаем — легче запутаться в направлении",
             "fix": "Используйте LEFT JOIN, переставив таблицы местами"},
        ],
        "2.11": [
            {"mistake": "Не указывать ORDER BY в OVER", "why_bad": "Оконные функции LAG/LEAD требуют ORDER BY — без него порядок не определён",
             "fix": "Всегда указывайте ORDER BY внутри OVER для окон по порядку"},
            {"mistake": "Путать LAG и LEAD", "why_bad": "LAG берёт предыдущую строку, LEAD — следующую. Легко перепутать знак смещения",
             "fix": "LAG(col, 1) — вверх (прошлое), LEAD(col, 1) — вниз (будущее)"},
        ],
        "2.12": [
            {"mistake": "NTILE(100) для перцентилей", "why_bad": "100 групп — это не перцентиль, а процентильные ранги. PERCENT_RANK точнее",
             "fix": "Используйте NTILE для K-групп (квартили, децили), PERCENT_RANK для непрерывного ранга"},
            {"mistake": "NTILE без ORDER BY", "why_bad": "Без сортировки NTILE распределяет строки по группам случайно",
             "fix": "Всегда указывайте ORDER BY в OVER для NTILE"},
        ],
    }

    iq_fixes = {
        "2.12": [
            {"q": "Когда NTILE(4) не даст равные группы?",
             "a": "Когда число строк не делится на 4. Первые N%4 групп получат на 1 строку больше (если остаток 3, первые 3 группы +1 строка)"},
        ],
    }

    any_fixed = False
    for lid, num, title, cj in rows:
        data = json.loads(cj)
        sections = data['sections']
        changed = False

        # Fix glossary (if < 3 items)
        for s in sections:
            if s['type'] == 'glossary':
                items = s.get('items', [])
                if len(items) < 3:
                    add_terms = glossary_fixes.get(num, [])
                    existing_terms = {g['term'] if isinstance(g, dict) else g for g in items}
                    for term in add_terms:
                        if term['term'] not in existing_terms:
                            items.append(term)
                            existing_terms.add(term['term'])
                            changed = True
                break

        # Fix common_mistakes (if < 2 items)
        for s in sections:
            if s['type'] == 'common_mistakes':
                items = s.get('items', [])
                if len(items) < 2:
                    add_mistakes = mistake_fixes.get(num, [])
                    for m in add_mistakes:
                        if m not in items:
                            items.append(m)
                            changed = True
                break

        # Fix interview_questions (if < 2 items)
        for s in sections:
            if s['type'] == 'interview_questions':
                items = s.get('items', [])
                if len(items) < 2:
                    add_iq = iq_fixes.get(num, [])
                    for q in add_iq:
                        if q not in items:
                            items.append(q)
                            changed = True
                break

        if changed:
            c.execute("UPDATE lessons SET content_json=? WHERE id=?", (json.dumps(data, ensure_ascii=False), lid))
            any_fixed = True

    if any_fixed:
        conn.commit()
        print("[migrate] Quality fixes applied.")

def _add_augmented_lessons(conn):
    """Add new augmented lessons (1.13, 5.13-5.15, 7.18-7.19, 8.10-8.11, 9.12-9.14, 10.9).
    Idempotent — checks if canary lesson '7.18' exists before inserting."""
    c = conn.cursor()
    if _exists(c, "lessons", "number", "7.18"):
        return
    from app.seed_augmented_content import (
        LESSONS_B1, LESSONS_B5, LESSONS_B7, LESSONS_B8, LESSONS_B9, LESSONS_B10,
    )
    for src in [LESSONS_B1, LESSONS_B5, LESSONS_B7, LESSONS_B8, LESSONS_B9, LESSONS_B10]:
        for fn in src:
            ld = fn()
            num = ld["number"]
            bn = int(num.split(".")[0])
            row = c.execute("SELECT id FROM blocks WHERE number=?", (bn,)).fetchone()
            if not row:
                continue
            block_id = row[0]
            if _exists(c, "lessons", "number", num):
                continue
            sections = json.loads(ld["sections_json"]) if isinstance(ld["sections_json"], str) else ld["sections_json"]
            content_payload = {
                "sections": sections,
                "minutes": ld.get("estimated_minutes", 45),
            }
            c.execute(
                "INSERT INTO lessons (block_id, number, title, content_json, difficulty, estimated_minutes, order_idx) VALUES (?,?,?,?,?,?,?)",
                (block_id, num, ld["title"], json.dumps(content_payload, ensure_ascii=False),
                 ld.get("difficulty", 2), ld.get("estimated_minutes", 45), int(num.split(".")[1]) - 1),
            )
            lesson_id = c.lastrowid
            for ex_data in ld["exercises"]:
                c.execute(
                    "INSERT INTO exercises (lesson_id, number, type, prompt, starter_code, solution_code, test_cases_json, hints_json, difficulty, expected_result_json) VALUES (?,?,?,?,?,?,?,?,?,?)",
                    (lesson_id, ex_data["number"], ex_data["type"], ex_data["prompt"],
                     ex_data["starter_code"], ex_data["solution_code"],
                     ex_data["test_cases_json"], ex_data["hints_json"],
                     ex_data["difficulty"], ex_data.get("expected_result_json")),
                )
    conn.commit()
    print("[migrate] Augmented lessons added.")


def _update_lesson_sections(conn, num, updater):
    """Add/replace sections in a lesson. `updater(sections)` returns modified sections list."""
    c = conn.cursor()
    row = c.execute("SELECT id, content_json FROM lessons WHERE number=?", (num,)).fetchone()
    if not row:
        return
    lid, cj = row
    data = json.loads(cj)
    sections = data.get("sections", [])
    old_len = len(sections)
    sections = updater(sections)
    if len(sections) != old_len:
        data["sections"] = sections
        c.execute("UPDATE lessons SET content_json=? WHERE id=?", (json.dumps(data, ensure_ascii=False), lid))
        conn.commit()

def _add_presentation_improvements(conn):
    """Debug challenges, recap quizzes, portfolio README, multiple testing fix."""
    # Debug challenges for 5 lessons
    debug_challenges = {
        "3.4": {
            "problem": "Почему этот код падает с ошибкой?",
            "buggy_code": "import pandas as pd\ndf = pd.read_csv('data.csv')\ndf['date'] = pd.to_datetime(df['date'])\ndf[df['date'] > '2020-01-01']  # KeyError: 'date'",
            "hint": "Проверь импорт данных — разделитель может отличаться",
            "fix": "pd.read_csv('data.csv', sep=';')  # или другой разделитель"
        },
        "5.6": {
            "problem": "Почему доверительный интервал несимметричный?",
            "buggy_code": "import numpy as np\ndata = np.random.exponential(1, 50)\nmean = np.mean(data)\nse = np.std(data) / np.sqrt(50)\nci = (mean - 1.96*se, mean + 1.96*se)  # CI symmetric, but data skewed!",
            "hint": "CLT требует n>30, но для экспоненциального 50 может быть мало",
            "fix": "Используй bootstrap для несимметричных CI"
        },
        "7.3": {
            "problem": "Почему accuracy на train 99%, а на test 52%?",
            "buggy_code": "from sklearn.ensemble import RandomForestClassifier\nfrom sklearn.model_selection import train_test_split\n\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)\nmodel = RandomForestClassifier(n_estimators=1000, max_depth=None, random_state=42)\nmodel.fit(X_train, y_train)\nprint(model.score(X_train, y_train))  # 0.99\nprint(model.score(X_test, y_test))    # 0.52",
            "hint": "Слишком сложное дерево без ограничений",
            "fix": "max_depth=10, min_samples_leaf=5 — ограничь сложность"
        },
        "8.4": {
            "problem": "StandardScaler испортил разреженные данные — почему?",
            "buggy_code": "from sklearn.preprocessing import StandardScaler\nimport numpy as np\n# One-hot encoded sparse data (mostly zeros)\nX = np.random.binomial(1, 0.1, (1000, 100))\nscaler = StandardScaler()\nX_scaled = scaler.fit_transform(X)  # Many values become -0.3...",
            "hint": "StandardScaler центрирует — разреженные перестают быть разреженными",
            "fix": "Для разреженных данных используй MaxAbsScaler или не центрируй"
        },
        "9.5": {
            "problem": "Почему эксперимент не воспроизводится?",
            "buggy_code": "import numpy as np\nimport pandas as pd\nfrom sklearn.ensemble import RandomForestClassifier\n\ndf = pd.read_csv('data.csv')\nX = df.drop('target', axis=1)\ny = df['target']\nmodel = RandomForestClassifier().fit(X, y)  # Different results every run!",
            "hint": "Нет random_state нигде",
            "fix": "np.random.seed(42); RandomForestClassifier(random_state=42)"
        },
    }
    for num, dc in debug_challenges.items():
        def _add_dc(sections, dc=dc):
            found = any(s.get("type") == "debug_challenge" for s in sections)
            if found:
                return sections
            sections.insert(4, {  # after summary
                "type": "debug_challenge",
                "problem": dc["problem"],
                "buggy_code": dc["buggy_code"],
                "hint": dc["hint"],
                "fix": dc["fix"],
            })
            return sections
        _update_lesson_sections(conn, num, _add_dc)

    # Cross-block recap quizzes (before first lesson of blocks 3-9)
    recap_data = {
        "3.1": "SQL: чем INNER JOIN отличается от LEFT JOIN? Оконные функции — что такое ROW_NUMBER? Что такое агрегатные функции и GROUP BY?",
        "4.1": "Pandas: как отфильтровать строки по условию? Как объединить два DataFrame? Что такое groupby и агрегация?",
        "5.1": "Pandas: что такое pivot и melt? Как очистить пропуски? Что такое merge и join?",
        "6.1": "Визуализация: какой тип графика для корреляции? Как построить box plot? Что такое Seaborn?",
        "7.1": "Статистика: что такое p-value? Доверительные интервалы — как считать? A/B тест — как работает?",
        "8.1": "ML: что такое переобучение? Как выбрать метрику? Что такое Random Forest?",
        "9.1": "Feature Engineering: как кодировать категории? Что такое StandardScaler? Как отбирать признаки?",
        "10.1": "DS-инструменты: Git, Docker, MLOps — зачем? Как структурировать ML-проект?",
    }
    for num, items_text in recap_data.items():
        items = [line.strip() for line in items_text.split("?") if line.strip()]
        items = [item + "?" for item in items]

        def _add_quiz(sections, items=items):
            found = any(s.get("type") == "recap_quiz" for s in sections)
            if found:
                return sections
            sections.insert(0, {
                "type": "recap_quiz",
                "items": items,
            })
            return sections
        _update_lesson_sections(conn, num, _add_quiz)

    # Portfolio README template → lesson 9.8
    def _add_readme(sections):
        found = any(s.get("type") == "portfolio_readme" for s in sections)
        if found:
            return sections
        sections.append({
            "type": "portfolio_readme",
            "content": (
                "# Project Title\n\n"
                "## Problem Statement\n_Business context and problem description._\n\n"
                "## Data\n- Source: _where from_\n- Size: _rows × columns_\n- Key features: _list_\n\n"
                "## Approach\n1. EDA\n2. Feature Engineering\n3. Modeling\n4. Validation\n\n"
                "## Results\n| Model | Accuracy | F1 |\n|-------|----------|----|\n| RF    | 0.87     | 0.85 |\n| XGB   | 0.91     | 0.89 |\n\n"
                "## Lessons Learned\n_Key takeaways._\n\n"
                "## How to Reproduce\n```bash\npip install -r requirements.txt\npython run.py\n```"
            ),
        })
        return sections
    _update_lesson_sections(conn, "9.8", _add_readme)

    # Multiple testing correction → lesson 5.8 theory
    c = conn.cursor()
    row = c.execute("SELECT id, content_json FROM lessons WHERE number='5.8'").fetchone()
    if row:
        lid, cj = row
        data = json.loads(cj)
        for s in data["sections"]:
            if s["type"] == "theory":
                if "Множественная проверка" in s["content"]:
                    break  # already added
                s["content"] += (
                    "\n\n**Важно: множественная проверка гипотез**\n"
                    "Если запускаете 20 A/B тестов одновременно, ожидайте 1 ложный "
                    "результат при α=0.05. **Коррекция**: Bonferroni (α/m), "
                    "FDR (Benjamini-Hochberg). Всегда указывайте primary metric "
                    "заранее — тест на одной метрике не требует коррекции."
                )
                c.execute("UPDATE lessons SET content_json=? WHERE id=?", (json.dumps(data, ensure_ascii=False), lid))
                conn.commit()
                break

    print("[migrate] Presentation improvements applied.")


def _add_roleplay_dialogues(conn):
    """
    Convert Block 10 interview_questions from plain strings to role-play format:
    HR (злой и коварный): question
    Я (наивный, робкий, но с добрым сердцем): answer
    Idempotent — skips lessons already in role-play format.
    """
    c = conn.cursor()
    rows = c.execute("""
        SELECT l.id, l.number, l.title, l.content_json
        FROM lessons l
        JOIN blocks b ON l.block_id = b.id
        WHERE b.number = 10
        ORDER BY l.number
    """).fetchall()

    dialogues = {
        "10.1": [
            ("Ну, рассказывай, чем ты вообще занимался в Data Science? Только без вот этой воды про «мне нравится анализировать данные», ладно?",
             "Я делал реальные проекты. Например, анализировал отток клиентов — сам собрал данные, почистил, обучил модель, завернул в FastAPI и задеплоил в Docker. Ещё A/B тесты считал с power analysis. Я понимаю, что мой опыт пока небольшой, но каждую задачу я стараюсь доделать до production, а не просто до тетрадки."),
            ("Ок, а почему ты хочешь работать именно у нас? Только учти — я слышала это сто раз.",
             "Честно — я изучил ваш продукт. Вы решаете задачу X, и у вас явно большой упор на качество данных. Мне откликается ваш подход к экспериментам (я читал ваш tech-блог). Я хочу расти как Data Scientist, и мне кажется, у вас я смогу учиться у сильных ребят и приносить реальную пользу."),
            ("Опиши свой самый сложный проект. Только покороче, у меня ещё 10 кандидатов сегодня.",
             "Самый сложный — прогнозирование оттока для SaaS-стартапа. Данных было мало (5000 строк), много пропусков. Я сделал EDA, применил KNNImputer, подобрал гиперпараметры через Optuna. Главная проблема — дисбаланс классов (23% оттока), использовал SMOTE и взвешенные классы. Модель дала ROC-AUC 0.87, задеплоил через FastAPI с мониторингом PSI."),
            ("А если бы ты сейчас начал этот проект заново — что бы сделал иначе?",
             "Я бы с самого начала поговорил с заказчиком, чтобы чётко понять бизнес-метрику — не accuracy, а сколько денег мы сохраняем. Я бы сделал более глубокий feature engineering с временными рядами. И обязательно настроил бы CI/CD для модели — в первый раз я про это забыл, и пришлось переделывать."),
        ],
        "10.2": [
            ("Ну, чем list от tuple отличается? Только не говори мне про immutable, это все знают.",
             "Да, immutable — это главное. Но кроме этого: tuple может быть ключом в словаре, а list — нет. Tuple занимает меньше памяти и создаётся быстрее. Ещё tuple используется для возврата нескольких значений из функции, а list — для однородных последовательностей, которые будут меняться."),
            ("Срезы в Python расскажи. Только без копипасты из документации.",
             "Срез — это sequence[start:stop:step]. start включается, stop — нет. Отрицательные индексы — с конца. Можно пропускать: s[:5] — первые 5, s[::-1] — разворот строки. Важно: для list срез возвращает новый список (shallow copy), а не view, как в NumPy."),
            ("List comprehension — это круто. А напиши comprehension, который достаёт из списка словарей все значения по ключу 'name', убирает None и сортирует.",
             "sorted([d['name'] for d in data if d.get('name') is not None]). Но если список большой, лучше генератор — sorted((d['name'] for d in data if ...)). Экономит память. А ещё больше двух if в comprehension лучше вынести в отдельную функцию."),
            ("А сборщик мусора? Расскажи, как работает. Только без «Python сам всё чистит».",
             "В CPython используется reference counting + generational GC. Счётчик ссылок — каждый объект знает, сколько раз на него ссылаются. Когда счётчик падает до 0 — объект сразу удаляется. Циклические ссылки обрабатывает generational GC (3 поколения)."),
        ],
        "10.3": [
            ("Декоратор напишешь? Только без примеров про логирование, это все умеют.",
             "Декоратор — функция, принимающая функцию и возвращающая функцию. Синтаксический сахар с @. Важно: использовать functools.wraps, чтобы сохранить __name__ и __doc__. Если с аргументами — тройная вложенность: def retry(n): def dec(func): @wraps(func) def wrapper(...): ... return wrapper; return dec."),
            ("GIL — что это и как с ним жить?",
             "Global Interpreter Lock — mutex, разрешающий только одному потоку выполнять байткод Python. Для CPU-bound задач threading бесполезен — нужен multiprocessing. Для I/O-bound — threading работает (GIL отпускается при ожидании). В numpy GIL не касается (C extensions)."),
            ("@staticmethod vs @classmethod — в чём разница? Объясни на примере из Data Science.",
             "@staticmethod — обычная функция внутри класса, не получает self или cls. @classmethod — получает cls как первый аргумент. Пример: класс Scaler. @classmethod from_config(cls, config) — альтернативный конструктор из YAML. @staticmethod validate_input(X) — проверка данных."),
            ("Контекстный менеджер with — реализуй свой. Только не копируй с StackOverflow.",
             "Класс с __enter__ и __exit__. Или @contextmanager с yield. Пример: менеджер подключения к БД — открывает соединение, передаёт курсор, закрывает при выходе даже при ошибке."),
        ],
        "10.4": [
            ("INNER JOIN от LEFT JOIN чем отличается? Быстро!",
             "INNER JOIN — только совпадающие строки в обеих таблицах. LEFT JOIN — все строки из левой + совпадающие из правой. Если в правой нет совпадения — NULL. Главная ошибка: писать условие на правую таблицу в WHERE при LEFT JOIN — это превращает его в INNER."),
            ("GROUP BY — что делает? И почему без агрегации падает?",
             "GROUP BY группирует строки по уникальным значениям. После GROUP BY в SELECT — только группируемые колонки или агрегатные функции. Иначе — ошибка (в строгих СУБД) или случайное значение (в MySQL)."),
            ("WHERE vs HAVING — один ответ, иначе не пройдёшь.",
             "WHERE — фильтр строк ДО группировки. HAVING — фильтр групп ПОСЛЕ агрегации. Порядок: FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY."),
            ("Первичный и внешний ключи — объясни как для стажёра.",
             "Первичный ключ (PRIMARY KEY) — уникальный идентификатор каждой строки. Не может быть NULL. Внешний ключ (FOREIGN KEY) — ссылается на первичный ключ другой таблицы, обеспечивает referential integrity."),
        ],
        "10.5": [
            ("Оконные функции — чем от GROUP BY отличаются? Я слушаю.",
             "GROUP BY схлопывает строки. Оконная функция считает по окну, но каждая строка остаётся. Синтаксис: SUM(col) OVER (PARTITION BY group_col ORDER BY order_col). PARTITION BY — как GROUP BY без схлопывания."),
            ("ROW_NUMBER от RANK — чем отличаются? Только быстро, у меня google meet через 5 минут.",
             "ROW_NUMBER — уникальный номер строки. RANK — одинаковые значения = одинаковый ранг, пропуски (1,2,2,4). DENSE_RANK — без пропусков (1,2,2,3). Для пагинации — ROW_NUMBER, для топ-N с одинаковыми — DENSE_RANK."),
            ("CTE — что это и зачем? Не говори «для читаемости», это банально.",
             "CTE (WITH) — именованный подзапрос. Можно ссылаться на один CTE несколько раз — выполнится один раз. WITH RECURSIVE — для иерархий (дерево категорий, оргструктура). Без него такие задачи решаются очень больно."),
            ("Медленный SQL-запрос. Что будешь делать?",
             "Смотрю EXPLAIN ANALYZE. Проверяю: все ли JOIN по индексам, нет ли Full Table Scan. Добавляю составные индексы. Самый частый косяк: SELECT * вместо конкретных колонок."),
        ],
        "10.6": [
            ("p-value — объясни как для пятиклассника. Только без «вероятность H0».",
             "p-value: «если бы никакого эффекта нет (H0 верна), какова вероятность увидеть такие данные или ещё экстремальнее?». Маленький p-value (<0.05): данные маловероятны при H0 → отвергаем H0. НО p-value ≠ P(H0|данные)!"),
            ("t-тест vs z-тест. Отличия. Быстро!",
             "z-тест — известна дисперсия совокупности и n>30. t-тест — дисперсия неизвестна. t-распределение шире для малых n. В реальной жизни t-тест почти всегда. В Python: scipy.stats.ttest_ind."),
            ("Центральная предельная теорема — что это даёт на практике?",
             "CLT: распределение выборочного среднего → нормальное при n>30. Практика: можем использовать z/t-тесты для не-нормальных данных, если n>30. Но CLT не гарантирует нормальность самих данных — только среднего."),
            ("Корреляция Пирсона vs Спирмена — когда что?",
             "Пирсон — линейная связь, требует нормальности. Спирмен — монотонная, работает с рангами. Если Пирсон=0.8, Спирмен=1 — связь есть, но нелинейная. В EDA смотрю обе."),
        ],
        "10.7": [
            ("Переобучение — что это и как бороться? Только не перечисляй всё подряд.",
             "Модель запомнила шум вместо сигнала: accuracy 99% на train и 70% на test. Причины: сложная модель, мало данных, data leakage. Борьба: CV, регуляризация, упрощение, больше данных, early stopping."),
            ("Random Forest vs градиентный бустинг — что выберешь и почему?",
             "Для табличных данных — бустинг (XGBoost, LightGBM), он точнее. RF — проще, меньше гиперпараметров, устойчивее к шуму. RF для быстрого baseline и малых данных, бустинг — когда нужна максимальная метрика."),
            ("Количество кластеров в K-Means — как выбрать? Только не говори «метод локтя».",
             "Метод локтя — первый шаг. Силуэтный коэффициент (ближе к 1 — лучше). Индекс Калински-Харабаса. Но главное — business interpretability: строю 3-5 вариантов и спрашиваю бизнес."),
            ("Дисбаланс классов — что делать? Только без SMOTE, это все знают.",
             "Начинаю с метрики: accuracy бесполезна при 99:1. Нужны precision, recall, F1, PR-AUC. Потом: взвешенные классы, изменение порога, undersampling. Лучший подход — собрать больше данных меньшинства."),
        ],
        "10.8": [
            ("Опиши полный цикл DS-проекта. Кратко, но без пропусков.",
             "1) Business Understanding — KPI. 2) Data Collection. 3) EDA. 4) Feature Engineering. 5) Baseline. 6) Iterate — гиперпараметры. 7) Validation. 8) Deploy — API, Docker. 9) Monitor — PSI, data drift. 10) Retrain."),
            ("Как выбираешь метрику для бизнес-задачи? Не говори F1, это слишком общо.",
             "Метрика = бизнес-цель. Отток — важнее recall. Кредитный скоринг — важнее precision. Всегда спрашиваю: «Что дороже — FP или FN?»."),
            ("Конфликт в команде — расскажи, как решал. Только без «мы поговорили и всё решили».",
             "Спорили XGBoost vs нейросеть. Вместо «кто прав» — сделали оба подхода за 2 дня и сравнили. XGBoost победил. Если бы нейросеть оказалась лучше — я бы первый признал. Урок: проверяем данными."),
            ("MDE в A/B тестировании — что это и почему важно?",
             "MDE — Minimum Detectable Effect. Минимальный эффект, который тест обнаружит с power=80%. MDE обратно связан с n: хотим 1% — нужны сотни тысяч. Без MDE тест либо ничего не покажет, либо сожрёт ресурсы."),
        ],
    }

    any_fixed = False
    for lid, num, title, cj in rows:
        data = json.loads(cj)
        sections = data["sections"]
        num_dialogues = dialogues.get(num)
        if not num_dialogues:
            continue
        changed = False
        for s in sections:
            if s["type"] == "interview_questions":
                items = s.get("items", [])
                if items and isinstance(items[0], str) and "HR (злой и коварный)" in items[0]:
                    continue
                new_items = []
                for q, a in num_dialogues:
                    new_items.append(
                        "**HR (злой и коварный):** " + q +
                        "\n\n**Я (наивный, робкий, но с добрым сердцем):** " + a
                    )
                s["items"] = new_items
                changed = True
                break
        if changed:
            c.execute("UPDATE lessons SET content_json=? WHERE id=?", (json.dumps(data, ensure_ascii=False), lid))
            any_fixed = True

    if any_fixed:
        conn.commit()
        print("[migrate] Role-play dialogues applied.")

def _add_block11_project(conn):
    """Create Block 11 (Финальный проект) and move lesson 10.10 → 11.1."""
    c = conn.cursor()
    # Create block 11 if missing
    row = c.execute("SELECT id FROM blocks WHERE number=11").fetchone()
    if not row:
        c.execute(
            "INSERT INTO blocks (number, title, description, theme) VALUES (?, ?, ?, ?)",
            (11, "Финальный проект",
             "Capstone-проекты: Космос (анализ миссий NASA) и Игры (анализ поведения игроков).",
             "neutral"),
        )
        block_id = c.lastrowid
        print("[migrate] Block 11 created.")
    else:
        block_id = row[0]

    # Remove lesson 10.10 if it exists (was moved to 11.1)
    c.execute("DELETE FROM lessons WHERE number='10.10'")

    def _insert_b11_lesson(fn, num, order):
        ld = fn()
        sections = json.loads(ld["sections_json"]) if isinstance(ld["sections_json"], str) else ld["sections_json"]
        content_payload = {
            "sections": sections,
            "minutes": ld.get("estimated_minutes", 45),
        }
        c.execute(
            "INSERT INTO lessons (block_id, number, title, content_json, difficulty, estimated_minutes, order_idx) VALUES (?,?,?,?,?,?,?)",
            (block_id, num, ld["title"], json.dumps(content_payload, ensure_ascii=False),
             ld.get("difficulty", 2), ld.get("estimated_minutes", 45), order),
        )
        lesson_id = c.lastrowid
        for ex_data in ld["exercises"]:
            c.execute(
                "INSERT INTO exercises (lesson_id, number, type, prompt, starter_code, solution_code, test_cases_json, hints_json, difficulty, expected_result_json) VALUES (?,?,?,?,?,?,?,?,?,?)",
                (lesson_id, ex_data["number"], ex_data["type"], ex_data["prompt"],
                 ex_data["starter_code"], ex_data["solution_code"],
                 ex_data["test_cases_json"], ex_data["hints_json"],
                 ex_data["difficulty"], ex_data.get("expected_result_json")),
            )
        print(f"[migrate] Lesson {num} added.")

    from app.seed_augmented_content import _11_1, _11_2, _11_3
    for fn, num, order in [(_11_1, "11.1", 0), (_11_2, "11.2", 1), (_11_3, "11.3", 2)]:
        if not c.execute("SELECT 1 FROM lessons WHERE number=?", (num,)).fetchone():
            _insert_b11_lesson(fn, num, order)
        else:
            print(f"[migrate] Lesson {num} already exists, skipped.")

    conn.commit()


if __name__ == "__main__":
    run_migrations()
