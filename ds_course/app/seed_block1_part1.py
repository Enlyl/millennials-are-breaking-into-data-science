"""
Блок 1: Python для Data Science — Космос.
12 уроков, ~80 упражнений.
"""
from app.seed_helpers import (
    ex, lesson, theory, analogy, visual, example,
    common_mistakes, interview_questions, knowledge_checklist,
)


def _1_1():
    return lesson(
        "1.1", "Переменные и типы данных", "space", [
            theory(
                "**Переменная** — это именованный контейнер для хранения данных. "
                "Представь коробку с наклейкой: наклейка — это имя, а то, что внутри, — значение.\n\n"
                "В Python не нужно заранее объявлять тип — он определяется автоматически.\n\n"
                "**Основные типы:**\n"
                "- `int` — целые числа: `42`, `-7`, `0`\n"
                "- `float` — дробные: `3.14`, `-0.5`\n"
                "- `str` — строки: `'Привет'`, `\"Ракета\"`\n"
                "- `bool` — логический: `True`, `False`\n"
                "- `NoneType` — отсутствие значения: `None`"
            ),
            analogy(
                "Переменная — ячейка камеры хранения на вокзале: ключ (имя) открывает ячейку со значением.",
                "Ячейка телеметрии: `altitude = 12000` — в ячейке 'altitude' лежит число 12000 метров."
            ),
            visual(
                "Переменные как наклейки на коробках",
                "    Имя (наклейка)        Значение (содержимое)\n"
                "   ┌──────────────┐     ┌────────────────┐\n"
                "   │  rocket_name │ ──▶ │  'Falcon 9'    │  (str)\n"
                "   │  altitude    │ ──▶ │   12000        │  (int)\n"
                "   │  is_in_orbit │ ──▶ │   False        │  (bool)\n"
                "   │  fuel_mass   │ ──▶ │   450.5        │  (float)\n"
                "   └──────────────┘     └────────────────┘"
            ),
            example(
                "Запиши параметры запуска ракеты-носителя и выведи их.",
                "1. Строка для имени.\n2. Целое число для высоты в метрах.\n3. Логическое для статуса.\n4. f-string для красивого вывода.",
                "rocket_name = 'Falcon 9'\n"
                "altitude_m = 12000\n"
                "is_in_orbit = False\n"
                "fuel_kg = 450.5\n"
                "\n"
                "print(f'Ракета: {rocket_name}')\n"
                "print(f'Высота: {altitude_m} м')\n"
                "print(f'Тип altitude: {type(altitude_m).__name__}')",
                "Ракета: Falcon 9\nВысота: 12000 м\nТип altitude: int",
                "Python автоматически понял типы. type(x).__name__ возвращает имя типа в виде строки."
            ),
            common_mistakes([
                {"mistake": "rocket-name = 'X'", "why_bad": "Дефис — это минус, Python думает это вычитание", "fix": "Используй подчёркивание: rocket_name"},
                {"mistake": "42 == '42'", "why_bad": "Разные типы — всегда False", "fix": "int('42') == 42"},
                {"mistake": "name = Falcon 9", "why_bad": "Python ищет переменные Falcon и 9", "fix": "name = 'Falcon 9' (в кавычках)"},
            ]),
            interview_questions([
                {"q": "Чем `is` отличается от `==`?",
                 "a": "`==` сравнивает значения, `is` — идентичность объектов (один ли объект в памяти)."},
                {"q": "Что такое динамическая типизация?",
                 "a": "Тип определяется во время выполнения, а не объявляется. Переменной можно присвоить сначала число, потом строку."},
            ]),
            knowledge_checklist([
                "Знаю 5 базовых типов Python",
                "Создаю переменные и присваиваю значения",
                "Понимаю разницу между int и float",
                "Использую f-строки для вывода",
                "Знаю, что type() возвращает тип объекта",
            ]),
        ],
        exercises=[
            ex(1, "python", "Создай переменную `rocket` со значением 'Saturn V' (тип str).",
               "# Создай переменную rocket\n",
               "rocket = 'Saturn V'",
               [{"check": "isinstance(rocket, str)", "msg": "rocket должен быть строкой"},
                {"check": "rocket == 'Saturn V'", "msg": "Значение должно быть 'Saturn V'"}],
               ["Используй = для присваивания", "Значение в кавычках — str"], 1),
            ex(2, "python", "Создай `speed` — целое число 7900 (первая космическая, м/с).",
               "speed = 0\n",
               "speed = 7900",
               [{"check": "isinstance(speed, int) and not isinstance(speed, bool)", "msg": "speed — int (не bool)"},
                {"check": "speed == 7900", "msg": "Значение 7900"},
                {"check": "speed > 0", "msg": "Скорость положительная"}],
               ["int — целое число, без точки", "Первая космическая ≈ 7900 м/с"], 1),
            ex(3, "python", "Создай `pi` = 3.14159 (дробное). Выведи её тип.",
               "pi = 0\n",
               "pi = 3.14159\nprint(type(pi).__name__)",
               [{"check": "isinstance(pi, float)", "msg": "pi — float"},
                {"check": "abs(pi - 3.14159) < 1e-6", "msg": "Значение 3.14159"}],
               ["Точка в числе делает его float", "type(pi).__name__ вернёт 'float'"], 1),
            ex(4, "python", "Создай `launched` = True (логическое значение).",
               "launched = False\n",
               "launched = True",
               [{"check": "isinstance(launched, bool)", "msg": "launched — bool"},
                {"check": "launched is True", "msg": "Значение True"}],
               ["True/False пишутся с большой буквы", "Без кавычек — bool"], 1),
            ex(5, "python", "Создай `mission` = None (миссия не определена).",
               "mission = ''\n",
               "mission = None",
               [{"check": "mission is None", "msg": "mission — None"}],
               ["None пишется с большой буквы", "None = отсутствие значения"], 1),
            ex(6, "python", "Переприсвой `counter`: 0, потом 100, потом 'готово'.",
               "counter = 0\n",
               "counter = 0\ncounter = 100\ncounter = 'готово'",
               [{"check": "counter == 'готово'", "msg": "В конце counter — 'готово'"}],
               ["Тип переменной может меняться", "Последнее присваивание побеждает"], 2),
            ex(7, "python", "Создай `planet`='Mars', `dist`=225, `habitable`=False. Выведи одной f-строкой.",
               "# Три переменные и f-string\n",
               "planet = 'Mars'\ndist = 225\nhabitable = False\nprint(f'{planet}: {dist} млн км, обитаема: {habitable}')",
               [{"check": "planet == 'Mars' and dist == 225 and habitable is False",
                 "msg": "Все три значения правильные"}],
               ["f'...{var}' подставляет значение", "Фигурные скобки {} обязательны"], 2),
            ex(8, "python", "Преобразуй строку '42' в целое число, сохрани в `n`.",
               "n = 0\n",
               "n = int('42')",
               [{"check": "isinstance(n, int) and not isinstance(n, str)", "msg": "n — int, не str"},
                {"check": "n == 42", "msg": "Значение 42"}],
               ["int() преобразует строку в число", "int('42') = 42"], 2),
        ],
        minutes=40, difficulty=1,
    )


def _1_2():
    return lesson(
        "1.2", "Условия и ветвления", "space", [
            theory(
                "**Условия** позволяют выполнять код по-разному в зависимости от данных.\n\n"
                "Ключевые слова: `if` (если), `elif` (иначе если), `else` (иначе).\n\n"
                "**Сравнения:** `==`, `!=`, `>`, `<`, `>=`, `<=`\n"
                "**Логика:** `and`, `or`, `not`\n\n"
                "**Важно:** отступы (4 пробела) — часть синтаксиса."
            ),
            analogy(
                "Условие — светофор: красный стой, жёлтый готовься, зелёный езжай.",
                "Если скорость ракеты > 7900 м/с — она вышла на орбиту, иначе — нет."
            ),
            example(
                "Определи статус ракеты по высоте: <100 км — 'на земле', 100-1000 — 'в атмосфере', >1000 — 'в космосе'.",
                "Цепочка if/elif/else. Каждая ветка — блок кода с отступом.",
                "altitude_km = 450\n\n"
                "if altitude_km < 100:\n"
                "    status = 'на земле'\n"
                "elif altitude_km < 1000:\n"
                "    status = 'в атмосфере'\n"
                "else:\n"
                "    status = 'в космосе'\n\n"
                "print(f'{altitude_km} км — {status}')",
                "450 км — в атмосфере",
                "450 < 100? Нет. 450 < 1000? Да → 'в атмосфере'."
            ),
            common_mistakes([
                {"mistake": "if x = 5:", "why_bad": "= — присваивание, нужно ==", "fix": "if x == 5:"},
                {"mistake": "Нет отступа после if", "why_bad": "IndentationError", "fix": "4 пробела перед кодом внутри if"},
            ]),
            interview_questions([
                {"q": "Разница между `if x:` и `if x is True:`?",
                 "a": "`if x:` срабатывает на любое правдивое значение (не 0, не '', не None). `if x is True:` — только на сам объект True."},
                {"q": "Что такое truthy и falsy?",
                 "a": "Falsy: 0, 0.0, '', [], {}, None, False. Всё остальное — truthy. Python приводит к bool в условии."},
            ]),
            knowledge_checklist([
                "Пишу if/elif/else с правильными отступами",
                "Знаю 6 операторов сравнения",
                "Использую and/or/not",
                "Понимаю разницу между = и ==",
                "Знаю falsy значения",
            ]),
        ],
        exercises=[
            ex(1, "python", "Дана `v = 7900`. Если v >= 7900, `orbit = True`, иначе `False`.",
               "v = 7900\norbit = None\n",
               "v = 7900\norbit = v >= 7900",
               [{"check": "isinstance(orbit, bool)", "msg": "orbit — bool"},
                {"check": "orbit is True", "msg": "orbit = True (v=7900 выполняет >=)"}],
               ["Сравнение возвращает bool", "v >= 7900 уже даёт True/False"], 1),
            ex(2, "python", "Дана `t = 3500`. t<3000 → 'норма', <4000 → 'горячо', иначе 'перегрев'. Сохрани в `status`.",
               "t = 3500\nstatus = ''\n",
               "t = 3500\nif t < 3000:\n    status = 'норма'\nelif t < 4000:\n    status = 'горячо'\nelse:\n    status = 'перегрев'",
               [{"check": "status == 'горячо'", "msg": "При t=3500 статус 'горячо'"}],
               ["elif, не else if", "3500<3000? Нет. 3500<4000? Да → 'горячо'"], 2),
            ex(3, "python", "Дан `age = 25`. Если age>=18 И age<65, `can_be_astronaut = True`, иначе `False`.",
               "age = 25\ncan_be_astronaut = False\n",
               "age = 25\ncan_be_astronaut = age >= 18 and age < 65",
               [{"check": "can_be_astronaut is True", "msg": "can_be_astronaut = True"}],
               ["and — оба True", "Можно записать одной строкой"], 2),
            ex(4, "python", "Дан `score = 85`. >=90 → 'A', 80-89 → 'B', 70-79 → 'C', иначе 'F'. Сохрани в `grade`.",
               "score = 85\ngrade = ''\n",
               "score = 85\nif score >= 90:\n    grade = 'A'\nelif score >= 80:\n    grade = 'B'\nelif score >= 70:\n    grade = 'C'\nelse:\n    grade = 'F'",
               [{"check": "grade == 'B'", "msg": "При score=85 grade='B'"}],
               ["Проверяем сверху вниз", "85>=90? Нет. 85>=80? Да → 'B'"], 2),
            ex(5, "python", "Дан `callsign = 'Apollo 11'`. Если начинается с 'Apollo', `is_apollo = True`.",
               "callsign = 'Apollo 11'\nis_apollo = False\n",
               "callsign = 'Apollo 11'\nis_apollo = callsign.startswith('Apollo')",
               [{"check": "is_apollo is True", "msg": "is_apollo = True"}],
               ["str.startswith() проверяет начало", "Метод возвращает bool"], 2),
            ex(6, "python", "Дан `a=10, b=20, c=15`. Найди максимум, сохрани в `mx`.",
               "a, b, c = 10, 20, 15\nmx = 0\n",
               "a, b, c = 10, 20, 15\nmx = max(a, b, c)",
               [{"check": "mx == 20", "msg": "mx = 20"}],
               ["max() встроенная функция", "Или через if/elif"], 1),
            ex(7, "python", "Дан `n = -5`. Тернарный оператор: `sign` = 'positive' если n>0, иначе 'non-positive'.",
               "n = -5\nsign = ''\n",
               "n = -5\nsign = 'positive' if n > 0 else 'non-positive'",
               [{"check": "sign == 'non-positive'", "msg": "При n=-5 sign = 'non-positive'"}],
               ["Тернарный: A if cond else B", "Всё в одну строку"], 3),
            ex(8, "python", "Дан `year = 2024`. Високосный ли? Сохрани bool в `is_leap` (делится на 4 И не на 100) ИЛИ делится на 400.",
               "year = 2024\nis_leap = False\n",
               "year = 2024\nis_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)",
               [{"check": "is_leap is True", "msg": "2024 — високосный"}],
               ["% — остаток от деления", "Скобки задают приоритет"], 3),
        ],
        minutes=45, difficulty=2,
    )


def _1_3():
    return lesson(
        "1.3", "Циклы и итерации", "space", [
            theory(
                "**Циклы** — способ повторять код много раз.\n\n"
                "**`for`** — перебирает элементы:\n"
                "```python\nfor i in range(5):\n    print(i)  # 0, 1, 2, 3, 4\n```\n\n"
                "**`while`** — повторяет, пока условие истинно:\n"
                "```python\nn = 0\nwhile n < 3:\n    print(n)\n    n += 1\n```\n\n"
                "**`break`** — выход из цикла. **`continue`** — пропуск итерации."
            ),
            analogy(
                "Цикл — конвейер: каждую минуту сходит деталь. for — фиксированное число, while — пока не остановим.",
                "Для каждого спутника в группировке выведи его орбиту."
            ),
            example(
                "Выведи обратный отсчёт перед запуском: 5, 4, 3, 2, 1, 'Пуск!'.",
                "range(5, 0, -1) — от 5 до 1 с шагом -1. range не включает правую границу.",
                "for i in range(5, 0, -1):\n    print(i)\nprint('Пуск!')",
                "5\n4\n3\n2\n1\nПуск!",
                "range(start, stop, step) — числа от start до stop (не включая) с шагом step."
            ),
            common_mistakes([
                {"mistake": "Бесконечный while True: без break", "why_bad": "Программа зависнет", "fix": "Добавь условие выхода"},
                {"mistake": "for i in range(10): — ожидание 1..10", "why_bad": "range(10) = 0..9", "fix": "range(1, 11) даст 1..10"},
            ]),
            interview_questions([
                {"q": "В чём разница между for и while?",
                 "a": "for — когда известно число итераций или нужно перебрать коллекцию. while — когда число итераций неизвестно и зависит от условия."},
                {"q": "Что делает range()?",
                 "a": "Возвращает последовательность чисел: range(stop), range(start, stop), range(start, stop, step). Не включает stop. Ленивая."},
            ]),
            knowledge_checklist([
                "Использую for с range и коллекциями",
                "Использую while с условием",
                "Знаю break и continue",
                "Делаю вложенные циклы",
                "Понимаю ленивость range",
            ]),
        ],
        exercises=[
            ex(1, "python", "Выведи числа от 1 до 5 (включительно), каждое на новой строке. Используй for и range.",
               "for i in range(1, 6):\n    print(i)\n",
               "for i in range(1, 6):\n    print(i)",
               [{"check": "sum(1 for _ in _printed_output.split('\\n') if _.strip().isdigit()) >= 5", "msg": "5 чисел в выводе"}],
               ["range(1,6) даёт 1..5", "print без end добавляет перенос"], 1),
            ex(2, "python", "Дан `planets = ['Mercury', 'Venus', 'Earth', 'Mars']`. Выведи каждую в формате 'Планета: X'.",
               "planets = ['Mercury', 'Venus', 'Earth', 'Mars']\n",
               "planets = ['Mercury', 'Venus', 'Earth', 'Mars']\nfor p in planets:\n    print(f'Планета: {p}')",
               [{"check": "'Mercury' in _printed_output and 'Mars' in _printed_output", "msg": "Все планеты в выводе"}],
               ["for p in list — перебор", "f-string подставляет значение"], 1),
            ex(3, "python", "Посчитай сумму чисел от 1 до 100. Сохрани в `s`.",
               "s = 0\n",
               "s = 0\nfor i in range(1, 101):\n    s += i",
               [{"check": "s == 5050", "msg": "1+2+...+100 = 5050"}],
               ["s += i добавляет i", "range(1, 101) даёт 1..100"], 2),
            ex(4, "python", "Дан `speeds = [7800, 7900, 8000, 7500, 11200]`. Посчитай, сколько >= 7900. Сохрани в `count`.",
               "speeds = [7800, 7900, 8000, 7500, 11200]\ncount = 0\n",
               "speeds = [7800, 7900, 8000, 7500, 11200]\ncount = sum(1 for v in speeds if v >= 7900)",
               [{"check": "count == 3", "msg": "Три значения ≥ 7900: 7900, 8000, 11200"}],
               ["sum с генератором", "if v >= 7900 фильтрует"], 2),
            ex(5, "python", "Дан `n = 5`. Используя while, вычисли факториал n. Сохрани в `fact`.",
               "n = 5\nfact = 1\n",
               "n = 5\nfact = 1\ni = 1\nwhile i <= n:\n    fact *= i\n    i += 1",
               [{"check": "fact == 120", "msg": "5! = 120"}],
               ["fact *= i умножает", "Начинай fact = 1, не 0"], 2),
            ex(6, "python", "Дан `nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]`. Создай `evens` — только чётные. Используй цикл.",
               "nums = list(range(1, 11))\nevens = []\n",
               "nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\nevens = []\nfor n in nums:\n    if n % 2 == 0:\n        evens.append(n)",
               [{"check": "evens == [2, 4, 6, 8, 10]", "msg": "Чётные: 2,4,6,8,10"}],
               ["n % 2 == 0 — чётное", ".append() добавляет"], 2),
            ex(7, "python", "Дан `data = [10, -5, 0, 3, -1, 8, -2]`. Используя continue, посчитай сумму положительных (включая 0). Сохрани в `pos_sum`.",
               "data = [10, -5, 0, 3, -1, 8, -2]\npos_sum = 0\n",
               "data = [10, -5, 0, 3, -1, 8, -2]\npos_sum = 0\nfor v in data:\n    if v < 0:\n        continue\n    pos_sum += v",
               [{"check": "pos_sum == 21", "msg": "10+0+3+8 = 21"}],
               ["continue пропускает итерацию", "0 считается неотрицательным (v<0 ловит только отрицательные)"], 2),
            ex(8, "python", "Дан `mysteries = [3, 7, 11, 13, 17, 19, 23]`. Найди первое число > 15, остановись. Сохрани в `found`.",
               "mysteries = [3, 7, 11, 13, 17, 19, 23]\nfound = None\n",
               "mysteries = [3, 7, 11, 13, 17, 19, 23]\nfound = None\nfor v in mysteries:\n    if v > 15:\n        found = v\n        break",
               [{"check": "found == 17", "msg": "Первое >15 — 17"}],
               ["break выходит сразу", "Без break цикл шёл бы до конца"], 2),
        ],
        minutes=50, difficulty=2,
    )


def _1_4():
    return lesson(
        "1.4", "Функции", "space", [
            theory(
                "**Функция** — именованный блок кода, который можно вызывать много раз.\n\n"
                "```python\ndef имя(аргументы):\n    # тело\n    return результат\n```\n\n"
                "**Аргументы** — входные данные. **return** — результат. "
                "Функция без return возвращает None.\n\n"
                "**Виды аргументов:**\n"
                "- Позиционные: `def f(x, y)`\n"
                "- С дефолтом: `def f(x, y=10)`\n"
                "- Именованные при вызове: `f(y=5, x=1)`"
            ),
            analogy(
                "Функция — кулинарный рецепт: ингредиенты = аргументы, готовка = тело, блюдо = return.",
                "Функция calc_fuel(altitude, mass) принимает высоту и массу, возвращает расход топлива."
            ),
            example(
                "Создай функцию escape_velocity(planet) для Марса, Луны, Земли.",
                "Словарь внутри функции — быстрый поиск. Если планеты нет — возвращаем None.",
                "def escape_velocity(planet):\n"
                "    velocities = {\n"
                "        'Earth': 11.19, 'Mars': 5.03, 'Moon': 2.38\n"
                "    }\n"
                "    return velocities.get(planet)\n\n"
                "print(escape_velocity('Mars'))",
                "5.03",
                "Словарный метод .get() возвращает None, если ключа нет — безопаснее, чем [ ]."
            ),
            common_mistakes([
                {"mistake": "Забыл return", "why_bad": "Функция всегда возвращает None", "fix": "Добавь return"},
                {"mistake": "def f(x=1, y):", "why_bad": "Не-дефолтный после дефолтного → SyntaxError", "fix": "Сначала без дефолтов: def f(y, x=1)"},
            ]),
            interview_questions([
                {"q": "Чем отличаются параметры и аргументы?",
                 "a": "Параметры — имена в определении (def f(x)). Аргументы — фактические значения при вызове (f(5))."},
                {"q": "Что такое *args и **kwargs?",
                 "a": "*args — произвольное число позиционных (кортеж). **kwargs — именованных (словарь)."},
            ]),
            knowledge_checklist([
                "Определяю функции через def",
                "Возвращаю результат через return",
                "Использую аргументы по умолчанию",
                "Понимаю область видимости",
                "Пишу docstring",
            ]),
        ],
        exercises=[
            ex(1, "python", "Создай функцию `greet(name)`, возвращающую 'Привет, {name}!'.",
               "def greet(name):\n    pass\n",
               "def greet(name):\n    return f'Привет, {name}!'",
               [{"check": "greet('Космонавт') == 'Привет, Космонавт!'", "msg": "greet('Космонавт') = 'Привет, Космонавт!'"}],
               ["return возвращает значение", "f-string для подстановки"], 1),
            ex(2, "python", "Создай функцию `square(x)`, возвращающую квадрат числа.",
               "def square(x):\n    pass\n",
               "def square(x):\n    return x ** 2",
               [{"check": "square(5) == 25", "msg": "square(5) = 25"},
                {"check": "square(-3) == 9", "msg": "square(-3) = 9"}],
               ["x ** 2 или x * x", "return, не print"], 1),
            ex(3, "python", "Создай функцию `celsius_to_kelvin(c)`, переводящую Цельсий в Кельвины (K = C + 273.15).",
               "def celsius_to_kelvin(c):\n    pass\n",
               "def celsius_to_kelvin(c):\n    return c + 273.15",
               [{"check": "abs(celsius_to_kelvin(0) - 273.15) < 0.01", "msg": "0°C = 273.15K"},
                {"check": "abs(celsius_to_kelvin(100) - 373.15) < 0.01", "msg": "100°C = 373.15K"}],
               ["return c + 273.15", "Простая формула"], 1),
            ex(4, "python", "Создай функцию `is_palindrome(s)`, возвращающую True, если строка — палиндром (без учёта регистра).",
               "def is_palindrome(s):\n    pass\n",
               "def is_palindrome(s):\n    s = s.lower()\n    return s == s[::-1]",
               [{"check": "is_palindrome('level') is True", "msg": "'level' — палиндром"},
                {"check": "is_palindrome('Level') is True", "msg": "Регистр не важен"},
                {"check": "is_palindrome('hello') is False", "msg": "'hello' — не палиндром"}],
               ["s[::-1] переворачивает", ".lower() убирает регистр"], 3),
            ex(5, "python", "Создай функцию `power(base, exp=2)`. По умолчанию — квадрат.",
               "def power(base, exp=2):\n    pass\n",
               "def power(base, exp=2):\n    return base ** exp",
               [{"check": "power(3) == 9", "msg": "power(3) = 9"},
                {"check": "power(2, 5) == 32", "msg": "power(2, 5) = 32"}],
               ["def f(x, y=2) — дефолт", "** — степень"], 2),
            ex(6, "python", "Создай `safe_div(a, b)`, возвращающую a/b, а если b==0 — None.",
               "def safe_div(a, b):\n    pass\n",
               "def safe_div(a, b):\n    if b == 0:\n        return None\n    return a / b",
               [{"check": "safe_div(10, 2) == 5.0", "msg": "10/2 = 5.0"},
                {"check": "safe_div(5, 0) is None", "msg": "Деление на 0 → None"}],
               ["if b == 0: return None", "Не забудь двоеточие"], 2),
            ex(7, "python", "Создай `list_stats(numbers)`, возвращающую кортеж (min, max, sum).",
               "def list_stats(numbers):\n    pass\n",
               "def list_stats(numbers):\n    return (min(numbers), max(numbers), sum(numbers))",
               [{"check": "list_stats([1, 2, 3, 4, 5]) == (1, 5, 15)", "msg": "(1, 5, 15) для [1..5]"}],
               ["min, max, sum — встроенные", "Возвращай кортеж в скобках"], 2),
            ex(8, "python", "Создай `filter_positive(nums)`, возвращающую список неотрицательных (≥0).",
               "def filter_positive(nums):\n    pass\n",
               "def filter_positive(nums):\n    return [n for n in nums if n >= 0]",
               [{"check": "filter_positive([-1, 0, 5, -3, 2]) == [0, 5, 2]", "msg": "[-1,0,5,-3,2] → [0,5,2]"}],
               ["List comprehension: [... for ... if ...]", "0 — неотрицательное"], 3),
            ex(9, "python", "Создай `fibonacci(n)`, возвращающую список первых n чисел Фибоначчи (с 0, 1).",
               "def fibonacci(n):\n    pass\n",
               "def fibonacci(n):\n    result = [0, 1]\n    while len(result) < n:\n        result.append(result[-1] + result[-2])\n    return result[:n]",
               [{"check": "fibonacci(8) == [0, 1, 1, 2, 3, 5, 8, 13]", "msg": "fibonacci(8)"},
                {"check": "fibonacci(1) == [0]", "msg": "fibonacci(1) = [0]"}],
               ["result[-1]+result[-2] — следующее", "result[:n] на случай n<2"], 3),
            ex(10, "python", "Создай `count_words(text)`, возвращающую {слово: кол-во}. Регистр не учитывай.",
               "def count_words(text):\n    pass\n",
               "def count_words(text):\n    words = text.lower().split()\n    counts = {}\n    for w in words:\n        counts[w] = counts.get(w, 0) + 1\n    return counts",
               [{"check": "count_words('Mars Mars Earth') == {'mars': 2, 'earth': 1}", "msg": "Словарь счётчиков"}],
               [".split() разбивает", ".get(w, 0) → 0 если нет ключа"], 3),
        ],
        minutes=60, difficulty=3,
    )


LESSONS = [_1_1, _1_2, _1_3, _1_4]
