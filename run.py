"""
Единственная точка запуска курса.
Запускает FastAPI-сервер сразу, а скачивание vendor-файлов делает
в фоне (на повторных запусках — мгновенно, без проверок).
"""
import os
import sys
import subprocess
import webbrowser
import threading
import time
import json
import shutil
from pathlib import Path

# Force UTF-8 stdout/stderr (Windows cp1251 не понимает эмодзи)
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).parent.resolve()
VENDOR = ROOT / "frontend" / "vendor"
PYODIDE_DIR = VENDOR / "pyodide"
SQLJS_DIR = VENDOR / "sqljs"

PYODIDE_VERSION = "0.26.2"
SQLJS_VERSION = "1.10.3"

PYODIDE_FILES = [
    f"https://cdn.jsdelivr.net/pyodide/v{PYODIDE_VERSION}/full/pyodide.js",
    f"https://cdn.jsdelivr.net/pyodide/v{PYODIDE_VERSION}/full/pyodide.asm.wasm",
    f"https://cdn.jsdelivr.net/pyodide/v{PYODIDE_VERSION}/full/pyodide.asm.js",
    f"https://cdn.jsdelivr.net/pyodide/v{PYODIDE_VERSION}/full/python_stdlib.zip",
    f"https://cdn.jsdelivr.net/pyodide/v{PYODIDE_VERSION}/full/pyodide-lock.json",
]

# Пакеты (whl) для оффлайн-работы. Без них matplotlib/sklearn не загрузятся.
PYODIDE_PACKAGES = [
    "numpy", "pandas", "matplotlib", "matplotlib-pyodide",
    "scikit-learn", "scipy",
    "pillow", "cycler", "fonttools", "kiwisolver", "packaging",
    "pyparsing", "python-dateutil", "pytz", "six",
    "joblib", "threadpoolctl",
]

SQLJS_FILES = [
    f"https://cdnjs.cloudflare.com/ajax/libs/sql.js/{SQLJS_VERSION}/sql-wasm.js",
    f"https://cdnjs.cloudflare.com/ajax/libs/sql.js/{SQLJS_VERSION}/sql-wasm.wasm",
]

# Маркер "всё скачано" — если есть, пропускаем ВСЕ проверки vendor
VENDOR_READY = VENDOR / ".vendor_ready"


def info(msg: str) -> None:
    print(f"\033[36m[ds-course]\033[0m {msg}", flush=True)


def ok(msg: str) -> None:
    print(f"\033[32m[ds-course]\033[0m {msg}", flush=True)


def warn(msg: str) -> None:
    print(f"\033[33m[ds-course]\033[0m {msg}", flush=True)


def ensure_dependencies() -> None:
    """Устанавливает зависимости из requirements.txt, если их нет."""
    try:
        import fastapi  # noqa
        import uvicorn  # noqa
        import pydantic  # noqa
    except ImportError:
        info("Устанавливаю зависимости Python (один раз)...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--quiet"]
        )
        ok("Зависимости установлены")


def _is_complete(path: Path, min_size: int = 1000) -> bool:
    """Файл существует и не пустой."""
    try:
        return path.exists() and path.stat().st_size >= min_size
    except OSError:
        return False


def _atomic_download(url: str, dest: Path) -> bool:
    """Скачивает во временный файл, потом переименовывает. Не оставляет мусор при ошибке."""
    if _is_complete(dest):
        return True
    tmp = dest.with_suffix(dest.suffix + ".part")
    try:
        import urllib.request
        with urllib.request.urlopen(url, timeout=30) as resp:
            with open(tmp, "wb") as f:
                shutil.copyfileobj(resp, f, 1024 * 64)
        if tmp.stat().st_size < 100:
            tmp.unlink(missing_ok=True)
            return False
        tmp.replace(dest)
        return True
    except Exception as e:
        tmp.unlink(missing_ok=True)
        warn(f"  Не удалось скачать {dest.name}: {e}")
        return False


def _gather_wheel_filenames(needed: set) -> dict:
    """Читает lock.json и возвращает {package_name: file_name}."""
    lock_path = PYODIDE_DIR / "pyodide-lock.json"
    if not lock_path.exists():
        return {}
    try:
        with open(lock_path, encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return {}
    packages = data.get("packages", {})
    out = {}
    for n in needed:
        p = packages.get(n, {})
        fn = p.get("file_name")
        if fn:
            out[n] = fn
    return out


def _collect_wheel_deps(package_names: list) -> set:
    """Рекурсивно собирает имена пакетов + их зависимостей из lock.json."""
    lock_path = PYODIDE_DIR / "pyodide-lock.json"
    if not lock_path.exists():
        return set()
    try:
        with open(lock_path, encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return set()
    packages = data.get("packages", {})
    out: set = set()

    def add(name: str) -> None:
        if name in out:
            return
        out.add(name)
        for dep in packages.get(name, {}).get("depends", []):
            add(dep)

    for n in package_names:
        if n in packages:
            add(n)
    return out


def _ensure_vendor_sync() -> None:
    """Синхронная версия — вызывается из фонового потока."""
    VENDOR.mkdir(parents=True, exist_ok=True)
    PYODIDE_DIR.mkdir(parents=True, exist_ok=True)
    SQLJS_DIR.mkdir(parents=True, exist_ok=True)

    # 1) Pyodide runtime файлы
    for url in PYODIDE_FILES:
        fname = url.rsplit("/", 1)[-1]
        _atomic_download(url, PYODIDE_DIR / fname)

    # 2) Wheel-файлы пакетов
    needed = _collect_wheel_deps(PYODIDE_PACKAGES)
    if needed:
        wheel_files = _gather_wheel_filenames(needed)
        for name, fname in wheel_files.items():
            if not fname:
                continue
            url = f"https://cdn.jsdelivr.net/pyodide/v{PYODIDE_VERSION}/full/{fname}"
            _atomic_download(url, PYODIDE_DIR / fname)

    # 3) sql.js
    for url in SQLJS_FILES:
        fname = url.rsplit("/", 1)[-1]
        _atomic_download(url, SQLJS_DIR / fname)

    # 4) Помечаем как готов
    VENDOR_READY.touch()


def _vendor_is_fully_ready() -> bool:
    """Быстрая проверка: все критичные файлы уже на диске."""
    if not VENDOR_READY.exists():
        return False
    # Двойная проверка: маркер мог остаться от старой версии
    for url in PYODIDE_FILES:
        fname = url.rsplit("/", 1)[-1]
        if not _is_complete(PYODIDE_DIR / fname):
            return False
    for url in SQLJS_FILES:
        fname = url.rsplit("/", 1)[-1]
        if not _is_complete(SQLJS_DIR / fname):
            return False
    # Хотя бы один wheel для matplotlib
    if not list(PYODIDE_DIR.glob("*matplotlib*.whl")):
        return False
    return True


def ensure_vendor_async() -> None:
    """Запускает проверку/скачивание vendor в фоне. Не блокирует."""
    if _vendor_is_fully_ready():
        return  # моментальный выход — всё уже скачано
    def _bg():
        try:
            info("Докачиваю vendor-файлы в фоне (один раз)...")
            _ensure_vendor_sync()
            ok("Vendor-файлы готовы")
        except Exception as e:
            warn(f"Ошибка при докачке vendor: {e}")
    threading.Thread(target=_bg, daemon=True).start()


def ensure_database() -> None:
    """Инициализирует БД при первом запуске."""
    from app.database import init_db
    init_db()


def open_browser_delayed(url: str, delay: float = 1.0) -> None:
    def _open():
        time.sleep(delay)
        try:
            webbrowser.open(url)
        except Exception:
            pass
    threading.Thread(target=_open, daemon=True).start()


def main() -> None:
    print()
    info("=" * 60)
    info("  DATA SCIENCE COURSE — Локальный самоучитель")
    info("=" * 60)
    print(flush=True)

    ensure_dependencies()
    # ВАЖНО: vendor check запускается в фоне, сервер стартует СРАЗУ
    ensure_vendor_async()
    ensure_database()

    print(flush=True)
    ok("=" * 60)
    ok("  ✅ Курс запущен: http://localhost:8000")
    ok("  Остановка: Ctrl+C в этом окне")
    ok("=" * 60)
    print(flush=True)

    open_browser_delayed("http://localhost:8000")

    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        log_level="warning",  # было info — info логировал каждый запрос, шумно
        reload=False,
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        info("Курс остановлен. До встречи!")
