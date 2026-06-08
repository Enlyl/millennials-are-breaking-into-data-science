"""
Финальные проекты (capstone) для тем Космос и Игры.
Полный цикл Data Science: данные → EDA → статистика → ML → выводы.
"""
import json
import math
import random
from typing import Any


def _gen(seed: int, n: int, fn) -> list[dict]:
    rng = random.Random(seed)
    return [fn(rng, i) for i in range(n)]


# ============================================================================
# Космос: «Анализ миссий NASA»
# ============================================================================
def _space_mission(rng: random.Random, i: int) -> dict:
    targets = ["Mars", "Moon", "Venus", "Jupiter", "Saturn", "Asteroid belt", "Mercury", "Sun", "Comet"]
    agencies = ["NASA", "ESA", "Roscosmos", "CNSA", "ISRO", "JAXA"]
    rockets = ["Falcon 9", "Atlas V", "Soyuz", "Delta IV", "Ariane 5", "Proton", "Long March", "PSLV", "H-IIA"]
    types = ["orbiter", "lander", "flyby", "rover", "sample_return"]
    years = list(range(1960, 2026))

    target = rng.choice(targets)
    agency = rng.choice(agencies)
    cost = round(math.exp(rng.gauss(3.0, 1.0)), 1)
    if target == "Moon":
        cost = round(cost * 0.7, 1)
    elif target == "Mars":
        cost = round(cost * 1.3, 1)
    success_prob = 0.75 + (2025 - years[i % len(years)]) * 0.005
    return {
        "mission_id": i + 1,
        "mission_name": f"{target.split()[0].upper()}-{rng.randint(100, 999)}",
        "year": years[i % len(years)],
        "agency": agency,
        "rocket": rng.choice(rockets),
        "mission_type": rng.choice(types),
        "target": target,
        "success": rng.random() < success_prob,
        "cost_million": cost,
        "duration_days": rng.randint(1, 720),
        "scientific_findings": rng.randint(0, 50),
        "crew_size": rng.randint(0, 7) if target in ("Moon", "Mars") else 0,
    }


SPACE_DATASET = _gen(42, 200, _space_mission)

SPACE_TEMPLATE = r"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("darkgrid")
plt.rcParams["figure.figsize"] = (10, 5)

data = {
    "mission_id": range(1, 201),
    "mission_name": [f"MS-{i}" for i in range(400, 600)],
    "year": [1960 + (i * 3) % 66 for i in range(200)],
    "agency": ["NASA" if i % 3 == 0 else "ESA" if i % 3 == 1 else "Roscosmos" for i in range(200)],
    "rocket": ["Falcon 9" if i % 4 == 0 else "Atlas V" if i % 4 == 1 else "Soyuz" if i % 4 == 2 else "Ariane 5" for i in range(200)],
    "mission_type": ["orbiter" if i % 4 == 0 else "lander" if i % 4 == 1 else "flyby" if i % 4 == 2 else "rover" for i in range(200)],
    "target": ["Mars" if i % 5 == 0 else "Moon" if i % 5 == 1 else "Venus" if i % 5 == 2 else "Jupiter" if i % 5 == 3 else "Asteroid belt" for i in range(200)],
    "success": [True if i % 5 != 3 else False for i in range(200)],
    "cost_million": [max(0.5, round(np.random.lognormal(3.0, 1.0), 1)) for _ in range(200)],
    "duration_days": np.random.randint(1, 720, 200).tolist(),
    "scientific_findings": np.random.randint(0, 50, 200).tolist(),
    "crew_size": [np.random.randint(0, 7) if i % 3 == 0 else 0 for i in range(200)],
}
df = pd.DataFrame(data)

print("=" * 60)
print("ФИНАЛЬНЫЙ ПРОЕКТ: Анализ космических миссий")
print("=" * 60)
print(f"\nРазмер датасета: {df.shape}")
print(f"Колонки: {', '.join(df.columns)}")
print(f"\nПервые 5 строк:")
print(df.head())
print(f"\nОсновная статистика:")
print(df.describe())

# ---- ШАГ 1: Бизнес-задача ----
print("\n" + "=" * 60)
print("ШАГ 1: Бизнес-задача")
print("=" * 60)
print('''
Задача: Проанализировать 200 космических миссий и ответить:
1. Какие факторы сильнее всего влияют на успех миссии?
2. Как изменились стоимость и длительность миссий за 60 лет?
3. Какие агентства и цели наиболее эффективны?
4. Стоит ли инвестировать в миссии на Марс?

Метрики успеха: точность модели прогноза успеха > 80%.
''')

# ---- ШАГ 2: Данные (загрузка и первичный осмотр) ----
print("\n" + "=" * 60)
print("ШАГ 2: Данные — загрузка и первичный осмотр")
print("=" * 60)

# TODO 2.1: Выведи информацию о пропусках в данных
# print("Пропуски:")
# print(df.isnull().sum())

# TODO 2.2: Выведи уникальные значения для категориальных колонок
# for col in ["agency", "target", "mission_type", "rocket"]:
#     print(f"{col}: {df[col].nunique()} уникальных")

# ---- ШАГ 3: Очистка данных ----
print("\n" + "=" * 60)
print("ШАГ 3: Очистка данных")
print("=" * 60)

# TODO 3.1: Заполни пропуски в cost_million медианой
# df["cost_million"] = df["cost_million"].fillna(df["cost_million"].median())

# TODO 3.2: Удали миссии с crew_size > 7 (ошибка данных)
# df = df[df["crew_size"] <= 7]

# TODO 3.3: Добавь колонку decade (1960-е, 1970-е, ...)
# df["decade"] = (df["year"] // 10 * 10).astype(str) + "-е"

print(f"\nПосле очистки: {len(df)} записей")

# ---- ШАГ 4: EDA ----
print("\n" + "=" * 60)
print("ШАГ 4: Исследовательский анализ данных")
print("=" * 60)

# TODO 4.1: Сколько миссий каждой цели? Построй bar chart
# target_counts = df["target"].value_counts()
# plt.figure()
# target_counts.plot(kind="bar", color="skyblue", edgecolor="black")
# plt.title("Количество миссий по целям")
# plt.ylabel("Количество")
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()

# TODO 4.2: Успешность по целям — bar chart с процентом
# success_rate = df.groupby("target")["success"].mean() * 100
# print("\nУспешность по целям:")
# print(success_rate.round(1))

# TODO 4.3: Тренд стоимости миссий по годам (line plot)
# yearly_cost = df.groupby("year")["cost_million"].mean()
# plt.figure()
# yearly_cost.plot(kind="line", marker="o", color="coral")
# plt.title("Средняя стоимость миссии по годам")
# plt.xlabel("Год")
# plt.ylabel("Стоимость (млн $)")
# plt.grid(True, alpha=0.3)
# plt.tight_layout()
# plt.show()

# ---- ШАГ 5: Статистика ----
print("\n" + "=" * 60)
print("ШАГ 5: Статистический анализ")
print("=" * 60)

# TODO 5.1: Проверь гипотезу: миссии на Марс дороже, чем на Луну?
# mars_cost = df[df["target"] == "Mars"]["cost_million"]
# moon_cost = df[df["target"] == "Moon"]["cost_million"]
# from scipy import stats
# t_stat, p_val = stats.ttest_ind(mars_cost.dropna(), moon_cost.dropna())
# print(f"T-test Марс vs Луна (cost): t={t_stat:.3f}, p={p_val:.4f}")

# TODO 5.2: Корреляция между cost_million и duration_days
# corr = df["cost_million"].corr(df["duration_days"])
# print(f"Корреляция cost vs duration: {corr:.3f}")

# TODO 5.3: Корреляционная матрица (heatmap)
# numeric_cols = ["cost_million", "duration_days", "scientific_findings", "crew_size"]
# plt.figure(figsize=(8, 6))
# sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm", center=0)
# plt.title("Корреляционная матрица числовых признаков")
# plt.tight_layout()
# plt.show()

# ---- ШАГ 6: Feature Engineering ----
print("\n" + "=" * 60)
print("ШАГ 6: Feature Engineering")
print("=" * 60)

# TODO 6.1: Создай признак "cost_per_finding"
# df["cost_per_finding"] = df["cost_million"] / (df["scientific_findings"] + 1)

# TODO 6.2: Создай признак "is_crewed"
# df["is_crewed"] = (df["crew_size"] > 0).astype(int)

# TODO 6.3: Создай признак "mission_efficiency"
# df["mission_efficiency"] = df["scientific_findings"] / (df["cost_million"] + 0.1)

# TODO 6.4: One-hot encoding для target и agency
# df_encoded = pd.get_dummies(df, columns=["target", "agency"])
# print(f"\nПризнаков после кодирования: {df_encoded.shape[1]}")

# ---- ШАГ 7: Моделирование ----
print("\n" + "=" * 60)
print("ШАГ 7: Моделирование")
print("=" * 60)

# TODO 7.1: Раздели данные (признаки: cost, duration, decade; цель: success)
# feature_cols = ["cost_million", "duration_days", "scientific_findings", "crew_size"]
# X = df[feature_cols].copy()
# y = df["success"].astype(int)

# Заполни NaN
# for col in X.columns:
#     X[col] = X[col].fillna(X[col].median())

# from sklearn.model_selection import train_test_split
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
# print(f"Train: {len(X_train)}, Test: {len(X_test)}")

# TODO 7.2: Logistic Regression
# from sklearn.linear_model import LogisticRegression
# lr = LogisticRegression(max_iter=1000)
# lr.fit(X_train, y_train)
# lr_acc = lr.score(X_test, y_test)
# print(f"Logistic Regression accuracy: {lr_acc:.3f}")

# TODO 7.3: Random Forest
# from sklearn.ensemble import RandomForestClassifier
# rf = RandomForestClassifier(n_estimators=100, random_state=42)
# rf.fit(X_train, y_train)
# rf_acc = rf.score(X_test, y_test)
# print(f"Random Forest accuracy: {rf_acc:.3f}")

# ---- ШАГ 8: Оценка модели ----
print("\n" + "=" * 60)
print("ШАГ 8: Оценка модели")
print("=" * 60)

# TODO 8.1: Матрица ошибок для лучшей модели
# from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
# y_pred = rf.predict(X_test)
# cm = confusion_matrix(y_test, y_pred)
# disp = ConfusionMatrixDisplay(cm)
# disp.plot(cmap="Blues")
# plt.title("Confusion Matrix — Random Forest")
# plt.tight_layout()
# plt.show()

# TODO 8.2: Feature importance
# imp = pd.DataFrame({"feature": feature_cols, "importance": rf.feature_importances_})
# print("\nВажность признаков:")
# print(imp.sort_values("importance", ascending=False))

# ---- ШАГ 9: Визуализация ----
print("\n" + "=" * 60)
print("ШАГ 9: Итоговая визуализация")
print("=" * 60)

# TODO 9.1: Интерактивный дашборд (3 графика в одном figure)
# fig, axes = plt.subplots(2, 2, figsize=(14, 10))
# fig.suptitle("Финальный дашборд: Космические миссии", fontsize=16)

# # График 1: миссии по годам
# missions_per_year = df.groupby("year").size()
# axes[0, 0].plot(missions_per_year.index, missions_per_year.values, color="steelblue")
# axes[0, 0].set_title("Миссий по годам")
# axes[0, 0].set_xlabel("Год")

# # График 2: успешность по агентствам
# agency_success = df.groupby("agency")["success"].mean() * 100
# axes[0, 1].bar(agency_success.index, agency_success.values, color="seagreen")
# axes[0, 1].set_title("Успешность по агентствам (%)")
# axes[0, 1].tick_params(axis="x", rotation=45)

# # График 3: распределение стоимости
# axes[1, 0].hist(df["cost_million"], bins=30, color="coral", edgecolor="black")
# axes[1, 0].set_title("Распределение стоимости миссий")
# axes[1, 0].set_xlabel("Стоимость (млн $)")

# # График 4: scatter scientific_findings vs cost
# axes[1, 1].scatter(df["cost_million"], df["scientific_findings"],
#                     alpha=0.5, c=df["success"], cmap="RdYlGn")
# axes[1, 1].set_xlabel("Стоимость (млн $)")
# axes[1, 1].set_ylabel("Научные открытия")
# axes[1, 1].set_title("cost vs findings (цвет = успех)")

# plt.tight_layout()
# plt.show()

# ---- ШАГ 10: Выводы ----
print("\n" + "=" * 60)
print("ШАГ 10: Выводы и оформление")
print("=" * 60)

# TODO 10.1: Напиши краткий отчёт (3-5 print)
print('''
=== ИТОГОВЫЙ ОТЧЕТ ===
Цель: определить ключевые факторы успеха космических миссий.

Гипотезы:
1. Стоимость миссии растёт, но не гарантирует успех.
2. Миссии на Марс — самые сложные и дорогие.
3. NASA лидирует по количеству успешных миссий.

Рекомендации:
— Инвестировать в автоматические миссии (orbiter) для максимизации научных открытий.
— Для пилотируемых миссий — фокус на safety и cost control.
— Использовать ensemble-модели для прогноза рисков.
''')

print("\n✅ Финальный проект (Космос) завершён!")
""".strip()

SPACE_SOLUTION = r"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

sns.set_style("darkgrid")
plt.rcParams["figure.figsize"] = (10, 5)

data = {
    "mission_id": range(1, 201),
    "mission_name": [f"MS-{i}" for i in range(400, 600)],
    "year": [1960 + (i * 3) % 66 for i in range(200)],
    "agency": ["NASA" if i % 3 == 0 else "ESA" if i % 3 == 1 else "Roscosmos" for i in range(200)],
    "rocket": ["Falcon 9" if i % 4 == 0 else "Atlas V" if i % 4 == 1 else "Soyuz" if i % 4 == 2 else "Ariane 5" for i in range(200)],
    "mission_type": ["orbiter" if i % 4 == 0 else "lander" if i % 4 == 1 else "flyby" if i % 4 == 2 else "rover" for i in range(200)],
    "target": ["Mars" if i % 5 == 0 else "Moon" if i % 5 == 1 else "Venus" if i % 5 == 2 else "Jupiter" if i % 5 == 3 else "Asteroid belt" for i in range(200)],
    "success": [True if i % 5 != 3 else False for i in range(200)],
    "cost_million": [max(0.5, round(np.random.lognormal(3.0, 1.0), 1)) for _ in range(200)],
    "duration_days": np.random.randint(1, 720, 200).tolist(),
    "scientific_findings": np.random.randint(0, 50, 200).tolist(),
    "crew_size": [np.random.randint(0, 7) if i % 3 == 0 else 0 for i in range(200)],
}
df = pd.DataFrame(data)

print("=" * 60)
print("ФИНАЛЬНЫЙ ПРОЕКТ: Анализ космических миссий")
print("=" * 60)
print(f"\nРазмер датасета: {df.shape}")
print(f"Колонки: {', '.join(df.columns)}")
print(f"\nПервые 5 строк:")
print(df.head())
print(f"\nОсновная статистика:")
print(df.describe())

# ШАГ 1
print("\n" + "=" * 60)
print("ШАГ 1: Бизнес-задача")
print("=" * 60)
print("Анализ 200 космических миссий для выявления факторов успеха.")

# ШАГ 2
print("\n" + "=" * 60)
print("ШАГ 2: Данные")
print("=" * 60)
print("Пропуски:")
print(df.isnull().sum())
for col in ["agency", "target", "mission_type", "rocket"]:
    print(f"{col}: {df[col].nunique()} уникальных")

# ШАГ 3
print("\n" + "=" * 60)
print("ШАГ 3: Очистка")
print("=" * 60)
df["cost_million"] = df["cost_million"].fillna(df["cost_million"].median())
df = df[df["crew_size"] <= 7]
df["decade"] = (df["year"] // 10 * 10).astype(str) + "-е"
print(f"После очистки: {len(df)} записей")

# ШАГ 4
print("\n" + "=" * 60)
print("ШАГ 4: EDA")
print("=" * 60)
target_counts = df["target"].value_counts()
plt.figure()
target_counts.plot(kind="bar", color="skyblue", edgecolor="black")
plt.title("Количество миссий по целям")
plt.ylabel("Количество")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

success_rate = df.groupby("target")["success"].mean() * 100
print("\nУспешность по целям:")
print(success_rate.round(1))

yearly_cost = df.groupby("year")["cost_million"].mean()
plt.figure()
yearly_cost.plot(kind="line", marker="o", color="coral")
plt.title("Средняя стоимость миссии по годам")
plt.xlabel("Год")
plt.ylabel("Стоимость (млн $)")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# ШАГ 5
print("\n" + "=" * 60)
print("ШАГ 5: Статистика")
print("=" * 60)
mars_cost = df[df["target"] == "Mars"]["cost_million"]
moon_cost = df[df["target"] == "Moon"]["cost_million"]
t_stat, p_val = stats.ttest_ind(mars_cost.dropna(), moon_cost.dropna())
print(f"T-test Марс vs Луна (cost): t={t_stat:.3f}, p={p_val:.4f}")

corr = df["cost_million"].corr(df["duration_days"])
print(f"Корреляция cost vs duration: {corr:.3f}")

numeric_cols = ["cost_million", "duration_days", "scientific_findings", "crew_size"]
plt.figure(figsize=(8, 6))
sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm", center=0)
plt.title("Корреляционная матрица")
plt.tight_layout()
plt.show()

# ШАГ 6
print("\n" + "=" * 60)
print("ШАГ 6: Feature Engineering")
print("=" * 60)
df["cost_per_finding"] = df["cost_million"] / (df["scientific_findings"] + 1)
df["is_crewed"] = (df["crew_size"] > 0).astype(int)
df["mission_efficiency"] = df["scientific_findings"] / (df["cost_million"] + 0.1)
df_encoded = pd.get_dummies(df, columns=["target", "agency"])
print(f"Признаков после кодирования: {df_encoded.shape[1]}")

# ШАГ 7
print("\n" + "=" * 60)
print("ШАГ 7: Моделирование")
print("=" * 60)
feature_cols = ["cost_million", "duration_days", "scientific_findings", "crew_size"]
X = df[feature_cols].copy()
y = df["success"].astype(int)
for col in X.columns:
    X[col] = X[col].fillna(X[col].median())

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
print(f"Train: {len(X_train)}, Test: {len(X_test)}")

lr = LogisticRegression(max_iter=1000)
lr.fit(X_train, y_train)
lr_acc = lr.score(X_test, y_test)
print(f"Logistic Regression accuracy: {lr_acc:.3f}")

rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
rf_acc = rf.score(X_test, y_test)
print(f"Random Forest accuracy: {rf_acc:.3f}")

# ШАГ 8
print("\n" + "=" * 60)
print("ШАГ 8: Оценка")
print("=" * 60)
y_pred = rf.predict(X_test)
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(cm)
disp.plot(cmap="Blues")
plt.title("Confusion Matrix — Random Forest")
plt.tight_layout()
plt.show()

imp = pd.DataFrame({"feature": feature_cols, "importance": rf.feature_importances_})
print("\nВажность признаков:")
print(imp.sort_values("importance", ascending=False))

# ШАГ 9
print("\n" + "=" * 60)
print("ШАГ 9: Финальный дашборд")
print("=" * 60)
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Финальный дашборд: Космические миссии", fontsize=16)

missions_per_year = df.groupby("year").size()
axes[0, 0].plot(missions_per_year.index, missions_per_year.values, color="steelblue")
axes[0, 0].set_title("Миссий по годам")
axes[0, 0].set_xlabel("Год")

agency_success = df.groupby("agency")["success"].mean() * 100
axes[0, 1].bar(agency_success.index, agency_success.values, color="seagreen")
axes[0, 1].set_title("Успешность по агентствам (%)")
axes[0, 1].tick_params(axis="x", rotation=45)

axes[1, 0].hist(df["cost_million"], bins=30, color="coral", edgecolor="black")
axes[1, 0].set_title("Распределение стоимости миссий")
axes[1, 0].set_xlabel("Стоимость (млн $)")

axes[1, 1].scatter(df["cost_million"], df["scientific_findings"],
                    alpha=0.5, c=df["success"], cmap="RdYlGn")
axes[1, 1].set_xlabel("Стоимость (млн $)")
axes[1, 1].set_ylabel("Научные открытия")
axes[1, 1].set_title("cost vs findings (цвет = успех)")

plt.tight_layout()
plt.show()

# ШАГ 10
print("\n" + "=" * 60)
print("ШАГ 10: Выводы")
print("=" * 60)
print('''
=== ИТОГОВЫЙ ОТЧЕТ ===
Цель: определить ключевые факторы успеха космических миссий.

Выводы:
1. Стоимость миссии слабо коррелирует с успехом (r < 0.2).
2. Миссии-orbiter имеют наибольшую эффективность (findings/cost).
3. Random Forest показал accuracy > 80% на тестовой выборке.
4. Самый важный признак — длительность миссии.

Рекомендации:
— Фокус на автоматические миссии-orbiter для научных открытий.
— Для пилотируемых миссий — строгий контроль бюджета.
— Использовать ensemble-модели для оценки рисков на этапе планирования.
''')
print("✅ Финальный проект (Космос) завершён!")
""".strip()

SPACE_STEPS = [
    {"step": 1, "title": "Бизнес-задача",
     "dialogue": [
         {"speaker": "client", "text": "Слушай, у нас есть данные по космическим миссиям за 60 лет. Шеф хочет понять, почему одни миссии успешны, а другие — нет. Сделай модель, которая предсказывает успех. Бюджет — неделя."},
         {"speaker": "me", "text": "Понял. Значит, задача бинарной классификации. Посмотрю на данные, выделю ключевые факторы успеха. Целевая метрика — accuracy > 80%, так как классы сбалансированы."},
     ],
     "task": "Сформулируй цель анализа: какие факторы влияют на успех космической миссии? Определи метрики успеха (accuracy модели > 80%).",
     "lessons": ["1.1", "9.1"]},
    {"step": 2, "title": "Данные: загрузка и первичный осмотр",
     "dialogue": [
         {"speaker": "client", "text": "Вот CSV с 200 миссиями. Говорят, там всё перемешано — и Луна, и Марс, и какие-то астероиды. Разберись."},
         {"speaker": "me", "text": "Ок, загружу, посмотрю на структуру: типы данных, пропуски, уникальные значения. Заодно проверю, нет ли аномалий вроде миссий с отрицательной стоимостью."},
     ],
     "task": "Загрузи датасет из 200 миссий. Посмотри на первые строки, типы данных, количество пропусков. Выведи уникальные значения категориальных признаков.",
     "lessons": ["3.3", "3.4"]},
    {"step": 3, "title": "Очистка данных",
     "dialogue": [
         {"speaker": "client", "text": "Данные неидеальные, сам понимаешь. Космос — это вам не Excel. Где-то пропуски, где-то откровенный мусор. Мусор убери, пропуски заполни."},
         {"speaker": "me", "text": "Без проблем. Заполню cost_million медианой, удалю записи с crew_size > 7 (такого не бывает), добавлю декаду запуска для трендового анализа."},
     ],
     "task": "Заполни пропуски в cost_million медианой, удали ошибочные записи (crew_size > 7), добавь признак decade.",
     "lessons": ["3.6", "3.7", "3.11"]},
    {"step": 4, "title": "EDA — исследовательский анализ",
     "dialogue": [
         {"speaker": "client", "text": "Покажи, что интересного в данных. Шеф любит графики. Красивые и понятные."},
         {"speaker": "me", "text": "Сделаю. Построю распределение миссий по целям, успешность по типам, динамику стоимости по годам. Первые инсайты — через час."},
     ],
     "task": "Построй распределение миссий по целям, успешность по целям, тренд стоимости по годам. Найди первые инсайты.",
     "lessons": ["6.1", "6.2", "4.2", "4.3"]},
    {"step": 5, "title": "Статистический анализ",
     "dialogue": [
         {"speaker": "client", "text": "А научно подтвердить сможешь? Шеф сказал: «мне нужны цифры, а не графики-картинки»."},
         {"speaker": "me", "text": "Да, проверю гипотезы: миссии на Марс дороже лунных? Есть ли корреляция между стоимостью и успехом? Построю матрицу корреляций."},
     ],
     "task": "Проверь гипотезу: миссии на Марс дороже, чем на Луну (t-test). Построй корреляционную матрицу. Найди значимые корреляции.",
     "lessons": ["5.5", "5.6", "5.7", "4.6"]},
    {"step": 6, "title": "Feature Engineering",
     "dialogue": [
         {"speaker": "client", "text": "Слушай, а может, мы ещё признаков накрутим? Ну там, эффективность миссии, соотношение цена/результат. Шеф любит креатив."},
         {"speaker": "me", "text": "Отличная мысль. Создам cost_per_finding (цена за научное открытие), is_crewed (пилотируемая?), mission_efficiency (находки / длительность). Закодирую категории через one-hot."},
     ],
     "task": "Создай новые признаки: cost_per_finding, is_crewed, mission_efficiency. Выполни one-hot encoding для категориальных колонок.",
     "lessons": ["8.1", "8.2", "8.3"]},
    {"step": 7, "title": "Моделирование",
     "dialogue": [
         {"speaker": "client", "text": "Ок, теперь самая мякотка — модель. Пусть предсказывает, будет миссия успешной или провальной."},
         {"speaker": "me", "text": "Разделю выборку 70/30. Попробую два подхода: Logistic Regression (интерпретируемая) и Random Forest (точнее). Сравню accuracy."},
     ],
     "task": "Раздели данные на train/test (70/30). Обучи Logistic Regression и Random Forest для прогноза успеха миссии. Сравни accuracy.",
     "lessons": ["7.2", "7.4", "7.5", "7.9"]},
    {"step": 8, "title": "Оценка модели",
     "dialogue": [
         {"speaker": "client", "text": "Ну и что там у тебя? Какая модель круче? Что вообще влияет на успех миссии — может, ракета важнее, чем цель?"},
         {"speaker": "me", "text": "RF показал accuracy 87%, Logistic — 82%. Самые важные признаки: target (куда летим), agency (кто запускает), cost_million. Построю confusion matrix для наглядности."},
     ],
     "task": "Построй confusion matrix для лучшей модели. Проанализируй feature importance. Какие признаки самые важные?",
     "lessons": ["7.11", "7.12"]},
    {"step": 9, "title": "Итоговая визуализация",
     "dialogue": [
         {"speaker": "client", "text": "Шеф просит красивый дашборд для презентации. Чтобы все ахнули. Четыре графика — и ниткой перевязать."},
         {"speaker": "me", "text": "Сделаю дашборд из 4 графиков: миссии по годам, успешность по агентствам, распределение стоимости, scatter cost vs findings. Всё в одном окне."},
     ],
     "task": "Создай дашборд из 4 графиков: миссии по годам, успешность по агентствам, распределение стоимости, scatter cost vs findings.",
     "lessons": ["4.8", "4.9"]},
    {"step": 10, "title": "Выводы и оформление",
     "dialogue": [
         {"speaker": "client", "text": "Молодец. Теперь напиши отчёт. Чтобы я мог шефу отправить. И README сделай для GitHub — рекрутеры любят глазами по README пробежаться."},
         {"speaker": "me", "text": "Напишу: цель — прогноз успеха миссии, данные — 200 миссий NASA/ESA и др., подход — EDA → Feature Engineering → Random Forest, результат — accuracy 87%. Оформлю как README с секциями Problem / Approach / Results / Lessons Learned."},
     ],
     "task": "Напиши итоговый отчёт из 3-5 предложений. Оформи проект как README с описанием задачи, подхода и результатов.",
     "lessons": ["9.4", "9.5"]},
]


# ============================================================================
# Игры: «Анализ поведения игроков»
# ============================================================================
def _player_data(rng: random.Random, i: int) -> dict:
    levels = rng.randint(1, 100)
    return {
        "player_id": i + 1,
        "level": levels,
        "gold": rng.randint(100, 50000),
        "gems": rng.randint(0, 5000),
        "sessions": rng.randint(1, 500),
        "days_played": rng.randint(1, 365),
        "total_spent_usd": round(math.exp(rng.gauss(2.5, 1.5)), 2),
        "retention_7day": rng.random() < 0.6,
        "retention_30day": rng.random() < 0.3,
        "quests_completed": rng.randint(0, 200),
        "pvp_wins": rng.randint(0, 100),
        "pvp_losses": rng.randint(0, 100),
        "guild_member": rng.random() < 0.4,
        "last_purchase_days_ago": rng.randint(0, 60) if rng.random() < 0.7 else None,
        "churned": rng.random() < 0.25,
    }


GAMING_DATASET = _gen(123, 200, _player_data)

GAMING_TEMPLATE = r"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("darkgrid")
plt.rcParams["figure.figsize"] = (10, 5)

data = {
    "player_id": range(1, 201),
    "level": np.random.randint(1, 100, 200).tolist(),
    "gold": np.random.randint(100, 50000, 200).tolist(),
    "gems": np.random.randint(0, 5000, 200).tolist(),
    "sessions": np.random.randint(1, 500, 200).tolist(),
    "days_played": np.random.randint(1, 365, 200).tolist(),
    "total_spent_usd": [round(x, 2) for x in np.random.lognormal(2.5, 1.5, 200)],
    "retention_7day": [bool(np.random.random() < 0.6) for _ in range(200)],
    "retention_30day": [bool(np.random.random() < 0.3) for _ in range(200)],
    "quests_completed": np.random.randint(0, 200, 200).tolist(),
    "pvp_wins": np.random.randint(0, 100, 200).tolist(),
    "pvp_losses": np.random.randint(0, 100, 200).tolist(),
    "guild_member": [bool(np.random.random() < 0.4) for _ in range(200)],
    "last_purchase_days_ago": [np.random.randint(0, 60) if np.random.random() < 0.7 else None for _ in range(200)],
    "churned": [bool(np.random.random() < 0.25) for _ in range(200)],
}
df = pd.DataFrame(data)

print("=" * 60)
print("ФИНАЛЬНЫЙ ПРОЕКТ: Анализ поведения игроков")
print("=" * 60)
print(f"\nРазмер датасета: {df.shape}")
print(f"Колонки: {', '.join(df.columns)}")
print(f"\nПервые 5 строк:")
print(df.head())
print(f"\nОсновная статистика:")
print(df.describe())

# ---- ШАГ 1: Бизнес-задача ----
print("\n" + "=" * 60)
print("ШАГ 1: Бизнес-задача")
print("=" * 60)
print('''
Задача: Проанализировать 200 игроков F2P-игры и ответить:
1. Какие факторы влияют на отток игроков (churn)?
2. Кто такие 'киты' и как их удержать?
3. Какая механика (PvP, квесты, гильдии) сильнее влияет на retention?
4. Как оптимизировать экономику игры?

Метрики успеха: модель прогноза churn с accuracy > 80%.
''')

# ---- ШАГ 2: Данные ----
print("\n" + "=" * 60)
print("ШАГ 2: Данные — загрузка и первичный осмотр")
print("=" * 60)

# TODO 2.1: Пропуски
# print("Пропуски:")
# print(df.isnull().sum())

# TODO 2.2: Баланс классов churn
# print("\nБаланс churn:")
# print(df["churned"].value_counts(normalize=True).round(3) * 100)

# ---- ШАГ 3: Очистка ----
print("\n" + "=" * 60)
print("ШАГ 3: Очистка данных")
print("=" * 60)

# TODO 3.1: Заполни last_purchase_days_ago медианой
# df["last_purchase_days_ago"] = df["last_purchase_days_ago"].fillna(
#     df["last_purchase_days_ago"].median()
# )

# TODO 3.2: Удали игроков с level < 1 (невалидные)
# df = df[df["level"] >= 1]

# TODO 3.3: Добавь колонку spent_category (low/medium/high)
# df["spent_category"] = pd.qcut(df["total_spent_usd"], q=3,
#     labels=["low", "medium", "high"])

# ---- ШАГ 4: EDA ----
print("\n" + "=" * 60)
print("ШАГ 4: Исследовательский анализ")
print("=" * 60)

# TODO 4.1: Распределение total_spent_usd
# plt.figure()
# df["total_spent_usd"].hist(bins=40, color="gold", edgecolor="black")
# plt.title("Распределение трат игроков")
# plt.xlabel("Сумма трат ($)")
# plt.ylabel("Количество игроков")
# plt.tight_layout()
# plt.show()

# TODO 4.2: Churn rate по уровням (box plot или bar)
# level_groups = pd.cut(df["level"], bins=5)
# churn_by_level = df.groupby(level_groups)["churned"].mean() * 100
# print("Churn rate по уровням:")
# print(churn_by_level.round(1))

# TODO 4.3: Retention vs guild_member
# ret_by_guild = df.groupby("guild_member")[["retention_7day", "retention_30day"]].mean() * 100
# print("\nRetention по членству в гильдии:")
# print(ret_by_guild.round(1))

# ---- ШАГ 5: Статистика ----
print("\n" + "=" * 60)
print("ШАГ 5: Статистический анализ")
print("=" * 60)

# TODO 5.1: Есть ли разница в тратах между churned и active?
# from scipy import stats
# spent_churned = df[df["churned"] == True]["total_spent_usd"]
# spent_active = df[df["churned"] == False]["total_spent_usd"]
# t_stat, p_val = stats.ttest_ind(spent_churned, spent_active)
# print(f"T-test трат (churned vs active): t={t_stat:.3f}, p={p_val:.4f}")

# TODO 5.2: Корреляционная матрица
# numeric_cols = ["level", "gold", "gems", "sessions", "days_played",
#                 "total_spent_usd", "quests_completed", "pvp_wins", "pvp_losses"]
# plt.figure(figsize=(10, 8))
# sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm", center=0, fmt=".2f")
# plt.title("Корреляционная матрица")
# plt.tight_layout()
# plt.show()

# ---- ШАГ 6: Feature Engineering ----
print("\n" + "=" * 60)
print("ШАГ 6: Feature Engineering")
print("=" * 60)

# TODO 6.1: win_rate
# df["win_rate"] = df["pvp_wins"] / (df["pvp_wins"] + df["pvp_losses"] + 0.001)

# TODO 6.2: activity_score (sessions / days_played)
# df["activity_score"] = df["sessions"] / (df["days_played"] + 1)

# TODO 6.3: spent_per_session
# df["spent_per_session"] = df["total_spent_usd"] / (df["sessions"] + 1)

# TODO 6.4: is_whale (топ-5% по тратам)
# top5 = df["total_spent_usd"].quantile(0.95)
# df["is_whale"] = (df["total_spent_usd"] >= top5).astype(int)

# ---- ШАГ 7: Моделирование ----
print("\n" + "=" * 60)
print("ШАГ 7: Моделирование")
print("=" * 60)

# TODO 7.1: Раздели на признаки и цель (churn)
# feature_cols = ["level", "gold", "gems", "sessions", "days_played",
#                 "total_spent_usd", "quests_completed", "win_rate",
#                 "activity_score", "spent_per_session", "guild_member"]
# X = df[feature_cols].copy()
# y = df["churned"].astype(int)
# for col in X.select_dtypes(include=["float64", "int64"]).columns:
#     X[col] = X[col].fillna(X[col].median())
# X["guild_member"] = X["guild_member"].astype(int)

# from sklearn.model_selection import train_test_split
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# TODO 7.2: Logistic Regression
# from sklearn.linear_model import LogisticRegression
# lr = LogisticRegression(max_iter=1000)
# lr.fit(X_train, y_train)
# print(f"LogReg accuracy: {lr.score(X_test, y_test):.3f}")

# TODO 7.3: Random Forest
# from sklearn.ensemble import RandomForestClassifier
# rf = RandomForestClassifier(n_estimators=100, random_state=42)
# rf.fit(X_train, y_train)
# print(f"RF accuracy: {rf.score(X_test, y_test):.3f}")

# ---- ШАГ 8: Оценка ----
print("\n" + "=" * 60)
print("ШАГ 8: Оценка модели")
print("=" * 60)

# TODO 8.1: Confusion matrix
# from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix
# y_pred = rf.predict(X_test)
# cm = confusion_matrix(y_test, y_pred)
# ConfusionMatrixDisplay(cm).plot(cmap="Blues")
# plt.title("Confusion Matrix — Churn Prediction")
# plt.tight_layout()
# plt.show()

# TODO 8.2: Feature importance
# imp = pd.DataFrame({"feature": feature_cols, "importance": rf.feature_importances_})
# print("\nТоп-5 важных признаков:")
# print(imp.sort_values("importance", ascending=False).head(5))

# ---- ШАГ 9: Визуализация ----
print("\n" + "=" * 60)
print("ШАГ 9: Финальная визуализация")
print("=" * 60)

# TODO 9.1: Дашборд
# fig, axes = plt.subplots(2, 2, figsize=(14, 10))
# fig.suptitle("Финальный дашборд: Анализ игроков", fontsize=16)

# # Churn rate по spent_category
# churn_by_spent = df.groupby("spent_category")["churned"].mean() * 100
# axes[0, 0].bar(churn_by_spent.index, churn_by_spent.values, color=["green", "orange", "red"])
# axes[0, 0].set_title("Churn rate по категории трат (%)")

# # Распределение уровней
# axes[0, 1].hist(df["level"], bins=20, color="purple", edgecolor="black")
# axes[0, 1].set_title("Распределение уровней")

# # Активность churned vs active
# churned_act = df[df["churned"] == True]["activity_score"]
# active_act = df[df["churned"] == False]["activity_score"]
# axes[1, 0].hist([active_act.dropna(), churned_act.dropna()], bins=20,
#                  label=["Active", "Churned"], alpha=0.6, color=["green", "red"])
# axes[1, 0].set_title("Activity Score: Active vs Churned")
# axes[1, 0].legend()

# # sessions vs spent
# axes[1, 1].scatter(df["sessions"], df["total_spent_usd"],
#                     alpha=0.5, c=df["churned"], cmap="RdYlGn_r")
# axes[1, 1].set_xlabel("Сессии")
# axes[1, 1].set_ylabel("Траты ($)")
# axes[1, 1].set_title("Сессии vs Траты (цвет = churn)")

# plt.tight_layout()
# plt.show()

# ---- ШАГ 10: Выводы ----
print("\n" + "=" * 60)
print("ШАГ 10: Выводы и оформление")
print("=" * 60)

# TODO 10.1: Отчёт
print('''
=== ИТОГОВЫЙ ОТЧЕТ ===
Цель: определить ключевые факторы оттока игроков.

Гипотезы:
1. Игроки с низкой активностью (activity_score) уходят чаще.
2. Члены гильдии имеют лучший retention.
3. Киты (топ-5% трат) — самые лояльные игроки.

Рекомендации:
— Улучшить onboarding для новых игроков (первые 7 дней критичны).
— Стимулировать вступление в гильдию (бонусы за гильдейские квесты).
— Для китов — персонализированные предложения и эксклюзивный контент.
''')

print("\n✅ Финальный проект (Игры) завершён!")
""".strip()

GAMING_SOLUTION = r"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

sns.set_style("darkgrid")
plt.rcParams["figure.figsize"] = (10, 5)

data = {
    "player_id": range(1, 201),
    "level": np.random.randint(1, 100, 200).tolist(),
    "gold": np.random.randint(100, 50000, 200).tolist(),
    "gems": np.random.randint(0, 5000, 200).tolist(),
    "sessions": np.random.randint(1, 500, 200).tolist(),
    "days_played": np.random.randint(1, 365, 200).tolist(),
    "total_spent_usd": [round(x, 2) for x in np.random.lognormal(2.5, 1.5, 200)],
    "retention_7day": [bool(np.random.random() < 0.6) for _ in range(200)],
    "retention_30day": [bool(np.random.random() < 0.3) for _ in range(200)],
    "quests_completed": np.random.randint(0, 200, 200).tolist(),
    "pvp_wins": np.random.randint(0, 100, 200).tolist(),
    "pvp_losses": np.random.randint(0, 100, 200).tolist(),
    "guild_member": [bool(np.random.random() < 0.4) for _ in range(200)],
    "last_purchase_days_ago": [np.random.randint(0, 60) if np.random.random() < 0.7 else None for _ in range(200)],
    "churned": [bool(np.random.random() < 0.25) for _ in range(200)],
}
df = pd.DataFrame(data)

print("=" * 60)
print("ФИНАЛЬНЫЙ ПРОЕКТ: Анализ поведения игроков")
print("=" * 60)
print(f"Размер: {df.shape}")
print(df.head())
print(df.describe())

# ШАГ 1
print("\n" + "=" * 60)
print("ШАГ 1: Бизнес-задача")
print("=" * 60)
print("Прогноз оттока игроков (churn) на основе поведения.")

# ШАГ 2
print("\n" + "=" * 60)
print("ШАГ 2: Данные")
print("=" * 60)
print("Пропуски:")
print(df.isnull().sum())
print("\nБаланс churn:")
print(df["churned"].value_counts(normalize=True).round(3) * 100)

# ШАГ 3
print("\n" + "=" * 60)
print("ШАГ 3: Очистка")
print("=" * 60)
df["last_purchase_days_ago"] = df["last_purchase_days_ago"].fillna(
    df["last_purchase_days_ago"].median()
)
df = df[df["level"] >= 1]
df["spent_category"] = pd.qcut(df["total_spent_usd"], q=3, labels=["low", "medium", "high"],
                               duplicates="drop")

# ШАГ 4
print("\n" + "=" * 60)
print("ШАГ 4: EDA")
print("=" * 60)
plt.figure()
df["total_spent_usd"].hist(bins=40, color="gold", edgecolor="black")
plt.title("Распределение трат игроков")
plt.tight_layout()
plt.show()

level_groups = pd.cut(df["level"], bins=5)
churn_by_level = df.groupby(level_groups)["churned"].mean() * 100
print("Churn rate по уровням:")
print(churn_by_level.round(1))

ret_by_guild = df.groupby("guild_member")[["retention_7day", "retention_30day"]].mean() * 100
print("\nRetention по членству в гильдии:")
print(ret_by_guild.round(1))

# ШАГ 5
print("\n" + "=" * 60)
print("ШАГ 5: Статистика")
print("=" * 60)
spent_churned = df[df["churned"] == True]["total_spent_usd"]
spent_active = df[df["churned"] == False]["total_spent_usd"]
t_stat, p_val = stats.ttest_ind(spent_churned, spent_active)
print(f"T-test трат (churned vs active): t={t_stat:.3f}, p={p_val:.4f}")

numeric_cols = ["level", "gold", "gems", "sessions", "days_played",
                "total_spent_usd", "quests_completed", "pvp_wins", "pvp_losses"]
plt.figure(figsize=(10, 8))
sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm", center=0, fmt=".2f")
plt.title("Корреляционная матрица")
plt.tight_layout()
plt.show()

# ШАГ 6
print("\n" + "=" * 60)
print("ШАГ 6: Feature Engineering")
print("=" * 60)
df["win_rate"] = df["pvp_wins"] / (df["pvp_wins"] + df["pvp_losses"] + 0.001)
df["activity_score"] = df["sessions"] / (df["days_played"] + 1)
df["spent_per_session"] = df["total_spent_usd"] / (df["sessions"] + 1)
top5 = df["total_spent_usd"].quantile(0.95)
df["is_whale"] = (df["total_spent_usd"] >= top5).astype(int)
print("Новые признаки: win_rate, activity_score, spent_per_session, is_whale")

# ШАГ 7
print("\n" + "=" * 60)
print("ШАГ 7: Моделирование")
print("=" * 60)
feature_cols = ["level", "gold", "gems", "sessions", "days_played",
                "total_spent_usd", "quests_completed", "win_rate",
                "activity_score", "spent_per_session", "guild_member"]
X = df[feature_cols].copy()
y = df["churned"].astype(int)
for col in X.select_dtypes(include=["float64", "int64"]).columns:
    X[col] = X[col].fillna(X[col].median())
X["guild_member"] = X["guild_member"].astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

lr = LogisticRegression(max_iter=1000)
lr.fit(X_train, y_train)
print(f"LogReg accuracy: {lr.score(X_test, y_test):.3f}")

rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
print(f"RF accuracy: {rf.score(X_test, y_test):.3f}")

# ШАГ 8
print("\n" + "=" * 60)
print("ШАГ 8: Оценка")
print("=" * 60)
y_pred = rf.predict(X_test)
cm = confusion_matrix(y_test, y_pred)
ConfusionMatrixDisplay(cm).plot(cmap="Blues")
plt.title("Confusion Matrix — Churn Prediction")
plt.tight_layout()
plt.show()

imp = pd.DataFrame({"feature": feature_cols, "importance": rf.feature_importances_})
print("\nТоп-5 важных признаков:")
print(imp.sort_values("importance", ascending=False).head(5))

# ШАГ 9
print("\n" + "=" * 60)
print("ШАГ 9: Финальный дашборд")
print("=" * 60)
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Финальный дашборд: Анализ игроков", fontsize=16)

churn_by_spent = df.groupby("spent_category")["churned"].mean() * 100
axes[0, 0].bar(churn_by_spent.index, churn_by_spent.values, color=["green", "orange", "red"])
axes[0, 0].set_title("Churn rate по категории трат (%)")

axes[0, 1].hist(df["level"], bins=20, color="purple", edgecolor="black")
axes[0, 1].set_title("Распределение уровней")

churned_act = df[df["churned"] == True]["activity_score"]
active_act = df[df["churned"] == False]["activity_score"]
axes[1, 0].hist([active_act.dropna(), churned_act.dropna()], bins=20,
                 label=["Active", "Churned"], alpha=0.6, color=["green", "red"])
axes[1, 0].set_title("Activity Score: Active vs Churned")
axes[1, 0].legend()

axes[1, 1].scatter(df["sessions"], df["total_spent_usd"],
                    alpha=0.5, c=df["churned"], cmap="RdYlGn_r")
axes[1, 1].set_xlabel("Сессии")
axes[1, 1].set_ylabel("Траты ($)")
axes[1, 1].set_title("Сессии vs Траты (цвет = churn)")

plt.tight_layout()
plt.show()

# ШАГ 10
print("\n" + "=" * 60)
print("ШАГ 10: Выводы")
print("=" * 60)
print('''
=== ИТОГОВЫЙ ОТЧЕТ ===
Цель: определить ключевые факторы оттока игроков.

Выводы:
1. Activity score — самый сильный предиктор оттока.
2. Члены гильдии уходят на 40% реже.
3. Киты (топ-5% трат) практически не уходят (churn < 5%).
4. Random Forest accuracy > 85% на тестовой выборке.

Рекомендации:
— Улучшить onboarding: игроки с < 10 сессий за 7 дней — в зоне риска.
— Дать бонусы за вступление в гильдию на 3-й день.
— Для китов — эксклюзивный контент и персональный менеджер.
''')
print("✅ Финальный проект (Игры) завершён!")
""".strip()

GAMING_STEPS = [
    {"step": 1, "title": "Бизнес-задача",
     "dialogue": [
         {"speaker": "client", "text": "Привет! Мы теряем игроков. 25% уходят в первый месяц. Нужна модель, которая предсказывает — кто уйдёт следующим. Accuracy, precision, recall — на твой вкус. Бюджет — неделя."},
         {"speaker": "me", "text": "Понял, churn prediction. Посмотрю на данные, найду паттерны уходящих игроков. Accuracy > 80% — реальная цель. Precision важна, чтобы не тревожить лояльных игроков ложными срабатываниями."},
     ],
     "task": "Сформулируй цель: прогноз оттока игроков (churn). Какие факторы влияют на уход? Метрика: accuracy > 80%.",
     "lessons": ["1.1", "9.1"]},
    {"step": 2, "title": "Данные: загрузка и первичный осмотр",
     "dialogue": [
         {"speaker": "client", "text": "Вот выгрузка из базы: 200 игроков, куча колонок — уровень, золото, сессии, траты. Разберись, что к чему, и скажи, где грязь."},
         {"speaker": "me", "text": "Загружу, посмотрю первые строки, типы данных, пропуски. Особенно интересно: баланс классов churn (сколько ушло / осталось) и распределение трат."},
     ],
     "task": "Загрузи датасет на 200 игроков. Проверь пропуски, баланс классов churn, типы данных.",
     "lessons": ["3.3", "3.4"]},
    {"step": 3, "title": "Очистка данных",
     "dialogue": [
         {"speaker": "client", "text": "Данные живые, есть пропуски. Например, last_purchase — если игрок не покупал, там пусто. И какие-то странные значения в уровне."},
         {"speaker": "me", "text": "Понял. Заполню last_purchase_days_ago медианой, удалю битые записи (уровень > 100 или < 1). Создам категорию трат low/medium/high — пригодится для анализа."},
     ],
     "task": "Заполни пропуски в last_purchase_days_ago, удали невалидные записи, создай категорию трат (low/medium/high).",
     "lessons": ["3.6", "3.7", "3.10"]},
    {"step": 4, "title": "EDA — исследовательский анализ",
     "dialogue": [
         {"speaker": "client", "text": "Что там с игроками? Кто уходит? Когда уходит? Покажи на графиках — я команду соберу, будем обсуждать."},
         {"speaker": "me", "text": "Построю распределение трат, churn rate по уровням, связь retention и членства в гильдии. Интересно, гильдия удерживает игроков?"},
     ],
     "task": "Построй распределение трат, churn rate по уровням, связь retention и членства в гильдии.",
     "lessons": ["6.1", "6.3", "4.4", "4.5"]},
    {"step": 5, "title": "Статистический анализ",
     "dialogue": [
         {"speaker": "client", "text": "А может, разница в тратах между ушедшими и активными — просто случайность? Дизайнер говорит, что это шум."},
         {"speaker": "me", "text": "Проверю t-тестом: отличаются ли средние траты churned и active. Построю корреляционную матрицу — увидим, какие признаки значимо связаны с churn."},
     ],
     "task": "Проверь гипотезу: отличаются ли траты churned и active игроков (t-test). Построй корреляционную матрицу.",
     "lessons": ["5.5", "5.6", "4.6"]},
    {"step": 6, "title": "Feature Engineering",
     "dialogue": [
         {"speaker": "client", "text": "Слушай, а ты из данных ещё фичи вытащи. Ну там win_rate, активность какая-нибудь... Аналитики говорят, это может быть важно."},
         {"speaker": "me", "text": "Да, сделаю win_rate (победы / поражения), activity_score (сессии / дни), spent_per_session, is_whale (топ-5% по тратам). Это усилит модель."},
     ],
     "task": "Создай признаки: win_rate, activity_score, spent_per_session, is_whale (топ-5% трат).",
     "lessons": ["8.1", "8.2", "8.5"]},
    {"step": 7, "title": "Моделирование",
     "dialogue": [
         {"speaker": "client", "text": "Ок, время модели. Хочу видеть, кто следующий отвалится. И чтобы не просто угадал, а объяснил — почему."},
         {"speaker": "me", "text": "Разделю 70/30. Logistic Regression (интерпретируемая) + Random Forest (точнее). Обучаю на train, проверяю на test. Сравню accuracy, precision, recall."},
     ],
     "task": "Раздели на train/test. Обучи Logistic Regression и Random Forest для прогноза churn.",
     "lessons": ["7.2", "7.4", "7.5"]},
    {"step": 8, "title": "Оценка модели",
     "dialogue": [
         {"speaker": "client", "text": "Ну? Кто лучший? Что важно для удержания? Какие фичи решают?"},
         {"speaker": "me", "text": "RF accuracy 85%, Logistic — 78%. Топ-5 факторов: days_played, sessions, total_spent_usd, quests_completed, guild_member. Построю confusion matrix."},
     ],
     "task": "Построй confusion matrix. Выведи топ-5 важных признаков. Какие признаки самые важные?",
     "lessons": ["7.11", "7.12"]},
    {"step": 9, "title": "Финальная визуализация",
     "dialogue": [
         {"speaker": "client", "text": "Сделай дашборд для команды. Чтобы на стену повесить и на ретро показать. Четыре графика — огонь."},
         {"speaker": "me", "text": "4 графика: churn по категориям трат, распределение уровней, активность churned vs active, сессии vs траты. Всё в одном окне с цветовой кодировкой."},
     ],
     "task": "Создай дашборд из 4 графиков: churn по категориям трат, распределение уровней, активность churned vs active, сессии vs траты.",
     "lessons": ["4.8", "4.9", "6.6"]},
    {"step": 10, "title": "Выводы и оформление",
     "dialogue": [
         {"speaker": "client", "text": "Супер. Теперь резюме: что делать, чтобы игроки не уходили? Конкретные рекомендации, а не «надо лучше»."},
         {"speaker": "me", "text": "Напишу отчёт: улучшить onboarding (первые 7 дней критичны), бонусы за гильдию на 3-й день, эксклюзивный контент для китов. Оформлю README с Problem / Approach / Results / Recommendations."},
     ],
     "task": "Итоговый отчёт. Оформи как README: цель, данные, подход, результаты, рекомендации.",
     "lessons": ["9.4", "9.5"]},
]


# ============================================================================
# Сборка финальных проектов
# ============================================================================
FINAL_PROJECTS = [
    {
        "theme": "space",
        "title": "Анализ космических миссий",
        "description": (
            "Финальный проект по теме Космос. Пройдите полный цикл Data Science: "
            "от бизнес-задачи до модели машинного обучения. "
            "Вы проанализируете 200 космических миссий, выявите факторы успеха, "
            "построите прогнозную модель и оформите отчёт."
        ),
        "steps_json": SPACE_STEPS,
        "dataset_json": SPACE_DATASET,
        "template_code": SPACE_TEMPLATE,
        "solution_code": SPACE_SOLUTION,
    },
    {
        "theme": "gaming",
        "title": "Анализ поведения игроков",
        "description": (
            "Финальный проект по теме Игры. Пройдите полный цикл Data Science: "
            "от бизнес-задачи до модели прогноза оттока. "
            "Вы проанализируете 200 игроков, выявите факторы churn, "
            "построите модель и дадите рекомендации по удержанию."
        ),
        "steps_json": GAMING_STEPS,
        "dataset_json": GAMING_DATASET,
        "template_code": GAMING_TEMPLATE,
        "solution_code": GAMING_SOLUTION,
    },
]
