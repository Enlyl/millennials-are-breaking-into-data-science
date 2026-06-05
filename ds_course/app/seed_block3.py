"""
Блок 3: NumPy и Pandas.
12 уроков, ~104 упражнения.
"""
from app.seed_helpers import (
    ex, lesson, theory, analogy, visual, example,
    common_mistakes, interview_questions, knowledge_checklist,
)


def _3_1():
    return lesson(
        "3.1", "NumPy: массивы и операции", "space", [
            theory(
                "**NumPy** (Numerical Python) — фундамент научных вычислений в Python. "
                "Главный объект — `ndarray` (N-мерный массив), который быстрее и компактнее "
                "обычных списков Python за счёт хранения элементов одного типа в непрерывной памяти.\n\n"
                "**Создание массивов:**\n"
                "- `np.array([1, 2, 3])` — из списка\n"
                "- `np.zeros(5)` — массив из нулей\n"
                "- `np.ones((2, 3))` — массив из единиц\n"
                "- `np.arange(0, 10, 2)` — как `range`, но возвращает массив\n"
                "- `np.linspace(0, 1, 5)` — 5 равноотстоящих точек от 0 до 1\n\n"
                "**Векторизация:** операции применяются поэлементно без явных циклов. "
                "`a + 2` прибавит 2 к каждому элементу, `a * b` — поэлементное умножение. "
                "Атрибуты: `arr.shape` (размерности), `arr.dtype` (тип), `arr.ndim` (число осей)."
            ),
            analogy(
                "Список Python — коробка с разнокалиберными предметами (медленный поиск). "
                "Массив NumPy — кассета на конвейере: все ячейки одинаковые, индексация мгновенная.",
                "Температуры двигателя ракеты, замеренные каждую секунду: `[3200, 3220, 3180, ...]` — "
                "идеально ложатся в `np.array` для мгновенного расчёта среднего и аномалий."
            ),
            visual(
                "Список vs массив NumPy",
                "  Python list:                  NumPy ndarray:\n"
                "  ┌───┬───┬───┬───┐             ┌─────┬─────┬─────┬─────┐\n"
                "  │ 10│3.5│ 7 │'x'│  разные     │  10 │  20 │  30 │  40 │  один тип (int64)\n"
                "  └───┴───┴───┴───┘  типы       └─────┴─────┴─────┴─────┘\n"
                "   указатели → объекты            плотная память, быстрый SIMD\n"
                "\n"
                "  shape = (4,)        ndim = 1         dtype = int64"
            ),
            example(
                "Создай массив скоростей 5 ракет и посчитай среднее.",
                "np.array() принимает список. .mean() — метод NumPy. Атрибут dtype показывает тип.",
                "import numpy as np\n"
                "speeds = np.array([7800, 7900, 8000, 7600, 11200])\n"
                "print('Среднее:', speeds.mean())\n"
                "print('Максимум:', speeds.max())\n"
                "print('Форма:', speeds.shape)\n"
                "print('Тип:', speeds.dtype)",
                "Среднее: 8500.0\nМаксимум: 11200\nФорма: (5,)\nТип: int64",
                "Все методы (.mean, .max) возвращают обычные числа Python или numpy-скаляры. "
                "shape = (5,) — одномерный массив из 5 элементов."
            ),
            common_mistakes([
                {"mistake": "np.array([1, 2, 3]) * 2 → повторение массива", "why_bad": "Ожидают список, получают поэлементное умножение [2,4,6]", "fix": "Это и есть векторизация. Для повторения: np.tile(arr, 2) или np.concatenate"},
                {"mistake": "a = np.array([1, '2', 3])", "why_bad": "NumPy приведёт всё к строке — dtype='<U11'", "fix": "Передавай числа: np.array([1, 2, 3])"},
                {"mistake": "np.arange(1, 5) — ожидание 1..5", "why_bad": "Правая граница исключается: 1,2,3,4", "fix": "np.arange(1, 6) даст 1..5"},
                {"mistake": "arr.shape[0] для 1D-массива", "why_bad": "shape = (5,), shape[0]=5 — ок, но для столбца (5,1) будет 5 строк, не 1", "fix": "Используй len(arr) для 1D, arr.shape[0] для 2D"},
            ]),
            interview_questions([
                {"q": "Почему NumPy быстрее списков Python?", "a": "1) Хранение в непрерывной памяти одного типа. 2) Векторизация — операции на уровне C, без интерпретатора. 3) SIMD-инструкции процессора."},
                {"q": "Чем ndarray отличается от list?", "a": "ndarray: один dtype, фиксированный размер, векторизация. list: разные типы, динамический, медленнее для математики."},
                {"q": "Что делает np.linspace(0, 1, 5)?", "a": "Возвращает 5 равноотстоящих точек от 0 до 1 включительно: [0., 0.25, 0.5, 0.75, 1.]."},
            ]),
            knowledge_checklist([
                "Создаю массивы через np.array, np.zeros, np.arange",
                "Знаю атрибуты shape, dtype, ndim",
                "Применяю поэлементные операции (+, *, /)",
                "Использую методы .mean(), .max(), .min(), .sum()",
                "Понимаю разницу между list и ndarray",
            ]),
        ],
        exercises=[
            ex(1, "python", "Создай `arr` — массив NumPy из [10, 20, 30, 40, 50].",
               "import numpy as np\n# твой код\n",
               "import numpy as np\narr = np.array([10, 20, 30, 40, 50])",
               [{"check": "isinstance(arr, np.ndarray)", "msg": "arr — np.ndarray"},
                {"check": "arr.shape == (5,)", "msg": "shape = (5,)"}],
               ["np.array([...])", "Импортируй numpy как np"], 1),
            ex(2, "python", "Создай `zeros_arr` — массив из 5 нулей.",
               "import numpy as np\n",
               "import numpy as np\nzeros_arr = np.zeros(5)",
               [{"check": "isinstance(zeros_arr, np.ndarray)", "msg": "ndarray"},
                {"check": "(zeros_arr == 0).all()", "msg": "Все нули"},
                {"check": "zeros_arr.shape == (5,)", "msg": "5 элементов"}],
               ["np.zeros(n)", "Передай целое число"], 1),
            ex(3, "python", "Создай `ones_2d` — массив 2×3 из единиц.",
               "import numpy as np\n",
               "import numpy as np\nones_2d = np.ones((2, 3))",
               [{"check": "ones_2d.shape == (2, 3)", "msg": "shape (2,3)"},
                {"check": "ones_2d.sum() == 6", "msg": "6 единиц"}],
               ["np.ones((rows, cols))", "Кортеж для 2D"], 1),
            ex(4, "python", "Создай `arange_arr` — np.arange(0, 20, 2).",
               "import numpy as np\n",
               "import numpy as np\nnarange_arr = np.arange(0, 20, 2)",
               [{"check": "len(arange_arr) == 10", "msg": "10 элементов"},
                {"check": "arange_arr[0] == 0 and arange_arr[-1] == 18", "msg": "0 и 18"}],
               ["np.arange(start, stop, step)", "stop не включается"], 1),
            ex(5, "python", "Создай `temps` из [3200, 3220, 3180, 3250, 3190]. Посчитай среднее в `mean_t`.",
               "import numpy as np\n",
               "import numpy as np\ntemps = np.array([3200, 3220, 3180, 3250, 3190])\nmean_t = temps.mean()",
               [{"check": "isinstance(temps, np.ndarray)", "msg": "temps — массив"},
                {"check": "abs(mean_t - 3208.0) < 0.5", "msg": "Среднее ≈ 3208"}],
               ["np.array(...)", ".mean() — метод"], 2),
            ex(6, "python", "Дан arr = np.array([3, 6, 9, 12]). Создай `doubled` — каждый элемент умножен на 2.",
               "import numpy as np\narr = np.array([3, 6, 9, 12])\n",
               "import numpy as np\narr = np.array([3, 6, 9, 12])\ndoubled = arr * 2",
               [{"check": "(doubled == np.array([6, 12, 18, 24])).all()", "msg": "[6,12,18,24]"}],
               ["Векторизация: arr * 2", "Цикл не нужен"], 1),
            ex(7, "python", "Даны a=np.array([1,2,3]) и b=np.array([10,20,30]). Создай `s` — поэлементную сумму.",
               "import numpy as np\na = np.array([1, 2, 3])\nb = np.array([10, 20, 30])\n",
               "import numpy as np\na = np.array([1, 2, 3])\nb = np.array([10, 20, 30])\ns = a + b",
               [{"check": "(s == np.array([11, 22, 33])).all()", "msg": "[11, 22, 33]"}],
               ["a + b поэлементно", "Это не конкатенация"], 2),
            ex(8, "python", "Создай `mtx` — двумерный массив [[1,2,3],[4,5,6]]. Найди сумму всех элементов в `total`.",
               "import numpy as np\n",
               "import numpy as np\nmtx = np.array([[1, 2, 3], [4, 5, 6]])\ntotal = mtx.sum()",
               [{"check": "mtx.ndim == 2", "msg": "2D"},
                {"check": "total == 21", "msg": "1+2+...+6 = 21"}],
               ["np.array([ [...], [...] ])", ".sum() суммирует всё"], 2),
            ex(9, "python", "Дан arr=np.array([5,10,15,20,25]). Сохрани в `stats` кортеж (мин, макс, среднее).",
               "import numpy as np\narr = np.array([5, 10, 15, 20, 25])\n",
               "import numpy as np\narr = np.array([5, 10, 15, 20, 25])\nstats = (arr.min(), arr.max(), arr.mean())",
               [{"check": "stats == (5, 25, 15.0)", "msg": "(5, 25, 15.0)"}],
               [".min(), .max(), .mean()", "Кортеж в скобках"], 3),
            ex(10, "python", "Создай `linspace_arr` = np.linspace(0, 10, 5). Сколько в нём элементов?",
               "import numpy as np\n",
               "import numpy as np\nlinspace_arr = np.linspace(0, 10, 5)",
               [{"check": "len(linspace_arr) == 5", "msg": "5 точек"},
                {"check": "abs(linspace_arr[0] - 0.0) < 1e-9", "msg": "Начало 0"},
                {"check": "abs(linspace_arr[-1] - 10.0) < 1e-9", "msg": "Конец 10"}],
               ["np.linspace(start, stop, num)", "Обе границы включены"], 2),
        ],
        minutes=50, difficulty=2,
    )


def _3_2():
    return lesson(
        "3.2", "NumPy: индексация, срезы, маски", "space", [
            theory(
                "**Индексация в NumPy** похожа на списки Python, но мощнее за счёт **булевых масок** и **fancy indexing**.\n\n"
                "**Базовая индексация:**\n"
                "- `arr[0]` — первый элемент\n"
                "- `arr[-1]` — последний\n"
                "- `arr[2:5]` — срез с 2 по 4 (5 не включается)\n"
                "- `arr[::2]` — каждый второй\n"
                "- `arr2d[0, 1]` — строка 0, столбец 1\n\n"
                "**Булева маска** — массив bool того же размера, который фильтрует элементы:\n"
                "```python\n"
                "mask = arr > 10\n"
                "arr[mask]  # только элементы > 10\n"
                "```\n\n"
                "**Fancy indexing** — передача списка индексов: `arr[[0, 2, 4]]`."
            ),
            analogy(
                "Булева маска — рентгеновский фильтр: показывает только те точки, где выполняется условие (перелом, трещина, >10).",
                "В телеметрии ракеты: `mask = temperatures > 3300` — оставляет только критические замеры для отчёта об аномалии."
            ),
            visual(
                "Булева маска: фильтрация как просеивание",
                "  Исходный массив:        Маска:               Результат:\n"
                "  [ 3,  7,  2,  9,  5 ]   [F,  T,  F,  T,  F]   [ 7,  9 ]\n"
                "                          условие: > 5\n"
                "\n"
                "  arr > 5  →  bool[]  →  arr[bool[]]\n"
                "\n"
                "  2D индексация: arr2d[1, 2] = arr2d[1][2]\n"
                "  ┌─────┬─────┬─────┐\n"
                "  │  0,0│  0,1│  0,2│\n"
                "  ├─────┼─────┼─────┤\n"
                "  │  1,0│  1,1│ ▒1,2▒ ← вот этот\n"
                "  └─────┴─────┴─────┘"
            ),
            example(
                "Из массива скоростей выбери только сверхзвуковые (> 343 м/с) и отрицательные (<0).",
                "Создаём две маски и применяем их к массиву. arr[mask] возвращает только подходящие элементы.",
                "import numpy as np\n"
                "speeds = np.array([-50, 100, 400, 800, 1200, -10, 350])\n"
                "supersonic = speeds[speeds > 343]\n"
                "negative = speeds[speeds < 0]\n"
                "print('Сверхзвуковые:', supersonic)\n"
                "print('Отрицательные:', negative)\n"
                "print('Среднее supersonic:', supersonic.mean())",
                "Сверхзвуковые: [ 400  800 1200  350]\nОтрицательные: [-50 -10]\nСреднее supersonic: 687.5",
                "speeds > 343 возвращает массив bool. speeds[mask] фильтрует. .mean() работает на отфильтрованном подмассиве."
            ),
            common_mistakes([
                {"mistake": "arr[mask] без скобок вокруг условия", "why_bad": "arr > 5, 7 — кортеж из двух массивов, IndexError", "fix": "Используй &(and) и |(or): arr[(arr>5) & (arr<10)]"},
                {"mistake": "arr[arr > 5 and arr < 10]", "why_bad": "and работает со скалярами, не с массивами", "fix": "Заменяй на &: arr[(arr>5) & (arr<10)]"},
                {"mistake": "arr2d[0][0] в логической маске", "why_bad": "Двойная индексация создаёт view, не копию", "fix": "Для копии: arr2d[0, :].copy()"},
                {"mistake": "arr[0:5] вместо arr[:5]", "why_bad": "Не ошибка, но избыточно", "fix": "Используй краткую форму arr[:5]"},
            ]),
            interview_questions([
                {"q": "Чем arr[mask] отличается от arr[indices]?", "a": "arr[mask] — булева фильтрация (True/False). arr[indices] — выбор по индексам (int или список int). Результат всегда 1D."},
                {"q": "Что вернёт arr[arr < 0] = 0?", "a": "Заменит все отрицательные значения на 0 в исходном массиве (in-place через fancy indexing)."},
                {"q": "Чем отличается срез list[1:3] от np.array[1:3]?", "a": "list[1:3] — копия. np.array[1:3] — view (тот же буфер). Меняешь срез — меняется оригинал."},
            ]),
            knowledge_checklist([
                "Делаю срезы arr[start:stop:step]",
                "Фильтрую через булеву маску arr[arr > x]",
                "Использую &, |, ~ вместо and, or, not",
                "Индексирую 2D-массивы: arr2d[i, j]",
                "Применяю fancy indexing arr[[0,2,4]]",
            ]),
        ],
        exercises=[
            ex(1, "python", "Дан arr=np.array([10,20,30,40,50]). Сохрани в `third` элемент с индексом 2.",
               "import numpy as np\narr = np.array([10, 20, 30, 40, 50])\n",
               "import numpy as np\narr = np.array([10, 20, 30, 40, 50])\nthird = arr[2]",
               [{"check": "third == 30", "msg": "arr[2] = 30"}],
               ["Индексы с 0", "arr[0]=10, arr[2]=30"], 1),
            ex(2, "python", "Дан arr=np.array([10,20,30,40,50]). Сохрани в `last` последний элемент.",
               "import numpy as np\narr = np.array([10, 20, 30, 40, 50])\n",
               "import numpy as np\narr = np.array([10, 20, 30, 40, 50])\nlast = arr[-1]",
               [{"check": "last == 50", "msg": "Последний — 50"}],
               ["Отрицательный индекс: -1", "Или arr[4]"], 1),
            ex(3, "python", "Дан arr=np.arange(10). Сохрани в `sl` срез [3,4,5,6,7].",
               "import numpy as np\narr = np.arange(10)\n",
               "import numpy as np\narr = np.arange(10)\nsl = arr[3:8]",
               [{"check": "(sl == np.array([3,4,5,6,7])).all()", "msg": "[3,4,5,6,7]"}],
               ["arr[start:stop]", "stop не включается"], 1),
            ex(4, "python", "Дан arr=np.arange(10). Сохрани в `even_idx` каждый второй элемент, начиная с 0: [0,2,4,6,8].",
               "import numpy as np\narr = np.arange(10)\n",
               "import numpy as np\narr = np.arange(10)\neven_idx = arr[::2]",
               [{"check": "(even_idx == np.array([0,2,4,6,8])).all()", "msg": "[0,2,4,6,8]"}],
               ["arr[::step]", "Шаг 2"], 1),
            ex(5, "python", "Дан arr=np.array([5,12,7,18,3,21]). Сохрани в `big` только элементы > 10.",
               "import numpy as np\narr = np.array([5, 12, 7, 18, 3, 21])\n",
               "import numpy as np\narr = np.array([5, 12, 7, 18, 3, 21])\nbig = arr[arr > 10]",
               [{"check": "(big == np.array([12, 18, 21])).all()", "msg": "[12, 18, 21]"}],
               ["arr[arr > 10]", "Булева маска"], 2),
            ex(6, "python", "Дан arr=np.array([5,12,7,18,3,21]). Сохрани в `mid` элементы от 5 до 20 (включительно).",
               "import numpy as np\narr = np.array([5, 12, 7, 18, 3, 21])\n",
               "import numpy as np\narr = np.array([5, 12, 7, 18, 3, 21])\nmid = arr[(arr >= 5) & (arr <= 20)]",
               [{"check": "(mid == np.array([5, 12, 7, 18])).all()", "msg": "[5,12,7,18]"}],
               ["& для AND, | для OR", "Скобки обязательны"], 3),
            ex(7, "python", "Дан arr=np.array([5,12,7,18,3,21]). Сохрани в `idx` элементы с индексами [0, 2, 4].",
               "import numpy as np\narr = np.array([5, 12, 7, 18, 3, 21])\n",
               "import numpy as np\narr = np.array([5, 12, 7, 18, 3, 21])\nidx = arr[[0, 2, 4]]",
               [{"check": "(idx == np.array([5, 7, 3])).all()", "msg": "[5, 7, 3]"}],
               ["Fancy indexing", "Список индексов в []"], 2),
            ex(8, "python", "Дан arr=np.array([-5, 3, -2, 8, -1, 0]). Замени отрицательные на 0, сохрани в `clean`.",
               "import numpy as np\narr = np.array([-5, 3, -2, 8, -1, 0])\n",
               "import numpy as np\narr = np.array([-5, 3, -2, 8, -1, 0])\nclean = arr.copy()\nclean[clean < 0] = 0",
               [{"check": "(clean == np.array([0, 3, 0, 8, 0, 0])).all()", "msg": "Все отрицательные = 0"}],
               ["Маска + присваивание", "copy() чтобы не менять оригинал"], 3),
            ex(9, "python", "Дан arr2d=np.array([[1,2,3],[4,5,6],[7,8,9]]). Сохрани в `row1` вторую строку.",
               "import numpy as np\narr2d = np.array([[1,2,3],[4,5,6],[7,8,9]])\n",
               "import numpy as np\narr2d = np.array([[1,2,3],[4,5,6],[7,8,9]])\nrow1 = arr2d[1]",
               [{"check": "(row1 == np.array([4,5,6])).all()", "msg": "[4,5,6]"}],
               ["arr2d[i] — i-я строка", "Индексы с 0"], 2),
            ex(10, "python", "Дан arr2d=np.array([[1,2,3],[4,5,6],[7,8,9]]). Сохрани в `corner` элемент [0,0] и [2,2] в виде массива.",
               "import numpy as np\narr2d = np.array([[1,2,3],[4,5,6],[7,8,9]])\n",
               "import numpy as np\narr2d = np.array([[1,2,3],[4,5,6],[7,8,9]])\ncorner = np.array([arr2d[0,0], arr2d[2,2]])",
               [{"check": "(corner == np.array([1, 9])).all()", "msg": "[1, 9]"}],
               ["arr2d[i, j]", "Собери в новый массив"], 3),
        ],
        minutes=55, difficulty=2,
    )


def _3_3():
    return lesson(
        "3.3", "Pandas: Series и DataFrame", "space", [
            theory(
                "**Pandas** — библиотека для табличных данных. Два главных объекта:\n\n"
                "**`Series`** — одномерный массив с индексом (аналог столбца таблицы):\n"
                "```python\n"
                "s = pd.Series([10, 20, 30], index=['a','b','c'])\n"
                "```\n\n"
                "**`DataFrame`** — двумерная таблица со столбцами и строками-индексами:\n"
                "```python\n"
                "df = pd.DataFrame({\n"
                "    'name': ['Falcon 9', 'Saturn V'],\n"
                "    'mass': [549054, 2970000]\n"
                "})\n"
                "```\n\n"
                "**Основные свойства:**\n"
                "- `df.shape` — (строки, столбцы)\n"
                "- `df.columns` — имена столбцов\n"
                "- `df.dtypes` — типы столбцов\n"
                "- `df.head(n)` — первые n строк\n"
                "- `df['col']` — выбор столбца (возвращает Series)\n"
                "- `df[['c1','c2']]` — выбор нескольких столбцов"
            ),
            analogy(
                "Series — один столбец Excel с подписанными строками. DataFrame — вся таблица Excel целиком.",
                "Таблица запусков SpaceX: столбцы `mission`, `rocket`, `date`, `success` — каждая строка = один запуск."
            ),
            visual(
                "Series и DataFrame",
                "  Series (1D):\n"
                "  Index  Values\n"
                "  ─────  ──────\n"
                "    a       10\n"
                "    b       20    ← s = pd.Series([10,20,30], index=['a','b','c'])\n"
                "    c       30\n"
                "\n"
                "  DataFrame (2D):\n"
                "        mission    rocket   payload_kg\n"
                "  ────────────────────────\n"
                "  0   'Crew-1'   'Falcon 9'    12000\n"
                "  1   'Crew-2'   'Falcon 9'    12000\n"
                "  2   'Apollo'   'Saturn V'   49000   ← df.shape = (3, 3)"
            ),
            example(
                "Создай DataFrame с тремя миссиями SpaceX и выведи первые 2 строки.",
                "DataFrame из словаря: ключи = имена столбцов, значения = данные. head(2) показывает первые 2 строки.",
                "import pandas as pd\n"
                "df = pd.DataFrame({\n"
                "    'mission': ['Crew-1', 'Crew-2', 'Starlink-23'],\n"
                "    'rocket': ['Falcon 9', 'Falcon 9', 'Falcon 9'],\n"
                "    'payload_kg': [12000, 12000, 15400]\n"
                "})\n"
                "print(df)\n"
                "print('---')\n"
                "print(df.head(2))",
                "      mission    rocket  payload_kg\n0    Crew-1  Falcon 9       12000\n1    Crew-2  Falcon 9       12000\n2  Starlink-23  Falcon 9       15400\n---\n  mission    rocket  payload_kg\n0  Crew-1  Falcon 9       12000\n1  Crew-2  Falcon 9       12000",
                "Без указания индекса Pandas создаёт RangeIndex 0..N-1. head(n) — срез первых n строк (по умолчанию 5)."
            ),
            common_mistakes([
                {"mistake": "df['col1', 'col2'] — двойной ключ", "why_bad": "Ищет столбец с именем кортежа ('col1', 'col2')", "fix": "Двойные скобки: df[['col1', 'col2']]"},
                {"mistake": "pd.Series([1,2,3]) без индекса", "why_bad": "Не ошибка, но индекс 0,1,2 — не информативно", "fix": "Задай index: pd.Series([1,2,3], index=['a','b','c'])"},
                {"mistake": "df.col для столбца с пробелом", "why_bad": "AttributeError: 'DataFrame' object has no attribute 'col name'", "fix": "Используй df['col name'] со скобками"},
                {"mistake": "Путаница df.shape[0] и [1]", "why_bad": "[0] — строки, [1] — столбцы. Легко перепутать", "fix": "Запомни: (rows, cols) как в матрице"},
            ]),
            interview_questions([
                {"q": "Чем Series отличается от DataFrame?", "a": "Series — одномерный массив с индексом (1 ось). DataFrame — двумерная таблица (2 оси: строки и столбцы), как словарь Series."},
                {"q": "Что такое индекс в Pandas?", "a": "Метки строк (и иногда столбцов). По умолчанию RangeIndex 0..N-1. Можно задать любой: даты, ID, строки."},
                {"q": "Как получить один столбец DataFrame?", "a": "df['col'] — Series. df[['col']] — DataFrame с одним столбцом. df.col — атрибутный доступ (если имя валидно)."},
            ]),
            knowledge_checklist([
                "Создаю Series и DataFrame",
                "Понимаю разницу между Series и DataFrame",
                "Использую df.shape, df.columns, df.dtypes",
                "Выбираю столбец через df['name']",
                "Использую head() для предпросмотра",
            ]),
        ],
        exercises=[
            ex(1, "python", "Импортируй pandas как pd.",
               "# импорт\n",
               "import pandas as pd",
               [{"check": "'pd' in dir() and pd.__name__ == 'pandas'", "msg": "pd доступен"}],
               ["import pandas as pd", "Стандартное сокращение"], 1),
            ex(2, "python", "Создай Series `s` из [100, 200, 300] с индексом ['x','y','z'].",
               "import pandas as pd\n",
               "import pandas as pd\ns = pd.Series([100, 200, 300], index=['x', 'y', 'z'])",
               [{"check": "isinstance(s, pd.Series)", "msg": "Series"},
                {"check": "s['y'] == 200", "msg": "s['y'] = 200"}],
               ["pd.Series(data, index=...)", "index — список меток"], 1),
            ex(3, "python", "Создай DataFrame `df` с колонками 'planet'=['Mars','Venus'] и 'radius_km'=[3389, 6052].",
               "import pandas as pd\n",
               "import pandas as pd\ndf = pd.DataFrame({'planet': ['Mars', 'Venus'], 'radius_km': [3389, 6052]})",
               [{"check": "isinstance(df, pd.DataFrame)", "msg": "DataFrame"},
                {"check": "df.shape == (2, 2)", "msg": "(2, 2)"},
                {"check": "'planet' in df.columns", "msg": "Колонка planet"}],
               ["pd.DataFrame({col: [values]})", "Словарь списков"], 1),
            ex(4, "python", "Дан df с колонками name, score. Сохрани в `scores` столбец score.",
               "import pandas as pd\ndf = pd.DataFrame({'name': ['A', 'B'], 'score': [10, 20]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'name': ['A', 'B'], 'score': [10, 20]})\nscores = df['score']",
               [{"check": "isinstance(scores, pd.Series)", "msg": "Series"},
                {"check": "list(scores) == [10, 20]", "msg": "[10, 20]"}],
               ["df['col']", "Один столбец — Series"], 1),
            ex(5, "python", "Дан df с 5 строками. Сохрани в `first3` первые 3 строки через head.",
               "import pandas as pd\ndf = pd.DataFrame({'x': [1,2,3,4,5]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'x': [1,2,3,4,5]})\nfirst3 = df.head(3)",
               [{"check": "first3.shape == (3, 1)", "msg": "(3,1)"}],
               ["df.head(n)", "n — кол-во строк"], 1),
            ex(6, "python", "Создай DataFrame `missions` с колонками mission, rocket, year (3 строки про SpaceX).",
               "import pandas as pd\n",
               "import pandas as pd\nmissions = pd.DataFrame({\n    'mission': ['Falcon 1', 'Falcon 9', 'Falcon Heavy'],\n    'rocket': ['Falcon 1', 'Falcon 9', 'Falcon Heavy'],\n    'year': [2008, 2010, 2018]\n})",
               [{"check": "missions.shape[0] == 3", "msg": "3 строки"},
                {"check": "'rocket' in missions.columns", "msg": "Колонка rocket"},
                {"check": "missions['year'].sum() == 4036", "msg": "Сумма годов = 4036"}],
               ["Словарь списков", "3 ключа = 3 колонки"], 2),
            ex(7, "python", "Дан df. Сохрани в `two_cols` DataFrame с колонками 'a' и 'b'.",
               "import pandas as pd\ndf = pd.DataFrame({'a':[1,2], 'b':[3,4], 'c':[5,6]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'a':[1,2], 'b':[3,4], 'c':[5,6]})\ntwo_cols = df[['a', 'b']]",
               [{"check": "list(two_cols.columns) == ['a', 'b']", "msg": "Колонки a, b"},
                {"check": "two_cols.shape == (2, 2)", "msg": "(2,2)"}],
               ["Двойные скобки df[[ ]]", "Список колонок внутри"], 2),
            ex(8, "python", "Создай Series `temps` из [3200, 3250, 3180] с именем 'engine_temp'.",
               "import pandas as pd\n",
               "import pandas as pd\ntemps = pd.Series([3200, 3250, 3180], name='engine_temp')",
               [{"check": "isinstance(temps, pd.Series)", "msg": "Series"},
                {"check": "temps.name == 'engine_temp'", "msg": "name задан"}],
               ["pd.Series(data, name=...)", "name — атрибут серии"], 2),
            ex(9, "python", "Дан df. Сохрани в `dtypes_info` — вызови df.dtypes.",
               "import pandas as pd\ndf = pd.DataFrame({'x':[1,2], 'y':['a','b']})\n",
               "import pandas as pd\ndf = pd.DataFrame({'x':[1,2], 'y':['a','b']})\ndtypes_info = df.dtypes",
               [{"check": "str(dtypes_info['x']) == 'int64'", "msg": "x — int64"},
                {"check": "str(dtypes_info['y']) == 'object'", "msg": "y — object"}],
               ["df.dtypes", "Возвращает Series с типами"], 2),
            ex(10, "python", "Создай DataFrame `df` из словаря, где колонка 'count' = [1,2,3,4]. Сохрани в `n` число строк.",
               "import pandas as pd\n",
               "import pandas as pd\ndf = pd.DataFrame({'count': [1, 2, 3, 4]})\nn = df.shape[0]",
               [{"check": "isinstance(df, pd.DataFrame)", "msg": "DataFrame"},
                {"check": "n == 4", "msg": "4 строки"}],
               ["df.shape[0] — строки", "df.shape[1] — столбцы"], 2),
        ],
        minutes=50, difficulty=2,
    )


def _3_4():
    return lesson(
        "3.4", "Импорт данных: CSV, JSON, Excel", "gaming", [
            theory(
                "**Pandas** умеет читать данные из большинства форматов. Самые частые:\n\n"
                "**CSV (Comma-Separated Values):**\n"
                "```python\n"
                "df = pd.read_csv('file.csv')\n"
                "```\n"
                "Параметры: `sep` (разделитель), `header` (None если нет заголовка), `encoding`, `parse_dates`.\n\n"
                "**JSON:**\n"
                "```python\n"
                "df = pd.read_json('file.json')  # или строка\n"
                "```\n"
                "Для вложенных JSON используют `json_normalize`.\n\n"
                "**Excel:**\n"
                "```python\n"
                "df = pd.read_excel('file.xlsx', sheet_name='Лист1')\n"
                "```\n\n"
                "**Быстрый просмотр:** `df.head()`, `df.info()`, `df.describe()` — "
                "последний даёт count/mean/std/min/max по числовым колонкам."
            ),
            analogy(
                "Чтение CSV — открыть книгу Excel: Pandas сам понимает, где строка, где столбец, где данные.",
                "Турнирная таблица CS:GO в CSV — загружаешь и сразу видишь колонки: player, team, kd, adr, hs_pct."
            ),
            visual(
                "Структура CSV и его чтение",
                "  CSV-файл:                Pandas DataFrame:\n"
                "  name,score,team          ┌─────────┬───────┬───────────┐\n"
                "  Alice,1500,FNATIC        │  name   │ score │   team    │\n"
                "  Bob,1200,NAVI    ───►    ├─────────┼───────┼───────────┤\n"
                "  Eve,1800,G2              │  Alice  │  1500 │  FNATIC   │\n"
                "                           │  Bob    │  1200 │  NAVI     │\n"
                "  разделитель ','          │  Eve    │  1800 │  G2       │\n"
                "                           └─────────┴───────┴───────────┘\n"
                "\n"
                "  pd.read_csv('file.csv') — всё в одной строке!"
            ),
            example(
                "Прочитай CSV-данные о матчах Dota 2 и посчитай средний KDA.",
                "pd.read_csv принимает путь/URL/BytesIO. .describe() даёт статистику по числовым колонкам. "
                "Здесь мы создадим DataFrame из словаря (имитация CSV).",
                "import pandas as pd\n"
                "from io import StringIO\n"
                "csv_data = '''player,team,kda\n"
                "Yatoro,Spirit,4.5\n"
                "Collapse,Spirit,5.2\n"
                "Mira,GG,3.8\n"
                "Crystallis,GG,2.9\n"
                "'''\n"
                "df = pd.read_csv(StringIO(csv_data))\n"
                "print(df)\n"
                "print('Средний KDA:', df['kda'].mean())",
                "     player   team  kda\n0    Yatoro  Spirit  4.5\n1  Collapse  Spirit  5.2\n2      Mira     GG  3.8\n3  Crystallis     GG  2.9\nСредний KDA: 4.1",
                "pd.read_csv парсит текст в DataFrame. .mean() — среднее по столбцу. StringIO используем, "
                "потому что в нашей песочнице нет файловой системы."
            ),
            common_mistakes([
                {"mistake": "pd.read_csv('file.csv') с путём с пробелами", "why_bad": "Без кавычек — синтаксическая ошибка", "fix": "Кавычки + raw-string: pd.read_csv(r'C:\\my data\\file.csv')"},
                {"mistake": "df = pd.read_excel без указания листа", "why_bad": "По умолчанию первый лист, но иногда нужны другие", "fix": "sheet_name='ИмяЛиста' или sheet_name=0 (по индексу)"},
                {"mistake": "Забыл parse_dates для колонки с датами", "why_bad": "Дата станет object (строкой)", "fix": "parse_dates=['date_col'] в read_csv"},
                {"mistake": "Кодировка: кириллица в CSV выдаёт кракозябры", "why_bad": "Файл в cp1251, а Pandas ждёт utf-8", "fix": "encoding='cp1251' или encoding='utf-8-sig' для BOM"},
            ]),
            interview_questions([
                {"q": "Чем read_csv отличается от read_table?", "a": "read_csv по умолчанию sep=','; read_table — sep='\\t'. В остальном — синонимы."},
                {"q": "Что делает df.info()?", "a": "Выводит: число строк, столбцов, типы, кол-во non-null значений и использование памяти. Идеально для первого осмотра."},
                {"q": "Как прочитать JSON с вложенными объектами?", "a": "pd.json_normalize(data) — разворачивает вложенные dict'ы в плоскую таблицу."},
            ]),
            knowledge_checklist([
                "Читаю CSV через pd.read_csv()",
                "Знаю параметры sep, header, encoding",
                "Использую df.head() и df.info() для просмотра",
                "Читаю JSON через pd.read_json() / json_normalize",
                "Указываю sheet_name для Excel",
            ]),
        ],
        exercises=[
            ex(1, "python", "Создай DataFrame `df` из словаря с колонками 'player' и 'kd' (3 строки про игроков CS).",
               "import pandas as pd\n",
               "import pandas as pd\ndf = pd.DataFrame({\n    'player': ['s1mple', 'NiKo', 'ZywOo'],\n    'kd': [1.34, 1.27, 1.31]\n})",
               [{"check": "isinstance(df, pd.DataFrame)", "msg": "DataFrame"},
                {"check": "df.shape[0] == 3", "msg": "3 строки"}],
               ["pd.DataFrame({col: [values]})", "Имитация CSV в памяти"], 1),
            ex(2, "python", "Прочитай CSV-строку через StringIO, сохрани в `df`. Колонки: id, score.",
               "import pandas as pd\nfrom io import StringIO\ncsv_data = 'id,score\\n1,1500\\n2,800\\n3,2100\\n'\n",
               "import pandas as pd\nfrom io import StringIO\ncsv_data = 'id,score\\n1,1500\\n2,800\\n3,2100\\n'\ndf = pd.read_csv(StringIO(csv_data))",
               [{"check": "df.shape == (3, 2)", "msg": "(3, 2)"},
                {"check": "list(df.columns) == ['id', 'score']", "msg": "Колонки id, score"}],
               ["pd.read_csv(StringIO(data))", "from io import StringIO"], 2),
            ex(3, "python", "Дан df с колонкой score. Сохрани в `mx` максимальный score.",
               "import pandas as pd\nfrom io import StringIO\ndf = pd.read_csv(StringIO('score\\n1500\\n800\\n2100\\n'))\n",
               "import pandas as pd\nfrom io import StringIO\ndf = pd.read_csv(StringIO('score\\n1500\\n800\\n2100\\n'))\nmx = df['score'].max()",
               [{"check": "mx == 2100", "msg": "max = 2100"}],
               ["df['col'].max()", "Series.max()"], 1),
            ex(4, "python", "Дан df. Сохрани в `info_str` результат вызова df.info() (вернёт None, но мы тестируем данные).",
               "import pandas as pd\ndf = pd.DataFrame({'a':[1,2,3], 'b':[4.0,5.0,6.0]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'a':[1,2,3], 'b':[4.0,5.0,6.0]})\ninfo_str = df.info()",
               [{"check": "df.shape == (3, 2)", "msg": "Таблица 3×2"}],
               ["df.info() — для просмотра", "Возвращает None"], 2),
            ex(5, "python", "Дан df. Сохрани в `desc` результат df.describe().",
               "import pandas as pd\ndf = pd.DataFrame({'score': [100, 200, 300, 400]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'score': [100, 200, 300, 400]})\ndesc = df.describe()",
               [{"check": "isinstance(desc, pd.DataFrame)", "msg": "DataFrame"},
                {"check": "abs(desc.loc['mean', 'score'] - 250.0) < 0.5", "msg": "mean = 250"}],
               ["df.describe()", "count, mean, std, min, max, квартили"], 2),
            ex(6, "python", "Создай DataFrame из списка словарей `data` (3 строки, колонки name, team).",
               "import pandas as pd\n",
               "import pandas as pd\ndata = [\n    {'name': 's1mple', 'team': 'NAVI'},\n    {'name': 'NiKo', 'team': 'G2'},\n    {'name': 'ZywOo', 'team': 'Vitality'}\n]\ndf = pd.DataFrame(data)",
               [{"check": "df.shape[0] == 3", "msg": "3 строки"},
                {"check": "df.iloc[0]['name'] == 's1mple'", "msg": "Первая строка — s1mple"}],
               ["pd.DataFrame(list_of_dicts)", "Ключи словаря = колонки"], 2),
            ex(7, "python", "Прочитай CSV с разделителем ';'. Сохрани в `df`.",
               "import pandas as pd\nfrom io import StringIO\ncsv_data = 'name;score\\nAlice;100\\nBob;200\\n'\n",
               "import pandas as pd\nfrom io import StringIO\ncsv_data = 'name;score\\nAlice;100\\nBob;200\\n'\ndf = pd.read_csv(StringIO(csv_data), sep=';')",
               [{"check": "list(df.columns) == ['name', 'score']", "msg": "Колонки"},
                {"check": "df.shape[0] == 2", "msg": "2 строки"}],
               ["sep=';'", "Разделитель в кавычках"], 2),
            ex(8, "python", "Дан df. Сохрани в `n_cols` число столбцов.",
               "import pandas as pd\ndf = pd.DataFrame({'a':[1], 'b':[2], 'c':[3], 'd':[4]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'a':[1], 'b':[2], 'c':[3], 'd':[4]})\nn_cols = df.shape[1]",
               [{"check": "n_cols == 4", "msg": "4 столбца"}],
               ["df.shape[1] — число столбцов", "df.shape[0] — строки"], 1),
            ex(9, "python", "Прочитай JSON-строку в DataFrame `df`.",
               "import pandas as pd\njson_str = '[{\"a\": 1, \"b\": 2}, {\"a\": 3, \"b\": 4}]'\n",
               "import pandas as pd\njson_str = '[{\"a\": 1, \"b\": 2}, {\"a\": 3, \"b\": 4}]'\ndf = pd.read_json(json_str)",
               [{"check": "df.shape == (2, 2)", "msg": "(2, 2)"},
                {"check": "df['a'].sum() == 4", "msg": "sum(a) = 4"}],
               ["pd.read_json(string)", "Список словарей → таблица"], 2),
            ex(10, "python", "Дан CSV без заголовка. Прочитай, передав header=None и names=['x','y']. Сохрани в `df`.",
               "import pandas as pd\nfrom io import StringIO\ncsv_data = '1,2\\n3,4\\n5,6\\n'\n",
               "import pandas as pd\nfrom io import StringIO\ncsv_data = '1,2\\n3,4\\n5,6\\n'\ndf = pd.read_csv(StringIO(csv_data), header=None, names=['x', 'y'])",
               [{"check": "list(df.columns) == ['x', 'y']", "msg": "Колонки x, y"},
                {"check": "df.shape == (3, 2)", "msg": "(3, 2)"}],
               ["header=None", "names=[...] — задаёт имена"], 3),
        ],
        minutes=50, difficulty=2,
    )


def _3_5():
    return lesson(
        "3.5", "Фильтрация и выборка данных", "gaming", [
            theory(
                "**Выборка и фильтрация** — основа анализа данных. В Pandas три способа:\n\n"
                "**1. Выбор столбцов:** `df['col']` или `df[['c1','c2']]`\n\n"
                "**2. Выбор строк по позиции (.iloc):** `df.iloc[0:3]` — строки 0,1,2\n\n"
                "**3. Выбор строк по условию (.loc с маской):**\n"
                "```python\n"
                "df[df['score'] > 1000]\n"
                "df[(df['score'] > 1000) & (df['team'] == 'NAVI')]\n"
                "```\n\n"
                "**Полезные методы:**\n"
                "- `df.query('score > 1000')` — фильтрация через строку-условие\n"
                "- `df.isin(['NAVI', 'G2'])` — принадлежность списку\n"
                "- `df.between(100, 500)` — диапазон\n"
                "- `df.nlargest(3, 'col')` — топ-3 по столбцу"
            ),
            analogy(
                "Фильтр в Pandas — поиск в Excel по критериям, только быстрее и гибче.",
                "Выбрать игроков NAVI с KD > 1.2: `df[(df.team=='NAVI') & (df.kd > 1.2)]` — аналог расширенного фильтра Excel."
            ),
            visual(
                "Булева маска в Pandas",
                "  Исходный df:                  Маска (score > 1500):\n"
                "       name  score  team             name  score  team\n"
                "  0   Alice   1500  NAVI      0   Alice   False NAVI\n"
                "  1     Bob   1800  G2        1     Bob   True  G2   ← оставить\n"
                "  2     Eve   1200  NAVI      2     Eve   False NAVI\n"
                "  3    John   2100  G2        3    John   True  G2   ← оставить\n"
                "\n"
                "  df[df['score'] > 1500]:\n"
                "       name  score  team\n"
                "  1     Bob   1800  G2\n"
                "  3    John   2100  G2"
            ),
            example(
                "Отфильтруй игроков Dota 2: только Spirit с KDA > 4.",
                "Составное условие требует & (and) и скобки. .loc[маска, столбцы] — комбинация фильтра и выбора колонок.",
                "import pandas as pd\n"
                "df = pd.DataFrame({\n"
                "    'player': ['Yatoro', 'Collapse', 'Mira', 'Crystallis'],\n"
                "    'team': ['Spirit', 'Spirit', 'GG', 'GG'],\n"
                "    'kda': [4.5, 5.2, 3.8, 2.9]\n"
                "})\n"
                "mask = (df['team'] == 'Spirit') & (df['kda'] > 4)\n"
                "result = df[mask]\n"
                "print(result)",
                "     player    team  kda\n0    Yatoro  Spirit  4.5\n1  Collapse  Spirit  5.2",
                "Оба игрока Spirit имеют KDA > 4 (4.5 и 5.2), поэтому оба попадают в результат. "
                "Скобки вокруг каждого условия обязательны: приоритет & ниже, чем ==."
            ),
            common_mistakes([
                {"mistake": "df[df['kda'] > 4 and df['team'] == 'Spirit']", "why_bad": "and работает с одним bool, не с массивом", "fix": "Используй &: df[(df['kda']>4) & (df['team']=='Spirit')]"},
                {"mistake": "df[mask] без скобок: df[df.a > 5 & df.b < 10]", "why_bad": "Приоритет: & ниже >, выражение развалится", "fix": "Скобки: df[(df.a > 5) & (df.b < 10)]"},
                {"mistake": "df['team'] == 'NAVI' and df['score']>1000 (цепочка)", "why_bad": "Python and не работает с pandas Series", "fix": "& побитовое: (df['team']=='NAVI') & (df['score']>1000)"},
                {"mistake": "df.iloc[0, 1] = колонка не df[0, 1]", "why_bad": "df[0,1] — KeyError, неправильный синтаксис", "fix": "Для позиций: df.iloc[0, 1]"},
            ]),
            interview_questions([
                {"q": "Чем .loc отличается от .iloc?", "a": ".loc — по меткам (label-based), .iloc — по числовым позициям (integer-based). df.loc[0:3] включает 3, df.iloc[0:3] — нет."},
                {"q": "Что быстрее: df[mask] или df.query()?", "a": "query() обычно быстрее на больших данных: использует numexpr для векторизации. На маленьких — разницы нет."},
                {"q": "Как выбрать 3 строки с самым высоким score?", "a": "df.nlargest(3, 'score') — топ-3 по убыванию. df.nsmallest(3, 'score') — топ-3 по возрастанию."},
            ]),
            knowledge_checklist([
                "Фильтрую строки через df[маска]",
                "Использую &, |, ~ для составных условий",
                "Знаю разницу между .loc и .iloc",
                "Применяю df.query() и df.isin()",
                "Использую nlargest/nsmallest",
            ]),
        ],
        exercises=[
            ex(1, "python", "Дан df с колонкой score. Сохрани в `high` строки, где score > 1500.",
               "import pandas as pd\ndf = pd.DataFrame({'player': ['A','B','C','D'], 'score':[1500,1800,1200,2100]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'player': ['A','B','C','D'], 'score':[1500,1800,1200,2100]})\nhigh = df[df['score'] > 1500]",
               [{"check": "high.shape[0] == 2", "msg": "2 строки: B, D"},
                {"check": "list(high['player']) == ['B', 'D']", "msg": "B, D"}],
               ["df[df['col'] > x]", "Возвращает DataFrame"], 1),
            ex(2, "python", "Дан df с колонками team, kd. Сохрани в `navi` строки, где team == 'NAVI'.",
               "import pandas as pd\ndf = pd.DataFrame({'player':['s1mple','NiKo'],'team':['NAVI','G2'],'kd':[1.34,1.27]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'player':['s1mple','NiKo'],'team':['NAVI','G2'],'kd':[1.34,1.27]})\nnavi = df[df['team'] == 'NAVI']",
               [{"check": "navi.shape[0] == 1", "msg": "1 строка"},
                {"check": "navi.iloc[0]['player'] == 's1mple'", "msg": "s1mple"}],
               ["df['col'] == 'value'", "Строки в кавычках"], 1),
            ex(3, "python", "Дан df. Сохрани в `top3` три строки с наибольшим score через nlargest.",
               "import pandas as pd\ndf = pd.DataFrame({'p':['A','B','C','D','E'], 'score':[100,500,300,800,200]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'p':['A','B','C','D','E'], 'score':[100,500,300,800,200]})\ntop3 = df.nlargest(3, 'score')",
               [{"check": "list(top3['p']) == ['D', 'B', 'C']", "msg": "D, B, C по убыванию"}],
               ["df.nlargest(n, 'col')", "Топ-N по убыванию"], 2),
            ex(4, "python", "Дан df. Сохрани в `result` строки с kd от 1.2 до 1.3 (включительно).",
               "import pandas as pd\ndf = pd.DataFrame({'player':['A','B','C','D'],'kd':[1.10,1.25,1.30,1.40]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'player':['A','B','C','D'],'kd':[1.10,1.25,1.30,1.40]})\nresult = df[df['kd'].between(1.2, 1.3)]",
               [{"check": "result.shape[0] == 2", "msg": "2 строки: B, C"},
                {"check": "list(result['player']) == ['B', 'C']", "msg": "B, C"}],
               [".between(a, b)", "Включительно с обеих сторон"], 2),
            ex(5, "python", "Дан df. Сохрани в `top2` через .iloc первые 2 строки.",
               "import pandas as pd\ndf = pd.DataFrame({'x':[10,20,30,40]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'x':[10,20,30,40]})\ntop2 = df.iloc[:2]",
               [{"check": "top2.shape[0] == 2", "msg": "2 строки"},
                {"check": "list(top2['x']) == [10, 20]", "msg": "[10, 20]"}],
               [".iloc[:n]", "По позициям"], 1),
            ex(6, "python", "Дан df. Сохрани в `good` строки, где team в ['NAVI','G2'].",
               "import pandas as pd\ndf = pd.DataFrame({'player':['A','B','C','D'],'team':['NAVI','G2','FaZe','NAVI']})\n",
               "import pandas as pd\ndf = pd.DataFrame({'player':['A','B','C','D'],'team':['NAVI','G2','FaZe','NAVI']})\ngood = df[df['team'].isin(['NAVI', 'G2'])]",
               [{"check": "good.shape[0] == 3", "msg": "3 строки"},
                {"check": "'FaZe' not in list(good['team'])", "msg": "FaZe отфильтрован"}],
               [".isin([list])", "isin принимает список"], 2),
            ex(7, "python", "Дан df. Используя query, сохрани в `q` строки с score >= 200.",
               "import pandas as pd\ndf = pd.DataFrame({'p':['A','B','C'],'score':[100,250,500]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'p':['A','B','C'],'score':[100,250,500]})\nq = df.query('score >= 200')",
               [{"check": "q.shape[0] == 2", "msg": "2 строки"},
                {"check": "list(q['p']) == ['B', 'C']", "msg": "B, C"}],
               ["df.query('cond')", "Строка-условие"], 2),
            ex(8, "python", "Дан df. Сохрани в `loc_result` строки, где score > 100, и колонки ['name','score'].",
               "import pandas as pd\ndf = pd.DataFrame({'name':['A','B','C'],'score':[50,200,500],'team':['X','Y','Z']})\n",
               "import pandas as pd\ndf = pd.DataFrame({'name':['A','B','C'],'score':[50,200,500],'team':['X','Y','Z']})\nloc_result = df.loc[df['score'] > 100, ['name', 'score']]",
               [{"check": "list(loc_result.columns) == ['name', 'score']", "msg": "Колонки name, score"},
                {"check": "loc_result.shape[0] == 2", "msg": "2 строки"}],
               [".loc[mask, [cols]]", "Фильтр + выбор колонок"], 3),
            ex(9, "python", "Дан df. Сохрани в `negate` строки, где team НЕ равен 'G2'.",
               "import pandas as pd\ndf = pd.DataFrame({'player':['A','B','C'],'team':['NAVI','G2','FaZe']})\n",
               "import pandas as pd\ndf = pd.DataFrame({'player':['A','B','C'],'team':['NAVI','G2','FaZe']})\nnegate = df[df['team'] != 'G2']",
               [{"check": "negate.shape[0] == 2", "msg": "2 строки"},
                {"check": "'G2' not in list(negate['team'])", "msg": "G2 нет"}],
               ["!= для не равно", "Или ~df['team'].eq('G2')"], 2),
            ex(10, "python", "Дан df. Сохрани в `bottom2` две строки с наименьшим score.",
               "import pandas as pd\ndf = pd.DataFrame({'p':['A','B','C','D'],'score':[100,500,300,800]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'p':['A','B','C','D'],'score':[100,500,300,800]})\nbottom2 = df.nsmallest(2, 'score')",
               [{"check": "list(bottom2['p']) == ['A', 'C']", "msg": "A, C по возрастанию"}],
               ["df.nsmallest(n, col)", "Топ-N по возрастанию"], 2),
        ],
        minutes=55, difficulty=3,
    )


def _3_6():
    return lesson(
        "3.6", "Очистка данных: пропуски", "space", [
            theory(
                "В реальных данных **пропуски (NaN)** встречаются повсюду. В Pandas они обозначаются `NaN` "
                "(Not a Number) и принадлежат типу `float`.\n\n"
                "**Обнаружение:**\n"
                "- `df.isna()` / `df.isnull()` — bool-маска NaN\n"
                "- `df.isna().sum()` — кол-во NaN по столбцам\n"
                "- `df.isna().any()` — есть ли хоть один NaN в каждом столбце\n\n"
                "**Стратегии обработки:**\n"
                "1. **Удаление:** `df.dropna()` — выкидывает строки с NaN. "
                "`df.dropna(subset=['col'])` — только по конкретной колонке.\n"
                "2. **Заполнение:** `df.fillna(value)`, `df.fillna(df.mean())`, `df.fillna(method='ffill')` — предыдущим значением.\n"
                "3. **Интерполяция:** `df.interpolate()` — для числовых временных рядов.\n\n"
                "**Правило:** удалять опасно (теряем данные), заполнять — осторожно (искажаем статистику)."
            ),
            analogy(
                "Пропуск в данных — пустая ячейка в анкете: можно выкинуть всю анкету, можно подставить среднее по остальным, "
                "а можно списать с соседней (forward fill).",
                "В таблице запусков ракет иногда отсутствует масса полезной нагрузки: можно заполнить медианой по типу ракеты."
            ),
            visual(
                "Стратегии работы с NaN",
                "  Исходно:                 dropna()            fillna(0):         fillna(mean):\n"
                "  ┌───┬────┬─────┐         ┌───┬────┬─────┐    ┌───┬────┬─────┐    ┌───┬────┬─────┐\n"
                "  │ x │ y  │ z   │         │ x │ y  │ z   │    │ x │ y  │ z   │    │ x │ y  │ z   │\n"
                "  ├───┼────┼─────┤         ├───┼────┼─────┤    ├───┼────┼─────┤    ├───┼────┼─────┤\n"
                "  │ 1 │NaN │ 100 │         │ 2 │ 20 │ NaN │    │ 1 │  0 │ 100 │    │ 1 │ 13 │ 100 │\n"
                "  │ 2 │ 20 │ NaN │         │ 4 │NaN │ 200 │    │ 2 │ 20 │   0 │    │ 2 │ 20 │ 200 │\n"
                "  │ 3 │ 10 │ 300 │         └───────────────┘    │ 3 │ 10 │ 300 │    │ 3 │ 10 │ 300 │\n"
                "  │ 4 │NaN │ 200 │                                │ 4 │  0 │ 200 │    │ 4 │ 13 │ 200 │\n"
                "  └───┴────┴─────┘         удалена строка 2      замена на 0         mean(y)=13"
            ),
            example(
                "В данных о запусках ракет есть пропуски в payload_kg. Посчитай их, заполни медианой.",
                "isna().sum() даёт счётчик по столбцам. median() не учитывает NaN. fillna заменяет NaN на указанное значение.",
                "import pandas as pd\n"
                "import numpy as np\n"
                "df = pd.DataFrame({\n"
                "    'mission': ['A', 'B', 'C', 'D', 'E'],\n"
                "    'payload_kg': [12000, np.nan, 15400, np.nan, 9000]\n"
                "})\n"
                "print('Пропуски:')\n"
                "print(df.isna().sum())\n"
                "median_payload = df['payload_kg'].median()\n"
                "df['payload_kg'] = df['payload_kg'].fillna(median_payload)\n"
                "print('После заполнения:')\n"
                "print(df)",
                "Пропуски:\nmission       0\npayload_kg    2\ndtype: int64\nПосле заполнения:\n  mission  payload_kg\n0       A     12000.0\n1       B     12000.0\n2       C     15400.0\n3       D     12000.0\n4       E      9000.0",
                "median по [12000, 15400, 9000] ≈ 12000. fillna заменяет NaN на 12000."
            ),
            common_mistakes([
                {"mistake": "df.fillna(0) для строковых колонок", "why_bad": "Число 0 в строках может не иметь смысла", "fix": "Заполняй осмысленным значением: df['col'].fillna('Unknown')"},
                {"mistake": "df.dropna() без раздумий", "why_bad": "Теряем данные: если 30% строк с одним пропуском — это критично", "fix": "Сначала посмотри df.isna().sum(), реши, можно ли заполнить"},
                {"mistake": "df.fillna(df.mean()) для категориальных", "why_bad": "Среднее по строкам — бессмысленно", "fix": "Для категорий используй mode() (мода) или отдельное значение"},
                {"mistake": "df == None вместо df.isna()", "why_bad": "None в Pandas превращается в NaN, но == ищет точное None", "fix": "Используй isna() / isnull() для поиска пропусков"},
            ]),
            interview_questions([
                {"q": "В чём разница между None, NaN и NA в Pandas?", "a": "None — Python-объект, в числовых колонках превращается в NaN. NaN — float из numpy. NA — общий пропущенный (pandas 1.0+)."},
                {"q": "Когда fillna(mean) — плохая идея?", "a": "1) Для категориальных признаков. 2) При сильно скошенном распределении (медиана лучше). 3) Если пропуски не случайны (MCAR)."},
                {"q": "Что делает ffill?", "a": "Forward fill: заменяет NaN на предыдущее известное значение. Удобно для временных рядов, где данные непрерывны."},
            ]),
            knowledge_checklist([
                "Обнаруживаю пропуски через isna().sum()",
                "Удаляю строки с NaN через dropna()",
                "Заполняю NaN через fillna(mean/median/mode)",
                "Использую ffill/bfill для временных рядов",
                "Понимаю, когда заполнение искажает данные",
            ]),
        ],
        exercises=[
            ex(1, "python", "Создай DataFrame с одним NaN в колонке 'score'. Сохрани в `cnt` кол-во NaN.",
               "import pandas as pd\nimport numpy as np\n",
               "import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({'player':['A','B','C'],'score':[100, np.nan, 200]})\ncnt = df.isna().sum().sum()",
               [{"check": "isinstance(df, pd.DataFrame)", "msg": "DataFrame"},
                {"check": "cnt == 1", "msg": "1 NaN"}],
               ["np.nan", "isna().sum().sum() — общее число"], 1),
            ex(2, "python", "Дан df с NaN. Заполни NaN в колонке score нулём. Сохрани в `df_filled`.",
               "import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({'score':[10, np.nan, 30]})\n",
               "import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({'score':[10, np.nan, 30]})\ndf_filled = df.fillna(0)",
               [{"check": "df_filled['score'].isna().sum() == 0", "msg": "Нет NaN"},
                {"check": "df_filled['score'].sum() == 40", "msg": "10+0+30 = 40"}],
               ["df.fillna(value)", "inplace=False по умолчанию"], 1),
            ex(3, "python", "Дан df. Удали все строки с хотя бы одним NaN. Сохрани в `clean`.",
               "import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({'a':[1, np.nan, 3], 'b':[4, 5, 6]})\n",
               "import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({'a':[1, np.nan, 3], 'b':[4, 5, 6]})\nclean = df.dropna()",
               [{"check": "clean.shape[0] == 2", "msg": "2 строки"},
                {"check": "clean['a'].isna().sum() == 0", "msg": "Нет NaN"}],
               ["df.dropna()", "По умолчанию axis=0 (строки)"], 2),
            ex(4, "python", "Дан df. Заполни NaN в 'score' средним значением. Сохрани в `df_mean`.",
               "import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({'score':[10, np.nan, 20, np.nan, 30]})\n",
               "import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({'score':[10, np.nan, 20, np.nan, 30]})\nmean_val = df['score'].mean()\ndf_mean = df.fillna({'score': mean_val})",
               [{"check": "df_mean['score'].isna().sum() == 0", "msg": "Нет NaN"},
                {"check": "abs(df_mean['score'].mean() - 20.0) < 0.5", "msg": "Среднее ≈ 20"}],
               ["df['col'].mean()", "fillna с dict по колонкам"], 3),
            ex(5, "python", "Дан df. Заполни NaN предыдущим значением (ffill). Сохрани в `df_ffill`.",
               "import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({'x':[1, np.nan, np.nan, 4, np.nan]})\n",
               "import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({'x':[1, np.nan, np.nan, 4, np.nan]})\ndf_ffill = df.ffill()",
               [{"check": "list(df_ffill['x']) == [1, 1, 1, 4, 4]", "msg": "ffill заменил"}],
               ["df.ffill()", "Или fillna(method='ffill')"], 2),
            ex(6, "python", "Дан df. Сохрани в `nan_score` — кол-во NaN именно в колонке score.",
               "import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({'name':['A',None,'C'],'score':[10, np.nan, np.nan]})\n",
               "import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({'name':['A',None,'C'],'score':[10, np.nan, np.nan]})\nnan_score = df['score'].isna().sum()",
               [{"check": "nan_score == 2", "msg": "2 NaN в score"}],
               ["df['col'].isna().sum()", "Только одна колонка"], 2),
            ex(7, "python", "Дан df. Удали только строки, где NaN в колонке 'score'. Сохрани в `df_clean`.",
               "import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({'name':['A','B','C','D'],'score':[10, np.nan, 30, 40]})\n",
               "import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({'name':['A','B','C','D'],'score':[10, np.nan, 30, 40]})\ndf_clean = df.dropna(subset=['score'])",
               [{"check": "df_clean.shape[0] == 3", "msg": "3 строки"}],
               ["dropna(subset=[col])", "Только по указанной колонке"], 2),
            ex(8, "python", "Дан df. Заполни NaN в 'score' медианой. Сохрани в `df_med`.",
               "import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({'score':[10, np.nan, 30, 40]})\n",
               "import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({'score':[10, np.nan, 30, 40]})\nmed = df['score'].median()\ndf_med = df.fillna(med)",
               [{"check": "df_med.loc[1, 'score'] == 30", "msg": "median(10,30,40) = 30"}],
               [".median()", "Устойчива к выбросам"], 3),
            ex(9, "python", "Дан df. Сохрани в `has_nan` — True/False, есть ли хоть один NaN во всей таблице.",
               "import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({'a':[1,2],'b':[3, np.nan]})\n",
               "import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({'a':[1,2],'b':[3, np.nan]})\nhas_nan = df.isna().any().any()",
               [{"check": "has_nan is True", "msg": "Есть NaN"}],
               [".isna().any()", "Двойной any: по столбцам и по всей таблице"], 2),
            ex(10, "python", "Дан df. Замени NaN на 0 только в числовых колонках. Сохрани в `df_zero`.",
               "import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({'x':[1, np.nan, 3], 'name':['a', None, 'c']})\n",
               "import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({'x':[1, np.nan, 3], 'name':['a', None, 'c']})\ndf_zero = df.fillna({'x': 0, 'name': 'unknown'})",
               [{"check": "df_zero.loc[1, 'x'] == 0", "msg": "x заменён на 0"},
                {"check": "df_zero.loc[1, 'name'] == 'unknown'", "msg": "name → unknown"}],
               ["fillna({col: value})", "Словарь замен"], 3),
        ],
        minutes=55, difficulty=3,
    )


def _3_7():
    return lesson(
        "3.7", "Очистка данных: дубликаты и выбросы", "gaming", [
            theory(
                "**Дубликаты** — повторяющиеся строки, часто из-за сбоев импорта или склейки источников.\n\n"
                "**Обнаружение и удаление:**\n"
                "- `df.duplicated()` — bool-маска дубликатов (первое вхождение = False)\n"
                "- `df.drop_duplicates()` — удалить дубликаты\n"
                "- `df.drop_duplicates(subset=['col'])` — уникальные по колонке (например, по player_id)\n\n"
                "**Выбросы (outliers)** — аномально большие/маленькие значения, которые сдвигают статистику.\n\n"
                "**Методы обнаружения:**\n"
                "1. **IQR-метод:** всё, что вне `[Q1 - 1.5*IQR, Q3 + 1.5*IQR]` — выброс.\n"
                "2. **Z-score:** |z| > 3 — выброс (для нормального распределения).\n"
                "3. **Доменный:** значение вне здравого смысла (KD = 99.9 — явно аномалия).\n\n"
                "**Действия:** удалить, заменить граничными значениями (clip), пометить флагом."
            ),
            analogy(
                "Дубликат — две одинаковые фотографии в галерее, оставляешь одну. "
                "Выброс — зарплата CEO среди обычных сотрудников: статистику по среднему она портит, лучше убрать или пометить.",
                "В таблице матчей Dota: одна и та же игра записана дважды (дубликат) или "
                "KD = 999 из-за бага (выброс)."
            ),
            visual(
                "IQR-метод: ящик с усами (boxplot)",
                "  ┌─────┐                      * — выброс\n"
                "  │ ─── │  ─── Q3 (75%)        выброс > Q3 + 1.5*IQR\n"
                "  │█████│                      выброс < Q1 - 1.5*IQR\n"
                "  │ ─── │  ─── медиана (Q2)   IQR = Q3 - Q1\n"
                "  │█████│\n"
                "  │ ─── │  ─── Q1 (25%)\n"
                "  └─────┘\n"
                "      ──┼──┼──┼──┼──┼──┼──┼──*\n"
                "     Q1  │  │  │  Q3     выброс\n"
                "\n"
                "  Пример: [1,2,3,4,5,6,7,8,9,100]\n"
                "  100 — выброс (> Q3+1.5*IQR)"
            ),
            example(
                "Удали дубликаты из данных о матчах и найди выбросы в KDA через IQR.",
                "duplicated() находит повторы. drop_duplicates() удаляет. "
                "Квантили Q1/Q3 и IQR позволяют найти выбросы.",
                "import pandas as pd\n"
                "df = pd.DataFrame({\n"
                "    'match_id': [1, 2, 2, 3, 4, 4, 5],\n"
                "    'kda': [3.5, 4.1, 4.1, 5.0, 99.9, 4.5, 2.8]\n"
                "})\n"
                "print('Дубликатов:', df.duplicated().sum())\n"
                "df_unique = df.drop_duplicates()\n"
                "Q1 = df_unique['kda'].quantile(0.25)\n"
                "Q3 = df_unique['kda'].quantile(0.75)\n"
                "IQR = Q3 - Q1\n"
                "lower, upper = Q1 - 1.5*IQR, Q3 + 1.5*IQR\n"
                "outliers = df_unique[(df_unique['kda'] < lower) | (df_unique['kda'] > upper)]\n"
                "print('Выбросы KDA:')\n"
                "print(outliers)",
                "Дубликатов: 1\nВыбросы KDA:\n   match_id   kda\n4         4  99.9",
                "Один полный дубликат (id=2) удалён. KDA=99.9 — выброс по IQR. "
                "В таблице 5 строк после удаления дубля, Q1≈3.5, Q3≈4.5, IQR≈1, верхняя граница ≈ 6."
            ),
            common_mistakes([
                {"mistake": "df.drop_duplicates() без subset для ID", "why_bad": "Удалит нужные строки с одинаковыми полями, но разными ID", "fix": "df.drop_duplicates(subset=['user_id'], keep='last')"},
                {"mistake": "Удалять все выбросы подряд", "why_bad": "Иногда выброс — это сигнал (например, фрод-транзакция), а не шум", "fix": "Сначала разберись, потом удаляй или заменяй"},
                {"mistake": "Использовать .mean() для данных с выбросами", "why_bad": "Среднее сильно сдвигается", "fix": "median() или trim_mean() из scipy"},
                {"mistake": "IQR для маленьких выборок (n<10)", "why_bad": "Квантили нестабильны, выбросы определяются шумом", "fix": "На малых данных — визуальный анализ или доменные правила"},
            ]),
            interview_questions([
                {"q": "Что делает keep='first' в drop_duplicates?", "a": "Оставляет первое вхождение дубликата, остальные удаляет. По умолчанию. Альтернативы: keep='last', keep=False (удалить все)."},
                {"q": "Чем выброс отличается от аномалии?", "a": "Выброс — статистический термин (далеко от центра распределения). Аномалия — доменное понятие (не соответствует логике процесса). Все выбросы — аномалии, но не все аномалии — выбросы."},
                {"q": "Как обработать выбросы?", "a": "1) Удалить (если выброс = ошибка). 2) Заменить границами (clip). 3) Логарифмировать. 4) Использовать робастные методы (медиана вместо среднего)."},
            ]),
            knowledge_checklist([
                "Нахожу дубликаты через df.duplicated()",
                "Удаляю дубликаты через df.drop_duplicates()",
                "Понимаю IQR-метод для выбросов",
                "Использую df.clip() для ограничения значений",
                "Отличаю статистический выброс от доменной аномалии",
            ]),
        ],
        exercises=[
            ex(1, "python", "Создай df с дубликатом строки. Сохрани в `dups` кол-во дубликатов.",
               "import pandas as pd\n",
               "import pandas as pd\ndf = pd.DataFrame({'a':[1,2,1], 'b':[3,4,3]})\ndups = df.duplicated().sum()",
               [{"check": "dups == 1", "msg": "1 дубликат"}],
               ["df.duplicated()", ".sum() считает True"], 1),
            ex(2, "python", "Дан df. Удали дубликаты, сохрани в `unique_df`.",
               "import pandas as pd\ndf = pd.DataFrame({'a':[1,1,2,2], 'b':[3,3,4,4]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'a':[1,1,2,2], 'b':[3,3,4,4]})\nunique_df = df.drop_duplicates()",
               [{"check": "unique_df.shape[0] == 2", "msg": "2 уникальные"},
                {"check": "unique_df.duplicated().sum() == 0", "msg": "Нет дубликатов"}],
               ["df.drop_duplicates()", "Оставляет первое вхождение"], 1),
            ex(3, "python", "Дан df. Удали дубликаты только по колонке 'player_id', оставь последнее. Сохрани в `result`.",
               "import pandas as pd\ndf = pd.DataFrame({'player_id':[1,1,2,2,3], 'score':[100,150,200,250,300]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'player_id':[1,1,2,2,3], 'score':[100,150,200,250,300]})\nresult = df.drop_duplicates(subset=['player_id'], keep='last')",
               [{"check": "result.shape[0] == 3", "msg": "3 игрока"},
                {"check": "result.iloc[0]['score'] == 150", "msg": "Оставлен последний (150)"}],
               ["subset=[col]", "keep='last'"], 3),
            ex(4, "python", "Дан df. Найди кол-во выбросов в 'score' через IQR (Q3 + 1.5*IQR).",
               "import pandas as pd\ndf = pd.DataFrame({'score':[10, 12, 11, 13, 12, 100, 14, 11]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'score':[10, 12, 11, 13, 12, 100, 14, 11]})\nQ1 = df['score'].quantile(0.25)\nQ3 = df['score'].quantile(0.75)\nIQR = Q3 - Q1\nupper = Q3 + 1.5 * IQR\nn_out = (df['score'] > upper).sum()",
               [{"check": "n_out == 1", "msg": "1 выброс: 100"}],
               [".quantile(0.25/0.75)", "IQR = Q3 - Q1"], 3),
            ex(5, "python", "Дан df. Замени значения score > 100 на 100 (clip). Сохрани в `clipped`.",
               "import pandas as pd\ndf = pd.DataFrame({'score':[50, 200, 80, 500, 90]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'score':[50, 200, 80, 500, 90]})\nclipped = df.copy()\nclipped['score'] = clipped['score'].clip(upper=100)",
               [{"check": "clipped['score'].max() == 100", "msg": "max = 100"},
                {"check": "clipped['score'].sum() == 50+100+80+100+90", "msg": "Сумма 420"}],
               [".clip(upper=...)", "Или np.clip"], 2),
            ex(6, "python", "Дан df. Удали дубликаты, оставив только False-дубликаты (не удаляя первое вхождение). Реально это невозможно, поэтому просто удали все дубликаты (keep=False). Сохрани в `no_dups`.",
               "import pandas as pd\ndf = pd.DataFrame({'a':[1,1,2,2,3]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'a':[1,1,2,2,3]})\nno_dups = df.drop_duplicates(keep=False)",
               [{"check": "no_dups.shape[0] == 1", "msg": "Только 3"},
                {"check": "list(no_dups['a']) == [3]", "msg": "[3]"}],
               ["keep=False", "Удаляет все вхождения дублей"], 3),
            ex(7, "python", "Дан df. Найди и сохрани в `outliers` строки, где score > Q3 + 1.5*IQR.",
               "import pandas as pd\ndf = pd.DataFrame({'x':[1,2,3,4,5,6,7,8,9,100]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'x':[1,2,3,4,5,6,7,8,9,100]})\nQ1 = df['x'].quantile(0.25)\nQ3 = df['x'].quantile(0.75)\nIQR = Q3 - Q1\noutliers = df[df['x'] > Q3 + 1.5 * IQR]",
               [{"check": "outliers.shape[0] == 1", "msg": "1 выброс"},
                {"check": "outliers.iloc[0]['x'] == 100", "msg": "100 — выброс"}],
               ["Q3 + 1.5*IQR", "Маска по условию"], 3),
            ex(8, "python", "Дан df. Сколько строк — точные дубликаты? Сохрани в `exact_dups`.",
               "import pandas as pd\ndf = pd.DataFrame({'a':[1,2,1,2,1], 'b':[10,20,10,20,10]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'a':[1,2,1,2,1], 'b':[10,20,10,20,10]})\nexact_dups = df.duplicated().sum()",
               [{"check": "exact_dups == 2", "msg": "2 дубликата"}],
               ["df.duplicated()", "True для повторов, кроме первого"], 1),
            ex(9, "python", "Дан df. Создай колонку 'is_outlier' (True/False): True, если score > 100 или score < 0.",
               "import pandas as pd\ndf = pd.DataFrame({'score':[10, 200, -5, 50, 150]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'score':[10, 200, -5, 50, 150]})\ndf['is_outlier'] = (df['score'] > 100) | (df['score'] < 0)",
               [{"check": "'is_outlier' in df.columns", "msg": "Колонка создана"},
                {"check": "df['is_outlier'].sum() == 3", "msg": "3 выброса: 200, -5, 150"}],
               ["Логическая маска", "| для OR"], 3),
            ex(10, "python", "Дан df с дубликатами. Удали полные дубликаты и замени выбросы (>200) на 200. Сохрани в `clean`.",
               "import pandas as pd\ndf = pd.DataFrame({'score':[100, 100, 500, 50, 200, 999]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'score':[100, 100, 500, 50, 200, 999]})\nclean = df.drop_duplicates().copy()\nclean['score'] = clean['score'].clip(upper=200)",
               [{"check": "clean.shape[0] == 4", "msg": "После удаления дублей 4 строки"},
                {"check": "clean['score'].max() == 200", "msg": "max = 200"}],
               ["drop_duplicates()", ".clip(upper=200)"], 3),
        ],
        minutes=55, difficulty=3,
    )


def _3_8():
    return lesson(
        "3.8", "Агрегации и groupby", "gaming", [
            theory(
                "**Агрегации** — сжатие данных: сумма, среднее, минимум, максимум, медиана, count, nunique.\n\n"
                "**Базовые методы Series:**\n"
                "```python\n"
                "df['score'].sum()\n"
                "df['score'].mean()\n"
                "df['score'].median()\n"
                "df['score'].std()      # стандартное отклонение\n"
                "df['score'].value_counts()  # частота значений\n"
                "df['team'].nunique()        # кол-во уникальных\n"
                "```\n\n"
                "**groupby — Split-Apply-Combine:**\n"
                "```python\n"
                "df.groupby('team')['score'].mean()\n"
                "df.groupby('team').agg({'score': 'mean', 'kd': 'max'})\n"
                "```\n\n"
                "**agg()** позволяет применить несколько функций:\n"
                "```python\n"
                "df.groupby('team')['score'].agg(['mean', 'median', 'count'])\n"
                "```\n\n"
                "**transform()** возвращает серию той же длины (например, среднее по группе для каждой строки)."
            ),
            analogy(
                "groupby — группировка в Excel по категории с агрегатной функцией (SUMIF, AVERAGEIF). Только в Pandas мощнее.",
                "Средний KD по командам в Dota 2: одна строка groupby — и получаешь таблицу с метриками по каждой команде."
            ),
            visual(
                "Split-Apply-Combine на groupby",
                "  Исходно:                Split (group):         Apply+Combine:\n"
                "  player   team  kd       team=NAVI  kd          team   mean_kd\n"
                "  s1mple   NAVI  1.34     ─────────  ───          ─────  ───────\n"
                "  NiKo     G2    1.27     s1mple    1.34         NAVI   1.34\n"
                "  ZywOo    Vital 1.31     b1t       1.25         G2     1.27\n"
                "  b1t      NAVI  1.25                         Vitality 1.31\n"
                "\n"
                "  df.groupby('team')['kd'].mean()\n"
                "\n"
                "  agg() — несколько функций сразу:\n"
                "  df.groupby('team').agg(mean_kd=('kd', 'mean'), n=('kd', 'count'))"
            ),
            example(
                "Посчитай суммарный и средний score по командам в Dota 2.",
                "groupby('team') группирует. ['score'] выбирает столбец. .agg() применяет функции. "
                "В agg удобно именовать колонки.",
                "import pandas as pd\n"
                "df = pd.DataFrame({\n"
                "    'player': ['Yatoro', 'Collapse', 'Mira', 'Crystallis', 'skiter'],\n"
                "    'team': ['Spirit', 'Spirit', 'GG', 'GG', 'Tundra'],\n"
                "    'score': [4500, 5200, 3800, 2900, 4100]\n"
                "})\n"
                "result = df.groupby('team')['score'].agg(['sum', 'mean', 'count'])\n"
                "print(result)",
                "         sum    mean  count\nteam\nGG      6700  3350.0      2\nSpirit  9700  4850.0      2\nTundra  4100  4100.0      1",
                "agg(['sum', 'mean', 'count']) применил три функции за раз. Spirit и GG — по 2 игрока, Tundra — 1."
            ),
            common_mistakes([
                {"mistake": "df.groupby('team').mean() для всего DataFrame", "why_bad": "Усреднит все числовые колонки, даже ненужные (год рождения и т.п.)", "fix": "Выбирай столбец: df.groupby('team')['score'].mean()"},
                {"mistake": "Группировка по колонке с NaN", "why_bad": "NaN-строки образуют отдельную группу, легко забыть", "fix": "dropna перед groupby или fillna категориальной меткой"},
                {"mistake": "df.groupby('team').sum() при наличии строковых колонок", "why_bad": "TypeError или склейка строк через sum", "fix": "Выбирай числовые: df.groupby('team')[['score', 'kd']].sum()"},
                {"mistake": "agg без указания функций — agg()", "why_bad": "Возвращает пустой результат", "fix": "Указывай функции: agg(['mean']) или agg({'col': 'mean'})"},
            ]),
            interview_questions([
                {"q": "Что делает groupby без агрегации?", "a": "Возвращает DataFrameGroupBy — 'ленивый' объект. Без .agg()/.sum()/.mean() он просто ждёт применения функции."},
                {"q": "Чем transform отличается от agg?", "a": "agg возвращает одну строку на группу (n_groups строк). transform возвращает серию той же длины, что и исходный df."},
                {"q": "Как сделать несколько агрегаций сразу?", "a": "agg(dict) — {'col1': ['mean', 'max'], 'col2': 'sum'}. Или в новом синтаксисе: agg(mean_x=('x', 'mean'), max_y=('y', 'max'))."},
            ]),
            knowledge_checklist([
                "Использую sum, mean, median, std, count, nunique",
                "Группирую через groupby",
                "Применяю agg() для нескольких функций",
                "Использую value_counts() для частот",
                "Понимаю Split-Apply-Combine",
            ]),
        ],
        exercises=[
            ex(1, "python", "Дан df с колонкой score. Сохрани в `s` сумму всех score.",
               "import pandas as pd\ndf = pd.DataFrame({'score':[100, 200, 300, 400]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'score':[100, 200, 300, 400]})\ns = df['score'].sum()",
               [{"check": "s == 1000", "msg": "Сумма = 1000"}],
               [".sum()", "Series.sum()"], 1),
            ex(2, "python", "Дан df. Сохрани в `m` среднее score.",
               "import pandas as pd\ndf = pd.DataFrame({'score':[10, 20, 30]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'score':[10, 20, 30]})\nm = df['score'].mean()",
               [{"check": "abs(m - 20.0) < 0.01", "msg": "Среднее = 20"}],
               [".mean()", "Игнорирует NaN"], 1),
            ex(3, "python", "Дан df с колонками team, score. Сохрани в `team_sum` Series: сумма score по командам.",
               "import pandas as pd\ndf = pd.DataFrame({'team':['A','A','B','B'],'score':[10,20,30,40]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'team':['A','A','B','B'],'score':[10,20,30,40]})\nteam_sum = df.groupby('team')['score'].sum()",
               [{"check": "team_sum['A'] == 30", "msg": "A = 30"},
                {"check": "team_sum['B'] == 70", "msg": "B = 70"}],
               ["groupby('col')", ".sum()"], 2),
            ex(4, "python", "Дан df. Сохрани в `team_mean` Series: средний score по командам.",
               "import pandas as pd\ndf = pd.DataFrame({'team':['A','A','B'],'score':[10,20,30]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'team':['A','A','B'],'score':[10,20,30]})\nteam_mean = df.groupby('team')['score'].mean()",
               [{"check": "abs(team_mean['A'] - 15.0) < 0.01", "msg": "A = 15"},
                {"check": "team_mean['B'] == 30", "msg": "B = 30"}],
               ["groupby", ".mean()"], 2),
            ex(5, "python", "Дан df. Сохрани в `counts` Series: сколько раз встречается каждый team.",
               "import pandas as pd\ndf = pd.DataFrame({'team':['A','A','A','B','B']})\n",
               "import pandas as pd\ndf = pd.DataFrame({'team':['A','A','A','B','B']})\ncounts = df['team'].value_counts()",
               [{"check": "counts['A'] == 3", "msg": "A — 3 раза"},
                {"check": "counts['B'] == 2", "msg": "B — 2 раза"}],
               [".value_counts()", "Удобно для частот"], 1),
            ex(6, "python", "Дан df. Сохрани в `agg_df` DataFrame: среднее и максимум score по командам (agg).",
               "import pandas as pd\ndf = pd.DataFrame({'team':['A','A','B','B'],'score':[10,20,30,40]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'team':['A','A','B','B'],'score':[10,20,30,40]})\nagg_df = df.groupby('team')['score'].agg(['mean', 'max'])",
               [{"check": "list(agg_df.columns) == ['mean', 'max']", "msg": "Колонки mean, max"},
                {"check": "agg_df.loc['A', 'mean'] == 15", "msg": "A mean = 15"}],
               [".agg([list])", "Несколько функций"], 3),
            ex(7, "python", "Дан df. Сохрани в `n_teams` кол-во уникальных команд.",
               "import pandas as pd\ndf = pd.DataFrame({'team':['A','B','A','C','B','A']})\n",
               "import pandas as pd\ndf = pd.DataFrame({'team':['A','B','A','C','B','A']})\nn_teams = df['team'].nunique()",
               [{"check": "n_teams == 3", "msg": "3 уникальные"}],
               [".nunique()", "Число уникальных"], 1),
            ex(8, "python", "Дан df. Сохрани в `med` Series: медиана score по командам.",
               "import pandas as pd\ndf = pd.DataFrame({'team':['A','A','A','B','B'],'score':[10,20,30,40,50]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'team':['A','A','A','B','B'],'score':[10,20,30,40,50]})\nmed = df.groupby('team')['score'].median()",
               [{"check": "med['A'] == 20", "msg": "A median = 20"},
                {"check": "med['B'] == 45", "msg": "B median = 45"}],
               [".median()", "Устойчива к выбросам"], 2),
            ex(9, "python", "Дан df. Сохрани в `multi` DataFrame: для каждой команды — sum и count score.",
               "import pandas as pd\ndf = pd.DataFrame({'team':['A','B','A','B'],'score':[10,20,30,40]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'team':['A','B','A','B'],'score':[10,20,30,40]})\nmulti = df.groupby('team')['score'].agg(total='sum', n='count')",
               [{"check": "list(multi.columns) == ['total', 'n']", "msg": "Колонки total, n"},
                {"check": "multi.loc['A', 'total'] == 40", "msg": "A total = 40"}],
               ["agg(name=('col', 'func'))", "Новый синтаксис"], 3),
            ex(10, "python", "Дан df. Сгруппируй по двум колонкам team И role. Сохрани в `g` сумму score.",
               "import pandas as pd\ndf = pd.DataFrame({\n    'team':['A','A','B','B'],\n    'role':['cap','sup','cap','sup'],\n    'score':[10,20,30,40]\n})\n",
               "import pandas as pd\ndf = pd.DataFrame({\n    'team':['A','A','B','B'],\n    'role':['cap','sup','cap','sup'],\n    'score':[10,20,30,40]\n})\ng = df.groupby(['team', 'role'])['score'].sum()",
               [{"check": "g.loc[('A', 'cap')] == 10", "msg": "A-cap = 10"},
                {"check": "g.loc[('B', 'sup')] == 40", "msg": "B-sup = 40"}],
               ["groupby([c1, c2])", "MultiIndex"], 3),
        ],
        minutes=55, difficulty=3,
    )


def _3_9():
    return lesson(
        "3.9", "Merge и Join в Pandas", "gaming", [
            theory(
                "**Merge** — соединение таблиц по ключу (аналог SQL JOIN). \n\n"
                "**Базовый синтаксис:**\n"
                "```python\n"
                "result = df1.merge(df2, on='key_col')\n"
                "result = df1.merge(df2, left_on='a', right_on='b')\n"
                "```\n\n"
                "**Типы соединений (how):**\n"
                "- `inner` (по умолчанию) — только совпадения\n"
                "- `left` — все из левой, NaN где нет совпадений в правой\n"
                "- `right` — все из правой\n"
                "- `outer` — все из обеих (union)\n\n"
                "**Суффиксы:** если колонки с одинаковыми именами, добавь `suffixes=('_x','_y')`.\n\n"
                "**join()** — соединение по индексу: `df1.join(df2)`.\n\n"
                "**concat()** — вертикальная/горизонтальная склейка:\n"
                "```python\n"
                "pd.concat([df1, df2])       # вертикально (строк больше)\n"
                "pd.concat([df1, df2], axis=1)  # горизонтально\n"
                "```"
            ),
            analogy(
                "merge — собрать два пазла: по общему элементу (ID игрока) соединяешь карточки игрока с карточкой команды.",
                "Таблица игроков Dota 2 + таблица команд: merge по `team_id` → у игрока появляется название команды и регион."
            ),
            visual(
                "Inner / Left / Outer join",
                "  df1 (players):           df2 (teams):\n"
                "  id   name   team_id      team_id  name   region\n"
                "  1    s1mple  1           1        NAVI   EU\n"
                "  2    NiKo    2           2        G2     EU\n"
                "  3    ZywOo   3           3        Vitality EU\n"
                "                          4        FaZe   NA  ← нет в df1\n"
                "\n"
                "  inner (default):         left:                  outer:\n"
                "  1 s1mple NAVI EU        1 s1mple NAVI EU       1 s1mple NAVI EU\n"
                "  2 NiKo   G2   EU        2 NiKo   G2   EU       2 NiKo   G2   EU\n"
                "  3 ZywOo  Vit  EU        3 ZywOo  Vit  EU       3 ZywOo  Vit  EU\n"
                "                          (FaZe не появляется)   4 NaN    FaZe  NA"
            ),
            example(
                "Соедини таблицу игроков с таблицей команд через merge по team_id.",
                "df1.merge(df2, on='team_id', how='left') сохраняет всех игроков, добавляя инфо о команде.",
                "import pandas as pd\n"
                "players = pd.DataFrame({\n"
                "    'player': ['s1mple', 'NiKo', 'ZywOo'],\n"
                "    'team_id': [1, 2, 3]\n"
                "})\n"
                "teams = pd.DataFrame({\n"
                "    'team_id': [1, 2, 3, 4],\n"
                "    'team_name': ['NAVI', 'G2', 'Vitality', 'FaZe'],\n"
                "    'region': ['EU', 'EU', 'EU', 'NA']\n"
                "})\n"
                "merged = players.merge(teams, on='team_id', how='left')\n"
                "print(merged)",
                "   player  team_id team_name region\n0  s1mple        1      NAVI     EU\n1    NiKo        2        G2     EU\n2   ZywOo        3  Vitality     EU",
                "how='left' сохранил всех 3 игроков. Команда FaZe (id=4) не попала, т.к. нет игроков. "
                "Если бы how='inner' — то же самое, т.к. все team_id игроков есть в teams."
            ),
            common_mistakes([
                {"mistake": "df1.merge(df2) без указания on", "why_bad": "Pandas ищет общие колонки, может упасть или объединить не по той", "fix": "Всегда указывай on= или left_on/right_on"},
                {"mistake": "merge по колонке с дубликатами без понимания", "why_bad": "Получишь декартово произведение — взрыв числа строк", "fix": "Проверяй уникальность: df['key'].is_unique"},
                {"mistake": "Путаница inner/left", "why_bad": "inner теряет строки без совпадений, left — нет", "fix": "Думай: мне нужны все строки из левой? → left"},
                {"mistake": "concat без ignore_index=True", "why_bad": "Индексы дублируются, .loc[0] даст 2 строки", "fix": "pd.concat([d1, d2], ignore_index=True)"},
            ]),
            interview_questions([
                {"q": "Чем merge отличается от join?", "a": "merge — по значениям колонок (on=). join — по индексу (по умолчанию). join удобен, когда индекс = ключ."},
                {"q": "Что такое декартово произведение и когда оно опасно?", "a": "Каждая строка левой × каждая строка правой. Возникает при merge без ключа или при дубликатах. N×M строк. Может взорвать память."},
                {"q": "Как сделать full outer join?", "a": "how='outer'. Получим все строки из обеих таблиц, NaN в недостающих колонках."},
            ]),
            knowledge_checklist([
                "Делаю merge с on= и how=",
                "Понимаю разницу inner/left/right/outer",
                "Использую pd.concat для склейки",
                "Использую left_on/right_on для разных имён ключей",
                "Обрабатываю суффиксы _x/_y",
            ]),
        ],
        exercises=[
            ex(1, "python", "Сделай inner merge df1 и df2 по 'id'. Сохрани в `result`.",
               "import pandas as pd\ndf1 = pd.DataFrame({'id':[1,2,3], 'name':['A','B','C']})\ndf2 = pd.DataFrame({'id':[2,3,4], 'score':[100,200,300]})\n",
               "import pandas as pd\ndf1 = pd.DataFrame({'id':[1,2,3], 'name':['A','B','C']})\ndf2 = pd.DataFrame({'id':[2,3,4], 'score':[100,200,300]})\nresult = df1.merge(df2, on='id', how='inner')",
               [{"check": "result.shape[0] == 2", "msg": "2 совпадения (id 2,3)"},
                {"check": "list(result.columns) == ['id', 'name', 'score']", "msg": "3 колонки"}],
               ["merge(on=...)", "how='inner'"], 1),
            ex(2, "python", "Сделай left merge по 'team_id'. Сохрани в `merged`.",
               "import pandas as pd\nplayers = pd.DataFrame({'p':['X','Y','Z'],'team_id':[1,2,9]})\nteams = pd.DataFrame({'team_id':[1,2,3],'name':['A','B','C']})\n",
               "import pandas as pd\nplayers = pd.DataFrame({'p':['X','Y','Z'],'team_id':[1,2,9]})\nteams = pd.DataFrame({'team_id':[1,2,3],'name':['A','B','C']})\nmerged = players.merge(teams, on='team_id', how='left')",
               [{"check": "merged.shape[0] == 3", "msg": "3 игрока (Z с NaN)"},
                {"check": "merged['name'].isna().sum() == 1", "msg": "1 NaN для Z"}],
               ["how='left'", "Сохраняет всех из левой"], 2),
            ex(3, "python", "Сделай outer merge по 'id'. Сохрани в `result`.",
               "import pandas as pd\ndf1 = pd.DataFrame({'id':[1,2],'a':['A','B']})\ndf2 = pd.DataFrame({'id':[2,3],'b':['X','Y']})\n",
               "import pandas as pd\ndf1 = pd.DataFrame({'id':[1,2],'a':['A','B']})\ndf2 = pd.DataFrame({'id':[2,3],'b':['X','Y']})\nresult = df1.merge(df2, on='id', how='outer')",
               [{"check": "result.shape[0] == 3", "msg": "3 строки (1,2,3)"},
                {"check": "result.shape[1] == 3", "msg": "3 колонки (id,a,b)"}],
               ["how='outer'", "Union"], 2),
            ex(4, "python", "Склей df1 и df2 вертикально через concat. Сохрани в `result`.",
               "import pandas as pd\ndf1 = pd.DataFrame({'a':[1,2]})\ndf2 = pd.DataFrame({'a':[3,4]})\n",
               "import pandas as pd\ndf1 = pd.DataFrame({'a':[1,2]})\ndf2 = pd.DataFrame({'a':[3,4]})\nresult = pd.concat([df1, df2], ignore_index=True)",
               [{"check": "result.shape[0] == 4", "msg": "4 строки"},
                {"check": "list(result['a']) == [1,2,3,4]", "msg": "[1,2,3,4]"}],
               ["pd.concat([d1, d2])", "ignore_index=True"], 2),
            ex(5, "python", "Сделай merge с разными именами ключей: left_on='team', right_on='team_name'. Сохрани в `m`.",
               "import pandas as pd\ndf1 = pd.DataFrame({'p':['X'],'team':['A']})\ndf2 = pd.DataFrame({'team_name':['A'],'region':['EU']})\n",
               "import pandas as pd\ndf1 = pd.DataFrame({'p':['X'],'team':['A']})\ndf2 = pd.DataFrame({'team_name':['A'],'region':['EU']})\nm = df1.merge(df2, left_on='team', right_on='team_name')",
               [{"check": "m.shape[0] == 1", "msg": "1 совпадение"},
                {"check": "m.loc[0, 'region'] == 'EU'", "msg": "region = EU"}],
               ["left_on/right_on", "Для разных имён"], 3),
            ex(6, "python", "Склей df1 и df2 горизонтально (axis=1). Сохрани в `result`.",
               "import pandas as pd\ndf1 = pd.DataFrame({'a':[1,2]})\ndf2 = pd.DataFrame({'b':[3,4]})\n",
               "import pandas as pd\ndf1 = pd.DataFrame({'a':[1,2]})\ndf2 = pd.DataFrame({'b':[3,4]})\nresult = pd.concat([df1, df2], axis=1)",
               [{"check": "result.shape == (2, 2)", "msg": "(2, 2)"},
                {"check": "list(result.columns) == ['a', 'b']", "msg": "a, b"}],
               ["axis=1", "Горизонтально"], 2),
            ex(7, "python", "Сделай merge с суффиксами _l и _r. Сохрани в `m`.",
               "import pandas as pd\ndf1 = pd.DataFrame({'id':[1], 'val':[10]})\ndf2 = pd.DataFrame({'id':[1], 'val':[20]})\n",
               "import pandas as pd\ndf1 = pd.DataFrame({'id':[1], 'val':[10]})\ndf2 = pd.DataFrame({'id':[1], 'val':[20]})\nm = df1.merge(df2, on='id', suffixes=('_l', '_r'))",
               [{"check": "'val_l' in m.columns and 'val_r' in m.columns", "msg": "val_l, val_r"},
                {"check": "m.loc[0, 'val_l'] == 10 and m.loc[0, 'val_r'] == 20", "msg": "10 и 20"}],
               ["suffixes=(...)", "Кортеж суффиксов"], 2),
            ex(8, "python", "Дан df1 с колонкой user_id и df2 с id. Сделай merge, сохрани в `m`.",
               "import pandas as pd\ndf1 = pd.DataFrame({'user_id':[1,2], 'name':['A','B']})\ndf2 = pd.DataFrame({'id':[1,3], 'order':[100,300]})\n",
               "import pandas as pd\ndf1 = pd.DataFrame({'user_id':[1,2], 'name':['A','B']})\ndf2 = pd.DataFrame({'id':[1,3], 'order':[100,300]})\nm = df1.merge(df2, left_on='user_id', right_on='id', how='inner')",
               [{"check": "m.shape[0] == 1", "msg": "1 совпадение (id=1)"},
                {"check": "m.loc[0, 'order'] == 100", "msg": "order=100"}],
               ["left_on/right_on", "how='inner'"], 3),
            ex(9, "python", "Сделай join df1 и df2 по индексу. Сохрани в `joined`.",
               "import pandas as pd\ndf1 = pd.DataFrame({'a':[1,2]}, index=['x','y'])\ndf2 = pd.DataFrame({'b':[3,4]}, index=['x','y'])\n",
               "import pandas as pd\ndf1 = pd.DataFrame({'a':[1,2]}, index=['x','y'])\ndf2 = pd.DataFrame({'b':[3,4]}, index=['x','y'])\njoined = df1.join(df2)",
               [{"check": "joined.shape == (2, 2)", "msg": "(2,2)"},
                {"check": "list(joined.columns) == ['a', 'b']", "msg": "a, b"}],
               [".join()", "По индексу"], 2),
            ex(10, "python", "После merge df1 и df2 по 'id' (left) посчитай сумму score. Сохрани в `total`.",
               "import pandas as pd\ndf1 = pd.DataFrame({'id':[1,2,3],'name':['A','B','C']})\ndf2 = pd.DataFrame({'id':[1,2],'score':[10,20]})\n",
               "import pandas as pd\ndf1 = pd.DataFrame({'id':[1,2,3],'name':['A','B','C']})\ndf2 = pd.DataFrame({'id':[1,2],'score':[10,20]})\nm = df1.merge(df2, on='id', how='left')\ntotal = m['score'].sum()",
               [{"check": "abs(total - 30.0) < 0.01", "msg": "10+20+0 = 30"}],
               ["merge(how='left')", ".sum() игнорирует NaN"], 3),
        ],
        minutes=60, difficulty=4,
    )


def _3_10():
    return lesson(
        "3.10", "Преобразование данных: pivot, melt, stack", "fintech", [
            theory(
                "Таблицы часто нужно **переформировать**: длинный формат → широкий и наоборот.\n\n"
                "**`pivot_table`** — широкая таблица (Excel-сводная):\n"
                "```python\n"
                "df.pivot_table(values='sales', index='region', columns='month', aggfunc='sum')\n"
                "```\n"
                "Параметры: `values` (что агрегируем), `index` (строки), `columns` (столбцы), `aggfunc` (функция).\n\n"
                "**`melt`** — длинный формат (unpivot):\n"
                "```python\n"
                "df.melt(id_vars=['region'], value_vars=['jan','feb'], var_name='month', value_name='sales')\n"
                "```\n\n"
                "**`stack` / `unstack`** — работа с MultiIndex:\n"
                "- `stack()` — столбцы → строки (широкая → длинная)\n"
                "- `unstack()` — строки → столбцы (длинная → широкая)\n\n"
                "**`crosstab`** — таблица сопряжённости (как pivot, но принимает Series):\n"
                "```python\n"
                "pd.crosstab(df['team'], df['role'])\n"
                "```"
            ),
            analogy(
                "pivot — как в Excel построить сводную: «покажи сумму продаж по регионам в строках и месяцам в столбцах». "
                "melt — обратная операция: из широкой таблицы сделать длинный список (для графиков и моделей).",
                "Продажи финтех-приложения: pivot даёт матрицу `регион × месяц`, melt — список строк (регион, месяц, сумма)."
            ),
            visual(
                "pivot vs melt",
                "  Исходный (длинный):        pivot (широкая):\n"
                "  region  month  sales       region   jan  feb  mar\n"
                "  EU      jan    100         EU       100  150  200\n"
                "  EU      feb    150         US        80  120  180\n"
                "  EU      mar    200\n"
                "  US      jan     80         melt (длинная):\n"
                "  US      feb    120         region  month  sales\n"
                "  US      mar    180         EU      jan    100\n"
                "                             US      jan     80\n"
                "  pivot_table(values='sales',\n"
                "    index='region', columns='month',\n"
                "    aggfunc='sum')"
            ),
            example(
                "Создай сводную таблицу продаж по регионам и месяцам.",
                "pivot_table принимает values (что агрегируем), index (строки), columns (столбцы), aggfunc. "
                "NaN в результате — где нет данных.",
                "import pandas as pd\n"
                "df = pd.DataFrame({\n"
                "    'region': ['EU','EU','US','US','EU'],\n"
                "    'month': ['jan','feb','jan','feb','jan'],\n"
                "    'sales': [100, 150, 80, 120, 50]\n"
                "})\n"
                "pivot = df.pivot_table(values='sales', index='region', columns='month', aggfunc='sum', fill_value=0)\n"
                "print(pivot)",
                "month    feb  jan\nregion\nEU       150  150\nUS       120   80",
                "EU: jan=100+50=150, feb=150. US: jan=80, feb=120. fill_value=0 заменяет пропуски нулями."
            ),
            common_mistakes([
                {"mistake": "pivot_table без aggfunc при дубликатах", "why_bad": "ValueError: index contains duplicate entries", "fix": "aggfunc='sum'/'mean'/'count' для агрегации дубликатов"},
                {"mistake": "melt без var_name", "why_bad": "Колонка с переменной получит имя 'variable'", "fix": "var_name='month', value_name='sales' для читаемости"},
                {"mistake": "stack на DataFrame с простым Index", "why_bad": "Получишь Series с MultiIndex — неудобно", "fix": "Сначала set_index, потом stack; либо используй pivot/melt"},
                {"mistake": "pivot вместо pivot_table при дубликатах", "why_bad": "ValueError — pivot не умеет агрегировать", "fix": "pivot_table с aggfunc"},
            ]),
            interview_questions([
                {"q": "Чем pivot отличается от pivot_table?", "a": "pivot — для уникальных комбинаций (без дубликатов). pivot_table — с агрегацией (sum, mean). Используй pivot_table по умолчанию."},
                {"q": "Когда использовать melt?", "a": "Когда данные хранятся в широком формате (один столбец на период), а нужны в длинном (одна строка на наблюдение) — для графиков, библиотек ML, БД."},
                {"q": "Что такое длинный vs широкий формат?", "a": "Длинный: каждое наблюдение — отдельная строка (tidy data). Широкий: значения разнесены по столбцам. Большинство ML-библиотек ждут длинный."},
            ]),
            knowledge_checklist([
                "Создаю сводные через pivot_table",
                "Знаю параметры values, index, columns, aggfunc",
                "Использую melt для длинного формата",
                "Применяю stack/unstack на MultiIndex",
                "Использую crosstab для сопряжённости",
            ]),
        ],
        exercises=[
            ex(1, "python", "Создай сводную таблицу: сумма sales по region. Сохрани в `p`.",
               "import pandas as pd\ndf = pd.DataFrame({'region':['EU','EU','US','US'],'sales':[100,150,80,120]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'region':['EU','EU','US','US'],'sales':[100,150,80,120]})\np = df.pivot_table(values='sales', index='region', aggfunc='sum')",
               [{"check": "p.loc['EU', 'sales'] == 250", "msg": "EU = 250"},
                {"check": "p.loc['US', 'sales'] == 200", "msg": "US = 200"}],
               ["pivot_table", "aggfunc='sum'"], 2),
            ex(2, "python", "Создай сводную по двум осям: region × month, aggfunc=sum. Сохрани в `p`.",
               "import pandas as pd\ndf = pd.DataFrame({\n    'region':['EU','EU','US','US'],\n    'month':['jan','feb','jan','feb'],\n    'sales':[100,150,80,120]\n})\n",
               "import pandas as pd\ndf = pd.DataFrame({\n    'region':['EU','EU','US','US'],\n    'month':['jan','feb','jan','feb'],\n    'sales':[100,150,80,120]\n})\np = df.pivot_table(values='sales', index='region', columns='month', aggfunc='sum')",
               [{"check": "p.loc['EU', 'jan'] == 100", "msg": "EU jan = 100"},
                {"check": "p.loc['US', 'feb'] == 120", "msg": "US feb = 120"}],
               ["index/columns", "aggfunc='sum'"], 2),
            ex(3, "python", "Сделай melt: id_vars='team', value_vars=['win','lose']. Сохрани в `melted`.",
               "import pandas as pd\ndf = pd.DataFrame({'team':['A','B'],'win':[5,3],'lose':[2,7]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'team':['A','B'],'win':[5,3],'lose':[2,7]})\nmelted = df.melt(id_vars='team', value_vars=['win', 'lose'], var_name='result', value_name='games')",
               [{"check": "melted.shape[0] == 4", "msg": "4 строки"},
                {"check": "list(melted.columns) == ['team', 'result', 'games']", "msg": "Колонки team, result, games"}],
               ["df.melt()", "id_vars/value_vars"], 3),
            ex(4, "python", "Дан df. Сделай pivot: строки — product, столбцы — month, значения — qty. Сохрани в `p`.",
               "import pandas as pd\ndf = pd.DataFrame({\n    'product':['A','A','B','B'],\n    'month':['jan','feb','jan','feb'],\n    'qty':[10,20,30,40]\n})\n",
               "import pandas as pd\ndf = pd.DataFrame({\n    'product':['A','A','B','B'],\n    'month':['jan','feb','jan','feb'],\n    'qty':[10,20,30,40]\n})\np = df.pivot(index='product', columns='month', values='qty')",
               [{"check": "p.loc['A', 'jan'] == 10", "msg": "A jan = 10"},
                {"check": "p.loc['B', 'feb'] == 40", "msg": "B feb = 40"}],
               ["df.pivot()", "index/columns/values"], 3),
            ex(5, "python", "Сделай crosstab: команды × роли. Сохрани в `ct`.",
               "import pandas as pd\ndf = pd.DataFrame({\n    'team':['A','A','B','B','A'],\n    'role':['cap','sup','cap','sup','sup']\n})\n",
               "import pandas as pd\ndf = pd.DataFrame({\n    'team':['A','A','B','B','A'],\n    'role':['cap','sup','cap','sup','sup']\n})\nct = pd.crosstab(df['team'], df['role'])",
               [{"check": "ct.loc['A', 'cap'] == 1", "msg": "A-cap = 1"},
                {"check": "ct.loc['A', 'sup'] == 2", "msg": "A-sup = 2"}],
               ["pd.crosstab()", "Два Series на вход"], 2),
            ex(6, "python", "Создай pivot_table с aggfunc=['sum','mean']. Сохрани в `p`.",
               "import pandas as pd\ndf = pd.DataFrame({'region':['EU','EU','US','US'],'sales':[100,150,80,120]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'region':['EU','EU','US','US'],'sales':[100,150,80,120]})\np = df.pivot_table(values='sales', index='region', aggfunc=['sum', 'mean'])",
               [{"check": "('sum', 'sales') in p.columns", "msg": "sum/sales"},
                {"check": "p[('sum', 'sales')].loc['EU'] == 250", "msg": "EU sum = 250"}],
               ["aggfunc=[list]", "MultiIndex колонок"], 3),
            ex(7, "python", "Дан df. Сделай melt: id_vars=['id'], value_vars=['m1','m2']. Сохрани в `m`.",
               "import pandas as pd\ndf = pd.DataFrame({'id':[1,2],'m1':[10,20],'m2':[30,40]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'id':[1,2],'m1':[10,20],'m2':[30,40]})\nm = df.melt(id_vars=['id'], value_vars=['m1', 'm2'])",
               [{"check": "m.shape[0] == 4", "msg": "4 строки"},
                {"check": "list(m.columns) == ['id', 'variable', 'value']", "msg": "id, variable, value"}],
               ["id_vars=[]", "value_vars=[]"], 2),
            ex(8, "python", "Дан df. Создай pivot_table с fill_value=0. Сохрани в `p`.",
               "import pandas as pd\ndf = pd.DataFrame({\n    'r':['EU','US'],\n    'm':['jan','jan'],\n    'v':[100,80]\n})\n",
               "import pandas as pd\ndf = pd.DataFrame({\n    'r':['EU','US'],\n    'm':['jan','jan'],\n    'v':[100,80]\n})\np = df.pivot_table(values='v', index='r', columns='m', fill_value=0, aggfunc='sum')",
               [{"check": "p.loc['EU', 'jan'] == 100", "msg": "EU jan = 100"},
                {"check": "p.shape == (2, 1)", "msg": "(2, 1)"}],
               ["fill_value=0", "aggfunc обязателен"], 2),
            ex(9, "python", "Дан DataFrame с MultiIndex. Сделай stack. Сохрани в `stacked`.",
               "import pandas as pd\ndf = pd.DataFrame({'A':[1,2],'B':[3,4]}, index=['x','y'])\n",
               "import pandas as pd\ndf = pd.DataFrame({'A':[1,2],'B':[3,4]}, index=['x','y'])\nstacked = df.stack()",
               [{"check": "len(stacked) == 4", "msg": "4 значения"},
                {"check": "stacked.loc[('x', 'A')] == 1", "msg": "x,A = 1"}],
               [".stack()", "MultiIndex"], 3),
            ex(10, "python", "Дан df. Посчитай общую сумму sales по всем регионам. Сохрани в `total`.",
               "import pandas as pd\ndf = pd.DataFrame({\n    'region':['EU','EU','US','US'],\n    'month':['jan','feb','jan','feb'],\n    'sales':[100,150,80,120]\n})\n",
               "import pandas as pd\ndf = pd.DataFrame({\n    'region':['EU','EU','US','US'],\n    'month':['jan','feb','jan','feb'],\n    'sales':[100,150,80,120]\n})\ntotal = df.pivot_table(values='sales', aggfunc='sum').iloc[0, 0]",
               [{"check": "total == 450", "msg": "100+150+80+120 = 450"}],
               ["pivot_table", "aggfunc='sum'"], 3),
        ],
        minutes=55, difficulty=3,
    )


def _3_11():
    return lesson(
        "3.11", "Работа с датами и временными рядами", "space", [
            theory(
                "**Дата и время** в Pandas — тип `datetime64`. Pandas умеет парсить, индексировать и "
                "извлекать компоненты.\n\n"
                "**Преобразование в дату:**\n"
                "```python\n"
                "df['date'] = pd.to_datetime(df['date_str'])\n"
                "```\n\n"
                "**Генерация диапазона дат:**\n"
                "```python\n"
                "pd.date_range('2020-01-01', periods=5, freq='D')  # 5 дней\n"
                "```\n"
                "Частоты: `D` (день), `H` (час), `M` (месяц), `Y` (год), `W` (неделя).\n\n"
                "**Атрибуты .dt:**\n"
                "- `df['date'].dt.year / .month / .day / .hour / .dayofweek`\n"
                "- `df['date'].dt.day_name()` — название дня недели\n\n"
                "**Resample** (как groupby, но по времени):\n"
                "```python\n"
                "df.set_index('date').resample('M')['sales'].sum()\n"
                "```\n\n"
                "**Diff / shift** — разности и лаги для временных рядов."
            ),
            analogy(
                "Временной ряд — это видео: каждый кадр — замер. Resample — замедление видео (один кадр в месяц вместо дня). "
                "Shift — посмотреть на кадр на секунду раньше.",
                "Температура двигателя ракеты, замеренная каждую секунду: resample('1min') — средняя за минуту, "
                "shift(1) — значение секунду назад."
            ),
            visual(
                "Resample: aggregation по времени",
                "  Сырые данные (каждую секунду):\n"
                "  time                 temp\n"
                "  2024-01-01 00:00:00   3200\n"
                "  2024-01-01 00:00:01   3210\n"
                "  2024-01-01 00:00:02   3220\n"
                "  2024-01-01 00:01:00   3250   ← новая минута\n"
                "  ...\n"
                "\n"
                "  resample('1min').mean():\n"
                "  2024-01-01 00:00:00   3210  (среднее за 60 сек)\n"
                "  2024-01-01 00:01:00   3250\n"
                "\n"
                "  Частоты: D=день, H=час, M=месяц, W=неделя, Y=год"
            ),
            example(
                "Преобразуй строки с датами запусков SpaceX в datetime, посчитай количество миссий по годам.",
                "pd.to_datetime парсит строки. .dt.year извлекает год. value_counts считает частоты.",
                "import pandas as pd\n"
                "df = pd.DataFrame({\n"
                "    'mission': ['Crew-1', 'Crew-2', 'Starlink-23', 'Crew-3'],\n"
                "    'date': ['2020-11-15', '2021-04-23', '2021-05-15', '2021-11-10']\n"
                "})\n"
                "df['date'] = pd.to_datetime(df['date'])\n"
                "df['year'] = df['date'].dt.year\n"
                "print(df)\n"
                "print('Миссий по годам:')\n"
                "print(df['year'].value_counts())",
                "      mission       date       year\n0      Crew-1 2020-11-15      2020\n1      Crew-2 2021-04-23      2021\n2  Starlink-23 2021-05-15      2021\n3      Crew-3 2021-11-10      2021\nМиссий по годам:\n2021    3\n2020    1",
                "to_datetime парсит ISO-формат. dt.year возвращает целое число. value_counts сортирует по убыванию."
            ),
            common_mistakes([
                {"mistake": "Сравнение datetime со строкой", "why_bad": "'2024-01-01' != datetime(2024,1,1) — разные типы", "fix": "Сначала pd.to_datetime, потом сравнивай"},
                {"mistake": "Resample без set_index", "why_bad": "Pandas не знает, по какой колонке агрегировать", "fix": "Сначала df.set_index('date'), потом resample"},
                {"mistake": "dt.month на строковой колонке", "why_bad": "AttributeError: 'Series' object has no attribute 'month'", "fix": "Сначала pd.to_datetime, потом dt.month"},
                {"mistake": "Неправильная частота в resample", "why_bad": "'M' устарело, даёт warning", "fix": "Используй 'ME' (month end) или 'MS' (month start) в новой версии"},
            ]),
            interview_questions([
                {"q": "Чем отличается resample от groupby?", "a": "resample работает с DatetimeIndex и понимает частоты (D, M, Y). groupby — с любой колонкой. Для времени удобнее resample."},
                {"q": "Что делает shift(1)?", "a": "Сдвигает серию на 1 период вперёд: первая строка = NaN, остальные — предыдущее значение. Используют для лаговых фич в ML."},
                {"q": "Какие частоты поддерживает date_range?", "a": "D (день), B (рабочий день), H (час), T/min (минута), S (секунда), M/ME/MS (месяц), Q (квартал), Y/YS (год), W (неделя)."},
            ]),
            knowledge_checklist([
                "Преобразую строки в дату через pd.to_datetime",
                "Извлекаю компоненты через .dt.year/.month/.day",
                "Генерирую диапазоны через pd.date_range",
                "Использую resample для агрегации по времени",
                "Использую shift для лагов",
            ]),
        ],
        exercises=[
            ex(1, "python", "Преобразуй строку '2024-01-15' в datetime. Сохрани в `dt`.",
               "import pandas as pd\n",
               "import pandas as pd\ndt = pd.to_datetime('2024-01-15')",
               [{"check": "pd.api.types.is_datetime64_any_dtype(pd.Series([dt]))", "msg": "datetime64"},
                {"check": "dt.year == 2024", "msg": "2024 год"}],
               ["pd.to_datetime()", "ISO-формат"], 1),
            ex(2, "python", "Создай диапазон из 5 дней начиная с 2024-01-01. Сохрани в `dates`.",
               "import pandas as pd\n",
               "import pandas as pd\ndates = pd.date_range('2024-01-01', periods=5, freq='D')",
               [{"check": "len(dates) == 5", "msg": "5 дат"},
                {"check": "dates[0].day == 1", "msg": "1 января"}],
               ["pd.date_range", "freq='D'"], 1),
            ex(3, "python", "Дан df с колонкой date_str. Преобразуй в datetime. Сохрани в `df`.",
               "import pandas as pd\ndf = pd.DataFrame({'date_str':['2024-01-01','2024-02-01']})\n",
               "import pandas as pd\ndf = pd.DataFrame({'date_str':['2024-01-01','2024-02-01']})\ndf['date'] = pd.to_datetime(df['date_str'])",
               [{"check": "pd.api.types.is_datetime64_any_dtype(df['date'])", "msg": "datetime64"},
                {"check": "df.shape[1] == 2", "msg": "2 колонки"}],
               ["pd.to_datetime()", "Исходный df дополнен"], 2),
            ex(4, "python", "Дан df с datetime-колонкой date. Извлеки месяц в новую колонку `month`.",
               "import pandas as pd\ndf = pd.DataFrame({'date': pd.to_datetime(['2024-01-15','2024-02-20','2024-03-10'])})\n",
               "import pandas as pd\ndf = pd.DataFrame({'date': pd.to_datetime(['2024-01-15','2024-02-20','2024-03-10'])})\ndf['month'] = df['date'].dt.month",
               [{"check": "'month' in df.columns", "msg": "Колонка month"},
                {"check": "list(df['month']) == [1, 2, 3]", "msg": "[1, 2, 3]"}],
               [".dt.month", "Accessor dt"], 2),
            ex(5, "python", "Дан df. Извлеки день недели (0=Пн, 6=Вс) в колонку `weekday`.",
               "import pandas as pd\ndf = pd.DataFrame({'date': pd.to_datetime(['2024-01-01','2024-01-02','2024-01-03'])})\n",
               "import pandas as pd\ndf = pd.DataFrame({'date': pd.to_datetime(['2024-01-01','2024-01-02','2024-01-03'])})\ndf['weekday'] = df['date'].dt.dayofweek",
               [{"check": "'weekday' in df.columns", "msg": "Колонка"},
                {"check": "df['weekday'].iloc[0] == 0", "msg": "Понедельник = 0"}],
               [".dt.dayofweek", "0=Пн, 6=Вс"], 2),
            ex(6, "python", "Дан df с datetime. Создай Series `years` с годами.",
               "import pandas as pd\ndf = pd.DataFrame({'date': pd.to_datetime(['2020-06-15','2021-07-20','2022-08-25'])})\n",
               "import pandas as pd\ndf = pd.DataFrame({'date': pd.to_datetime(['2020-06-15','2021-07-20','2022-08-25'])})\nyears = df['date'].dt.year",
               [{"check": "list(years) == [2020, 2021, 2022]", "msg": "[2020, 2021, 2022]"}],
               [".dt.year", "Целое число"], 1),
            ex(7, "python", "Дан df с DatetimeIndex и колонкой value. Сделай resample по 2 дням, sum. Сохрани в `r`.",
               "import pandas as pd\ndf = pd.DataFrame({'value':[1,2,3,4]}, index=pd.date_range('2024-01-01', periods=4, freq='D'))\n",
               "import pandas as pd\ndf = pd.DataFrame({'value':[1,2,3,4]}, index=pd.date_range('2024-01-01', periods=4, freq='D'))\nr = df.resample('2D').sum()",
               [{"check": "r.shape[0] == 2", "msg": "2 периода"},
                {"check": "r['value'].iloc[0] == 3", "msg": "1+2=3"}],
               ["set_index", ".resample('2D').sum()"], 3),
            ex(8, "python", "Дан Series `s` с DatetimeIndex (4 дня). Сделай shift на 1. Сохрани в `shifted`.",
               "import pandas as pd\ns = pd.Series([10,20,30,40], index=pd.date_range('2024-01-01', periods=4, freq='D'))\n",
               "import pandas as pd\ns = pd.Series([10,20,30,40], index=pd.date_range('2024-01-01', periods=4, freq='D'))\nshifted = s.shift(1)",
               [{"check": "shifted.iloc[0] != shifted.iloc[0] or pd.isna(shifted.iloc[0])", "msg": "Первая = NaN"},
                {"check": "shifted.iloc[1] == 10", "msg": "Вторая = 10"}],
               [".shift(1)", "Сдвиг на 1"], 2),
            ex(9, "python", "Дан df с datetime. Вычисли разность в днях между двумя датами. Сохрани в `diff_days`.",
               "import pandas as pd\ndf = pd.DataFrame({\n    'start': pd.to_datetime(['2024-01-01']),\n    'end': pd.to_datetime(['2024-01-15'])\n})\n",
               "import pandas as pd\ndf = pd.DataFrame({\n    'start': pd.to_datetime(['2024-01-01']),\n    'end': pd.to_datetime(['2024-01-15'])\n})\ndiff_days = (df['end'] - df['start']).dt.days.iloc[0]",
               [{"check": "diff_days == 14", "msg": "14 дней"}],
               ["- между датами", ".dt.days"], 2),
            ex(10, "python", "Создай Series `s` с DatetimeIndex из 3 дат: 2024-01-01, 2024-02-01, 2024-03-01. Значения [10,20,30].",
               "import pandas as pd\n",
               "import pandas as pd\ns = pd.Series([10, 20, 30], index=pd.date_range('2024-01-01', periods=3, freq='MS'))",
               [{"check": "len(s) == 3", "msg": "3 элемента"},
                {"check": "s.iloc[1] == 20", "msg": "Второй = 20"},
                {"check": "pd.api.types.is_datetime64_any_dtype(pd.Series(s.index))", "msg": "DatetimeIndex"}],
               ["pd.date_range", "freq='MS' (месяц)"], 2),
        ],
        minutes=55, difficulty=3,
    )


def _3_12():
    return lesson(
        "3.12", "Мини-проект: Очистка и подготовка реального датасета", "gaming", [
            theory(
                "В этом проекте мы применим всё изученное к **реальному набору данных** о матчах Dota 2. "
                "Этапы очистки:\n\n"
                "1. **Загрузка и осмотр** — `head()`, `info()`, `dtypes`, `shape`\n"
                "2. **Пропуски** — обнаружение, стратегия (drop/fill)\n"
                "3. **Дубликаты** — поиск и удаление\n"
                "4. **Выбросы** — IQR-метод, clip или удаление\n"
                "5. **Преобразования** — типы данных, новые колонки\n"
                "6. **Анализ** — groupby, pivot, value_counts\n\n"
                "**Цель:** получить чистый DataFrame, готовый к визуализации и ML-моделям."
            ),
            analogy(
                "Очистка данных — как подготовка продуктов перед готовкой: моем, чистим, нарезаем. "
                "Без этого даже хороший рецепт не спасёт.",
                "Грязный лог матчей Dota 2: пропуски в KDA, дубли, KD=99 из-за бага — превращаем в аккуратную таблицу для аналитики."
            ),
            visual(
                "Pipeline очистки данных",
                "  Сырой df\n"
                "     │\n"
                "     ▼\n"
                "  ┌──────────────────┐\n"
                "  │ 1. head/info     │  первый осмотр\n"
                "  └────────┬─────────┘\n"
                "           ▼\n"
                "  ┌──────────────────┐\n"
                "  │ 2. dropna/fillna │  пропуски\n"
                "  └────────┬─────────┘\n"
                "           ▼\n"
                "  ┌──────────────────┐\n"
                "  │ 3. drop_dupl.    │  дубликаты\n"
                "  └────────┬─────────┘\n"
                "           ▼\n"
                "  ┌──────────────────┐\n"
                "  │ 4. clip / IQR    │  выбросы\n"
                "  └────────┬─────────┘\n"
                "           ▼\n"
                "  ┌──────────────────┐\n"
                "  │ 5. типы / новые  │  фичи\n"
                "  └────────┬─────────┘\n"
                "           ▼\n"
                "     Чистый df  →  анализ"
            ),
            example(
                "Очисти датасет матчей: пропуски → медиана, дубликаты удалить, выбросы KDA заменить границами.",
                "Пошагово: осмотр → fillna → drop_duplicates → clip. В конце — groupby для проверки результата.",
                "import pandas as pd\n"
                "import numpy as np\n"
                "df = pd.DataFrame({\n"
                "    'match_id': [1, 2, 2, 3, 4, 5],\n"
                "    'player': ['A','B','B','C','D','E'],\n"
                "    'team': ['X','Y','Y','Z','X','Y'],\n"
                "    'kda': [3.5, 4.1, 4.1, 5.0, 99.9, np.nan]\n"
                "})\n"
                "print('До очистки:', df.shape)\n"
                "df['kda'] = df['kda'].fillna(df['kda'].median())\n"
                "df = df.drop_duplicates()\n"
                "df['kda'] = df['kda'].clip(upper=20)\n"
                "print('После:')\n"
                "print(df.groupby('team')['kda'].mean())",
                "До очистки: (6, 4)\nkda\nteam\nX    3.500000\nY    4.100000\nZ    5.000000\nName: kda, dtype: float64",
                "Pipeline: NaN → median(3.8) → drop_duplicates (id=2) → clip(<=20) убирает выброс 99.9. "
                "Результат: 5 строк, медиана по командам осмысленна."
            ),
            common_mistakes([
                {"mistake": "Сразу удалять пропуски без анализа", "why_bad": "Можно потерять 50% данных, которые можно было заполнить", "fix": "isna().sum() сначала, потом стратегия"},
                {"mistake": "Забыть проверить результат после очистки", "why_bad": "Можно удалить нужные строки или исказить статистику", "fix": "Проверяй shape, describe, value_counts до и после"},
                {"mistake": "Применять clip до удаления дубликатов", "why_bad": "Clip не убирает дубли — порядок шагов важен", "fix": "drop_duplicates сначала, потом clip"},
                {"mistake": "Использовать fillna(0) для скошенных данных", "why_bad": "0 сильно сдвинет среднее", "fix": "median() или ffill() — лучше для скошенных"},
            ]),
            interview_questions([
                {"q": "Какой первый шаг в очистке данных?", "a": "Осмотр: df.head(), df.info(), df.describe(), df.isna().sum(). Понять структуру и масштаб проблем ДО любых трансформаций."},
                {"q": "Когда fillna(mean) опасно?", "a": "При несимметричном распределении (outliers) или при MCAR-нарушении. Всегда проверяй распределение до заполнения."},
                {"q": "Как проверить качество очистки?", "a": "Сравнить describe() до/после. Проверить, что выбросы пропали (max, min). Убедиться, что пропусков 0. Посмотреть на распределения (гистограммы)."},
            ]),
            knowledge_checklist([
                "Загружаю данные и делаю первый осмотр",
                "Обрабатываю пропуски осмысленно",
                "Удаляю дубликаты правильно (subset, keep)",
                "Нахожу и обрабатываю выбросы",
                "Делаю groupby для проверки результата",
            ]),
        ],
        exercises=[
            ex(1, "python", "Создай df с 5 строками матчей (player, team, kda). Сохрани в `df`.",
               "import pandas as pd\n",
               "import pandas as pd\ndf = pd.DataFrame({\n    'player': ['A','B','C','D','E'],\n    'team': ['X','Y','X','Y','Z'],\n    'kda': [3.0, 4.0, 5.0, 2.5, 6.0]\n})",
               [{"check": "df.shape == (5, 3)", "msg": "5 строк, 3 колонки"}],
               ["pd.DataFrame({...})", "3 колонки"], 1),
            ex(2, "python", "Дан df. Заполни NaN в 'kda' медианой. Сохрани в `df_clean`.",
               "import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({'kda':[3.0, np.nan, 5.0, np.nan, 2.0]})\n",
               "import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({'kda':[3.0, np.nan, 5.0, np.nan, 2.0]})\ndf_clean = df.copy()\ndf_clean['kda'] = df_clean['kda'].fillna(df_clean['kda'].median())",
               [{"check": "df_clean['kda'].isna().sum() == 0", "msg": "Нет NaN"},
                {"check": "abs(df_clean['kda'].iloc[1] - 3.0) < 0.01", "msg": "median ≈ 3.0"}],
               ["fillna(median)", "Не меняй оригинал"], 2),
            ex(3, "python", "Дан df с дубликатами. Удали точные дубликаты. Сохрани в `df_unique`.",
               "import pandas as pd\ndf = pd.DataFrame({'p':['A','B','A','C','B'], 'kda':[3,4,3,5,4]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'p':['A','B','A','C','B'], 'kda':[3,4,3,5,4]})\ndf_unique = df.drop_duplicates()",
               [{"check": "df_unique.shape[0] == 3", "msg": "3 уникальные"},
                {"check": "df_unique.duplicated().sum() == 0", "msg": "Нет дублей"}],
               ["drop_duplicates()", "Без subset"], 1),
            ex(4, "python", "Дан df. Замени KDA > 20 на 20 (clip). Сохрани в `df_clip`.",
               "import pandas as pd\ndf = pd.DataFrame({'kda':[3, 4, 25, 100, 5]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'kda':[3, 4, 25, 100, 5]})\ndf_clip = df.copy()\ndf_clip['kda'] = df_clip['kda'].clip(upper=20)",
               [{"check": "df_clip['kda'].max() == 20", "msg": "max = 20"},
                {"check": "df_clip['kda'].iloc[2] == 20", "msg": "25 → 20"}],
               [".clip(upper=20)", "Ограничить сверху"], 2),
            ex(5, "python", "Дан df. Посчитай среднее kda по командам. Сохрани в `team_avg`.",
               "import pandas as pd\ndf = pd.DataFrame({'team':['X','X','Y','Y'],'kda':[3,5,2,4]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'team':['X','X','Y','Y'],'kda':[3,5,2,4]})\nteam_avg = df.groupby('team')['kda'].mean()",
               [{"check": "abs(team_avg['X'] - 4.0) < 0.01", "msg": "X = 4"},
                {"check": "abs(team_avg['Y'] - 3.0) < 0.01", "msg": "Y = 3"}],
               ["groupby", ".mean()"], 2),
            ex(6, "python", "Дан df. Посчитай сколько матчей у каждого игрока. Сохрани в `counts`.",
               "import pandas as pd\ndf = pd.DataFrame({'player':['A','B','A','A','C','B']})\n",
               "import pandas as pd\ndf = pd.DataFrame({'player':['A','B','A','A','C','B']})\ncounts = df['player'].value_counts()",
               [{"check": "counts['A'] == 3", "msg": "A — 3"},
                {"check": "counts['B'] == 2", "msg": "B — 2"},
                {"check": "counts['C'] == 1", "msg": "C — 1"}],
               [".value_counts()", "По убыванию"], 1),
            ex(7, "python", "Дан df с колонкой date_str. Преобразуй в datetime. Сохрани в `df`.",
               "import pandas as pd\ndf = pd.DataFrame({'date_str':['2024-01-15','2024-02-20']})\n",
               "import pandas as pd\ndf = pd.DataFrame({'date_str':['2024-01-15','2024-02-20']})\ndf['date'] = pd.to_datetime(df['date_str'])",
               [{"check": "pd.api.types.is_datetime64_any_dtype(df['date'])", "msg": "datetime64"}],
               ["pd.to_datetime()", "Новая колонка"], 2),
            ex(8, "python", "Дан df. Сделай merge с таблицей команд по 'team'. Сохрани в `merged`.",
               "import pandas as pd\nplayers = pd.DataFrame({'player':['A','B'],'team':['X','Y']})\nteams = pd.DataFrame({'team':['X','Y'],'region':['EU','NA']})\n",
               "import pandas as pd\nplayers = pd.DataFrame({'player':['A','B'],'team':['X','Y']})\nteams = pd.DataFrame({'team':['X','Y'],'region':['EU','NA']})\nmerged = players.merge(teams, on='team')",
               [{"check": "merged.shape == (2, 3)", "msg": "(2, 3)"},
                {"check": "merged.loc[0, 'region'] == 'EU'", "msg": "EU"}],
               ["merge(on=...)", "how='inner' по умолчанию"], 2),
            ex(9, "python", "Дан df. Создай pivot: строки team, столбцы role, aggfunc=mean для kda. Сохрани в `p`.",
               "import pandas as pd\ndf = pd.DataFrame({\n    'team':['X','X','Y','Y'],\n    'role':['cap','sup','cap','sup'],\n    'kda':[3,5,2,4]\n})\n",
               "import pandas as pd\ndf = pd.DataFrame({\n    'team':['X','X','Y','Y'],\n    'role':['cap','sup','cap','sup'],\n    'kda':[3,5,2,4]\n})\np = df.pivot_table(values='kda', index='team', columns='role', aggfunc='mean')",
               [{"check": "p.loc['X', 'cap'] == 3", "msg": "X cap = 3"},
                {"check": "p.loc['Y', 'sup'] == 4", "msg": "Y sup = 4"}],
               ["pivot_table", "index/columns"], 3),
            ex(10, "python", "Дан df. Удали дубликаты по 'player' (оставь последнее) и заполни kda медианой. Сохрани в `final`.",
               "import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({\n    'player':['A','A','B','B','C'],\n    'kda':[3.0, np.nan, 5.0, 4.0, np.nan]\n})\n",
               "import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({\n    'player':['A','A','B','B','C'],\n    'kda':[3.0, np.nan, 5.0, 4.0, np.nan]\n})\ndf = df.drop_duplicates(subset=['player'], keep='last')\nfinal = df.copy()\nfinal['kda'] = final['kda'].fillna(final['kda'].median())",
               [{"check": "final.shape[0] == 3", "msg": "3 игрока"},
                {"check": "final['kda'].isna().sum() == 0", "msg": "Нет NaN"}],
               ["drop_duplicates(subset=...)", "fillna(median)"], 3),
            ex(11, "python", "Дан df. Построй сводную: среднее kda по team и role, fill_value=0. Сохрани в `p`.",
               "import pandas as pd\ndf = pd.DataFrame({\n    'team':['X','Y'],\n    'role':['cap','cap'],\n    'kda':[3.0, 5.0]\n})\n",
               "import pandas as pd\ndf = pd.DataFrame({\n    'team':['X','Y'],\n    'role':['cap','cap'],\n    'kda':[3.0, 5.0]\n})\np = df.pivot_table(values='kda', index='team', columns='role', aggfunc='mean', fill_value=0)",
               [{"check": "p.loc['X', 'cap'] == 3.0", "msg": "X cap = 3"},
                {"check": "p.shape == (2, 1)", "msg": "(2,1)"}],
               ["pivot_table", "fill_value=0"], 3),
            ex(12, "python", "Финальный pipeline: дан грязный df. Удали дубли, заполни kda медианой, замени KDA>15 на 15. Сохрани в `clean`.",
               "import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({\n    'player':['A','B','A','C','D'],\n    'kda':[3.0, 4.0, 3.0, np.nan, 20.0]\n})\n",
               "import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({\n    'player':['A','B','A','C','D'],\n    'kda':[3.0, 4.0, 3.0, np.nan, 20.0]\n})\ndf = df.drop_duplicates()\nmed = df['kda'].median()\ndf['kda'] = df['kda'].fillna(med)\ndf['kda'] = df['kda'].clip(upper=15)\nclean = df",
               [{"check": "clean.shape[0] == 4", "msg": "4 строки"},
                {"check": "clean['kda'].isna().sum() == 0", "msg": "Нет NaN"},
                {"check": "clean['kda'].max() == 15", "msg": "max = 15"}],
               ["drop_duplicates()", "fillna + clip"], 3),
        ],
        minutes=90, difficulty=4,
    )


LESSONS = [_3_1, _3_2, _3_3, _3_4, _3_5, _3_6, _3_7, _3_8, _3_9, _3_10, _3_11, _3_12]
