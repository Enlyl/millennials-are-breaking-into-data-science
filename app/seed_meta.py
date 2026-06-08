"""
Метаданные для остальных блоков (3-10), проекты, достижения, вопросы собеседований.
Блоки 1 и 2 имеют полный контент в отдельных модулях.
"""
import math
import random
from typing import Any, Callable


def _gen(seed: int, n: int, fn: Callable) -> list[dict]:
    """Генерирует список из n записей через изолированный Random(seed)."""
    rng = random.Random(seed)
    return [fn(rng, i) for i in range(n)]


def _w(rng: random.Random, items: list, weights: list):
    """Weighted choice (random.choices возвращает список, берём [0])."""
    return rng.choices(items, weights=weights)[0]


# ============================================================================
# Блоки 1-10 (метаданные)
# ============================================================================
BLOCKS_META: list[dict[str, Any]] = [
    {
        "number": 1,
        "title": "Python для Data Science",
        "description": "Основы языка Python: переменные, циклы, функции, списки, словари, файлы, CSV, обработка ошибок. Тема — Космос.",
        "theme": "space",
        "lessons_meta": [],  # Заполняется из реальных уроков
    },
    {
        "number": 2,
        "title": "SQL для Data Science",
        "description": "SELECT, JOIN, GROUP BY, оконные функции, CTE, подзапросы, оптимизация. Тема — Видеоигры.",
        "theme": "gaming",
        "lessons_meta": [],
    },
    {
        "number": 3,
        "title": "NumPy и Pandas",
        "description": "Работа с массивами, таблицами, очистка данных, агрегация, merge, временные ряды.",
        "theme": "mixed",
        "lessons_meta": [
            "NumPy: массивы и операции",
            "NumPy: индексация, срезы, маски",
            "Pandas: Series и DataFrame",
            "Импорт данных: CSV, JSON, Excel",
            "Фильтрация и выборка данных",
            "Очистка данных: пропуски",
            "Очистка данных: дубликаты и выбросы",
            "Агрегации и groupby",
            "Merge и Join в Pandas",
            "Преобразование данных: pivot, melt, stack",
            "Работа с датами и временными рядами",
            "Мини-проект: Очистка и подготовка реального датасета",
        ],
    },
    {
        "number": 4,
        "title": "Визуализация данных",
        "description": "Matplotlib, Seaborn, типы графиков, дашборды. Тема — Космос.",
        "theme": "space",
        "lessons_meta": [
            "Matplotlib: основы",
            "Типы графиков: линейный, столбчатый, круговой",
            "Scatter plot и корреляционные диаграммы",
            "Гистограммы и box plot",
            "Seaborn: статистические визуализации",
            "Heatmap и pairplot",
            "Как выбрать правильный тип графика",
            "Оформление и стиль: цвета, заголовки, легенды",
            "Сторителлинг с данными",
            "Мини-проект: Дашборд анализа космической миссии",
        ],
    },
    {
        "number": 5,
        "title": "Статистика для Data Science",
        "description": "Описательная статистика, распределения, корреляция, гипотезы, A/B тесты.",
        "theme": "mixed",
        "lessons_meta": [
            "Описательная статистика: среднее, медиана, мода",
            "Дисперсия, стандартное отклонение, IQR",
            "Типы распределений",
            "Корреляция и причинно-следственные связи",
            "Центральная предельная теорема",
            "Доверительные интервалы",
            "Гипотезы и p-value",
            "A/B тестирование: теория",
            "A/B тестирование: практика",
            "Мини-проект: A/B тест новой механики в игре",
        ],
    },
    {
        "number": 6,
        "title": "EDA — Исследовательский анализ данных",
        "description": "Полный цикл исследовательского анализа. Тема — Космос.",
        "theme": "space",
        "lessons_meta": [
            "Что такое EDA и зачем он нужен",
            "Первичный осмотр датасета",
            "Анализ числовых переменных",
            "Анализ категориальных переменных",
            "Анализ взаимосвязей между переменными",
            "Обнаружение аномалий и выбросов",
            "Формулировка гипотез по данным",
            "Мини-проект: Полный EDA датасета SpaceX миссий",
        ],
    },
    {
        "number": 7,
        "title": "Машинное обучение",
        "description": "Supervised/unsupervised, метрики, регрессия, классификация, деревья, ансамбли, кластеризация.",
        "theme": "mixed",
        "lessons_meta": [
            "Типы ML: supervised, unsupervised, reinforcement",
            "Train/Test Split и кросс-валидация",
            "Переобучение и недообучение",
            "Метрики регрессии: MAE, MSE, RMSE, R²",
            "Метрики классификации: accuracy, precision, recall, F1",
            "Линейная регрессия",
            "Логистическая регрессия",
            "Дерево решений",
            "Random Forest",
            "Gradient Boosting (XGBoost / LightGBM)",
            "K-Means кластеризация",
            "Интерпретация моделей: feature importance, SHAP",
            "Сравнение и выбор модели",
            "Мини-проект: Прогноз оттока игроков",
        ],
    },
    {
        "number": 8,
        "title": "Feature Engineering",
        "description": "Создание признаков, кодирование, масштабирование, отбор. Тема — Видеоигры.",
        "theme": "gaming",
        "lessons_meta": [
            "Что такое feature engineering и почему это важно",
            "Создание новых признаков",
            "Кодирование категориальных переменных",
            "Масштабирование: MinMax, Standard, Robust",
            "Работа с датами: извлечение признаков",
            "Базовая обработка текста",
            "Отбор признаков: методы и метрики",
            "Мини-проект: Feature engineering для модели рекомендаций",
        ],
    },
    {
        "number": 9,
        "title": "Производственный Data Science",
        "description": "Git, Jupyter, структура ML-проекта, Docker, MLOps, воспроизводимость.",
        "theme": "neutral",
        "lessons_meta": [
            "Git: основы для Data Scientist",
            "Git: ветки, merge, pull request",
            "Jupyter Notebooks: best practices",
            "Структура ML-проекта",
            "Воспроизводимость: seeds, requirements.txt, README",
            "Docker: минимальный старт для DS",
            "Основы MLOps: эксперименты, версионирование",
            "Мини-проект: Оформить проект по стандартам GitHub",
        ],
    },
    {
        "number": 10,
        "title": "Подготовка к собеседованиям",
        "description": "280 вопросов по Python, SQL, статистике, ML, DS General. Junior-уровень.",
        "theme": "neutral",
        "lessons_meta": [
            "Структура собеседования в Data Science",
            "Python: основные вопросы на собеседовании",
            "Python: продвинутые вопросы",
            "SQL: базовые вопросы",
            "SQL: продвинутые запросы",
            "Статистика и теория вероятностей",
            "Машинное обучение: теория",
            "DS General и поведенческие вопросы",
        ],
    },
    {
        "number": 11,
        "title": "Финальный проект",
        "description": "Capstone-проекты: Космос (анализ миссий NASA) и Игры (анализ поведения игроков). Полный цикл Data Science.",
        "theme": "neutral",
        "lessons_meta": [],
    },
]


# ============================================================================
# Проекты (20 штук)
# ============================================================================
PROJECTS: list[dict[str, Any]] = [
    # Игровые
    {
        "block": 3, "title": "G1: Анализ экономики игровой валюты",
        "description": (
            "Ты работаешь аналитиком в F2P-игре 'Realm of Heroes' с аудиторией 50K DAU. "
            "В игре два типа валюты: soft (золото, добывается в боях) и hard (гемы, покупаются "
            "за реальные деньги). Плохой баланс экономики убивает retention: избыток золота "
            "ведёт к инфляции и обесцениванию наград, дефицит — к оттоку игроков. "
            "В твоём распоряжении датасет на 200 игроков с их балансами, уровнями, числом сессий "
            "и суммой реальных трат. Нужно построить распределения обеих валют, найти 'китов' "
            "(топ-1% по тратам), проверить корреляцию уровень-золото, выявить выбросы. "
            "Deliverable: 3-4 графика matplotlib (гистограммы и scatter) и текстовый отчёт "
            "в print() с ключевыми цифрами и рекомендацией геймдизайнеру по балансу."
        ),
        "theme": "gaming", "difficulty": 2,
        "template_code": r'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)
N = 200
df = pd.DataFrame({
    "player_id": range(1, N + 1),
    "level": np.random.randint(1, 80, N),
    "gold": np.random.lognormal(7.0, 1.2, N).astype(int),
    "gems": np.random.exponential(150, N).astype(int),
    "sessions": np.random.poisson(40, N),
    "days_played": np.random.randint(1, 365, N),
    "total_spent_usd": np.random.exponential(15, N).round(2),
})

print("Размер:", df.shape)
print(df.head())
print("\nDescribe:")
print(df[["gold", "gems", "total_spent_usd"]].describe())

# TODO 1: Построй две гистограммы (subplot 1x2) — золото и гемы.
#   Подсвети медиану красной пунктирной линией, добавь легенду.

# TODO 2: Найди китов — игроков с total_spent_usd в топ-1%.
#   Напечатай их количество, суммарный вклад и долю от общего дохода.

# TODO 3: Scatter level vs gold. Раскрась китов в красный, остальных — синий.
#   Посчитай корреляцию Пирсона и напечатай значение.

# TODO 4: Напечатай 2-3 предложения с рекомендацией для геймдизайнера.
plt.tight_layout()
plt.show()
''',
        "solution_code": r'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)
N = 200
df = pd.DataFrame({
    "player_id": range(1, N + 1),
    "level": np.random.randint(1, 80, N),
    "gold": np.random.lognormal(7.0, 1.2, N).astype(int),
    "gems": np.random.exponential(150, N).astype(int),
    "sessions": np.random.poisson(40, N),
    "days_played": np.random.randint(1, 365, N),
    "total_spent_usd": np.random.exponential(15, N).round(2),
})

print("=== БАЗОВАЯ СТАТИСТИКА ===")
print(df[["gold", "gems", "total_spent_usd"]].describe())

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].hist(df.gold, bins=40, color="gold", edgecolor="black")
axes[0].axvline(df.gold.median(), color="red", linestyle="--",
                label=f"медиана={df.gold.median():.0f}")
axes[0].set_title("Распределение золота (soft currency)")
axes[0].set_xlabel("Золото")
axes[0].legend()
axes[1].hist(df.gems, bins=40, color="cyan", edgecolor="black")
axes[1].axvline(df.gems.median(), color="red", linestyle="--",
                label=f"медиана={df.gems.median():.0f}")
axes[1].set_title("Распределение гемов (hard currency)")
axes[1].set_xlabel("Гемы")
axes[1].legend()

whale_threshold = df.total_spent_usd.quantile(0.99)
whales = df[df.total_spent_usd >= whale_threshold]
share = whales.total_spent_usd.sum() / df.total_spent_usd.sum() * 100
print(f"\n=== КИТЫ (топ-1%, траты >= {whale_threshold:.2f}$) ===")
print(f"Количество: {len(whales)}")
print(f"Суммарно: {whales.total_spent_usd.sum():.0f}$ ({share:.1f}% дохода)")

fig2, ax = plt.subplots(figsize=(7, 5))
ax.scatter(df.level, df.gold, alpha=0.4, s=20, label="обычные")
ax.scatter(whales.level, whales.gold, color="red", s=40, label="киты")
corr = df.level.corr(df.gold)
ax.text(0.05, 0.95, f"Корреляция Пирсона = {corr:.2f}",
        transform=ax.transAxes,
        bbox=dict(boxstyle="round", facecolor="wheat"))
ax.set_xlabel("Уровень")
ax.set_ylabel("Золото")
ax.set_title("Уровень vs Золото")
ax.legend()

print("\n=== РЕКОМЕНДАЦИЯ ===")
print(f"Распределение золота логнормальное (медиана {df.gold.median():.0f}). "
      f"{len(whales)} кит-игроков дают {share:.1f}% дохода. "
      f"Корреляция уровень-золото = {corr:.2f} (слабая). "
      f"Стоит добавить ежедневный бонус новичкам и anti-inflation sink "
      f"для топ-игроков.")
plt.tight_layout()
plt.show()
''',
        "dataset": {
            "seed": 42,
            "n": 200,
            "fields": ["player_id", "level", "gold", "gems", "sessions", "days_played", "total_spent_usd"],
            "note": "Логнормальное распределение золота, экспоненциальное гемов — типичная F2P-экономика",
            "records": _gen(42, 200, lambda r, i: {
                "player_id": i + 1,
                "level": r.randint(1, 80),
                "gold": int(r.lognormvariate(7.0, 1.2)),
                "gems": int(r.expovariate(1 / 150)),
                "sessions": max(1, int(r.gauss(40, 15))),
                "days_played": r.randint(1, 365),
                "total_spent_usd": round(r.expovariate(1 / 15), 2),
            }),
        },
    },
    {
        "block": 7, "title": "G2: Прогноз оттока игроков (Churn)",
        "description": (
            "Ты — продуктовый аналитик в мобильной PvP-игре. Маркетинг планирует "
            "кампанию по удержанию, но бюджет ограничен 5000 игроками. Нужно заранее "
            "выявить тех, кто собирается уйти в ближайший месяц, и предложить им бонус. "
            "В датасете 400 игроков: уровень, суммарное время в игре, число покупок, "
            "дней с последнего логина, средняя длина сессии, сессий в неделю и флаг — "
            "уйдёт ли игрок (churned). Нужно обучить модель логистической регрессии, "
            "оценить качество через train/test split (accuracy, precision, recall, "
            "F1) и интерпретировать коэффициенты — какие признаки сильнее всего "
            "влияют на отток. Deliverable: обученная модель + отчёт с метриками + "
            "топ-3 фактора churn."
        ),
        "theme": "gaming", "difficulty": 4,
        "template_code": r'''
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import StandardScaler

np.random.seed(42)
N = 400
df = pd.DataFrame({
    "level": np.random.randint(1, 80, N),
    "playtime_hours": np.random.gamma(3, 20, N).round(1),
    "purchases": np.random.poisson(1.5, N),
    "days_since_login": np.random.randint(0, 60, N),
    "avg_session_min": np.random.gamma(2, 5, N).round(1),
    "sessions_per_week": np.random.randint(1, 25, N),
})
# target: high churn risk if low engagement + high days_since_login
logit = (-0.03 * df.level - 0.02 * df.playtime_hours
         - 0.3 * df.sessions_per_week + 0.08 * df.days_since_login
         - 0.1 * df.purchases)
prob = 1 / (1 + np.exp(-logit + 1.5))
df["churned"] = (np.random.rand(N) < prob).astype(int)

print("Размер:", df.shape)
print("Churn rate:", df.churned.mean().round(3))
print(df.head())

# TODO 1: Раздели X и y, сделай train_test_split (test_size=0.25, random_state=42).

# TODO 2: Обучи StandardScaler на train, примени к train и test.

# TODO 3: Обучи LogisticRegression. Предскажи классы на test.

# TODO 4: Напечатай accuracy, precision, recall, F1. Сделай вывод — модель полезна?

# TODO 5: Напечатай топ-3 признака по абсолютному коэффициенту — что сильнее всего
#   влияет на churn?
''',
        "solution_code": r'''
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (accuracy_score, precision_score,
                             recall_score, f1_score, confusion_matrix)
from sklearn.preprocessing import StandardScaler

np.random.seed(42)
N = 400
df = pd.DataFrame({
    "level": np.random.randint(1, 80, N),
    "playtime_hours": np.random.gamma(3, 20, N).round(1),
    "purchases": np.random.poisson(1.5, N),
    "days_since_login": np.random.randint(0, 60, N),
    "avg_session_min": np.random.gamma(2, 5, N).round(1),
    "sessions_per_week": np.random.randint(1, 25, N),
})
logit = (-0.03 * df.level - 0.02 * df.playtime_hours
         - 0.3 * df.sessions_per_week + 0.08 * df.days_since_login
         - 0.1 * df.purchases)
prob = 1 / (1 + np.exp(-logit + 1.5))
df["churned"] = (np.random.rand(N) < prob).astype(int)

X = df.drop(columns=["churned"])
y = df["churned"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train_s, y_train)
y_pred = model.predict(X_test_s)

acc = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred, zero_division=0)
rec = recall_score(y_test, y_pred, zero_division=0)
f1 = f1_score(y_test, y_pred, zero_division=0)

print("=== МЕТРИКИ НА ТЕСТЕ ===")
print(f"Accuracy:  {acc:.3f}")
print(f"Precision: {prec:.3f}")
print(f"Recall:    {rec:.3f}")
print(f"F1:        {f1:.3f}")
print("\nConfusion matrix:")
print(confusion_matrix(y_test, y_pred))

coefs = pd.Series(model.coef_[0], index=X.columns)
top3 = coefs.abs().sort_values(ascending=False).head(3)
print("\n=== ТОП-3 ФАКТОРА CHURN ===")
for name, abs_c in top3.items():
    sign = "увеличивает" if coefs[name] > 0 else "снижает"
    print(f"  {name}: коэф={coefs[name]:+.3f} ({sign} шанс churn)")

base_rate = y_test.mean()
print(f"\nBaseline (все 'не уйдут'): accuracy={1 - base_rate:.3f}")
print(f"Модель улучшает baseline на {acc - (1 - base_rate):+.3f}")
''',
        "dataset": {
            "seed": 42,
            "n": 400,
            "fields": ["level", "playtime_hours", "purchases", "days_since_login",
                       "avg_session_min", "sessions_per_week", "churned"],
            "note": "churned сгенерирован через логит от поведенческих признаков",
            "records": _gen(42, 400, lambda r, i: {
                "level": r.randint(1, 80),
                "playtime_hours": round(max(0.1, r.gauss(60, 30)), 1),
                "purchases": max(0, int(r.gauss(1.5, 2))),
                "days_since_login": r.randint(0, 60),
                "avg_session_min": round(max(1.0, r.gauss(10, 4)), 1),
                "sessions_per_week": r.randint(1, 25),
                "churned": 0,
            }),
        },
    },
    {
        "block": 7, "title": "G3: Сегментация игроков по поведению",
        "description": (
            "Команда growth в социальной MMO хочет запустить таргетированные акции: "
            "'казуалам' — ежедневные бонусы, 'хардкорщикам' — турниры, 'социалам' — "
            "гильдейские ивенты. У тебя 250 игроков с метриками: время в игре, сессий "
            "в неделю, покупки, PvP-матчи, достижения, социальная активность. "
            "Нужно с помощью K-Means выделить 3-4 сегмента, проинтерпретировать "
            "каждый кластер по средним признакам, нарисовать scatter-plot в 2D "
            "(например, время-в-игре vs PvP-матчи) с цветом по кластеру. "
            "Deliverable: обученная модель + elbow/inertia график + scatter с "
            "кластерами + средние значения признаков по кластерам + названия сегментов."
        ),
        "theme": "gaming", "difficulty": 3,
        "template_code": r'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

np.random.seed(42)
N = 250
df = pd.DataFrame({
    "playtime_hours": np.random.gamma(3, 20, N).round(1),
    "sessions_per_week": np.random.randint(1, 25, N),
    "purchases": np.random.poisson(1.5, N),
    "pvp_matches": np.random.randint(0, 200, N),
    "achievements": np.random.randint(0, 100, N),
    "guild_activity": np.random.randint(0, 30, N),
})

print("Размер:", df.shape)
print(df.head())
print("\nDescribe:")
print(df.describe())

# TODO 1: Стандартизируй все признаки через StandardScaler.

# TODO 2: Построй график зависимости inertia (sum of squared distances)
#   от K в диапазоне 2..7. Используй elbow-метод для выбора K.

# TODO 3: Обучи KMeans с выбранным K (default random_state=42). Предскащи labels.

# TODO 4: Scatter playtime_hours vs pvp_matches, раскрась по кластеру.
#   Подпиши кластеры — какие игроки там живут.

# TODO 5: Напечатай средние значения признаков по кластерам (groupby).
#   Дай каждому кластеру осмысленное название.
plt.tight_layout()
plt.show()
''',
        "solution_code": r'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

np.random.seed(42)
N = 250
df = pd.DataFrame({
    "playtime_hours": np.random.gamma(3, 20, N).round(1),
    "sessions_per_week": np.random.randint(1, 25, N),
    "purchases": np.random.poisson(1.5, N),
    "pvp_matches": np.random.randint(0, 200, N),
    "achievements": np.random.randint(0, 100, N),
    "guild_activity": np.random.randint(0, 30, N),
})

X = df.values
scaler = StandardScaler()
X_s = scaler.fit_transform(X)

inertias = []
K_range = range(2, 8)
for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_s)
    inertias.append(km.inertia_)

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
axes[0].plot(list(K_range), inertias, marker="o", color="navy")
axes[0].set_xlabel("K (число кластеров)")
axes[0].set_ylabel("Inertia")
axes[0].set_title("Elbow method")
axes[0].grid(alpha=0.3)

K_FINAL = 4
km = KMeans(n_clusters=K_FINAL, random_state=42, n_init=10)
labels = km.fit_predict(X_s)
df["cluster"] = labels

for c in range(K_FINAL):
    mask = labels == c
    axes[1].scatter(df.loc[mask, "playtime_hours"],
                    df.loc[mask, "pvp_matches"],
                    label=f"cluster {c}", s=30, alpha=0.6)
axes[1].set_xlabel("Время в игре (часы)")
axes[1].set_ylabel("PvP-матчи")
axes[1].set_title("Сегменты игроков")
axes[1].legend()
axes[1].grid(alpha=0.3)

print("=== СРЕДНИЕ ПО КЛАСТЕРАМ ===")
summary = df.groupby("cluster").mean().round(1)
print(summary)

names = {
    0: "казуалы (мало играют, мало покупают)",
    1: "хардкор-PvP (много матчей, много времени)",
    2: "коллекционеры (много достижений, средние траты)",
    3: "социалы (высокая guild_activity)",
}
print("\n=== ИНТЕРПРЕТАЦИЯ ===")
for c, desc in names.items():
    size = (labels == c).sum()
    print(f"  Кластер {c} ({size} игроков): {desc}")
plt.tight_layout()
plt.show()
''',
        "dataset": {
            "seed": 42,
            "n": 250,
            "fields": ["playtime_hours", "sessions_per_week", "purchases",
                       "pvp_matches", "achievements", "guild_activity"],
            "note": "Реалистичные логнормальные распределения игровых метрик",
            "records": _gen(42, 250, lambda r, i: {
                "playtime_hours": round(max(0.1, r.gauss(60, 30)), 1),
                "sessions_per_week": r.randint(1, 25),
                "purchases": max(0, int(r.gauss(1.5, 2))),
                "pvp_matches": r.randint(0, 200),
                "achievements": r.randint(0, 100),
                "guild_activity": r.randint(0, 30),
            }),
        },
    },
    {
        "block": 5, "title": "G4: Балансировка оружия: анализ win rate",
        "description": (
            "Ты — геймдизайнер шутера 'Frontline'. После последнего патча игроки жалуются: "
            "винтовка DMR-14 слишком сильная, а дробовик R-9 — слишком слабый. У тебя лог "
            "из 2000 матчей: оружие, факт победы, damage, accuracy, дальность, fire rate, "
            "число использований. Нужно посчитать win rate по каждому оружию, построить "
            "доверительные интервалы 95% для пропорции (Wilson interval — формула вручную, "
            "без scipy), выявить оружие с win rate статистически значимо выше/ниже 50% "
            "(z-тест для пропорции), построить bar chart с CI. "
            "Deliverable: таблица оружия с win_rate, CI, z-статистикой + график с "
            "подсветкой дисбалансных стволов + список рекомендаций ('ослабить', 'усилить', "
            "'ОК')."
        ),
        "theme": "gaming", "difficulty": 3,
        "template_code": r'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)
WEAPONS = ["AR-15", "DMR-14", "R-9", "SMG-X", "LMG-K", "Sniper-7", "Pistol-1"]
rows = []
for w in WEAPONS:
    uses = np.random.randint(150, 400)
    # base win rate; DMR-14 overpowered, R-9 weak
    base = {"AR-15": 0.50, "DMR-14": 0.62, "R-9": 0.40, "SMG-X": 0.51,
            "LMG-K": 0.48, "Sniper-7": 0.55, "Pistol-1": 0.46}[w]
    wins = np.random.binomial(uses, base)
    rows.append({"weapon": w, "uses": int(uses), "wins": int(wins),
                 "damage": np.random.randint(20, 60),
                 "accuracy": round(np.random.uniform(0.3, 0.9), 2),
                 "fire_rate": np.random.randint(5, 15)})
df = pd.DataFrame(rows)
print(df)

# TODO 1: Посчитай win_rate = wins / uses для каждого оружия.

# TODO 2: Реализуй Wilson 95% CI для пропорции:
#   z = 1.96
#   denom = 1 + z^2 / n
#   center = (p + z^2 / (2n)) / denom
#   margin = z * sqrt(p(1-p)/n + z^2/(4n^2)) / denom
#   CI = (center - margin, center + margin)

# TODO 3: Сделай z-тест пропорции против H0: p=0.5
#   z = (p - 0.5) / sqrt(0.5 * 0.5 / n)
#   p-value (двусторонний) ≈ 2 * (1 - |z| нормированное)
#   Для простоты: если |z| > 1.96, отвергаем H0.

# TODO 4: Напечатай таблицу с weapon, win_rate, CI_low, CI_high, z, verdict
#   (overpowered если win_rate > 0.55 и p<0.05, underpowered если < 0.45 и p<0.05, else OK).

# TODO 5: Bar chart win_rate с error bars (CI_low..CI_high), подсвети дисбаланс.
plt.tight_layout()
plt.show()
''',
        "solution_code": r'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)
WEAPONS = ["AR-15", "DMR-14", "R-9", "SMG-X", "LMG-K", "Sniper-7", "Pistol-1"]
rows = []
for w in WEAPONS:
    uses = np.random.randint(150, 400)
    base = {"AR-15": 0.50, "DMR-14": 0.62, "R-9": 0.40, "SMG-X": 0.51,
            "LMG-K": 0.48, "Sniper-7": 0.55, "Pistol-1": 0.46}[w]
    wins = np.random.binomial(uses, base)
    rows.append({"weapon": w, "uses": int(uses), "wins": int(wins),
                 "damage": np.random.randint(20, 60),
                 "accuracy": round(np.random.uniform(0.3, 0.9), 2),
                 "fire_rate": np.random.randint(5, 15)})
df = pd.DataFrame(rows)


def wilson_ci(p, n, z=1.96):
    denom = 1 + z ** 2 / n
    center = (p + z ** 2 / (2 * n)) / denom
    margin = z * np.sqrt(p * (1 - p) / n + z ** 2 / (4 * n ** 2)) / denom
    return center - margin, center + margin


def z_test_prop(p, n):
    if n == 0:
        return 0.0
    return (p - 0.5) / np.sqrt(0.25 / n)


df["win_rate"] = df.wins / df.uses
ci = df.apply(lambda r: wilson_ci(r.win_rate, r.uses), axis=1)
df["ci_low"] = [c[0] for c in ci]
df["ci_high"] = [c[1] for c in ci]
df["z"] = df.apply(lambda r: z_test_prop(r.win_rate, r.uses), axis=1)


def verdict(row):
    if abs(row.z) < 1.96:
        return "ОК"
    if row.win_rate > 0.55:
        return "ОСЛАБИТЬ (OP)"
    if row.win_rate < 0.45:
        return "УСИЛИТЬ (UP)"
    return "ОК"


df["verdict"] = df.apply(verdict, axis=1)

print(df[["weapon", "uses", "win_rate", "ci_low", "ci_high", "z", "verdict"]]
      .round(3).to_string(index=False))

fig, ax = plt.subplots(figsize=(9, 5))
colors = df.verdict.map({"ОК": "gray", "ОСЛАБИТЬ (OP)": "red",
                          "УСИЛИТЬ (UP)": "blue"})
ax.bar(df.weapon, df.win_rate, color=colors, edgecolor="black")
ax.errorbar(df.weapon, df.win_rate,
            yerr=[df.win_rate - df.ci_low, df.ci_high - df.win_rate],
            fmt="none", ecolor="black", capsize=4)
ax.axhline(0.5, color="black", linestyle="--", label="баланс (50%)")
ax.set_ylabel("Win rate")
ax.set_title("Баланс оружия: 95% Wilson CI")
ax.legend()
plt.xticks(rotation=20)

print("\n=== РЕКОМЕНДАЦИИ ===")
for _, r in df.iterrows():
    if r.verdict != "ОК":
        print(f"  {r.weapon}: win_rate={r.win_rate:.2f}, "
              f"z={r.z:+.2f} -> {r.verdict}")
plt.tight_layout()
plt.show()
''',
        "dataset": {
            "seed": 42,
            "n_weapons": 7,
            "fields": ["weapon", "uses", "wins", "damage", "accuracy", "fire_rate"],
            "note": "Wilson 95% CI и z-тест пропорции — выявляем дисбаланс без scipy",
            "records": [
                {"weapon": "AR-15", "uses": 312, "wins": 159, "damage": 34, "accuracy": 0.62, "fire_rate": 9},
                {"weapon": "DMR-14", "uses": 287, "wins": 178, "damage": 55, "accuracy": 0.78, "fire_rate": 6},
                {"weapon": "R-9", "uses": 198, "wins": 79, "damage": 80, "accuracy": 0.41, "fire_rate": 5},
                {"weapon": "SMG-X", "uses": 341, "wins": 174, "damage": 24, "accuracy": 0.55, "fire_rate": 13},
                {"weapon": "LMG-K", "uses": 165, "wins": 79, "damage": 30, "accuracy": 0.48, "fire_rate": 11},
                {"weapon": "Sniper-7", "uses": 224, "wins": 123, "damage": 90, "accuracy": 0.85, "fire_rate": 4},
                {"weapon": "Pistol-1", "uses": 376, "wins": 173, "damage": 18, "accuracy": 0.58, "fire_rate": 8},
            ],
        },
    },
    {
        "block": 5, "title": "G5: A/B тест новой игровой механики",
        "description": (
            "Команда геймдизайнеров добавила новую механику 'Combo System' — за "
            "серию убийств игрок получает x2/x3/x5 множитель очков. Твоя задача — "
            "провести A/B тест: 400 игроков получают старую механику (control), "
            "400 — новую (treatment). Метрика — Day-7 retention (вернулся ли "
            "игрок на 7-й день) и среднее число сессий за первую неделю. "
            "Нужно посчитать retention и средние по группам, проверить "
            "статистическую значимость (z-тест для пропорций, t-тест Уэлча "
            "для средних — реализуем вручную без scipy), оценить размер эффекта "
            "(Cohen's d) и принять решение: раскатываем механику или нет. "
            "Deliverable: таблица с метриками, p-value (приближённо), verdict "
            "и графики (bar chart по retention, boxplot сессий)."
        ),
        "theme": "gaming", "difficulty": 4,
        "template_code": r'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)
N_PER_GROUP = 400
df = pd.DataFrame({
    "player_id": range(1, 2 * N_PER_GROUP + 1),
    "group": ["control"] * N_PER_GROUP + ["treatment"] * N_PER_GROUP,
})
# Симулируем retention: control 35%, treatment 43%
df["day7_retained"] = np.where(
    df.group == "control",
    (np.random.rand(N_PER_GROUP) < 0.35).astype(int),
    (np.random.rand(N_PER_GROUP) < 0.43).astype(int),
)
# Симулируем сессии за неделю
df["sessions_week_1"] = np.where(
    df.group == "control",
    np.random.poisson(8, N_PER_GROUP),
    np.random.poisson(10, N_PER_GROUP),
)

print("Размер:", df.shape)
print(df.groupby("group").agg(
    n=("player_id", "count"),
    retention=("day7_retained", "mean"),
    avg_sessions=("sessions_week_1", "mean"),
).round(3))

# TODO 1: z-тест для разницы пропорций (retention).
#   z = (p_t - p_c) / sqrt(p_pool * (1 - p_pool) * (1/n_c + 1/n_t))
#   p_pool = (x_t + x_c) / (n_t + n_c)

# TODO 2: t-тест Уэлча (вручную, без scipy):
#   t = (m_t - m_c) / sqrt(var_t/n_t + var_c/n_c)
#   df (Welch–Satterthwaite) можешь не считать — для вывода достаточно |t| > 2.

# TODO 3: Cohen's d для sessions: (m_t - m_c) / pooled_std

# TODO 4: Bar chart retention по группам (±95% CI для пропорции).
#   Boxplot sessions_week_1 по группам.

# TODO 5: Напечатай итог: выкатываем новую механику? (yes / no / need more data)
plt.tight_layout()
plt.show()
''',
        "solution_code": r'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)
N_PER_GROUP = 400
df = pd.DataFrame({
    "player_id": range(1, 2 * N_PER_GROUP + 1),
    "group": ["control"] * N_PER_GROUP + ["treatment"] * N_PER_GROUP,
})
df["day7_retained"] = np.where(
    df.group == "control",
    (np.random.rand(N_PER_GROUP) < 0.35).astype(int),
    (np.random.rand(N_PER_GROUP) < 0.43).astype(int),
)
df["sessions_week_1"] = np.where(
    df.group == "control",
    np.random.poisson(8, N_PER_GROUP),
    np.random.poisson(10, N_PER_GROUP),
)

c = df[df.group == "control"]
t = df[df.group == "treatment"]

# Retention
p_c, p_t = c.day7_retained.mean(), t.day7_retained.mean()
n_c, n_t = len(c), len(t)
p_pool = (c.day7_retained.sum() + t.day7_retained.sum()) / (n_c + n_t)
z_ret = (p_t - p_c) / np.sqrt(p_pool * (1 - p_pool) * (1 / n_c + 1 / n_t))

# Sessions
m_c, m_t = c.sessions_week_1.mean(), t.sessions_week_1.mean()
v_c, v_t = c.sessions_week_1.var(ddof=1), t.sessions_week_1.var(ddof=1)
t_sess = (m_t - m_c) / np.sqrt(v_c / n_c + v_t / n_t)
pooled_std = np.sqrt(((n_c - 1) * v_c + (n_t - 1) * v_t) / (n_c + n_t - 2))
cohens_d = (m_t - m_c) / pooled_std

print("=== A/B ТЕСТ: 'Combo System' ===")
print(f"Retention: control={p_c:.3f}, treatment={p_t:.3f}, "
      f"diff={p_t - p_c:+.3f}, z={z_ret:+.2f}")
print(f"Sessions:  control={m_c:.2f}, treatment={m_t:.2f}, "
      f"diff={m_t - m_c:+.2f}, t={t_sess:+.2f}, Cohen's d={cohens_d:+.2f}")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
labels = ["control", "treatment"]
retention_vals = [p_c, p_t]
ci_c = 1.96 * np.sqrt(p_c * (1 - p_c) / n_c)
ci_t = 1.96 * np.sqrt(p_t * (1 - p_t) / n_t)
axes[0].bar(labels, retention_vals,
            yerr=[ci_c, ci_t], color=["lightgray", "lightgreen"],
            edgecolor="black", capsize=8)
axes[0].set_ylabel("Day-7 retention")
axes[0].set_title("Retention: z = {:.2f}".format(z_ret))
axes[0].set_ylim(0, 0.6)

axes[1].boxplot([c.sessions_week_1, t.sessions_week_1],
                labels=labels, patch_artist=True,
                boxprops=dict(facecolor="lightblue"))
axes[1].set_ylabel("Сессий за неделю")
axes[1].set_title("Sessions: t = {:.2f}, Cohen's d = {:.2f}".format(t_sess, cohens_d))

verdict_ret = "ЗНАЧИМО" if abs(z_ret) > 1.96 else "НЕ ЗНАЧИМО"
verdict_sess = "ЗНАЧИМО" if abs(t_sess) > 2 else "НЕ ЗНАЧИМО"
print(f"\nRetention p≈0.05: |z|={abs(z_ret):.2f} -> {verdict_ret}")
print(f"Sessions  p≈0.05: |t|={abs(t_sess):.2f} -> {verdict_sess}")

if abs(z_ret) > 1.96 and abs(t_sess) > 2:
    print("\n>>> ВЕРДИКТ: раскатываем Combo System на 100% игроков.")
else:
    print("\n>>> ВЕРДИКТ: нужно больше данных или доработка.")
plt.tight_layout()
plt.show()
''',
        "dataset": {
            "seed": 42,
            "n_per_group": 400,
            "fields": ["player_id", "group", "day7_retained", "sessions_week_1"],
            "note": "Treatment даёт +8% retention и +2 сессии в неделю — статистически значимо",
            "records": ([
                {"player_id": i + 1, "group": "control",
                 "day7_retained": 0, "sessions_week_1": 0}
                for i in range(5)
            ] + [
                {"player_id": 400 + i + 1, "group": "treatment",
                 "day7_retained": 0, "sessions_week_1": 0}
                for i in range(5)
            ]),
        },
    },
    {
        "block": 8, "title": "G6: Рекомендательная система скинов",
        "description": (
            "Игровой магазин скинов в 'Hero Wars' хочет персонализировать витрину: "
            "вместо одинаковой выдачи топ-скинов — рекомендовать каждому игроку "
            "3 скина, максимально похожих на те, что он уже покупал. У тебя "
            "история покупок 500 игроков и каталог 50 скинов с признаками: "
            "редкость (common/rare/epic/legendary), тип (weapon/armor/mount/pet), "
            "цена, фракция, тематика. Нужно сделать feature engineering: "
            "one-hot для категориальных, масштабирование числовых, потом построить "
            "простой content-based рекомендатель через косинусное сходство. "
            "Deliverable: обученная модель + пример рекомендаций для случайного "
            "игрока + визуализация feature space (heatmap корреляций признаков)."
        ),
        "theme": "gaming", "difficulty": 4,
        "template_code": r'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics.pairwise import cosine_similarity

np.random.seed(42)
SKINS = []
RARITY = ["common", "rare", "epic", "legendary"]
TYPE = ["weapon", "armor", "mount", "pet"]
FACTION = ["humans", "orcs", "elves", "undead"]
for i in range(50):
    SKINS.append({
        "skin_id": f"S{i:03d}",
        "rarity": np.random.choice(RARITY, p=[0.5, 0.3, 0.15, 0.05]),
        "type": np.random.choice(TYPE),
        "faction": np.random.choice(FACTION),
        "price_gems": np.random.randint(50, 5000),
        "popularity": round(np.random.uniform(0, 1), 2),
    })
skins = pd.DataFrame(SKINS)

# История покупок
N_PLAYERS = 500
purchases = []
for p in range(N_PLAYERS):
    n_buy = np.random.randint(2, 8)
    bought = np.random.choice(skins.skin_id, size=n_buy, replace=False)
    for s in bought:
        purchases.append({"player_id": p, "skin_id": s})
history = pd.DataFrame(purchases)

print("Skins:", skins.shape)
print("Purchases:", history.shape)
print(skins.head())

# TODO 1: One-hot encoding для rarity/type/faction. StandardScaler для price_gems и popularity.
#   Собери матрицу признаков скинов.

# TODO 2: Посчитай косинусное сходство между скинами.
#   Для случайного игрока возьми его последнюю покупку и найди top-3 похожих скина,
#   которые он ещё не купил.

# TODO 3: Напечатай результат: "Игрок #X уже купил S0XX. Рекомендуем: S..., S..., S..."

# TODO 4: Heatmap корреляций числовых признаков.
plt.tight_layout()
plt.show()
''',
        "solution_code": r'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics.pairwise import cosine_similarity

np.random.seed(42)
SKINS = []
RARITY = ["common", "rare", "epic", "legendary"]
TYPE = ["weapon", "armor", "mount", "pet"]
FACTION = ["humans", "orcs", "elves", "undead"]
for i in range(50):
    SKINS.append({
        "skin_id": f"S{i:03d}",
        "rarity": np.random.choice(RARITY, p=[0.5, 0.3, 0.15, 0.05]),
        "type": np.random.choice(TYPE),
        "faction": np.random.choice(FACTION),
        "price_gems": np.random.randint(50, 5000),
        "popularity": round(np.random.uniform(0, 1), 2),
    })
skins = pd.DataFrame(SKINS)

N_PLAYERS = 500
purchases = []
for p in range(N_PLAYERS):
    n_buy = np.random.randint(2, 8)
    bought = np.random.choice(skins.skin_id, size=n_buy, replace=False)
    for s in bought:
        purchases.append({"player_id": p, "skin_id": s})
history = pd.DataFrame(purchases)

# Feature engineering
ohe = OneHotEncoder(sparse_output=False)
cat_feats = ohe.fit_transform(skins[["rarity", "type", "faction"]])
scaler = StandardScaler()
num_feats = scaler.fit_transform(skins[["price_gems", "popularity"]])
skin_features = np.hstack([cat_feats, num_feats])

# Cosine similarity
sim = cosine_similarity(skin_features)
sim_df = pd.DataFrame(sim, index=skins.skin_id, columns=skins.skin_id)

# Рекомендация для случайного игрока
player_id = 42
bought = set(history[history.player_id == player_id].skin_id)
last_skin = list(bought)[-1]
scores = sim_df[last_skin].drop(last_skin)
candidates = scores[~scores.index.isin(bought)].sort_values(ascending=False)
top3 = candidates.head(3)

print(f"Игрок #{player_id} купил: {sorted(bought)}")
print(f"\nРекомендации (на основе последней покупки {last_skin}):")
for skin_id, score in top3.items():
    info = skins[skins.skin_id == skin_id].iloc[0]
    print(f"  {skin_id} ({info.rarity}/{info.type}/{info.faction}, "
          f"{info.price_gems}💎, score={score:.3f})")

# Heatmap корреляций
num_df = skins[["price_gems", "popularity"]].copy()
dummies = pd.get_dummies(skins[["rarity", "type", "faction"]])
full = pd.concat([num_df, dummies], axis=1)
corr = full.corr()

fig, ax = plt.subplots(figsize=(9, 8))
im = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
ax.set_xticks(range(len(corr.columns)))
ax.set_xticklabels(corr.columns, rotation=90, fontsize=7)
ax.set_yticks(range(len(corr.columns)))
ax.set_yticklabels(corr.columns, fontsize=7)
ax.set_title("Корреляция признаков скинов")
plt.colorbar(im)
plt.tight_layout()
plt.show()
''',
        "dataset": {
            "seed": 42,
            "n_skins": 50,
            "n_purchases_sample": 10,
            "fields_skins": ["skin_id", "rarity", "type", "faction", "price_gems", "popularity"],
            "note": "Content-based рекомендации через косинусное сходство one-hot + scaled фичей",
            "records_skins": [
                {"skin_id": "S000", "rarity": "common", "type": "weapon", "faction": "humans", "price_gems": 120, "popularity": 0.42},
                {"skin_id": "S001", "rarity": "epic", "type": "armor", "faction": "orcs", "price_gems": 1200, "popularity": 0.78},
                {"skin_id": "S002", "rarity": "legendary", "type": "mount", "faction": "elves", "price_gems": 4800, "popularity": 0.91},
                {"skin_id": "S003", "rarity": "rare", "type": "pet", "faction": "undead", "price_gems": 600, "popularity": 0.55},
            ],
        },
    },
    {
        "block": 5, "title": "G7: Анализ матчмейкинга и fairness",
        "description": (
            "Ты — аналитик в PvP-шутере. Игроки жалуются: 'Мне кидает противников "
            "на 200 MMR выше, мне специально сливают матчи'. Нужно проверить, "
            "насколько система ELO-матчмейкинга справедлива. У тебя лог из 1500 "
            "матчей: MMR игрока 1, MMR игрока 2, победитель, длительность, разница "
            "очков. Нужно посчитать распределение разницы MMR, проверить гипотезу "
            "'система старается балансировать' (средняя |ΔMMR| близка к нулю?), "
            "оценить корреляцию между разницей MMR и победой (логично: у кого MMR "
            "выше, тот чаще выигрывает), построить 3 графика (histogram ΔMMR, "
            "scatter ΔMMR vs winner=player1, box по категориям). "
            "Deliverable: таблица статистик + 3 графика + verdict ('fair' / 'rigged' / "
            "'needs improvement')."
        ),
        "theme": "gaming", "difficulty": 3,
        "template_code": r'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)
N = 1500
mmr1 = np.random.normal(1500, 200, N).astype(int)
# Соперник подбирается ±200 MMR
mmr2 = mmr1 + np.random.normal(0, 200, N).astype(int)
# Победитель зависит от разницы MMR + шум
delta = mmr1 - mmr2
prob_p1 = 1 / (1 + np.exp(-delta / 200))
winner = (np.random.rand(N) < prob_p1).astype(int)  # 1 = p1, 0 = p2

df = pd.DataFrame({
    "match_id": range(1, N + 1),
    "mmr_p1": mmr1,
    "mmr_p2": mmr2,
    "delta_mmr": delta,
    "winner": np.where(winner == 1, "p1", "p2"),
    "duration_min": np.random.gamma(8, 4, N).round(1),
    "score_diff": np.random.normal(0, 5, N).round(1),
})
print("Размер:", df.shape)
print(df.head())
print("\n|ΔMMR| describe:")
print(df.delta_mmr.abs().describe())

# TODO 1: Гистограмма распределения delta_mmr (ось X — разница, ось Y — частота).
#   Подсвети среднюю вертикальной линией.

# TODO 2: Boxplot: раздели матчи на 3 группы по |delta_mmr| (small <100, medium 100-300, large >300).
#   Для каждой группы посчитай win rate p1.

# TODO 3: Проверь гипотезу: средний delta_mmr ≈ 0? (просто посмотри mean и std).

# TODO 4: Напечатай verdict: 'fair' если средний |delta_mmr| < 250 и
#   win rate в small близок к 50%; иначе 'needs improvement'.
plt.tight_layout()
plt.show()
''',
        "solution_code": r'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)
N = 1500
mmr1 = np.random.normal(1500, 200, N).astype(int)
mmr2 = mmr1 + np.random.normal(0, 200, N).astype(int)
delta = mmr1 - mmr2
prob_p1 = 1 / (1 + np.exp(-delta / 200))
winner = (np.random.rand(N) < prob_p1).astype(int)

df = pd.DataFrame({
    "match_id": range(1, N + 1),
    "mmr_p1": mmr1,
    "mmr_p2": mmr2,
    "delta_mmr": delta,
    "winner_is_p1": winner,
    "duration_min": np.random.gamma(8, 4, N).round(1),
    "score_diff": np.random.normal(0, 5, N).round(1),
})

mean_delta = df.delta_mmr.mean()
std_delta = df.delta_mmr.std()
mean_abs = df.delta_mmr.abs().mean()
print(f"Средний ΔMMR: {mean_delta:+.2f} (std={std_delta:.2f})")
print(f"Средний |ΔMMR|: {mean_abs:.2f}")

def bucket(d):
    ad = abs(d)
    if ad < 100:
        return "small (<100)"
    if ad < 300:
        return "medium (100-300)"
    return "large (>300)"

df["balance_bucket"] = df.delta_mmr.apply(bucket)
wr_by_bucket = df.groupby("balance_bucket").agg(
    matches=("match_id", "count"),
    win_rate_p1=("winner_is_p1", "mean"),
)
print("\nWin rate p1 по группам баланса:")
print(wr_by_bucket.round(3))

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
axes[0].hist(df.delta_mmr, bins=50, color="steelblue", edgecolor="black")
axes[0].axvline(mean_delta, color="red", linestyle="--",
                label=f"mean={mean_delta:+.1f}")
axes[0].set_xlabel("ΔMMR (p1 - p2)")
axes[0].set_ylabel("Частота")
axes[0].set_title("Распределение разницы MMR")
axes[0].legend()

bucket_order = ["small (<100)", "medium (100-300)", "large (>300)"]
data = [df[df.balance_bucket == b].winner_is_p1 for b in bucket_order]
axes[1].boxplot(data, labels=bucket_order, patch_artist=True,
                boxprops=dict(facecolor="lightblue"))
axes[1].axhline(0.5, color="red", linestyle="--", label="честный матч (50%)")
axes[1].set_ylabel("Win rate игрока 1")
axes[1].set_title("Win rate vs дисбаланс матча")
axes[1].legend()

small_wr = wr_by_bucket.loc["small (<100)", "win_rate_p1"]
if abs(mean_delta) < 10 and 0.45 < small_wr < 0.55:
    verdict = "FAIR — матчмейкер работает корректно"
elif 0.40 < small_wr < 0.60:
    verdict = "NEEDS IMPROVEMENT — небольшой перекос"
else:
    verdict = "RIGGED — подозрительный дисбаланс"

print(f"\n=== ВЕРДИКТ ===\n{verdict}")
plt.tight_layout()
plt.show()
''',
        "dataset": {
            "seed": 42,
            "n_matches": 1500,
            "fields": ["match_id", "mmr_p1", "mmr_p2", "delta_mmr",
                       "winner", "duration_min", "score_diff"],
            "note": "MMR ~ N(1500, 200), ΔMMR ~ N(0, 200) — типичный ELO-матчмейкер",
            "records": _gen(42, 1500, lambda r, i: {
                "match_id": i + 1,
                "mmr_p1": int(r.gauss(1500, 200)),
                "mmr_p2": int(r.gauss(1500, 200)),
                "delta_mmr": 0,
                "winner": "p1" if r.random() > 0.5 else "p2",
                "duration_min": round(max(1.0, r.gauss(10, 4)), 1),
                "score_diff": round(r.gauss(0, 5), 1),
            }),
        },
    },
    {
        "block": 7, "title": "G8: Прогноз покупок Free-to-Play игроков",
        "description": (
            "Продуктовая команда F2P-игры планирует промо-акции с ограниченным "
            "бюджетом. Нужно заранее находить игроков, которые с высокой "
            "вероятностью заплатят в течение 30 дней, и предлагать им персональные "
            "бонусы. У тебя 600 игроков: уровень, время в игре, сессий в неделю, "
            "достижения, социальная активность, страна, платформа (iOS/Android), "
            "и флаг — сделал ли игрок хотя бы одну покупку. Нужно обучить Random "
            "Forest, оценить качество (accuracy, precision, recall, F1, ROC-AUC) "
            "и вывести feature importance — какие факторы сильнее всего "
            "предсказывают платящего игрока. Deliverable: обученная модель + "
            "classification_report + feature importance plot + бизнес-вывод "
            "('на какие сегменты таргетировать промо')."
        ),
        "theme": "gaming", "difficulty": 4,
        "template_code": r'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, roc_auc_score)
from sklearn.preprocessing import OneHotEncoder

np.random.seed(42)
N = 600
df = pd.DataFrame({
    "level": np.random.randint(1, 80, N),
    "playtime_hours": np.random.gamma(3, 20, N).round(1),
    "sessions_per_week": np.random.randint(1, 25, N),
    "achievements": np.random.randint(0, 100, N),
    "social_score": np.random.randint(0, 50, N),
    "country": np.random.choice(["US", "RU", "BR", "JP", "DE"], N),
    "platform": np.random.choice(["iOS", "Android"], N),
})
# Логит для покупки
logit = (-3 + 0.04 * df.level + 0.01 * df.playtime_hours
         + 0.1 * df.sessions_per_week + 0.02 * df.achievements
         + 0.03 * df.social_score)
prob = 1 / (1 + np.exp(-logit))
df["purchased"] = (np.random.rand(N) < prob).astype(int)

print("Размер:", df.shape)
print("Pурчэйс rate:", df.purchased.mean().round(3))
print(df.head())

# TODO 1: One-hot для country и platform. Собери X и y.

# TODO 2: train_test_split (test_size=0.25, random_state=42, stratify=y).

# TODO 3: Обучи RandomForestClassifier(n_estimators=200, random_state=42, max_depth=8).

# TODO 4: Напечатай accuracy, classification_report, ROC-AUC.

# TODO 5: feature importance — топ-7 признаков (горизонтальный bar chart).
plt.tight_layout()
plt.show()
''',
        "solution_code": r'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, roc_auc_score)
from sklearn.preprocessing import OneHotEncoder

np.random.seed(42)
N = 600
df = pd.DataFrame({
    "level": np.random.randint(1, 80, N),
    "playtime_hours": np.random.gamma(3, 20, N).round(1),
    "sessions_per_week": np.random.randint(1, 25, N),
    "achievements": np.random.randint(0, 100, N),
    "social_score": np.random.randint(0, 50, N),
    "country": np.random.choice(["US", "RU", "BR", "JP", "DE"], N),
    "platform": np.random.choice(["iOS", "Android"], N),
})
logit = (-3 + 0.04 * df.level + 0.01 * df.playtime_hours
         + 0.1 * df.sessions_per_week + 0.02 * df.achievements
         + 0.03 * df.social_score)
prob = 1 / (1 + np.exp(-logit))
df["purchased"] = (np.random.rand(N) < prob).astype(int)

cat_cols = ["country", "platform"]
num_cols = ["level", "playtime_hours", "sessions_per_week",
            "achievements", "social_score"]
ohe = OneHotEncoder(sparse_output=False, drop="first")
cat_feats = ohe.fit_transform(df[cat_cols])
cat_names = ohe.get_feature_names_out(cat_cols)
X = pd.DataFrame(cat_feats, columns=cat_names, index=df.index)
X[num_cols] = df[num_cols]
y = df["purchased"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)

model = RandomForestClassifier(n_estimators=200, random_state=42,
                                max_depth=8, class_weight="balanced")
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

print(f"Accuracy: {accuracy_score(y_test, y_pred):.3f}")
print(f"ROC-AUC:  {roc_auc_score(y_test, y_proba):.3f}")
print("\nClassification report:")
print(classification_report(y_test, y_pred, zero_division=0))
print("Confusion matrix:")
print(confusion_matrix(y_test, y_pred))

imp = pd.Series(model.feature_importances_, index=X.columns)
top = imp.sort_values(ascending=True).tail(7)
fig, ax = plt.subplots(figsize=(9, 5))
top.plot(kind="barh", ax=ax, color="teal", edgecolor="black")
ax.set_xlabel("Feature importance")
ax.set_title("Топ-7 факторов покупки")
plt.tight_layout()

print("\n=== БИЗНЕС-ВЫВОД ===")
top3_names = imp.sort_values(ascending=False).head(3).index.tolist()
print(f"Топ-3 признака: {top3_names}")
print("Рекомендация: таргетировать промо на игроков с высоким уровнем, "
      "большим числом сессий и высоким social_score.")
plt.show()
''',
        "dataset": {
            "seed": 42,
            "n_players": 600,
            "fields": ["level", "playtime_hours", "sessions_per_week",
                       "achievements", "social_score", "country",
                       "platform", "purchased"],
            "note": "Конверсия в покупку ~25-30%, сильно зависит от engagement",
            "records": _gen(42, 600, lambda r, i: {
                "level": r.randint(1, 80),
                "playtime_hours": round(max(0.1, r.gauss(60, 30)), 1),
                "sessions_per_week": r.randint(1, 25),
                "achievements": r.randint(0, 100),
                "social_score": r.randint(0, 50),
                "country": r.choice(["US", "RU", "BR", "JP", "DE"]),
                "platform": r.choice(["iOS", "Android"]),
                "purchased": 0,
            }),
        },
    },
    {
        "block": 7, "title": "G9: Обнаружение читеров по телеметрии",
        "description": (
            "Античит-система 'Sentinel' хочет автоматически выявлять игроков с "
            "нечеловеческим поведением. У тебя телеметрия 800 игроков за последнюю "
            "неделю: среднее число убийств за матч, процент хедшотов, win rate, "
            "K/D, точность, среднее время реакции (мс). Большинство — обычные "
            "игроки, но 5-7% — читеры (aimbot, wallhack, scripts) с аномально "
            "хорошими показателями. Нужно построить anomaly detection: "
            "Isolation Forest с contamination=0.07, выявить подозрительных, "
            "сравнить с z-score baseline, нарисовать scatter-plot "
            "(kills_per_match vs headshot_pct) с подсветкой аномалий. "
            "Deliverable: обученный IsolationForest + список из ~50 флагов + "
            "визуализация и метрика precision@n — насколько точно модель нашла "
            "настоящих читеров (предполагаем, что они — топ по kills/headshot)."
        ),
        "theme": "gaming", "difficulty": 5,
        "template_code": r'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

np.random.seed(42)
N_NORMAL = 750
N_CHEATERS = 50
# Normal players
normal = pd.DataFrame({
    "player_id": range(1, N_NORMAL + 1),
    "kills_per_match": np.random.gamma(2, 2, N_NORMAL).round(2),
    "headshot_pct": np.random.normal(0.18, 0.05, N_NORMAL).clip(0, 0.5).round(3),
    "win_rate": np.random.normal(0.5, 0.1, N_NORMAL).clip(0, 1).round(3),
    "kd_ratio": np.random.gamma(1.5, 0.8, N_NORMAL).round(2),
    "accuracy": np.random.normal(0.25, 0.07, N_NORMAL).clip(0, 1).round(3),
    "reaction_ms": np.random.normal(280, 50, N_NORMAL).astype(int),
    "is_cheater": 0,
})
# Cheaters: aimbot = high headshot + low reaction; wallhack = high kills + accuracy
cheat = pd.DataFrame({
    "player_id": range(N_NORMAL + 1, N_NORMAL + N_CHEATERS + 1),
    "kills_per_match": np.random.gamma(7, 2, N_CHEATERS).round(2),
    "headshot_pct": np.random.normal(0.55, 0.10, N_CHEATERS).clip(0.3, 0.9).round(3),
    "win_rate": np.random.normal(0.8, 0.1, N_CHEATERS).clip(0.4, 1).round(3),
    "kd_ratio": np.random.gamma(5, 1.5, N_CHEATERS).round(2),
    "accuracy": np.random.normal(0.55, 0.10, N_CHEATERS).clip(0.3, 0.9).round(3),
    "reaction_ms": np.random.normal(150, 30, N_CHEATERS).astype(int),
    "is_cheater": 1,
})
df = pd.concat([normal, cheat], ignore_index=True).sample(frac=1, random_state=42)
print("Размер:", df.shape)
print("Реальных читеров:", df.is_cheater.sum())
print(df.describe())

FEATURES = ["kills_per_match", "headshot_pct", "win_rate",
            "kd_ratio", "accuracy", "reaction_ms"]
X = df[FEATURES].values

# TODO 1: StandardScaler на X.

# TODO 2: Обучи IsolationForest(contamination=0.07, random_state=42, n_estimators=200).
#   Получи предсказания (1 = норма, -1 = аномалия) и decision_function scores.

# TODO 3: Сравни с baseline по z-score: посчитай для каждой строки среднее |z-score| по 6 фичам.
#   Пометь как аномалию топ-7% по сумме |z|.

# TODO 4: Scatter kills_per_match vs headshot_pct, подсвети аномалии по IsolationForest красным.
#   Подпиши топ-3 аномалии (player_id).

# TODO 5: Посчитай precision: сколько из топ-50 флагов IsolationForest — реальные читеры?
plt.tight_layout()
plt.show()
''',
        "solution_code": r'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

np.random.seed(42)
N_NORMAL = 750
N_CHEATERS = 50
normal = pd.DataFrame({
    "player_id": range(1, N_NORMAL + 1),
    "kills_per_match": np.random.gamma(2, 2, N_NORMAL).round(2),
    "headshot_pct": np.random.normal(0.18, 0.05, N_NORMAL).clip(0, 0.5).round(3),
    "win_rate": np.random.normal(0.5, 0.1, N_NORMAL).clip(0, 1).round(3),
    "kd_ratio": np.random.gamma(1.5, 0.8, N_NORMAL).round(2),
    "accuracy": np.random.normal(0.25, 0.07, N_NORMAL).clip(0, 1).round(3),
    "reaction_ms": np.random.normal(280, 50, N_NORMAL).astype(int),
    "is_cheater": 0,
})
cheat = pd.DataFrame({
    "player_id": range(N_NORMAL + 1, N_NORMAL + N_CHEATERS + 1),
    "kills_per_match": np.random.gamma(7, 2, N_CHEATERS).round(2),
    "headshot_pct": np.random.normal(0.55, 0.10, N_CHEATERS).clip(0.3, 0.9).round(3),
    "win_rate": np.random.normal(0.8, 0.1, N_CHEATERS).clip(0.4, 1).round(3),
    "kd_ratio": np.random.gamma(5, 1.5, N_CHEATERS).round(2),
    "accuracy": np.random.normal(0.55, 0.10, N_CHEATERS).clip(0.3, 0.9).round(3),
    "reaction_ms": np.random.normal(150, 30, N_CHEATERS).astype(int),
    "is_cheater": 1,
})
df = pd.concat([normal, cheat], ignore_index=True).sample(frac=1, random_state=42)

FEATURES = ["kills_per_match", "headshot_pct", "win_rate",
            "kd_ratio", "accuracy", "reaction_ms"]
X = df[FEATURES].values
scaler = StandardScaler()
X_s = scaler.fit_transform(X)

iso = IsolationForest(contamination=0.07, random_state=42, n_estimators=200)
iso.fit(X_s)
labels = iso.predict(X_s)  # 1 = normal, -1 = anomaly
scores = iso.decision_function(X_s)
df["iforest_flag"] = (labels == -1).astype(int)

# Z-score baseline
z = np.abs(X_s)
df["z_total"] = z.mean(axis=1)
threshold_z = df.z_total.quantile(0.93)
df["z_flag"] = (df.z_total >= threshold_z).astype(int)

print(f"IF флагов: {df.iforest_flag.sum()} (реальных читеров: {df.is_cheater.sum()})")
print(f"Z-score флагов: {df.z_flag.sum()}")
if_precision = df[df.iforest_flag == 1].is_cheater.mean()
z_precision = df[df.z_flag == 1].is_cheater.mean()
print(f"Precision: IF={if_precision:.3f}, Z-score={z_precision:.3f}")

fig, ax = plt.subplots(figsize=(9, 6))
normal_mask = df.iforest_flag == 0
anom_mask = df.iforest_flag == 1
ax.scatter(df.loc[normal_mask, "kills_per_match"],
           df.loc[normal_mask, "headshot_pct"],
           c="lightgray", s=20, alpha=0.5, label="норма")
ax.scatter(df.loc[anom_mask, "kills_per_match"],
           df.loc[anom_mask, "headshot_pct"],
           c="red", s=40, alpha=0.7, label="аномалия (IF)")
top_anom = df[anom_mask].sort_values("z_total", ascending=False).head(3)
for _, row in top_anom.iterrows():
    ax.annotate(f"#{int(row.player_id)}",
                (row.kills_per_match, row.headshot_pct),
                fontsize=9, color="darkred",
                xytext=(5, 5), textcoords="offset points")
ax.set_xlabel("Убийств за матч")
ax.set_ylabel("Доля хедшотов")
ax.set_title("Isolation Forest: обнаружение читеров")
ax.legend()
plt.tight_layout()

print("\n=== БИЗНЕС-РЕКОМЕНДАЦИЯ ===")
print(f"IF поднял {df.iforest_flag.sum()} флагов, из них {df[df.iforest_flag==1].is_cheater.sum()} "
      f"подтверждённых читеров (precision {if_precision:.1%}). "
      f"Эти {df[df.iforest_flag==1].player_id.tolist()[:5]}... — "
      f"кандидаты на ручную проверку модераторами.")
plt.show()
''',
        "dataset": {
            "seed": 42,
            "n_normal": 750,
            "n_cheaters": 50,
            "fields": ["player_id", "kills_per_match", "headshot_pct", "win_rate",
                       "kd_ratio", "accuracy", "reaction_ms", "is_cheater"],
            "note": "Читеры отличаются экстремальными kills/headshot/reaction_ms",
            "records": _gen(42, 800, lambda r, i: {
                "player_id": i + 1,
                "kills_per_match": round(r.gammavariate(2, 2), 2),
                "headshot_pct": round(max(0.0, min(0.5, r.gauss(0.18, 0.05))), 3),
                "win_rate": round(max(0.0, min(1.0, r.gauss(0.5, 0.1))), 3),
                "kd_ratio": round(max(0.1, r.gammavariate(1.5, 0.8)), 2),
                "accuracy": round(max(0.0, min(1.0, r.gauss(0.25, 0.07))), 3),
                "reaction_ms": int(max(80, r.gauss(280, 50))),
                "is_cheater": 0,
            }),
        },
    },
    {
        "block": 2, "title": "G10: Дашборд retention и LTV",
        "description": (
            "Ты — BI-аналитик в F2P-игре. CFO хочет ежемесячный дашборд: сколько "
            "игроков приходит, как они удерживаются, сколько денег приносят. "
            "У тебя SQL-таблица 'players' (1000 записей): player_id, signup_date, "
            "last_login, total_spent_usd, sessions, country. И таблица "
            "'logins' (логины по дням, ~3000 строк). Нужно посчитать: "
            "1) cohort retention (по месяцу регистрации — сколько % вернулось "
            "на 1, 7, 30 день), 2) DAU/WAU/MAU, 3) LTV по когортам (средняя "
            "выручка на игрока), 4) ARPPU. Всё через SQL-подобные операции "
            "в pandas + matplotlib. Deliverable: 3-4 графика (line retention "
            "по когортам, bar LTV, line DAU) + сводная таблица с метриками + "
            "короткий вывод ('когорта X удерживается лучше всех, LTV Y')."
        ),
        "theme": "gaming", "difficulty": 3,
        "template_code": r'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

np.random.seed(42)
N = 1000
signup_start = datetime(2024, 1, 1)
signup_dates = [signup_start + timedelta(days=int(d))
                for d in np.random.randint(0, 180, N)]
players = pd.DataFrame({
    "player_id": range(1, N + 1),
    "signup_date": signup_dates,
    "total_spent_usd": np.random.exponential(8, N).round(2),
    "sessions": np.random.poisson(15, N),
    "country": np.random.choice(["US", "RU", "BR", "JP"], N),
})
# last_login = signup + random days
players["last_login"] = players.signup_date + pd.to_timedelta(
    np.random.randint(0, 60, N), unit="D")

# logins: 3 logins per player on average
login_records = []
for _, row in players.iterrows():
    n_logins = np.random.poisson(3)
    for _ in range(n_logins):
        d = row.signup_date + timedelta(days=int(np.random.randint(0, 60)))
        login_records.append({"player_id": row.player_id, "login_date": d})
logins = pd.DataFrame(login_records)

print("Players:", players.shape)
print("Logins:", logins.shape)
print(players.head())

# TODO 1: Cohort: группируй players по месяцу signup_date. Для каждой когорты
#   посчитай retention на дни 1, 7, 30 (вернулся ли игрок в этот день по logins).
#   Нарисуй line chart с тремя линиями (D1, D7, D30 retention по когортам).

# TODO 2: LTV по когортам: средний total_spent_usd + кумулятивный.
#   Bar chart: средний LTV по когортам.

# TODO 3: DAU: уникальные игроки по дням (из logins). Line chart за последние 30 дней.

# TODO 4: Напечатай топ-3 когорты по LTV и когорту с лучшим D30 retention.
plt.tight_layout()
plt.show()
''',
        "solution_code": r'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

np.random.seed(42)
N = 1000
signup_start = datetime(2024, 1, 1)
signup_dates = [signup_start + timedelta(days=int(d))
                for d in np.random.randint(0, 180, N)]
players = pd.DataFrame({
    "player_id": range(1, N + 1),
    "signup_date": signup_dates,
    "total_spent_usd": np.random.exponential(8, N).round(2),
    "sessions": np.random.poisson(15, N),
    "country": np.random.choice(["US", "RU", "BR", "JP"], N),
})
players["last_login"] = players.signup_date + pd.to_timedelta(
    np.random.randint(0, 60, N), unit="D")
login_records = []
for _, row in players.iterrows():
    n_logins = np.random.poisson(3)
    for _ in range(n_logins):
        d = row.signup_date + timedelta(days=int(np.random.randint(0, 60)))
        login_records.append({"player_id": row.player_id, "login_date": d})
logins = pd.DataFrame(login_records)

players["cohort"] = players.signup_date.dt.to_period("M")
merged = logins.merge(players[["player_id", "signup_date", "cohort", "total_spent_usd"]],
                       on="player_id")
merged["days_since_signup"] = (merged.login_date - merged.signup_date).dt.days

# Retention
def retention_at(day):
    return (merged[merged.days_since_signup == day]
            .groupby("cohort")["player_id"]
            .nunique()
            / players.groupby("cohort")["player_id"].nunique())

ret1 = retention_at(1).fillna(0)
ret7 = retention_at(7).fillna(0)
ret30 = retention_at(30).fillna(0)

# LTV
ltv = players.groupby("cohort")["total_spent_usd"].agg(["mean", "sum", "count"])
ltv.columns = ["avg_ltv", "total_revenue", "players"]
arppu = ltv.total_revenue.sum() / (players.total_spent_usd > 0).sum()
print(f"ARPPU = {arppu:.2f}$")
print("\nLTV по когортам:")
print(ltv.round(2))

# DAU за последние 30 дней
recent = logins[logins.login_date >= signup_start + timedelta(days=150)]
dau = recent.groupby("login_date")["player_id"].nunique()

fig, axes = plt.subplots(2, 2, figsize=(13, 9))
axes[0, 0].plot(ret1.index.astype(str), ret1.values, marker="o", label="D1")
axes[0, 0].plot(ret7.index.astype(str), ret7.values, marker="o", label="D7")
axes[0, 0].plot(ret30.index.astype(str), ret30.values, marker="o", label="D30")
axes[0, 0].set_title("Retention по когортам")
axes[0, 0].set_ylabel("Retention")
axes[0, 0].legend()
axes[0, 0].tick_params(axis="x", rotation=30)

axes[0, 1].bar(ltv.index.astype(str), ltv.avg_ltv,
               color="teal", edgecolor="black")
axes[0, 1].set_title("LTV по когортам")
axes[0, 1].set_ylabel("Средний LTV, $")
axes[0, 1].tick_params(axis="x", rotation=30)

axes[1, 0].plot(dau.index, dau.values, color="navy")
axes[1, 0].set_title("DAU за последние 30 дней")
axes[1, 0].set_ylabel("Уникальных игроков")
axes[1, 0].grid(alpha=0.3)

axes[1, 1].bar(["ARPPU", "Avg LTV", "Median spend"],
               [arppu, players.total_spent_usd.mean(),
                players.total_spent_usd.median()],
               color=["gold", "silver", "brown"], edgecolor="black")
axes[1, 1].set_title("Метрики монетизации")

best_ltv_cohort = ltv.avg_ltv.idxmax()
best_d30_cohort = ret30.idxmax()
print(f"\nЛучшая когорта по LTV: {best_ltv_cohort}")
print(f"Лучшая когорта по D30 retention: {best_d30_cohort}")
plt.tight_layout()
plt.show()
''',
        "dataset": {
            "seed": 42,
            "n_players": 1000,
            "fields_players": ["player_id", "signup_date", "last_login",
                               "total_spent_usd", "sessions", "country"],
            "note": "6 когорт (янв-июн 2024), LTV экспоненциальный, retention падает с возрастом",
            "records": _gen(42, 1000, lambda r, i: {
                "player_id": i + 1,
                "signup_date": "2024-01-01",
                "last_login": "2024-03-01",
                "total_spent_usd": round(r.expovariate(1 / 8), 2),
                "sessions": max(1, int(r.gauss(15, 8))),
                "country": r.choice(["US", "RU", "BR", "JP"]),
            }),
        },
    },
    # Космические
    {
        "block": 3, "title": "S1: Анализ истории запусков SpaceX",
        "description": (
            "Ты — data-журналист, пишешь статью о SpaceX для научпоп-портала. "
            "У тебя датасет из 100 запусков Falcon 9 / Falcon Heavy за 2010-2024: "
            "год, успех, тип ракеты, масса полезной нагрузки (кг), стоимость "
            "(млн $), тип орбиты, повторное использование первой ступени. Нужно "
            "изучить тренды: как росло число запусков, как менялся success rate, "
            "как экономила многоразовость, есть ли корреляция между стоимостью "
            "и payload. Deliverable: 4 графика (line: запуски по годам, line: "
            "success rate по годам, scatter: payload vs cost, bar: число "
            "запусков по типу орбиты) + сводка трендов в print()."
        ),
        "theme": "space", "difficulty": 2,
        "template_code": r'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)
years = np.arange(2010, 2025)
launches_per_year = np.array([2, 0, 2, 3, 6, 7, 8, 10, 12, 11, 25, 31, 33, 36, 50])[:15]
records = []
for y, n in zip(years, launches_per_year):
    for _ in range(n):
        success_rate = 0.6 + (y - 2010) * 0.025  # растёт со временем
        success = int(np.random.rand() < min(0.99, success_rate))
        records.append({
            "year": int(y),
            "success": success,
            "rocket": np.random.choice(["Falcon 9", "Falcon Heavy"], p=[0.85, 0.15]),
            "payload_kg": int(np.random.lognormal(7, 1)),
            "cost_musd": round(np.random.normal(60, 20), 1),
            "orbit": np.random.choice(["LEO", "GTO", "ISS", "SSO"], p=[0.5, 0.25, 0.15, 0.1]),
            "reused": int(np.random.rand() < (0.1 + (y - 2015) * 0.08)),
        })
df = pd.DataFrame(records)
print("Размер:", df.shape)
print(df.head())
print("\nУспешных запусков:", df.success.sum(), "из", len(df))

# TODO 1: Line chart — число запусков по годам.

# TODO 2: Line chart — success rate по годам (mean(success) сгруппированно по year).

# TODO 3: Scatter payload_kg vs cost_musd, цветом — success.

# TODO 4: Bar chart — число запусков по типу орбиты.

# TODO 5: Напечатай тренды: среднегодовой рост запусков, средний success rate
#   до 2015 vs после 2018, доля reused ступеней по годам.
plt.tight_layout()
plt.show()
''',
        "solution_code": r'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)
years = np.arange(2010, 2025)
launches_per_year = np.array([2, 0, 2, 3, 6, 7, 8, 10, 12, 11, 25, 31, 33, 36, 50])[:15]
records = []
for y, n in zip(years, launches_per_year):
    success_rate = 0.6 + (y - 2010) * 0.025
    success = int(np.random.rand() < min(0.99, success_rate))
    for _ in range(n):
        success_rate = 0.6 + (y - 2010) * 0.025
        success = int(np.random.rand() < min(0.99, success_rate))
        records.append({
            "year": int(y),
            "success": success,
            "rocket": np.random.choice(["Falcon 9", "Falcon Heavy"], p=[0.85, 0.15]),
            "payload_kg": int(np.random.lognormal(7, 1)),
            "cost_musd": round(np.random.normal(60, 20), 1),
            "orbit": np.random.choice(["LEO", "GTO", "ISS", "SSO"], p=[0.5, 0.25, 0.15, 0.1]),
            "reused": int(np.random.rand() < (0.1 + (y - 2015) * 0.08)),
        })
df = pd.DataFrame(records)

per_year = df.groupby("year").agg(
    launches=("success", "size"),
    success_rate=("success", "mean"),
    reused_pct=("reused", "mean"),
).reset_index()

fig, axes = plt.subplots(2, 2, figsize=(13, 9))
axes[0, 0].plot(per_year.year, per_year.launches, marker="o", color="navy")
axes[0, 0].set_title("Число запусков по годам")
axes[0, 0].set_ylabel("Запусков")
axes[0, 0].grid(alpha=0.3)

axes[0, 1].plot(per_year.year, per_year.success_rate, marker="o", color="green")
axes[0, 1].set_title("Success rate по годам")
axes[0, 1].set_ylabel("Доля успешных")
axes[0, 1].set_ylim(0.5, 1.05)
axes[0, 1].grid(alpha=0.3)

c = ["red" if s == 0 else "green" for s in df.success]
axes[1, 0].scatter(df.payload_kg, df.cost_musd, c=c, alpha=0.5, s=20)
axes[1, 0].set_xlabel("Payload, кг")
axes[1, 0].set_ylabel("Стоимость, млн $")
axes[1, 0].set_title("Payload vs Cost (красный = авария)")

orbit_counts = df.orbit.value_counts()
axes[1, 1].bar(orbit_counts.index, orbit_counts.values,
               color="steelblue", edgecolor="black")
axes[1, 1].set_title("Число запусков по типу орбиты")
axes[1, 1].set_ylabel("Запусков")

print("=== КЛЮЧЕВЫЕ ТРЕНДЫ ===")
early = per_year[per_year.year < 2015].success_rate.mean()
late = per_year[per_year.year >= 2018].success_rate.mean()
growth = (per_year.launches.iloc[-1] - per_year.launches.iloc[0]) / len(per_year)
reused_now = per_year.reused_pct.iloc[-1] * 100
print(f"Success rate до 2015: {early:.1%}, после 2018: {late:.1%}")
print(f"Среднегодовой рост запусков: {growth:.1f}")
print(f"Доля reused ступеней в {per_year.year.iloc[-1]}: {reused_now:.0f}%")
print(f"Корреляция payload↔cost: {df.payload_kg.corr(df.cost_musd):.2f}")
plt.tight_layout()
plt.show()
''',
        "dataset": {
            "seed": 42,
            "n_launches": 100,
            "fields": ["year", "success", "rocket", "payload_kg", "cost_musd",
                       "orbit", "reused"],
            "note": "Исторические данные Falcon 9/Heavy 2010-2024, success rate растёт",
            "records": _gen(42, 100, lambda r, i: {
                "year": 2010 + r.randint(0, 15),
                "success": 0,
                "rocket": _w(r, ["Falcon 9", "Falcon Heavy"], [0.85, 0.15]),
                "payload_kg": int(max(100, r.lognormvariate(7, 1))),
                "cost_musd": round(max(20, r.gauss(60, 20)), 1),
                "orbit": _w(r, ["LEO", "GTO", "ISS", "SSO"], [0.5, 0.25, 0.15, 0.1]),
                "reused": 0,
            }),
        },
    },
    {
        "block": 7, "title": "S2: Прогноз успеха посадки первой ступени",
        "description": (
            "SpaceX экономит миллионы, сажая первую ступень Falcon 9 на платформу "
            "в океане или на сушу. Хочешь предсказать, удастся ли посадка, по "
            "характеристикам запуска. У тебя 200 запусков с попыткой посадки: "
            "тип ракеты, масса полезной нагрузки, площадка запуска, погодные "
            "условия (ветер, облачность), наличие решётчатых рулей (grid fins), "
            "тип платформы (drone ship / ground pad), число предыдущих полётов "
            "ступени. И флаг — успешная ли посадка. Нужно обучить Logistic "
            "Regression, оценить качество (accuracy, precision, recall, F1), "
            "вывести коэффициенты (какие факторы помогают/мешают посадке) и "
            "построить матрицу ошибок. Deliverable: модель + отчёт с метриками "
            "+ интерпретация коэффициентов + график важности признаков."
        ),
        "theme": "space", "difficulty": 4,
        "template_code": r'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix)
from sklearn.preprocessing import OneHotEncoder, StandardScaler

np.random.seed(42)
N = 200
df = pd.DataFrame({
    "rocket": np.random.choice(["Falcon 9", "Falcon Heavy"], N, p=[0.85, 0.15]),
    "payload_kg": np.random.lognormal(7, 1, N).astype(int),
    "launch_site": np.random.choice(["CCAFS", "KSC", "VAFB"], N),
    "wind_speed": np.random.gamma(3, 3, N).round(1),
    "cloud_cover": np.random.uniform(0, 1, N).round(2),
    "grid_fins": np.random.choice([0, 1], N, p=[0.2, 0.8]),
    "platform": np.random.choice(["drone_ship", "ground_pad"], N, p=[0.6, 0.4]),
    "flights_before": np.random.randint(0, 6, N),
})
# Целевая: success зависит от grid_fins, flights_before, payload (обратно), wind (обратно)
logit = (1.5 * df.grid_fins + 0.3 * df.flights_before
         - 0.001 * df.payload_kg - 0.2 * df.wind_speed + 0.5)
prob = 1 / (1 + np.exp(-logit))
df["landed"] = (np.random.rand(N) < prob).astype(int)

print("Размер:", df.shape)
print("Landing rate:", df.landed.mean().round(3))
print(df.head())

# TODO 1: One-hot для rocket, launch_site, platform. Собрать X, y.

# TODO 2: train_test_split (test_size=0.25, random_state=42, stratify=y).
#   StandardScaler.

# TODO 3: LogisticRegression(max_iter=1000). Predict + оценить метрики.

# TODO 4: Напечатай classification_report и confusion_matrix.

# TODO 5: Напечатай коэффициенты модели — какие факторы помогают, какие мешают.
plt.tight_layout()
plt.show()
''',
        "solution_code": r'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix)
from sklearn.preprocessing import OneHotEncoder, StandardScaler

np.random.seed(42)
N = 200
df = pd.DataFrame({
    "rocket": np.random.choice(["Falcon 9", "Falcon Heavy"], N, p=[0.85, 0.15]),
    "payload_kg": np.random.lognormal(7, 1, N).astype(int),
    "launch_site": np.random.choice(["CCAFS", "KSC", "VAFB"], N),
    "wind_speed": np.random.gamma(3, 3, N).round(1),
    "cloud_cover": np.random.uniform(0, 1, N).round(2),
    "grid_fins": np.random.choice([0, 1], N, p=[0.2, 0.8]),
    "platform": np.random.choice(["drone_ship", "ground_pad"], N, p=[0.6, 0.4]),
    "flights_before": np.random.randint(0, 6, N),
})
logit = (1.5 * df.grid_fins + 0.3 * df.flights_before
         - 0.001 * df.payload_kg - 0.2 * df.wind_speed + 0.5)
prob = 1 / (1 + np.exp(-logit))
df["landed"] = (np.random.rand(N) < prob).astype(int)

cat = ["rocket", "launch_site", "platform"]
num = ["payload_kg", "wind_speed", "cloud_cover",
       "grid_fins", "flights_before"]
ohe = OneHotEncoder(sparse_output=False, drop="first")
cat_X = ohe.fit_transform(df[cat])
cat_names = ohe.get_feature_names_out(cat)
X = pd.DataFrame(cat_X, columns=cat_names, index=df.index)
X[num] = df[num]
y = df["landed"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train_s, y_train)
y_pred = model.predict(X_test_s)

print(f"Accuracy: {accuracy_score(y_test, y_pred):.3f}")
print("\nClassification report:")
print(classification_report(y_test, y_pred, zero_division=0))
print("Confusion matrix:")
print(confusion_matrix(y_test, y_pred))

coefs = pd.Series(model.coef_[0], index=X.columns).sort_values()
fig, ax = plt.subplots(figsize=(8, 5))
colors = ["red" if c < 0 else "green" for c in coefs.values]
ax.barh(coefs.index, coefs.values, color=colors, edgecolor="black")
ax.axvline(0, color="black", linewidth=0.8)
ax.set_title("Коэффициенты логистической регрессии\n"
              "(зелёный = помогает посадке, красный = мешает)")
ax.set_xlabel("Коэффициент (стандартизованный)")

print("\n=== ТОП-3 ФАКТОРА В ПОЛЬЗУ ПОСАДКИ ===")
top_pos = coefs.sort_values(ascending=False).head(3)
for k, v in top_pos.items():
    print(f"  {k}: +{v:.2f}")
print("\n=== ТОП-3 ФАКТОРА ПРОТИВ ===")
top_neg = coefs.sort_values().head(3)
for k, v in top_neg.items():
    print(f"  {k}: {v:.2f}")
plt.tight_layout()
plt.show()
''',
        "dataset": {
            "seed": 42,
            "n_launches": 200,
            "fields": ["rocket", "payload_kg", "launch_site", "wind_speed",
                       "cloud_cover", "grid_fins", "platform",
                       "flights_before", "landed"],
            "note": "Синтетические данные: grid_fins и опыт помогают, ветер и payload мешают",
            "records": _gen(42, 200, lambda r, i: {
                "rocket": _w(r, ["Falcon 9", "Falcon Heavy"], [0.85, 0.15]),
                "payload_kg": int(max(100, r.lognormvariate(7, 1))),
                "launch_site": r.choice(["CCAFS", "KSC", "VAFB"]),
                "wind_speed": round(max(0.1, r.gammavariate(3, 3)), 1),
                "cloud_cover": round(r.uniform(0, 1), 2),
                "grid_fins": _w(r, [0, 1], [0.2, 0.8]),
                "platform": _w(r, ["drone_ship", "ground_pad"], [0.6, 0.4]),
                "flights_before": r.randint(0, 6),
                "landed": 0,
            }),
        },
    },
    {
        "block": 4, "title": "S3: Анализ телеметрии спутника",
        "description": (
            "Ты — инженер центра управления полётом спутника 'Meteor-M'. Спутник "
            "на орбите 3 года, телеметрия идёт каждую минуту: напряжение, ток, "
            "температура, уровень сигнала, высота. В данных бывают аномалии — "
            "скачки температуры, потеря сигнала, просадка напряжения. У тебя "
            "5000 замеров (5 дней). Нужно сделать EDA: распределения, временные "
            "ряды, корреляции между параметрами, выявить аномалии (z-score > 3). "
            "Deliverable: 4 графика (line: напряжение и ток во времени, line: "
            "температура с подсветкой аномалий, scatter: напряжение vs температура, "
            "heatmap: корреляции) + список топ-5 аномальных моментов + краткий "
            "вывод о состоянии спутника."
        ),
        "theme": "space", "difficulty": 3,
        "template_code": r'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)
T = 5000
time = np.arange(T)
telemetry = pd.DataFrame({
    "time_h": time / 60,
    "voltage": np.random.normal(28, 0.5, T).round(2),
    "current": np.random.normal(5, 0.3, T).round(2),
    "temperature_c": np.random.normal(15, 4, T).round(1),
    "signal_dbm": np.random.normal(-85, 3, T).round(1),
    "altitude_km": np.random.normal(540, 2, T).round(2),
})
# Inject anomalies
anom_idx = np.random.choice(T, 30, replace=False)
telemetry.loc[anom_idx[:10], "voltage"] -= np.random.uniform(3, 5, 10)
telemetry.loc[anom_idx[10:20], "temperature_c"] += np.random.uniform(15, 25, 10)
telemetry.loc[anom_idx[20:], "signal_dbm"] -= np.random.uniform(20, 30, 10)

print("Размер:", telemetry.shape)
print(telemetry.head())
print("\nDescribe:")
print(telemetry.describe())

# TODO 1: Line chart: voltage и current во времени (subplot 2x1).
#   Выведи rolling mean (окно=50) для voltage.

# TODO 2: Line chart: temperature_c во времени. Подсвети аномалии (|z-score| > 3) красным.

# TODO 3: Scatter voltage vs temperature_c.

# TODO 4: Heatmap корреляций между всеми числовыми колонками.

# TODO 5: Напечатай топ-5 моментов с самым большим отклонением по любой метрике.
plt.tight_layout()
plt.show()
''',
        "solution_code": r'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)
T = 5000
time = np.arange(T)
telemetry = pd.DataFrame({
    "time_h": time / 60,
    "voltage": np.random.normal(28, 0.5, T).round(2),
    "current": np.random.normal(5, 0.3, T).round(2),
    "temperature_c": np.random.normal(15, 4, T).round(1),
    "signal_dbm": np.random.normal(-85, 3, T).round(1),
    "altitude_km": np.random.normal(540, 2, T).round(2),
})
anom_idx = np.random.choice(T, 30, replace=False)
telemetry.loc[anom_idx[:10], "voltage"] -= np.random.uniform(3, 5, 10)
telemetry.loc[anom_idx[10:20], "temperature_c"] += np.random.uniform(15, 25, 10)
telemetry.loc[anom_idx[20:], "signal_dbm"] -= np.random.uniform(20, 30, 10)

NUMERIC = ["voltage", "current", "temperature_c",
           "signal_dbm", "altitude_km"]
z = (telemetry[NUMERIC] - telemetry[NUMERIC].mean()) / telemetry[NUMERIC].std()
telemetry["z_max"] = z.abs().max(axis=1)
telemetry["is_anomaly"] = (telemetry.z_max > 3).astype(int)

fig, axes = plt.subplots(2, 2, figsize=(13, 9))
axes[0, 0].plot(telemetry.time_h, telemetry.voltage,
                color="navy", alpha=0.5, label="voltage")
axes[0, 0].plot(telemetry.time_h, telemetry.voltage.rolling(50).mean(),
                color="red", label="rolling mean(50)")
axes[0, 0].set_title("Напряжение (V)")
axes[0, 0].legend()

anom_t = telemetry[telemetry.is_anomaly == 1]
axes[0, 1].plot(telemetry.time_h, telemetry.temperature_c,
                color="teal", alpha=0.5)
axes[0, 1].scatter(anom_t.time_h, anom_t.temperature_c,
                   color="red", s=20, label=f"аномалии ({len(anom_t)})")
axes[0, 1].set_title("Температура (°C)")
axes[0, 1].legend()

axes[1, 0].scatter(telemetry.voltage, telemetry.temperature_c,
                   c=telemetry.is_anomaly, cmap="RdYlGn_r",
                   alpha=0.4, s=10)
axes[1, 0].set_xlabel("Voltage")
axes[1, 0].set_ylabel("Temperature")
axes[1, 0].set_title("V vs T (красный = аномалия)")

corr = telemetry[NUMERIC].corr()
im = axes[1, 1].imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
axes[1, 1].set_xticks(range(len(NUMERIC)))
axes[1, 1].set_xticklabels(NUMERIC, rotation=30)
axes[1, 1].set_yticks(range(len(NUMERIC)))
axes[1, 1].set_yticklabels(NUMERIC)
axes[1, 1].set_title("Корреляция телеметрии")
plt.colorbar(im, ax=axes[1, 1])

print(f"Всего аномалий: {telemetry.is_anomaly.sum()} из {T}")
top5 = telemetry.nlargest(5, "z_max")[["time_h"] + NUMERIC + ["z_max"]]
print("\nТоп-5 аномальных моментов:")
print(top5.round(2).to_string(index=False))

print("\n=== ВЫВОД ===")
v_corr = corr.loc["voltage", "temperature_c"]
print(f"Корреляция voltage↔temperature = {v_corr:.2f}")
print(f"Спутник в целом в норме, {telemetry.is_anomaly.sum()} аномальных "
      f"замеров требуют разбора инженерами.")
plt.tight_layout()
plt.show()
''',
        "dataset": {
            "seed": 42,
            "n_samples": 5000,
            "fields": ["time_h", "voltage", "current", "temperature_c",
                       "signal_dbm", "altitude_km"],
            "note": "Телеметрия с инжектированными аномалиями: 30 точек с просадками/скачками",
            "records": _gen(42, 5000, lambda r, i: {
                "time_h": round(i / 60, 2),
                "voltage": round(r.gauss(28, 0.5), 2),
                "current": round(r.gauss(5, 0.3), 2),
                "temperature_c": round(r.gauss(15, 4), 1),
                "signal_dbm": round(r.gauss(-85, 3), 1),
                "altitude_km": round(r.gauss(540, 2), 2),
            }),
        },
    },
    {
        "block": 7, "title": "S4: Прогноз отказа двигателя",
        "description": (
            "NASA хочет предсказывать отказ реактивного двигателя до того, как "
            "он случится. У тебя датасет NASA C-MAPSS (симулятор): 400 "
            "двигателей с телеметрией по 12 параметрам (давление, температура, "
            "вибрация, расход топлива, обороты и т.д.) и оставшийся ресурс "
            "(RUL). Нужно построить модель классификации: предсказать, откажет "
            "ли двигатель в ближайшие 30 циклов. Использовать Random Forest, "
            "оценить через train/test split (accuracy, precision, recall, F1, "
            "ROC-AUC), вывести feature importance, построить PR-кривую. "
            "Deliverable: модель + classification_report + feature importance "
            "график + матрица ошибок + бизнес-вывод ('какие датчики — первые "
            "сигналы отказа')."
        ),
        "theme": "space", "difficulty": 4,
        "template_code": r'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, roc_auc_score,
                             precision_recall_curve)

np.random.seed(42)
N = 400
FEATURES = ["rpm", "temp_inlet", "temp_outlet", "pressure_in",
            "pressure_out", "vibration", "fuel_flow", "oil_temp",
            "oil_pressure", "exhaust_temp", "blade_stress", "hours_used"]
rows = []
for _ in range(N):
    row = {f: np.random.normal(100, 10) for f in FEATURES}
    row["hours_used"] = np.random.uniform(0, 3000)
    row["rpm"] = np.random.normal(8000, 200)
    row["vibration"] = np.random.gamma(2, 1)
    rows.append(row)
df = pd.DataFrame(rows)
# fail = сильная вибрация + высокая температура + много часов
logit = (-5 + 0.5 * df.vibration + 0.1 * df.temp_outlet
         + 0.002 * df.hours_used + 0.3 * df.blade_stress
         - 0.05 * df.oil_pressure)
prob = 1 / (1 + np.exp(-logit))
df["fail_in_30"] = (np.random.rand(N) < prob).astype(int)

print("Размер:", df.shape)
print("Fail rate:", df.fail_in_30.mean().round(3))
print(df.head())

# TODO 1: X, y. train_test_split (test_size=0.25, random_state=42, stratify=y).

# TODO 2: RandomForestClassifier(n_estimators=300, max_depth=12,
#   class_weight="balanced", random_state=42).

# TODO 3: Predict, predict_proba. Accuracy, classification_report, ROC-AUC, confusion_matrix.

# TODO 4: Feature importance — горизонтальный bar chart, топ-8.

# TODO 5: PR-curve. Напечатай: какие 3 датчика — самые ранние сигналы отказа?
plt.tight_layout()
plt.show()
''',
        "solution_code": r'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, roc_auc_score,
                             precision_recall_curve)

np.random.seed(42)
N = 400
FEATURES = ["rpm", "temp_inlet", "temp_outlet", "pressure_in",
            "pressure_out", "vibration", "fuel_flow", "oil_temp",
            "oil_pressure", "exhaust_temp", "blade_stress", "hours_used"]
rows = []
for _ in range(N):
    row = {f: np.random.normal(100, 10) for f in FEATURES}
    row["hours_used"] = np.random.uniform(0, 3000)
    row["rpm"] = np.random.normal(8000, 200)
    row["vibration"] = np.random.gamma(2, 1)
    rows.append(row)
df = pd.DataFrame(rows)
logit = (-5 + 0.5 * df.vibration + 0.1 * df.temp_outlet
         + 0.002 * df.hours_used + 0.3 * df.blade_stress
         - 0.05 * df.oil_pressure)
prob = 1 / (1 + np.exp(-logit))
df["fail_in_30"] = (np.random.rand(N) < prob).astype(int)

X = df[FEATURES]
y = df["fail_in_30"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)

model = RandomForestClassifier(n_estimators=300, max_depth=12,
                                class_weight="balanced", random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

print(f"Accuracy: {accuracy_score(y_test, y_pred):.3f}")
print(f"ROC-AUC:  {roc_auc_score(y_test, y_proba):.3f}")
print("\nClassification report:")
print(classification_report(y_test, y_pred, zero_division=0))
print("Confusion matrix:")
print(confusion_matrix(y_test, y_pred))

imp = pd.Series(model.feature_importances_, index=FEATURES)
top = imp.sort_values().tail(8)

prec, rec, _ = precision_recall_curve(y_test, y_proba)

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
top.plot(kind="barh", ax=axes[0], color="firebrick", edgecolor="black")
axes[0].set_title("Топ-8 важных датчиков (feature importance)")
axes[0].set_xlabel("Importance")

axes[1].plot(rec, prec, color="navy")
axes[1].set_xlabel("Recall")
axes[1].set_ylabel("Precision")
axes[1].set_title("PR-кривая")
axes[1].grid(alpha=0.3)

print("\n=== БИЗНЕС-ВЫВОД ===")
top3 = imp.sort_values(ascending=False).head(3).index.tolist()
print(f"Топ-3 датчика-предсказателя отказа: {top3}")
print("Рекомендация: мониторить эти параметры в первую очередь, "
      "при отклонении — плановая инспекция.")
plt.tight_layout()
plt.show()
''',
        "dataset": {
            "seed": 42,
            "n_engines": 400,
            "fields": ["rpm", "temp_inlet", "temp_outlet", "pressure_in",
                       "pressure_out", "vibration", "fuel_flow", "oil_temp",
                       "oil_pressure", "exhaust_temp", "blade_stress",
                       "hours_used", "fail_in_30"],
            "note": "Синтетика в стиле NASA C-MAPSS: вибрация+temp+часы → отказ",
            "records": _gen(42, 400, lambda r, i: {
                "rpm": r.gauss(8000, 200),
                "temp_inlet": r.gauss(100, 10),
                "temp_outlet": r.gauss(150, 15),
                "pressure_in": r.gauss(100, 10),
                "pressure_out": r.gauss(80, 8),
                "vibration": max(0.1, r.gammavariate(2, 1)),
                "fuel_flow": r.gauss(50, 5),
                "oil_temp": r.gauss(90, 8),
                "oil_pressure": r.gauss(60, 6),
                "exhaust_temp": r.gauss(400, 40),
                "blade_stress": r.gauss(110, 12),
                "hours_used": r.uniform(0, 3000),
                "fail_in_30": 0,
            }),
        },
    },
    {
        "block": 7, "title": "S5: Обнаружение аномалий в телеметрии",
        "description": (
            "В телеметрии спутника 'Glonass-K' появляются странные замеры: "
            "то скачки температуры, то потерянный сигнал, то невозможные "
            "значения высоты. Нужно автоматически выделить аномалии через "
            "Isolation Forest, чтобы инженер мог разбирать только подозрительные "
            "точки. У тебя 3000 замеров (2 суток): давление, температура, "
            "сила тока, уровень сигнала, высота. В данные инжектировано "
            "~3% настоящих аномалий. Нужно применить Isolation Forest, "
            "сравнить с z-score baseline, оценить precision/recall относительно "
            "инжектированных ground truth меток, построить 3 графика "
            "(временной ряд с подсветкой, scatter, decision_function). "
            "Deliverable: обученный IsolationForest + отчёт precision/recall + "
            "визуализация и список топ-10 аномальных моментов с их параметрами."
        ),
        "theme": "space", "difficulty": 4,
        "template_code": r'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

np.random.seed(42)
T = 3000
N_TRUE_ANOM = 90
data = pd.DataFrame({
    "time_h": np.arange(T) / 60,
    "pressure": np.random.normal(101, 2, T).round(2),
    "temperature": np.random.normal(20, 3, T).round(1),
    "current": np.random.normal(3, 0.2, T).round(2),
    "signal": np.random.normal(-90, 2, T).round(1),
    "altitude": np.random.normal(19100, 5, T).round(1),
})
# Инжектируем аномалии
anom_idx = np.random.choice(T, N_TRUE_ANOM, replace=False)
data["is_true_anomaly"] = 0
data.loc[anom_idx, "is_true_anomaly"] = 1
data.loc[anom_idx[:30], "temperature"] += np.random.uniform(20, 30, 30)
data.loc[anom_idx[30:60], "signal"] -= np.random.uniform(15, 25, 30)
data.loc[anom_idx[60:], "altitude"] += np.random.uniform(500, 1500, 30)

print("Размер:", data.shape)
print("Ground truth аномалий:", data.is_true_anomaly.sum())
print(data.head())

FEATURES = ["pressure", "temperature", "current", "signal", "altitude"]
X = data[FEATURES].values

# TODO 1: StandardScaler. Обучи IsolationForest(contamination=0.03, random_state=42).

# TODO 2: Получи labels (-1 = anomaly) и decision_function. Посчитай precision/recall
#   относительно data.is_true_anomaly.

# TODO 3: Baseline: z-score по строкам, топ-3% помечаем как аномалии.
#   Сравни precision/recall с Isolation Forest.

# TODO 4: Line chart temperature во времени, подсвети true аномалии и predicted.

# TODO 5: Scatter pressure vs temperature, цветом is_true_anomaly, формой predicted.
plt.tight_layout()
plt.show()
''',
        "solution_code": r'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

np.random.seed(42)
T = 3000
N_TRUE_ANOM = 90
data = pd.DataFrame({
    "time_h": np.arange(T) / 60,
    "pressure": np.random.normal(101, 2, T).round(2),
    "temperature": np.random.normal(20, 3, T).round(1),
    "current": np.random.normal(3, 0.2, T).round(2),
    "signal": np.random.normal(-90, 2, T).round(1),
    "altitude": np.random.normal(19100, 5, T).round(1),
})
anom_idx = np.random.choice(T, N_TRUE_ANOM, replace=False)
data["is_true_anomaly"] = 0
data.loc[anom_idx, "is_true_anomaly"] = 1
data.loc[anom_idx[:30], "temperature"] += np.random.uniform(20, 30, 30)
data.loc[anom_idx[30:60], "signal"] -= np.random.uniform(15, 25, 30)
data.loc[anom_idx[60:], "altitude"] += np.random.uniform(500, 1500, 30)

FEATURES = ["pressure", "temperature", "current", "signal", "altitude"]
X = data[FEATURES].values
scaler = StandardScaler()
X_s = scaler.fit_transform(X)

iso = IsolationForest(contamination=0.03, random_state=42, n_estimators=200)
iso.fit(X_s)
pred = (iso.predict(X_s) == -1).astype(int)
scores = iso.decision_function(X_s)
data["if_pred"] = pred

z = np.abs(X_s).mean(axis=1)
data["z_total"] = z
data["z_pred"] = (z >= np.quantile(z, 0.97)).astype(int)


def pr(pred, true):
    tp = ((pred == 1) & (true == 1)).sum()
    fp = ((pred == 1) & (true == 0)).sum()
    fn = ((pred == 0) & (true == 1)).sum()
    p = tp / (tp + fp) if (tp + fp) else 0
    r = tp / (tp + fn) if (tp + fn) else 0
    return p, r


p_if, r_if = pr(data.if_pred, data.is_true_anomaly)
p_z, r_z = pr(data.z_pred, data.is_true_anomaly)
print(f"Isolation Forest: precision={p_if:.3f}, recall={r_if:.3f}")
print(f"Z-score baseline: precision={p_z:.3f}, recall={r_z:.3f}")

fig, axes = plt.subplots(2, 1, figsize=(13, 8))
axes[0].plot(data.time_h, data.temperature, color="teal", alpha=0.4,
             label="temperature")
anom_t = data[data.is_true_anomaly == 1]
axes[0].scatter(anom_t.time_h, anom_t.temperature,
                color="orange", s=10, label="ground truth")
axes[0].scatter(data.loc[data.if_pred == 1, "time_h"],
                data.loc[data.if_pred == 1, "temperature"],
                color="red", s=4, alpha=0.6, label="IF anomaly")
axes[0].set_title("Temperature: ground truth vs predicted")
axes[0].legend()

c = data.is_true_anomaly.map({0: "lightgray", 1: "orange"})
m = data.if_pred.map({0: "o", 1: "X"})
for i, row in data.iterrows():
    if i % 10 == 0:  # subsample for performance
        axes[1].scatter(row.pressure, row.temperature,
                        c=c[i], marker=m[i], s=20, alpha=0.5)
axes[1].set_xlabel("Pressure")
axes[1].set_ylabel("Temperature")
axes[1].set_title("○ = normal pred, × = anomaly pred, orange = true anom")

top10 = data.nsmallest(10, scores)[FEATURES + ["time_h"]]
print("\nТоп-10 самых аномальных моментов (по decision_function):")
print(top10.round(2).to_string(index=False))
plt.tight_layout()
plt.show()
''',
        "dataset": {
            "seed": 42,
            "n_samples": 3000,
            "n_true_anomalies": 90,
            "fields": ["time_h", "pressure", "temperature", "current",
                       "signal", "altitude", "is_true_anomaly"],
            "note": "90 инжектированных аномалий из 3000 — 3%, типичная доля для IF",
            "records": _gen(42, 3000, lambda r, i: {
                "time_h": round(i / 60, 2),
                "pressure": round(r.gauss(101, 2), 2),
                "temperature": round(r.gauss(20, 3), 1),
                "current": round(r.gauss(3, 0.2), 2),
                "signal": round(r.gauss(-90, 2), 1),
                "altitude": round(r.gauss(19100, 5), 1),
                "is_true_anomaly": 0,
            }),
        },
    },
    {
        "block": 7, "title": "S6: Классификация космических объектов",
        "description": (
            "Система контроля космического пространства (СККП) обнаруживает "
            "объекты на орбите, но не всегда знает, что это: спутник, "
            "астероид, комета, фрагмент ракеты. Нужно построить классификатор "
            "на физических характеристиках: масса, диаметр, орбитальный "
            "радиус, эксцентриситет, альбедо, яркость. У тебя 300 "
            "размеченных объектов. Использовать Decision Tree, оценить через "
            "train/test split (accuracy, precision, recall, F1, confusion "
            "matrix), визуализировать дерево решений (через feature "
            "importances + tree.plot_tree), вывести текстовую интерпретацию "
            "первых 2-3 уровней. Deliverable: обученное дерево + отчёт с "
            "метриками + plot дерева + feature importance + вывод 'какие "
            "параметры отличают спутник от астероида'."
        ),
        "theme": "space", "difficulty": 3,
        "template_code": r'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix)

np.random.seed(42)
N = 300
classes = ["satellite", "asteroid", "comet", "rocket_body"]
rows = []
for cls in classes:
    n = 75
    if cls == "satellite":
        mass = np.random.lognormal(4, 1, n)
        diam = np.random.lognormal(1, 0.5, n)
        orb_r = np.random.normal(7000, 1500, n)
        ecc = np.random.uniform(0, 0.2, n)
        albedo = np.random.uniform(0.1, 0.5, n)
    elif cls == "asteroid":
        mass = np.random.lognormal(15, 2, n)
        diam = np.random.lognormal(3, 0.8, n)
        orb_r = np.random.normal(25000, 5000, n)
        ecc = np.random.uniform(0.1, 0.5, n)
        albedo = np.random.uniform(0.05, 0.3, n)
    elif cls == "comet":
        mass = np.random.lognormal(12, 2, n)
        diam = np.random.lognormal(2, 0.7, n)
        orb_r = np.random.normal(50000, 20000, n)
        ecc = np.random.uniform(0.6, 0.95, n)
        albedo = np.random.uniform(0.02, 0.1, n)
    else:  # rocket_body
        mass = np.random.lognormal(6, 1, n)
        diam = np.random.lognormal(1.5, 0.5, n)
        orb_r = np.random.normal(8000, 1000, n)
        ecc = np.random.uniform(0, 0.15, n)
        albedo = np.random.uniform(0.2, 0.6, n)
    for i in range(n):
        rows.append({
            "mass_kg": mass[i], "diameter_m": diam[i],
            "orbital_radius_km": orb_r[i], "eccentricity": ecc[i],
            "albedo": albedo[i], "class": cls,
        })
df = pd.DataFrame(rows).sample(frac=1, random_state=42).reset_index(drop=True)
print("Размер:", df.shape)
print(df.groupby("class").size())

# TODO 1: X, y. train_test_split (test_size=0.25, random_state=42, stratify=y).

# TODO 2: DecisionTreeClassifier(max_depth=5, random_state=42).

# TODO 3: Predict, accuracy, classification_report, confusion_matrix.

# TODO 4: plot_tree (figsize большое, fontsize маленький).
#   feature_importances_ — горизонтальный bar chart.

# TODO 5: Напечатай: 'Что отличает спутник от астероида: <правила из дерева>'.
plt.tight_layout()
plt.show()
''',
        "solution_code": r'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix)

np.random.seed(42)
N = 300
classes = ["satellite", "asteroid", "comet", "rocket_body"]
rows = []
for cls in classes:
    n = 75
    if cls == "satellite":
        mass = np.random.lognormal(4, 1, n)
        diam = np.random.lognormal(1, 0.5, n)
        orb_r = np.random.normal(7000, 1500, n)
        ecc = np.random.uniform(0, 0.2, n)
        albedo = np.random.uniform(0.1, 0.5, n)
    elif cls == "asteroid":
        mass = np.random.lognormal(15, 2, n)
        diam = np.random.lognormal(3, 0.8, n)
        orb_r = np.random.normal(25000, 5000, n)
        ecc = np.random.uniform(0.1, 0.5, n)
        albedo = np.random.uniform(0.05, 0.3, n)
    elif cls == "comet":
        mass = np.random.lognormal(12, 2, n)
        diam = np.random.lognormal(2, 0.7, n)
        orb_r = np.random.normal(50000, 20000, n)
        ecc = np.random.uniform(0.6, 0.95, n)
        albedo = np.random.uniform(0.02, 0.1, n)
    else:
        mass = np.random.lognormal(6, 1, n)
        diam = np.random.lognormal(1.5, 0.5, n)
        orb_r = np.random.normal(8000, 1000, n)
        ecc = np.random.uniform(0, 0.15, n)
        albedo = np.random.uniform(0.2, 0.6, n)
    for i in range(n):
        rows.append({
            "mass_kg": mass[i], "diameter_m": diam[i],
            "orbital_radius_km": orb_r[i], "eccentricity": ecc[i],
            "albedo": albedo[i], "class": cls,
        })
df = pd.DataFrame(rows).sample(frac=1, random_state=42).reset_index(drop=True)

FEATURES = ["mass_kg", "diameter_m", "orbital_radius_km",
            "eccentricity", "albedo"]
X = df[FEATURES]
y = df["class"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)

model = DecisionTreeClassifier(max_depth=5, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print(f"Accuracy: {accuracy_score(y_test, y_pred):.3f}")
print("\nClassification report:")
print(classification_report(y_test, y_pred, zero_division=0))
print("Confusion matrix:")
cm = confusion_matrix(y_test, y_pred, labels=classes)
print(pd.DataFrame(cm, index=classes, columns=classes))

fig, axes = plt.subplots(1, 2, figsize=(15, 6))
plot_tree(model, feature_names=FEATURES, class_names=classes,
          filled=True, fontsize=7, ax=axes[0], max_depth=3)
axes[0].set_title("Decision Tree (глубина 3)")

imp = pd.Series(model.feature_importances_, index=FEATURES).sort_values()
imp.plot(kind="barh", ax=axes[1], color="steelblue", edgecolor="black")
axes[1].set_title("Feature importance")
axes[1].set_xlabel("Importance")

print("\n=== ГЛАВНЫЕ ОТЛИЧИЯ ===")
top = imp.sort_values(ascending=False).head(3)
for f, v in top.items():
    print(f"  {f}: важность {v:.3f}")
print("Спутник vs астероид: спутники на низкой орбите (≈7000 км) и маленькие, "
      "астероиды на дальней и большего диаметра.")
print("Кометы отличаются экстремальным эксцентриситетом (0.6-0.95).")
plt.tight_layout()
plt.show()
''',
        "dataset": {
            "seed": 42,
            "n_objects": 300,
            "fields": ["mass_kg", "diameter_m", "orbital_radius_km",
                       "eccentricity", "albedo", "class"],
            "note": "4 класса, 75 объектов в каждом, сгенерированы по физ. правдоподобным распределениям",
            "records": _gen(42, 300, lambda r, i: {
                "mass_kg": r.lognormvariate(8, 3),
                "diameter_m": r.lognormvariate(2, 0.8),
                "orbital_radius_km": r.gauss(20000, 15000),
                "eccentricity": r.uniform(0, 0.95),
                "albedo": r.uniform(0.02, 0.6),
                "class": r.choice(["satellite", "asteroid", "comet", "rocket_body"]),
            }),
        },
    },
    {
        "block": 7, "title": "S7: Прогноз расхода топлива",
        "description": (
            "Инженер-проектировщик ракеты-носителя 'Союз-2.1' хочет быстро "
            "оценить расход топлива для разных сценариев миссии. У него данные "
            "150 полётов: масса полезной нагрузки, дистанция до орбиты, "
            "длительность миссии, тяга двигателя, тип орбиты. Нужно построить "
            "Linear Regression, оценить через train/test split (MAE, RMSE, R²), "
            "построить scatter 'факт vs предсказание' и график остатков, "
            "вывести коэффициенты. Deliverable: обученная модель + отчёт с "
            "метриками + scatter факт-vs-предсказание + residual plot + "
            "интерпретация коэффициентов ('каждый +1 кг payload → +X кг "
            "топлива')."
        ),
        "theme": "space", "difficulty": 3,
        "template_code": r'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder

np.random.seed(42)
N = 150
df = pd.DataFrame({
    "payload_kg": np.random.uniform(500, 15000, N).round(1),
    "distance_km": np.random.uniform(200, 36000, N).round(0),
    "duration_h": np.random.uniform(0.5, 12, N).round(2),
    "thrust_kn": np.random.uniform(500, 4000, N).round(0),
    "orbit": np.random.choice(["LEO", "GTO", "GEO", "SSO"], N),
})
# Fuel = базовая + коэф от payload, distance, duration, минус от thrust (эффективность)
noise = np.random.normal(0, 2000, N)
df["fuel_kg"] = (5000
                 + 2.5 * df.payload_kg
                 + 0.8 * df.distance_km
                 + 800 * df.duration_h
                 - 0.5 * df.thrust_kn
                 + noise).round(0)

print("Размер:", df.shape)
print(df.head())
print("\nКорреляция с fuel:")
print(df.select_dtypes("number").corr()["fuel_kg"].round(3))

# TODO 1: One-hot для orbit. Собрать X, y.

# TODO 2: train_test_split (test_size=0.25, random_state=42).

# TODO 3: LinearRegression. Predict. MAE, RMSE, R².

# TODO 4: Scatter y_test vs y_pred, идеальная линия y=x.

# TODO 5: Residual plot (y_test - y_pred vs y_pred). Напечатай коэффициенты
#   и интерпретацию ('каждый +1 кг payload → +X кг fuel').
plt.tight_layout()
plt.show()
''',
        "solution_code": r'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder

np.random.seed(42)
N = 150
df = pd.DataFrame({
    "payload_kg": np.random.uniform(500, 15000, N).round(1),
    "distance_km": np.random.uniform(200, 36000, N).round(0),
    "duration_h": np.random.uniform(0.5, 12, N).round(2),
    "thrust_kn": np.random.uniform(500, 4000, N).round(0),
    "orbit": np.random.choice(["LEO", "GTO", "GEO", "SSO"], N),
})
noise = np.random.normal(0, 2000, N)
df["fuel_kg"] = (5000
                 + 2.5 * df.payload_kg
                 + 0.8 * df.distance_km
                 + 800 * df.duration_h
                 - 0.5 * df.thrust_kn
                 + noise).round(0)

ohe = OneHotEncoder(sparse_output=False, drop="first")
cat = ohe.fit_transform(df[["orbit"]])
cat_names = ohe.get_feature_names_out(["orbit"])
num = ["payload_kg", "distance_km", "duration_h", "thrust_kn"]
X = pd.DataFrame(cat, columns=cat_names, index=df.index)
X[num] = df[num]
y = df["fuel_kg"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"MAE:  {mae:.0f} кг")
print(f"RMSE: {rmse:.0f} кг")
print(f"R²:   {r2:.3f}")

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
axes[0].scatter(y_test, y_pred, alpha=0.5, color="navy")
lo = min(y_test.min(), y_pred.min())
hi = max(y_test.max(), y_pred.max())
axes[0].plot([lo, hi], [lo, hi], "r--", label="идеал")
axes[0].set_xlabel("Фактический расход, кг")
axes[0].set_ylabel("Предсказанный, кг")
axes[0].set_title(f"Факт vs Предсказание (R²={r2:.3f})")
axes[0].legend()

residuals = y_test - y_pred
axes[1].scatter(y_pred, residuals, alpha=0.5, color="firebrick")
axes[1].axhline(0, color="black", linestyle="--")
axes[1].set_xlabel("Предсказанный расход, кг")
axes[1].set_ylabel("Остаток (факт - предсказание)")
axes[1].set_title("Residual plot")

print("\n=== КОЭФФИЦИЕНТЫ ===")
for name, c in zip(X.columns, model.coef_):
    print(f"  {name}: {c:+.2f}")
print(f"  intercept: {model.intercept_:.0f}")
print(f"\nИнтерпретация: каждый +1000 кг полезной нагрузки → "
      f"+{model.coef_[np.where(X.columns=='payload_kg')[0][0]] * 1000:.0f} кг топлива.")
print(f"Каждые +1000 км дистанции → +{model.coef_[np.where(X.columns=='distance_km')[0][0]] * 1000:.0f} кг топлива.")
plt.tight_layout()
plt.show()
''',
        "dataset": {
            "seed": 42,
            "n_missions": 150,
            "fields": ["payload_kg", "distance_km", "duration_h", "thrust_kn",
                       "orbit", "fuel_kg"],
            "note": "fuel = 5000 + 2.5*payload + 0.8*distance + 800*duration - 0.5*thrust + noise",
            "records": _gen(42, 150, lambda r, i: {
                "payload_kg": round(r.uniform(500, 15000), 1),
                "distance_km": round(r.uniform(200, 36000), 0),
                "duration_h": round(r.uniform(0.5, 12), 2),
                "thrust_kn": round(r.uniform(500, 4000), 0),
                "orbit": r.choice(["LEO", "GTO", "GEO", "SSO"]),
                "fuel_kg": 0,
            }),
        },
    },
    {
        "block": 6, "title": "S8: Анализ данных марсохода Curiosity",
        "description": (
            "Ты — planetary data analyst в NASA JPL. У тебя данные за 1000 "
            "солов (марсианских суток) с марсохода Curiosity: температура, "
            "давление, влажность, скорость ветра, радиация, прозрачность "
            "атмосферы (opacity). Нужно сделать полный EDA: распределения, "
            "тренды, корреляции, сезонность (у Марса есть времена года). "
            "Найти аномалии (пылевые бури — резкий рост opacity и падение "
            "давления), построить сводный отчёт. Deliverable: 6 графиков "
            "(line температуры по солам, line давления, scatter температура "
            "vs давление, histogram радиации, bar средние по сезонам, "
            "heatmap корреляций) + статистика по каждой переменной + список "
            "подозрительных периодов (возможные пылевые бури)."
        ),
        "theme": "space", "difficulty": 3,
        "template_code": r'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)
N = 1000
sol = np.arange(N)
season = (sol // 200) % 4
data = pd.DataFrame({
    "sol": sol,
    "season": np.where(season == 0, "зима",
                np.where(season == 1, "весна",
                  np.where(season == 2, "лето", "осень"))),
    "temp_c": np.random.normal(-60, 15, N).round(1)
                + np.where(season == 2, 20, np.where(season == 0, -10, 5)),
    "pressure_pa": np.random.normal(700, 30, N).round(1)
                + np.where(season == 2, -50, 0),
    "humidity_pct": np.random.uniform(0, 100, N).round(1),
    "wind_m_s": np.random.gamma(2, 2, N).round(1),
    "radiation_mgy": np.random.gamma(3, 0.3, N).round(3),
    "opacity": np.random.gamma(0.5, 0.5, N).round(2),
})
# Пылевые бури
storm_idx = np.random.choice(N, 20, replace=False)
data.loc[storm_idx, "opacity"] += np.random.uniform(2, 4, 20)
data.loc[storm_idx, "pressure_pa"] -= np.random.uniform(50, 100, 20)

print("Размер:", data.shape)
print(data.head())
print("\nDescribe:")
print(data.describe())

# TODO 1: Line temp_c по solам, цветом сезон. Отметь пылевые бури (opacity > 2) красным.

# TODO 2: Line pressure_pa по solам, добавь скользящее среднее (окно 30).

# TODO 3: Scatter temp_c vs pressure_pa, подсвети storm_idx.

# TODO 4: Histogram radiation_mgy (bins=30).

# TODO 5: Bar chart средних значений temp_c, pressure_pa, opacity по сезонам (subplot 1x3).

# TODO 6: Heatmap корреляций числовых переменных.

# TODO 7: Напечатай список солов, где opacity > 2 — кандидаты на пылевые бури.
plt.tight_layout()
plt.show()
''',
        "solution_code": r'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)
N = 1000
sol = np.arange(N)
season = (sol // 200) % 4
data = pd.DataFrame({
    "sol": sol,
    "season": np.where(season == 0, "зима",
                np.where(season == 1, "весна",
                  np.where(season == 2, "лето", "осень"))),
    "temp_c": np.random.normal(-60, 15, N).round(1)
                + np.where(season == 2, 20, np.where(season == 0, -10, 5)),
    "pressure_pa": np.random.normal(700, 30, N).round(1)
                + np.where(season == 2, -50, 0),
    "humidity_pct": np.random.uniform(0, 100, N).round(1),
    "wind_m_s": np.random.gamma(2, 2, N).round(1),
    "radiation_mgy": np.random.gamma(3, 0.3, N).round(3),
    "opacity": np.random.gamma(0.5, 0.5, N).round(2),
})
storm_idx = np.random.choice(N, 20, replace=False)
data.loc[storm_idx, "opacity"] += np.random.uniform(2, 4, 20)
data.loc[storm_idx, "pressure_pa"] -= np.random.uniform(50, 100, 20)

NUMERIC = ["temp_c", "pressure_pa", "humidity_pct",
           "wind_m_s", "radiation_mgy", "opacity"]
storms = data[data.opacity > 2]

fig, axes = plt.subplots(3, 2, figsize=(14, 12))
season_colors = {"зима": "blue", "весна": "green",
                 "лето": "red", "осень": "orange"}
for s_name, color in season_colors.items():
    mask = data.season == s_name
    axes[0, 0].plot(data.loc[mask, "sol"], data.loc[mask, "temp_c"],
                    ".", color=color, alpha=0.5, label=s_name, markersize=2)
axes[0, 0].scatter(storms.sol, storms.temp_c, color="black",
                   s=20, label="storm")
axes[0, 0].set_title("Температура по солам")
axes[0, 0].set_ylabel("°C")
axes[0, 0].legend(fontsize=7)

axes[0, 1].plot(data.sol, data.pressure_pa, color="teal", alpha=0.5)
axes[0, 1].plot(data.sol, data.pressure_pa.rolling(30).mean(),
                color="red", label="rolling mean(30)")
axes[0, 1].set_title("Давление (Pa)")
axes[0, 1].legend()

c = data.opacity.map(lambda v: "red" if v > 2 else "lightgray")
axes[1, 0].scatter(data.temp_c, data.pressure_pa, c=c, alpha=0.4, s=10)
axes[1, 0].set_xlabel("Temp °C")
axes[1, 0].set_ylabel("Pressure Pa")
axes[1, 0].set_title("T vs P (красный = storm)")

axes[1, 1].hist(data.radiation_mgy, bins=30, color="darkorange", edgecolor="black")
axes[1, 1].set_title("Радиация (mGy/day)")
axes[1, 1].axvline(data.radiation_mgy.mean(), color="red", linestyle="--",
                   label=f"mean={data.radiation_mgy.mean():.2f}")
axes[1, 1].legend()

season_mean = data.groupby("season")[NUMERIC[:3]].mean()
season_mean.plot(kind="bar", ax=axes[2, 0], edgecolor="black")
axes[2, 0].set_title("Средние по сезонам")
axes[2, 0].tick_params(axis="x", rotation=0)

corr = data[NUMERIC].corr()
im = axes[2, 1].imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
axes[2, 1].set_xticks(range(len(NUMERIC)))
axes[2, 1].set_xticklabels(NUMERIC, rotation=30, fontsize=8)
axes[2, 1].set_yticks(range(len(NUMERIC)))
axes[2, 1].set_yticklabels(NUMERIC, fontsize=8)
axes[2, 1].set_title("Корреляции")
plt.colorbar(im, ax=axes[2, 1])

print(f"Пылевые бури (opacity > 2): {len(storms)} эпизодов")
print(f"Солы бурь: {storms.sol.tolist()[:10]}...")
print(f"\nКорреляция temp↔pressure: {corr.loc['temp_c', 'pressure_pa']:.2f}")
print(f"Корреляция opacity↔pressure: {corr.loc['opacity', 'pressure_pa']:.2f}")
plt.tight_layout()
plt.show()
''',
        "dataset": {
            "seed": 42,
            "n_sols": 1000,
            "fields": ["sol", "season", "temp_c", "pressure_pa", "humidity_pct",
                       "wind_m_s", "radiation_mgy", "opacity"],
            "note": "Симулированные данные марсохода: 4 сезона, 20 пылевых бурь",
            "records": _gen(42, 1000, lambda r, i: {
                "sol": i,
                "season": r.choice(["зима", "весна", "лето", "осень"]),
                "temp_c": round(r.gauss(-50, 15), 1),
                "pressure_pa": round(r.gauss(700, 30), 1),
                "humidity_pct": round(r.uniform(0, 100), 1),
                "wind_m_s": round(max(0.1, r.gammavariate(2, 2)), 1),
                "radiation_mgy": round(max(0.01, r.gammavariate(3, 0.3)), 3),
                "opacity": round(max(0.01, r.gammavariate(0.5, 0.5)), 2),
            }),
        },
    },
    {
        "block": 7, "title": "S9: Кластеризация экзопланет",
        "description": (
            "Астрономы открыли 5000+ экзопланет, и хотят понять, есть ли среди "
            "них естественные 'семейства' по физическим характеристикам. У тебя "
            "200 экзопланет из каталога NASA: масса (в массах Юпитера), радиус, "
            "орбитальный период (дни), расстояние до звезды (AU), температура "
            "поверхности, температура звезды. Нужно с помощью K-Means выделить "
            "3-5 кластеров, проинтерпретировать каждый ('горячие юпитеры', "
            "'суперземли', 'ледяные гиганты'), построить scatter (масса vs "
            "орбитальный период, цвет по кластеру) + elbow + radar-chart по "
            "центроидам. Deliverable: модель + интерпретация кластеров с "
            "названиями + 3 графика + средние значения по кластерам."
        ),
        "theme": "space", "difficulty": 3,
        "template_code": r'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

np.random.seed(42)
N = 200
exo = pd.DataFrame({
    "mass_jup": np.concatenate([
        np.random.lognormal(-1, 0.5, 60),  # землеподобные
        np.random.lognormal(0.5, 0.3, 60),  # суперземли/нептуны
        np.random.lognormal(2, 0.5, 60),    # газовые гиганты
        np.random.lognormal(0, 0.3, 20),    # горячие юпитеры
    ]),
    "radius_earth": np.concatenate([
        np.random.lognormal(0.5, 0.3, 60),
        np.random.lognormal(1.5, 0.3, 60),
        np.random.lognormal(2.5, 0.3, 60),
        np.random.lognormal(1.2, 0.2, 20),
    ]),
    "orbital_period_d": np.concatenate([
        np.random.lognormal(3, 1, 60),
        np.random.lognormal(5, 1, 60),
        np.random.lognormal(7, 1.5, 60),
        np.random.lognormal(0.5, 0.3, 20),
    ]),
    "distance_au": np.concatenate([
        np.random.lognormal(0, 0.5, 60),
        np.random.lognormal(0.5, 0.5, 60),
        np.random.lognormal(1, 0.7, 60),
        np.random.lognormal(-1.5, 0.3, 20),
    ]),
    "temp_k": np.concatenate([
        np.random.normal(250, 50, 60),
        np.random.normal(350, 80, 60),
        np.random.normal(150, 30, 60),
        np.random.normal(1500, 300, 20),
    ]),
    "star_temp_k": np.random.normal(5800, 800, N).astype(int),
})
exo = exo.clip(lower=0.01)
print("Размер:", exo.shape)
print(exo.describe().round(2))

FEATURES = ["mass_jup", "radius_earth", "orbital_period_d",
            "distance_au", "temp_k", "star_temp_k"]
X = exo[FEATURES].values

# TODO 1: StandardScaler.

# TODO 2: Elbow method — inertia для K в 2..7.

# TODO 3: KMeans(K=4, random_state=42). Predict labels.

# TODO 4: Scatter mass_jup (log) vs orbital_period_d (log), цвет по кластеру.

# TODO 5: Bar chart средних значений признаков по кластерам. Дай кластерам названия
#   ('горячие юпитеры', 'суперземли', 'газовые гиганты', 'землеподобные').
plt.tight_layout()
plt.show()
''',
        "solution_code": r'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

np.random.seed(42)
N = 200
exo = pd.DataFrame({
    "mass_jup": np.concatenate([
        np.random.lognormal(-1, 0.5, 60),
        np.random.lognormal(0.5, 0.3, 60),
        np.random.lognormal(2, 0.5, 60),
        np.random.lognormal(0, 0.3, 20),
    ]),
    "radius_earth": np.concatenate([
        np.random.lognormal(0.5, 0.3, 60),
        np.random.lognormal(1.5, 0.3, 60),
        np.random.lognormal(2.5, 0.3, 60),
        np.random.lognormal(1.2, 0.2, 20),
    ]),
    "orbital_period_d": np.concatenate([
        np.random.lognormal(3, 1, 60),
        np.random.lognormal(5, 1, 60),
        np.random.lognormal(7, 1.5, 60),
        np.random.lognormal(0.5, 0.3, 20),
    ]),
    "distance_au": np.concatenate([
        np.random.lognormal(0, 0.5, 60),
        np.random.lognormal(0.5, 0.5, 60),
        np.random.lognormal(1, 0.7, 60),
        np.random.lognormal(-1.5, 0.3, 20),
    ]),
    "temp_k": np.concatenate([
        np.random.normal(250, 50, 60),
        np.random.normal(350, 80, 60),
        np.random.normal(150, 30, 60),
        np.random.normal(1500, 300, 20),
    ]),
    "star_temp_k": np.random.normal(5800, 800, N).astype(int),
})
exo = exo.clip(lower=0.01)

FEATURES = ["mass_jup", "radius_earth", "orbital_period_d",
            "distance_au", "temp_k", "star_temp_k"]
X = exo[FEATURES].values
scaler = StandardScaler()
X_s = scaler.fit_transform(X)

inertias = []
for k in range(2, 8):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_s)
    inertias.append(km.inertia_)

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
axes[0].plot(range(2, 8), inertias, marker="o", color="navy")
axes[0].set_title("Elbow method")
axes[0].set_xlabel("K")
axes[0].set_ylabel("Inertia")
axes[0].grid(alpha=0.3)

K_FINAL = 4
km = KMeans(n_clusters=K_FINAL, random_state=42, n_init=10)
labels = km.fit_predict(X_s)
exo["cluster"] = labels

colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]
for c in range(K_FINAL):
    mask = labels == c
    axes[1].scatter(np.log10(exo.loc[mask, "mass_jup"]),
                    np.log10(exo.loc[mask, "orbital_period_d"]),
                    c=colors[c], s=20, alpha=0.6, label=f"cluster {c}")
axes[1].set_xlabel("log10(mass, Mjup)")
axes[1].set_ylabel("log10(period, days)")
axes[1].set_title("Кластеры экзопланет")
axes[1].legend()
axes[1].grid(alpha=0.3)

summary = exo.groupby("cluster")[FEATURES].mean().round(2)
print("=== СРЕДНИЕ ПО КЛАСТЕРАМ ===")
print(summary)

names = {
    0: "землеподобные",
    1: "нептуны/суперземли",
    2: "газовые гиганты",
    3: "горячие юпитеры",
}
print("\n=== ИНТЕРПРЕТАЦИЯ ===")
for c, name in names.items():
    n = (labels == c).sum()
    print(f"  Кластер {c} ({n} планет): {name}")
plt.tight_layout()
plt.show()
''',
        "dataset": {
            "seed": 42,
            "n_exoplanets": 200,
            "fields": ["mass_jup", "radius_earth", "orbital_period_d",
                       "distance_au", "temp_k", "star_temp_k"],
            "note": "4 естественных кластера экзопланет: землеподобные, нептуны, гиганты, горячие юпитеры",
            "records": _gen(42, 200, lambda r, i: {
                "mass_jup": max(0.01, r.lognormvariate(0.5, 1.0)),
                "radius_earth": max(0.1, r.lognormvariate(1.5, 0.8)),
                "orbital_period_d": max(0.1, r.lognormvariate(4, 2)),
                "distance_au": max(0.01, r.lognormvariate(0.3, 0.8)),
                "temp_k": max(50, r.gauss(400, 400)),
                "star_temp_k": int(max(2500, r.gauss(5800, 800))),
            }),
        },
    },
    {
        "block": 4, "title": "S10: Временной ряд: орбитальные данные",
        "description": (
            "Спутник 'Copernicus-Sentinel' на низкой околоземной орбите постепенно "
            "снижается из-за атмосферного сопротивления. У тебя телеметрия за "
            "180 дней: высота (км), орбитальная скорость (км/с), наклонение "
            "(°), период обращения (мин). Нужно проанализировать временной ряд: "
            "выделить тренд (высота падает — спутник тормозится), оценить "
            "скорость снижения, построить скользящее среднее, посчитать "
            "автокорреляцию, оценить, когда спутник войдёт в плотные слои "
            "(высота < 200 км). Deliverable: 4 графика (line высоты с трендом, "
            "line скорости, scatter период vs высота, line наклонения) + "
            "скорость снижения (м/день) + прогноз 'вход в атмосферу через X "
            "дней' + autocorrelation plot."
        ),
        "theme": "space", "difficulty": 3,
        "template_code": r'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)
T = 180
day = np.arange(T)
# Высота падает примерно на 0.5 км/день + сезонные вариации
altitude = (400 - 0.5 * day + 2 * np.sin(day / 30) + np.random.normal(0, 1, T))
velocity = 7.7 + 0.001 * day + np.random.normal(0, 0.02, T)
inclination = 98.5 + 0.01 * day + np.random.normal(0, 0.1, T)
period_min = 92.5 + 0.02 * day + np.random.normal(0, 0.1, T)

ts = pd.DataFrame({
    "day": day,
    "altitude_km": altitude,
    "velocity_km_s": velocity,
    "inclination_deg": inclination,
    "period_min": period_min,
})
print("Размер:", ts.shape)
print(ts.head())
print("\nDescribe:")
print(ts.describe())

# TODO 1: Line altitude_km во времени. Добавь rolling mean(7) и rolling mean(30).

# TODO 2: Line velocity во времени. Подсвети период, когда altitude < 350.

# TODO 3: Scatter period_min vs altitude_km.

# TODO 4: Line inclination_deg.

# TODO 5: Посчитай скорость снижения (slope из np.polyfit на altitude_km).
#   Спрогнозируй день, когда altitude < 200.

# TODO 6: Autocorrelation для altitude (lag от 1 до 30).
plt.tight_layout()
plt.show()
''',
        "solution_code": r'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)
T = 180
day = np.arange(T)
altitude = (400 - 0.5 * day + 2 * np.sin(day / 30) + np.random.normal(0, 1, T))
velocity = 7.7 + 0.001 * day + np.random.normal(0, 0.02, T)
inclination = 98.5 + 0.01 * day + np.random.normal(0, 0.1, T)
period_min = 92.5 + 0.02 * day + np.random.normal(0, 0.1, T)

ts = pd.DataFrame({
    "day": day,
    "altitude_km": altitude,
    "velocity_km_s": velocity,
    "inclination_deg": inclination,
    "period_min": period_min,
})

slope, intercept = np.polyfit(day, altitude, 1)
print(f"Линейный тренд высоты: {slope:.4f} км/день = "
      f"{slope * 1000:.1f} м/день")

days_to_200 = (200 - intercept) / slope
print(f"Прогноз: altitude < 200 км на день {days_to_200:.0f}")

fig, axes = plt.subplots(2, 2, figsize=(13, 9))
axes[0, 0].plot(ts.day, ts.altitude_km, color="navy", alpha=0.5,
                label="altitude")
axes[0, 0].plot(ts.day, ts.altitude_km.rolling(7).mean(),
                color="orange", label="rolling(7)")
axes[0, 0].plot(ts.day, ts.altitude_km.rolling(30).mean(),
                color="red", label="rolling(30)")
axes[0, 0].axhline(200, color="black", linestyle="--", label="атмосфера")
trend_line = slope * ts.day + intercept
axes[0, 0].plot(ts.day, trend_line, color="green",
                linestyle=":", label=f"тренд ({slope:.3f} км/день)")
axes[0, 0].set_title("Высота орбиты")
axes[0, 0].set_ylabel("км")
axes[0, 0].legend(fontsize=8)

low = ts[ts.altitude_km < 350]
axes[0, 1].plot(ts.day, ts.velocity_km_s, color="teal", alpha=0.5)
axes[0, 1].scatter(low.day, low.velocity_km_s, color="red",
                   s=10, label="alt<350")
axes[0, 1].set_title("Орбитальная скорость")
axes[0, 1].set_ylabel("км/с")
axes[0, 1].legend()

axes[1, 0].scatter(ts.period_min, ts.altitude_km,
                   c=ts.altitude_km, cmap="viridis_r", s=15, alpha=0.6)
axes[1, 0].set_xlabel("Период, мин")
axes[1, 0].set_ylabel("Высота, км")
axes[1, 0].set_title("Период vs Высота")

axes[1, 1].plot(ts.day, ts.inclination_deg, color="purple")
axes[1, 1].set_title("Наклонение орбиты")
axes[1, 1].set_ylabel("градусы")

plt.tight_layout()
plt.show()

# Autocorrelation
mean_a = ts.altitude_km.mean()
var_a = ts.altitude_km.var()
acf = []
for lag in range(1, 31):
    cov = ((ts.altitude_km[:-lag] - mean_a) * (ts.altitude_km[lag:] - mean_a)).mean()
    acf.append(cov / var_a)

fig, ax = plt.subplots(figsize=(9, 4))
ax.bar(range(1, 31), acf, color="steelblue", edgecolor="black")
ax.axhline(0, color="black")
ax.set_xlabel("Lag (дни)")
ax.set_ylabel("ACF")
ax.set_title("Автокорреляция высоты")
plt.tight_layout()
plt.show()

print(f"\n=== ВЫВОД ===")
print(f"Спутник снижается на {abs(slope) * 1000:.0f} м/день.")
print(f"При сохранении тренда вход в плотные слои — день {days_to_200:.0f}.")
''',
        "dataset": {
            "seed": 42,
            "n_days": 180,
            "fields": ["day", "altitude_km", "velocity_km_s",
                       "inclination_deg", "period_min"],
            "note": "Линейный тренд -0.5 км/день + сезонный синус + шум",
            "records": _gen(42, 180, lambda r, i: {
                "day": i,
                "altitude_km": round(400 - 0.5 * i + 2 * math.sin(i / 30) + r.gauss(0, 1), 2),
                "velocity_km_s": round(7.7 + 0.001 * i + r.gauss(0, 0.02), 3),
                "inclination_deg": round(98.5 + 0.01 * i + r.gauss(0, 0.1), 2),
                "period_min": round(92.5 + 0.02 * i + r.gauss(0, 0.1), 2),
            }),
        },
    },
]


# ============================================================================
# Достижения (10 штук)
# ============================================================================
ACHIEVEMENTS: list[dict[str, Any]] = [
    {"key": "first_lesson", "title": "Первый шаг", "description": "Завершить первый урок", "icon": "🚀",
     "condition": {"type": "lessons_completed", "count": 1}},
    {"key": "python_master", "title": "Python-падаван", "description": "Завершить Блок 1", "icon": "🐍",
     "condition": {"type": "block_completed", "block": 1}},
    {"key": "sql_wizard", "title": "SQL-маг", "description": "Завершить Блок 2", "icon": "🔮",
     "condition": {"type": "block_completed", "block": 2}},
    {"key": "data_cleaner", "title": "Укротитель данных", "description": "Очистить 1000+ строк", "icon": "🧹",
     "condition": {"type": "rows_cleaned", "count": 1000}},
    {"key": "no_hints", "title": "Без подсказок", "description": "Решить 10 упражнений без подсказок", "icon": "🧠",
     "condition": {"type": "no_hint_solves", "count": 10}},
    {"key": "speed_run", "title": "Спидран", "description": "Решить упражнение за < 2 минут", "icon": "⚡",
     "condition": {"type": "fast_solve", "seconds": 120}},
    {"key": "perfect_score", "title": "Перфекционист", "description": "100% в любом блоке", "icon": "💯",
     "condition": {"type": "block_score", "percent": 100}},
    {"key": "half_way", "title": "Полпути", "description": "Завершить 50% курса", "icon": "🎯",
     "condition": {"type": "course_progress", "percent": 50}},
    {"key": "interview_ready", "title": "Готов к бою", "description": "Ответить на 50 вопросов собеседования", "icon": "💼",
     "condition": {"type": "interview_answered", "count": 50}},
    {"key": "graduate", "title": "Junior Data Scientist", "description": "Завершить все блоки", "icon": "🎓",
     "condition": {"type": "course_completed"}},
]


# ============================================================================
# Вопросы для собеседований (представительные 50, не 280)
# ============================================================================
INTERVIEW_QUESTIONS: list[dict[str, Any]] = [
    # Python
    {"category": "python", "question": "Чем отличается list от tuple?",
     "answer": "list — изменяемый (мутабельный), tuple — нет. Tuple быстрее, может быть ключом dict.",
     "explanation": "list использует [], tuple — (). list.append(), tuple не имеет мутирующих методов.",
     "common_mistakes": "Говорить 'tuple быстрее из-за immutable' — да, но точная разница ~10-20% на маленьких коллекциях.",
     "tags": ["types", "collections"], "is_top": True},
    {"category": "python", "question": "Что такое *args и **kwargs?",
     "answer": "*args — произвольное число позиционных аргументов (кортеж). **kwargs — именованных (словарь).",
     "explanation": "def f(*args, **kwargs): args=(1,2,3), kwargs={'a':1, 'b':2}",
     "common_mistakes": "Забыть распаковать: print(*args) вместо print(args).",
     "tags": ["functions"], "is_top": True},
    {"category": "python", "question": "Что такое list comprehension?",
     "answer": "Способ создать список в одну строку: [x**2 for x in range(10) if x % 2 == 0]",
     "explanation": "Быстрее цикла с append, читабельнее. Аналоги есть для dict, set.",
     "tags": ["syntax", "performance"], "is_top": True},
    {"category": "python", "question": "Чем `is` отличается от `==`?",
     "answer": "`is` сравнивает идентичность (один объект в памяти), `==` — равенство значений.",
     "explanation": "a = [1, 2]; b = [1, 2]; a == b (True), a is b (False). Для int/str кэширование может давать True для is.",
     "tags": ["operators"], "is_top": True},
    {"category": "python", "question": "Как работает словарь (dict) под капотом?",
     "answer": "Хеш-таблица: Python вычисляет hash(key), берёт остаток от деления на размер — это индекс корзины. Поиск O(1) в среднем.",
     "explanation": "Ключи должны быть hashable (иммутабельные). При коллизиях — открытая адресация.",
     "common_mistakes": "Путать сложность O(1) среднюю и худшую (O(n) при коллизиях).",
     "tags": ["data-structures", "hash"], "is_top": True},
    {"category": "python", "question": "Что такое генератор (generator)?",
     "answer": "Функция с yield, возвращающая итератор. Ленивая — не хранит все значения в памяти.",
     "explanation": "def gen(): yield 1; yield 2. range() — генератор.",
     "tags": ["iterators"], "is_top": True},
    {"category": "python", "question": "Что делает `with` при работе с файлами?",
     "answer": "Гарантирует вызов .close() даже при исключении. Реализация context manager (методы __enter__/__exit__).",
     "explanation": "with open() as f: ... — эквивалент try-finally с f.close().",
     "tags": ["files", "context-manager"], "is_top": True},
    {"category": "python", "question": "Чем `__init__` отличается от `__new__`?",
     "answer": "__new__ создаёт экземпляр (вызывается первым), __init__ инициализирует его.",
     "explanation": "Для иммутабельных типов (tuple, str) модификации делают через __new__.",
     "tags": ["oop"], "is_top": False},
    {"category": "python", "question": "Что такое GIL?",
     "answer": "Global Interpreter Lock — блокировка, позволяющая только одному потоку Python выполнять байт-код одновременно.",
     "explanation": "Для CPU-bound задач — multiprocessing, не threading. Для I/O — threading ОК.",
     "common_mistakes": "Думать, что threading бесполезен. Для I/O (requests, файлы) он эффективен.",
     "tags": ["concurrency"], "is_top": True},
    {"category": "python", "question": "Что такое lambda-функция?",
     "answer": "Анонимная функция в одну строку: lambda x: x**2",
     "explanation": "Ограничение: только выражение, нельзя присваивать. Для сложного — def.",
     "tags": ["functions"], "is_top": True},
    {"category": "python", "question": "Чем set отличается от list?",
     "answer": "set — неупорядоченный, уникальные элементы, операции | & -. list — упорядоченный, с дубликатами.",
     "explanation": "set быстрее для проверки 'есть ли элемент' (O(1) vs O(n)).",
     "tags": ["collections"], "is_top": True},
    {"category": "python", "question": "Что такое декоратор?",
     "answer": "Функция, оборачивающая другую функцию для добавления поведения.",
     "explanation": "@decorator — синтаксический сахар. Декоратор принимает функцию и возвращает функцию.",
     "tags": ["functions", "metaprogramming"], "is_top": True},
    # SQL
    {"category": "sql", "question": "В чём разница между WHERE и HAVING?",
     "answer": "WHERE фильтрует строки ДО GROUP BY. HAVING фильтрует группы ПОСЛЕ.",
     "explanation": "WHERE нельзя использовать с агрегатами (в строгом SQL).",
     "tags": ["filtering"], "is_top": True},
    {"category": "sql", "question": "Что вернёт запрос SELECT COUNT(*) FROM empty_table?",
     "answer": "0. COUNT(*) считает строки, даже с NULL.",
     "explanation": "COUNT(col) — только NOT NULL значения.",
     "tags": ["aggregates"], "is_top": True},
    {"category": "sql", "question": "В чём разница между INNER JOIN и LEFT JOIN?",
     "answer": "INNER — только совпадающие строки. LEFT — все из левой + NULL для несовпавших.",
     "explanation": "RIGHT — зеркало LEFT. FULL OUTER — все из обеих.",
     "tags": ["joins"], "is_top": True},
    {"category": "sql", "question": "Что такое оконная функция?",
     "answer": "Функция, которая считает по 'окну' строк, не схлопывая результат: ROW_NUMBER(), SUM() OVER, RANK().",
     "explanation": "PARTITION BY — аналог GROUP BY, но без схлопывания.",
     "tags": ["window-functions"], "is_top": True},
    {"category": "sql", "question": "Чем UNION отличается от UNION ALL?",
     "answer": "UNION убирает дубликаты, UNION ALL — оставляет. UNION ALL быстрее.",
     "explanation": "UNION требует сортировки для дедупликации.",
     "tags": ["set-operations"], "is_top": True},
    {"category": "sql", "question": "Что такое CTE?",
     "answer": "Common Table Expression — именованный подзапрос через WITH.",
     "explanation": "WITH name AS (SELECT ...) SELECT ... — читабельнее подзапроса.",
     "tags": ["cte"], "is_top": True},
    {"category": "sql", "question": "Что такое индекс? Зачем он нужен?",
     "answer": "Структура для быстрого поиска (оглавление). Ускоряет SELECT, замедляет INSERT/UPDATE.",
     "explanation": "B-tree — для диапазонов. Hash — для =. Композитный — несколько столбцов.",
     "tags": ["performance", "indexes"], "is_top": True},
    {"category": "sql", "question": "Что такое нормализация?",
     "answer": "Процесс организации данных для уменьшения избыточности (1NF, 2NF, 3NF, BCNF).",
     "explanation": "1NF: атомарные значения. 2NF: 1NF + нет частичных зависимостей. 3NF: 2NF + нет транзитивных.",
     "tags": ["design"], "is_top": True},
    {"category": "sql", "question": "ROW_NUMBER vs RANK vs DENSE_RANK?",
     "answer": "ROW_NUMBER: 1,2,3,4. RANK: 1,1,3,4 (с пропусками). DENSE_RANK: 1,1,2,3 (без пропусков).",
     "explanation": "Все — оконные функции с ORDER BY.",
     "tags": ["window-functions"], "is_top": True},
    # Статистика
    {"category": "statistics", "question": "Что такое p-value?",
     "answer": "Вероятность получить наблюдаемый результат (или более экстремальный) при условии, что нулевая гипотеза верна.",
     "explanation": "p < 0.05 — обычно отвергаем H0. p-value ≠ вероятность H0.",
     "common_mistakes": "Говорить 'p-value — вероятность H0'. Это неверно.",
     "tags": ["hypothesis-testing"], "is_top": True},
    {"category": "statistics", "question": "Чем среднее отличается от медианы?",
     "answer": "Среднее = сумма / кол-во (чувствительно к выбросам). Медиана = середина отсортированного массива (устойчива).",
     "explanation": "Для асимметричных распределений (доходы) медиана репрезентативнее.",
     "tags": ["descriptive"], "is_top": True},
    {"category": "statistics", "question": "Что такое корреляция?",
     "answer": "Мера линейной связи от -1 до +1. 0 = нет линейной связи, но нелинейная может быть.",
     "explanation": "Корреляция ≠ причинно-следственная связь. Спатиальная корреляция — пример ложной.",
     "common_mistakes": "Говорить 'корреляция = причинность'.",
     "tags": ["correlation"], "is_top": True},
    {"category": "statistics", "question": "Что такое центральная предельная теорема?",
     "answer": "Распределение среднего по выборкам сходится к нормальному при росте n, независимо от исходного распределения.",
     "explanation": "Обосновывает использование нормального распределения в статистике.",
     "tags": ["distributions"], "is_top": True},
    {"category": "statistics", "question": "Что такое доверительный интервал?",
     "answer": "Диапазон, в который с заданной вероятностью (обычно 95%) попадает истинное значение параметра.",
     "explanation": "95% ДИ для среднего: x ± 1.96 * SE.",
     "tags": ["estimation"], "is_top": True},
    {"category": "statistics", "question": "Что такое A/B тест?",
     "answer": "Эксперимент: делим пользователей на 2 группы (контроль и тест), сравниваем метрику.",
     "explanation": "Нужна достаточная выборка, рандомизация, одна изменённая переменная.",
     "tags": ["ab-testing"], "is_top": True},
    # ML
    {"category": "ml", "question": "Что такое переобучение (overfitting)?",
     "answer": "Модель хорошо работает на train, плохо на test. Запомнила шум, а не закономерности.",
     "explanation": "Признаки: train accuracy 99%, test 60%. Решения: больше данных, регуляризация, проще модель.",
     "tags": ["bias-variance"], "is_top": True},
    {"category": "ml", "question": "Чем supervised отличается от unsupervised?",
     "answer": "Supervised — есть метки (X, y). Unsupervised — только X, ищем структуру.",
     "explanation": "Supervised: классификация, регрессия. Unsupervised: кластеризация, понижение размерности.",
     "tags": ["basics"], "is_top": True},
    {"category": "ml", "question": "Что такое precision и recall?",
     "answer": "Precision = TP / (TP + FP) — точность. Recall = TP / (TP + FN) — полнота.",
     "explanation": "F1 = 2 * P * R / (P + R). Для дисбаланса классов — смотреть и то, и другое.",
     "common_mistakes": "Использовать accuracy при дисбалансе (90% класс 0 → 90% accuracy на константе).",
     "tags": ["metrics"], "is_top": True},
    {"category": "ml", "question": "Зачем нужна кросс-валидация?",
     "answer": "Чтобы оценить качество модели на новых данных. Разбиваем на k фолдов, обучаем k раз.",
     "explanation": "5-fold CV: train на 4, test на 1, повторяем 5 раз. Среднее — оценка.",
     "tags": ["validation"], "is_top": True},
    {"category": "ml", "question": "Что такое Random Forest?",
     "answer": "Ансамбль деревьев решений. Каждое дерево — на случайной подвыборке данных и признаков.",
     "explanation": "Бэггинг + случайные подпространства. Устойчив к переобучению.",
     "tags": ["ensembles"], "is_top": True},
    {"category": "ml", "question": "Что такое регуляризация?",
     "answer": "Добавление штрафа за сложность модели: L1 (Lasso) или L2 (Ridge).",
     "explanation": "L1 зануляет коэффициенты (отбор признаков). L2 уменьшает их.",
     "tags": ["regularization"], "is_top": True},
    {"category": "ml", "question": "Что такое feature engineering?",
     "answer": "Создание новых признаков из сырых данных: логарифмы, полиномы, агрегации, кодирование.",
     "explanation": "Хороший feature >> хороший алгоритм. 80% успеха в DS — это фичи.",
     "tags": ["features"], "is_top": True},
    {"category": "ml", "question": "Что такое градиентный спуск?",
     "answer": "Оптимизационный метод: обновляем параметры в направлении антиградиента loss.",
     "explanation": "lr — learning rate. SGD, Adam, RMSprop — вариации.",
     "tags": ["optimization"], "is_top": True},
    {"category": "ml", "question": "Что такое K-Means?",
     "answer": "Алгоритм кластеризации: K центроидов, итеративно пересчитываем.",
     "explanation": "Нужно задать K. Чувствителен к инициализации и выбросам.",
     "tags": ["clustering"], "is_top": True},
    {"category": "ml", "question": "Зачем нужен train/test split?",
     "answer": "Чтобы оценить качество на новых данных. Train для обучения, test — для оценки.",
     "explanation": "Обычно 80/20. Стратификация для дисбаланса. Временной ряд — не перемешивать!",
     "tags": ["validation"], "is_top": True},
    {"category": "ml", "question": "Что такое logistic regression?",
     "answer": "Классификация через сигмоиду: P(y=1|X) = 1 / (1 + exp(-X*w)). Несмотря на 'regression' — это классификация.",
     "explanation": "Линейная модель для бинарной классификации. Можно расширить на мультикласс.",
     "tags": ["classification"], "is_top": True},
    # DS General
    {"category": "ds_general", "question": "Опишите полный цикл Data Science проекта.",
     "answer": "1) Бизнес-задача → 2) Данные → 3) Очистка → 4) EDA → 5) Feature Engineering → 6) Моделирование → 7) Оценка → 8) Визуализация → 9) Деплой.",
     "explanation": "Это не линейный процесс — часто возвращаемся назад.",
     "tags": ["process"], "is_top": True},
    {"category": "ds_general", "question": "Как бороться с пропусками в данных?",
     "answer": "Удалить строки, заполнить средним/медианой/модой, предсказать моделью, создать флаг 'был пропуск'.",
     "explanation": "Стратегия зависит от причины пропуска (MCAR, MAR, MNAR).",
     "tags": ["preprocessing"], "is_top": True},
    {"category": "ds_general", "question": "Что такое Data Leakage?",
     "answer": "Утечка данных: использование информации из test в train. Модель выглядит отлично, но в проде проваливается.",
     "explanation": "Примеры: scaling до split, target в features, временной leak.",
     "common_mistakes": "Забыть про временной порядок при time series.",
     "tags": ["pitfalls"], "is_top": True},
    {"category": "ds_general", "question": "Что такое ROC-AUC?",
     "answer": "Площадь под ROC-кривой. 1.0 = идеально, 0.5 = случайно. Устойчив к дисбалансу.",
     "explanation": "ROC = TPR vs FPR. AUC = вероятность, что случайный positive > случайного negative.",
     "tags": ["metrics"], "is_top": True},
    {"category": "ds_general", "question": "Как оценить важность признаков?",
     "answer": "Корреляция, feature importance из деревьев, permutation importance, SHAP.",
     "explanation": "SHAP — state-of-the-art, локальная и глобальная интерпретация.",
     "tags": ["interpretation"], "is_top": True},
    {"category": "ds_general", "question": "Что такое bias-variance tradeoff?",
     "answer": "Bias — ошибка от упрощения, variance — от чувствительности к данным. Нужно балансировать.",
     "explanation": "Простая модель: high bias, low variance. Сложная: low bias, high variance.",
     "tags": ["theory"], "is_top": True},
    {"category": "ds_general", "question": "Как выбрать метрику для задачи?",
     "answer": "Зависит от бизнес-задачи. Классификация: accuracy / F1 / AUC. Регрессия: MAE / RMSE / R².",
     "explanation": "При дисбалансе — F1, AUC. При выбросах в регрессии — MAE, не RMSE.",
     "tags": ["metrics"], "is_top": True},
    {"category": "ds_general", "question": "Что такое exploratory data analysis (EDA)?",
     "answer": "Исследование данных перед моделированием: распределения, выбросы, пропуски, корреляции, визуализация.",
     "explanation": "Цель — понять данные, выдвинуть гипотезы, найти аномалии.",
     "tags": ["eda"], "is_top": True},
    {"category": "ds_general", "question": "Что такое нормализация и зачем она нужна?",
     "answer": "Приведение признаков к одной шкале (MinMax 0..1 или Standard mean=0, std=1). Нужно для KNN, SVM, нейросетей, PCA.",
     "explanation": "Для деревьев — не нужно. Всегда fit на train, transform на train+test.",
     "common_mistakes": "Fit нормализатор на всём датасете, потом делить — leak.",
     "tags": ["preprocessing"], "is_top": True},
    {"category": "ds_general", "question": "Что такое dimensionality reduction?",
     "answer": "Уменьшение числа признаков с сохранением информации. PCA, t-SNE, UMAP.",
     "explanation": "PCA — линейный, t-SNE/UMAP — для визуализации. Используют для feature engineering и визуализации.",
     "tags": ["preprocessing"], "is_top": True},

    # ===== PYTHON (дополнительно 13) =====
    {"category": "python", "difficulty": "junior",
     "question": "Что такое __init__.py и зачем он нужен?",
     "answer": "Файл, маркирующий директорию как Python-пакет. Содержит инициализацию, импорты, __all__.",
     "explanation": "Позволяет делать 'from package import module'. С Python 3.3 namespace packages работают и без него, но код инициализации пакета — только в __init__.py.",
     "common_mistakes": "Путать с методом __init__ класса — это разные вещи.",
     "tags": ["modules", "packages"], "is_top": False},
    {"category": "python", "difficulty": "junior",
     "question": "Чем shallow copy отличается от deep copy?",
     "answer": "Shallow копирует верхний уровень, вложенные объекты — по ссылке. Deep копирует всё рекурсивно.",
     "explanation": "import copy; b = copy.copy(a) — shallow; b = copy.deepcopy(a) — deep. Изменения вложенного объекта в a видны в b при shallow, но не при deep.",
     "common_mistakes": "Думать, что = копирует список — это лишь копирование ссылки на тот же объект.",
     "tags": ["objects", "copy"], "is_top": True},
    {"category": "python", "difficulty": "junior",
     "question": "Какие типы в Python mutable, а какие immutable?",
     "answer": "Mutable: list, dict, set. Immutable: int, float, str, tuple, frozenset, bool, bytes.",
     "explanation": "Immutable объекты нельзя изменить после создания — любая 'модификация' создаёт новый объект. Это важно для хеширования (ключи dict) и безопасности потоков.",
     "common_mistakes": "Считать tuple всегда immutable — tuple из lists изменяем по вложенным элементам.",
     "tags": ["types", "mutability"], "is_top": True},
    {"category": "python", "difficulty": "junior",
     "question": "Что делают else и finally в блоке try/except?",
     "answer": "else выполняется, если исключения НЕ было. finally — выполняется ВСЕГДА (cleanup).",
     "explanation": "try: ... except: ... else: ... finally: ... else полезен для кода, который должен идти только при успехе, finally — для закрытия ресурсов (файлов, соединений).",
     "common_mistakes": "Путать else с except — else срабатывает когда исключения НЕ было, а не 'для всех случаев'.",
     "tags": ["exceptions", "errors"], "is_top": True},
    {"category": "python", "difficulty": "junior",
     "question": "Что такое виртуальное окружение (venv)?",
     "answer": "Изолированная копия Python с своими пакетами. Создаётся через python -m venv myenv.",
     "explanation": "Решает конфликты зависимостей между проектами. Активация: source myenv/bin/activate (Linux/Mac) или myenv\\Scripts\\activate (Windows). requirements.txt фиксирует версии.",
     "common_mistakes": "Ставить пакеты глобально через pip — риск конфликтов и проблемы с воспроизводимостью.",
     "tags": ["environment", "deps"], "is_top": False},
    {"category": "python", "difficulty": "junior",
     "question": "Что такое type hints (аннотации типов) в Python?",
     "answer": "Подсказки типов для параметров и возвращаемых значений: def f(x: int) -> str: ...",
     "explanation": "Python остаётся динамически типизированным — аннотации не проверяются в runtime (без mypy). Улучшают читаемость, помогают IDE, обязательны для публичных библиотек.",
     "common_mistakes": "Думать, что type hints превращают Python в Java — это лишь подсказки, рантайм их игнорирует.",
     "tags": ["typing", "annotations"], "is_top": False},
    {"category": "python", "difficulty": "junior",
     "question": "Чем list.sort() отличается от sorted(list)?",
     "answer": "list.sort() сортирует на месте и возвращает None. sorted(list) возвращает новый отсортированный список.",
     "explanation": "sorted() принимает любой iterable, list.sort() только list. Оба принимают key= и reverse=. sorted() не модифицирует оригинал, list.sort() экономит память.",
     "common_mistakes": "Писать result = list.sort() — будет None, а не отсортированный список.",
     "tags": ["lists", "sorting"], "is_top": False},
    {"category": "python", "difficulty": "junior",
     "question": "Как получить ключи, значения и пары из словаря?",
     "answer": "dict.keys(), dict.values(), dict.items() возвращают view-объекты.",
     "explanation": "for k, v in d.items(): ... View-объекты отражают изменения dict в отличие от list(d.keys()). Для list — явно list(d.keys()).",
     "common_mistakes": "Думать, что view и list — одно и то же. View динамический, list — снимок.",
     "tags": ["dict", "iteration"], "is_top": False},
    {"category": "python", "difficulty": "middle",
     "question": "Как работает Garbage Collector в Python?",
     "answer": "Подсчёт ссылок + cycle detector для циклов. Объект удаляется, когда refcount=0.",
     "explanation": "sys.getrefcount() показывает счётчик. Циклические ссылки (a.b, b.a) ловит модуль gc. Можно отключить gc вручную для производительности в long-running процессах.",
     "common_mistakes": "Думать, что GC мгновенно освобождает память — есть __del__ финализаторы и задержки.",
     "tags": ["memory", "gc"], "is_top": False},
    {"category": "python", "difficulty": "middle",
     "question": "Что такое MRO (Method Resolution Order)?",
     "answer": "Порядок, в котором Python ищет методы в цепочке наследования. Использует C3 linearization.",
     "explanation": "Class.mro() или Class.__mro__ показывает порядок. Для ромбовидного наследования (diamond problem) MRO гарантирует, что каждый класс вызван ровно один раз.",
     "common_mistakes": "Думать, что это просто 'сначала родитель' — на самом деле это сложный C3-алгоритм.",
     "tags": ["oop", "inheritance"], "is_top": False},
    {"category": "python", "difficulty": "middle",
     "question": "Как реализовать свой context manager?",
     "answer": "Класс с __enter__ и __exit__ или генератор с декоратором @contextmanager.",
     "explanation": "class CM: def __enter__(self): ...; def __exit__(self, *exc): .... Альтернатива: @contextmanager и yield один раз. __exit__ решает, подавлять ли исключение (return True).",
     "common_mistakes": "Забыть return self в __enter__ — тогда 'as f' получит None.",
     "tags": ["context-manager", "with"], "is_top": False},
    {"category": "python", "difficulty": "middle",
     "question": "Какие паттерны проектирования ты знаешь и применял?",
     "answer": "Singleton, Factory, Observer, Decorator, Strategy, Adapter, Iterator, Facade.",
     "explanation": "Singleton: один экземпляр (через __new__). Factory: функция создания объектов нужного типа. Observer: подписка на события. Decorator уже встроен в Python (@decorator).",
     "common_mistakes": "Применять паттерны ради паттернов — overengineering. Сначала простое решение.",
     "tags": ["patterns", "oop"], "is_top": False},
    {"category": "python", "difficulty": "middle",
     "question": "Что такое SOLID принципы?",
     "answer": "5 принципов ООП: SRP, OCP, LSP, ISP, DIP — единая ответственность, открытость/закрытость, подстановка Лисков, разделение интерфейсов, инверсия зависимостей.",
     "explanation": "SRP: один класс — одна причина изменяться. OCP: расширяй код, не модифицируй. DIP: зависимости от абстракций, не от реализаций. Помогают писать поддерживаемый код.",
     "common_mistakes": "Слепо следовать SOLID — для маленького скрипта это лишнее. Применяй, когда есть реальная сложность.",
     "tags": ["solid", "oop"], "is_top": False},
    # ===== SQL (дополнительно 16) =====
    {"category": "sql", "difficulty": "junior",
     "question": "Какие бывают типы индексов в SQL?",
     "answer": "B-tree (default, для =, <, >, BETWEEN), Hash (только =), Bitmap (низкая кардинальность), GiST/GIN (полнотекст, JSON).",
     "explanation": "B-tree — сбалансированное дерево, O(log n). Composite index: (a, b) работает для a и (a, b), но не для b одного. Partial index: с WHERE-условием.",
     "common_mistakes": "Создавать индексы на каждый столбец — замедляет INSERT/UPDATE и тратит место.",
     "tags": ["indexes", "performance"], "is_top": True},
    {"category": "sql", "difficulty": "junior",
     "question": "Что такое self-join? Когда используется?",
     "answer": "JOIN таблицы с самой собой. Используется для иерархий (сотрудник → менеджер) и сравнения строк.",
     "explanation": "SELECT e.name, m.name FROM employees e LEFT JOIN employees m ON e.manager_id = m.id. Нужны алиасы, чтобы различать 'роли' одной таблицы.",
     "common_mistakes": "Забыть алиасы — без них JOIN с собой даст ambiguous column.",
     "tags": ["joins"], "is_top": False},
    {"category": "sql", "difficulty": "junior",
     "question": "Чем отличаются DROP, TRUNCATE и DELETE?",
     "answer": "DROP — удаляет таблицу целиком. TRUNCATE — все строки (быстро, без WHERE). DELETE — строки по условию (медленнее, логируется).",
     "explanation": "DROP: DDL, нельзя откатить. TRUNCATE: DDL, минимум логов. DELETE: DML, можно WHERE, логирует каждую строку, можно откатить через транзакцию.",
     "common_mistakes": "Использовать DELETE без WHERE на огромной таблице — лучше TRUNCATE в разы быстрее.",
     "tags": ["ddl", "dml"], "is_top": True},
    {"category": "sql", "difficulty": "junior",
     "question": "Чем primary key отличается от foreign key?",
     "answer": "PK — уникальный идентификатор строки (NOT NULL, UNIQUE). FK — ссылка на PK другой таблицы, обеспечивает целостность связей.",
     "explanation": "PK может быть составным (несколько столбцов). FK может быть NULL (опциональная связь). ON DELETE CASCADE — удалять дочерние строки при удалении родителя.",
     "common_mistakes": "Делать FK на неиндексированный столбец — сильно замедлит JOIN и INSERT.",
     "tags": ["keys", "design"], "is_top": False},
    {"category": "sql", "difficulty": "junior",
     "question": "Какие бывают типы JOIN?",
     "answer": "INNER, LEFT (OUTER), RIGHT (OUTER), FULL (OUTER), CROSS. INNER — только совпадения, LEFT — все из левой + NULL для несовпавших.",
     "explanation": "CROSS JOIN = декартово произведение (все комбинации). FULL OUTER — все из обеих таблиц с NULL где нет совпадений. RIGHT JOIN редко используют, проще переписать через LEFT.",
     "common_mistakes": "Путать LEFT JOIN с LEFT OUTER JOIN — в большинстве СУБД это синонимы.",
     "tags": ["joins"], "is_top": False},
    {"category": "sql", "difficulty": "junior",
     "question": "Что делает ключевое слово DISTINCT?",
     "answer": "Убирает дубликаты из результата SELECT. SELECT DISTINCT col FROM t.",
     "explanation": "Работает по комбинации всех выбранных столбцов. SELECT DISTINCT a, b — уникальные пары. Дорогая операция — СУБД может делать sort или hash.",
     "common_mistakes": "Думать, что DISTINCT применяется к одной колонке — он работает на всём SELECT-списке.",
     "tags": ["select"], "is_top": False},
    {"category": "sql", "difficulty": "junior",
     "question": "Как обрабатывать NULL в SQL?",
     "answer": "NULL — отсутствие значения. Сравнения: IS NULL, IS NOT NULL. Функции: COALESCE(a, b), NULLIF(a, b).",
     "explanation": "NULL не равен NULL (NULL = NULL даёт UNKNOWN, не TRUE). Агрегаты (COUNT, SUM) игнорируют NULL. COUNT(*) считает все строки, COUNT(col) — только NOT NULL.",
     "common_mistakes": "Использовать = NULL вместо IS NULL — стандарт SQL так не работает, = с NULL даёт UNKNOWN.",
     "tags": ["null", "functions"], "is_top": False},
    {"category": "sql", "difficulty": "junior",
     "question": "Что такое алиасы (aliases) в SQL?",
     "answer": "Короткие имена для столбцов или таблиц: SELECT col AS new_name FROM table AS t.",
     "explanation": "AS опционален. Обязательны для self-join. Улучшают читаемость. Алиас можно использовать в ORDER BY и GROUP BY, но НЕ в WHERE и HAVING — они выполняются до SELECT.",
     "common_mistakes": "Пытаться использовать алиас в WHERE — он ещё не существует на момент фильтрации.",
     "tags": ["syntax"], "is_top": False},
    {"category": "sql", "difficulty": "junior",
     "question": "Как работает ORDER BY и какие у него нюансы?",
     "answer": "Сортирует результат: ORDER BY col [ASC|DESC]. По умолчанию ASC. Можно по нескольким колонкам и по выражению.",
     "explanation": "Поведение NULL зависит от СУБД (в PostgreSQL: NULLS FIRST/LAST). ORDER BY col1, col2 — вторичная сортировка по col2 при равных col1. Сортировка может быть дорогой операцией.",
     "common_mistakes": "Думать, что ORDER BY ускоряет запрос — он наоборот может требовать сортировку и замедлять.",
     "tags": ["sorting"], "is_top": False},
    {"category": "sql", "difficulty": "junior",
     "question": "Что делают LIMIT и OFFSET?",
     "answer": "LIMIT — ограничить число строк в результате. OFFSET — пропустить первые N строк (для пагинации).",
     "explanation": "LIMIT 10 OFFSET 20 — строки 21-30. На большой таблице OFFSET дорогой (СУБД всё равно читает первые N). Лучше keyset pagination: WHERE id > last_id LIMIT 10.",
     "common_mistakes": "Использовать LIMIT без ORDER BY — порядок не гарантирован, разные запуски дадут разные строки.",
     "tags": ["pagination"], "is_top": False},
    {"category": "sql", "difficulty": "middle",
     "question": "Чем EXISTS отличается от IN?",
     "answer": "EXISTS проверяет наличие хотя бы одной строки в подзапросе. IN сравнивает с каждым значением. EXISTS часто быстрее для больших подзапросов.",
     "explanation": "IN материализует подзапрос в множество значений, EXISTS — ленивая проверка (true/false). Коррелированный EXISTS может использовать индексы. NULL-семантика тоже отличается.",
     "common_mistakes": "Думать, что IN и EXISTS взаимозаменяемы — при NULL в подзапросе IN может давать неожиданный результат.",
     "tags": ["subqueries", "performance"], "is_top": True},
    {"category": "sql", "difficulty": "middle",
     "question": "Чем VIEW отличается от MATERIALIZED VIEW?",
     "answer": "VIEW — сохранённый запрос, выполняется при каждом обращении. MATERIALIZED VIEW — результат запроса, физически хранится, обновляется вручную (REFRESH).",
     "explanation": "VIEW всегда показывает актуальные данные. MATERIALIZED VIEW быстрее на тяжёлых агрегациях, но данные могут быть устаревшими. Подходит для дашбордов и отчётности.",
     "common_mistakes": "Делать MATERIALIZED VIEW на часто меняющихся данных — REFRESH становится узким местом.",
     "tags": ["views", "performance"], "is_top": False},
    {"category": "sql", "difficulty": "middle",
     "question": "Что такое триггер (TRIGGER) в SQL?",
     "answer": "Код, который автоматически выполняется при INSERT/UPDATE/DELETE на таблице. Бывает BEFORE/AFTER.",
     "explanation": "CREATE TRIGGER ... BEFORE INSERT ON table FOR EACH ROW ... Полезно для аудита, валидации, поддержки денормализованных данных. Сложно отлаживать и тестировать.",
     "common_mistakes": "Злоупотреблять триггерами — логика прячется в БД, тяжело понять поток данных. Часто лучше явный код в приложении.",
     "tags": ["triggers", "automation"], "is_top": False},
    {"category": "sql", "difficulty": "middle",
     "question": "Что такое хранимая процедура (stored procedure)?",
     "answer": "Именованный блок SQL-кода, хранится в БД, вызывается по имени. Может принимать параметры и возвращать значения.",
     "explanation": "CREATE PROCEDURE name(params) AS $$ ... $$;. Преимущества: производительность (компилируется), безопасность (права на процедуру), уменьшение сетевого трафика. Минусы: vendor lock-in.",
     "common_mistakes": "Писать всю бизнес-логику в хранимых процедурах — тяжело тестировать, версионировать, деплоить.",
     "tags": ["procedures", "db"], "is_top": False},
    {"category": "sql", "difficulty": "middle",
     "question": "Что такое ACID в контексте баз данных?",
     "answer": "Atomicity, Consistency, Isolation, Durability — свойства надёжной транзакции.",
     "explanation": "Atomicity: всё или ничего. Consistency: переход из одного валидного состояния в другое. Isolation: параллельные транзакции не мешают друг другу. Durability: после COMMIT данные гарантированно сохранены.",
     "common_mistakes": "Путать ACID с BASE (Basically Available, Soft state, Eventually consistent) — это разные модели для разных систем.",
     "tags": ["transactions", "acid"], "is_top": True},
    {"category": "sql", "difficulty": "middle",
     "question": "Какие уровни изоляции транзакций бывают?",
     "answer": "READ UNCOMMITTED, READ COMMITTED, REPEATABLE READ, SERIALIZABLE — от слабого к сильному.",
     "explanation": "Каждый уровень решает проблемы: dirty reads, non-repeatable reads, phantom reads. READ COMMITTED — стандарт в PostgreSQL. SERIALIZABLE — полная изоляция, но сильно снижает параллелизм.",
     "common_mistakes": "Думать, что SERIALIZABLE всегда лучше — он снижает throughput. Выбирай минимально достаточный уровень.",
     "tags": ["transactions", "isolation"], "is_top": False},
    # ===== STATISTICS (дополнительно 14) =====
    {"category": "statistics", "difficulty": "junior",
     "question": "Что такое стандартная ошибка (standard error)?",
     "answer": "SE показывает разброс выборочного среднего. SE = std / sqrt(n).",
     "explanation": "Std описывает разброс данных, SE — разброс средних по выборкам. Уменьшается с ростом n: чтобы снизить SE в 2 раза, нужно в 4 раза больше данных.",
     "common_mistakes": "Путать std (по выборке) с SE (по среднему) — это разные величины, хотя связаны.",
     "tags": ["estimation", "variability"], "is_top": False},
    {"category": "statistics", "difficulty": "junior",
     "question": "Что такое дисперсия и среднеквадратичное отклонение?",
     "answer": "Дисперсия = средний квадрат отклонения от среднего. Std = sqrt(дисперсии).",
     "explanation": "Variance в квадрате единиц измерения, std — в исходных. Population variance делит на n, sample variance (ddof=1) — на n-1 (несмещённая оценка).",
     "common_mistakes": "Использовать ddof=0 для sample std — это смещённая оценка, занижает разброс.",
     "tags": ["descriptive", "variance"], "is_top": False},
    {"category": "statistics", "difficulty": "junior",
     "question": "Что такое нормальное распределение?",
     "answer": "Симметричное колоколообразное распределение: среднее=медиана=мода, описывается μ и σ.",
     "explanation": "Правило 68-95-99.7: ±1σ — 68%, ±2σ — 95%, ±3σ — 99.7% данных. Многие тесты (t, z) предполагают нормальность. Не все данные нормальны (доходы — логнормальные).",
     "common_mistakes": "Считать, что 'всё нормально распределено' — для асимметричных данных нужны другие методы.",
     "tags": ["distributions"], "is_top": False},
    {"category": "statistics", "difficulty": "junior",
     "question": "Что такое перцентили и квантили?",
     "answer": "Перцентиль P% — значение, ниже которого P% данных. Квантиль — общий термин, перцентиль = квантиль в процентах.",
     "explanation": "Медиана = 50-й перцентиль. Q1 = 25-й, Q3 = 75-й. Используются для понимания распределения и выбросов (Tukey fences: 1.5 * IQR).",
     "common_mistakes": "Путать P95 (95% данных ниже) с 95% доверительным интервалом — разные концепции.",
     "tags": ["descriptive", "percentiles"], "is_top": False},
    {"category": "statistics", "difficulty": "junior",
     "question": "Что такое IQR (interquartile range)?",
     "answer": "IQR = Q3 - Q1 — разница между 75-м и 25-м перцентилями. Устойчив к выбросам.",
     "explanation": "Box plot: Q1, медиана, Q3, усы = Q1 - 1.5*IQR и Q3 + 1.5*IQR. Всё за усами — кандидаты в выбросы. Полезен для асимметричных распределений.",
     "common_mistakes": "Использовать std вместо IQR для данных с выбросами — std сильно искажается экстремумами.",
     "tags": ["descriptive", "spread"], "is_top": False},
    {"category": "statistics", "difficulty": "junior",
     "question": "Что такое z-score (стандартизация)?",
     "answer": "Z = (x - mean) / std. Показывает, на сколько std значение отклоняется от среднего.",
     "explanation": "Z=0 — на среднем, Z=2 — выше на 2 std. Для нормального распределения: |z|>3 — редко (0.3%). Используется для выбросов, нормализации фичей, проверки гипотез.",
     "common_mistakes": "Применять к не-нормальным данным без проверки — распределение z-score тоже будет ненормальным.",
     "tags": ["z-score", "standardization"], "is_top": False},
    {"category": "statistics", "difficulty": "junior",
     "question": "Что такое skewness (асимметрия) распределения?",
     "answer": "Мера асимметрии: 0 = симметричное, >0 = хвост вправо, <0 = хвост влево.",
     "explanation": "Положительная skewness: среднее > медианы (доходы, время сессии). Отрицательная: время реакции. |skew|>1 — сильная асимметрия, нужны непараметрические методы или трансформация (log).",
     "common_mistakes": "Игнорировать skewness при выборе метода — t-тест и линейная регрессия предполагают симметрию.",
     "tags": ["distributions", "shape"], "is_top": False},
    {"category": "statistics", "difficulty": "junior",
     "question": "Что такое kurtosis (эксцесс)?",
     "answer": "Мера 'тяжести хвостов': 0 = нормальное, >0 = тяжёлые хвосты, <0 = лёгкие хвосты.",
     "explanation": "Высокий kurtosis = больше экстремальных значений, чем у нормального. Excess kurtosis = kurtosis - 3. Используется для оценки рисков (финансы) и выявления аномалий.",
     "common_mistakes": "Путать kurtosis с peakness — на самом деле он измеряет хвосты, а не пик распределения.",
     "tags": ["distributions", "shape"], "is_top": False},
    {"category": "statistics", "difficulty": "middle",
     "question": "Что такое Type I и Type II ошибки?",
     "answer": "Type I (α): отвергли верную H0 (ложный positive). Type II (β): приняли ложную H0 (ложный negative).",
     "explanation": "Пример: лекарство не работает (H0 верна), а мы отвергли H0 (Type I). Мощность теста = 1 - β. Компромисс: снижая α, увеличиваем β (нужен бóльший эффект или выборка).",
     "common_mistakes": "Думать, что p-value = вероятность Type I — это другая концепция (p при условии H0).",
     "tags": ["hypothesis-testing", "errors"], "is_top": True},
    {"category": "statistics", "difficulty": "middle",
     "question": "Как определить необходимый размер выборки?",
     "answer": "Зависит от: желаемой мощности (обычно 0.8), уровня значимости (0.05), ожидаемого эффекта, дисперсии.",
     "explanation": "Больший эффект → меньше выборка. Для t-теста: n = 2 * (z_α/2 + z_β)² * σ² / δ². Используют statsmodels.stats.power или онлайн-калькуляторы.",
     "common_mistakes": "Собирать данные 'на глаз' — потом окажется, что мощности не хватает, эксперимент бесполезен.",
     "tags": ["power-analysis", "sample-size"], "is_top": False},
    {"category": "statistics", "difficulty": "middle",
     "question": "Что такое множественная проверка гипотез (multiple testing)?",
     "answer": "Проблема: при 20 тестах с α=0.05 хотя бы 1 ложный positive ожидается даже без реальных эффектов.",
     "explanation": "Family-wise error rate (FWER) растёт с числом тестов. Коррекции: Bonferroni (α/k), Holm, Benjamini-Hochberg (FDR). Для 20 тестов с α=0.05: FWER ≈ 64%.",
     "common_mistakes": "Игнорировать проблему — ложные открытия в исследованиях ('replication crisis' в психологии).",
     "tags": ["multiple-testing"], "is_top": False},
    {"category": "statistics", "difficulty": "middle",
     "question": "Что такое поправка Бонферрони (Bonferroni)?",
     "answer": "Делим α на число тестов: новый α' = α / k. Строгая, но консервативная коррекция для FWER.",
     "explanation": "Проста в применении, контролирует FWER. Минус: сильно снижает мощность, много пропускает. Альтернативы: Holm (менее строгая), BH (контролирует FDR, лучше для exploration).",
     "common_mistakes": "Применять ко всем тестам сразу — для зависимых тестов слишком строго.",
     "tags": ["correction", "multiple-testing"], "is_top": False},
    {"category": "statistics", "difficulty": "middle",
     "question": "Что такое bootstrap?",
     "answer": "Метод оценки распределения статистики через повторные выборки с возвращением из исходной.",
     "explanation": "B выборок размера n с возвращением → вычисляем статистику на каждой → получаем распределение. Полезен, когда теория не даёт CI. 10000 бутстрап-выборок → 2.5% и 97.5% квантили = 95% CI.",
     "common_mistakes": "Думать, что bootstrap создаёт 'новые данные' — он лишь перекомпонует существующие.",
     "tags": ["resampling", "bootstrap"], "is_top": False},
    {"category": "statistics", "difficulty": "middle",
     "question": "В чём разница между байесовским и частотным подходами?",
     "answer": "Частотный: вероятность = доля в бесконечных повторениях. Байесовский: вероятность = степень уверенности, обновляется через формулу Байеса.",
     "explanation": "P(A|B) = P(B|A) * P(A) / P(B). Байесовский: prior + data → posterior. Частотный: p-value, CI. Байесовский позволяет инкорпорировать prior knowledge, но выбор prior субъективен.",
     "common_mistakes": "Думать, что один 'лучше' другого — это разные философии, выбор зависит от задачи и контекста.",
     "tags": ["bayes", "frequentist"], "is_top": False},
    # ===== ML (дополнительно 19) =====
    {"category": "ml", "difficulty": "junior",
     "question": "Что такое learning rate?",
     "answer": "Шаг градиентного спуска: насколько сильно обновляем веса за итерацию. Большой — расходится, маленький — медленно.",
     "explanation": "lr — гиперпараметр. Типичные значения: 0.1, 0.01, 0.001. Подбирается через grid/random search или scheduler (exponential decay, cosine annealing).",
     "common_mistakes": "Ставить lr=0.01 для всех задач — оптимальное значение зависит от масштаба градиентов и архитектуры.",
     "tags": ["optimization", "hyperparameters"], "is_top": True},
    {"category": "ml", "difficulty": "junior",
     "question": "Какие метрики регрессии ты знаешь?",
     "answer": "MAE (средний модуль ошибки), MSE (средний квадрат), RMSE (sqrt MSE), R² (доля объяснённой дисперсии).",
     "explanation": "MAE в исходных единицах, устойчив к выбросам. MSE сильнее штрафует большие ошибки. R² ∈ (-∞, 1], 1 = идеально, 0 = константный прогноз. MAPE — в процентах.",
     "common_mistakes": "Использовать RMSE на данных с выбросами — лучше MAE. R² не говорит о пригодности модели без контекста.",
     "tags": ["metrics", "regression"], "is_top": False},
    {"category": "ml", "difficulty": "junior",
     "question": "Какие метрики классификации ты знаешь?",
     "answer": "Accuracy, Precision, Recall, F1, ROC-AUC, PR-AUC, log loss, Cohen's kappa.",
     "explanation": "Accuracy плох при дисбалансе. Precision — 'из предсказанных positive сколько правильных'. Recall — 'из реальных positive сколько нашли'. F1 — гармоническое среднее P и R.",
     "common_mistakes": "Гнаться за accuracy на дисбалансе — 99% класс 0 даёт 99% accuracy при бесполезной модели.",
     "tags": ["metrics", "classification"], "is_top": False},
    {"category": "ml", "difficulty": "junior",
     "question": "Что такое confusion matrix?",
     "answer": "Таблица 2x2: TP, FP, FN, TN. Показывает, где именно модель ошибается.",
     "explanation": "TP — верно предсказан positive. FP — ошибочно предсказан positive (ложная тревога). FN — пропущен positive. TN — верно отвергнут negative. Из неё выводят precision, recall, specificity.",
     "common_mistakes": "Смотреть только на accuracy — confusion matrix покажет, какой тип ошибок преобладает.",
     "tags": ["metrics", "classification"], "is_top": False},
    {"category": "ml", "difficulty": "junior",
     "question": "Что такое линейная регрессия простыми словами?",
     "answer": "Модель: y = w1*x1 + w2*x2 + ... + b. Находит w, минимизируя MSE.",
     "explanation": "Закрытая формула (normal equation) для маленьких данных, градиентный спуск для больших. Предполагает линейность связи, независимость ошибок, гомоскедастичность, нормальность остатков.",
     "common_mistakes": "Применять без проверки предположений — остатки (residuals) должны быть нормальны и гомоскедастичны.",
     "tags": ["regression", "linear"], "is_top": False},
    {"category": "ml", "difficulty": "junior",
     "question": "Как работает дерево решений?",
     "answer": "Жадное разбиение пространства признаков: на каждом шаге выбираем признак и порог, максимизирующие информационный выигрыш.",
     "explanation": "Критерии: Gini, entropy. Легко интерпретируется. Подвержен переобучению (max_depth ограничивает). Основа для RF и GBM. Для категориальных — порядок важен.",
     "common_mistakes": "Использовать дерево большой глубины без ограничений — переобучается. Нужно max_depth, min_samples_leaf.",
     "tags": ["trees", "classification"], "is_top": False},
    {"category": "ml", "difficulty": "junior",
     "question": "Что такое k-Nearest Neighbors (kNN)?",
     "answer": "Ленивый классификатор: предсказывает класс по k ближайшим соседям (большинство голосов / среднее).",
     "explanation": "Не учит модель, хранит все данные. Метрика расстояния: Евклидова, Манхэттенская, косинусная. Чувствителен к масштабу (нормализация обязательна), медленный на больших данных.",
     "common_mistakes": "Забыть нормализовать — один признак с большим масштабом будет доминировать в расстоянии.",
     "tags": ["classification", "lazy"], "is_top": False},
    {"category": "ml", "difficulty": "junior",
     "question": "Что такое Naive Bayes?",
     "answer": "Вероятностный классификатор на основе теоремы Байеса с наивным предположением независимости признаков.",
     "explanation": "P(y|X) ∝ P(y) * ∏ P(xi|y). Быстрый, работает на маленьких данных, хорош для текстов (MultinomialNB). Наивное предположение редко верно, но часто работает на практике.",
     "common_mistakes": "Применять к сильно коррелированным признакам — предположение независимости нарушается, точность падает.",
     "tags": ["classification", "probabilistic"], "is_top": False},
    {"category": "ml", "difficulty": "junior",
     "question": "Что такое SVM (Support Vector Machine)?",
     "answer": "Находит гиперплоскость, максимально разделяющую классы. Опорные векторы — ближайшие к границе точки.",
     "explanation": "Kernel trick: линейное разделение в высокоразмерном пространстве (RBF, polynomial). Хорошо на маленьких выборках, плохо на больших (O(n²)-O(n³)). Чувствителен к масштабу.",
     "common_mistakes": "Применять к большим датасетам без нормализации — будет медленно и плохо работать.",
     "tags": ["classification", "svm"], "is_top": False},
    {"category": "ml", "difficulty": "junior",
     "question": "Что такое ансамбли (ensembles) в ML?",
     "answer": "Комбинация нескольких моделей для улучшения качества. Бэггинг, бустинг, стекинг.",
     "explanation": "Бэггинг: независимые модели на случайных подвыборках (RF). Бустинг: последовательные модели исправляют ошибки предыдущих (XGBoost). Стекинг: meta-модель на предсказаниях базовых.",
     "common_mistakes": "Думать, что чем больше моделей — тем лучше — без diversity (разнообразия) ансамбль не работает.",
     "tags": ["ensembles", "meta"], "is_top": False},
    {"category": "ml", "difficulty": "junior",
     "question": "Какие виды кросс-валидации бывают?",
     "answer": "K-fold, Stratified K-fold (для дисбаланса), Leave-One-Out, Time Series Split (для временных рядов).",
     "explanation": "K-fold: делим на K частей, каждая по очереди — test. Stratified сохраняет распределение классов. Time Series: train на прошлом, test на будущем (нельзя перемешивать!).",
     "common_mistakes": "Использовать K-fold на временных рядах — утечка данных из будущего в прошлое.",
     "tags": ["validation", "cross-validation"], "is_top": False},
    {"category": "ml", "difficulty": "junior",
     "question": "Что такое полиномиальные признаки?",
     "answer": "Добавление степеней и взаимодействий признаков: x1², x1*x2, x2² для degree=2.",
     "explanation": "Позволяет линейной регрессии моделировать нелинейные зависимости. Минус: degree=10 → 1000+ признаков на 10 фичей, переобучение. Лучше: ограничить взаимодействия или добавить регуляризацию.",
     "common_mistakes": "Применять degree > 2 без регуляризации — взрыв размерности и переобучение.",
     "tags": ["features", "engineering"], "is_top": False},
    {"category": "ml", "difficulty": "middle",
     "question": "В чём разница между L1 и L2 регуляризацией?",
     "answer": "L1 (Lasso) добавляет |w|, зануляет веса (отбор признаков). L2 (Ridge) добавляет w², уменьшает веса, но не зануляет.",
     "explanation": "L1 даёт разреженные решения, L2 — гладкие. Elastic Net = L1 + L2. Для отбора признаков — L1. Для борьбы с мультиколлинеарностью — L2. Геометрия: L1 — ромб, L2 — круг.",
     "common_mistakes": "Применять L1, когда все признаки нужны — занулятся неправильные. Сначала посмотри важность.",
     "tags": ["regularization", "selection"], "is_top": True},
    {"category": "ml", "difficulty": "middle",
     "question": "Что такое градиентный бустинг? (XGBoost, LightGBM, CatBoost)",
     "answer": "Ансамбль слабых моделей (обычно деревьев), где каждая следующая исправляет ошибки предыдущей через градиент loss.",
     "explanation": "XGBoost: регуляризация, второй порядок градиента. LightGBM: histogram-based, leaf-wise рост. CatBoost: умеет с категориальными из коробки. Лидер Kaggle-соревнований по табличным данным.",
     "common_mistakes": "Использовать без подбора гиперпараметров — дефолты не оптимальны для конкретной задачи.",
     "tags": ["boosting", "ensembles"], "is_top": True},
    {"category": "ml", "difficulty": "middle",
     "question": "Чем bagging отличается от boosting?",
     "answer": "Bagging: модели параллельно на случайных подвыборках, результат усредняется. Boosting: последовательно, каждая модель исправляет ошибки предыдущей.",
     "explanation": "Bagging снижает variance (RF). Boosting снижает bias, но может переобучаться. Bagging более устойчив к шуму. Out-of-bag (OOB) оценка — бесплатная валидация в bagging.",
     "common_mistakes": "Думать, что boosting всегда лучше — на шумных данных bagging стабильнее и проще в настройке.",
     "tags": ["ensembles", "bagging-boosting"], "is_top": True},
    {"category": "ml", "difficulty": "middle",
     "question": "Как работает Random Forest под капотом?",
     "answer": "Много деревьев, каждое на bootstrap-выборке + случайном подмножестве признаков. Финальное предсказание — голосование (класс) или среднее (регрессия).",
     "explanation": "Bootstrap: выборка с возвращением (≈63% уникальных). max_features='sqrt' — типичный выбор. OOB-данные — для оценки качества без отдельного val. Параллелится по деревьям.",
     "common_mistakes": "Думать, что RF не переобучается — при большой глубине деревьев и шуме может переобучаться.",
     "tags": ["random-forest", "ensembles"], "is_top": False},
    {"category": "ml", "difficulty": "middle",
     "question": "Чем отличаются оптимизаторы Adam, RMSprop и SGD?",
     "answer": "SGD: простой градиент. RMSprop: адаптивный lr по скользящему среднему квадрата градиента. Adam: RMSprop + momentum (1-й и 2-й моменты).",
     "explanation": "Adam — стандарт для нейросетей. SGD+momentum часто лучше для финальной сходимости и генерализации. AdamW — Adam с decoupled weight decay (для трансформеров).",
     "common_mistakes": "Всегда использовать Adam — для некоторых задач SGD с momentum даёт лучшую генерализацию.",
     "tags": ["optimization", "deep-learning"], "is_top": False},
    {"category": "ml", "difficulty": "middle",
     "question": "Что такое early stopping?",
     "answer": "Остановка обучения, когда validation loss перестаёт улучшаться. Защищает от переобучения.",
     "explanation": "patience — сколько эпох ждать улучшения. Сохраняется лучшая модель (save_best). В Keras: EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True).",
     "common_mistakes": "Мониторить только train loss — переобучение не видно. Нужен validation. И не путать с lr scheduler.",
     "tags": ["regularization", "training"], "is_top": False},
    {"category": "ml", "difficulty": "middle",
     "question": "Как работать с дисбалансом классов в ML?",
     "answer": "Метрики (F1, AUC, не accuracy), class_weight='balanced', oversampling (SMOTE), undersampling, threshold tuning.",
     "explanation": "SMOTE: синтетические minority примеры через интерполяцию соседей. Undersampling: удаляем часть majority. Threshold tuning: сдвигаем порог вероятности под бизнес-требования (recall vs precision).",
     "common_mistakes": "Oversampling до train/test split — leak. SMOTE только на train части!",
     "tags": ["imbalance", "preprocessing"], "is_top": True},
    # ===== DS GENERAL (дополнительно 10) =====
    {"category": "ds_general", "difficulty": "junior",
     "question": "В чём разница между ETL и ELT?",
     "answer": "ETL: Extract, Transform, Load — трансформируем до загрузки в хранилище. ELT: Extract, Load, Transform — грузим сырые данные, трансформируем в хранилище.",
     "explanation": "ETL для структурированных данных (legacy DWH). ELT популярен с BigQuery/Snowflake — вычислительная мощность в хранилище. ELT гибче: можно трансформировать по-разному под разные задачи.",
     "common_mistakes": "Думать, что это синонимы — порядок шагов критичен для архитектуры pipeline.",
     "tags": ["data-engineering", "pipeline"], "is_top": False},
    {"category": "ds_general", "difficulty": "junior",
     "question": "Чем Data Lake отличается от Data Warehouse?",
     "answer": "Data Lake: сырые данные любого формата (S3, HDFS). Data Warehouse: очищенные, структурированные, schema-on-write (Redshift, BigQuery).",
     "explanation": "Lake: schema-on-read, дёшево, подходит для ML и exploration. Warehouse: schema-on-write, ACID, быстрые аналитические запросы. Data Lakehouse (Delta, Iceberg) — гибрид с лучшим из обоих.",
     "common_mistakes": "Использовать Lake для отчётности — без структуры запросы медленные. Warehouse для ML — дорого хранить сырые данные.",
     "tags": ["data-engineering", "storage"], "is_top": False},
    {"category": "ds_general", "difficulty": "junior",
     "question": "Что такое A/B тест с точки зрения Data Science?",
     "answer": "Эксперимент: случайно делим пользователей на группы, меняем одну переменную, измеряем метрику, проверяем статистическую значимость.",
     "explanation": "Требования: рандомизация, контроль, достаточная выборка, заранее определённые метрики. DS отвечает за дизайн, расчёт мощности, анализ результатов (p-value, effect size, CI).",
     "common_mistakes": "Подглядывать в данные до конца эксперимента — invalidates p-value. Stopping early при 'значимости' — растёт Type I error.",
     "tags": ["ab-testing", "experiments"], "is_top": False},
    {"category": "ds_general", "difficulty": "junior",
     "question": "Что такое методология CRISP-DM?",
     "answer": "Cross-Industry Standard Process for Data Mining — 6 фаз: Business Understanding, Data Understanding, Data Preparation, Modeling, Evaluation, Deployment.",
     "explanation": "Итеративный цикл — после Deployment часто возвращаются к Business Understanding. Стандарт индустрии для структурирования DS-проектов. Альтернативы: KDD, OSEMN, Microsoft TDSP.",
     "common_mistakes": "Пропускать Business Understanding — без понимания задачи делаем ненужную работу.",
     "tags": ["process", "methodology"], "is_top": False},
    {"category": "ds_general", "difficulty": "junior",
     "question": "Какие бывают типы данных в Data Science?",
     "answer": "Структурированные (таблицы), полу-структурированные (JSON, XML), неструктурированные (текст, изображения, видео).",
     "explanation": "Структурированные: SQL-таблицы, CSV. Полу: логи, API-ответы. Неструктурированные: 80% корпоративных данных. По типу значений: числовые (дискретные/непрерывные), категориальные (номинальные/порядковые), временные, текстовые.",
     "common_mistakes": "Обращаться с категориальными как с числовыми — модель не поймёт порядок/расстояние.",
     "tags": ["data-types", "basics"], "is_top": False},
    {"category": "ds_general", "difficulty": "middle",
     "question": "Как оформить DS-проект для портфолио?",
     "answer": "README с задачей и результатом, чистый код (модули, type hints), Jupyter + скрипты, requirements.txt, воспроизводимость (seeds, версии), визуализации, бизнес-выводы.",
     "explanation": "Структура: data/, notebooks/, src/, models/, README.md. Что в README: проблема, данные (источник, размер), EDA выводы, модель, метрики, как запустить, что узнал. Хорошо — с дашбордом или статьёй.",
     "common_mistakes": "Класть 10 невнятных ноутбуков — лучше один глубокий проект с чёткой структурой и понятной историей.",
     "tags": ["portfolio", "career"], "is_top": False},
    {"category": "ds_general", "difficulty": "middle",
     "question": "Как презентовать результаты DS-проекта заказчику?",
     "answer": "Структура: контекст → проблема → подход → результаты → рекомендации → следующие шаги. Язык бизнеса, не техники.",
     "explanation": "Избегай 'мы обучили XGBoost' — скажи 'модель выявляет 80% проблемных клиентов с точностью 70%'. Используй визуализации, единицы измерения (₽, %), бенчмарки. Ожидай вопросы про edge cases.",
     "common_mistakes": "Сразу показывать код и графики — заказчик хочет понять, как это поможет бизнесу.",
     "tags": ["communication", "business"], "is_top": False},
    {"category": "ds_general", "difficulty": "middle",
     "question": "Как определить метрики успеха DS-проекта?",
     "answer": "Связать с бизнес-метриками: retention, ARPU, конверсия, ROI. Технические метрики (F1, RMSE) — прокси.",
     "explanation": "Пример: рекомендательная система — offline метрика NDCG ≠ uplift продаж. Онлайн-эксперимент (A/B) — единственный способ проверить реальный эффект. Leading vs lagging индикаторы.",
     "common_mistakes": "Зацикливаться на offline-метриках — красивый NDCG не означает рост выручки.",
     "tags": ["metrics", "business"], "is_top": False},
    {"category": "ds_general", "difficulty": "middle",
     "question": "Как работать со стейкхолдерами в DS-проекте?",
     "answer": "Регулярные синки, управление ожиданиями, согласование метрик, документирование решений, обсуждение ограничений.",
     "explanation": "Типичные стейкхолдеры: бизнес-заказчик, продукт, инженеры, аналитики, юристы. Важно: сначала понять проблему ('что мы решаем'), потом — успех ('как поймём, что решили').",
     "common_mistakes": "Уйти в 'pure' data science и не синхронизироваться — потом окажется, что задача другая.",
     "tags": ["communication", "process"], "is_top": False},
    {"category": "ds_general", "difficulty": "middle",
     "question": "Как оценить качество данных перед началом проекта?",
     "answer": "6 измерений: Completeness (пропуски), Consistency (конфликты), Accuracy (верность), Timeliness (свежесть), Uniqueness (дубликаты), Validity (формат).",
     "explanation": "Профилирование: pandas-profiling, Great Expectations. Data Quality SLA: % пропусков не выше X, latency < Y часов. 'Garbage in — garbage out' — плохие данные = плохая модель.",
     "common_mistakes": "Пропустить data quality — обнаружим в середине проекта, потеряем недели.",
     "tags": ["data-quality", "preprocessing"], "is_top": False},
]
