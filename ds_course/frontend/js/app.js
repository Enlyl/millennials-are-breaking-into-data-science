/* Data Science Course — главный контроллер. */
(function() {
  "use strict";

  // ============================================================================
  // Состояние
  // ============================================================================
  const state = {
    blocks: [],
    lessons: {}, // number -> lesson
    progress: {},
    summary: { lessons_total: 0, lessons_done: 0, exercises_total: 0, exercises_solved: 0 },
    achievements: [],
    pyodideReady: false,
  };

  const completedLessons = new Set(JSON.parse(localStorage.getItem("ds_completed_lessons") || "[]"));
  const solvedExercises = new Set(JSON.parse(localStorage.getItem("ds_solved_exercises") || "[]"));

  // ============================================================================
  // Утилиты
  // ============================================================================
  const $ = (sel, parent = document) => parent.querySelector(sel);
  const $$ = (sel, parent = document) => Array.from(parent.querySelectorAll(sel));

  function escapeHtml(s) {
    if (s == null) return "";
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function debounce(fn, ms) {
    let t;
    return (...args) => { clearTimeout(t); t = setTimeout(() => fn(...args), ms); };
  }

  // Безопасно парсит JSON-поле: если это уже массив/объект — возвращает как есть,
  // если строка — JSON.parse, иначе fallback.
  function parseJsonField(field, fallback = []) {
    if (field == null) return fallback;
    if (typeof field === "string") {
      try { return JSON.parse(field); }
      catch (e) { return fallback; }
    }
    if (Array.isArray(field) || typeof field === "object") return field;
    return fallback;
  }

  // Простая markdown-подсветка
  function md(text) {
    if (!text) return "";
    return escapeHtml(text)
      .replace(/```(\w*)\n([\s\S]*?)```/g, (m, lang, code) =>
        `<pre><code class="lang-${lang}">${code}</code></pre>`)
      .replace(/`([^`]+)`/g, "<code>$1</code>")
      .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
      .replace(/\n\n/g, "</p><p>")
      .replace(/^/, "<p>")
      .replace(/$/, "</p>")
      .replace(/<p><\/p>/g, "")
      .replace(/<p>(<pre>[\s\S]*?<\/pre>)<\/p>/g, "$1")
      .replace(/<p>(<ul>[\s\S]*?<\/ul>)<\/p>/g, "$1")
      .replace(/<p>(<ol>[\s\S]*?<\/ol>)<\/p>/g, "$1");
  }

  // ============================================================================
  // API
  // ============================================================================
  async function api(path, opts = {}) {
    const res = await fetch("/api" + path, {
      headers: { "Content-Type": "application/json" },
      ...opts,
    });
    if (!res.ok) throw new Error(`API ${path}: ${res.status}`);
    return res.json();
  }

  async function loadInitial() {
    try {
      state.blocks = await api("/lessons/blocks");
    } catch (e) {
      console.error("Failed to load blocks:", e);
      state.blocks = [];
      throw e;
    }
    try {
      state.summary = await api("/progress/summary");
    } catch (e) {
      console.error("Failed to load summary:", e);
      state.summary = { lessons_total: 0, lessons_done: 0, exercises_total: 0, exercises_solved: 0 };
    }
    try {
      state.achievements = await api("/achievements/");
    } catch (e) {
      console.error("Failed to load achievements:", e);
      state.achievements = [];
    }
    updateProgressUI();
    renderSidebar();
    // Загружаем все уроки для сайдбара в фоне
    loadAllLessonsForSidebar();
  }

  function updateProgressUI() {
    const total = state.summary.lessons_total || 1;
    const done = completedLessons.size;
    const pct = Math.round((done / total) * 100);
    $("#progress-pct").textContent = pct + "%";
    $("#progress-fill").style.width = pct + "%";
  }

  // ============================================================================
  // Sidebar
  // ============================================================================
  function renderSidebar() {
    const nav = $("#blocks-nav");
    if (!nav) return;
    const themeClass = { space: "theme-space", gaming: "theme-gaming", mixed: "theme-mixed", neutral: "theme-mixed" };
    if (!state.allLessons) {
      // Начальный рендер до загрузки уроков — только заголовки блоков
      let html = "";
      for (const block of state.blocks) {
        const theme = themeClass[block.theme] || "theme-mixed";
        html += `<div class="block-title ${theme}"><span class="block-num">${block.number}</span>${escapeHtml(block.title)}</div>`;
      }
      nav.innerHTML = html;
    } else {
      renderSidebarFull();
    }
  }

  function renderSidebarFull() {
    const nav = $("#blocks-nav");
    if (!nav) return;
    const themeClass = { space: "theme-space", gaming: "theme-gaming", mixed: "theme-mixed", neutral: "theme-mixed" };
    let html = "";
    for (const block of state.blocks) {
      const theme = themeClass[block.theme] || "theme-mixed";
      html += `<div class="block-title ${theme}"><span class="block-num">${block.number}</span>${escapeHtml(block.title)}</div>`;
      const blockLessons = state.allLessons.filter(l => l.block_id === block.id);
      for (const lesson of blockLessons) {
        const isCompleted = completedLessons.has(lesson.number);
        const status = isCompleted ? "✅" : "○";
        const statusClass = isCompleted ? "completed" : "available";
        html += `<a href="#/lesson/${lesson.number}" class="lesson-link ${isCompleted ? "completed" : ""}" data-lesson="${lesson.number}">
          <span class="lesson-status ${statusClass}">${status}</span>
          <span class="lesson-title">${escapeHtml(lesson.title)}</span>
        </a>`;
      }
    }
    nav.innerHTML = html;
  }

  async function loadAllLessonsForSidebar() {
    try {
      const allLessons = await api("/lessons/");
      state.allLessons = allLessons;
      renderSidebarFull();
    } catch (e) {
      console.error("loadAllLessonsForSidebar failed:", e);
    }
  }

  // ============================================================================
  // Router
  // ============================================================================
  function parseHash() {
    const hash = location.hash.slice(1) || "/";
    const [path, ...rest] = hash.split("/").filter(Boolean);
    return { path: "/" + path, params: rest };
  }

  async function route() {
    const { path, params } = parseHash();
    highlightNav(path);

    try {
      if (path === "/" || path === "/home") {
        await renderHome();
      } else if (path === "/lesson") {
        await renderLesson(params[0]);
      } else if (path === "/projects") {
        await renderProjects();
      } else if (path === "/project") {
        await renderProject(params[0]);
      } else if (path === "/interview") {
        await renderInterview();
      } else if (path === "/achievements") {
        await renderAchievements();
      } else if (path === "/final") {
        await renderFinal();
      } else {
        await renderHome();
      }
    } catch (e) {
      console.error(e);
      $("#main").innerHTML = `<div class="card"><h2>Ошибка</h2><p>${escapeHtml(e.message)}</p></div>`;
    }
  }

  function highlightNav(path) {
    $$(".nav-link").forEach(el => {
      el.classList.toggle("active",
        (path === "/" && el.dataset.view === "home") ||
        (path === "/" + el.dataset.view));
    });
  }

  // ============================================================================
  // Views
  // ============================================================================
  async function renderHome() {
    const main = $("#main");
    if (!main) return;
    const themeIcon = { space: "🚀", gaming: "🎮", mixed: "📊", neutral: "📚" };
    const blockCards = (state.blocks || []).filter(b => b.number <= 9).map(b => {
      const icon = themeIcon[b.theme] || "📚";
      const firstLesson = (state.allLessons || []).find(l => l.block_id === b.id);
      const href = firstLesson ? `#/lesson/${firstLesson.number}` : `#/`;
      return `<a href="${href}" class="feature-card">
          <div class="feature-icon">${icon}</div>
          <div class="feature-title">Блок ${b.number}: ${escapeHtml(b.title)}</div>
          <div class="feature-desc">${escapeHtml(b.description || "")}</div>
        </a>`;
    }).join("");
    main.innerHTML = `
      <div class="welcome-card">
        <h1>🚀 Добро пожаловать в Data Science Course</h1>
        <p>Полный курс-самоучитель: Python, SQL, NumPy, Pandas, Matplotlib, статистика, EDA, ML, Feature Engineering и Production DS.</p>
      </div>
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-value">${state.summary.lessons_total || 0}</div>
          <div class="stat-label">Уроков в курсе</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">${completedLessons.size}</div>
          <div class="stat-label">Пройдено</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">${solvedExercises.size}</div>
          <div class="stat-label">Упражнений решено</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">${(state.achievements || []).filter(a => a.earned).length}</div>
          <div class="stat-label">Достижений</div>
        </div>
      </div>
      <h2 style="margin: 24px 0 16px;">Все блоки курса</h2>
      <div class="feature-grid">${blockCards}
        <a href="#/projects" class="feature-card">
          <div class="feature-icon">📁</div>
          <div class="feature-title">Проекты</div>
          <div class="feature-desc">20 практических проектов для портфолио.</div>
        </a>
        <a href="#/interview" class="feature-card">
          <div class="feature-icon">💼</div>
          <div class="feature-title">Собеседования</div>
          <div class="feature-desc">База вопросов с ответами для подготовки.</div>
        </a>
        <a href="#/achievements" class="feature-card">
          <div class="feature-icon">🏆</div>
          <div class="feature-title">Достижения</div>
          <div class="feature-desc">10 достижений за прогресс в обучении.</div>
        </a>
        <a href="#/final" class="feature-card">
          <div class="feature-icon">🎓</div>
          <div class="feature-title">Финальный проект</div>
          <div class="feature-desc">Комплексное задание для портфолио.</div>
        </a>
      </div>
    `;
  }

  async function renderLesson(number) {
    if (!number) {
      $("#main").innerHTML = `<div class="card"><h2>Урок не указан</h2></div>`;
      return;
    }
    const main = $("#main");
    main.innerHTML = `<div class="loading"><div class="spinner"></div><p>Загружаю урок ${number}...</p></div>`;
    try {
      const lesson = await api(`/lessons/${number}`);
      const content = lesson.content_json || {};
      const sections = content.sections || [];
      const minutes = content.minutes || lesson.estimated_minutes || 45;

      const block = lesson.block || {};
      let html = `
        <div class="view-header">
          <div class="breadcrumb">
            <a href="#/">Главная</a> / <a href="#/">Блок ${block.number}</a> / Урок ${lesson.number}
          </div>
          <h1>${escapeHtml(lesson.title)}</h1>
          <div style="display:flex; gap:12px; align-items:center; margin-top:8px; font-size:12px; color:var(--text-secondary);">
            <span>⏱ ${minutes} мин</span>
            <span>📊 Сложность: ${"⭐".repeat(lesson.difficulty || 2)}</span>
            ${completedLessons.has(lesson.number) ? '<span style="color:var(--success);">✅ Пройден</span>' : ''}
            <button class="btn ${completedLessons.has(lesson.number) ? '' : 'btn-success'}" id="mark-complete">
              ${completedLessons.has(lesson.number) ? 'Отметить непройденным' : '✅ Отметить пройденным'}
            </button>
          </div>
        </div>
      `;

      // Sections
      sections.forEach((sec, idx) => {
        const secId = `sec-${idx}`;
        const open = sec.type === "theory" || sec.type === "example";
        html += renderSection(sec, secId, open);
      });

      // Exercises
      if (lesson.exercises && lesson.exercises.length > 0) {
        html += `<h2 style="margin: 24px 0 12px;">💻 Упражнения (${lesson.exercises.length})</h2>`;
        lesson.exercises.forEach((ex, idx) => {
          html += renderExercise(ex, idx, lesson.number, lesson);
        });
      }

      // Navigation
      const navHtml = renderLessonNav(lesson.number);
      html += navHtml;

      main.innerHTML = html;

      // Bind section toggles
      $$(".section-header").forEach(h => {
        h.addEventListener("click", () => {
          const body = h.nextElementSibling;
          const toggle = h.querySelector(".section-toggle");
          body.classList.toggle("collapsed");
          toggle.classList.toggle("open");
        });
      });

      // Bind mark complete
      $("#mark-complete").addEventListener("click", () => {
        if (completedLessons.has(lesson.number)) {
          completedLessons.delete(lesson.number);
        } else {
          completedLessons.add(lesson.number);
          checkAchievements();
        }
        localStorage.setItem("ds_completed_lessons", JSON.stringify([...completedLessons]));
        api("/progress/update", {
          method: "POST",
          body: JSON.stringify({
            lesson_id: lesson.id,
            completed: completedLessons.has(lesson.number),
            score: 100,
          }),
        }).catch(() => {});
        renderLesson(lesson.number);
        updateProgressUI();
        loadAllLessonsForSidebar();
      });

      // Bind exercises
      bindExercises(lesson);

    } catch (e) {
      main.innerHTML = `<div class="card"><h2>Ошибка</h2><p>${escapeHtml(e.message)}</p></div>`;
    }
  }

  function renderSection(sec, id, open = true) {
    const icons = { theory: "📖", analogy: "🌌", example: "💡", visual: "🎨", common_mistakes: "⚠️", interview_questions: "🎯", knowledge_checklist: "✅" };
    const titles = { theory: "Теория", analogy: "Аналогия", example: "Пример", visual: "Визуализация", common_mistakes: "Типовые ошибки", interview_questions: "Вопросы собеседований", knowledge_checklist: "Чеклист знаний" };
    const icon = icons[sec.type] || "📌";
    const title = titles[sec.type] || sec.type;

    let body = "";
    if (sec.type === "theory") {
      body = `<div class="theory-content">${md(sec.content)}</div>`;
    } else if (sec.type === "analogy") {
      body = `
        <div class="analogy-box">
          <div class="label">🌍 Из жизни</div>
          <p>${escapeHtml(sec.real_world || "")}</p>
        </div>
        <div class="analogy-box" style="border-color: var(--accent-space)">
          <div class="label" style="color: var(--accent-space)">🚀 Пример из ${sec.domain_example && sec.domain_example.toLowerCase().includes("игр") ? "игр" : "космоса"}</div>
          <p>${escapeHtml(sec.domain_example || "")}</p>
        </div>
      `;
    } else if (sec.type === "example") {
      body = `
        <div class="example-box">
          <div class="example-problem">Задача: ${escapeHtml(sec.problem || "")}</div>
          <div class="example-explanation">${escapeHtml(sec.solution_explanation || "")}</div>
          <pre><code>${escapeHtml(sec.code || "")}</code></pre>
          <div class="example-output">${escapeHtml(sec.output || "")}</div>
          <div class="example-output-explanation">${escapeHtml(sec.output_explanation || "")}</div>
        </div>
      `;
    } else if (sec.type === "visual") {
      body = `
        <p>${escapeHtml(sec.description || "")}</p>
        ${sec.ascii_diagram ? `<div class="visual-ascii">${escapeHtml(sec.ascii_diagram)}</div>` : ""}
      `;
    } else if (sec.type === "common_mistakes") {
      body = (sec.items || []).map(item => `
        <div class="mistake-item">
          <div><code>${escapeHtml(item.mistake || "")}</code></div>
          <div class="why">❌ ${escapeHtml(item.why_bad || "")}</div>
          <div class="why" style="color: var(--success)">✅ ${escapeHtml(item.fix || "")}</div>
        </div>
      `).join("");
    } else if (sec.type === "interview_questions") {
      body = (sec.items || []).map(item => `
        <div class="interview-item">
          <div><strong>В:</strong> ${escapeHtml(item.q || "")}</div>
          <div class="a"><strong>О:</strong> ${escapeHtml(item.a || "")}</div>
        </div>
      `).join("");
    } else if (sec.type === "knowledge_checklist") {
      body = (sec.items || []).map((item, i) => `
        <label class="checklist-item">
          <input type="checkbox" data-cl="${i}"> ${escapeHtml(item)}
        </label>
      `).join("");
    }

    return `
      <div class="lesson-section" data-section-type="${sec.type}">
        <div class="section-header" data-toggle="${id}">
          <span class="section-icon">${icon}</span>
          <span class="section-title">${title}</span>
          <span class="section-toggle ${open ? "open" : ""}">▶</span>
        </div>
        <div class="section-body ${open ? "" : "collapsed"}">${body}</div>
      </div>
    `;
  }

  function renderExercise(ex, idx, lessonNumber, lesson) {
    const hintText = parseJsonField(ex.hints_json).join(" | ");
    const isSolved = solvedExercises.has(`${lessonNumber}.${ex.number}`);
    return `
      <div class="exercise" data-exercise-id="${ex.id}" data-ex-num="${ex.number}">
        <div class="exercise-header">
          <div class="exercise-num">${ex.number}</div>
          <div class="exercise-prompt">${escapeHtml(ex.prompt)}</div>
          <div class="exercise-difficulty">${"⭐".repeat(ex.difficulty || 2)}</div>
        </div>
        <div class="exercise-body">
          <div class="editor-pane">
            <div class="pane-label">📝 Редактор (${ex.type === "sql" ? "SQL" : "Python"})</div>
            <textarea class="code-editor" data-ex-type="${ex.type}" spellcheck="false">${escapeHtml(ex.starter_code || "")}</textarea>
          </div>
          <div class="output-pane">
            <div class="pane-label">📤 Вывод</div>
            <div class="output-area info" data-output>Нажми ▶ Запустить для проверки кода</div>
            <div class="plot-area" data-plot hidden></div>
          </div>
          <div class="hint-area">💡 ${escapeHtml(hintText)}</div>
          <div class="test-results"></div>
          <div class="exercise-actions">
            <button class="btn btn-primary" data-action="run">▶ Запустить</button>
            <button class="btn btn-success" data-action="check">✓ Проверить</button>
            <button class="btn" data-action="hint">💡 Подсказка</button>
            <button class="btn btn-warm" data-action="solution">📋 Решение</button>
            <button class="btn" data-action="reset">↺ Сбросить</button>
            ${isSolved ? '<span style="color: var(--success); font-size: 12px;">✅ Решено</span>' : ""}
          </div>
        </div>
      </div>
    `;
  }

  function bindExercises(lesson) {
    $$(".exercise").forEach(exEl => {
      const exId = parseInt(exEl.dataset.exerciseId);
      const exNum = parseInt(exEl.dataset.exNum);
      const editor = $(".code-editor", exEl);
      const output = $("[data-output]", exEl);
      const hintArea = $(".hint-area", exEl);
      const testResults = $(".test-results", exEl);

      // Ctrl+Enter для запуска
      editor.addEventListener("keydown", (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
          e.preventDefault();
          $("[data-action='run']", exEl).click();
        }
      });

      $("[data-action='run']", exEl).addEventListener("click", async () => {
        output.className = "output-area info";
        output.textContent = "⏳ Запускаю...";
        const plotArea = $("[data-plot]", exEl);
        if (plotArea) { plotArea.hidden = true; plotArea.innerHTML = ""; }
        const ex = lesson.exercises.find(e => e.id === exId);
        if (ex.type === "sql") {
          if (!window.SqlSandbox) { output.textContent = "SQL sandbox не загружен"; return; }
          const r = await window.SqlSandbox.executeQuery(editor.value);
          if (r.error) {
            output.className = "output-area error";
            output.textContent = "❌ Ошибка: " + r.error;
          } else {
            output.className = "output-area success";
            output.textContent = formatSqlResult(r);
          }
        } else {
          if (!window.PythonSandbox) { output.textContent = "Python sandbox не загружен"; return; }
          const r = await window.PythonSandbox.runCode(editor.value);
          if (r.stderr) {
            output.className = "output-area error";
            output.textContent = r.stderr || "(нет вывода)";
          } else {
            output.className = "output-area success";
            output.textContent = r.stdout || "(код выполнен успешно)";
            if (r.engine === "mock") {
              output.textContent += "\n\n⚠️ Mock-режим: для полноценной работы установите Pyodide локально.";
            }
          }
          if (r.plots && r.plots.length && plotArea) {
            plotArea.hidden = false;
            plotArea.innerHTML = r.plots.map(b64 =>
              `<img class="plot-img" src="data:image/png;base64,${b64}" alt="plot"/>`
            ).join("");
          }
        }
      });

      $("[data-action='check']", exEl).addEventListener("click", async () => {
        output.className = "output-area info";
        output.textContent = "⏳ Проверяю...";
        testResults.innerHTML = "";
        testResults.classList.add("visible");
        const ex = lesson.exercises.find(e => e.id === exId);
        try {
          if (ex.type === "sql") {
            const tests = parseJsonField(ex.test_cases_json);
            const result = await window.SqlSandbox.runAndCheck(editor.value, ex.expected_result_json);
            if (result.error) {
              output.className = "output-area error";
              output.textContent = "❌ " + result.error;
              return;
            }
            if (result.check.pass) {
              output.className = "output-area success";
              output.textContent = `✅ Правильно! ${result.rowCount} строк, ${result.timeMs}мс`;
              markSolved(lesson.number, ex.number, exId, true);
            } else {
              output.className = "output-area error";
              output.textContent = `❌ ${result.check.msg}\n\n${formatSqlResult(result)}`;
            }
          } else {
            const tests = parseJsonField(ex.test_cases_json);
            const result = await window.PythonSandbox.runAndCheck(editor.value, tests);
            if (result.error) {
              output.className = "output-area error";
              output.textContent = "❌ Ошибка: " + result.error;
              return;
            }
            const passed = result.results.filter(r => r.pass).length;
            const total = result.results.length;
            testResults.innerHTML = result.results.map(r => `
              <div class="test-result-item ${r.pass ? "pass" : "fail"}">
                <span>${r.pass ? "✓" : "✗"}</span>
                <span class="test-msg">${escapeHtml(r.description)} — ${escapeHtml(r.msg)}</span>
              </div>
            `).join("");
            if (passed === total && total > 0) {
              output.className = "output-area success";
              output.textContent = `✅ Все тесты пройдены (${passed}/${total})!`;
              markSolved(lesson.number, ex.number, exId, true);
            } else {
              output.className = "output-area error";
              output.textContent = `❌ Пройдено ${passed}/${total} тестов`;
            }
            if (result.plots && result.plots.length) {
              const plotArea = $("[data-plot]", exEl);
              if (plotArea) {
                plotArea.hidden = false;
                plotArea.innerHTML = result.plots.map(b64 =>
                  `<img class="plot-img" src="data:image/png;base64,${b64}" alt="plot"/>`
                ).join("");
              }
            }
          }
        } catch (e) {
          output.className = "output-area error";
          output.textContent = "❌ " + e.message;
        }
      });

      $("[data-action='hint']", exEl).addEventListener("click", () => {
        hintArea.classList.toggle("visible");
      });

      $("[data-action='solution']", exEl).addEventListener("click", async () => {
        try {
          const data = await api(`/lessons/${lesson.number}/solution/${exNum}`);
          editor.value = data.solution;
          output.className = "output-area info";
          output.textContent = "📋 Решение загружено в редактор. Нажми ✓ Проверить.";
        } catch (e) {
          output.textContent = "❌ Не удалось загрузить решение: " + e.message;
          output.className = "output-area error";
        }
      });

      $("[data-action='reset']", exEl).addEventListener("click", () => {
        const ex = lesson.exercises.find(e => e.id === exId);
        editor.value = ex.starter_code || "";
        output.className = "output-area info";
        output.textContent = "↺ Сброшено";
        testResults.innerHTML = "";
        testResults.classList.remove("visible");
        hintArea.classList.remove("visible");
      });
    });
  }

  function markSolved(lessonNumber, exNumber, exId, passed) {
    const key = `${lessonNumber}.${exNumber}`;
    if (passed) {
      solvedExercises.add(key);
      api("/progress/attempt", {
        method: "POST",
        body: JSON.stringify({ exercise_id: exId, user_code: "", passed: true, score: 100 }),
      }).catch(() => {});
      checkAchievements();
    }
    localStorage.setItem("ds_solved_exercises", JSON.stringify([...solvedExercises]));
    // Если все упражнения урока решены — отметить урок пройденным
    if (passed) {
      // Опционально: можно отметить урок
    }
  }

  function formatSqlResult(r) {
    if (r.rowCount === 0) return "(пустой результат)";
    let lines = [`Строк: ${r.rowCount} | ${r.timeMs}мс`, ""];
    if (r.columns && r.columns.length > 0) {
      // Простая таблица
      const widths = r.columns.map((c, i) =>
        Math.max(c.length, ...r.rows.map(row => String(row[c] ?? "").length))
      );
      lines.push(r.columns.map((c, i) => c.padEnd(widths[i])).join(" | "));
      lines.push(widths.map(w => "-".repeat(w)).join("-+-"));
      r.rows.slice(0, 50).forEach(row => {
        lines.push(r.columns.map((c, i) => String(row[c] ?? "").padEnd(widths[i])).join(" | "));
      });
      if (r.rowCount > 50) lines.push(`... ещё ${r.rowCount - 50} строк`);
    }
    return lines.join("\n");
  }

  function renderLessonNav(currentNumber) {
    if (!state.allLessons) return "";
    const idx = state.allLessons.findIndex(l => l.number === currentNumber);
    const prev = idx > 0 ? state.allLessons[idx - 1] : null;
    const next = idx < state.allLessons.length - 1 ? state.allLessons[idx + 1] : null;
    return `
      <div class="lesson-nav">
        ${prev ? `<a href="#/lesson/${prev.number}" class="btn">← ${escapeHtml(prev.title)}</a>` : "<span></span>"}
        ${next ? `<a href="#/lesson/${next.number}" class="btn">${escapeHtml(next.title)} →</a>` : "<span></span>"}
      </div>
    `;
  }

  async function renderProjects() {
    const main = $("#main");
    main.innerHTML = `<div class="loading"><div class="spinner"></div><p>Загружаю проекты...</p></div>`;
    try {
      const projects = await api("/projects/");
      let html = `
        <div class="view-header">
          <h1>📁 Проекты для портфолио</h1>
          <p style="color: var(--text-secondary); margin-top: 4px;">20 практических проектов: 10 игровых + 10 космических. Применяй знания из разных блоков.</p>
        </div>
      `;
      const games = projects.filter(p => p.theme === "gaming");
      const space = projects.filter(p => p.theme === "space");
      const others = projects.filter(p => p.theme !== "gaming" && p.theme !== "space");

      if (games.length > 0) {
        html += `<h2 style="margin: 16px 0 12px;">🎮 Игровые проекты</h2>`;
        html += games.map(p => renderProjectCard(p)).join("");
      }
      if (space.length > 0) {
        html += `<h2 style="margin: 24px 0 12px;">🚀 Космические проекты</h2>`;
        html += space.map(p => renderProjectCard(p)).join("");
      }
      if (others.length > 0) {
        html += `<h2 style="margin: 24px 0 12px;">📌 Другие</h2>`;
        html += others.map(p => renderProjectCard(p)).join("");
      }

      main.innerHTML = html;
    } catch (e) {
      main.innerHTML = `<div class="card"><h2>Ошибка</h2><p>${escapeHtml(e.message)}</p></div>`;
    }
  }

  function renderProjectCard(p) {
    return `
      <a href="#/project/${p.id}" class="project-card" style="text-decoration:none;color:inherit;display:block;">
        <div class="p-title">${escapeHtml(p.title)}</div>
        <div class="p-desc">${escapeHtml(p.description || "")}</div>
        <div class="p-meta">
          ${p.theme ? `<span class="badge theme-${p.theme}">${p.theme === "space" ? "🚀 Космос" : p.theme === "gaming" ? "🎮 Игры" : "📌 Разное"}</span>` : ""}
          ${p.block_title ? `<span class="badge">${escapeHtml(p.block_title)}</span>` : ""}
          ${p.difficulty ? `<span class="badge">${"⭐".repeat(p.difficulty)}</span>` : ""}
        </div>
      </a>
    `;
  }

  async function renderProject(id) {
    const main = $("#main");
    main.innerHTML = `<div class="loading"><div class="spinner"></div><p>Загружаю проект...</p></div>`;
    try {
      const p = await api(`/projects/${id}`);
      let datasetStr = "";
      try {
        const d = typeof p.dataset_json === "string" ? JSON.parse(p.dataset_json) : p.dataset_json;
        if (d && Object.keys(d).length > 0) {
          const summary = Object.keys(d).slice(0, 6).map(k => {
            const v = d[k];
            const preview = Array.isArray(v) ? `[массив ${v.length} элементов]` :
                            typeof v === "object" && v !== null ? `{${Object.keys(v).slice(0,3).join(", ")}...}` :
                            JSON.stringify(v).slice(0, 60);
            return `<li><code>${escapeHtml(k)}</code>: ${escapeHtml(preview)}</li>`;
          }).join("");
          datasetStr = `
            <div class="card">
              <h2>📊 Данные</h2>
              <p>Структура сгенерированного датасета:</p>
              <ul>${summary}</ul>
            </div>
          `;
        }
      } catch (e) {}

      const html = `
        <div class="view-header">
          <div class="breadcrumb">
            <a href="#/">Главная</a> / <a href="#/projects">Проекты</a> / ${escapeHtml(p.title)}
          </div>
          <h1>${escapeHtml(p.title)}</h1>
          <div style="display:flex; gap:12px; margin-top:8px; font-size:13px;">
            <span class="badge theme-${p.theme}">${p.theme === "space" ? "🚀 Космос" : p.theme === "gaming" ? "🎮 Игры" : "📌 Разное"}</span>
            <span class="badge">${"⭐".repeat(p.difficulty || 3)}</span>
            ${p.block_title ? `<span class="badge">${escapeHtml(p.block_title)}</span>` : ""}
          </div>
        </div>

        <div class="card">
          <h2>📋 Описание</h2>
          <p style="white-space:pre-line; line-height:1.6;">${escapeHtml(p.description || "")}</p>
        </div>

        ${datasetStr}

        <div class="card">
          <h2>🚀 Стартовый код</h2>
          <p style="color: var(--text-secondary); font-size:13px;">Скопируй, доработай, запусти. Метки <code>TODO</code> показывают, что нужно реализовать.</p>
          <pre style="background:#0a0a1a; padding:14px; border-radius:6px; overflow:auto; max-height:380px;"><code>${escapeHtml(p.template_code || "# (код появится скоро)")}</code></pre>
        </div>

        <div class="card">
          <h2>✅ Эталонное решение</h2>
          <p style="color: var(--text-secondary); font-size:13px;">Сверься с этим решением, если застрял. Постарайся сначала решить сам.</p>
          <details>
            <summary style="cursor:pointer; color: var(--accent);">Показать решение</summary>
            <pre style="background:#0a0a1a; padding:14px; border-radius:6px; overflow:auto; max-height:480px; margin-top:10px;"><code>${escapeHtml(p.solution_code || "# (решение появится скоро)")}</code></pre>
          </details>
        </div>

        <div style="margin-top:24px;">
          <a href="#/projects" class="btn">← Назад к проектам</a>
        </div>
      `;
      main.innerHTML = html;
    } catch (e) {
      main.innerHTML = `<div class="card"><h2>Ошибка</h2><p>${escapeHtml(e.message)}</p></div>`;
    }
  }

  async function renderInterview() {
    const main = $("#main");
    main.innerHTML = `<div class="loading"><div class="spinner"></div><p>Загружаю вопросы...</p></div>`;
    try {
      const all = await api("/interview/?limit=200");
      const categories = [...new Set(all.map(q => q.category))];
      let html = `
        <div class="view-header">
          <h1>💼 Подготовка к собеседованиям</h1>
          <p style="color: var(--text-secondary); margin-top: 4px;">База вопросов для Junior Data Scientist. Используй фильтры для тренировки.</p>
        </div>
        <div class="filter-bar" id="interview-filters">
          <button class="filter-btn active" data-cat="all">Все</button>
          ${categories.map(c => `<button class="filter-btn" data-cat="${c}">${c}</button>`).join("")}
          <button class="filter-btn" data-top="1">⭐ Часто задают</button>
          <button class="filter-btn" data-action="random">🎲 Случайный</button>
        </div>
        <div id="interview-list"></div>
      `;
      main.innerHTML = html;

      const showQuestions = (filter = "all", top = false) => {
        let filtered = all;
        if (filter !== "all") filtered = filtered.filter(q => q.category === filter);
        if (top) filtered = filtered.filter(q => q.is_top);
        const list = $("#interview-list");
        list.innerHTML = filtered.map(q => `
          <div class="interview-card">
            <div class="q">${escapeHtml(q.question)}</div>
            <div class="a">${escapeHtml(q.answer)}</div>
            ${q.explanation ? `<div class="explanation">💡 ${escapeHtml(q.explanation)}</div>` : ""}
            ${q.common_mistakes ? `<div class="mistakes">⚠️ ${escapeHtml(q.common_mistakes)}</div>` : ""}
            <div class="badges">
              <span class="badge category">${escapeHtml(q.category)}</span>
              <span class="badge">${q.difficulty}</span>
              ${q.is_top ? '<span class="badge top">⭐ Часто</span>' : ""}
            </div>
          </div>
        `).join("") || "<p>Нет вопросов по фильтру</p>";
      };
      showQuestions();

      $$("#interview-filters .filter-btn").forEach(btn => {
        btn.addEventListener("click", () => {
          if (btn.dataset.action === "random") {
            const q = all[Math.floor(Math.random() * all.length)];
            $("#interview-list").innerHTML = `
              <div class="interview-card">
                <div class="q">${escapeHtml(q.question)}</div>
                <details>
                  <summary style="cursor:pointer; color: var(--accent-space); margin: 8px 0;">Показать ответ</summary>
                  <div class="a">${escapeHtml(q.answer)}</div>
                  ${q.explanation ? `<div class="explanation">💡 ${escapeHtml(q.explanation)}</div>` : ""}
                </details>
              </div>
            `;
            return;
          }
          $$("#interview-filters .filter-btn").forEach(b => b.classList.remove("active"));
          btn.classList.add("active");
          showQuestions(btn.dataset.cat || "all", btn.dataset.top === "1");
        });
      });
    } catch (e) {
      main.innerHTML = `<div class="card"><h2>Ошибка</h2><p>${escapeHtml(e.message)}</p></div>`;
    }
  }

  async function renderAchievements() {
    const main = $("#main");
    let html = `
      <div class="view-header">
        <h1>🏆 Достижения</h1>
        <p style="color: var(--text-secondary); margin-top: 4px;">Зарабатывай достижения, проходя курс.</p>
      </div>
    `;
    if (!state.achievements || state.achievements.length === 0) {
      html += `<div class="card"><p>Достижения не загружены.</p></div>`;
    } else {
      html += state.achievements.map(a => `
        <div class="achievement-card ${a.earned ? "earned" : ""}">
          <div class="achievement-icon">${a.icon || "🏆"}</div>
          <div class="achievement-info">
            <div class="a-title">${escapeHtml(a.title)}</div>
            <div class="a-desc">${escapeHtml(a.description || "")}</div>
          </div>
          <div class="achievement-status">${a.earned ? "✓ Получено" : "🔒"}</div>
        </div>
      `).join("");
    }
    main.innerHTML = html;
  }

  async function renderFinal() {
    const main = $("#main");
    main.innerHTML = `
      <div class="view-header">
        <h1>🎓 Финальный проект</h1>
        <p style="color: var(--text-secondary); margin-top: 4px;">"От данных до решения: полный Data Science цикл"</p>
      </div>
      <div class="card">
        <h2>Этапы финального проекта</h2>
        <ol style="margin: 12px 0 0 24px; line-height: 2;">
          <li><strong>Бизнес-задача</strong> — формулировка, метрики успеха</li>
          <li><strong>Данные</strong> — загрузка, первичный осмотр</li>
          <li><strong>Очистка</strong> — пропуски, выбросы, типы</li>
          <li><strong>EDA</strong> — гипотезы, инсайты, визуализации</li>
          <li><strong>Статистика</strong> — проверка гипотез, значимость</li>
          <li><strong>Feature Engineering</strong> — новые признаки, кодирование</li>
          <li><strong>Моделирование</strong> — 3+ модели, сравнение</li>
          <li><strong>Оценка</strong> — метрики, интерпретация, выводы</li>
          <li><strong>Визуализация</strong> — финальный дашборд</li>
          <li><strong>Оформление</strong> — README, структура репо</li>
          <li><strong>Кейс для резюме</strong> — описание для HR</li>
        </ol>
      </div>
      <div class="card">
        <h2>Выбери тему</h2>
        <p>Космос (SpaceX данные) или Игры (игровая платформа). Начни с любого блока, где есть нужные навыки.</p>
        <div class="feature-grid" style="margin-top: 16px;">
          <a href="#/lesson/1.1" class="feature-card">
            <div class="feature-icon">🚀</div>
            <div class="feature-title">Космос: начни с Python</div>
            <div class="feature-desc">Блок 1 → 3 → 4 → 6 → 7</div>
          </a>
          <a href="#/lesson/2.1" class="feature-card">
            <div class="feature-icon">🎮</div>
            <div class="feature-title">Игры: начни с SQL</div>
            <div class="feature-desc">Блок 2 → 3 → 5 → 7</div>
          </a>
        </div>
      </div>
    `;
  }

  // ============================================================================
  // Достижения
  // ============================================================================
  function checkAchievements() {
    // first_lesson
    if (completedLessons.size >= 1) earnAch("first_lesson");
    // python_master
    if (isBlockDone(1)) earnAch("python_master");
    // sql_wizard
    if (isBlockDone(2)) earnAch("sql_wizard");
    // no_hints
    if (solvedExercises.size >= 10) earnAch("no_hints");
    // half_way
    if (state.summary.lessons_total > 0 &&
        completedLessons.size >= state.summary.lessons_total / 2) {
      earnAch("half_way");
    }
  }

  function isBlockDone(blockNum) {
    if (!state.allLessons) return false;
    const blockLessons = state.allLessons.filter(l => l.block_id === blockNum);
    return blockLessons.length > 0 && blockLessons.every(l => completedLessons.has(l.number));
  }

  function earnAch(key) {
    api(`/achievements/earn/${key}`, { method: "POST" })
      .then(r => {
        if (r.status === "earned") {
          const ach = state.achievements.find(a => a.key === key);
          if (ach) showAchievementModal(ach);
        }
      })
      .catch(() => {});
  }

  function showAchievementModal(ach) {
    $("#achievement-icon").textContent = ach.icon || "🏆";
    $("#achievement-title").textContent = "Получено: " + ach.title;
    $("#achievement-desc").textContent = ach.description || "";
    $("#achievement-modal").classList.remove("hidden");
  }

  // ============================================================================
  // Init
  // ============================================================================
  async function init() {
    window.SandboxLog = (msg, level) => console[level === "error" ? "error" : "log"]("[sandbox]", msg);
    window.addEventListener("hashchange", route);
    try {
      await loadInitial();
    } catch (e) {
      $("#main").innerHTML = `<div class="card"><h2>Ошибка загрузки</h2><p>${escapeHtml(e.message)}</p></div>`;
      return;
    }
    // Preload sandboxes
    if (window.PythonSandbox) {
      window.PythonSandbox.ensurePyodide().catch(() => {});
    }
    await route();
  }

  document.addEventListener("DOMContentLoaded", init);
})();
