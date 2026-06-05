"""
Единственная точка запуска курса.
Проверяет зависимости, инициализирует БД, скачивает vendor-файлы,
запускает FastAPI-сервер и открывает браузер.
"""
import os
import sys
import subprocess
import webbrowser
import threading
import time
from pathlib import Path

ROOT = Path(__file__).parent.resolve()
VENDOR = ROOT / "frontend" / "vendor"
PYODIDE_VERSION = "0.26.2"
SQLJS_VERSION = "1.10.3"

PYODIDE_FILES = [
    f"https://cdn.jsdelivr.net/pyodide/v{PYODIDE_VERSION}/full/pyodide.js",
    f"https://cdn.jsdelivr.net/pyodide/v{PYODIDE_VERSION}/full/pyodide.asm.wasm",
    f"https://cdn.jsdelivr.net/pyodide/v{PYODIDE_VERSION}/full/pyodide.asm.js",
    f"https://cdn.jsdelivr.net/pyodide/v{PYODIDE_VERSION}/full/python_stdlib.zip",
    f"https://cdn.jsdelivr.net/pyodide/v{PYODIDE_VERSION}/full/pyodide-lock.json",
]
# Пакеты (whl) качаются отдельно — иначе loadPackage() в браузере
# будет пытаться скачать их с CDN, что не работает в полностью оффлайн режиме.
# Сюда можно добавить любой пакет из pyodide-lock.json.
PYODIDE_PACKAGES = [
    "numpy", "pandas", "matplotlib", "matplotlib-pyodide",
    "scikit-learn", "scipy", "scikit-image",
    # Зависимости matplotlib/numpy/pandas
    "pillow", "cycler", "fonttools", "kiwisolver", "packaging",
    "pyparsing", "python-dateutil", "pytz", "six",
    "joblib", "threadpoolctl",
]

SQLJS_FILES = [
    f"https://cdnjs.cloudflare.com/ajax/libs/sql.js/{SQLJS_VERSION}/sql-wasm.js",
    f"https://cdnjs.cloudflare.com/ajax/libs/sql.js/{SQLJS_VERSION}/sql-wasm.wasm",
]


def info(msg: str) -> None:
    print(f"\033[36m[ds-course]\033[0m {msg}")


def ok(msg: str) -> None:
    print(f"\033[32m[ds-course]\033[0m {msg}")


def warn(msg: str) -> None:
    print(f"\033[33m[ds-course]\033[0m {msg}")


def err(msg: str) -> None:
    print(f"\033[31m[ds-course]\033[0m {msg}")


def ensure_dependencies() -> None:
    """Устанавливает зависимости из requirements.txt, если их нет."""
    info("Проверяю зависимости Python...")
    try:
        import fastapi  # noqa
        import uvicorn  # noqa
        import pydantic  # noqa
        ok("Зависимости уже установлены")
    except ImportError:
        info("Устанавливаю зависимости (это нужно сделать только один раз)...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--quiet"]
        )
        ok("Зависимости установлены")


def download_file(url: str, dest: Path) -> bool:
    """Скачивает файл, возвращает True если успешно."""
    if dest.exists() and dest.stat().st_size > 1000:
        return True
    try:
        import urllib.request
        info(f"  → {dest.name} ({url.rsplit('/', 1)[-1]})")
        urllib.request.urlretrieve(url, dest)
        return True
    except Exception as e:
        warn(f"  Не удалось скачать {dest.name}: {e}")
        return False


def ensure_vendor_files() -> None:
    """Скачивает Pyodide и sql.js в frontend/vendor/."""
    VENDOR.mkdir(parents=True, exist_ok=True)
    pyodide_dir = VENDOR / "pyodide"
    pyodide_dir.mkdir(parents=True, exist_ok=True)
    sqljs_dir = VENDOR / "sqljs"
    sqljs_dir.mkdir(parents=True, exist_ok=True)

    info("Проверяю файлы Pyodide (Python в браузере)...")
    for url in PYODIDE_FILES:
        fname = url.rsplit("/", 1)[-1]
        download_file(url, pyodide_dir / fname)

    # Качаем .whl для нужных пакетов и всех их транзитивных зависимостей
    # по pyodide-lock.json (с CDN jsdelivr).
    if not (pyodide_dir / "matplotlib-3.5.2-cp312-cp312-pyodide_2024_0_wasm32.whl").exists():
        info("Качаю Pyodide-пакеты (numpy, matplotlib, sklearn, ...)...")
        try:
            import json
            import urllib.request
            lock = pyodide_dir / "pyodide-lock.json"
            if lock.exists():
                with open(lock, encoding="utf-8") as f:
                    lock_data = json.load(f)
                packages = lock_data.get("packages", {})

                def collect_deps(name: str, out: set) -> None:
                    if name in out:
                        return
                    out.add(name)
                    for dep in packages.get(name, {}).get("depends", []):
                        collect_deps(dep, out)

                needed: set = set()
                for pkg in PYODIDE_PACKAGES:
                    if pkg in packages:
                        collect_deps(pkg, needed)
                    else:
                        warn(f"  Пакет {pkg} не найден в lock, пропускаю")

                for name in sorted(needed):
                    fn = packages[name].get("file_name")
                    if not fn:
                        continue
                    dest = pyodide_dir / fn
                    if dest.exists() and dest.stat().st_size > 1000:
                        continue
                    url = f"https://cdn.jsdelivr.net/pyodide/v{PYODIDE_VERSION}/full/{fn}"
                    info(f"  → {fn}")
                    try:
                        urllib.request.urlretrieve(url, dest)
                    except Exception as e:
                        warn(f"  Не удалось скачать {fn}: {e}")
                ok(f"  Пакеты Pyodide готовы ({len(needed)} whl)")
        except Exception as e:
            warn(f"  Ошибка при скачивании пакетов: {e}")

    info("Проверяю файлы sql.js (SQLite в браузере)...")
    for url in SQLJS_FILES:
        fname = url.rsplit("/", 1)[-1]
        download_file(url, sqljs_dir / fname)

    pkgs_file = pyodide_dir / "packages.json"
    if not pkgs_file.exists():
        try:
            import urllib.request
            urllib.request.urlretrieve(
                f"https://cdn.jsdelivr.net/pyodide/v{PYODIDE_VERSION}/full/packages.json",
                pkgs_file,
            )
        except Exception as e:
            warn(f"  Не удалось скачать packages.json: {e}")

    ok("Vendor-файлы готовы")


def ensure_database() -> None:
    """Инициализирует БД при первом запуске."""
    info("Проверяю базу данных...")
    from app.database import init_db, DB_PATH
    if not DB_PATH.exists():
        init_db()
        ok(f"База данных создана: {DB_PATH}")
    else:
        init_db()  # no-op если уже инициализирована
        ok("База данных готова")


def open_browser_delayed(url: str, delay: float = 1.5) -> None:
    def _open():
        time.sleep(delay)
        try:
            webbrowser.open(url)
        except Exception:
            pass
    t = threading.Thread(target=_open, daemon=True)
    t.start()


def main() -> None:
    print()
    info("=" * 60)
    info("  DATA SCIENCE COURSE — Локальный самоучитель")
    info("=" * 60)
    print()

    ensure_dependencies()
    ensure_vendor_files()
    ensure_database()

    print()
    ok("=" * 60)
    ok("  ✅ Курс запущен: http://localhost:8000")
    ok("  Остановка: Ctrl+C в этом окне")
    ok("=" * 60)
    print()

    open_browser_delayed("http://localhost:8000")

    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        log_level="info",
        reload=False,
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        info("Курс остановлен. До встречи!")
