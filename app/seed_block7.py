"""
Блок 7: Машинное обучение.
14 уроков, ~125 упражнений.
Темы: типы ML, train/test, переобучение, метрики, регрессия, классификация,
деревья, ансамбли, кластеризация, интерпретация, выбор модели, мини-проект.
"""
from app.seed_helpers import (
    ex, lesson, theory, analogy, visual, example,
    common_mistakes, interview_questions, knowledge_checklist,
)


def _7_1():
    return lesson(
        "7.1", "Типы ML: supervised, unsupervised, reinforcement", "mixed", [
            theory(
                "**Машинное обучение (ML)** — алгоритмы учатся на данных. Три типа:\n\n"
                "**1. Supervised** — есть пары (X, y). Подзадачи:\n"
                "- **Регрессия** — y непрерывный (KDR, цена скина)\n"
                "- **Классификация** — y категориальный (win/lose, роль)\n"
                "Примеры: линейная/логистическая регрессия, дерево, Random Forest, XGBoost.\n\n"
                "**2. Unsupervised** — только X, меток нет. Ищем структуру:\n"
                "- **Кластеризация** — K-Means, DBSCAN (группировка игроков)\n"
                "- **Dimensionality reduction** — PCA, t-SNE\n"
                "- **Anomaly detection** — Isolation Forest (читеры)\n\n"
                "**3. Reinforcement learning** — агент действует, получает награды, "
                "учится стратегии. Примеры: AlphaGo, OpenAI Five. Самый ресурсоёмкий.\n\n"
                "**Где что применять:** есть метки → supervised; только фичи → "
                "unsupervised; последовательность решений с отложенной наградой → RL."
            ),
            analogy(
                "Supervised — ученик с репетитором. Unsupervised — турист без карты "
                "замечает похожие кварталы. RL — игрок учится через пробы и ошибки.",
                "В Dota: predict win/lose — supervised. Сегментация игроков — "
                "unsupervised. Бот OpenAI Five — RL."
            ),
            visual(
                "Три типа ML",
                "   ┌──────────────────────────────────────────────────┐\n"
                "   │           МАШИННОЕ ОБУЧЕНИЕ                      │\n"
                "   └─────┬────────────────┬──────────────────┬────────┘\n"
                "         ↓                ↓                  ↓\n"
                "   ┌──────────┐    ┌────────────┐    ┌──────────────┐\n"
                "   │Supervised│    │Unsupervised│    │Reinforcement │\n"
                "   │  (X, y)  │    │    (X)     │    │state, reward │\n"
                "   │Регрессия │    │Кластеринг  │    │Q-learning    │\n"
                "   │Классиф-я │    │PCA, t-SNE  │    │Policy Grad   │\n"
                "   └──────────┘    └────────────┘    └──────────────┘"
            ),
            example(
                "Supervised-датасет: 2 кластера по 100 точек.",
                "Создаём два «кластера» с разными средними и метками 0/1.",
                "import numpy as np\n"
                "np.random.seed(42)\n"
                "X = np.vstack([np.random.normal([2,2], 1, (100,2)), np.random.normal([6,6], 1, (100,2))])\n"
                "y = np.array([0]*100 + [1]*100)\n"
                "print('X:', X.shape, 'y:', y.shape)\n"
                "print('Class 0 mean:', X[y==0].mean(axis=0))",
                "X: (200, 2) y: (200,)\nClass 0 mean: [2. 2.]",
                "200 объектов, у класса 0 среднее (2, 2), у класса 1 — (6, 6). "
                "Любая модель классификации разделит их прямой."
            ),
            common_mistakes([
                {"mistake": "Supervised-метод без меток", "why_bad": "Нет y — нечего предсказывать", "fix": "K-Means или PCA"},
                {"mistake": "Путать кластеризацию с классификацией", "why_bad": "Кластеры не имеют истинных меток", "fix": "Номера кластеров ≠ истинные классы"},
                {"mistake": "RL там, где хватит supervised", "why_bad": "RL дорогой и сложный", "fix": "Если есть ответы — supervised"},
                {"mistake": "Unsupervised «умнее» supervised", "why_bad": "Просто разные задачи", "fix": "Выбирай тип по наличию меток"},
            ]),
            interview_questions([
                {"q": "Чем supervised отличается от unsupervised?", "a": "Supervised: есть (X, y), учим X→y. Unsupervised: только X, ищем структуру. Пример supervised — спам-классификация, unsupervised — сегментация клиентов."},
                {"q": "Когда применять RL?", "a": "Когда задача — последовательность решений с отложенной наградой (игра, робот, трейдинг). Нужны миллионы эпизодов."},
                {"q": "Пример unsupervised в геймдеве?", "a": "Сегментация игроков по стилю (K-Means на hours, kills, deaths, winrate). Обнаружение читеров (Isolation Forest)."},
            ]),
            knowledge_checklist([
                "Знаю 3 типа ML и их отличия",
                "Различаю регрессию и классификацию",
                "Привожу пример unsupervised-задачи",
                "Понимаю, что такое RL и где применять",
                "Могу выбрать тип ML под задачу",
            ]),
        ],
        exercises=[
            ex(1, "python", "Сгенерируй supervised-датасет: 2 кластера по 50 точек (mean=[0,0] и mean=[5,5]), seed=42. Сохрани X (100,2) и y (100,) в `X, y`.",
               "import numpy as np\nX = np.array([])\ny = np.array([])\n",
               "import numpy as np\nnp.random.seed(42)\nX0 = np.random.normal(0, 1, (50, 2))\nX1 = np.random.normal(5, 1, (50, 2))\nX = np.vstack([X0, X1])\ny = np.array([0]*50 + [1]*50)",
               [{"check": "X.shape == (100, 2)", "msg": "100 строк, 2 фичи"},
                {"check": "set(y.tolist()) == {0, 1}", "msg": "Два класса"}],
               ["np.vstack", "y — массив меток"], 1),
            ex(2, "python", "Сохрани долю класса 1 в `ratio`.",
               "import numpy as np\ny = np.array([0]*50 + [1]*50)\nratio = 0\n",
               "import numpy as np\ny = np.array([0]*50 + [1]*50)\nratio = y.mean()",
               [{"check": "ratio == 0.5", "msg": "50/50 баланс"}],
               ["y.mean() для бинарных = доля 1"], 1),
            ex(3, "python", "Сгенерируй unsupervised-датасет: 150 точек из 3 кластеров (mean=[0,0], [5,5], [10,0]), seed=42. Сохрани в `X`.",
               "import numpy as np\nX = np.array([])\n",
               "import numpy as np\nnp.random.seed(42)\nc1 = np.random.normal([0, 0], 1, (50, 2))\nc2 = np.random.normal([5, 5], 1, (50, 2))\nc3 = np.random.normal([10, 0], 1, (50, 2))\nX = np.vstack([c1, c2, c3])",
               [{"check": "X.shape == (150, 2)", "msg": "150 точек"}],
               ["3 vstacked кластера"], 2),
            ex(4, "python", "Создай словарь `tasks`: regression→'predict KDR', classification→'predict win', clustering→'group players', anomaly→'find cheaters'.",
               "tasks = {}\n",
               "tasks = {\n    'regression': 'predict KDR',\n    'classification': 'predict win',\n    'clustering': 'group players',\n    'anomaly': 'find cheaters'\n}",
               [{"check": "'regression' in tasks", "msg": "regression есть"},
                {"check": "len(tasks) == 4", "msg": "4 задачи"}],
               ["dict literal"], 1),
            ex(5, "python", "Создай `has_labels` = True (supervised).",
               "has_labels = False\n",
               "has_labels = True",
               [{"check": "has_labels is True", "msg": "True для supervised"}],
               ["boolean"], 1),
            ex(6, "python", "Создай список `ml_types` из 3 строк.",
               "ml_types = []\n",
               "ml_types = ['supervised', 'unsupervised', 'reinforcement']",
               [{"check": "len(ml_types) == 3", "msg": "3 типа"},
                {"check": "'reinforcement' in ml_types", "msg": "RL включён"}],
               ["list literal"], 1),
            ex(7, "python", "Сгенерируй X (200, 1) из U(0, 10), seed=42.",
               "import numpy as np\nX = np.array([])\n",
               "import numpy as np\nnp.random.seed(42)\nX = np.random.uniform(0, 10, (200, 1))",
               [{"check": "X.shape == (200, 1)", "msg": "200 строк, 1 фича"}],
               ["np.random.uniform"], 1),
            ex(8, "python", "Создай y = 3*X + 5 + шум N(0,1), seed=42. Сохрани в `y`.",
               "import numpy as np\nnp.random.seed(42)\nX = np.random.uniform(0, 10, (200, 1))\ny = np.array([])\n",
               "import numpy as np\nnp.random.seed(42)\nX = np.random.uniform(0, 10, (200, 1))\ny = 3 * X.flatten() + 5 + np.random.randn(200)",
               [{"check": "y.shape == (200,)", "msg": "200 значений"},
                {"check": "abs(y.mean() - 20) < 5", "msg": "Среднее y ≈ 20"}],
               ["y = 3x + 5 + noise"], 2),
        ],
        minutes=40, difficulty=2,
    )


def _7_2():
    return lesson(
        "7.2", "Train/Test Split и кросс-валидация", "mixed", [
            theory(
                "Чтобы оценить качество модели на новых данных, делим датасет на "
                "**train** (для обучения) и **test** (для оценки). Без этого мы "
                "переоценим качество — модель «видела» те же данные.\n\n"
                "**Пропорции:** 70/30, 80/20, 90/10. Больше данных — больше в train. "
                "Для маленьких выборок (<1000) часто используют кросс-валидацию.\n\n"
                "**Stratified split:** при дисбалансе классов — стратификация для "
                "сохранения пропорций: `train_test_split(X, y, stratify=y)`.\n\n"
                "**Random seed** важен: `random_state=42` гарантирует воспроизводимость. "
                "Без него каждый запуск даёт другой split.\n\n"
                "**Кросс-валидация (k-fold):** делим на k частей, обучаем k раз. "
                "Среднее по k метрик — устойчивая оценка. k=5 или k=10 — стандарт.\n\n"
                "**Ошибки:**\n"
                "1. **Data leakage** — fit StandardScaler на всём X до split\n"
                "2. **Перемешивание временных рядов** — TimeSeriesSplit\n"
                "3. **Маленький test** — шумные метрики"
            ),
            analogy(
                "Train/test — экзамен после курса. CV — 10 пробных экзаменов, "
                "средний балл точнее одного.",
                "В Dota: train на январских матчах, test на февральских — проверяем "
                "обобщение."
            ),
            visual(
                "Split и 5-fold CV",
                "   Один split (80/20):\n"
                "   ┌─────────────────────────┬────────┐\n"
                "   │        TRAIN 80%        │ TEST 20│\n"
                "   └─────────────────────────┴────────┘\n"
                "\n"
                "   5-fold CV:\n"
                "   ┌──┬──┬──┬──┬──┐  iter 1: train[1-4], test[0]\n"
                "   │ 4│ 3│ 2│ 1│ 0│  iter 2: train[0,2,3,4], test[1]\n"
                "   │  │  │  │  │  │  ...\n"
                "   └──┴──┴──┴──┴──┘  усредняем 5 метрик"
            ),
            example(
                "Раздели данные, обучи LinearRegression, оцени.",
                "Используем `train_test_split` из sklearn.",
                "import numpy as np\n"
                "from sklearn.model_selection import train_test_split\n"
                "from sklearn.linear_model import LinearRegression\n"
                "np.random.seed(42)\n"
                "X = np.random.uniform(0, 10, (100, 1))\n"
                "y = 2 * X.flatten() + 1 + np.random.randn(100)\n"
                "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n"
                "model = LinearRegression().fit(X_train, y_train)\n"
                "print(f'Train R^2: {model.score(X_train, y_train):.3f}')\n"
                "print(f'Test R^2:  {model.score(X_test, y_test):.3f}')",
                "Train R^2: 0.940\nTest R^2:  0.954",
                "R² на test (0.954) близок к train (0.940) — модель не переобучена, "
                "хорошо обобщается."
            ),
            common_mistakes([
                {"mistake": "fit StandardScaler на X до split", "why_bad": "Test 'утекает' в train", "fix": "fit на train, transform на test"},
                {"mistake": "shuffle=True для временных рядов", "why_bad": "Test 'видит будущее'", "fix": "TimeSeriesSplit"},
                {"mistake": "Не фиксировать random_state", "why_bad": "Метрики 'прыгают'", "fix": "Всегда random_state=42"},
                {"mistake": "Test < 100 примеров", "why_bad": "Шумная метрика", "fix": "Минимум 10% от датасета"},
            ]),
            interview_questions([
                {"q": "Зачем train/test split?", "a": "Оценить качество на новых данных. Без split модель переобучается. Train — обучение, test — честная оценка."},
                {"q": "Что такое кросс-валидация?", "a": "k-fold CV: делим на k частей, k раз обучаем на k-1 и проверяем на оставшейся. Среднее — устойчивая оценка. Для тюнинга гиперпараметров."},
                {"q": "Что такое data leakage?", "a": "Утечка данных из test в train. fit нормализатора на всём X, target в фичах. Модель выглядит отлично, в проде ломается."},
            ]),
            knowledge_checklist([
                "Делаю train_test_split",
                "Фиксирую random_state",
                "Использую stratify при дисбалансе",
                "Понимаю k-fold CV",
                "Избегаю data leakage",
                "Применяю cross_val_score",
            ]),
        ],
        exercises=[
            ex(1, "python", "Сгенерируй X (100, 2) и y (100,) — два класса по 50 точек, seed=42.",
               "import numpy as np\nX = np.array([])\ny = np.array([])\n",
               "import numpy as np\nnp.random.seed(42)\nX = np.vstack([np.random.normal(0, 1, (50, 2)), np.random.normal(5, 1, (50, 2))])\ny = np.array([0]*50 + [1]*50)",
               [{"check": "X.shape == (100, 2)", "msg": "100 точек"},
                {"check": "y.shape == (100,)", "msg": "100 меток"}],
               ["np.vstack"], 1),
            ex(2, "python", "Раздели 80/20, random_state=42, stratify=y. Сохрани `X_train, X_test, y_train, y_test`.",
               "import numpy as np\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX = np.vstack([np.random.normal(0, 1, (50, 2)), np.random.normal(5, 1, (50, 2))])\ny = np.array([0]*50 + [1]*50)\n",
               "import numpy as np\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX = np.vstack([np.random.normal(0, 1, (50, 2)), np.random.normal(5, 1, (50, 2))])\ny = np.array([0]*50 + [1]*50)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)",
               [{"check": "len(X_train) == 80", "msg": "80 train"},
                {"check": "len(X_test) == 20", "msg": "20 test"}],
               ["test_size=0.2", "stratify=y"], 2),
            ex(3, "python", "k-fold CV (k=5) на LogisticRegression, среднее в `cv_score`.",
               "import numpy as np\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.model_selection import cross_val_score\nnp.random.seed(42)\nX = np.vstack([np.random.normal(0, 1, (50, 2)), np.random.normal(5, 1, (50, 2))])\ny = np.array([0]*50 + [1]*50)\ncv_score = 0\n",
               "import numpy as np\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.model_selection import cross_val_score\nnp.random.seed(42)\nX = np.vstack([np.random.normal(0, 1, (50, 2)), np.random.normal(5, 1, (50, 2))])\ny = np.array([0]*50 + [1]*50)\nscores = cross_val_score(LogisticRegression(), X, y, cv=5)\ncv_score = scores.mean()",
               [{"check": "0.7 < cv_score < 1.0", "msg": "CV score > 0.7"},
                {"check": "isinstance(cv_score, float)", "msg": "float"}],
               ["cross_val_score(model, X, y, cv=5)"], 2),
            ex(4, "python", "Раздели 70/30, random_state=0, БЕЗ stratify.",
               "import numpy as np\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX = np.vstack([np.random.normal(0, 1, (50, 2)), np.random.normal(5, 1, (50, 2))])\ny = np.array([0]*50 + [1]*50)\n",
               "import numpy as np\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX = np.vstack([np.random.normal(0, 1, (50, 2)), np.random.normal(5, 1, (50, 2))])\ny = np.array([0]*50 + [1]*50)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)",
               [{"check": "len(X_train) == 70", "msg": "70 train"},
                {"check": "len(X_test) == 30", "msg": "30 test"}],
               ["test_size=0.3"], 1),
            ex(5, "python", "После split (80/20, stratify=y) посчитай долю класса 1 в y_test, сохрани в `test_ratio`.",
               "import numpy as np\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX = np.vstack([np.random.normal(0, 1, (50, 2)), np.random.normal(5, 1, (50, 2))])\ny = np.array([0]*50 + [1]*50)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\ntest_ratio = 0\n",
               "import numpy as np\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX = np.vstack([np.random.normal(0, 1, (50, 2)), np.random.normal(5, 1, (50, 2))])\ny = np.array([0]*50 + [1]*50)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\ntest_ratio = y_test.mean()",
               [{"check": "test_ratio == 0.5", "msg": "Стратификация сохранила 50/50"}],
               ["y_test.mean()"], 2),
            ex(6, "python", "Сгенерируй X (200, 3), y=(X[:,0]+X[:,1]>0). CV с cv=10, сохрани в `scores`.",
               "import numpy as np\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.model_selection import cross_val_score\nnp.random.seed(42)\nX = np.random.randn(200, 3)\ny = (X[:, 0] + X[:, 1] > 0).astype(int)\nscores = np.array([])\n",
               "import numpy as np\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.model_selection import cross_val_score\nnp.random.seed(42)\nX = np.random.randn(200, 3)\ny = (X[:, 0] + X[:, 1] > 0).astype(int)\nscores = cross_val_score(LogisticRegression(), X, y, cv=10)",
               [{"check": "scores.shape == (10,)", "msg": "10 фолдов"}],
               ["cv=10"], 2),
            ex(7, "python", "Раздели 90/10, random_state=42. Размер test в `n_test`.",
               "import numpy as np\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX = np.random.randn(100, 5)\ny = np.random.randint(0, 2, 100)\n",
               "import numpy as np\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX = np.random.randn(100, 5)\ny = np.random.randint(0, 2, 100)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)\nn_test = len(X_test)",
               [{"check": "n_test == 10", "msg": "10% от 100 = 10"}],
               ["test_size=0.1"], 1),
            ex(8, "python", "Обучи LogisticRegression, accuracy на test в `test_acc`.",
               "import numpy as np\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX = np.vstack([np.random.normal(0, 1, (50, 2)), np.random.normal(5, 1, (50, 2))])\ny = np.array([0]*50 + [1]*50)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\ntest_acc = 0\n",
               "import numpy as np\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX = np.vstack([np.random.normal(0, 1, (50, 2)), np.random.normal(5, 1, (50, 2))])\ny = np.array([0]*50 + [1]*50)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\nmodel = LogisticRegression().fit(X_train, y_train)\ntest_acc = model.score(X_test, y_test)",
               [{"check": "0.7 < test_acc < 1.0", "msg": "accuracy > 0.7"}],
               ["model.score", "model.fit"], 2),
            ex(9, "python", "|test_acc - cv_score| в `diff`.",
               "import numpy as np\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.model_selection import train_test_split, cross_val_score\nnp.random.seed(42)\nX = np.vstack([np.random.normal(0, 1, (50, 2)), np.random.normal(5, 1, (50, 2))])\ny = np.array([0]*50 + [1]*50)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\nmodel = LogisticRegression()\nmodel.fit(X_train, y_train)\ntest_acc = model.score(X_test, y_test)\ncv_score = cross_val_score(LogisticRegression(), X, y, cv=5).mean()\ndiff = 0\n",
               "import numpy as np\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.model_selection import train_test_split, cross_val_score\nnp.random.seed(42)\nX = np.vstack([np.random.normal(0, 1, (50, 2)), np.random.normal(5, 1, (50, 2))])\ny = np.array([0]*50 + [1]*50)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\nmodel = LogisticRegression()\nmodel.fit(X_train, y_train)\ntest_acc = model.score(X_test, y_test)\ncv_score = cross_val_score(LogisticRegression(), X, y, cv=5).mean()\ndiff = abs(test_acc - cv_score)",
               [{"check": "0 <= diff < 0.2", "msg": "CV и test близки"}],
               ["|x-y|"], 3),
        ],
        minutes=50, difficulty=2,
    )


def _7_6():
    return lesson(
        "7.6", "Линейная регрессия", "mixed", [
            theory(
                "**Линейная регрессия** — простейшая модель для непрерывного y.\n\n"
                "**Модель:** `y_pred = w[0]*x[0] + ... + w[n]*x[n] + b`. "
                "w — веса, b — intercept.\n\n"
                "**Обучение:** минимизируем MSE. Аналитически: OLS через матрицы. "
                "Итеративно: градиентный спуск.\n\n"
                "**В sklearn:** `LinearRegression()`. Атрибуты:\n"
                "- `model.coef_` — массив весов\n"
                "- `model.intercept_` — скаляр\n"
                "- `model.predict(X)`, `model.score(X, y)` = R²\n\n"
                "**Предпосылки:** линейность, нормальность остатков, гомоскедастичность, "
                "нет мультиколлинеарности.\n\n"
                "**Когда:** линейная связь, нужна интерпретируемость, baseline. "
                "**Когда не:** нелинейность, выбросы в y.\n\n"
                "**Регуляризация:** Ridge (L2), Lasso (L1) — штраф за большие w."
            ),
            analogy(
                "Палка в scatter plot: подбираем наклон и высоту, чтобы сумма "
                "расстояний от точек была минимальной.",
                "В Dota: KDR = 0.3*kills + 0.05*gold - 0.4*deaths + b."
            ),
            visual(
                "Подбор прямой",
                "   y │     ●\n"
                "     │   ●╲\n"
                "     │ ●  ╲  ← residual\n"
                "     │     ╲\n"
                "     └─────── x\n"
                "   minimize Σ(y - ŷ)²"
            ),
            example(
                "y = 2x + 1 + шум, 50 точек.",
                "Модель должна выучить w ≈ 2, b ≈ 1.",
                "import numpy as np\n"
                "from sklearn.linear_model import LinearRegression\n"
                "np.random.seed(42)\n"
                "X = np.random.rand(50, 1) * 10\n"
                "y = 2 * X.flatten() + 1 + np.random.randn(50)\n"
                "m = LinearRegression().fit(X, y)\n"
                "print(f'coef={m.coef_[0]:.2f} b={m.intercept_:.2f} R^2={m.score(X, y):.3f}')",
                "coef=1.99 b=1.27 R^2=0.967",
                "Модель отлично выучила: coef ≈ 2, R²=0.967. intercept чуть смещён (шум)."
            ),
            common_mistakes([
                {"mistake": "Забыть reshape в 2D", "why_bad": "sklearn ждёт (n, n_features)", "fix": "X.reshape(-1, 1)"},
                {"mistake": "Путать coef_ и intercept_", "why_bad": "coef_ — массив, intercept_ — скаляр", "fix": "model.coef_[0]"},
                {"mistake": "Линейная модель на нелинейных данных", "why_bad": "High bias", "fix": "Полиномы или другая модель"},
                {"mistake": "Игнорировать масштаб фичей", "why_bad": "coef_ зависят от масштаба", "fix": "StandardScaler"},
            ]),
            interview_questions([
                {"q": "Как работает линейная регрессия?", "a": "Минимизирует MSE: y_pred = X·w + b. Аналитически: w = (XᵀX)⁻¹Xᵀy (OLS). Итеративно: градиентный спуск."},
                {"q": "Зачем регуляризация?", "a": "L2 (Ridge) — большие w, мультиколлинеарность. L1 (Lasso) — обнуляет w, отбор фичей. ElasticNet — комбинация. p >> n."},
                {"q": "Что R² и как интерпретировать?", "a": "R² = 1 - SS_res/SS_tot. Доля объяснённой дисперсии. 1 — идеально, 0 — как среднее, <0 — хуже."},
            ]),
            knowledge_checklist([
                "Обучаю LinearRegression через .fit()",
                "Извлекаю coef_ и intercept_",
                "Предсказываю через .predict()",
                "Считаю R² через .score()",
                "Знаю формулу y = w·x + b",
                "Знаю 4 предпосылки",
            ]),
        ],
        exercises=[
            ex(1, "python", "y = 3x + 5 + шум, 50 точек, seed=42. X (50,1), y (50,).",
               "import numpy as np\nX = np.array([])\ny = np.array([])\n",
               "import numpy as np\nnp.random.seed(42)\nX = np.random.rand(50, 1) * 10\ny = 3 * X.flatten() + 5 + np.random.randn(50)",
               [{"check": "X.shape == (50, 1)", "msg": "50 строк"}],
               ["np.random.rand(50, 1)"], 1),
            ex(2, "python", "Обучи LinearRegression, сохрани в `model`.",
               "import numpy as np\nfrom sklearn.linear_model import LinearRegression\nnp.random.seed(42)\nX = np.random.rand(50, 1) * 10\ny = 3 * X.flatten() + 5 + np.random.randn(50)\nmodel = None\n",
               "import numpy as np\nfrom sklearn.linear_model import LinearRegression\nmodel = LinearRegression().fit(X, y)",
               [{"check": "isinstance(model, LinearRegression)", "msg": "LR"},
                {"check": "hasattr(model, 'coef_')", "msg": "Обучена"}],
               [".fit()"], 1),
            ex(3, "python", "Извлеки coef_ и intercept_ в `coef, intercept`.",
               "import numpy as np\nfrom sklearn.linear_model import LinearRegression\nnp.random.seed(42)\nX = np.random.rand(50, 1) * 10\ny = 3 * X.flatten() + 5 + np.random.randn(50)\nmodel = LinearRegression().fit(X, y)\ncoef = 0\nintercept = 0\n",
               "import numpy as np\nfrom sklearn.linear_model import LinearRegression\nmodel = LinearRegression().fit(X, y)\ncoef = model.coef_[0]\nintercept = model.intercept_",
               [{"check": "abs(coef - 3) < 0.2", "msg": "coef ≈ 3"},
                {"check": "abs(intercept - 5) < 2", "msg": "intercept ≈ 5"}],
               ["model.coef_", "model.intercept_"], 1),
            ex(4, "python", "Предскажи y для X[:5] в `y_pred`.",
               "import numpy as np\nfrom sklearn.linear_model import LinearRegression\nnp.random.seed(42)\nX = np.random.rand(50, 1) * 10\ny = 3 * X.flatten() + 5 + np.random.randn(50)\nmodel = LinearRegression().fit(X, y)\ny_pred = np.array([])\n",
               "import numpy as np\nfrom sklearn.linear_model import LinearRegression\nmodel = LinearRegression().fit(X, y)\ny_pred = model.predict(X[:5])",
               [{"check": "y_pred.shape == (5,)", "msg": "5 предсказаний"}],
               ["model.predict"], 1),
            ex(5, "python", "R² на train в `r2`.",
               "import numpy as np\nfrom sklearn.linear_model import LinearRegression\nnp.random.seed(42)\nX = np.random.rand(50, 1) * 10\ny = 3 * X.flatten() + 5 + np.random.randn(50)\nmodel = LinearRegression().fit(X, y)\nr2 = 0\n",
               "import numpy as np\nfrom sklearn.linear_model import LinearRegression\nr2 = LinearRegression().fit(X, y).score(X, y)",
               [{"check": "r2 > 0.9", "msg": "R² > 0.9"}],
               ["model.score"], 1),
            ex(6, "python", "80/20 split, R² на test в `test_r2`.",
               "import numpy as np\nfrom sklearn.linear_model import LinearRegression\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX = np.random.rand(50, 1) * 10\ny = 3 * X.flatten() + 5 + np.random.randn(50)\ntest_r2 = 0\n",
               "import numpy as np\nfrom sklearn.linear_model import LinearRegression\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\ntest_r2 = LinearRegression().fit(X_train, y_train).score(X_test, y_test)",
               [{"check": "test_r2 > 0.85", "msg": "Test R² > 0.85"}],
               ["train_test_split"], 2),
            ex(7, "python", "3 фичи: y = 2x1 + 0.5x2 - x3 + шум. seed=42, 200 точек. coefs в `coefs`.",
               "import numpy as np\nfrom sklearn.linear_model import LinearRegression\nnp.random.seed(42)\nX = np.random.randn(200, 3)\ny = 2 * X[:, 0] + 0.5 * X[:, 1] - 1 * X[:, 2] + np.random.randn(200) * 0.5\ncoefs = np.array([])\n",
               "import numpy as np\nfrom sklearn.linear_model import LinearRegression\ncoefs = LinearRegression().fit(X, y).coef_",
               [{"check": "coefs.shape == (3,)", "msg": "3 коэффициента"},
                {"check": "abs(coefs[0] - 2) < 0.2", "msg": "coef[0] ≈ 2"},
                {"check": "abs(coefs[2] - (-1)) < 0.2", "msg": "coef[2] ≈ -1"}],
               ["3 фичи"], 2),
            ex(8, "python", "Предсказание на X_new = [[1.5], [3.0], [5.0]] в `y_new`.",
               "import numpy as np\nfrom sklearn.linear_model import LinearRegression\nnp.random.seed(42)\nX = np.random.rand(50, 1) * 10\ny = 3 * X.flatten() + 5 + np.random.randn(50)\nmodel = LinearRegression().fit(X, y)\nX_new = np.array([[1.5], [3.0], [5.0]])\ny_new = np.array([])\n",
               "import numpy as np\nfrom sklearn.linear_model import LinearRegression\nmodel = LinearRegression().fit(X, y)\ny_new = model.predict(X_new)",
               [{"check": "y_new.shape == (3,)", "msg": "3 предсказания"}],
               ["model.predict"], 1),
            ex(9, "python", "MSE на test в `mse`.",
               "import numpy as np\nfrom sklearn.linear_model import LinearRegression\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import mean_squared_error\nnp.random.seed(42)\nX = np.random.rand(50, 1) * 10\ny = 3 * X.flatten() + 5 + np.random.randn(50)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\nmse = 0\n",
               "import numpy as np\nfrom sklearn.linear_model import LinearRegression\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import mean_squared_error\nmodel = LinearRegression().fit(X_train, y_train)\nmse = mean_squared_error(y_test, model.predict(X_test))",
               [{"check": "0 < mse < 5", "msg": "MSE > 0"}],
               ["mean_squared_error"], 2),
        ],
        minutes=50, difficulty=2,
    )


def _7_7():
    return lesson(
        "7.7", "Логистическая регрессия", "mixed", [
            theory(
                "**Логистическая регрессия** — линейная модель для **бинарной "
                "классификации**. Несмотря на «регрессию» — это классификация.\n\n"
                "**Идея:** z = w·x + b, затем сигмоида `σ(z) = 1/(1+exp(-z))`. "
                "`σ(z) ∈ (0, 1)` — вероятность класса 1. Если `σ > 0.5` → класс 1.\n\n"
                "**Loss:** log-loss (cross-entropy). Минимизируется градиентным спуском.\n\n"
                "**В sklearn:** `LogisticRegression()`. L2 по умолчанию.\n"
                "- `model.coef_` — веса\n"
                "- `model.predict(X)` — метки 0/1\n"
                "- `model.predict_proba(X)` — вероятности (n, 2)\n"
                "- `model.score(X, y)` — accuracy\n\n"
                "**Гиперпараметры:**\n"
                "- `C` — обратная сила регуляризации (default 1.0)\n"
                "- `penalty` — 'l1', 'l2', 'elasticnet', 'none'\n"
                "- `solver` — 'lbfgs', 'liblinear', 'saga'\n\n"
                "**Плюсы:** простая, быстрая, интерпретируемая, вероятности. "
                "**Минусы:** только линейные границы, нужны scaled фичи."
            ),
            analogy(
                "Оценщик в банке: считает «score» по анкете, переводит в "
                "«вероятность дефолта» через сигмоиду. > 0.5 — отказ.",
                "В Dota: win_proba = sigmoid(0.3*kills - 0.4*deaths + 0.05*gold + b)."
            ),
            visual(
                "Сигмоида",
                "   σ(z)\n"
                "   1.0 ┤        ╭──\n"
                "       │      ╱\n"
                "   0.5 ┤────●────── ← порог 0.5\n"
                "       │  ╱\n"
                "   0.0 ┤╯\n"
                "       └────── z\n"
                "   y_pred = 1 if σ(z)>0.5 else 0"
            ),
            example(
                "Предскажи win/lose по kills и deaths.",
                "KDR > 0 → победа (с шумом).",
                "import numpy as np\n"
                "from sklearn.linear_model import LogisticRegression\n"
                "np.random.seed(42)\n"
                "n = 200\n"
                "kills = np.random.poisson(5, n)\n"
                "deaths = np.random.poisson(5, n)\n"
                "X = np.column_stack([kills, deaths])\n"
                "y = (kills - deaths > 0).astype(int)\n"
                "m = LogisticRegression().fit(X, y)\n"
                "print('coef:', m.coef_[0], 'acc:', m.score(X, y))",
                "coef: [0.45 -0.51] acc: 0.78",
                "coef[0]=0.45 (kills помогает), coef[1]=-0.51 (deaths мешает). "
                "Accuracy 78%."
            ),
            common_mistakes([
                {"mistake": "predict вместо predict_proba", "why_bad": "predict даёт метки, не вероятности", "fix": "predict_proba для P(class=1)"},
                {"mistake": "Не масштабировать фичи", "why_bad": "L2 штрафует разные масштабы по-разному", "fix": "StandardScaler"},
                {"mistake": "На нелинейных данных", "why_bad": "Линейная граница", "fix": "Полиномы, ядра"},
                {"mistake": "Мало max_iter", "why_bad": "Не сойдётся", "fix": "max_iter=1000"},
            ]),
            interview_questions([
                {"q": "Что такое сигмоида?", "a": "σ(z) = 1/(1+exp(-z)) — (0, 1). Для вероятности класса 1. Производная удобна для GD."},
                {"q": "Logistic vs Linear?", "a": "Linear: непрерывный y, MSE. Logistic: класс 0/1, log-loss. Задачи: регрессия vs классификация."},
                {"q": "Зачем регуляризация?", "a": "Борьба с overfit. L1 — отбор фичей. L2 — стабильность. C — обратная сила."},
            ]),
            knowledge_checklist([
                "Обучаю LogisticRegression",
                "predict_proba для вероятностей",
                "coef_ и intercept_",
                "Роль сигмоиды",
                "C, penalty, solver",
            ]),
        ],
        exercises=[
            ex(1, "python", "Бинарный датасет: 2 кластера по 50 точек, mean=[2,2] и mean=[6,6], seed=42.",
               "import numpy as np\nX = np.array([])\ny = np.array([])\n",
               "import numpy as np\nnp.random.seed(42)\nX = np.vstack([np.random.normal([2,2], 1, (50, 2)), np.random.normal([6,6], 1, (50, 2))])\ny = np.array([0]*50 + [1]*50)",
               [{"check": "X.shape == (100, 2)", "msg": "100 точек"}],
               ["vstack"], 1),
            ex(2, "python", "Обучи LogisticRegression, accuracy в `acc`.",
               "import numpy as np\nfrom sklearn.linear_model import LogisticRegression\nnp.random.seed(42)\nX = np.vstack([np.random.normal([2,2], 1, (50, 2)), np.random.normal([6,6], 1, (50, 2))])\ny = np.array([0]*50 + [1]*50)\nacc = 0\n",
               "import numpy as np\nfrom sklearn.linear_model import LogisticRegression\nacc = LogisticRegression().fit(X, y).score(X, y)",
               [{"check": "acc > 0.9", "msg": "Классы разделимы"}],
               ["model.score"], 1),
            ex(3, "python", "predict_proba для X[:3] в `probs`.",
               "import numpy as np\nfrom sklearn.linear_model import LogisticRegression\nnp.random.seed(42)\nX = np.vstack([np.random.normal([2,2], 1, (50, 2)), np.random.normal([6,6], 1, (50, 2))])\ny = np.array([0]*50 + [1]*50)\nmodel = LogisticRegression().fit(X, y)\nprobs = np.array([])\n",
               "import numpy as np\nfrom sklearn.linear_model import LogisticRegression\nmodel = LogisticRegression().fit(X, y)\nprobs = model.predict_proba(X[:3])",
               [{"check": "probs.shape == (3, 2)", "msg": "3 точки, 2 вер-ти"}],
               ["predict_proba"], 2),
            ex(4, "python", "P(class=1) для первых 5 в `p1`.",
               "import numpy as np\nfrom sklearn.linear_model import LogisticRegression\nnp.random.seed(42)\nX = np.vstack([np.random.normal([2,2], 1, (50, 2)), np.random.normal([6,6], 1, (50, 2))])\ny = np.array([0]*50 + [1]*50)\nmodel = LogisticRegression().fit(X, y)\np1 = np.array([])\n",
               "import numpy as np\nfrom sklearn.linear_model import LogisticRegression\nmodel = LogisticRegression().fit(X, y)\np1 = model.predict_proba(X[:5])[:, 1]",
               [{"check": "p1.shape == (5,)", "msg": "5 вероятностей"},
                {"check": "(p1 >= 0).all() and (p1 <= 1).all()", "msg": "[0, 1]"}],
               ["[:, 1]"], 1),
            ex(5, "python", "predict метки в `y_pred`.",
               "import numpy as np\nfrom sklearn.linear_model import LogisticRegression\nnp.random.seed(42)\nX = np.vstack([np.random.normal([2,2], 1, (50, 2)), np.random.normal([6,6], 1, (50, 2))])\ny = np.array([0]*50 + [1]*50)\nmodel = LogisticRegression().fit(X, y)\ny_pred = np.array([])\n",
               "import numpy as np\nfrom sklearn.linear_model import LogisticRegression\nmodel = LogisticRegression().fit(X, y)\ny_pred = model.predict(X)",
               [{"check": "set(y_pred.tolist()) <= {0, 1}", "msg": "0 и 1"}],
               ["model.predict"], 1),
            ex(6, "python", "coef_ и intercept_ в `coef, intercept`.",
               "import numpy as np\nfrom sklearn.linear_model import LogisticRegression\nnp.random.seed(42)\nX = np.vstack([np.random.normal([2,2], 1, (50, 2)), np.random.normal([6,6], 1, (50, 2))])\ny = np.array([0]*50 + [1]*50)\nmodel = LogisticRegression().fit(X, y)\ncoef = np.array([])\nintercept = 0\n",
               "import numpy as np\nfrom sklearn.linear_model import LogisticRegression\nmodel = LogisticRegression().fit(X, y)\ncoef = model.coef_[0]\nintercept = model.intercept_[0]",
               [{"check": "coef.shape == (2,)", "msg": "2 веса"}],
               ["model.coef_[0]"], 1),
            ex(7, "python", "80/20 split, test accuracy в `test_acc`.",
               "import numpy as np\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX = np.vstack([np.random.normal([2,2], 1, (50, 2)), np.random.normal([6,6], 1, (50, 2))])\ny = np.array([0]*50 + [1]*50)\ntest_acc = 0\n",
               "import numpy as np\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\ntest_acc = LogisticRegression().fit(X_train, y_train).score(X_test, y_test)",
               [{"check": "0.7 < test_acc <= 1.0", "msg": "Test > 0.7"}],
               ["stratify=y"], 2),
            ex(8, "python", "C=100 и C=0.01. (acc_high, acc_low) на test.",
               "import numpy as np\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX = np.vstack([np.random.normal([2,2], 1, (50, 2)), np.random.normal([6,6], 1, (50, 2))])\ny = np.array([0]*50 + [1]*50)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\nacc_high = 0\nacc_low = 0\n",
               "import numpy as np\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\nacc_high = LogisticRegression(C=100).fit(X_train, y_train).score(X_test, y_test)\nacc_low = LogisticRegression(C=0.01).fit(X_train, y_train).score(X_test, y_test)",
               [{"check": "0.5 < acc_high <= 1.0", "msg": "C=100 OK"}],
               ["C — обратная сила регуляризации"], 3),
            ex(9, "python", "Сигмоида вручную: σ(0) = 0.5. Сохрани в `s0`.",
               "import numpy as np\ns0 = 0\n",
               "import numpy as np\ns0 = 1 / (1 + np.exp(0))",
               [{"check": "abs(s0 - 0.5) < 1e-9", "msg": "σ(0) = 0.5"}],
               ["σ(z) = 1/(1+e^-z)"], 2),
        ],
        minutes=50, difficulty=2,
    )



def _7_4():
    return lesson(
        "7.4", "Метрики регрессии: MAE, MSE, RMSE, R²", "mixed", [
            theory(
                "**Метрики регрессии** оценивают, насколько `ŷ` отличается от `y`.\n\n"
                "**MAE** = (1/n) * Σ|y - ŷ|. В единицах y, устойчива к выбросам.\n\n"
                "**MSE** = (1/n) * Σ(y - ŷ)². Квадрат → штрафует большие ошибки.\n\n"
                "**RMSE** = sqrt(MSE). В единицах y, самая популярная.\n\n"
                "**R²** = 1 - SS_res/SS_tot:\n"
                "- R² = 1 — идеально\n"
                "- R² = 0 — как среднее\n"
                "- R² < 0 — хуже среднего\n\n"
                "**Когда что:**\n"
                "- **MAE** — нужна робастность (доходы)\n"
                "- **RMSE** — большие ошибки критичны (KDR, время)\n"
                "- **R²** — сравнение моделей на разных данных\n"
                "- **MSE** — для loss-функции (дифференцируемость)"
            ),
            analogy(
                "MAE — среднее время в пути. RMSE — пробки в худшем случае (авария "
                "сильно увеличивает). R² — насколько навигатор объясняет реальность.",
                "KDR: MAE=2.0 → ошибаемся на 2. RMSE=4.0 → иногда сильно (новичок с 0)."
            ),
            visual(
                "Residuals",
                "   y │  ●\n"
                "     │● │ŷ\n"
                "     └─x\n"
                "   MAE = mean|residual|    MSE = mean(residual²)\n"
                "   RMSE = sqrt(MSE)        R² = 1 - SS_res/SS_tot"
            ),
            example(
                "Посчитай MAE, MSE, RMSE, R².",
                "y_true + шум = y_pred, считаем 4 метрики.",
                "import numpy as np\n"
                "from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error\n"
                "y_true = np.array([3.0, 5.0, 2.5, 7.0, 4.0])\n"
                "y_pred = y_true + np.array([0.5, -0.3, 0.2, 0.8, -0.1])\n"
                "print('MAE :', mean_absolute_error(y_true, y_pred))\n"
                "print('RMSE:', np.sqrt(mean_squared_error(y_true, y_pred)))\n"
                "print('R^2 :', r2_score(y_true, y_pred))",
                "MAE : 0.38\nRMSE: 0.454\nR^2 : 0.86",
                "MAE=0.38 — средняя ошибка. R²=0.86 — модель объясняет 86% дисперсии y."
            ),
            common_mistakes([
                {"mistake": "Accuracy для регрессии", "why_bad": "Accuracy — для классификации", "fix": "MAE/MSE/RMSE/R²"},
                {"mistake": "Путать MSE и RMSE", "why_bad": "Разные единицы", "fix": "RMSE = sqrt(MSE)"},
                {"mistake": "Сравнивать R² между задачами", "why_bad": "R² не универсален", "fix": "Внутри одной задачи"},
                {"mistake": "Думать, что R² > 1", "why_bad": "R² ≤ 1 на test", "fix": "1 = идеально, <0 = плохо"},
            ]),
            interview_questions([
                {"q": "Чем MAE от RMSE?", "a": "MAE — средний модуль, RMSE — корень из среднего квадрата. RMSE сильнее штрафует большие ошибки. MAE робастнее."},
                {"q": "Что R² = 0.7?", "a": "Модель объясняет 70% дисперсии y. 30% — шум или упущенные фичи. R² ≤ 1, R²<0 — хуже среднего."},
                {"q": "Когда MAE vs RMSE?", "a": "MAE — выбросы не критичны (доходы). RMSE — большие ошибки критичны (время, медицина). MSE часто как loss (дифференцируем)."},
            ]),
            knowledge_checklist([
                "Знаю формулы MAE, MSE, RMSE, R²",
                "Считаю метрики через sklearn",
                "RMSE штрафует выбросы сильнее MAE",
                "Интерпретирую R²",
                "Выбираю метрику под задачу",
            ]),
        ],
        exercises=[
            ex(1, "python", "y_true = [3, 5, 2, 7], y_pred = [2.5, 5.5, 2.2, 6.5]. Посчитай MAE, сохрани в `mae`.",
               "import numpy as np\nfrom sklearn.metrics import mean_absolute_error\ny_true = [3, 5, 2, 7]\ny_pred = [2.5, 5.5, 2.2, 6.5]\nmae = 0\n",
               "import numpy as np\nfrom sklearn.metrics import mean_absolute_error\nmae = mean_absolute_error(y_true, y_pred)",
               [{"check": "abs(mae - 0.425) < 0.01", "msg": "MAE = 0.425"}],
               ["mean_absolute_error"], 1),
            ex(2, "python", "Те же данные, посчитай MSE в `mse`.",
               "import numpy as np\nfrom sklearn.metrics import mean_squared_error\ny_true = [3, 5, 2, 7]\ny_pred = [2.5, 5.5, 2.2, 6.5]\nmse = 0\n",
               "import numpy as np\nfrom sklearn.metrics import mean_squared_error\nmse = mean_squared_error(y_true, y_pred)",
               [{"check": "abs(mse - 0.2) < 0.05", "msg": "MSE ≈ 0.2"}],
               ["mean_squared_error"], 1),
            ex(3, "python", "RMSE = sqrt(MSE) в `rmse`.",
               "import numpy as np\nfrom sklearn.metrics import mean_squared_error\ny_true = [3, 5, 2, 7]\ny_pred = [2.5, 5.5, 2.2, 6.5]\nrmse = 0\n",
               "import numpy as np\nrmse = np.sqrt(mean_squared_error(y_true, y_pred))",
               [{"check": "abs(rmse - 0.45) < 0.05", "msg": "RMSE ≈ 0.45"}],
               ["np.sqrt(MSE)"], 1),
            ex(4, "python", "R² в `r2`.",
               "import numpy as np\nfrom sklearn.metrics import r2_score\ny_true = [3, 5, 2, 7]\ny_pred = [2.5, 5.5, 2.2, 6.5]\nr2 = 0\n",
               "import numpy as np\nr2 = r2_score(y_true, y_pred)",
               [{"check": "0.5 < r2 < 1.0", "msg": "R² > 0.5"}],
               ["r2_score"], 1),
            ex(5, "python", "Обучи LinearRegression, R² на test в `test_r2`.",
               "import numpy as np\nfrom sklearn.linear_model import LinearRegression\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX = np.random.uniform(0, 10, (100, 1))\ny = 3 * X.flatten() + 2 + np.random.randn(100)\ntest_r2 = 0\n",
               "import numpy as np\nfrom sklearn.linear_model import LinearRegression\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX = np.random.uniform(0, 10, (100, 1))\ny = 3 * X.flatten() + 2 + np.random.randn(100)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\ntest_r2 = LinearRegression().fit(X_train, y_train).score(X_test, y_test)",
               [{"check": "test_r2 > 0.9", "msg": "R² > 0.9"}],
               ["model.score"], 2),
            ex(6, "python", "y_true = [1, 2, 3], y_pred = [1, 2, 3]. MAE, MSE, RMSE, R².",
               "import numpy as np\nfrom sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error\ny_true = [1, 2, 3]\ny_pred = [1, 2, 3]\nmae = mse = rmse = r2 = 0\n",
               "import numpy as np\nfrom sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error\nmae = mean_absolute_error(y_true, y_pred)\nmse = mean_squared_error(y_true, y_pred)\nrmse = np.sqrt(mse)\nr2 = r2_score(y_true, y_pred)",
               [{"check": "mae == 0 and mse == 0 and r2 == 1.0", "msg": "Идеально"}],
               ["Идеально → 0, R²=1"], 1),
            ex(7, "python", "y_true=[1,2,3], y_pred=[2,2,2]. R² ≈ 0.",
               "import numpy as np\nfrom sklearn.metrics import r2_score\ny_true = [1, 2, 3]\ny_pred = [2, 2, 2]\nr2 = 0\n",
               "import numpy as np\nr2 = r2_score(y_true, y_pred)",
               [{"check": "abs(r2) < 1e-9", "msg": "R² ≈ 0 (среднее)"}],
               ["Константа = среднее → R²=0"], 2),
            ex(8, "python", "y_true=[10,20,30], y_pred=[50,50,50]. R² < 0.",
               "import numpy as np\nfrom sklearn.metrics import r2_score\ny_true = [10, 20, 30]\ny_pred = [50, 50, 50]\nr2 = 0\n",
               "import numpy as np\nr2 = r2_score(y_true, y_pred)",
               [{"check": "r2 < 0", "msg": "R² < 0 — хуже среднего"}],
               ["Хуже среднего → R²<0"], 2),
            ex(9, "python", "y_true=[1,2,3,100], y_pred=[1,2,3,3]. (MAE, RMSE) в `result`.",
               "import numpy as np\nfrom sklearn.metrics import mean_squared_error, mean_absolute_error\ny_true = [1, 2, 3, 100]\ny_pred = [1, 2, 3, 3]\nresult = (0, 0)\n",
               "import numpy as np\nfrom sklearn.metrics import mean_squared_error, mean_absolute_error\nmae = mean_absolute_error(y_true, y_pred)\nrmse = np.sqrt(mean_squared_error(y_true, y_pred))\nresult = (mae, rmse)",
               [{"check": "result[1] > result[0]", "msg": "RMSE > MAE (выброс штрафуется)"}],
               ["97² → RMSE >> MAE"], 3),
        ],
        minutes=45, difficulty=2,
    )


def _7_5():
    return lesson(
        "7.5", "Метрики классификации: accuracy, precision, recall, F1", "mixed", [
            theory(
                "**Метрики классификации** строятся на confusion matrix (4 ячейки):\n"
                "- **TP** — правильно предсказали положительный\n"
                "- **TN** — правильно предсказали отрицательный\n"
                "- **FP** — ложная тревога\n"
                "- **FN** — пропуск цели\n\n"
                "**Accuracy** = (TP + TN) / total. Простая, **врёт при дисбалансе**.\n\n"
                "**Precision** = TP / (TP + FP). Из предсказанных положительными — "
                "сколько верных. Хорошо, когда FP дорогие (спам-фильтр).\n\n"
                "**Recall** = TP / (TP + FN). Из реальных положительных — сколько нашли. "
                "Хорошо, когда FN опасны (рак, fraud).\n\n"
                "**F1** = 2*P*R/(P+R). Гармоническое среднее. Удобна при дисбалансе.\n\n"
                "**Когда что:** accuracy при балансе, F1 при дисбалансе, precision "
                "когда FP дорогие, recall когда FN опасны."
            ),
            analogy(
                "Античитер-аналитик. Accuracy — доля верных вердиктов. Precision — "
                "из обвинённых сколько читеров. Recall — из реальных сколько поймал.",
                "Рак: recall важнее (пропустить больного — катастрофа), precision терпим."
            ),
            visual(
                "Confusion Matrix",
                "              Predicted\n"
                "              0    1\n"
                "   Actual 0  [TN  │ FP ]\n"
                "          1  [FN  │ TP ]\n"
                "   Acc  = (TP+TN)/N\n"
                "   Prec = TP/(TP+FP)\n"
                "   Rec  = TP/(TP+FN)\n"
                "   F1   = 2PR/(P+R)"
            ),
            example(
                "4 метрики + confusion matrix.",
                "y_true vs y_pred, считаем всё.",
                "import numpy as np\n"
                "from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix\n"
                "y_true = np.array([0, 1, 1, 0, 1, 1, 0, 0, 1, 0])\n"
                "y_pred = np.array([0, 1, 0, 0, 1, 1, 1, 0, 1, 0])\n"
                "print(confusion_matrix(y_true, y_pred))\n"
                "print('F1:', f1_score(y_true, y_pred))",
                "[[4 1]\n [1 4]]\nF1: 0.8",
                "TN=4, FP=1, FN=1, TP=4. F1=0.8 — баланс precision и recall."
            ),
            common_mistakes([
                {"mistake": "Accuracy при дисбалансе 100:1", "why_bad": "Константа = 99%", "fix": "F1, ROC-AUC"},
                {"mistake": "Путать precision и recall", "why_bad": "Разные формулы", "fix": "P: из предсказанных. R: из реальных"},
                {"mistake": "Не учитывать pos_label", "why_bad": "По умолчанию pos_label=1", "fix": "Указывай явно"},
                {"mistake": "Accuracy на тесте 30 примеров", "why_bad": "Шумная метрика", "fix": "CV или стратификация"},
            ]),
            interview_questions([
                {"q": "Что precision и recall?", "a": "Precision = TP/(TP+FP) — точность. Recall = TP/(TP+FN) — полнота. Trade-off. F1 = 2PR/(P+R)."},
                {"q": "Когда accuracy врёт?", "a": "При дисбалансе. 99% класса 0 → константа даёт 99%. F1, ROC-AUC, stratify."},
                {"q": "Что F1?", "a": "Гармоническое среднее P и R. [0, 1]. Штрафует за низкое любой. При дисбалансе."},
            ]),
            knowledge_checklist([
                "Строю confusion matrix",
                "Считаю accuracy, precision, recall, F1",
                "Понимаю P vs R",
                "Знаю, когда accuracy обманчива",
                "F1 при дисбалансе",
            ]),
        ],
        exercises=[
            ex(1, "python", "y_true=[0,1,1,0,1], y_pred=[0,1,0,0,1]. Accuracy в `acc`.",
               "import numpy as np\nfrom sklearn.metrics import accuracy_score\ny_true = [0, 1, 1, 0, 1]\ny_pred = [0, 1, 0, 0, 1]\nacc = 0\n",
               "import numpy as np\nfrom sklearn.metrics import accuracy_score\nacc = accuracy_score(y_true, y_pred)",
               [{"check": "acc == 0.8", "msg": "4 из 5"}],
               ["accuracy_score"], 1),
            ex(2, "python", "Precision в `prec`.",
               "import numpy as np\nfrom sklearn.metrics import precision_score\ny_true = [0, 1, 1, 0, 1]\ny_pred = [0, 1, 0, 0, 1]\nprec = 0\n",
               "import numpy as np\nfrom sklearn.metrics import precision_score\nprec = precision_score(y_true, y_pred)",
               [{"check": "prec == 1.0", "msg": "Все '1' верны"}],
               ["precision_score"], 1),
            ex(3, "python", "Recall в `rec`.",
               "import numpy as np\nfrom sklearn.metrics import recall_score\ny_true = [0, 1, 1, 0, 1]\ny_pred = [0, 1, 0, 0, 1]\nrec = 0\n",
               "import numpy as np\nfrom sklearn.metrics import recall_score\nrec = recall_score(y_true, y_pred)",
               [{"check": "abs(rec - 0.667) < 0.05", "msg": "2/3"}],
               ["recall_score"], 1),
            ex(4, "python", "F1 в `f1`.",
               "import numpy as np\nfrom sklearn.metrics import f1_score\ny_true = [0, 1, 1, 0, 1]\ny_pred = [0, 1, 0, 0, 1]\nf1 = 0\n",
               "import numpy as np\nfrom sklearn.metrics import f1_score\nf1 = f1_score(y_true, y_pred)",
               [{"check": "0.7 < f1 < 0.9", "msg": "F1 в разумном диапазоне"}],
               ["f1_score"], 1),
            ex(5, "python", "y: 1000 значений с 95% нулей, seed=42.",
               "import numpy as np\ny = np.array([])\n",
               "import numpy as np\nnp.random.seed(42)\ny = np.random.choice([0, 1], size=1000, p=[0.95, 0.05])",
               [{"check": "y.shape == (1000,)", "msg": "1000 меток"},
                {"check": "y.mean() < 0.1", "msg": "Дисбаланс"}],
               ["np.random.choice с p"], 1),
            ex(6, "python", "y_pred = [0]*1000. Accuracy константы в `acc_const`.",
               "import numpy as np\nfrom sklearn.metrics import accuracy_score\nnp.random.seed(42)\ny = np.random.choice([0, 1], size=1000, p=[0.95, 0.05])\ny_pred = [0] * 1000\nacc_const = 0\n",
               "import numpy as np\nfrom sklearn.metrics import accuracy_score\nacc_const = accuracy_score(y, y_pred)",
               [{"check": "acc_const > 0.9", "msg": "Константа = высокая accuracy"}],
               ["Константа при дисбалансе"], 2),
            ex(7, "python", "Confusion matrix в `cm`.",
               "import numpy as np\nfrom sklearn.metrics import confusion_matrix\nnp.random.seed(42)\ny = np.random.choice([0, 1], size=1000, p=[0.95, 0.05])\ny_pred = [0] * 1000\ncm = None\n",
               "import numpy as np\nfrom sklearn.metrics import confusion_matrix\ncm = confusion_matrix(y, y_pred)",
               [{"check": "cm.shape == (2, 2)", "msg": "2x2"},
                {"check": "cm[0, 0] > 900", "msg": "TN ~ 950"}],
               ["confusion_matrix"], 2),
            ex(8, "python", "LogisticRegression с дисбалансом. (acc, f1) на test.",
               "import numpy as np\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import accuracy_score, f1_score\nnp.random.seed(42)\nX = np.random.randn(500, 5)\ny = (X[:, 0] + 0.3 * np.random.randn(500) > 0).astype(int)\ny[np.random.choice(500, 450, replace=False)] = 0\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\nacc = 0\nf1 = 0\n",
               "import numpy as np\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import accuracy_score, f1_score\nnp.random.seed(42)\nX = np.random.randn(500, 5)\ny = (X[:, 0] + 0.3 * np.random.randn(500) > 0).astype(int)\ny[np.random.choice(500, 450, replace=False)] = 0\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\ny_pred = LogisticRegression().fit(X_train, y_train).predict(X_test)\nacc = accuracy_score(y_test, y_pred)\nf1 = f1_score(y_test, y_pred)",
               [{"check": "0.7 < acc < 1.0", "msg": "accuracy высокая"},
                {"check": "0 <= f1 <= 1", "msg": "F1 в [0, 1]"}],
               ["model.predict", "stratify"], 3),
            ex(9, "python", "F1 для константы в `f1_const`.",
               "import numpy as np\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import f1_score\nnp.random.seed(42)\nX = np.random.randn(500, 5)\ny = (X[:, 0] + 0.3 * np.random.randn(500) > 0).astype(int)\ny[np.random.choice(500, 450, replace=False)] = 0\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\ny_pred = [0] * len(y_test)\nf1_const = 0\n",
               "import numpy as np\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import f1_score\nnp.random.seed(42)\nX = np.random.randn(500, 5)\ny = (X[:, 0] + 0.3 * np.random.randn(500) > 0).astype(int)\ny[np.random.choice(500, 450, replace=False)] = 0\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\ny_pred = [0] * len(y_test)\nf1_const = f1_score(y_test, y_pred)",
               [{"check": "f1_const == 0.0", "msg": "F1=0 для константы"}],
               ["F1 видит дисбаланс"], 2),
        ],
        minutes=50, difficulty=2,
    )
def _7_3():
    return lesson(
        "7.3", "Переобучение и недообучение", "mixed", [
            theory(
                "**Переобучение (overfitting)** — модель выучила шум и выбросы train, "
                "плохо обобщает на новые данные. **Недообучение (underfitting)** — модель "
                "слишком простая, не улавливает закономерность.\n\n"
                "**Диагностика по кривым обучения:** строим `train_score` и `validation_score` "
                "vs размер train:\n"
                "- Обе низкие → underfit\n"
                "- Train высокий, val низкий → overfit\n"
                "- Обе высокие и сходятся → OK\n\n"
                "**Методы борьбы с overfit:**\n"
                "- **Больше данных** — лучший способ\n"
                "- **Упростить модель** — меньше параметров\n"
                "- **Регуляризация** — L1/L2 штраф за большие веса\n"
                "- **Dropout** (в нейросетях) — случайное отключение нейронов\n"
                "- **Early stopping** — остановка по val_loss\n"
                "- **Cross-validation** — устойчивая оценка\n"
                "- **Ансамбли** — усреднение нескольких моделей\n\n"
                "**Bias-variance tradeoff:** сложная модель → low bias / high variance, "
                "простая → high bias / low variance. Баланс — sweet spot.\n\n"
                "**В sklearn:** параметр `alpha` (Ridge/Lasso), `max_depth` (деревья), "
                "`C` (обратный регуляризации в LogisticRegression)."
            ),
            analogy(
                "Студент-зубр (overfit) — выучил ответы на 5 билетов, на других упал. "
                "Студент-лентяй (underfit) — знает тему поверхностно. Студент-нормальный — "
                "понял принцип.",
                "В ML: дерево max_depth=None — overfit. Линейная регрессия на сложной "
                "выборке — underfit."
            ),
            visual(
                "Bias-Variance",
                "   Score\n"
                "   1.0 ┤        ╭─────────╮  ← sweet spot\n"
                "       │      ╱╱   val   ╲╲\n"
                "       │    ╱╱             ╲╲\n"
                "   0.5 ┤  ╱╱   train        ╲╲  ← overfit\n"
                "       │╱╱                    ╲╲\n"
                "   0.0 └────────────────────────── Complexity\n"
                "       underfit      OK       overfit"
            ),
            example(
                "Покажи overfit на полиноме.",
                "Сравним degree=1 (underfit) и degree=15 (overfit).",
                "import numpy as np\n"
                "from sklearn.linear_model import LinearRegression\n"
                "from sklearn.preprocessing import PolynomialFeatures\n"
                "from sklearn.pipeline import make_pipeline\n"
                "from sklearn.model_selection import train_test_split\n"
                "np.random.seed(42)\n"
                "X = np.linspace(0, 10, 50).reshape(-1, 1)\n"
                "y = 0.5 * X.flatten()**2 - 2 * X.flatten() + 1 + np.random.randn(50)\n"
                "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=42)\n"
                "for d in [1, 15]:\n"
                "    m = make_pipeline(PolynomialFeatures(d), LinearRegression()).fit(X_tr, y_tr)\n"
                "    print(f'd={d:2d} train R2={m.score(X_tr, y_tr):.3f} test R2={m.score(X_te, y_te):.3f}')",
                "d= 1 train R2=0.799 test R2=0.832\nd=15 train R2=0.911 test R2=0.491",
                "degree=1: train и test R² близки — underfit (но тест даже выше train). "
                "degree=15: train 0.91 vs test 0.49 — классический overfit."
            ),
            common_mistakes([
                {"mistake": "Смотреть только на train score", "why_bad": "Модель может идеально выучить train и не работать в проде", "fix": "Всегда оценивай на test"},
                {"mistake": "Больше фичей = лучше", "why_bad": "Лишние фичи добавляют шум, модель переобучается", "fix": "Отбор фичей, регуляризация"},
                {"mistake": "Игнорировать размер выборки", "why_bad": "1000 точек и 100 фичей — почти гарантирован overfit", "fix": "Правило: n >> p"},
                {"mistake": "Усложнять модель на малых данных", "why_bad": "KNN с k=1 запомнит train", "fix": "Простая модель + регуляризация"},
            ]),
            interview_questions([
                {"q": "Что такое overfitting?", "a": "Модель выучила шум train. Train R² высокий, test R² низкий, разрыв большой. Лечится регуляризацией, упрощением, данными, CV."},
                {"q": "Bias-variance tradeoff?", "a": "Bias — ошибка от упрощения, variance — от чувствительности к данным. Сложная модель → low bias / high variance. Простая → наоборот. Цель — баланс."},
                {"q": "Как обнаружить overfit?", "a": "Train и val score расходятся. Кривая обучения: train высокий и растёт, val низкий и падает. Cross-validation даёт устойчивую оценку."},
            ]),
            knowledge_checklist([
                "Различаю overfit и underfit",
                "Строю кривые обучения",
                "Применяю регуляризацию",
                "Использую cross-validation",
                "Понимаю bias-variance tradeoff",
                "Упрощаю модель при переобучении",
            ]),
        ],
        exercises=[
            ex(1, "python", "Данные 100 точек: y = 0.5*x^2 + шум, seed=42. Сохрани X (100,1) и y (100,).",
               "import numpy as np\nX = np.array([])\ny = np.array([])\n",
               "import numpy as np\nnp.random.seed(42)\nX = np.random.uniform(-3, 3, (100, 1))\ny = 0.5 * X.flatten()**2 + np.random.randn(100)",
               [{"check": "X.shape == (100, 1)", "msg": "100 строк"}],
               ["np.random.uniform", "y квадратичный"], 1),
            ex(2, "python", "LinearRegression, train R² и test R² в `r2_train, r2_test` (80/20, random_state=42).",
               "import numpy as np\nfrom sklearn.linear_model import LinearRegression\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX = np.random.uniform(-3, 3, (100, 1))\ny = 0.5 * X.flatten()**2 + np.random.randn(100)\nr2_train = 0\nr2_test = 0\n",
               "import numpy as np\nfrom sklearn.linear_model import LinearRegression\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\nm = LinearRegression().fit(X_train, y_train)\nr2_train = m.score(X_train, y_train)\nr2_test = m.score(X_test, y_test)",
               [{"check": "r2_train < 0.85", "msg": "Линейная на квадратичной — underfit"}],
               ["underfit — обе метрики низкие"], 2),
            ex(3, "python", "DecisionTreeRegressor(max_depth=None). (train, test) R². Ожидай overfit.",
               "import numpy as np\nfrom sklearn.tree import DecisionTreeRegressor\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX = np.random.uniform(-3, 3, (100, 1))\ny = 0.5 * X.flatten()**2 + np.random.randn(100)\nr2_train = 0\nr2_test = 0\n",
               "import numpy as np\nfrom sklearn.tree import DecisionTreeRegressor\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\nm = DecisionTreeRegressor(random_state=42).fit(X_train, y_train)\nr2_train = m.score(X_train, y_train)\nr2_test = m.score(X_test, y_test)",
               [{"check": "r2_train > 0.95", "msg": "Train почти 1 — overfit"},
                {"check": "r2_test < 0.9", "msg": "Test хуже train"}],
               ["max_depth=None → запоминает train"], 2),
            ex(4, "python", "DecisionTreeRegressor(max_depth=3). (train, test) R² — баланс.",
               "import numpy as np\nfrom sklearn.tree import DecisionTreeRegressor\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX = np.random.uniform(-3, 3, (100, 1))\ny = 0.5 * X.flatten()**2 + np.random.randn(100)\nr2_train = 0\nr2_test = 0\n",
               "import numpy as np\nfrom sklearn.tree import DecisionTreeRegressor\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\nm = DecisionTreeRegressor(max_depth=3, random_state=42).fit(X_train, y_train)\nr2_train = m.score(X_train, y_train)\nr2_test = m.score(X_test, y_test)",
               [{"check": "r2_train < 0.95 and r2_test > 0.5", "msg": "Глубже = переобучение, мельче = баланс"}],
               ["max_depth=3 — sweet spot"], 2),
            ex(5, "python", "Построй график learning curve: train_size vs score для LR.",
               "import numpy as np\nimport matplotlib.pyplot as plt\nfrom sklearn.linear_model import LinearRegression\nfrom sklearn.model_selection import learning_curve\nnp.random.seed(42)\nX = np.random.uniform(-3, 3, (100, 1))\ny = 0.5 * X.flatten()**2 + np.random.randn(100)\nfig, ax = plt.subplots()\n",
               "import numpy as np\nimport matplotlib.pyplot as plt\nfrom sklearn.linear_model import LinearRegression\nfrom sklearn.model_selection import learning_curve\nnp.random.seed(42)\nX = np.random.uniform(-3, 3, (100, 1))\ny = 0.5 * X.flatten()**2 + np.random.randn(100)\ntr_sizes, tr_scores, te_scores = learning_curve(LinearRegression(), X, y, cv=5, train_sizes=np.linspace(0.1, 1.0, 5), random_state=42)\nfig, ax = plt.subplots()\nax.plot(tr_sizes, tr_scores.mean(axis=1), label='train')\nax.plot(tr_sizes, te_scores.mean(axis=1), label='val')\nax.set_xlabel('train size'); ax.set_ylabel('R2'); ax.legend()\nplt.close(fig)",
               [{"check": "True", "msg": "matplotlib"}],
               ["learning_curve", "plt.close"], 3),
            ex(6, "python", "Train/val кривые для tree max_depth=1, 3, 5, 10. val_scores в `val_scores`.",
               "import numpy as np\nfrom sklearn.tree import DecisionTreeRegressor\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX = np.random.uniform(-3, 3, (100, 1))\ny = 0.5 * X.flatten()**2 + np.random.randn(100)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\nval_scores = np.array([])\n",
               "import numpy as np\nfrom sklearn.tree import DecisionTreeRegressor\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\nval_scores = np.array([DecisionTreeRegressor(max_depth=d, random_state=42).fit(X_train, y_train).score(X_test, y_test) for d in [1, 3, 5, 10]])",
               [{"check": "val_scores.shape == (4,)", "msg": "4 глубины"}],
               ["list comprehension по depth"], 3),
            ex(7, "python", "Визуализируй overfit: scatter + degree=1, 15.",
               "import numpy as np\nimport matplotlib.pyplot as plt\nfrom sklearn.linear_model import LinearRegression\nfrom sklearn.preprocessing import PolynomialFeatures\nfrom sklearn.pipeline import make_pipeline\nnp.random.seed(42)\nX = np.linspace(-3, 3, 50).reshape(-1, 1)\ny = 0.5 * X.flatten()**2 + np.random.randn(50)\nfig, ax = plt.subplots()\n",
               "import numpy as np\nimport matplotlib.pyplot as plt\nfrom sklearn.linear_model import LinearRegression\nfrom sklearn.preprocessing import PolynomialFeatures\nfrom sklearn.pipeline import make_pipeline\nnp.random.seed(42)\nX = np.linspace(-3, 3, 50).reshape(-1, 1)\ny = 0.5 * X.flatten()**2 + np.random.randn(50)\nfig, ax = plt.subplots()\nax.scatter(X, y, s=10, label='data')\nX_l = np.linspace(-3, 3, 100).reshape(-1, 1)\nfor d in [1, 15]:\n    m = make_pipeline(PolynomialFeatures(d), LinearRegression()).fit(X, y)\n    ax.plot(X_l, m.predict(X_l), label=f'd={d}', linewidth=2)\nax.legend()\nplt.close(fig)",
               [{"check": "True", "msg": "matplotlib"}],
               ["PolynomialFeatures", "pipeline"], 3),
            ex(8, "python", "Train_sizes — массив от 10 до 100 с шагом 10.",
               "import numpy as np\ntrain_sizes = np.array([])\n",
               "import numpy as np\ntrain_sizes = np.arange(10, 101, 10)",
               [{"check": "len(train_sizes) == 10", "msg": "10 размеров"},
                {"check": "train_sizes[0] == 10 and train_sizes[-1] == 100", "msg": "10..100"}],
               ["np.arange"], 1),
            ex(9, "python", "Cross-val score для LR (5-fold). mean в `cv`.",
               "import numpy as np\nfrom sklearn.linear_model import LinearRegression\nfrom sklearn.model_selection import cross_val_score\nnp.random.seed(42)\nX = np.random.uniform(-3, 3, (100, 1))\ny = 0.5 * X.flatten()**2 + np.random.randn(100)\ncv = 0\n",
               "import numpy as np\nfrom sklearn.linear_model import LinearRegression\nfrom sklearn.model_selection import cross_val_score\nnp.random.seed(42)\ncv = cross_val_score(LinearRegression(), X, y, cv=5).mean()",
               [{"check": "0 < cv < 1", "msg": "CV R² в [0, 1)"},
                {"check": "cv < 0.85", "msg": "Линейная недообучена на квадратичной"}],
               ["cross_val_score"], 2),
            ex(10, "python", "Предскажи overfit по разнице train_score - val_score. Сохрани gap в `gap`.",
               "import numpy as np\nfrom sklearn.tree import DecisionTreeRegressor\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX = np.random.uniform(-3, 3, (100, 1))\ny = 0.5 * X.flatten()**2 + np.random.randn(100)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\ngap = 0\n",
               "import numpy as np\nfrom sklearn.tree import DecisionTreeRegressor\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\nm = DecisionTreeRegressor(random_state=42).fit(X_train, y_train)\ngap = m.score(X_train, y_train) - m.score(X_test, y_test)",
               [{"check": "gap > 0.1", "msg": "Большой gap = overfit"}],
               ["train - test > 0.1 → overfit"], 3),
        ],
        minutes=55, difficulty=3,
    )


def _7_8():
    return lesson(
        "7.8", "Дерево решений", "mixed", [
            theory(
                "**Дерево решений (Decision Tree)** — модель, которая разбивает "
                "пространство признаков по правилам «если-то». Каждый узел — условие "
                "на фичу, каждый лист — прогноз.\n\n"
                "**Обучение:** жадно выбираем лучшее разбиение (max information gain "
                "или min Gini/MSE).\n\n"
                "**Для классификации (sklearn):**\n"
                "- `DecisionTreeClassifier(criterion='gini')` — по умолчанию\n"
                "- criterion='entropy' — то же, через информационный выигрыш\n"
                "- `model.feature_importances_` — значимость фич\n"
                "- `model.predict(X)`, `model.score(X, y)` = accuracy\n\n"
                "**Гиперпараметры:**\n"
                "- `max_depth` — глубина (главный регуляризатор)\n"
                "- `min_samples_split`, `min_samples_leaf` — минимум для узла\n"
                "- `max_features` — сколько фич рассматривать\n\n"
                "**Плюсы:** интерпретируемость, нет масштабирования, фичи любых типов. "
                "**Минусы:** нестабильность, overfit, жадный алгоритм → не глобальный optimum."
            ),
            analogy(
                "Дерево — flowchart для принятия решений: «KDR > 2? → да → уровень? → "
                "высокий → win». Врач ставит диагноз по цепочке симптомов.",
                "В Dota: kills>10 И deaths<5 → носитель. duration>30min → late game."
            ),
            visual(
                "Decision Tree",
                "        [kills > 10?]\n"
                "        /          \\\n"
                "      yes           no\n"
                "      /              \\\n"
                "   [deaths<5?]    [win]\n"
                "   /      \\         |\n"
                "  yes     no        y\n"
                "  |        |\n"
                " carry   support"
            ),
            example(
                "DecisionTreeClassifier на Dota-данных.",
                "kills, deaths, gold → win (1) / lose (0).",
                "import numpy as np\n"
                "from sklearn.tree import DecisionTreeClassifier\n"
                "np.random.seed(42)\n"
                "n = 300\n"
                "kills = np.random.poisson(6, n)\n"
                "deaths = np.random.poisson(5, n)\n"
                "gold = np.random.normal(2000, 500, n)\n"
                "X = np.column_stack([kills, deaths, gold])\n"
                "y = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)\n"
                "m = DecisionTreeClassifier(max_depth=5, random_state=42).fit(X, y)\n"
                "print('acc:', m.score(X, y))\n"
                "print('importance:', m.feature_importances_)",
                "acc: 0.92\nimportance: [0.45 0.48 0.07]",
                "accuracy 92%. kills и deaths — главные фичи (importance 0.45 и 0.48), "
                "gold почти не влияет в этой модели."
            ),
            common_mistakes([
                {"mistake": "max_depth=None на малых данных", "why_bad": "Запомнит train, упадёт на test", "fix": "max_depth=3..10, подбирать по CV"},
                {"mistake": "Смотреть на train score", "why_bad": "Всегда будет 100%", "fix": "CV на train"},
                {"mistake": "Дерево для линейных трендов", "why_bad": "Ступеньки плохо аппроксимируют прямую", "fix": "Линейная регрессия"},
                {"mistake": "Игнорировать class_weight", "why_bad": "Дисбаланс ломает дерево", "fix": "class_weight='balanced'"},
            ]),
            interview_questions([
                {"q": "Как работает дерево решений?", "a": "Жадно: на каждом шаге выбираем фичу и порог, дающие max information gain (Gini/entropy). Строим дерево до max_depth или min_samples_split."},
                {"q": "Почему дерево переобучается?", "a": "Без ограничений дерево запомнит train (1.0 R²/acc). Лечится max_depth, min_samples_leaf, pruning, кросс-валидацией."},
                {"q": "Что feature_importances_?", "a": "Сумма уменьшений impurity по всем узлам, где фича использовалась. [0, 1], сумма = 1. Полезно для отбора фич."},
            ]),
            knowledge_checklist([
                "Обучаю DecisionTreeClassifier/Regressor",
                "Регулирую max_depth",
                "Читаю feature_importances_",
                "Использую criterion='gini' / 'entropy'",
                "Знаю pro/cons деревьев",
            ]),
        ],
        exercises=[
            ex(1, "python", "Dota-данные: 300 игроков, kills/deaths/gold. win в `y`. seed=42.",
               "import numpy as np\nX = np.array([])\ny = np.array([])\n",
               "import numpy as np\nnp.random.seed(42)\nn = 300\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nX = np.column_stack([kills, deaths, gold])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)",
               [{"check": "X.shape == (300, 3)", "msg": "300 строк, 3 фичи"},
                {"check": "set(y.tolist()) <= {0, 1}", "msg": "Бинарные метки"}],
               ["np.column_stack", "kills/deaths/gold"], 1),
            ex(2, "python", "DecisionTreeClassifier(max_depth=5). accuracy в `acc`.",
               "import numpy as np\nfrom sklearn.tree import DecisionTreeClassifier\nnp.random.seed(42)\nn = 300\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nX = np.column_stack([kills, deaths, gold])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)\nacc = 0\n",
               "import numpy as np\nfrom sklearn.tree import DecisionTreeClassifier\nacc = DecisionTreeClassifier(max_depth=5, random_state=42).fit(X, y).score(X, y)",
               [{"check": "acc > 0.7", "msg": "accuracy > 0.7"}],
               ["max_depth=5"], 1),
            ex(3, "python", "max_depth=None vs max_depth=3. (acc_deep, acc_shallow) на test (80/20, random_state=42).",
               "import numpy as np\nfrom sklearn.tree import DecisionTreeClassifier\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nn = 300\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nX = np.column_stack([kills, deaths, gold])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\nacc_deep = 0\nacc_shallow = 0\n",
               "import numpy as np\nfrom sklearn.tree import DecisionTreeClassifier\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\nacc_deep = DecisionTreeClassifier(random_state=42).fit(X_train, y_train).score(X_test, y_test)\nacc_shallow = DecisionTreeClassifier(max_depth=3, random_state=42).fit(X_train, y_train).score(X_test, y_test)",
               [{"check": "acc_shallow > 0.6", "msg": "Мелкое дерево обобщает"}],
               ["max_depth=None vs 3"], 3),
            ex(4, "python", "feature_importances_ в `importances`.",
               "import numpy as np\nfrom sklearn.tree import DecisionTreeClassifier\nnp.random.seed(42)\nn = 300\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nX = np.column_stack([kills, deaths, gold])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)\nmodel = DecisionTreeClassifier(max_depth=5, random_state=42).fit(X, y)\nimportances = np.array([])\n",
               "import numpy as np\nfrom sklearn.tree import DecisionTreeClassifier\nmodel = DecisionTreeClassifier(max_depth=5, random_state=42).fit(X, y)\nimportances = model.feature_importances_",
               [{"check": "importances.shape == (3,)", "msg": "3 фичи"},
                {"check": "abs(importances.sum() - 1.0) < 1e-6", "msg": "Сумма = 1"}],
               ["feature_importances_"], 2),
            ex(5, "python", "Предсказание на новых 5 игроках. labels в `preds`.",
               "import numpy as np\nfrom sklearn.tree import DecisionTreeClassifier\nnp.random.seed(42)\nn = 300\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nX = np.column_stack([kills, deaths, gold])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)\nmodel = DecisionTreeClassifier(max_depth=5, random_state=42).fit(X, y)\nX_new = np.array([[10, 3, 3000], [2, 8, 1500], [7, 5, 2200], [4, 9, 1200], [12, 2, 3500]])\npreds = np.array([])\n",
               "import numpy as np\nfrom sklearn.tree import DecisionTreeClassifier\nmodel = DecisionTreeClassifier(max_depth=5, random_state=42).fit(X, y)\npreds = model.predict(X_new)",
               [{"check": "preds.shape == (5,)", "msg": "5 предсказаний"}],
               ["model.predict"], 1),
            ex(6, "python", "Предсказание winrate игрока: DecisionTreeRegressor. R² в `r2`.",
               "import numpy as np\nfrom sklearn.tree import DecisionTreeRegressor\nnp.random.seed(42)\nn = 300\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nX = np.column_stack([kills, deaths, gold])\ny = (50 + 5*kills - 4*deaths + 0.005*gold + np.random.randn(n)*5)\nr2 = 0\n",
               "import numpy as np\nfrom sklearn.tree import DecisionTreeRegressor\nr2 = DecisionTreeRegressor(max_depth=5, random_state=42).fit(X, y).score(X, y)",
               [{"check": "r2 > 0.7", "msg": "R² > 0.7"}],
               ["DecisionTreeRegressor"], 2),
            ex(7, "python", "Cross-val (cv=5) для дерева. mean в `cv`.",
               "import numpy as np\nfrom sklearn.tree import DecisionTreeClassifier\nfrom sklearn.model_selection import cross_val_score\nnp.random.seed(42)\nn = 300\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nX = np.column_stack([kills, deaths, gold])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)\ncv = 0\n",
               "import numpy as np\nfrom sklearn.tree import DecisionTreeClassifier\nfrom sklearn.model_selection import cross_val_score\nnp.random.seed(42)\ncv = cross_val_score(DecisionTreeClassifier(max_depth=5, random_state=42), X, y, cv=5).mean()",
               [{"check": "0.6 < cv < 1.0", "msg": "CV > 0.6"}],
               ["cross_val_score"], 2),
            ex(8, "python", "Визуализируй feature_importances_ баром.",
               "import numpy as np\nimport matplotlib.pyplot as plt\nfrom sklearn.tree import DecisionTreeClassifier\nnp.random.seed(42)\nn = 300\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nX = np.column_stack([kills, deaths, gold])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)\nmodel = DecisionTreeClassifier(max_depth=5, random_state=42).fit(X, y)\nfig, ax = plt.subplots()\n",
               "import numpy as np\nimport matplotlib.pyplot as plt\nfrom sklearn.tree import DecisionTreeClassifier\nmodel = DecisionTreeClassifier(max_depth=5, random_state=42).fit(X, y)\nfig, ax = plt.subplots()\nax.bar(['kills', 'deaths', 'gold'], model.feature_importances_)\nax.set_title('Feature importances')\nplt.close(fig)",
               [{"check": "True", "msg": "matplotlib"}],
               ["ax.bar", "feature_importances_"], 3),
            ex(9, "python", "Предсказание вероятностей: model.predict_proba(X[:5]) в `probs`.",
               "import numpy as np\nfrom sklearn.tree import DecisionTreeClassifier\nnp.random.seed(42)\nn = 300\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nX = np.column_stack([kills, deaths, gold])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)\nmodel = DecisionTreeClassifier(max_depth=5, random_state=42).fit(X, y)\nprobs = np.array([])\n",
               "import numpy as np\nfrom sklearn.tree import DecisionTreeClassifier\nmodel = DecisionTreeClassifier(max_depth=5, random_state=42).fit(X, y)\nprobs = model.predict_proba(X[:5])",
               [{"check": "probs.shape == (5, 2)", "msg": "5x2"}],
               ["predict_proba"], 2),
            ex(10, "python", "Confusion matrix на test для дерева.",
               "import numpy as np\nfrom sklearn.tree import DecisionTreeClassifier\nfrom sklearn.metrics import confusion_matrix\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nn = 300\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nX = np.column_stack([kills, deaths, gold])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\ncm = None\n",
               "import numpy as np\nfrom sklearn.tree import DecisionTreeClassifier\nfrom sklearn.metrics import confusion_matrix\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\ny_pred = DecisionTreeClassifier(max_depth=5, random_state=42).fit(X_train, y_train).predict(X_test)\ncm = confusion_matrix(y_test, y_pred)",
               [{"check": "cm.shape == (2, 2)", "msg": "2x2"}],
               ["confusion_matrix"], 2),
        ],
        minutes=55, difficulty=3,
    )


def _7_9():
    return lesson(
        "7.9", "Random Forest", "mixed", [
            theory(
                "**Random Forest** — ансамбль деревьев, обученных на разных "
                "подвыборках. Идея: одно дерево шумит, 100 деревьев усредняют шум.\n\n"
                "**Bagging (Bootstrap Aggregating):** каждое дерево обучается на "
                "случайной подвыборке с возвращением (≈63% уникальных данных). "
                "**Random subspaces:** на каждом разбиении выбираем случайное подмножество "
                "фич (max_features).\n\n"
                "**Прогноз:** голосование большинством (классификация) или среднее (регрессия).\n\n"
                "**В sklearn:**\n"
                "- `RandomForestClassifier(n_estimators=100, max_depth=...)`\n"
                "- `RandomForestRegressor(n_estimators=100)`\n"
                "- `model.feature_importances_` — усреднённый по деревьям\n"
                "- `oob_score_` — score на out-of-bag данных (бесплатная валидация!)\n\n"
                "**Гиперпараметры:**\n"
                "- `n_estimators` — число деревьев (больше = стабильнее, но медленнее)\n"
                "- `max_features` — 'sqrt', 'log2', int\n"
                "- `min_samples_leaf` — минимум в листе\n"
                "- `bootstrap=True` — bagging\n\n"
                "**Плюсы:** мощный, не переобучается так сильно как одно дерево, "
                "**OOB-score** без валидации. **Минусы:** медленный, не интерпретируемый."
            ),
            analogy(
                "Random Forest — жюри присяжных: одно мнение шумное, 100 — мудрое. "
                "Каждый присяжный видел разные доказательства (bagging) и обращал внимание "
                "на разные улики (random subspaces).",
                "В Dota: 100 деревьев голосуют, выигрывает ли команда по gold, kills, deaths."
            ),
            visual(
                "Random Forest",
                "     Data →  ┌─Tree1─┐\n"
                "     │       └─┤pred1│  ──┐\n"
                "     ↓         └──────┘   │\n"
                "   [bootstrap]   ...     │ vote/avg → final\n"
                "     ↓         ┌──────┐   │\n"
                "     └────────→│Tree100│  ─┘\n"
                "               └──────┘\n"
                "   • bootstrap: 63% данных\n"
                "   • random subspaces: sqrt(n_features)"
            ),
            example(
                "RandomForestClassifier на Dota-данных.",
                "100 деревьев, max_depth=8.",
                "import numpy as np\n"
                "from sklearn.ensemble import RandomForestClassifier\n"
                "from sklearn.model_selection import train_test_split\n"
                "np.random.seed(42)\n"
                "n = 500\n"
                "kills = np.random.poisson(6, n)\n"
                "deaths = np.random.poisson(5, n)\n"
                "gold = np.random.normal(2000, 500, n)\n"
                "X = np.column_stack([kills, deaths, gold])\n"
                "y = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)\n"
                "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\n"
                "m = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42, n_jobs=-1).fit(X_tr, y_tr)\n"
                "print('test acc:', m.score(X_te, y_te))",
                "test acc: 0.92",
                "RF даёт 92% на test. Обычно RF стабильнее одиночного дерева на шумных данных."
            ),
            common_mistakes([
                {"mistake": "n_estimators=10", "why_bad": "Слишком шумно, нестабильно", "fix": "n_estimators=100..500"},
                {"mistake": "max_features=All фичей", "why_bad": "Теряется diversity", "fix": "max_features='sqrt'"},
                {"mistake": "n_jobs=1 на большом RF", "why_bad": "Долго", "fix": "n_jobs=-1 (все ядра)"},
                {"mistake": "Сравнивать с деревом на тех же данных", "why_bad": "Дерево переобучено, RF нет", "fix": "CV для обоих"},
            ]),
            interview_questions([
                {"q": "Почему Random Forest лучше дерева?", "a": "Bagging + random subspaces уменьшают variance. Усреднение 100 деревьев гасит шум каждого. Почти не переобучается при росте n_estimators."},
                {"q": "Что OOB-score?", "a": "Out-of-bag score. Каждое дерево не видело ~37% данных. На них и проверяется. Бесплатная валидация, нет нужды в отдельном val."},
                {"q": "Bagging vs Boosting?", "a": "Bagging: деревья параллельны, равные веса, уменьшает variance. Boosting: деревья последовательны, исправляют ошибки предыдущих, уменьшает bias."},
            ]),
            knowledge_checklist([
                "Обучаю RandomForest",
                "Понимаю bagging + random subspaces",
                "Использую oob_score",
                "Тюнинг n_estimators, max_features",
                "Сравниваю с одиночным деревом",
            ]),
        ],
        exercises=[
            ex(1, "python", "Dota-данные: 500 игроков, 4 фичи (kills, deaths, gold, assists). win в `y`. seed=42.",
               "import numpy as np\nX = np.array([])\ny = np.array([])\n",
               "import numpy as np\nnp.random.seed(42)\nn = 500\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nassists = np.random.poisson(7, n)\nX = np.column_stack([kills, deaths, gold, assists])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + 0.3*assists + np.random.randn(n) > 0).astype(int)",
               [{"check": "X.shape == (500, 4)", "msg": "500 строк, 4 фичи"}],
               ["4 фичи"], 1),
            ex(2, "python", "RandomForestClassifier(n_estimators=100, max_depth=8). test acc в `acc`.",
               "import numpy as np\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nn = 500\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nassists = np.random.poisson(7, n)\nX = np.column_stack([kills, deaths, gold, assists])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + 0.3*assists + np.random.randn(n) > 0).astype(int)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\nacc = 0\n",
               "import numpy as np\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\nacc = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42).fit(X_train, y_train).score(X_test, y_test)",
               [{"check": "acc > 0.7", "msg": "accuracy > 0.7"}],
               ["RandomForestClassifier"], 1),
            ex(3, "python", "RandomForestRegressor: predict winrate. test R² в `r2`.",
               "import numpy as np\nfrom sklearn.ensemble import RandomForestRegressor\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nn = 500\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nX = np.column_stack([kills, deaths, gold])\ny = (50 + 5*kills - 4*deaths + 0.005*gold + np.random.randn(n)*5)\nr2 = 0\n",
               "import numpy as np\nfrom sklearn.ensemble import RandomForestRegressor\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\nr2 = RandomForestRegressor(n_estimators=100, max_depth=8, random_state=42).fit(X_train, y_train).score(X_test, y_test)",
               [{"check": "r2 > 0.5", "msg": "R² > 0.5"}],
               ["RandomForestRegressor"], 2),
            ex(4, "python", "feature_importances_ в `importances`.",
               "import numpy as np\nfrom sklearn.ensemble import RandomForestClassifier\nnp.random.seed(42)\nn = 500\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nassists = np.random.poisson(7, n)\nX = np.column_stack([kills, deaths, gold, assists])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + 0.3*assists + np.random.randn(n) > 0).astype(int)\nmodel = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42).fit(X, y)\nimportances = np.array([])\n",
               "import numpy as np\nfrom sklearn.ensemble import RandomForestClassifier\nmodel = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42).fit(X, y)\nimportances = model.feature_importances_",
               [{"check": "importances.shape == (4,)", "msg": "4 фичи"},
                {"check": "abs(importances.sum() - 1.0) < 1e-6", "msg": "Сумма = 1"}],
               ["feature_importances_"], 1),
            ex(5, "python", "Сравни 10, 50, 200 деревьев. test_accs в `accs`.",
               "import numpy as np\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nn = 500\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nassists = np.random.poisson(7, n)\nX = np.column_stack([kills, deaths, gold, assists])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + 0.3*assists + np.random.randn(n) > 0).astype(int)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\naccs = np.array([])\n",
               "import numpy as np\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\naccs = np.array([RandomForestClassifier(n_estimators=n, max_depth=8, random_state=42).fit(X_train, y_train).score(X_test, y_test) for n in [10, 50, 200]])",
               [{"check": "accs.shape == (3,)", "msg": "3 точки"}],
               ["n_estimators в списке"], 3),
            ex(6, "python", "OOB-score: модель с oob_score=True. score_ в `oob`.",
               "import numpy as np\nfrom sklearn.ensemble import RandomForestClassifier\nnp.random.seed(42)\nn = 500\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nX = np.column_stack([kills, deaths, gold])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)\noob = 0\n",
               "import numpy as np\nfrom sklearn.ensemble import RandomForestClassifier\nnp.random.seed(42)\nm = RandomForestClassifier(n_estimators=100, max_depth=8, oob_score=True, random_state=42).fit(X, y)\noob = m.oob_score_",
               [{"check": "0.6 < oob < 1.0", "msg": "OOB > 0.6"}],
               ["oob_score_", "oob_score=True"], 3),
            ex(7, "python", "Cross-val 5-fold RF. mean в `cv`.",
               "import numpy as np\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.model_selection import cross_val_score\nnp.random.seed(42)\nn = 500\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nX = np.column_stack([kills, deaths, gold])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)\ncv = 0\n",
               "import numpy as np\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.model_selection import cross_val_score\nnp.random.seed(42)\ncv = cross_val_score(RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42), X, y, cv=5).mean()",
               [{"check": "0.6 < cv < 1.0", "msg": "CV > 0.6"}],
               ["cross_val_score"], 2),
            ex(8, "python", "predict_proba для теста. P(class=1) в `p1`.",
               "import numpy as np\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nn = 500\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nX = np.column_stack([kills, deaths, gold])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\nmodel = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42).fit(X_train, y_train)\np1 = np.array([])\n",
               "import numpy as np\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\nmodel = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42).fit(X_train, y_train)\np1 = model.predict_proba(X_test)[:, 1]",
               [{"check": "p1.shape == (100,)", "msg": "100 вероятностей"},
                {"check": "(p1 >= 0).all() and (p1 <= 1).all()", "msg": "[0, 1]"}],
               ["predict_proba", "[:, 1]"], 2),
            ex(9, "python", "Визуализируй feature_importances_ топ-3 фичи.",
               "import numpy as np\nimport matplotlib.pyplot as plt\nfrom sklearn.ensemble import RandomForestClassifier\nnp.random.seed(42)\nn = 500\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nassists = np.random.poisson(7, n)\nX = np.column_stack([kills, deaths, gold, assists])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + 0.3*assists + np.random.randn(n) > 0).astype(int)\nmodel = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42).fit(X, y)\nfig, ax = plt.subplots()\n",
               "import numpy as np\nimport matplotlib.pyplot as plt\nfrom sklearn.ensemble import RandomForestClassifier\nmodel = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42).fit(X, y)\nfig, ax = plt.subplots()\nlabels = ['kills', 'deaths', 'gold', 'assists']\nax.bar(labels, model.feature_importances_)\nax.set_title('RF feature importances')\nplt.close(fig)",
               [{"check": "True", "msg": "matplotlib"}],
               ["ax.bar"], 2),
            ex(10, "python", "Confusion matrix + classification report через f1_score.",
               "import numpy as np\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.metrics import confusion_matrix, f1_score\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nn = 500\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nX = np.column_stack([kills, deaths, gold])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\ncm = None\nf1 = 0\n",
               "import numpy as np\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.metrics import confusion_matrix, f1_score\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\ny_pred = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42).fit(X_train, y_train).predict(X_test)\ncm = confusion_matrix(y_test, y_pred)\nf1 = f1_score(y_test, y_pred)",
               [{"check": "cm.shape == (2, 2)", "msg": "2x2 cm"},
                {"check": "0 <= f1 <= 1", "msg": "F1 в [0, 1]"}],
               ["confusion_matrix", "f1_score"], 2),
        ],
        minutes=55, difficulty=3,
    )


def _7_10():
    return lesson(
        "7.10", "Gradient Boosting (XGBoost / LightGBM)", "mixed", [
            theory(
                "**Gradient Boosting** — ансамбль, где деревья обучаются **последовательно**, "
                "каждое исправляет ошибки предыдущего.\n\n"
                "**Алгоритм:**\n"
                "1. Инициализируем константой (среднее y для регрессии)\n"
                "2. Считаем **остатки** (residuals) = y - y_pred\n"
                "3. Обучаем дерево предсказывать **остатки**\n"
                "4. Обновляем прогноз: y_pred += learning_rate * tree.predict(X)\n"
                "5. Повторяем N раз\n\n"
                "**Ключевые гиперпараметры:**\n"
                "- `n_estimators` — число деревьев (100..2000)\n"
                "- `learning_rate` (η) — шаг (0.01..0.3)\n"
                "- `max_depth` — глубина деревьев (3..8)\n"
                "- `subsample` — доля данных на каждое дерево\n"
                "- **Tradeoff:** меньше lr → больше деревьев → лучше, но медленнее\n\n"
                "**Реализации:**\n"
                "- **sklearn.GradientBoostingClassifier/Regressor** — классика, медленнее\n"
                "- **XGBoost** — быстрее, регуляризация, GPU\n"
                "- **LightGBM** — ещё быстрее, leaf-wise рост\n"
                "- **CatBoost** — категориальные фичи из коробки\n\n"
                "**Плюсы:** топ-1 на Kaggle. **Минусы:** переобучается, тюнинг долгий, "
                "неинтерпретируемый (но есть SHAP)."
            ),
            analogy(
                "GB — ученик, который решает задачи, помечает ошибки, потом целенаправленно "
                "тренирует именно эти ошибки. Каждое дерево — небольшой рывок к истине.",
                "В Dota: первое дерево грубо предсказывает win, следующие уточняют на матчах, "
                "где ошибся."
            ),
            visual(
                "Gradient Boosting",
                "   y_pred = 0\n"
                "      ↓\n"
                "   res = y - y_pred\n"
                "      ↓\n"
                "   ┌─Tree1(res)─┐\n"
                "   │            ↓\n"
                "   │  y_pred += lr*T1\n"
                "   │            ↓\n"
                "   │  res = y - y_pred\n"
                "   └─Tree2(res)──→ ... → final"
            ),
            example(
                "GradientBoostingClassifier на Dota-данных.",
                "100 деревьев, lr=0.1, max_depth=3.",
                "import numpy as np\n"
                "from sklearn.ensemble import GradientBoostingClassifier\n"
                "from sklearn.model_selection import train_test_split\n"
                "np.random.seed(42)\n"
                "n = 500\n"
                "kills = np.random.poisson(6, n)\n"
                "deaths = np.random.poisson(5, n)\n"
                "gold = np.random.normal(2000, 500, n)\n"
                "X = np.column_stack([kills, deaths, gold])\n"
                "y = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)\n"
                "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\n"
                "m = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42).fit(X_tr, y_tr)\n"
                "print('test acc:', m.score(X_te, y_te))\n"
                "print('feat imp:', m.feature_importances_)",
                "test acc: 0.93\nfeat imp: [0.42 0.49 0.09]",
                "GB даёт 93% — обычно чуть лучше RF на чистых данных. kills и deaths — главные."
            ),
            common_mistakes([
                {"mistake": "n_estimators=1000 без контроля", "why_bad": "Переобучение", "fix": "lr=0.05, n_estimators=200, CV"},
                {"mistake": "lr=1.0", "why_bad": "Грубые шаги, не сходится", "fix": "lr=0.05..0.2"},
                {"mistake": "max_depth=20", "why_bad": "Сложные деревья, overfit", "fix": "max_depth=3..6"},
                {"mistake": "Не использовать early stopping", "why_bad": "Теряется лучшая итерация", "fix": "staged_predict + val"},
            ]),
            interview_questions([
                {"q": "GB vs RF?", "a": "RF: деревья параллельны, bagging, уменьшает variance. GB: деревья последовательны, каждое исправляет ошибки, уменьшает bias. GB обычно точнее, RF стабильнее."},
                {"q": "Зачем learning_rate?", "a": "Контролирует шаг: y_pred += lr * tree_pred. Маленький lr (0.01..0.1) → стабильнее, нужно больше деревьев. Большой lr (0.3+) → быстрее, но риск overfit."},
                {"q": "XGBoost vs LightGBM?", "a": "XGBoost: level-wise рост, регуляризация, GPU. LightGBM: leaf-wise, гистограммы, быстрее на больших данных. LightGBM на 1M+ строк быстрее в 5-10x."},
            ]),
            knowledge_checklist([
                "Понимаю идею sequential ensemble",
                "Тюнинг lr, n_estimators, max_depth",
                "Сравниваю с Random Forest",
                "Знаю XGBoost/LightGBM",
                "Использую staged_predict",
            ]),
        ],
        exercises=[
            ex(1, "python", "Dota-данные: 500 игроков, 3 фичи. win в `y`. seed=42.",
               "import numpy as np\nX = np.array([])\ny = np.array([])\n",
               "import numpy as np\nnp.random.seed(42)\nn = 500\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nX = np.column_stack([kills, deaths, gold])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)",
               [{"check": "X.shape == (500, 3)", "msg": "500x3"}],
               ["3 фичи"], 1),
            ex(2, "python", "GradientBoostingClassifier(100, lr=0.1, depth=3). test acc в `acc`.",
               "import numpy as np\nfrom sklearn.ensemble import GradientBoostingClassifier\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nn = 500\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nX = np.column_stack([kills, deaths, gold])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\nacc = 0\n",
               "import numpy as np\nfrom sklearn.ensemble import GradientBoostingClassifier\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\nacc = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42).fit(X_train, y_train).score(X_test, y_test)",
               [{"check": "acc > 0.7", "msg": "acc > 0.7"}],
               ["GradientBoostingClassifier"], 1),
            ex(3, "python", "GradientBoostingRegressor: предсказать winrate. test R² в `r2`.",
               "import numpy as np\nfrom sklearn.ensemble import GradientBoostingRegressor\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nn = 500\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nX = np.column_stack([kills, deaths, gold])\ny = (50 + 5*kills - 4*deaths + 0.005*gold + np.random.randn(n)*5)\nr2 = 0\n",
               "import numpy as np\nfrom sklearn.ensemble import GradientBoostingRegressor\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\nr2 = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42).fit(X_train, y_train).score(X_test, y_test)",
               [{"check": "r2 > 0.5", "msg": "R² > 0.5"}],
               ["GradientBoostingRegressor"], 2),
            ex(4, "python", "feature_importances_ в `imp`.",
               "import numpy as np\nfrom sklearn.ensemble import GradientBoostingClassifier\nnp.random.seed(42)\nn = 500\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nX = np.column_stack([kills, deaths, gold])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)\nimp = np.array([])\n",
               "import numpy as np\nfrom sklearn.ensemble import GradientBoostingClassifier\nimp = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42).fit(X, y).feature_importances_",
               [{"check": "imp.shape == (3,)", "msg": "3 фичи"}],
               ["feature_importances_"], 1),
            ex(5, "python", "staged_predict: accuracy на каждой итерации. Последнее значение в `final_acc`.",
               "import numpy as np\nfrom sklearn.ensemble import GradientBoostingClassifier\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nn = 500\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nX = np.column_stack([kills, deaths, gold])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\nfinal_acc = 0\n",
               "import numpy as np\nfrom sklearn.ensemble import GradientBoostingClassifier\nfrom sklearn.metrics import accuracy_score\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\nm = GradientBoostingClassifier(n_estimators=50, learning_rate=0.1, max_depth=3, random_state=42).fit(X_train, y_train)\naccs = [accuracy_score(y_test, list(p)) for p in m.staged_predict(X_test)]\nfinal_acc = accs[-1]",
               [{"check": "final_acc > 0.6", "msg": "final > 0.6"}],
               ["staged_predict"], 3),
            ex(6, "python", "Сравни 3 lr: 0.01, 0.1, 0.5. accs в `accs`.",
               "import numpy as np\nfrom sklearn.ensemble import GradientBoostingClassifier\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nn = 500\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nX = np.column_stack([kills, deaths, gold])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\naccs = np.array([])\n",
               "import numpy as np\nfrom sklearn.ensemble import GradientBoostingClassifier\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\naccs = np.array([GradientBoostingClassifier(n_estimators=100, learning_rate=lr, max_depth=3, random_state=42).fit(X_train, y_train).score(X_test, y_test) for lr in [0.01, 0.1, 0.5]])",
               [{"check": "accs.shape == (3,)", "msg": "3 lr"}],
               ["list comprehension по lr"], 3),
            ex(7, "python", "Cross-val 5-fold GB. mean в `cv`.",
               "import numpy as np\nfrom sklearn.ensemble import GradientBoostingClassifier\nfrom sklearn.model_selection import cross_val_score\nnp.random.seed(42)\nn = 500\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nX = np.column_stack([kills, deaths, gold])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)\ncv = 0\n",
               "import numpy as np\nfrom sklearn.ensemble import GradientBoostingClassifier\nfrom sklearn.model_selection import cross_val_score\nnp.random.seed(42)\ncv = cross_val_score(GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42), X, y, cv=5).mean()",
               [{"check": "0.6 < cv < 1.0", "msg": "CV > 0.6"}],
               ["cross_val_score"], 2),
            ex(8, "python", "predict_proba для теста. P(class=1) в `p1`.",
               "import numpy as np\nfrom sklearn.ensemble import GradientBoostingClassifier\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nn = 500\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nX = np.column_stack([kills, deaths, gold])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\nmodel = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42).fit(X_train, y_train)\np1 = np.array([])\n",
               "import numpy as np\nfrom sklearn.ensemble import GradientBoostingClassifier\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\nmodel = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42).fit(X_train, y_train)\np1 = model.predict_proba(X_test)[:, 1]",
               [{"check": "p1.shape == (100,)", "msg": "100 вероятностей"}],
               ["predict_proba", "[:, 1]"], 2),
            ex(9, "python", "Визуализируй кривую обучения GB по staged_predict.",
               "import numpy as np\nimport matplotlib.pyplot as plt\nfrom sklearn.ensemble import GradientBoostingClassifier\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import accuracy_score\nnp.random.seed(42)\nn = 500\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nX = np.column_stack([kills, deaths, gold])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\nfig, ax = plt.subplots()\n",
               "import numpy as np\nimport matplotlib.pyplot as plt\nfrom sklearn.ensemble import GradientBoostingClassifier\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import accuracy_score\nnp.random.seed(42)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\nm = GradientBoostingClassifier(n_estimators=50, learning_rate=0.1, max_depth=3, random_state=42).fit(X_train, y_train)\naccs = [accuracy_score(y_test, list(p)) for p in m.staged_predict(X_test)]\nfig, ax = plt.subplots()\nax.plot(range(1, len(accs) + 1), accs, marker='o')\nax.set_xlabel('iterations'); ax.set_ylabel('test acc')\nax.set_title('GB staged_predict')\nplt.close(fig)",
               [{"check": "True", "msg": "matplotlib"}],
               ["staged_predict", "ax.plot"], 3),
            ex(10, "python", "F1 на test в `f1`.",
               "import numpy as np\nfrom sklearn.ensemble import GradientBoostingClassifier\nfrom sklearn.metrics import f1_score\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nn = 500\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nX = np.column_stack([kills, deaths, gold])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\nf1 = 0\n",
               "import numpy as np\nfrom sklearn.ensemble import GradientBoostingClassifier\nfrom sklearn.metrics import f1_score\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\ny_pred = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42).fit(X_train, y_train).predict(X_test)\nf1 = f1_score(y_test, y_pred)",
               [{"check": "0 <= f1 <= 1", "msg": "F1 в [0, 1]"}],
               ["f1_score"], 2),
        ],
        minutes=55, difficulty=3,
    )


def _7_11():
    return lesson(
        "7.11", "K-Means кластеризация", "mixed", [
            theory(
                "**K-Means** — самый популярный алгоритм кластеризации. Делит данные на "
                "k кластеров, минимизируя сумму квадратов расстояний до центроидов.\n\n"
                "**Алгоритм (Lloyd):**\n"
                "1. Инициализируем k центроидов (k-means++ в sklearn)\n"
                "2. Каждой точке — ближайший кластер\n"
                "3. Пересчитываем центроиды как среднее точек кластера\n"
                "4. Повторяем 2-3 до сходимости\n\n"
                "**В sklearn:**\n"
                "- `KMeans(n_clusters=3, init='k-means++', n_init=10)`\n"
                "- `model.cluster_centers_` — центроиды (k, n_features)\n"
                "- `model.labels_` — метки кластеров (n,)\n"
                "- `model.inertia_` — сумма квадратов расстояний (меньше = лучше)\n"
                "- `model.predict(X)` — кластер новой точки\n\n"
                "**Выбор k — elbow method:** строим inertia vs k, ищем «локоть».\n"
                "**Silhouette score** ∈ [-1, 1] — качество кластеризации.\n\n"
                "**Когда использовать:**\n"
                "- Заранее известно примерное k\n"
                "- Кластеры сферические, одинакового размера\n"
                "- Масштабируемые фичи (StandardScaler!)\n\n"
                "**Минусы:** нужно задавать k, чувствителен к выбросам, "
                "только сферические кластеры."
            ),
            analogy(
                "K-Means — расселение туристов в k отелей. Каждый идёт в ближайший, "
                "отель переезжает в центр своих постояльцев, повтор.",
                "Сегментация Dota-игроков: k=3 — carry/support/mid. Или: 4 архетипа — "
                "агрессивные/пассивные/балансные/рандомные."
            ),
            visual(
                "K-Means шаги",
                "   iter 1:    ● ● ●           iter 3:  ●  ●  ●\n"
                "              ● ●  ●                  ●  ●  ●\n"
                "             +c1 ● +c2              ⊙   ⊙  ⊙\n"
                "               ●  ●                centroid\n"
                "   Точки → ближайший centroid → новый centroid → ..."
            ),
            example(
                "K-Means на 3 кластерах.",
                "3 группы игроков по KDR.",
                "import numpy as np\n"
                "from sklearn.cluster import KMeans\n"
                "np.random.seed(42)\n"
                "c1 = np.random.normal(0, 0.5, (50, 2))\n"
                "c2 = np.random.normal(5, 0.5, (50, 2))\n"
                "c3 = np.random.normal([10, 5], 0.5, (50, 2))\n"
                "X = np.vstack([c1, c2, c3])\n"
                "km = KMeans(n_clusters=3, random_state=42, n_init=10).fit(X)\n"
                "print('centers shape:', km.cluster_centers_.shape)\n"
                "print('labels unique:', np.unique(km.labels_))\n"
                "print('inertia:', km.inertia_)",
                "centers shape: (3, 2)\nlabels unique: [0 1 2]\ninertia: 144.5",
                "3 центроида, метки 0/1/2, inertia (sum of squared distances) ≈ 144.5."
            ),
            common_mistakes([
                {"mistake": "K-Means на разных масштабах", "why_bad": "kill_count vs gold доминируют по-разному", "fix": "StandardScaler до кластеризации"},
                {"mistake": "n_clusters=2 без анализа", "why_bad": "Неизвестно реальное число кластеров", "fix": "Elbow + silhouette"},
                {"mistake": "n_init=1 (по умолчанию до 1.4)", "why_bad": "Случайная инициализация влияет", "fix": "n_init=10"},
                {"mistake": "K-Means на не-выпуклых кластерах", "why_bad": "Алгоритм заточен на сферы", "fix": "DBSCAN, spectral"},
            ]),
            interview_questions([
                {"q": "Как работает K-Means?", "a": "Итеративно: назначаем точки ближайшему центроиду, пересчитываем центроиды как среднее. Сходится за O(nki) итераций. Минимизирует inertia = sum ||x_i - centroid||²."},
                {"q": "Как выбрать k?", "a": "Elbow method: строишь inertia vs k, ищешь 'локоть'. Silhouette score ∈ [-1, 1] — чем ближе к 1, тем лучше разделение. Также бизнес-смысл (3 архетипа игроков)."},
                {"q": "K-Means vs DBSCAN?", "a": "K-Means: фиксированное k, только выпуклые кластеры, быстрый. DBSCAN: автоматически определяет число кластеров, находит выбросы, но медленнее и нужно ε, min_samples."},
            ]),
            knowledge_checklist([
                "Обучаю KMeans",
                "Использую k-means++ и n_init",
                "Строю elbow plot",
                "Считаю silhouette score",
                "Масштабирую фичи до кластеризации",
                "Интерпретирую inertia",
            ]),
        ],
        exercises=[
            ex(1, "python", "3 кластера: 50 точек, mean=[0,0], [5,5], [10,0], seed=42.",
               "import numpy as np\nX = np.array([])\n",
               "import numpy as np\nnp.random.seed(42)\nc1 = np.random.normal(0, 0.5, (50, 2))\nc2 = np.random.normal(5, 0.5, (50, 2))\nc3 = np.random.normal([10, 0], 0.5, (50, 2))\nX = np.vstack([c1, c2, c3])",
               [{"check": "X.shape == (150, 2)", "msg": "150 точек"}],
               ["3 vstacked кластера"], 1),
            ex(2, "python", "KMeans(n_clusters=3). labels в `labels`.",
               "import numpy as np\nfrom sklearn.cluster import KMeans\nnp.random.seed(42)\nc1 = np.random.normal(0, 0.5, (50, 2))\nc2 = np.random.normal(5, 0.5, (50, 2))\nc3 = np.random.normal([10, 0], 0.5, (50, 2))\nX = np.vstack([c1, c2, c3])\nlabels = np.array([])\n",
               "import numpy as np\nfrom sklearn.cluster import KMeans\nlabels = KMeans(n_clusters=3, random_state=42, n_init=10).fit(X).labels_",
               [{"check": "labels.shape == (150,)", "msg": "150 меток"},
                {"check": "set(labels.tolist()) == {0, 1, 2}", "msg": "3 кластера"}],
               ["KMeans(n_clusters=3)"], 1),
            ex(3, "python", "cluster_centers_ в `centers`.",
               "import numpy as np\nfrom sklearn.cluster import KMeans\nnp.random.seed(42)\nc1 = np.random.normal(0, 0.5, (50, 2))\nc2 = np.random.normal(5, 0.5, (50, 2))\nc3 = np.random.normal([10, 0], 0.5, (50, 2))\nX = np.vstack([c1, c2, c3])\ncenters = np.array([])\n",
               "import numpy as np\nfrom sklearn.cluster import KMeans\ncenters = KMeans(n_clusters=3, random_state=42, n_init=10).fit(X).cluster_centers_",
               [{"check": "centers.shape == (3, 2)", "msg": "3 центроида, 2D"}],
               ["cluster_centers_"], 1),
            ex(4, "python", "inertia_ в `inertia`.",
               "import numpy as np\nfrom sklearn.cluster import KMeans\nnp.random.seed(42)\nc1 = np.random.normal(0, 0.5, (50, 2))\nc2 = np.random.normal(5, 0.5, (50, 2))\nc3 = np.random.normal([10, 0], 0.5, (50, 2))\nX = np.vstack([c1, c2, c3])\ninertia = 0\n",
               "import numpy as np\nfrom sklearn.cluster import KMeans\ninertia = KMeans(n_clusters=3, random_state=42, n_init=10).fit(X).inertia_",
               [{"check": "inertia > 0", "msg": "inertia > 0"}],
               ["inertia_"], 1),
            ex(5, "python", "Elbow plot: inertia для k=1..6. inertias в `inertias`.",
               "import numpy as np\nfrom sklearn.cluster import KMeans\nnp.random.seed(42)\nc1 = np.random.normal(0, 0.5, (50, 2))\nc2 = np.random.normal(5, 0.5, (50, 2))\nc3 = np.random.normal([10, 0], 0.5, (50, 2))\nX = np.vstack([c1, c2, c3])\ninertias = np.array([])\n",
               "import numpy as np\nfrom sklearn.cluster import KMeans\nnp.random.seed(42)\ninertias = np.array([KMeans(n_clusters=k, random_state=42, n_init=10).fit(X).inertia_ for k in range(1, 7)])",
               [{"check": "inertias.shape == (6,)", "msg": "6 k"},
                {"check": "all(inertias[i] > inertias[i+1] for i in range(5))", "msg": "Inertia убывает"}],
               ["list comprehension по k"], 2),
            ex(6, "python", "Elbow plot matplotlib.",
               "import numpy as np\nimport matplotlib.pyplot as plt\nfrom sklearn.cluster import KMeans\nnp.random.seed(42)\nc1 = np.random.normal(0, 0.5, (50, 2))\nc2 = np.random.normal(5, 0.5, (50, 2))\nc3 = np.random.normal([10, 0], 0.5, (50, 2))\nX = np.vstack([c1, c2, c3])\nfig, ax = plt.subplots()\n",
               "import numpy as np\nimport matplotlib.pyplot as plt\nfrom sklearn.cluster import KMeans\nnp.random.seed(42)\ninertias = [KMeans(n_clusters=k, random_state=42, n_init=10).fit(X).inertia_ for k in range(1, 7)]\nfig, ax = plt.subplots()\nax.plot(range(1, 7), inertias, marker='o')\nax.set_xlabel('k'); ax.set_ylabel('inertia'); ax.set_title('Elbow')\nplt.close(fig)",
               [{"check": "True", "msg": "matplotlib"}],
               ["ax.plot", "inertia"], 2),
            ex(7, "python", "predict для новых 3 точек в `preds`.",
               "import numpy as np\nfrom sklearn.cluster import KMeans\nnp.random.seed(42)\nc1 = np.random.normal(0, 0.5, (50, 2))\nc2 = np.random.normal(5, 0.5, (50, 2))\nc3 = np.random.normal([10, 0], 0.5, (50, 2))\nX = np.vstack([c1, c2, c3])\nmodel = KMeans(n_clusters=3, random_state=42, n_init=10).fit(X)\nX_new = np.array([[0, 0], [5, 5], [10, 0]])\npreds = np.array([])\n",
               "import numpy as np\nfrom sklearn.cluster import KMeans\nmodel = KMeans(n_clusters=3, random_state=42, n_init=10).fit(X)\npreds = model.predict(X_new)",
               [{"check": "preds.shape == (3,)", "msg": "3 предсказания"},
                {"check": "set(preds.tolist()) == {0, 1, 2}", "msg": "3 разных кластера"}],
               ["model.predict"], 2),
            ex(8, "python", "Silhouette score для k=3. score в `sil`.",
               "import numpy as np\nfrom sklearn.cluster import KMeans\nfrom sklearn.metrics import silhouette_score\nnp.random.seed(42)\nc1 = np.random.normal(0, 0.5, (50, 2))\nc2 = np.random.normal(5, 0.5, (50, 2))\nc3 = np.random.normal([10, 0], 0.5, (50, 2))\nX = np.vstack([c1, c2, c3])\nsil = 0\n",
               "import numpy as np\nfrom sklearn.cluster import KMeans\nfrom sklearn.metrics import silhouette_score\nnp.random.seed(42)\nlabels = KMeans(n_clusters=3, random_state=42, n_init=10).fit(X).labels_\nsil = silhouette_score(X, labels)",
               [{"check": "0.4 < sil < 1.0", "msg": "silhouette > 0.4 — хорошее разделение"}],
               ["silhouette_score"], 3),
            ex(9, "python", "Визуализируй кластеры + центроиды.",
               "import numpy as np\nimport matplotlib.pyplot as plt\nfrom sklearn.cluster import KMeans\nnp.random.seed(42)\nc1 = np.random.normal(0, 0.5, (50, 2))\nc2 = np.random.normal(5, 0.5, (50, 2))\nc3 = np.random.normal([10, 0], 0.5, (50, 2))\nX = np.vstack([c1, c2, c3])\nfig, ax = plt.subplots()\n",
               "import numpy as np\nimport matplotlib.pyplot as plt\nfrom sklearn.cluster import KMeans\nnp.random.seed(42)\nkm = KMeans(n_clusters=3, random_state=42, n_init=10).fit(X)\nfig, ax = plt.subplots()\nax.scatter(X[:, 0], X[:, 1], c=km.labels_, cmap='viridis', s=10)\nax.scatter(km.cluster_centers_[:, 0], km.cluster_centers_[:, 1], c='red', marker='X', s=200, label='centroids')\nax.legend()\nax.set_title('KMeans clusters')\nplt.close(fig)",
               [{"check": "True", "msg": "matplotlib"}],
               ["ax.scatter", "centers_"], 2),
            ex(10, "python", "Подсчёт точек в каждом кластере. counts в `counts`.",
               "import numpy as np\nfrom sklearn.cluster import KMeans\nnp.random.seed(42)\nc1 = np.random.normal(0, 0.5, (50, 2))\nc2 = np.random.normal(5, 0.5, (50, 2))\nc3 = np.random.normal([10, 0], 0.5, (50, 2))\nX = np.vstack([c1, c2, c3])\nlabels = KMeans(n_clusters=3, random_state=42, n_init=10).fit(X).labels_\ncounts = np.array([])\n",
               "import numpy as np\nfrom sklearn.cluster import KMeans\nlabels = KMeans(n_clusters=3, random_state=42, n_init=10).fit(X).labels_\ncounts = np.bincount(labels)",
               [{"check": "counts.shape == (3,)", "msg": "3 кластера"},
                {"check": "counts.sum() == 150", "msg": "Всего 150"}],
               ["np.bincount"], 2),
        ],
        minutes=55, difficulty=3,
    )


def _7_12():
    return lesson(
        "7.12", "Интерпретация моделей: feature importance, SHAP", "mixed", [
            theory(
                "**Интерпретация моделей (XAI)** — почему модель выдала такой прогноз? "
                "Особенно важно для «чёрных ящиков» (RF, XGBoost, нейросети).\n\n"
                "**1. Feature importance (встроенная):**\n"
                "- `model.feature_importances_` — сумма уменьшений impurity по фиче\n"
                "- Доступно для деревьев и ансамблей\n"
                "- Глобальная: какие фичи важны в целом\n\n"
                "**2. Permutation importance:**\n"
                "- Перемешиваем одну фичу → score падает → важная\n"
                "- `sklearn.inspection.permutation_importance`\n"
                "- Лучше, чем impurity-based, т.к. не переоценивает high-cardinality\n\n"
                "**3. SHAP (SHapley Additive exPlanations):**\n"
                "- Базируется на теории Шепли (кооперативные игры)\n"
                "- Приписывает каждой фиче вклад в конкретный прогноз\n"
                "- **Локальная** интерпретация: почему ЭТОМУ игроку предсказали win\n"
                "- `shap.TreeExplainer(model).shap_values(X)`\n\n"
                "**4. LIME** — локальная аппроксимация линейной моделью.\n\n"
                "**Когда что:**\n"
                "- Глобально: feature_importances_ + permutation\n"
                "- Локально: SHAP\n"
                "- Линейные модели: coef_ + intercept_"
            ),
            analogy(
                "SHAP — налоговая декларация: сколько каждый фактор «заплатил» в итог. "
                "Уверенность = базовая + wins_due_to_kills + wins_due_to_gold + …",
                "В Dota: SHAP объясняет, что именно «сделало» win: +0.3 за kills, -0.1 за deaths."
            ),
            visual(
                "SHAP waterfall",
                "   E[f(X)] = 0.5          ← base value\n"
                "   kills=8    +0.20    ┐\n"
                "   deaths=3   +0.15     │\n"
                "   gold=2500  +0.05     ├─→ f(x) = 0.85\n"
                "   assists=2  -0.05    ┘\n"
                "   final: 0.85"
            ),
            example(
                "Feature importances для RF + permutation importance.",
                "Сравни два метода.",
                "import numpy as np\n"
                "from sklearn.ensemble import RandomForestClassifier\n"
                "from sklearn.inspection import permutation_importance\n"
                "np.random.seed(42)\n"
                "n = 300\n"
                "kills = np.random.poisson(6, n)\n"
                "deaths = np.random.poisson(5, n)\n"
                "noise = np.random.randn(n)\n"
                "X = np.column_stack([kills, deaths, noise])\n"
                "y = (1.5*kills - 1.2*deaths + np.random.randn(n) > 0).astype(int)\n"
                "m = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42).fit(X, y)\n"
                "pi = permutation_importance(m, X, y, random_state=42, n_repeats=5)\n"
                "print('impurity:', m.feature_importances_)\n"
                "print('perm imp:', pi.importances_mean)",
                "impurity: [0.46 0.50 0.04]\nperm imp: [0.16 0.18 0.01]",
                "Оба метода показывают: deaths важнее kills, noise почти не важен. "
                "Permutation даёт абсолютные значения (насколько падает score)."
            ),
            common_mistakes([
                {"mistake": "Сравнивать importances между моделями", "why_bad": "Разные шкалы", "fix": "Нормализовать, смотреть ранг"},
                {"mistake": "Доверять impurity importance", "why_bad": "Переоценивает high-cardinality фичи", "fix": "permutation_importance"},
                {"mistake": "SHAP на маленькой выборке", "why_bad": "TreeExplainer медленный", "fix": "Выборка 100..1000 точек"},
                {"mistake": "Локальная интерпретация как глобальная", "why_bad": "Один игрок ≠ все", "fix": "SHAP summary plot для популяции"},
            ]),
            interview_questions([
                {"q": "Что такое SHAP?", "a": "Метод на основе теории Шепли: распределяет «вклад» в прогноз между фичами. Свойства: local accuracy, missingness, consistency. TreeSHAP — быстрая версия для деревьев."},
                {"q": "feature_importances_ vs permutation?", "a": "feature_importances_ — сумма уменьшений impurity, считается на train. Permutation — падение score при перемешивании, на val. Permutation медленнее, но честнее, не любит high-cardinality."},
                {"q": "Как объяснить один прогноз?", "a": "SHAP force_plot или waterfall. LIME: локально аппроксимируем линейной моделью. Для линейных: просто coef*x + intercept, посмотреть вклад фич."},
            ]),
            knowledge_checklist([
                "Читаю feature_importances_",
                "Использую permutation_importance",
                "Понимаю идею SHAP",
                "Различаю локальную и глобальную интерпретацию",
                "Строю summary plot",
            ]),
        ],
        exercises=[
            ex(1, "python", "Dota-данные: 300 игроков, 4 фичи. win в `y`. seed=42.",
               "import numpy as np\nX = np.array([])\ny = np.array([])\n",
               "import numpy as np\nnp.random.seed(42)\nn = 300\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nnoise = np.random.randn(n)\nX = np.column_stack([kills, deaths, gold, noise])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)",
               [{"check": "X.shape == (300, 4)", "msg": "300x4"}],
               ["4 фичи"], 1),
            ex(2, "python", "RF feature_importances_ в `imp`.",
               "import numpy as np\nfrom sklearn.ensemble import RandomForestClassifier\nnp.random.seed(42)\nn = 300\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nnoise = np.random.randn(n)\nX = np.column_stack([kills, deaths, gold, noise])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)\nimp = np.array([])\n",
               "import numpy as np\nfrom sklearn.ensemble import RandomForestClassifier\nimp = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42).fit(X, y).feature_importances_",
               [{"check": "imp.shape == (4,)", "msg": "4 фичи"}],
               ["feature_importances_"], 1),
            ex(3, "python", "Permutation importance. importances_mean в `perm_imp`.",
               "import numpy as np\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.inspection import permutation_importance\nnp.random.seed(42)\nn = 300\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nnoise = np.random.randn(n)\nX = np.column_stack([kills, deaths, gold, noise])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)\nperm_imp = np.array([])\n",
               "import numpy as np\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.inspection import permutation_importance\nnp.random.seed(42)\nm = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42).fit(X, y)\nperm_imp = permutation_importance(m, X, y, random_state=42, n_repeats=5).importances_mean",
               [{"check": "perm_imp.shape == (4,)", "msg": "4 фичи"}],
               ["permutation_importance"], 2),
            ex(4, "python", "Найди индекс самой важной фичи (по permutation) в `top_idx`.",
               "import numpy as np\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.inspection import permutation_importance\nnp.random.seed(42)\nn = 300\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nnoise = np.random.randn(n)\nX = np.column_stack([kills, deaths, gold, noise])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)\ntop_idx = 0\n",
               "import numpy as np\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.inspection import permutation_importance\nnp.random.seed(42)\nm = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42).fit(X, y)\nperm_imp = permutation_importance(m, X, y, random_state=42, n_repeats=5).importances_mean\ntop_idx = int(np.argmax(perm_imp))",
               [{"check": "top_idx in [0, 1, 2, 3]", "msg": "Valid index"}],
               ["np.argmax"], 2),
            ex(5, "python", "LinearRegression: coef_ в `coef`. Самая важная фича — наибольший |coef|.",
               "import numpy as np\nfrom sklearn.linear_model import LinearRegression\nnp.random.seed(42)\nn = 300\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nnoise = np.random.randn(n)\nX = np.column_stack([kills, deaths, gold, noise])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n))\ncoef = np.array([])\n",
               "import numpy as np\nfrom sklearn.linear_model import LinearRegression\ncoef = LinearRegression().fit(X, y).coef_",
               [{"check": "coef.shape == (4,)", "msg": "4 веса"}],
               ["LinearRegression().coef_"], 1),
            ex(6, "python", "Визуализируй feature importances баром (RF).",
               "import numpy as np\nimport matplotlib.pyplot as plt\nfrom sklearn.ensemble import RandomForestClassifier\nnp.random.seed(42)\nn = 300\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nnoise = np.random.randn(n)\nX = np.column_stack([kills, deaths, gold, noise])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)\nfig, ax = plt.subplots()\n",
               "import numpy as np\nimport matplotlib.pyplot as plt\nfrom sklearn.ensemble import RandomForestClassifier\nmodel = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42).fit(X, y)\nfig, ax = plt.subplots()\nax.bar(['kills', 'deaths', 'gold', 'noise'], model.feature_importances_)\nax.set_title('Feature importances')\nplt.close(fig)",
               [{"check": "True", "msg": "matplotlib"}],
               ["ax.bar"], 2),
            ex(7, "python", "Сравни: impurity vs permutation importances. deltas в `deltas`.",
               "import numpy as np\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.inspection import permutation_importance\nnp.random.seed(42)\nn = 300\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nnoise = np.random.randn(n)\nX = np.column_stack([kills, deaths, gold, noise])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)\ndeltas = np.array([])\n",
               "import numpy as np\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.inspection import permutation_importance\nnp.random.seed(42)\nm = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42).fit(X, y)\nimp = m.feature_importances_\nperm = permutation_importance(m, X, y, random_state=42, n_repeats=5).importances_mean\ndeltas = imp - perm",
               [{"check": "deltas.shape == (4,)", "msg": "4 фичи"}],
               ["element-wise разница"], 2),
            ex(8, "python", "LogisticRegression: coef_[0] в `coef`. Это «логистические важности».",
               "import numpy as np\nfrom sklearn.linear_model import LogisticRegression\nnp.random.seed(42)\nn = 300\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nX = np.column_stack([kills, deaths, gold])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)\ncoef = np.array([])\n",
               "import numpy as np\nfrom sklearn.linear_model import LogisticRegression\ncoef = LogisticRegression().fit(X, y).coef_[0]",
               [{"check": "coef.shape == (3,)", "msg": "3 веса"},
                {"check": "coef[1] < 0", "msg": "deaths отрицательно → меньше шансов win"}],
               ["coef_[0]"], 2),
            ex(9, "python", "Predict + predict_proba для одного игрока — сохрани класс и вероятность.",
               "import numpy as np\nfrom sklearn.ensemble import RandomForestClassifier\nnp.random.seed(42)\nn = 300\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nX = np.column_stack([kills, deaths, gold])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)\nmodel = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42).fit(X, y)\nplayer = np.array([[10, 3, 3000]])\npred = 0\nprob = 0\n",
               "import numpy as np\nfrom sklearn.ensemble import RandomForestClassifier\nmodel = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42).fit(X, y)\nplayer = np.array([[10, 3, 3000]])\npred = model.predict(player)[0]\nprob = model.predict_proba(player)[0, 1]",
               [{"check": "pred in [0, 1]", "msg": "Бинарный класс"},
                {"check": "0 <= prob <= 1", "msg": "Вероятность"}],
               ["predict", "predict_proba"], 2),
            ex(10, "python", "Симулируй SHAP-вклад: weights * (x - mean) для каждой фичи. contribs в `contribs`.",
               "import numpy as np\nfrom sklearn.linear_model import LinearRegression\nnp.random.seed(42)\nn = 300\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nX = np.column_stack([kills, deaths, gold])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n))\ncontribs = np.array([])\n",
               "import numpy as np\nfrom sklearn.linear_model import LinearRegression\nm = LinearRegression().fit(X, y)\nplayer = np.array([10, 3, 3000])\nmeans = X.mean(axis=0)\ncontribs = m.coef_ * (player - means)",
               [{"check": "contribs.shape == (3,)", "msg": "3 фичи"}],
               ["coef_ * (x - mean)"], 3),
        ],
        minutes=50, difficulty=3,
    )


def _7_13():
    return lesson(
        "7.13", "Сравнение и выбор модели", "mixed", [
            theory(
                "**Выбор модели** — системный процесс, а не «попробовал одно и норм».\n\n"
                "**1. Baseline:** всегда сначала простая модель (LogReg, Dummy). Если "
                "XGBoost даёт +0.5% — может, не стоит.\n\n"
                "**2. Метрика под задачу:**\n"
                "- Регрессия: RMSE/R²/MAE\n"
                "- Классификация (баланс): accuracy\n"
                "- Классификация (дисбаланс): F1, ROC-AUC, PR-AUC\n"
                "- Ranking: NDCG, MAP\n"
                "- Бизнес: precision@k, recall@k, ROI\n\n"
                "**3. Кросс-валидация (k=5/10) + усреднение.** Один split — шумный.\n\n"
                "**4. Статистическая значимость:**\n"
                "- Paired t-test: разница значима?\n"
                "- Или хотя бы std по фолдам\n\n"
                "**5. Стоимость модели:**\n"
                "- Время обучения, инференса, память\n"
                "- Интерпретируемость (линейная > RF > XGBoost > нейросеть)\n\n"
                "**6. Переобучение vs обобщение:** сравни train и val score. "
                "Лучшая модель — баланс.\n\n"
                "**Процесс:**\n"
                "1. EDA → понимание данных\n"
                "2. Baseline\n"
                "3. 2-3 сильные модели\n"
                "4. CV-сравнение\n"
                "5. Тюнинг лучшей (GridSearch, RandomSearch)\n"
                "6. Финальная модель → test (один раз!)\n\n"
                "**Чеклист:** масштабирование? фичи? ансамбль лучших?"
            ),
            analogy(
                "Выбор модели — выбор инструмента: молоток, дрель, лазер. Для гвоздя — "
                "молоток, не лазер. Baseline = самый простой рабочий инструмент.",
                "В Dota-аналитике: сегментация → K-Means, прогноз KDR → Ridge/RF, "
                "прогноз win → XGBoost/GB."
            ),
            visual(
                "Model selection flowchart",
                "         Data\n"
                "          ↓\n"
                "   ┌─Baseline (LogReg)─┐\n"
                "   │ acc: 0.85         │\n"
                "   └──────────┬─────────┘\n"
                "              ↓\n"
                "   ┌─Strong models (RF, XGB)──┐\n"
                "   │ 5-fold CV → mean/std     │\n"
                "   └──────────┬───────────────┘\n"
                "              ↓\n"
                "   ┌─Best: XGB (0.91 ± 0.02)─┐\n"
                "   │  Tune + Ensemble        │\n"
                "   └──────────┬──────────────┘\n"
                "              ↓\n"
                "          Test once"
            ),
            example(
                "Сравни 3 модели на одних данных.",
                "LogReg, RF, GB. CV mean ± std.",
                "import numpy as np\n"
                "from sklearn.linear_model import LogisticRegression\n"
                "from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier\n"
                "from sklearn.model_selection import cross_val_score\n"
                "np.random.seed(42)\n"
                "n = 500\n"
                "kills = np.random.poisson(6, n)\n"
                "deaths = np.random.poisson(5, n)\n"
                "gold = np.random.normal(2000, 500, n)\n"
                "X = np.column_stack([kills, deaths, gold])\n"
                "y = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)\n"
                "for name, m in [('LR', LogisticRegression()),\n"
                "                ('RF', RandomForestClassifier(n_estimators=100, random_state=42)),\n"
                "                ('GB', GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, random_state=42))]:\n"
                "    s = cross_val_score(m, X, y, cv=5)\n"
                "    print(f'{name}: {s.mean():.3f} ± {s.std():.3f}')",
                "LR: 0.838 ± 0.030\nRF: 0.892 ± 0.024\nGB: 0.916 ± 0.020",
                "GB лучший (0.916), RF рядом (0.892), LR сильно хуже. std маленький → "
                "стабильно. Итог: выбираем GB, тюнингуем lr/n_estimators."
            ),
            common_mistakes([
                {"mistake": "Смотреть только на test acc", "why_bad": "Один split — шумный, переобучение к нему", "fix": "CV, std"},
                {"mistake": "Тюнить на test", "why_bad": "Test перестаёт быть честным", "fix": "Test только в конце"},
                {"mistake": "Гнаться за accuracy при дисбалансе", "why_bad": "Константа = 99%", "fix": "F1, AUC"},
                {"mistake": "Одна модель на все случаи", "why_bad": "Каждая задача — свой лучший алгоритм", "fix": "Сравнивай 2-3"},
            ]),
            interview_questions([
                {"q": "Как выбрать лучшую модель?", "a": "CV на train (mean ± std), метрика под задачу, учёт времени/интерпретируемости. Test — только в конце, один раз. Лучшая — не всегда самая сложная."},
                {"q": "Сколько моделей сравнивать?", "a": "2-3 разных семейства. Baseline + 1-2 сильных. Ансамбль лучших может дать +1-3% сверху. Больше — diminishing returns."},
                {"q": "Когда LogReg лучше XGBoost?", "a": "Линейные данные, малый train, важна интерпретируемость, нужны вероятности с калибровкой, baseline. На 100k+ строк XGBoost почти всегда выиграет."},
            ]),
            knowledge_checklist([
                "Строю baseline",
                "Сравниваю модели через CV",
                "Выбираю метрику под задачу",
                "Учитываю стоимость модели",
                "Test использую один раз в конце",
            ]),
        ],
        exercises=[
            ex(1, "python", "Dota-данные: 500 игроков, 3 фичи. win в `y`. seed=42.",
               "import numpy as np\nX = np.array([])\ny = np.array([])\n",
               "import numpy as np\nnp.random.seed(42)\nn = 500\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nX = np.column_stack([kills, deaths, gold])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)",
               [{"check": "X.shape == (500, 3)", "msg": "500x3"}],
               ["3 фичи"], 1),
            ex(2, "python", "CV (cv=5) для LogReg. mean в `acc_lr`.",
               "import numpy as np\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.model_selection import cross_val_score\nnp.random.seed(42)\nn = 500\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nX = np.column_stack([kills, deaths, gold])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)\nacc_lr = 0\n",
               "import numpy as np\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.model_selection import cross_val_score\nnp.random.seed(42)\nacc_lr = cross_val_score(LogisticRegression(), X, y, cv=5).mean()",
               [{"check": "0.5 < acc_lr < 1.0", "msg": "LR acc > 0.5"}],
               ["cross_val_score"], 1),
            ex(3, "python", "CV (cv=5) для RF. mean в `acc_rf`.",
               "import numpy as np\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.model_selection import cross_val_score\nnp.random.seed(42)\nn = 500\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nX = np.column_stack([kills, deaths, gold])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)\nacc_rf = 0\n",
               "import numpy as np\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.model_selection import cross_val_score\nnp.random.seed(42)\nacc_rf = cross_val_score(RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42), X, y, cv=5).mean()",
               [{"check": "0.5 < acc_rf < 1.0", "msg": "RF acc > 0.5"}],
               ["cross_val_score"], 1),
            ex(4, "python", "CV (cv=5) для GB. mean в `acc_gb`.",
               "import numpy as np\nfrom sklearn.ensemble import GradientBoostingClassifier\nfrom sklearn.model_selection import cross_val_score\nnp.random.seed(42)\nn = 500\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nX = np.column_stack([kills, deaths, gold])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)\nacc_gb = 0\n",
               "import numpy as np\nfrom sklearn.ensemble import GradientBoostingClassifier\nfrom sklearn.model_selection import cross_val_score\nnp.random.seed(42)\nacc_gb = cross_val_score(GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42), X, y, cv=5).mean()",
               [{"check": "0.5 < acc_gb < 1.0", "msg": "GB acc > 0.5"}],
               ["cross_val_score"], 1),
            ex(5, "python", "Сравни: dict {model: score} в `scores`.",
               "import numpy as np\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier\nfrom sklearn.model_selection import cross_val_score\nnp.random.seed(42)\nn = 500\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nX = np.column_stack([kills, deaths, gold])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)\nscores = {}\n",
               "import numpy as np\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier\nfrom sklearn.model_selection import cross_val_score\nnp.random.seed(42)\nscores = {\n    'LR': cross_val_score(LogisticRegression(), X, y, cv=5).mean(),\n    'RF': cross_val_score(RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42), X, y, cv=5).mean(),\n    'GB': cross_val_score(GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42), X, y, cv=5).mean(),\n}",
               [{"check": "len(scores) == 3", "msg": "3 модели"}],
               ["dict comprehension"], 2),
            ex(6, "python", "Лучшая модель по max score в `best`.",
               "import numpy as np\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier\nfrom sklearn.model_selection import cross_val_score\nnp.random.seed(42)\nn = 500\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nX = np.column_stack([kills, deaths, gold])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)\nbest = ''\n",
               "import numpy as np\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier\nfrom sklearn.model_selection import cross_val_score\nnp.random.seed(42)\nscores = {\n    'LR': cross_val_score(LogisticRegression(), X, y, cv=5).mean(),\n    'RF': cross_val_score(RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42), X, y, cv=5).mean(),\n    'GB': cross_val_score(GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42), X, y, cv=5).mean(),\n}\nbest = max(scores, key=scores.get)",
               [{"check": "best in ['LR', 'RF', 'GB']", "msg": "Valid name"}],
               ["max(dict, key=)"], 2),
            ex(7, "python", "Визуализируй scores баром.",
               "import numpy as np\nimport matplotlib.pyplot as plt\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier\nfrom sklearn.model_selection import cross_val_score\nnp.random.seed(42)\nn = 500\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nX = np.column_stack([kills, deaths, gold])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)\nfig, ax = plt.subplots()\n",
               "import numpy as np\nimport matplotlib.pyplot as plt\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier\nfrom sklearn.model_selection import cross_val_score\nnp.random.seed(42)\nscores = {\n    'LR': cross_val_score(LogisticRegression(), X, y, cv=5).mean(),\n    'RF': cross_val_score(RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42), X, y, cv=5).mean(),\n    'GB': cross_val_score(GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42), X, y, cv=5).mean(),\n}\nfig, ax = plt.subplots()\nax.bar(scores.keys(), scores.values())\nax.set_ylim(0.5, 1.0)\nax.set_title('Model comparison')\nplt.close(fig)",
               [{"check": "True", "msg": "matplotlib"}],
               ["ax.bar", "ax.set_ylim"], 2),
            ex(8, "python", "std по фолдам для GB в `std_gb`.",
               "import numpy as np\nfrom sklearn.ensemble import GradientBoostingClassifier\nfrom sklearn.model_selection import cross_val_score\nnp.random.seed(42)\nn = 500\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nX = np.column_stack([kills, deaths, gold])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)\nstd_gb = 0\n",
               "import numpy as np\nfrom sklearn.ensemble import GradientBoostingClassifier\nfrom sklearn.model_selection import cross_val_score\nnp.random.seed(42)\nstd_gb = cross_val_score(GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42), X, y, cv=5).std()",
               [{"check": "0 < std_gb < 0.1", "msg": "std в разумных пределах"}],
               [".std()"], 1),
            ex(9, "python", "Final test accuracy лучшей модели (GB) в `test_acc`. 80/20 split, random_state=42.",
               "import numpy as np\nfrom sklearn.ensemble import GradientBoostingClassifier\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nn = 500\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nX = np.column_stack([kills, deaths, gold])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\ntest_acc = 0\n",
               "import numpy as np\nfrom sklearn.ensemble import GradientBoostingClassifier\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\ntest_acc = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42).fit(X_train, y_train).score(X_test, y_test)",
               [{"check": "0.7 < test_acc < 1.0", "msg": "test > 0.7"}],
               ["Test один раз в конце"], 2),
            ex(10, "python", "Время обучения GB (timing) в `time_s`.",
               "import numpy as np\nimport time\nfrom sklearn.ensemble import GradientBoostingClassifier\nnp.random.seed(42)\nn = 500\nkills = np.random.poisson(6, n)\ndeaths = np.random.poisson(5, n)\ngold = np.random.normal(2000, 500, n)\nX = np.column_stack([kills, deaths, gold])\ny = (1.5*kills - 1.2*deaths + 0.001*gold + np.random.randn(n) > 0).astype(int)\ntime_s = 0\n",
               "import numpy as np\nimport time\nfrom sklearn.ensemble import GradientBoostingClassifier\nnp.random.seed(42)\nt0 = time.time()\nGradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42).fit(X, y)\ntime_s = time.time() - t0",
               [{"check": "time_s > 0", "msg": "Время > 0"}],
               ["time.time()"], 1),
        ],
        minutes=55, difficulty=3,
    )


def _7_14():
    return lesson(
        "7.14", "Мини-проект: Прогноз оттока игроков", "project", [
            theory(
                "**Мини-проект:** полный цикл ML на реальной задаче — прогноз оттока "
                "игроков (churn prediction). Метрика: ROC-AUC, F1 (дисбаланс).\n\n"
                "**Цель:** по активности игрока (sessions, kills, days_inactive, "
                "purchases) предсказать, уйдёт ли он в ближайший месяц.\n\n"
                "**Pipeline:**\n"
                "1. **Генерация данных:** синтетический Dota-датасет с признаками\n"
                "2. **EDA:** распределения, корреляции, дисбаланс\n"
                "3. **Train/test split:** stratify по y\n"
                "4. **Baseline:** DummyClassifier / LogReg\n"
                "5. **Модели:** LogReg, RF, GB\n"
                "6. **CV-сравнение:** mean ± std\n"
                "7. **Тюнинг:** GridSearch (опционально)\n"
                "8. **Final test:** ROC-AUC, F1, confusion matrix\n"
                "9. **Интерпретация:** feature_importances_, SHAP-like\n\n"
                "**Ключевые навыки:**\n"
                "- Работа с дисбалансом (class_weight, stratify)\n"
                "- Выбор метрики (F1 > accuracy при churn)\n"
                "- Полный цикл: EDA → baseline → models → select → test"
            ),
            analogy(
                "Churn prediction — анти-уход: маркетинг звонит тем, кого модель "
                "назовёт 'уходящим'. Если модель ошибается на 100k игроков — "
                "компания теряет деньги на удержании и пропускает реальный отток.",
                "Предсказываем 'уйдёт ли игрок', основываясь на его активности."
            ),
            visual(
                "Churn pipeline",
                "   Data → EDA → Split\n"
                "              ↓\n"
                "   Baseline(LogReg) → CV(5) → 0.78\n"
                "   RF → CV(5) → 0.85\n"
                "   GB → CV(5) → 0.88  ← best\n"
                "              ↓\n"
                "   Test: AUC=0.91, F1=0.74\n"
                "              ↓\n"
                "   Feature importance: sessions, days_inactive"
            ),
            example(
                "Полный пайплайн на синтетических данных.",
                "1000 игроков, 5 фич, 30% churn.",
                "import numpy as np\n"
                "from sklearn.model_selection import train_test_split, cross_val_score\n"
                "from sklearn.linear_model import LogisticRegression\n"
                "from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier\n"
                "from sklearn.metrics import roc_auc_score, f1_score, confusion_matrix\n"
                "np.random.seed(42)\n"
                "n = 1000\n"
                "sessions = np.random.poisson(20, n)\n"
                "days_inactive = np.random.exponential(5, n)\n"
                "kills = np.random.poisson(5, n)\n"
                "purchases = np.random.poisson(1, n)\n"
                "level = np.random.randint(1, 30, n)\n"
                "X = np.column_stack([sessions, days_inactive, kills, purchases, level])\n"
                "y = ((-0.1*sessions + 0.3*days_inactive - 0.2*kills - 0.5*purchases + 0.05*level + np.random.randn(n)) > 0).astype(int)\n"
                "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\n"
                "for name, m in [('LR', LogisticRegression(max_iter=1000)),\n"
                "                ('RF', RandomForestClassifier(n_estimators=100, max_depth=8, class_weight='balanced', random_state=42)),\n"
                "                ('GB', GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42))]:\n"
                "    cv = cross_val_score(m, X_tr, y_tr, cv=5, scoring='roc_auc').mean()\n"
                "    print(f'{name}: CV AUC={cv:.3f}')\n"
                "gb = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42).fit(X_tr, y_tr)\n"
                "y_pred = gb.predict(X_te)\n"
                "y_proba = gb.predict_proba(X_te)[:, 1]\n"
                "print(f'Test AUC: {roc_auc_score(y_te, y_proba):.3f} F1: {f1_score(y_te, y_pred):.3f}')",
                "LR: CV AUC=0.812\nRF: CV AUC=0.875\nGB: CV AUC=0.901\nTest AUC: 0.911 F1: 0.762",
                "GB — лучшая модель: Test AUC=0.91, F1=0.76. Дни неактивности и сессии — "
                "главные предикторы."
            ),
            common_mistakes([
                {"mistake": "Accuracy при дисбалансе churn", "why_bad": "95% не уходят → 95% accuracy у константы", "fix": "F1, ROC-AUC, PR-AUC"},
                {"mistake": "Не стратифицировать", "why_bad": "Test может не содержать churn-класс", "fix": "stratify=y"},
                {"mistake": "Тюнинг на test", "why_bad": "Test перестаёт быть честным", "fix": "CV + final test"},
                {"mistake": "Игнорировать feature engineering", "why_bad": "Сырые фичи часто слабые", "fix": "sessions/level, days/avg и т.д."},
            ]),
            interview_questions([
                {"q": "Что такое churn prediction?", "a": "Бинарная классификация: уйдёт ли клиент/игрок. Типичный дисбаланс (5-15% churn). Метрики: F1, ROC-AUC. Бизнес-метрика: сколько удержали из flagged."},
                {"q": "Как бороться с дисбалансом?", "a": "class_weight='balanced', oversampling (SMOTE), undersampling, stratify, F1/PR-AUC вместо accuracy."},
                {"q": "Что важнее: precision или recall в churn?", "a": "Зависит от стоимости. Если удержание клиента стоит 5, а потеря 100 — recall важнее."},
            ]),
            knowledge_checklist([
                "Делаю EDA перед моделированием",
                "Работаю с дисбалансом",
                "CV-сравнение моделей",
                "Метрики под бизнес",
                "Feature importance и интерпретация",
            ]),
        ],
        exercises=[
            ex(1, "python", "Сгенерируй 1000 игроков с 5 фичами. Сохрани X (1000, 5) и y (1000,). seed=42.",
               "import numpy as np\nX = np.array([])\ny = np.array([])\n",
               "import numpy as np\nnp.random.seed(42)\nn = 1000\nsessions = np.random.poisson(20, n)\ndays_inactive = np.random.exponential(5, n)\nkills = np.random.poisson(5, n)\npurchases = np.random.poisson(1, n)\nlevel = np.random.randint(1, 30, n)\nX = np.column_stack([sessions, days_inactive, kills, purchases, level])\ny = ((-0.1*sessions + 0.3*days_inactive - 0.2*kills - 0.5*purchases + 0.05*level + np.random.randn(n)) > 0).astype(int)",
               [{"check": "X.shape == (1000, 5)", "msg": "1000x5"},
                {"check": "y.shape == (1000,)", "msg": "1000 меток"}],
               ["5 фич: sessions, days_inactive, kills, purchases, level"], 1),
            ex(2, "python", "Доля churn в `churn_rate`.",
               "import numpy as np\nnp.random.seed(42)\nn = 1000\nsessions = np.random.poisson(20, n)\ndays_inactive = np.random.exponential(5, n)\nkills = np.random.poisson(5, n)\npurchases = np.random.poisson(1, n)\nlevel = np.random.randint(1, 30, n)\nX = np.column_stack([sessions, days_inactive, kills, purchases, level])\ny = ((-0.1*sessions + 0.3*days_inactive - 0.2*kills - 0.5*purchases + 0.05*level + np.random.randn(n)) > 0).astype(int)\nchurn_rate = 0\n",
               "import numpy as np\nchurn_rate = y.mean()",
               [{"check": "0.2 < churn_rate < 0.5", "msg": "Дисбаланс, но не экстремальный"}],
               ["y.mean()"], 1),
            ex(3, "python", "Train/test split 80/20, stratify=y, random_state=42. Сохрани размер test в `n_test`.",
               "import numpy as np\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nn = 1000\nsessions = np.random.poisson(20, n)\ndays_inactive = np.random.exponential(5, n)\nkills = np.random.poisson(5, n)\npurchases = np.random.poisson(1, n)\nlevel = np.random.randint(1, 30, n)\nX = np.column_stack([sessions, days_inactive, kills, purchases, level])\ny = ((-0.1*sessions + 0.3*days_inactive - 0.2*kills - 0.5*purchases + 0.05*level + np.random.randn(n)) > 0).astype(int)\n",
               "import numpy as np\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\nn_test = len(X_test)",
               [{"check": "n_test == 200", "msg": "20% от 1000"}],
               ["stratify=y"], 1),
            ex(4, "python", "CV (cv=5, scoring='roc_auc') для LogReg. mean в `lr_auc`.",
               "import numpy as np\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.model_selection import cross_val_score, train_test_split\nnp.random.seed(42)\nn = 1000\nsessions = np.random.poisson(20, n)\ndays_inactive = np.random.exponential(5, n)\nkills = np.random.poisson(5, n)\npurchases = np.random.poisson(1, n)\nlevel = np.random.randint(1, 30, n)\nX = np.column_stack([sessions, days_inactive, kills, purchases, level])\ny = ((-0.1*sessions + 0.3*days_inactive - 0.2*kills - 0.5*purchases + 0.05*level + np.random.randn(n)) > 0).astype(int)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\nlr_auc = 0\n",
               "import numpy as np\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.model_selection import cross_val_score\nnp.random.seed(42)\nlr_auc = cross_val_score(LogisticRegression(max_iter=1000), X_train, y_train, cv=5, scoring='roc_auc').mean()",
               [{"check": "0.6 < lr_auc < 1.0", "msg": "AUC > 0.6"}],
               ["scoring='roc_auc'"], 2),
            ex(5, "python", "CV AUC для RF с class_weight='balanced'. mean в `rf_auc`.",
               "import numpy as np\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.model_selection import cross_val_score, train_test_split\nnp.random.seed(42)\nn = 1000\nsessions = np.random.poisson(20, n)\ndays_inactive = np.random.exponential(5, n)\nkills = np.random.poisson(5, n)\npurchases = np.random.poisson(1, n)\nlevel = np.random.randint(1, 30, n)\nX = np.column_stack([sessions, days_inactive, kills, purchases, level])\ny = ((-0.1*sessions + 0.3*days_inactive - 0.2*kills - 0.5*purchases + 0.05*level + np.random.randn(n)) > 0).astype(int)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\nrf_auc = 0\n",
               "import numpy as np\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.model_selection import cross_val_score\nnp.random.seed(42)\nrf_auc = cross_val_score(RandomForestClassifier(n_estimators=100, max_depth=8, class_weight='balanced', random_state=42), X_train, y_train, cv=5, scoring='roc_auc').mean()",
               [{"check": "0.6 < rf_auc < 1.0", "msg": "RF AUC > 0.6"}],
               ["class_weight='balanced'"], 2),
            ex(6, "python", "CV AUC для GB. mean в `gb_auc`.",
               "import numpy as np\nfrom sklearn.ensemble import GradientBoostingClassifier\nfrom sklearn.model_selection import cross_val_score, train_test_split\nnp.random.seed(42)\nn = 1000\nsessions = np.random.poisson(20, n)\ndays_inactive = np.random.exponential(5, n)\nkills = np.random.poisson(5, n)\npurchases = np.random.poisson(1, n)\nlevel = np.random.randint(1, 30, n)\nX = np.column_stack([sessions, days_inactive, kills, purchases, level])\ny = ((-0.1*sessions + 0.3*days_inactive - 0.2*kills - 0.5*purchases + 0.05*level + np.random.randn(n)) > 0).astype(int)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\ngb_auc = 0\n",
               "import numpy as np\nfrom sklearn.ensemble import GradientBoostingClassifier\nfrom sklearn.model_selection import cross_val_score\nnp.random.seed(42)\ngb_auc = cross_val_score(GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42), X_train, y_train, cv=5, scoring='roc_auc').mean()",
               [{"check": "0.6 < gb_auc < 1.0", "msg": "GB AUC > 0.6"}],
               ["scoring='roc_auc'"], 2),
            ex(7, "python", "Обучи GB на train, test AUC и F1 в `test_auc, test_f1`.",
               "import numpy as np\nfrom sklearn.ensemble import GradientBoostingClassifier\nfrom sklearn.metrics import roc_auc_score, f1_score\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nn = 1000\nsessions = np.random.poisson(20, n)\ndays_inactive = np.random.exponential(5, n)\nkills = np.random.poisson(5, n)\npurchases = np.random.poisson(1, n)\nlevel = np.random.randint(1, 30, n)\nX = np.column_stack([sessions, days_inactive, kills, purchases, level])\ny = ((-0.1*sessions + 0.3*days_inactive - 0.2*kills - 0.5*purchases + 0.05*level + np.random.randn(n)) > 0).astype(int)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\ntest_auc = 0\ntest_f1 = 0\n",
               "import numpy as np\nfrom sklearn.ensemble import GradientBoostingClassifier\nfrom sklearn.metrics import roc_auc_score, f1_score\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\nm = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42).fit(X_train, y_train)\ntest_auc = roc_auc_score(y_test, m.predict_proba(X_test)[:, 1])\ntest_f1 = f1_score(y_test, m.predict(X_test))",
               [{"check": "0.6 < test_auc < 1.0", "msg": "Test AUC > 0.6"},
                {"check": "0 < test_f1 <= 1.0", "msg": "Test F1 в (0, 1]"}],
               ["roc_auc_score", "f1_score"], 2),
            ex(8, "python", "Confusion matrix на test в `cm`.",
               "import numpy as np\nfrom sklearn.ensemble import GradientBoostingClassifier\nfrom sklearn.metrics import confusion_matrix\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nn = 1000\nsessions = np.random.poisson(20, n)\ndays_inactive = np.random.exponential(5, n)\nkills = np.random.poisson(5, n)\npurchases = np.random.poisson(1, n)\nlevel = np.random.randint(1, 30, n)\nX = np.column_stack([sessions, days_inactive, kills, purchases, level])\ny = ((-0.1*sessions + 0.3*days_inactive - 0.2*kills - 0.5*purchases + 0.05*level + np.random.randn(n)) > 0).astype(int)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\ncm = None\n",
               "import numpy as np\nfrom sklearn.ensemble import GradientBoostingClassifier\nfrom sklearn.metrics import confusion_matrix\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\ny_pred = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42).fit(X_train, y_train).predict(X_test)\ncm = confusion_matrix(y_test, y_pred)",
               [{"check": "cm.shape == (2, 2)", "msg": "2x2"}],
               ["confusion_matrix"], 2),
            ex(9, "python", "feature_importances_ в `imp` (главные предикторы churn).",
               "import numpy as np\nfrom sklearn.ensemble import GradientBoostingClassifier\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nn = 1000\nsessions = np.random.poisson(20, n)\ndays_inactive = np.random.exponential(5, n)\nkills = np.random.poisson(5, n)\npurchases = np.random.poisson(1, n)\nlevel = np.random.randint(1, 30, n)\nX = np.column_stack([sessions, days_inactive, kills, purchases, level])\ny = ((-0.1*sessions + 0.3*days_inactive - 0.2*kills - 0.5*purchases + 0.05*level + np.random.randn(n)) > 0).astype(int)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\nimp = np.array([])\n",
               "import numpy as np\nfrom sklearn.ensemble import GradientBoostingClassifier\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\nimp = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42).fit(X_train, y_train).feature_importances_",
               [{"check": "imp.shape == (5,)", "msg": "5 фич"}],
               ["feature_importances_"], 2),
            ex(10, "python", "Визуализируй feature_importances_ баром.",
               "import numpy as np\nimport matplotlib.pyplot as plt\nfrom sklearn.ensemble import GradientBoostingClassifier\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nn = 1000\nsessions = np.random.poisson(20, n)\ndays_inactive = np.random.exponential(5, n)\nkills = np.random.poisson(5, n)\npurchases = np.random.poisson(1, n)\nlevel = np.random.randint(1, 30, n)\nX = np.column_stack([sessions, days_inactive, kills, purchases, level])\ny = ((-0.1*sessions + 0.3*days_inactive - 0.2*kills - 0.5*purchases + 0.05*level + np.random.randn(n)) > 0).astype(int)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\nfig, ax = plt.subplots()\n",
               "import numpy as np\nimport matplotlib.pyplot as plt\nfrom sklearn.ensemble import GradientBoostingClassifier\nfrom sklearn.model_selection import train_test_split\nnp.random.seed(42)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\nm = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42).fit(X_train, y_train)\nfig, ax = plt.subplots()\nlabels = ['sessions', 'days_inact', 'kills', 'purchases', 'level']\nax.bar(labels, m.feature_importances_)\nax.set_title('Churn feature importances')\nplt.close(fig)",
               [{"check": "True", "msg": "matplotlib"}],
               ["ax.bar"], 2),
            ex(11, "python", "Сравни модели: CV AUC в dict `scores`.",
               "import numpy as np\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier\nfrom sklearn.model_selection import cross_val_score, train_test_split\nnp.random.seed(42)\nn = 1000\nsessions = np.random.poisson(20, n)\ndays_inactive = np.random.exponential(5, n)\nkills = np.random.poisson(5, n)\npurchases = np.random.poisson(1, n)\nlevel = np.random.randint(1, 30, n)\nX = np.column_stack([sessions, days_inactive, kills, purchases, level])\ny = ((-0.1*sessions + 0.3*days_inactive - 0.2*kills - 0.5*purchases + 0.05*level + np.random.randn(n)) > 0).astype(int)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\nscores = {}\n",
               "import numpy as np\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier\nfrom sklearn.model_selection import cross_val_score\nnp.random.seed(42)\nscores = {\n    'LR': cross_val_score(LogisticRegression(max_iter=1000), X_train, y_train, cv=5, scoring='roc_auc').mean(),\n    'RF': cross_val_score(RandomForestClassifier(n_estimators=100, max_depth=8, class_weight='balanced', random_state=42), X_train, y_train, cv=5, scoring='roc_auc').mean(),\n    'GB': cross_val_score(GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42), X_train, y_train, cv=5, scoring='roc_auc').mean(),\n}",
               [{"check": "len(scores) == 3", "msg": "3 модели"}],
               ["dict из 3 моделей"], 3),
            ex(12, "python", "Лучшая модель по AUC в `best`.",
               "import numpy as np\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier\nfrom sklearn.model_selection import cross_val_score\nnp.random.seed(42)\nn = 1000\nsessions = np.random.poisson(20, n)\ndays_inactive = np.random.exponential(5, n)\nkills = np.random.poisson(5, n)\npurchases = np.random.poisson(1, n)\nlevel = np.random.randint(1, 30, n)\nX = np.column_stack([sessions, days_inactive, kills, purchases, level])\ny = ((-0.1*sessions + 0.3*days_inactive - 0.2*kills - 0.5*purchases + 0.05*level + np.random.randn(n)) > 0).astype(int)\nbest = ''\n",
               "import numpy as np\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier\nfrom sklearn.model_selection import cross_val_score\nnp.random.seed(42)\nscores = {\n    'LR': cross_val_score(LogisticRegression(max_iter=1000), X, y, cv=5, scoring='roc_auc').mean(),\n    'RF': cross_val_score(RandomForestClassifier(n_estimators=100, max_depth=8, class_weight='balanced', random_state=42), X, y, cv=5, scoring='roc_auc').mean(),\n    'GB': cross_val_score(GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42), X, y, cv=5, scoring='roc_auc').mean(),\n}\nbest = max(scores, key=scores.get)",
               [{"check": "best in ['LR', 'RF', 'GB']", "msg": "Valid name"}],
               ["max(dict, key=)"], 2),
        ],
        minutes=70, difficulty=4,
    )


LESSONS = [_7_1, _7_2, _7_3, _7_4, _7_5, _7_6, _7_7, _7_8, _7_9, _7_10, _7_11, _7_12, _7_13, _7_14]

