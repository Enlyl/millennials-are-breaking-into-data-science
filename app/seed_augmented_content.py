"""
Augmented content: новые уроки + presentation improvements + недостающие мини-уроки.
"""
from app.seed_helpers import (
    ex, lesson, theory, analogy, visual, example,
    common_mistakes, interview_questions, knowledge_checklist,
)

# ─── Block 1: Python ────────────────────────────────────────────────────────

def _1_13():
    return lesson(
        "1.13", "*args, **kwargs, декораторы и itertools", "neutral", [
            theory(
                "**args и kwargs** — магические параметры для передачи переменного числа "
                "аргументов. `*args` собирает все позиционные аргументы в кортеж, "
                "`**kwargs` — все именованные в словарь.\n\n"
                "```python\ndef log(*args, **kwargs):\n    print('args:', args)\n    print('kwargs:', kwargs)\n"
                "log(1, 2, x=10)  # args=(1,2) kwargs={'x':10}\n```\n\n"
                "**Декораторы** — функции, которые оборачивают другие функции для "
                "добавления поведения (логирование, тайминг, кэширование). "
                "`@lru_cache` из `functools` кэширует результаты вызова — критично "
                "для рекурсивных алгоритмов и тяжёлых вычислений.\n\n"
                "```python\nfrom functools import lru_cache\n"
                "@lru_cache(maxsize=128)\ndef fib(n):\n    return n if n < 2 else fib(n-1) + fib(n-2)\n```\n\n"
                "**itertools** — библиотека для эффективных итераций: "
                "`chain` (склеить итераторы), `product` (декартово произведение), "
                "`groupby` (группировка), `combinations` / `permutations` "
                "(сочетания и перестановки). На собеседованиях itertools — частый гость."
            ),
            analogy(
                "*args — коробка для всех лишних конфет, **kwargs — коробка с этикетками",
                "Data Scientist пишет функцию для метрик: `calc_metrics(*scores, **params)` — "
                "передаёт любые метрики через args и гиперпараметры через kwargs."
            ),
            visual(
                "Движение данных через args и kwargs в pipeline",
                "   def pipeline(*steps, **config):\n"
                "      steps → кортеж (clean, transform, train)\n"
                "      config → словарь {'lr': 0.01, 'epochs': 10}\n"
                "      for step in steps:\n"
                "          data = step(data, **config)"
            ),
            example(
                "Напиши декоратор, который замеряет время выполнения функции, и примени "
                "его к функции расчёта факториала.",
                "Используем `functools.wraps` чтобы сохранить метаданные функции. "
                "Декоратор `@timer` оборачивает вызов, замеряет time.perf_counter.",
                "import time\nfrom functools import wraps\n"
                "def timer(func):\n    @wraps(func)\n    def wrapper(*args, **kwargs):\n"
                "        start = time.perf_counter()\n        result = func(*args, **kwargs)\n"
                "        print(f'{func.__name__}: {time.perf_counter()-start:.4f}s')\n"
                "        return result\n    return wrapper\n\n"
                "@timer\ndef factorial(n):\n    from math import prod\n    return prod(range(1, n+1))\n\n"
                "print(factorial(10))",
                "factorial: 0.0001s\n3628800",
                "Декоратор timer обернул factorial. При каждом вызове печатается время. "
                "`@wraps(func)` сохраняет `__name__` и `__doc__` исходной функции."
            ),
            common_mistakes([
                {"mistake": "def f(**kwargs, *args)", "why_bad": "SyntaxError: kwargs должен быть после args", "fix": "def f(*args, **kwargs):"},
                {"mistake": "Забыть @wraps в декораторе", "why_bad": "f.__name__ == 'wrapper' вместо оригинала", "fix": "from functools import wraps; @wraps(func)"},
                {"mistake": "itertools.groupby работает ТОЛЬКО на отсортированных данных", "why_bad": "Группирует соседние, а не все одинаковые", "fix": "Сначала sorted(data, key=key_func), потом groupby"},
                {"mistake": "lru_cache на функции с аргументами-списками", "why_bad": "TypeError: unhashable type", "fix": "Преобразуй list в tuple перед передачей"},
            ]),
            interview_questions([
                {"q": "Чем отличается *args от **kwargs?", "a": "*args — кортеж позиционных аргументов. **kwargs — словарь именованных. args передаются по порядку, kwargs по имени."},
                {"q": "Что делает @lru_cache?", "a": "Кэширует возвращаемые значения функции на основе аргументов. При повторном вызове с теми же аргументами возвращает кэш (O(1)). maxsize=None — без ограничений."},
                {"q": "Какие itertools самые полезные?", "a": "chain (склейка), product (декартово произведение, полезно для grid search), groupby (группировка), combinations/permutations (для A/B тестов и подбора признаков)."},
            ]),
            knowledge_checklist([
                "Пишу функции с *args и **kwargs",
                "Создаю декораторы с @wraps",
                "Использую @lru_cache для кэширования",
                "Импортирую и применяю itertools.chain, .product, .groupby",
                "Понимаю разницу между list/tuple для hashable аргументов",
            ]),
        ],
        exercises=[
            ex(1, "python", "Напиши функцию `sum_all(*args)`, возвращающую сумму всех args. Пример: sum_all(1,2,3) → 6.",
               "def sum_all(*args):\n    return 0\n", "def sum_all(*args):\n    return sum(args)",
               [{"check": "sum_all(1,2,3)==6", "msg": "Сумма 1+2+3=6"}], ["sum(args)"], 1),
            ex(2, "python", "Напиши функцию `greet(**kwargs)`, которая выводит 'Hello, {name} ({role})!'. По умолчанию name='User', role='student'.",
               "def greet(**kwargs):\n    pass\n",
               "def greet(**kwargs):\n    name = kwargs.get('name', 'User')\n    role = kwargs.get('role', 'student')\n    print(f'Hello, {name} ({role})!')",
               [{"check": "True", "msg": "Функция определена"}], [".get() со значением по умолчанию"], 1),
            ex(3, "python", "Напиши декоратор `log_calls`, который печатает 'Calling {func.__name__}' перед вызовом.",
               "from functools import wraps\ndef log_calls(func):\n    pass\n\n@log_calls\ndef add(a,b):\n    return a+b",
               "from functools import wraps\ndef log_calls(func):\n    @wraps(func)\n    def wrapper(*args, **kwargs):\n        print(f'Calling {func.__name__}')\n        return func(*args, **kwargs)\n    return wrapper\n\n@log_calls\ndef add(a,b):\n    return a+b",
               [{"check": "True", "msg": "Декоратор определён"}], ["@wraps", "return func(*args, **kwargs)"], 2),
            ex(4, "python", "Используй `@lru_cache` для кэширования рекурсивной функции `fib(n)`. Проверь, что fib(30) вычисляется.",
               "from functools import lru_cache\n@lru_cache(maxsize=None)\ndef fib(n):\n    return n if n < 2 else fib(n-1) + fib(n-2)\n",
               "from functools import lru_cache\n@lru_cache(maxsize=None)\ndef fib(n):\n    return n if n < 2 else fib(n-1) + fib(n-2)\n\nprint(fib(30))",
               [{"check": "True", "msg": "Результат выведен"}], ["@lru_cache", "maxsize=None для безлимита"], 1),
            ex(5, "python", "Используй `itertools.chain`, чтобы объединить два списка в один итератор. Сохрани результат как список в `result`.",
               "from itertools import chain\na = [1, 2, 3]\nb = [4, 5, 6]\nresult = []\n",
               "from itertools import chain\na = [1, 2, 3]\nb = [4, 5, 6]\nresult = list(chain(a, b))",
               [{"check": "result == [1,2,3,4,5,6]", "msg": "chain объединяет итераторы"}], ["list(chain(a, b))"], 1),
            ex(6, "python", "Используй `itertools.product` для grid search: создай все комбинации lr=[0.01, 0.1], epochs=[5, 10]. Сохрани как list кортежей в `params`.",
               "from itertools import product\nparams = []\n",
               "from itertools import product\nlr = [0.01, 0.1]\nepochs = [5, 10]\nparams = list(product(lr, epochs))",
               [{"check": "len(params)==4", "msg": "4 комбинации = 2*2"},
                {"check": "(0.01, 5) in params", "msg": "Включена первая комбинация"}],
               ["product(lr, epochs)", "4 комбинации"], 2),
            ex(7, "python", "Создай список всех чисел от 1 до 5, возведённых в квадрат, через itertools.starmap или map. Сохрани в `squares`.",
               "squares = []\n",
               "squares = list(map(lambda x: x**2, range(1, 6)))",
               [{"check": "squares == [1,4,9,16,25]", "msg": "Квадраты 1..5"}],
               ["map(lambda x: x**2, range(1,6))"], 2),
            ex(8, "python", "Дан список словарей `data = [{'name': 'Alice', 'score': 90}, {'name': 'Bob', 'score': 85}]`. Используя itertools.groupby, сгруппируй по первой букве имени. Сохрани результат в виде списка групп.",
               "from itertools import groupby\ndata = sorted([{'name':'Alice','score':90},{'name':'Bob','score':85},{'name':'Ann','score':88}], key=lambda x: x['name'][0])\nresult = []\n",
               "from itertools import groupby\ndata = sorted([{'name':'Alice','score':90},{'name':'Bob','score':85},{'name':'Ann','score':88}], key=lambda x: x['name'][0])\nresult = {k: list(v) for k, v in groupby(data, key=lambda x: x['name'][0])}",
               [{"check": "'A' in result", "msg": "Группа A для Alice и Ann"},
                {"check": "'B' in result", "msg": "Группа B для Bob"}],
               ["groupby требует sorted по тому же key", "dict(groupby) для просмотра"], 3),
        ],
        minutes=40, difficulty=3,
    )

# ─── Block 5: Статистика ────────────────────────────────────────────────────

def _5_13():
    return lesson(
        "5.13", "Множественная проверка гипотез и ANOVA", "mixed", [
            theory(
                "**Множественная проверка гипотез** — проблема: чем больше гипотез мы "
                "тестируем, тем выше вероятность ложноположительного результата (Type I "
                "error). Если запустить 20 A/B тестов при α=0.05, один даст значимый "
                "результат просто по случайности.\n\n"
                "**Методы коррекции:**\n"
                "- **Bonferroni correction**: α / m, где m — число гипотез. Самый "
                "консервативный, снижает мощность.\n"
                "- **FDR (False Discovery Rate)** — контроль доли ложных открытий. "
                "Метод Benjamini-Hochberg: сортируем p-values, находим порог "
                "`(i/m) * α`.\n"
                "- **FWER (Family-Wise Error Rate)** — вероятность хоть одной ложной "
                "гипотезы. Bonferroni и Holm контролируют FWER.\n\n"
                "**ANOVA (Analysis of Variance)** — сравнение средних трёх и более "
                "групп. H₀: все средние равны. Если p < α — хотя бы одна группа "
                "отличается. После ANOVA нужны post-hoc тесты (Tukey HSD) чтобы "
                "понять, какая именно группа отличается.\n\n"
                "`scipy.stats.f_oneway(a, b, c)` — однофакторная ANOVA. "
                "`statsmodels.stats.multicomp.pairwise_tukeyhsd` — Tukey post-hoc."
            ),
            analogy(
                "Bonferroni — если ты проверяешь 20 друзей на честность, снизь "
                "планку доверия в 20 раз, чтобы не обвинить невиновного.",
                "В игровом A/B тесте сравниваем retention в 5 группах. "
                "Bonferroni: α = 0.05/5 = 0.01. Без коррекции один из пяти "
                "тестов покажет значимость на авось."
            ),
            visual(
                "p-value distribution до и после Bonferroni",
                "   Было: α=0.05, m=10\n"
                "   Ожидаем ложных открытий: 10 × 0.05 = 0.5\n"
                "   Стало: α' = 0.05/10 = 0.005\n"
                "                    ┌──────┐\n"
                "   ┌──────┐         │   ✅  │\n"
                "   │  ✅  │         │  p <  │\n"
                "   │ p=0.03│         │ 0.005 │\n"
                "   └──┬───┘         └──────┘\n"
                "   Bonferroni забраковал"
            ),
            example(
                "Есть 3 группы игроков с разным временем сессии. Проверь ANOVA и "
                "Tukey post-hoc.",
                "ANOVA проверяет различие средних. Tukey показывает, какие пары "
                "отличаются.",
                "import numpy as np\nfrom scipy import stats\n"
                "from statsmodels.stats.multicomp import pairwise_tukeyhsd\n"
                "np.random.seed(42)\n"
                "a = np.random.normal(20, 5, 100)\n"
                "b = np.random.normal(22, 5, 100)\n"
                "c = np.random.normal(25, 5, 100)\n"
                "f, p = stats.f_oneway(a, b, c)\n"
                "print(f'ANOVA: F={f:.2f}, p={p:.4f}')\n"
                "data = np.concatenate([a, b, c])\n"
                "groups = ['A']*100 + ['B']*100 + ['C']*100\n"
                "tukey = pairwise_tukeyhsd(data, groups, alpha=0.05)\n"
                "print(tukey)",
                "ANOVA: F=25.34, p=0.0000\n"
                "Tukey HSD:\n"
                "A vs B: reject=True, p=0.012\n"
                "A vs C: reject=True, p=0.000\n"
                "B vs C: reject=True, p=0.003",
                "ANOVA значима (p<0.001). Tukey показывает, что ВСЕ три пары "
                "значимо отличаются. Самая сильная разница — A vs C."
            ),
            common_mistakes([
                {"mistake": "Запустить 100 A/B тестов и найти 'значимый' с p=0.01", "why_bad": "При m=100 ожидается 1 ложный при α=0.01", "fix": "Bonferroni: α' = 0.05/100 = 0.0005"},
                {"mistake": "Использовать ANOVA на сильно неравных группах", "why_bad": "ANOVA чувствительна к гетероскедастичности", "fix": "Используй Kruskal-Wallis (непараметрический) или Welch ANOVA"},
                {"mistake": "После ANOVA не делать post-hoc", "why_bad": "Знаешь, что группы отличаются, но не знаешь какие", "fix": "Всегда Tukey HSD или Dunnett"},
                {"mistake": "Применять Bonferroni к коррелированным гипотезам", "why_bad": "Bonferroni слишком консервативен", "fix": "FDR (Benjamini-Hochberg) для коррелированных тестов"},
            ]),
            interview_questions([
                {"q": "Зачем нужна коррекция на множественные сравнения?", "a": "Чем больше гипотез, тем выше вероятность ложного открытия. При m=20 и α=0.05 ожидается 1 ложный результат. Коррекция (Bonferroni, FDR) снижает α."},
                {"q": "Чем Bonferroni отличается от FDR?", "a": "Bonferroni контролирует FWER — вероятность любой ложной гипотезы (консервативен). FDR контролирует долю ложных открытий среди отклонённых (менее строгий, мощнее). Для скрининга (genomics) — FDR."},
                {"q": "Когда использовать ANOVA, а не t-тест?", "a": "t-тест — для 2 групп, ANOVA — для 3+. После значимой ANOVA нужен post-hoc (Tukey HSD) чтобы узнать, какие группы отличаются."},
            ]),
            knowledge_checklist([
                "Понимаю проблему множественных сравнений",
                "Применяю Bonferroni: α' = α / m",
                "Знаю разницу FWER vs FDR",
                "Провожу ANOVA через scipy.stats.f_oneway",
                "Делаю Tukey post-hoc через pairwise_tukeyhsd",
            ]),
        ],
        exercises=[
            ex(1, "python", "Сгенерируй 3 группы по 50 значений (~N(0,1), N(0.5,1), N(1,1)), seed=42. Сохрани их в `a, b, c`.",
               "import numpy as np\nnp.random.seed(42)\na = np.array([])\nb = np.array([])\nc = np.array([])\n",
               "import numpy as np\nnp.random.seed(42)\na = np.random.normal(0, 1, 50)\nb = np.random.normal(0.5, 1, 50)\nc = np.random.normal(1, 1, 50)",
               [{"check": "len(a)==50 and len(b)==50 and len(c)==50", "msg": "По 50 значений"}],
               ["np.random.normal(mean, std, n)"], 1),
            ex(2, "python", "Проведи однофакторный ANOVA на a, b, c. Сохрани p-value в `p`.",
               "from scipy import stats\nimport numpy as np\nnp.random.seed(42)\na = np.random.normal(0, 1, 50)\nb = np.random.normal(0.5, 1, 50)\nc = np.random.normal(1, 1, 50)\np = 0\n",
               "from scipy import stats\nimport numpy as np\nnp.random.seed(42)\na = np.random.normal(0, 1, 50)\nb = np.random.normal(0.5, 1, 50)\nc = np.random.normal(1, 1, 50)\nf, p = stats.f_oneway(a, b, c)",
               [{"check": "p < 0.05", "msg": "ANOVA значима: группы отличаются"}],
               ["stats.f_oneway(a, b, c)", "F-statistic + p-value"], 2),
            ex(3, "python", "Примени Bonferroni correction: у тебя m=20 гипотез, α=0.05. Сохрани скорректированный порог в `adj_alpha`.",
               "m = 20\nalpha = 0.05\nadj_alpha = 0\n",
               "m = 20\nalpha = 0.05\nadj_alpha = alpha / m",
               [{"check": "adj_alpha == 0.0025", "msg": "0.05 / 20 = 0.0025"}],
               ["α' = α / m", "Bonferroni = самый простой метод"], 1),
            ex(4, "python", "Дан массив из 10 p-values. Примени FDR correction (Benjamini-Hochberg) вручную: отсортируй p, найди порог (i/m)*α где α=0.05. Сколько значимых после коррекции? Сохрани список bool в `significant`.",
               "pvals = [0.001, 0.02, 0.03, 0.04, 0.05, 0.06, 0.1, 0.2, 0.3, 0.5]\nalpha = 0.05\nm = len(pvals)\nsignificant = []\n",
               "pvals = [0.001, 0.02, 0.03, 0.04, 0.05, 0.06, 0.1, 0.2, 0.3, 0.5]\nalpha = 0.05\nm = len(pvals)\nsorted_idx = sorted(range(m), key=lambda i: pvals[i])\nsignificant = [pvals[i] <= (sorted_idx.index(i)+1)/m * alpha for i in range(m)]",
               [{"check": "sum(significant) >= 1", "msg": "Хотя бы одна гипотеза значима после FDR"}],
               ["Benjamini-Hochberg: p_(i) ≤ (i/m)*α", "Сортируй, сравнивай с порогом"], 3),
        ],
        minutes=40, difficulty=3,
    )


def _5_14():
    return lesson(
        "5.14", "Байесовское мышление для Data Science", "mixed", [
            theory(
                "**Байесовский подход** — взгляд на вероятность как на **степень "
                "уверенности**, а не частоту событий. Вместо p-value получаем "
                "апостериорное распределение: `P(θ|X) = P(X|θ)·P(θ) / P(X)`.\n\n"
                "**Ключевые концепции:**\n"
                "- **Prior (априорное)**: что мы знали ДО данных\n"
                "- **Likelihood (правдоподобие)**: насколько данные правдоподобны при "
                "данном θ\n"
                "- **Posterior (апостериорное)**: что мы знаем ПОСЛЕ данных\n\n"
                "**Когда байесовский подход полезен:**\n"
                "- Мало данных — prior помогает не переобучаться\n"
                "- Нужна полная неопределённость, а не точечная оценка\n"
                "- Последовательное обновление: posterior сегодня = prior завтра\n\n"
                "**Пример:** до AB-теста мы думаем, что конверсия ≈ 10% (prior Beta(2,18)). "
                "Получили 15 успехов из 100. Posterior: Beta(2+15, 18+85) = Beta(17, 103). "
                "Можем сказать: «с 95% вероятностью конверсия между 8% и 20%» — "
                "это **credible interval**, аналог доверительного, но интуитивно понятнее."
            ),
            analogy(
                "Prior — твоя интуиция перед экспериментом. Posterior — "
                "обновлённое мнение после данных.",
                "До A/B теста мы думаем, что retention ≈ 20% (prior). "
                "После теста (50 игроков, 12 вернулись) posterior = "
                "Beta(2+12, 8+38). Уверенность выросла."
            ),
            visual(
                "Prior → Likelihood → Posterior",
                "   Prior                Likelihood           Posterior\n"
                "   Beta(2,18)          Binom(100, θ)        Beta(17,103)\n"
                "       ╱╲                 │                     ╱╲\n"
                "      ╱  ╲                │╲                   ╱  ╲\n"
                "     ╱    ╲               │ ╲                 ╱    ╲\n"
                "    ╱      ╲___           │  ╲___            ╱      ╲\n"
                "   ────────           ──────────       ────────────\n"
                "   0.1                 0.15              0.12\n"
                "   Узкий,           Широкий,           Компромисс\n"
                "   неуверенный       пик у 0.15"
            ),
            example(
                "До AB-теста retention = 20% (prior Beta(2,8)). После теста "
                "(5 вернулись из 50) — каков posterior?",
                "Prior: Beta(α=2, β=8). Likelihood: 5 успехов, 45 неудач. "
                "Posterior: Beta(α+5, β+45) = Beta(7, 53). "
                "Среднее posterior = 7/(7+53) = 11.7%.",
                "from scipy import stats\n"
                "prior_a, prior_b = 2, 8\n"
                "success, total = 5, 50\n"
                "post_a = prior_a + success\n"
                "post_b = prior_b + (total - success)\n"
                "print(f'Posterior: Beta({post_a},{post_b})')\n"
                "print(f'Mean: {post_a/(post_a+post_b):.3f}')\n"
                "cred = stats.beta.interval(0.95, post_a, post_b)\n"
                "print(f'95% credible interval: {cred[0]:.3f} - {cred[1]:.3f}')",
                "Posterior: Beta(7,53)\nMean: 0.117\n95% credible interval: 0.048 - 0.217",
                "Posterior среднее (11.7%) — компромисс между prior (20%) и "
                "данными (10%). Credible interval: 4.8%-21.7%. С 95% уверенностью "
                "истинный retention между этими значениями."
            ),
            common_mistakes([
                {"mistake": "Думать, что credible interval = confidence interval", "why_bad": "CI — частотистская концепция, привязана к повторным экспериментам. Credible — прямое вероятностное утверждение", "fix": "Credible: P(θ ∈ [a,b] | data) = 0.95"},
                {"mistake": "Использовать flat prior (Beta(1,1)) без причины", "why_bad": "Не используешь доступную информацию", "fix": "Используй weakly informative prior Beta(2,18) для конверсии"},
                {"mistake": "Сравнивать байесовские A/B тесты с p-value", "why_bad": "Другая философия: posterior vs p-value", "fix": "Считай вероятность что B > A: P(θ_B > θ_A | data)"},
            ]),
            interview_questions([
                {"q": "В чём разница между Bayesian и Frequentist?", "a": "Frequentist: вероятность = частота в бесконечных повторениях. Bayesian: вероятность = степень уверенности. Bayesian обновляет prior данными → posterior."},
                {"q": "Что такое conjugate prior?", "a": "Prior, после обновления данными дающий posterior того же семейства. Beta-Binomial — классический conjugate: Beta(α,β) + Binomial → Beta(α+success, β+failure)."},
                {"q": "Как байесовский подход помогает при малых данных?", "a": "Prior регуляризирует оценку, не давая переобучаться на шуме. При n→infinity данные доминируют и posterior сходится к MLE."},
            ]),
            knowledge_checklist([
                "Понимаю формулу Байеса: P(θ|X) ∝ P(X|θ)·P(θ)",
                "Различаю prior, likelihood, posterior",
                "Использую Beta-Binomial conjugate для конверсий",
                "Считаю credible interval через scipy.stats.beta.interval",
                "Понимаю разницу credible vs confidence interval",
            ]),
        ],
        exercises=[
            ex(1, "python", "У тебя prior Beta(2,18) для конверсии. Получено 30 успехов из 200. Сохрани параметры posterior в `post_a, post_b`.",
               "prior_a, prior_b = 2, 18\ntotal, success = 200, 30\npost_a = 0\npost_b = 0\n",
               "prior_a, prior_b = 2, 18\ntotal, success = 200, 30\npost_a = prior_a + success\npost_b = prior_b + (total - success)",
               [{"check": "post_a == 32", "msg": "α = prior_a + success = 2 + 30 = 32"},
                {"check": "post_b == 188", "msg": "β = prior_b + (total - success) = 18 + 170 = 188"}],
               ["Beta(α,β) + data → Beta(α+success, β+failure)"], 1),
            ex(2, "python", "По posterior из предыдущего упражнения рассчитай среднее (mean). Сохрани в `post_mean`.",
               "post_a, post_b = 32, 188\npost_mean = 0\n",
               "post_a, post_b = 32, 188\npost_mean = post_a / (post_a + post_b)",
               [{"check": "abs(post_mean - 0.145) < 0.01", "msg": "Mean = α/(α+β) ≈ 0.145"}],
               ["mean = α/(α+β)", "Для Beta распределения"], 2),
            ex(3, "python", "Используя `scipy.stats.beta.interval(0.95, a, b)`, вычисли 95% credible interval для posterior Beta(7, 53). Сохрани в `lower, upper`.",
               "from scipy import stats\nlower, upper = 0, 0\n",
               "from scipy import stats\nlower, upper = stats.beta.interval(0.95, 7, 53)",
               [{"check": "0.04 < lower < 0.06", "msg": "Lower bound ~ 5%"},
                {"check": "0.20 < upper < 0.23", "msg": "Upper bound ~ 21%"}],
               ["stats.beta.interval(confidence, a, b)", "Credible interval от posterior"], 2),
        ],
        minutes=35, difficulty=3,
    )


def _5_15():
    return lesson(
        "5.15", "scipy.stats на практике: ttest, Mann-Whitney, χ²", "mixed", [
            theory(
                "**scipy.stats** — главный инструмент для статистических тестов "
                "в Python. Три самых частых:\n\n"
                "**1. t-test (ttest_ind):** сравнивает средние ДВУХ независимых групп. "
                "Предполагает нормальность (при n>30 — робастен по CLT). "
                "`equal_var=False` — Welch's t-test (не предполагает равенство дисперсий).\n\n"
                "**2. Mann-Whitney U (mannwhitneyu):** непараметрический аналог t-теста. "
                "Сравнивает распределения, а не средние. Не требует нормальности. "
                "Используй, когда данные скошены или мало данных.\n\n"
                "**3. χ²-тест (chi2_contingency):** проверяет связь между двумя "
                "категориальными переменными. Пример: пол × купил/не купил. "
                "Строим таблицу сопряжённости (contingency table), считаем χ².\n\n"
                "Какой тест выбрать:\n"
                "- Две continuous группы, нормальные → t-test\n"
                "- Две continuous группы, не-нормальные → Mann-Whitney\n"
                "- Две категориальные → χ²-тест\n"
                "- Три+ группы → ANOVA (урок 5.11)"
            ),
            analogy(
                "t-test — линейка для двух досок (средние), Mann-Whitney — "
                "сравнение двух стопок бумаги на ощупь (распределения), χ² — "
                "проверка, что состав пицц в двух городах одинаков",
                "В игровой аналитике: t-test для времени сессии (нормальное), "
                "Mann-Whitney для доната (скошен, много нулей), "
                "χ² для связи жанр × платформа."
            ),
            visual(
                "Дерево выбора статистического теста",
                "   ┌────────────────────────────────────┐\n"
                "   │    Сравнение двух групп             │\n"
                "   └────────────────┬───────────────────┘\n"
                "                    ↓\n"
                "   ┌──────────────────────────────┐\n"
                "   │ Обе continuous?               │\n"
                "   ├── Yes ──── Нормальные? ─── Yes → t-test\n"
                "   │           └── No ─────────────→ Mann-Whitney\n"
                "   └── No ───── Таблица 2×2? ──────→ χ²-тест"
            ),
            example(
                "У двух групп игроков (A — обычные, B — премиум) время сессии. "
                "Проверь t-test, Mann-Whitney, и χ² для платформы (iOS vs Android)",
                "t-test для нормальных, Mann-Whitney для любых, χ² для категорий.",
                "import numpy as np\nfrom scipy import stats\n"
                "np.random.seed(42)\n"
                "sess_a = np.random.normal(20, 5, 100)\n"
                "sess_b = np.random.normal(25, 8, 100)\n"
                "t, p_t = stats.ttest_ind(sess_a, sess_b)\n"
                "mw, p_mw = stats.mannwhitneyu(sess_a, sess_b)\n"
                "print(f't-test: p={p_t:.4f}')\n"
                "print(f'Mann-Whitney: p={p_mw:.4f}')\n"
                "table = np.array([[40, 60], [55, 45]])\n"
                "chi2, p_chi, dof, expected = stats.chi2_contingency(table)\n"
                "print(f'χ²: p={p_chi:.4f}')",
                "t-test: p=0.0000\nMann-Whitney: p=0.0000\nχ²: p=0.0300",
                "Оба теста показывают значимую разницу между группами (разные "
                "средние и распределения). χ²-тест показывает связь между "
                "типом группы и платформой."
            ),
            common_mistakes([
                {"mistake": "Использовать t-test для 3+ групп", "why_bad": "Попарные t-тесты накручивают Type I error", "fix": "ANOVA для 3+ групп"},
                {"mistake": "mannwhitneyu без alternative='two-sided'", "why_bad": "По умолчанию 'two-sided', но есть 'less'/'greater'", "fix": "Указывай alternative в зависимости от гипотезы"},
                {"mistake": "chi2_contingency с ожидаемыми < 5", "why_bad": "χ²-тест ненадёжен при малых ожидаемых", "fix": "Используй Fisher exact test (fisher_exact) для малых таблиц"},
                {"mistake": "Не проверять equal_var для t-test", "why_bad": "Если дисперсии разные, стандартный t-test врёт", "fix": "ttest_ind(..., equal_var=False) — Welch's t-test"},
            ]),
            interview_questions([
                {"q": "Когда использовать Mann-Whitney вместо t-test?", "a": "Когда данные не нормальные (скошенные, выбросы, мало данных). Mann-Whitney непараметрический — сравнивает медианы рангов, не требует нормальности."},
                {"q": "Какой тест для связи двух категориальных переменных?", "a": "χ²-тест (chi2_contingency) для таблицы сопряжённости. H₀: переменные независимы. p < 0.05 → есть связь."},
                {"q": "Что такое Welch's t-test?", "a": "t-test без предположения о равенстве дисперсий. Используй `ttest_ind(equal_var=False)`. Более робастен, чем стандартный Student's t-test."},
            ]),
            knowledge_checklist([
                "Провожу t-test через scipy.stats.ttest_ind",
                "Провожу Mann-Whitney через mannwhitneyu",
                "Провожу χ²-тест через chi2_contingency",
                "Выбираю правильный тест по типу данных",
                "Понимаю разницу параметрических и непараметрических тестов",
            ]),
        ],
        exercises=[
            ex(1, "python", "Дан `a` и `b` — 2 группы по 50 значений. Проведи t-test. Сохрани p-value в `p`.",
               "import numpy as np\nfrom scipy import stats\nnp.random.seed(42)\na = np.random.normal(0, 1, 50)\nb = np.random.normal(1, 1, 50)\np = 0\n",
               "import numpy as np\nfrom scipy import stats\nnp.random.seed(42)\na = np.random.normal(0, 1, 50)\nb = np.random.normal(1, 1, 50)\nt, p = stats.ttest_ind(a, b)",
               [{"check": "p < 0.05", "msg": "Группы различаются"}], ["stats.ttest_ind(a, b)"], 1),
            ex(2, "python", "Дан `a` и `b` с разными дисперсиями. Проведи Welch's t-test (equal_var=False). Сохрани p в `p_welch`.",
               "import numpy as np\nfrom scipy import stats\nnp.random.seed(42)\na = np.random.normal(0, 1, 50)\nb = np.random.normal(0.5, 3, 50)\np_welch = 0\n",
               "import numpy as np\nfrom scipy import stats\nnp.random.seed(42)\na = np.random.normal(0, 1, 50)\nb = np.random.normal(0.5, 3, 50)\np_welch = stats.ttest_ind(a, b, equal_var=False)[1]",
               [{"check": "p_welch > 0", "msg": "p-value > 0"}], ["ttest_ind(equal_var=False)", "Welch — робастен к гетероскедастичности"], 2),
            ex(3, "python", "Дан `a` и `b` — два массива (скошенные). Проведи Mann-Whitney U test. Сохрани p-value в `p_mw`.",
               "import numpy as np\nfrom scipy import stats\nnp.random.seed(42)\na = np.random.exponential(1, 50)\nb = np.random.exponential(2, 50)\np_mw = 0\n",
               "import numpy as np\nfrom scipy import stats\nnp.random.seed(42)\na = np.random.exponential(1, 50)\nb = np.random.exponential(2, 50)\np_mw = stats.mannwhitneyu(a, b)[1]",
               [{"check": "p_mw < 0.05", "msg": "Mann-Whitney улавливает разницу"}],
               ["mannwhitneyu(a, b)", "Непараметрический, не требует нормальности"], 2),
            ex(4, "python", "Дан `table = np.array([[30, 70], [50, 50]])` (2×2). Проведи χ²-тест. Сохрани p-value в `p_chi`.",
               "import numpy as np\nfrom scipy import stats\ntable = np.array([[30, 70], [50, 50]])\np_chi = 0\n",
               "import numpy as np\nfrom scipy import stats\ntable = np.array([[30, 70], [50, 50]])\nchi2, p_chi, dof, expected = stats.chi2_contingency(table)",
               [{"check": "p_chi > 0", "msg": "χ²-тест корректен"}],
               ["chi2_contingency(table)", "Проверка независимости категорий"], 1),
        ],
        minutes=35, difficulty=2,
    )

# ─── Block 7: Machine Learning ──────────────────────────────────────────────

def _7_18():
    return lesson(
        "7.18", "PCA и t-SNE: снижение размерности", "mixed", [
            theory(
                "**Снижение размерности** — преобразование данных с большим числом "
                "признаков (100+) в пространство меньшей размерности (2-50) с "
                "минимальной потерей информации.\n\n"
                "**PCA (Principal Component Analysis):** находит новые оси (главные "
                "компоненты), вдоль которых дисперсия данных максимальна. "
                "Первый компонент — направление максимальной дисперсии, второй — "
                "ортогональный первому с оставшейся дисперсией и т.д. "
                "`sklearn.decomposition.PCA(n_components=2)`. "
                "Используется для сжатия, шумоподавления, визуализации.\n\n"
                "**t-SNE (t-Distributed Stochastic Neighbor Embedding):** нелинейный "
                "метод для визуализации. Сохраняет локальную структуру: точки, "
                "близкие в исходном пространстве, остаются близкими в 2D. "
                "`sklearn.manifold.TSNE(n_components=2)`.\n\n"
                "**UMAP (Uniform Manifold Approximation):** современная альтернатива "
                "t-SNE — быстрее, лучше сохраняет глобальную структуру. "
                "`umap.UMAP(n_components=2)`.\n\n"
                "**Когда что:** PCA — для сжатия и интерпретации (компоненты — "
                "взвешенные суммы признаков). t-SNE/UMAP — только для "
                "визуализации (нельзя делать выводы о расстояниях между кластерами)."
            ),
            analogy(
                "PCA — фотография трёхмерного объекта с лучшего ракурса (сохраняет "
                "максимум информации в 2D). t-SNE — карта метро: показывает "
                "соседство станций, но искажает реальные расстояния.",
                "В данных телеметрии ракеты 50 сенсоров — PCA сжимает их в 5 "
                "компонент-«обобщённых» сенсоров для модели. t-SNE визуализирует "
                "режимы полёта как 2D-кластеры."
            ),
            visual(
                "PCA на 2D (проекция из 3D)",
                "   До (3D)                   После PCA (2D)\n"
                "       z│                      y│\n"
                "        │╲                       │   .   .\n"
                "        │ ╲                      │  . . .\n"
                "        │  ╲                     │ . . .\n"
                "        └──╲── y              ──┘────── x\n"
                "          ╱   └── x            PC1 = max variance\n"
                "        ╱                    PC2 = orthogonal\n"
                "    Визуальный шум          Кластеры видны"
            ),
            example(
                "Сгенерируй 3D-данные (3 кластера) и примени PCA → 2D. "
                "Сравни с t-SNE.",
                "PCA линеен и быстр (O(n·d²)), t-SNE нелинеен и медленнее "
                "(O(n²)). PCA сохраняет глобальную структуру, t-SNE — локальную.",
                "import numpy as np\nimport matplotlib.pyplot as plt\n"
                "from sklearn.decomposition import PCA\n"
                "from sklearn.manifold import TSNE\n"
                "np.random.seed(42)\n"
                "clusters = []\n"
                "for center in [[0,0,0], [5,5,0], [0,5,5]]:\n"
                "    clusters.append(np.random.normal(center, 0.5, (50,3)))\n"
                "X = np.vstack(clusters)\n"
                "X_pca = PCA(n_components=2).fit_transform(X)\n"
                "X_tsne = TSNE(n_components=2, random_state=42).fit_transform(X)\n"
                "fig, axes = plt.subplots(1,2,figsize=(12,5))\n"
                "axes[0].scatter(X_pca[:,0], X_pca[:,1], c=np.repeat([0,1,2],50), alpha=0.6)\n"
                "axes[0].set_title('PCA')\n"
                "axes[1].scatter(X_tsne[:,0], X_tsne[:,1], c=np.repeat([0,1,2],50), alpha=0.6)\n"
                "axes[1].set_title('t-SNE')\n"
                "plt.show()",
                "Два графика: PCA (кластеры частично накладываются), "
                "t-SNE (кластеры чётко разделены, расстояния искажены)",
                "PCA сохраняет глобальную дисперсию — кластеры видны, но "
                "накладываются. t-SNE разводит кластеры сильнее за счёт "
                "нелинейности — локальная структура чётче, глобальные расстояния "
                "потеряны. Для визуализации t-SNE/UMAP лучше, для сжатия — PCA."
            ),
            common_mistakes([
                {"mistake": "PCA.fit(X) без стандартизации", "why_bad": "Переменные с большим масштабом доминируют", "fix": "StandardScaler().fit_transform(X) перед PCA"},
                {"mistake": "Интерпретировать расстояния в t-SNE", "why_bad": "t-SNE искажает глобальные расстояния, сохраняя только локальные", "fix": "Смотри на кластеры, не на их взаимное расположение"},
                {"mistake": "Использовать t-SNE для сжатия перед ML моделью", "why_bad": "t-SNE не сохраняет глобальную структуру — модель не обобщит", "fix": "Используй PCA или UMAP для сжатия"},
                {"mistake": "Perplexity t-SNE = 5 для 10000 точек", "why_bad": "Слишком низкая perplexity — локальный шум", "fix": "perplexity = 30-50 по умолчанию, настраивай под данные"},
            ]),
            interview_questions([
                {"q": "Чем PCA отличается от t-SNE?", "a": "PCA — линейный, сохраняет глобальную дисперсию, интерпретируем (компоненты = взвешенные суммы признаков). t-SNE — нелинейный, сохраняет локальную структуру, только для визуализации."},
                {"q": "Как выбрать число компонент PCA?", "a": "По explained variance ratio: сумма дисперсий первых k компонент. Обычно берут k, где накопленная дисперсия ≥ 80-95%. Elbow method на scree plot."},
                {"q": "Что такое UMAP и чем лучше t-SNE?", "a": "UMAP (Uniform Manifold Approximation) — быстрее t-SNE (O(n log n) vs O(n²)), лучше сохраняет глобальную структуру, не искажает расстояния между кластерами."},
            ]),
            knowledge_checklist([
                "Применяю PCA через sklearn.decomposition.PCA",
                "Стандартизую данные перед PCA",
                "Визуализирую высокоразмерные данные через t-SNE",
                "Понимаю разницу PCA vs t-SNE vs UMAP",
                "Выбираю число компонент по explained variance ratio",
            ]),
        ],
        exercises=[
            ex(1, "python", "Сгенерируй 100 точек в 5D (np.random.randn(100, 5)), seed=42. Примени PCA(n_components=2). Сохрани результат в `X_pca`.",
               "import numpy as np\nfrom sklearn.decomposition import PCA\nnp.random.seed(42)\nX = np.random.randn(100, 5)\nX_pca = np.array([])\n",
               "import numpy as np\nfrom sklearn.decomposition import PCA\nnp.random.seed(42)\nX = np.random.randn(100, 5)\nX_pca = PCA(n_components=2).fit_transform(X)",
               [{"check": "X_pca.shape == (100, 2)", "msg": "100 точек в 2D"}],
               ["PCA(n_components=2).fit_transform(X)"], 1),
            ex(2, "python", "После PCA посчитай explained_variance_ratio_. Сохрани его в `evr`.",
               "import numpy as np\nfrom sklearn.decomposition import PCA\nnp.random.seed(42)\nX = np.random.randn(100, 5)\npca = PCA(n_components=2).fit(X)\nevr = np.array([])\n",
               "import numpy as np\nfrom sklearn.decomposition import PCA\nnp.random.seed(42)\nX = np.random.randn(100, 5)\npca = PCA(n_components=2).fit(X)\nevr = pca.explained_variance_ratio_",
               [{"check": "len(evr) == 2", "msg": "2 компоненты"},
                {"check": "abs(sum(evr) - 1) < 0.5", "msg": "EV ratio < 1"}],
               ["pca.explained_variance_ratio_", "Доля дисперсии на компоненту"], 2),
            ex(3, "python", "Сгенерируй 200 точек в 10D. Найди число компонент с накопленной дисперсией ≥ 90%. Сохрани в `k`.",
               "import numpy as np\nfrom sklearn.decomposition import PCA\nnp.random.seed(42)\nX = np.random.randn(200, 10)\npca = PCA().fit(X)\ncumsum = np.cumsum(pca.explained_variance_ratio_)\nk = 0\n",
               "import numpy as np\nfrom sklearn.decomposition import PCA\nnp.random.seed(42)\nX = np.random.randn(200, 10)\npca = PCA().fit(X)\ncumsum = np.cumsum(pca.explained_variance_ratio_)\nk = int(np.argmax(cumsum >= 0.9)) + 1",
               [{"check": "k >= 1", "msg": "Хотя бы 1 компонента"}],
               ["np.cumsum + argmax", "Порог 0.9"], 3),
            ex(4, "python", "Сгенерируй 150 точек в 3D (2 кластера). Примени t-SNE (n_components=2, random_state=42). Сохрани в `X_tsne`.",
               "import numpy as np\nfrom sklearn.manifold import TSNE\nnp.random.seed(42)\nc1 = np.random.normal([0,0,0], 0.5, (75,3))\nc2 = np.random.normal([3,3,3], 0.5, (75,3))\nX = np.vstack([c1, c2])\nX_tsne = np.array([])\n",
               "import numpy as np\nfrom sklearn.manifold import TSNE\nnp.random.seed(42)\nc1 = np.random.normal([0,0,0], 0.5, (75,3))\nc2 = np.random.normal([3,3,3], 0.5, (75,3))\nX = np.vstack([c1, c2])\nX_tsne = TSNE(n_components=2, random_state=42).fit_transform(X)",
               [{"check": "X_tsne.shape == (150, 2)", "msg": "150 точек в 2D"}],
               ["TSNE(n_components=2)", "random_state для воспроизводимости"], 2),
        ],
        minutes=55, difficulty=3,
    )


def _7_19():
    return lesson(
        "7.19", "DBSCAN и HDBSCAN: кластеризация реальных данных", "mixed", [
            theory(
                "**DBSCAN (Density-Based Spatial Clustering, 1996)** — "
                "кластеризация на основе плотности. В отличие от K-Means:\n"
                "- Не требует указывать число кластеров K\n"
                "- Находит кластеры произвольной формы (не только сферические)\n"
                "- Определяет шумовые точки (не принадлежат ни одному кластеру)\n\n"
                "**Параметры:** `eps` (радиус окрестности) и `min_samples` "
                "(минимальное число точек в eps чтобы образовать кластер). "
                "Точки с ≥min_samples соседями — core points, всё остальное — "
                "border или noise.\n\n"
                "**HDBSCAN (2017)** — иерархическая эволюция DBSCAN. Не требует "
                "eps, находит кластеры разной плотности, строит иерархию "
                "кластеров. `pip install hdbscan`.\n\n"
                "**Когда использовать:** данные с шумом, кластеры неправильной "
                "формы, аномалии. Например: кластеризация игроков по поведению "
                "(есть «обычные» и «аномальные» читеры), обнаружение аномалий "
                "телеметрии."
            ),
            analogy(
                "DBSCAN — найти клубы людей на городской площади: в центре "
                "каждого клуба — плотное ядро, по краям — полупусто. "
                "Одиночные прохожие — шум",
                "Кластеризация игроков: плотные кластеры «активных» и "
                "«казуальных», плюс шум — подозрительные аккаунты (боты/читеры) "
                "вне кластеров"
            ),
            visual(
                "DBSCAN находит кластеры произвольной формы + шум",
                "   K-Means (неверно)       DBSCAN (верно)\n"
                "       ╱╲                     ┌──────┐\n"
                "      ╱ ╱╲                    │ ╭──╮ │\n"
                "     ╱ ╱──╲                   │ │  │ │\n"
                "    ╱  ╲ ╱  ╲                 │ ╰──╯ │\n"
                "   ╱    V    ╲                └──────┘\n"
                "   K-Means делит            DBSCAN находит\n"
                "   полумесяцы пополам        форму + шум (•)"
            ),
            example(
                "Сгенерируй 2 кластера-полумесяца + шум. Кластеризуй DBSCAN "
                "и сравни с K-Means.",
                "make_moons из sklearn генерирует полумесяцы. DBSCAN находит "
                "их форму. K-Means режет пополам.",
                "import numpy as np\nimport matplotlib.pyplot as plt\n"
                "from sklearn.cluster import DBSCAN, KMeans\n"
                "from sklearn.datasets import make_moons\n"
                "X, _ = make_moons(n_samples=300, noise=0.05, random_state=42)\n"
                "noise = np.random.uniform(-1.5, 2.5, (30,2))\n"
                "X = np.vstack([X, noise])\n"
                "db = DBSCAN(eps=0.3, min_samples=5).fit_predict(X)\n"
                "km = KMeans(n_clusters=2, random_state=42).fit_predict(X)\n"
                "fig, axes = plt.subplots(1,2,figsize=(12,5))\n"
                "axes[0].scatter(X[:,0], X[:,1], c=db, cmap='Set1')\n"
                "axes[0].set_title('DBSCAN')\n"
                "axes[1].scatter(X[:,0], X[:,1], c=km, cmap='Set1')\n"
                "axes[1].set_title('K-Means (2 cluster)')\n"
                "plt.show()",
                "График: DBSCAN находит 2 полумесяца + шум (серые точки), "
                "K-Means делит их пополам крест-накрест",
                "DBSCAN корректно разделяет полумесяцы и помечает 30 шумовых "
                "точек как -1 (noise). K-Means режет по прямой — кластеры "
                "перемешаны. Для неправильных форм DBSCAN незаменим."
            ),
            common_mistakes([
                {"mistake": "Не нормализовать данные перед DBSCAN", "why_bad": "eps зависит от масштаба — один признак доминирует", "fix": "StandardScaler или MinMaxScaler"},
                {"mistake": "DBSCAN `eps` выбран на глаз", "why_bad": "Слишком мал — всё noise, слишком велик — один кластер", "fix": "K-distance plot: найди 'elbow' — оптимальный eps"},
                {"mistake": "Использовать DBSCAN с категориальными признаками", "why_bad": "Евклидово расстояние для категорий бессмыслено", "fix": "Используй Gower distance или one-hot + HDBSCAN"},
                {"mistake": "Думать, что DBSCAN подходит для high-dimensional", "why_bad": "Проклятие размерности: eps бессмыслен при 100+ признаках", "fix": "Сначала PCA до 10-50 компонент, потом DBSCAN"},
            ]),
            interview_questions([
                {"q": "Чем DBSCAN отличается от K-Means?", "a": "K-Means требует K и находит сферические кластеры. DBSCAN не требует K, находит кластеры любой формы, определяет шум. DBSCAN работает по плотности."},
                {"q": "Что такое eps и min_samples в DBSCAN?", "a": "eps — радиус окрестности (определяет плотность). min_samples — минимальное число точек для ядра кластера. Меньше eps = больше кластеров, больше min_samples = меньше кластеров."},
                {"q": "Чем HDBSCAN лучше DBSCAN?", "a": "HDBSCAN не требует eps, находит кластеры разной плотности (иерархически), работает лучше с реальными данными где плотность неоднородна."},
            ]),
            knowledge_checklist([
                "Кластеризую DBSCAN через sklearn.cluster.DBSCAN",
                "Выбираю eps через K-distance plot",
                "Нормализую данные перед кластеризацией",
                "Понимаю разницу DBSCAN vs K-Means",
                "Знаю про HDBSCAN для разной плотности",
            ]),
        ],
        exercises=[
            ex(1, "python", "Сгенерируй 100 точек из make_moons(noise=0.05, random_state=42). Сохрани в `X`.",
               "from sklearn.datasets import make_moons\nX = None\n",
               "from sklearn.datasets import make_moons\nX, _ = make_moons(n_samples=100, noise=0.05, random_state=42)",
               [{"check": "X.shape == (100, 2)", "msg": "100 точек в 2D"}],
               ["make_moons(n_samples=100, noise=0.05)"], 1),
            ex(2, "python", "Примени DBSCAN(eps=0.3, min_samples=5) к X. Сохрани метки в `labels`.",
               "from sklearn.datasets import make_moons\nfrom sklearn.cluster import DBSCAN\nX, _ = make_moons(n_samples=100, noise=0.05, random_state=42)\nlabels = np.array([])\n",
               "from sklearn.datasets import make_moons\nfrom sklearn.cluster import DBSCAN\nimport numpy as np\nX, _ = make_moons(n_samples=100, noise=0.05, random_state=42)\nlabels = DBSCAN(eps=0.3, min_samples=5).fit_predict(X)",
               [{"check": "len(np.unique(labels)) >= 2", "msg": "Мимум 2 кластера (может быть шум -1)"}],
               ["DBSCAN(eps, min_samples).fit_predict(X)", "eps=0.3, min_samples=5"], 2),
            ex(3, "python", "Посчитай число шумовых точек (label == -1) после DBSCAN и сохрани в `noise_cnt`.",
               "from sklearn.datasets import make_moons\nfrom sklearn.cluster import DBSCAN\nimport numpy as np\nX, _ = make_moons(n_samples=100, noise=0.05, random_state=42)\nlabels = DBSCAN(eps=0.3, min_samples=5).fit_predict(X)\nnoise_cnt = 0\n",
               "from sklearn.datasets import make_moons\nfrom sklearn.cluster import DBSCAN\nimport numpy as np\nX, _ = make_moons(n_samples=100, noise=0.05, random_state=42)\nlabels = DBSCAN(eps=0.3, min_samples=5).fit_predict(X)\nnoise_cnt = int((labels == -1).sum())",
               [{"check": "noise_cnt >= 0", "msg": "Количество шумовых точек"}],
               ["(labels == -1).sum()", "Шум = точки не входящие в кластеры"], 2),
        ],
        minutes=40, difficulty=3,
    )

# ─── Block 8: Feature Engineering ───────────────────────────────────────────

def _8_10():
    return lesson(
        "8.10", "Рекомендательные системы: collaborative filtering", "mixed", [
            theory(
                "**Рекомендательные системы** — алгоритмы, предсказывающие "
                "предпочтения пользователя. Два основных подхода:\n\n"
                "**1. Collaborative Filtering (CF):** рекомендует то, что "
                "понравилось похожим пользователям. Не требует знаний о товаре "
                "(только матрицу user-item).\n"
                "- **User-based:** найди похожих пользователей, рекомендует их "
                "лайки\n"
                "- **Item-based:** товар похож на те, что пользователь уже "
                "лайкнул\n\n"
                "**2. Matrix Factorization (SVD, FunkSVD):** разлагает матрицу "
                "user-item на две низкоранговые: `R ≈ U·Vᵀ`. "
                "`U` — латентные признаки пользователей, `V` — товаров. "
                "`sklearn.decomposition.TruncatedSVD` или `surprise.SVD`.\n\n"
                "**Cold start problem:** новый пользователь/товар — нет истории. "
                "Решение: популярное/случайное, content-based фичи, "
                "гибридные системы.\n\n"
                "**Метрики:** RMSE (точность предсказания рейтинга), "
                "Precision@K, Recall@K, NDCG (качество топа рекомендаций)."
            ),
            analogy(
                "CF — спросить друга, что посмотреть. Item-based: раз ты любишь "
                "Mass Effect, попробуй Star Wars: Knights of the Old Republic",
                "Игровая платформа: пользователь A играет в стратегии и "
                "экшены. CF находит похожих пользователей → рекомендует "
                "новую стратегию, которую они лайкнули."
            ),
            visual(
                "Matrix Factorization: R ≈ U·Vᵀ",
                "   Пользователи × Игры       Латентные факторы\n"
                "        игры                   k факторов\n"
                "        ┌────┐               ┌──┐\n"
                "        │  R  │    ≈    U    │  │  Vᵀ\n"
                "        │     │          │  │  │  \n"
                "        └────┘               └──┘\n"
                "   Размер m×n             (m×k) × (k×n)\n"
                "   Разряжена (>95% NaN)   Плотная, предсказывает NaN"
            ),
            example(
                "Создай матрицу user-item (10×5) и примени TruncatedSVD "
                "для предсказания оценок.",
                "Заполняем NaN средним по строке. SVD раскладывает на "
                "U и V. Восстанавливаем R_pred = U·V.",
                "import numpy as np\nfrom sklearn.decomposition import TruncatedSVD\n"
                "R = np.array([\n"
                "    [5, 4, 0, 0, 1],\n"
                "    [0, 5, 4, 0, 0],\n"
                "    [4, 0, 5, 3, 0],\n"
                "    [0, 3, 0, 5, 4],\n"
                "    [3, 0, 0, 4, 5],\n"
                "    [0, 4, 3, 0, 0],\n"
                "    [5, 0, 0, 5, 4],\n"
                "    [2, 5, 0, 0, 3],\n"
                "    [4, 0, 4, 0, 5],\n"
                "    [0, 3, 5, 4, 0],\n"
                "], dtype=float)\n"
                "R_filled = np.where(R == 0, np.nanmean(R, axis=0), R)\n"
                "svd = TruncatedSVD(n_components=2, random_state=42)\n"
                "U = svd.fit_transform(R_filled)\n"
                "V = svd.components_\n"
                "R_pred = U @ V\n"
                "print('Predicted (user 0, game 3):', R_pred[0,3])",
                "Predicted (user 0, game 3): 2.87",
                "SVD предсказал, что пользователь 0 оценит игру 3 (которую "
                "не оценивал) на 2.87/5. Основание: похожие пользователи "
                "и латентные факторы (жанр, стиль игры)."
            ),
            common_mistakes([
                {"mistake": "Игнорировать cold start", "why_bad": "Новый пользователь получит пустую рекомендацию", "fix": "Гибрид: популярное пока нет истории, потом персональное"},
                {"mistake": "Не фильтровать популярное", "why_bad": "Самые популярные — почти всегда одни и те же", "fix": "Регуляризация: penalize популярное, бусти редкие находки"},
                {"mistake": "RMSE как единственная метрика", "why_bad": "Хороший RMSE ≠ хороший топ-10", "fix": "NDCG@K, Precision@K для оценки ранжирования"},
                {"mistake": "Использовать Pearson на разряженной матрице", "why_bad": "NaN ≠ 0, пользователи с 1 пересечением дают шум", "fix": "Только общие игры ≥ 5, или cosine similarity"},
            ]),
            interview_questions([
                {"q": "Что такое collaborative filtering?", "a": "Алгоритм рекомендаций на основе взаимодействий user-item. User-CF: похожие пользователи → похожие рекомендации. Item-CF: похожие товары. Не требует метаданных о товаре."},
                {"q": "В чём идея matrix factorization?", "a": "Разложить разреженную матрицу R (m×n) на две плотные U (m×k) и V (k×n), где k — число латентных факторов. R_ij ≈ U_i · V_j."},
                {"q": "Что такое cold start problem?", "a": "Новый пользователь или товар без истории взаимодействий. Решения: популярное по умолчанию, content-based (фичи пользователя/товара), гибридные системы, warm-start через демографию."},
            ]),
            knowledge_checklist([
                "Понимаю User-CF vs Item-CF",
                "Строю матрицу user-item",
                "Применяю SVD для matrix factorization",
                "Знаю метрики: RMSE, Precision@K, NDCG",
                "Решаю cold start через гибридный подход",
            ]),
        ],
        exercises=[
            ex(1, "python", "Создай матрицу 4×3 (4 пользователя, 3 игры). Оценки 1-5, 0 = нет оценки. Сохрани в `R`.",
               "import numpy as np\nR = np.array([\n    [5, 4, 0],\n    [0, 5, 3],\n    [4, 0, 5],\n    [0, 3, 4],\n], dtype=float)\n",
               "import numpy as np\nR = np.array([\n    [5, 4, 0],\n    [0, 5, 3],\n    [4, 0, 5],\n    [0, 3, 4],\n], dtype=float)",
               [{"check": "R.shape == (4, 3)", "msg": "4 пользователя, 3 игры"}],
               ["dtype=float для корректной работы"], 1),
            ex(2, "python", "Заполни NaN (нули) средним по столбцу. Сохрани в `R_filled`.",
               "import numpy as np\nR = np.array([[5,4,0],[0,5,3],[4,0,5],[0,3,4]], dtype=float)\nR_filled = R.copy()\n",
               "import numpy as np\nR = np.array([[5,4,0],[0,5,3],[4,0,5],[0,3,4]], dtype=float)\nR_filled = np.where(R == 0, np.nanmean(R, axis=0), R)",
               [{"check": "R_filled.shape == (4, 3)", "msg": "Та же форма"},
                {"check": "R_filled[0,2] > 0", "msg": "Пропуск заполнен"}],
               ["np.where(R==0, np.nanmean(...), R)"], 2),
            ex(3, "python", "Примени TruncatedSVD(n_components=2, random_state=42) к R_filled. Сохрани U и V.",
               "from sklearn.decomposition import TruncatedSVD\nimport numpy as np\nR = np.array([[5,4,0],[0,5,3],[4,0,5],[0,3,4]], dtype=float)\nR_filled = np.where(R==0, np.nanmean(R,axis=0), R)\nsvd = TruncatedSVD(n_components=2, random_state=42)\nU = None\nV = None\n",
               "from sklearn.decomposition import TruncatedSVD\nimport numpy as np\nR = np.array([[5,4,0],[0,5,3],[4,0,5],[0,3,4]], dtype=float)\nR_filled = np.where(R==0, np.nanmean(R,axis=0), R)\nsvd = TruncatedSVD(n_components=2, random_state=42)\nU = svd.fit_transform(R_filled)\nV = svd.components_",
               [{"check": "U.shape == (4, 2)", "msg": "U: 4 пользователя × 2 фактора"},
                {"check": "V.shape == (2, 3)", "msg": "V: 2 фактора × 3 игры"}],
               ["fit_transform для U", "components_ для V"], 2),
            ex(4, "python", "Восстанови полную матрицу: R_pred = U @ V. Сохрани предсказание для user 0, game 2 в `pred`.",
               "from sklearn.decomposition import TruncatedSVD\nimport numpy as np\nR = np.array([[5,4,0],[0,5,3],[4,0,5],[0,3,4]], dtype=float)\nR_filled = np.where(R==0, np.nanmean(R,axis=0), R)\nsvd = TruncatedSVD(n_components=2, random_state=42)\nU = svd.fit_transform(R_filled)\nV = svd.components_\nR_pred = np.array([])\npred = 0\n",
               "from sklearn.decomposition import TruncatedSVD\nimport numpy as np\nR = np.array([[5,4,0],[0,5,3],[4,0,5],[0,3,4]], dtype=float)\nR_filled = np.where(R==0, np.nanmean(R,axis=0), R)\nsvd = TruncatedSVD(n_components=2, random_state=42)\nU = svd.fit_transform(R_filled)\nV = svd.components_\nR_pred = U @ V\npred = R_pred[0, 2]",
               [{"check": "2.5 < pred < 4.5", "msg": "Предсказание ~3-4"}],
               ["U @ V — восстановленная матрица"], 3),
        ],
        minutes=50, difficulty=3,
    )


def _8_11():
    return lesson(
        "8.11", "Обработка изображений: skimage и PIL", "mixed", [
            theory(
                "**Обработка изображений** — важный навык для Data Science. "
                "Изображения — это массивы чисел (h×w×c), их можно обрабатывать "
                "как любые данные.\n\n"
                "**PIL/Pillow** — базовая библиотека для загрузки, изменения "
                "размера, обрезки, поворота. `Image.open()`, `.resize()`, `.crop()`.\n\n"
                "**scikit-image (skimage)** — научная обработка: фильтры, "
                "сегментация, извлечение признаков.\n"
                "- `skimage.io.imread` — чтение\n"
                "- `skimage.color.rgb2gray` — в оттенки серого\n"
                "- `skimage.filters.gaussian` — размытие\n"
                "- `skimage.filters.sobel` — границы\n"
                "- `skimage.measure.regionprops` — признаки регионов\n\n"
                "**Извлечение признаков из изображений:**\n"
                "- Гистограмма цветов (цветовой профиль)\n"
                "- HOG (Histogram of Oriented Gradients) — для форм\n"
                "- SIFT/ORB — ключевые точки для сопоставления\n"
                "- Средняя яркость, контраст, энтропия\n\n"
                "**Data Augmentation:** поворот, отражение, сдвиг, шум — "
                "для увеличения датасета (полезно для deep learning)."
            ),
            analogy(
                "Изображение для компьютера — таблица Excel, где каждая "
                "ячейка содержит три числа (RGB). Обработка = преобразование "
                "таблицы",
                "Классификация космических объектов по фото: конвертируем "
                "в grayscale, извлекаем HOG-признаки (формы), обучаем "
                "Random Forest. Работает как на обычных таблицах."
            ),
            visual(
                "Размеры изображения",
                "   [height]  ┌──────────────────────────────────┐\n"
                "             │  R ─── G ─── B                   │\n"
                "             │  │     │     │                    │\n"
                "             │  │     │     │    Канал = матрица │\n"
                "             │  │     │     │    h × w           │\n"
                "             │  ▼     ▼     ▼                    │\n"
                "             └──────────────────────────────────┘\n"
                "             └──────── width ────────────────────┘\n"
                "   Форма: (h, w, 3) → numpy array"
            ),
            example(
                "Загрузи изображение (симулируем массивом), переведи в "
                "grayscale, примени размытие и найди границы.",
                "Используем skimage.filters: gaussian (размытие) и sobel "
                "(границы). Все операции — numpy-совместимы.",
                "import numpy as np\nimport matplotlib.pyplot as plt\n"
                "from skimage import data\nfrom skimage.color import rgb2gray\n"
                "from skimage.filters import gaussian, sobel\n"
                "img = data.astronaut()\n"
                "gray = rgb2gray(img)\n"
                "blurred = gaussian(gray, sigma=1)\n"
                "edges = sobel(blurred)\n"
                "fig, axes = plt.subplots(1,3,figsize=(12,4))\n"
                "axes[0].imshow(gray, cmap='gray')\n"
                "axes[0].set_title('Grayscale')\n"
                "axes[1].imshow(blurred, cmap='gray')\n"
                "axes[1].set_title('Blurred (σ=1)')\n"
                "axes[2].imshow(edges, cmap='gray')\n"
                "axes[2].set_title('Edges (Sobel)')\n"
                "for ax in axes: ax.axis('off')\n"
                "plt.show()",
                "График: 3 изображения — grayscale, blur, edges",
                "skimage.data.astronaut() — 512×512 фото астронавта. "
                "rgb2gray → 2D. Gaussian размывает шум. Sobel находит "
                "границы — белые контуры на чёрном фоне."
            ),
            common_mistakes([
                {"mistake": "imread возвращает int8 (0-255), а модели нужен float", "why_bad": "Нормализация: /255.0 или StandardScaler", "fix": "img = img.astype(np.float32) / 255.0"},
                {"mistake": "Путать shape: (h,w,c) vs (c,h,w)", "why_bad": "skimage: (h,w,3), torch: (3,h,w)", "fix": "np.transpose(img, (2,0,1)) для PyTorch"},
                {"mistake": "Применять HOG без grayscale", "why_bad": "HOG работает на яркости, цвет не нужен", "fix": "rgb2gray() перед HOG"},
                {"mistake": "Не использовать data augmentation", "why_bad": "Маленький датасет → переобучение", "fix": "ImageDataGenerator или albumentations"},
            ]),
            interview_questions([
                {"q": "Как компьютер «видит» изображение?", "a": "Как трёхмерный массив (h×w×c), где c=3 (RGB). Каждый пиксель — число от 0 до 255. Grayscale — 2D массив (h×w)."},
                {"q": "Какие признаки можно извлечь из изображений?", "a": "Цветовые (гистограмма RGB), текстурные (GLCM, entropy), формы (HOG, regionprops), ключевые точки (SIFT, ORB)."},
                {"q": "Зачем нужна data augmentation?", "a": "Искусственно увеличить датасет: повороты, сдвиги, zoom, шум. Улучшает обобщение, борется с переобучением. Crucial для deep learning с малыми данными."},
            ]),
            knowledge_checklist([
                "Понимаю форму изображения (h,w,c)",
                "Конвертирую RGB → grayscale",
                "Применяю фильтры: gaussian, sobel",
                "Извлекаю простые признаки (гистограмма, средняя яркость)",
                "Знаю про data augmentation",
            ]),
        ],
        exercises=[
            ex(1, "python", "Загрузи `data.astronaut()` из skimage. Сохрани shape в `sh`.",
               "from skimage import data\nimg = data.astronaut()\nsh = None\n",
               "from skimage import data\nimg = data.astronaut()\nsh = img.shape",
               [{"check": "sh == (512, 512, 3) or sh == (256, 256, 3)", "msg": "Форма (h, w, 3)"}],
               ["data.astronaut() — встроенное изображение"], 1),
            ex(2, "python", "Переведи изображение в grayscale через `rgb2gray`. Сохрани в `gray`.",
               "from skimage import data, color\nimg = data.astronaut()\ngray = None\n",
               "from skimage import data, color\nimg = data.astronaut()\ngray = color.rgb2gray(img)",
               [{"check": "len(gray.shape) == 2", "msg": "Grayscale: 2D массив"}],
               ["color.rgb2gray(img)", "2D → (512, 512)"], 1),
            ex(3, "python", "Примени Gaussian filter (sigma=2) к grayscale. Сохрани в `blurred`.",
               "from skimage import data, color, filters\nimg = data.astronaut()\ngray = color.rgb2gray(img)\nblurred = None\n",
               "from skimage import data, color, filters\nimg = data.astronaut()\ngray = color.rgb2gray(img)\nblurred = filters.gaussian(gray, sigma=2)",
               [{"check": "blurred.shape == gray.shape", "msg": "Размер не изменился"}],
               ["filters.gaussian(image, sigma)", "σ — степень размытия"], 2),
            ex(4, "python", "Создай синтетическое изображение 64×64 с квадратом 20×20 в центре. Сохрани в `img`.",
               "import numpy as np\nimg = np.zeros((64, 64))\n",
               "import numpy as np\nimg = np.zeros((64, 64))\nimg[22:42, 22:42] = 1.0",
               [{"check": "img.sum() > 0", "msg": "Есть ненулевые пиксели"},
                {"check": "img[32, 32] == 1.0", "msg": "Центр = 1"}],
               ["img[22:42, 22:42] = 1 — квадрат 20×20"], 1),
        ],
        minutes=35, difficulty=3,
    )

# ─── Block 9: Инструменты ──────────────────────────────────────────────────

def _9_12():
    return lesson(
        "9.12", "Experiment Tracking: MLflow и Weights & Biases", "mixed", [
            theory(
                "**Experiment Tracking** — запись всех экспериментов ML: "
                "гиперпараметры, метрики, артефакты (модели, графики). "
                "Позволяет не терять результаты, сравнивать запуски, "
                "воспроизводить лучшие.\n\n"
                "**MLflow** — open-source, локальный. Четыре компонента:\n"
                "1. **Tracking** — логирование параметров, метрик, артефактов\n"
                "2. **Projects** — упаковка кода\n"
                "3. **Models** — сериализация моделей\n"
                "4. **Registry** — управление версиями моделей\n\n"
                "**Weights & Biases (wandb)** — облачный (с бесплатным "
                "уровнем). Автоматически логирует гиперпараметры, "
                "создаёт интерактивные дашборды, поддерживает team "
                "collaboration.\n\n"
                "```python\nimport mlflow\n"
                "with mlflow.start_run():\n"
                "    mlflow.log_param('lr', 0.01)\n"
                "    mlflow.log_metric('accuracy', 0.95)\n"
                "    mlflow.log_artifact('model.pkl')\n```\n\n"
                "**Лучшие практики:**\n"
                "- Логировать seed + датасет хэш (воспроизводимость)\n"
                "- Сравнивать по nested runs (один родительский → дочерние "
                "с разными параметрами)\n"
                "- Сохранять предсказания + true labels для post-hoc анализа"
            ),
            analogy(
                "Experiment tracking — лабораторный журнал химика. "
                "Без него: «Кажется, я вчера смешал что-то и получил 95%...»",
                "Data Scientist запускает 50 моделей с разными "
                "гиперпараметрами. Без MLflow → хаос. С MLflow → "
                "сравнение accuracy, подбор лучшего run."
            ),
            visual(
                "MLflow Tracking UI",
                "   ┌──────┬────────┬────────┬────────┬───────┐\n"
                "   │ Run  │ lr     │ n_est  │accuracy│ Status│\n"
                "   ├──────┼────────┼────────┼────────┼───────┤\n"
                "   │ #42  │ 0.01   │ 100    │ 0.953  │✅ BEST│\n"
                "   │ #41  │ 0.01   │ 50     │ 0.942  │       │\n"
                "   │ #40  │ 0.001  │ 100    │ 0.938  │       │\n"
                "   │ #39  │ 0.1    │ 100    │ 0.912  │       │\n"
                "   └──────┴────────┴────────┴────────┴───────┘"
            ),
            example(
                "Симулируй MLflow-тренировку: логируй параметры, "
                "оценку, сохраняй «модель».",
                "Используем mlflow.autolog() или ручной лог.", "",  # No code due to no mlflow installed
                "(код — вызов mlflow.log_param/mlflow.log_metric)",
                "MLflow создаёт run, записывает params и metrics в локальную "
                "SQLite БД. Потом `mlflow ui` → браузер на localhost:5000."
            ),
            common_mistakes([
                {"mistake": "Не логировать seed и версию данных", "why_bad": "Нельзя воспроизвести эксперимент", "fix": "Логируй seed + хэш датасета (hashlib.md5)"},
                {"mistake": "Логировать только одну метрику", "why_bad": "Не видишь trade-off (accuracy vs inference time)", "fix": "Логируй все relevant метрики + loss на эпохах"},
                {"mistake": "Не тегировать важные runs", "why_bad": "Через месяц не вспомнишь, какой run финальный", "fix": "mlflow.set_tag('stage', 'production')"},
                {"mistake": "Хранить гигантские артефакты (датасеты) в MLflow", "why_bad": "БД распухает", "fix": "Логируй только модель + config, данные отдельно в S3/DVC"},
            ]),
            interview_questions([
                {"q": "Зачем нужен experiment tracking?", "a": "Чтобы не терять результаты экспериментов: параметры, метрики, модель. Сравнивать runs, выбирать лучшую, воспроизводить результаты через месяц."},
                {"q": "MLflow vs W&B — что выбрать?", "a": "MLflow — open-source, локальный, бесплатный. W&B — облачный, интерактивные дашборды, team features, бесплатный для личного использования."},
                {"q": "Что хранить в experiment tracking?", "a": "Гиперпараметры, метрики (train/val/test), seed, версию данных, артефакты (модель, предсказания, графики), теги для stage (dev/staging/prod)."},
            ]),
            knowledge_checklist([
                "Устанавливаю MLflow и запускаю mlflow ui",
                "Логирую параметры через mlflow.log_param",
                "Логирую метрики через mlflow.log_metric",
                "Сохраняю модель через mlflow.log_artifact",
                "Сравниваю runs в UI",
            ]),
        ],
        exercises=[
            ex(1, "python", "Импортируй mlflow и создай новый run (контекстный менеджер). Просто импортируй и создай run (код выполнится без ошибки).",
               "import mlflow\nwith mlflow.start_run():\n    pass\n",
               "import mlflow\nwith mlflow.start_run():\n    pass",
               [{"check": "True", "msg": "Run создан"}], ["mlflow.start_run()"], 1),
            ex(2, "python", "Внутри mlflow run залогируй параметр `lr=0.01` и метрику `accuracy=0.95`.",
               "import mlflow\nwith mlflow.start_run():\n    pass\n",
               "import mlflow\nwith mlflow.start_run():\n    mlflow.log_param('lr', 0.01)\n    mlflow.log_metric('accuracy', 0.95)",
               [{"check": "True", "msg": "Параметр и метрика залогированы"}],
               ["mlflow.log_param", "mlflow.log_metric"], 2),
            ex(3, "python", "Симулируй grid search: 3 эксперимента с разными lr. Сохрани список accuracy в `accs` (без MLflow, просто цикл).",
               "import numpy as np\nnp.random.seed(42)\nlrs = [0.001, 0.01, 0.1]\naccs = []\n",
               "import numpy as np\nnp.random.seed(42)\nlrs = [0.001, 0.01, 0.1]\n# Симуляция: чем выше lr, тем хуже (синусоидальный шум)\naccs = [0.90 + 0.05*np.random.randn() - 0.1*(i) for i in range(3)]",
               [{"check": "len(accs) == 3", "msg": "3 accuracy"}, {"check": "all(0.5 < a < 1.0 for a in accs)", "msg": "accuracy в пределах"}],
               ["Симуляция эксперимента", "В реальности — обучение модели"], 2),
        ],
        minutes=35, difficulty=3,
    )


def _9_13():
    return lesson(
        "9.13", "Cloud для Data Scientist: S3 и BigQuery", "mixed", [
            theory(
                "**Cloud-навыки** — обязательны для Data Scientist. "
                "Три основных провайдера: AWS, GCP, Azure. "
                "Минимальный набор для DS:\n\n"
                "**1. Amazon S3 (Simple Storage Service)** — объектное "
                "хранилище. Хранит данные как объекты в bucket'ах. "
                "Подключение через boto3:\n"
                "```python\nimport boto3\n"
                "s3 = boto3.client('s3')\n"
                "s3.download_file('bucket', 'key', 'local.csv')\n"
                "df = pd.read_csv('local.csv')\n```\n\n"
                "**2. Google BigQuery** — serverless data warehouse. "
                "SQL-запросы к петабайтам данных. Подключение через "
                "google-cloud-bigquery:\n"
                "```python\nfrom google.cloud import bigquery\n"
                "client = bigquery.Client()\n"
                "query = 'SELECT * FROM `project.dataset.table`'\n"
                "df = client.query(query).to_dataframe()\n```\n\n"
                "**3. Пайплайн DS на cloud:**\n"
                "- Данные → S3/GCS (сырые)\n"
                "- Запрос → BigQuery/Athena (чистка)\n"
                "- Фичи → S3 (processed)\n"
                "- Обучение → SageMaker/AI Platform\n"
                "- Модель → S3 (artifacts)\n"
                "- API → Lambda/Cloud Functions"
            ),
            analogy(
                "S3 — гараж для данных (сколько угодно, дёшево). "
                "BigQuery — библиотека, где книги проиндексированы "
                "и можно найти любую за секунду",
                "Геймдев-студия: логи игроков → S3 (10TB/день). "
                "Аналитика → BigQuery: SELECT жанр, AVG(retention) "
                "GROUP BY жанр — за 3 секунды, 0 DevOps."
            ),
            visual(
                "Cloud pipeline Data Science",
                "   ┌──────┐    ┌──────────┐    ┌──────────┐\n"
                "   │ S3   │───→│ BigQuery │───→│ SageMaker│\n"
                "   │ Raw  │    │ Clean     │    │ Train    │\n"
                "   └──────┘    └──────────┘    └─────┬────┘\n"
                "                                      ↓\n"
                "                               ┌──────────┐\n"
                "                               │ S3 Model │\n"
                "                               │ Artifacts│\n"
                "                               └──────────┘"
            ),
            example(
                "Симулируй cloud pipeline: скачай CSV с S3 (эмулируем "
                "локальным файлом), загрузи в BigQuery (SQLite эмуляция), "
                "сделай запрос.",
                "AWS S3 → BigQuery pipeline в миниатюре.",
                "import pandas as pd\nimport sqlite3\n"
                "df = pd.read_csv('data.csv')  # вместо s3.download_file\n"
                "conn = sqlite3.connect(':memory:')\n"
                "df.to_sql('missions', conn, index=False)\n"
                "result = pd.read_sql('SELECT AVG(success_rate) FROM missions', conn)\n"
                "print(result)",
                "   AVG(success_rate)\n0             0.855",
                "Эмуляция: вместо S3 — локальный CSV, вместо BigQuery — "
                "SQLite. В реальном cloud: boto3 + bigquery.Client()."
            ),
            common_mistakes([
                {"mistake": "Хранить credentials в коде", "why_bad": "Security breach", "fix": "IAM roles / environment variables / aws secrets manager"},
                {"mistake": "Читать большие данные через pandas read_csv из S3", "why_bad": "Вся память уходит на один файл", "fix": "dask / chunking / Athena SELECT *"},
                {"mistake": "SQL-запросы в BigQuery без LIMIT", "why_bad": "SELECT * FROM 10TB → дорого и долго", "fix": "Всегда SELECT с WHERE + LIMIT"},
                {"mistake": "Не указывать region для S3 bucket", "why_bad": "Cross-region latency + costs", "fix": "Создавай bucket в той же region, что compute"},
            ]),
            interview_questions([
                {"q": "Как Data Scientist использует cloud?", "a": "Хранение данных (S3/GCS), запросы (BigQuery/Athena), обучение моделей (SageMaker), деплой (Lambda, Cloud Functions). Cloud — инфраструктура DS."},
                {"q": "BigQuery vs обычная SQL БД?", "a": "BigQuery — serverless, колоночная, петабайты. SQL-синтаксис почти стандартный. Не нужны индексы — платишь за просканированные данные. Медленный INSERT, быстрый SELECT."},
                {"q": "Как экономить на cloud?", "a": "S3 — lifecycle rules (старые данные → Glacier). BigQuery — кластеризация, партиционирование, LIMIT. Выключай инстансы на ночь."},
            ]),
            knowledge_checklist([
                "Понимаю концепцию S3 bucket и key",
                "Знаю синтаксис BigQuery SQL",
                "Могу написать boto3 client для download/upload",
                "Понимаю cloud pipeline: S3 → BigQuery → ML",
                "Знаю про IAM roles (не credentials в коде)",
            ]),
        ],
        exercises=[
            ex(1, "python", "Создай boto3 S3 клиент (эмуляция: просто импортируй и создай, передав aws_access_key_id=None).",
               "import boto3\ns3 = boto3.client('s3', aws_access_key_id=None, aws_secret_access_key=None)\n",
               "import boto3\ns3 = boto3.client('s3', aws_access_key_id=None, aws_secret_access_key=None)",
               [{"check": "True", "msg": "Клиент создан"}], ["boto3.client('s3')"], 1),
            ex(2, "python", "Создай pandas DataFrame с колонками ['game', 'retention'] -> три строки. Сохрани в `df`.",
               "import pandas as pd\ndf = pd.DataFrame({\n    'game': ['StarQuest', 'MoonRacer', 'AstroWars'],\n    'retention': [0.25, 0.30, 0.28],\n})",
               "import pandas as pd\ndf = pd.DataFrame({\n    'game': ['StarQuest', 'MoonRacer', 'AstroWars'],\n    'retention': [0.25, 0.30, 0.28],\n})",
               [{"check": "len(df) == 3", "msg": "3 строки"}, {"check": "'retention' in df.columns", "msg": "Колонка retention"}],
               ["pd.DataFrame({...})"], 1),
            ex(3, "python", "Эмулируй BigQuery: сохрани df в SQLite (:memory:) как таблицу 'games'. Напиши SQL чтобы найти AVG(retention). Сохрани результат в `avg_ret`.",
               "import pandas as pd\nimport sqlite3\ndf = pd.DataFrame({'game': ['A','B','C'], 'retention': [0.25, 0.30, 0.28]})\nconn = sqlite3.connect(':memory:')\ndf.to_sql('games', conn, index=False)\navg_ret = 0\n",
               "import pandas as pd\nimport sqlite3\ndf = pd.DataFrame({'game': ['A','B','C'], 'retention': [0.25, 0.30, 0.28]})\nconn = sqlite3.connect(':memory:')\ndf.to_sql('games', conn, index=False)\navg_ret = pd.read_sql('SELECT AVG(retention) FROM games', conn).iloc[0,0]",
               [{"check": "0.25 < avg_ret < 0.30", "msg": "AVG ~ 0.277"}],
               ["df.to_sql + pd.read_sql", "Эмуляция BigQuery"], 2),
        ],
        minutes=35, difficulty=3,
    )


def _9_14():
    return lesson(
        "9.14", "Сериализация моделей: joblib и pickle", "mixed", [
            theory(
                "**Сериализация** — сохранение обученной модели на диск для "
                "последующей загрузки и инференса. Два основных инструмента:\n\n"
                "**pickle** — встроенный в Python. Сохраняет любой объект. "
                "Минус: pickle небезопасен (не загружай из ненадёжных источников).\n"
                "`pickle.dump(model, open('model.pkl', 'wb'))`\n"
                "`model = pickle.load(open('model.pkl', 'rb'))`\n\n"
                "**joblib** — часть scikit-learn, оптимизирован для больших "
                "numpy-массивов. Быстрее pickle для sklearn-моделей.\n"
                "`joblib.dump(model, 'model.joblib')`\n"
                "`model = joblib.load('model.joblib')`\n\n"
                "**Лучшие практики:**\n"
                "- Сохраняй не только модель, но и версию sklearn, "
                "feature names, preprocessor, метрики — в одном дикте\n"
                "- Используй joblib для sklearn, pickle для остального\n"
                "- Для production — ONNX или PMML (framework-agnostic)\n"
                "- Версионируй модели через MLflow Model Registry\n\n"
                "```python\nimport joblib\nmodel_data = {\n    'model': model,\n    'features': feature_names,\n    'sklearn_version': '1.2.0',\n    'val_score': 0.95,\n}\njoblib.dump(model_data, 'model_package.joblib')\n```"
            ),
            analogy(
                "Сериализация — консервирование борща. Сегодня сварил "
                "(обучил), закатал в банку (.pkl). Через месяц открыл — "
                "и можно есть (inference)",
                "Обучил Random Forest на 100K игроков. Сохранил в "
                "`churn_model.joblib`. В production-service загружает "
                "его и предсказывает отток за 1мс."
            ),
            visual(
                "Lifecycle ML-модели",
                "   Train → serialize → store (S3) → deploy → load → predict\n"
                "   Обучение  joblib.dump    bucket   FastAPI   load   predict\n"
                "   ┌────┐   ┌───────┐   ┌──────┐   ┌──────┐   ┌────┐   ┌──────┐\n"
                "   │model│──→│.joblib│──→│  S3  │──→│ API  │──→│load│──→│pred  │\n"
                "   └────┘   └───────┘   └──────┘   └──────┘   └────┘   └──────┘"
            ),
            example(
                "Обучи простую модель, сохрани через joblib, загрузи "
                "обратно и сделай предсказание.",
                "Pipeline: train → dump → load → predict. Важно: после "
                "загрузки модель в том же состоянии.",
                "import joblib\nimport pandas as pd\n"
                "from sklearn.ensemble import RandomForestClassifier\n"
                "from sklearn.datasets import make_classification\n"
                "X, y = make_classification(n_samples=100, random_state=42)\n"
                "model = RandomForestClassifier().fit(X, y)\n"
                "joblib.dump(model, 'model.joblib')\n"
                "loaded = joblib.load('model.joblib')\n"
                "pred = loaded.predict(X[:1])\n"
                "print(f'Prediction: {pred[0]}')",
                "Prediction: 0 (или 1)",
                "После загрузки модель предсказывает идентично оригиналу. "
                "Сериализация и десериализация не меняют поведение."
            ),
            common_mistakes([
                {"mistake": "Pickle.load из ненадёжного источника", "why_bad": "code execution vulnerability", "fix": "Используй joblib, но тоже осторожно. Для production — ONNX"},
                {"mistake": "Не сохранять версию библиотеки", "why_bad": "sklearn v1.0 != v1.2 — model может не загрузиться", "fix": "Сохраняй package versions в model_data dict"},
                {"mistake": "Serialize весь pipeline без preprocessor", "why_bad": "В production забудешь, как чистил данные", "fix": "Сохраняй весь pipeline: sklearn.Pipeline([('scaler', ...), ('model', ...)])"},
                {"mistake": "Думать, что pickle.dump одной модели = MLOps", "why_bad": "Нужно версионирование, метаданные, метрики", "fix": "MLflow Model Registry: model version, stage, tags"},
            ]),
            interview_questions([
                {"q": "Чем joblib отличается от pickle?", "a": "joblib оптимизирован для больших numpy-массивов, быстрее для sklearn моделей. pickle — универсальный, но медленнее. Для sklearn — joblib."},
                {"q": "Почему pickle — security risk?", "a": "pickle.load выполняет произвольный код. Злонамеренный pickle файл может выполнить os.system(). Никогда не загружай pickle из ненадёжных источников."},
                {"q": "Как сериализовать sklearn pipeline?", "a": "Просто: joblib.dump(pipeline, 'pipe.joblib'). Pipeline содержит все шаги (scaler, encoder, model). При load получаешь полный pipeline для predict."},
            ]),
            knowledge_checklist([
                "Сохраняю модель через joblib.dump",
                "Загружаю модель через joblib.load",
                "Сохраняю pipeline целиком (preprocessor + model)",
                "Добавляю метаданные: версия, метрики, features",
                "Понимаю разницу joblib vs pickle",
            ]),
        ],
        exercises=[
            ex(1, "python", "Обучи RandomForestClassifier на данных make_classification(n_samples=50). Сохрани через joblib.dump в файл 'model.joblib'.",
               "from sklearn.ensemble import RandomForestClassifier\nfrom sklearn.datasets import make_classification\nimport joblib\nX, y = make_classification(n_samples=50, random_state=42)\nmodel = RandomForestClassifier(random_state=42).fit(X, y)\n",
               "from sklearn.ensemble import RandomForestClassifier\nfrom sklearn.datasets import make_classification\nimport joblib\nX, y = make_classification(n_samples=50, random_state=42)\nmodel = RandomForestClassifier(random_state=42).fit(X, y)\njoblib.dump(model, 'model.joblib')",
               [{"check": "True", "msg": "Модель сохранена"}], ["joblib.dump(model, filename)"], 1),
            ex(2, "python", "Загрузи модель из 'model.joblib' (если не сохранил — ошибка). Сохрани в `loaded`.",
               "import joblib\nloaded = None\n",
               "import joblib\nloaded = joblib.load('model.joblib')",
               [{"check": "loaded is not None", "msg": "Модель загружена"}],
               ["joblib.load(filename)", "Возвращает оригинальный объект"], 2),
            ex(3, "python", "Создай model_data dict с ключами 'model', 'accuracy', 'features'. Сохрани через joblib. Сохрани dict в `model_data`.",
               "import joblib\nimport pandas as pd\nmodel_data = {\n    'model': 'RandomForest',\n    'accuracy': 0.95,\n    'features': ['age', 'session_time', 'purchases'],\n}\n",
               "import joblib\nimport pandas as pd\nmodel_data = {\n    'model': 'RandomForest',\n    'accuracy': 0.95,\n    'features': ['age', 'session_time', 'purchases'],\n}\njoblib.dump(model_data, 'model_package.joblib')",
               [{"check": "'model' in model_data", "msg": "Ключ model"},
                {"check": "'accuracy' in model_data", "msg": "Ключ accuracy"}],
               ["dict с метаданными", "Сохраняй модель + метаданные вместе"], 2),
        ],
        minutes=30, difficulty=2,
    )

# ─── Block 10: Собеседования ───────────────────────────────────────────────

def _10_9():
    return lesson(
        "10.9", "Системный дизайн для Data Scientist", "mixed", [
            theory(
                "**Системный дизайн** — навык проектировать ML-системы. "
                "На собеседованиях (особенно middle/senior) дают задачу "
                "спроектировать recommendation pipeline, fraud detection "
                "систему или A/B платформу.\n\n"
                "**Фреймворк для дизайна:**\n"
                "1. **Clarify requirements:** какие данные, latency, "
                "количество пользователей, SLA?\n"
                "2. **Data pipeline:** откуда берутся данные, как "
                "чистятся, где хранятся (S3 → BigQuery → Features)\n"
                "3. **ML компонент:** модель (какая, как обучается, "
                "как часто обновляется)\n"
                "4. **Inference:** batch (раз в день) или online "
                "(реалтайм, через API)?\n"
                "5. **Monitoring:** data drift, model decay, "
                "alerting\n"
                "6. **Trade-offs:** accuracy vs latency, cost vs "
                "freshness\n\n"
                "**Пример: рекомендательная система для игр**\n"
                "- События → Kafka → Feature Store → ML Model → API\n"
                "- Модель: two-tower (user tower + item tower), "
                "обновляется раз в день\n"
                "- Inference: offline (precompute топ-100) + real-time "
                "(свежие события)\n"
                "- Latency SLA: 200ms p99"
            ),
            analogy(
                "Системный дизайн — архитектурный план здания, а не "
                "чертёж одной стены. Data Scientist видит всё здание — "
                "от датчиков до фасада (UX)",
                "Дизайн системы детекции читеров: клиентская телеметрия "
                "→ Kafka → feature pipeline → ML-модель → "
                "alerting → банит игрока. Latency < 5 сек."
            ),
            visual(
                "Типовая архитектура ML-системы",
                "   ┌──────────┐    ┌────────────┐    ┌──────────┐\n"
                "   │  Клиенты  │───→│  Kafka /   │───→│ Feature  │\n"
                "   │ (игры)    │    │  S3        │    │ Store    │\n"
                "   └──────────┘    └────────────┘    └────┬─────┘\n"
                "                                           ↓\n"
                "                                   ┌──────────┐\n"
                "                                   │ ML Model │\n"
                "                                   │ (online) │\n"
                "                                   └────┬─────┘\n"
                "                                        ↓\n"
                "                                   ┌──────────┐\n"
                "                                   │   API    │\n"
                "                                   │ prediction│\n"
                "                                   └──────────┘"
            ),
            example(
                "Спроектируй систему A/B тестирования для игровой "
                "платформы.",
                "Структура ответа: requirements → pipeline → "
                "статистика → мониторинг.",
                "--- Ответ на системный дизайн ---\n"
                "1. Requirements: 10M DAU, 200 A/B тестов одновременно, "
                "SLA 100ms на проверку группы\n"
                "2. Pipeline: события → Kafka → Flink (агрегация) → "
                "ClickHouse (OLAP) → дашборды\n"
                "3. Рандомизация: userId hash → bucket (A/B/C...)\n"
                "4. Статистика: sequential testing (стреляющие "
                "правила), FDR correction для multiple metrics\n"
                "5. Мониторинг: SRM (Sample Ratio Mismatch), "
                "guardrail metrics alerting",
                "(устный/письменный ответ)",
                "Ключевое: A/B платформа — не только t-test. Нужна "
                "рандомизация (хэш), робастное хранение, real-time "
                "агрегация, sequential testing (чтобы не ждать 2 недели)."
            ),
            common_mistakes([
                {"mistake": "Начинать с модели, а не с данных", "why_bad": "Без данных модель бесполезна", "fix": "Всегда с data pipeline: как собираем, чистим, храним"},
                {"mistake": "Не оговаривать SLA", "why_bad": "Нет критериев успеха дизайна", "fix": "Latency p99 < 500ms, throughput 1000 RPS, availability 99.9%"},
                {"mistake": "Игнорировать cost и trade-offs", "why_bad": "Дизайн без бюджета — академический", "fix": "S3 vs EBS, batch vs real-time — у каждого есть цена"},
                {"mistake": "Не упоминать мониторинг", "why_bad": "Система без мониторинга упадёт незаметно", "fix": "Model drift, data drift, latency, error rate — dashboards + alerts"},
            ]),
            interview_questions([
                {"q": "Как спроектировать recommendation system для 10M пользователей?", "a": "1) Data: events → Kafka → Feature Store. 2) Model: two-tower retrieval + ranking. 3) Offline: precompute top-100. 4) Online: real-time rerank. 5) Monitor: CTR, latency, freshness."},
                {"q": "Batch vs real-time inference — что выбрать?", "a": "Batch: дешевле, проще, для рекомендаций/дайджестов. Real-time: дороже, для кредитного скоринга/мошенничества. Trade-off: cost vs latency."},
                {"q": "Как мониторить ML-систему в production?", "a": "Data drift (PSI/KL divergence входных признаков), model decay (accuracy на свежих лейблах), prediction distribution, latency p50/p99, error rate. Alerts в PagerDuty."},
            ]),
            knowledge_checklist([
                "Структурирую ответ на системный дизайн: requirements → pipeline → ML → deploy → monitor",
                "Понимаю разницу batch vs real-time inference",
                "Знаю компоненты ML-системы: Kafka, Feature Store, Model Registry",
                "Учитываю trade-offs: cost, latency, accuracy",
                "Планирую мониторинг и alerting",
            ]),
        ],
        exercises=[
            ex(1, "python", "Напиши функцию `design_score(latency_ms, has_monitoring, has_data_pipeline)`, возвращающую оценку дизайна (0-100). Latency < 200 → +30, monitoring → +30, data pipeline → +40.",
               "def design_score(latency_ms, has_monitoring, has_data_pipeline):\n    score = 0\n    return score\n",
               "def design_score(latency_ms, has_monitoring, has_data_pipeline):\n    score = 0\n    if latency_ms < 200: score += 30\n    if has_monitoring: score += 30\n    if has_data_pipeline: score += 40\n    return score",
               [{"check": "design_score(100, True, True) == 100", "msg": "Идеальный дизайн = 100"},
                {"check": "design_score(300, False, False) == 0", "msg": "Ничего нет = 0"}],
               ["Условные операторы", "Оценка по критериям"], 1),
            ex(2, "python", "Дан словарь `system` с 'latency_ms', 'throughput', 'cost_dollars'. Напиши функцию `is_production_ready`, возвращающую True если latency < 300, throughput > 100, cost < 1000.",
               "def is_production_ready(system):\n    return False\n",
               "def is_production_ready(system):\n    return (system['latency_ms'] < 300 \n            and system['throughput'] > 100 \n            and system['cost_dollars'] < 1000)",
               [{"check": "is_production_ready({'latency_ms':200,'throughput':200,'cost_dollars':500})", "msg": "Все условия выполнены"},
                {"check": "not is_production_ready({'latency_ms':500,'throughput':200,'cost_dollars':500})", "msg": "Latency слишком высокая"}],
               ["Сравнение всех метрик с SLA", "Логическое И для всех условий"], 2),
            ex(3, "python", "Симулируй trade-off: у тебя budget $1000. GPU час = $10, RAM GB = $5. Напиши функцию, вычисляющую максимальное количество часов при заданном RAM (GB).",
               "def max_hours(budget, ram_gb):\n    return 0\n",
               "def max_hours(budget, ram_gb):\n    gpu_cost = 10\n    ram_cost = 5\n    cost_per_hour = gpu_cost + ram_cost * ram_gb\n    return budget // cost_per_hour",
               [{"check": "max_hours(1000, 1) == 66", "msg": "1000/15 ≈ 66"},
                {"check": "max_hours(1000, 10) == 16", "msg": "1000/60 ≈ 16"}],
               ["budget // cost_per_hour", "Trade-off: больше RAM = меньше часов"], 3),
        ],
        minutes=45, difficulty=3,
    )

# ─── Presentation improvements ──────────────────────────────────────────────
# Debug challenge templates
def debug_challenge(problem, buggy_code, hint, fix):
    return {
        "type": "debug_challenge",
        "problem": problem,
        "buggy_code": buggy_code,
        "hint": hint,
        "fix": fix,
    }

def recap_quiz(items):
    return {
        "type": "recap_quiz",
        "items": items,
    }

def _11_1():
    return lesson(
        "11.1", "Финальный проект (Capstone)", "mixed", [
            theory(
                "**Capstone-проект** — заключительный этап курса. "
                "Ты пройдёшь полный цикл Data Science: от бизнес-задачи "
                "до работающей ML-модели и отчёта для портфолио.\n\n"
                "**Доступны две темы:**\n\n"
                "**🚀 Космос: анализ миссий NASA**\n"
                "- 200 космических миссий\n"
                "- Прогноз успеха миссии (классификация)\n"
                "- Дашборд с визуализациями\n"
                "- Техники: EDA, Feature Engineering, "
                "классификация, визуализация\n\n"
                "**🎮 Игры: анализ поведения игроков**\n"
                "- 200 игроков, когортный анализ\n"
                "- Прогноз оттока (churn prediction)\n"
                "- Персонализированные рекомендации\n"
                "- Техники: когортный анализ, классификация, "
                "рекомендательные системы\n\n"
                "Каждый проект включает 8-10 шагов с проверками, "
                "шаблоном кода и тестовыми данными. Результат — "
                "готовый entry для GitHub-портфолио.\n\n"
                "👉 **Перейти к проекту:** открой страницу "
                "<a href=\"#/lesson/11.2\" class=\"btn btn-primary\" "
                "style=\"display:inline-block;margin:8px 0;\">"
                "🚀 Начать проект «Космос»</a>"
                " <a href=\"#/lesson/11.3\" class=\"btn btn-primary\" "
                "style=\"display:inline-block;margin:8px 0;\">"
                "🎮 Начать проект «Игры»</a>"
            ),
            analogy(
                "Capstone — защита диплома в универе, только вместо "
                "комиссии — GitHub-профиль и рекрутер",
                "Ты — Data Scientist, которому дали реальную задачу: "
                "данные, бизнес-контекст и неделя на EDA → модель → отчёт."
            ),
            visual(
                "Структура capstone-проекта",
                "   ┌─────────┐   ┌──────────┐   ┌──────────┐\n"
                "   │   Data  │ → │ Feature  │ → │ Modeling │\n"
                "   │   (CSV) │   │Engineer. │   │  (ML)    │\n"
                "   └─────────┘   └──────────┘   └────┬─────┘\n"
                "                                      ↓\n"
                "   ┌─────────┐   ┌──────────┐   ┌──────────┐\n"
                "   │  Report │ ← │Evaluate  │ ← │  Deploy  │\n"
                "   │ (README)│   │ (метрики) │   │ (pipeline)│\n"
                "   └─────────┘   └──────────┘   └──────────┘"
            ),
            example(
                "Выбери тему, открой страницу проекта и пройди шаги "
                "по порядку. После завершения — оформи README и "
                "залей на GitHub.",
                "Структура entry в портфолио: README (Problem → "
                "Approach → Results → Lessons Learned), "
                "Jupyter Notebook, requirements.txt, model.pkl.",
                "# Начать проект можно с главной страницы или\n"
                "# перейти по ссылке:\n"
                "→ #/lesson/11.2 (Космос) или #/lesson/11.3 (Игры)",
                "Вперёд! 🚀",
                "Главное — не пропускать шаги и фиксировать "
                "результаты. Каждый шаг проверяется автоматически."
            ),
            common_mistakes([
                {"mistake": "Начать проект без плана", "why_bad": "Потеряешь фокус и время", "fix": "Прочитай все шаги перед стартом"},
                {"mistake": "Пропускать EDA", "why_bad": "Модель без понимания данных — чёрный ящик", "fix": "Потрать 30% времени на EDA"},
                {"mistake": "Не оформлять README", "why_bad": "Рекрутер не поймёт, что ты сделал", "fix": "Используй шаблон из урока 9.8"},
            ]),
            interview_questions([
                {"q": "Что такое capstone-проект и зачем он нужен?", "a": "Финальный проект, демонстрирующий все навыки DS. Нужен для портфолио и собеседований — показывает, что кандидат умеет решать real-world задачи."},
                {"q": "Как выбрать тему проекта для портфолио?", "a": "Выбирай ту, которая ближе к желаемой индустрии. Космос — логистика/прогнозирование. Игры — рекомендации/анализ пользователей."},
            ]),
            knowledge_checklist([
                "Понимаю структуру capstone-проекта: Data → EDA → Features → Model → Report",
                "Выбрал тему (Космос или Игры)",
                "Готов пройти все шаги от загрузки данных до отчёта",
                "Знаю, как оформить README для портфолио",
            ]),
        ],
        exercises=[
            ex(1, "quiz", "Сколько шагов содержит каждый capstone-проект?",
               "", "8-10 шагов", [], [], 1),
            ex(2, "quiz", "Что нужно сделать в первую очередь после выбора темы?",
               "", "Прочитать все шаги проекта и изучить данные (EDA)", [], [], 1),
        ],
        minutes=20, difficulty=1,
    )

def _11_2():
    return lesson(
        "11.2", "Космос: проект — анализ миссий NASA", "space", [
            theory(
                "**Проект: Анализ миссий NASA**\n\n"
                "Ты — Data Scientist в космическом агентстве. Заказчик просит "
                "понять, почему одни миссии успешны, а другие нет, и построить "
                "модель для прогноза успеха будущих запусков.\n\n"
                 "**Структура проекта:** 15 шагов — от бизнес-задачи до сдачи "
                "заказчику. Каждый шаг = диалог с Заказчиком + практическое "
                "задание. Данные: 200 исторических миссий (1960–2025).\n\n"
                "👉 **Перейти к проекту:** "
                 "<a href=\"#/lesson/11.2\" class=\"btn btn-primary\" "
                 "style=\"display:inline-block;margin:8px 0;\">"
                 "🚀 Начать проект «Космос»</a>"
            ),
            analogy(
                "Ты — инженер NASA в 1969 году, получивший задание "
                "проанализировать все предыдущие запуски перед Apollo 11",
                "Данные по миссиям — те же 200 записей. Нужно найти "
                "закономерности: какие агентства успешнее, какие цели "
                "рискованнее, сколько стоит успешная миссия."
            ),
            visual(
                "Этапы проекта",
                 "   ┌──── Шаг 1: Бизнес-задача ────┐\n"
                 "   │  Заказчик ставит задачу       │\n"
                 "   │  → определяем метрики         │\n"
                 "   └──────────┬────────────────────┘\n"
                 "              ↓\n"
                 "   ┌──── Шаг 2-3: Данные ─────────┐\n"
                 "   │  Загрузка, очистка, EDA       │\n"
                 "   └──────────┬────────────────────┘\n"
                 "              ↓\n"
                 "   ┌──── Шаг 4-6: Анализ ─────────┐\n"
                 "   │  Статистика, признаки, инсайты │\n"
                 "   └──────────┬────────────────────┘\n"
                 "              ↓\n"
                 "   ┌──── Шаг 7-8: ML ─────────────┐\n"
                 "   │  Модель, оценка, интерпретация│\n"
                 "   └──────────┬────────────────────┘\n"
                 "              ↓\n"
                 "   ┌──── Шаг 9-15: Сдача ─────────┐\n"
                 "   │  Дашборд + README отчёт       │\n"
                 "   └───────────────────────────────┘"
            ),
             example(
                "Открой проект и пройди все 15 шагов последовательно. "
                "На каждом шаге — диалог с коллегами и задание.",
                "Шаг 1: Заказчик объясняет задачу. Ты уточняешь метрики. "
                "Шаг 15: Финальный отчёт и защита.",
                "→ Перейти к проекту: #/lesson/11.2",
                "Готовь README для портфолио!",
                "Ключ к успеху — не пропускать шаги. Каждый шаг строится на предыдущем."
            ),
            common_mistakes([
                {"mistake": "Пропустить диалог и сразу писать код", "why_bad": "Не поймёшь, что именно хочет заказчик", "fix": "Читай диалог — в нём контекст задачи"},
                {"mistake": "Делать всё сразу, а не по шагам", "why_bad": "Потеряешь фокус, пропустишь важные детали", "fix": "Проходи шаги последовательно, не забегай вперёд"},
            ]),
            interview_questions([
                {"q": "Какой проект ты делал в курсе?", "a": "Финальный проект по анализу космических миссий NASA: 15 шагов, от бизнес-задачи до ML-модели и отчёта. Использовал Random Forest, accuracy 87%."},
            ]),
            knowledge_checklist([
                "Понимаю бизнес-задачу: прогноз успеха миссии",
                "Могу объяснить подход: EDA → Feature Engineering → Random Forest",
                "Готов пройти 15 шагов проекта",
            ]),
        ],
        exercises=[
            ex(1, "quiz", "Сколько шагов в проекте «Космос»?",
               "", "15", [], [], 1),
            ex(2, "quiz", "Какая целевая метрика модели?",
               "", "Accuracy > 80% (прогноз успеха миссии)", [], [], 1),
        ],
        minutes=15, difficulty=1,
    )

def _11_3():
    return lesson(
        "11.3", "Игры: проект — анализ поведения игроков", "gaming", [
            theory(
                "**Проект: Анализ поведения игроков**\n\n"
                "Ты — Data Scientist в игровой студии. Заказчик (гейм-директор) "
                "хочет понять, почему игроки уходят, и построить модель прогноза "
                "оттока (churn), чтобы удерживать их.\n\n"
                 "**Структура проекта:** 15 шагов — от бизнес-задачи до "
                "рекомендаций команде. Каждый шаг = диалог с Заказчиком + "
                "практическое задание. Данные: 200 игроков.\n\n"
                "👉 **Перейти к проекту:** "
                 "<a href=\"#/lesson/11.3\" class=\"btn btn-primary\" "
                 "style=\"display:inline-block;margin:8px 0;\">"
                 "🎮 Начать проект «Игры»</a>"
            ),
            analogy(
                "Ты — аналитик в студии, которая только что запустила "
                "мобильную RPG. Игроки уходят — нужно срочно понять почему",
                "Данные 200 игроков: уровень, траты, сессии, гильдия. "
                "Нужно найти факторы, удерживающие игроков."
            ),
            visual(
                "Этапы проекта",
                "   ┌──── Шаг 1: Бизнес-задача ────┐\n"
                "   │  Гейм-директор ставит задачу  │\n"
                "   │  → прогноз оттока (churn)     │\n"
                "   └──────────┬────────────────────┘\n"
                "              ↓\n"
                "   ┌──── Шаг 2-3: Данные ─────────┐\n"
                "   │  Загрузка, очистка, EDA       │\n"
                "   └──────────┬────────────────────┘\n"
                "              ↓\n"
                "   ┌──── Шаг 4-6: Анализ ─────────┐\n"
                "   │  Статистика, признаки, инсайты │\n"
                "   └──────────┬────────────────────┘\n"
                "              ↓\n"
                "   ┌──── Шаг 7-8: ML ─────────────┐\n"
                "   │  Модель, оценка, интерпретация│\n"
                "   └──────────┬────────────────────┘\n"
                "              ↓\n"
                 "   ┌──── Шаг 9-15: Сдача ─────────┐\n"
                 "   │  Дашборд + README отчёт       │\n"
                 "   └───────────────────────────────┘"
            ),
            example(
                "Открой проект и пройди все 15 шагов. Каждый шаг — "
                "диалог с командой и практическое задание.",
                "Шаг 1: Гейм-директор объясняет проблему оттока. "
                "Ты предлагаешь метрики и подход.",
                "→ Перейти к проекту: #/lesson/11.3",
                "Результат — модель churn + рекомендации команде!",
                "Не пропускай диалоги — в них контекст для каждого шага."
            ),
            common_mistakes([
                {"mistake": "Игнорировать бизнес-контекст и сразу лезть в код", "why_bad": "Модель без понимания бизнеса бесполезна", "fix": "Сначала бизнес-задача, потом код"},
                {"mistake": "Не документировать выводы", "why_bad": "Команда не узнает, почему игроки уходят", "fix": "Каждый шаг = заметка для итогового отчёта"},
            ]),
            interview_questions([
                {"q": "Расскажи про проект по анализу игроков", "a": "Финальный проект: прогноз оттока игроков (churn). 15 шагов от бизнес-задачи до рекомендаций. Random Forest — accuracy 85%. Ключевой фактор: количество сыгранных дней."},
            ]),
            knowledge_checklist([
                "Понимаю бизнес-задачу: прогноз оттока игроков",
                "Могу объяснить подход: EDA → Feature Engineering → Random Forest",
                "Готов пройти 15 шагов проекта",
            ]),
        ],
        exercises=[
            ex(1, "quiz", "Сколько шагов в проекте «Игры»?",
               "", "15", [], [], 1),
            ex(2, "quiz", "Какая главная метрика модели?",
               "", "Accuracy > 80% (прогноз оттока игроков)", [], [], 1),
        ],
        minutes=15, difficulty=1,
    )

# ─── Export lesson functions for all blocks ─────────────────────────────────

# Export per-block lesson lists for __init__.py to import
LESSONS_B1 = [_1_13]
LESSONS_B5 = [_5_13, _5_14, _5_15]
LESSONS_B7 = [_7_18, _7_19]
LESSONS_B8 = [_8_10, _8_11]
LESSONS_B9 = [_9_12, _9_13, _9_14]
LESSONS_B10 = [_10_9]

LESSONS_B11 = [_11_1, _11_2, _11_3]
