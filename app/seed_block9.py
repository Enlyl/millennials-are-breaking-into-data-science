"""
Блок 9: Производственный Data Science.
8 уроков, ~70 упражнений.
Git, Jupyter, структура ML-проекта, Docker, MLOps, воспроизводимость.
"""
from app.seed_helpers import (
    ex, lesson, theory, analogy, visual, example,
    common_mistakes, interview_questions, knowledge_checklist,
)


def _9_1():
    return lesson(
        "9.1", "Git: основы для Data Scientist", "neutral", [
            theory(
                "**Git** — распределённая система контроля версий. "
                "Data Scientist использует Git каждый день: сохранять эксперименты, "
                "делиться кодом с командой, откатываться к рабочей версии, "
                "сравнивать результаты разных запусков модели.\n\n"
                "**Базовые понятия:**\n"
                "- **Репозиторий (repo)** — папка проекта, за которой следит Git.\n"
                "- **Коммит (commit)** — снимок состояния файлов в конкретный момент.\n"
                "- **Индекс (staging area)** — промежуточная зона: что попадёт в следующий коммит.\n"
                "- **HEAD** — указатель на текущий коммит (обычно последний).\n\n"
                "**Минимальный рабочий процесс:**\n"
                "```\n"
                "git init                      # инициализировать репозиторий\n"
                "git status                    # что изменилось\n"
                "git add файл.py               # подготовить к коммиту\n"
                "git commit -m 'сообщение'     # зафиксировать\n"
                "git log --oneline             # история коммитов\n"
                "```\n\n"
                "**`.gitignore`** — файл, в котором перечислены пути, которые Git не должен отслеживать: "
                "большие данные, модели, виртуальные окружения, секреты, логи.\n\n"
                "**Зачем DS:** каждый ноутбук, скрипт обучения и параметр модели — "
                "это эксперимент. Без Git через неделю вы не вспомните, какая версия кода дала accuracy 0.92."
            ),
            analogy(
                "Git — это система сохранений в видеоигре: каждый commit — отдельный слот, "
                "в который можно вернуться, если сломал что-то в текущем.",
                "Data Scientist сохраняет «слоты» перед запуском обучения, "
                "перед сменой гиперпараметров, перед рефакторингом — и может откатиться."
            ),
            visual(
                "Граф коммитов: линейная история изменений",
                "* commit 7h8i  (HEAD -> main)\n"
                "|\n"
                "* commit e5f6\n"
                "|\n"
                "* commit c3d4\n"
                "|\n"
                "* commit a1b2  (init)\n"
                "\n"
                "  git log --oneline:\n"
                "  7h8i deploy model\n"
                "  e5f6 fix bug in preprocessing\n"
                "  c3d4 add training script\n"
                "  a1b2 initial commit"
            ),
            example(
                "Создай локальный репозиторий, добавь файл и сделай первый коммит.",
                "git init создаёт скрытую папку .git. git status показывает, что есть неотслеживаемые файлы. "
                "git add переводит файл в индекс. git commit -m фиксирует снимок с сообщением.",
                "$ git init my-ds-project\n"
                "Initialized empty Git repository in my-ds-project/.git/\n\n"
                "$ cd my-ds-project\n"
                "$ echo 'print(\"hello\")' > train.py\n"
                "$ git status\n"
                "Untracked files:\n"
                "  train.py\n\n"
                "$ git add train.py\n"
                "$ git commit -m 'add training script'\n"
                "[main (root-commit) a1b2c3] add training script\n"
                " 1 file changed, 1 insertion(+)\n\n"
                "$ git log --oneline\n"
                "a1b2c3 add training script",
                "Initialized empty Git repository...\n"
                "Untracked files: train.py\n"
                "[main (root-commit) a1b2c3] add training script\n"
                "1 file changed\n"
                "a1b2c3 add training script",
                "После init появилась папка .git. add перевёл файл в индекс, "
                "commit зафиксировал снимок и создал hash 'a1b2c3'. log показывает историю."
            ),
            common_mistakes([
                {"mistake": "Коммитить большие файлы (данные, .csv, .pkl модели)",
                 "why_bad": "Репозиторий раздувается, клонирование занимает часы, GitHub запрещает >100MB",
                 "fix": "Добавь data/, models/, *.csv, *.pkl в .gitignore"},
                {"mistake": "Нет .gitignore в проекте",
                 "why_bad": "В Git попадают __pycache__, .ipynb_checkpoints, .env, виртуальные окружения",
                 "fix": "Создай .gitignore сразу после git init (для Python + DS)"},
                {"mistake": "Секреты и API-ключи прямо в коде",
                 "why_bad": "Секреты утекают в публичный репозиторий навсегда, даже после удаления",
                 "fix": "Используй переменные окружения, .env (в .gitignore), config.py"},
                {"mistake": "Сообщение коммита 'fix' или 'update'",
                 "why_bad": "Через месяц непонятно, что меняли — git log бесполезен",
                 "fix": "Пиши конкретно: 'fix NaN handling in features.py'"},
                {"mistake": "Один гигантский коммит раз в неделю",
                 "why_bad": "Невозможно откатить часть изменений, сложно ревьюить",
                 "fix": "Маленькие атомарные коммиты: одна фича/фикс = один commit"},
            ]),
            interview_questions([
                {"q": "Что такое Git и зачем он Data Scientist?",
                 "a": "Git — распределённая система контроля версий. DS нужен для: истории экспериментов, "
                      "совместной работы, воспроизводимости кода, отката к рабочей версии."},
                {"q": "Что такое .gitignore и зачем он нужен?",
                 "a": ".gitignore — файл со списком шаблонов путей, которые Git игнорирует. "
                      "Используется для данных, моделей, секретов, виртуальных окружений, кэшей."},
                {"q": "В чём разница между git add и git commit?",
                 "a": "git add перемещает изменения в индекс (staging area). "
                      "git commit берёт всё из индекса и создаёт снимок (коммит) в истории."},
            ]),
            knowledge_checklist([
                "Инициализирую репозиторий командой git init",
                "Понимаю три состояния: working dir, staging, committed",
                "Использую git add / git commit / git status / git log",
                "Создаю .gitignore и понимаю, что туда класть",
                "Пишу осмысленные сообщения коммитов",
                "Не коммичу большие файлы и секреты",
            ]),
        ],
        exercises=[
            ex(1, "python", "Создай список `commits` из 5 словарей с ключами 'hash' (4 символа) и 'msg'.",
               "commits = []\n",
               "commits = [\n"
               "    {'hash': 'a1b2', 'msg': 'init project'},\n"
               "    {'hash': 'c3d4', 'msg': 'add data loader'},\n"
               "    {'hash': 'e5f6', 'msg': 'train baseline model'},\n"
               "    {'hash': 'g7h8', 'msg': 'fix preprocessing bug'},\n"
               "    {'hash': 'i9j0', 'msg': 'deploy to staging'},\n"
               "]\n",
               [{"check": "isinstance(commits, list)", "msg": "commits — список"},
                {"check": "len(commits) == 5", "msg": "Ровно 5 коммитов"},
                {"check": "all(isinstance(c, dict) and 'hash' in c and 'msg' in c for c in commits)",
                 "msg": "Каждый элемент — словарь с ключами hash и msg"}],
               ["Словарь = {'ключ': 'значение'}", "list.append() добавляет в конец"], 1),
            ex(2, "python", "Дан `status` — словарь с ключами 'branch', 'modified', 'untracked', 'staged'. "
                            "Заполни значениями: 'main', 3, ['data.csv'], ['train.py'].",
               "status = {}\n",
               "status = {\n"
               "    'branch': 'main',\n"
               "    'modified': 3,\n"
               "    'untracked': ['data.csv'],\n"
               "    'staged': ['train.py'],\n"
               "}\n",
               [{"check": "isinstance(status, dict)", "msg": "status — словарь"},
                {"check": "status.get('branch') == 'main'", "msg": "Ветка main"},
                {"check": "status.get('modified') == 3", "msg": "3 модифицированных файла"},
                {"check": "'data.csv' in status.get('untracked', [])", "msg": "data.csv в untracked"}],
               ["Словарь: ключ -> значение", "Список значений в []"], 1),
            ex(3, "python", "Создай строку `gitignore` — содержимое .gitignore для DS-проекта (минимум 5 строк).",
               "gitignore = ''\n",
               "gitignore = (\n"
               "    '__pycache__/\\n'\n"
               "    '*.pyc\\n'\n"
               "    '.ipynb_checkpoints/\\n'\n"
               "    'data/raw/\\n'\n"
               "    'models/*.pkl\\n'\n"
               "    '.env\\n'\n"
               "    'venv/\\n'\n"
               ")\n",
               [{"check": "isinstance(gitignore, str)", "msg": "gitignore — строка"},
                {"check": "'\\n' in gitignore", "msg": "Есть переносы строк"},
                {"check": "gitignore.count('\\n') >= 5", "msg": "Минимум 5 строк"},
                {"check": "'data' in gitignore or '*.pkl' in gitignore or 'venv' in gitignore",
                 "msg": "Игнорируются данные/модели/окружение"}],
               ["Каждая строка .gitignore — отдельный шаблон", "\\n — перенос строки"], 2),
            ex(4, "python", "Создай функцию `make_commit(commits, msg)`, добавляющую коммит (с псевдо-hash) в список.",
               "def make_commit(commits, msg):\n    pass\n",
               "import hashlib\n"
               "def make_commit(commits, msg):\n"
               "    n = len(commits)\n"
               "    h = hashlib.md5(msg.encode()).hexdigest()[:4]\n"
               "    commits.append({'hash': h, 'msg': msg})\n"
               "    return commits[n]\n",
               [{"check": "isinstance(make_commit([], 'test'), dict)", "msg": "Возвращает словарь"},
                {"check": "'hash' in make_commit([], 'init') and 'msg' in make_commit([], 'init')",
                 "msg": "Словарь с hash и msg"}],
               ["hashlib.md5(...).hexdigest()[:4] — 4 символа хеша", ".append() добавляет в конец"], 3),
            ex(5, "python", "Дан список коммитов. Создай `log_oneline` — список строк формата 'hash msg'.",
               "commits = [{'hash': 'a1b2', 'msg': 'init'}, {'hash': 'c3d4', 'msg': 'train'}]\nlog_oneline = []\n",
               "commits = [{'hash': 'a1b2', 'msg': 'init'}, {'hash': 'c3d4', 'msg': 'train'}]\n"
               "log_oneline = [f\"{c['hash']} {c['msg']}\" for c in commits]\n",
               [{"check": "isinstance(log_oneline, list)", "msg": "log_oneline — список"},
                {"check": "all(isinstance(s, str) for s in log_oneline)", "msg": "Все элементы — строки"},
                {"check": "'a1b2' in log_oneline[0] and 'init' in log_oneline[0]",
                 "msg": "Первая строка содержит hash и msg"}],
               ["f\"{c['hash']} {c['msg']}\" — f-string", "List comprehension: [... for c in ...]"], 2),
            ex(6, "python", "Создай словарь `tracked_files` — расширения, которые нужно отслеживать: "
                            "py, ipynb, md, json, yml, csv (если маленький).",
               "tracked_files = {}\n",
               "tracked_files = {\n"
               "    'code': ['.py', '.ipynb'],\n"
               "    'docs': ['.md', '.txt'],\n"
               "    'config': ['.json', '.yml', '.yaml'],\n"
               "    'data': ['.csv'],\n"
               "}\n",
               [{"check": "isinstance(tracked_files, dict)", "msg": "Словарь"},
                {"check": "tracked_files.get('code') == ['.py', '.ipynb']", "msg": "Код: .py, .ipynb"},
                {"check": "'.py' in str(tracked_files)", "msg": ".py присутствует"}],
               ["Группируй по типам файлов", "Список в []"], 1),
            ex(7, "python", "Дан список путей `paths = ['data/train.csv', 'src/train.py', 'models/clf.pkl', 'README.md']`. "
                            "Создай `to_ignore` — пути, которые нужно добавить в .gitignore "
                            "(большие данные и модели).",
               "paths = ['data/train.csv', 'src/train.py', 'models/clf.pkl', 'README.md']\nto_ignore = []\n",
               "paths = ['data/train.csv', 'src/train.py', 'models/clf.pkl', 'README.md']\n"
               "to_ignore = [p for p in paths if p.startswith('data/') or p.startswith('models/')]\n",
               [{"check": "isinstance(to_ignore, list)", "msg": "Список"},
                {"check": "'data/train.csv' in to_ignore and 'models/clf.pkl' in to_ignore",
                 "msg": "data/ и models/ в ignore"},
                {"check": "'src/train.py' not in to_ignore", "msg": "src/train.py НЕ в ignore"}],
               ["startswith('data/') — путь начинается с data/", "List comprehension с if"], 2),
            ex(8, "python", "Создай функцию `commit_message(branch, action)`, возвращающую строку вида 'branch: action done'.",
               "def commit_message(branch, action):\n    pass\n",
               "def commit_message(branch, action):\n"
               "    return f'{branch}: {action} done'\n",
               [{"check": "commit_message('main', 'init') == 'main: init done'",
                 "msg": "main: init done"},
                {"check": "commit_message('feature', 'add model') == 'feature: add model done'",
                 "msg": "feature: add model done"}],
               ["f-string для форматирования", "return возвращает строку"], 1),
            ex(9, "python", "Дан `repo` — словарь {'name': str, 'commits': int, 'branches': list}. "
                            "Заполни для типичного DS-проекта: 3 коммита, 2 ветки.",
               "repo = {}\n",
               "repo = {\n"
               "    'name': 'churn-prediction',\n"
               "    'commits': 3,\n"
               "    'branches': ['main', 'feature/eda'],\n"
               "}\n",
               [{"check": "isinstance(repo, dict)", "msg": "repo — словарь"},
                {"check": "isinstance(repo.get('name'), str)", "msg": "name — строка"},
                {"check": "isinstance(repo.get('commits'), int)", "msg": "commits — int"},
                {"check": "isinstance(repo.get('branches'), list)", "msg": "branches — список"}],
               ["Словарь: ключ -> значение", "Имя проекта — строка"], 1),
            ex(10, "python", "Создай `staging` — список файлов, готовых к коммиту (3 файла: train.py, eval.py, README.md).",
               "staging = []\n",
               "staging = ['train.py', 'eval.py', 'README.md']\n",
               [{"check": "isinstance(staging, list)", "msg": "staging — список"},
                {"check": "len(staging) == 3", "msg": "3 файла"},
                {"check": "all(isinstance(f, str) for f in staging)", "msg": "Все элементы — строки"},
                {"check": "'train.py' in staging and 'README.md' in staging",
                 "msg": "train.py и README.md в списке"}],
               ["list = [a, b, c]", "Файлы — строки с расширением"], 1),
        ],
        minutes=40, difficulty=2,
    )


def _9_2():
    return lesson(
        "9.2", "Git: ветки, merge, pull request", "neutral", [
            theory(
                "**Ветка (branch)** — параллельная линия разработки. В Git ветки лёгкие: "
                "это просто указатель на коммит. По умолчанию вы на ветке `main` (или `master`).\n\n"
                "**Зачем ветки Data Scientist:**\n"
                "- Эксперимент с новой моделью, не ломая main\n"
                "- Несколько человек работают над одним проектом\n"
                "- Изоляция фич: новый feature engineering, гиперпараметры, отладка\n\n"
                "**Основные команды:**\n"
                "```\n"
                "git branch имя_ветки           # создать ветку\n"
                "git checkout имя_ветки         # переключиться\n"
                "git checkout -b имя_ветки      # создать и сразу переключиться\n"
                "git merge имя_ветки            # влить ветку в текущую\n"
                "git branch -d имя_ветки        # удалить (после merge)\n"
                "```\n\n"
                "**Merge vs Rebase:**\n"
                "- `merge` — сохраняет историю с развилкой, создаёт merge commit\n"
                "- `rebase` — переписывает историю линейно (для локальной чистки)\n\n"
                "**Pull Request (PR)** — предложение влить вашу ветку в main через платформу "
                "(GitHub, GitLab, Bitbucket). Это место для код-ревью, обсуждений и CI-проверок.\n\n"
                "**Merge conflict** — когда две ветки изменили одни и те же строки. "
                "Git не может решить автоматически — нужно править вручную, выбирая вариант."
            ),
            analogy(
                "Ветка в Git — это черновик статьи: вы правите свою копию, не трогая оригинал, "
                "а потом редактор (merge) вливает ваши изменения в чистовик.",
                "Data Scientist создаёт ветку `experiment/lstm` для новой архитектуры, "
                "а после успешных метрик вливает её в main через PR."
            ),
            visual(
                "Граф с веткой и merge: развилка и слияние",
                "* 9i0j  (HEAD -> main, feature/x)\n"
                "|\\\n"
                "| * 7h8i  (feature/x)\n"
                "| |\n"
                "* | 6g7h\n"
                "|\\\n"
                "| * 5f6g\n"
                "|/\n"
                "* 4e5d\n"
                "|\n"
                "* 3c4d\n"
                "\n"
                "main и feature/x разошлись после 4e5d, "
                "потом main получил 6g7h, а feature — 5f6g, 7h8i. "
                "В 9i0j — merge commit, объединяющий обе истории."
            ),
            example(
                "Создай ветку, внеси изменение и влей её в main.",
                "checkout -b создаёт ветку и переключается на неё одной командой. "
                "Вносим изменение, коммитим, переключаемся обратно на main и делаем merge. "
                "После успешного merge ветку можно удалить через -d.",
                "$ git checkout -b feature/better-features\n"
                "Switched to a new branch 'feature/better-features'\n\n"
                "$ git add features.py\n"
                "$ git commit -m 'add log-transform of skewed features'\n"
                "[feature/better-features 7h8i9j] add log-transform ...\n\n"
                "$ git checkout main\n"
                "Switched to branch 'main'\n\n"
                "$ git merge feature/better-features\n"
                "Updating 6g7h..7h8i\n"
                "Fast-forward\n"
                " features.py | 12 +++++++++++-\n"
                " 1 file changed, 11 insertions(+)\n\n"
                "$ git branch -d feature/better-features\n"
                "Deleted branch feature/better-features",
                "Switched to a new branch 'feature/better-features'\n"
                "[feature/better-features 7h8i9j] add log-transform ...\n"
                "Updating 6g7h..7h8i\n"
                "Fast-forward",
                "Ветка создана, изменение закоммичено, переключились на main, "
                "merge сделал fast-forward (прямое перемещение main на 7h8i9j). "
                "Ветка удалена после успешного вливания."
            ),
            common_mistakes([
                {"mistake": "Работать сразу в main, не создавая ветку",
                 "why_bad": "Сломанный код попадает в основную ветку, ломает команду, нет изоляции экспериментов",
                 "fix": "Перед новой задачей — git checkout -b feature/описание"},
                {"mistake": "Один PR с десятками не связанных изменений",
                 "why_bad": "Невозможно ревьюить, высок риск отклонить всё",
                 "fix": "Один PR = одна логическая задача (фича/баг/рефактор)"},
                {"mistake": "Игнорировать merge conflict, форсить git push --force",
                 "why_bad": "Можно потерять чужой код, сломать историю",
                 "fix": "Разреши конфликт вручную, обсуди с автором"},
                {"mistake": "Длинные живущие ветки (месяцы без merge)",
                 "why_bad": "Растёт число конфликтов, отстаёт от main, невозможно мержить",
                 "fix": "Короткоживущие ветки: создал -> PR -> merge -> удалил, в течение дней"},
                {"mistake": "Не делать git pull перед push",
                 "why_bad": "Push отклонён из-за отставания от remote main",
                 "fix": "Всегда: git pull --rebase origin main, потом git push"},
            ]),
            interview_questions([
                {"q": "Что такое merge conflict и как его разрешить?",
                 "a": "Конфликт возникает, когда две ветки изменили одни и те же строки. "
                      "Git помечает их маркерами >>>>>> ======= <<<<<<<. "
                      "Нужно вручную выбрать нужный вариант, убрать маркеры, сделать commit."},
                {"q": "В чём разница между merge и rebase?",
                 "a": "merge сохраняет историю с развилками и создаёт merge commit. "
                      "rebase переписывает коммиты так, будто они шли линейно от main. "
                      "merge — для общей истории, rebase — для локальной чистки."},
                {"q": "Зачем нужны Pull Requests?",
                 "a": "PR — механизм код-ревью: команда проверяет код до вливания в main, "
                      "обсуждает, запускает CI. Помогает ловить баги и делиться знаниями."},
            ]),
            knowledge_checklist([
                "Создаю ветки через git checkout -b",
                "Переключаюсь между ветками",
                "Делаю merge и понимаю fast-forward",
                "Разрешаю простые merge conflict",
                "Открываю Pull Request и провожу код-ревью",
                "Удаляю слитые ветки",
            ]),
        ],
        exercises=[
            ex(1, "python", "Создай список `branches` из 4 веток: 'main' и три feature-ветки (префикс 'feature/').",
               "branches = []\n",
               "branches = ['main', 'feature/eda', 'feature/lstm', 'feature/hyperparam-tuning']\n",
               [{"check": "isinstance(branches, list)", "msg": "Список"},
                {"check": "len(branches) == 4", "msg": "4 ветки"},
                {"check": "'main' in branches", "msg": "main присутствует"},
                {"check": "sum(1 for b in branches if b.startswith('feature/')) == 3",
                 "msg": "3 feature-ветки с префиксом 'feature/'"}],
               ["Имена веток — строки", "Префикс feature/ для экспериментов"], 1),
            ex(2, "python", "Создай функцию `checkout(branch)`, возвращающую f-строку 'Switched to branch \"X\"'.",
               "def checkout(branch):\n    pass\n",
               "def checkout(branch):\n"
               "    return f'Switched to branch \"{branch}\"'\n",
               [{"check": "checkout('main') == 'Switched to branch \"main\"'",
                 "msg": "Switched to branch \"main\""},
                {"check": "checkout('feature/x') == 'Switched to branch \"feature/x\"'",
                 "msg": "feature/x"}],
               ["f-string подставляет значение", "Экранируй кавычки \\\" внутри f-string"], 1),
            ex(3, "python", "Создай словарь `merge_result` с ключами 'fast_forward' (bool), "
                            "'conflicts' (int), 'commits_added' (int). Заполни: True, 0, 3.",
               "merge_result = {}\n",
               "merge_result = {\n"
               "    'fast_forward': True,\n"
               "    'conflicts': 0,\n"
               "    'commits_added': 3,\n"
               "}\n",
               [{"check": "isinstance(merge_result, dict)", "msg": "Словарь"},
                {"check": "merge_result.get('fast_forward') is True", "msg": "fast_forward = True"},
                {"check": "merge_result.get('conflicts') == 0", "msg": "0 конфликтов"},
                {"check": "merge_result.get('commits_added') == 3", "msg": "3 новых коммита"}],
               ["Словарь: ключ -> значение", "bool True/False с большой буквы"], 1),
            ex(4, "python", "Создай функцию `is_conflict_marker(line)`: возвращает True, "
                            "если строка начинается с '<<<<<<<' или '=======' или '>>>>>>>'.",
               "def is_conflict_marker(line):\n    pass\n",
               "def is_conflict_marker(line):\n"
               "    return line.startswith('<<<<<<<') or line.startswith('=======') or line.startswith('>>>>>>>')\n",
               [{"check": "is_conflict_marker('<<<<<<< HEAD') is True", "msg": "<<<<<<< — маркер"},
                {"check": "is_conflict_marker('=======') is True", "msg": "======= — маркер"},
                {"check": "is_conflict_marker('>>>>>>> feature') is True", "msg": ">>>>>>> — маркер"},
                {"check": "is_conflict_marker('normal code') is False", "msg": "Обычный код — не маркер"}],
               ["str.startswith() проверяет начало строки", "or — логическое ИЛИ"], 2),
            ex(5, "python", "Дан `pull_request` — словарь с 'title', 'author', 'branch_from', 'branch_to', 'reviews'. "
                            "Заполни: 'Add log-transform', 'alice', 'feature/log', 'main', 2.",
               "pull_request = {}\n",
               "pull_request = {\n"
               "    'title': 'Add log-transform',\n"
               "    'author': 'alice',\n"
               "    'branch_from': 'feature/log',\n"
               "    'branch_to': 'main',\n"
               "    'reviews': 2,\n"
               "}\n",
               [{"check": "isinstance(pull_request, dict)", "msg": "Словарь"},
                {"check": "pull_request.get('branch_from') == 'feature/log'", "msg": "from: feature/log"},
                {"check": "pull_request.get('branch_to') == 'main'", "msg": "to: main"},
                {"check": "pull_request.get('reviews') == 2", "msg": "2 ревью"}],
               ["Словарь: ключ -> значение", "PR всегда идёт в main/master"], 1),
            ex(6, "python", "Создай функцию `create_branch(name)`, которая проверяет префикс "
                            "и возвращает полное имя: 'feature/' + name, если name не содержит '/'.",
               "def create_branch(name):\n    pass\n",
               "def create_branch(name):\n"
               "    if '/' in name:\n"
               "        return name\n"
               "    return 'feature/' + name\n",
               [{"check": "create_branch('lstm') == 'feature/lstm'", "msg": "lstm -> feature/lstm"},
                {"check": "create_branch('fix/bug') == 'fix/bug'", "msg": "fix/bug остаётся как есть"}],
               ["if '/' in name — проверка вхождения", "Префикс 'feature/' для простых имён"], 2),
            ex(7, "python", "Дан список веток. Создай `merged_branches` — те, что влиты в main (есть в 'merged').",
               "branches = ['main', 'feature/a', 'feature/b', 'feature/c']\n"
               "merged = ['feature/a', 'feature/c']\n"
               "merged_branches = []\n",
               "branches = ['main', 'feature/a', 'feature/b', 'feature/c']\n"
               "merged = ['feature/a', 'feature/c']\n"
               "merged_branches = [b for b in branches if b in merged and b != 'main']\n",
               [{"check": "isinstance(merged_branches, list)", "msg": "Список"},
                {"check": "'feature/a' in merged_branches and 'feature/c' in merged_branches",
                 "msg": "feature/a и feature/c"},
                {"check": "'feature/b' not in merged_branches and 'main' not in merged_branches",
                 "msg": "feature/b и main не в списке"}],
               ["List comprehension с условием", "main не считается feature-веткой"], 2),
            ex(8, "python", "Создай словарь `workflow` с этапами PR: 'open', 'review', 'ci_pass', 'merge'. "
                            "Каждому этапу — список разрешённых действий.",
               "workflow = {}\n",
               "workflow = {\n"
               "    'open': ['push commits'],\n"
               "    'review': ['comment', 'approve', 'request changes'],\n"
               "    'ci_pass': ['merge', 'close'],\n"
               "    'merge': ['delete branch'],\n"
               "}\n",
               [{"check": "isinstance(workflow, dict)", "msg": "Словарь"},
                {"check": "'merge' in workflow.get('ci_pass', [])", "msg": "merge разрешён после ci_pass"},
                {"check": "len(workflow) == 4", "msg": "4 этапа"}],
               ["Словарь: этап -> действия", "Список действий в []"], 2),
            ex(9, "python", "Создай функцию `rebase_commits(local, upstream)`, возвращающую "
                            "количество локальных коммитов, которые нужно replay'ить.",
               "def rebase_commits(local, upstream):\n    pass\n",
               "def rebase_commits(local, upstream):\n"
               "    common = min(len(local), len(upstream))\n"
               "    return max(0, len(local) - common)\n",
               [{"check": "rebase_commits(['a','b','c'], ['a']) == 2", "msg": "2 коммита для rebase"},
                {"check": "rebase_commits(['a','b'], ['a','b','c']) == 0", "msg": "0 — локально ничего нового"}],
               ["max(0, ...) — не уходить в минус", "rebase переносит только локальные коммиты"], 3),
            ex(10, "python", "Дан список конфликтов `conflicts = ['src/features.py', 'src/train.py']`. "
                             "Создай `resolution` — словарь {файл: 'resolved'}.",
               "conflicts = ['src/features.py', 'src/train.py']\nresolution = {}\n",
               "conflicts = ['src/features.py', 'src/train.py']\n"
               "resolution = {f: 'resolved' for f in conflicts}\n",
               [{"check": "isinstance(resolution, dict)", "msg": "Словарь"},
                {"check": "len(resolution) == 2", "msg": "2 файла"},
                {"check": "resolution.get('src/features.py') == 'resolved'", "msg": "features.py resolved"},
                {"check": "all(v == 'resolved' for v in resolution.values())", "msg": "Все marked resolved"}],
               ["Dict comprehension: {k: v for k in ...}", "Файл — ключ, статус — значение"], 2),
        ],
        minutes=45, difficulty=2,
    )


def _9_3():
    return lesson(
        "9.3", "Jupyter Notebooks: best practices", "neutral", [
            theory(
                "**Jupyter Notebook** — интерактивная среда для анализа данных и экспериментов. "
                "Состоит из **ячеек (cells)** двух типов: **code** (код) и **markdown** (текст/формулы).\n\n"
                "**Основные концепции:**\n"
                "- **Kernel** — вычислительное ядро, хранит состояние переменных между ячейками.\n"
                "- **Cell order** — порядок выполнения не обязан совпадать с визуальным! "
                "Можно запустить ячейку 5, потом 3, потом 7 — состояние «поедет».\n"
                "- **Magic commands** — специальные команды: `%timeit`, `%matplotlib inline`, `%%time`.\n\n"
                "**Best practices для DS:**\n"
                "1. **Сверху вниз — линейный поток.** Notebook должен запускаться "
                "`Restart & Run All` без ошибок.\n"
                "2. **Одна ячейка = один логический шаг.** Загрузка данных, EDA, фичи, модель.\n"
                "3. **Magic %load_ext autoreload** — авто-перезагрузка модулей при изменении.\n"
                "4. **Скрывайте длинный вывод** через `;` или `display.max_rows`.\n"
                "5. **Не храните данные в ноутбуке** — читайте из файла или БД.\n"
                "6. **Версионируйте**: используйте **jupytext** (.ipynb ↔ .py) или **nbstripout** "
                "(чистит output перед коммитом).\n"
                "7. **В продакшене** — переносите код из ноутбука в `.py` модули.\n\n"
                "**Частая ошибка:** «hidden state» — переменная из старой ячейки существует, "
                "но при перезапуске kernel её нет. Воспроизводимость страдает."
            ),
            analogy(
                "Notebook — лабораторный журнал учёного: каждый эксперимент пронумерован, "
                "есть дата, гипотеза, результат, выводы. Но если страницы перепутаны — "
                "журнал бесполезен.",
                "Data Scientist ведёт .ipynb как журнал экспериментов: фичи, "
                "гиперпараметры, метрики, графики. Линейный порядок = воспроизводимость."
            ),
            visual(
                "Структура ячейки и порядок выполнения",
                "+----------------------------------+\n"
                "|  In [7]:  X = pd.read_csv(...)   |   <-- ячейка 7\n"
                "+----------------------------------+\n"
                "              |\n"
                "              v\n"
                "+----------------------------------+\n"
                "|  Kernel state: {X: DataFrame}    |   <-- состояние ядра\n"
                "+----------------------------------+\n"
                "              |\n"
                "              v\n"
                "+----------------------------------+\n"
                "|  In [3]:  X.head()               |   <-- ячейка 3\n"
                "+----------------------------------+\n"
                "\n"
                "  Внимание: визуальный порядок (3, 7) "
                "НЕ равен порядку выполнения (7, 3)!"
            ),
            example(
                "Хороший заголовок DS-ноутбука: imports, конфиги, загрузка, разведочный анализ.",
                "Сверху — все импорты и seed. Дальше — функции/утилиты. Затем — данные. "
                "Markdown-ячейки разделяют смысловые блоки. В конце — выводы и метрики.",
                "# Churn Prediction — EDA\n"
                "## 1. Imports\n"
                "import numpy as np\n"
                "import pandas as pd\n"
                "import matplotlib.pyplot as plt\n"
                "SEED = 42\n"
                "np.random.seed(SEED)\n\n"
                "## 2. Загрузка\n"
                "df = pd.read_csv('data/churn.csv')\n"
                "print(f'Rows: {len(df)}, cols: {df.shape[1]}')\n\n"
                "## 3. Базовая статистика\n"
                "df.describe().T\n\n"
                "## 4. Выводы\n"
                "- 7000 клиентов, 21 признак\n"
                "- Целевая переменная: 26.5% отток\n"
                "- Пропуски в 'TotalCharges' — нужно обработать",
                "Rows: 7043, cols: 21\n"
                "         count      mean       std  ...\n"
                "tenure   7043.0  32.371...   24.55...\n"
                "MonthlyCharges  7043.0  64.76...  30.08...",
                "Markdown-ячейки дают структуру. Код — линейный. "
                "Внизу — секция 'Выводы' с конкретными числами. "
                "Restart & Run All даст тот же результат."
            ),
            common_mistakes([
                {"mistake": "Запускать ячейки в случайном порядке (out of order)",
                 "why_bad": "Hidden state: переменные из пропущенных ячеек. "
                            "При Restart & Run All всё ломается.",
                 "fix": "Периодически делай Kernel > Restart & Run All"},
                {"mistake": "Не ставить random seed",
                 "why_bad": "Результаты обучения разные при каждом запуске — "
                            "нельзя сравнить эксперименты",
                 "fix": "В первой ячейке: np.random.seed(42); torch.manual_seed(42); random.seed(42)"},
                {"mistake": "Огромный вывод (print(df.head(1000)))",
                 "why_bad": "Notebook раздувается до сотен МБ, не коммитится в Git",
                 "fix": "Ограничивай: df.head(5), используй .sample(10), pd.options.display.max_rows = 20"},
                {"mistake": "Секреты и пути в коде ноутбука",
                 "why_bad": "API-ключи утекают в GitHub, жёсткие пути ломают запуск у коллег",
                 "fix": "Используй os.environ['API_KEY'], config.yaml, относительные пути"},
                {"mistake": "Вся логика в одном гигантском .ipynb без модулей",
                 "why_bad": "Нельзя переиспользовать код, нельзя тестировать, нельзя деплоить",
                 "fix": "Логику выноси в src/, в ноутбуке — только вызовы и анализ"},
            ]),
            interview_questions([
                {"q": "Что такое hidden state в Jupyter и как с ним бороться?",
                 "a": "Hidden state — переменные, оставшиеся в kernel после удаления/изменения ячеек. "
                      "Борьба: периодический Restart & Run All, линейный поток, "
                      "вынос логики в .py модули."},
                {"q": "Зачем нужен jupytext?",
                 "a": "Jupytext синхронизирует .ipynb с .py файлом (или наоборот). "
                      "В git хранится .py — diff'ы читаемы, .ipynb не коммитится."},
                {"q": "Magic-команды `%timeit` и `%%time` — в чём разница?",
                 "a": "%timeit — line magic, применяется к одной строке. "
                      "%%time — cell magic, ко всей ячейке (пишется в начале ячейки). "
                      "Оба измеряют время выполнения."},
            ]),
            knowledge_checklist([
                "Понимаю разницу между code и markdown ячейками",
                "Делаю Kernel > Restart & Run All перед коммитом",
                "Ставлю seed в первой ячейке",
                "Использую %timeit / %matplotlib inline",
                "Ограничиваю вывод (head, sample, display options)",
                "Выношу логику в .py модули",
            ]),
        ],
        exercises=[
            ex(1, "python", "Создай словарь `cell` с типами: 'code' и 'markdown'. Заполни примером code-ячейки.",
               "cell = {}\n",
               "cell = {\n"
               "    'type': 'code',\n"
               "    'source': 'import pandas as pd\\ndf = pd.read_csv(\"data.csv\")',\n"
               "    'execution_count': 3,\n"
               "    'outputs': ['<DataFrame info>'],\n"
               "}\n",
               [{"check": "isinstance(cell, dict)", "msg": "Словарь"},
                {"check": "cell.get('type') == 'code'", "msg": "type = code"},
                {"check": "isinstance(cell.get('source'), str)", "msg": "source — строка"},
                {"check": "isinstance(cell.get('execution_count'), int)", "msg": "execution_count — int"}],
               ["Словарь: ключ -> значение", "Notebook = JSON со списком cells"], 1),
            ex(2, "python", "Создай список `cells` из 4 ячеек: 1 markdown-заголовок, 2 code, 1 markdown-вывод.",
               "cells = []\n",
               "cells = [\n"
               "    {'type': 'markdown', 'source': '# Churn EDA'},\n"
               "    {'type': 'code', 'source': 'import pandas as pd'},\n"
               "    {'type': 'code', 'source': 'df = pd.read_csv(\"churn.csv\")'},\n"
               "    {'type': 'markdown', 'source': '## Выводы: высокий отток в первый месяц'},\n"
               "]\n",
               [{"check": "isinstance(cells, list)", "msg": "Список"},
                {"check": "len(cells) == 4", "msg": "4 ячейки"},
                {"check": "sum(1 for c in cells if c['type'] == 'code') == 2", "msg": "2 code-ячейки"},
                {"check": "sum(1 for c in cells if c['type'] == 'markdown') == 2", "msg": "2 markdown-ячейки"}],
               ["List of dicts", "code и markdown — типы ячеек"], 1),
            ex(3, "python", "Создай функцию `set_seed(seed)`, которая возвращает словарь с установленными seed'ами "
                            "для numpy, random, torch (если есть) — без реальных вызовов, просто конфиг.",
               "def set_seed(seed):\n    pass\n",
               "def set_seed(seed):\n"
               "    return {\n"
               "        'numpy_seed': seed,\n"
               "        'python_seed': seed,\n"
               "        'torch_seed': seed,\n"
               "        'cuda_seed': seed,\n"
               "    }\n",
               [{"check": "isinstance(set_seed(42), dict)", "msg": "Возвращает словарь"},
                {"check": "set_seed(42).get('numpy_seed') == 42", "msg": "numpy seed = 42"},
                {"check": "set_seed(7).get('python_seed') == 7", "msg": "python seed = 7"}],
               ["Словарь с seed'ами для всех генераторов", "Один seed — везде одинаковый"], 2),
            ex(4, "python", "Создай список `best_practices` из 5 строк — правила хорошего ноутбука.",
               "best_practices = []\n",
               "best_practices = [\n"
               "    'Restart & Run All before commit',\n"
               "    'Set random seed at the top',\n"
               "    'One cell = one logical step',\n"
               "    'Use markdown for section headers',\n"
               "    'Limit output (head, sample, max_rows)',\n"
               "]\n",
               [{"check": "isinstance(best_practices, list)", "msg": "Список"},
                {"check": "len(best_practices) == 5", "msg": "5 правил"},
                {"check": "all(isinstance(s, str) for s in best_practices)", "msg": "Все — строки"}],
               ["Каждое правило — строка", "Список в []"], 1),
            ex(5, "python", "Создай функцию `is_runnable(cells)`: возвращает True, если все code-ячейки "
                            "выполняются в правильном порядке (execution_count возрастает).",
               "def is_runnable(cells):\n    pass\n",
               "def is_runnable(cells):\n"
               "    counts = [c.get('execution_count', 0) for c in cells if c.get('type') == 'code']\n"
               "    return counts == sorted(counts) and len(counts) > 0\n",
               [{"check": "is_runnable([{'type': 'code', 'execution_count': 1}, {'type': 'code', 'execution_count': 2}]) is True",
                 "msg": "1, 2 — порядок верный"},
                {"check": "is_runnable([{'type': 'code', 'execution_count': 5}, {'type': 'code', 'execution_count': 3}]) is False",
                 "msg": "5, 3 — out of order"}],
               ["execution_count монотонно растёт", "Фильтруй только code-ячейки"], 3),
            ex(6, "python", "Создай словарь `nb_metadata` для ноутбука: 'kernelspec', 'language', 'author'.",
               "nb_metadata = {}\n",
               "nb_metadata = {\n"
               "    'kernelspec': 'python3',\n"
               "    'language': 'python',\n"
               "    'author': 'alice',\n"
               "    'version': '0.1.0',\n"
               "}\n",
               [{"check": "isinstance(nb_metadata, dict)", "msg": "Словарь"},
                {"check": "nb_metadata.get('kernelspec') == 'python3'", "msg": "kernelspec python3"},
                {"check": "nb_metadata.get('language') == 'python'", "msg": "language python"}],
               ["kernelspec — какой kernel", "author — кто создал"], 1),
            ex(7, "python", "Создай функцию `strip_output(nb)`, возвращающую копию с пустым списком outputs у каждой code-ячейки.",
               "def strip_output(nb):\n    pass\n",
               "def strip_output(nb):\n"
               "    import copy\n"
               "    nb = copy.deepcopy(nb)\n"
               "    for cell in nb.get('cells', []):\n"
               "        if cell.get('cell_type') == 'code':\n"
               "            cell['outputs'] = []\n"
               "            cell['execution_count'] = None\n"
               "    return nb\n",
               [{"check": "isinstance(strip_output({'cells': []}), dict)", "msg": "Возвращает словарь"},
                {"check": "strip_output({'cells': [{'cell_type': 'code', 'outputs': [1,2,3]}]})['cells'][0]['outputs'] == []",
                 "msg": "outputs очищены"}],
               ["copy.deepcopy — глубокая копия", "outputs = [] для каждой code-ячейки"], 3),
            ex(8, "python", "Создай словарь `magic_cmds` с магическими командами: "
                            "%timeit (line), %%time (cell), %matplotlib inline, %load_ext autoreload.",
               "magic_cmds = {}\n",
               "magic_cmds = {\n"
               "    '%timeit': 'measure execution time (line)',\n"
               "    '%%time': 'measure execution time (cell)',\n"
               "    '%matplotlib inline': 'show plots in notebook',\n"
               "    '%load_ext autoreload': 'auto-reload modules',\n"
               "    '%pwd': 'print working directory',\n"
               "}\n",
               [{"check": "isinstance(magic_cmds, dict)", "msg": "Словарь"},
                {"check": "'%timeit' in magic_cmds", "msg": "%timeit в словаре"},
                {"check": "'%%time' in magic_cmds", "msg": "%%time в словаре"},
                {"check": "len(magic_cmds) >= 4", "msg": "4+ команды"}],
               ["Словарь: команда -> описание", "% — line magic, %% — cell magic"], 2),
            ex(9, "python", "Дан список экспериментов. Создай `results` — список словарей {params, metric}.",
               "experiments = [\n"
               "    {'lr': 0.01, 'epochs': 10},\n"
               "    {'lr': 0.001, 'epochs': 10},\n"
               "    {'lr': 0.01, 'epochs': 50},\n"
               "]\n"
               "results = []\n",
               "experiments = [\n"
               "    {'lr': 0.01, 'epochs': 10},\n"
               "    {'lr': 0.001, 'epochs': 10},\n"
               "    {'lr': 0.01, 'epochs': 50},\n"
               "    ]\n"
               "results = [{'params': e, 'metric': 0.85 + i * 0.02} for i, e in enumerate(experiments)]\n",
               [{"check": "isinstance(results, list)", "msg": "Список"},
                {"check": "len(results) == 3", "msg": "3 результата"},
                {"check": "all('params' in r and 'metric' in r for r in results)", "msg": "params и metric в каждом"}],
               ["List of dicts", "enumerate для индекса"], 2),
            ex(10, "python", "Создай функцию `clean_notebook(nb)`, которая убирает ячейки с тегом 'scratch'.",
               "def clean_notebook(nb):\n    pass\n",
               "def clean_notebook(nb):\n"
               "    return [c for c in nb.get('cells', []) if 'scratch' not in c.get('tags', [])]\n",
                [{"check": "isinstance(clean_notebook({'cells': []}), list)", "msg": "Возвращает список"},
                 {"check": "clean_notebook({'cells': [{'tags': ['scratch']}, {'tags': []}]}) == [{'tags': []}]",
                  "msg": "scratch-ячейка удалена"}],
                ["List comprehension с if", "tags — список меток ячейки"], 2),
        ],
        minutes=45, difficulty=2,
    )


def _9_4():
    return lesson(
        "9.4", "Структура ML-проекта", "neutral", [
            theory(
                "Хорошо структурированный ML-проект экономит часы на онбординге, "
                "отладке и деплое. Стандарт де-факто — **Cookiecutter Data Science**.\n\n"
                "**Базовые принципы:**\n"
                "1. **Separation of concerns** — данные отдельно, код отдельно, конфиги отдельно.\n"
                "2. **Src layout** — весь переиспользуемый код лежит в `src/`, а не в корне. "
                "Это позволяет импортировать как пакет и тестировать.\n"
                "3. **Notebooks — для разведки**, не для продакшена. "
                "Финальная логика — в `.py` модулях.\n"
                "4. **Данные — версионируются отдельно** (DVC, S3, DVC), не в Git.\n"
                "5. **Модели — артефакты**, лежат в `models/` (в `.gitignore`).\n\n"
                "**Типичная структура:**\n"
                "```\n"
                "project/\n"
                "├── data/             # .gitignore\n"
                "│   ├── raw/\n"
                "│   ├── processed/\n"
                "├── models/           # .gitignore\n"
                "├── notebooks/        # EDA, experiments\n"
                "├── src/              # переиспользуемый код\n"
                "│   ├── data/\n"
                "│   ├── features/\n"
                "│   ├── models/\n"
                "│   └── visualization/\n"
                "├── tests/            # unit-тесты\n"
                "├── config/           # конфиги (yaml, json)\n"
                "├── reports/          # финальные отчёты, графики\n"
                "├── .gitignore\n"
                "├── README.md\n"
                "├── requirements.txt\n"
                "└── pyproject.toml    # или setup.py\n"
                "```\n\n"
                "**`__init__.py`** в каждой подпапке `src/` делает её Python-пакетом — "
                "можно делать `from src.features import build_features`."
            ),
            analogy(
                "ML-проект — это кухня ресторана: сырьё (data/raw) отдельно, "
                "полуфабрикаты (data/processed) в холодильнике, "
                "рецепты (src/features) в картотеке, готовое блюдо (models) уходит клиенту.",
                "Data Scientist открывает проект и сразу знает, где данные, "
                "где фичи, где обучить модель — без угадывания."
            ),
            visual(
                "Структура ML-проекта (cookiecutter-style)",
                "my-ml-project/\n"
                "├── data/\n"
                "│   ├── raw/        ← исходные данные (.gitignore)\n"
                "│   ├── processed/  ← очищенные\n"
                "│   └── external/   ← внешние источники\n"
                "├── notebooks/      ← EDA, эксперименты\n"
                "├── src/            ← переиспользуемый код\n"
                "│   ├── data/       ← загрузчики\n"
                "│   ├── features/   ← feature engineering\n"
                "│   ├── models/     ← train.py, predict.py\n"
                "│   └── visualization/\n"
                "├── models/         ← .pkl, .joblib (.gitignore)\n"
                "├── tests/          ← unit-тесты\n"
                "├── reports/        ← финальные отчёты\n"
                "├── config/         ← config.yaml\n"
                "├── README.md\n"
                "└── requirements.txt"
            ),
            example(
                "Создай структуру папок и файл src/features/build_features.py.",
                "Touch-команды создают пустые папки (на практике — реальные файлы). "
                "src/features/__init__.py делает папку пакетом, build_features.py содержит функции.",
                "$ mkdir -p data/raw data/processed notebooks src/data src/features src/models tests\n"
                "$ touch src/features/__init__.py\n"
                "$ touch src/features/build_features.py\n\n"
                "# src/features/build_features.py\n"
                "import pandas as pd\n\n"
                "def add_log_features(df: pd.DataFrame) -> pd.DataFrame:\n"
                "    df = df.copy()\n"
                "    df['log_income'] = np.log1p(df['income'])\n"
                "    return df\n",
                "Создана структура:\n"
                "src/features/__init__.py\n"
                "src/features/build_features.py",
                "Папка src/features стала пакетом благодаря __init__.py. "
                "Функция add_log_features может быть вызвана из ноутбука или скрипта обучения."
            ),
            common_mistakes([
                {"mistake": "Весь код в корне проекта (model.py, train.py, data.py в корне)",
                 "why_bad": "Нельзя импортировать как пакет, путаются модули с одинаковыми именами",
                 "fix": "Перенеси в src/ и добавь __init__.py"},
                {"mistake": "Ноутбуки в корне, а финальный код в ноутбуках",
                 "why_bad": "Нет версионирования, нельзя тестировать, нельзя деплоить",
                 "fix": "EDA в notebooks/, продакшен-код в src/"},
                {"mistake": "Данные и модели в Git",
                 "why_bad": "Репозиторий раздувается, нельзя открыть в браузере, "
                            "чувствительные данные утекают",
                 "fix": "Положи в .gitignore, используй DVC или S3"},
                {"mistake": "Огромный make_pipeline.ipynb на 200 ячеек",
                 "why_bad": "Невозможно понять структуру, перезапуск ломается, "
                            "нельзя использовать функции в других проектах",
                 "fix": "Дроби на notebooks/01_eda.ipynb, 02_features.ipynb, 03_model.ipynb "
                       "и выноси логику в src/"},
                {"mistake": "Конфиги захардкожены в коде (path = '/Users/alice/data/')",
                 "why_bad": "Не запускается у коллег, в CI, в проде",
                 "fix": "Вынеси в config/config.yaml, читай через os.environ или hydra"},
            ]),
            interview_questions([
                {"q": "Зачем нужна папка src/ в ML-проекте?",
                 "a": "src/ отделяет переиспользуемый код от ноутбуков и скриптов. "
                      "Позволяет импортировать как пакет (src.features.build_features), "
                      "тестировать (pytest tests/), и не путать с корневыми скриптами."},
                {"q": "Что такое __init__.py и зачем он нужен?",
                 "a": "__init__.py делает папку Python-пакетом. Позволяет импортировать модули: "
                      "from src.features import build_features. Без него — ImportError."},
                {"q": "Где должны лежать данные в ML-проекте?",
                 "a": "В data/raw/ и data/processed/, но НЕ в Git (добавить в .gitignore). "
                      "Версионирование — через DVC, S3, Git LFS или облачные хранилища."},
            ]),
            knowledge_checklist([
                "Знаю структуру cookiecutter-data-science",
                "Отделяю код (src/) от ноутбуков (notebooks/)",
                "Данные и модели — в .gitignore",
                "Конфиги — в config/, не в коде",
                "Понимаю роль __init__.py",
            ]),
        ],
        exercises=[
            ex(1, "python", "Создай словарь `project_tree` — пары 'папка': 'описание' для 6 папок проекта.",
               "project_tree = {}\n",
               "project_tree = {\n"
               "    'data/raw': 'raw datasets, never modified',\n"
               "    'data/processed': 'cleaned, feature-engineered data',\n"
               "    'notebooks': 'EDA and experiments (.ipynb)',\n"
               "    'src': 'reusable Python code',\n"
               "    'models': 'trained model artifacts',\n"
               "    'tests': 'unit tests',\n"
               "}\n",
               [{"check": "isinstance(project_tree, dict)", "msg": "Словарь"},
                {"check": "len(project_tree) == 6", "msg": "6 папок"},
                {"check": "project_tree.get('data/raw') == 'raw datasets, never modified'",
                 "msg": "data/raw описание"},
                {"check": "'notebooks' in project_tree and 'src' in project_tree",
                 "msg": "notebooks и src присутствуют"}],
               ["Словарь: папка -> описание", "6 ключевых папок"], 1),
            ex(2, "python", "Создай список `folders` всех нужных папок (включая вложенные).",
               "folders = []\n",
               "folders = [\n"
               "    'data/raw', 'data/processed', 'data/external',\n"
               "    'notebooks', 'src/data', 'src/features',\n"
               "    'src/models', 'src/visualization',\n"
               "    'models', 'tests', 'reports', 'config',\n"
               "]\n",
               [{"check": "isinstance(folders, list)", "msg": "Список"},
                {"check": "len(folders) >= 10", "msg": "10+ папок"},
                {"check": "'data/raw' in folders and 'src/features' in folders",
                 "msg": "data/raw и src/features"},
                {"check": "all(isinstance(f, str) for f in folders)", "msg": "Все — строки"}],
               ["Список папок", "Вложенность через '/'"], 1),
            ex(3, "python", "Создай функцию `make_init_files(folders)`, возвращающую список путей к __init__.py "
                            "(по одному для каждой папки src/*).",
               "def make_init_files(folders):\n    pass\n",
               "def make_init_files(folders):\n"
               "    return [f + '/__init__.py' for f in folders if f.startswith('src/')]\n",
               [{"check": "isinstance(make_init_files(['src/data', 'src/features', 'notebooks']), list)",
                 "msg": "Возвращает список"},
                {"check": "'src/data/__init__.py' in make_init_files(['src/data'])",
                 "msg": "src/data/__init__.py"},
                {"check": "'notebooks/__init__.py' not in make_init_files(['src/data', 'notebooks'])",
                 "msg": "notebooks/__init__.py НЕ создаётся"}],
               ["List comprehension с if", "Только src/* папки получают __init__.py"], 2),
            ex(4, "python", "Создай словарь `gitignore_rules` — что игнорировать в ML-проекте (5 правил).",
               "gitignore_rules = {}\n",
               "gitignore_rules = {\n"
               "    'data': 'raw and processed data',\n"
               "    'models': 'trained model binaries',\n"
               "    '.env': 'environment variables and secrets',\n"
               "    '__pycache__': 'Python bytecode cache',\n"
               "    '.ipynb_checkpoints': 'Jupyter checkpoints',\n"
               "}\n",
               [{"check": "isinstance(gitignore_rules, dict)", "msg": "Словарь"},
                {"check": "len(gitignore_rules) == 5", "msg": "5 правил"},
                {"check": "gitignore_rules.get('data') == 'raw and processed data'", "msg": "data"},
                {"check": "gitignore_rules.get('models') == 'trained model binaries'", "msg": "models"}],
               ["Словарь: паттерн -> описание", "5 базовых правил"], 1),
            ex(5, "python", "Создай функцию `is_in_src(path)`, возвращающую True, если путь начинается с 'src/'.",
               "def is_in_src(path):\n    pass\n",
               "def is_in_src(path):\n"
               "    return path.startswith('src/')\n",
               [{"check": "is_in_src('src/features/build.py') is True", "msg": "src/features в src"},
                {"check": "is_in_src('notebooks/eda.ipynb') is False", "msg": "notebooks не в src"},
                {"check": "is_in_src('data/raw/x.csv') is False", "msg": "data не в src"}],
               ["str.startswith() проверяет префикс", "src/ — начало пути"], 1),
            ex(6, "python", "Создай список `module_paths` — пути к Python-модулям в src/.",
               "module_paths = []\n",
               "module_paths = [\n"
               "    'src/data/make_dataset.py',\n"
               "    'src/features/build_features.py',\n"
               "    'src/models/train_model.py',\n"
               "    'src/models/predict_model.py',\n"
               "    'src/visualization/visualize.py',\n"
               "]\n",
               [{"check": "isinstance(module_paths, list)", "msg": "Список"},
                {"check": "len(module_paths) >= 4", "msg": "4+ модуля"},
                {"check": "all(p.startswith('src/') and p.endswith('.py') for p in module_paths)",
                 "msg": "Все в src/ и .py"}],
               ["Список путей к .py", "Каждый в src/"], 1),
            ex(7, "python", "Дан список файлов. Создай `code_files` — только .py и .ipynb в src/ или notebooks/.",
               "files = ['src/data/load.py', 'data/raw/x.csv', 'notebooks/eda.ipynb', 'models/clf.pkl', 'src/features/build.py']\n"
               "code_files = []\n",
               "files = ['src/data/load.py', 'data/raw/x.csv', 'notebooks/eda.ipynb', 'models/clf.pkl', 'src/features/build.py']\n"
               "code_files = [f for f in files if (f.endswith('.py') or f.endswith('.ipynb')) and (f.startswith('src/') or f.startswith('notebooks/'))]\n",
               [{"check": "isinstance(code_files, list)", "msg": "Список"},
                {"check": "'src/data/load.py' in code_files", "msg": "load.py включён"},
                {"check": "'notebooks/eda.ipynb' in code_files", "msg": "eda.ipynb включён"},
                {"check": "'data/raw/x.csv' not in code_files and 'models/clf.pkl' not in code_files",
                 "msg": "csv и pkl исключены"}],
               ["endswith('.py') или endswith('.ipynb')", "startswith('src/' или 'notebooks/')"], 3),
            ex(8, "python", "Создай словарь `config` — базовый config.yaml для ML-проекта (модели, данные, обучение).",
               "config = {}\n",
               "config = {\n"
               "    'data': {'raw_path': 'data/raw/', 'processed_path': 'data/processed/'},\n"
               "    'model': {'name': 'random_forest', 'n_estimators': 100},\n"
               "    'train': {'test_size': 0.2, 'random_state': 42},\n"
               "}\n",
               [{"check": "isinstance(config, dict)", "msg": "Словарь"},
                {"check": "isinstance(config.get('data'), dict)", "msg": "data — вложенный словарь"},
                {"check": "isinstance(config.get('model'), dict)", "msg": "model — вложенный словарь"},
                {"check": "config.get('train', {}).get('random_state') == 42", "msg": "random_state = 42"}],
               ["Вложенные словари для секций", "random_state для воспроизводимости"], 2),
            ex(9, "python", "Создай функцию `list_src_init(folders)`, возвращающую __init__.py только для src-папок "
                            "(с фильтром дубликатов).",
               "def list_src_init(folders):\n    pass\n",
               "def list_src_init(folders):\n"
               "    seen = set()\n"
               "    result = []\n"
               "    for f in folders:\n"
               "        if f.startswith('src/'):\n"
               "            init_path = f + '/__init__.py'\n"
               "            if init_path not in seen:\n"
               "                seen.add(init_path)\n"
               "                result.append(init_path)\n"
               "    return result\n",
               [{"check": "isinstance(list_src_init(['src/data']), list)", "msg": "Список"},
                {"check": "'src/data/__init__.py' in list_src_init(['src/data', 'src/features'])",
                 "msg": "src/data/__init__.py"},
                {"check": "len(list_src_init(['src/data', 'src/data'])) == 1", "msg": "Дубликаты убраны"}],
               ["set для уникальности", "Только src/* префикс"], 3),
            ex(10, "python", "Создай список `stages` — этапы ML-пайплайна в правильном порядке.",
               "stages = []\n",
               "stages = [\n"
               "    'data_ingestion',\n"
               "    'data_validation',\n"
               "    'data_preprocessing',\n"
               "    'feature_engineering',\n"
               "    'model_training',\n"
               "    'model_evaluation',\n"
               "    'model_deployment',\n"
               "]\n",
               [{"check": "isinstance(stages, list)", "msg": "Список"},
                {"check": "len(stages) == 7", "msg": "7 этапов"},
                {"check": "stages[0] == 'data_ingestion'", "msg": "Первым идёт data_ingestion"},
                {"check": "stages[-1] == 'model_deployment'", "msg": "Последним — deployment"},
                {"check": "stages.index('model_training') < stages.index('model_evaluation')",
                 "msg": "training раньше evaluation"}],
                ["Этапы в правильном порядке", "index() возвращает позицию"], 2),
        ],
        minutes=50, difficulty=2,
    )


def _9_5():
    return lesson(
        "9.5", "Воспроизводимость: seeds, requirements.txt, README", "neutral", [
            theory(
                "**Воспроизводимость** — способность запустить ваш код через полгода (или у коллеги) "
                "и получить **те же результаты**. Для Data Scientist это критично: "
                "без воспроизводимости нельзя проверить эксперимент, "
                "нельзя передать проект команде, нельзя задеплоить.\n\n"
                "**Три столпа воспроизводимости:**\n\n"
                "1. **Random seeds везде**\n"
                "```python\n"
                "import random, numpy as np\n"
                "random.seed(42)\n"
                "np.random.seed(42)\n"
                "# + torch.manual_seed(42), tensorflow.random.set_seed(42)\n"
                "```\n\n"
                "2. **Зафиксированные версии библиотек**\n"
                "```\n"
                "# requirements.txt — НЕ pip freeze в начале, а проверенные версии\n"
                "numpy==1.24.3\n"
                "pandas==2.0.1\n"
                "scikit-learn==1.3.0\n"
                "```\n"
                "Оператор `==` фиксирует версию. `>=` — нет.\n\n"
                "3. **README с инструкциями**\n"
                "Хороший README содержит: что это, как поставить, как запустить, как тестировать, "
                "где данные, лицензия.\n\n"
                "**Дополнительно:** Docker (следующий урок), DVC для версионирования данных, "
                "Makefile / CLI для воспроизводимого запуска."
            ),
            analogy(
                "Воспроизводимость — это рецепт борща: если вы записали «помидоры» "
                "вместо «800 г спелых помидоров сорта Бычье сердце», никто не повторит.",
                "Data Scientist пишет: Python 3.11, pandas==2.0.1, seed=42, "
                "данные в data/raw/churn_v3.csv, команда запуска: `python src/models/train.py`."
            ),
            visual(
                "Анатомия requirements.txt: что фиксировать",
                "# requirements.txt — фиксированные версии\n"
                "\n"
                "# Core\n"
                "numpy==1.24.3          # == точная версия\n"
                "pandas==2.0.1\n"
                "scikit-learn==1.3.0\n"
                "\n"
                "# Visualization\n"
                "matplotlib==3.7.2\n"
                "seaborn==0.12.2\n"
                "\n"
                "# ИЗБЕГАЙ:\n"
                "numpy>=1.20            # слишком широкий диапазон\n"
                "pandas                 # вообще без версии\n"
                "scikit-learn==1.*      # мажорная версия плавает"
            ),
            example(
                "Полный README.md для ML-проекта churn prediction.",
                "Title → описание → как ставить → как использовать → данные → тесты → лицензия. "
                "Бейджи Travis/Coverage — опционально, но показывают зрелость проекта.",
                "# Churn Prediction\n"
                "\n"
                "![Python](https://img.shields.io/badge/python-3.11-blue)\n"
                "\n"
                "Прогноз оттока клиентов на основе истории платежей.\n"
                "\n"
                "## Установка\n"
                "```bash\n"
                "git clone https://github.com/alice/churn.git\n"
                "cd churn\n"
                "python -m venv venv && source venv/bin/activate\n"
                "pip install -r requirements.txt\n"
                "```\n"
                "\n"
                "## Использование\n"
                "```bash\n"
                "python src/models/train.py --config config/config.yaml\n"
                "```\n"
                "\n"
                "## Данные\n"
                "Положите `churn.csv` в `data/raw/`. Скачать: [ссылка].\n"
                "\n"
                "## Тесты\n"
                "```bash\n"
                "pytest tests/\n"
                "```\n"
                "\n"
                "## Лицензия\n"
                "MIT",
                "README в формате Markdown, готов для отображения на GitHub.\n"
                "Бейджи, команды, структура.",
                "README — это визитка проекта. Без него никто (включая вас через год) "
                "не разберётся, как запустить. README на GitHub рендерится автоматически."
            ),
            common_mistakes([
                {"mistake": "requirements.txt без версий (pandas, numpy)",
                 "why_bad": "Через месяц pip установит новую версию, и код может сломаться",
                 "fix": "Фиксируй версии: numpy==1.24.3, можно через pip freeze > requirements.txt"},
                {"mistake": "Использовать '>=' или '*' в версиях",
                 "why_bad": "Широкий диапазон — кто-то получит другую версию",
                 "fix": "== для продакшена, >= для библиотек (но с верхней границей)"},
                {"mistake": "Не сохранять random seed",
                 "why_bad": "Random forest, train/test split, shuffling — всё это random. "
                            "Результаты не воспроизводятся.",
                 "fix": "В начале скрипта: np.random.seed(42), в train_test_split(random_state=42)"},
                {"mistake": "README без инструкции по запуску",
                 "why_bad": "Новый разработчик не знает, с чего начать",
                 "fix": "Минимум: install, run, tests, data sources"},
                {"mistake": "Сохранять в Git абсолютные пути (/Users/alice/data/)",
                 "why_bad": "У коллеги и в CI другие пути — краш",
                 "fix": "Относительные пути + переменные окружения (DATA_DIR=$PWD/data)"},
            ]),
            interview_questions([
                {"q": "Зачем нужен random seed в DS?",
                 "a": "Чтобы получать одни и те же результаты при каждом запуске: "
                      "разбиение train/test, инициализация весов, бутстрап. "
                      "Без seed нельзя сравнить два эксперимента."},
                {"q": "В чём разница между == и >= в requirements.txt?",
                 "a": "== фиксирует точную версию (воспроизводимость). "
                      ">= указывает минимальную, допуская обновления. "
                      "Для продакшена и экспериментов — ==, для библиотек общего "
                      "назначения — >= с верхней границей."},
                {"q": "Что должно быть в README ML-проекта?",
                 "a": "Title, описание, бейджи, установка (install), запуск (usage), "
                      "откуда данные, как тестировать, лицензия. "
                      "Бонус: структура проекта, результаты экспериментов, авторы."},
            ]),
            knowledge_checklist([
                "Ставлю random seed для всех генераторов",
                "Фиксирую версии библиотек (numpy==1.24.3)",
                "Пишу requirements.txt с версиями",
                "Пишу README с инструкциями",
                "Использую относительные пути и переменные окружения",
            ]),
        ],
        exercises=[
            ex(1, "python", "Создай словарь `seeds` — seed'ы для разных библиотек.",
               "seeds = {}\n",
               "seeds = {\n"
               "    'python_random': 42,\n"
               "    'numpy': 42,\n"
               "    'torch': 42,\n"
               "    'sklearn': 42,\n"
               "}\n",
               [{"check": "isinstance(seeds, dict)", "msg": "Словарь"},
                {"check": "seeds.get('numpy') == 42", "msg": "numpy seed = 42"},
                {"check": "seeds.get('torch') == 42", "msg": "torch seed = 42"},
                {"check": "len(seeds) >= 3", "msg": "3+ библиотеки"}],
               ["Словарь: библиотека -> seed", "Один seed для всех"], 1),
            ex(2, "python", "Создай список `requirements` из 5 строк формата 'package==X.Y.Z'.",
               "requirements = []\n",
               "requirements = [\n"
               "    'numpy==1.24.3',\n"
               "    'pandas==2.0.1',\n"
               "    'scikit-learn==1.3.0',\n"
               "    'matplotlib==3.7.2',\n"
               "    'seaborn==0.12.2',\n"
               "]\n",
               [{"check": "isinstance(requirements, list)", "msg": "Список"},
                {"check": "len(requirements) == 5", "msg": "5 пакетов"},
                {"check": "all('==' in r for r in requirements)", "msg": "Все с =="},
                {"check": "all(r.count('==') == 1 for r in requirements)", "msg": "Ровно один =="}],
               ["Формат: name==X.Y.Z", "== фиксирует версию"], 1),
            ex(3, "python", "Создай функцию `parse_requirement(line)`, разбирающую 'pandas==2.0.1' в словарь.",
               "def parse_requirement(line):\n    pass\n",
               "def parse_requirement(line):\n"
               "    name, version = line.split('==')\n"
               "    return {'name': name, 'version': version}\n",
               [{"check": "isinstance(parse_requirement('numpy==1.24.3'), dict)", "msg": "Словарь"},
                {"check": "parse_requirement('numpy==1.24.3').get('name') == 'numpy'", "msg": "name"},
                {"check": "parse_requirement('numpy==1.24.3').get('version') == '1.24.3'", "msg": "version"}],
               ["str.split('==') разбивает по '=='", "Две части: name и version"], 2),
            ex(4, "python", "Создай словарь `readme_sections` — обязательные секции README.",
               "readme_sections = {}\n",
               "readme_sections = {\n"
               "    'Title': 'Project name and one-liner',\n"
               "    'Installation': 'How to install dependencies',\n"
               "    'Usage': 'How to run the code',\n"
               "    'Data': 'Where to get the data',\n"
               "    'Tests': 'How to run tests',\n"
               "    'License': 'MIT, Apache 2.0, etc.',\n"
               "}\n",
               [{"check": "isinstance(readme_sections, dict)", "msg": "Словарь"},
                {"check": "len(readme_sections) >= 5", "msg": "5+ секций"},
                {"check": "'Installation' in readme_sections", "msg": "Installation есть"},
                {"check": "'Usage' in readme_sections", "msg": "Usage есть"}],
               ["Словарь: секция -> описание", "5 базовых секций"], 1),
            ex(5, "python", "Создай функцию `is_pinned(requirement)`, возвращающую True, "
                            "если строка содержит '==' (а не '>=' или '*').",
               "def is_pinned(requirement):\n    pass\n",
               "def is_pinned(requirement):\n"
               "    return '==' in requirement and '>=' not in requirement and '*' not in requirement\n",
               [{"check": "is_pinned('numpy==1.24.3') is True", "msg": "numpy==1.24.3 pinned"},
                {"check": "is_pinned('numpy>=1.20') is False", "msg": "numpy>=1.20 NOT pinned"},
                {"check": "is_pinned('numpy==1.*') is False", "msg": "numpy==1.* NOT pinned"}],
               ["== фиксирует", ">= и * — нет", "in проверяет вхождение"], 2),
            ex(6, "python", "Создай список `cli_commands` — типичные команды для воспроизводимого запуска.",
               "cli_commands = []\n",
               "cli_commands = [\n"
               "    'python -m venv venv',\n"
               "    'source venv/bin/activate',\n"
               "    'pip install -r requirements.txt',\n"
               "    'python src/models/train.py --config config/config.yaml',\n"
               "    'pytest tests/',\n"
               "]\n",
               [{"check": "isinstance(cli_commands, list)", "msg": "Список"},
                {"check": "len(cli_commands) == 5", "msg": "5 команд"},
                {"check": "'pytest' in cli_commands[4]", "msg": "pytest последняя"},
                {"check": "'pip install' in cli_commands[2]", "msg": "pip install"}],
               ["Список shell-команд", "venv → install → run → test"], 1),
            ex(7, "python", "Дан список требований. Создай `pinned` — только зафиксированные (==).",
               "reqs = ['numpy==1.24.3', 'pandas>=2.0', 'scipy', 'sklearn==1.3.0']\n"
               "pinned = []\n",
               "reqs = ['numpy==1.24.3', 'pandas>=2.0', 'scipy', 'sklearn==1.3.0']\n"
               "pinned = [r for r in reqs if '==' in r and '>=' not in r]\n",
               [{"check": "isinstance(pinned, list)", "msg": "Список"},
                {"check": "'numpy==1.24.3' in pinned and 'sklearn==1.3.0' in pinned",
                 "msg": "== версии в списке"},
                {"check": "'pandas>=2.0' not in pinned and 'scipy' not in pinned",
                 "msg": ">= и без версии исключены"}],
               ["Фильтр: '==' in r and '>=' not in r", "List comprehension"], 2),
            ex(8, "python", "Создай функцию `make_readme(title, description)`, возвращающую строку README "
                            "с заголовком и описанием.",
               "def make_readme(title, description):\n    pass\n",
               "def make_readme(title, description):\n"
               "    return f'# {title}\\n\\n{description}\\n\\n## Installation\\npip install -r requirements.txt\\n'\n",
               [{"check": "'# Churn' in make_readme('Churn', 'Predict churn')", "msg": "Title — Churn"},
                {"check": "'## Installation' in make_readme('X', 'Y')", "msg": "Installation section"},
                {"check": "isinstance(make_readme('A', 'B'), str)", "msg": "Возвращает строку"}],
               ["f-string для шаблона", "Markdown — обычный текст"], 2),
            ex(9, "python", "Создай словарь `env_vars` — переменные окружения для проекта.",
               "env_vars = {}\n",
               "env_vars = {\n"
               "    'DATA_DIR': 'data/',\n"
               "    'MODEL_DIR': 'models/',\n"
               "    'LOG_LEVEL': 'INFO',\n"
               "    'RANDOM_SEED': '42',\n"
               "    'PYTHONHASHSEED': '42',\n"
               "}\n",
               [{"check": "isinstance(env_vars, dict)", "msg": "Словарь"},
                {"check": "env_vars.get('DATA_DIR') == 'data/'", "msg": "DATA_DIR"},
                {"check": "env_vars.get('RANDOM_SEED') == '42'", "msg": "RANDOM_SEED"},
                {"check": "env_vars.get('PYTHONHASHSEED') == '42'", "msg": "PYTHONHASHSEED"}],
               ["Словарь: имя -> значение", "PYTHONHASHSEED для хешей"], 1),
            ex(10, "python", "Создай функцию `bump_version(req, new_version)`, возвращающую строку "
                            "'package==new_version'.",
               "def bump_version(req, new_version):\n    pass\n",
               "def bump_version(req, new_version):\n"
               "    name = req.split('==')[0]\n"
               "    return f'{name}=={new_version}'\n",
               [{"check": "bump_version('numpy==1.24.3', '1.25.0') == 'numpy==1.25.0'", "msg": "1.24.3 -> 1.25.0"},
                {"check": "bump_version('pandas==2.0.1', '2.1.0') == 'pandas==2.1.0'", "msg": "2.0.1 -> 2.1.0"}],
               ["split('==')[0] — берём имя", "f-string собирает новую строку"], 2),
        ],
        minutes=40, difficulty=2,
    )


def _9_6():
    return lesson(
        "9.6", "Docker: минимальный старт для DS", "neutral", [
            theory(
                "**Docker** — платформа для упаковки приложения в **контейнер**: "
                "изолированную среду с кодом, зависимостями и системными библиотеками. "
                "Контейнер работает одинаково на вашем ноутбуке, на сервере коллеги и в облаке.\n\n"
                "**Ключевые понятия:**\n"
                "- **Image (образ)** — read-only шаблон: «как должна выглядеть среда».\n"
                "- **Container (контейнер)** — запущенный экземпляр образа.\n"
                "- **Dockerfile** — рецепт для сборки образа.\n"
                "- **Layer (слой)** — каждый шаг Dockerfile — отдельный слой; слои кэшируются.\n"
                "- **Registry (реестр)** — хранилище образов: Docker Hub, GHCR, ECR.\n\n"
                "**Базовый Dockerfile для DS:**\n"
                "```dockerfile\n"
                "# Базовый образ с Python\n"
                "FROM python:3.11-slim\n\n"
                "# Рабочая директория внутри контейнера\n"
                "WORKDIR /app\n\n"
                "# Сначала копируем requirements для кэширования слоя\n"
                "COPY requirements.txt .\n"
                "RUN pip install --no-cache-dir -r requirements.txt\n\n"
                "# Копируем код\n"
                "COPY src/ ./src/\n"
                "COPY config/ ./config/\n\n"
                "# Запуск\n"
                "CMD [\"python\", \"src/models/train.py\"]\n"
                "```\n\n"
                "**Основные команды:**\n"
                "```\n"
                "docker build -t my-model:v1 .    # собрать образ\n"
                "docker run my-model:v1          # запустить контейнер\n"
                "docker run -p 8000:8000 my-api   # проброс порта\n"
                "docker images                   # список образов\n"
                "docker ps                       # запущенные контейнеры\n"
                "```\n\n"
                "**Для DS особенно важно:** одинаковая среда на всех машинах, "
                "воспроизводимость экспериментов, удобный деплой ML-моделей."
            ),
            analogy(
                "Docker-образ — это консервы: банка запечатана (read-only), "
                "содержит всё нужное (код + библиотеки), одинаковая в любом магазине (registry). "
                "Открыл — получил контейнер (запущенный процесс).",
                "Data Scientist пакует обученную модель + Python + sklearn + код в один образ, "
                "и тот одинаково работает на его Mac, на сервере заказчика и в Kubernetes."
            ),
            visual(
                "Docker: слои образа и связь с контейнером",
                "+----------------------------------+\n"
                "|  Layer 5: COPY src/ ./src/       |   <-- ваш код\n"
                "+----------------------------------+\n"
                "|  Layer 4: COPY requirements.txt  |\n"
                "+----------------------------------+\n"
                "|  Layer 3: RUN pip install ...    |   <-- библиотеки\n"
                "+----------------------------------+\n"
                "|  Layer 2: WORKDIR /app           |\n"
                "+----------------------------------+\n"
                "|  Layer 1: FROM python:3.11-slim  |   <-- базовый Python\n"
                "+----------------------------------+\n"
                "  |\n"
                "  v\n"
                "  Image  =  read-only слои\n"
                "  Container = Image + writable layer (изменения runtime)"
            ),
            example(
                "Собери и запусти ML-сервис в Docker.",
                "docker build собирает образ по Dockerfile. -t даёт имя и тег. "
                "docker run запускает контейнер. -p 8000:8000 пробрасывает порт "
                "хоста на порт контейнера (для API).",
                "# Dockerfile\n"
                "FROM python:3.11-slim\n"
                "WORKDIR /app\n"
                "COPY requirements.txt .\n"
                "RUN pip install -r requirements.txt\n"
                "COPY src/ ./src/\n"
                "EXPOSE 8000\n"
                "CMD [\"uvicorn\", \"src.api.app:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]\n\n"
                "# Сборка и запуск\n"
                "$ docker build -t churn-api:v1 .\n"
                "Successfully built a1b2c3\n\n"
                "$ docker run -d -p 8000:8000 --name api churn-api:v1\n"
                "5d4e3f2a1b...\n\n"
                "$ curl http://localhost:8000/health\n"
                "{\"status\": \"ok\"}",
                "Successfully built a1b2c3\n"
                "5d4e3f2a1b...\n"
                "{\"status\": \"ok\"}",
                "Образ churn-api:v1 собран. Контейнер запущен в фоне (-d), "
                "порт 8000 проброшен. Healthcheck вернул OK. "
                "Код, зависимости и среда полностью изолированы внутри."
            ),
            common_mistakes([
                {"mistake": "Использовать образ ubuntu:latest как базовый",
                 "why_bad": "Огромный (1+ ГБ), включает ненужные пакеты, медленный pip install",
                 "fix": "python:3.11-slim (~150 МБ) или python:3.11-alpine (~50 МБ)"},
                {"mistake": "Не использовать .dockerignore",
                 "why_bad": "В образ попадает .git, .env, __pycache__, .ipynb_checkpoints — "
                            "образ раздувается, возможна утечка секретов",
                 "fix": "Создай .dockerignore: .git, .env, __pycache__, *.ipynb, data/, models/"},
                {"mistake": "Копировать всё в один слой COPY . .",
                 "why_bad": "При любом изменении кода пересобирается ВСЁ: pip install с нуля",
                 "fix": "Сначала COPY requirements.txt + RUN pip install, потом COPY src/"},
                {"mistake": "Запускать процесс от root внутри контейнера",
                 "why_bad": "Уязвимость: если атакующий пролезет, он получит root контейнера",
                 "fix": "USER nonroot или USER 1000 в Dockerfile"},
                {"mistake": "Держать данные внутри контейнера",
                 "why_bad": "Контейнер эфемерен — данные пропадут при удалении",
                 "fix": "Volumes: -v /host/path:/container/path или named volumes"},
            ]),
            interview_questions([
                {"q": "Чем Docker отличается от виртуальной машины?",
                 "a": "VM эмулирует hardware (гипервизор, своё ядро ОС, ГБ ОЗУ). "
                      "Docker делит ядро с хостом, изолирует через namespaces/cgroups, "
                      "запускается за секунды, весит десятки/сотни МБ."},
                {"q": "Что такое слои (layers) в Docker?",
                 "a": "Каждый шаг Dockerfile создаёт read-only слой. Слои кэшируются: "
                      "если requirements.txt не менялся, повторный docker build не "
                      "запускает pip install. Это ускоряет сборку."},
                {"q": "Зачем нужен .dockerignore?",
                 "a": "Аналог .gitignore, но для docker build context. Исключает .git, "
                      ".env, __pycache__, большие данные из образа — ускоряет сборку, "
                      "уменьшает размер, защищает секреты."},
            ]),
            knowledge_checklist([
                "Понимаю разницу image vs container",
                "Пишу Dockerfile с базовым образом",
                "Использую WORKDIR, COPY, RUN, CMD",
                "Пробрасываю порты через -p",
                "Использую .dockerignore",
                "Понимаю слои и кэширование",
            ]),
        ],
        exercises=[
            ex(1, "python", "Создай словарь `docker_config` с ключами 'image', 'ports', 'env', 'volumes'.",
               "docker_config = {}\n",
               "docker_config = {\n"
               "    'image': 'python:3.11-slim',\n"
               "    'ports': {'8000': 8000},\n"
               "    'env': {'ENV': 'production', 'LOG_LEVEL': 'INFO'},\n"
               "    'volumes': {'./data': '/app/data'},\n"
               "}\n",
               [{"check": "isinstance(docker_config, dict)", "msg": "Словарь"},
                {"check": "docker_config.get('image', '').startswith('python')", "msg": "Python-образ"},
                {"check": "isinstance(docker_config.get('ports'), dict)", "msg": "ports — словарь"},
                {"check": "docker_config.get('ports', {}).get('8000') == 8000", "msg": "8000:8000"}],
               ["Ключи — строки в кавычках", "ports — словарь host:container"], 1),
            ex(2, "python", "Создай список `dockerfile_lines` — строки простого Dockerfile (FROM, WORKDIR, COPY, RUN, CMD).",
               "dockerfile_lines = []\n",
               "dockerfile_lines = [\n"
               "    'FROM python:3.11-slim',\n"
               "    'WORKDIR /app',\n"
               "    'COPY requirements.txt .',\n"
               "    'RUN pip install --no-cache-dir -r requirements.txt',\n"
               "    'COPY src/ ./src/',\n"
               "    'CMD [\"python\", \"src/models/train.py\"]',\n"
               "]\n",
               [{"check": "isinstance(dockerfile_lines, list)", "msg": "Список"},
                {"check": "len(dockerfile_lines) >= 5", "msg": "5+ строк"},
                {"check": "any('FROM' in l for l in dockerfile_lines)", "msg": "FROM есть"},
                {"check": "any('CMD' in l for l in dockerfile_lines)", "msg": "CMD есть"},
                {"check": "any('pip install' in l for l in dockerfile_lines)", "msg": "pip install есть"}],
               ["Каждая строка — отдельная инструкция", "FROM — базовый образ"], 1),
            ex(3, "python", "Создай функцию `parse_dockerfile(lines)`, возвращающую словарь "
                            "{FROM, WORKDIR, COPY, RUN, CMD}.",
               "def parse_dockerfile(lines):\n    pass\n",
               "def parse_dockerfile(lines):\n"
               "    result = {}\n"
               "    for line in lines:\n"
               "        instr = line.split()[0]\n"
               "        if instr in {'FROM', 'WORKDIR', 'COPY', 'RUN', 'CMD'}:\n"
               "            result[instr] = line\n"
               "    return result\n",
               [{"check": "isinstance(parse_dockerfile(['FROM python:3.11']), dict)", "msg": "Словарь"},
                {"check": "'FROM' in parse_dockerfile(['FROM python:3.11'])", "msg": "FROM в словаре"},
                {"check": "parse_dockerfile(['FROM x', 'WORKDIR /app']).get('WORKDIR') == 'WORKDIR /app'",
                 "msg": "WORKDIR извлечён"}],
               ["split()[0] — первое слово", "Проверяем, что инструкция известна"], 3),
            ex(4, "python", "Создай словарь `layers` — шаги Dockerfile и их назначение.",
               "layers = {}\n",
               "layers = {\n"
               "    'FROM': 'base image (python:3.11-slim)',\n"
               "    'WORKDIR': 'set working directory inside container',\n"
               "    'COPY requirements.txt': 'copy dependencies file',\n"
               "    'RUN pip install': 'install python packages',\n"
               "    'COPY src/': 'copy application code',\n"
               "    'CMD': 'default command to run',\n"
               "}\n",
               [{"check": "isinstance(layers, dict)", "msg": "Словарь"},
                {"check": "layers.get('FROM') == 'base image (python:3.11-slim)'", "msg": "FROM"},
                {"check": "layers.get('WORKDIR') == 'set working directory inside container'", "msg": "WORKDIR"}],
               ["Словарь: шаг -> описание", "6 базовых шагов"], 1),
            ex(5, "python", "Создай функцию `image_size_mb(layers_sizes)`, считающую суммарный размер слоёв в МБ.",
               "def image_size_mb(layers_sizes):\n    pass\n",
               "def image_size_mb(layers_sizes):\n"
               "    return sum(layers_sizes)\n",
               [{"check": "image_size_mb([100, 50, 30]) == 180", "msg": "180 МБ"},
                {"check": "image_size_mb([]) == 0", "msg": "Пустой список = 0"}],
               ["sum() для суммы", "Размеры в МБ"], 1),
            ex(6, "python", "Создай список `dockerignore` — содержимое .dockerignore (минимум 5 строк).",
               "dockerignore = []\n",
               "dockerignore = [\n"
               "    '.git',\n"
               "    '.env',\n"
               "    '__pycache__',\n"
               "    '*.pyc',\n"
               "    '.ipynb_checkpoints',\n"
               "    'data/raw/',\n"
               "    'models/',\n"
               "    'tests/',\n"
               "    '.venv',\n"
               "]\n",
               [{"check": "isinstance(dockerignore, list)", "msg": "Список"},
                {"check": "len(dockerignore) >= 5", "msg": "5+ строк"},
                {"check": "'.git' in dockerignore", "msg": ".git"},
                {"check": "'.env' in dockerignore", "msg": ".env"},
                {"check": "'__pycache__' in dockerignore", "msg": "__pycache__"}],
               ["Список шаблонов", ".git, .env, __pycache__ обязательно"], 1),
            ex(7, "python", "Создай функцию `port_mapping(host_port, container_port)`, возвращающую строку 'H:C'.",
               "def port_mapping(host_port, container_port):\n    pass\n",
               "def port_mapping(host_port, container_port):\n"
               "    return f'{host_port}:{container_port}'\n",
               [{"check": "port_mapping(8000, 8000) == '8000:8000'", "msg": "8000:8000"},
                {"check": "port_mapping(5000, 80) == '5000:80'", "msg": "5000:80"}],
               ["f-string с двоеточием", "host:container"], 1),
            ex(8, "python", "Дан список команд. Создай `images` — только успешные docker build (без 'Error').",
               "logs = ['Step 1/3 : FROM python:3.11', 'Step 2/3 : WORKDIR /app', 'Error: not found', 'Successfully built a1b2c3']\n"
               "successful = []\n",
               "logs = ['Step 1/3 : FROM python:3.11', 'Step 2/3 : WORKDIR /app', 'Error: not found', 'Successfully built a1b2c3']\n"
               "successful = [l for l in logs if 'Error' not in l and 'Successfully' in l]\n",
               [{"check": "isinstance(successful, list)", "msg": "Список"},
                {"check": "'Successfully built a1b2c3' in successful", "msg": "Successfully есть"},
                {"check": "len(successful) == 1", "msg": "Только 1 успешный"}],
               ["Фильтр: 'Error' not in l and 'Successfully' in l", "Только итоговая строка"], 2),
            ex(9, "python", "Создай словарь `container` — состояние контейнера: id, image, status, ports.",
               "container = {}\n",
               "container = {\n"
               "    'id': '5d4e3f2a1b',\n"
               "    'image': 'churn-api:v1',\n"
               "    'status': 'running',\n"
               "    'ports': '0.0.0.0:8000->8000/tcp',\n"
               "}\n",
               [{"check": "isinstance(container, dict)", "msg": "Словарь"},
                {"check": "container.get('status') == 'running'", "msg": "running"},
                {"check": "'8000' in container.get('ports', '')", "msg": "8000 в ports"},
                {"check": "container.get('image', '').startswith('churn')", "msg": "churn-образ"}],
               ["Словарь: поле -> значение", "status: running/stopped/exited"], 1),
            ex(10, "python", "Создай функцию `docker_run_cmd(image, port=None, volume=None)`, "
                            "возвращающую список аргументов для docker run.",
               "def docker_run_cmd(image, port=None, volume=None):\n    pass\n",
               "def docker_run_cmd(image, port=None, volume=None):\n"
               "    cmd = ['docker', 'run', '-d', image]\n"
               "    if port:\n"
               "        cmd[2:2] = ['-p', f'{port}:{port}']\n"
               "    if volume:\n"
               "        cmd[2:2] = ['-v', volume]\n"
               "    return cmd\n",
               [{"check": "isinstance(docker_run_cmd('img'), list)", "msg": "Список"},
                {"check": "'docker' in docker_run_cmd('img') and 'img' in docker_run_cmd('img')",
                 "msg": "docker run img"},
                {"check": "'-p' in docker_run_cmd('img', port=8000)", "msg": "-p при port"}],
               ["list.insert() для вставки", "Базовый cmd + опции"], 3),
        ],
        minutes=50, difficulty=3,
    )


def _9_7():
    return lesson(
        "9.7", "Основы MLOps: эксперименты, версионирование", "neutral", [
            theory(
                "**MLOps** — практика внедрения и поддержки ML-моделей в продакшене. "
                "Это DevOps + Data Science + мониторинг.\n\n"
                "**Главные проблемы без MLOps:**\n"
                "1. Непонятно, какая версия модели в проде\n"
                "2. Нельзя воспроизвести результат эксперимента\n"
                "3. Развёртывание занимает недели\n"
                "4. Нет мониторинга деградации модели\n\n"
                "**Основные компоненты:**\n\n"
                "**1. Трекинг экспериментов (Experiment Tracking)**\n"
                "Каждый запуск сохраняет: параметры, метрики, артефакты, версию кода, "
                "датасет. Инструменты: **MLflow**, Weights & Biases, Neptune, ClearML.\n\n"
                "**Пример с MLflow:**\n"
                "```python\n"
                "import mlflow\n"
                "mlflow.set_experiment('churn')\n"
                "with mlflow.start_run():\n"
                "    mlflow.log_param('n_estimators', 100)\n"
                "    mlflow.log_metric('accuracy', 0.92)\n"
                "    mlflow.sklearn.log_model(model, 'model')\n"
                "```\n\n"
                "**2. Версионирование данных (Data Versioning)**\n"
                "Git хранит код, но не данные. Для данных: **DVC** (Data Version Control), "
                "Pachyderm, Delta Lake. DVC хранит хеши файлов в Git, а сами файлы в S3/GDrive.\n\n"
                "**3. Model Registry**\n"
                "Центральное хранилище моделей со стадиями: None → Staging → Production → Archived. "
                "MLflow Model Registry, BentoML, SageMaker.\n\n"
                "**4. CI/CD для ML**\n"
                "GitHub Actions / GitLab CI запускают тесты, переобучают модель, "
                "деплоят, если метрики лучше предыдущей."
            ),
            analogy(
                "MLOps — это ресторанный бизнес: эксперимент = проба нового блюда шеф-поваром, "
                "трекинг = книга рецептов с датами, model registry = меню, "
                "а CI/CD = конвейер, который готовит и подаёт блюдо гостям.",
                "Data Scientist логирует эксперименты, лучшую модель регистрирует, "
                "CI пайплайн деплоит её в прод, а мониторинг следит за качеством."
            ),
            visual(
                "MLflow Tracking: UI с экспериментами",
                "+--------------------------------------------------+\n"
                "|  Experiments: churn-prediction                   |\n"
                "+--------------------------------------------------+\n"
                "|  Run ID  | n_est | max_depth | accuracy | F1    |\n"
                "+----------+-------+-----------+----------+-------+\n"
                "|  a1b2c3  | 100   | 5         | 0.910    | 0.870 |\n"
                "|  d4e5f6  | 200   | 10        | 0.920    | 0.885 |\n"
                "|  g7h8i9  | 200   | 15        | 0.925    | 0.890 | <-- best\n"
                "+--------------------------------------------------+\n"
                "  mlflow ui → http://localhost:5000"
            ),
            example(
                "Запуск эксперимента в MLflow с логированием параметров, метрик и модели.",
                "mlflow.set_experiment создаёт эксперимент. start_run() — контекст, "
                "log_param/log_metric логируют. log_model — артефакт (модель). "
                "UI покажет таблицу со всеми запусками.",
                "import mlflow\n"
                "import mlflow.sklearn\n"
                "from sklearn.ensemble import RandomForestClassifier\n"
                "from sklearn.metrics import accuracy_score\n\n"
                "mlflow.set_experiment('churn')\n\n"
                "with mlflow.start_run(run_name='rf-v1'):\n"
                "    params = {'n_estimators': 200, 'max_depth': 10, 'random_state': 42}\n"
                "    mlflow.log_params(params)\n\n"
                "    model = RandomForestClassifier(**params)\n"
                "    model.fit(X_train, y_train)\n"
                "    preds = model.predict(X_test)\n"
                "    acc = accuracy_score(y_test, preds)\n"
                "    mlflow.log_metric('accuracy', acc)\n"
                "    mlflow.sklearn.log_model(model, 'model')\n\n"
                "print(f'Run ID: {mlflow.active_run().info.run_id}, acc={acc:.3f}')",
                "Run ID: g7h8i9j0k1l2, acc=0.925",
                "Параметры и метрики сохранены в MLflow. Модель — как артефакт. "
                "Можно открыть mlflow ui и сравнить запуски."
            ),
            common_mistakes([
                {"mistake": "Не логировать параметры эксперимента",
                 "why_bad": "Через месяц непонятно, какие гиперпараметры дали лучший результат",
                 "fix": "mlflow.log_params({...}) в начале каждого запуска"},
                {"mistake": "Хранить модели в Git (model.pkl в репо)",
                 "why_bad": "Репозиторий раздувается, нет версионирования моделей",
                 "fix": "mlflow.sklearn.log_model() или DVC для версионирования"},
                {"mistake": "Нет версионирования данных",
                 "why_bad": "Нельзя воспроизвести: «обучил на старых данных, уже нет»",
                 "fix": "DVC: dvc add data/raw/churn.csv; dvc push"},
                {"mistake": "Деплой модели без тестов",
                 "why_bad": "Сломанная модель уходит в прод, никто не замечает",
                 "fix": "CI: pytest + проверка метрик > baseline, иначе блокировать деплой"},
                {"mistake": "Нет мониторинга в проде",
                 "why_bad": "Модель деградирует из-за data drift, никто не замечает неделями",
                 "fix": "Логируй входные данные и предсказания, отслеживай распределения"},
            ]),
            interview_questions([
                {"q": "Что такое experiment tracking и зачем он нужен?",
                 "a": "Experiment tracking — запись параметров, метрик, артефактов и кода "
                      "каждого запуска модели. Нужен для: сравнения экспериментов, "
                      "воспроизводимости, аудита. Инструменты: MLflow, W&B."},
                {"q": "Чем DVC отличается от Git?",
                 "a": "Git версионирует только текст (код). DVC версионирует данные и модели: "
                      "в Git хранит .dvc файлы с хешами, сами файлы — в S3/GDrive/S3. "
                      "dvc add/dvc push/dvc pull аналогичны git add/commit/push."},
                {"q": "Что такое model registry?",
                 "a": "Центральное хранилище моделей со стадиями (Staging, Production, Archived). "
                      "Позволяет отслеживать, какая версия модели в проде, откатываться, "
                      "сравнивать кандидатов на деплой."},
            ]),
            knowledge_checklist([
                "Логирую параметры и метрики (mlflow.log_params/metrics)",
                "Сохраняю модели как артефакты",
                "Понимаю, что Git не для данных и моделей",
                "Знаю про DVC для версионирования данных",
                "Использую seed для воспроизводимости",
                "Понимаю стадии model registry (Staging → Production)",
            ]),
        ],
        exercises=[
            ex(1, "python", "Создай словарь `experiment` — запись об эксперименте: params, metrics, run_id, model_uri.",
               "experiment = {}\n",
               "experiment = {\n"
               "    'run_id': 'g7h8i9j0',\n"
               "    'params': {'n_estimators': 200, 'max_depth': 10},\n"
               "    'metrics': {'accuracy': 0.92, 'f1': 0.88},\n"
               "    'model_uri': 'runs:/g7h8i9j0/model',\n"
               "}\n",
               [{"check": "isinstance(experiment, dict)", "msg": "Словарь"},
                {"check": "isinstance(experiment.get('params'), dict)", "msg": "params — словарь"},
                {"check": "isinstance(experiment.get('metrics'), dict)", "msg": "metrics — словарь"},
                {"check": "experiment.get('metrics', {}).get('accuracy') == 0.92", "msg": "accuracy = 0.92"}],
               ["Словарь: поле -> значение", "params и metrics — вложенные словари"], 1),
            ex(2, "python", "Создай список `runs` из 3 экспериментов с разными accuracy (0.85, 0.90, 0.88).",
               "runs = []\n",
               "runs = [\n"
               "    {'run_id': 'a1b2', 'accuracy': 0.85, 'n_estimators': 100},\n"
               "    {'run_id': 'c3d4', 'accuracy': 0.90, 'n_estimators': 200},\n"
               "    {'run_id': 'e5f6', 'accuracy': 0.88, 'n_estimators': 150},\n"
               "]\n",
               [{"check": "isinstance(runs, list)", "msg": "Список"},
                {"check": "len(runs) == 3", "msg": "3 запуска"},
                {"check": "all(isinstance(r, dict) for r in runs)", "msg": "Все — словари"},
                {"check": "all('accuracy' in r for r in runs)", "msg": "У всех есть accuracy"}],
               ["Список словарей", "Каждый запуск — отдельный dict"], 1),
            ex(3, "python", "Создай функцию `best_run(runs)`, возвращающую запуск с максимальной accuracy.",
               "def best_run(runs):\n    pass\n",
               "def best_run(runs):\n"
               "    return max(runs, key=lambda r: r.get('accuracy', 0))\n",
               [{"check": "isinstance(best_run([{'accuracy': 0.9}]), dict)", "msg": "Словарь"},
                {"check": "best_run([{'accuracy': 0.8}, {'accuracy': 0.95}]).get('accuracy') == 0.95",
                 "msg": "0.95 побеждает"},
                {"check": "best_run([{'accuracy': 0.7}, {'accuracy': 0.85}, {'accuracy': 0.6}]).get('accuracy') == 0.85",
                 "msg": "0.85 — лучшая из трёх"}],
               ["max(..., key=lambda r: r['accuracy'])", "lambda — анонимная функция"], 2),
            ex(4, "python", "Создай словарь `model_stages` — стадии model registry и их описание.",
               "model_stages = {}\n",
               "model_stages = {\n"
               "    'None': 'newly registered, not yet validated',\n"
               "    'Staging': 'testing in pre-production environment',\n"
               "    'Production': 'live, serving predictions',\n"
               "    'Archived': 'retired, kept for audit',\n"
               "}\n",
               [{"check": "isinstance(model_stages, dict)", "msg": "Словарь"},
                {"check": "len(model_stages) == 4", "msg": "4 стадии"},
                {"check": "'Production' in model_stages", "msg": "Production есть"},
                {"check": "model_stages.get('Staging') == 'testing in pre-production environment'",
                 "msg": "Staging описание"}],
               ["Словарь: стадия -> описание", "None → Staging → Production → Archived"], 1),
            ex(5, "python", "Создай функцию `transition_stage(current, target)`, возвращающую словарь "
                            "{from, to, allowed: bool}. target='Production' разрешён только из 'Staging'.",
               "def transition_stage(current, target):\n    pass\n",
               "def transition_stage(current, target):\n"
               "    allowed = (current == 'Staging' and target == 'Production')\n"
               "    return {'from': current, 'to': target, 'allowed': allowed}\n",
               [{"check": "isinstance(transition_stage('None', 'Staging'), dict)", "msg": "Словарь"},
                {"check": "transition_stage('Staging', 'Production').get('allowed') is True",
                 "msg": "Staging → Production: allowed"},
                {"check": "transition_stage('None', 'Production').get('allowed') is False",
                 "msg": "None → Production: NOT allowed"}],
               ["Словарь с from/to/allowed", "Проверяем переход"], 3),
            ex(6, "python", "Создай список `dvc_commands` — основные команды DVC.",
               "dvc_commands = []\n",
               "dvc_commands = [\n"
               "    'dvc init',\n"
               "    'dvc add data/raw/churn.csv',\n"
               "    'dvc remote add -d storage s3://bucket/dvc',\n"
               "    'dvc push',\n"
               "    'dvc pull',\n"
               "    'git add data/raw/churn.csv.dvc .gitignore',\n"
               "]\n",
               [{"check": "isinstance(dvc_commands, list)", "msg": "Список"},
                {"check": "len(dvc_commands) >= 5", "msg": "5+ команд"},
                {"check": "'dvc init' in dvc_commands", "msg": "dvc init"},
                {"check": "'dvc push' in dvc_commands and 'dvc pull' in dvc_commands",
                 "msg": "push и pull"}],
               ["Список команд", "init → add → push/pull"], 1),
            ex(7, "python", "Создай словарь `metrics_history` — история метрик во времени: 3 записи с timestamp.",
               "metrics_history = []\n",
               "metrics_history = [\n"
               "    {'timestamp': '2026-01-15T10:00', 'accuracy': 0.85, 'run_id': 'a1b2'},\n"
               "    {'timestamp': '2026-02-20T14:00', 'accuracy': 0.90, 'run_id': 'c3d4'},\n"
               "    {'timestamp': '2026-05-10T09:00', 'accuracy': 0.92, 'run_id': 'e5f6'},\n"
               "]\n",
               [{"check": "isinstance(metrics_history, list)", "msg": "Список"},
                {"check": "len(metrics_history) == 3", "msg": "3 записи"},
                {"check": "all('timestamp' in m and 'accuracy' in m for m in metrics_history)",
                 "msg": "У всех timestamp и accuracy"}],
               ["Список словарей", "Каждая запись — снимок метрик"], 1),
            ex(8, "python", "Создай функцию `avg_metric(metrics_history)`, считающую среднее accuracy.",
               "def avg_metric(metrics_history):\n    pass\n",
               "def avg_metric(metrics_history):\n"
               "    accs = [m['accuracy'] for m in metrics_history]\n"
               "    return sum(accs) / len(accs) if accs else 0\n",
               [{"check": "abs(avg_metric([{'accuracy': 0.8}, {'accuracy': 0.9}]) - 0.85) < 1e-6",
                 "msg": "Среднее 0.85"},
                {"check": "avg_metric([]) == 0", "msg": "Пустой список = 0"}],
               ["List comprehension для извлечения", "sum/len для среднего"], 2),
            ex(9, "python", "Создай словарь `pipeline_stage` — стадия CI/CD пайплайна: name, scripts, required.",
               "pipeline_stage = {}\n",
               "pipeline_stage = {\n"
               "    'name': 'test',\n"
               "    'scripts': ['pytest tests/', 'flake8 src/'],\n"
               "    'required': True,\n"
               "}\n",
               [{"check": "isinstance(pipeline_stage, dict)", "msg": "Словарь"},
                {"check": "isinstance(pipeline_stage.get('scripts'), list)", "msg": "scripts — список"},
                {"check": "pipeline_stage.get('required') is True", "msg": "required = True"},
                {"check": "any('pytest' in s for s in pipeline_stage.get('scripts', []))",
                 "msg": "pytest в scripts"}],
               ["Словарь: name/scripts/required", "required: блокирует дальнейшие стадии"], 2),
            ex(10, "python", "Создай функцию `should_deploy(metrics, baseline)`, возвращающую True, "
                            "если accuracy > baseline.",
               "def should_deploy(metrics, baseline):\n    pass\n",
               "def should_deploy(metrics, baseline):\n"
               "    return metrics.get('accuracy', 0) > baseline\n",
               [{"check": "should_deploy({'accuracy': 0.9}, 0.85) is True", "msg": "0.9 > 0.85"},
                {"check": "should_deploy({'accuracy': 0.8}, 0.85) is False", "msg": "0.8 < 0.85"},
                {"check": "should_deploy({}, 0.5) is False", "msg": "Пустые метрики = False"}],
               ["dict.get() с дефолтом", "Сравнение >"], 1),
        ],
        minutes=50, difficulty=3,
    )


def _9_8():
    return lesson(
        "9.8", "Мини-проект: Оформить проект по стандартам GitHub", "neutral", [
            theory(
                "В этом мини-проекте вы примените всё из блока 9: "
                "соберёте «правильный» ML-проект — со структурой, Git, "
                "requirements, README, .gitignore, seed'ами и логированием эксперимента.\n\n"
                "**Чек-лист «production-ready» DS-проекта:**\n\n"
                "1. **Структура** — `data/`, `notebooks/`, `src/`, `tests/`, `config/`, `models/`, `reports/`.\n"
                "2. **`.gitignore`** — исключает `__pycache__/`, `*.pyc`, `.ipynb_checkpoints`, `data/`, `models/`, `.env`.\n"
                "3. **`requirements.txt`** — зафиксированные версии (`numpy==1.24.3`).\n"
                "4. **`README.md`** — описание, установка, запуск, тесты, данные, лицензия.\n"
                "5. **`config/config.yaml`** — параметры обучения, пути, гиперпараметры.\n"
                "6. **Random seed** в каждом скрипте (numpy, random, torch).\n"
                "7. **Логирование эксперимента** (MLflow или JSON-файл с метриками).\n"
                "8. **`src/` layout** с `__init__.py` в подпапках.\n"
                "9. **Git-ветки** для фич, осмысленные коммиты.\n"
                "10. **(Опционально) Dockerfile** для контейнеризации.\n\n"
                "**Что вы создадите:**\n"
                "Полную спецификацию проекта в виде Python-словарей и списков: "
                "структуру папок, конфиги, README, requirements, описание эксперимента."
            ),
            analogy(
                "Production-ready проект — это паспорт гражданина: имя, адрес, документы, "
                "правила. Без паспорта вас не пустят в продакшен.",
                "Data Scientist сдаёт ML-проект как инженер сдаёт здание: с проектом, "
                "документацией, тестами и инструкцией по эксплуатации."
            ),
            visual(
                "Финальная структура production-ready ML-проекта",
                "churn-prediction/\n"
                "├── data/                    ← данные (.gitignore)\n"
                "│   ├── raw/\n"
                "│   └── processed/\n"
                "├── models/                  ← обученные модели (.gitignore)\n"
                "├── notebooks/\n"
                "│   ├── 01_eda.ipynb\n"
                "│   └── 02_experiments.ipynb\n"
                "├── src/\n"
                "│   ├── __init__.py\n"
                "│   ├── data/__init__.py + make_dataset.py\n"
                "│   ├── features/__init__.py + build_features.py\n"
                "│   ├── models/__init__.py + train_model.py + predict_model.py\n"
                "│   └── visualization/__init__.py + visualize.py\n"
                "├── tests/\n"
                "├── reports/                 ← графики, метрики\n"
                "├── config/config.yaml\n"
                "├── .gitignore\n"
                "├── README.md\n"
                "├── requirements.txt\n"
                "├── Dockerfile\n"
                "└── .dvc/                    ← DVC метаданные"
            ),
            example(
                "Полная спецификация проекта churn-prediction: метаданные, структура, конфиг, эксперимент.",
                "Собираем всё в один словарь `project` со вложенными секциями: structure, "
                "dependencies, gitignore, readme_sections, config, experiment. "
                "Это шаблон для реального проекта — можно положить в project.json и генерировать README.",
                "project = {\n"
                "    'name': 'churn-prediction',\n"
                "    'version': '1.0.0',\n"
                "    'python': '3.11',\n"
                "    'license': 'MIT',\n"
                "    'author': 'alice',\n"
                "    'structure': {\n"
                "        'data': ['raw', 'processed'],\n"
                "        'src': ['data', 'features', 'models', 'visualization'],\n"
                "    },\n"
                "    'dependencies': {\n"
                "        'numpy': '1.24.3',\n"
                "        'pandas': '2.0.1',\n"
                "        'scikit-learn': '1.3.0',\n"
                "    },\n"
                "    'seeds': {'numpy': 42, 'python': 42},\n"
                "    'experiment': {\n"
                "        'name': 'rf-baseline',\n"
                "        'params': {'n_estimators': 200, 'max_depth': 10},\n"
                "        'metrics': {'accuracy': 0.92, 'f1': 0.88},\n"
                "    },\n"
                "}\n",
                "Project: churn-prediction v1.0.0\n"
                "Python: 3.11\n"
                "Structure: data/, src/, tests/, config/\n"
                "Best experiment: rf-baseline (acc=0.92)",
                "Это полная спецификация, на основе которой можно автоматически сгенерировать "
                "README, проверить наличие всех папок, и убедиться, что версии зафиксированы. "
                "Такой шаблон — основа reproducible ML."
            ),
            common_mistakes([
                {"mistake": "Сдать проект без README",
                 "why_bad": "Никто (включая вас через год) не разберётся, как запустить",
                 "fix": "README обязателен: install, run, tests, data, license"},
                {"mistake": "requirements.txt с незафиксированными версиями",
                 "why_bad": "Через месяц код может сломаться из-за обновлений",
                 "fix": "Все версии — с == в requirements.txt"},
                {"mistake": "Секреты и API-ключи закоммичены в репо",
                 "why_bad": "Утечка, которую невозможно откатить (git помнит всё)",
                 "fix": ".env в .gitignore, секреты через переменные окружения / vault"},
                {"mistake": "Данные и модели в Git",
                 "why_bad": "Репозиторий раздувается до гигабайт, pull/push тормозит",
                 "fix": "DVC или S3 для данных, MLflow/DVC для моделей"},
                {"mistake": "Один огромный коммит со всем проектом",
                 "why_bad": "Невозможно откатить, нельзя ревьюить",
                 "fix": "Инициализация → структура → data loader → features → model → docs"},
            ]),
            interview_questions([
                {"q": "Что должно быть в production-ready ML-проекте?",
                 "a": "Структура папок (data/, src/, tests/, notebooks/, config/), README, "
                      "requirements.txt с зафиксированными версиями, .gitignore, "
                      "random seed, логирование экспериментов, тесты, "
                      "опционально Dockerfile и CI/CD."},
                {"q": "Как организовать воспроизводимость ML-эксперимента?",
                 "a": "1) Random seed везде. 2) Версии библиотек в requirements. "
                      "3) Версионирование данных (DVC). 4) Логирование в MLflow. "
                      "5) README с командами запуска. 6) Docker для среды."},
                {"q": "Зачем нужен src/ layout, а не скрипты в корне?",
                 "a": "src/ — это пакет: можно импортировать (from src.features import ...), "
                      "тестировать (pytest), и не путать с утилитами. "
                      "Корневые скрипты — для CLI entry points (train.py, predict.py)."},
            ]),
            knowledge_checklist([
                "Структура cookiecutter-data-science",
                "README с инструкциями (install, run, test)",
                "requirements.txt с == версиями",
                ".gitignore для Python + DS",
                "Random seed для воспроизводимости",
                "Логирование экспериментов (MLflow или JSON)",
                "Git: ветки для фич, осмысленные коммиты",
            ]),
        ],
        exercises=[
            ex(1, "python", "Создай словарь `project` — полная спецификация проекта (name, version, python, license).",
               "project = {}\n",
               "project = {\n"
               "    'name': 'churn-prediction',\n"
               "    'version': '1.0.0',\n"
               "    'python': '3.11',\n"
               "    'license': 'MIT',\n"
               "    'author': 'alice',\n"
               "    'theme': 'customer analytics',\n"
               "}\n",
               [{"check": "isinstance(project, dict)", "msg": "Словарь"},
                {"check": "project.get('name') == 'churn-prediction'", "msg": "name"},
                {"check": "project.get('version') == '1.0.0'", "msg": "version"},
                {"check": "project.get('python') == '3.11'", "msg": "python"},
                {"check": "project.get('license') == 'MIT'", "msg": "MIT license"}],
               ["Словарь спецификации", "name/version/python/license — базовые поля"], 1),
            ex(2, "python", "Создай список `required_folders` — все обязательные папки production-ready проекта.",
               "required_folders = []\n",
               "required_folders = [\n"
               "    'data/raw', 'data/processed',\n"
               "    'notebooks',\n"
               "    'src/data', 'src/features', 'src/models', 'src/visualization',\n"
               "    'models',\n"
               "    'tests',\n"
               "    'config',\n"
               "    'reports',\n"
               "]\n",
               [{"check": "isinstance(required_folders, list)", "msg": "Список"},
                {"check": "len(required_folders) >= 8", "msg": "8+ папок"},
                {"check": "'data/raw' in required_folders", "msg": "data/raw"},
                {"check": "'notebooks' in required_folders", "msg": "notebooks"},
                {"check": "'src/features' in required_folders", "msg": "src/features"},
                {"check": "'tests' in required_folders", "msg": "tests"}],
               ["Список обязательных папок", "data, src, tests, config, models, reports"], 1),
            ex(3, "python", "Создай словарь `dependencies` — 5 пакетов с зафиксированными версиями.",
               "dependencies = {}\n",
               "dependencies = {\n"
               "    'numpy': '1.24.3',\n"
               "    'pandas': '2.0.1',\n"
               "    'scikit-learn': '1.3.0',\n"
               "    'matplotlib': '3.7.2',\n"
               "    'mlflow': '2.5.0',\n"
               "}\n",
               [{"check": "isinstance(dependencies, dict)", "msg": "Словарь"},
                {"check": "len(dependencies) >= 5", "msg": "5+ пакетов"},
                {"check": "dependencies.get('numpy') == '1.24.3'", "msg": "numpy 1.24.3"},
                {"check": "all('.' in v for v in dependencies.values())", "msg": "Все версии вида X.Y.Z"}],
               ["Словарь: пакет -> версия", "5 базовых DS-пакетов"], 1),
            ex(4, "python", "Создай функцию `render_requirements(deps)`, превращающую словарь в список строк 'name==version'.",
               "def render_requirements(deps):\n    pass\n",
               "def render_requirements(deps):\n"
               "    return [f'{name}=={version}' for name, version in deps.items()]\n",
               [{"check": "isinstance(render_requirements({'a': '1.0'}), list)", "msg": "Список"},
                {"check": "render_requirements({'numpy': '1.24.3'}) == ['numpy==1.24.3']", "msg": "numpy==1.24.3"},
                {"check": "len(render_requirements({'a': '1.0', 'b': '2.0'})) == 2", "msg": "2 строки"}],
               ["f-string шаблон", ".items() для пар ключ-значение"], 2),
            ex(5, "python", "Создай словарь `gitignore` — все паттерны для production-ready DS-проекта.",
               "gitignore = {}\n",
               "gitignore = {\n"
               "    'python': ['__pycache__/', '*.pyc', '*.pyo', '.venv/', 'venv/'],\n"
               "    'jupyter': ['.ipynb_checkpoints/', '*.ipynb'],\n"
               "    'data': ['data/raw/', 'data/processed/*.parquet'],\n"
               "    'models': ['models/*.pkl', 'models/*.joblib', 'mlruns/'],\n"
               "    'secrets': ['.env', 'secrets.yaml', '*.key'],\n"
               "    'os': ['.DS_Store', 'Thumbs.db'],\n"
               "}\n",
               [{"check": "isinstance(gitignore, dict)", "msg": "Словарь"},
                {"check": "len(gitignore) >= 5", "msg": "5+ категорий"},
                {"check": "'__pycache__/' in gitignore.get('python', [])", "msg": "__pycache__"},
                {"check": "'.env' in gitignore.get('secrets', [])", "msg": ".env"},
                {"check": "'data/raw/' in gitignore.get('data', [])", "msg": "data/raw/"}],
               ["Словарь: категория -> шаблоны", "python, jupyter, data, models, secrets"], 2),
            ex(6, "python", "Создай словарь `readme_template` — шаблон README с placeholders.",
               "readme_template = {}\n",
               "readme_template = {\n"
               "    'title': '# {name}',\n"
               "    'description': '{description}',\n"
               "    'badges': '![Python](https://img.shields.io/badge/python-{python}-blue)',\n"
               "    'installation': '## Installation\\npip install -r requirements.txt',\n"
               "    'usage': '## Usage\\npython src/models/train.py',\n"
               "    'tests': '## Tests\\npytest tests/',\n"
               "    'license': '## License\\n{license}',\n"
               "}\n",
               [{"check": "isinstance(readme_template, dict)", "msg": "Словарь"},
                {"check": "'{name}' in readme_template.get('title', '')", "msg": "title placeholder"},
                {"check": "'{python}' in readme_template.get('badges', '')", "msg": "python placeholder"},
                {"check": "len(readme_template) >= 5", "msg": "5+ секций"}],
               ["Словарь: секция -> шаблон", "{name}, {python} — placeholders"], 2),
            ex(7, "python", "Создай словарь `config` — production-ready config с секциями data, model, train, mlflow.",
               "config = {}\n",
               "config = {\n"
               "    'data': {\n"
               "        'raw_path': 'data/raw/churn.csv',\n"
               "        'processed_path': 'data/processed/churn.parquet',\n"
               "        'test_size': 0.2,\n"
               "    },\n"
               "    'model': {\n"
               "        'name': 'random_forest',\n"
               "        'n_estimators': 200,\n"
               "        'max_depth': 10,\n"
               "    },\n"
               "    'train': {\n"
               "        'random_state': 42,\n"
               "        'cv_folds': 5,\n"
               "    },\n"
               "    'mlflow': {\n"
               "        'experiment_name': 'churn-prediction',\n"
               "        'tracking_uri': 'mlruns/',\n"
               "    },\n"
               "}\n",
               [{"check": "isinstance(config, dict)", "msg": "Словарь"},
                {"check": "isinstance(config.get('data'), dict)", "msg": "data — словарь"},
                {"check": "isinstance(config.get('model'), dict)", "msg": "model — словарь"},
                {"check": "config.get('train', {}).get('random_state') == 42", "msg": "random_state = 42"},
                {"check": "isinstance(config.get('mlflow'), dict)", "msg": "mlflow — словарь"}],
               ["Вложенные словари для секций", "4 секции: data, model, train, mlflow"], 2),
            ex(8, "python", "Создай словарь `experiment` — лучший эксперимент: name, params, metrics, artifacts.",
               "experiment = {}\n",
               "experiment = {\n"
               "    'name': 'rf-v3-best',\n"
               "    'run_id': 'g7h8i9j0',\n"
               "    'params': {'n_estimators': 200, 'max_depth': 15, 'min_samples_split': 5},\n"
               "    'metrics': {'accuracy': 0.925, 'f1': 0.89, 'auc': 0.95},\n"
               "    'artifacts': ['model.pkl', 'feature_importance.png', 'confusion_matrix.png'],\n"
               "    'dataset_version': 'v3.1',\n"
               "    'git_commit': 'a1b2c3d',\n"
               "}\n",
               [{"check": "isinstance(experiment, dict)", "msg": "Словарь"},
                {"check": "isinstance(experiment.get('params'), dict)", "msg": "params — словарь"},
                {"check": "isinstance(experiment.get('metrics'), dict)", "msg": "metrics — словарь"},
                {"check": "isinstance(experiment.get('artifacts'), list)", "msg": "artifacts — список"},
                {"check": "experiment.get('metrics', {}).get('accuracy', 0) > 0.9", "msg": "accuracy > 0.9"}],
               ["Словарь: поле -> значение", "params, metrics, artifacts — вложенные структуры"], 2),
            ex(9, "python", "Создай функцию `validate_project(project)`, проверяющую наличие ключевых полей.",
               "def validate_project(project):\n    pass\n",
               "def validate_project(project):\n"
               "    required = ['name', 'version', 'python', 'license']\n"
               "    missing = [k for k in required if k not in project]\n"
               "    return {'valid': len(missing) == 0, 'missing': missing}\n",
               [{"check": "isinstance(validate_project({}), dict)", "msg": "Словарь"},
                {"check": "validate_project({}).get('valid') is False", "msg": "Пустой проект — невалиден"},
                {"check": "validate_project({'name': 'x', 'version': '1', 'python': '3.11', 'license': 'MIT'}).get('valid') is True",
                 "msg": "Полный проект — валиден"},
                {"check": "'missing' in validate_project({})", "msg": "missing в результате"}],
               ["Список required полей", "Возвращаем словарь valid/missing"], 3),
            ex(10, "python", "Создай список `release_steps` — шаги для первого релиза проекта на GitHub.",
               "release_steps = []\n",
               "release_steps = [\n"
               "    'git init',\n"
               "    'git add .',\n"
               "    'git commit -m \"initial project structure\"',\n"
               "    'git branch -M main',\n"
               "    'git remote add origin https://github.com/alice/churn.git',\n"
               "    'git push -u origin main',\n"
               "    'git tag v1.0.0',\n"
               "    'git push --tags',\n"
               "    'Create release on GitHub with release notes',\n"
               "]\n",
               [{"check": "isinstance(release_steps, list)", "msg": "Список"},
                {"check": "len(release_steps) >= 7", "msg": "7+ шагов"},
                {"check": "'git init' in release_steps", "msg": "git init"},
                {"check": "'git push' in ' '.join(release_steps)", "msg": "git push есть"}],
               ["Список шагов релиза", "init → commit → push → tag → release"], 2),
            ex(11, "python", "Создай словарь `health_check` — проверки готовности проекта к продакшену.",
               "health_check = {}\n",
               "health_check = {\n"
               "    'readme_exists': True,\n"
               "    'requirements_pinned': True,\n"
               "    'gitignore_present': True,\n"
               "    'tests_passing': True,\n"
               "    'seeds_set': True,\n"
               "    'logging_enabled': True,\n"
               "    'no_secrets_in_repo': True,\n"
               "    'docker_buildable': False,\n"
               "    'data_versioned': True,\n"
               "    'model_in_registry': False,\n"
               "}\n",
               [{"check": "isinstance(health_check, dict)", "msg": "Словарь"},
                {"check": "health_check.get('readme_exists') is True", "msg": "readme yes"},
                {"check": "health_check.get('requirements_pinned') is True", "msg": "pinned yes"},
                {"check": "health_check.get('no_secrets_in_repo') is True", "msg": "no secrets"},
                {"check": "sum(1 for v in health_check.values() if v is True) >= 7", "msg": "7+ проверок пройдено"}],
               ["Словарь чек-листа", "True/False для каждой проверки"], 2),
            ex(12, "python", "Создай функцию `project_score(health)`, считающую процент пройденных проверок.",
               "def project_score(health):\n    pass\n",
               "def project_score(health):\n"
               "    total = len(health)\n"
               "    passed = sum(1 for v in health.values() if v is True)\n"
               "    return round(passed / total * 100, 1) if total > 0 else 0\n",
               [{"check": "project_score({'a': True, 'b': True, 'c': False}) == 66.7",
                 "msg": "2/3 = 66.7%"},
                {"check": "project_score({}) == 0", "msg": "Пустой = 0%"},
                {"check": "project_score({'a': True}) == 100.0", "msg": "1/1 = 100%"}],
               ["sum(1 for v in ... if v)", "Деление и round", "Процент пройденных"], 3),
        ],
        minutes=60, difficulty=3,
    )


LESSONS = [_9_1, _9_2, _9_3, _9_4, _9_5, _9_6, _9_7, _9_8]
