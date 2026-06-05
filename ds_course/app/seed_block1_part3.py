"""
Блок 1, часть 3: уроки 1.9-1.12
"""
from app.seed_helpers import (
    ex, lesson, theory, analogy, visual, example,
    common_mistakes, interview_questions, knowledge_checklist,
)


def _1_9():
    return lesson(
        "1.9", "Чтение и запись файлов", "space", [
            theory(
                "Python работает с файлами через `open()`.\n\n"
                "```python\n# Чтение целиком\nwith open('data.txt', 'r', encoding='utf-8') as f:\n    text = f.read()\n\n"
                "# Построчно\nwith open('data.txt') as f:\n    for line in f:\n        print(line.strip())\n\n"
                "# Запись\nwith open('out.txt', 'w', encoding='utf-8') as f:\n    f.write('Hello, Mars!')\n```\n\n"
                "**Режимы:** `'r'` чтение, `'w'` запись (перезапишет), `'a'` дозапись.\n\n"
                "**`with`** гарантирует закрытие файла даже при ошибке."
            ),
            analogy(
                "Открыть файл — открыть книгу: читать (r), писать в новую (w), добавлять страницы (a). Закрыть книгу важно — иначе потеряются данные.",
                "Запись логов телеметрии: каждую секунду добавляем строку через режим 'a'."
            ),
            example(
                "Прочитай файл missions.txt со списком миссий (по одной на строке), посчитай количество.",
                "Открываем в режиме чтения, читаем строки, считаем.",
                "with open('missions.txt', 'r', encoding='utf-8') as f:\n"
                "    lines = f.readlines()\n\n"
                "print(f'Миссий: {len(lines)}')\n"
                "print('Первая:', lines[0].strip())",
                "Миссий: 4\nПервая: Apollo 11",
                "readlines() возвращает список строк (с символами переноса). strip() убирает \\n."
            ),
            common_mistakes([
                {"mistake": "Забыл encoding='utf-8'", "why_bad": "Русский текст — кракозябры", "fix": "Всегда указывай encoding='utf-8'"},
                {"mistake": "f = open(...); f.close()", "why_bad": "Если ошибка — файл не закроется", "fix": "with open() as f:"},
                {"mistake": "'r' режим для записи", "why_bad": "UnsupportedOperation", "fix": "'w' для перезаписи, 'a' для дозаписи"},
            ]),
            interview_questions([
                {"q": "Зачем `with` при работе с файлами?",
                 "a": "Гарантирует вызов .close() даже при исключении. Реализация context manager."},
                {"q": "Text mode vs binary mode?",
                 "a": "Text — строки, декодирование utf-8. Binary — байты, без декодирования."},
            ]),
            knowledge_checklist([
                "Открываю файлы через with open()",
                "Читаю через .read() и цикл for line in f",
                "Пишу через .write() и .writelines()",
                "Знаю режимы r, w, a",
                "Всегда указываю encoding='utf-8'",
            ]),
        ],
        exercises=[
            ex(1, "python", "Открой `test.txt` для чтения и прочитай всё в переменную `content`.",
               "with open('test.txt', 'r', encoding='utf-8') as f:\n    content = ''\n",
               "with open('test.txt', 'r', encoding='utf-8') as f:\n    content = f.read()",
               [{"check": "isinstance(content, str)", "msg": "content — строка"}],
               ["with open() as f — контекстный менеджер", ".read()"], 2),
            ex(2, "python", "Открой `test.txt` для записи и запиши 'Apollo 11'.",
               "with open('test.txt', 'w', encoding='utf-8') as f:\n    pass\n",
               "with open('test.txt', 'w', encoding='utf-8') as f:\n    f.write('Apollo 11')",
               [{"check": "open('test.txt').read() == 'Apollo 11'", "msg": "Файл содержит 'Apollo 11'"}],
               ["'w' перезаписывает", ".write() пишет строку"], 2),
            ex(3, "python", "Открой `data.txt`, прочитай построчно, сохрани количество строк в `n`.",
               "with open('data.txt', 'r', encoding='utf-8') as f:\n    n = 0\n",
               "with open('data.txt', 'r', encoding='utf-8') as f:\n    n = sum(1 for _ in f)",
               [{"check": "isinstance(n, int)", "msg": "n — int"}],
               ["for _ in f — перебор строк", "sum(1 for ...)"], 2),
            ex(4, "python", "Запиши в `out.txt` числа от 1 до 5, каждое на новой строке.",
               "with open('out.txt', 'w', encoding='utf-8') as f:\n    pass\n",
               "with open('out.txt', 'w', encoding='utf-8') as f:\n    for i in range(1, 6):\n        f.write(f'{i}\\n')",
               [{"check": "open('out.txt').read().strip().split('\\n') == ['1','2','3','4','5']", "msg": "5 строк 1..5"}],
               ["f'\\n' добавляет перенос", "f-string"], 3),
            ex(5, "python", "Дан файл `log.txt` с несколькими строками. Прочитай все строки в список `lines` (с переносами).",
               "with open('log.txt', 'r', encoding='utf-8') as f:\n    lines = []\n",
               "with open('log.txt', 'r', encoding='utf-8') as f:\n    lines = f.readlines()",
               [{"check": "isinstance(lines, list)", "msg": "lines — список"},
                {"check": "all(isinstance(l, str) for l in lines)", "msg": "Элементы — строки"}],
               [".readlines() — список всех строк"], 2),
            ex(6, "python", "Открой `app.log` в режиме дозаписи ('a') и добавь 'New entry\\n'.",
               "with open('app.log', 'a', encoding='utf-8') as f:\n    pass\n",
               "with open('app.log', 'a', encoding='utf-8') as f:\n    f.write('New entry\\n')",
               [{"check": "open('app.log').read().endswith('New entry\\n')", "msg": "Файл заканчивается на 'New entry\\n'"}],
               ["'a' добавляет, не перезаписывает", ".write()"], 2),
            ex(7, "python", "Прочитай `config.json`, посчитай количество символов, сохрани в `size`.",
               "with open('config.json', 'r', encoding='utf-8') as f:\n    size = 0\n",
               "with open('config.json', 'r', encoding='utf-8') as f:\n    size = len(f.read())",
               [{"check": "isinstance(size, int)", "msg": "size — int"}],
               ["len(f.read())", "Включая пробелы и переносы"], 2),
            ex(8, "python", "Дан `lines = ['A', 'B', 'C']`. Запиши в `out.txt`, каждую с переносом строки.",
               "lines = ['A', 'B', 'C']\n",
               "lines = ['A', 'B', 'C']\nwith open('out.txt', 'w', encoding='utf-8') as f:\n    for line in lines:\n        f.write(line + '\\n')",
               [{"check": "open('out.txt').read() == 'A\\nB\\nC\\n'", "msg": "A, B, C через перенос"}],
               ["Цикл по списку", "Каждая строка с \\n"], 3),
        ],
        minutes=40, difficulty=2,
    )


def _1_10():
    return lesson(
        "1.10", "Работа с CSV", "space", [
            theory(
                "**CSV** (Comma-Separated Values) — текстовый формат таблиц.\n\n"
                "```python\nimport csv\n\n"
                "# Чтение\nwith open('data.csv', 'r', encoding='utf-8') as f:\n    reader = csv.DictReader(f)\n    for row in reader:\n        print(row['name'], row['value'])\n\n"
                "# Запись\nwith open('out.csv', 'w', encoding='utf-8', newline='') as f:\n    writer = csv.DictWriter(f, fieldnames=['name', 'value'])\n    writer.writeheader()\n    writer.writerow({'name': 'Apollo', 'value': 11})\n```\n\n"
                "**`csv.DictReader`** читает в dict, **`csv.reader`** — в list."
            ),
            analogy(
                "CSV — таблица Excel, сохранённая как текст. Строка — запись, столбцы разделены запятой.",
                "Телеметрия: timestamp,altitude,speed,fuel."
            ),
            example(
                "Прочитай CSV с данными запусков и найди миссии с cost > 100.",
                "DictReader, фильтрация по значению.",
                "import csv\n"
                "with open('launches.csv', 'r', encoding='utf-8') as f:\n"
                "    reader = csv.DictReader(f)\n"
                "    expensive = [r for r in reader if int(r['cost_mln']) > 100]\n"
                "    for m in expensive:\n"
                "        print(f'{m[\"name\"]}: {m[\"cost_mln\"]} млн')",
                "Apollo Program: 250 млн\nArtemis: 150 млн",
                "DictReader даёт dict. Числа приходят как str — нужна конвертация в int/float."
            ),
            common_mistakes([
                {"mistake": "Открытие CSV без newline='' на Windows", "why_bad": "Двойные переносы", "fix": "newline='' на запись"},
                {"mistake": "Числа из CSV как строки: '10' + '20' = '1020'", "why_bad": "Строки, не числа", "fix": "int(row['x']) или float()"},
            ]),
            interview_questions([
                {"q": "Когда csv, а когда pandas?",
                 "a": "csv — для маленьких файлов и простых операций (до ~100к строк). pandas — для аналитики, больших файлов."},
                {"q": "Почему DictReader удобнее reader?",
                 "a": "Доступ по имени столбца, не по индексу. Код не ломается при изменении порядка."},
            ]),
            knowledge_checklist([
                "Читаю CSV через csv.DictReader",
                "Записываю CSV через csv.DictWriter",
                "Конвертирую строковые значения в числа",
                "List comprehension для фильтрации",
                "Знаю ограничения csv vs pandas",
            ]),
        ],
        exercises=[
            ex(1, "python", "Дан CSV-текст 'name,age\\nAlice,30\\nBob,25\\n'. Прочитай через DictReader, посчитай строки (без заголовка). Сохрани в `n`.",
               "import csv, io\ndata = 'name,age\\nAlice,30\\nBob,25\\n'\nn = 0\n",
               "import csv, io\ndata = 'name,age\\nAlice,30\\nBob,25\\n'\nreader = csv.DictReader(io.StringIO(data))\nn = sum(1 for _ in reader)",
               [{"check": "n == 2", "msg": "2 строки"}],
               ["DictReader пропускает заголовок", "sum(1 for _)"], 2),
            ex(2, "python", "Дан CSV 'x,y\\n1,10\\n2,20\\n3,30\\n'. Прочитай, посчитай сумму y, сохрани в `s`.",
               "import csv, io\ndata = 'x,y\\n1,10\\n2,20\\n3,30\\n'\ns = 0\n",
               "import csv, io\ndata = 'x,y\\n1,10\\n2,20\\n3,30\\n'\nreader = csv.DictReader(io.StringIO(data))\ns = sum(int(r['y']) for r in reader)",
               [{"check": "s == 60", "msg": "10+20+30 = 60"}],
               ["int() для строки в число"], 2),
            ex(3, "python", "Дан CSV 'name,score\\nA,80\\nB,95\\nC,70\\n'. Найди имя с максимальным score, сохрани в `top`.",
               "import csv, io\ndata = 'name,score\\nA,80\\nB,95\\nC,70\\n'\ntop = ''\n",
               "import csv, io\ndata = 'name,score\\nA,80\\nB,95\\nC,70\\n'\nreader = csv.DictReader(io.StringIO(data))\nrows = list(reader)\ntop = max(rows, key=lambda r: int(r['score']))['name']",
               [{"check": "top == 'B'", "msg": "B имеет max 95"}],
               ["max() с key функцией", "lambda r: int(r['score'])"], 3),
            ex(4, "python", "Дан список словарей. Запиши в CSV-строку. Поля: 'id', 'value'.",
               "import csv, io\nrows = [{'id': 1, 'value': 'x'}, {'id': 2, 'value': 'y'}]\nout = ''\n",
               "import csv, io\nrows = [{'id': 1, 'value': 'x'}, {'id': 2, 'value': 'y'}]\nbuf = io.StringIO()\nw = csv.DictWriter(buf, fieldnames=['id', 'value'])\nw.writeheader()\nw.writerows(rows)\nout = buf.getvalue()",
               [{"check": "'id,value' in out", "msg": "Заголовок"},
                {"check": "'1,x' in out and '2,y' in out", "msg": "Строки"}],
               ["writerows — множественная запись", "writeheader() один раз"], 3),
            ex(5, "python", "Дан CSV 'a,b,c\\n1,2,3\\n4,5,6\\n'. Прочитай, создай список словарей. Сохрани в `data`.",
               "import csv, io\ntext = 'a,b,c\\n1,2,3\\n4,5,6\\n'\ndata = []\n",
               "import csv, io\ntext = 'a,b,c\\n1,2,3\\n4,5,6\\n'\nreader = csv.DictReader(io.StringIO(text))\ndata = list(reader)",
               [{"check": "data == [{'a': '1', 'b': '2', 'c': '3'}, {'a': '4', 'b': '5', 'c': '6'}]", "msg": "2 словаря"}],
               ["list(reader) собирает", "Значения — строки"], 2),
            ex(6, "python", "Дан CSV 'planet,mass\\nEarth,1\\nMars,0.107\\nJupiter,317.8\\n'. Сумма масс, сохрани в `total` (float).",
               "import csv, io\ntext = 'planet,mass\\nEarth,1\\nMars,0.107\\nJupiter,317.8\\n'\ntotal = 0.0\n",
               "import csv, io\ntext = 'planet,mass\\nEarth,1\\nMars,0.107\\nJupiter,317.8\\n'\nreader = csv.DictReader(io.StringIO(text))\ntotal = sum(float(r['mass']) for r in reader)",
               [{"check": "abs(total - 318.907) < 0.01", "msg": "≈ 318.9"}],
               ["float() для дробных"], 2),
            ex(7, "python", "Дан CSV 'lang,users\\nPython,100\\nR,50\\nJulia,10\\n'. Отфильтруй с users>30, посчитай их количество, сохрани в `n`.",
               "import csv, io\ntext = 'lang,users\\nPython,100\\nR,50\\nJulia,10\\n'\nn = 0\n",
               "import csv, io\ntext = 'lang,users\\nPython,100\\nR,50\\nJulia,10\\n'\nreader = csv.DictReader(io.StringIO(text))\nfiltered = [r for r in reader if int(r['users']) > 30]\nn = len(filtered)",
               [{"check": "n == 2", "msg": "Python и R > 30"}],
               ["List comprehension с условием", "len()"], 3),
            ex(8, "python", "Дан CSV 'city,temp\\nNYC,20\\nLA,25\\nChicago,15\\nNYC,22\\n'. Средняя температура, сохрани в `avg` (float).",
               "import csv, io\ntext = 'city,temp\\nNYC,20\\nLA,25\\nChicago,15\\nNYC,22\\n'\navg = 0.0\n",
               "import csv, io\ntext = 'city,temp\\nNYC,20\\nLA,25\\nChicago,15\\nNYC,22\\n'\nreader = csv.DictReader(io.StringIO(text))\ntemps = [int(r['temp']) for r in reader]\navg = sum(temps) / len(temps)",
               [{"check": "abs(avg - 20.5) < 0.01", "msg": "20.5"}],
               ["List comprehension", "sum/len"], 3),
        ],
        minutes=45, difficulty=2,
    )


def _1_11():
    return lesson(
        "1.11", "Обработка ошибок", "space", [
            theory(
                "**Исключения** — ошибки во время выполнения. Python не падает, если их правильно обработать.\n\n"
                "```python\ntry:\n    result = 10 / 0\nexcept ZeroDivisionError:\n    print('На ноль делить нельзя')\nfinally:\n    print('Это выполнится всегда')\n```\n\n"
                "**Основные типы:**\n"
                "- `ValueError` — неправильное значение (int('abc'))\n"
                "- `TypeError` — неправильный тип ('a' + 1)\n"
                "- `KeyError` — нет ключа в dict\n"
                "- `IndexError` — индекс за пределами списка\n"
                "- `ZeroDivisionError` — деление на ноль\n"
                "- `FileNotFoundError` — файл не найден"
            ),
            analogy(
                "Try/except — парашют: основной полёт (try), запасной (except).",
                "При чтении телеметрии файл может отсутствовать — except ловит ошибку и пробует другое хранилище."
            ),
            example(
                "Безопасно преобразуй строку в число. Если нельзя — верни 0.",
                "try пытается int(s), except ловит ValueError.",
                "def safe_int(s, default=0):\n"
                "    try:\n"
                "        return int(s)\n"
                "    except ValueError:\n"
                "        return default\n\n"
                "print(safe_int('42'))\nprint(safe_int('abc'))",
                "42\n0",
                "ValueError ловится, возвращаем default. Другие ошибки (TypeError) не ловятся — это правильно."
            ),
            common_mistakes([
                {"mistake": "try: ... except: — голый except", "why_bad": "Ловит ВСЁ (даже KeyboardInterrupt)", "fix": "except SomeError:"},
                {"mistake": "except: pass — проглатывание", "why_bad": "Скрывает баги", "fix": "Логируй или поднимай заново"},
            ]),
            interview_questions([
                {"q": "Зачем `finally`?",
                 "a": "Выполняется ВСЕГДА, даже если был return или непойманное исключение. Для cleanup."},
                {"q": "raise vs assert?",
                 "a": "raise — выбрасывает всегда. assert — проверка условия, отключается через -O."},
            ]),
            knowledge_checklist([
                "Оборачиваю рискованный код в try/except",
                "Знаю основные типы исключений",
                "Использую finally для cleanup",
                "Выбрасываю исключения через raise",
                "Не использую голый except",
            ]),
        ],
        exercises=[
            ex(1, "python", "Попробуй `int('abc')`, поймай ValueError, `n = 0`.",
               "n = None\n",
               "n = None\ntry:\n    n = int('abc')\nexcept ValueError:\n    n = 0",
               [{"check": "n == 0", "msg": "n = 0 после except"}],
               ["try: — попытка", "except ValueError:"], 2),
            ex(2, "python", "Создай `safe_div(a, b)`, возвращающую a/b, при ZeroDivisionError — None.",
               "def safe_div(a, b):\n    pass\n",
               "def safe_div(a, b):\n    try:\n        return a / b\n    except ZeroDivisionError:\n        return None",
               [{"check": "safe_div(10, 0) is None", "msg": "Деление на 0 → None"},
                {"check": "safe_div(10, 2) == 5.0", "msg": "10/2 = 5.0"}],
               ["except ZeroDivisionError:", "Возвращай None"], 2),
            ex(3, "python", "Попробуй открыть `nofile.txt`, поймай FileNotFoundError, `content = ''`.",
               "content = None\n",
               "content = None\ntry:\n    with open('nofile.txt') as f:\n        content = f.read()\nexcept FileNotFoundError:\n    content = ''",
               [{"check": "content == ''", "msg": "Файл не найден → ''"}],
               ["FileNotFoundError", "open() внутри try"], 2),
            ex(4, "python", "Дан `d = {'a': 1}`. Безопасно получи `d['b']`, при KeyError возвращай 0. Сохрани в `v`.",
               "d = {'a': 1}\nv = 0\n",
               "d = {'a': 1}\nv = 0\ntry:\n    v = d['b']\nexcept KeyError:\n    v = 0",
               [{"check": "v == 0", "msg": "v = 0 после KeyError"}],
               ["KeyError", "Лучше .get(), но try тоже работает"], 2),
            ex(5, "python", "try/except/finally: внутри try `x = 1`, except (ValueError) `x = -1`, finally выведи 'done'. Изначально x = 0.",
               "x = 0\n",
               "x = 0\ntry:\n    x = 1\nexcept ValueError:\n    x = -1\nfinally:\n    print('done')",
               [{"check": "x == 1", "msg": "x = 1"},
                {"check": "'done' in _printed_output", "msg": "Выведено 'done'"}],
               ["finally всегда", "print в finally"], 2),
            ex(6, "python", "Создай `parse_list(s)`: строку '1,2,3' → [1, 2, 3]. Если не парсится — [].",
               "def parse_list(s):\n    pass\n",
               "def parse_list(s):\n    try:\n        return [int(x) for x in s.split(',')]\n    except (ValueError, AttributeError):\n        return []",
               [{"check": "parse_list('1,2,3') == [1, 2, 3]", "msg": "Парсинг работает"},
                {"check": "parse_list('') == []", "msg": "Пустая строка → []"}],
               ["split(',')", "int(x)", "except (ValueError, AttributeError)"], 3),
            ex(7, "python", "Создай `get_value(d, key, default=None)`, безопасно возвращающую d[key], при KeyError — default.",
               "def get_value(d, key, default=None):\n    pass\n",
               "def get_value(d, key, default=None):\n    try:\n        return d[key]\n    except KeyError:\n        return default",
               [{"check": "get_value({'a': 1}, 'a') == 1", "msg": "Есть ключ → значение"},
                {"check": "get_value({'a': 1}, 'b') is None", "msg": "Нет ключа → None"}],
               ["except KeyError:", "return default"], 2),
            ex(8, "python", "Попроси пользователя ввести число через input, повторяй, пока не получится. Сохрани итог в `n`.",
               "n = 0\n",
               "n = 0\nwhile True:\n    s = input('Введи число: ')\n    try:\n        n = int(s)\n        break\n    except ValueError:\n        print('Не число, ещё раз')",
               [{"check": "call_user_code_with_input('n', ['abc', '5'], {}) == 5", "msg": "После 'abc' и '5' = 5"}],
               ["while True", "break при успехе"], 3),
        ],
        minutes=45, difficulty=3,
    )


def _1_12():
    return lesson(
        "1.12", "Мини-проект: Анализ телеметрии ракеты", "space", [
            theory(
                "В этом мини-проекте ты применишь всё из Блока 1: переменные, условия, циклы, функции, словари, списки, файлы и CSV.\n\n"
                "**Задача:** дан CSV-файл с телеметрией тестового запуска ракеты (время, высота, скорость, температура двигателя, давление). Нужно:\n\n"
                "1. Прочитать данные из CSV\n"
                "2. Найти аномалии (температура > 3500°C)\n"
                "3. Вычислить ключевые статистики\n"
                "4. Сформировать отчёт"
            ),
            analogy(
                "Работа инженера телеметрии: сырые данные → аномалии → статистики → отчёт для команды. В Data Science это EDA на минимальном уровне.",
                "SpaceX анализирует телеметрию каждого запуска Falcon 9, чтобы улучшить следующую итерацию."
            ),
            example(
                "Полный разбор решения мини-проекта.",
                "Шаг за шагом: чтение, статистики, аномалии, отчёт.",
                "import csv\n\n"
                "def analyze_telemetry(filepath):\n"
                "    rows = []\n"
                "    with open(filepath, 'r', encoding='utf-8') as f:\n"
                "        reader = csv.DictReader(f)\n"
                "        for row in reader:\n"
                "            rows.append({\n"
                "                'time': float(row['time']),\n"
                "                'altitude': float(row['altitude']),\n"
                "                'speed': float(row['speed']),\n"
                "                'temp': float(row['temp']),\n"
                "                'pressure': float(row['pressure'])\n"
                "            })\n"
                "    if not rows:\n"
                "        return 'Нет данных'\n"
                "    n = len(rows)\n"
                "    return {\n"
                "        'count': n,\n"
                "        'max_altitude': max(r['altitude'] for r in rows),\n"
                "        'max_speed': max(r['speed'] for r in rows),\n"
                "        'avg_temp': sum(r['temp'] for r in rows) / n,\n"
                "        'anomalies': [r for r in rows if r['temp'] > 3500]\n"
                "    }",
                "Возвращает словарь с отчётом",
                "Словарь — гибкая структура для отчёта. Аномалии выделяются в отдельный список."
            ),
            common_mistakes([
                {"mistake": "Обращение к колонке, которой нет", "why_bad": "KeyError", "fix": "Проверяй заголовки DictReader.fieldnames"},
                {"mistake": "Деление на ноль, если CSV пустой", "why_bad": "ZeroDivisionError", "fix": "Проверяй len(rows) > 0"},
            ]),
            interview_questions([
                {"q": "Как обработать CSV с разной кодировкой?",
                 "a": "Открывать с правильным encoding. Часто 'utf-8', иногда 'cp1251' (Windows) или 'latin-1'."},
                {"q": "Что делать с пропусками в данных?",
                 "a": "Заменять на None, среднее, медиану или удалять строку. Стратегия зависит от задачи."},
            ]),
            knowledge_checklist([
                "Читаю CSV в Python-структуры",
                "Конвертирую строки в числа",
                "Фильтрую данные по условию",
                "Вычисляю max/min/avg",
                "Формирую отчёт как dict",
            ]),
        ],
        exercises=[
            ex(1, "python", "Создай функцию `calc_stats(numbers)`, возвращающую dict {'avg', 'min', 'max', 'count'}.",
               "def calc_stats(numbers):\n    pass\n",
               "def calc_stats(numbers):\n    return {\n        'avg': sum(numbers) / len(numbers),\n        'min': min(numbers),\n        'max': max(numbers),\n        'count': len(numbers)\n    }",
               [{"check": "call_user_code('calc_stats', [[10, 20, 30]], {}) == {'avg': 20.0, 'min': 10, 'max': 30, 'count': 3}",
                 "msg": "Правильный отчёт"}],
               ["dict literal", "return {...}"], 2),
            ex(2, "python", "Создай `find_anomalies(temps, threshold=3500)`, возвращающую список индексов temps > threshold.",
               "def find_anomalies(temps, threshold=3500):\n    pass\n",
               "def find_anomalies(temps, threshold=3500):\n    return [i for i, t in enumerate(temps) if t > threshold]",
               [{"check": "find_anomalies([3000, 3600, 3200, 4000]) == [1, 3]", "msg": "Индексы аномалий"}],
               ["enumerate()", "list comprehension"], 3),
            ex(3, "python", "Создай `telemetry_report(data)` для списка dict. Верни dict: count, max_altitude, max_speed, avg_temp, anomalies_count.",
               "def telemetry_report(data):\n    pass\n",
               "def telemetry_report(data):\n    if not data:\n        return {'count': 0}\n    return {\n        'count': len(data),\n        'max_altitude': max(r['altitude'] for r in data),\n        'max_speed': max(r['speed'] for r in data),\n        'avg_temp': sum(r['temp'] for r in data) / len(data),\n        'anomalies_count': sum(1 for r in data if r['temp'] > 3500)\n    }",
               [{"check": "call_user_code('telemetry_report', [[{'altitude':100,'speed':200,'temp':3200},{'altitude':200,'speed':300,'temp':3600}]], {})['count'] == 2",
                 "msg": "count = 2"},
                {"check": "call_user_code('telemetry_report', [[{'altitude':100,'speed':200,'temp':3200},{'altitude':200,'speed':300,'temp':3600}]], {})['anomalies_count'] == 1",
                 "msg": "1 аномалия (3600 > 3500)"}],
               ["if not data:", "max() с генератором", "sum(1 for ...)"], 3),
            ex(4, "python", "Дан CSV 'time,altitude,speed,temp\\n0,0,0,20\\n1,100,50,500\\n2,1000,500,2500\\n'. Прочитай и посчитай среднее temp, сохрани в `avg`.",
               "import csv, io\ntext = 'time,altitude,speed,temp\\n0,0,0,20\\n1,100,50,500\\n2,1000,500,2500\\n'\navg = 0.0\n",
               "import csv, io\ntext = 'time,altitude,speed,temp\\n0,0,0,20\\n1,100,50,500\\n2,1000,500,2500\\n'\nreader = csv.DictReader(io.StringIO(text))\ntemps = [float(r['temp']) for r in reader]\navg = sum(temps) / len(temps)",
               [{"check": "abs(avg - 1006.666) < 0.1", "msg": "Среднее ≈ 1006.67"}],
               ["float() для конвертации", "sum/len"], 3),
        ],
        minutes=90, difficulty=4,
    )


LESSONS = [_1_9, _1_10, _1_11, _1_12]
