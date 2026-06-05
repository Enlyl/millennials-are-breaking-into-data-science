"""
Блок 8: Feature Engineering — Игровая индустрия.
8 уроков, ~70 упражнений.
"""
from app.seed_helpers import (
    ex, lesson, theory, analogy, visual, example,
    common_mistakes, interview_questions, knowledge_checklist,
)


def _8_1():
    return lesson(
        "8.1", "Что такое feature engineering и почему это важно", "gaming", [
            theory(
                "**Feature engineering** — это процесс создания, преобразования и отбора признаков "
                "(фичей) в данных, чтобы модель машинного обучения работала лучше.\n\n"
                "Говорят, что качество модели на 80% зависит от фичей и только на 20% от алгоритма. "
                "Один хорошо придуманный признак может дать больший прирост точности, чем смена "
                "алгоритма с Random Forest на градиентный бустинг.\n\n"
                "**Зачем это нужно:**\n"
                "- Модели работают с числами — категории и текст надо кодировать.\n"
                "- Признаки разного масштаба (рубли vs. проценты) искажают расстояния в KNN, SVM, "
                "нейросетях.\n"
                "- Скрытые закономерности (час дня, день недели, длина текста) — это золото для "
                "модели.\n\n"
                "**Виды работ:**\n"
                "1. **Создание** новых признаков (отношения, разности, агрегаты).\n"
                "2. **Кодирование** категориальных переменных.\n"
                "3. **Масштабирование** числовых признаков.\n"
                "4. **Извлечение** признаков из дат и текста.\n"
                "5. **Отбор** наиболее информативных фичей."
            ),
            analogy(
                "Feature engineering — это кулинария: данные — это сырые продукты, фичи — это "
                "нарезанные и приготовленные ингредиенты, а модель — повар, которому нужно подать "
                "уже подготовленные компоненты.",
                "Из даты '2024-03-15 14:23:00' повар приготовит фичи: hour=14, is_weekend=True, "
                "minutes_since_launch=12345 — и модель сможет 'попробовать' каждую на вкус."
            ),
            visual(
                "Место feature engineering в ML-пайплайне",
                "  СЫРЫЕ ДАННЫЕ          FEATURE ENG.          МОДЕЛЬ\n"
                "  ┌──────────┐         ┌──────────────┐      ┌────────┐\n"
                "  │ user_id  │         │ user_id_hash │      │        │\n"
                "  │ age      │  ──▶    │ age_norm     │ ──▶  │  ML    │ ──▶ score\n"
                "  │ country  │         │ country_ohe  │      │ model  │\n"
                "  │ reg_date │         │ reg_year     │      │        │\n"
                "  │ genre    │         │ genre_idx    │      │        │\n"
                "  └──────────┘         └──────────────┘      └────────┘"
            ),
            example(
                "Игру оценили 1000 раз. У неё рейтинг 8.2. Создай признак-отношение "
                "rating_per_review = rating * log(1 + reviews).",
                "log-преобразование сжимает длинный хвост. Произведение выделяет популярные игры.",
                "import numpy as np\n"
                "rating = 8.2\n"
                "reviews = 1000\n"
                "new_feature = rating * np.log1p(reviews)\n"
                "print(f'new_feature = {new_feature:.3f}')",
                "new_feature = 75.736",
                "log1p(x) = log(1+x) — стандартный приём для сжатия больших значений. "
                "8.2 * log(1001) ≈ 8.2 * 6.909 ≈ 75.74."
            ),
            common_mistakes([
                {"mistake": "Считать, что модель сама разберётся в сырых данных",
                 "why_bad": "Без подготовки категорий, дат, масштабов точность падает в разы",
                 "fix": "Всегда делаем exploratory data analysis и базовый feature engineering"},
                {"mistake": "Создавать тысячи фичей без отбора",
                 "why_bad": "Проклятие размерности, переобучение, медленный инференс",
                 "fix": "Отбираем top-k через SelectKBest, importance или бизнес-смысл"},
                {"mistake": "Игнорировать утечку данных (data leakage)",
                 "why_bad": "Фичи, посчитанные по всему датасету, 'знают' ответ",
                 "fix": "Fit трансформеры (scaler, encoder) только на train"},
                {"mistake": "Не сохранять трансформер для инференса",
                 "why_bad": "На проде получим другой масштаб — модель выдаст мусор",
                 "fix": "joblib.dump(scaler, 'scaler.pkl') и применяем тот же объект"},
            ]),
            interview_questions([
                {"q": "Почему feature engineering называют самым важным шагом в ML?",
                 "a": "Ансамбль алгоритмов не спасёт от мусорных фичей: модель учит то, что ей дали. "
                      "Хорошие фичи делают задачу линейно разделимой, плохие — превращают данные в шум."},
                {"q": "Что такое data leakage в контексте фичей?",
                 "a": "Это когда в обучающую выборку попадает информация из теста или из будущего. "
                      "Например, среднее по всему датасету, target encoding без фолдов, "
                      "масштабирование до split."},
                {"q": "Какие типы признаков ты выделяешь?",
                 "a": "Числовые (непрерывные/дискретные), категориальные (номинальные/порядковые), "
                      "бинарные, временные, текстовые, географические."},
            ]),
            knowledge_checklist([
                "Понимаю, что feature engineering важнее выбора алгоритма",
                "Знаю 5 основных видов работ с фичами",
                "Умею находить утечку данных в пайплайне",
                "Различаю числовые, категориальные и временные признаки",
                "Понимаю, что трансформер надо обучать только на train",
                "Знаю, что log-преобразование сжимает длинный хвост",
            ]),
        ],
        exercises=[
            ex(1, "python", "Создай список из 5 фичей для стриминговой платформы игр: user_id, age, country, hours_played, rating.",
               "# 5 фичей — стриминг игр\n",
               "features = ['user_id', 'age', 'country', 'hours_played', 'rating']\nprint(features)",
               [{"check": "isinstance(features, list)", "msg": "features — list"},
                {"check": "len(features) == 5", "msg": "Ровно 5 фичей"},
                {"check": "'rating' in features", "msg": "Есть rating"},
                {"check": "'country' in features", "msg": "Есть country"}],
               ["Список строк в []", "Длина списка == число элементов"], 1),
            ex(2, "python", "Дан rating=8.5, reviews=5000. Создай new_feat = rating * log1p(reviews). Сохрани в `f`.",
               "import numpy as np\nrating = 8.5\nreviews = 5000\nf = 0\n",
               "import numpy as np\nrating = 8.5\nreviews = 5000\nf = rating * np.log1p(reviews)\nprint(f'{f:.3f}')",
               [{"check": "abs(f - 8.5 * np.log1p(5000)) < 1e-6", "msg": "f = rating*log1p(reviews)"},
                {"check": "f > 70 and f < 100", "msg": "Ожидаемый диапазон"}],
               ["np.log1p(x) = log(1+x)", "Простое произведение"], 2),
            ex(3, "python", "Дан список `ratings = [9, 8, 7, 6, 5]`. Создай список `log_ratings` = log1p от каждого.",
               "import numpy as np\nratings = [9, 8, 7, 6, 5]\nlog_ratings = []\n",
               "import numpy as np\nratings = [9, 8, 7, 6, 5]\nlog_ratings = [np.log1p(r) for r in ratings]",
               [{"check": "len(log_ratings) == 5", "msg": "5 значений"},
                {"check": "abs(log_ratings[0] - np.log1p(9)) < 1e-6", "msg": "log1p(9) на первом месте"}],
               ["List comprehension: [f(x) for x in list]", "np.log1p"], 2),
            ex(4, "python", "Создай DataFrame с колонками title, rating, reviews. Заполни 3 строками про игры.",
               "import pandas as pd\n# твой код\n",
               "import pandas as pd\ndf = pd.DataFrame({\n    'title': ['Elden Ring', 'Hades', 'Stardew Valley'],\n    'rating': [9.5, 9.0, 8.8],\n    'reviews': [50000, 30000, 25000]\n})",
               [{"check": "isinstance(df, pd.DataFrame)", "msg": "df — DataFrame"},
                {"check": "df.shape == (3, 3)", "msg": "3 строки, 3 колонки"},
                {"check": "'title' in df.columns", "msg": "Колонка title есть"}],
               ["pd.DataFrame({...})", "Ключи=имена колонок"], 1),
            ex(5, "python", "Из df с колонкой price создай new_price = price * 0.9 (скидка 10%). "
                            "Сохрани в `df['new_price']`.",
               "import pandas as pd\ndf = pd.DataFrame({'price': [100, 200, 300]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'price': [100, 200, 300]})\ndf['new_price'] = df['price'] * 0.9",
               [{"check": "'new_price' in df.columns", "msg": "Колонка new_price создана"},
                {"check": "abs(df['new_price'].sum() - 540) < 1e-6", "msg": "90+180+270 = 540"}],
               ["df['col'] = expr создаёт колонку", "Поэлементное умножение"], 2),
            ex(6, "python", "Дан DataFrame с price и tax. Создай total = price + price*tax. "
                            "Сохрани в df['total'].",
               "import pandas as pd\ndf = pd.DataFrame({'price':[100,200], 'tax':[0.2,0.1]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'price':[100,200], 'tax':[0.2,0.1]})\ndf['total'] = df['price'] * (1 + df['tax'])",
               [{"check": "'total' in df.columns", "msg": "Колонка total"},
                {"check": "abs(df['total'].iloc[0] - 120) < 1e-6", "msg": "100*1.2 = 120"}],
               ["df['col']*1.2 — векторная операция", "(1 + df['tax']) скобки важны"], 2),
            ex(7, "python", "Словарь типов фичей. Для каждой фичи укажи тип: "
                            "{'age':'numeric', 'country':'categorical', 'is_premium':'binary'}.",
               "# твой код\n",
               "feature_types = {\n    'age': 'numeric',\n    'country': 'categorical',\n    'is_premium': 'binary'\n}",
               [{"check": "isinstance(feature_types, dict)", "msg": "Словарь"},
                {"check": "feature_types.get('country') == 'categorical'", "msg": "country — categorical"},
                {"check": "feature_types.get('is_premium') == 'binary'", "msg": "is_premium — binary"}],
               ["dict = {key:value}", ".get() возвращает None если нет"], 1),
            ex(8, "python", "Дан список цен. Создай `discounted` = [p*0.8 if p>50 else p for p in prices].",
               "prices = [30, 50, 70, 100]\ndiscounted = []\n",
               "prices = [30, 50, 70, 100]\ndiscounted = [p * 0.8 if p > 50 else p for p in prices]",
               [{"check": "discounted[0] == 30", "msg": "30 → 30 (не >50)"},
                {"check": "abs(discounted[2] - 56) < 1e-6", "msg": "70*0.8 = 56"},
                {"check": "abs(discounted[3] - 80) < 1e-6", "msg": "100*0.8 = 80"}],
               ["List comprehension с условием", "if/else внутри comprehension"], 3),
        ],
        minutes=45, difficulty=2,
    )


def _8_2():
    return lesson(
        "8.2", "Создание новых признаков", "gaming", [
            theory(
                "Создание новых признаков — это доменное творчество. Хорошая фича выделяет сигнал, "
                "который не очевиден из исходных колонок.\n\n"
                "**Основные приёмы:**\n"
                "- **Арифметика**: сумма, разность, произведение, отношение.\n"
                "- **Бинаризация**: is_premium = price > 100.\n"
                "- **Полиномы**: x^2, x*y, x^2 + y^2.\n"
                "- **Агрегации по группам**: средний рейтинг жанра, доля платящих в стране.\n"
                "- **Взаимодействия**: genre * platform, age * hours_played.\n"
                "- **Бининг**: age → young/middle/old.\n\n"
                "**Где брать идеи:** EDA (matplotlib histplot, scatter), бизнес-логика, "
                "соревнования Kaggle (смотрим топ-решения)."
            ),
            analogy(
                "Создание фичей — как готовить комбо-блюдо: было яйцо, мука и сахар — стал торт. "
                "Сами ингредиенты не изменились, но их сочетание раскрыло новое свойство.",
                "Колонки rating, reviews, price не объясняют популярность, а "
                "popularity = rating * log(reviews) / price — объясняет."
            ),
            visual(
                "Типы создаваемых признаков",
                "  ИСХОДНЫЕ                  НОВЫЕ ПРИЗНАКИ\n"
                "  ┌────────────┐\n"
                "  │ price      │ ──▶   log_price = log1p(price)\n"
                "  │ rating     │ ──▶   is_top = rating >= 9\n"
                "  │ hours      │ ──▶   hours_per_dollar = hours / price\n"
                "  │ genre      │ ──▶   genre_avg_rating (group agg)\n"
                "  │ age, hours │ ──▶   age * hours (interaction)\n"
                "  └────────────┘"
            ),
            example(
                "Из таблицы игр создай признак 'quality_per_dollar' = rating / price.",
                "Делим рейтинг на цену — получаем 'качество за доллар'. Высокое значение = выгодная покупка.",
                "import pandas as pd\n"
                "df = pd.DataFrame({\n"
                "    'title': ['A', 'B', 'C'],\n"
                "    'rating': [9.0, 8.0, 7.0],\n"
                "    'price': [60, 20, 10]\n"
                "})\n"
                "df['qpd'] = df['rating'] / df['price']\n"
                "print(df)",
                "  title  rating  price       qpd\n"
                "0     A     9.0     60  0.150000\n"
                "1     B     8.0     20  0.400000\n"
                "2     C     7.0     10  0.700000",
                "Игра C выгоднее всего: 0.7 очков рейтинга за доллар. Игра A — дорогая, но с высоким "
                "рейтингом."
            ),
            common_mistakes([
                {"mistake": "Делить на ноль без проверки (price = 0)",
                 "why_bad": "Получим inf или NaN",
                 "fix": "df['qpd'] = df['rating'] / df['price'].replace(0, np.nan)"},
                {"mistake": "Создавать признак, дублирующий таргет",
                 "why_bad": "Это утечка данных — модель 'подглядывает'",
                 "fix": "Проверяем корреляцию новой фичи с таргетом и бизнес-смысл"},
                {"mistake": "Забыть про новые значения в проде",
                 "why_bad": "Если в новых данных жанр 'MMO' не встречался, mean_encoding даст NaN",
                 "fix": "Fillna глобальным средним или используем target encoding с фолдами"},
                {"mistake": "Плодить десятки почти одинаковых фичей",
                 "why_bad": "Мультиколлинеарность раздувает variance у линейных моделей",
                 "fix": "Оставляем одну из коррелирующих, остальные дропаем"},
            ]),
            interview_questions([
                {"q": "Что такое target encoding и чем он опасен?",
                 "a": "Это замена категории средним значением таргета. Опасен утечкой: среднее по всему "
                      "train 'знает' будущее. Решение — считать по фолдам или с сглаживанием."},
                {"q": "Зачем делать бининг непрерывной переменной?",
                 "a": "Чтобы поймать нелинейности (например, доход <30k vs >30k), снизить влияние "
                      "выбросов, использовать как категориальный признак в деревьях."},
                {"q": "Что такое feature interactions и когда они полезны?",
                 "a": "Произведения/суммы пар фичей. Полезны, когда эффект одной фичи зависит от "
                      "значения другой: скидка * premium_status, возраст * жанр."},
            ]),
            knowledge_checklist([
                "Создаю арифметические фичи (сумма, разность, отношение)",
                "Делаю бинаризацию порогами",
                "Использую групповые агрегации (groupby agg)",
                "Генерирую полиномиальные и интеракционные фичи",
                "Проверяю отсутствие утечки данных",
                "Защищаюсь от деления на ноль",
            ]),
        ],
        exercises=[
            ex(1, "python", "Дан DataFrame с price, rating. Создай `df['quality'] = rating / price`.",
               "import pandas as pd\ndf = pd.DataFrame({'price':[10,20,30], 'rating':[8,9,7]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'price':[10,20,30], 'rating':[8,9,7]})\ndf['quality'] = df['rating'] / df['price']",
               [{"check": "'quality' in df.columns", "msg": "Колонка quality"},
                {"check": "abs(df['quality'].iloc[0] - 0.8) < 1e-6", "msg": "8/10 = 0.8"}],
               ["df['new'] = df['a'] / df['b']", "Поэлементная операция"], 1),
            ex(2, "python", "Создай бинарный признак `is_premium = price > 100` для df.",
               "import pandas as pd\ndf = pd.DataFrame({'price':[50, 150, 200, 80]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'price':[50, 150, 200, 80]})\ndf['is_premium'] = df['price'] > 100",
               [{"check": "'is_premium' in df.columns", "msg": "Колонка создана"},
                {"check": "df['is_premium'].dtype == bool", "msg": "Тип bool"},
                {"check": "df['is_premium'].sum() == 2", "msg": "Два True (150 и 200)"}],
               ["Булево сравнение даёт True/False", "df['col'] = df['x'] > n"], 1),
            ex(3, "python", "Создай df['log_price'] = log1p(price). Используй numpy.",
               "import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({'price':[10, 100, 1000]})\n",
               "import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({'price':[10, 100, 1000]})\ndf['log_price'] = np.log1p(df['price'])",
               [{"check": "'log_price' in df.columns", "msg": "log_price есть"},
                {"check": "abs(df['log_price'].iloc[0] - np.log1p(10)) < 1e-6", "msg": "log1p(10) на первом"}],
               ["np.log1p — сжатие хвоста", "Работает с pd.Series"], 2),
            ex(4, "python", "Дан df с жанрами и рейтингами. Создай `genre_avg` = средний рейтинг по жанру.",
               "import pandas as pd\ndf = pd.DataFrame({'genre':['RPG','RPG','Action','Action'], 'rating':[9,8,7,6]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'genre':['RPG','RPG','Action','Action'], 'rating':[9,8,7,6]})\ndf['genre_avg'] = df.groupby('genre')['rating'].transform('mean')",
               [{"check": "'genre_avg' in df.columns", "msg": "Колонка genre_avg"},
                {"check": "abs(df['genre_avg'].iloc[0] - 8.5) < 1e-6", "msg": "RPG: (9+8)/2 = 8.5"},
                {"check": "abs(df['genre_avg'].iloc[2] - 6.5) < 1e-6", "msg": "Action: (7+6)/2 = 6.5"}],
               ["groupby(...).transform('mean')", "transform сохраняет индекс"], 3),
            ex(5, "python", "Создай интеракцию: `df['score'] = price * rating`.",
               "import pandas as pd\ndf = pd.DataFrame({'price':[10,20], 'rating':[8,9]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'price':[10,20], 'rating':[8,9]})\ndf['score'] = df['price'] * df['rating']",
               [{"check": "'score' in df.columns", "msg": "Колонка score"},
                {"check": "df['score'].iloc[0] == 80", "msg": "10*8 = 80"}],
               ["Поэлементное умножение Series", "Новый признак — комбинация двух"], 1),
            ex(6, "python", "Сделай бининг: `df['age_group'] = pd.cut(age, bins=[0,18,35,100], labels=['young','mid','old'])`.",
               "import pandas as pd\ndf = pd.DataFrame({'age':[10,25,40,60]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'age':[10,25,40,60]})\ndf['age_group'] = pd.cut(df['age'], bins=[0,18,35,100], labels=['young','mid','old'])",
               [{"check": "'age_group' in df.columns", "msg": "age_group есть"},
                {"check": "df['age_group'].iloc[0] == 'young'", "msg": "10 → young"},
                {"check": "df['age_group'].iloc[2] == 'old'", "msg": "40 → old"}],
               ["pd.cut — бининг по границам", "bins — список границ"], 2),
            ex(7, "python", "Дан df с price. Создай `df['price_safe'] = price / price.max()`. Это min-max вручную.",
               "import pandas as pd\ndf = pd.DataFrame({'price':[10,20,40]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'price':[10,20,40]})\ndf['price_safe'] = df['price'] / df['price'].max()",
               [{"check": "'price_safe' in df.columns", "msg": "Колонка price_safe"},
                {"check": "abs(df['price_safe'].max() - 1.0) < 1e-6", "msg": "max=1.0"},
                {"check": "abs(df['price_safe'].iloc[0] - 0.25) < 1e-6", "msg": "10/40=0.25"}],
               ["df['x'] / df['x'].max() — нормировка в [0,1]", "max() встроенный"], 2),
            ex(8, "python", "Создай `df['review_density'] = reviews / (hours_played + 1)` — отзывы на час игры.",
               "import pandas as pd\ndf = pd.DataFrame({'reviews':[100,200], 'hours_played':[10,0]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'reviews':[100,200], 'hours_played':[10,0]})\ndf['review_density'] = df['reviews'] / (df['hours_played'] + 1)",
               [{"check": "'review_density' in df.columns", "msg": "review_density есть"},
                {"check": "abs(df['review_density'].iloc[0] - 100/11) < 1e-6", "msg": "100/11 на первом"},
                {"check": "df['review_density'].iloc[1] == 100.0", "msg": "200/1=100 — защита от /0"}],
               ["+1 защищает от деления на 0", "Гладкий фикс вместо inf"], 3),
            ex(9, "python", "Дан df. Создай `df['is_top_genre'] = (genre == 'RPG')`.",
               "import pandas as pd\ndf = pd.DataFrame({'genre':['RPG','Action','RPG','Sports']})\n",
               "import pandas as pd\ndf = pd.DataFrame({'genre':['RPG','Action','RPG','Sports']})\ndf['is_top_genre'] = (df['genre'] == 'RPG')",
               [{"check": "'is_top_genre' in df.columns", "msg": "Колонка создана"},
                {"check": "df['is_top_genre'].sum() == 2", "msg": "Два True"},
                {"check": "df['is_top_genre'].dtype == bool", "msg": "bool тип"}],
               ["== даёт bool Series", "Скобки улучшают читаемость"], 1),
            ex(10, "python", "Создай полином 2-й степени: `df['rating_sq'] = rating ** 2`.",
               "import pandas as pd\ndf = pd.DataFrame({'rating':[5,7,9]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'rating':[5,7,9]})\ndf['rating_sq'] = df['rating'] ** 2",
               [{"check": "'rating_sq' in df.columns", "msg": "Колонка rating_sq"},
                {"check": "df['rating_sq'].iloc[2] == 81", "msg": "9**2 = 81"}],
               ["** — степень", "Полезно для нелинейных моделей"], 1),
        ],
        minutes=50, difficulty=2,
    )


def _8_3():
    return lesson(
        "8.3", "Кодирование категориальных переменных", "gaming", [
            theory(
                "ML-модели не понимают строки — им нужны числа. Кодирование превращает категории "
                "(жанр, страна, платформа) в числовые векторы.\n\n"
                "**Основные методы:**\n\n"
                "**1. Label Encoding** — каждой категории присваиваем целое число (0, 1, 2, ...). "
                "Подходит для **порядковых** признаков (low/medium/high) и для деревянных моделей "
                "(Random Forest, LightGBM), которые не считают 2+1=3.\n\n"
                "**2. One-Hot Encoding (OHE)** — каждая категория становится отдельной бинарной "
                "колонкой. Подходит для **номинальных** признаков (жанры, цвета). "
                "Минус: взрыв размерности при высокой кардинальности.\n\n"
                "**3. Target Encoding** — заменяем категорию средним таргета по ней. Опасен утечкой — "
                "считают по фолдам.\n\n"
                "**4. Frequency Encoding** — заменяем частотой категории. Простой, без утечки, "
                "но теряет семантику."
            ),
            analogy(
                "Категориальное кодирование — это как разложить книги по шкафам: Label Encoding — "
                "расставить по алфавиту в один ряд, OHE — для каждого жанра свой шкаф.",
                "Жанр RPG, Action, Sports через OHE: RPG=[1,0,0], Action=[0,1,0], Sports=[0,0,1]. "
                "Никакой порядок не навязан."
            ),
            visual(
                "Сравнение Label vs One-Hot",
                "  Исходно:    Action\n"
                "  Action      RPG\n"
                "  RPG         Sports\n"
                "  Sports      Action\n"
                "\n"
                "  Label Enc:    One-Hot Enc:\n"
                "  ┌──────┐      ┌──────┬─────┬────────┐\n"
                "  │  0   │      │ 1 0 0│ 0 1 0│ 0 0 1  │\n"
                "  │  1   │      │ Action│ RPG  │ Sports │\n"
                "  │  2   │      └──────┴─────┴────────┘\n"
                "  │  0   │        3 колонки на 3 категории\n"
                "  └──────┘"
            ),
            example(
                "Закодируй жанры через LabelEncoder и OneHotEncoder.",
                "LabelEncoder даёт 1 колонку, OHE — k бинарных колонок. Для дерева — Label, для "
                "линейной — OHE.",
                "import pandas as pd\n"
                "from sklearn.preprocessing import LabelEncoder, OneHotEncoder\n"
                "df = pd.DataFrame({'genre':['RPG','Action','RPG','Sports']})\n"
                "le = LabelEncoder()\n"
                "df['le'] = le.fit_transform(df['genre'])\n"
                "ohe = OneHotEncoder(sparse_output=False)\n"
                "ohe_arr = ohe.fit_transform(df[['genre']])\n"
                "print('Label:', df['le'].tolist())\n"
                "print('OHE shape:', ohe_arr.shape)",
                "Label: [1, 0, 1, 2]\nOHE shape: (4, 3)",
                "Action=0, RPG=1, Sports=2. OHE: (4 строки, 3 уникальных жанра). "
                "OHE нужен, чтобы модель не считала Sports 'больше' Action."
            ),
            common_mistakes([
                {"mistake": "LabelEncoder для номинальных признаков в линейной модели",
                 "why_bad": "Модель думает: Sport=2 > Action=1 > RPG=0 — это ложный порядок",
                 "fix": "Используем OHE для номинальных, Label только для порядковых и деревьев"},
                {"mistake": "fit_transform на всём датасете, а потом split",
                 "why_bad": "Утечка: encoder 'видел' тест, новые категории не появятся",
                 "fix": "Сначала split, потом fit на train, transform на test"},
                {"mistake": "OHE для признака с 10000 уникальных",
                 "why_bad": "Матрица 10000 столбцов, память и переобучение",
                 "fix": "Target encoding, frequency encoding или embeddings (для нейросетей)"},
                {"mistake": "Забыть про drop='first' для OHE в линейной модели",
                 "why_bad": "Dummy variable trap: сумма колонок = 1, мультиколлинеарность",
                 "fix": "pd.get_dummies(df, drop_first=True) или OHE(drop='first')"},
            ]),
            interview_questions([
                {"q": "Когда использовать Label, а когда One-Hot?",
                 "a": "Label — для порядковых фичей (small/medium/large) и деревянных моделей. "
                      "OHE — для номинальных фичей в линейных/нейронных моделях."},
                {"q": "Что такое target encoding и как избежать утечки?",
                 "a": "Замена категории на среднее таргета. Утечка: среднее по всему train знает "
                      "будущее. Решение — считать по фолдам, с сглаживанием "
                      "(m-estimate, Bayesian smoothing)."},
                {"q": "Как бороться с высокой кардинальностью (10000 стран)?",
                 "a": "Target encoding, frequency encoding, хеширование (Hashing trick), "
                      "объединение редких категорий в 'other', обучение эмбеддингов."},
            ]),
            knowledge_checklist([
                "Знаю разницу между Label и One-Hot",
                "Использую OHE для номинальных, Label для порядковых",
                "Применяю fit только на train, transform на test",
                "Понимаю dummy variable trap",
                "Знаю про target и frequency encoding",
                "Умею работать с редкими категориями",
            ]),
        ],
        exercises=[
            ex(1, "python", "Список жанров ['RPG','Action','RPG','Sports']. Примени LabelEncoder, "
                            "сохрани результат в `le_result`.",
               "from sklearn.preprocessing import LabelEncoder\ngenres = ['RPG','Action','RPG','Sports']\nle_result = []\n",
               "from sklearn.preprocessing import LabelEncoder\ngenres = ['RPG','Action','RPG','Sports']\nle = LabelEncoder()\nle_result = le.fit_transform(genres).tolist()\nprint(le_result)",
               [{"check": "isinstance(le_result, list)", "msg": "Список"},
                {"check": "len(le_result) == 4", "msg": "4 значения"},
                {"check": "set(le_result) == {0, 1, 2}", "msg": "Уникальные 0,1,2"}],
               ["fit_transform возвращает ndarray", ".tolist() → list"], 2),
            ex(2, "python", "Используя pd.get_dummies, закодируй df с колонкой genre. "
                            "Сохрани в `dummies`.",
               "import pandas as pd\ndf = pd.DataFrame({'genre':['RPG','Action','Sports']})\ndummies = None\n",
               "import pandas as pd\ndf = pd.DataFrame({'genre':['RPG','Action','Sports']})\ndummies = pd.get_dummies(df['genre'])\nprint(dummies)",
               [{"check": "dummies.shape == (3, 3)", "msg": "(3, 3)"},
                {"check": "dummies.sum().sum() == 3", "msg": "3 единицы всего"},
                {"check": "dummies['RPG'].iloc[0] == 1", "msg": "RPG[0] = 1"}],
               ["pd.get_dummies превращает строки в 0/1", "Каждая категория = колонка"], 2),
            ex(3, "python", "pd.get_dummies с drop_first=True. Закодируй genre и сохрани в `d`.",
               "import pandas as pd\ndf = pd.DataFrame({'genre':['A','B','C']})\nd = None\n",
               "import pandas as pd\ndf = pd.DataFrame({'genre':['A','B','C']})\nd = pd.get_dummies(df['genre'], drop_first=True)\nprint(d)",
               [{"check": "d.shape == (3, 2)", "msg": "(3, 2) — убрали один столбец"},
                {"check": "set(d.columns) == {'B','C'}", "msg": "Колонки B и C"}],
               ["drop_first=True избегает мультиколлинеарности", "Первый уровень — baseline"], 2),
            ex(4, "python", "Создай словарь frequency encoding: посчитай, сколько раз встречается каждый жанр.",
               "from collections import Counter\ngenres = ['RPG','Action','RPG','Sports','Action','RPG']\nfreq = None\n",
               "from collections import Counter\ngenres = ['RPG','Action','RPG','Sports','Action','RPG']\nfreq = dict(Counter(genres))\nprint(freq)",
               [{"check": "isinstance(freq, dict)", "msg": "freq — dict"},
                {"check": "freq['RPG'] == 3", "msg": "RPG встретился 3 раза"},
                {"check": "freq['Sports'] == 1", "msg": "Sports встретился 1 раз"}],
               ["Counter подсчитывает элементы", "dict(Counter(...)) — словарь"], 1),
            ex(5, "python", "Frequency encoding в DataFrame: замени genre на число его вхождений.",
               "import pandas as pd\ndf = pd.DataFrame({'genre':['RPG','Action','RPG','Sports']})\n",
               "import pandas as pd\ndf = pd.DataFrame({'genre':['RPG','Action','RPG','Sports']})\nfreq = df['genre'].value_counts()\ndf['genre_freq'] = df['genre'].map(freq)\nprint(df)",
               [{"check": "'genre_freq' in df.columns", "msg": "Колонка genre_freq"},
                {"check": "df['genre_freq'].iloc[0] == 2", "msg": "RPG → 2"},
                {"check": "df['genre_freq'].iloc[1] == 1", "msg": "Action → 1"}],
               ["value_counts() — частоты", "map() подставляет значения"], 2),
            ex(6, "python", "Создай порядковый LabelEncoder: small/medium/large → 0/1/2. Используй `classes_`.",
               "from sklearn.preprocessing import LabelEncoder\nlabels = ['small','large','medium','small']\nresult = []\n",
               "from sklearn.preprocessing import LabelEncoder\nlabels = ['small','large','medium','small']\nle = LabelEncoder()\nresult = le.fit_transform(labels).tolist()\nprint(result, le.classes_)",
               [{"check": "len(result) == 4", "msg": "4 значения"},
                {"check": "set(result) == {0, 1, 2}", "msg": "0, 1, 2"}],
               ["LabelEncoder для порядковых — минимум странностей", "classes_ показывает маппинг"], 2),
            ex(7, "python", "OneHotEncoder из sklearn на df['genre']. Получи массив, сохрани в `arr`.",
               "import pandas as pd\nfrom sklearn.preprocessing import OneHotEncoder\ndf = pd.DataFrame({'genre':['RPG','Action','RPG']})\narr = None\n",
               "import pandas as pd\nfrom sklearn.preprocessing import OneHotEncoder\ndf = pd.DataFrame({'genre':['RPG','Action','RPG']})\nohe = OneHotEncoder(sparse_output=False)\narr = ohe.fit_transform(df[['genre']])\nprint(arr)",
               [{"check": "arr.shape == (3, 2)", "msg": "(3, 2) — 2 жанра"},
                {"check": "arr.sum() == 3", "msg": "3 единицы"},
                {"check": "(arr[0] == arr[2]).all()", "msg": "Первая и третья одинаковы (RPG)"}],
               ["sparse_output=False — обычный массив", "fit_transform на колонке [[ ]]"], 3),
            ex(8, "python", "Target encoding вручную: посчитай средний rating по жанру.",
               "import pandas as pd\ndf = pd.DataFrame({'genre':['RPG','RPG','Action','Action'], 'rating':[9,8,7,6]})\nte = None\n",
               "import pandas as pd\ndf = pd.DataFrame({'genre':['RPG','RPG','Action','Action'], 'rating':[9,8,7,6]})\nte = df.groupby('genre')['rating'].mean()\nprint(te)",
               [{"check": "isinstance(te, pd.Series)", "msg": "Series"},
                {"check": "abs(te['RPG'] - 8.5) < 1e-6", "msg": "RPG mean=8.5"},
                {"check": "abs(te['Action'] - 6.5) < 1e-6", "msg": "Action mean=6.5"}],
               ["groupby + mean — простой target encoding", "Опасен утечкой на проде"], 3),
            ex(9, "python", "Объедини редкие категории: замени все жанры с частотой <2 на 'other'.",
               "import pandas as pd\ndf = pd.DataFrame({'genre':['RPG','RPG','Action','Sports']})\ndf['genre_clean'] = None\n",
               "import pandas as pd\ndf = pd.DataFrame({'genre':['RPG','RPG','Action','Sports']})\nfreq = df['genre'].value_counts()\nrare = freq[freq < 2].index\ndf['genre_clean'] = df['genre'].replace(rare, 'other')\nprint(df)",
               [{"check": "'genre_clean' in df.columns", "msg": "Колонка создана"},
                {"check": "(df['genre_clean'] == 'other').sum() == 2", "msg": "Action и Sports → other"}],
               ["value_counts + index + replace", "Редкие категории — шум"], 3),
            ex(10, "python", "fit на train, transform на test: обучи LabelEncoder на train, примени к test. "
                             "Если новой категории нет — le.transform упадёт, поэтому оборачиваем в try.",
               "from sklearn.preprocessing import LabelEncoder\ntrain = ['RPG','Action','Sports']\ntest = ['RPG','Sports','FPS']\nle = LabelEncoder()\nle.fit(train)\nresult = []\n",
               "from sklearn.preprocessing import LabelEncoder\ntrain = ['RPG','Action','Sports']\ntest = ['RPG','Sports','FPS']\nle = LabelEncoder()\nle.fit(train)\nknown = set(le.classes_)\nresult = [le.transform([x])[0] if x in known else -1 for x in test]\nprint(result)",
               [{"check": "result[0] == 0 or result[0] == 1 or result[0] == 2", "msg": "RPG кодируется"},
                {"check": "result[2] == -1", "msg": "FPS — неизвестная → -1"}],
               ["set(le.classes_) — известные классы", "-1 для неизвестных — простой sentinel"], 3),
        ],
        minutes=50, difficulty=2,
    )


def _8_4():
    return lesson(
        "8.4", "Масштабирование: MinMax, Standard, Robust", "gaming", [
            theory(
                "Разные признаки часто имеют разный масштаб: age ∈ [0, 100], price ∈ [0, 1000], "
                "rating ∈ [0, 10]. Модели, основанные на расстояниях (KNN, SVM, K-means) и "
                "градиентном спуске (нейросети, линейная регрессия), работают хуже, когда один "
                "признак доминирует.\n\n"
                "**Три главных скейлера:**\n\n"
                "**1. MinMaxScaler** — приводит значения в диапазон [0, 1]:\n"
                "  x' = (x - min) / (max - min)\n"
                "  Плюс: фиксированный диапазон. Минус: чувствителен к выбросам.\n\n"
                "**2. StandardScaler** — приводит к N(0, 1) (среднее 0, std 1):\n"
                "  x' = (x - mean) / std\n"
                "  Плюс: устойчив к выбросам чуть лучше. Минус: нет фиксированного диапазона.\n\n"
                "**3. RobustScaler** — использует медиану и IQR (межквартильный размах):\n"
                "  x' = (x - median) / IQR\n"
                "  Плюс: очень устойчив к выбросам. Минус: менее интуитивен.\n\n"
                "**Важно:** деревья решений (RandomForest, XGBoost) не требуют масштабирования."
            ),
            analogy(
                "Масштабирование — это привести всех к одному росту для фото: "
                "кто-то 150 см, кто-то 200 см — на фото они выглядят одинаково.",
                "MinMax сжимает rating [0..10] и price [0..1000] в один диапазон [0..1], "
                "чтобы модель не 'смотрела' только на цену."
            ),
            visual(
                "Сравнение скейлеров на выбросах",
                "  Исходные:  [1, 2, 3, 4, 5, 100]  ← выброс 100\n"
                "\n"
                "  MinMax:    [0.00, 0.01, 0.02, 0.03, 0.04, 1.00]\n"
                "             ↑ все значения сжались в ноль\n"
                "\n"
                "  Standard:  [-1.0, -1.0, -1.0, -0.99, -0.99, 2.0]\n"
                "             ↑ выброс далеко, остальные сжаты\n"
                "\n"
                "  Robust:    [-1.0, -0.5, 0.0, 0.5, 1.0, 47.5]\n"
                "             ↑ выброс всё ещё большой, но остальные распределены нормально"
            ),
            example(
                "Сравни MinMax и Standard на массиве [10, 20, 30, 40, 50].",
                "MinMax даст [0, 0.25, 0.5, 0.75, 1]. Standard даст [-1.41, -0.71, 0, 0.71, 1.41] — "
                "симметрично вокруг нуля.",
                "import numpy as np\n"
                "from sklearn.preprocessing import MinMaxScaler, StandardScaler\n"
                "X = np.array([[10],[20],[30],[40],[50]], dtype=float)\n"
                "mm = MinMaxScaler().fit_transform(X).flatten()\n"
                "ss = StandardScaler().fit_transform(X).flatten()\n"
                "print('MinMax:', mm.round(3))\n"
                "print('Standard:', ss.round(3))",
                "MinMax: [0.    0.25  0.5   0.75  1.   ]\nStandard: [-1.414 -0.707  0.     0.707  1.414]",
                "MinMax: (10-10)/(50-10) = 0; (50-10)/(50-10) = 1. "
                "Standard: среднее 30, std ≈ 14.14; (10-30)/14.14 ≈ -1.41."
            ),
            common_mistakes([
                {"mistake": "Масштабирование до train/test split (data leakage)",
                 "why_bad": "Scaler 'видел' среднее и std теста → завышенная оценка",
                 "fix": "Сначала split, потом fit на train, transform на test"},
                {"mistake": "Использовать Standard, когда есть огромные выбросы",
                 "why_bad": "std раздут, остальные значения сжаты в ноль",
                 "fix": "Сначала клипуем выбросы (winsorize) или используем RobustScaler"},
                {"mistake": "Scaler на категориальных/бинарных фичах",
                 "why_bad": "MinMax превратит 0/1 в 0/0.27 — бессмысленно",
                 "fix": "Масштабируем только числовые непрерывные"},
                {"mistake": "Не сохранить скейлер для продакшна",
                 "why_bad": "Новые данные отскейлятся по-другому → мусор на инференсе",
                 "fix": "joblib.dump(scaler, 'scaler.pkl') и применяем тот же объект"},
            ]),
            interview_questions([
                {"q": "Зачем масштабировать признаки?",
                 "a": "Чтобы признаки с большим масштабом не доминировали в расстояниях и градиентах. "
                      "Критично для KNN, SVM, K-means, нейросетей, линейной регрессии."},
                {"q": "Чем MinMax отличается от Standard?",
                 "a": "MinMax: x' = (x-min)/(max-min), результат в [0,1]. Чувствителен к выбросам. "
                      "Standard: x' = (x-mean)/std, среднее 0 и std 1. Менее чувствителен, "
                      "но нет фиксированного диапазона."},
                {"q": "Когда использовать RobustScaler?",
                 "a": "Когда в данных есть сильные выбросы: использует медиану и IQR вместо "
                      "среднего и std. Полезен для финансовых, медицинских данных."},
                {"q": "Нужно ли масштабировать для Random Forest?",
                 "a": "Нет. Деревья используют пороги и не чувствительны к масштабу. "
                      "Масштабировать нужно для KNN, SVM, линейной/логистической регрессии, "
                      "нейросетей."},
            ]),
            knowledge_checklist([
                "Знаю формулу MinMax, Standard, Robust",
                "Применяю fit на train, transform на test",
                "Понимаю, какие модели требуют масштабирования",
                "Использую RobustScaler при выбросах",
                "Сохраняю скейлер для инференса",
                "Не масштабирую категориальные признаки",
            ]),
        ],
        exercises=[
            ex(1, "python", "Создай массив X = [[10],[20],[30],[40],[50]]. MinMaxScaler.fit_transform(X). "
                            "Сохрани в `scaled`.",
               "import numpy as np\nfrom sklearn.preprocessing import MinMaxScaler\nX = np.array([[10],[20],[30],[40],[50]], dtype=float)\nscaled = None\n",
               "import numpy as np\nfrom sklearn.preprocessing import MinMaxScaler\nX = np.array([[10],[20],[30],[40],[50]], dtype=float)\nscaled = MinMaxScaler().fit_transform(X)\nprint(scaled.flatten().round(2))",
               [{"check": "isinstance(scaled, np.ndarray)", "msg": "ndarray"},
                {"check": "scaled.min() >= 0 and scaled.max() <= 1", "msg": "В диапазоне [0, 1]"}],
               ["MinMaxScaler.fit_transform сразу", "На вход 2D"], 1),
            ex(2, "python", "StandardScaler на том же X. Сохрани в `ss`.",
               "import numpy as np\nfrom sklearn.preprocessing import StandardScaler\nX = np.array([[10],[20],[30],[40],[50]], dtype=float)\nss = None\n",
               "import numpy as np\nfrom sklearn.preprocessing import StandardScaler\nX = np.array([[10],[20],[30],[40],[50]], dtype=float)\nss = StandardScaler().fit_transform(X)\nprint(ss.flatten().round(2))",
               [{"check": "abs(ss.mean()) < 1e-6", "msg": "Среднее ≈ 0"},
                {"check": "abs(ss.std() - 1) < 1e-6", "msg": "std ≈ 1"}],
               ["StandardScaler центрирует", "std=1 после трансформа"], 1),
            ex(3, "python", "RobustScaler на X = [[1],[2],[3],[4],[5],[100]]. Сохрани в `rs`.",
               "import numpy as np\nfrom sklearn.preprocessing import RobustScaler\nX = np.array([[1],[2],[3],[4],[5],[100]], dtype=float)\nrs = None\n",
               "import numpy as np\nfrom sklearn.preprocessing import RobustScaler\nX = np.array([[1],[2],[3],[4],[5],[100]], dtype=float)\nrs = RobustScaler().fit_transform(X)\nprint(rs.flatten().round(2))",
               [{"check": "isinstance(rs, np.ndarray)", "msg": "ndarray"},
                {"check": "rs.shape == (6, 1)", "msg": "(6, 1)"}],
               ["Robust — медиана и IQR", "Устойчив к выбросу 100"], 2),
            ex(4, "python", "Сделай MinMax на колонке rating DataFrame. Сохрани в `df['rating_mm']`.",
               "import pandas as pd\nfrom sklearn.preprocessing import MinMaxScaler\ndf = pd.DataFrame({'rating':[2,4,6,8,10]})\n",
               "import pandas as pd\nfrom sklearn.preprocessing import MinMaxScaler\ndf = pd.DataFrame({'rating':[2,4,6,8,10]})\ndf['rating_mm'] = MinMaxScaler().fit_transform(df[['rating']])\nprint(df)",
               [{"check": "'rating_mm' in df.columns", "msg": "Колонка rating_mm"},
                {"check": "abs(df['rating_mm'].min() - 0) < 1e-6", "msg": "min=0"},
                {"check": "abs(df['rating_mm'].max() - 1) < 1e-6", "msg": "max=1"}],
               ["df[['col']] — 2D для sklearn", "fit_transform возвращает массив"], 2),
            ex(5, "python", "Сравни среднее и std до и после StandardScaler. "
                            "Сохрани `mean_after` и `std_after`.",
               "import numpy as np\nfrom sklearn.preprocessing import StandardScaler\nnp.random.seed(0)\nX = np.random.randn(100, 1) * 5 + 100\nmean_after = 0\nstd_after = 0\n",
               "import numpy as np\nfrom sklearn.preprocessing import StandardScaler\nnp.random.seed(0)\nX = np.random.randn(100, 1) * 5 + 100\ns = StandardScaler().fit_transform(X)\nmean_after = s.mean()\nstd_after = s.std()\nprint(round(mean_after, 2), round(std_after, 2))",
               [{"check": "abs(mean_after) < 0.1", "msg": "mean ≈ 0"},
                {"check": "abs(std_after - 1) < 0.1", "msg": "std ≈ 1"}],
               ["np.random.seed для воспроизводимости", "После Standard: mean=0, std=1"], 2),
            ex(6, "python", "Сделай ручной MinMax: scaled = (x - x.min()) / (x.max() - x.min()).",
               "import numpy as np\nx = np.array([5, 10, 15, 20])\nresult = x\n",
               "import numpy as np\nx = np.array([5, 10, 15, 20])\nresult = (x - x.min()) / (x.max() - x.min())\nprint(result)",
               [{"check": "abs(result[0] - 0) < 1e-6", "msg": "min → 0"},
                {"check": "abs(result[-1] - 1) < 1e-6", "msg": "max → 1"}],
               ["Ручной MinMax без sklearn", "(x-min)/(max-min)"], 1),
            ex(7, "python", "Сделай ручной Standard: z = (x - x.mean()) / x.std().",
               "import numpy as np\nx = np.array([10, 20, 30, 40, 50], dtype=float)\nz = x\n",
               "import numpy as np\nx = np.array([10, 20, 30, 40, 50], dtype=float)\nz = (x - x.mean()) / x.std()\nprint(z.round(2))",
               [{"check": "abs(z.mean()) < 1e-6", "msg": "mean=0"},
                {"check": "abs(z.std() - 1) < 1e-6", "msg": "std=1"}],
               ["mean=30, std≈14.14", "(x-mean)/std"], 2),
            ex(8, "python", "fit на train, transform на test: MinMaxScaler на price. "
                            "Сохрани в `test_scaled`.",
               "import numpy as np\nfrom sklearn.preprocessing import MinMaxScaler\ntrain = np.array([[10],[20],[30]])\ntest = np.array([[15],[25]])\ntest_scaled = None\n",
               "import numpy as np\nfrom sklearn.preprocessing import MinMaxScaler\ntrain = np.array([[10],[20],[30]])\ntest = np.array([[15],[25]])\nsc = MinMaxScaler()\nsc.fit(train)\ntest_scaled = sc.transform(test)\nprint(test_scaled.flatten())",
               [{"check": "isinstance(test_scaled, np.ndarray)", "msg": "ndarray"},
                {"check": "abs(test_scaled[0, 0] - 0.25) < 1e-6", "msg": "15: (15-10)/20 = 0.25"}],
               ["fit на train, transform на test", "Без утечки данных"], 2),
            ex(9, "python", "RobustScaler на price с выбросом. Сравни с MinMax — у какого значения "
                            "масштаб меньше 'сломан'? Сохрани min/max в `rs_min`, `rs_max`.",
               "import numpy as np\nfrom sklearn.preprocessing import RobustScaler\nX = np.array([[1],[2],[3],[4],[1000]], dtype=float)\nrs_min = 0\nrs_max = 0\n",
               "import numpy as np\nfrom sklearn.preprocessing import RobustScaler\nX = np.array([[1],[2],[3],[4],[1000]], dtype=float)\nrs = RobustScaler().fit_transform(X)\nrs_min = rs.min()\nrs_max = rs.max()\nprint('Robust:', round(rs_min, 2), round(rs_max, 2))",
               [{"check": "abs(rs_min) < 5 and abs(rs_max) < 5", "msg": "Robust держит обычные значения в разумном диапазоне"}],
               ["median=3, IQR=1.5", "1000 → огромный, но 1,2,3,4 — норм"], 3),
            ex(10, "python", "Сохрани MinMaxScaler в файл через joblib и загрузи обратно. "
                             "Сохрани в `loaded`.",
               "import numpy as np\nfrom sklearn.preprocessing import MinMaxScaler\nimport joblib\nimport io\nsc = MinMaxScaler().fit(np.array([[0],[10]], dtype=float))\nloaded = None\n",
               "import numpy as np\nfrom sklearn.preprocessing import MinMaxScaler\nimport joblib\nsc = MinMaxScaler().fit(np.array([[0],[10]], dtype=float))\nbuf = io.BytesIO()\njoblib.dump(sc, buf)\nbuf.seek(0)\nloaded = joblib.load(buf)\nprint(loaded.transform([[5]]))",
               [{"check": "isinstance(loaded, MinMaxScaler)", "msg": "MinMaxScaler instance"}],
               ["joblib.dump / joblib.load", "Важно для продакшна"], 3),
        ],
        minutes=55, difficulty=2,
    )


def _8_5():
    return lesson(
        "8.5", "Работа с датами: извлечение признаков", "gaming", [
            theory(
                "Дата и время — золотая жила для фичей. Из одного timestamp можно достать десятки "
                "полезных признаков.\n\n"
                "**Что извлекать:**\n"
                "- **year, month, day** — базовые компоненты.\n"
                "- **dayofweek** (0=Пн, 6=Вс) — паттерны выходных.\n"
                "- **hour** — суточные пики активности.\n"
                "- **quarter, weekofyear** — сезонность.\n"
                "- **is_weekend** — бинарный флаг.\n"
                "- **days_since** — сколько дней прошло с события (релиз → сейчас).\n"
                "- **is_month_start/end** — флаги начала/конца месяца.\n\n"
                "**Инструменты:**\n"
                "- `pd.to_datetime()` — парсинг строк в datetime.\n"
                "- `.dt.year`, `.dt.month`, `.dt.day` — атрибуты.\n"
                "- `.dt.day_name()` — название дня.\n"
                "- `np.datetime64`, `pd.Timestamp` — базовые типы."
            ),
            analogy(
                "Дата — это запечатанный конверт: внутри спрятаны кусочки информации (год, месяц, "
                "день, час). Чтобы их достать — нужно вскрыть конверт через pd.to_datetime.",
                "Из '2024-03-15 14:30:00' достаём year=2024, month=3, day=15, hour=14, "
                "dayofweek=4 (пятница)."
            ),
            visual(
                "Анатомия datetime",
                "  '2024-03-15 14:30:45'\n"
                "  │  │  │  │  │  │  │\n"
                "  │  │  │  │  │  └─── second=45\n"
                "  │  │  │  │  └────── minute=30\n"
                "  │  │  │  └───────── hour=14\n"
                "  │  │  └──────────── day=15\n"
                "  │  └─────────────── month=3\n"
                "  └────────────────── year=2024\n"
                "\n"
                "  dayofweek=4 (Friday)\n"
                "  quarter=1\n"
                "  is_weekend=False"
            ),
            example(
                "Распарси дату и извлеки year, month, day, dayofweek, hour.",
                "pd.to_datetime превращает строку в datetime. Атрибут .dt даёт доступ к компонентам.",
                "import pandas as pd\n"
                "df = pd.DataFrame({'ts':['2024-03-15 14:30:00','2024-07-20 09:15:00']})\n"
                "df['ts'] = pd.to_datetime(df['ts'])\n"
                "df['year'] = df['ts'].dt.year\n"
                "df['month'] = df['ts'].dt.month\n"
                "df['day'] = df['ts'].dt.day\n"
                "df['dow'] = df['ts'].dt.dayofweek\n"
                "df['hour'] = df['ts'].dt.hour\n"
                "print(df)",
                "                   ts  year  month  day  dow  hour\n"
                "0 2024-03-15 14:30:00  2024      3   15    4    14\n"
                "1 2024-07-20 09:15:00  2024      7   20    5     9",
                "2024-03-15 — пятница (dayofweek=4). 2024-07-20 — суббота (dayofweek=5). "
                "Можно добавить is_weekend = dow >= 5."
            ),
            common_mistakes([
                {"mistake": "Не парсить дату — оставить строкой",
                 "why_bad": "Модель не понимает '2024-03-15' как дату, теряем кучу информации",
                 "fix": "Всегда pd.to_datetime с указанием формата при необходимости"},
                {"mistake": "Забыть про таймзону",
                 "why_bad": "Событие в 23:00 UTC = 02:00 следующего дня в Москве",
                 "fix": "df['ts'] = pd.to_datetime(df['ts'], utc=True).dt.tz_convert('Europe/Moscow')"},
                {"mistake": "Считать days_since от текущей даты при обучении",
                 "why_bad": "Утечка: модель знает сегодняшнее число, на проде — другое",
                 "fix": "Считаем days_since от reference_date (например, релиза игры)"},
                {"mistake": "Использовать dayofweek как число без учёта порядка",
                 "why_bad": "Линейная модель решит, что 6 (вс) > 0 (пн) — это шум",
                 "fix": "Либо OHE dayofweek, либо sin/cos-кодировка циклических фичей"},
            ]),
            interview_questions([
                {"q": "Зачем извлекать фичи из дат, а не подавать их как есть?",
                 "a": "Числовой timestamp — это просто счётчик секунд. Модель не знает, что 'выходные' "
                      "или 'праздники' важны. Извлечённые фичи дают семантику: месяц, день недели, "
                      "час пик."},
                {"q": "Что такое циклические фичи и зачем их кодировать через sin/cos?",
                 "a": "Час 23 и час 0 — близки по смыслу, но 23 ≠ 0. sin/cos превращают круг в 2D: "
                      "hour_sin=sin(2π*h/24), hour_cos=cos(2π*h/24). Модель видит 'близость'."},
                {"q": "Как обработать пропущенные даты?",
                 "a": "Заменить на placeholder дату, создать флаг is_missing, либо импутировать "
                      "медианой/средним. Зависит от домена."},
            ]),
            knowledge_checklist([
                "Парсю даты через pd.to_datetime",
                "Извлекаю year, month, day, dayofweek, hour",
                "Создаю is_weekend, quarter, weekofyear",
                "Считаю days_since от reference_date",
                "Использую sin/cos для циклических фичей",
                "Понимаю риск утечки при days_since от now",
            ]),
        ],
        exercises=[
            ex(1, "python", "pd.to_datetime для списка строк. Сохрани Series в `ts`.",
               "import pandas as pd\ndates = ['2024-01-15','2024-06-20','2024-12-31']\nts = None\n",
               "import pandas as pd\ndates = ['2024-01-15','2024-06-20','2024-12-31']\nts = pd.to_datetime(dates)\nprint(ts)",
               [{"check": "isinstance(ts, pd.Series)", "msg": "Series"},
                {"check": "ts.dtype.kind == 'M'", "msg": "datetime dtype"}],
               ["pd.to_datetime превращает в datetime64", "dtype.kind='M' для datetime"], 1),
            ex(2, "python", "Из Series `ts` извлеки year, month, day. Сохрани в df.",
               "import pandas as pd\nts = pd.to_datetime(['2024-03-15','2024-07-20'])\ndf = pd.DataFrame()\n",
               "import pandas as pd\nts = pd.to_datetime(['2024-03-15','2024-07-20'])\ndf = pd.DataFrame()\ndf['year'] = ts.dt.year\ndf['month'] = ts.dt.month\ndf['day'] = ts.dt.day\nprint(df)",
               [{"check": "'year' in df.columns", "msg": "Колонка year"},
                {"check": "df['year'].iloc[0] == 2024", "msg": "year=2024"},
                {"check": "df['month'].iloc[0] == 3", "msg": "month=3"}],
               [".dt.year, .dt.month, .dt.day", "Атрибут .dt — аксессор"], 1),
            ex(3, "python", "Из ts достань dayofweek (0=Пн, 6=Вс). Сохрани в `dow`.",
               "import pandas as pd\nts = pd.to_datetime(['2024-03-15','2024-03-16','2024-03-17'])\ndow = None\n",
               "import pandas as pd\nts = pd.to_datetime(['2024-03-15','2024-03-16','2024-03-17'])\ndow = ts.dt.dayofweek\nprint(dow.tolist())",
               [{"check": "isinstance(dow, pd.Series)", "msg": "Series"},
                {"check": "dow.iloc[0] == 4", "msg": "15 марта 2024 = пятница = 4"}],
               [".dt.dayofweek", "Понедельник = 0"], 2),
            ex(4, "python", "Из ts достань hour. Сохрани в `hours`.",
               "import pandas as pd\nts = pd.to_datetime(['2024-01-01 09:30','2024-01-01 23:45'])\nhours = None\n",
               "import pandas as pd\nts = pd.to_datetime(['2024-01-01 09:30','2024-01-01 23:45'])\nhours = ts.dt.hour\nprint(hours.tolist())",
               [{"check": "hours.iloc[0] == 9", "msg": "9 утра"},
                {"check": "hours.iloc[1] == 23", "msg": "23 вечера"}],
               [".dt.hour", "Извлекаем час"], 1),
            ex(5, "python", "Создай `is_weekend = dayofweek >= 5`. Сохрани в Series.",
               "import pandas as pd\nts = pd.to_datetime(['2024-03-15','2024-03-16','2024-03-17'])\nis_weekend = None\n",
               "import pandas as pd\nts = pd.to_datetime(['2024-03-15','2024-03-16','2024-03-17'])\nis_weekend = (ts.dt.dayofweek >= 5)\nprint(is_weekend.tolist())",
               [{"check": "is_weekend.iloc[0] == False", "msg": "Пт — не выходной"},
                {"check": "is_weekend.iloc[1] == True", "msg": "Сб — выходной"},
                {"check": "is_weekend.iloc[2] == True", "msg": "Вс — выходной"}],
               ["dayofweek >= 5 для сб/вс", "Вс = 6, Сб = 5"], 2),
            ex(6, "python", "Посчитай `days_since = (ts - ref_date).dt.days`. ref_date = '2020-01-01'.",
               "import pandas as pd\nts = pd.to_datetime(['2020-01-01','2024-01-01'])\nref = pd.Timestamp('2020-01-01')\ndays_since = None\n",
               "import pandas as pd\nts = pd.to_datetime(['2020-01-01','2024-01-01'])\nref = pd.Timestamp('2020-01-01')\ndays_since = (ts - ref).dt.days\nprint(days_since.tolist())",
               [{"check": "days_since.iloc[0] == 0", "msg": "0 дней"},
                {"check": "abs(days_since.iloc[1] - 1461) < 2", "msg": "≈ 1461 день (4 года)"}],
               ["datetime - datetime = Timedelta", ".dt.days извлекает дни"], 2),
            ex(7, "python", "Создай quarter (1-4) через `.dt.quarter`. Сохрани в `q`.",
               "import pandas as pd\nts = pd.to_datetime(['2024-01-15','2024-05-15','2024-09-15','2024-12-15'])\nq = None\n",
               "import pandas as pd\nts = pd.to_datetime(['2024-01-15','2024-05-15','2024-09-15','2024-12-15'])\nq = ts.dt.quarter\nprint(q.tolist())",
               [{"check": "q.iloc[0] == 1", "msg": "Янв = Q1"},
                {"check": "q.iloc[1] == 2", "msg": "Май = Q2"},
                {"check": "q.iloc[3] == 4", "msg": "Дек = Q4"}],
               [".dt.quarter", "1=Янв-Мар, 2=Апр-Июн..."], 1),
            ex(8, "python", "Циклическая фича: hour_sin = sin(2*pi*hour/24), hour_cos = cos(...). "
                            "Сохрани массив в `cyclic`.",
               "import numpy as np\nhours = np.array([0, 6, 12, 18])\ncyclic = None\n",
               "import numpy as np\nhours = np.array([0, 6, 12, 18])\ncyclic = np.column_stack([np.sin(2*np.pi*hours/24), np.cos(2*np.pi*hours/24)])\nprint(cyclic)",
               [{"check": "cyclic.shape == (4, 2)", "msg": "(4, 2) — 4 часа, 2 фичи"},
                {"check": "abs(cyclic[0, 0] - 0) < 1e-6", "msg": "sin(0) = 0"},
                {"check": "abs(cyclic[3, 0] - (-1)) < 1e-6", "msg": "sin(18*2π/24) = sin(3π/2) = -1"}],
               ["sin/cos — стандарт для циклов", "column_stack собирает в матрицу"], 3),
            ex(9, "python", "Из ts достань название дня недели. Сохрани в `day_name`.",
               "import pandas as pd\nts = pd.to_datetime(['2024-03-15'])\nday_name = None\n",
               "import pandas as pd\nts = pd.to_datetime(['2024-03-15'])\nday_name = ts.dt.day_name()\nprint(day_name.iloc[0])",
               [{"check": "day_name.iloc[0] == 'Friday'", "msg": "Пятница = Friday"}],
               [".dt.day_name()", "Английский вывод по умолчанию"], 1),
            ex(10, "python", "Парсинг с форматом: to_datetime('15-03-2024', format='%d-%m-%Y').",
               "import pandas as pd\nresult = None\n",
               "import pandas as pd\nresult = pd.to_datetime(['15-03-2024'], format='%d-%m-%Y')\nprint(result.iloc[0])",
               [{"check": "str(result.iloc[0])[:10] == '2024-03-15'", "msg": "Распарсилось в 2024-03-15"}],
               ["format='%d-%m-%Y'", "Быстрее и безопаснее"], 2),
        ],
        minutes=50, difficulty=2,
    )


def _8_6():
    return lesson(
        "8.6", "Базовая обработка текста", "gaming", [
            theory(
                "Текст — самый богатый и самый сложный источник фичей. Простые подходы (Bag of Words, "
                "TF-IDF) уже дают хороший результат и не требуют нейросетей.\n\n"
                "**Bag of Words (CountVectorizer):**\n"
                "Считает, сколько раз каждое слово встречается в документе. Документ → вектор частот.\n"
                "  'great game' → [1, 1, 0, 0, ...]\n\n"
                "**TF-IDF (TfidfVectorizer):**\n"
                "TF = частота слова в документе, IDF = log(N / df). Слова 'the', 'is' получают "
                "маленький вес, а редкие 'breathtaking' — большой.\n\n"
                "**Препроцессинг:**\n"
                "- Приведение к нижнему регистру: 'Game' → 'game'.\n"
                "- Удаление пунктуации: `re.sub(r'[^\\w\\s]', '', text)`.\n"
                "- Удаление стоп-слов (the, is, a) — `stop_words='english'`.\n"
                "- Стемминг/лемматизация (snowball, wordnet) — play, played, playing → play.\n\n"
                "**Метрики фичей:**\n"
                "- n-grams: униграммы (одно слово), биграммы (пары), триграммы.\n"
                "- max_features: ограничение словаря.\n"
                "- min_df, max_df: отсечение редких/частых слов."
            ),
            analogy(
                "Текст — это картина из кубиков. CountVectorizer считает, сколько кубиков каждого "
                "цвета в картине. TF-IDF — то же, но штрафует цвета, которые есть в каждой картине "
                "(серый фон).",
                "Отзыв 'boring boring story' → BoW: boring=2, story=1. TF-IDF: boring тоже высок, "
                "если в других отзывах его нет."
            ),
            visual(
                "CountVectorizer vs TF-IDF",
                "  Документы:\n"
                "    D1: 'great game'\n"
                "    D2: 'boring game'\n"
                "    D3: 'great story'\n"
                "\n"
                "  Словарь: {great, game, boring, story}\n"
                "\n"
                "  Count:            TF-IDF:\n"
                "  ┌────────────┐    ┌─────────────────────┐\n"
                "  │ 1 1 0 0  D1│    │ 0.7 0.3  0   0   D1 │\n"
                "  │ 0 1 1 0  D2│    │  0  0.3 0.7  0   D2 │\n"
                "  │ 1 0 0 1  D3│    │ 0.7  0   0  0.7  D3 │\n"
                "  └────────────┘    └─────────────────────┘"
            ),
            example(
                "Примени CountVectorizer к трём отзывам об играх. Посмотри shape.",
                "CountVectorizer.fit_transform превращает корпус в разреженную матрицу. "
                "shape = (n_docs, n_features).",
                "from sklearn.feature_extraction.text import CountVectorizer\n"
                "docs = ['great game with great story',\n"
                "        'boring gameplay',\n"
                "        'amazing graphics and story']\n"
                "cv = CountVectorizer()\n"
                "X = cv.fit_transform(docs)\n"
                "print('Shape:', X.shape)\n"
                "print('Vocab:', cv.get_feature_names_out())",
                "Shape: (3, 8)\nVocab: ['amazing' 'and' 'boring' 'game' 'gameplay' 'graphics' 'great' 'story']",
                "8 уникальных слов. В D1 'great' встретилось 2 раза. "
                "В D3 'story' встретилось 1 раз, как и 'and', 'amazing', 'graphics'."
            ),
            common_mistakes([
                {"mistake": "fit_transform на всех данных, потом split",
                 "why_bad": "Утечка: TF-IDF знает слова из теста",
                 "fix": "Сначала split, потом fit на train, transform на test"},
                {"mistake": "Слишком большой max_features",
                 "why_bad": "Память, шум, медленное обучение",
                 "fix": "max_features=1000..10000 — хорошая отправная точка"},
                {"mistake": "Не убирать стоп-слова",
                 "why_bad": "'the', 'is', 'a' занимают место и шумят",
                 "fix": "stop_words='english' в CountVectorizer/TfidfVectorizer"},
                {"mistake": "Токенизация без учёта регистра и знаков препинания",
                 "why_bad": "'Game' и 'game' — разные токены, шум",
                 "fix": "lowercase=True (по умолчанию), регулярка для токенов"},
                {"mistake": "Огромный словарь из-за min_df=1",
                 "why_bad": "Каждое уникальное слово = фича, переобучение",
                 "fix": "min_df=2 или 5 — отсекаем редкие слова"},
            ]),
            interview_questions([
                {"q": "Чем CountVectorizer отличается от TfidfVectorizer?",
                 "a": "CountVectorizer — частоты слов. TfidfVectorizer — TF * IDF, штрафует слова, "
                      "которые встречаются во многих документах. TF-IDF обычно лучше для классификации."},
                {"q": "Зачем нужны n-grams?",
                 "a": "Биграммы 'not good' дают негативный смысл, который невидим в униграммах. "
                      "Триграммы 'New York' — это один смысл, не два слова. Но n-grams раздувают "
                      "словарь, нужна балансировка."},
                {"q": "Что такое стемминг и лемматизация?",
                 "a": "Стемминг — отсечение окончаний (playing → play). Лемматизация — приведение "
                      "к начальной форме (better → good). Лемматизация точнее, но медленнее."},
            ]),
            knowledge_checklist([
                "Использую CountVectorizer и TfidfVectorizer",
                "Применяю fit на train, transform на test",
                "Ограничиваю max_features, min_df",
                "Убираю стоп-слова",
                "Использую n-grams (bigram, trigram)",
                "Понимаю формулу TF-IDF",
            ]),
        ],
        exercises=[
            ex(1, "python", "CountVectorizer на 2 документа. Сохрани матрицу в `X`.",
               "from sklearn.feature_extraction.text import CountVectorizer\ndocs = ['great game', 'bad game']\nX = None\n",
               "from sklearn.feature_extraction.text import CountVectorizer\ndocs = ['great game', 'bad game']\nX = CountVectorizer().fit_transform(docs)\nprint(X.shape)",
               [{"check": "X.shape == (2, 3)", "msg": "(2, 3) — 2 документа, 3 слова"}],
               ["fit_transform возвращает sparse matrix", "Словарь строится автоматически"], 1),
            ex(2, "python", "Получи словарь через get_feature_names_out. Сохрани в `vocab`.",
               "from sklearn.feature_extraction.text import CountVectorizer\ndocs = ['cat dog', 'dog bird']\nvocab = None\n",
               "from sklearn.feature_extraction.text import CountVectorizer\ndocs = ['cat dog', 'dog bird']\ncv = CountVectorizer()\ncv.fit(docs)\nvocab = cv.get_feature_names_out()\nprint(vocab)",
               [{"check": "isinstance(vocab, np.ndarray)", "msg": "ndarray"},
                {"check": "set(vocab) == {'cat','dog','bird'}", "msg": "3 слова"}],
               ["get_feature_names_out → массив имён", "Сортировка по алфавиту"], 2),
            ex(3, "python", "TfidfVectorizer на 3 документа. Сохрани в `X`.",
               "from sklearn.feature_extraction.text import TfidfVectorizer\ndocs = ['great game', 'bad game', 'great story']\nX = None\n",
               "from sklearn.feature_extraction.text import TfidfVectorizer\ndocs = ['great game', 'bad game', 'great story']\nX = TfidfVectorizer().fit_transform(docs)\nprint(X.shape)",
               [{"check": "X.shape == (3, 4)", "msg": "(3, 4) — 3 документа, 4 слова"}],
               ["TfidfVectorizer — TF * IDF", "Штрафует частые слова"], 2),
            ex(4, "python", "CountVectorizer с stop_words='english'. Слова 'the', 'is' не попадут в словарь.",
               "from sklearn.feature_extraction.text import CountVectorizer\ndocs = ['this is a great game', 'the game is good']\nX = None\n",
               "from sklearn.feature_extraction.text import CountVectorizer\ndocs = ['this is a great game', 'the game is good']\nX = CountVectorizer(stop_words='english').fit_transform(docs)\nprint(X.shape)",
               [{"check": "X.shape[1] <= 3", "msg": "Стоп-слова убраны"}],
               ["stop_words='english'", "Убирает the, is, a..."], 2),
            ex(5, "python", "TfidfVectorizer с max_features=100. Сохрани shape в `s`.",
               "from sklearn.feature_extraction.text import TfidfVectorizer\nimport numpy as np\nrng = np.random.RandomState(0)\ndocs = ['word' + str(i) for i in rng.randint(0, 500, 200)]\ns = None\n",
               "from sklearn.feature_extraction.text import TfidfVectorizer\nimport numpy as np\nrng = np.random.RandomState(0)\ndocs = ['word' + str(i) for i in rng.randint(0, 500, 200)]\ns = TfidfVectorizer(max_features=100).fit_transform(docs).shape\nprint(s)",
               [{"check": "s[1] == 100", "msg": "100 фичей (max_features)"}],
               ["max_features ограничивает словарь", "Топ-100 по частоте"], 2),
            ex(6, "python", "TfidfVectorizer с ngram_range=(1,2). Должны быть униграммы и биграммы.",
               "from sklearn.feature_extraction.text import TfidfVectorizer\ndocs = ['great game', 'great story']\nX = None\n",
               "from sklearn.feature_extraction.text import TfidfVectorizer\ndocs = ['great game', 'great story']\nX = TfidfVectorizer(ngram_range=(1,2)).fit_transform(docs)\nprint(X.shape)",
               [{"check": "X.shape[1] >= 4", "msg": "Униграммы + биграммы"}],
               ["ngram_range=(1,2) — уни + би", "great game, great story"], 3),
            ex(7, "python", "Приведение к нижнему регистру: text.lower().",
               "text = 'GREAT Game'\nresult = text\n",
               "text = 'GREAT Game'\nresult = text.lower()\nprint(result)",
               [{"check": "result == 'great game'", "msg": "В нижнем регистре"}],
               [".lower() — метод строки", "Регистр не важен для BoW"], 1),
            ex(8, "python", "Удаление пунктуации: re.sub(r'[^\\w\\s]', '', text).",
               "import re\ntext = 'great, game! with: fun.'\nresult = text\n",
               "import re\ntext = 'great, game! with: fun.'\nresult = re.sub(r'[^\\w\\s]', '', text)\nprint(result)",
               [{"check": "',' not in result", "msg": "Запятая убрана"},
                {"check": "'!' not in result", "msg": "Восклицательный убран"},
                {"check": "'great' in result", "msg": "Слово great осталось"}],
               ["r'[^\\w\\s]' — всё кроме букв и пробелов", "re.sub заменяет"], 2),
            ex(9, "python", "min_df=2 в CountVectorizer. Слово, встретившееся 1 раз, не попадёт в словарь.",
               "from sklearn.feature_extraction.text import CountVectorizer\ndocs = ['cat dog', 'cat bird', 'mouse']\nX = None\n",
               "from sklearn.feature_extraction.text import CountVectorizer\ndocs = ['cat dog', 'cat bird', 'mouse']\nX = CountVectorizer(min_df=2).fit_transform(docs)\nprint(X.shape)",
               [{"check": "X.shape[1] == 1", "msg": "Только 'cat' (>=2 раза)"}],
               ["min_df=2 — минимум 2 документа", "Отсекает редкие слова"], 3),
            ex(10, "python", "transform на новых данных после fit. Сохрани shape в `new_shape`.",
               "from sklearn.feature_extraction.text import TfidfVectorizer\ntrain = ['great game', 'bad story']\ntest = ['amazing game']\nnew_shape = None\n",
               "from sklearn.feature_extraction.text import TfidfVectorizer\ntrain = ['great game', 'bad story']\ntest = ['amazing game']\ntv = TfidfVectorizer()\ntv.fit(train)\nnew_shape = tv.transform(test).shape\nprint(new_shape)",
               [{"check": "new_shape == (1, 4)", "msg": "1 документ, 4 слова из train"},
                {"check": "new_shape[1] == 4", "msg": "Vocab из train"}],
               ["fit на train, transform на test", "Словарь зафиксирован"], 2),
        ],
        minutes=50, difficulty=2,
    )


def _8_7():
    return lesson(
        "8.7", "Отбор признаков: методы и метрики", "gaming", [
            theory(
                "Больше фичей ≠ лучше. Слишком много признаков ведёт к переобучению, мультиколлинеарности, "
                "медленному обучению и трудно интерпретируемой модели.\n\n"
                "**Три семейства методов отбора:**\n\n"
                "**1. Filter (фильтры):**\n"
                "Оцениваем каждую фичу независимо от модели.\n"
                "- `SelectKBest(score_func=f_classif)` — ANOVA F-value для классификации.\n"
                "- `chi2` — хи-квадрат для категорий.\n"
                "- `mutual_info_classif` — mutual information (нелинейная зависимость).\n"
                "- Корреляция Пирсона с таргетом.\n"
                "**Плюс:** быстро, не зависит от модели. **Минус:** игнорирует взаимодействия.\n\n"
                "**2. Wrapper (обёртки):**\n"
                "Обучаем модель многократно с разными подмножествами.\n"
                "- Recursive Feature Elimination (RFE) — рекурсивно убираем наименее важные.\n"
                "- Forward/Backward selection.\n"
                "**Плюс:** учитывает модель. **Минус:** медленно.\n\n"
                "**3. Embedded (встроенные):**\n"
                "Отбор внутри модели: L1-регуляризация (Lasso), feature_importances_ в деревьях.\n"
                "**Плюс:** быстро, учитывает модель. **Минус:** специфично для модели."
            ),
            analogy(
                "Отбор признаков — это кастинг в фильм. Filter — отсев по фото (быстро, грубо). "
                "Wrapper — пробные съёмки (точно, долго). Embedded — выбор по ходу съёмок (сбалансировано).",
                "Из 1000 фичей отзывов на игры SelectKBest оставит 50 самых 'говорящих' — те, что "
                "отличают положительные отзывы от отрицательных."
            ),
            visual(
                "Pipeline отбора признаков",
                "  ┌─────────────┐\n"
                "  │ 1000 фичей  │\n"
                "  └──────┬──────┘\n"
                "         │ Filter (f_classif, mi)\n"
                "  ┌──────▼──────┐\n"
                "  │  200 фичей  │\n"
                "  └──────┬──────┘\n"
                "         │ Embedded (L1, tree importance)\n"
                "  ┌──────▼──────┐\n"
                "  │   50 фичей  │\n"
                "  └──────┬──────┘\n"
                "         │ Wrapper (RFE)\n"
                "  ┌──────▼──────┐\n"
                "  │   10 фичей  │ — финальная модель\n"
                "  └─────────────┘"
            ),
            example(
                "SelectKBest с f_classif — выбери 2 лучших признака из 4.",
                "f_classif считает F-статистику между фичей и таргетом. Чем больше — тем сильнее связь.",
                "import numpy as np\n"
                "from sklearn.feature_selection import SelectKBest, f_classif\n"
                "X = np.array([[1, 1, 0, 0],[1, 0, 1, 0],[0, 1, 0, 1],[0, 0, 1, 1]])\n"
                "y = np.array([0, 1, 0, 1])\n"
                "sel = SelectKBest(f_classif, k=2).fit(X, y)\n"
                "print('Scores:', sel.scores_.round(2))\n"
                "print('Selected:', sel.get_support())\n"
                "print('X_new shape:', sel.transform(X).shape)",
                "Scores: [0.  4.  0.  4.]\nSelected: [False  True False  True]\nX_new shape: (4, 2)",
                "Фичи 1 и 3 (индексы) дают F=4 — выбраны. Фичи 0 и 2 дают F=0 — отброшены. "
                "Итог: матрица 4x2."
            ),
            common_mistakes([
                {"mistake": "Отбор фичей на всём датасете до split",
                 "why_bad": "Утечка: скор считался с использованием test",
                 "fix": "Сначала split, потом fit_select на train, transform на test"},
                {"mistake": "Использовать f_classif на отрицательных значениях",
                 "why_bad": "f_classif требует неотрицательные значения",
                 "fix": "Сначала MinMax/StandardScaler, потом f_classif"},
                {"mistake": "Выбирать k=10000 из 100 фичей",
                 "why_bad": "SelectKBest с k>n_features не уменьшит размерность",
                 "fix": "k < n_features, обычно 10..50"},
                {"mistake": "Не учитывать мультиколлинеарность",
                 "why_bad": "Сильно коррелирующие фичи дублируют сигнал, переобучение",
                 "fix": "Дропаем одну из пары с corr > 0.95"},
            ]),
            interview_questions([
                {"q": "Чем filter-методы отличаются от wrapper?",
                 "a": "Filter оценивают каждую фичу отдельно (быстро, грубо). Wrapper перебирают "
                      "подмножества (медленно, точно). Embedded — компромисс внутри модели."},
                {"q": "Что такое SelectKBest и какие у него параметры?",
                 "a": "Transformer, выбирающий k фичей с наибольшим скором. Параметры: score_func "
                      "(f_classif, chi2, mutual_info_classif), k (число фичей)."},
                {"q": "Как избежать утечки при отборе фичей?",
                 "a": "Сначала train/test split, потом fit на train, transform на test. Или "
                      "используем pipeline с cross-validation (SelectKBest внутри пайплайна)."},
                {"q": "Что такое L1-регуляризация и как она помогает в отборе?",
                 "a": "Lasso добавляет штраф |w| к функции потерь. Веса不重要ых фичей сжимаются "
                      "к 0 — фактически автоматический отбор."},
            ]),
            knowledge_checklist([
                "Знаю разницу между filter, wrapper, embedded",
                "Использую SelectKBest с f_classif или mutual_info",
                "Применяю fit на train, transform на test",
                "Понимаю ограничения f_classif (только неотрицательные)",
                "Использую chi2 для категориальных фичей",
                "Знаю про L1-регуляризацию как встроенный отбор",
            ]),
        ],
        exercises=[
            ex(1, "python", "SelectKBest(f_classif, k=2) на X, y. Сохрани sel в переменную.",
               "import numpy as np\nfrom sklearn.feature_selection import SelectKBest, f_classif\nX = np.array([[1,2,3,4],[4,3,2,1],[1,1,0,0],[0,0,1,1]], dtype=float)\ny = np.array([0, 1, 0, 1])\nsel = None\n",
               "import numpy as np\nfrom sklearn.feature_selection import SelectKBest, f_classif\nX = np.array([[1,2,3,4],[4,3,2,1],[1,1,0,0],[0,0,1,1]], dtype=float)\ny = np.array([0, 1, 0, 1])\nsel = SelectKBest(f_classif, k=2).fit(X, y)\nprint(sel.scores_)",
               [{"check": "isinstance(sel, SelectKBest)", "msg": "SelectKBest"},
                {"check": "len(sel.scores_) == 4", "msg": "4 скора"}],
               ["fit(X, y) — обучение", "scores_ — массив F-значений"], 2),
            ex(2, "python", "Получи выбранные фичи через `sel.get_support()`. Сохрани в `mask`.",
               "import numpy as np\nfrom sklearn.feature_selection import SelectKBest, f_classif\nX = np.array([[1,2,3,4],[4,3,2,1],[1,1,0,0],[0,0,1,1]], dtype=float)\ny = np.array([0, 1, 0, 1])\nmask = None\n",
               "import numpy as np\nfrom sklearn.feature_selection import SelectKBest, f_classif\nX = np.array([[1,2,3,4],[4,3,2,1],[1,1,0,0],[0,0,1,1]], dtype=float)\ny = np.array([0, 1, 0, 1])\nsel = SelectKBest(f_classif, k=2).fit(X, y)\nmask = sel.get_support()\nprint(mask)",
               [{"check": "isinstance(mask, np.ndarray)", "msg": "ndarray"},
                {"check": "mask.dtype == bool", "msg": "bool"},
                {"check": "mask.sum() == 2", "msg": "2 True (k=2)"}],
               ["get_support() — маска выбранных", "True = выбрано"], 2),
            ex(3, "python", "sel.transform(X). Сохрани результат в `X_new`.",
               "import numpy as np\nfrom sklearn.feature_selection import SelectKBest, f_classif\nX = np.array([[1,2,3,4],[4,3,2,1],[1,1,0,0],[0,0,1,1]], dtype=float)\ny = np.array([0, 1, 0, 1])\nX_new = None\n",
               "import numpy as np\nfrom sklearn.feature_selection import SelectKBest, f_classif\nX = np.array([[1,2,3,4],[4,3,2,1],[1,1,0,0],[0,0,1,1]], dtype=float)\ny = np.array([0, 1, 0, 1])\nsel = SelectKBest(f_classif, k=2).fit(X, y)\nX_new = sel.transform(X)\nprint(X_new.shape)",
               [{"check": "X_new.shape == (4, 2)", "msg": "(4, 2) — 4 строки, 2 фичи"}],
               ["transform применяет отбор", "fit + transform = fit_transform"], 2),
            ex(4, "python", "fit_transform одной строкой. Сохрани shape в `s`.",
               "import numpy as np\nfrom sklearn.feature_selection import SelectKBest, f_classif\nX = np.random.RandomState(0).rand(10, 5)\ny = np.random.RandomState(0).randint(0, 2, 10)\ns = None\n",
               "import numpy as np\nfrom sklearn.feature_selection import SelectKBest, f_classif\nX = np.random.RandomState(0).rand(10, 5)\ny = np.random.RandomState(0).randint(0, 2, 10)\ns = SelectKBest(f_classif, k=3).fit_transform(X, y).shape\nprint(s)",
               [{"check": "s == (10, 3)", "msg": "(10, 3) — 3 фичи"}],
               ["fit_transform(X, y)", "Возвращает ndarray"], 2),
            ex(5, "python", "f_classif_scores = sel.scores_. Сохрани в `scores`.",
               "import numpy as np\nfrom sklearn.feature_selection import SelectKBest, f_classif\nX = np.array([[1,0],[0,1],[1,0],[0,1]], dtype=float)\ny = np.array([0, 1, 0, 1])\nscores = None\n",
               "import numpy as np\nfrom sklearn.feature_selection import SelectKBest, f_classif\nX = np.array([[1,0],[0,1],[1,0],[0,1]], dtype=float)\ny = np.array([0, 1, 0, 1])\nsel = SelectKBest(f_classif, k=1).fit(X, y)\nscores = sel.scores_\nprint(scores)",
               [{"check": "isinstance(scores, np.ndarray)", "msg": "ndarray"},
                {"check": "scores.shape == (2,)", "msg": "2 скора (2 фичи)"}],
               ["scores_ — F-значения", "Чем больше, тем лучше фича"], 2),
            ex(6, "python", "mutual_info_classif для нелинейных зависимостей. Сохрани shape.",
               "import numpy as np\nfrom sklearn.feature_selection import SelectKBest, mutual_info_classif\nX = np.random.RandomState(0).rand(20, 4)\ny = (X[:, 0] ** 2 > 0.5).astype(int)\nshape = None\n",
               "import numpy as np\nfrom sklearn.feature_selection import SelectKBest, mutual_info_classif\nX = np.random.RandomState(0).rand(20, 4)\ny = (X[:, 0] ** 2 > 0.5).astype(int)\nshape = SelectKBest(mutual_info_classif, k=2).fit_transform(X, y).shape\nprint(shape)",
               [{"check": "shape == (20, 2)", "msg": "(20, 2) — 2 фичи из 4"}],
               ["mutual_info_classif ловит нелинейности", "Медленнее f_classif"], 3),
            ex(7, "python", "chi2 для неотрицательных. Сохрани sel.",
               "import numpy as np\nfrom sklearn.feature_selection import SelectKBest, chi2\nX = np.array([[1,2],[2,3],[3,1],[4,2]], dtype=int)\ny = np.array([0, 1, 0, 1])\nsel = None\n",
               "import numpy as np\nfrom sklearn.feature_selection import SelectKBest, chi2\nX = np.array([[1,2],[2,3],[3,1],[4,2]], dtype=int)\ny = np.array([0, 1, 0, 1])\nsel = SelectKBest(chi2, k=1).fit(X, y)\nprint(sel.scores_, sel.pvalues_)",
               [{"check": "isinstance(sel, SelectKBest)", "msg": "SelectKBest"},
                {"check": "sel.k_features_ == 1", "msg": "k=1 фича"}],
               ["chi2 — для категориальных/счётных", "scores_ и pvalues_"], 3),
            ex(8, "python", "Корреляция фичи с таргетом через np.corrcoef. Сохрани в `corr`.",
               "import numpy as np\nx = np.array([1, 2, 3, 4, 5], dtype=float)\ny = np.array([2, 4, 5, 4, 5], dtype=float)\ncorr = 0\n",
               "import numpy as np\nx = np.array([1, 2, 3, 4, 5], dtype=float)\ny = np.array([2, 4, 5, 4, 5], dtype=float)\ncorr = np.corrcoef(x, y)[0, 1]\nprint(round(corr, 3))",
               [{"check": "isinstance(corr, float) or isinstance(corr, np.floating)", "msg": "float"},
                {"check": "abs(corr) <= 1.0", "msg": "Корреляция в [-1, 1]"}],
               ["np.corrcoef возвращает матрицу 2x2", "[0, 1] — нужный элемент"], 2),
            ex(9, "python", "Удаление сильно коррелирующих фичей: оставь одну из пары с corr > 0.9. "
                            "Сохрани список колонок в `keep`.",
               "import numpy as np\nimport pandas as pd\ndf = pd.DataFrame({'a':[1,2,3,4], 'b':[1,2,3,4], 'c':[1,1,1,1], 'd':[4,3,2,1]})\nkeep = []\n",
               "import numpy as np\nimport pandas as pd\ndf = pd.DataFrame({'a':[1,2,3,4], 'b':[1,2,3,4], 'c':[1,1,1,1], 'd':[4,3,2,1]})\ncorr = df.corr().abs()\nupper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))\nto_drop = [c for c in upper.columns if any(upper[c] > 0.9)]\nkeep = [c for c in df.columns if c not in to_drop]\nprint(keep)",
               [{"check": "isinstance(keep, list)", "msg": "Список"},
                {"check": "len(keep) >= 1", "msg": "Хотя бы 1 фича"}],
               ["corr + triu — верхний треугольник", "drop=True для дубликатов"], 3),
            ex(10, "python", "Pipeline: StandardScaler -> SelectKBest(k=2). Сохрани X_new shape.",
               "import numpy as np\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.feature_selection import SelectKBest, f_classif\nX = np.random.RandomState(0).rand(10, 4)\ny = np.random.RandomState(0).randint(0, 2, 10)\nnew_shape = None\n",
               "import numpy as np\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.feature_selection import SelectKBest, f_classif\nX = np.random.RandomState(0).rand(10, 4)\ny = np.random.RandomState(0).randint(0, 2, 10)\nsc = StandardScaler()\nXs = sc.fit_transform(X)\nnew_shape = SelectKBest(f_classif, k=2).fit_transform(Xs, y).shape\nprint(new_shape)",
               [{"check": "new_shape == (10, 2)", "msg": "(10, 2)"}],
               ["Сначала масштабируем, потом отбираем", "f_classif требует неотрицательные, но работает с z-score"], 3),
        ],
        minutes=50, difficulty=3,
    )


def _8_8():
    return lesson(
        "8.8", "Мини-проект: Feature engineering для модели рекомендаций игр", "gaming", [
            theory(
                "В мини-проекте собираем полный пайплайн feature engineering для задачи "
                "рекомендации игр пользователю. У нас есть:\n\n"
                "**Источники данных:**\n"
                "- `users`: user_id, age, country, gender, registered_at.\n"
                "- `games`: game_id, title, genre, platform, price, release_date, rating, reviews.\n"
                "- `plays`: user_id, game_id, hours_played, last_played.\n\n"
                "**Что делаем:**\n"
                "1. Загружаем и объединяем таблицы.\n"
                "2. Создаём фичи пользователя: age_group, is_old_user, country_freq.\n"
                "3. Создаём фичи игры: log_price, quality_per_dollar, age_in_years.\n"
                "4. Создаём фичи взаимодействия: hours_per_dollar, is_recently_played.\n"
                "5. Кодируем категориальные: OHE для жанра, label для платформы.\n"
                "6. Масштабируем числовые фичи.\n"
                "7. Отбираем top-k через SelectKBest.\n\n"
                "**Результат:** матрица признаков (n_users × n_features), готовая для ML."
            ),
            analogy(
                "Этот проект — как собрать конструктор Lego: кубики — таблицы, инструкция — "
                "этапы FE, а готовая модель — это фигурка, которую мы покажем на конкурсе.",
                "Без FE у нас сырые таблицы users/games/plays. После FE — матрица, где каждая "
                "строка = пользователь, каждый столбец = подготовленный признак."
            ),
            visual(
                "Пайплайн мини-проекта",
                "  users ─┐\n"
                "         ├──▶ merge ──▶ create features ──▶ encode ──▶ scale ──▶ select\n"
                "  games ─┤                                                       │\n"
                "         │                                                       ▼\n"
                "  plays ─┘                                                  ML model"
            ),
            example(
                "Полный пайплайн: от трёх таблиц до матрицы X (n×k).",
                "Объединяем, создаём фичи, кодируем, масштабируем, отбираем — пять шагов.",
                "import pandas as pd\n"
                "import numpy as np\n"
                "from sklearn.preprocessing import StandardScaler, OneHotEncoder\n"
                "from sklearn.feature_selection import SelectKBest, f_classif\n"
                "from sklearn.compose import ColumnTransformer\n"
                "\n"
                "users = pd.DataFrame({'user_id':[1,2,3], 'age':[25,40,15], 'country':['RU','US','JP']})\n"
                "games = pd.DataFrame({'game_id':[1,2,3], 'genre':['RPG','Action','RPG'], 'price':[60,30,40]})\n"
                "plays = pd.DataFrame({'user_id':[1,2,3], 'game_id':[1,2,3], 'hours_played':[10,50,5]})\n"
                "\n"
                "df = plays.merge(users, on='user_id').merge(games, on='game_id')\n"
                "df['hours_per_dollar'] = df['hours_played'] / (df['price'] + 1)\n"
                "X = df[['age','hours_played','price','hours_per_dollar']]\n"
                "print('X shape:', X.shape)\n"
                "print(X)",
                "X shape: (3, 4)\n"
                "   age  hours_played  price  hours_per_dollar\n"
                "0   25            10     60           0.164\n"
                "1   40            50     30           1.613\n"
                "2   15             5     40           0.122",
                "Merge трёх таблиц → 3 строки. Создали hours_per_dollar. Итог: матрица 3x4, "
                "готова к масштабированию и отбору."
            ),
            common_mistakes([
                {"mistake": "Merge без проверки дубликатов",
                 "why_bad": "Один user-game встретится 5 раз → вздутые фичи",
                 "fix": "plays.drop_duplicates(['user_id','game_id'])"},
                {"mistake": "Применить StandardScaler к hours_per_dollar и age вместе",
                 "why_bad": "Возможно, ничего страшного, но смешение масштабов — плохая практика",
                 "fix": "Используем ColumnTransformer или аккуратно разделяем"},
                {"mistake": "Забыть обработать пропуски в price/hours_played",
                 "why_bad": "NaN сломает merge, модель получит мусор",
                 "fix": "df.fillna({...}) до merge или dropna по ключу"},
                {"mistake": "Отбор фичей на всей матрице до split",
                 "why_bad": "Утечка, завышенная оценка",
                 "fix": "Pipeline с SelectKBest внутри cross_val_score"},
            ]),
            interview_questions([
                {"q": "Как бы ты построил FE для рекомендательной системы?",
                 "a": "1) User-фичи: age, country_freq, активность. 2) Item-фичи: жанр, цена, рейтинг. "
                      "3) User-item фичи: hours_played, log_ratio. 4) Матрица user×item, TF-IDF на "
                      "описаниях. 5) Опционально — embeddings."},
                {"q": "Как объединить таблицы без потери информации?",
                 "a": "Проверяем типы ключей, удаляем дубликаты до merge, после merge проверяем "
                      "размерности (expected = n_left × n_right), обрабатываем NaN."},
                {"q": "Что важнее: больше фичей или их качество?",
                 "a": "Качество. 10 хороших фичей лучше 1000 шумных. Шумные фичи раздувают "
                      "дисперсию, замедляют обучение, мешают интерпретации."},
            ]),
            knowledge_checklist([
                "Объединяю таблицы через merge/join",
                "Создаю user-, item- и interaction-фичи",
                "Кодирую категории и масштабирую числовые",
                "Использую SelectKBest для отбора",
                "Проверяю отсутствие утечек и NaN",
                "Собираю весь пайплайн в sklearn Pipeline",
            ]),
        ],
        exercises=[
            ex(1, "python", "Создай три таблицы: users (3 строки), games (3 строки), plays (3 строки). "
                            "Сохрани в `users`, `games`, `plays`.",
               "import pandas as pd\nusers = None\ngames = None\nplays = None\n",
               "import pandas as pd\nusers = pd.DataFrame({\n    'user_id':[1,2,3],\n    'age':[25,40,15],\n    'country':['RU','US','JP']\n})\ngames = pd.DataFrame({\n    'game_id':[1,2,3],\n    'genre':['RPG','Action','RPG'],\n    'price':[60,30,40]\n})\nplays = pd.DataFrame({\n    'user_id':[1,2,3],\n    'game_id':[1,2,3],\n    'hours_played':[10,50,5]\n})\nprint(users, games, plays)",
               [{"check": "isinstance(users, pd.DataFrame)", "msg": "users — DataFrame"},
                {"check": "isinstance(games, pd.DataFrame)", "msg": "games — DataFrame"},
                {"check": "isinstance(plays, pd.DataFrame)", "msg": "plays — DataFrame"},
                {"check": "users.shape[0] == 3 and games.shape[0] == 3 and plays.shape[0] == 3", "msg": "По 3 строки"}],
               ["pd.DataFrame({...})", "user_id и game_id — ключи для merge"], 1),
            ex(2, "python", "Объедини plays+users+games в df. Сохрани в `df`.",
               "import pandas as pd\nusers = pd.DataFrame({'user_id':[1,2,3], 'age':[25,40,15]})\ngames = pd.DataFrame({'game_id':[1,2,3], 'price':[60,30,40]})\nplays = pd.DataFrame({'user_id':[1,2,3], 'game_id':[1,2,3], 'hours_played':[10,50,5]})\ndf = None\n",
               "import pandas as pd\nusers = pd.DataFrame({'user_id':[1,2,3], 'age':[25,40,15]})\ngames = pd.DataFrame({'game_id':[1,2,3], 'price':[60,30,40]})\nplays = pd.DataFrame({'user_id':[1,2,3], 'game_id':[1,2,3], 'hours_played':[10,50,5]})\ndf = plays.merge(users, on='user_id').merge(games, on='game_id')\nprint(df)",
               [{"check": "isinstance(df, pd.DataFrame)", "msg": "DataFrame"},
                {"check": "df.shape == (3, 5)", "msg": "(3, 5) — все колонки"},
                {"check": "set(['user_id','game_id','age','price','hours_played']).issubset(df.columns)", "msg": "Все колонки"}],
               ["merge дважды", "Ключи user_id, game_id"], 1),
            ex(3, "python", "Создай df['hours_per_dollar'] = hours_played / (price + 1).",
               "import pandas as pd\ndf = pd.DataFrame({'hours_played':[10,50,5], 'price':[60,30,40]})\n",
               "import pandas as pd\ndf = pd.DataFrame({'hours_played':[10,50,5], 'price':[60,30,40]})\ndf['hours_per_dollar'] = df['hours_played'] / (df['price'] + 1)\nprint(df)",
               [{"check": "'hours_per_dollar' in df.columns", "msg": "Колонка создана"},
                {"check": "abs(df['hours_per_dollar'].iloc[0] - 10/61) < 1e-6", "msg": "10/61 на первом"}],
               ["Защита от /0 через +1", "Поэлементное деление"], 2),
            ex(4, "python", "Создай df['log_price'] = log1p(price). Используй numpy.",
               "import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({'price':[10, 100, 1000]})\n",
               "import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({'price':[10, 100, 1000]})\ndf['log_price'] = np.log1p(df['price'])\nprint(df)",
               [{"check": "'log_price' in df.columns", "msg": "log_price"},
                {"check": "abs(df['log_price'].iloc[2] - np.log1p(1000)) < 1e-6", "msg": "log1p(1000)"}],
               ["np.log1p сжатие хвоста", "log1p(x) = log(1+x)"], 2),
            ex(5, "python", "Создай бинарный is_premium = price > 50.",
               "import pandas as pd\ndf = pd.DataFrame({'price':[20, 60, 100]})\ndf['is_premium'] = None\n",
               "import pandas as pd\ndf = pd.DataFrame({'price':[20, 60, 100]})\ndf['is_premium'] = df['price'] > 50\nprint(df)",
               [{"check": "'is_premium' in df.columns", "msg": "Колонка"},
                {"check": "df['is_premium'].sum() == 2", "msg": "Два True"},
                {"check": "df['is_premium'].dtype == bool", "msg": "bool"}],
               ["Сравнение даёт bool", "Series из bool"], 1),
            ex(6, "python", "OHE для жанров: pd.get_dummies на колонке genre. "
                            "Сохрани в `genre_dummies`.",
               "import pandas as pd\ndf = pd.DataFrame({'genre':['RPG','Action','RPG']})\ngenre_dummies = None\n",
               "import pandas as pd\ndf = pd.DataFrame({'genre':['RPG','Action','RPG']})\ngenre_dummies = pd.get_dummies(df['genre'])\nprint(genre_dummies)",
               [{"check": "isinstance(genre_dummies, pd.DataFrame)", "msg": "DataFrame"},
                {"check": "genre_dummies.shape == (3, 2)", "msg": "(3, 2)"},
                {"check": "genre_dummies['RPG'].iloc[0] == 1", "msg": "RPG[0]=1"}],
               ["pd.get_dummies", "OHE вручную"], 2),
            ex(7, "python", "StandardScaler на ['age','hours_played','price']. Сохрани в df_scaled.",
               "import pandas as pd\nfrom sklearn.preprocessing import StandardScaler\ndf = pd.DataFrame({'age':[20,30,40], 'hours_played':[10,20,30], 'price':[50,60,70]})\ndf_scaled = None\n",
               "import pandas as pd\nfrom sklearn.preprocessing import StandardScaler\ndf = pd.DataFrame({'age':[20,30,40], 'hours_played':[10,20,30], 'price':[50,60,70]})\nsc = StandardScaler()\ndf_scaled = pd.DataFrame(sc.fit_transform(df), columns=df.columns, index=df.index)\nprint(df_scaled.describe().round(2))",
               [{"check": "isinstance(df_scaled, pd.DataFrame)", "msg": "DataFrame"},
                {"check": "abs(df_scaled.mean().mean()) < 1e-6", "msg": "Среднее ≈ 0"}],
               ["fit_transform, потом DataFrame", "columns сохраняем"], 2),
            ex(8, "python", "frequency encoding страны: замени country на частоту.",
               "import pandas as pd\ndf = pd.DataFrame({'country':['RU','US','RU','JP','RU']})\ndf['country_freq'] = None\n",
               "import pandas as pd\ndf = pd.DataFrame({'country':['RU','US','RU','JP','RU']})\nfreq = df['country'].value_counts()\ndf['country_freq'] = df['country'].map(freq)\nprint(df)",
               [{"check": "'country_freq' in df.columns", "msg": "Колонка"},
                {"check": "df['country_freq'].iloc[0] == 3", "msg": "RU → 3"},
                {"check": "df['country_freq'].iloc[3] == 1", "msg": "JP → 1"}],
               ["value_counts + map", "Frequency encoding"], 2),
            ex(9, "python", "Target encoding жанра по среднему rating. Сохрани в df['genre_te'].",
               "import pandas as pd\ndf = pd.DataFrame({'genre':['RPG','RPG','Action','Action'], 'rating':[9,8,7,6]})\ndf['genre_te'] = None\n",
               "import pandas as pd\ndf = pd.DataFrame({'genre':['RPG','RPG','Action','Action'], 'rating':[9,8,7,6]})\ndf['genre_te'] = df.groupby('genre')['rating'].transform('mean')\nprint(df)",
               [{"check": "'genre_te' in df.columns", "msg": "Колонка"},
                {"check": "abs(df['genre_te'].iloc[0] - 8.5) < 1e-6", "msg": "RPG: 8.5"}],
               ["groupby + transform('mean')", "Target encoding"], 3),
            ex(10, "python", "SelectKBest(f_classif, k=2) на df[['age','price','hours_played']], таргет y. "
                             "Сохрани X_new shape.",
               "import pandas as pd\nimport numpy as np\nfrom sklearn.feature_selection import SelectKBest, f_classif\ndf = pd.DataFrame({'age':[20,40,25,50], 'price':[60,30,40,20], 'hours_played':[10,50,5,30]})\ny = np.array([0, 1, 0, 1])\nnew_shape = None\n",
               "import pandas as np\nfrom sklearn.feature_selection import SelectKBest, f_classif\ndf = pd.DataFrame({'age':[20,40,25,50], 'price':[60,30,40,20], 'hours_played':[10,50,5,30]})\ny = np.array([0, 1, 0, 1])\nnew_shape = SelectKBest(f_classif, k=2).fit_transform(df, y).shape\nprint(new_shape)",
               [{"check": "new_shape == (4, 2)", "msg": "(4, 2) — 2 фичи из 3"}],
               ["fit_transform(X, y)", "k=2 лучших из 3"], 2),
            ex(11, "python", "Pipeline: StandardScaler + SelectKBest(k=2). Сохрани X_new.",
               "import pandas as pd\nimport numpy as np\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.feature_selection import SelectKBest, f_classif\ndf = pd.DataFrame({'age':[20,40,25,50], 'price':[60,30,40,20], 'hours_played':[10,50,5,30]})\ny = np.array([0, 1, 0, 1])\nX_new = None\n",
               "import pandas as pd\nimport numpy as np\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.feature_selection import SelectKBest, f_classif\ndf = pd.DataFrame({'age':[20,40,25,50], 'price':[60,30,40,20], 'hours_played':[10,50,5,30]})\ny = np.array([0, 1, 0, 1])\nsc = StandardScaler()\nXs = sc.fit_transform(df)\nX_new = SelectKBest(f_classif, k=2).fit_transform(Xs, y)\nprint(X_new.shape)",
               [{"check": "X_new.shape == (4, 2)", "msg": "(4, 2)"}],
               ["Pipeline вручную", "Сначала масштаб, потом отбор"], 3),
            ex(12, "python", "Финальный merge с проверкой: после merge проверь, что shape ожидаемый. "
                             "Сохрани merged в `result`.",
               "import pandas as pd\nusers = pd.DataFrame({'user_id':[1,2,3], 'age':[25,40,15]})\nplays = pd.DataFrame({'user_id':[1,2,3], 'game_id':[1,2,3]})\ngames = pd.DataFrame({'game_id':[1,2,3], 'price':[60,30,40]})\nresult = None\n",
               "import pandas as pd\nusers = pd.DataFrame({'user_id':[1,2,3], 'age':[25,40,15]})\nplays = pd.DataFrame({'user_id':[1,2,3], 'game_id':[1,2,3]})\ngames = pd.DataFrame({'game_id':[1,2,3], 'price':[60,30,40]})\nresult = plays.merge(users, on='user_id').merge(games, on='game_id')\nprint(result.shape)\nprint(result)",
               [{"check": "isinstance(result, pd.DataFrame)", "msg": "DataFrame"},
                {"check": "result.shape == (3, 4)", "msg": "(3, 4) — 3 строки, 4 колонки"},
                {"check": "'age' in result.columns and 'price' in result.columns", "msg": "age и price есть"}],
               ["Двойной merge: plays→users→games", "Проверяем размерности"], 2),
        ],
        minutes=70, difficulty=3,
    )


LESSONS = [_8_1, _8_2, _8_3, _8_4, _8_5, _8_6, _8_7, _8_8]
