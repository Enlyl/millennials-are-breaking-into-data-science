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
  let _splashStart = Date.now();
  const splashMsg = () => document.getElementById("splash-msg");
  function updateSplash(msg) {
    const el = splashMsg();
    if (el) el.textContent = msg;
  }
  function hideSplash() {
    const el = document.getElementById("splash");
    if (!el) return;
    // Минимальное время показа 1.5с для плавного впечатления
    const elapsed = Date.now() - _splashStart;
    const minShow = Math.max(0, 1500 - elapsed);
    setTimeout(() => {
      el.classList.add("splash-fading");
      // Ждём окончания transition, либо скрываем через 1с (fallback)
      const hide = () => { el.style.display = "none"; };
      el.addEventListener("transitionend", hide, { once: true });
      setTimeout(hide, 1000);
    }, minShow);
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
    // Загружаем блоки, прогресс, достижения и уроки параллельно
    const [blocks, summary, achievements, allLessons] = await Promise.all([
      api("/lessons/blocks").catch(e => { console.error("Failed to load blocks:", e); return []; }),
      api("/progress/summary").catch(e => {
        console.error("Failed to load summary:", e);
        return { lessons_total: 0, lessons_done: 0, exercises_total: 0, exercises_solved: 0 };
      }),
      api("/achievements/").catch(e => { console.error("Failed to load achievements:", e); return []; }),
      api("/lessons/").catch(e => { console.error("loadAllLessonsForSidebar failed:", e); return []; }),
    ]);
    state.blocks = blocks;
    state.summary = summary;
    state.achievements = achievements;
    state.allLessons = allLessons;
    updateProgressUI();
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
      //
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
      const nums = state.blocks.map(b => b.number);
      localStorage.setItem("ds_sidebar_collapsed", JSON.stringify(nums));
    }
    const collapsed = new Set(JSON.parse(localStorage.getItem("ds_sidebar_collapsed") || "[]"));
        if (wasCollapsed) { collapsed.add(blockNum); } else { collapsed.delete(blockNum); }
        localStorage.setItem("ds_sidebar_collapsed", JSON.stringify([...collapsed]));
      });
    });
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
    const blockCards = (state.blocks || []).map(b => {
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

      // Capstone project lessons (11.2, 11.3) — render interactive comic instead of sections
      if (number === "11.2" || number === "11.3") {
        renderCapstoneLesson(main, lesson, number);
        return;
      }

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
      further_reading: "🔗", prerequisites: "📋",
      debug_challenge: "🐛", recap_quiz: "🔄", portfolio_readme: "📄"
    };
    const titles = {
      theory: "Теория", analogy: "Аналогия", example: "Пример", visual: "Визуализация",
      common_mistakes: "Типовые ошибки", interview_questions: "Вопросы собеседований",
      knowledge_checklist: "Чеклист знаний",
      learning_objectives: "Цели урока", summary: "Ключевые выводы",
      glossary: "Глоссарий", further_reading: "Дополнительные материалы",
      prerequisites: "Что нужно знать",
      debug_challenge: "Debug Challenge", recap_quiz: "Опрос по прошлому блоку", portfolio_readme: "Шаблон портфолио"
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
      body = (sec.items || []).map(item => {
        if (typeof item === "string") {
          // Role-play format: **HR:** ... \n\n **Я:** ...
          const text = escapeHtml(item);
          const html = text
            .replace(/\*\*HR/g, '<strong class="role-hr">🧛 HR')
            .replace(/\*\*Я/g, '<strong class="role-me">😊 Я')
            .replace(/\*\*/g, '</strong>')
            .replace(/\n\n/g, '<br><br>');
          return `<div class="interview-roleplay">${html}</div>`;
        }
        return `
          <div class="interview-item">
            <div><strong>В:</strong> ${escapeHtml(item.q || "")}</div>
            <div class="a"><strong>О:</strong> ${escapeHtml(item.a || "")}</div>
          </div>
        `;
      }).join("");
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
    } else if (sec.type === "debug_challenge") {
      body = `
        <div class="debug-challenge-box">
          <div class="debug-problem">${escapeHtml(sec.problem || "")}</div>
          <div class="debug-hint" style="color: var(--warning); font-size: var(--text-sm); margin-bottom: var(--space-2);">💡 Подсказка: ${escapeHtml(sec.hint || "")}</div>
          <pre><code class="language-python">${escapeHtml(sec.buggy_code || "")}</code></pre>
          <details style="margin-top: var(--space-2);">
            <summary style="cursor: pointer; color: var(--accent);">Показать исправление</summary>
            <div class="debug-fix" style="margin-top: var(--space-2); padding: var(--space-2); background: var(--surface-alt); border-radius: 8px;">
              <pre><code>${escapeHtml(sec.fix || "")}</code></pre>
            </div>
          </details>
        </div>
      `;
    } else if (sec.type === "recap_quiz") {
      body = `
        <div class="recap-quiz-box">
          <p style="margin-bottom: var(--space-3); color: var(--text-secondary);">Проверь себя перед началом блока:</p>
          <ol style="padding-left: var(--space-4);">
            ${(sec.items || []).map(item => `<li style="margin-bottom: var(--space-2);">${escapeHtml(item)}</li>`).join("")}
          </ol>
        </div>
      `;
    } else if (sec.type === "portfolio_readme") {
      body = `
        <div class="portfolio-readme-box">
          <p style="margin-bottom: var(--space-3); color: var(--text-secondary);">Шаблон README для твоего портфолио-проекта:</p>
          <pre><code>${escapeHtml(sec.content || "")}</code></pre>
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
          <h2>📋 Этапы проекта (${(fp.steps_json || []).length} шагов)</h2>
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
  // Capstone Lesson — интерактивный комикс для уроков 11.2 и 11.3
  // ============================================================================
  const _capstoneProgress = {};

  const _capstoneCharacters = {
    client: { name: "Заказчик", emoji: "👔", color: "#E65100", avatar: "/static/img/avatars/client.png", role: "Клиент", description: "Представитель заказчика. Даёт задание и принимает финальный результат. Строгий, но справедливый." },
    me: { name: "Я", emoji: "😊", color: "#1565C0", avatar: "/static/img/avatars/me.png", role: "Новичок в DS", description: "Начинающий дата-сайентист. Когда получает задачу, поначалу паникует и просит совета у более опытных коллег." },
    alexey: { name: "Весёлый Лёха", emoji: "😄", color: "#2E7D32", avatar: "/static/img/avatars/alexey.png", role: "Middle Data Scientist", description: "Оптимист и душа команды. Всегда подбадривает коллег, верит, что любая задача решается, если подойти к ней с улыбкой." },
    malder: { name: "Мрачный Малдер", emoji: "🕵️", color: "#4E342E", avatar: "/static/img/avatars/malder.png", role: "Senior Data Scientist", description: "Скептик с многолетним опытом. Любит говорить «я же предупреждал» и рассказывать страшные истории о продакшне." },
    dmitry: { name: "Озабоченный Дима", emoji: "😰", color: "#C62828", avatar: "/static/img/avatars/dmitry.png", role: "Team Lead", description: "Вечно переживает за дедлайны, качество кода и настроение в команде. Носит с собой блокнот для записи страхов." },
    scully: { name: "Научная Скалли", emoji: "🔬", color: "#283593", avatar: "/static/img/avatars/scully.png", role: "Research Scientist", description: "Доктор наук, подходит к любой задаче как к научному исследованию. Требует статистических обоснований и A/B-тестов." },
    sergey: { name: "Серёжа-геймер", emoji: "🎮", color: "#00838F", avatar: "/static/img/avatars/sergey.png", role: "ML Engineer", description: "Мыслит категориями RPG: баги — это мобы, дедлайн — босс-файт, а нейросети — магия высшего уровня." },
    galina: { name: "Продуктивная Галя", emoji: "📋", color: "#F57F17", avatar: "/static/img/avatars/galina.png", role: "Project Manager", description: "Мастер планирования и декомпозиции задач. Её любимые слова: «давай запишем это в бэклог» и «а какой deadline?»" },
    igor: { name: "Мрачный Игорь", emoji: "🔧", color: "#37474F", avatar: "/static/img/avatars/igor.png", role: "DevOps Engineer", description: "Молчаливый администратор всего, что работает. Починит любой баг за пять минут, но никогда не расскажет как." },
    stepan: { name: "Дизайнер Стёпка", emoji: "🎨", color: "#6A1B9A", avatar: "/static/img/avatars/stepan.png", role: "UX/UI Designer", description: "Перфекционист с острым чувством прекрасного. Верстает так, что хочется плакать от счастья (или от количества правок)." },
    viktor: { name: "Странный Витя", emoji: "🐱", color: "#F9A825", avatar: "/static/img/avatars/viktor.png", role: "Data Analyst", description: "Говорит загадками и цитатами из «Матрицы». Находит инсайты там, где другие видят только шум." },
  };

  function _getAvatarHtml(speakerId) {
    const ch = _capstoneCharacters[speakerId];
    if (!ch) return `<div class="chat-av-unknown" title="?">?</div>`;
    const role = ch.role ? ` · ${ch.role}` : "";
    return `
      <div class="chat-av" data-speaker="${speakerId}" title="${ch.name}${role}">
        <img src="${ch.avatar}" alt="${ch.name}" class="chat-av-img" loading="lazy"
          onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
        <div class="chat-av-fallback" style="background:${ch.color};">${ch.emoji}</div>
      </div>
    `;
  }

  function _getSpeakerLabel(speakerId) {
    const ch = _capstoneCharacters[speakerId];
    if (!ch) return "";
    if (speakerId === "client") return '<span>👔 Заказчик</span>';
    if (speakerId === "me") return '<span>😊 Я</span>';
    return `<span style="color:${ch.color};">${ch.emoji} ${ch.name}</span>`;
  }

  function _showCharacterModal(ch) {
    const modal = document.getElementById("character-modal");
    if (!modal) return;
    modal.querySelector(".character-modal-avatar")?.setAttribute("src", ch.avatar || "");
    modal.querySelector(".character-modal-avatar")?.setAttribute("alt", ch.name || "");
    const nameEl = modal.querySelector(".character-modal-name");
    if (nameEl) nameEl.textContent = `${ch.emoji || ""} ${ch.name || ""}`;
    const roleEl = modal.querySelector(".character-modal-role");
    if (roleEl) roleEl.textContent = ch.role || "";
    const descEl = modal.querySelector(".character-modal-desc");
    if (descEl) descEl.textContent = ch.description || "";
    modal.style.display = "flex";
  }

  function _hideCharacterModal() {
    const modal = document.getElementById("character-modal");
    if (modal) modal.style.display = "none";
  }

  function _loadCapstoneProgress(theme) {
    try {
      const saved = localStorage.getItem("ds_capstone_progress");
      if (saved) {
        const parsed = JSON.parse(saved);
        if (parsed[theme]) {
          return {
            currentStep: parsed[theme].currentStep || 0,
            hintIndex: parsed[theme].hintIndex || {},
          };
        }
      }
    } catch (e) {}
    return { currentStep: 0, hintIndex: {} };
  }

  function _saveCapstoneProgress(theme, pp) {
    try {
      let saved = {};
      const raw = localStorage.getItem("ds_capstone_progress");
      if (raw) try { saved = JSON.parse(raw); } catch (e) {}
      saved[theme] = {
        currentStep: pp.currentStep,
        hintIndex: pp.hintIndex || {},
      };
      localStorage.setItem("ds_capstone_progress", JSON.stringify(saved));
    } catch (e) {}
  }

  function _resetCapstoneProgress(theme, fp, pp, meta, main) {
    if (!confirm("Сбросить весь прогресс по этому проекту?")) return;
    pp.currentStep = 0;
    pp.hintIndex = {};
    _saveCapstoneProgress(theme, pp);
    _renderCapstoneStep(fp, pp, theme, meta, main);
  }

  async function renderCapstoneLesson(main, lesson, number) {
    const theme = number === "11.2" ? "space" : "gaming";
    const themeMeta = {
      space: { icon: "🚀", title: "Анализ миссий NASA", color: "#1a237e", badge: "ВЫПУСК 1" },
      gaming: { icon: "🎮", title: "Анализ поведения игроков", color: "#4a148c", badge: "ВЫПУСК 2" },
    };
    const meta = themeMeta[theme];

    main.innerHTML = `
      <div class="view-header">
        <div class="breadcrumb">
          <a href="#/">Главная</a> / <a href="#/">Блок 11</a> / Урок ${lesson.number}
        </div>
        <h1>${escapeHtml(lesson.title)}</h1>
        <div style="margin-top:4px;"><button class="btn btn-secondary btn-sm" id="reset-capstone-progress" style="font-size:11px;">↺ Сбросить прогресс</button></div>
      </div>
      <div class="comic-view" data-theme="${theme}">
        <div class="comic-header" style="border-bottom: 2px solid ${meta.color};">
          <div>
            <span class="comic-badge" style="background: ${meta.color};">${meta.badge}</span>
            <span class="comic-project-title">${meta.icon} ${meta.title}</span>
          </div>
          <div class="comic-progress" id="comic-progress"></div>
        </div>
        <div class="comic-loading"><div class="spinner"></div><p>Загружаю проект...</p></div>
        <div class="comic-stage" id="comic-stage" style="display:none;">
          <div class="comic-panel" id="comic-panel"></div>
          <div class="comic-nav" id="comic-nav"></div>
        </div>
      </div>
    `;

    try {
      const fp = await api("/final-project/" + theme);
      const pp = _loadCapstoneProgress(theme);
      _capstoneProgress[theme] = pp;
      document.getElementById("reset-capstone-progress").onclick = () =>
        _resetCapstoneProgress(theme, fp, pp, meta, main);
      _renderCapstoneStep(fp, pp, theme, meta, main);
    } catch (e) {
      const loading = main.querySelector(".comic-loading");
      if (loading) loading.outerHTML = `<div class="card"><h2>Ошибка загрузки</h2><p>${escapeHtml(e.message)}</p></div>`;
    }
  }

  function _renderCapstoneStep(fp, pp, theme, meta, main) {
    const stage = $(`#comic-stage`);
    const loading = main.querySelector(".comic-loading");
    if (loading) loading.style.display = "none";
    stage.style.display = "block";

    const steps = fp.steps_json || [];
    const idx = pp.currentStep;
    const step = steps[idx];
    if (!step) return;
    const totalSteps = steps.length;
    const hintIdx = (pp.hintIndex || {})[idx] || 0;

    const progressHtml = steps.map((s, i) =>
      `<div class="comic-progress-dot ${i === idx ? 'active' : ''}" title="Шаг ${i+1}: ${s.title}"></div>`
    ).join("");

    let lastSpeaker = null;
    const bubblesHtml = (step.dialogue || []).map((d, entryIdx) => {
      const isNewSpeaker = d.speaker !== lastSpeaker;
      lastSpeaker = d.speaker;
      const side = d.speaker === "me" ? "me" : "other";

      const avatarBlock = isNewSpeaker ? _getAvatarHtml(d.speaker) : '<div class="chat-av-spacer"></div>';
      const nameBlock = isNewSpeaker
        ? `<div class="chat-name ${d.speaker === 'me' ? 'chat-name-me' : ''}">${_getSpeakerLabel(d.speaker)}</div>`
        : "";

      return `
        <div class="chat-msg chat-msg-${side}${isNewSpeaker ? '' : ' chat-msg-cont'}" data-speaker="${d.speaker}">
          <div class="chat-msg-inner">
            ${side !== "me" ? `<div class="chat-av-col">${avatarBlock}</div>` : ""}
            <div class="chat-body">
              ${nameBlock}
              <div class="chat-bubble">${escapeHtml(d.text)}</div>
              ${side !== "me" ? `<div class="chat-reactions" data-idx="${entryIdx}"><span class="chat-reaction" data-react="👍">👍</span><span class="chat-reaction" data-react="😂">😂</span><span class="chat-reaction" data-react="🔥">🔥</span><span class="chat-reaction" data-react="💩">💩</span><span class="chat-reaction" data-react="🤡">🤡</span></div>` : ""}
            </div>
            ${side === "me" ? `<div class="chat-av-col">${avatarBlock}</div>` : ""}
          </div>
        </div>
      `;
    }).join("");

    // --- Hints ---
    const hintsHtml = (step.hints && step.hints.length) ? `
      <div class="chat-hints">
        ${step.hints.slice(0, hintIdx).map(h => `<div class="chat-hint">💡 ${escapeHtml(h)}</div>`).join("")}
        ${hintIdx < step.hints.length ? `<button class="btn btn-sm btn-ghost chat-hint-btn">💡 Показать подсказку</button>` : ""}
      </div>
    ` : "";

    // --- Task (professional style) ---
    const taskHtml = step.task ? `
      <div class="work-task">
        <div class="work-task-hdr">📋 Задание</div>
        <div class="work-task-text">${escapeHtml(step.task)}</div>
      </div>
    ` : "";

    // --- Code snippet ---
    const codeHtml = step.code ? `
      <div class="work-code">
        <div class="work-code-hdr">📄 Стартовый код</div>
        <pre class="work-code-block"><code>${escapeHtml(step.code)}</code></pre>
        <button class="btn btn-xs btn-ghost work-code-copy" data-code="${escapeHtml(step.code).replace(/"/g,'&quot;')}">📋 Копировать</button>
      </div>
    ` : "";

    // --- Data snippet ---
    const dataHtml = step.data_snippet ? `
      <div class="work-data">
        <div class="work-data-hdr">📊 Фрагмент данных</div>
        <pre class="work-data-block"><code>${escapeHtml(step.data_snippet)}</code></pre>
      </div>
    ` : "";

    const lessonsHtml = (step.lessons || []).length ? `
      <div class="work-links">📚 Полезные уроки: ${step.lessons.map(l => `<a href="#/lesson/${l}" class="work-link">${l}</a>`).join(", ")}</div>
    ` : "";

    const panel = $(`#comic-panel`);
    panel.innerHTML = `
      <div class="chat-day-divider">Шаг ${idx + 1} / ${totalSteps} · ${escapeHtml(step.title)}</div>
      <div class="chat-panel-top">
        <div class="chat-feed">
          ${bubblesHtml}
          <div class="chat-typing-container" style="display:none;">
            <div class="chat-typing-avatar"></div>
            <div class="chat-typing-bubble">
              <div class="chat-typing-dots"><span></span><span></span><span></span></div>
              <span class="chat-typing-label">печатает</span>
            </div>
          </div>
        </div>
        ${hintsHtml}
      </div>
      <div class="chat-panel-divider"></div>
      <div class="chat-panel-bottom">
        ${taskHtml}
        ${codeHtml}
        ${dataHtml}
        ${lessonsHtml}
      </div>
    `;

    // --- Typing animation: progressive reveal of ALL messages top→bottom ---
    const typingBox = panel.querySelector(".chat-typing-container");
    const typingAv = panel.querySelector(".chat-typing-avatar");
    const allMsgs = Array.from(panel.querySelectorAll(".chat-msg"));
    if (allMsgs.length > 0 && typingBox) {
      const feed = panel.querySelector(".chat-feed");
      if (!window._typedSteps) window._typedSteps = {};
      const animKey = theme + "-" + idx;
      const alreadyTyped = window._typedSteps[animKey] || false;
      window._typedSteps[animKey] = true;

      // Hide ALL messages from flow
      allMsgs.forEach(m => { m.style.display = "none"; });

      if (!alreadyTyped) {
        // Animate each message with typing indicator, top→bottom
        let delay = 400; // initial pause
        allMsgs.forEach((msg, i) => {
          const speaker = msg.dataset.speaker || "";
          const ch = _capstoneCharacters[speaker] || { emoji: "💬", name: speaker };
          const isSelf = msg.classList.contains("chat-msg-me");

          if (isSelf) {
            // Own message: no typing indicator, just appear
            delay += 150;
            setTimeout(() => {
              msg.style.display = "block";
              msg.classList.add("chat-msg-appear");
              feed.scrollTop = feed.scrollHeight;
            }, delay);
          } else {
            // Colleague: show typing indicator, then reveal
            const typingDuration = 1600 + Math.random() * 1000;

            // Show typing indicator for this speaker
            setTimeout(() => {
              typingAv.innerHTML = ch.emoji;
              typingBox.style.display = "flex";
              typingBox.classList.remove("chat-typing-hide");
              typingBox.classList.add("chat-typing-show");
              feed.scrollTop = feed.scrollHeight;
            }, delay);

            delay += typingDuration;

            // Hide typing, show message
            setTimeout(() => {
              typingBox.classList.remove("chat-typing-show");
              typingBox.classList.add("chat-typing-hide");
              msg.style.display = "block";
              msg.classList.add("chat-msg-appear");
              feed.scrollTop = feed.scrollHeight;
            }, delay);
          }
        });
        // Hide typing box at end
        setTimeout(() => { typingBox.style.display = "none"; }, delay);
      } else {
        // Already seen: show all at once
        allMsgs.forEach(m => { m.style.display = "block"; });
      }
    }

    // --- Bind choice buttons ---
    // (no more choices — all dialogue is simple text)

    // --- Bind hint button ---
    const hintBtn = panel.querySelector(".chat-hint-btn");
    if (hintBtn) {
      hintBtn.onclick = function() {
        if (!pp.hintIndex) pp.hintIndex = {};
        pp.hintIndex[idx] = (pp.hintIndex[idx] || 0) + 1;
        _saveCapstoneProgress(theme, pp);
        _renderCapstoneStep(fp, pp, theme, meta, main);
      };
    }

    // --- Bind avatar click → character modal (delegation) ---
    panel.addEventListener("click", function _avClick(e) {
      const av = e.target.closest(".chat-av");
      if (!av) return;
      const sid = av.dataset.speaker;
      const ch = sid ? _capstoneCharacters[sid] : null;
      if (!ch) return;
      _showCharacterModal(ch);
    });

    // --- Bind reactions on colleague messages ---
    panel.addEventListener("click", function _reactClick(e) {
      const react = e.target.closest(".chat-reaction");
      if (!react) return;
      const container = react.closest(".chat-reactions");
      if (!container) return;
      const prev = container.querySelector(".chat-reaction.active");
      if (prev === react) {
        react.classList.remove("active");
      } else {
        if (prev) prev.classList.remove("active");
        react.classList.add("active");
      }
    });

    // --- Bind code copy ---
    const copyBtn = panel.querySelector(".work-code-copy");
    if (copyBtn) {
      copyBtn.onclick = function() {
        navigator.clipboard.writeText(this.dataset.code).catch(() => {});
        this.textContent = "✅ Скопировано";
        setTimeout(() => { this.textContent = "📋 Копировать"; }, 2000);
      };
    }

    // --- Nav ---
    const nav = $(`#comic-nav`);
    nav.innerHTML = `
      <button class="btn btn-secondary" id="comic-prev" ${idx === 0 ? 'disabled' : ''}>◀ Назад</button>
      <div class="comic-progress-strip">${progressHtml}</div>
      <button class="btn btn-primary" id="comic-next">${idx < totalSteps - 1 ? 'Вперёд ▶' : '🎉 Завершить'}</button>
    `;

    const progressEl = $(`#comic-progress`);
    if (progressEl) progressEl.innerHTML = progressHtml;

    const prevBtn = $(`#comic-prev`);
    const nextBtn = $(`#comic-next`);

    if (prevBtn) prevBtn.onclick = () => {
      if (pp.currentStep > 0) { pp.currentStep--; _saveCapstoneProgress(theme, pp); _renderCapstoneStep(fp, pp, theme, meta, main); }
    };
    if (nextBtn) nextBtn.onclick = () => {
      if (idx < totalSteps - 1) { pp.currentStep++; _saveCapstoneProgress(theme, pp); _renderCapstoneStep(fp, pp, theme, meta, main); }
      else { _showCapstoneComplete(theme, meta, main); }
    };

    const feed = panel.querySelector(".chat-feed");
    if (feed) feed.scrollTop = 0;
  }

  function _showCapstoneComplete(theme, meta, main) {
    const panel = $(`#comic-panel`);
    const nav = $(`#comic-nav`);
    const otherTheme = theme === "space" ? "gaming" : "space";
    const otherNum = theme === "space" ? "11.3" : "11.2";

    // Mark all steps completed
    _saveCapstoneProgress(theme, _capstoneProgress[theme]);

    panel.innerHTML = `
      <div class="project-complete">
        <div class="project-complete-icon">🎉</div>
        <h2>Проект сдан!</h2>
        <p>Поздравляю! Ты прошёл все 15 шагов проекта «${meta.title}».</p>
        <div class="project-complete-stats">
          <div class="project-complete-stat">
            <span class="stat-number">15</span>
            <span class="stat-label">Шагов пройдено</span>
          </div>
          <div class="project-complete-stat">
            <span class="stat-number">${meta.icon}</span>
            <span class="stat-label">Готово для портфолио</span>
          </div>
        </div>
        <p style="margin-top: var(--space-4);">
          Не забудь оформить README — используй шаблон из урока 9.8.
        </p>
        <div style="margin-top: var(--space-4); display: flex; gap: var(--space-3); justify-content: center; flex-wrap: wrap;">
          <a href="#/lesson/${otherNum}" class="btn btn-primary">
            ${meta.icon === "🚀" ? '🎮 Пройти проект «Игры»' : '🚀 Пройти проект «Космос»'}
          </a>
          <a href="#/" class="btn btn-secondary">🏠 На главную</a>
        </div>
      </div>
    `;
    nav.innerHTML = ``;
    const progressEl = $(`#comic-progress`);
    if (progressEl) progressEl.innerHTML = Array(15).fill(0).map(() => `<div class="comic-progress-dot done"></div>`).join("");
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

    // Character modal
    const charModal = document.getElementById("character-modal");
    if (charModal) {
      const closeBtn = charModal.querySelector(".character-modal-close");
      closeBtn?.addEventListener("click", _hideCharacterModal);
      charModal.addEventListener("click", function _charOutside(e) {
        if (e.target === charModal && charModal.style.display !== "none") _hideCharacterModal();
      });
      document.addEventListener("keydown", function _charEsc(e) {
        if (e.key === "Escape" && charModal.style.display !== "none") _hideCharacterModal();
      });
    }

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
