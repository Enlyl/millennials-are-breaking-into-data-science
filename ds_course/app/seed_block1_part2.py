"""
Блок 1, часть 2: уроки 1.5-1.8
"""
from app.seed_helpers import (
    ex, lesson, theory, analogy, visual, example,
    common_mistakes, interview_questions, knowledge_checklist,
)


def _1_5():
    return lesson(
        "1.5", "Списки и операции над ними", "space", [
            theory(
                "**Список (list)** — упорядоченная изменяемая коллекция.\n\n"
                "```python\nmissions = ['Apollo 11', 'Apollo 12', 'Soyuz 1']\n"
                "missions[0]          # 'Apollo 11'\n"
                "missions[-1]         # 'Soyuz 1' (с конца)\n"
                "missions.append('Artemis 1')\n"
                "missions.insert(1, 'Vostok 1')\n"
                "missions[1:3]        # срез [1, 3)\n"
                "len(missions)        # длина\n```\n\n"
                "**Срезы** `[start:stop:step]` — мощный инструмент. `[::-1]` разворачивает."
            ),
            analogy(
                "Список — полка с пронумерованными ящиками: можно положить (append), убрать (remove), достать по номеру.",
                "Список missions хранит названия космических миссий в порядке запуска."
            ),
            example(
                "Дан список температур двигателя за минуту. Найди среднее, максимум и кол-во превышений 3000°C.",
                "Используем sum/len, max и sum с условием для подсчёта.",
                "temps = [2800, 2950, 3100, 3050, 2900, 3200, 2850]\n"
                "avg = sum(temps) / len(temps)\n"
                "mx = max(temps)\n"
                "overheat = sum(1 for t in temps if t > 3000)\n"
                "print(f'Средняя: {avg:.0f}, Макс: {mx}, Перегревов: {overheat}')",
                "Средняя: 2979, Макс: 3200, Перегревов: 3",
                "f'{avg:.0f}' округляет до целого. sum(1 for ...) — короткий способ подсчёта."
            ),
            common_mistakes([
                {"mistake": "lst[10] когда в списке 3 элемента", "why_bad": "IndexError", "fix": "Проверяй длину"},
                {"mistake": "lst = lst.sort()", "why_bad": "sort() возвращает None, lst станет None", "fix": "lst.sort() или sorted(lst)"},
                {"mistake": "lst1 = lst2 — копия ссылки", "why_bad": "Изменения lst2 затронут lst1", "fix": "lst1 = lst2[:] или lst2.copy()"},
            ]),
            interview_questions([
                {"q": "Разница между list и tuple?",
                 "a": "list изменяемый, tuple — нет. Tuple быстрее, может быть ключом словаря."},
                {"q": "list.sort() vs sorted(list)?",
                 "a": "list.sort() меняет на месте, возвращает None. sorted(list) возвращает новый список, оригинал не меняется."},
            ]),
            knowledge_checklist([
                "Создаю списки, индексирую, делаю срезы",
                "Добавляю/удаляю: append, insert, remove, pop",
                "Использую len, min, max, sum",
                "Сортирую: sort() и sorted()",
                "Понимаю мутабельность",
            ]),
        ],
        exercises=[
            ex(1, "python", "Создай список `planets` из 4 планет: 'Mercury', 'Venus', 'Earth', 'Mars'.",
               "planets = []\n",
               "planets = ['Mercury', 'Venus', 'Earth', 'Mars']",
               [{"check": "planets == ['Mercury', 'Venus', 'Earth', 'Mars']", "msg": "Список в указанном порядке"}],
               ["Элементы в скобках через запятую", "Строки в кавычках"], 1),
            ex(2, "python", "Дан `planets = ['Mercury', 'Venus', 'Earth', 'Mars']`. Сохрани в `first` первый, в `last` — последний.",
               "planets = ['Mercury', 'Venus', 'Earth', 'Mars']\nfirst = ''\nlast = ''\n",
               "planets = ['Mercury', 'Venus', 'Earth', 'Mars']\nfirst = planets[0]\nlast = planets[-1]",
               [{"check": "first == 'Mercury'", "msg": "first = 'Mercury'"},
                {"check": "last == 'Mars'", "msg": "last = 'Mars'"}],
               ["Индекс 0 — первый", "-1 — последний"], 1),
            ex(3, "python", "Дан `nums = [10, 20, 30, 40, 50]`. Создай `sliced` — элементы с индексами 1, 2, 3.",
               "nums = [10, 20, 30, 40, 50]\nsliced = []\n",
               "nums = [10, 20, 30, 40, 50]\nsliced = nums[1:4]",
               [{"check": "sliced == [20, 30, 40]", "msg": "sliced = [20, 30, 40]"}],
               ["Срез [1:4] — от 1 до 4 не включая", "Это индексы 1, 2, 3"], 2),
            ex(4, "python", "Дан список `missions = []`. Добавь 'Apollo 11', 'Apollo 12', 'Apollo 13'. Выведи длину.",
               "missions = []\n",
               "missions = []\nmissions.append('Apollo 11')\nmissions.append('Apollo 12')\nmissions.append('Apollo 13')\nprint(len(missions))",
               [{"check": "missions == ['Apollo 11', 'Apollo 12', 'Apollo 13']", "msg": "3 миссии"},
                {"check": "'3' in _printed_output", "msg": "Выведена длина 3"}],
               [".append() в конец", "len() возвращает длину"], 1),
            ex(5, "python", "Дан `nums = [3, 1, 4, 1, 5, 9, 2, 6]`. Отсортируй по возрастанию (на месте).",
               "nums = [3, 1, 4, 1, 5, 9, 2, 6]\n",
               "nums = [3, 1, 4, 1, 5, 9, 2, 6]\nnums.sort()",
               [{"check": "nums == [1, 1, 2, 3, 4, 5, 6, 9]", "msg": "Отсортирован"}],
               [".sort() меняет на месте", "sorted() вернул бы новый"], 2),
            ex(6, "python", "Дан `nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]`. Создай `squared` — список квадратов.",
               "nums = list(range(1, 11))\nsquared = []\n",
               "nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\nsquared = [n ** 2 for n in nums]",
               [{"check": "squared == [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]", "msg": "Квадраты 1..10"}],
               ["List comprehension: [n**2 for n in nums]", "Или цикл с append"], 2),
            ex(7, "python", "Даны `a = [1, 2, 3]` и `b = [4, 5, 6]`. Создай `c` — их конкатенацию.",
               "a = [1, 2, 3]\nb = [4, 5, 6]\nc = []\n",
               "a = [1, 2, 3]\nb = [4, 5, 6]\nc = a + b",
               [{"check": "c == [1, 2, 3, 4, 5, 6]", "msg": "c = [1..6]"}],
               ["+ склеивает списки", "Или a.extend(b)"], 1),
            ex(8, "python", "Дан `telemetry = [12.5, 13.1, 12.8, 14.2, 13.5, 12.0]`. Вычисли среднее, сохрани в `avg`.",
               "telemetry = [12.5, 13.1, 12.8, 14.2, 13.5, 12.0]\navg = 0\n",
               "telemetry = [12.5, 13.1, 12.8, 14.2, 13.5, 12.0]\navg = sum(telemetry) / len(telemetry)",
               [{"check": "abs(avg - 13.0166) < 0.01", "msg": "Среднее ≈ 13.02"}],
               ["sum() / len()", "Или statistics.mean()"], 2),
            ex(9, "python", "Дан `nums = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]`. Посчитай, сколько раз встречается 3, сохрани в `count_3`.",
               "nums = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]\ncount_3 = 0\n",
               "nums = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]\ncount_3 = nums.count(3)",
               [{"check": "count_3 == 3", "msg": "3 встречается 3 раза"}],
               ["list.count(x) считает", "Возвращает int"], 2),
            ex(10, "python", "Дан `data = [5, 2, 8, 1, 9, 3]`. Найди индекс максимального элемента, сохрани в `idx_max`.",
               "data = [5, 2, 8, 1, 9, 3]\nidx_max = -1\n",
               "data = [5, 2, 8, 1, 9, 3]\nidx_max = data.index(max(data))",
               [{"check": "idx_max == 4", "msg": "9 на индексе 4"}],
               ["max(data) — наибольшее", ".index() — позиция"], 2),
        ],
        minutes=50, difficulty=2,
    )


def _1_6():
    return lesson(
        "1.6", "Словари", "space", [
            theory(
                "**Словарь (dict)** — коллекция пар ключ:значение.\n\n"
                "```python\nrocket = {'name': 'Falcon 9', 'mass_kg': 549054, 'stages': 2}\n"
                "rocket['name']            # 'Falcon 9'\n"
                "rocket.get('payload', 0)  # безопасно, default 0\n"
                "rocket.keys()             # все ключи\n"
                "rocket.values()           # все значения\n"
                "rocket.items()            # пары (key, value)\n```\n\n"
                "**Важно:** ключи должны быть иммутабельными (строки, числа, кортежи)."
            ),
            analogy(
                "Словарь — записная книжка: имя → телефон. Имя уникально (ключ), телефон может меняться (значение).",
                "Словарь mission_params = {'target': 'Mars', 'duration_days': 210, 'crew_size': 4}."
            ),
            example(
                "Создай словарь с информацией о планете и выведи каждый параметр.",
                "Используем .items() для перебора пар.",
                "planet = {'name': 'Mars', 'mass': 6.4e23, 'moons': 2, 'atmosphere': True}\n\n"
                "for key, value in planet.items():\n    print(f'{key}: {value}')",
                "name: Mars\nmass: 6.4e+23\nmoons: 2\natmosphere: True",
                ".items() возвращает пары (key, value) — удобно для цикла."
            ),
            common_mistakes([
                {"mistake": "d['key'] когда ключа нет", "why_bad": "KeyError", "fix": "d.get('key', default)"},
                {"mistake": "Ключ-список: {[1, 2]: 'a'}", "why_bad": "TypeError: unhashable", "fix": "Кортеж: {(1, 2): 'a'}"},
            ]),
            interview_questions([
                {"q": "Как работает dict под капотом?",
                 "a": "Python вычисляет hash(key), берёт остаток от деления на размер таблицы — это индекс корзины. Поиск O(1)."},
                {"q": "Что быстрее: dict.get() или dict[key] с try/except?",
                 "a": "При отсутствии ключа — get() быстрее, потому что не создаёт исключение."},
            ]),
            knowledge_checklist([
                "Создаю словари с разными типами значений",
                "Получаю значение через [] и .get()",
                "Добавляю и удаляю ключи",
                "Перебираю через keys/values/items",
                "Понимаю, какие объекты могут быть ключами",
            ]),
        ],
        exercises=[
            ex(1, "python", "Создай словарь `rocket` с ключами 'name'='Falcon 9' и 'stages'=2.",
               "rocket = {}\n",
               "rocket = {'name': 'Falcon 9', 'stages': 2}",
               [{"check": "rocket['name'] == 'Falcon 9'", "msg": "name = 'Falcon 9'"},
                {"check": "rocket['stages'] == 2", "msg": "stages = 2"}],
               ["Фигурные скобки и двоеточие", "Ключ в кавычках"], 1),
            ex(2, "python", "Дан `mission = {'target': 'Mars', 'year': 2024}`. Получи и сохрани в `target` значение по ключу 'target'.",
               "mission = {'target': 'Mars', 'year': 2024}\ntarget = ''\n",
               "mission = {'target': 'Mars', 'year': 2024}\ntarget = mission['target']",
               [{"check": "target == 'Mars'", "msg": "target = 'Mars'"}],
               ["d['key'] — доступ по ключу", "Если ключа нет — KeyError"], 1),
            ex(3, "python", "Дан `crew = {'commander': 'Олег', 'pilot': 'Анна'}`. Используя .get(), получи 'engineer' с дефолтом 'Неизвестно'. Сохрани в `eng`.",
               "crew = {'commander': 'Олег', 'pilot': 'Анна'}\neng = ''\n",
               "crew = {'commander': 'Олег', 'pilot': 'Анна'}\neng = crew.get('engineer', 'Неизвестно')",
               [{"check": "eng == 'Неизвестно'", "msg": "Дефолт сработал"}],
               [".get(key, default) безопаснее []", "Возвращает default, если ключа нет"], 1),
            ex(4, "python", "Дан пустой словарь `d = {}`. Добавь 'speed'=7900, затем обнови до 11200. Финальное в `final`.",
               "d = {}\nfinal = 0\n",
               "d = {}\nd['speed'] = 7900\nd['speed'] = 11200\nfinal = d['speed']",
               [{"check": "final == 11200", "msg": "Финальное 11200"}],
               ["d[key] = value", "Присваивание существующему обновляет"], 2),
            ex(5, "python", "Дан `speeds = {'earth': 11.19, 'mars': 5.03, 'moon': 2.38}`. Среднее всех значений, сохрани в `avg`.",
               "speeds = {'earth': 11.19, 'mars': 5.03, 'moon': 2.38}\navg = 0\n",
               "speeds = {'earth': 11.19, 'mars': 5.03, 'moon': 2.38}\navg = sum(speeds.values()) / len(speeds)",
               [{"check": "abs(avg - 6.2) < 0.1", "msg": "Среднее ≈ 6.2"}],
               [".values() — все значения", "sum() / len()"], 2),
            ex(6, "python", "Дан `planets = {'Earth': 1, 'Mars': 2}`. Добавь 'Jupiter' = 3. Сохрани `len(planets)` в `n`.",
               "planets = {'Earth': 1, 'Mars': 2}\nn = 0\n",
               "planets = {'Earth': 1, 'Mars': 2}\nplanets['Jupiter'] = 3\nn = len(planets)",
               [{"check": "n == 3", "msg": "3 планеты"}],
               ["d['key'] = value", "len() для словаря"], 1),
            ex(7, "python", "Дан `counts = {'a': 3, 'b': 5, 'c': 1}`. Найди ключ с максимальным значением, сохрани в `max_key`.",
               "counts = {'a': 3, 'b': 5, 'c': 1}\nmax_key = ''\n",
               "counts = {'a': 3, 'b': 5, 'c': 1}\nmax_key = max(counts, key=counts.get)",
               [{"check": "max_key == 'b'", "msg": "b имеет max 5"}],
               ["max(d, key=d.get)", "key= задаёт функцию сравнения"], 3),
            ex(8, "python", "Дан список пар `[('name', 'Apollo'), ('year', 1969)]`. Преобразуй в словарь `d`.",
               "pairs = [('name', 'Apollo'), ('year', 1969)]\nd = {}\n",
               "pairs = [('name', 'Apollo'), ('year', 1969)]\nd = dict(pairs)",
               [{"check": "d == {'name': 'Apollo', 'year': 1969}", "msg": "Словарь из пар"}],
               ["dict() принимает пары", "Или {k: v for k, v in pairs}"], 2),
            ex(9, "python", "Дан `d = {'x': 1, 'y': 2, 'z': 3}`. Создай список `keys` всех ключей и `vals` всех значений.",
               "d = {'x': 1, 'y': 2, 'z': 3}\nkeys = []\nvals = []\n",
               "d = {'x': 1, 'y': 2, 'z': 3}\nkeys = list(d.keys())\nvals = list(d.values())",
               [{"check": "set(keys) == {'x', 'y', 'z'}", "msg": "keys"},
                {"check": "set(vals) == {1, 2, 3}", "msg": "vals"}],
               [".keys() и .values() — view-объекты", "list() превращает в список"], 2),
            ex(10, "python", "Дан `users = {'alice': 25, 'bob': 17, 'carol': 30}`. Создай `adults` — только тех, кому >= 18.",
               "users = {'alice': 25, 'bob': 17, 'carol': 30}\nadults = {}\n",
               "users = {'alice': 25, 'bob': 17, 'carol': 30}\nadults = {k: v for k, v in users.items() if v >= 18}",
               [{"check": "adults == {'alice': 25, 'carol': 30}", "msg": "Совершеннолетние"}],
               ["Dict comprehension", "Аналог list comprehension"], 3),
        ],
        minutes=50, difficulty=2,
    )


def _1_7():
    return lesson(
        "1.7", "Множества и кортежи", "space", [
            theory(
                "**Множество (set)** — неупорядоченная коллекция уникальных элементов.\n\n"
                "```python\nunique = {1, 2, 3, 2, 1}  # {1, 2, 3}\n"
                "unique.add(4)\n"
                "unique.discard(5)  # безопасно, без ошибки\n```\n\n"
                "**Операции:** `a | b` объединение, `a & b` пересечение, `a - b` разность.\n\n"
                "**Кортеж (tuple)** — неизменяемый список:\n"
                "```python\npoint = (10, 20)\n"
                "x, y = point  # распаковка\n```"
            ),
            analogy(
                "Множество — клуб: участники уникальны, порядок не важен. Кортеж — фотография: зафиксированные данные, нельзя изменить.",
                "Set: уникальные ID спутников. Tuple: координаты (x, y) на карте."
            ),
            example(
                "Найди планеты, которые встречаются в обоих списках миссий.",
                "Преобразуем в set и используем & (пересечение).",
                "mission1 = ['Mars', 'Venus', 'Mars', 'Jupiter']\n"
                "mission2 = ['Mars', 'Saturn', 'Jupiter', 'Mars']\n\n"
                "common = set(mission1) & set(mission2)\nprint(f'Общие: {common}')",
                "Общие: {'Mars', 'Jupiter'}",
                "Set убирает дубликаты, & оставляет только пересечение."
            ),
            common_mistakes([
                {"mistake": "{} — это dict, не set", "why_bad": "type({}) = dict", "fix": "set() — пустое множество"},
                {"mistake": "lst[0] = 'new' для tuple", "why_bad": "TypeError", "fix": "Преобразуй в list"},
            ]),
            interview_questions([
                {"q": "Когда использовать set, а когда list?",
                 "a": "Set — для уникальности и операций | & -. List — когда важен порядок и допускаются дубли."},
                {"q": "Можно ли использовать list как ключ dict?",
                 "a": "Нет. Ключ должен быть hashable. List мутабельный → TypeError."},
            ]),
            knowledge_checklist([
                "Создаю множества и кортежи",
                "Знаю операции | & - для множеств",
                "Использую распаковку кортежей",
                "Понимаю иммутабельность кортежей",
                "Знаю, когда применять set",
            ]),
        ],
        exercises=[
            ex(1, "python", "Дан список `missions = ['Mars', 'Mars', 'Venus', 'Jupiter', 'Venus']`. Создай `unique` — множество уникальных миссий.",
               "missions = ['Mars', 'Mars', 'Venus', 'Jupiter', 'Venus']\nunique = set()\n",
               "missions = ['Mars', 'Mars', 'Venus', 'Jupiter', 'Venus']\nunique = set(missions)",
               [{"check": "unique == {'Mars', 'Venus', 'Jupiter'}", "msg": "Уникальные миссии"}],
               ["set() убирает дубли", "Порядок не гарантирован"], 1),
            ex(2, "python", "Создай кортеж `point` с координатами (10, 20, 30).",
               "point = ()\n",
               "point = (10, 20, 30)",
               [{"check": "point == (10, 20, 30)", "msg": "Кортеж из 3 элементов"},
                {"check": "isinstance(point, tuple)", "msg": "Это tuple"}],
               ["Круглые скобки и запятые", "point[0] = 1 вызовет ошибку"], 1),
            ex(3, "python", "Дан кортеж `coords = (100, 200)`. Распакуй его в `x` и `y`.",
               "coords = (100, 200)\nx = 0\ny = 0\n",
               "coords = (100, 200)\nx, y = coords",
               [{"check": "x == 100", "msg": "x = 100"},
                {"check": "y == 200", "msg": "y = 200"}],
               ["x, y = tuple — распаковка", "Количество переменных = длине"], 1),
            ex(4, "python", "Даны `a = {1, 2, 3}` и `b = {3, 4, 5}`. Создай `c` — их объединение (|).",
               "a = {1, 2, 3}\nb = {3, 4, 5}\nc = set()\n",
               "a = {1, 2, 3}\nb = {3, 4, 5}\nc = a | b",
               [{"check": "c == {1, 2, 3, 4, 5}", "msg": "Объединение = {1,2,3,4,5}"}],
               ["| — объединение", "Или a.union(b)"], 2),
            ex(5, "python", "Даны `a = {1, 2, 3}` и `b = {3, 4, 5}`. Создай `c` — их пересечение (&).",
               "a = {1, 2, 3}\nb = {3, 4, 5}\nc = set()\n",
               "a = {1, 2, 3}\nb = {3, 4, 5}\nc = a & b",
               [{"check": "c == {3}", "msg": "Только 3 общее"}],
               ["& — пересечение", "Возвращает общие"], 2),
            ex(6, "python", "Дан список `nums = [1, 2, 2, 3, 4, 4, 5, 1, 2]`. Создай `counts` — {число: кол-во}, используя set.",
               "nums = [1, 2, 2, 3, 4, 4, 5, 1, 2]\ncounts = {}\n",
               "nums = [1, 2, 2, 3, 4, 4, 5, 1, 2]\ncounts = {n: nums.count(n) for n in set(nums)}",
               [{"check": "counts[2] == 3", "msg": "2 встречается 3 раза"},
                {"check": "counts[1] == 2", "msg": "1 встречается 2 раза"}],
               ["set(nums) убирает дубли", "dict comprehension"], 3),
            ex(7, "python", "Дан кортеж `t = (5, 2, 8, 1, 9)`. Найди max и min, сохрани в `mx` и `mn`.",
               "t = (5, 2, 8, 1, 9)\nmx = 0\nmn = 0\n",
               "t = (5, 2, 8, 1, 9)\nmx = max(t)\nmn = min(t)",
               [{"check": "mx == 9", "msg": "max = 9"},
                {"check": "mn == 1", "msg": "min = 1"}],
               ["max, min работают с кортежами", "Tuple — последовательность"], 2),
            ex(8, "python", "Дан `data = [1..10]`. Преобразуй в кортеж `t`, посчитай сумму чётных.",
               "data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\nt = ()\ns = 0\n",
               "data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\nt = tuple(data)\ns = sum(x for x in t if x % 2 == 0)",
               [{"check": "isinstance(t, tuple)", "msg": "t — кортеж"},
                {"check": "s == 30", "msg": "2+4+6+8+10 = 30"}],
               ["tuple(list) — преобразование", "sum с генератором"], 3),
        ],
        minutes=35, difficulty=2,
    )


def _1_8():
    return lesson(
        "1.8", "Обработка строк", "space", [
            theory(
                "Строки в Python — иммутабельные последовательности. Богатый набор методов:\n\n"
                "```python\ns = 'Apollo 11 Launched'\n"
                "s.lower()              # 'apollo 11 launched'\n"
                "s.upper()              # 'APOLLO 11 LAUNCHED'\n"
                "s.split()              # ['Apollo', '11', 'Launched']\n"
                "s.replace('11', 'X')   # 'Apollo X Launched'\n"
                "s.startswith('A')      # True\n"
                "s.find('11')           # 7 (индекс) или -1\n"
                "','.join(['a', 'b'])   # 'a,b'\n```\n\n"
                "**f-strings** для форматирования:\n"
                "```python\nf'{name} летит на {planet}'\n"
                "f'{value:.2f}'   # 2 знака после точки\n"
                "f'{count:>5}'    # выравнивание\n```"
            ),
            analogy(
                "Строковые методы — инструменты для работы с текстом: CAPS, поиск (Ctrl+F), замена.",
                "Очистка логов: убрать пробелы, привести к нижнему регистру, разделить."
            ),
            example(
                "Обработай название миссии: приведи к нижнему регистру, замени пробелы на '_', посчитай длину.",
                "Цепочка методов: .lower().replace(' ', '_').",
                "mission = 'Apollo 11 Moon Landing'\n"
                "clean = mission.lower().replace(' ', '_')\n"
                "length = len(clean)\n"
                "print(f'{clean} (длина: {length})')",
                "apollo_11_moon_landing (длина: 23)",
                "Методы можно вызывать цепочкой — результат одного передаётся в следующий."
            ),
            common_mistakes([
                {"mistake": "s.replace(...) без s = ", "why_bad": "Строки иммутабельны", "fix": "s = s.replace(...)"},
                {"mistake": "s.find() vs s.index()", "why_bad": "find() возвращает -1, index() — ValueError", "fix": "find() для безопасной проверки"},
            ]),
            interview_questions([
                {"q": "Почему строки иммутабельны?",
                 "a": "Позволяет использовать как ключи dict и элементы set (hashable). Упрощает многопоточность."},
                {"q": "Чем f-string лучше .format()?",
                 "a": "f-строки быстрее, читабельнее, поддерживают выражения внутри {}."},
            ]),
            knowledge_checklist([
                "Использую .lower(), .upper(), .strip()",
                "split() и .join()",
                ".replace(), .startswith(), .endswith()",
                "Форматирую через f-strings",
                "Понимаю иммутабельность",
            ]),
        ],
        exercises=[
            ex(1, "python", "Дана `s = 'Hello, World!'`. Приведи к верхнему регистру, сохрани в `upper_s`.",
               "s = 'Hello, World!'\nupper_s = ''\n",
               "s = 'Hello, World!'\nupper_s = s.upper()",
               [{"check": "upper_s == 'HELLO, WORLD!'", "msg": "Все заглавные"}],
               [".upper() возвращает новую строку"], 1),
            ex(2, "python", "Дана `s = 'Apollo 11'`. Раздели по пробелу, сохрани в `parts`.",
               "s = 'Apollo 11'\nparts = []\n",
               "s = 'Apollo 11'\nparts = s.split(' ')",
               [{"check": "parts == ['Apollo', '11']", "msg": "2 элемента"}],
               [".split(' ') по пробелу"], 1),
            ex(3, "python", "Дан список `words = ['Mars', 'is', 'red']`. Собери в строку через пробел, сохрани в `s`.",
               "words = ['Mars', 'is', 'red']\ns = ''\n",
               "words = ['Mars', 'is', 'red']\ns = ' '.join(words)",
               [{"check": "s == 'Mars is red'", "msg": "Строка через пробел"}],
               ["' '.join(list)", "Разделитель — первый аргумент"], 1),
            ex(4, "python", "Дана `s = 'hello world'`. Замени 'world' на 'Mars', сохрани в `new_s`.",
               "s = 'hello world'\nnew_s = ''\n",
               "s = 'hello world'\nnew_s = s.replace('world', 'Mars')",
               [{"check": "new_s == 'hello Mars'", "msg": "Заменено"}],
               [".replace(old, new)"], 1),
            ex(5, "python", "Дана `s = '  Apollo 11  '`. Убери пробелы по краям, сохрани в `clean`.",
               "s = '  Apollo 11  '\nclean = ''\n",
               "s = '  Apollo 11  '\nclean = s.strip()",
               [{"check": "clean == 'Apollo 11'", "msg": "Без крайних пробелов"}],
               [".strip()"], 1),
            ex(6, "python", "Дана `s = 'mission-2024-mars'`. Проверь, начинается ли она с 'mission'. Сохрани bool в `result`.",
               "s = 'mission-2024-mars'\nresult = False\n",
               "s = 'mission-2024-mars'\nresult = s.startswith('mission')",
               [{"check": "result is True", "msg": "Начинается с 'mission'"}],
               [".startswith() возвращает bool"], 2),
            ex(7, "python", "Дана `s = 'Apollo 11 launched in 1969'`. Найди индекс '1969'. Сохрани в `idx`.",
               "s = 'Apollo 11 launched in 1969'\nidx = -1\n",
               "s = 'Apollo 11 launched in 1969'\nidx = s.find('1969')",
               [{"check": "idx == 22", "msg": "Индекс = 22"}],
               [".find() возвращает индекс или -1"], 2),
            ex(8, "python", "Дан список цен `[19.99, 5.50, 100.0]`. Сформируй `prices` с 2 знаками после запятой через ' | '.",
               "prices = [19.99, 5.50, 100.0]\ns = ''\n",
               "prices = [19.99, 5.50, 100.0]\ns = ' | '.join(f'{p:.2f}' for p in prices)",
               [{"check": "s == '19.99 | 5.50 | 100.00'", "msg": "Строка с 2 знаками"}],
               ["f'{p:.2f}' форматирует", "join с генератором"], 3),
            ex(9, "python", "Дана `s = '  SPACEX  '`. К нижнему регистру, без пробелов, 'space' → 'rocket'. Сохрани в `result`.",
               "s = '  SPACEX  '\nresult = ''\n",
               "s = '  SPACEX  '\nresult = s.strip().lower().replace('space', 'rocket')",
               [{"check": "result == 'rocketx'", "msg": "Конечный результат 'rocketx'"}],
               ["Цепочка: strip → lower → replace"], 2),
            ex(10, "python", "Дан текст. Посчитай количество слов, сохрани в `word_count`.",
               "text = 'Mars is the fourth planet from the Sun and the second-smallest planet in the Solar System.'\nword_count = 0\n",
               "text = 'Mars is the fourth planet from the Sun and the second-smallest planet in the Solar System.'\nword_count = len(text.split())",
               [{"check": "word_count == 17", "msg": "17 слов"}],
               ["split() по whitespace", "len() от списка"], 2),
        ],
        minutes=50, difficulty=2,
    )


LESSONS = [_1_5, _1_6, _1_7, _1_8]
