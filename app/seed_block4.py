"""
Блок 4: Визуализация данных.
10 уроков, ~90 упражнений (большинство с matplotlib).
"""
from app.seed_helpers import (
    ex, lesson, theory, analogy, visual, example,
    common_mistakes, interview_questions, knowledge_checklist,
)


def _4_1():
    return lesson(
        "4.1", "Matplotlib: основы", "space", [
            theory(
                "**Matplotlib** — главная библиотека визуализации в Python. "
                "Создатель — Джон Хантер (2003), вдохновлённый MATLAB.\n\n"
                "**Иерархия объектов:**\n"
                "- `Figure` — холст (всё окно графика)\n"
                "- `Axes` — система координат, на которой рисуем\n"
                "- `Artist` — всё, что нарисовано (линии, точки, текст)\n\n"
                "**Базовый сценарий:**\n"
                "```python\n"
                "import matplotlib.pyplot as plt\n"
                "plt.plot(x, y)          # рисуем\n"
                "plt.title('График')     # заголовок\n"
                "plt.xlabel('X')         # ось X\n"
                "plt.show()              # показать (в браузере — PNG)\n"
                "```\n\n"
                "**Параметры plot():**\n"
                "- `color` — цвет ('red', '#FF0000', 'C0')\n"
                "- `linestyle` — '-' (сплошная), '--' (пунктир), ':' (точки), '-.' (штрих-пунктир)\n"
                "- `marker` — 'o' (круг), 's' (квадрат), '^' (треугольник), '*' (звезда)\n"
                "- `alpha` — прозрачность от 0 до 1\n"
                "- `linewidth`/`markersize` — толщина линии/размер маркера\n\n"
                "**figsize=(width, height)** в дюймах задаёт размер холста. "
                "`plt.figure(figsize=(10, 6))` создаёт широкий график. "
                "Для научных графиков — золотое сечение 10×6 или 12×7.\n\n"
                "В браузере `plt.show()` перехватывается нашей песочницей и "
                "возвращает PNG в base64 — график появится справа от кода."
            ),
            analogy(
                "Figure — это рамка для картины, Axes — сам холст с координатами, а plot() — мазки кистью.",
                "Телеметрия ракеты: Figure — экран в ЦУП, Axes — координатная сетка, линии — графики температуры и скорости."
            ),
            visual(
                "Структура matplotlib: Figure → Axes → plot()",
                "  ┌──────────────── Figure ────────────────┐\n"
                "  │                                          │\n"
                "  │   ┌──────────── Axes ─────────────┐     │\n"
                "  │   │  Y ▲                          │     │\n"
                "  │   │    │       .  •  •             │     │\n"
                "  │   │    │     •        •            │     │\n"
                "  │   │    │   •            •          │     │\n"
                "  │   │    └─────────────────────► X   │     │\n"
                "  │   │       title='Траектория'       │     │\n"
                "  │   └─────────────────────────────────┘     │\n"
                "  │   xlabel='Время'      ylabel='Высота'    │\n"
                "  └──────────────────────────────────────────┘"
            ),
            example(
                "Построй график высоты ракеты по времени: t = [0,10,20,30,40,50], h = [0,1200,4500,9800,18000,32000].",
                "Используем списки Python. plt.plot() рисует линию по умолчанию. plt.show() рендерит в PNG.",
                "import matplotlib.pyplot as plt\n"
                "t = [0, 10, 20, 30, 40, 50]\n"
                "h = [0, 1200, 4500, 9800, 18000, 32000]\n"
                "plt.plot(t, h, marker='o', color='royalblue')\n"
                "plt.title('Высота ракеты')\n"
                "plt.xlabel('Время, с')\n"
                "plt.ylabel('Высота, м')\n"
                "plt.grid(True, alpha=0.3)\n"
                "plt.show()",
                "[График: синяя линия с круглыми маркерами, ось X — время, ось Y — высота, сетка]",
                "plt.grid(True, alpha=0.3) добавляет полупрозрачную сетку — улучшает читаемость."
            ),
            common_mistakes([
                {"mistake": "plt.plot(y) без x", "why_bad": "X будет 0,1,2,...N-1 — часто не то, что нужно", "fix": "Всегда задавай x явно или используй np.arange"},
                {"mistake": "plt.plot(x, y) вместо plt.plot(y, x)", "why_bad": "Поменяются оси — график будет зеркальным", "fix": "plot(ось_X, ось_Y) — сначала независимая переменная"},
                {"mistake": "Забыл plt.show()", "why_bad": "В Jupyter ничего не появится, в скрипте — пустое окно", "fix": "plt.show() в конце"},
                {"mistake": "plt.plot(x, y) — массивы разной длины", "why_bad": "ValueError: x and y must have same first dimension", "fix": "Проверяй len(x) == len(y)"},
                {"mistake": "Не импортировал matplotlib", "why_bad": "NameError: name 'plt' is not defined", "fix": "import matplotlib.pyplot as plt"},
            ]),
            interview_questions([
                {"q": "Чем Figure отличается от Axes?",
                 "a": "Figure — окно/холст целиком (может содержать несколько Axes). Axes — конкретная система координат с осями X/Y, на которой рисуем."},
                {"q": "Что делает plt.show()?",
                 "a": "В интерактивном режиме открывает окно. В скрипте — блокирует до закрытия окна. В нашей песочнице — перехватывается и возвращает PNG."},
                {"q": "Зачем нужен параметр alpha?",
                 "a": "Прозрачность от 0 (невидимо) до 1 (непрозрачно). Полезно при наложении графиков: alpha=0.5 показывает оба."},
            ]),
            knowledge_checklist([
                "Импортирую matplotlib.pyplot как plt",
                "Использую plt.plot(x, y) для линейного графика",
                "Добавляю title, xlabel, ylabel",
                "Задаю color, marker, linestyle, alpha",
                "Использую plt.figure(figsize=(w, h))",
                "Вызываю plt.show() в конце",
                "Использую plt.grid() для сетки",
            ]),
        ],
        exercises=[
            ex(1, "python", "Построй простой линейный график y = 2x + 1 для x = 0..5.",
               "import matplotlib.pyplot as plt\n# твой код\n",
               "import matplotlib.pyplot as plt\nx = list(range(6))\nplt.plot(x, [2*i+1 for i in x])\nplt.title('y = 2x + 1')\nplt.show()",
               [{"check": "True", "msg": "График построен (проверь визуально справа)"}],
               ["plt.plot(x, y) — линейный график", "x = 0..5 — это 6 точек"], 1),
            ex(2, "python", "Построй y = x^2 для x от 0 до 10. Используй np.linspace(0, 10, 100).",
               "import matplotlib.pyplot as plt\nimport numpy as np\n# твой код\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nx = np.linspace(0, 10, 100)\nplt.plot(x, x**2)\nplt.title('y = x^2')\nplt.show()",
               [{"check": "True", "msg": "График построен"}],
               ["np.linspace(0, 10, 100) даст 100 точек", "x**2 — поэлементный квадрат"], 1),
            ex(3, "python", "Построй график температуры двигателя: t=[0,1,2,3,4,5], T=[20,180,520,1100,2400,2900].",
               "import matplotlib.pyplot as plt\n# t — время (с), T — температура (°C)\n",
               "import matplotlib.pyplot as plt\nt = [0, 1, 2, 3, 4, 5]\nT = [20, 180, 520, 1100, 2400, 2900]\nplt.plot(t, T, marker='o', color='orangered')\nplt.title('Нагрев двигателя')\nplt.xlabel('Время, с')\nplt.ylabel('Температура, °C')\nplt.show()",
               [{"check": "True", "msg": "График температуры построен"}],
               ["marker='o' рисует точки", "color='orangered' — оранжево-красный"], 1),
            ex(4, "python", "Два графика на одном холсте: y1 = sin(x), y2 = cos(x) для x от 0 до 2π.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n# твой код\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nx = np.linspace(0, 2*np.pi, 100)\nplt.plot(x, np.sin(x), label='sin')\nplt.plot(x, np.cos(x), label='cos', linestyle='--')\nplt.legend()\nplt.title('sin и cos')\nplt.show()",
               [{"check": "True", "msg": "Два графика на одном холсте"}],
               ["linestyle='--' — пунктир", "label= и legend() — легенда"], 2),
            ex(5, "python", "Построй график с figsize=(10, 6), цветом 'darkgreen', маркером 's' (квадрат).",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nx = np.linspace(0, 5, 20)\nplt.figure(figsize=(10, 6))\nplt.plot(x, np.exp(x/2), color='darkgreen', marker='s')\nplt.title('Экспоненциальный рост')\nplt.show()",
               [{"check": "True", "msg": "Большой график с квадратными маркерами"}],
               ["figsize=(10, 6) — 10×6 дюймов", "marker='s' — square (квадрат)"], 2),
            ex(6, "python", "Сделай график с прозрачностью alpha=0.5 и сеткой.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nx = np.linspace(0, 10, 50)\nplt.plot(x, np.sin(x), alpha=0.5, linewidth=2)\nplt.grid(True, alpha=0.3)\nplt.title('Полупрозрачный график')\nplt.show()",
               [{"check": "True", "msg": "Прозрачность и сетка работают"}],
               ["alpha=0.5 — полупрозрачный", "plt.grid() добавляет сетку"], 2),
            ex(7, "python", "Создай массив y = x^3 - 2x для x от -5 до 5, построй, добавь title и подписи осей.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n# твой код\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nx = np.linspace(-5, 5, 100)\ny = x**3 - 2*x\nplt.plot(x, y, color='purple')\nplt.title('Кубическая функция')\nplt.xlabel('x')\nplt.ylabel('y = x^3 - 2x')\nplt.axhline(y=0, color='black', linewidth=0.5)\nplt.show()",
               [{"check": "True", "msg": "Кубический график построен"}],
               ["axhline рисует горизонтальную линию", "linewidth — толщина"], 2),
            ex(8, "python", "Используй plt.style.use('ggplot') перед построением.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nplt.style.use('ggplot')\nx = np.linspace(0, 10, 100)\nplt.plot(x, np.sin(x))\nplt.title('Стиль ggplot')\nplt.show()",
               [{"check": "True", "msg": "Стиль ggplot применён"}],
               ["plt.style.use() меняет стиль всех графиков", "'ggplot' — серый фон с белой сеткой"], 3),
            ex(9, "python", "Добавь на график аннотацию: plt.annotate('Пик', xy=(5, 25), xytext=(6, 20), arrowprops=dict(arrowstyle='->')).",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nx = np.linspace(0, 10, 100)\nplt.plot(x, x**2)\nplt.annotate('Пик', xy=(5, 25), xytext=(6, 20), arrowprops=dict(arrowstyle='->'))\nplt.title('График с аннотацией')\nplt.show()",
               [{"check": "True", "msg": "Аннотация добавлена"}],
               ["xy — точка, на которую указывает стрелка", "xytext — где текст"], 3),
            ex(10, "python", "Сохрани график в base64 (этот формат использует наша песочница).",
               "import matplotlib.pyplot as plt\nimport numpy as np\nimport io, base64\n# создай график, сохрани в buf = io.BytesIO(), затем plt.savefig(buf, format='png')\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nimport io, base64\nx = np.linspace(0, 5, 50)\nplt.plot(x, x**2)\nbuf = io.BytesIO()\nplt.savefig(buf, format='png')\ndata = base64.b64encode(buf.getvalue()).decode()\nplt.show()",
               [{"check": "True", "msg": "График сохранён в base64"}],
               ["BytesIO — буфер в памяти", "plt.savefig(buf, format='png') — сохраняет в буфер"], 3),
        ],
        minutes=50, difficulty=2,
    )


def _4_2():
    return lesson(
        "4.2", "Типы графиков: линейный, столбчатый, круговой", "space", [
            theory(
                "Разные графики решают разные задачи. Неправильный тип графика "
                "скрывает суть данных или вводит в заблуждение.\n\n"
                "**Линейный (line plot) — `plt.plot(x, y)`:**\n"
                "- Для непрерывных процессов: время → значение\n"
                "- Тренды, температура, скорость, курс акций\n"
                "- X почти всегда — время или непрерывная величина\n\n"
                "**Столбчатый (bar chart) — `plt.bar(categories, values)`:**\n"
                "- Сравнение категорий: планеты по массе, страны по населению\n"
                "- Категории дискретны (не время)\n"
                "- Вертикальный `bar()` и горизонтальный `barh()`\n\n"
                "**Круговой (pie chart) — `plt.pie(sizes, labels=...)`:**\n"
                "- Доли от целого (≤ 5–7 сегментов)\n"
                "- Процентное соотношение: распределение топлива, типов планет\n"
                "- **Плохо** для сравнения похожих долей — используй bar\n"
                "- `autopct='%1.1f%%'` — подписи процентов\n\n"
                "**Правило большого пальца:**\n"
                "- Изменение во времени → line\n"
                "- Сравнение категорий → bar\n"
                "- Доли целого → pie (только если < 7 сегментов)"
            ),
            analogy(
                "Line — спидометр (непрерывная величина по времени). Bar — гистограмма роста в классе. Pie — кусок пиццы от целого.",
                "Линейный: температура двигателя по секундам. Столбчатый: массы планет Солнечной системы. Круговой: доля топлива, окислителя и полезной нагрузки в ракете."
            ),
            visual(
                "Три типа графиков на одном холсте (через subplots)",
                "  ┌── Line ──────────┬── Bar ───────────┬── Pie ───────────┐\n"
                "  │  Y ▲            │       █          │      ___         │\n"
                "  │    │  ╱         │     █ █          │    ╱     ╲       │\n"
                "  │    │╱           │   █ █ █          │   │  45%  │      │\n"
                "  │    ╱            │   █ █ █ █        │   │ 30% 25│      │\n"
                "  │   ╱             │   █ █ █ █ █      │    ╲____╱        │\n"
                "  │  ╱__________► X │   A B C D E      │                  │\n"
                "  │  время→значение │  категория→величина│  доли от целого │\n"
                "  └─────────────────┴──────────────────┴──────────────────┘"
            ),
            example(
                "Сравни массы планет Солнечной системы (в массах Земли): Меркурий 0.055, Венера 0.815, Земля 1.0, Марс 0.107. Построй bar и pie.",
                "Bar — для точного сравнения. Pie — для наглядности долей. На bar подписи точнее, на pie — интуитивнее.",
                "import matplotlib.pyplot as plt\n"
                "planets = ['Mercury', 'Venus', 'Earth', 'Mars']\n"
                "masses = [0.055, 0.815, 1.0, 0.107]\n"
                "fig, axes = plt.subplots(1, 2, figsize=(12, 5))\n"
                "axes[0].bar(planets, masses, color=['#888', '#E8C07D', '#4C72B0', '#C44E52'])\n"
                "axes[0].set_title('Массы планет (bar)')\n"
                "axes[0].set_ylabel('Масса, M_Земли')\n"
                "axes[1].pie(masses, labels=planets, autopct='%1.1f%%', startangle=90)\n"
                "axes[1].set_title('Доля массы (pie)')\n"
                "plt.show()",
                "[Слева: столбчатая диаграмма, Земля — самый высокий. Справа: круговая, Венера и Земля — большие доли]",
                "`fig, axes = plt.subplots(1, 2)` создаёт 2 Axes в одной Figure. `startangle=90` поворачивает первый сегмент наверх."
            ),
            common_mistakes([
                {"mistake": "plt.bar([1,2,3], [10,20,30]) без labels", "why_bad": "Непонятно, что за категории", "fix": "Передай первый аргумент как список строк: plt.bar(['A','B','C'], [10,20,30])"},
                {"mistake": "Pie с 15+ сегментами", "why_bad": "Каша, невозможно прочитать", "fix": "Сгруппируй мелкие в 'Другое' или используй bar"},
                {"mistake": "plt.pie без labels=", "why_bad": "Без подписей не понять, где что", "fix": "labels=names обязательно для pie"},
                {"mistake": "Line для категорий", "why_bad": "Линия между 'Марс' и 'Земля' бессмысленна", "fix": "Используй bar для дискретных категорий"},
                {"mistake": "plt.bar() и plt.pie() на одних осях", "why_bad": "Axes у bar — декартовы, у pie — полярные. Нельзя смешивать", "fix": "Используй subplots(1, 2)"},
            ]),
            interview_questions([
                {"q": "Когда выбрать pie, а когда bar?",
                 "a": "Pie — когда показываешь доли от 100% и сегментов мало (≤5). Bar — когда важна точность сравнения или сегментов много."},
                {"q": "Почему bar лучше pie?",
                 "a": "Человеческий глаз точнее сравнивает длины/высоты, чем углы и площади. На bar сразу видно, что столбец A на 20% выше B, на pie это оценить сложно."},
                {"q": "Что нельзя рисовать линией?",
                 "a": "Категориальные данные (породы собак, марки машин) и дискретные величины без естественного порядка."},
            ]),
            knowledge_checklist([
                "Использую plt.plot() для времени и непрерывных величин",
                "Использую plt.bar() для сравнения категорий",
                "Использую plt.pie() для долей (≤5-7 сегментов)",
                "Подписываю оси и сегменты",
                "Создаю subplots(1, 2) для нескольких графиков",
                "Использую autopct для процентов в pie",
            ]),
        ],
        exercises=[
            ex(1, "python", "Построй bar-график: высоты 4 спутников = [400, 550, 1200, 35786] (LEO, LEO, LEO, GEO).",
               "import matplotlib.pyplot as plt\n# satellites = ['ISS', 'Hubble', 'GPS', 'Geostationary']\n",
               "import matplotlib.pyplot as plt\nsatellites = ['ISS', 'Hubble', 'GPS', 'Geostationary']\nheights = [400, 550, 1200, 35786]\nplt.bar(satellites, heights, color='steelblue')\nplt.title('Высота орбит спутников')\nplt.ylabel('Высота, км')\nplt.show()",
               [{"check": "True", "msg": "Bar-график построен"}],
               ["plt.bar(категории, значения)", "GEO (35786) намного выше LEO"], 1),
            ex(2, "python", "Сделай горизонтальный barh для топ-5 самых длинных рек (в тыс. км): Нил 6.65, Амазонка 6.4, Янцзы 6.3, Миссисипи 6.27, Обь 5.41.",
               "import matplotlib.pyplot as plt\n",
               "import matplotlib.pyplot as plt\nrivers = ['Нил', 'Амазонка', 'Янцзы', 'Миссисипи', 'Обь']\nlengths = [6.65, 6.4, 6.3, 6.27, 5.41]\nplt.barh(rivers, lengths, color='teal')\nplt.title('Самые длинные реки')\nplt.xlabel('Длина, тыс. км')\nplt.show()",
               [{"check": "True", "msg": "Горизонтальный bar построен"}],
               ["plt.barh() — горизонтальные столбцы", "Удобно для длинных подписей"], 1),
            ex(3, "python", "Построй pie для распределения топлива: окислитель 70%, горючее 25%, остальное 5%.",
               "import matplotlib.pyplot as plt\n",
               "import matplotlib.pyplot as plt\nlabels = ['Окислитель', 'Горючее', 'Остальное']\nsizes = [70, 25, 5]\ncolors = ['royalblue', 'orangered', 'gold']\nplt.pie(sizes, labels=labels, colors=colors, autopct='%1.0f%%', startangle=90)\nplt.title('Состав топлива ракеты')\nplt.axis('equal')\nplt.show()",
               [{"check": "True", "msg": "Круговая диаграмма построена"}],
               ["autopct='%1.0f%%' — целые проценты", "axis('equal') делает круг круглым"], 1),
            ex(4, "python", "Построй stacked bar: масса аппарата по компонентам (топливо, обшивка, полезная нагрузка) для 3 ракет.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nrockets = ['Falcon 9', 'Atlas V', 'Ariane 5']\nfuel = [400, 350, 500]\nhull = [25, 30, 40]\npayload = [22, 18, 21]\nfig, ax = plt.subplots()\nax.bar(rockets, fuel, label='Топливо', color='orangered')\nax.bar(rockets, hull, bottom=fuel, label='Обшивка', color='steelblue')\nax.bar(rockets, payload, bottom=np.array(fuel)+np.array(hull), label='Полезная', color='gold')\nax.legend()\nplt.title('Масса по компонентам')\nplt.show()",
               [{"check": "True", "msg": "Stacked bar построен"}],
               ["bottom= — сдвиг столбика вверх", "Складываем по слоям снизу вверх"], 2),
            ex(5, "python", "Сравни два графика: line для тренда и bar для категорий. data: time=[1,2,3,4,5], val=[10,20,15,25,30].",
               "import matplotlib.pyplot as plt\n",
               "import matplotlib.pyplot as plt\nfig, axes = plt.subplots(1, 2, figsize=(12, 4))\naxes[0].plot([1,2,3,4,5], [10,20,15,25,30], marker='o')\naxes[0].set_title('Line: тренд')\naxes[0].set_xlabel('День')\naxes[1].bar(['Пн','Вт','Ср','Чт','Пт'], [10,20,15,25,30], color='coral')\naxes[1].set_title('Bar: категории')\nplt.tight_layout()\nplt.show()",
               [{"check": "True", "msg": "Два графика рядом"}],
               ["plt.subplots(1, 2) — 1 строка, 2 столбца", "tight_layout() выравнивает"], 2),
            ex(6, "python", "Построй pie с explode — выдели один сегмент.",
               "import matplotlib.pyplot as plt\n# доли: 'Кислород' 50%, 'Азот' 30%, 'CO2' 15%, 'Другие' 5%. Выдели 'Кислород'.\n",
               "import matplotlib.pyplot as plt\nlabels = ['Кислород', 'Азот', 'CO2', 'Другие']\nsizes = [50, 30, 15, 5]\nexplode = (0.1, 0, 0, 0)\nplt.pie(sizes, labels=labels, explode=explode, autopct='%1.0f%%', startangle=90)\nplt.title('Атмосфера Марса')\nplt.show()",
               [{"check": "True", "msg": "Сегмент выделен"}],
               ["explode=(0.1, 0, 0, 0) — выдвигает первый", "Кортеж длины labels"], 2),
            ex(7, "python", "Построй bar с разными цветами столбцов: colors=['red','blue','green','gold'].",
               "import matplotlib.pyplot as plt\n",
               "import matplotlib.pyplot as plt\nmissions = ['Apollo', 'Vostok', 'Shuttle', 'Artemis']\ndurations = [12, 1.8, 8, 25]\ncolors = ['red', 'blue', 'green', 'gold']\nplt.bar(missions, durations, color=colors)\nplt.title('Длительности программ, дней')\nplt.show()",
               [{"check": "True", "msg": "Bar с цветами построен"}],
               ["color= принимает список цветов", "Длина списка = число столбцов"], 1),
            ex(8, "python", "Построй line + bar на одних осях через twinx().",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nx = np.arange(5)\nfig, ax1 = plt.subplots()\nax1.bar(x, [10, 20, 15, 25, 30], color='lightblue', label='Высота')\nax1.set_ylabel('Высота, км', color='blue')\nax2 = ax1.twinx()\nax2.plot(x, [200, 400, 350, 500, 600], color='red', marker='o', label='Скорость')\nax2.set_ylabel('Скорость, м/с', color='red')\nplt.title('Высота и скорость')\nplt.show()",
               [{"check": "True", "msg": "Двойные оси построены"}],
               ["twinx() — вторая ось Y", "Полезно для разных единиц измерения"], 3),
            ex(9, "python", "Построй grouped bar: результаты эксперимента A и B по 4 параметрам.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nparams = ['p1', 'p2', 'p3', 'p4']\na_vals = [10, 20, 15, 25]\nb_vals = [12, 18, 20, 22]\nx = np.arange(len(params))\nwidth = 0.35\nplt.bar(x - width/2, a_vals, width, label='A', color='steelblue')\nplt.bar(x + width/2, b_vals, width, label='B', color='coral')\nplt.xticks(x, params)\nplt.legend()\nplt.title('Сравнение A vs B')\nplt.show()",
               [{"check": "True", "msg": "Grouped bar построен"}],
               ["width=0.35 — ширина столбика", "x ± width/2 сдвигает группы"], 3),
            ex(10, "python", "Построй line с маркерами и заливкой между кривой и нулём (fill_between).",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nx = np.linspace(0, 2*np.pi, 100)\ny = np.sin(x)\nplt.plot(x, y, color='purple')\nplt.fill_between(x, y, alpha=0.3, color='purple')\nplt.axhline(y=0, color='black', linewidth=0.5)\nplt.title('sin(x) с заливкой')\nplt.show()",
               [{"check": "True", "msg": "График с заливкой построен"}],
               ["fill_between закрашивает область", "alpha=0.3 делает полупрозрачным"], 3),
        ],
        minutes=50, difficulty=2,
    )


def _4_3():
    return lesson(
        "4.3", "Scatter plot и корреляционные диаграммы", "space", [
            theory(
                "**Scatter plot** (`plt.scatter(x, y)`) — главный инструмент "
                "для изучения связи между двумя переменными.\n\n"
                "**Когда использовать:**\n"
                "- Есть две числовые переменные, хотим увидеть зависимость\n"
                "- Поиск выбросов (outliers)\n"
                "- Кластерный анализ — видны ли группы?\n\n"
                "**Полезные параметры:**\n"
                "- `s=` — размер точки (можно массив: размер = значение третьей переменной)\n"
                "- `c=` — цвет (можно массив: цвет = категория или непрерывная величина)\n"
                "- `alpha=` — прозрачность (при тысячах точек спасает от каши)\n"
                "- `cmap=` — цветовая карта ('viridis', 'plasma', 'coolwarm')\n"
                "- `marker=` — форма точки\n\n"
                "**Корреляция vs Scatter:**\n"
                "- Коэффициент корреляции Пирсона r ∈ [-1, 1]\n"
                "- r > 0.7 — сильная положительная связь\n"
                "- r < -0.7 — сильная отрицательная\n"
                "- Scatter показывает связь визуально, r — численно\n"
                "- **Важно:** корреляция ≠ причинность!\n\n"
                "**3D-данные:** можно закодировать третью переменную через размер "
                "или цвет точки, получив bubble chart."
            ),
            analogy(
                "Scatter — облако точек в небе: видишь, есть ли форма, направление ветра, скопления.",
                "Точка на scatter — запуск: X = температура двигателя, Y = высота. Кучность точек вдоль линии = связь."
            ),
            visual(
                "Scatter plot с цветовым кодированием",
                "         Y ▲\n"
                "           │     • ●\n"
                "           │   • ● •\n"
                "           │ • • ●   •\n"
                "           │• ● •  • •\n"
                "           │ ● • • •\n"
                "           │• ● •\n"
                "           └─────────────────► X\n"
                "           • — низкое Z    ● — высокое Z\n"
                "           (c= массив, cmap='viridis')"
            ),
            example(
                "Сгенерируй 200 точек: x ~ N(0,1), y = 2x + шум. Построй scatter, посчитай корреляцию.",
                "Используем np.random.seed для воспроизводимости. np.corrcoef возвращает матрицу [[1, r], [r, 1]].",
                "import matplotlib.pyplot as plt\n"
                "import numpy as np\n"
                "np.random.seed(42)\n"
                "x = np.random.normal(0, 1, 200)\n"
                "y = 2 * x + np.random.normal(0, 0.5, 200)\n"
                "plt.figure(figsize=(8, 6))\n"
                "plt.scatter(x, y, alpha=0.6, s=30, c='royalblue', edgecolor='white')\n"
                "plt.title(f'scatter: r = {np.corrcoef(x, y)[0, 1]:.3f}')\n"
                "plt.xlabel('X')\n"
                "plt.ylabel('Y = 2X + noise')\n"
                "plt.grid(True, alpha=0.3)\n"
                "plt.show()",
                "[Облако точек вдоль прямой y=2x, корреляция ≈ 0.97]",
                "np.corrcoef(x, y)[0, 1] — берём элемент [0,1] корреляционной матрицы. edgecolor='white' делает точки чётче на фоне."
            ),
            common_mistakes([
                {"mistake": "plt.scatter(x, y) при 10000 точек без alpha", "why_bad": "Каша, ничего не видно", "fix": "alpha=0.3 или 0.5"},
                {"mistake": "Перепутал s и c: s=100, c='red'", "why_bad": "s=100 — это размер, c='red' — цвет, не цвет=100", "fix": "s принимает число или массив, c — цвет или массив"},
                {"mistake": "Делаю scatter для времени", "why_bad": "Потеряешь временной порядок", "fix": "Для времени — line plot, scatter для пары числовых переменных"},
                {"mistake": "Путаю корреляцию с причинностью", "why_bad": "Ложные выводы: 'X вызывает Y' из r>0", "fix": "Корреляция показывает только статистическую связь"},
                {"mistake": "Не убрал выбросы перед расчётом r", "why_bad": "r сильно зависит от outliers", "fix": "Сначала визуализируй (scatter), потом считай метрики"},
            ]),
            interview_questions([
                {"q": "Чем scatter отличается от line plot?",
                 "a": "Line соединяет точки линией (подразумевается порядок/тренд). Scatter показывает облако — подходит для пары числовых переменных без порядка."},
                {"q": "Что такое корреляция Пирсона?",
                 "a": "Мера линейной связи от -1 до 1. 0 — нет линейной связи, ±1 — идеальная прямая. Не ловит нелинейные зависимости (y = x^2 даст r≈0)."},
                {"q": "Как показать 3 переменные на 2D scatter?",
                 "a": "X, Y — две переменные. Цвет (c=) или размер точки (s=) — третья. Получается bubble chart."},
            ]),
            knowledge_checklist([
                "Использую plt.scatter(x, y) для пары числовых переменных",
                "Задаю alpha < 1 при большом числе точек",
                "Использую c= и cmap= для цветового кодирования",
                "Использую s= для размерного кодирования (bubble)",
                "Считаю np.corrcoef() для количественной оценки",
                "Помню: корреляция ≠ причинность",
            ]),
        ],
        exercises=[
            ex(1, "python", "Сгенерируй 100 точек x ~ N(0,1), y ~ N(0,1). Построй scatter с alpha=0.6.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\nx = np.random.normal(0, 1, 100)\ny = np.random.normal(0, 1, 100)\nplt.scatter(x, y, alpha=0.6)\nplt.title('Случайное облако')\nplt.xlabel('X')\nplt.ylabel('Y')\nplt.show()",
               [{"check": "True", "msg": "Scatter построен"}],
               ["np.random.seed(42) — воспроизводимость", "alpha=0.6 — полупрозрачные точки"], 1),
            ex(2, "python", "Построй scatter с цветом по значению: используй c=y и cmap='viridis'.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\nx = np.random.normal(0, 1, 100)\ny = np.random.normal(0, 1, 100)\nplt.scatter(x, y, c=y, cmap='viridis', alpha=0.7)\nplt.colorbar(label='Y')\nplt.title('Scatter с цветом')\nplt.show()",
               [{"check": "True", "msg": "Scatter с цветом построен"}],
               ["c=y — цвет зависит от Y", "colorbar() добавляет шкалу"], 2),
            ex(3, "python", "Bubble chart: x, y, s=x**2 + y**2 + 20 (размер).",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\nx = np.random.normal(0, 1, 50)\ny = np.random.normal(0, 1, 50)\nsizes = x**2 + y**2 + 20\nplt.scatter(x, y, s=sizes*30, alpha=0.5, c='coral', edgecolor='black')\nplt.title('Bubble chart')\nplt.show()",
               [{"check": "True", "msg": "Bubble chart построен"}],
               ["s= принимает массив размеров", "sizes*30 — масштабирование"], 2),
            ex(4, "python", "Два scatter на одном рисунке: сильный r (y = 2x) и слабый r (y случайный).",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\nfig, axes = plt.subplots(1, 2, figsize=(12, 5))\nx = np.random.normal(0, 1, 100)\naxes[0].scatter(x, 2*x + np.random.normal(0, 0.3, 100), alpha=0.6, color='green')\naxes[0].set_title('Сильная корреляция (r≈0.96)')\naxes[1].scatter(x, np.random.normal(0, 1, 100), alpha=0.6, color='red')\naxes[1].set_title('Слабая корреляция (r≈0)')\nplt.show()",
               [{"check": "True", "msg": "Два scatter на одном рисунке"}],
               ["subplots(1, 2) — два Axes", "Сравниваем облака"], 2),
            ex(5, "python", "Scatter с разными категориями через цикл и список цветов.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\ncolors = ['red', 'blue', 'green']\nlabels = ['A', 'B', 'C']\nfor i, (c, l) in enumerate(zip(colors, labels)):\n    x = np.random.normal(i, 1, 50)\n    y = np.random.normal(i, 1, 50)\n    plt.scatter(x, y, c=c, label=l, alpha=0.6)\nplt.legend()\nplt.title('Группы точек')\nplt.show()",
               [{"check": "True", "msg": "Группы на одном scatter"}],
               ["zip() объединяет списки", "label= для легенды"], 2),
            ex(6, "python", "Scatter с линией тренда: вычисли коэффициенты np.polyfit(x, y, 1) и нарисуй прямую.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\nx = np.random.normal(0, 1, 100)\ny = 2*x + 0.5 + np.random.normal(0, 0.5, 100)\nslope, intercept = np.polyfit(x, y, 1)\nplt.scatter(x, y, alpha=0.5, label='Данные')\nplt.plot(x, slope*x + intercept, 'r-', label=f'y = {slope:.2f}x + {intercept:.2f}')\nplt.legend()\nplt.title('Линия тренда')\nplt.show()",
               [{"check": "True", "msg": "Тренд проведён"}],
               ["polyfit(..., 1) — линейная регрессия", "Возвращает [slope, intercept]"], 3),
            ex(7, "python", "Построй scatter с логарифмической осью Y: plt.yscale('log').",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\nx = np.arange(1, 21)\ny = np.exp(x/3) * np.random.uniform(0.8, 1.2, 20)\nplt.scatter(x, y, c='teal', s=50)\nplt.yscale('log')\nplt.title('Логарифмическая шкала Y')\nplt.xlabel('День')\nplt.ylabel('Сигнал (log)')\nplt.show()",
               [{"check": "True", "msg": "Лог-ось применена"}],
               ["yscale('log') — логарифмическая ось", "Полезно для экспоненциального роста"], 3),
            ex(8, "python", "Scatter с выделением выбросов: отметь красным точки с |y - mean| > 2*std.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\nx = np.random.normal(0, 1, 100)\ny = 0.5*x + np.random.normal(0, 0.5, 100)\nmean_y, std_y = y.mean(), y.std()\noutliers = np.abs(y - mean_y) > 2*std_y\nplt.scatter(x[~outliers], y[~outliers], c='blue', alpha=0.6, label='Норма')\nplt.scatter(x[outliers], y[outliers], c='red', s=100, label='Выбросы')\nplt.legend()\nplt.title('Поиск выбросов')\nplt.show()",
               [{"check": "True", "msg": "Выбросы выделены"}],
               ["Булева маска np.abs(...) > 2*std", "Два plt.scatter: один для нормы, другой для outliers"], 3),
            ex(9, "python", "Scatter с annotate: подпиши 3 самые верхние точки координатами (x, y).",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\nx = np.random.normal(0, 1, 50)\ny = np.random.normal(0, 1, 50)\nplt.scatter(x, y, alpha=0.6)\ntop_idx = np.argsort(y)[-3:]\nfor i in top_idx:\n    plt.annotate(f'({x[i]:.1f}, {y[i]:.1f})', (x[i], y[i]), xytext=(5, 5), textcoords='offset points')\nplt.title('Топ-3 точки подписаны')\nplt.show()",
               [{"check": "True", "msg": "Точки подписаны"}],
               ["np.argsort сортирует индексы", "[-3:] — последние 3 (наибольшие y)"], 3),
            ex(10, "python", "Scatter + гистограммы маргинальных распределений через subplots (снизу и сбоку).",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\nx = np.random.normal(0, 1, 300)\ny = x + np.random.normal(0, 0.5, 300)\nfig = plt.figure(figsize=(8, 8))\nax_main = fig.add_axes([0.1, 0.1, 0.7, 0.7])\nax_x = fig.add_axes([0.1, 0.85, 0.7, 0.13])\nax_y = fig.add_axes([0.85, 0.1, 0.13, 0.7])\nax_main.scatter(x, y, alpha=0.4)\nax_x.hist(x, bins=30, color='steelblue')\nax_y.hist(y, bins=30, orientation='horizontal', color='coral')\nplt.show()",
               [{"check": "True", "msg": "Marginal plots построены"}],
               ["add_axes([left, bottom, width, height]) в долях Figure", "Marginal plots — стандартный приём"], 3),
        ],
        minutes=55, difficulty=2,
    )


def _4_4():
    return lesson(
        "4.4", "Гистограммы и box plot", "space", [
            theory(
                "**Гистограмма** (`plt.hist(data, bins=...)`) показывает распределение одной "
                "числовой переменной — сколько значений попало в каждый интервал (bin).\n\n"
                "**Параметры hist:**\n"
                "- `bins=` — число интервалов (больше = детальнее, но шумнее)\n"
                "- `range=(min, max)` — фиксированные границы\n"
                "- `density=True` — нормировка в плотность (площадь = 1)\n"
                "- `alpha=` — прозрачность для наложения нескольких\n"
                "- `color=`, `edgecolor=` — цвета\n"
                "- `cumulative=True` — кумулятивная гистограмма\n\n"
                "**Правило bins:** √n (Стурджес) или log2(n)+1. Слишком мало — "
                "теряешь детали, слишком много — спагетти.\n\n"
                "**Box plot** (`plt.boxplot(data)`) — компактный обзор распределения:\n"
                "- **Ящик** — от Q1 (25%) до Q3 (75%), IQR = Q3-Q1\n"
                "- **Линия в ящике** — медиана (Q2)\n"
                "- **Усы (whiskers)** — min/max в пределах 1.5×IQR\n"
                "- **Точки за усами** — выбросы (outliers)\n\n"
                "**Когда что:**\n"
                "- Hist — форма распределения (нормальное? скошенное?)\n"
                "- Box — сравнение групп, поиск выбросов, медиана\n"
                "- Для очень больших данных — kdeplot (оценка плотности)"
            ),
            analogy(
                "Hist — карта высот: видно, где горы (пики распределения). Box — сводка погоды: среднее, экстремумы, аномалии.",
                "Hist: распределение температур двигателя за час. Box: сравнение температур трёх двигателей — где медиана выше, где выбросы."
            ),
            visual(
                "Box plot в разрезе",
                "      upper whisker ─┐\n"
                "                     │  ┌─ outlier (точка)\n"
                "      Q3 ─────────────┼──┤\n"
                "                     │  │  ← ящик (IQR = Q3-Q1)\n"
                "      median ─────────┼──┤  ← линия в ящике\n"
                "                     │  │\n"
                "      Q1 ─────────────┼──┘\n"
                "      lower whisker ──┘\n"
                "      \n"
                "      Hist: ╱╲      ╱─╲       ╱╲\n"
                "           ╱  ╲    ╱   ╲     ╱  ╲   ╱─╲\n"
                "         ─╱────╲──╱─────╲───╱────╲─╱───╲──"
            ),
            example(
                "Сгенерируй 1000 значений N(0, 1) — нормальное распределение. Построй hist с bins=30.",
                "np.random.seed делает результат воспроизводимым. density=True нормирует, чтобы сравнивать с PDF.",
                "import matplotlib.pyplot as plt\n"
                "import numpy as np\n"
                "np.random.seed(42)\n"
                "data = np.random.normal(0, 1, 1000)\n"
                "fig, axes = plt.subplots(1, 2, figsize=(12, 4))\n"
                "axes[0].hist(data, bins=30, color='steelblue', edgecolor='black')\n"
                "axes[0].set_title('Histogram')\n"
                "axes[0].set_xlabel('Значение')\n"
                "axes[0].set_ylabel('Частота')\n"
                "axes[1].boxplot(data, vert=False)\n"
                "axes[1].set_title('Box plot')\n"
                "axes[1].set_xlabel('Значение')\n"
                "plt.tight_layout()\n"
                "plt.show()",
                "[Слева: колокол с пиком около 0. Справа: ящик с медианой 0, без выбросов]",
                "tight_layout() автоматически расставляет отступы между Axes. vert=False у boxplot — горизонтальный ящик."
            ),
            common_mistakes([
                {"mistake": "plt.hist(data) с bins=10 при n=100000", "why_bad": "Грубая картинка, потеряны детали", "fix": "Увеличь bins до 50-100 или используй log-scale"},
                {"mistake": "Сравниваю hist с разным binwidth", "why_bad": "Визуально разные, хотя данные одинаковы", "fix": "Используй одинаковые bins или density=True"},
                {"mistake": "Box plot для категориальных данных", "why_bad": "Box имеет смысл только для числовых", "fix": "Для категорий — bar с count или countplot"},
                {"mistake": "plt.boxplot([a, b, c]) без подписей", "why_bad": "Не понятно, какая коробка — какой группе", "fix": "Передай labels= или используй tick_labels="},
                {"mistake": "Считаю среднее вместо медианы для скошенного", "why_bad": "Среднее сдвигается выбросами, медиана стабильнее", "fix": "Box plot показывает медиану — это и есть робастная оценка центра"},
            ]),
            interview_questions([
                {"q": "Как выбрать bins в гистограмме?",
                 "a": "Правило Стурджеса: bins = log2(n) + 1. Правило Фридмана-Диакониса: 2·IQR/n^(1/3). На практике — пробуй 20-50 и смотри глазами."},
                {"q": "Что показывает box plot, чего не показывает hist?",
                 "a": "Box компактно показывает 5 статистик (min, Q1, median, Q3, max) + выбросы. Удобен для сравнения групп. Hist лучше показывает форму распределения (мультимодальность)."},
                {"q": "Что такое IQR?",
                 "a": "Inter-Quartile Range = Q3 - Q1. Это размах средних 50% данных. Усы boxplot — 1.5×IQR от ящика. Точки за усами — outliers."},
            ]),
            knowledge_checklist([
                "Использую plt.hist() с bins",
                "Использую density=True для сравнения с теоретическим распределением",
                "Использую alpha < 1 при наложении нескольких hist",
                "Читаю box plot: медиана, IQR, усы, выбросы",
                "Использую np.percentile(data, [25, 50, 75]) для квантилей",
                "Применяю np.random.seed для воспроизводимости",
            ]),
        ],
        exercises=[
            ex(1, "python", "Сгенерируй 500 значений N(100, 15), построй hist с bins=25, подпиши оси.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\ndata = np.random.normal(100, 15, 500)\nplt.hist(data, bins=25, color='teal', edgecolor='black')\nplt.title('Распределение N(100, 15)')\nplt.xlabel('Значение')\nplt.ylabel('Частота')\nplt.show()",
               [{"check": "True", "msg": "Гистограмма построена"}],
               ["np.random.normal(mean, std, n)", "bins=25 — 25 интервалов"], 1),
            ex(2, "python", "Наложение двух hist с alpha=0.5: N(0,1) и N(2,1), по 500 точек.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\na = np.random.normal(0, 1, 500)\nb = np.random.normal(2, 1, 500)\nplt.hist(a, bins=30, alpha=0.5, label='N(0,1)', color='steelblue')\nplt.hist(b, bins=30, alpha=0.5, label='N(2,1)', color='orangered')\nplt.legend()\nplt.title('Два распределения')\nplt.show()",
               [{"check": "True", "msg": "Наложение работает"}],
               ["alpha=0.5 — полупрозрачность", "label + legend — подписи"], 1),
            ex(3, "python", "Box plot для 3 групп: a = N(0,1), b = N(0,2), c = uniform(0,1).",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\ndata = [np.random.normal(0, 1, 100), np.random.normal(0, 2, 100), np.random.uniform(0, 1, 100)]\nlabels = ['N(0,1)', 'N(0,2)', 'U(0,1)']\nplt.boxplot(data, tick_labels=labels)\nplt.title('Сравнение 3 распределений')\nplt.ylabel('Значение')\nplt.show()",
               [{"check": "True", "msg": "Box plot построен"}],
               ["boxplot принимает список массивов", "tick_labels — подписи групп"], 2),
            ex(4, "python", "Hist с density=True и наложением теоретической PDF (нормальное).",
               "import matplotlib.pyplot as plt\nimport numpy as np\n# np.exp(-x**2/2)/np.sqrt(2*np.pi) — формула нормального распределения\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\ndata = np.random.normal(0, 1, 1000)\nplt.hist(data, bins=30, density=True, alpha=0.5, label='Эмпирическая')\nxs = np.linspace(-4, 4, 200)\npdf = np.exp(-xs**2/2) / np.sqrt(2*np.pi)\nplt.plot(xs, pdf, 'r-', linewidth=2, label='Теоретическая N(0,1)')\nplt.legend()\nplt.title('Hist + PDF')\nplt.show()",
               [{"check": "True", "msg": "PDF наложена"}],
               ["density=True нормирует в плотность", "Формула нормального распределения"], 3),
            ex(5, "python", "Cumulative hist: cumulative=True.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\ndata = np.random.normal(0, 1, 1000)\nplt.hist(data, bins=30, cumulative=True, color='slateblue', edgecolor='white')\nplt.title('Кумулятивная гистограмма')\nplt.xlabel('Значение')\nplt.ylabel('<= значения')\nplt.show()",
               [{"check": "True", "msg": "Кумулятивная hist построена"}],
               ["cumulative=True — накопительная", "Y — кол-во точек <= X"], 2),
            ex(6, "python", "Box plot горизонтальный: vert=False.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\ndata = [np.random.normal(0, 1, 100), np.random.normal(2, 0.5, 100)]\nplt.boxplot(data, vert=False, tick_labels=['A', 'B'], patch_artist=True)\nplt.title('Горизонтальные box plots')\nplt.xlabel('Значение')\nplt.show()",
               [{"check": "True", "msg": "Горизонтальный box plot построен"}],
               ["vert=False — горизонтальный", "patch_artist=True — заливка цветом"], 2),
            ex(7, "python", "Hist с range=(0, 10) — обрежь данные вне диапазона.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\ndata = np.random.normal(5, 3, 1000)\nplt.hist(data, bins=30, range=(0, 10), color='goldenrod', edgecolor='black')\nplt.title('Hist с range=(0, 10)')\nplt.show()",
               [{"check": "True", "msg": "Hist с range построена"}],
               ["range= обрезает данные", "Полезно для выбросов"], 2),
            ex(8, "python", "Подсветка выбросов: box plot с fliers (точки выбросов) красным цветом.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\ndata = np.concatenate([np.random.normal(0, 1, 100), [10, -8, 12]])\nbp = plt.boxplot(data, patch_artist=True)\nfor flier in bp['fliers']:\n    flier.set(marker='o', markerfacecolor='red', markersize=10, markeredgecolor='red')\nplt.title('Box plot с красными outliers')\nplt.show()",
               [{"check": "True", "msg": "Выбросы выделены"}],
               ["bp['fliers'] — точки за усами", "markerfacecolor — цвет заливки маркера"], 3),
            ex(9, "python", "Сравни 4 группы через boxplot: создай список из 4 numpy-массивов.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\ndata = [np.random.normal(i, 1, 100) for i in range(4)]\nplt.boxplot(data, patch_artist=True, tick_labels=['A','B','C','D'])\nplt.title('4 группы')\nplt.ylabel('Значение')\nplt.grid(True, alpha=0.3)\nplt.show()",
               [{"check": "True", "msg": "4 группы на box plot"}],
               ["List comprehension для 4 групп", "patch_artist=True для заливки"], 2),
            ex(10, "python", "Hist + box на одном рисунке через gridspec.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nimport matplotlib.gridspec as gridspec\nnp.random.seed(42)\ndata = np.random.normal(0, 1, 500)\nfig = plt.figure(figsize=(8, 6))\ngs = gridspec.GridSpec(2, 1, height_ratios=[3, 1])\nax1 = fig.add_subplot(gs[0])\nax2 = fig.add_subplot(gs[1])\nax1.hist(data, bins=30, color='steelblue', edgecolor='white')\nax2.boxplot(data, vert=False, patch_artist=True)\nax1.set_title('Hist сверху, Box снизу')\nplt.tight_layout()\nplt.show()",
               [{"check": "True", "msg": "Hist + box комбинация"}],
               ["gridspec для сложной раскладки", "height_ratios — пропорции высот"], 3),
        ],
        minutes=50, difficulty=2,
    )


def _4_5():
    return lesson(
        "4.5", "Seaborn: статистические визуализации", "space", [
            theory(
                "**Seaborn** — высокоуровневая библиотека поверх matplotlib. "
                "Девиз: «красивые графики по умолчанию».\n\n"
                "**Основные функции Seaborn:**\n"
                "- `sns.histplot(data, x=, hue=)` — гистограмма с группировкой\n"
                "- `sns.boxplot(data, x=, y=)` — box plot с разбивкой по категории\n"
                "- `sns.violinplot(data, x=, y=)` — box plot + плотность (силуэт скрипки)\n"
                "- `sns.scatterplot(data, x=, y=, hue=, size=)` — scatter с автоматической легендой\n"
                "- `sns.lineplot(data, x=, y=, hue=)` — линия с доверительным интервалом\n"
                "- `sns.barplot(data, x=, y=)` — bar со средним и CI (вместо суммы)\n"
                "- `sns.heatmap(matrix, annot=True)` — тепловая карта с числами\n"
                "- `sns.pairplot(data, hue=)` — все пары переменных сразу\n\n"
                "**Преимущества seaborn:**\n"
                "- Работа с DataFrame напрямую (`data=df, x='col1'`)\n"
                "- Hue — раскраска по категории одной строкой\n"
                "- Автоматические доверительные интервалы (CI)\n"
                "- Красивые темы: `sns.set_style('whitegrid')`, `darkgrid`, `ticks`\n\n"
                "**В нашей браузерной песочнице seaborn может не загрузиться** "
                "(требует pandas). Поэтому ниже мы реализуем аналоги через matplotlib, "
                "но в реальных проектах предпочитайте seaborn."
            ),
            analogy(
                "Matplotlib — кисть и краски (полный контроль). Seaborn — готовые фото-фильтры: одна команда — красивый график.",
                "Matplotlib: plt.bar(planets, masses). Seaborn: sns.barplot(data=df, x='planet', y='mass', hue='mission')."
            ),
            visual(
                "Seaborn vs Matplotlib: один и тот же график, разный объём кода",
                "  Matplotlib (8 строк):        Seaborn (3 строки):\n"
                "  plt.hist(a, alpha=0.5)       sns.histplot(data=df,\n"
                "  plt.hist(b, alpha=0.5)             x='value',\n"
                "  plt.legend()                         hue='group')\n"
                "  plt.title(...)\n"
                "  plt.xlabel(...)\n"
                "  plt.ylabel(...)\n"
                "  plt.grid(True)\n"
                "  plt.show()\n"
                "  \n"
                "  → Seaborn экономит время на типовых графиках."
            ),
            example(
                "Эквивалент sns.boxplot в matplotlib: 3 группы на одном box plot с цветами.",
                "Seaborn делает это в одну строку с DataFrame. Matplotlib требует больше кода, но работает в браузере.",
                "import matplotlib.pyplot as plt\n"
                "import numpy as np\n"
                "np.random.seed(42)\n"
                "groups = ['Falcon 9', 'Atlas V', 'Ariane 5']\n"
                "data = [np.random.normal(i, 1, 50) for i in range(3)]\n"
                "colors = ['#4C72B0', '#DD8452', '#55A868']\n"
                "fig, ax = plt.subplots(figsize=(8, 6))\n"
                "bp = ax.boxplot(data, patch_artist=True, tick_labels=groups)\n"
                "for patch, color in zip(bp['boxes'], colors):\n"
                "    patch.set_facecolor(color)\n"
                "ax.set_title('Сравнение эффективности ракет')\n"
                "ax.set_ylabel('Эффективность, %')\n"
                "ax.grid(True, alpha=0.3)\n"
                "plt.show()",
                "[3 цветных box plot'а рядом, медианы смещены, общая сетка]",
                "patch_artist=True включает заливку. zip(bp['boxes'], colors) связывает ящики с цветами. set_facecolor красит конкретный ящик."
            ),
            common_mistakes([
                {"mistake": "sns.boxplot(data=df) без x= и y=", "why_bad": "Seaborn не поймёт, что с чем сравнивать", "fix": "Укажи явно: x='category', y='value'"},
                {"mistake": "Смешиваю seaborn и matplotlib axes", "why_bad": "Seaborn использует текущие axes — могут конфликтовать", "fix": "Передавай ax= в sns-функции"},
                {"mistake": "Забыл sns.set_theme() или sns.set_style()", "why_bad": "Стандартный стиль matplotlib — не seaborn", "fix": "sns.set_style('whitegrid') в начале"},
                {"mistake": "sns.pairplot(df) на 50-колоночном DataFrame", "why_bad": "50x50=2500 графиков, браузер зависнет", "fix": "Выбери нужные колонки: sns.pairplot(df[col_list])"},
                {"mistake": "Seaborn без pip install seaborn", "why_bad": "ModuleNotFoundError", "fix": "pip install seaborn (в обычном Python)"},
            ]),
            interview_questions([
                {"q": "Зачем seaborn, если есть matplotlib?",
                 "a": "Seaborn: 1) удобная работа с DataFrame (data=df, x=col, y=col), 2) hue= для раскраски по категории одной строкой, 3) автоматические CI, 4) статистические графики (violin, swarm) из коробки. Минус — меньше контроля над деталями."},
                {"q": "Что такое violin plot?",
                 "a": "Комбинация box plot и KDE: ширина 'скрипки' в каждой точке показывает плотность. Видно, есть ли несколько мод, чего box не показывает."},
                {"q": "Что делает параметр hue?",
                 "a": "Раскрашивает элементы по значениям категориальной переменной. sns.scatterplot(df, x='a', y='b', hue='group') — точки разных групп разными цветами."},
            ]),
            knowledge_checklist([
                "Знаю, что seaborn — надстройка над matplotlib",
                "Использую sns.histplot, sns.boxplot, sns.scatterplot (концептуально)",
                "Понимаю hue= для раскраски по категории",
                "Могу воспроизвести seaborn-график через matplotlib",
                "Знаю про sns.set_style() и sns.set_theme()",
            ]),
        ],
        exercises=[
            ex(1, "python", "Эквивалент sns.histplot: hist для 3 групп на одних осях с легендой.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\ngroups = {'A': np.random.normal(0, 1, 300), 'B': np.random.normal(2, 1, 300), 'C': np.random.normal(-1, 0.5, 300)}\ncolors = ['steelblue', 'coral', 'teal']\nfor (name, data), c in zip(groups.items(), colors):\n    plt.hist(data, bins=25, alpha=0.5, color=c, label=name)\nplt.legend()\nplt.title('Гистограмма по группам (аналог sns.histplot)')\nplt.show()",
               [{"check": "True", "msg": "Группы отображены"}],
               ["hue= в seaborn = цикл по группам в matplotlib", "alpha=0.5 для прозрачности"], 1),
            ex(2, "python", "Эквивалент sns.boxplot с hue: 2 группы x 2 подгруппы.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\nfig, ax = plt.subplots()\ndata1 = np.random.normal(0, 1, 100)\ndata2 = np.random.normal(0.5, 1, 100)\ndata3 = np.random.normal(0, 0.5, 100)\ndata4 = np.random.normal(0.5, 0.5, 100)\nax.boxplot([data1, data2, data3, data4], tick_labels=['A1','A2','B1','B2'], patch_artist=True)\nplt.title('Boxplot с группами и подгруппами')\nplt.show()",
               [{"check": "True", "msg": "Box plot с группами"}],
               ["tick_labels=4 — 4 категории", "patch_artist=True для заливки"], 2),
            ex(3, "python", "Эквивалент sns.scatterplot с hue: 3 категории, разные цвета.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\ncolors_map = {'Mars': 'red', 'Earth': 'blue', 'Jupiter': 'orange'}\nfor planet, c in colors_map.items():\n    n = 50\n    x = np.random.normal(hash(planet) % 5, 1, n)\n    y = np.random.normal(hash(planet) % 4, 1, n)\n    plt.scatter(x, y, c=c, label=planet, alpha=0.6, s=50)\nplt.legend()\nplt.title('Scatter с категориями (аналог hue)')\nplt.show()",
               [{"check": "True", "msg": "Scatter с категориями"}],
               ["hue=scatterplot = цикл по категориям", "label= для легенды"], 2),
            ex(4, "python", "Эквивалент sns.lineplot с доверительным интервалом (заливка).",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\nx = np.linspace(0, 10, 20)\ny = np.sin(x) + np.random.normal(0, 0.2, 20)\nplt.plot(x, y, 'o-', color='teal', label='Среднее')\nplt.fill_between(x, y - 0.4, y + 0.4, alpha=0.3, color='teal', label='CI')\nplt.legend()\nplt.title('Lineplot с CI (аналог sns.lineplot)')\nplt.show()",
               [{"check": "True", "msg": "CI отображено"}],
               ["fill_between — аналог CI", "В seaborn CI считается автоматически"], 2),
            ex(5, "python", "Стиль seaborn через matplotlib: plt.style.use('seaborn-v0_8-whitegrid').",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nplt.style.use('seaborn-v0_8-whitegrid')\nnp.random.seed(42)\ndata = [np.random.normal(0, 1, 100), np.random.normal(2, 1, 100)]\nplt.boxplot(data, tick_labels=['A', 'B'], patch_artist=True)\nplt.title('Seaborn-стиль через matplotlib')\nplt.show()",
               [{"check": "True", "msg": "Стиль применён"}],
               ["seaborn-v0_8-* — встроенные стили", "В новых версиях matplotlib есть стили seaborn"], 2),
            ex(6, "python", "Аналог sns.violinplot через KDE: построй KDE-кривые для двух групп.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\ndef kde(x, points):\n    n = len(x)\n    h = 1.06 * np.std(x) * n**(-1/5)\n    return np.array([np.sum(np.exp(-0.5*((points - xi)/h)**2) / (h*np.sqrt(2*np.pi))) / n for xi in x])\nnp.random.seed(42)\na = np.random.normal(0, 1, 200)\nb = np.random.normal(2, 1, 200)\nxs = np.linspace(-4, 6, 200)\nplt.fill_between(xs, kde(a, xs), alpha=0.4, label='A', color='steelblue')\nplt.fill_between(xs, kde(b, xs), alpha=0.4, label='B', color='coral')\nplt.legend()\nplt.title('KDE (аналог violinplot)')\nplt.show()",
               [{"check": "True", "msg": "KDE построена"}],
               ["KDE = оценка плотности", "Violinplot = box + KDE"], 3),
            ex(7, "python", "Аналог sns.barplot: bar со средним и errorbar (вертикальные чёрточки).",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\ngroups = ['A', 'B', 'C', 'D']\ndata = [np.random.normal(i, 1, 30) for i in range(4)]\nmeans = [d.mean() for d in data]\nsems = [d.std() / np.sqrt(len(d)) for d in data]\nplt.bar(groups, means, yerr=sems, capsize=5, color='slateblue', edgecolor='black')\nplt.title('Bar с доверительными интервалами (аналог sns.barplot)')\nplt.ylabel('Среднее +/- SEM')\nplt.show()",
               [{"check": "True", "msg": "Bar с CI построен"}],
               ["yerr= — планки погрешности", "capsize=5 — засечки на планках"], 3),
            ex(8, "python", "Scatter с линией регрессии (аналог sns.regplot).",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\nx = np.random.normal(0, 1, 100)\ny = 2*x + 1 + np.random.normal(0, 0.5, 100)\nslope, intercept = np.polyfit(x, y, 1)\nplt.scatter(x, y, alpha=0.5, color='steelblue')\nxs = np.linspace(x.min(), x.max(), 100)\nplt.plot(xs, slope*xs + intercept, 'r-', linewidth=2, label=f'y={slope:.2f}x+{intercept:.2f}')\nplt.legend()\nplt.title('Regression plot')\nplt.show()",
               [{"check": "True", "msg": "Регрессия проведена"}],
               ["polyfit(..., 1) — линейная регрессия", "В seaborn sns.regplot делает это в 1 строку"], 3),
            ex(9, "python", "Гистограмма с разбивкой по группам через plt.subplots(1, 3).",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\nfig, axes = plt.subplots(1, 3, figsize=(15, 4))\nfor ax, mu in zip(axes, [0, 2, -1]):\n    data = np.random.normal(mu, 1, 500)\n    ax.hist(data, bins=25, color='teal', edgecolor='white', alpha=0.7)\n    ax.set_title(f'N({mu}, 1)')\n    ax.set_ylim(0, 130)\nplt.tight_layout()\nplt.show()",
               [{"check": "True", "msg": "3 гистограммы в ряд"}],
               ["Одна ось Y для сравнения (ylim)", "subplots(1, 3) — 1 строка, 3 столбца"], 2),
            ex(10, "python", "Categorical scatter (strip-plot аналог) — точки с jitter по X.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\ncategories = ['A', 'B', 'C']\nfor i, cat in enumerate(categories):\n    y = np.random.normal(i, 0.3, 30)\n    x = np.random.uniform(i - 0.2, i + 0.2, 30)\n    plt.scatter(x, y, alpha=0.5, s=30)\nplt.xticks(range(3), categories)\nplt.title('Strip plot (аналог sns.stripplot)')\nplt.show()",
               [{"check": "True", "msg": "Strip plot построен"}],
               ["x сдвигается случайно — jitter", "Видно плотность по Y"], 3),
        ],
        minutes=45, difficulty=2,
    )


def _4_6():
    return lesson(
        "4.6", "Heatmap и pairplot", "space", [
            theory(
                "**Heatmap** (тепловая карта) — двумерная визуализация, где цвет "
                "кодирует значение. Самый частый случай — корреляционная матрица.\n\n"
                "**plt.imshow(matrix, cmap=, aspect=):**\n"
                "- `cmap='viridis'` — последовательная палитра (низкие→высокие)\n"
                "- `cmap='coolwarm'` — расходящаяся (отрицательные/положительные)\n"
                "- `cmap='RdBu_r'` — то же, в красно-синих тонах\n"
                "- `aspect='auto'` — растягивает ячейки; 'equal' — квадратные\n"
                "- `plt.colorbar()` — шкала цветов\n\n"
                "**plt.pcolormesh(matrix)** — альтернатива imshow для сеток, "
                "поддерживает неравномерные шаги.\n\n"
                "**Pairplot (scatter matrix):**\n"
                "Показывает все пары переменных в таблице. Диагональ — гистограммы, "
                "вне диагонали — scatter. Идеален для первичного обзора данных.\n\n"
                "**Когда использовать:**\n"
                "- Heatmap — корреляции, матрицы ошибок, временные ряды (год×месяц)\n"
                "- Pairplot — первые шаги EDA, поиск связей\n"
                "- Heatmap с аннотациями (`annot=True` в seaborn) — для отчётов"
            ),
            analogy(
                "Heatmap — карта погоды: тёплые зоны красные, холодные синие. Pairplot — фоторобот: каждый ракурс показывает свою грань.",
                "Heatmap: корреляция параметров двигателя. Pairplot: все пары телеметрии корабля."
            ),
            visual(
                "Heatmap и pairplot",
                "  Heatmap (5x5):           Pairplot (3 переменные):\n"
                "  +---+---+---+---+---+      y2 ^  \\    |  \\   |\n"
                "  |###|***|...|###|***|        |   \\   |  \\  |\n"
                "  |***|###|...|***|###|        |    \\  |   \\ |\n"
                "  |...|...|###|...|...|        |     \\ |    \\|\n"
                "  |###|***|...|###|***|        +------+-------->\n"
                "  |***|###|...|***|###|          y1     y2   y3\n"
                "  +---+---+---+---+---+         (диагональ: гистограммы)\n"
                "  # — высокое, . — низкое"
            ),
            example(
                "Сгенерируй 4 переменные с разной корреляцией. Построй корреляционную матрицу как heatmap.",
                "np.corrcoef возвращает матрицу. imshow показывает её как картинку. colorbar добавляет шкалу.",
                "import matplotlib.pyplot as plt\n"
                "import numpy as np\n"
                "np.random.seed(42)\n"
                "n = 500\n"
                "x1 = np.random.normal(0, 1, n)\n"
                "x2 = 0.8 * x1 + np.random.normal(0, 0.5, n)\n"
                "x3 = -0.5 * x1 + np.random.normal(0, 0.7, n)\n"
                "x4 = np.random.normal(0, 1, n)\n"
                "data = np.vstack([x1, x2, x3, x4])\n"
                "corr = np.corrcoef(data)\n"
                "fig, ax = plt.subplots(figsize=(7, 6))\n"
                "im = ax.imshow(corr, cmap='coolwarm', vmin=-1, vmax=1)\n"
                "ax.set_xticks(range(4))\n"
                "ax.set_yticks(range(4))\n"
                "ax.set_xticklabels(['X1','X2','X3','X4'])\n"
                "ax.set_yticklabels(['X1','X2','X3','X4'])\n"
                "for i in range(4):\n"
                "    for j in range(4):\n"
                "        ax.text(j, i, f'{corr[i,j]:.2f}', ha='center', va='center', color='black')\n"
                "plt.colorbar(im, ax=ax, label='r')\n"
                "plt.title('Корреляционная матрица')\n"
                "plt.show()",
                "[5x5 матрица: тёплые тона для +1, холодные для -1, диагональ = 1, числа в ячейках]",
                "vmin=-1, vmax=1 фиксируют шкалу: красный всегда +1, синий всегда -1. ax.text рисует числа в каждой ячейке."
            ),
            common_mistakes([
                {"mistake": "imshow без vmin/vmax", "why_bad": "Шкала плавает между графиками, нельзя сравнивать", "fix": "Зафиксируй vmin=-1, vmax=1 для корреляций"},
                {"mistake": "Pairplot на >10 переменных", "why_bad": "100 графиков, веб-страница зависнет", "fix": "Выбери 3-5 самых важных"},
                {"mistake": "Heatmap без colorbar", "why_bad": "Непонятно, какой цвет какому значению", "fix": "Всегда добавляй plt.colorbar()"},
                {"mistake": "Использование cmap='jet'", "why_bad": "Искажает восприятие (не линейно, не perceptually uniform)", "fix": "Используй 'viridis' (default), 'plasma', 'coolwarm'"},
                {"mistake": "Heatmap для категорий", "why_bad": "Цвет подразумевает порядок, у категорий его нет", "fix": "Для категорий — bar или grouped bar"},
            ]),
            interview_questions([
                {"q": "Что показывает корреляционная матрица?",
                 "a": "Линейную связь между всеми парами числовых переменных. Диагональ всегда 1 (переменная с собой). Симметрична относительно диагонали."},
                {"q": "Почему pairplot полезен в EDA?",
                 "a": "Одним взглядом видишь распределения (диагональ) и связи (вне диагонали). Помогает найти нелинейные зависимости, кластеры, выбросы, не замечаемые по одной метрике."},
                {"q": "Чем diverging colormap отличается от sequential?",
                 "a": "Sequential ('viridis') — для значений от 0 до max (один смысловой полюс). Diverging ('coolwarm') — для значений с осмысленным нулём (корреляция, прибыль/убыток) — белый/нейтральный цвет в центре."},
            ]),
            knowledge_checklist([
                "Использую plt.imshow() для матриц и сеток",
                "Задаю cmap='viridis' или 'coolwarm' осмысленно",
                "Фиксирую vmin/vmax для воспроизводимости",
                "Добавляю colorbar для шкалы",
                "Использую pcolormesh для неравномерных сеток",
                "Подписываю оси и добавляю числа через ax.text",
            ]),
        ],
        exercises=[
            ex(1, "python", "Создай матрицу 5x5 (np.random.rand(5,5)), покажи через imshow с cmap='viridis'.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\nm = np.random.rand(5, 5)\nplt.imshow(m, cmap='viridis')\nplt.colorbar()\nplt.title('Случайная матрица 5x5')\nplt.show()",
               [{"check": "True", "msg": "Heatmap построена"}],
               ["imshow для 2D массивов", "viridis — стандартная палитра"], 1),
            ex(2, "python", "Корреляционная матрица для 4 переменных с числами в ячейках.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\ndata = np.random.randn(4, 200)\ncorr = np.corrcoef(data)\nfig, ax = plt.subplots()\nim = ax.imshow(corr, cmap='coolwarm', vmin=-1, vmax=1)\nfor i in range(4):\n    for j in range(4):\n        ax.text(j, i, f'{corr[i,j]:.2f}', ha='center', va='center')\nplt.colorbar(im)\nplt.title('Корреляция 4 переменных')\nplt.show()",
               [{"check": "True", "msg": "Корреляционная heatmap построена"}],
               ["vmin/vmax=±1 фиксируют шкалу", "coolwarm — diverging палитра"], 2),
            ex(3, "python", "pcolormesh для неравномерной сетки (X, Y, Z разных размеров).",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nx = np.arange(11)\ny = np.arange(11)\nX, Y = np.meshgrid(x, y)\nZ = np.sin(X*0.5) * np.cos(Y*0.5)\nplt.pcolormesh(X, Y, Z, cmap='plasma', shading='auto')\nplt.colorbar(label='Z')\nplt.title('pcolormesh')\nplt.xlabel('X')\nplt.ylabel('Y')\nplt.show()",
               [{"check": "True", "msg": "pcolormesh построен"}],
               ["pcolormesh — для произвольных сеток", "shading='auto' — авто-выбор заливки"], 2),
            ex(4, "python", "Матрица ошибок 3x3 как heatmap: diagonal=10, off=2.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\ncm = np.array([[10, 1, 2], [2, 8, 1], [1, 2, 9]])\nplt.imshow(cm, cmap='Blues')\nfor i in range(3):\n    for j in range(3):\n        plt.text(j, i, str(cm[i,j]), ha='center', va='center', color='red' if cm[i,j] < 5 else 'white')\nplt.colorbar()\nplt.title('Матрица ошибок')\nplt.show()",
               [{"check": "True", "msg": "Confusion matrix heatmap построена"}],
               ["Confusion matrix — стандартный heatmap в ML", "Цвет текста зависит от яркости фона"], 2),
            ex(5, "python", "Pairplot вручную: scatter matrix 3x3 через subplots.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\ndata = np.random.randn(200, 3)\nlabels = ['X', 'Y', 'Z']\nfig, axes = plt.subplots(3, 3, figsize=(9, 9))\nfor i in range(3):\n    for j in range(3):\n        if i == j:\n            axes[i, j].hist(data[:, i], bins=20, color='steelblue', edgecolor='white')\n        else:\n            axes[i, j].scatter(data[:, j], data[:, i], s=10, alpha=0.5)\n        if i == 2: axes[i, j].set_xlabel(labels[j])\n        if j == 0: axes[i, j].set_ylabel(labels[i])\nplt.tight_layout()\nplt.show()",
               [{"check": "True", "msg": "Pairplot построен"}],
               ["i==j — гистограмма, иначе scatter", "sns.pairplot делает то же в 1 строку"], 2),
            ex(6, "python", "Heatmap с временной шкалой: год по X, месяц по Y, данные — температура.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nmonths = ['Янв','Фев','Мар','Апр','Май','Июн','Июл','Авг','Сен','Окт','Ноя','Дек']\nyears = [2020, 2021, 2022, 2023]\nnp.random.seed(42)\ndata = np.random.normal(15, 10, (4, 12))\nfig, ax = plt.subplots(figsize=(10, 4))\nim = ax.imshow(data, cmap='RdYlBu_r', aspect='auto')\nax.set_xticks(range(12))\nax.set_xticklabels(months)\nax.set_yticks(range(4))\nax.set_yticklabels(years)\nplt.colorbar(im, label='Температура, °C')\nplt.title('Температура по месяцам')\nplt.show()",
               [{"check": "True", "msg": "Временная heatmap построена"}],
               ["aspect='auto' — растягивает подписи", "Цветом кодируется третья переменная"], 2),
            ex(7, "python", "contour plot (контурный график) через plt.contourf.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nx = np.linspace(-3, 3, 100)\ny = np.linspace(-3, 3, 100)\nX, Y = np.meshgrid(x, y)\nZ = np.exp(-(X**2 + Y**2))\nplt.contourf(X, Y, Z, levels=15, cmap='viridis')\nplt.colorbar(label='Z')\nplt.title('contourf')\nplt.xlabel('X')\nplt.ylabel('Y')\nplt.show()",
               [{"check": "True", "msg": "Контурный график построен"}],
               ["contourf — залитые контуры", "levels=15 — 15 уровней"], 2),
            ex(8, "python", "Двухцветная heatmap: red для +, blue для −.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\nm = np.random.randn(5, 5)\nplt.imshow(m, cmap='RdBu_r', vmin=-2, vmax=2)\nfor i in range(5):\n    for j in range(5):\n        plt.text(j, i, f'{m[i,j]:.1f}', ha='center', va='center', color='black')\nplt.colorbar()\nplt.title('Diverging heatmap')\nplt.show()",
               [{"check": "True", "msg": "Diverging heatmap построена"}],
               ["RdBu_r — красно-синяя diverging", "0 в центре — белый/нейтральный"], 2),
            ex(9, "python", "Heatmap пропусков: NaN — белым, остальное — viridis.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\nm = np.random.rand(10, 10)\nm[np.random.rand(10, 10) > 0.7] = np.nan\nmasked = np.ma.masked_invalid(m)\ncmap = plt.cm.viridis.copy()\ncmap.set_bad('white')\nplt.imshow(masked, cmap=cmap, aspect='auto')\nplt.colorbar()\nplt.title('Пропуски (белые) и значения')\nplt.show()",
               [{"check": "True", "msg": "Heatmap пропусков построена"}],
               ["np.ma.masked_invalid скрывает NaN", "set_bad('white') — цвет для NaN"], 3),
            ex(10, "python", "3D-surface heatmap: 10x10 значений, построй как imshow с аннотациями.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\nm = np.random.randint(0, 100, (10, 10))\nfig, ax = plt.subplots(figsize=(8, 8))\nax.imshow(m, cmap='YlOrRd')\nax.set_xticks(range(10))\nax.set_yticks(range(10))\nfor i in range(10):\n    for j in range(10):\n        ax.text(j, i, str(m[i,j]), ha='center', va='center', color='black' if m[i,j] > 50 else 'white', fontsize=8)\nplt.title('Сетка 10x10 с числами')\nplt.colorbar()\nplt.show()",
               [{"check": "True", "msg": "Heatmap с аннотациями построена"}],
               ["YlOrRd — красно-жёлтая", "Цвет текста зависит от фона"], 2),
        ],
        minutes=50, difficulty=3,
    )


def _4_7():
    return lesson(
        "4.7", "Как выбрать правильный тип графика", "space", [
            theory(
                "Неправильный график — это **обман**, даже если данные верные. "
                "Вот дерево решений:\n\n"
                "**1. Что показываем?**\n"
                "- **Одна числовая переменная** → hist, box, density (kde), violin\n"
                "- **Две числовые** → scatter, line (если X — время/порядок)\n"
                "- **Числовая + категориальная** → bar, box, violin, strip\n"
                "- **Две категориальные** → heatmap, grouped/stacked bar\n"
                "- **3+ числовые** → pairplot, scatter с цветом/размером, 3D\n"
                "- **Географические** → choropleth, scatter на карте\n\n"
                "**2. Какова цель?**\n"
                "- **Сравнить** категории → bar (НЕ pie)\n"
                "- **Показать тренд** во времени → line\n"
                "- **Показать связь** двух переменных → scatter\n"
                "- **Показать распределение** → hist, box\n"
                "- **Показать долю** целого → pie (только ≤5 сегментов!)\n"
                "- **Показать часть целого с динамикой** → stacked bar / area\n\n"
                "**3. Сколько данных?**\n"
                "- < 30 точек — избегай bar/pie, рискуешь misleading\n"
                "- 30–1000 — scatter, box, hist\n"
                "- > 1000 — нужен alpha/hexbin/density\n\n"
                "**Правила хорошего тона:**\n"
                "- Y-axis начинается с 0 для bar\n"
                "- Не обрезай ось Y, чтобы преувеличить разницу\n"
                "- Подписи, легенда, единицы измерения\n"
                "- Цвет = категория, не украшение"
            ),
            analogy(
                "Выбор графика — выбор инструмента: молотком не закручивают шурупы, отвёрткой не забивают гвозди.",
                "Скорость ракеты по времени — линейный. Сравнение 5 миссий — bar. Доля топлива — pie. Температура двигателя — hist."
            ),
            visual(
                "Дерево выбора графика",
                "                    +- Сравнить категории -> bar\n"
                "     Категории? ----+\n"
                "        |           +- Доли целого -> pie (<=5)\n"
                "        v\n"
                "   Тип данных?     +- 1 числовая -> hist/box\n"
                "        |\n"
                "        +- Числовые? --- 2 числовые -> scatter/line\n"
                "        |\n"
                "        +- Гео? -> карта\n"
                "        \n"
                "  Время?  -> line\n"
                "  Связь?  -> scatter\n"
                "  Распред. -> hist/box"
            ),
            example(
                "Одни и те же данные — 3 разных графика. Данные: кол-во спутников по типу орбиты (LEO=5000, MEO=150, GEO=500, HEO=10).",
                "Pie подходит, потому что <=4 сегмента. Bar лучше для точного сравнения. Line здесь бессмысленно — категории не упорядочены по времени.",
                "import matplotlib.pyplot as plt\n"
                "labels = ['LEO', 'MEO', 'GEO', 'HEO']\n"
                "counts = [5000, 150, 500, 10]\n"
                "fig, axes = plt.subplots(1, 2, figsize=(12, 5))\n"
                "axes[0].bar(labels, counts, color=['#4C72B0','#DD8452','#55A868','#C44E52'])\n"
                "axes[0].set_title('Спутники по орбитам (bar — лучший выбор)')\n"
                "axes[0].set_ylabel('Количество')\n"
                "axes[1].pie(counts, labels=labels, autopct='%1.1f%%', startangle=90)\n"
                "axes[1].set_title('Доли (pie — LEO 88%)')\n"
                "plt.show()",
                "[Bar: LEO — гигантский столбец. Pie: 88% синий кусок. Line не подходит — нет оси времени]",
                "Bar показывает абсолютные числа, pie — проценты. Для 'сколько спутников' лучше bar: '5000' понятнее '88%'."
            ),
            common_mistakes([
                {"mistake": "Pie с 12 сегментами", "why_bad": "Невозможно прочитать, не работают углы", "fix": "Топ-5 + 'Другое' или используй bar"},
                {"mistake": "Bar для временного ряда", "why_bad": "Теряется непрерывность тренда", "fix": "Line plot для времени"},
                {"mistake": "Line для категорий", "why_bad": "Линия между 'Меркурий' и 'Юпитер' бессмысленна", "fix": "Bar для категорий"},
                {"mistake": "3D pie chart", "why_bad": "Искажает пропорции, читать невозможно", "fix": "Никогда. Используй 2D pie или bar"},
                {"mistake": "Bar с обрезанной осью Y", "why_bad": "Разница 5% выглядит как 50%", "fix": "Y начинается с 0 для bar"},
                {"mistake": "Heatmap для несвязанных категорий", "why_bad": "Цвет подразумевает порядок", "fix": "Bar/table"},
            ]),
            interview_questions([
                {"q": "Как выбрать между line и bar?",
                 "a": "Line — когда X непрерывный (время, расстояние) и важен тренд. Bar — когда X категориальный или важен дискретный счёт."},
                {"q": "Когда pie — плохой выбор?",
                 "a": "> 5-7 сегментов (каша), похожие доли (не отличить), нужна точность (глаз плохо оценивает углы), часть 3D pie (всегда)."},
                {"q": "Box plot или violin plot?",
                 "a": "Box — стандарт, компактен, понятен. Violin — показывает мультимодальность и форму, но тяжелее читается. Для 2-3 групп — box, для одной с глубоким анализом формы — violin."},
            ]),
            knowledge_checklist([
                "Различаю 5 типов данных: числовая, категориальная, время, гео, связь",
                "Выбираю line для времени",
                "Выбираю bar для сравнения категорий",
                "Выбираю pie только для долей ≤5",
                "Выбираю scatter для пары числовых",
                "Выбираю hist/box для распределения",
                "Избегаю 3D pie, обрезанных осей, bar для времени",
            ]),
        ],
        exercises=[
            ex(1, "python", "Температура двигателя за 60 секунд — какой график выбрать? Построй line.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\nt = np.arange(60)\nT = 2000 + 500*np.sin(t/10) + np.random.normal(0, 50, 60)\nplt.plot(t, T, color='orangered')\nplt.title('Температура двигателя (line — время)')\nplt.xlabel('Время, с')\nplt.ylabel('T, °C')\nplt.show()",
               [{"check": "True", "msg": "Line для времени построен"}],
               ["Время -> line, не bar", "Bar скрыл бы непрерывность тренда"], 1),
            ex(2, "python", "Сравнение массы 6 планет — какой график? Построй bar.",
               "import matplotlib.pyplot as plt\n",
               "import matplotlib.pyplot as plt\nplanets = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn']\nmasses = [0.055, 0.815, 1.0, 0.107, 317.8, 95.2]\nplt.bar(planets, masses, color='slateblue')\nplt.title('Массы планет (bar — категории)')\nplt.ylabel('Масса, M_Земли')\nplt.yscale('log')\nplt.show()",
               [{"check": "True", "msg": "Bar для категорий построен"}],
               ["Категории -> bar", "yscale('log') — иначе Юпитер задавит"], 1),
            ex(3, "python", "Распределение 1000 значений — какой график? Построй hist.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\ndata = np.random.exponential(2, 1000)\nplt.hist(data, bins=30, color='teal', edgecolor='white')\nplt.title('Распределение (hist — форма)')\nplt.xlabel('Значение')\nplt.show()",
               [{"check": "True", "msg": "Hist для распределения построен"}],
               ["Распределение -> hist или kde", "Box не покажет мультимодальность"], 1),
            ex(4, "python", "Связь высоты и температуры — какой график? Построй scatter.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\naltitude = np.random.uniform(0, 10000, 200)\ntemp = 25 - altitude/200 + np.random.normal(0, 2, 200)\nplt.scatter(altitude, temp, alpha=0.5, s=20, color='steelblue')\nplt.title('Высота vs температура (scatter — связь)')\nplt.xlabel('Высота, м')\nplt.ylabel('Температура, °C')\nplt.show()",
               [{"check": "True", "msg": "Scatter для связи построен"}],
               ["Связь 2 переменных -> scatter", "Видна линейная обратная зависимость"], 1),
            ex(5, "python", "Доли расхода топлива по этапам полёта — какой график? Построй pie (5 сегментов).",
               "import matplotlib.pyplot as plt\n",
               "import matplotlib.pyplot as plt\nstages = ['Взлёт', 'Разгон', 'Выход на орбиту', 'Манёвры', 'Сход']\nfuel = [40, 35, 15, 7, 3]\nplt.pie(fuel, labels=stages, autopct='%1.0f%%', startangle=90)\nplt.title('Расход топлива (pie — 5 сегментов ОК)')\nplt.show()",
               [{"check": "True", "msg": "Pie для долей построен"}],
               ["5 сегментов — граница допустимого", "Взлёт+Разгон = 75%"], 1),
            ex(6, "python", "Плохой выбор: pie с 10 сегментами. Перестрой на bar.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\nlabels = [f'S{i}' for i in range(10)]\nvalues = np.random.rand(10)\nplt.bar(labels, values, color='coral')\nplt.title('Перестроили pie -> bar (так лучше)')\nplt.ylabel('Значение')\nplt.show()",
               [{"check": "True", "msg": "Pie перестроен в bar"}],
               [">5 сегментов -> bar", "Pie с 10+ кусками нечитаем"], 2),
            ex(7, "python", "Сравнение 3 ракет-носителей по 3 параметрам — какой график? Grouped bar.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nrockets = ['Falcon 9', 'Atlas V', 'Ariane 5']\npayload = [22.8, 18.0, 21.0]\nheight = [70, 58, 53]\ncost = [62, 110, 165]\nx = np.arange(3)\nwidth = 0.27\nplt.bar(x - width, payload, width, label='Полезная, т')\nplt.bar(x, height, width, label='Высота, м')\nplt.bar(x + width, cost, width, label='Стоимость, $M')\nplt.xticks(x, rockets)\nplt.legend()\nplt.title('3 ракеты x 3 параметра')\nplt.show()",
               [{"check": "True", "msg": "Grouped bar построен"}],
               ["3 категории x 3 параметра -> grouped bar", "width — ширина столбика в группе"], 2),
            ex(8, "python", "Box vs Hist: построй ОБА для одного набора, сравни.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\ndata = np.concatenate([np.random.normal(0, 1, 200), np.random.normal(5, 0.5, 100)])\nfig, axes = plt.subplots(1, 2, figsize=(12, 5))\naxes[0].boxplot(data, vert=False, patch_artist=True)\naxes[0].set_title('Box — не видно bimodality')\naxes[1].hist(data, bins=50, density=True, color='teal', alpha=0.7, edgecolor='white')\naxes[1].set_title('Hist — видно 2 пика')\nplt.show()",
               [{"check": "True", "msg": "Box vs hist сравнение"}],
               ["Box скрывает мультимодальность", "Hist показывает форму"], 3),
            ex(9, "python", "Облако из 5000 точек — какой график? Scatter с alpha=0.1.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\nx = np.random.randn(5000)\ny = 2*x + np.random.randn(5000)\nplt.scatter(x, y, s=5, alpha=0.1, color='steelblue')\nplt.title('5000 точек: scatter с alpha=0.1')\nplt.xlabel('X')\nplt.ylabel('Y')\nplt.show()",
               [{"check": "True", "msg": "Scatter с большим N"}],
               ["Много точек -> нужен alpha", "Без alpha — сплошная каша"], 2),
            ex(10, "python", "Площадной график (area): 3 накопленных значения по времени.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nt = np.arange(0, 20)\ny1 = t * 1.0\ny2 = t * 0.7\ny3 = t * 0.3\nplt.stackplot(t, y1, y2, y3, labels=['A','B','C'], colors=['steelblue','coral','gold'], alpha=0.7)\nplt.legend()\nplt.title('Stackplot (area chart)')\nplt.xlabel('Время')\nplt.ylabel('Накопленное значение')\nplt.show()",
               [{"check": "True", "msg": "Stackplot построен"}],
               ["Stackplot = area + категории", "Показывает динамику долей"], 3),
        ],
        minutes=45, difficulty=2,
    )


def _4_8():
    return lesson(
        "4.8", "Оформление и стиль: цвета, заголовки, легенды", "space", [
            theory(
                "График без хорошего оформления — как письмо без знаков препинания. "
                "Данные могут быть верными, но если их невозможно прочитать — толку мало.\n\n"
                "**Заголовок и подписи:**\n"
                "- `plt.title('Текст', fontsize=14, fontweight='bold')`\n"
                "- `plt.xlabel('X')`, `plt.ylabel('Y')`\n"
                "- Включай **единицы измерения**: 'Температура, °C', не 'Температура'\n"
                "- Включай **что показано**: 'Среднее ± SD' лучше 'Значение'\n\n"
                "**Цвета:**\n"
                "- Именованные: 'red', 'steelblue', 'coral', 'teal'\n"
                "- Hex: '#FF5733'\n"
                "- По индексу палитры: 'C0', 'C1'...\n"
                "- Из cmap: `cmap(0.5)` — число от 0 до 1\n"
                "- Прозрачность: `alpha=0..1`\n"
                "- **Цвет = смысл**: прибыль = зелёный, убыль = красный\n"
                "- **Цвет не должен избыточно кодировать** (если уже есть легенда)\n\n"
                "**Легенда:**\n"
                "- `plt.legend()` — автоматически по label= в plt.plot/scatter/bar\n"
                "- `loc='best'`, `'upper right'`, `'center'` и т.д.\n"
                "- `frameon=True/False` — рамка\n"
                "- `fontsize=10`\n\n"
                "**Сетка:**\n"
                "- `plt.grid(True, alpha=0.3, linestyle='--')`\n"
                "- Только для измерения значений, не везде\n\n"
                "**Стили:**\n"
                "- `plt.style.use('ggplot')`, `'seaborn-v0_8'`, `'bmh'`, `'fivethirtyeight'`\n"
                "- `plt.style.available` — список всех"
            ),
            analogy(
                "Оформление графика — причёска и костюм на собеседовании. Данные — резюме, без хорошего представления не оценят.",
                "График для отчёта NASA: тёмно-синий фон, белый шрифт, логотип, точные подписи с единицами."
            ),
            visual(
                "Элементы оформления",
                "  +---- Заголовок: 'bold, fontsize=14' ----+\n"
                "  |                                          |\n"
                "  |  Y ^                                     |\n"
                "  |    |  +- ylabel: 'Температура, °C' +    |\n"
                "  |    |/\\                               |    |\n"
                "  |    |  \\___    . . . grid  : - - -     |    |\n"
                "  |    |______\\_________________________> X |\n"
                "  |           xlabel: 'Время, с'             |\n"
                "  |  \\___                                     |\n"
                "  |  +- Легенда: '- A' (steelblue)  -+     |\n"
                "  |  |           '-- B' (coral)         |     |\n"
                "  |  +----------------------------------+     |\n"
                "  +------------------------------------------+"
            ),
            example(
                "Сделай 'отчётный' график: жирный заголовок, подписи с единицами, легенда, сетка, сохранение в PNG.",
                "Хороший график = данные + контекст (что, где, когда, единицы). savefig сохраняет в файл (или в буфер в браузере).",
                "import matplotlib.pyplot as plt\n"
                "import numpy as np\n"
                "np.random.seed(42)\n"
                "fig, ax = plt.subplots(figsize=(10, 6))\n"
                "x = np.linspace(0, 10, 100)\n"
                "ax.plot(x, np.sin(x), color='#1f77b4', linewidth=2, label='sin(x)')\n"
                "ax.plot(x, np.cos(x), color='#ff7f0e', linewidth=2, linestyle='--', label='cos(x)')\n"
                "ax.set_title('Тригонометрические функции\\n(частота дискретизации: 100 точек)', fontsize=14, fontweight='bold')\n"
                "ax.set_xlabel('Угол, радианы', fontsize=12)\n"
                "ax.set_ylabel('Значение функции', fontsize=12)\n"
                "ax.legend(loc='upper right', fontsize=11, frameon=True, shadow=True)\n"
                "ax.grid(True, alpha=0.3, linestyle='--')\n"
                "ax.set_xlim(0, 2*np.pi)\n"
                "plt.tight_layout()\n"
                "plt.show()",
                "[Чистый график с двумя кривыми, заголовком в 2 строки, легендой в правом верхнем углу, сеткой пунктиром]",
                "tight_layout() автоматически подгоняет отступы, чтобы подписи не обрезались. shadow=True добавляет тень легенде."
            ),
            common_mistakes([
                {"mistake": "Заголовок без единиц измерения", "why_bad": "'Температура' — это что? °C, °F, K?", "fix": "'Температура двигателя, °C'"},
                {"mistake": "Цвет ради красоты, не ради смысла", "why_bad": "Distracting, нарушает восприятие", "fix": "Цвет = категория, или состояние (хорошо/плохо)"},
                {"mistake": "Легенда перекрывает данные", "why_bad": "Важная часть графика скрыта", "fix": "loc='best' или вынеси за Axes"},
                {"mistake": "Шрифт 8pt или 20pt", "why_bad": "Мелкий не читается, крупный — выглядит детским", "fix": "10-14pt для подписей, 14-18 для заголовка"},
                {"mistake": "Белая сетка на белом фоне", "why_bad": "Сетки не видно", "fix": "Проверяй контраст"},
                {"mistake": "Hex код с ошибкой '#ZZZZZZ'", "why_bad": "Не парсится, падает на дефолт", "fix": "Валидные hex: #FF5733, не #GGGGGG"},
            ]),
            interview_questions([
                {"q": "Зачем нужна легенда?",
                 "a": "Чтобы читатель знал, какой цвет/маркер/линия что означает. Без легенды график с 3+ сериями — бесполезен."},
                {"q": "Когда использовать сетку?",
                 "a": "Когда нужно считывать значения с графика (научные/инженерные). Когда график иллюстративный, показывает тренд — сетка может мешать (используй минимальную или убери)."},
                {"q": "Что важнее: данные или оформление?",
                 "a": "Данные важнее. Плохой график с верными данными — полезен. Красивый график с неверными данными — вреден. Но хорошее оформление помогает понять верные данные."},
            ]),
            knowledge_checklist([
                "Всегда подписываю оси с единицами",
                "Заголовок информативный (что + единицы)",
                "Использую plt.legend() при >1 серии",
                "Задаю color осмысленно (категории, состояния)",
                "Используют alpha= для прозрачности",
                "Применяю plt.style.use() для готовых тем",
                "Использую tight_layout() или subplots_adjust",
            ]),
        ],
        exercises=[
            ex(1, "python", "Добавь к графику жирный заголовок fontsize=14, подписи осей с единицами.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nx = np.linspace(0, 10, 100)\nplt.plot(x, np.sin(x))\nplt.title('Синусоида', fontsize=14, fontweight='bold')\nplt.xlabel('Время, с', fontsize=12)\nplt.ylabel('Амплитуда, м', fontsize=12)\nplt.show()",
               [{"check": "True", "msg": "Заголовок и подписи добавлены"}],
               ["fontsize=14 — крупнее", "fontweight='bold' — жирный"], 1),
            ex(2, "python", "Построй 2 линии с разными цветами и стилями + легенду.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nx = np.linspace(0, 5, 50)\nplt.plot(x, x, color='steelblue', linestyle='-', marker='o', label='Линейная')\nplt.plot(x, x**2/5, color='coral', linestyle='--', marker='s', label='Квадратичная')\nplt.legend(loc='upper left')\nplt.title('Сравнение функций')\nplt.show()",
               [{"check": "True", "msg": "Легенда работает"}],
               ["label= в plt.plot", "loc='upper left' — положение"], 1),
            ex(3, "python", "Используй hex-коды цветов: '#E63946' (красный), '#1D3557' (тёмно-синий).",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nx = np.linspace(0, 5, 30)\nplt.plot(x, x, color='#E63946', linewidth=2, label='Серия A')\nplt.plot(x, x*0.8, color='#1D3557', linewidth=2, label='Серия B')\nplt.legend()\nplt.title('Hex-цвета')\nplt.show()",
               [{"check": "True", "msg": "Hex-цвета применены"}],
               ["#RRGGBB — формат hex", "Хорошая контрастная пара"], 2),
            ex(4, "python", "Полупрозрачные scatter двух групп с легендой.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\nplt.scatter(np.random.normal(0, 1, 100), np.random.normal(0, 1, 100), alpha=0.5, color='red', label='Группа A', s=50)\nplt.scatter(np.random.normal(2, 1, 100), np.random.normal(2, 1, 100), alpha=0.5, color='blue', label='Группа B', s=50)\nplt.legend()\nplt.title('Две группы с прозрачностью')\nplt.show()",
               [{"check": "True", "msg": "Легенда для scatter работает"}],
               ["alpha=0.5 — полупрозрачно", "Разные цвета для групп"], 2),
            ex(5, "python", "Стиль 'ggplot': plt.style.use('ggplot').",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nplt.style.use('ggplot')\nx = np.linspace(0, 5, 50)\nplt.plot(x, x, label='A')\nplt.plot(x, x*0.7, label='B')\nplt.legend()\nplt.title('Стиль ggplot')\nplt.show()",
               [{"check": "True", "msg": "Стиль ggplot применён"}],
               ["ggplot — серый фон, белая сетка", "plt.style.use меняет всё"], 2),
            ex(6, "python", "figsize=(12, 7), tight_layout(), subplot с большим количеством места.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nfig, axes = plt.subplots(1, 2, figsize=(12, 7))\naxes[0].plot(np.linspace(0, 5, 30), np.sin(np.linspace(0, 5, 30)), 'o-')\naxes[0].set_title('A')\naxes[1].bar(['A','B','C'], [10, 20, 15], color='coral')\naxes[1].set_title('B')\nplt.tight_layout()\nplt.show()",
               [{"check": "True", "msg": "tight_layout работает"}],
               ["figsize=(12, 7) — большой холст", "tight_layout() — авто-отступы"], 2),
            ex(7, "python", "Цветные столбцы: прибыль зелёный, убыль красный.",
               "import matplotlib.pyplot as plt\n",
               "import matplotlib.pyplot as plt\nmonths = ['Янв', 'Фев', 'Мар', 'Апр', 'Май']\nprofit = [120, -50, 200, -30, 180]\ncolors = ['green' if p > 0 else 'red' for p in profit]\nplt.bar(months, profit, color=colors)\nplt.axhline(y=0, color='black', linewidth=0.5)\nplt.title('Прибыль/убыток по месяцам')\nplt.ylabel('Прибыль, тыс. $')\nplt.show()",
               [{"check": "True", "msg": "Цвета по знаку построены"}],
               ["Цвет = состояние (прибыль/убыль)", "axhline(0) — линия нуля"], 2),
            ex(8, "python", "Сохранение графика в PNG через io.BytesIO (как делает наша песочница).",
               "import matplotlib.pyplot as plt\nimport numpy as np\nimport io, base64\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nimport io, base64\nx = np.linspace(0, 5, 50)\nplt.plot(x, np.sin(x))\nplt.title('Сохранение в PNG')\nbuf = io.BytesIO()\nplt.savefig(buf, format='png', dpi=100, bbox_inches='tight')\ndata = base64.b64encode(buf.getvalue()).decode()\nplt.show()",
               [{"check": "True", "msg": "График сохранён в base64"}],
               ["savefig в BytesIO", "dpi=100 — качество"], 3),
            ex(9, "python", "График с двумя Y-осями (twinx) и легендами.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nt = np.arange(0, 10, 0.1)\nfig, ax1 = plt.subplots()\nax1.plot(t, np.sin(t), 'b-', label='Сигнал')\nax1.set_xlabel('Время, с')\nax1.set_ylabel('Сигнал, В', color='blue')\nax1.tick_params(axis='y', labelcolor='blue')\nax2 = ax1.twinx()\nax2.plot(t, np.cos(t), 'r-', label='Производная')\nax2.set_ylabel('Производная', color='red')\nax2.tick_params(axis='y', labelcolor='red')\nplt.title('Сигнал и его производная')\nplt.show()",
               [{"check": "True", "msg": "Двойные оси построены"}],
               ["twinx() — вторая ось Y", "Цвет меток совпадает с цветом графика"], 3),
            ex(10, "python", "Полный 'production-ready' график: title, labels, legend, grid, tight_layout, dpi.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\nfig, ax = plt.subplots(figsize=(10, 6), dpi=100)\nx = np.linspace(0, 10, 100)\nax.plot(x, np.sin(x), label='sin(x)', linewidth=2, color='royalblue')\nax.plot(x, np.cos(x), label='cos(x)', linewidth=2, color='orangered', linestyle='--')\nax.fill_between(x, np.sin(x) - 0.2, np.sin(x) + 0.2, alpha=0.2, color='royalblue')\nax.set_title('Тригонометрические функции (n=100 точек)', fontsize=14, fontweight='bold')\nax.set_xlabel('Угол, радианы', fontsize=12)\nax.set_ylabel('Значение', fontsize=12)\nax.legend(loc='best', fontsize=11, framealpha=0.9)\nax.grid(True, alpha=0.3, linestyle='--')\nax.set_xlim(0, 2*np.pi)\nplt.tight_layout()\nplt.show()",
               [{"check": "True", "msg": "Production-ready график построен"}],
               ["dpi=100 — quality", "tight_layout() — авто-отступы", "framealpha — прозрачность легенды"], 3),
        ],
        minutes=45, difficulty=2,
    )


def _4_9():
    return lesson(
        "4.9", "Сторителлинг с данными", "space", [
            theory(
                "**Сторителлинг с данными** — это умение превратить сухие цифры "
                "в историю, которая убеждает. Три принципа:\n\n"
                "**1. Знай свою аудиторию:**\n"
                "- **Технический эксперт**: плотный график, детали, оси, единицы\n"
                "- **Менеджер**: один punchline-график с аннотацией\n"
                "- **Широкая публика**: простая визуализация, яркая история\n\n"
                "**2. Структура: setup → conflict → resolution:**\n"
                "- **Setup** (контекст): 'Мы запустили 10 спутников за 2 года'\n"
                "- **Conflict** (проблема): 'Но 3 вышли из строя на орбите'\n"
                "- **Resolution** (вывод): 'После редизайна 0% отказов за 12 месяцев'\n\n"
                "**3. Приёмы визуального сторителлинга:**\n"
                "- **Highlight** — выдели ключевую точку цветом/аннотацией\n"
                "- **Annotation** — добавь текст прямо на график\n"
                "- **Color**: один яркий цвет среди серых — фокус внимания\n"
                "- **Subplot story**: 4 графика в ряд — как страницы комикса\n"
                "- **Title as headline**: 'Температура' слабо, "
                "'Температура двигателя выросла на 40% за 60 секунд' сильно\n\n"
                "**Анти-паттерны:**\n"
                "- 3D-эффекты, искажающие пропорции\n"
                "- Rainbow color maps (jet) — не информативны\n"
                "- Шумные данные без выделения главного\n"
                "- Заголовки-клише без чисел\n\n"
                "**Реальные примеры:**\n"
                "- Hans Rosling (Gapminder): анимация пузырьков\n"
                "- New York Times COVID dashboard: понятные heatmap\n"
                "- NASA mission dashboards: телеметрия в реальном времени"
            ),
            analogy(
                "Сторителлинг с данными — документальный фильм: факты (данные) + нарратив (что мы хотим сказать) + визуал (кадры).",
                "Презентация для инвесторов: 'Наш спутник проработал 24 месяца, рынок растёт 20% в год, мы захватываем 5% — это $50M выручки к 2027'."
            ),
            visual(
                "Сторителлинг-структура",
                "  SETUP                 CONFLICT             RESOLUTION\n"
                "  +---------------+    +---------------+   +---------------+\n"
                "  |  До редизайна |    |  Проблема     |   |  После        |\n"
                "  |  (серые)      | -> |  (красный)    | ->|  (зелёный)    |\n"
                "  |               |    |  всплеск      |   |  стабильно    |\n"
                "  +---------------+    +---------------+   +---------------+\n"
                "  Заголовок: 'Как мы снизили отказы с 30% до 2% за 6 месяцев'"
            ),
            example(
                "Построй 4 графика, рассказывающих историю космической миссии: (1) запуск, (2) выход на орбиту, (3) проблема, (4) восстановление.",
                "Каждый subplot — сцена истории. Цветом и аннотациями выделяем ключевые моменты.",
                "import matplotlib.pyplot as plt\n"
                "import numpy as np\n"
                "np.random.seed(42)\n"
                "fig, axes = plt.subplots(2, 2, figsize=(14, 10))\n"
                "fig.suptitle('Хроника миссии Mars-X1: путь к успеху', fontsize=16, fontweight='bold')\n"
                "t1 = np.linspace(0, 60, 100)\n"
                "axes[0, 0].plot(t1, 2000 + 50*t1, 'b-', linewidth=2)\n"
                "axes[0, 0].set_title('1. Запуск: T растёт линейно')\n"
                "axes[0, 0].set_xlabel('Время, с')\n"
                "axes[0, 0].set_ylabel('Температура, °C')\n"
                "axes[0, 0].grid(True, alpha=0.3)\n"
                "t2 = np.linspace(60, 600, 100)\n"
                "axes[0, 1].plot(t2, 5000 - 5*t2, 'g-', linewidth=2)\n"
                "axes[0, 1].set_title('2. Стабилизация на орбите')\n"
                "axes[0, 1].set_xlabel('Время, с')\n"
                "axes[0, 1].set_ylabel('Температура, °C')\n"
                "axes[0, 1].grid(True, alpha=0.3)\n"
                "t3 = np.linspace(600, 1200, 100)\n"
                "temp3 = 2000 + 30*np.sin(t3/20) + np.random.normal(0, 20, 100)\n"
                "temp3[60:80] += 800\n"
                "axes[1, 0].plot(t3, temp3, 'r-', linewidth=1)\n"
                "axes[1, 0].axvspan(800, 900, alpha=0.3, color='red', label='Аномалия')\n"
                "axes[1, 0].set_title('3. Проблема: аномальный нагрев')\n"
                "axes[1, 0].set_xlabel('Время, с')\n"
                "axes[1, 0].set_ylabel('Температура, °C')\n"
                "axes[1, 0].legend()\n"
                "axes[1, 0].grid(True, alpha=0.3)\n"
                "t4 = np.linspace(1200, 1800, 100)\n"
                "temp4 = 2000 + 30*np.sin(t4/20) + np.random.normal(0, 20, 100)\n"
                "axes[1, 1].plot(t4, temp4, 'g-', linewidth=2)\n"
                "axes[1, 1].set_title('4. Восстановление: стабильная работа')\n"
                "axes[1, 1].set_xlabel('Время, с')\n"
                "axes[1, 1].set_ylabel('Температура, °C')\n"
                "axes[1, 1].grid(True, alpha=0.3)\n"
                "plt.tight_layout()\n"
                "plt.show()",
                "[2x2 сетка с 4 сценами: синий (старт), зелёный (орбита), красный (проблема с выделением), зелёный (норма)]",
                "fig.suptitle() — общий заголовок для всех subplot. axvspan() рисует цветной прямоугольник, выделяющий аномалию."
            ),
            common_mistakes([
                {"mistake": "Заголовок 'График 1' / 'Зависимость X от Y'", "why_bad": "Никакой истории, никакого вывода", "fix": "Заголовок-утверждение: 'X вырос втрое после обновления'"},
                {"mistake": "10 графиков на одном слайде", "why_bad": "Сбивает с толку, ни один не запоминается", "fix": "1 punchline-график или 4-6 в логическом порядке"},
                {"mistake": "Нет выделения главного", "why_bad": "Зритель не понимает, куда смотреть", "fix": "Цвет + аннотация на ключевой точке"},
                {"mistake": "Прячу вывод в подпись оси", "why_bad": "Никто не читает оси", "fix": "Вывод в заголовке или жирной аннотации"},
                {"mistake": "Использую rainbow colormap", "why_bad": "Не информативно, отвлекает", "fix": "Sequential (viridis) или diverging (coolwarm)"},
            ]),
            interview_questions([
                {"q": "Что такое punchline-график?",
                 "a": "Один график с одним главным выводом. Заголовок-утверждение, выделенная ключевая точка, минимум деталей. Для менеджера/инвестора, не для технаря."},
                {"q": "Как сделать визуальный фокус?",
                 "a": "1) Цвет: 1 яркий среди серых. 2) Размер: ключевой элемент крупнее. 3) Аннотация: стрелка + текст. 4) Изоляция: остальное в lightgray, главное в full color."},
                {"q": "Чем сторителлинг отличается от просто графика?",
                 "a": "График показывает данные. Сторителлинг ведёт к выводу: данные + контекст + интерпретация + призыв к действию."},
            ]),
            knowledge_checklist([
                "Знаю 3 принципа: аудитория, структура, фокус",
                "Использую заголовок-утверждение",
                "Выделяю ключевую точку цветом",
                "Добавляю аннотации к важным данным",
                "Использую axvspan/axhspan для зон внимания",
                "Использую fig.suptitle для общей истории",
                "Строю серию subplot как 'главы' истории",
            ]),
        ],
        exercises=[
            ex(1, "python", "Заголовок-утверждение: 'Falcon 9 обогнал конкурентов по числу запусков в 2023'.",
               "import matplotlib.pyplot as plt\n",
               "import matplotlib.pyplot as plt\nrockets = ['Falcon 9', 'Atlas V', 'Ariane 5', 'Soyuz']\nlaunches_2023 = [98, 6, 3, 18]\ncolors = ['#1f77b4' if r == 'Falcon 9' else '#cccccc' for r in rockets]\nplt.bar(rockets, launches_2023, color=colors)\nplt.title('Falcon 9 опередил конкурентов в 7-15 раз по запускам (2023)', fontsize=13, fontweight='bold')\nplt.ylabel('Число запусков')\nplt.show()",
               [{"check": "True", "msg": "Заголовок-утверждение применён"}],
               ["Заголовок содержит число и контекст", "Один яркий цвет среди серых"], 1),
            ex(2, "python", "Выдели ключевую точку: scatter с подсветкой максимума красным.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\nx = np.arange(20)\ny = np.cumsum(np.random.randn(20))\nplt.plot(x, y, color='gray', linewidth=1, label='Динамика')\nmax_idx = np.argmax(y)\nplt.scatter(x[max_idx], y[max_idx], s=200, color='red', zorder=5, label=f'Пик: {y[max_idx]:.1f}')\nplt.annotate(f'Максимум: {y[max_idx]:.1f}', (x[max_idx], y[max_idx]), xytext=(5, 10), textcoords='offset points', color='red')\nplt.legend()\nplt.title('Где был пик?')\nplt.show()",
               [{"check": "True", "msg": "Ключевая точка выделена"}],
               ["zorder=5 — поверх линии", "annotate с offset points"], 2),
            ex(3, "python", "axvspan: подсветка зоны аномалии (например, t=60..80).",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\nt = np.arange(100)\nv = np.random.normal(0, 1, 100).cumsum()\nv[60:80] += 10\nplt.plot(t, v, color='steelblue')\nplt.axvspan(60, 80, alpha=0.3, color='red', label='Аномалия')\nplt.legend()\nplt.title('Всплеск в зоне 60-80')\nplt.xlabel('Время')\nplt.show()",
               [{"check": "True", "msg": "Зона выделена"}],
               ["axvspan рисует прямоугольник по X", "alpha=0.3 — полупрозрачно"], 2),
            ex(4, "python", "axhline с аннотацией: целевое значение и его описание.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\nt = np.arange(50)\nperf = 80 + 5*np.sin(t/5) + np.random.normal(0, 1, 50)\nplt.plot(t, perf, label='Производительность')\nplt.axhline(y=85, color='red', linestyle='--', label='Цель: 85%')\nplt.annotate('Цель 85%', xy=(0, 85), xytext=(20, 90), arrowprops=dict(arrowstyle='->', color='red'))\nplt.legend()\nplt.title('Мы приближаемся к цели')\nplt.show()",
               [{"check": "True", "msg": "Цель обозначена"}],
               ["axhline — горизонтальная линия", "annotate с arrowprops"], 2),
            ex(5, "python", "fig.suptitle: общий заголовок для 2 subplot.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nfig, axes = plt.subplots(1, 2, figsize=(12, 4))\nfig.suptitle('До и после: внедрение новой теплозащиты', fontsize=14, fontweight='bold')\naxes[0].plot(np.arange(30), 2000 + 30*np.arange(30) + np.random.normal(0, 50, 30), color='red')\naxes[0].set_title('До: T растёт')\naxes[1].plot(np.arange(30), 1500 + 5*np.arange(30) + np.random.normal(0, 20, 30), color='green')\naxes[1].set_title('После: T стабильна')\nplt.tight_layout()\nplt.show()",
               [{"check": "True", "msg": "Общий заголовок добавлен"}],
               ["suptitle для общей истории", "2 subplot = 2 главы"], 2),
            ex(6, "python", "Story-flow: 3 subplot в ряд с цветовой прогрессией серый→жёлтый→зелёный.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nfig, axes = plt.subplots(1, 3, figsize=(15, 4))\nfig.suptitle('Уровень риска миссии: снизился с высокого до низкого', fontsize=13, fontweight='bold')\ncolors = ['#e74c3c', '#f1c40f', '#27ae60']\ntitles = ['Старт: высокий риск', 'Середина: средний', 'Финиш: низкий']\nfor ax, c, t in zip(axes, colors, titles):\n    x = np.arange(20)\n    y = 50 + 10*np.sin(x/3) + np.random.normal(0, 2, 20)\n    ax.plot(x, y, color=c, linewidth=2)\n    ax.set_title(t)\n    ax.set_ylim(30, 70)\n    ax.grid(True, alpha=0.3)\nplt.tight_layout()\nplt.show()",
               [{"check": "True", "msg": "Story-flow построен"}],
               ["Цвет = эмоция: красный=опасно, зелёный=хорошо", "3 subplot = setup/conflict/resolution"], 2),
            ex(7, "python", "Highlight через fill_between: подсветка зоны перевыполнения плана.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nt = np.arange(12)\nplan = np.full(12, 100)\nactual = np.array([80, 95, 110, 105, 115, 120, 125, 130, 128, 132, 135, 140])\nplt.plot(t, plan, 'k--', label='План')\nplt.plot(t, actual, 'b-', linewidth=2, label='Факт')\nplt.fill_between(t, plan, actual, where=(actual > plan), color='green', alpha=0.3, label='Перевыполнение')\nplt.fill_between(t, plan, actual, where=(actual < plan), color='red', alpha=0.3, label='Недовыполнение')\nplt.legend()\nplt.title('Мы перевыполнили план с 3-го месяца')\nplt.xlabel('Месяц')\nplt.ylabel('Продажи, %')\nplt.show()",
               [{"check": "True", "msg": "Зоны подсвечены"}],
               ["fill_between с where — условная заливка", "Зелёный/красный = хорошо/плохо"], 3),
            ex(8, "python", "Big title с подзаголовком через fig.text.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nfig, ax = plt.subplots(figsize=(10, 5))\nfig.suptitle('Заголовок-история', fontsize=16, fontweight='bold')\nfig.text(0.5, 0.92, 'Подзаголовок с деталями и контекстом', ha='center', fontsize=11, style='italic', color='gray')\nax.plot(np.arange(20), np.random.randn(20).cumsum())\nax.grid(True, alpha=0.3)\nplt.show()",
               [{"check": "True", "msg": "Big title + subtitle работают"}],
               ["suptitle — крупный", "fig.text — подзаголовок вручную"], 2),
            ex(9, "python", "Сравнение A/B: bar с двумя столбцами, выигрышный отмечен зелёной звездой.",
               "import matplotlib.pyplot as plt\n",
               "import matplotlib.pyplot as plt\nlabels = ['A', 'B']\nconv = [0.30, 0.35]\ncolors = ['gray', 'green']\nbars = plt.bar(labels, conv, color=colors)\nplt.ylabel('Конверсия')\nplt.title('B выигрывает: +5пп к конверсии')\nfor bar, v in zip(bars, conv):\n    plt.text(bar.get_x() + bar.get_width()/2, v + 0.005, f'{v*100:.0f}%', ha='center', fontsize=12, fontweight='bold')\nplt.text(1, 0.36, '*', ha='center', fontsize=30, color='green')\nplt.ylim(0, 0.4)\nplt.show()",
               [{"check": "True", "msg": "A/B с выделением победителя"}],
               ["Зелёный = выигрыш", "Звезда — выделение"], 2),
            ex(10, "python", "Итоговая панель: 4 subplot = 4 главы истории (setup, conflict, action, result).",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\nfig, axes = plt.subplots(2, 2, figsize=(14, 10))\nfig.suptitle('История оптимизации: от хаоса к порядку', fontsize=15, fontweight='bold')\ntitles = ['1. Setup: исходные данные', '2. Conflict: всплеск ошибок', '3. Action: внедрение ML', '4. Result: стабильность']\ndata = [\n    np.random.normal(50, 5, 30),\n    np.concatenate([np.random.normal(50, 5, 20), np.random.normal(70, 5, 10)]),\n    np.random.normal(50, 3, 30),\n    np.random.normal(50, 1, 30)\n]\ncolors = ['steelblue', 'red', 'orange', 'green']\nfor ax, t, d, c in zip(axes.flatten(), titles, data, colors):\n    ax.plot(d, color=c, marker='o', markersize=4)\n    ax.set_title(t)\n    ax.grid(True, alpha=0.3)\n    ax.set_ylim(30, 90)\nplt.tight_layout()\nplt.show()",
               [{"check": "True", "msg": "4 главы истории построены"}],
               ["2x2 = 4 главы", "suptitle объединяет в одну историю"], 3),
        ],
        minutes=55, difficulty=3,
    )


def _4_10():
    return lesson(
        "4.10", "Мини-проект: Дашборд космической миссии", "space", [
            theory(
                "**Финальный мини-проект** — собрать дашборд для космической миссии "
                "'Mars Expedition 2026'. Дашборд — это композиция из 4-6 графиков на одной Figure.\n\n"
                "**Сценарий миссии:**\n"
                "- Запуск ракеты-носителя с космодрома\n"
                "- Полёт к Марсу (180 дней)\n"
                "- Работа на поверхности 60 дней\n"
                "- Возвращение\n\n"
                "**Что в дашборде:**\n"
                "1. **Телеметрия**: температура двигателя, давление, вибрация по времени\n"
                "2. **Расход топлива**: pie или stacked area\n"
                "3. **Связь параметров**: scatter (высота vs скорость)\n"
                "4. **Сравнение этапов**: bar с метриками каждого этапа\n"
                "5. **Heatmap**: корреляция параметров корабля\n"
                "6. **Итог миссии**: текстовый блок с метриками успеха\n\n"
                "**Архитектура дашборда:**\n"
                "```python\n"
                "fig = plt.figure(figsize=(16, 10))\n"
                "gs = gridspec.GridSpec(3, 3)  # 3x3 сетка\n"
                "ax1 = fig.add_subplot(gs[0, :2])   # телеметрия — широкий\n"
                "ax2 = fig.add_subplot(gs[0, 2])    # расход топлива\n"
                "ax3 = fig.add_subplot(gs[1, :2])   # scatter\n"
                "ax4 = fig.add_subplot(gs[1, 2])    # heatmap\n"
                "ax5 = fig.add_subplot(gs[2, :])    # bar по этапам\n"
                "fig.suptitle('DASHBOARD', fontsize=18)\n"
                "```\n\n"
                "**Правила хорошего дашборда:**\n"
                "- Один общий заголовок\n"
                "- Логическая композиция (глаза идут слева направо, сверху вниз)\n"
                "- Контрастные цвета для разных подсистем\n"
                "- Минимум декора, максимум данных\n"
                "- Сетка не везде — только где нужно считывать значения"
            ),
            analogy(
                "Дашборд — приборная панель самолёта: 6 круглых циферблатов, каждый показывает своё, пилот мгновенно читает.",
                "NASA mission control: 4 экрана, на каждом — свой график. Один большой — главная телеметрия, остальные — детали."
            ),
            visual(
                "Структура дашборда Mars Expedition 2026",
                "  +------------------ MARS EXPEDITION 2026 ------------------+\n"
                "  | +-------------------------------+ +------------------+ |\n"
                "  | | 1. Телеметрия: T, P, V        | | 2. Расход топлива | |\n"
                "  | |    (линейный график)          | |    (pie)          | |\n"
                "  | +-------------------------------+ +------------------+ |\n"
                "  | +-------------------------------+ +------------------+ |\n"
                "  | | 3. Высота vs Скорость         | | 4. Heatmap        | |\n"
                "  | |    (scatter)                  | |    корреляций     | |\n"
                "  | +-------------------------------+ +------------------+ |\n"
                "  | +------------------------------------------------------+ |\n"
                "  | | 5. Сравнение этапов миссии (bar)                     | |\n"
                "  | +------------------------------------------------------+ |\n"
                "  +----------------------------------------------------------+"
            ),
            example(
                "Минимальный дашборд: 2x2 subplot с телеметрией, pie, scatter и bar.",
                "gridspec даёт гибкую раскладку. fig.suptitle — общий заголовок. tight_layout предотвращает наложение.",
                "import matplotlib.pyplot as plt\n"
                "import numpy as np\n"
                "import matplotlib.gridspec as gridspec\n"
                "np.random.seed(42)\n"
                "fig = plt.figure(figsize=(14, 10))\n"
                "fig.suptitle('MARS EXPEDITION 2026 — Mission Dashboard', fontsize=16, fontweight='bold')\n"
                "gs = gridspec.GridSpec(2, 2, hspace=0.3, wspace=0.3)\n"
                "ax1 = fig.add_subplot(gs[0, 0])\n"
                "t = np.linspace(0, 100, 200)\n"
                "ax1.plot(t, 1500 + 200*np.sin(t/10) + np.random.normal(0, 30, 200), color='orangered', label='T')\n"
                "ax1.set_title('Температура двигателя')\n"
                "ax1.set_xlabel('Время, с')\n"
                "ax1.set_ylabel('T, °C')\n"
                "ax1.grid(True, alpha=0.3)\n"
                "ax1.legend()\n"
                "ax2 = fig.add_subplot(gs[0, 1])\n"
                "ax2.pie([55, 25, 15, 5], labels=['Взлёт', 'Перелёт', 'Посадка', 'Возврат'], autopct='%1.0f%%', startangle=90)\n"
                "ax2.set_title('Расход топлива по этапам')\n"
                "ax3 = fig.add_subplot(gs[1, 0])\n"
                "alt = np.linspace(0, 400000, 100)\n"
                "speed = np.sqrt(2 * 9.8 * alt) + np.random.normal(0, 50, 100)\n"
                "ax3.scatter(alt, speed, alpha=0.6, s=20, color='steelblue')\n"
                "ax3.set_title('Высота vs Скорость')\n"
                "ax3.set_xlabel('Высота, м')\n"
                "ax3.set_ylabel('Скорость, м/с')\n"
                "ax3.grid(True, alpha=0.3)\n"
                "ax4 = fig.add_subplot(gs[1, 1])\n"
                "stages = ['Взлёт', 'Перелёт', 'Посадка', 'Возврат']\n"
                "success = [98, 95, 87, 92]\n"
                "ax4.bar(stages, success, color=['green','steelblue','coral','gold'])\n"
                "ax4.set_title('Успешность этапов, %')\n"
                "ax4.set_ylabel('%')\n"
                "ax4.set_ylim(80, 100)\n"
                "plt.show()",
                "[2x2 дашборд: телеметрия (красная линия), pie топлива, scatter высоты/скорости, bar успешности]",
                "gridspec.GridSpec(2, 2) делит Figure на 2x2. hspace/wspace — отступы между subplot. add_subplot(gs[i,j]) помещает Axes в нужную ячейку."
            ),
            common_mistakes([
                {"mistake": "Все subplot одинакового размера", "why_bad": "Главный график теряется среди деталей", "fix": "Главный — на 2 ячейки, остальные — на 1"},
                {"mistake": "Разные стили на разных subplot", "why_bad": "Выглядит как слайд-шоу из 1990-х", "fix": "Один plt.style.use() для всего дашборда"},
                {"mistake": "Нет общего заголовка", "why_bad": "Непонятно, что за дашборд", "fix": "fig.suptitle() с названием миссии"},
                {"mistake": "Цветовая каша", "why_bad": "5 случайных цветов — нет смысла", "fix": "Одна палитра (например, colorbrewer Set2) для всех графиков"},
                {"mistake": "Мелкие подписи (8pt)", "why_bad": "На проекторе не видно", "fix": "10-12pt для осей, 14-16 для заголовков"},
            ]),
            interview_questions([
                {"q": "Что отличает хороший дашборд от плохого?",
                 "a": "Хороший: 1) читается за 5 секунд, 2) ответ на главный вопрос в верхнем левом, 3) минимум 'шумных' деталей, 4) логическая группировка, 5) единый стиль."},
                {"q": "Сколько графиков должно быть на дашборде?",
                 "a": "4-6. Меньше — недорассказано. Больше — каша. Исключение: BI-инструменты (Tableau) с фильтрами, там 10+."},
                {"q": "Как расставлять приоритеты в композиции?",
                 "a": "Z-паттерн: верх-лево (главный) → верх-право → низ-лево → низ-право. Или F-паттерн для текстовых отчётов."},
            ]),
            knowledge_checklist([
                "Использую plt.subplots или gridspec для раскладки",
                "Размещаю главный график в верхнем левом углу",
                "Добавляю fig.suptitle с названием дашборда",
                "Использую единый стиль для всех subplot",
                "Применяю tight_layout() или hspace/wspace",
                "Использую ограниченную палитру",
                "Подписи читаемы (>=10pt)",
            ]),
        ],
        exercises=[
            ex(1, "python", "Этап 1: Построй график телеметрии температуры двигателя за 200 секунд.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\nt = np.linspace(0, 200, 200)\nT = 1500 + 300*np.sin(t/15) + 50*np.sin(t/3) + np.random.normal(0, 25, 200)\nplt.figure(figsize=(10, 4))\nplt.plot(t, T, color='orangered', linewidth=1)\nplt.title('Телеметрия: температура двигателя (200 с)')\nplt.xlabel('Время, с')\nplt.ylabel('T, °C')\nplt.grid(True, alpha=0.3)\nplt.show()",
               [{"check": "True", "msg": "Телеметрия построена"}],
               ["200 точек — плотный график", "2 синусоиды + шум"], 1),
            ex(2, "python", "Этап 2: Построй pie распределения топлива по этапам миссии.",
               "import matplotlib.pyplot as plt\n",
               "import matplotlib.pyplot as plt\nstages = ['Взлёт', 'Перелёт', 'Посадка', 'Возврат']\nfuel = [55, 25, 15, 5]\ncolors = ['#e74c3c', '#3498db', '#2ecc71', '#f1c40f']\nplt.pie(fuel, labels=stages, colors=colors, autopct='%1.0f%%', startangle=90)\nplt.title('Расход топлива по этапам миссии')\nplt.show()",
               [{"check": "True", "msg": "Pie расхода построен"}],
               ["4 сегмента — оптимально для pie", "Цветом кодируем этап"], 1),
            ex(3, "python", "Этап 3: Scatter высота vs скорость с линией идеальной зависимости.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\nalt = np.linspace(0, 400000, 100)\nspeed_actual = np.sqrt(2 * 9.8 * alt) + np.random.normal(0, 80, 100)\nspeed_ideal = np.sqrt(2 * 9.8 * alt)\nplt.figure(figsize=(8, 6))\nplt.scatter(alt, speed_actual, alpha=0.5, s=20, color='steelblue', label='Факт')\nplt.plot(alt, speed_ideal, 'r-', linewidth=2, label='Идеал (v=sqrt(2gh))')\nplt.title('Высота vs Скорость')\nplt.xlabel('Высота, м')\nplt.ylabel('Скорость, м/с')\nplt.legend()\nplt.grid(True, alpha=0.3)\nplt.show()",
               [{"check": "True", "msg": "Scatter с теорией построен"}],
               ["sqrt(2*g*h) — формула скорости от высоты", "Красная линия = теория"], 2),
            ex(4, "python", "Этап 4: Heatmap корреляции 5 параметров корабля.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\nn = 200\nT = np.random.normal(1500, 100, n)\nP = 0.7*T + np.random.normal(0, 30, n)\nV = 0.3*T + np.random.normal(0, 20, n)\nF = -0.5*P + np.random.normal(0, 50, n)\nA = np.random.normal(100, 10, n)\ndata = np.vstack([T, P, V, F, A])\ncorr = np.corrcoef(data)\nlabels = ['T', 'P', 'V', 'F', 'A']\nfig, ax = plt.subplots(figsize=(7, 6))\nim = ax.imshow(corr, cmap='coolwarm', vmin=-1, vmax=1)\nax.set_xticks(range(5)); ax.set_yticks(range(5))\nax.set_xticklabels(labels); ax.set_yticklabels(labels)\nfor i in range(5):\n    for j in range(5):\n        ax.text(j, i, f'{corr[i,j]:.2f}', ha='center', va='center')\nplt.colorbar(im, label='r')\nplt.title('Корреляция параметров корабля')\nplt.show()",
               [{"check": "True", "msg": "Heatmap корреляции построена"}],
               ["vmin/vmax=±1 для шкалы", "T и P сильно связаны"], 2),
            ex(5, "python", "Этап 5: Bar с успешностью каждого этапа (4 столбца).",
               "import matplotlib.pyplot as plt\n",
               "import matplotlib.pyplot as plt\nstages = ['Взлёт', 'Перелёт', 'Посадка', 'Возврат']\nsuccess = [98, 95, 87, 92]\ncolors = ['green' if s > 90 else 'orange' for s in success]\nplt.bar(stages, success, color=colors, edgecolor='black')\nplt.axhline(y=90, color='red', linestyle='--', label='Цель: 90%')\nplt.title('Успешность этапов миссии')\nplt.ylabel('Успешность, %')\nplt.ylim(80, 100)\nplt.legend()\nfor i, v in enumerate(success):\n    plt.text(i, v + 0.5, f'{v}%', ha='center', fontweight='bold')\nplt.show()",
               [{"check": "True", "msg": "Bar успешности построен"}],
               ["axhline(90) — линия цели", "Цвет по порогу"], 2),
            ex(6, "python", "Этап 6: Box plot 4 этапов по 100 замеров температуры каждый.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\ndata = [np.random.normal(1500, 100, 100), np.random.normal(1200, 50, 100), np.random.normal(1800, 150, 100), np.random.normal(1400, 80, 100)]\nlabels = ['Взлёт', 'Перелёт', 'Посадка', 'Возврат']\nplt.boxplot(data, tick_labels=labels, patch_artist=True)\nplt.title('Температура по этапам миссии')\nplt.ylabel('T, °C')\nplt.grid(True, alpha=0.3)\nplt.show()",
               [{"check": "True", "msg": "Box plot этапов построен"}],
               ["4 группы = 4 этапа", "patch_artist для заливки"], 2),
            ex(7, "python", "Этап 7: Собери 2x2 subplot (телеметрия, pie, scatter, bar).",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\nfig, axes = plt.subplots(2, 2, figsize=(12, 10))\nfig.suptitle('MARS EXPEDITION 2026', fontsize=14, fontweight='bold')\nt = np.linspace(0, 100, 200)\naxes[0, 0].plot(t, 1500 + 200*np.sin(t/10) + np.random.normal(0, 30, 200), color='orangered')\naxes[0, 0].set_title('Телеметрия')\naxes[0, 0].grid(True, alpha=0.3)\naxes[0, 1].pie([55, 25, 15, 5], labels=['A','B','C','D'], autopct='%1.0f%%', startangle=90)\naxes[0, 1].set_title('Топливо')\nalt = np.linspace(0, 400000, 100)\naxes[1, 0].scatter(alt, np.sqrt(2*9.8*alt) + np.random.normal(0, 50, 100), alpha=0.5, s=15)\naxes[1, 0].set_title('Связь параметров')\naxes[1, 0].grid(True, alpha=0.3)\naxes[1, 1].bar(['A','B','C','D'], [98, 95, 87, 92], color=['green','steelblue','coral','gold'])\naxes[1, 1].set_title('Успешность, %')\nplt.tight_layout()\nplt.show()",
               [{"check": "True", "msg": "2x2 дашборд собран"}],
               ["suptitle общий заголовок", "tight_layout() выравнивает"], 2),
            ex(8, "python", "Этап 8: Стилизация: добавь стиль 'seaborn-v0_8-whitegrid'.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nplt.style.use('seaborn-v0_8-whitegrid')\nnp.random.seed(42)\nfig, axes = plt.subplots(2, 2, figsize=(12, 10))\nfig.suptitle('MARS 2026 (стиль seaborn)', fontsize=14, fontweight='bold')\nt = np.linspace(0, 100, 200)\naxes[0, 0].plot(t, 1500 + 200*np.sin(t/10) + np.random.normal(0, 30, 200), color='orangered')\naxes[0, 0].set_title('Телеметрия')\naxes[0, 1].pie([55, 25, 15, 5], labels=['A','B','C','D'], autopct='%1.0f%%', startangle=90)\naxes[0, 1].set_title('Топливо')\nalt = np.linspace(0, 400000, 100)\naxes[1, 0].scatter(alt, np.sqrt(2*9.8*alt) + np.random.normal(0, 50, 100), alpha=0.5, s=15, color='steelblue')\naxes[1, 0].set_title('Связь параметров')\naxes[1, 1].bar(['A','B','C','D'], [98, 95, 87, 92])\naxes[1, 1].set_title('Успешность, %')\nplt.tight_layout()\nplt.show()",
               [{"check": "True", "msg": "Стиль применён ко всему дашборду"}],
               ["plt.style.use() влияет на все Axes", "Белая сетка — seaborn-style"], 2),
            ex(9, "python", "Этап 9: Добавь выделение: axvspan для зоны аномалии на телеметрии.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\nfig, axes = plt.subplots(1, 2, figsize=(14, 5))\nt = np.linspace(0, 200, 200)\nT = 1500 + 200*np.sin(t/10) + np.random.normal(0, 30, 200)\nT[80:120] += 400\naxes[0].plot(t, T, color='orangered', linewidth=1)\naxes[0].axvspan(80, 120, alpha=0.3, color='red', label='Аномалия')\naxes[0].annotate('Всплеск T', xy=(100, T[100]), xytext=(130, 2200), arrowprops=dict(arrowstyle='->', color='red'))\naxes[0].set_title('Телеметрия с выделением')\naxes[0].legend()\naxes[0].grid(True, alpha=0.3)\naxes[1].bar(['Норма','Аномалия'], [30, 30], color=['green','red'])\naxes[1].set_title('Счётчик замеров')\nplt.tight_layout()\nplt.show()",
               [{"check": "True", "msg": "Аномалия выделена"}],
               ["axvspan(80, 120) — зона", "annotate с стрелкой"], 2),
            ex(10, "python", "Этап 10: Используй gridspec для гибкой раскладки (3x3).",
               "import matplotlib.pyplot as plt\nimport numpy as np\nimport matplotlib.gridspec as gridspec\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nimport matplotlib.gridspec as gridspec\nnp.random.seed(42)\nfig = plt.figure(figsize=(14, 10))\nfig.suptitle('DASHBOARD 3x3', fontsize=16, fontweight='bold')\ngs = gridspec.GridSpec(3, 3, hspace=0.4, wspace=0.3)\nax1 = fig.add_subplot(gs[0, :])\nt = np.linspace(0, 200, 200)\nax1.plot(t, 1500 + 200*np.sin(t/10) + np.random.normal(0, 30, 200), color='orangered')\nax1.set_title('Телеметрия (широкий)')\nax1.grid(True, alpha=0.3)\nax2 = fig.add_subplot(gs[1, 0])\nax2.pie([55, 25, 15, 5], labels=['A','B','C','D'], autopct='%1.0f%%', startangle=90)\nax2.set_title('Топливо')\nax3 = fig.add_subplot(gs[1, 1])\nax3.bar(['A','B','C','D'], [98, 95, 87, 92])\nax3.set_title('Успешность')\nax4 = fig.add_subplot(gs[1, 2])\nnp.random.seed(42)\ndata = [np.random.normal(i, 1, 50) for i in range(4)]\nax4.boxplot(data, tick_labels=['A','B','C','D'])\nax4.set_title('Распределения')\nax5 = fig.add_subplot(gs[2, :])\nax5.scatter(np.random.normal(0, 1, 200), np.random.normal(0, 1, 200), alpha=0.4, s=10)\nax5.set_title('Scatter (широкий)')\nax5.grid(True, alpha=0.3)\nplt.show()",
               [{"check": "True", "msg": "Гибкая раскладка работает"}],
               ["gs[0, :] — занять всю строку", "hspace/wspace — отступы"], 3),
            ex(11, "python", "Этап 11: Добавь итоговый текстовый блок (ax.text) с метриками успеха.",
               "import matplotlib.pyplot as plt\nimport numpy as np\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nfig, ax = plt.subplots(figsize=(8, 5))\nax.axis('off')\nax.text(0.5, 0.9, 'MARS EXPEDITION 2026', ha='center', fontsize=18, fontweight='bold', transform=ax.transAxes)\nax.text(0.5, 0.75, 'Финальный отчёт', ha='center', fontsize=14, color='gray', transform=ax.transAxes)\nmetrics = [\n    'Длительность: 240 дней',\n    'Расстояние: 225 млн км',\n    'Успешность: 93%',\n    'Собрано образцов: 12 кг',\n    'Фото: 5400 шт'\n]\nfor i, m in enumerate(metrics):\n    ax.text(0.1, 0.55 - i*0.08, '* ' + m, fontsize=12, transform=ax.transAxes)\nax.text(0.5, 0.1, 'Миссия выполнена!', ha='center', fontsize=14, color='green', fontweight='bold', transform=ax.transAxes)\nplt.show()",
               [{"check": "True", "msg": "Текстовый блок добавлен"}],
               ["axis('off') — скрыть оси", "transAxes — координаты 0-1"], 2),
            ex(12, "python", "Этап 12: Финальный дашборд: 4 графика + текстовый блок в едином стиле.",
               "import matplotlib.pyplot as plt\nimport numpy as np\nimport matplotlib.gridspec as gridspec\n",
               "import matplotlib.pyplot as plt\nimport numpy as np\nimport matplotlib.gridspec as gridspec\nplt.style.use('seaborn-v0_8-whitegrid')\nnp.random.seed(42)\nfig = plt.figure(figsize=(16, 10))\nfig.suptitle('MARS EXPEDITION 2026 — Mission Dashboard', fontsize=18, fontweight='bold', y=0.98)\ngs = gridspec.GridSpec(3, 3, hspace=0.5, wspace=0.3)\nax1 = fig.add_subplot(gs[0, :2])\nt = np.linspace(0, 200, 200)\nT = 1500 + 200*np.sin(t/10) + np.random.normal(0, 30, 200)\nax1.plot(t, T, color='orangered')\nax1.fill_between(t, T-50, T+50, alpha=0.2, color='orangered')\nax1.set_title('Телеметрия (T двигателя, °C)')\nax1.set_xlabel('Время, с')\nax2 = fig.add_subplot(gs[0, 2])\nax2.pie([55, 25, 15, 5], labels=['Взлёт','Перелёт','Посадка','Возврат'], autopct='%1.0f%%', startangle=90, colors=['#e74c3c','#3498db','#2ecc71','#f1c40f'])\nax2.set_title('Расход топлива')\nax3 = fig.add_subplot(gs[1, :2])\nalt = np.linspace(0, 400000, 100)\nax3.scatter(alt, np.sqrt(2*9.8*alt) + np.random.normal(0, 50, 100), alpha=0.5, s=20, color='steelblue')\nax3.set_title('Высота vs Скорость')\nax3.set_xlabel('Высота, м'); ax3.set_ylabel('Скорость, м/с')\nax4 = fig.add_subplot(gs[1, 2])\nstages = ['Взлёт','Перелёт','Посадка','Возврат']\nsuccess = [98, 95, 87, 92]\ncolors = ['green' if s > 90 else 'orange' for s in success]\nax4.bar(stages, success, color=colors, edgecolor='black')\nax4.set_ylim(80, 100)\nax4.set_title('Успешность, %')\nax4.axhline(y=90, color='red', linestyle='--', alpha=0.5)\nax5 = fig.add_subplot(gs[2, :])\nax5.axis('off')\nax5.text(0.5, 0.7, 'ИТОГИ МИССИИ', ha='center', fontsize=15, fontweight='bold', transform=ax5.transAxes)\nmetrics_text = '  |  '.join([f'Длительность: 240 дней', 'Успешность: 93%', 'Образцы: 12 кг', 'Фото: 5400'])\nax5.text(0.5, 0.3, metrics_text, ha='center', fontsize=12, transform=ax5.transAxes)\nplt.show()",
               [{"check": "True", "msg": "Финальный дашборд собран"}],
               ["GridSpec 3x3 + suptitle", "5 элементов: телеметрия, pie, scatter, bar, итог", "Единый стиль seaborn-v0_8-whitegrid"], 3),
        ],
        minutes=90, difficulty=4,
    )


LESSONS = [_4_1, _4_2, _4_3, _4_4, _4_5, _4_6, _4_7, _4_8, _4_9, _4_10]
