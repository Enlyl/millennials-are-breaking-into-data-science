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

  // Активные интервалы (прогресс-бары), которые нужно чистить при навигации
  let _activeTimers = [];

  // Runtime status indicator (sidebar)
  function setRuntimeStatus(engine, state) {
    const row = document.querySelector(`.runtime-status .rs-row[data-engine="${engine}"]`);
    if (!row) return;
    const stateEl = row.querySelector(".rs-state");
    row.classList.remove("ready", "failed", "loading");
    if (state === "ready") {
      row.classList.add("ready");
      stateEl.textContent = "✓ готов";
    } else if (state === "failed") {
      row.classList.add("failed");
      stateEl.textContent = "✗ недоступен";
    } else {
      row.classList.add("loading");
      stateEl.textContent = "⏳ загрузка";
    }
  }
  setRuntimeStatus("py", "loading");
  setRuntimeStatus("sql", "loading");

  // Theme switcher
  const NU_ICONS = {
    "🚀": "💀", "🏠": "🤘",
    "🏆": "🎵", "📁": "🛠️", "💼": "📋", "🎓": "🏁",
  };
  const NU_BLOCK_ICONS = ["🎧", "🕹️", "🥁", "🎸", "💣", "📼", "🦴", "📻", "🎙️"];

  // Teenage Engineering: minimalist geometric shapes, off-white, black ink
  const TE_ICONS = {
    "🚀": "▶", "🏠": "□",
    "🏆": "★", "📁": "▤", "💼": "▦", "🎓": "◉",
  };
  const TE_BLOCK_ICONS = ["■", "▢", "▣", "▤", "▥", "▦", "▧", "▨", "▩"];

  function getThemeIcon(defaultIcon, theme) {
    if (theme === "nu-metal" && NU_ICONS[defaultIcon]) return NU_ICONS[defaultIcon];
    if (theme === "teenage-engineering" && TE_ICONS[defaultIcon]) return TE_ICONS[defaultIcon];
    return defaultIcon;
  }

  function setTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("ds_theme", theme);
    document.querySelectorAll(".theme-btn").forEach(b => {
      b.classList.toggle("active", b.dataset.theme === theme);
    });
    // Only re-render home page icons (CSS handles nav/sidebar icons)
    if (location.hash === "#/" || location.hash === "") {
      renderHome();
    }
  }
  function initTheme() {
    const saved = localStorage.getItem("ds_theme") || "dark";
    document.documentElement.setAttribute("data-theme", saved);
    document.querySelectorAll(".theme-btn").forEach(b => {
      b.classList.toggle("active", b.dataset.theme === saved);
      b.addEventListener("click", () => setTheme(b.dataset.theme));
    });
  }

  // Splash screen
  const splashMsg = () => document.getElementById("splash-msg");
  function updateSplash(msg) {
    const el = splashMsg();
    if (el) el.textContent = msg;
  }
  function hideSplash() {
    const el = document.getElementById("splash");
    if (el) el.classList.add("hidden");
  }

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
    // Ждём уроки перед рендером сайдбара — избегаем layout shift
    await loadAllLessonsForSidebar();
    renderSidebarFull();
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
    renderSidebarFull();
  }

  function renderSidebarFull() {
    const nav = $("#blocks-nav");
    if (!nav) return;
    const themeClass = { space: "theme-space", gaming: "theme-gaming", mixed: "theme-mixed", neutral: "theme-mixed" };
    const collapsed = new Set(JSON.parse(localStorage.getItem("ds_sidebar_collapsed") || "[]"));
    let html = "";
    for (const block of state.blocks) {
      if (block.number === 10) continue;
      const blockLessons = state.allLessons.filter(l => l.block_id === block.id);
      if (blockLessons.length === 0) continue;
      const theme = themeClass[block.theme] || "theme-mixed";
      const isCollapsed = collapsed.has(block.number);
      html += `<div class="block-wrapper ${isCollapsed ? "collapsed" : ""}" data-block="${block.number}">
        <div class="block-title ${theme}">
          <span class="collapse-arrow">${isCollapsed ? "▶" : "▼"}</span>
          <span class="block-num">${block.number}</span>${escapeHtml(block.title)}
        </div>
        <div class="block-lessons">`;
      for (const lesson of blockLessons) {
        const isCompleted = completedLessons.has(lesson.number);
        const status = isCompleted ? "✅" : "○";
        const statusClass = isCompleted ? "completed" : "available";
        html += `<a href="#/lesson/${lesson.number}" class="lesson-link ${isCompleted ? "completed" : ""}" data-lesson="${lesson.number}">
          <span class="lesson-status ${statusClass}">${status}</span>
          <span class="lesson-title">${escapeHtml(lesson.title)}</span>
        </a>`;
      }
      html += `</div></div>`;
    }
    nav.innerHTML = html;
    // Collapse toggle
    nav.querySelectorAll(".block-title").forEach(el => {
      el.addEventListener("click", function(e) {
        if (e.target.closest(".lesson-link")) return;
        const wrapper = this.closest(".block-wrapper");
        if (!wrapper) return;
        const blockNum = parseInt(wrapper.dataset.block);
        const arrow = this.querySelector(".collapse-arrow");
        const wasCollapsed = wrapper.classList.toggle("collapsed");
        arrow.textContent = wasCollapsed ? "▶" : "▼";
    const collapsedRaw = localStorage.getItem("ds_sidebar_collapsed");
    if (!collapsedRaw) {
      const nums = state.blocks.filter(b => b.number !== 10).map(b => b.number);
      localStorage.setItem("ds_sidebar_collapsed", JSON.stringify(nums));
    }
    const collapsed = new Set(JSON.parse(localStorage.getItem("ds_sidebar_collapsed") || "[]"));
        if (wasCollapsed) { collapsed.add(blockNum); } else { collapsed.delete(blockNum); }
        localStorage.setItem("ds_sidebar_collapsed", JSON.stringify([...collapsed]));
      });
    });
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
    // Очищаем активные таймеры при навигации
    _activeTimers.forEach(t => clearInterval(t));
    _activeTimers = [];

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
    const curTheme = document.documentElement.getAttribute("data-theme") || "dark";
    const themeIcon = { space: "🚀", gaming: "🎮", mixed: "📊", neutral: "📚" };
    const blockCards = (state.blocks || []).filter(b => b.number <= 9).map(b => {
      let icon;
      if (curTheme === "nu-metal") {
        icon = NU_BLOCK_ICONS[(b.number - 1) % NU_BLOCK_ICONS.length];
      } else if (curTheme === "teenage-engineering") {
        icon = TE_BLOCK_ICONS[(b.number - 1) % TE_BLOCK_ICONS.length];
      } else {
        icon = getThemeIcon(themeIcon[b.theme] || "📚", curTheme);
      }
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
        <h1>${getThemeIcon("🚀", curTheme)} Добро пожаловать в Data Science Course</h1>
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
          <div class="feature-icon">${getThemeIcon("📁", curTheme)}</div>
          <div class="feature-title">Проекты</div>
          <div class="feature-desc">20 практических проектов для портфолио.</div>
        </a>
        <a href="#/interview" class="feature-card">
          <div class="feature-icon">${getThemeIcon("💼", curTheme)}</div>
          <div class="feature-title">Собеседования</div>
          <div class="feature-desc">База вопросов с ответами для подготовки.</div>
        </a>
        <a href="#/achievements" class="feature-card">
          <div class="feature-icon">${getThemeIcon("🏆", curTheme)}</div>
          <div class="feature-title">Достижения</div>
          <div class="feature-desc">10 достижений за прогресс в обучении.</div>
        </a>
        <a href="#/final" class="feature-card">
          <div class="feature-icon">${getThemeIcon("🎓", curTheme)}</div>
          <div class="feature-title">Финальный проект</div>
          <div class="feature-desc">Комплексное задание для портфолио.</div>
        </a>
      </div>
    `;
  }

  function updateMarkCompleteBtn(lessonNum) {
    const btn = $("#mark-complete");
    if (!btn) return;
    const isDone = completedLessons.has(lessonNum);
    btn.textContent = isDone ? "✓ Выполнено" : "✓ Отметить выполненным";
    btn.classList.toggle("btn-success", !isDone);
    btn.classList.toggle("btn-secondary", isDone);
  }

  function updateSidebarLessonStatus(lessonNum) {
    const link = document.querySelector(`#blocks-nav .lesson-link[data-lesson="${lessonNum}"]`);
    if (!link) return;
    const isDone = completedLessons.has(lessonNum);
    link.classList.toggle("completed", isDone);
    const status = link.querySelector(".lesson-status");
    if (status) {
      status.textContent = isDone ? "✅" : "○";
      status.className = isDone ? "lesson-status completed" : "lesson-status available";
    }
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
        const toggle = () => {
          const body = h.nextElementSibling;
          const t = h.querySelector(".section-toggle");
          body.classList.toggle("collapsed");
          t.classList.toggle("open");
        };
        h.addEventListener("click", toggle);
        h.addEventListener("keydown", e => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); toggle(); } });
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
        // Targeted update instead of full re-render
        updateMarkCompleteBtn(lesson.number);
        updateProgressUI();
        // Sidebar lesson status update in-place
        updateSidebarLessonStatus(lesson.number);
      });

      // Bind exercises
      bindExercises(lesson);

    } catch (e) {
      main.innerHTML = `<div class="card"><h2>Ошибка</h2><p>${escapeHtml(e.message)}</p></div>`;
    }
  }

  function renderSection(sec, id, open = true) {
    const icons = {
      theory: "📖", analogy: "🌌", example: "💡", visual: "🎨",
      common_mistakes: "⚠️", interview_questions: "🎯", knowledge_checklist: "✅",
      learning_objectives: "🎯", summary: "📌", glossary: "📚",
      further_reading: "🔗", prerequisites: "📋"
    };
    const titles = {
      theory: "Теория", analogy: "Аналогия", example: "Пример", visual: "Визуализация",
      common_mistakes: "Типовые ошибки", interview_questions: "Вопросы собеседований",
      knowledge_checklist: "Чеклист знаний",
      learning_objectives: "Цели урока", summary: "Ключевые выводы",
      glossary: "Глоссарий", further_reading: "Дополнительные материалы",
      prerequisites: "Что нужно знать"
    };
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
    } else if (sec.type === "learning_objectives") {
      body = `
        <div class="objectives-box">
          <p style="margin-bottom: var(--space-3); color: var(--text-secondary); font-size: var(--text-sm);">
            🎯 После этого урока ты сможешь:
          </p>
          <ul class="objectives-list">
            ${(sec.items || []).map(item => `<li>${escapeHtml(item)}</li>`).join("")}
          </ul>
        </div>
      `;
    } else if (sec.type === "summary") {
      body = `
        <div class="summary-box">
          <ul class="summary-list">
            ${(sec.items || []).map(item => `<li>${escapeHtml(item)}</li>`).join("")}
          </ul>
        </div>
      `;
    } else if (sec.type === "glossary") {
      body = `
        <div class="glossary-box">
          ${(sec.items || []).map(item => `
            <div class="glossary-item">
              <div class="glossary-term">${escapeHtml(item.term || "")}</div>
              <div class="glossary-definition">${escapeHtml(item.definition || "")}</div>
            </div>
          `).join("")}
        </div>
      `;
    } else if (sec.type === "further_reading") {
      body = `
        <div class="further-reading-box">
          <ul class="further-reading-list">
            ${(sec.items || []).map(item => `
              <li>
                <a href="${escapeHtml(item.url || "#")}" target="_blank" rel="noopener noreferrer">
                  ${escapeHtml(item.title || item.url || "")}
                </a>
                ${item.description ? `<div class="fr-desc">${escapeHtml(item.description)}</div>` : ""}
              </li>
            `).join("")}
          </ul>
        </div>
      `;
    } else if (sec.type === "prerequisites") {
      body = `
        <div class="prerequisites-box">
          <p style="color: var(--text-secondary); margin-bottom: var(--space-3);">
            📋 Перед изучением этого урока рекомендуется пройти:
          </p>
          <ul class="prerequisites-list">
            ${(sec.items || []).map(item => `<li>${escapeHtml(item)}</li>`).join("")}
          </ul>
        </div>
      `;
    }

    return `
      <div class="lesson-section" data-section-type="${sec.type}">
        <div class="section-header" data-toggle="${id}" tabindex="0" role="button">
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
        if (exEl.dataset.busy === "1") return;
        exEl.dataset.busy = "1";
        const runBtn = $("[data-action='run']", exEl);
        const chkBtn = $("[data-action='check']", exEl);
        runBtn.disabled = true;
        chkBtn.disabled = true;
        try {
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
            const code = editor.value;
            const needsMpl = /^\s*(import\s+matplotlib|from\s+matplotlib)/m.test(code) ||
                             /^\s*(import\s+numpy|from\s+numpy)/m.test(code);
            const mplReady = window.PythonSandbox.matplotlibLoaded;
            let progressTimer = null;
            if (needsMpl && !mplReady) {
              let s = 0;
              progressTimer = setInterval(() => {
                s += 2;
                output.textContent = `⏳ Загружаю matplotlib... (${s}с, нужно при первом запуске)`;
              }, 2000);
              _activeTimers.push(progressTimer);
            }
            const r = await window.PythonSandbox.runCode(code);
            if (progressTimer) { clearInterval(progressTimer); _activeTimers = _activeTimers.filter(t => t !== progressTimer); }
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
        } finally {
          runBtn.disabled = false;
          chkBtn.disabled = false;
          exEl.dataset.busy = "0";
        }
      });

      $("[data-action='check']", exEl).addEventListener("click", async () => {
        if (exEl.dataset.busy === "1") return;
        exEl.dataset.busy = "1";
        const runBtn = $("[data-action='run']", exEl);
        const chkBtn = $("[data-action='check']", exEl);
        runBtn.disabled = true;
        chkBtn.disabled = true;
        try {
          output.className = "output-area info";
          output.textContent = "⏳ Проверяю...";
          testResults.innerHTML = "";
          testResults.classList.add("visible");
          const ex = lesson.exercises.find(e => e.id === exId);
          if (ex.type === "sql") {
            const result = await window.SqlSandbox.runAndCheck(editor.value, ex.expected_result_json, ex.solution_code);
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
            const checkCode = editor.value;
            const checkNeedsMpl = /^\s*(import\s+matplotlib|from\s+matplotlib)/m.test(checkCode) ||
                                  /^\s*(import\s+numpy|from\s+numpy)/m.test(checkCode);
            const mplReady = window.PythonSandbox.matplotlibLoaded;
            let checkProgressTimer = null;
            if (checkNeedsMpl && !mplReady) {
              let cs = 0;
              checkProgressTimer = setInterval(() => {
                cs += 2;
                output.textContent = `⏳ Загружаю matplotlib... (${cs}с, нужно при первом запуске)`;
              }, 2000);
              _activeTimers.push(checkProgressTimer);
            }
            const result = await window.PythonSandbox.runAndCheck(checkCode, tests);
            if (checkProgressTimer) { clearInterval(checkProgressTimer); _activeTimers = _activeTimers.filter(t => t !== checkProgressTimer); }
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
        } finally {
          runBtn.disabled = false;
          chkBtn.disabled = false;
          exEl.dataset.busy = "0";
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
        if (!confirm("Сбросить код упражнения? Результат не сохранится.")) return;
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
          <div class="interview-card" data-q="${escapeHtml(q.question)}">
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
          showQuestions("all", false);
          setTimeout(() => {
            const card = document.querySelector(`.interview-card[data-q="${escapeHtml(q.question)}"]`);
            if (card) {
              card.scrollIntoView({ behavior: "smooth", block: "center" });
              card.style.boxShadow = "0 0 0 2px var(--accent-ds)";
              setTimeout(() => card.style.boxShadow = "", 3000);
            }
          }, 0);
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
      <div class="card" id="final-theme-chooser">
        <h2>Выбери тему проекта</h2>
        <p>Пройди полный цикл Data Science: от бизнес-задачи до ML-модели и отчёта.</p>
        <div class="feature-grid" style="margin-top: 16px;" id="final-theme-cards">
          <div class="feature-card" data-theme="space" style="cursor:pointer;">
            <div class="feature-icon">🚀</div>
            <div class="feature-title">Космос: анализ миссий NASA</div>
            <div class="feature-desc">200 миссий, прогноз успеха, дашборд</div>
          </div>
          <div class="feature-card" data-theme="gaming" style="cursor:pointer;">
            <div class="feature-icon">🎮</div>
            <div class="feature-title">Игры: анализ поведения игроков</div>
            <div class="feature-desc">200 игроков, прогноз оттока, рекомендации</div>
          </div>
        </div>
      </div>
      <div id="final-project-content"></div>
    `;
    $$("#final-theme-cards .feature-card").forEach(card => {
      card.addEventListener("click", () => loadFinalProject(card.dataset.theme));
    });
  }

  async function loadFinalProject(theme) {
    const content = $("#final-project-content");
    const chooser = $("#final-theme-chooser");
    content.innerHTML = `<div class="loading"><div class="spinner"></div><p>Загружаю проект...</p></div>`;
    try {
      const fp = await api("/final-project/" + theme);
      chooser.style.display = "none";
      let datasetStr = "";
      try {
        const ds = fp.dataset_json || {};
        const keys = Object.keys(ds).slice(0, 6);
        if (keys.length > 0) {
          datasetStr = keys.map(k => {
            const v = ds[k];
            const preview = Array.isArray(v) ? `[массив ${v.length} элементов]` :
                            typeof v === "object" && v !== null ? `{${Object.keys(v).slice(0,3).join(", ")}...}` :
                            String(v).slice(0, 60);
            return `<li><code>${escapeHtml(k)}</code>: ${escapeHtml(preview)}</li>`;
          }).join("");
          const totalEntries = ds.mission_id ? ds.mission_id.length : ds.player_id ? ds.player_id.length : "200";
          datasetStr = `
            <div class="card">
              <h2>📊 Данные</h2>
              <p>Датасет содержит <strong>${totalEntries} записей</strong>. Ниже — структура ключевых полей.</p>
              <ul>${datasetStr}</ul>
            </div>
          `;
        }
      } catch (e) {}

      const stepsHtml = (fp.steps_json || []).map(s => `
        <details style="margin: 8px 0;">
          <summary style="cursor:pointer; color: var(--accent); font-weight:600;">
            Шаг ${s.step}: ${escapeHtml(s.title)}
          </summary>
          <p style="margin: 8px 0 4px 0; line-height:1.5;">${escapeHtml(s.description)}</p>
          ${s.lessons && s.lessons.length ? `
            <p style="font-size:13px; color: var(--text-secondary);">
              📚 Связанные уроки: ${s.lessons.map(l => `<a href="#/lesson/${l}" style="color: var(--accent-space);">${l}</a>`).join(", ")}
            </p>
          ` : ""}
        </details>
      `).join("");

      content.innerHTML = `
        <div class="view-header" style="margin-top:24px;">
          <h1>${escapeHtml(fp.title)}</h1>
          <div style="display:flex; gap:12px; margin-top:8px; font-size:13px;">
            <span class="badge" style="background: ${theme === "space" ? "#1a237e" : "#4a148c"}">
              ${theme === "space" ? "🚀 Космос" : "🎮 Игры"}
            </span>
          </div>
        </div>

        <div class="card">
          <h2>📋 Описание</h2>
          <p style="white-space:pre-line; line-height:1.6;">${escapeHtml(fp.description || "")}</p>
        </div>

        <div class="card">
          <h2>📋 Этапы проекта (10 шагов)</h2>
          <p style="color: var(--text-secondary); font-size:13px; margin-bottom:8px;">
            Раскрой каждый шаг, чтобы увидеть описание и ссылки на уроки.
          </p>
          ${stepsHtml}
        </div>

        ${datasetStr}

        <div class="card">
          <h2>🚀 Стартовый код</h2>
          <p style="color: var(--text-secondary); font-size:13px;">
            Скопируй код в среду выполнения (например, в урок с Python-песочницей).
            Метки <code>TODO</code> показывают, что нужно реализовать.
            Каждый TODO соответствует одному из шагов выше.
          </p>
          <pre style="background:#0a0a1a; padding:14px; border-radius:6px; overflow:auto; max-height:480px;"><code>${escapeHtml(fp.template_code || "# (код появится скоро)")}</code></pre>
        </div>

        <div class="card">
          <h2>✅ Эталонное решение</h2>
          <p style="color: var(--text-secondary); font-size:13px;">
            Сверься с этим решением, если застрял. Постарайся сначала решить сам.
          </p>
          <details>
            <summary style="cursor:pointer; color: var(--accent);">Показать решение</summary>
            <pre style="background:#0a0a1a; padding:14px; border-radius:6px; overflow:auto; max-height:480px; margin-top:10px;"><code>${escapeHtml(fp.solution_code || "# (решение появится скоро)")}</code></pre>
          </details>
        </div>

        <div style="margin-top:24px; display:flex; gap:12px; flex-wrap:wrap;">
          <button class="btn" id="btn-back-themes">← Выбрать другую тему</button>
          <a href="#/projects" class="btn">→ К другим проектам</a>
        </div>
      `;
      const backBtn = $("#btn-back-themes");
      if (backBtn) backBtn.addEventListener("click", backToThemeChooser);
    } catch (e) {
      content.innerHTML = `<div class="card"><h2>Ошибка</h2><p>${escapeHtml(e.message)}</p></div>`;
    }
  }

  function backToThemeChooser() {
    const chooser = $("#final-theme-chooser");
    const content = $("#final-project-content");
    if (chooser) chooser.style.display = "";
    if (content) content.innerHTML = "";
    window.scrollTo(0, 0);
  }

  // ============================================================================
  // Достижения
  // ============================================================================
  let _achCheckPending = false;
  function checkAchievements() {
    if (_achCheckPending) return;
    _achCheckPending = true;
    setTimeout(() => { _achCheckPending = false; }, 1000);
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
    openModal();
  }

  // ============================================================================
  // Init
  // ============================================================================
  async function init() {
    window.SandboxLog = (msg, level) => console[level === "error" ? "error" : "log"]("[sandbox]", msg);
    window.addEventListener("hashchange", route);

    // Тema switcher
    initTheme();

    // Sidebar toggle (mobile)
    const toggle = document.getElementById("sidebar-toggle");
    const sidebar = document.getElementById("sidebar");
    const overlay = document.getElementById("sidebar-overlay");
    function closeSidebar() { sidebar?.classList.remove("open"); overlay?.classList.remove("open"); toggle?.setAttribute("aria-expanded", "false"); toggle && (toggle.textContent = "☰"); }
    function openSidebar() { sidebar?.classList.add("open"); overlay?.classList.add("open"); toggle?.setAttribute("aria-expanded", "true"); toggle && (toggle.textContent = "✕"); }
    toggle?.addEventListener("click", () => {
      const isOpen = sidebar?.classList.toggle("open");
      overlay?.classList.toggle("open", isOpen);
      toggle.setAttribute("aria-expanded", isOpen);
      toggle.textContent = isOpen ? "✕" : "☰";
    });
    overlay?.addEventListener("click", closeSidebar);
    document.addEventListener("keydown", e => { if (e.key === "Escape" && sidebar?.classList.contains("open")) closeSidebar(); });
    // Close sidebar on nav
    document.addEventListener("click", e => { if (e.target.closest?.(".nav-link, .lesson-link")) closeSidebar(); });

    // Modal accessibility: focus trap, Escape, aria-hidden
    const modal = document.getElementById("achievement-modal");
    const modalClose = document.getElementById("achievement-close");
    let _lastFocused = null;
    function openModal() {
      modal.classList.remove("hidden");
      modal.removeAttribute("aria-hidden");
      _lastFocused = document.activeElement;
      modalClose.focus();
      document.body.style.overflow = "hidden";
    }
    function closeModal() {
      modal.classList.add("hidden");
      modal.setAttribute("aria-hidden", "true");
      document.body.style.overflow = "";
      _lastFocused?.focus();
    }
    modalClose?.addEventListener("click", closeModal);
    modal?.addEventListener("click", e => { if (e.target === modal) closeModal(); });
    document.addEventListener("keydown", e => { if (e.key === "Escape" && !modal.classList.contains("hidden")) closeModal(); });
    // Focus trap
    modal?.addEventListener("keydown", e => {
      if (e.key === "Tab") {
        const focusable = modal.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
        const first = focusable[0];
        const last = focusable[focusable.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });

    // Запускаем загрузку sandbox-ов ПАРАЛЛЕЛЬНО с загрузкой данных
    updateSplash("Загружаю Python окружение...");
    const pyPromise = (window.PythonSandbox?.ensurePyodide() || Promise.resolve(null))
      .then(() => setRuntimeStatus("py", window.PythonSandbox?.engine === "mock" ? "failed" : "ready"))
      .catch(() => setRuntimeStatus("py", "failed"));

    const sqlPromise = (window.SqlSandbox?.ensureSqlJs() || Promise.resolve(null))
      .then(() => setRuntimeStatus("sql", "ready"))
      .catch(() => setRuntimeStatus("sql", "failed"));

    updateSplash("Загружаю данные курса...");
    try {
      await loadInitial();
    } catch (e) {
      $("#main").innerHTML = `<div class="card"><h2>Ошибка загрузки</h2><p>${escapeHtml(e.message)}</p></div>`;
      hideSplash();
      return;
    }

    updateSplash("Подготавливаю интерфейс...");
    await route();

    // Прячем сплеш сразу после отрисовки — sandbox-ы догружаются в фоне
    hideSplash();
  }

  document.addEventListener("DOMContentLoaded", init);
})();
