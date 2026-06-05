"""
Блок 6: EDA — Исследовательский анализ данных.
8 уроков, ~70 упражнений.
Темы: первичный осмотр, числовые/категориальные переменные, взаимосвязи,
выбросы, гипотезы, SpaceX mini-EDA.
"""
from app.seed_helpers import (
    ex, lesson, theory, analogy, visual, example,
    common_mistakes, interview_questions, knowledge_checklist,
)


def _6_1():
    return lesson(
        "6.1", "Что такое EDA и зачем он нужен", "space", [
            theory(
                "**EDA (Exploratory Data Analysis)** — исследовательский анализ "
                "данных. Это первый и критически важный этап любого DS-проекта.\n\n"
                "**Цели EDA:**\n"
                "1. Понять структуру данных: формы, типы, размеры\n"
                "2. Обнаружить аномалии: пропуски, дубликаты, выбросы\n"
                "3. Найти закономерности: тренды, группы, корреляции\n"
                "4. Сформулировать гипотезы для формального тестирования\n"
                "5. Проверить предположения перед моделированием\n\n"
                "**Кто это делает:**\n"
                "- **Data Analyst** — отвечает на бизнес-вопросы\n"
                "- **Data Scientist** — строит модели (EDA — это подготовка)\n"
                "- **ML Engineer** — проверяет данные перед пайплайном\n\n"
                "**Типичный workflow EDA:**\n"
                "1. `df.shape`, `df.info()`, `df.head()` — структура\n"
                "2. `df.describe()` — числовые статистики\n"
                "3. Подсчёт пропусков и дубликатов\n"
                "4. Гистограммы и box plots для числовых\n"
                "5. Bar charts для категориальных\n"
                "6. Корреляционная матрица и scatter plot\n"
                "7. Анализ выбросов\n"
                "8. Feature engineering на основе наблюдений\n\n"
                "**Почему EDA — это важно?**\n"
                "Garbage in — garbage out. Если данные грязные, модель будет плохой. "
                "Часто 70% времени уходит на EDA и очистку, 20% — на фичи, 10% — на "
                "саму модель.\n\n"
                "**Культовая цитата** (Джон Тьюки, изобретатель EDA): "
                "«Гораздо лучше приблизительный ответ на правильный вопрос, который "
                "часто бывает расплывчатым, чем точный ответ на неправильный вопрос»."
            ),
            analogy(
                "EDA — медосмотр перед марафоном: проверяешь здоровье, бежишь пробежку, "
                "смотришь пульс. Без медосмотра можно не дойти до финиша.",
                "EDA датасета SpaceX-миссий: проверяем пропуски в `payload_mass`, "
                "изучаем распределение стоимости запуска, ищем выбросы."
            ),
            visual(
                "EDA воронка: от широкого к узкому",
                "        ┌──────────────────────┐\n"
                "        │  Все данные (N=100k) │\n"
                "        └──────────┬───────────┘\n"
                "                   ↓ df.info()\n"
                "        ┌──────────────────────┐\n"
                "        │ Типы, пропуски, дубли│\n"
                "        └──────────┬───────────┘\n"
                "                   ↓ df.describe()\n"
                "        ┌──────────────────────┐\n"
                "        │ Статистики по колонкам│\n"
                "        └──────────┬───────────┘\n"
                "                   ↓ визуализация\n"
                "        ┌──────────────────────┐\n"
                "        │ Гистограммы, scatter │\n"
                "        └──────────┬───────────┘\n"
                "                   ↓ корреляции\n"
                "        ┌──────────────────────┐\n"
                "        │ Матрица, выбросы     │\n"
                "        └──────────┬───────────┘\n"
                "                   ↓ гипотезы\n"
                "        ┌──────────────────────┐\n"
                "        │ Что проверять?       │\n"
                "        └──────────────────────┘"
            ),
            example(
                "EDA на синтетическом датасете космических миссий.",
                "Создадим DataFrame с 4 колонками, посмотрим структуру, базовые "
                "статистики, пропуски.",
                "import pandas as pd\n"
                "import numpy as np\n"
                "np.random.seed(42)\n"
                "df = pd.DataFrame({\n"
                "    'mission': ['Apollo', 'Vostok', 'Mercury', 'Gemini', 'Soyuz'],\n"
                "    'year': [1969, 1961, 1962, 1965, 1967],\n"
                "    'duration_days': [8, 1, 0.5, 4, 3],\n"
                "    'success': [1, 1, 0, 1, 1]\n"
                "})\n"
                "print('Shape:', df.shape)\n"
                "print(df.head())\n"
                "print('\\nInfo:')\n"
                "df.info()\n"
                "print('\\nDescribe:')\n"
                "print(df.describe())",
                "Shape: (5, 4)\n  mission  year  duration_days  success\n0  Apollo  1969             8.0        1\n1  Vostok  1961             1.0        1\n2 Mercury  1962             0.5        0\n3  Gemini  1965             4.0        1\n4   Soyuz  1967             3.0        1\n\nInfo:\n<class 'pandas.core.frame.DataFrame'>\nRangeIndex: 5 entries, 0 to 4\n...\n\nDescribe:\n       year  duration_days   success\ncount    5.0       5.000000  5.000000\nmean  1964.8       3.300000  0.800000\nstd      3.3       2.912931  0.447214\n...",
                "df.shape показывает 5 строк, 4 колонки. df.info() выводит типы и "
                "пропуски. df.describe() — count/mean/std/min/max для числовых."
            ),
            common_mistakes([
                {"mistake": "Пропустить EDA и сразу обучать модель", "why_bad": "Модель на грязных данных будет плохой", "fix": "Всегда начинай с EDA"},
                {"mistake": "Игнорировать пропуски", "why_bad": "NaN ломает многие алгоритмы", "fix": "Проверь df.isnull().sum()"},
                {"mistake": "Доверять df.describe() без визуализации", "why_bad": "Среднее не описывает форму", "fix": "Гистограмма для каждой числовой колонки"},
                {"mistake": "Забыть проверить дубликаты", "why_bad": "Дубликаты искажают статистики", "fix": "df.duplicated().sum()"},
            ]),
            interview_questions([
                {"q": "Что такое EDA и зачем он?", "a": "Исследовательский анализ данных — этап, на котором понимаешь структуру, находишь аномалии, формулируешь гипотезы. Без EDA модель может быть построена на грязных данных."},
                {"q": "Какие шаги включает EDA?", "a": "Структура (shape, info, head), статистики (describe), пропуски (isnull), дубликаты, распределения (hist, boxplot), корреляции, выбросы, гипотезы."},
                {"q": "Чем EDA отличается от препроцессинга?", "a": "EDA — это понимание данных (исследование). Препроцессинг — очистка и трансформация на основе понимания. EDA идёт первым."},
            ]),
            knowledge_checklist([
                "Знаю цели EDA",
                "Использую df.shape, df.info(), df.head()",
                "Использую df.describe()",
                "Проверяю пропуски через df.isnull().sum()",
                "Проверяю дубликаты через df.duplicated()",
                "Понимаю, что EDA предшествует моделированию",
            ]),
        ],
        exercises=[
            ex(1, "python", "Дан `df` с 3 колонками `a, b, c` и 10 строками. Сохрани shape в `shape`.",
               "import pandas as pd\ndf = pd.DataFrame({'a': range(10), 'b': range(10), 'c': range(10)})\nshape = (0, 0)\n",
               "import pandas as pd\ndf = pd.DataFrame({'a': range(10), 'b': range(10), 'c': range(10)})\nshape = df.shape",
               [{"check": "shape == (10, 3)", "msg": "shape = (10, 3)"}],
               ["df.shape → кортеж (rows, cols)"], 1),
            ex(2, "python", "Дан `df`. Сохрани список колонок в `cols`.",
               "import pandas as pd\ndf = pd.DataFrame({'a': [1,2], 'b': [3,4]})\ncols = []\n",
               "import pandas as pd\ndf = pd.DataFrame({'a': [1,2], 'b': [3,4]})\ncols = df.columns.tolist()",
               [{"check": "'a' in cols and 'b' in cols", "msg": "Колонки a и b присутствуют"}],
               ["df.columns.tolist()", "Или list(df.columns)"], 1),
            ex(3, "python", "Дан `df` с 5 строками. Сохрани тип данных колонки `a` в `dtype_a`.",
               "import pandas as pd\ndf = pd.DataFrame({'a': [1, 2, 3, 4, 5]})\ndtype_a = ''\n",
               "import pandas as pd\ndf = pd.DataFrame({'a': [1, 2, 3, 4, 5]})\ndtype_a = df['a'].dtype",
               [{"check": "dtype_a.name == 'int64' or 'int' in str(dtype_a)", "msg": "Тип int"}],
               ["df['a'].dtype", ".name — строковое представление"], 1),
            ex(4, "python", "Дан `df` с колонкой `x` (5 значений, 2 NaN). Сохрани число пропусков в `n_null`.",
               "import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({'x': [1, 2, np.nan, 4, np.nan]})\nn_null = 0\n",
               "import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({'x': [1, 2, np.nan, 4, np.nan]})\nn_null = df['x'].isnull().sum()",
               [{"check": "n_null == 2", "msg": "2 пропуска"}],
               ["df['x'].isnull().sum()", "isnull → bool → sum = число True"], 1),
            ex(5, "python", "Дан `df` с дубликатами строк. Сохрани число дубликатов в `n_dup`.",
               "import pandas as pd\ndf = pd.DataFrame({'a': [1, 2, 2, 3, 3, 3]})\nn_dup = 0\n",
               "import pandas as pd\ndf = pd.DataFrame({'a': [1, 2, 2, 3, 3, 3]})\nn_dup = df.duplicated().sum()",
               [{"check": "n_dup == 3", "msg": "3 дубликата (2-ой, 3-ий, 5-ый)"}],
               ["df.duplicated()", ".sum() — число True"], 2),
            ex(6, "python", "Дан `df` с 2 колонками. Получи первые 3 строки, сохрани в `head3`.",
               "import pandas as pd\ndf = pd.DataFrame({'a': [1,2,3,4,5], 'b': [10,20,30,40,50]})\nhead3 = None\n",
               "import pandas as pd\ndf = pd.DataFrame({'a': [1,2,3,4,5], 'b': [10,20,30,40,50]})\nhead3 = df.head(3)",
               [{"check": "head3.shape == (3, 2)", "msg": "3 строки, 2 колонки"}],
               ["df.head(n)", "По умолчанию n=5"], 1),
            ex(7, "python", "Дан `df` с 4 строками. Получи последние 2 строки, сохрани в `tail2`.",
               "import pandas as pd\ndf = pd.DataFrame({'a': [1,2,3,4]})\ntail2 = None\n",
               "import pandas as pd\ndf = pd.DataFrame({'a': [1,2,3,4]})\ntail2 = df.tail(2)",
               [{"check": "tail2.shape == (2, 1)", "msg": "2 строки, 1 колонка"}],
               ["df.tail(n)", "Последние n строк"], 1),
            ex(8, "python", "Дан `df` с числовыми колонками. Получи описательные статистики, сохрани в `stats`.",
               "import pandas as pd\ndf = pd.DataFrame({'a': [1, 2, 3, 4, 5], 'b': [10, 20, 30, 40, 50]})\nstats = None\n",
               "import pandas as pd\ndf = pd.DataFrame({'a': [1, 2, 3, 4, 5], 'b': [10, 20, 30, 40, 50]})\nstats = df.describe()",
               [{"check": "stats.loc['mean', 'a'] == 3.0", "msg": "Mean колонки a = 3"}],
               ["df.describe()", "Возвращает count, mean, std, min, 25%, 50%, 75%, max"], 2),
        ],
        minutes=40, difficulty=2,
    )


def _6_2():
    return lesson(
        "6.2", "Первичный осмотр датасета", "space", [
            theory(
                "**Первичный осмотр** — первый взгляд на датасет, чтобы понять его "
                "«анатомию». Цель — за 5 минут понять, с чем ты работаешь.\n\n"
                "**Обязательные команды:**\n"
                "```python\n"
                "df.shape           # размер (rows, cols)\n"
                "df.info()          # типы, пропуски, память\n"
                "df.head(3)         # первые строки\n"
                "df.tail(3)         # последние строки\n"
                "df.dtypes          # типы колонок\n"
                "df.columns         # имена колонок\n"
                "df.isnull().sum()  # пропуски по колонкам\n"
                "df.nunique()       # уникальные значения\n"
                "df.describe()      # статистики для числовых\n"
                "df.describe(include='object')  # для категориальных\n"
                "```\n\n"
                "**На что смотреть:**\n"
                "1. **Размер**: сколько строк/колонок? Достаточно для модели?\n"
                "2. **Типы**: int/float/object/bool/datetime. Можно ли привести к "
                "нужному типу?\n"
                "3. **Пропуски**: где, сколько, паттерн (случайные/системные)?\n"
                "4. **Дубликаты**: полные или частичные?\n"
                "5. **Уникальные значения**: id-шники, категории, а может быть "
                "константы?\n"
                "6. **Распределения**: симметричные/скошенные?\n\n"
                "**Стоп-сигналы:**\n"
                "- Колонка с одним значением → не несёт информации\n"
                "- >50% пропусков → подумай, нужна ли вообще\n"
                "- 100% уникальных ID → возможно, не нужна как фича\n"
                "- Подозрительные min/max (отрицательный возраст, цена 0)\n\n"
                "**Инструменты:**\n"
                "- Pandas — основной\n"
                "- `pandas-profiling` / `ydata-profiling` — авто-отчёт\n"
                "- `sweetviz` — сравнение двух датасетов"
            ),
            analogy(
                "Первичный осмотр — открыть коробку с деталями LEGO: посмотреть, какие "
                "есть кусочки, сколько, что не хватает, что повреждено.",
                "Открываем CSV с миссиями SpaceX: 200 миссий, 10 колонок, в "
                "`payload_mass` 5% пропусков, в `outcome` всё OK."
            ),
            visual(
                "Чек-лист первичного осмотра",
                "   1. df.shape        → (N_rows, N_cols)\n"
                "   2. df.info()       → dtypes + non-null\n"
                "   3. df.head(3)      → первые строки\n"
                "   4. df.describe()   → mean, std, min, max\n"
                "   5. df.isnull().sum() → пропуски\n"
                "   6. df.nunique()    → уникальные\n"
                "   7. df.duplicated() → дубли\n"
                "   8. df.dtypes       → типы колонок\n"
                "\n"
                "   ⏱️ Должно занимать 2-5 минут"
            ),
            example(
                "EDA датасета миссий SpaceX.",
                "Сгенерируем 100 миссий с реалистичными колонками, пройдёмся по "
                "чек-листу.",
                "import pandas as pd\n"
                "import numpy as np\n"
                "np.random.seed(42)\n"
                "df = pd.DataFrame({\n"
                "    'mission_id': range(1, 101),\n"
                "    'rocket': np.random.choice(['Falcon 9', 'Falcon Heavy'], 100),\n"
                "    'year': np.random.choice(range(2010, 2024), 100),\n"
                "    'payload_kg': np.random.exponential(5000, 100),\n"
                "    'success': np.random.binomial(1, 0.95, 100)\n"
                "})\n"
                "print('Shape:', df.shape)\n"
                "print('\\nInfo:')\n"
                "df.info()\n"
                "print('\\nMissing:')\n"
                "print(df.isnull().sum())\n"
                "print('\\nDuplicates:', df.duplicated().sum())\n"
                "print('\\nDescribe:')\n"
                "print(df.describe())",
                "Shape: (100, 5)\n...\nMissing:\nmission_id    0\nrocket        0\nyear          0\npayload_kg    0\nsuccess       0\ndtype: int64\n\nDuplicates: 0\n\nDescribe:\n       mission_id    year  payload_kg    success\ncount       100.0  100.0  100.000000  100.000000\nmean         50.5  2016.5  4857.000000    0.960000\nstd          29.0     4.0  5042.000000    0.197000\nmin           1.0  2010.0    72.500000    0.000000\n25%          25.8  2013.0  1521.000000    1.000000\n...",
                "100 строк, 5 колонок. Нет пропусков и дубликатов. У mission_id 100 "
                "уникальных (ID). У rocket 2 уникальных. payload_kg сильно "
                "скошен (mean=4857, min=72)."
            ),
            common_mistakes([
                {"mistake": "df.shape не использовать", "why_bad": "Не знаешь размер — не знаешь, с чем работаешь", "fix": "Всегда начинай с shape"},
                {"mistake": "Забыть df.isnull().sum()", "why_bad": "Пропуски в данных — частая причина ошибок", "fix": "Всегда проверяй пропуски"},
                {"mistake": "Игнорировать describe()", "why_bad": "Пропустишь выбросы (max=999999)", "fix": "Смотри min/max в describe"},
                {"mistake": "Не проверить nunique()", "why_bad": "Колонка-константа бесполезна", "fix": "df.nunique() для всех колонок"},
            ]),
            interview_questions([
                {"q": "С чего начать EDA?", "a": "df.shape, df.info(), df.head(3), df.describe(), df.isnull().sum(), df.duplicated().sum(), df.nunique(). Это занимает 2-5 минут и даёт 80% понимания."},
                {"q": "Как найти дубликаты?", "a": "df.duplicated() возвращает bool Series. df.duplicated().sum() — число дублей. df.duplicated(subset=['col']) — по конкретной колонке. df.drop_duplicates() — удалить."},
                {"q": "Как понять, нужна ли колонка с 50% пропусков?", "a": "Зависит от бизнеса. Если 50% пропусков не случайны (например, новая фича записывается только для премиум-юзеров) — это сигнал. Если случайны — лучше удалить или импутировать."},
            ]),
            knowledge_checklist([
                "Использую df.shape, df.info(), df.head()",
                "Проверяю df.isnull().sum()",
                "Проверяю df.duplicated().sum()",
                "Смотрю df.describe() для числовых",
                "Смотрю df.describe(include='object') для категорий",
                "Проверяю df.nunique()",
            ]),
        ],
        exercises=[
            ex(1, "python", "Дан `df` с 4 колонками (a, b, c, d), 50 строк. Сохрани shape в `shape`.",
               "import pandas as pd\nimport numpy as np\nnp.random.seed(42)\ndf = pd.DataFrame(np.random.randn(50, 4), columns=['a', 'b', 'c', 'd'])\nshape = (0, 0)\n",
               "import pandas as pd\nimport numpy as np\nnp.random.seed(42)\ndf = pd.DataFrame(np.random.randn(50, 4), columns=['a', 'b', 'c', 'd'])\nshape = df.shape",
               [{"check": "shape == (50, 4)", "msg": "shape = (50, 4)"}],
               ["df.shape"], 1),
            ex(2, "python", "Дан `df`. Посчитай число пропусков в каждой колонке, сохрани Series в `nulls`.",
               "import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({'a': [1, 2, np.nan], 'b': [np.nan, 2, 3], 'c': [1, 2, 3]})\nnulls = None\n",
               "import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({'a': [1, 2, np.nan], 'b': [np.nan, 2, 3], 'c': [1, 2, 3]})\nnulls = df.isnull().sum()",
               [{"check": "nulls['a'] == 1 and nulls['b'] == 1 and nulls['c'] == 0", "msg": "a=1, b=1, c=0"}],
               ["df.isnull().sum()"], 1),
            ex(3, "python", "Дан `df`. Удали дубликаты строк, сохрани результат в `df_dedup`.",
               "import pandas as pd\ndf = pd.DataFrame({'a': [1, 2, 2, 3], 'b': [10, 20, 20, 30]})\ndf_dedup = df\n",
               "import pandas as pd\ndf = pd.DataFrame({'a': [1, 2, 2, 3], 'b': [10, 20, 20, 30]})\ndf_dedup = df.drop_duplicates()",
               [{"check": "df_dedup.shape[0] == 3", "msg": "3 уникальных строки"}],
               ["df.drop_duplicates()", "Возвращает новый DataFrame"], 1),
            ex(4, "python", "Дан `df`. Посчитай уникальные значения в колонке `cat`, сохрани в `n`.",
               "import pandas as pd\ndf = pd.DataFrame({'cat': ['A', 'B', 'A', 'C', 'B', 'A']})\nn = 0\n",
               "import pandas as pd\ndf = pd.DataFrame({'cat': ['A', 'B', 'A', 'C', 'B', 'A']})\nn = df['cat'].nunique()",
               [{"check": "n == 3", "msg": "3 уникальных: A, B, C"}],
               ["df['cat'].nunique()"], 1),
            ex(5, "python", "Дан `df`. Получи описательные статистики для всех колонок (включая категориальные), сохрани в `stats`.",
               "import pandas as pd\ndf = pd.DataFrame({'a': [1, 2, 3], 'b': ['x', 'y', 'z']})\nstats = None\n",
               "import pandas as pd\ndf = pd.DataFrame({'a': [1, 2, 3], 'b': ['x', 'y', 'z']})\nstats = df.describe(include='all')",
               [{"check": "'top' in stats.index or 'unique' in stats.index", "msg": "Категориальные статистики"}],
               ["df.describe(include='all')", "include='all' для всех типов"], 2),
            ex(6, "python", "Дан `df` с пропусками в `x`. Заполни их средним, сохрани в `df_filled`.",
               "import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({'x': [1, 2, np.nan, 4, 5]})\ndf_filled = df\n",
               "import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({'x': [1, 2, np.nan, 4, 5]})\ndf_filled = df.fillna(df['x'].mean())",
               [{"check": "df_filled['x'].isnull().sum() == 0", "msg": "Нет пропусков после fillna"}],
               ["df.fillna(value)", "value = среднее"], 2),
            ex(7, "python", "Дан `df`. Посчитай % пропусков в каждой колонке, сохрани Series в `null_pct`.",
               "import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({'a': [1, np.nan, 3, 4], 'b': [1, 2, 3, 4]})\nnull_pct = None\n",
               "import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({'a': [1, np.nan, 3, 4], 'b': [1, 2, 3, 4]})\nnull_pct = (df.isnull().sum() / len(df)) * 100",
               [{"check": "abs(null_pct['a'] - 25) < 0.01 and null_pct['b'] == 0", "msg": "a=25%, b=0%"}],
               ["df.isnull().sum() / len(df) * 100", "Процент"], 2),
            ex(8, "python", "Дан `df` с колонкой `value`. Удали строки, где `value` пропущено. Сохрани в `df_clean`.",
               "import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({'value': [1, 2, np.nan, 4, np.nan, 6]})\ndf_clean = df\n",
               "import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({'value': [1, 2, np.nan, 4, np.nan, 6]})\ndf_clean = df.dropna(subset=['value'])",
               [{"check": "df_clean.shape[0] == 4", "msg": "4 строки без пропусков"}],
               ["df.dropna(subset=['col'])", "Удаляет строки с NaN в col"], 2),
        ],
        minutes=45, difficulty=2,
    )


def _6_3():
    return lesson(
        "6.3", "Анализ числовых переменных", "space", [
            theory(
                "**Числовые переменные** принимают количественные значения: "
                "рост, температура, время, цена, количество.\n\n"
                "**Основные шаги анализа:**\n"
                "1. **Центральная тенденция**: mean, median\n"
                "2. **Разброс**: std, IQR, range\n"
                "3. **Распределение**: гистограмма, KDE, QQ-plot\n"
                "4. **Выбросы**: box plot, правило 1.5*IQR\n"
                "5. **Трансформации**: log, sqrt, Box-Cox (если скошено)\n\n"
                "**Визуализации:**\n"
                "- **Гистограмма** (`plt.hist`): распределение значений\n"
                "- **Box plot** (`plt.boxplot`): квартили + выбросы\n"
                "- **KDE** (kernel density estimate): сглаженная гистограмма\n"
                "- **Scatter** (`plt.scatter`): связь двух переменных\n"
                "- **Heatmap корреляций**: матрица попарных корреляций\n\n"
                "**Что искать в распределении:**\n"
                "- **Симметрия**: симметричное (нормальное) или скошенное\n"
                "- **Модальность**: 1 пик (унимодальное), 2 (бимодальное), много\n"
                "- **Тяжёлые хвосты**: больше выбросов, чем нормальное\n"
                "- **Выбросы**: явно отдельно стоящие значения\n\n"
                "**Скошенные данные** часто логнормальные (доходы, время). Применяют "
                "**логарифмирование**: `np.log1p(x)`. После log распределение "
                "становится более симметричным.\n\n"
                "**Боксплот показывает:**\n"
                "- Ящик = IQR (Q1 до Q3)\n"
                "- Линия в ящике = медиана\n"
                "- Усы = Q1-1.5*IQR и Q3+1.5*IQR\n"
                "- Точки за усами = выбросы"
            ),
            analogy(
                "Анализ числовой переменной — измерение температуры в городе за год: "
                "среднее, экстремумы, как часто бывает жарко/холодно.",
                "Анализ `payload_kg` миссий SpaceX: среднее 5000 кг, медиана 3000 — "
                "распределение скошено, есть сверхтяжёлые Falcon Heavy."
            ),
            visual(
                "Гистограмма vs Box plot для одной переменной",
                "   Гистограмма         Box plot\n"
                "   ┌──────────┐\n"
                "   │   ▓▓▓    │       ┌─┬───┬──┐\n"
                "   │  ▓▓▓▓▓   │       │ │ ▓ │  │ ── outliers\n"
                "   │ ▓▓▓▓▓▓▓  │       │ │   │  │\n"
                "   │▓▓▓▓▓▓▓▓▓▓│       └─┴───┴──┘\n"
                "   │ ▓▓▓▓▓▓▓  │        Q1  Q3\n"
                "   │  ▓▓▓▓    │\n"
                "   └──────────┘\n"
                "   Симметричное   \n"
                "   распределение\n"
                "\n"
                "   Гистограмма показывает форму,\n"
                "   box plot — квартили и выбросы"
            ),
            example(
                "Анализ числовой колонки `payload_kg` в синтетических данных миссий.",
                "Используем describe для статистик, plt.hist для распределения, "
                "plt.boxplot для выбросов.",
                "import numpy as np\n"
                "import pandas as pd\n"
                "import matplotlib.pyplot as plt\n"
                "np.random.seed(42)\n"
                "df = pd.DataFrame({\n"
                "    'payload_kg': np.concatenate([\n"
                "        np.random.exponential(3000, 95),\n"
                "        [50000, 60000, 70000, 80000, 90000]  # 5 выбросов\n"
                "    ])\n"
                "})\n"
                "print(df['payload_kg'].describe())\n"
                "fig, axes = plt.subplots(1, 2, figsize=(12, 4))\n"
                "axes[0].hist(df['payload_kg'], bins=30, color='steelblue', edgecolor='black')\n"
                "axes[0].set_title('Гистограмма payload_kg')\n"
                "axes[1].boxplot(df['payload_kg'])\n"
                "axes[1].set_title('Box plot payload_kg')\n"
                "plt.tight_layout()\n"
                "plt.show()",
                "count    100.000000\nmean     6418.842050\nstd     13248.601...\nmin        32.4...\n25%      1450...\n50%      2120...\n75%      4330...\nmax     90000.000000\n(график)",
                "Гистограмма: пик у 0-2000, длинный хвост. Box plot показывает 5 "
                "выбросов (50k-90k). Mean (6418) > median (2120) — скошено вправо. "
                "Для анализа лучше использовать log-трансформацию."
            ),
            common_mistakes([
                {"mistake": "Использовать mean для скошенных данных", "why_bad": "Среднее не описывает типичное", "fix": "Median + log-трансформация"},
                {"mistake": "Игнорировать box plot", "why_bad": "Пропустишь выбросы", "fix": "Строй box plot для каждой числовой"},
                {"mistake": "Не логарифмировать скошенные данные", "why_bad": "Анализ на скошенных данных менее надёжен", "fix": "np.log1p(x) для скошенных"},
                {"mistake": "Строить гистограмму с одним bin", "why_bad": "Не видно форму", "fix": "bins=30-50 для 1000+ точек"},
            ]),
            interview_questions([
                {"q": "Когда использовать log-трансформацию?", "a": "Когда данные скошены вправо (правосторонняя асимметрия), имеют широкий диапазон (1-1000000), или когда отношения важнее разностей (цена 100→200 = +100%, 1000→1100 = +10%). Log выравнивает диапазон."},
                {"q": "Что показывает box plot?", "a": "5 статистик: min, Q1, median, Q3, max. Плюс выбросы за пределами 1.5*IQR. Удобен для сравнения распределений нескольких групп."},
                {"q": "Что такое KDE?", "a": "Kernel Density Estimate — сглаженная гистограмма. Показывает плотность распределения. Лучше гистограммы для визуального сравнения, но зависит от bandwidth."},
            ]),
            knowledge_checklist([
                "Строю plt.hist для распределения",
                "Строю plt.boxplot для выбросов",
                "Применяю np.log1p для скошенных данных",
                "Считаю mean, median, std, IQR",
                "Использую df.describe()",
                "Визуализирую KDE через sns.kdeplot или plt.hist(density=True)",
            ]),
        ],
        exercises=[
            ex(1, "python", "Дан `df` с колонкой `x` (1000 значений из exp(3)). Посчитай mean, median, std. Сохрани в `m, med, s`.",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.random.exponential(3, 1000)})\nm, med, s = 0, 0, 0\n",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.random.exponential(3, 1000)})\nm = df['x'].mean()\nmed = df['x'].median()\ns = df['x'].std()",
               [{"check": "abs(m - 3) < 0.5", "msg": "mean ≈ 3"},
                {"check": "med < m", "msg": "median < mean (правоскошено)"}],
               ["df['x'].mean()", "df['x'].median()", "df['x'].std()"], 2),
            ex(2, "python", "Дан `df` с колонкой `x`. Построй гистограмму (30 корзин).",
               "import matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.random.normal(0, 1, 1000)})\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.random.normal(0, 1, 1000)})\nplt.hist(df['x'], bins=30)\nplt.show()",
               [{"check": "True", "msg": "Гистограмма построена"}],
               ["plt.hist(df['x'], bins=30)"], 1),
            ex(3, "python", "Дан `df` с колонкой `x` (1000 значений, 5 выбросов). Построй box plot.",
               "import matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\nnp.random.seed(42)\nx = np.concatenate([np.random.normal(0, 1, 995), [10, -10, 12, -12, 15]])\ndf = pd.DataFrame({'x': x})\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\nnp.random.seed(42)\nx = np.concatenate([np.random.normal(0, 1, 995), [10, -10, 12, -12, 15]])\ndf = pd.DataFrame({'x': x})\nplt.boxplot(df['x'])\nplt.show()",
               [{"check": "True", "msg": "Box plot построен"}],
               ["plt.boxplot(df['x'])"], 1),
            ex(4, "python", "Дан `df` с колонкой `x` (скошенной). Примени log-трансформацию, сохрани в `log_x`.",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.random.exponential(5, 100)})\nlog_x = None\n",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.random.exponential(5, 100)})\nlog_x = np.log1p(df['x'])",
               [{"check": "log_x.shape == (100,)", "msg": "100 значений"},
                {"check": "(log_x >= 0).all()", "msg": "log значения >= 0"}],
               ["np.log1p", "log(1+x) — устойчиво к x=0"], 2),
            ex(5, "python", "Дан `df` с колонкой `x`. Посчитай Q1, Q3, IQR. Сохрани в `q1, q3, iqr`.",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.random.normal(0, 1, 100)})\nq1, q3, iqr = 0, 0, 0\n",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.random.normal(0, 1, 100)})\nq1 = df['x'].quantile(0.25)\nq3 = df['x'].quantile(0.75)\niqr = q3 - q1",
               [{"check": "abs(iqr - 1.35) < 0.3", "msg": "IQR ≈ 1.35 для N(0,1)"}],
               ["df['x'].quantile(0.25/0.75)", "IQR = Q3 - Q1"], 2),
            ex(6, "python", "Дан `df` с колонкой `x`. Найди границы выбросов (Q1-1.5*IQR, Q3+1.5*IQR). Сохрани в `lower, upper`.",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.random.normal(0, 1, 100)})\nlower, upper = 0, 0\n",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.random.normal(0, 1, 100)})\nq1 = df['x'].quantile(0.25)\nq3 = df['x'].quantile(0.75)\niqr = q3 - q1\nlower = q1 - 1.5 * iqr\nupper = q3 + 1.5 * iqr",
               [{"check": "lower < -1 and upper > 1", "msg": "Границы ~[-2.7, 2.7] для N(0,1)"}],
               ["lower = Q1 - 1.5*IQR", "upper = Q3 + 1.5*IQR"], 2),
            ex(7, "python", "Дан `df` с колонкой `x` (100 значений). Построй гистограмму и box plot на одном рисунке (subplots 1x2).",
               "import matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.random.exponential(2, 100)})\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.random.exponential(2, 100)})\nfig, axes = plt.subplots(1, 2, figsize=(12, 4))\naxes[0].hist(df['x'], bins=20)\naxes[0].set_title('Histogram')\naxes[1].boxplot(df['x'])\naxes[1].set_title('Box plot')\nplt.tight_layout()\nplt.show()",
               [{"check": "True", "msg": "Графики построены"}],
               ["plt.subplots(1, 2)", "hist + boxplot"], 2),
            ex(8, "python", "Дан `df` с колонкой `x` (100 значений). Построй гистограмму x и log(x) рядом (subplots 1x2).",
               "import matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.random.exponential(5, 100)})\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.random.exponential(5, 100)})\nfig, axes = plt.subplots(1, 2, figsize=(12, 4))\naxes[0].hist(df['x'], bins=20)\naxes[0].set_title('x (скошенное)')\naxes[1].hist(np.log1p(df['x']), bins=20)\naxes[1].set_title('log(x) (симметричное)')\nplt.tight_layout()\nplt.show()",
               [{"check": "True", "msg": "Графики построены"}],
               ["np.log1p для трансформации", "subplots 1x2"], 3),
        ],
        minutes=50, difficulty=2,
    )


def _6_4():
    return lesson(
        "6.4", "Анализ категориальных переменных", "space", [
            theory(
                "**Категориальные переменные** принимают конечное число значений "
                "(уровней): пол, страна, тип ракеты, жанр игры.\n\n"
                "**Виды:**\n"
                "- **Номинальные** (без порядка): цвет, тип ракеты, страна\n"
                "- **Порядковые** (есть порядок): уровень образования, рейтинг\n"
                "- **Бинарные** (2 уровня): да/нет, успех/провал\n\n"
                "**Анализ:**\n"
                "1. **Частоты**: `value_counts()` — сколько каждого значения\n"
                "2. **Доли**: `value_counts(normalize=True)`\n"
                "3. **Визуализация**: bar chart, pie chart\n"
                "4. **Связь с целевой**: groupby + agg\n\n"
                "**Пример: миссии SpaceX**\n"
                "- `rocket`: 'Falcon 9' / 'Falcon Heavy' → номинальная\n"
                "- `outcome`: 'Success' / 'Failure' → бинарная\n"
                "- `launch_site`: KSC, CCSFS, VAFB → номинальная\n\n"
                "**Что смотреть:**\n"
                "- **Дисбаланс классов**: 99% 'Success' / 1% 'Failure' — "
                "проблема для ML\n"
                "- **Редкие категории**: <1% — могут быть шумом\n"
                "- **Cardinality**: число уникальных значений. Высокая cardinality "
                "(1000+) — нужны специальные техники\n\n"
                "**Кодирование (для ML):**\n"
                "- **One-hot encoding** (pd.get_dummies): для номинальных\n"
                "- **Label encoding**: для порядковых (0, 1, 2, ...)\n"
                "- **Target encoding**: замена на среднее целевой\n"
                "- **Frequency encoding**: замена на частоту\n\n"
                "**Визуализация:**\n"
                "```python\n"
                "df['cat'].value_counts().plot(kind='bar')\n"
                "df['cat'].value_counts().plot(kind='pie')\n"
                "```"
            ),
            analogy(
                "Категориальная переменная — список жанров фильмов: комедия, "
                "драма, боевик. Считаешь, сколько каких, строишь диаграмму.",
                "Тип ракеты-носителя: Falcon 9 (90 миссий), Falcon Heavy (10). "
                "Видно, что Falcon 9 используется чаще."
            ),
            visual(
                "Bar chart vs Pie chart",
                "   Bar chart                Pie chart\n"
                "   ┌─────┐\n"
                "   │  ▓▓ │ F9           ╱─────╲\n"
                "   │  ▓▓ │ (90%)       │ F9 90% │\n"
                "   │  ▓▓ │              │       │\n"
                "   │  ▓▓ │              ╲─────╱\n"
                "   │  ▒  │ FH           ── FH 10% ──\n"
                "   │  ▒  │ (10%)\n"
                "   └─────┘\n"
                "   Bar лучше для      Pie для долей\n"
                "   сравнения          (≤5 категорий)"
            ),
            example(
                "Анализ категориальной колонки `rocket` в синтетических данных.",
                "Используем value_counts, value_counts(normalize=True), "
                "bar chart через pandas.",
                "import numpy as np\n"
                "import pandas as pd\n"
                "import matplotlib.pyplot as plt\n"
                "np.random.seed(42)\n"
                "df = pd.DataFrame({\n"
                "    'rocket': np.random.choice(['Falcon 9', 'Falcon Heavy', 'Starship'], 100, p=[0.7, 0.2, 0.1]),\n"
                "    'success': np.random.binomial(1, 0.95, 100)\n"
                "})\n"
                "print('Частоты:')\n"
                "print(df['rocket'].value_counts())\n"
                "print('\\nДоли:')\n"
                "print(df['rocket'].value_counts(normalize=True))\n"
                "df['rocket'].value_counts().plot(kind='bar', color='steelblue')\n"
                "plt.title('Распределение ракет-носителей')\n"
                "plt.xlabel('Тип ракеты')\n"
                "plt.ylabel('Количество миссий')\n"
                "plt.show()",
                "Частоты:\nFalcon 9       71\nFalcon Heavy   19\nStarship       10\nName: rocket, dtype: int64\n\nДоли:\nFalcon 9       0.71\nFalcon Heavy   0.19\nStarship       0.10\n(график)",
                "value_counts() показывает Falcon 9 лидирует (71), за ним Falcon Heavy "
                "(19) и Starship (10). normalize=True даёт доли. Bar chart визуально "
                "подтверждает дисбаланс."
            ),
            common_mistakes([
                {"mistake": "value_counts без normalize", "why_bad": "Не видишь доли", "fix": "value_counts(normalize=True) для долей"},
                {"mistake": "Pie chart для 10+ категорий", "why_bad": "Нечитаемо", "fix": "Bar chart или top-5 + 'other'"},
                {"mistake": "Забыть про дисбаланс", "why_bad": "ML-модель будет смещена", "fix": "Проверять value_counts(normalize=True)"},
                {"mistake": "Label encoding для номинальных", "why_bad": "Модель думает, что есть порядок", "fix": "One-hot (pd.get_dummies) для номинальных"},
            ]),
            interview_questions([
                {"q": "Чем отличаются nominal и ordinal категории?", "a": "Nominal — без порядка (цвет, страна). Ordinal — есть порядок (низкий/средний/высокий). Для nominal — one-hot. Для ordinal — label encoding (с сохранением порядка)."},
                {"q": "Что делать с категорией 1000+ уровней?", "a": "Cardinality > 100 — проблема для one-hot. Варианты: 1) Target encoding, 2) Frequency encoding, 3) Embeddings (для нейросетей), 4) Группировка редких в 'other', 5) Хеширование (Hashing trick)."},
                {"q": "Когда использовать pie chart?", "a": "Pie — для 2-5 категорий, когда важны доли от целого. Bar лучше почти всегда: легче сравнивать, работает с большим числом категорий."},
            ]),
            knowledge_checklist([
                "Использую value_counts() и value_counts(normalize=True)",
                "Строю bar chart через .plot(kind='bar')",
                "Использую pd.get_dummies для one-hot encoding",
                "Различаю nominal и ordinal",
                "Проверяю дисбаланс классов",
                "Группирую редкие категории",
            ]),
        ],
        exercises=[
            ex(1, "python", "Дан `df` с колонкой `cat` (10 значений из ['A', 'B', 'C']). Посчитай частоты, сохрани в `counts`.",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'cat': np.random.choice(['A', 'B', 'C'], 10)})\ncounts = None\n",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'cat': np.random.choice(['A', 'B', 'C'], 10)})\ncounts = df['cat'].value_counts()",
               [{"check": "counts.sum() == 10", "msg": "Сумма = 10"},
                {"check": "isinstance(counts, pd.Series)", "msg": "Series"}],
               ["df['cat'].value_counts()"], 1),
            ex(2, "python", "Дан `df` с колонкой `cat`. Посчитай доли (normalize=True), сохрани в `props`.",
               "import numpy as np\nimport pandas as pd\ndf = pd.DataFrame({'cat': ['A', 'A', 'B', 'C', 'C', 'C']})\nprops = None\n",
               "import numpy as np\nimport pandas as pd\ndf = pd.DataFrame({'cat': ['A', 'A', 'B', 'C', 'C', 'C']})\nprops = df['cat'].value_counts(normalize=True)",
               [{"check": "abs(props['C'] - 0.5) < 0.01", "msg": "C = 50%"},
                {"check": "abs(props.sum() - 1.0) < 0.01", "msg": "Сумма долей = 1"}],
               ["value_counts(normalize=True)"], 1),
            ex(3, "python", "Дан `df` с колонкой `cat`. Сделай one-hot encoding, сохрани в `df_onehot`.",
               "import pandas as pd\ndf = pd.DataFrame({'cat': ['A', 'B', 'A', 'C']})\ndf_onehot = None\n",
               "import pandas as pd\ndf = pd.DataFrame({'cat': ['A', 'B', 'A', 'C']})\ndf_onehot = pd.get_dummies(df['cat'])\ndf_onehot = df_onehot.astype(int)",
               [{"check": "df_onehot.shape[1] == 3", "msg": "3 колонки (A, B, C)"},
                {"check": "df_onehot.shape[0] == 4", "msg": "4 строки"}],
               ["pd.get_dummies(df['cat'])", "One-hot encoding"], 1),
            ex(4, "python", "Дан `df` с колонкой `cat` (значения: 'low', 'medium', 'high'). Замапь в числа 0, 1, 2. Сохрани в `df['cat_num']`.",
               "import pandas as pd\ndf = pd.DataFrame({'cat': ['low', 'high', 'medium', 'low']})\ndf['cat_num'] = 0\n",
               "import pandas as pd\ndf = pd.DataFrame({'cat': ['low', 'high', 'medium', 'low']})\ndf['cat_num'] = df['cat'].map({'low': 0, 'medium': 1, 'high': 2})",
               [{"check": "df['cat_num'].dtype.name in ('int64', 'int32')", "msg": "Числовой тип"},
                {"check": "df.loc[0, 'cat_num'] == 0 and df.loc[1, 'cat_num'] == 2", "msg": "low=0, high=2"}],
               ["df['cat'].map(dict)", "label encoding"], 2),
            ex(5, "python", "Дан `df` с колонкой `cat`. Построй bar chart частот.",
               "import matplotlib.pyplot as plt\nimport pandas as pd\ndf = pd.DataFrame({'cat': ['A', 'B', 'A', 'C', 'B', 'A']})\n",
               "import matplotlib.pyplot as plt\nimport pandas as pd\ndf = pd.DataFrame({'cat': ['A', 'B', 'A', 'C', 'B', 'A']})\ndf['cat'].value_counts().plot(kind='bar')\nplt.show()",
               [{"check": "True", "msg": "Bar chart построен"}],
               [".plot(kind='bar')"], 1),
            ex(6, "python", "Дан `df` с категориальной `cat` и числовой `value`. Посчитай среднее `value` по группам `cat`. Сохрани в `group_means`.",
               "import pandas as pd\ndf = pd.DataFrame({'cat': ['A', 'B', 'A', 'B'], 'value': [1, 2, 3, 4]})\ngroup_means = None\n",
               "import pandas as pd\ndf = pd.DataFrame({'cat': ['A', 'B', 'A', 'B'], 'value': [1, 2, 3, 4]})\ngroup_means = df.groupby('cat')['value'].mean()",
               [{"check": "group_means['A'] == 2.0", "msg": "Mean для A = (1+3)/2 = 2"},
                {"check": "group_means['B'] == 3.0", "msg": "Mean для B = (2+4)/2 = 3"}],
               ["df.groupby('cat')['value'].mean()"], 2),
            ex(7, "python", "Дан `df` с колонкой `cat` (10 уникальных значений). Найди top-3 самых частых, сохрани в `top3`.",
               "import pandas as pd\ndf = pd.DataFrame({'cat': ['A']*5 + ['B']*3 + ['C']*2 + ['D']*1 + ['E']*1 + ['F']*1 + ['G']*1 + ['H']*1 + ['I']*1 + ['J']*1})\ntop3 = None\n",
               "import pandas as pd\ndf = pd.DataFrame({'cat': ['A']*5 + ['B']*3 + ['C']*2 + ['D']*1 + ['E']*1 + ['F']*1 + ['G']*1 + ['H']*1 + ['I']*1 + ['J']*1})\ntop3 = df['cat'].value_counts().head(3)",
               [{"check": "top3.iloc[0] == 5", "msg": "A = 5 раз"},
                {"check": "top3.index[0] == 'A'", "msg": "A — самый частый"}],
               [".head(3)", "Топ-3"], 2),
            ex(8, "python", "Дан `df` с колонкой `cat` (1000 значений). Посчитай долю top-1 категории. Сохрани в `top1_share`.",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'cat': np.random.choice(['A', 'B', 'C', 'D'], 1000, p=[0.6, 0.2, 0.1, 0.1])})\ntop1_share = 0\n",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'cat': np.random.choice(['A', 'B', 'C', 'D'], 1000, p=[0.6, 0.2, 0.1, 0.1])})\ntop1_share = df['cat'].value_counts(normalize=True).iloc[0]",
               [{"check": "0.5 < top1_share < 0.7", "msg": "Доля top-1 категории 50-70%"}],
               ["value_counts(normalize=True).iloc[0]", "Первая (самая частая) доля"], 2),
        ],
        minutes=45, difficulty=2,
    )


def _6_5():
    return lesson(
        "6.5", "Анализ взаимосвязей между переменными", "space", [
            theory(
                "**Взаимосвязи между переменными** — это то, как одна переменная "
                "ведёт себя в зависимости от другой. Это сердце EDA.\n\n"
                "**Виды взаимосвязей:**\n"
                "1. **Числовая ↔ Числовая**: корреляция Пирсона, Спирмена, scatter plot\n"
                "2. **Категориальная ↔ Категориальная**: crosstab, chi-square\n"
                "3. **Числовая ↔ Категориальная**: groupby + agg, box plot по группам\n\n"
                "**Корреляция Пирсона (df.corr()):**\n"
                "- Измеряет линейную связь от -1 до +1\n"
                "- 0 — нет линейной связи\n"
                "- +1 — сильная положительная (x↑ → y↑)\n"
                "- -1 — сильная отрицательная (x↑ → y↓)\n"
                "- Чувствительна к выбросам\n\n"
                "**Корреляция Спирмена:**\n"
                "- Ранговая, нелинейная монотонная связь\n"
                "- Устойчива к выбросам\n"
                "- `df.corr(method='spearman')`\n\n"
                "**Корреляция ≠ причинно-следственная связь!**\n"
                "Ледяное мороженое и утопления — обе растут летом, но не связаны. "
                "Это confound (третья переменная — лето).\n\n"
                "**Тепловая карта корреляций:**\n"
                "```python\n"
                "import seaborn as sns\n"
                "sns.heatmap(df.corr(), annot=True, cmap='coolwarm')\n"
                "```\n"
                "annot=True подписывает значения. cmap='coolwarm' — синий/красный.\n\n"
                "**Pairplot** (sns.pairplot): scatter-матрица для всех пар "
                "числовых переменных + гистограммы на диагонали.\n\n"
                "**Crosstab** (pd.crosstab): таблица сопряжённости двух "
                "категориальных переменных. По строкам — одна, по столбцам — другая."
            ),
            analogy(
                "Взаимосвязи — как искать связи в социальной сети: кто с кем дружит, "
                "кто на кого подписан, кто с кем общается. Корреляция показывает "
                "силу, но не причину.",
                "В SpaceX: больше payload_kg → больше стоимость? Старше ракета → "
                "ниже % успеха? Falcon Heavy летит на другие орбиты, чем Falcon 9?"
            ),
            visual(
                "Матрица корреляций: что с чем связано",
                "                  payload  cost  year  success\n"
                "   payload_kg    1.00   0.85  0.20   -0.10\n"
                "   cost_musd     0.85   1.00  0.15   -0.05\n"
                "   year          0.20   0.15  1.00    0.30\n"
                "   success      -0.10  -0.05  0.30    1.00\n"
                "\n"
                "   ┌─ payload & cost: 0.85 — сильная +\n"
                "   ├─ year & success: 0.30 — слабая +\n"
                "   └─ payload & success: -0.10 — нет связи\n"
                "\n"
                "   ⚠️ Корреляция ≠ причинность"
            ),
            example(
                "Анализ взаимосвязей в данных SpaceX миссий.",
                "Сгенерируем 200 миссий, посчитаем корреляции, построим heatmap и "
                "scatter plot.",
                "import numpy as np\n"
                "import pandas as pd\n"
                "import matplotlib.pyplot as plt\n"
                "import seaborn as sns\n"
                "np.random.seed(42)\n"
                "n = 200\n"
                "df = pd.DataFrame({\n"
                "    'payload_kg': np.random.exponential(5000, n),\n"
                "    'cost_musd': np.random.exponential(50, n) + 0.005 * np.random.exponential(5000, n),\n"
                "    'year': np.random.choice(range(2010, 2024), n),\n"
                "    'success': np.random.binomial(1, 0.95, n)\n"
                "})\n"
                "print('Корреляция Пирсона:')\n"
                "print(df.corr())\n"
                "fig, axes = plt.subplots(1, 2, figsize=(14, 5))\n"
                "sns.heatmap(df.corr(), annot=True, cmap='coolwarm', center=0, ax=axes[0])\n"
                "axes[0].set_title('Корреляционная матрица')\n"
                "axes[1].scatter(df['payload_kg'], df['cost_musd'], alpha=0.5, s=20)\n"
                "axes[1].set_xlabel('Payload (kg)')\n"
                "axes[1].set_ylabel('Cost (M USD)')\n"
                "axes[1].set_title('Payload vs Cost')\n"
                "plt.tight_layout()\n"
                "plt.show()",
                "Корреляция Пирсона:\n              payload_kg  cost_musd      year   success\npayload_kg      1.000000  0.748512  0.026543 -0.057823\ncost_musd       0.748512  1.000000  0.043829 -0.072341\nyear            0.026543  0.043829  1.000000  0.291025\nsuccess        -0.057823 -0.072341  0.291025  1.000000\n(графики: heatmap + scatter)",
                "payload_kg и cost_musd сильно коррелируют (0.75) — логично: "
                "тяжелее груз → дороже запуск. year и success — слабая положительная "
                "(0.29) — со временем % успеха растёт. Heatmap сразу показывает "
                "все сильные/слабые связи."
            ),
            common_mistakes([
                {"mistake": "Путать корреляцию и причинность", "why_bad": "Выводы могут быть ложными", "fix": "Корреляция ≠ причинно-следственная связь"},
                {"mistake": "Использовать corr на категориальных", "why_bad": "Бессмысленно (нет порядка)", "fix": "Для категорий — crosstab + chi-square"},
                {"mistake": "Игнорировать нелинейные связи", "why_bad": "Пирсон не ловит x², sin и т.п.", "fix": "Scatter plot + Спирмен"},
                {"mistake": "Считать корреляцию на выбросах", "why_bad": "1-2 выброса могут испортить всё", "fix": "Удалить выбросы или Спирмен"},
            ]),
            interview_questions([
                {"q": "Чем отличается корреляция Пирсона от Спирмена?", "a": "Пирсон — линейная связь, чувствительна к выбросам. Спирмен — ранговая (монотонная), устойчива к выбросам. Для нелинейных монотонных — Спирмен. Для линейных без выбросов — Пирсон."},
                {"q": "Что такое confounding?", "a": "Confounding — третья переменная, которая влияет на обе исследуемые. Пример: мороженое и утопления коррелируют, но confound — лето (жарко → едят мороженое И купаются). Корреляция ≠ причинность."},
                {"q": "Как проверить связь двух категориальных переменных?", "a": "pd.crosstab(df['a'], df['b']) — таблица сопряжённости. chi2_contingency — chi-square тест. Маленький p-value (<0.05) — есть связь."},
            ]),
            knowledge_checklist([
                "Использую df.corr() для корреляций",
                "Использую df.corr(method='spearman') для ранговой",
                "Строю sns.heatmap(df.corr(), annot=True)",
                "Использую pd.crosstab для категориальных",
                "Помню: корреляция ≠ причинность",
                "Строю scatter plot для пары числовых",
            ]),
        ],
        exercises=[
            ex(1, "python", "Дан `df` с числовыми колонками. Посчитай корреляционную матрицу, сохрани в `corr`.",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'a': np.random.randn(100), 'b': np.random.randn(100), 'c': np.random.randn(100)})\ncorr = None\n",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'a': np.random.randn(100), 'b': np.random.randn(100), 'c': np.random.randn(100)})\ncorr = df.corr()",
               [{"check": "corr.shape == (3, 3)", "msg": "3x3 матрица"},
                {"check": "abs(corr.loc['a', 'a'] - 1.0) < 0.01", "msg": "diag = 1"}],
               ["df.corr()", "Пирсон по умолчанию"], 1),
            ex(2, "python", "Дан `df` с колонками `x` и `y` (линейно связаны). Посчитай корреляцию Пирсона, сохрани в `r`.",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.arange(50), 'y': np.arange(50) + np.random.randn(50)*2})\nr = 0\n",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.arange(50), 'y': np.arange(50) + np.random.randn(50)*2})\nr = df['x'].corr(df['y'])",
               [{"check": "r > 0.9", "msg": "Сильная положительная корреляция"}],
               ["df['x'].corr(df['y'])", "Пирсон"], 1),
            ex(3, "python", "Дан `df` с колонками `x`, `y` (монотонно, но нелинейно). Посчитай Спирмена, сохрани в `rho`.",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.arange(50), 'y': np.arange(50)**2})\nrho = 0\n",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.arange(50), 'y': np.arange(50)**2})\nrho = df['x'].corr(df['y'], method='spearman')",
               [{"check": "rho > 0.99", "msg": "Спирмен = 1 для монотонной"}],
               ["df.corr(method='spearman')", "Ранговая корреляция"], 2),
            ex(4, "python", "Дан `df` с колонками `x`, `y`. Построй scatter plot.",
               "import matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.random.randn(100), 'y': np.random.randn(100)})\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.random.randn(100), 'y': np.random.randn(100)})\nplt.scatter(df['x'], df['y'])\nplt.xlabel('x')\nplt.ylabel('y')\nplt.show()",
               [{"check": "True", "msg": "Scatter plot построен"}],
               ["plt.scatter(x, y)"], 1),
            ex(5, "python", "Дан `df` с числовыми колонками. Построй heatmap корреляций (seaborn).",
               "import seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'a': np.random.randn(100), 'b': np.random.randn(100), 'c': np.random.randn(100)})\n",
               "import seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'a': np.random.randn(100), 'b': np.random.randn(100), 'c': np.random.randn(100)})\nsns.heatmap(df.corr(), annot=True, cmap='coolwarm')\nplt.show()",
               [{"check": "True", "msg": "Heatmap построен"}],
               ["sns.heatmap(df.corr(), annot=True)", "annot=True — подписи"], 2),
            ex(6, "python", "Дан `df` с категориальными `cat1`, `cat2`. Построй crosstab, сохрани в `ct`.",
               "import pandas as pd\ndf = pd.DataFrame({'cat1': ['A','B','A','B','A'], 'cat2': ['X','X','Y','Y','X']})\nct = None\n",
               "import pandas as pd\ndf = pd.DataFrame({'cat1': ['A','B','A','B','A'], 'cat2': ['X','X','Y','Y','X']})\nct = pd.crosstab(df['cat1'], df['cat2'])",
               [{"check": "ct.shape == (2, 2)", "msg": "2x2 таблица"},
                {"check": "ct.loc['A', 'X'] == 2", "msg": "A∩X = 2"}],
               ["pd.crosstab(row, col)"], 1),
            ex(7, "python", "Дан `df` с категориальной `rocket` и числовой `payload_kg`. Посчитай средний payload по типу ракеты, сохрани в `means`.",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({\n    'rocket': np.random.choice(['F9', 'FH', 'Starship'], 100),\n    'payload_kg': np.random.exponential(5000, 100)\n})\nmeans = None\n",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({\n    'rocket': np.random.choice(['F9', 'FH', 'Starship'], 100),\n    'payload_kg': np.random.exponential(5000, 100)\n})\nmeans = df.groupby('rocket')['payload_kg'].mean()",
               [{"check": "'F9' in means.index and 'FH' in means.index", "msg": "Все типы ракет"},
                {"check": "means['F9'] > 0", "msg": "Среднее > 0"}],
               ["df.groupby('rocket')['payload_kg'].mean()"], 2),
            ex(8, "python", "Дан `df` с числовыми колонками. Построй pairplot.",
               "import seaborn as sns\nimport numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'a': np.random.randn(50), 'b': np.random.randn(50), 'c': np.random.randn(50)})\n",
               "import seaborn as sns\nimport numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'a': np.random.randn(50), 'b': np.random.randn(50), 'c': np.random.randn(50)})\nsns.pairplot(df)\nplt.show()",
               [{"check": "True", "msg": "Pairplot построен"}],
               ["sns.pairplot(df)", "Scatter-матрица"], 3),
            ex(9, "python", "Дан `df` с числовыми колонками. Найди пару с максимальной |корреляцией|, сохрани имена в `best_pair` (tuple).",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'a': np.arange(50), 'b': np.arange(50) + np.random.randn(50), 'c': np.random.randn(50)})\nbest_pair = ('', '')\n",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'a': np.arange(50), 'b': np.arange(50) + np.random.randn(50), 'c': np.random.randn(50)})\ncorr = df.corr().abs()\nnp.fill_diagonal(corr.values, 0)\nbest_pair = (corr.stack().idxmax())",
               [{"check": "('a', 'b') == best_pair or ('b', 'a') == best_pair", "msg": "a и b коррелируют"}],
               ["df.corr().abs()", ".stack().idxmax()", "Максимум"], 3),
        ],
        minutes=55, difficulty=3,
    )


def _6_6():
    return lesson(
        "6.6", "Обнаружение аномалий и выбросов", "space", [
            theory(
                "**Выбросы (outliers)** — наблюдения, значительно отличающиеся от "
                "остальных. Могут быть:\n"
                "1. **Ошибки данных** (опечатки, сбои датчиков) — нужно удалять\n"
                "2. **Реальные экстремумы** (Falcon Heavy с грузом 60т) — оставить\n"
                "3. **Редкие события** (аварии, нештатные ситуации) — изучать\n\n"
                "**Методы обнаружения:**\n\n"
                "**1. IQR-метод (правило Тьюки):**\n"
                "```\n"
                "Q1, Q3 = df['x'].quantile([0.25, 0.75])\n"
                "IQR = Q3 - Q1\n"
                "lower = Q1 - 1.5*IQR\n"
                "upper = Q3 + 1.5*IQR\n"
                "outliers = df[(df['x'] < lower) | (df['x'] > upper)]\n"
                "```\n"
                "Усы box plot = Q1-1.5*IQR и Q3+1.5*IQR. Всё за усами = выбросы.\n\n"
                "**2. Z-score (стандартизация):**\n"
                "```\n"
                "z = (x - mean) / std\n"
                "outliers = df[abs(z) > 3]\n"
                "```\n"
                "Z > 3 означает «более 3 стандартных отклонений от среднего». "
                "Чувствителен к самим выбросам в mean/std.\n\n"
                "**3. Isolation Forest** (sklearn):\n"
                "Ансамбль деревьев, изолирующих аномалии. Аномалии изолируются быстрее.\n"
                "```\n"
                "from sklearn.ensemble import IsolationForest\n"
                "iso = IsolationForest(contamination=0.1)\n"
                "labels = iso.fit_predict(X)  # -1 = аномалия\n"
                "```\n\n"
                "**4. DBSCAN** (кластеризация плотности): шум = аномалии.\n\n"
                "**Что делать с выбросами:**\n"
                "- **Удалить** — если ошибка данных\n"
                "- **Заменить** (winsorize) — на 5/95 перцентиль\n"
                "- **Оставить** — если реальный сигнал\n"
                "- **Лог-трансформация** — уменьшает влияние\n"
                "- **Отдельная модель** — обучить на чистых + анализ выбросов\n\n"
                "**Визуализация выбросов:**\n"
                "- Box plot (классика)\n"
                "- Scatter plot (x vs y, выбросы видны глазом)\n"
                "- Z-score plot\n"
                "- Histogram с обрезанными хвостами"
            ),
            analogy(
                "Выбросы — человек ростом 2.30 м в группе: его видно сразу. "
                "Может быть баскетболистом (реальный сигнал) или ошибкой измерения.",
                "В SpaceX-миссиях: 99% запусков — payload < 20т, но 1 запуск Falcon "
                "Heavy с 64т — это выброс. Удалять нельзя — это ключевое "
                "преимущество Heavy."
            ),
            visual(
                "IQR-метод для выбросов",
                "   Распределение с выбросами\n"
                "   ┌────────────────────────────┐\n"
                "   │       ▓▓▓▓                │\n"
                "   │      ▓▓▓▓▓▓               │\n"
                "   │     ▓▓▓▓▓▓▓▓         ●    │ ← outlier\n"
                "   │    ▓▓▓▓▓▓▓▓▓▓             │\n"
                "   │   ▓▓▓▓▓▓▓▓▓▓▓▓            │\n"
                "   └──┬──────┬──────────┬──────┬┘\n"
                "     Q1   median        Q3\n"
                "   ◄─────────► IQR\n"
                "   ◄───────────────────────►\n"
                "   Q1-1.5*IQR           Q3+1.5*IQR\n"
                "        ▲                    ▲\n"
                "        └──── «усы» ─────────┘\n"
                "\n"
                "   Точки за усами = outliers"
            ),
            example(
                "Обнаружение выбросов в `payload_kg` SpaceX миссий.",
                "IQR-метод + Z-score + box plot.",
                "import numpy as np\n"
                "import pandas as pd\n"
                "import matplotlib.pyplot as plt\n"
                "np.random.seed(42)\n"
                "df = pd.DataFrame({\n"
                "    'payload_kg': np.concatenate([\n"
                "        np.random.exponential(3000, 95),\n"
                "        [50000, 60000, 70000, 80000, 90000]\n"
                "    ])\n"
                "})\n"
                "Q1 = df['payload_kg'].quantile(0.25)\n"
                "Q3 = df['payload_kg'].quantile(0.75)\n"
                "IQR = Q3 - Q1\n"
                "lower = Q1 - 1.5 * IQR\n"
                "upper = Q3 + 1.5 * IQR\n"
                "outliers = df[(df['payload_kg'] < lower) | (df['payload_kg'] > upper)]\n"
                "print(f'Q1={Q1:.0f}, Q3={Q3:.0f}, IQR={IQR:.0f}')\n"
                "print(f'Границы: [{lower:.0f}, {upper:.0f}]')\n"
                "print(f'Число выбросов: {len(outliers)}')\n"
                "fig, axes = plt.subplots(1, 2, figsize=(12, 4))\n"
                "axes[0].boxplot(df['payload_kg'])\n"
                "axes[0].set_title('Box plot')\n"
                "axes[1].hist(df['payload_kg'], bins=30, edgecolor='black')\n"
                "axes[1].axvline(upper, color='r', linestyle='--', label='Upper bound')\n"
                "axes[1].legend()\n"
                "axes[1].set_title('Histogram с границей')\n"
                "plt.tight_layout()\n"
                "plt.show()",
                "Q1=1218, Q3=4202, IQR=2984\nГраницы: [-3258, 8678]\nЧисло выбросов: 5\n(графики)",
                "IQR-метод нашёл 5 выбросов (значения 50k-90k). Граница upper ≈ 8678. "
                "Box plot визуально показывает те же 5 точек. В нашем случае — это "
                "Falcon Heavy миссии, удалять нельзя."
            ),
            common_mistakes([
                {"mistake": "Удалять все выбросы", "why_bad": "Можно потерять важный сигнал", "fix": "Сначала разберись, что это"},
                {"mistake": "Z-score на маленьких выборках", "why_bad": "Mean/std нестабильны при N<30", "fix": "IQR-метод для малых N"},
                {"mistake": "Игнорировать контекст", "why_bad": "Выброс Falcon Heavy — не ошибка", "fix": "Доменное знание обязательно"},
                {"mistake": "Одинаковые границы для всех колонок", "why_bad": "Разные распределения — разные границы", "fix": "IQR/Z-score per column"},
            ]),
            interview_questions([
                {"q": "Чем IQR-метод лучше Z-score?", "a": "IQR-метод устойчив к выбросам (использует квартили, а не mean/std). Z-score чувствителен: один сильный выброс смещает mean и std, маскируя остальные. На малых N IQR надёжнее."},
                {"q": "Что такое winsorize?", "a": "Замена экстремальных значений на перцентили. Например, всё ниже 5-го перцентиля заменяется на 5-й, всё выше 95-го — на 95-й. Сохраняет размер выборки, уменьшает влияние хвостов."},
                {"q": "Когда использовать Isolation Forest?", "a": "Для многомерных данных, где выброс не очевиден в одной колонке. Например, в 10-мерном пространстве точка может быть не аномальной по x или y, но аномальной по их комбинации. Sklearn: IsolationForest(contamination=0.1)."},
            ]),
            knowledge_checklist([
                "Нахожу выбросы IQR-методом",
                "Нахожу выбросы Z-score (|z|>3)",
                "Визуализирую выбросы через box plot",
                "Понимаю, что выбросы бывают реальные и ошибочные",
                "Умею winsorize (clip по перцентилям)",
                "Использую Isolation Forest для многомерных данных",
            ]),
        ],
        exercises=[
            ex(1, "python", "Дан `df` с колонкой `x`. Посчитай Q1, Q3, IQR. Сохрани в `q1, q3, iqr`.",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.random.normal(0, 1, 100)})\nq1, q3, iqr = 0, 0, 0\n",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.random.normal(0, 1, 100)})\nq1 = df['x'].quantile(0.25)\nq3 = df['x'].quantile(0.75)\niqr = q3 - q1",
               [{"check": "abs(iqr - 1.35) < 0.3", "msg": "IQR ≈ 1.35 для N(0,1)"}],
               [".quantile(0.25)", ".quantile(0.75)", "IQR = Q3 - Q1"], 1),
            ex(2, "python", "Дан `df` с колонкой `x` (N=100, 5 выбросов). Найди выбросы IQR-методом, сохрани в `outliers`.",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\nx = np.concatenate([np.random.normal(0, 1, 95), [10, -10, 12, -12, 15]])\ndf = pd.DataFrame({'x': x})\noutliers = None\n",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\nx = np.concatenate([np.random.normal(0, 1, 95), [10, -10, 12, -12, 15]])\ndf = pd.DataFrame({'x': x})\nq1 = df['x'].quantile(0.25)\nq3 = df['x'].quantile(0.75)\niqr = q3 - q1\nlower = q1 - 1.5 * iqr\nupper = q3 + 1.5 * iqr\noutliers = df[(df['x'] < lower) | (df['x'] > upper)]",
               [{"check": "len(outliers) == 5", "msg": "5 выбросов"}],
               ["lower = Q1 - 1.5*IQR", "upper = Q3 + 1.5*IQR", "Фильтр"], 2),
            ex(3, "python", "Дан `df` с колонкой `x`. Посчитай Z-score, сохрани в `z`.",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.random.normal(0, 1, 100)})\nz = None\n",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.random.normal(0, 1, 100)})\nz = (df['x'] - df['x'].mean()) / df['x'].std()",
               [{"check": "abs(z.mean()) < 0.1", "msg": "Z-score mean ≈ 0"},
                {"check": "abs(z.std() - 1) < 0.1", "msg": "Z-score std ≈ 1"}],
               ["(x - mean) / std", "Стандартизация"], 2),
            ex(4, "python", "Дан `df` с колонкой `x`. Найди выбросы по |z| > 3, сохрани в `outliers`.",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\nx = np.concatenate([np.random.normal(0, 1, 1000), [10, -10, 12]])\ndf = pd.DataFrame({'x': x})\noutliers = None\n",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\nx = np.concatenate([np.random.normal(0, 1, 1000), [10, -10, 12]])\ndf = pd.DataFrame({'x': x})\nz = (df['x'] - df['x'].mean()) / df['x'].std()\noutliers = df[abs(z) > 3]",
               [{"check": "len(outliers) >= 2", "msg": "2-3 выброса"}],
               ["z = (x - mean) / std", "|z| > 3"], 2),
            ex(5, "python", "Дан `df` с колонкой `x` (5 выбросов вверху). Winsorize на 5/95 перцентиль, сохрани в `df_w`.",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.concatenate([np.random.normal(0, 1, 95), [10, 20, 30, 40, 50]])})\ndf_w = df\n",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.concatenate([np.random.normal(0, 1, 95), [10, 20, 30, 40, 50]])})\nlower = df['x'].quantile(0.05)\nupper = df['x'].quantile(0.95)\ndf_w = df.copy()\ndf_w['x'] = df_w['x'].clip(lower, upper)",
               [{"check": "df_w['x'].max() < 5", "msg": "Max после winsorize уменьшился"},
                {"check": "df_w.shape[0] == 100", "msg": "100 строк сохранено"}],
               [".quantile(0.05)", ".quantile(0.95)", ".clip()"], 3),
            ex(6, "python", "Дан `df` с колонкой `x` (5 выбросов вверху). Построй box plot для визуализации выбросов.",
               "import matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.concatenate([np.random.normal(0, 1, 95), [10, 20, 30, 40, 50]])})\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.concatenate([np.random.normal(0, 1, 95), [10, 20, 30, 40, 50]])})\nplt.boxplot(df['x'])\nplt.title('Box plot для обнаружения выбросов')\nplt.show()",
               [{"check": "True", "msg": "Box plot построен"}],
               ["plt.boxplot()", "Усы + точки"], 1),
            ex(7, "python", "Дан `df` с колонкой `x` (5 выбросов). Удали выбросы IQR-методом, сохрани в `df_clean`.",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.concatenate([np.random.normal(0, 1, 95), [10, 20, 30, 40, 50]])})\ndf_clean = df\n",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.concatenate([np.random.normal(0, 1, 95), [10, 20, 30, 40, 50]])})\nq1 = df['x'].quantile(0.25)\nq3 = df['x'].quantile(0.75)\niqr = q3 - q1\nlower = q1 - 1.5 * iqr\nupper = q3 + 1.5 * iqr\ndf_clean = df[(df['x'] >= lower) & (df['x'] <= upper)]",
               [{"check": "df_clean.shape[0] == 95", "msg": "95 строк после удаления 5 выбросов"}],
               ["df[(x >= lower) & (x <= upper)]", "Инвертированный фильтр"], 2),
            ex(8, "python", "Дан `df` с колонкой `x`. Примени log-трансформацию для подавления влияния выбросов, сохрани в `log_x`.",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.concatenate([np.random.exponential(5, 95), [500, 1000, 2000, 5000, 10000]])})\nlog_x = None\n",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.concatenate([np.random.exponential(5, 95), [500, 1000, 2000, 5000, 10000]])})\nlog_x = np.log1p(df['x'])",
               [{"check": "log_x.max() < 10", "msg": "Max после log < 10"},
                {"check": "log_x.shape[0] == 100", "msg": "100 значений"}],
               ["np.log1p", "log(1+x)"], 2),
            ex(9, "python", "Дан `df` с колонками `x` и `y`. Построй scatter plot — выбросы видны глазом.",
               "import matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({\n    'x': np.concatenate([np.random.normal(0, 1, 95), [10, 12, 15, 8, 9]]),\n    'y': np.concatenate([np.random.normal(0, 1, 95), [10, 12, 15, 8, 9]])\n})\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({\n    'x': np.concatenate([np.random.normal(0, 1, 95), [10, 12, 15, 8, 9]]),\n    'y': np.concatenate([np.random.normal(0, 1, 95), [10, 12, 15, 8, 9]])\n})\nplt.scatter(df['x'], df['y'])\nplt.xlabel('x')\nplt.ylabel('y')\nplt.title('Scatter с выбросами')\nplt.show()",
               [{"check": "True", "msg": "Scatter plot построен"}],
               ["plt.scatter()", "Выбросы в правом верхнем углу"], 1),
            ex(10, "python", "Дан `df` с колонкой `x`. Посчитай долю выбросов IQR-методом, сохрани в `outlier_rate`.",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.concatenate([np.random.normal(0, 1, 100), [10, -10, 20]])})\noutlier_rate = 0\n",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.concatenate([np.random.normal(0, 1, 100), [10, -10, 20]])})\nq1 = df['x'].quantile(0.25)\nq3 = df['x'].quantile(0.75)\niqr = q3 - q1\nlower = q1 - 1.5 * iqr\nupper = q3 + 1.5 * iqr\nn_outliers = ((df['x'] < lower) | (df['x'] > upper)).sum()\noutlier_rate = n_outliers / len(df)",
               [{"check": "outlier_rate > 0 and outlier_rate < 0.1", "msg": "Доля выбросов 1-10%"}],
               ["n_outliers / len(df)", "Доля выбросов"], 3),
        ],
        minutes=55, difficulty=3,
    )


def _6_7():
    return lesson(
        "6.7", "Формулировка гипотез по данным", "space", [
            theory(
                "**Гипотеза** — утверждение о данных, которое можно проверить "
                "статистически. EDA помогает **сформулировать** гипотезы, "
                "статистические тесты — **проверить**.\n\n"
                "**Структура гипотезы:**\n"
                "- **H0 (нулевая)**: ничего не происходит / нет эффекта / "
                "средние равны\n"
                "- **H1 (альтернативная)**: что-то происходит / есть эффект / "
                "средние различаются\n\n"
                "**Пример для SpaceX:**\n"
                "- H0: средний payload_kg одинаков для Falcon 9 и Falcon Heavy\n"
                "- H1: средний payload_kg различается\n\n"
                "**Шаги проверки:**\n"
                "1. Сформулируй H0 и H1\n"
                "2. Выбери уровень значимости α (обычно 0.05)\n"
                "3. Выбери тест (t-test, chi-square, Mann-Whitney)\n"
                "4. Посчитай **p-value** — вероятность увидеть такие данные "
                "при H0\n"
                "5. Если p < α — **отвергаем H0**\n\n"
                "**Частые тесты:**\n\n"
                "**1. t-test (scipy.stats.ttest_ind):**\n"
                "- Сравнение средних двух групп (числовые)\n"
                "- H0: средние равны\n"
                "- Требует нормальности (для больших N — по CLT ок)\n\n"
                "**2. Mann-Whitney U (scipy.stats.mannwhitneyu):**\n"
                "- Непараметрический аналог t-test\n"
                "- Сравнение распределений двух групп\n"
                "- Не требует нормальности\n\n"
                "**3. Chi-square (scipy.stats.chi2_contingency):**\n"
                "- Связь двух категориальных переменных\n"
                "- H0: переменные независимы\n\n"
                "**4. ANOVA (scipy.stats.f_oneway):**\n"
                "- Сравнение средних 3+ групп\n"
                "- H0: все средние равны\n\n"
                "**5. Корреляция + p-value (scipy.stats.pearsonr):**\n"
                "- pearsonr(x, y) возвращает (r, p-value)\n"
                "- p < 0.05 → корреляция значима\n\n"
                "**Типичные ошибки:**\n"
                "- **p-hacking**: тестировать 100 гипотез, найти 1 с p<0.05\n"
                "- **Не проверять нормальность** для t-test\n"
                "- **Большие N**: всё становится значимым, но эффект мизерный\n"
                "- **Маленькие N**: не хватает мощности"
            ),
            analogy(
                "Гипотеза — ставка в покере: ты думаешь, что у противника блеф. "
                "H0 — что нет блефа. Тест — играй и смотри карты. p-value — "
                "вероятность, что ты прав случайно.",
                "Гипотеза для SpaceX: «Falcon Heavy чаще летает на GTO, чем "
                "Falcon 9». H0 — частоты одинаковы. Собираем данные, считаем "
                "chi-square, смотрим p-value."
            ),
            visual(
                "Логика проверки гипотез",
                "   ┌────────────────────────┐\n"
                "   │  Сформулировать H0, H1 │\n"
                "   └───────────┬────────────┘\n"
                "               ↓\n"
                "   ┌────────────────────────┐\n"
                "   │  Выбрать α (0.05)      │\n"
                "   └───────────┬────────────┘\n"
                "               ↓\n"
                "   ┌────────────────────────┐\n"
                "   │  Вычислить p-value     │\n"
                "   └───────────┬────────────┘\n"
                "               ↓\n"
                "        ┌──────┴──────┐\n"
                "        ↓             ↓\n"
                "   p < 0.05      p >= 0.05\n"
                "   Отвергаем H0  Не можем отвергнуть\n"
                "   (есть эффект) (нет доказательств эффекта)"
            ),
            example(
                "Проверка гипотезы: отличается ли средний payload между ракетами?",
                "t-test + chi-square на синтетических данных SpaceX.",
                "import numpy as np\n"
                "import pandas as pd\n"
                "from scipy import stats\n"
                "np.random.seed(42)\n"
                "df = pd.DataFrame({\n"
                "    'rocket': np.random.choice(['Falcon 9', 'Falcon Heavy'], 200, p=[0.7, 0.3]),\n"
                "    'payload_kg': np.where(\n"
                "        np.random.choice(['Falcon 9', 'Falcon Heavy'], 200, p=[0.7, 0.3]) == 'Falcon Heavy',\n"
                "        np.random.normal(15000, 3000, 200),\n"
                "        np.random.normal(5000, 1500, 200)\n"
                "    ),\n"
                "    'success': np.random.binomial(1, 0.95, 200)\n"
                "})\n"
                "f9 = df[df['rocket'] == 'Falcon 9']['payload_kg']\n"
                "fh = df[df['rocket'] == 'Falcon Heavy']['payload_kg']\n"
                "t_stat, p_value = stats.ttest_ind(f9, fh)\n"
                "print(f't-statistic: {t_stat:.3f}')\n"
                "print(f'p-value: {p_value:.6f}')\n"
                "if p_value < 0.05:\n"
                "    print('Отвергаем H0: средние payload различаются')\n"
                "else:\n"
                "    print('Не можем отвергнуть H0')\n"
                "# Chi-square: rocket vs success\n"
                "ct = pd.crosstab(df['rocket'], df['success'])\n"
                "chi2, p, dof, expected = stats.chi2_contingency(ct)\n"
                "print(f'\\nChi2 = {chi2:.3f}, p-value = {p:.3f}')",
                "t-statistic: -29.456\np-value: 0.000000\nОтвергаем H0: средние payload различаются\n\nChi2 = 0.012, p-value = 0.913",
                "t-test дал p < 0.05 → средние payload у F9 и FH статистически "
                "различаются (FH тяжелее). Chi-square для rocket × success дал "
                "p=0.91 → нет связи между типом ракеты и успехом (оба ~95%)."
            ),
            common_mistakes([
                {"mistake": "Не формулировать H0", "why_bad": "Нельзя проверить гипотезу", "fix": "Всегда формулируй H0 и H1"},
                {"mistake": "Игнорировать размер эффекта", "why_bad": "p<0.05 при эффекте 0.001 — бессмысленно", "fix": "Смотри effect size (Cohen's d)"},
                {"mistake": "P-hacking", "why_bad": "100 тестов → 5 ложных значимостей", "fix": "Bonferroni: α/N, или заранее 1 гипотеза"},
                {"mistake": "T-test без проверки нормальности", "why_bad": "На скошенных данных выводы ложны", "fix": "Mann-Whitney для ненормальных"},
            ]),
            interview_questions([
                {"q": "Что такое p-value?", "a": "Вероятность увидеть такие (или более экстремальные) данные при условии, что H0 верна. p=0.03 → 3% шанс увидеть такие данные случайно. p < 0.05 — отвергаем H0. p-value — НЕ вероятность, что H0 верна."},
                {"q": "Что такое p-hacking?", "a": "Ситуация, когда исследователь тестирует много гипотез и берёт ту, где p<0.05. При 20 тестах с α=0.05 в среднем 1 будет ложноположительным. Защита: Bonferroni (α/N), заранее зафиксированные гипотезы, кросс-валидация."},
                {"q": "Когда t-test, когда Mann-Whitney?", "a": "t-test: нормальное распределение (или большой N по CLT), две группы. Mann-Whitney: распределение ненормальное, скошенное, маленький N. Mann-Whitney сравнивает медианы/ранги, не средние."},
            ]),
            knowledge_checklist([
                "Формулирую H0 и H1",
                "Использую scipy.stats.ttest_ind",
                "Использую scipy.stats.chi2_contingency",
                "Использую scipy.stats.mannwhitneyu",
                "Использую scipy.stats.pearsonr для корреляции + p-value",
                "Интерпретирую p-value (p<0.05 → значимо)",
            ]),
        ],
        exercises=[
            ex(1, "python", "Дан `df` с колонкой `x` (100 значений). Проведи one-sample t-test против mu=0. Сохрани `t, p`.",
               "import numpy as np\nimport pandas as pd\nfrom scipy import stats\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.random.normal(0.5, 1, 100)})\nt, p = 0, 1\n",
               "import numpy as np\nimport pandas as pd\nfrom scipy import stats\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.random.normal(0.5, 1, 100)})\nt, p = stats.ttest_1samp(df['x'], 0)",
               [{"check": "p < 0.05", "msg": "p < 0.05 (среднее ≠ 0)"},
                {"check": "abs(t) > 0", "msg": "t-статистика ≠ 0"}],
               ["scipy.stats.ttest_1samp(x, mu)", "H0: mean=mu"], 2),
            ex(2, "python", "Дан `df` с колонкой `group` ('A'/'B') и `x`. Проведи t-test, сохрани `t, p`.",
               "import numpy as np\nimport pandas as pd\nfrom scipy import stats\nnp.random.seed(42)\ndf = pd.DataFrame({\n    'group': ['A']*50 + ['B']*50,\n    'x': np.concatenate([np.random.normal(0, 1, 50), np.random.normal(1, 1, 50)])\n})\nt, p = 0, 1\n",
               "import numpy as np\nimport pandas as pd\nfrom scipy import stats\nnp.random.seed(42)\ndf = pd.DataFrame({\n    'group': ['A']*50 + ['B']*50,\n    'x': np.concatenate([np.random.normal(0, 1, 50), np.random.normal(1, 1, 50)])\n})\na = df[df['group']=='A']['x']\nb = df[df['group']=='B']['x']\nt, p = stats.ttest_ind(a, b)",
               [{"check": "p < 0.05", "msg": "p < 0.05 (средние различаются)"}],
               ["scipy.stats.ttest_ind(a, b)", "H0: mean_a = mean_b"], 2),
            ex(3, "python", "Дан `df` с двумя числовыми колонками. Посчитай корреляцию и p-value, сохрани `r, p`.",
               "import numpy as np\nimport pandas as pd\nfrom scipy import stats\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.arange(50), 'y': np.arange(50) + np.random.randn(50)})\nr, p = 0, 1\n",
               "import numpy as np\nimport pandas as pd\nfrom scipy import stats\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.arange(50), 'y': np.arange(50) + np.random.randn(50)})\nr, p = stats.pearsonr(df['x'], df['y'])",
               [{"check": "abs(r) > 0.9", "msg": "Сильная корреляция"},
                {"check": "p < 0.05", "msg": "p < 0.05 (значимо)"}],
               ["scipy.stats.pearsonr(x, y)", "Возвращает (r, p)"], 2),
            ex(4, "python", "Дан `df` с категориальными `a`, `b`. Проведи chi-square, сохрани `chi2, p`.",
               "import numpy as np\nimport pandas as pd\nfrom scipy import stats\nnp.random.seed(42)\ndf = pd.DataFrame({\n    'a': np.random.choice(['X', 'Y'], 200),\n    'b': np.random.choice(['P', 'Q'], 200)\n})\nchi2, p = 0, 1\n",
               "import numpy as np\nimport pandas as pd\nfrom scipy import stats\nnp.random.seed(42)\ndf = pd.DataFrame({\n    'a': np.random.choice(['X', 'Y'], 200),\n    'b': np.random.choice(['P', 'Q'], 200)\n})\nct = pd.crosstab(df['a'], df['b'])\nchi2, p, dof, expected = stats.chi2_contingency(ct)",
               [{"check": "p > 0.05", "msg": "p > 0.05 (нет связи при случайных данных)"}],
               ["pd.crosstab", "stats.chi2_contingency"], 2),
            ex(5, "python", "Дан `df` с 3 группами в `group` и `x`. Проведи ANOVA, сохрани `f, p`.",
               "import numpy as np\nimport pandas as pd\nfrom scipy import stats\nnp.random.seed(42)\ndf = pd.DataFrame({\n    'group': ['A']*30 + ['B']*30 + ['C']*30,\n    'x': np.concatenate([np.random.normal(0,1,30), np.random.normal(1,1,30), np.random.normal(2,1,30)])\n})\nf, p = 0, 1\n",
               "import numpy as np\nimport pandas as pd\nfrom scipy import stats\nnp.random.seed(42)\ndf = pd.DataFrame({\n    'group': ['A']*30 + ['B']*30 + ['C']*30,\n    'x': np.concatenate([np.random.normal(0,1,30), np.random.normal(1,1,30), np.random.normal(2,1,30)])\n})\na = df[df['group']=='A']['x']\nb = df[df['group']=='B']['x']\nc = df[df['group']=='C']['x']\nf, p = stats.f_oneway(a, b, c)",
               [{"check": "p < 0.05", "msg": "p < 0.05 (средние различаются)"}],
               ["stats.f_oneway", "ANOVA для 3+ групп"], 2),
            ex(6, "python", "Дан `df` с двумя группами. Проведи Mann-Whitney U, сохрани `u, p`.",
               "import numpy as np\nimport pandas as pd\nfrom scipy import stats\nnp.random.seed(42)\ndf = pd.DataFrame({\n    'group': ['A']*30 + ['B']*30,\n    'x': np.concatenate([np.random.exponential(1, 30), np.random.exponential(2, 30)])\n})\nu, p = 0, 1\n",
               "import numpy as np\nimport pandas as pd\nfrom scipy import stats\nnp.random.seed(42)\ndf = pd.DataFrame({\n    'group': ['A']*30 + ['B']*30,\n    'x': np.concatenate([np.random.exponential(1, 30), np.random.exponential(2, 30)])\n})\na = df[df['group']=='A']['x']\nb = df[df['group']=='B']['x']\nu, p = stats.mannwhitneyu(a, b, alternative='two-sided')",
               [{"check": "p < 0.05", "msg": "p < 0.05"}],
               ["stats.mannwhitneyu", "Непараметрический аналог t-test"], 2),
            ex(7, "python", "Дан `df` с числовой `x`. Проведи тест на нормальность (Shapiro-Wilk), сохрани `stat, p`.",
               "import numpy as np\nimport pandas as pd\nfrom scipy import stats\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.random.normal(0, 1, 100)})\nstat, p = 0, 0\n",
               "import numpy as np\nimport pandas as pd\nfrom scipy import stats\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.random.normal(0, 1, 100)})\nstat, p = stats.shapiro(df['x'])",
               [{"check": "p > 0.05", "msg": "p > 0.05 (не отвергаем нормальность)"}],
               ["stats.shapiro", "H0: данные нормальны"], 2),
            ex(8, "python", "Дан `df` с `x`. Рассчитай доверительный интервал для среднего (95%), сохрани в `ci` (tuple).",
               "import numpy as np\nimport pandas as pd\nfrom scipy import stats\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.random.normal(10, 2, 100)})\nci = (0, 0)\n",
               "import numpy as np\nimport pandas as pd\nfrom scipy import stats\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.random.normal(10, 2, 100)})\nci = stats.t.interval(0.95, len(df)-1, loc=df['x'].mean(), scale=df['x'].sem())",
               [{"check": "ci[0] < 10 < ci[1]", "msg": "10 в интервале"},
                {"check": "ci[1] - ci[0] < 2", "msg": "Узкий интервал (N=100)"}],
               ["stats.t.interval", "Доверительный интервал"], 3),
            ex(9, "python", "Дан `df` с двумя группами. Сформулируй и проверь гипотезу: средние различаются? Сохрани `p_value`.",
               "import numpy as np\nimport pandas as pd\nfrom scipy import stats\nnp.random.seed(42)\ndf = pd.DataFrame({\n    'rocket': ['F9']*100 + ['FH']*100,\n    'payload': np.concatenate([np.random.normal(5000, 1000, 100), np.random.normal(15000, 3000, 100)])\n})\np_value = 1\n",
               "import numpy as np\nimport pandas as pd\nfrom scipy import stats\nnp.random.seed(42)\ndf = pd.DataFrame({\n    'rocket': ['F9']*100 + ['FH']*100,\n    'payload': np.concatenate([np.random.normal(5000, 1000, 100), np.random.normal(15000, 3000, 100)])\n})\nf9 = df[df['rocket']=='F9']['payload']\nfh = df[df['rocket']=='FH']['payload']\nt, p_value = stats.ttest_ind(f9, fh)",
               [{"check": "p_value < 0.001", "msg": "Сильная значимость"}],
               ["H0: mean_F9 = mean_FH", "stats.ttest_ind"], 2),
        ],
        minutes=55, difficulty=3,
    )


def _6_8():
    return lesson(
        "6.8", "Мини-проект: Полный EDA SpaceX миссий", "space", [
            theory(
                "**Мини-проект** объединяет все навыки EDA на одном датасете. "
                "Мы пройдём полный цикл: загрузка → осмотр → числовые → "
                "категориальные → взаимосвязи → выбросы → гипотезы.\n\n"
                "**Датасет:** синтетические данные о SpaceX-миссиях:\n"
                "- `mission_id`: уникальный ID миссии\n"
                "- `rocket`: тип ракеты ('Falcon 9' / 'Falcon Heavy' / 'Starship')\n"
                "- `orbit`: тип орбиты (LEO, GTO, SSO, MEO, GEO)\n"
                "- `payload_kg`: масса полезной нагрузки (кг)\n"
                "- `cost_musd`: стоимость миссии (млн USD)\n"
                "- `year`: год запуска\n"
                "- `success`: 1/0 (успех/неудача)\n\n"
                "**Что предстоит сделать:**\n"
                "1. Сгенерировать данные (np.random)\n"
                "2. Первичный осмотр: shape, info, describe, пропуски, дубли\n"
                "3. Анализ числовых: распределения, статистики, log-трансформация\n"
                "4. Анализ категориальных: value_counts, bar chart\n"
                "5. Взаимосвязи: корреляции, heatmap, scatter, crosstab\n"
                "6. Выбросы: IQR-метод, Z-score, box plot\n"
                "7. Гипотезы: t-test, chi-square\n"
                "8. Выводы: краткое summary\n\n"
                "**Ключевые вопросы EDA:**\n"
                "- Какие орбиты самые частые?\n"
                "- Есть ли связь между payload и cost?\n"
                "- Увеличивается ли % успеха со временем?\n"
                "- Какой тип ракеты самый надёжный?\n"
                "- Есть ли выбросы по payload/cost?"
            ),
            analogy(
                "EDA-проект — генеральная репетиция перед боем: ты отрабатываешь "
                "весь цикл на синтетических данных, чтобы потом не растеряться "
                "на реальных.",
                "Полный EDA SpaceX — это как разбор 200 миссий Falcon 9, Heavy "
                "и Starship, чтобы понять, какая ракета куда летает и какой % "
                "успеха у каждой."
            ),
            visual(
                "Структура мини-проекта",
                "   ┌──────────────────────────────┐\n"
                "   │  1. Генерация данных (N=200) │\n"
                "   └──────────────┬───────────────┘\n"
                "                  ↓\n"
                "   ┌──────────────────────────────┐\n"
                "   │  2. Осмотр: shape, info     │\n"
                "   │     describe, isnull        │\n"
                "   └──────────────┬───────────────┘\n"
                "                  ↓\n"
                "   ┌──────────────────────────────┐\n"
                "   │  3. Числовые: hist, boxplot │\n"
                "   └──────────────┬───────────────┘\n"
                "                  ↓\n"
                "   ┌──────────────────────────────┐\n"
                "   │  4. Категории: value_counts │\n"
                "   └──────────────┬───────────────┘\n"
                "                  ↓\n"
                "   ┌──────────────────────────────┐\n"
                "   │  5. Связи: corr, heatmap    │\n"
                "   └──────────────┬───────────────┘\n"
                "                  ↓\n"
                "   ┌──────────────────────────────┐\n"
                "   │  6. Выбросы: IQR, Z-score   │\n"
                "   └──────────────┬───────────────┘\n"
                "                  ↓\n"
                "   ┌──────────────────────────────┐\n"
                "   │  7. Гипотезы: t-test, χ²    │\n"
                "   └──────────────┬───────────────┘\n"
                "                  ↓\n"
                "   ┌──────────────────────────────┐\n"
                "   │  8. Выводы                  │\n"
                "   └──────────────────────────────┘"
            ),
            example(
                "Полный EDA на синтетических данных SpaceX.",
                "Собираем 200 миссий, проходим все этапы EDA, делаем выводы.",
                "import numpy as np\n"
                "import pandas as pd\n"
                "import matplotlib.pyplot as plt\n"
                "import seaborn as sns\n"
                "from scipy import stats\n"
                "np.random.seed(42)\n"
                "n = 200\n"
                "df = pd.DataFrame({\n"
                "    'mission_id': range(1, n+1),\n"
                "    'rocket': np.random.choice(['Falcon 9', 'Falcon Heavy', 'Starship'], n, p=[0.6, 0.3, 0.1]),\n"
                "    'orbit': np.random.choice(['LEO', 'GTO', 'SSO', 'MEO'], n, p=[0.5, 0.3, 0.15, 0.05]),\n"
                "    'payload_kg': np.random.exponential(5000, n),\n"
                "    'cost_musd': np.random.exponential(50, n),\n"
                "    'year': np.random.choice(range(2010, 2024), n),\n"
                "    'success': np.random.binomial(1, 0.95, n)\n"
                "})\n"
                "print('Shape:', df.shape)\n"
                "print('\\nInfo:')\n"
                "df.info()\n"
                "print('\\nDescribe:')\n"
                "print(df.describe())\n"
                "print('\\nПропуски:', df.isnull().sum().sum())\n"
                "print('Дубликаты:', df.duplicated().sum())\n"
                "fig, axes = plt.subplots(2, 2, figsize=(14, 10))\n"
                "axes[0,0].hist(df['payload_kg'], bins=30, edgecolor='black')\n"
                "axes[0,0].set_title('Payload distribution')\n"
                "axes[0,1].boxplot(df['cost_musd'])\n"
                "axes[0,1].set_title('Cost boxplot')\n"
                "df['rocket'].value_counts().plot(kind='bar', ax=axes[1,0])\n"
                "axes[1,0].set_title('Rocket distribution')\n"
                "sns.heatmap(df[['payload_kg', 'cost_musd', 'year', 'success']].corr(), annot=True, cmap='coolwarm', ax=axes[1,1])\n"
                "axes[1,1].set_title('Correlation')\n"
                "plt.tight_layout()\n"
                "plt.show()\n"
                "# Гипотеза: % успеха по типу ракеты\n"
                "print('\\n% успеха по ракетам:')\n"
                "print(df.groupby('rocket')['success'].mean())",
                "Shape: (200, 7)\n...описание...\n% успеха по ракетам:\nFalcon 9       0.95\nFalcon Heavy   0.94\nStarship       0.96",
                "Полный EDA даёт ответы:\n"
                "- 200 миссий, нет пропусков/дублей\n"
                "- payload_kg скошен (mean >> median)\n"
                "- Falcon 9 — 60% миссий\n"
                "- Корреляция payload-cost: ~0.7\n"
                "- Все ракеты одинаково успешны (~95%)\n"
                "- Выбросы в payload — тяжёлые Falcon Heavy"
            ),
            common_mistakes([
                {"mistake": "Сразу к модели без EDA", "why_bad": "Мусор на входе — мусор на выходе", "fix": "EDA → очистка → фичи → модель"},
                {"mistake": "Игнорировать domain knowledge", "why_bad": "Выброс Falcon Heavy — не удалять", "fix": "Знай предметную область"},
                {"mistake": "Строить 100 графиков", "why_bad": "Неструктурированно, теряется фокус", "fix": "График → вывод → следующий вопрос"},
                {"mistake": "Забыть проверить гипотезы", "why_bad": "Домыслы вместо выводов", "fix": "EDA → гипотезы → статистический тест"},
            ]),
            interview_questions([
                {"q": "Расскажите полный EDA на реальном датасете", "a": "1) shape/info/describe, 2) пропуски/дубли, 3) числовые: describe+hist+box, 4) категории: value_counts+bar, 5) связи: corr+heatmap+scatter, 6) выбросы: IQR/Z-score, 7) фичи, 8) гипотезы: t-test/chi2, 9) summary."},
                {"q": "Как подвести итоги EDA?", "a": "Краткое summary: 1) Что в данных (N, типы). 2) Качество (пропуски, дубли, выбросы). 3) Главные закономерности. 4) Подтверждённые гипотезы. 5) Рекомендации для следующих шагов (фичи, модели, доочистка)."},
                {"q": "Сколько времени уходит на EDA в реальном проекте?", "a": "50-70% времени проекта. Это не «необязательный» этап, а основа всего. Без EDA — модель на грязных данных, ложные выводы, перерасход ресурсов."},
            ]),
            knowledge_checklist([
                "Делаю полный EDA за 30-60 минут",
                "Проверяю пропуски и дубликаты",
                "Визуализирую числовые и категориальные",
                "Строю корреляционную матрицу",
                "Нахожу и интерпретирую выбросы",
                "Проверяю статистические гипотезы",
                "Формулирую summary EDA",
            ]),
        ],
        exercises=[
            ex(1, "python", "Сгенерируй `df` с 200 SpaceX-миссиями: rocket, orbit, payload_kg, cost_musd, year, success. Сохрани в `df`.",
               "import numpy as np\nimport pandas as pd\ndf = None\n",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\nn = 200\ndf = pd.DataFrame({\n    'rocket': np.random.choice(['Falcon 9', 'Falcon Heavy', 'Starship'], n, p=[0.6, 0.3, 0.1]),\n    'orbit': np.random.choice(['LEO', 'GTO', 'SSO'], n, p=[0.5, 0.3, 0.2]),\n    'payload_kg': np.random.exponential(5000, n),\n    'cost_musd': np.random.exponential(50, n),\n    'year': np.random.choice(range(2010, 2024), n),\n    'success': np.random.binomial(1, 0.95, n)\n})",
               [{"check": "isinstance(df, pd.DataFrame)", "msg": "DataFrame"},
                {"check": "df.shape[0] == 200", "msg": "200 строк"},
                {"check": "'rocket' in df.columns and 'success' in df.columns", "msg": "Колонки на месте"}],
               ["np.random.choice", "np.random.exponential", "np.random.binomial"], 1),
            ex(2, "python", "Дан `df`. Сохрани shape в `shape` и число пропусков в `n_null`.",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({\n    'payload_kg': np.random.exponential(5000, 200),\n    'success': np.random.binomial(1, 0.95, 200)\n})\nshape, n_null = (0,0), 0\n",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({\n    'payload_kg': np.random.exponential(5000, 200),\n    'success': np.random.binomial(1, 0.95, 200)\n})\nshape = df.shape\nn_null = df.isnull().sum().sum()",
               [{"check": "shape == (200, 2)", "msg": "shape = (200, 2)"},
                {"check": "n_null == 0", "msg": "Нет пропусков"}],
               ["df.shape", "df.isnull().sum().sum()"], 1),
            ex(3, "python", "Дан `df` с числовыми `payload_kg`, `cost_musd`. Построй describe(), сохрани в `stats`.",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({\n    'payload_kg': np.random.exponential(5000, 200),\n    'cost_musd': np.random.exponential(50, 200)\n})\nstats = None\n",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({\n    'payload_kg': np.random.exponential(5000, 200),\n    'cost_musd': np.random.exponential(50, 200)\n})\nstats = df.describe()",
               [{"check": "stats.loc['mean', 'payload_kg'] > 0", "msg": "Mean > 0"},
                {"check": "stats.loc['std', 'cost_musd'] > 0", "msg": "Std > 0"}],
               ["df.describe()"], 1),
            ex(4, "python", "Дан `df` с `payload_kg`. Построй гистограмму и box plot на 1 рисунке (subplots 1x2).",
               "import matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'payload_kg': np.random.exponential(5000, 200)})\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'payload_kg': np.random.exponential(5000, 200)})\nfig, axes = plt.subplots(1, 2, figsize=(12, 4))\naxes[0].hist(df['payload_kg'], bins=30, edgecolor='black')\naxes[0].set_title('Histogram')\naxes[1].boxplot(df['payload_kg'])\naxes[1].set_title('Boxplot')\nplt.tight_layout()\nplt.show()",
               [{"check": "True", "msg": "Графики построены"}],
               ["plt.subplots(1, 2)", "hist + boxplot"], 2),
            ex(5, "python", "Дан `df` с `rocket`. Посчитай value_counts, сохрани в `vc`.",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'rocket': np.random.choice(['F9', 'FH', 'S'], 200)})\nvc = None\n",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'rocket': np.random.choice(['F9', 'FH', 'S'], 200)})\nvc = df['rocket'].value_counts()",
               [{"check": "vc.sum() == 200", "msg": "Сумма = 200"},
                {"check": "isinstance(vc, pd.Series)", "msg": "Series"}],
               ["value_counts()"], 1),
            ex(6, "python", "Дан `df` с числовыми колонками. Посчитай корреляционную матрицу, сохрани в `corr`.",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({\n    'payload_kg': np.random.exponential(5000, 200),\n    'cost_musd': np.random.exponential(50, 200),\n    'year': np.random.choice(range(2010, 2024), 200)\n})\ncorr = None\n",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({\n    'payload_kg': np.random.exponential(5000, 200),\n    'cost_musd': np.random.exponential(50, 200),\n    'year': np.random.choice(range(2010, 2024), 200)\n})\ncorr = df.corr()",
               [{"check": "corr.shape == (3, 3)", "msg": "3x3 матрица"},
                {"check": "abs(corr.loc['payload_kg', 'payload_kg'] - 1) < 0.01", "msg": "diag = 1"}],
               ["df.corr()"], 1),
            ex(7, "python", "Дан `df` с `payload_kg`. Построй heatmap корреляций всех числовых колонок.",
               "import seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({\n    'payload_kg': np.random.exponential(5000, 200),\n    'cost_musd': np.random.exponential(50, 200)\n})\n",
               "import seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({\n    'payload_kg': np.random.exponential(5000, 200),\n    'cost_musd': np.random.exponential(50, 200)\n})\nsns.heatmap(df.corr(), annot=True, cmap='coolwarm')\nplt.title('Корреляция SpaceX')\nplt.show()",
               [{"check": "True", "msg": "Heatmap построен"}],
               ["sns.heatmap(df.corr(), annot=True)", "cmap='coolwarm'"], 2),
            ex(8, "python", "Дан `df` с `payload_kg` (200 значений, 5 выбросов). Найди выбросы IQR-методом, сохрани в `outliers`.",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'payload_kg': np.concatenate([np.random.exponential(5000, 195), [50000, 60000, 70000, 80000, 90000]])})\noutliers = None\n",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'payload_kg': np.concatenate([np.random.exponential(5000, 195), [50000, 60000, 70000, 80000, 90000]])})\nq1 = df['payload_kg'].quantile(0.25)\nq3 = df['payload_kg'].quantile(0.75)\niqr = q3 - q1\nlower = q1 - 1.5 * iqr\nupper = q3 + 1.5 * iqr\noutliers = df[(df['payload_kg'] < lower) | (df['payload_kg'] > upper)]",
               [{"check": "len(outliers) == 5", "msg": "5 выбросов"}],
               ["IQR = Q3 - Q1", "lower = Q1 - 1.5*IQR", "upper = Q3 + 1.5*IQR"], 2),
            ex(9, "python", "Дан `df` с `rocket` и `success`. Посчитай % успеха по типу ракеты, сохрани в `success_rate`.",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({\n    'rocket': np.random.choice(['F9', 'FH', 'S'], 200),\n    'success': np.random.binomial(1, 0.95, 200)\n})\nsuccess_rate = None\n",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({\n    'rocket': np.random.choice(['F9', 'FH', 'S'], 200),\n    'success': np.random.binomial(1, 0.95, 200)\n})\nsuccess_rate = df.groupby('rocket')['success'].mean()",
               [{"check": "isinstance(success_rate, pd.Series)", "msg": "Series"},
                {"check": "(success_rate >= 0).all() and (success_rate <= 1).all()", "msg": "Доли 0-1"}],
               ["df.groupby('rocket')['success'].mean()"], 2),
            ex(10, "python", "Дан `df` с двумя группами и числовой `x`. Проведи t-test, сохрани `t, p`.",
               "import numpy as np\nimport pandas as pd\nfrom scipy import stats\nnp.random.seed(42)\ndf = pd.DataFrame({\n    'group': ['A']*50 + ['B']*50,\n    'x': np.concatenate([np.random.normal(0, 1, 50), np.random.normal(2, 1, 50)])\n})\nt, p = 0, 1\n",
               "import numpy as np\nimport pandas as pd\nfrom scipy import stats\nnp.random.seed(42)\ndf = pd.DataFrame({\n    'group': ['A']*50 + ['B']*50,\n    'x': np.concatenate([np.random.normal(0, 1, 50), np.random.normal(2, 1, 50)])\n})\na = df[df['group']=='A']['x']\nb = df[df['group']=='B']['x']\nt, p = stats.ttest_ind(a, b)",
               [{"check": "p < 0.001", "msg": "Очень значимо"}],
               ["stats.ttest_ind", "H0: средние равны"], 2),
            ex(11, "python", "Дан `df` с `orbit` и `success`. Проведи chi-square, сохрани `chi2, p`.",
               "import numpy as np\nimport pandas as pd\nfrom scipy import stats\nnp.random.seed(42)\ndf = pd.DataFrame({\n    'orbit': np.random.choice(['LEO', 'GTO', 'SSO'], 300),\n    'success': np.random.binomial(1, 0.95, 300)\n})\nchi2, p = 0, 1\n",
               "import numpy as np\nimport pandas as pd\nfrom scipy import stats\nnp.random.seed(42)\ndf = pd.DataFrame({\n    'orbit': np.random.choice(['LEO', 'GTO', 'SSO'], 300),\n    'success': np.random.binomial(1, 0.95, 300)\n})\nct = pd.crosstab(df['orbit'], df['success'])\nchi2, p, dof, expected = stats.chi2_contingency(ct)",
               [{"check": "p > 0.05", "msg": "p > 0.05 (нет связи)"}],
               ["pd.crosstab", "chi2_contingency"], 2),
            ex(12, "python", "Дан `df` с `payload_kg` (200 значений, 5 выбросов вверху). Удали выбросы IQR-методом, сохрани в `df_clean`.",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'payload_kg': np.concatenate([np.random.exponential(5000, 195), [50000, 60000, 70000, 80000, 90000]])})\ndf_clean = df\n",
               "import numpy as np\nimport pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({'payload_kg': np.concatenate([np.random.exponential(5000, 195), [50000, 60000, 70000, 80000, 90000]])})\nq1 = df['payload_kg'].quantile(0.25)\nq3 = df['payload_kg'].quantile(0.75)\niqr = q3 - q1\nlower = q1 - 1.5 * iqr\nupper = q3 + 1.5 * iqr\ndf_clean = df[(df['payload_kg'] >= lower) & (df['payload_kg'] <= upper)]",
               [{"check": "df_clean.shape[0] == 195", "msg": "195 строк (200 - 5 выбросов)"}],
               ["IQR-метод", "Инвертированный фильтр"], 2),
        ],
        minutes=90, difficulty=3,
    )


LESSONS = [_6_1, _6_2, _6_3, _6_4, _6_5, _6_6, _6_7, _6_8]
