/* SQL sandbox: sql.js (SQLite в браузере) + проверка результата.
 */
(function() {
  "use strict";

  const SQLJS_BASE = "/vendor/sqljs";
  let sqlReady = null;

  async function ensureSqlJs() {
    if (sqlReady) return sqlReady;
    sqlReady = (async () => {
      await loadScript(`${SQLJS_BASE}/sql-wasm.js`);
      const SQL = await window.initSqlJs({
        locateFile: (file) => `${SQLJS_BASE}/${file}`,
      });
      return SQL;
    })();
    return sqlReady;
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
   * Стандартная схема для тестов SQL.
   * Используется во всех упражнениях Блока 2.
   */
  const DEFAULT_SCHEMA = {
    tables: [
      `CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        score INTEGER DEFAULT 0,
        team_id INTEGER
      );`,
      `CREATE TABLE IF NOT EXISTS teams (
        id INTEGER PRIMARY KEY,
        team_name TEXT NOT NULL
      );`,
      `INSERT OR IGNORE INTO teams (id, team_name) VALUES (1, 'Red'), (2, 'Blue'), (3, 'Green');`,
      `INSERT OR IGNORE INTO players (id, name, score, team_id) VALUES
        (1, 'Alice', 1500, 1),
        (2, 'Bob', 800, 1),
        (3, 'Charlie', 600, 2),
        (4, 'Diana', 1200, 2),
        (5, 'Eve', 950, 3);`,
    ],
  };

  /**
   * Создаёт БД с дефолтной схемой + дополнительными скриптами.
   */
  async function createDb(extraSetup = []) {
    const SQL = await ensureSqlJs();
    const db = new SQL.Database();
    for (const stmt of DEFAULT_SCHEMA.tables) {
      db.run(stmt);
    }
    for (const stmt of extraSetup || []) {
      db.run(stmt);
    }
    return db;
  }

  /**
   * Выполняет запрос. Возвращает { columns, rows, error, timeMs, rowCount }.
   */
  async function executeQuery(query, extraSetup) {
    const db = await createDb(extraSetup);
    const start = performance.now();
    let columns = [];
    let rows = [];
    let error = "";

    try {
      const results = db.exec(query);
      if (results.length > 0) {
        columns = results[0].columns;
        rows = results[0].values.map(row => {
          const obj = {};
          columns.forEach((c, i) => { obj[c] = row[i]; });
          return obj;
        });
      }
    } catch (e) {
      error = e.message || String(e);
    }

    const timeMs = Math.round(performance.now() - start);
    db.close();
    return { columns, rows, error, timeMs, rowCount: rows.length };
  }

  /**
   * Сравнивает результат запроса с ожидаемым.
   * Сортирует строки и сравнивает поэлементно.
   */
  function compareResults(actual, expected) {
    if (expected.error) {
      return { pass: false, msg: "Ожидалась ошибка: " + expected.error };
    }

    const expRows = expected.rows || [];
    const expColumns = expected.columns;

    // Если ожидаются конкретные колонки — проверим их
    if (expColumns && expColumns.length > 0) {
      const missing = expColumns.filter(c => !actual.columns.includes(c));
      if (missing.length > 0) {
        return { pass: false, msg: "Нет столбцов: " + missing.join(", ") };
      }
    }

    // Сравнение по строкам
    const expSorted = JSON.stringify(sortRows(expRows));
    const actSorted = JSON.stringify(sortRows(actual.rows.map(r =>
      Object.fromEntries(Object.entries(r).map(([k, v]) => [k, v === null ? null : v]))
    )));

    if (actSorted === expSorted) {
      return { pass: true, msg: "OK" };
    }

    // Попробуем сравнить по количеству строк
    if (actual.rowCount === expRows.length) {
      return {
        pass: false,
        msg: "Количество совпадает, но содержимое отличается",
      };
    }

    return {
      pass: false,
      msg: `Ожидалось строк: ${expRows.length}, получено: ${actual.rowCount}`,
    };
  }

  function sortRows(rows) {
    return [...rows].sort((a, b) => JSON.stringify(a).localeCompare(JSON.stringify(b)));
  }

  /**
   * Запускает запрос с проверкой expected_result_json.
   */
  async function runAndCheck(query, expectedJson) {
    let expected = null;
    try {
      if (expectedJson) expected = JSON.parse(expectedJson);
    } catch (e) {
      expected = null;
    }

    const result = await executeQuery(query);
    let check = { pass: false, msg: "Нет ожидаемого результата" };

    if (expected && expected.rows) {
      check = compareResults(result, expected);
    } else {
      // Если нет expected, считаем успехом отсутствие ошибки
      check = { pass: !result.error, msg: result.error || "Выполнено" };
    }

    return {
      ...result,
      check,
      passed: check.pass,
    };
  }

  window.SqlSandbox = {
    ensureSqlJs,
    createDb,
    executeQuery,
    runAndCheck,
    DEFAULT_SCHEMA,
  };
})();
