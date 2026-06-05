/* Python sandbox: Pyodide + проверка тест-кейсов.
 * Ожидается, что глобально доступен window.pyodide после загрузки.
 */
(function() {
  "use strict";

  const PYODIDE_VERSION = "0.26.2";
  // Локальный base — для pyodide.js, .wasm, .asm.js, stdlib, lock.
  // Пакеты (whl) берутся с CDN чтобы не качать ~30MB локально.
  const PYODIDE_LOCAL = "/vendor/pyodide";
  const PYODIDE_CDN = `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/`;

  let pyodideReady = null;
  let pyodideLoading = false;
  let currentEngine = null; // "pyodide" | "mock"

  function log(msg, level = "info") {
    if (window.SandboxLog) window.SandboxLog(msg, level);
  }

  /**
   * Загружает Pyodide из локальной папки /vendor/pyodide/.
   * Пакеты подгружаются с CDN (быстрее, меньше места).
   * Если не удаётся — fallback на mock-режим.
   */
  async function ensurePyodide() {
    if (pyodideReady) return pyodideReady;
    if (pyodideLoading) {
      while (!pyodideReady) await new Promise(r => setTimeout(r, 100));
      return pyodideReady;
    }
    pyodideLoading = true;

    try {
      // Загружаем pyodide.js локально
      await loadScript(`${PYODIDE_LOCAL}/pyodide.js`);

      if (typeof window.loadPyodide !== "function") {
        throw new Error("loadPyodide не найден");
      }

      // indexURL ставим локальный — для .wasm, .asm.js, stdlib.
      // Но wheel-файлы он будет искать локально. Подменим config.indexURL
      // после loadPyodide нельзя, поэтому используем гибридный подход:
      // грузим pyodide.js с локального, а в loadPyodide передаём локальный
      // indexURL. Пакеты же подгружаем с CDN явно.
      pyodideReady = window.loadPyodide({
        indexURL: PYODIDE_LOCAL,
        // Пакеты пусть ищет на CDN
        packageCacheDir: PYODIDE_CDN,
        // Чтобы loadPackagesFromImports() и loadPackage() искали на CDN,
        // подменяем config.indexURL после загрузки
      });
      const py = await pyodideReady;
      // Подменяем путь к wheel-пакетам на CDN
      try {
        py.config.indexURL = PYODIDE_CDN;
        py.packageCacheDir = PYODIDE_CDN;
        if (py._api && py._api.config) {
          py._api.config.indexURL = PYODIDE_CDN;
        }
      } catch (e) { /* ignore */ }
      currentEngine = "pyodide";
      log("Pyodide загружен ✓", "success");
      return py;
    } catch (e) {
      log("Не удалось загрузить Pyodide, использую mock: " + e.message, "error");
      currentEngine = "mock";
      pyodideReady = Promise.resolve(makeMockPyodide());
      return pyodideReady;
    } finally {
      pyodideLoading = false;
    }
  }

  function loadScript(src) {
    return new Promise((resolve, reject) => {
      const existing = document.querySelector(`script[src="${src}"]`);
      if (existing) {
        if (existing.dataset.loaded) resolve();
        else existing.addEventListener("load", resolve);
        return;
      }
      const s = document.createElement("script");
      s.src = src;
      s.onload = () => { s.dataset.loaded = "1"; resolve(); };
      s.onerror = () => reject(new Error("Не удалось загрузить " + src));
      document.head.appendChild(s);
    });
  }

  /**
   * Mock-Python: ограниченный интерпретатор для простых выражений.
   * Используется только как fallback, если Pyodide не загрузился.
   * Не поддерживает полный Python, только безопасные присваивания и базовые вызовы.
   */
  function makeMockPyodide() {
    const globals = {};
    let outputBuffer = [];

    function capturePrint(...args) {
      const text = args.map(a => typeof a === "string" ? a : JSON.stringify(a)).join(" ");
      outputBuffer.push(text);
    }

    return {
      isMock: true,
      runPython(code) {
        outputBuffer = [];
        try {
          // Очень простой псевдо-Python: только присваивания и print
          const lines = code.split("\n");
          for (let line of lines) {
            line = line.trim();
            if (!line || line.startsWith("#")) continue;
            if (line.startsWith("print(")) {
              const m = line.match(/^print\((.*)\)$/);
              if (m) {
                let expr = m[1].trim();
                // f-string: f'...' — заменяем {var} на значение
                if (expr.startsWith("f'") || expr.startsWith('f"')) {
                  expr = expr.slice(1);
                  expr = expr.replace(/[{}]([^{}])+[{}]/g, (mm) => {
                    const varName = mm.slice(1, -1);
                    return globals[varName] !== undefined ? globals[varName] : "undefined";
                  });
                }
                // String literal
                if ((expr.startsWith("'") && expr.endsWith("'")) ||
                    (expr.startsWith('"') && expr.endsWith('"'))) {
                  outputBuffer.push(expr.slice(1, -1));
                } else {
                  // Evaluate
                  try {
                    const val = Function(...Object.keys(globals),
                      "return " + expr)(...Object.values(globals));
                    outputBuffer.push(String(val));
                  } catch (e) {
                    outputBuffer.push("Error: " + e.message);
                  }
                }
              }
            } else if (line.includes("=") && !line.includes("==")) {
              const [lhs, ...rhs] = line.split("=");
              const varName = lhs.trim();
              const rhsStr = rhs.join("=").trim();
              try {
                const val = Function(...Object.keys(globals),
                  "return " + rhsStr)(...Object.values(globals));
                globals[varName] = val;
              } catch (e) {
                globals[varName] = rhsStr; // строка
              }
            } else if (line.startsWith("def ")) {
              // Игнорируем определения функций в mock
              continue;
            } else if (line.startsWith("for ") || line.startsWith("if ") ||
                       line.startsWith("while ")) {
              // Игнорируем сложные конструкции
              continue;
            } else {
              try {
                const val = Function(...Object.keys(globals),
                  "return " + line)(...Object.values(globals));
                outputBuffer.push(String(val));
              } catch (e) {
                // ignore
              }
            }
          }
          return outputBuffer.join("\n");
        } catch (e) {
          throw e;
        }
      },
      globals,
    };
  }

  let matplotlibLoaded = false;
  let matplotlibLoading = null;
  let matplotlibFailed = false;
  /**
   * Загружает matplotlib + numpy в Pyodide (для визуализации).
   * Делается один раз. С таймаутом 60s и прогресс-логом.
   */
  async function ensureMatplotlib() {
    if (matplotlibLoaded) return true;
    if (matplotlibFailed) return false;
    if (matplotlibLoading) return matplotlibLoading;
    matplotlibLoading = (async () => {
      const py = await ensurePyodide();
      if (!py || py.isMock) {
        matplotlibFailed = true;
        log("Matplotlib недоступен в mock-режиме", "error");
        return false;
      }
      try {
        log("Загружаю matplotlib... (5-15 сек)", "info");

        // Параллельно слушаем прогресс через динамический логгер
        const origLog = log;
        let progressInterval = null;
        let progressSec = 0;
        progressInterval = setInterval(() => {
          progressSec += 2;
          if (progressSec <= 60) {
            origLog(`Matplotlib загружается... (${progressSec}с)`, "info");
          }
        }, 2000);

        // Таймаут 60 сек
        const timeout = new Promise((_, reject) =>
          setTimeout(() => reject(new Error("Timeout 60s")), 60000)
        );
        await Promise.race([
          py.loadPackage(["matplotlib", "numpy"]),
          timeout
        ]);
        clearInterval(progressInterval);

        py.runPython(`
import matplotlib
matplotlib.use("AGG")
import matplotlib.pyplot as plt
import io as _ds_io2
import base64 as _ds_b64

def _ds_show(*args, **kwargs):
    import sys as _ds_sys3
    figs = []
    for num in plt.get_fignums():
        fig = plt.figure(num)
        buf = _ds_io2.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight", dpi=100)
        plt.close(fig)
        figs.append(_ds_b64.b64encode(buf.getvalue()).decode("ascii"))
    for f in figs:
        print("__DS_PLOT__" + f + "__DS_END__")

plt.show = _ds_show
`);
        matplotlibLoaded = true;
        log("Matplotlib загружен ✓", "success");
        return true;
      } catch (e) {
        matplotlibFailed = true;
        log("Matplotlib не загружен: " + e.message, "error");
        return false;
      }
    })();
    return matplotlibLoading;
  }

  /**
   * Запускает Python-код и возвращает { stdout, stderr, plots }.
   * plots — массив base64-PNG из plt.show() и явных вызовов _ds_show().
   * Перенаправляем stdout/stderr на стороне Python (работает в любой версии Pyodide).
   */
  async function runCode(code) {
    const py = await ensurePyodide();

    // Если пользователь импортирует matplotlib/numpy — загрузим заранее
    if (/^\s*(import\s+matplotlib|from\s+matplotlib)/m.test(code) ||
        /^\s*import\s+numpy/m.test(code) ||
        /^\s*from\s+numpy/m.test(code)) {
      await ensureMatplotlib();
    }

    const wrapped = `
import sys as _ds_sys
import io as _ds_io
_ds_captured_stdout = _ds_io.StringIO()
_ds_captured_stderr = _ds_io.StringIO()
_ds_old_stdout = _ds_sys.stdout
_ds_old_stderr = _ds_sys.stderr
_ds_sys.stdout = _ds_captured_stdout
_ds_sys.stderr = _ds_captured_stderr
_ds_run_error = None
try:
    exec(compile(${JSON.stringify(code)}, '<user>', 'exec'), globals())
except Exception as _ds_e:
    _ds_run_error = str(_ds_e)
finally:
    _ds_sys.stdout = _ds_old_stdout
    _ds_sys.stderr = _ds_old_stderr
_captured_out = _ds_captured_stdout.getvalue()
_captured_err = _ds_captured_stderr.getvalue()
`;
    let stdout = "";
    let stderr = "";
    let runError = null;
    try {
      py.runPython(wrapped);
      // В Pyodide 0.26 globals — это JS Object, не dict. Используем runPython
      // для безопасного чтения. Возвращаем кортеж (out, err, error).
      const result = py.runPython("(_captured_out, _captured_err, _ds_run_error)");
      if (Array.isArray(result) || (result && typeof result.toJs === "function")) {
        const arr = typeof result.toJs === "function" ? result.toJs() : result;
        stdout = String(arr[0] ?? "");
        const errVal = arr[1] ?? "";
        const errExc = arr[2];
        if (errExc != null && errExc !== "None" && errExc !== false) {
          runError = String(errExc);
        } else {
          stderr = String(errVal);
        }
      }
    } catch (e) {
      runError = e.message || String(e);
    }

    const plots = extractPlots(stdout);
    if (plots.length) {
      stdout = stdout.replace(/__DS_PLOT__[A-Za-z0-9+/=]+__DS_END__/g, "").trim();
    }
    return {
      stdout: stdout.trim(),
      stderr: runError || stderr.trim(),
      plots,
      engine: currentEngine,
    };
  }

  function extractPlots(text) {
    const re = /__DS_PLOT__([A-Za-z0-9+/=]+)__DS_END__/g;
    const out = [];
    let m;
    while ((m = re.exec(text)) !== null) out.push(m[1]);
    return out;
  }

  /**
   * Выполняет код и проверяет test_cases.
   * Возвращает { passed, total, results, output, error, plots }.
   */
  async function runAndCheck(code, testCases) {
    const py = await ensurePyodide();
    let stdout = "";
    let stderr = "";
    let runError = null;

    try {
      if (/^\s*(import\s+matplotlib|from\s+matplotlib)/m.test(code) ||
          /^\s*import\s+numpy/m.test(code) ||
          /^\s*from\s+numpy/m.test(code)) {
        await ensureMatplotlib();
      }

      const wrapped = `
import sys as _ds_sys
import io as _ds_io
_ds_captured_stdout = _ds_io.StringIO()
_ds_captured_stderr = _ds_io.StringIO()
_ds_old_stdout = _ds_sys.stdout
_ds_old_stderr = _ds_sys.stderr
_ds_sys.stdout = _ds_captured_stdout
_ds_sys.stderr = _ds_captured_stderr
_ds_run_error = None
try:
    exec(compile(${JSON.stringify(code)}, '<user>', 'exec'), globals())
except Exception as _ds_e:
    _ds_run_error = str(_ds_e)
finally:
    _ds_sys.stdout = _ds_old_stdout
    _ds_sys.stderr = _ds_old_stderr
_captured_out = _ds_captured_stdout.getvalue()
_captured_err = _ds_captured_stderr.getvalue()
`;
      py.runPython(wrapped);
      const result = py.runPython("(_captured_out, _captured_err, _ds_run_error)");
      if (result && typeof result.toJs === "function") {
        const arr = result.toJs();
        stdout = String(arr[0] ?? "");
        const errVal = arr[1] ?? "";
        const errExc = arr[2];
        if (errExc != null && errExc !== "None" && errExc !== false) {
          runError = String(errExc);
        } else {
          stderr = String(errVal);
        }
      }

      // Прогоняем test cases
      const results = [];
      for (const tc of testCases || []) {
        try {
          const checkResult = py.runPython(tc.check);
          const ok = Boolean(checkResult);
          results.push({
            description: tc.description || tc.check,
            pass: ok,
            msg: tc.msg || (ok ? "OK" : "FAILED"),
          });
        } catch (e) {
          results.push({
            description: tc.description || tc.check,
            pass: false,
            msg: "Ошибка проверки: " + (e.message || String(e)),
          });
        }
      }

      const passed = results.filter(r => r.pass).length;
      const plots = extractPlots(stdout);
      const cleanStdout = stdout.replace(/__DS_PLOT__[A-Za-z0-9+/=]+__DS_END__/g, "").trim();
      return {
        passed: passed === results.length && results.length > 0,
        total: results.length,
        passed_count: passed,
        results,
        output: cleanStdout,
        error: runError || stderr.trim(),
        plots,
        engine: currentEngine,
      };
    } catch (e) {
      return {
        passed: false,
        total: 0,
        results: [],
        output: stdout.trim(),
        error: runError || stderr.trim() || (e.message || String(e)),
        plots: [],
        engine: currentEngine,
      };
    }
  }

  /**
   * Mock-проверка для простых упражнений, когда Pyodide не загрузился.
   * Очень ограниченная — поддерживает только самые простые проверки.
   */
  async function runAndCheckMock(code, testCases) {
    const py = await ensurePyodide();
    if (!py.isMock) return runAndCheck(code, testCases);

    const output = py.runPython(code);
    const results = (testCases || []).map(tc => {
      try {
        const ok = Function("output", ...Object.keys(py.globals),
          "return " + tc.check)(output, ...Object.values(py.globals));
        return { description: tc.description, pass: !!ok, msg: ok ? "OK (mock)" : "FAILED" };
      } catch (e) {
        return { description: tc.description, pass: false, msg: "Mock: проверка не поддерживается. Установите Pyodide." };
      }
    });
    return {
      passed: results.every(r => r.pass),
      total: results.length,
      passed_count: results.filter(r => r.pass).length,
      results,
      output,
      error: "",
      engine: "mock",
    };
  }

  window.PythonSandbox = {
    ensurePyodide,
    ensureMatplotlib,
    runCode,
    runAndCheck,
    runAndCheckMock,
    get engine() { return currentEngine; },
  };
})();
