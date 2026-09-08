/* ===================================================================
   「1帧6秒」倡议主题网站 — 共享交互脚本 (i18n 双语：zh / en)
   功能：导航高亮 / 代码复制 / 体积估算器 / 方案选择器 / 自检清单
   =================================================================== */
(function () {
  "use strict";

  /* ---------- 0. 文案字典（按页面 lang 切换） ---------- */
  var I18N = {
    zh: {
      copy: "复制",
      copied: "已复制 ✓",
      copyFailed: "复制失败",
      calcInvalid: '<p class="danger-text">请输入有效的分钟数（≥1）。</p>',
      calcSummary: function (min, sec) {
        return '时长 ' + min + ' 分钟（' + sec + ' 秒）的预估：';
      },
      calcHead: '<tr><th>级别</th><th>名称</th><th>总帧数</th><th>预估体积</th><th>说明</th></tr>',
      frames: "帧",
      lockedByTarget: '<span class="muted">按目标体积锁定</span>',
      calcFootnote: '体积为经验区间中值按分钟线性换算，实际受内容复杂度、编码器版本影响。L7 需用 2-Pass 模式锁定目标体积。',
      levels: [
        { id: "L1", name: "标准级",      note: "彩色 CRF32" },
        { id: "L2", name: "黑白级",      note: "黑白 CRF32" },
        { id: "L3", name: "高压缩级",    note: "黑白 CRF34" },
        { id: "L4", name: "智能调优级",  note: "+stillimage ★推荐" },
        { id: "L5", name: "音频极限级",  note: "8k音频" },
        { id: "L6", name: "长间隔级",    note: "10秒/360p" },
        { id: "L7", name: "2-Pass级",    note: "按目标锁定体积" },
        { id: "L8", name: "H.265极限级", note: "需确认H.265支持" }
      ],
      lvlName: {
        l1: "L1 标准级", l2: "L2 黑白级", l3: "L3 高压缩级", l4: "L4 智能调优级",
        l5: "L5 音频极限级", l6: "L6 长间隔级", l7: "L7 2-Pass级", l8: "L8 H.265极限级"
      },
      selRecommend: ' 为你推荐',
      selLink: '查看该级别的完整 ffmpeg 命令 →',
      selReason: {
        color: "需保留彩色与品牌呈现，480p 彩色 CRF32 兼顾专业感与体积。如需投影大屏，可升格为 720p+CRF28。",
        archiveGood: "企业内训长期存档，黑白+stillimage 在体积与清晰度间最佳平衡，存储成本可降 80～90%。",
        archive: "企业内训/知识库标准入库方案；对历史存量批量转码可降为 L5。",
        emailGood: "邮箱附件限制 10～25MB，L4 的 99 分钟约 16～19MB 可稳妥放入；电脑大屏黑白依然清晰。",
        email: "需控制在 10MB 以内通过附件限制，L6（10秒/360p/8k）牺牲画质换取通过性。",
        imPoor: "极低带宽下手机小屏观看，360p 足够，体积最小传输最快。",
        im: "手机小屏对分辨率不敏感，8k 音频外放足够清晰，4G/5G 秒传。",
        mooc: "面向低带宽受众，极低带宽优化版，兼容老旧设备；若涉配色讲解则退回 L1。",
        offline: "移动端离线批量下载，每集 &lt;10MB，存储友好；iOS 用户若支持 H.265 可选 L8。",
        fallback: "综合推荐——体积与体验的最佳平衡点。"
      }
    },
    en: {
      copy: "Copy",
      copied: "Copied ✓",
      copyFailed: "Copy failed",
      calcInvalid: '<p class="danger-text">Please enter a valid duration in minutes (≥1).</p>',
      calcSummary: function (min, sec) {
        return 'Estimated for ' + min + ' minutes (' + sec + ' seconds):';
      },
      calcHead: '<tr><th>Level</th><th>Name</th><th>Total frames</th><th>Est. size</th><th>Notes</th></tr>',
      frames: "frames",
      lockedByTarget: '<span class="muted">Locked to target size</span>',
      calcFootnote: 'Sizes are midpoints of empirical ranges scaled linearly by minute; actual results vary with content complexity and encoder version. L7 needs 2-Pass mode to lock the target size.',
      levels: [
        { id: "L1", name: "Standard",      note: "Color CRF 32" },
        { id: "L2", name: "Grayscale",     note: "B&W CRF 32" },
        { id: "L3", name: "High compression", note: "B&W CRF 34" },
        { id: "L4", name: "Smart tuning",  note: "+stillimage ★recommended" },
        { id: "L5", name: "Audio extreme", note: "8k audio" },
        { id: "L6", name: "Long interval", note: "10 s / 360p" },
        { id: "L7", name: "2-Pass",        note: "Locked to target size" },
        { id: "L8", name: "H.265 extreme", note: "Confirm H.265 support" }
      ],
      lvlName: {
        l1: "L1 Standard", l2: "L2 Grayscale", l3: "L3 High compression", l4: "L4 Smart tuning",
        l5: "L5 Audio extreme", l6: "L6 Long interval", l7: "L7 2-Pass", l8: "L8 H.265 extreme"
      },
      selRecommend: ' — recommended for you',
      selLink: 'View the full ffmpeg command for this level →',
      selReason: {
        color: "Color and brand presentation must be kept; 480p color CRF 32 balances professionalism and size. If projecting on a big screen, upgrade to 720p + CRF 28.",
        archiveGood: "Long-term archive for corporate training; B&W + stillimage is the best balance of size and sharpness, cutting storage costs 80–90%.",
        archive: "The standard intake plan for corporate training / knowledge-bases; batch transcoding legacy archives can drop to L5.",
        emailGood: "Email attachments are limited to 10–25MB; L4's ~16–19MB for 99 minutes fits safely, and B&W stays sharp on desktop screens.",
        email: "Must stay under 10MB to pass attachment limits; L6 (10 s/360p/8k) trades quality for deliverability.",
        imPoor: "Very low bandwidth, small phone screen; 360p is enough — smallest and fastest to transfer.",
        im: "Phone screens are resolution-insensitive; 8k audio is clear enough on speakers and sends in seconds over 4G/5G.",
        mooc: "For low-bandwidth audiences; ultra-low-bandwidth optimized and compatible with old devices; fall back to L1 if palettes are being explained.",
        offline: "Batch offline downloads on mobile; each episode <10MB is storage-friendly; iOS users with H.265 support can pick L8.",
        fallback: "Overall recommendation — the best balance of size and experience."
      }
    }
  };

  function currentLang() {
    var htmlLang = (document.documentElement.lang || "zh-CN").toLowerCase();
    return htmlLang.indexOf("en") === 0 ? "en" : "zh";
  }
  var T = I18N[currentLang()];

  /* ---------- 1. 导航当前页高亮 ---------- */
  function initNavActive() {
    var path = location.pathname.split("/").pop() || "index.html";
    var links = document.querySelectorAll(".nav-links a, .footer-nav a");
    links.forEach(function (a) {
      var href = a.getAttribute("href");
      if (href === path) a.classList.add("active");
    });
  }

  /* ---------- 2. 代码复制按钮 ---------- */
  function copyText(text, btn) {
    // 优先用现代 API
    if (navigator.clipboard && navigator.clipboard.writeText && location.protocol !== "file:") {
      navigator.clipboard.writeText(text).then(function () {
        flashCopied(btn);
      }, function () {
        fallbackCopy(text, btn);
      });
    } else {
      fallbackCopy(text, btn);
    }
  }

  function fallbackCopy(text, btn) {
    // 回退：textarea + execCommand（兼容 file:// 与旧浏览器）
    var ta = document.createElement("textarea");
    ta.value = text;
    ta.style.position = "fixed";
    ta.style.left = "-9999px";
    ta.style.top = "0";
    document.body.appendChild(ta);
    ta.focus();
    ta.select();
    try {
      document.execCommand("copy");
      flashCopied(btn);
    } catch (e) {
      ta.remove();
      btn.textContent = T.copyFailed;
      setTimeout(function () { btn.textContent = T.copy; }, 1500);
      return;
    }
    ta.remove();
  }

  function flashCopied(btn) {
    btn.classList.add("copied");
    btn.textContent = T.copied;
    setTimeout(function () {
      btn.classList.remove("copied");
      btn.textContent = T.copy;
    }, 1600);
  }

  function initCopyButtons() {
    var btns = document.querySelectorAll(".copy-btn");
    btns.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var targetId = btn.getAttribute("data-copy");
        var el = document.getElementById(targetId);
        if (el) copyText(el.textContent.trim(), btn);
      });
    });
  }

  /* ---------- 3. 体积估算器 ---------- */
  // 99 分钟基准中值（取原文各区间的中点），按分钟线性缩放
  var BASE_MIN = 99;
  var LEVELS = [
    { id: "L1", color: "l1", mid: 32.5, interval: 6 },
    { id: "L2", color: "l2", mid: 26.0, interval: 6 },
    { id: "L3", color: "l3", mid: 20.0, interval: 6 },
    { id: "L4", color: "l4", mid: 17.5, interval: 6 },
    { id: "L5", color: "l5", mid: 15.5, interval: 6 },
    { id: "L6", color: "l6", mid: 11.0, interval: 10 },
    { id: "L7", color: "l7", mid: null, interval: 10 },
    { id: "L8", color: "l8", mid: 7.0,  interval: 10 }
  ];

  function initCalculator() {
    var btn = document.getElementById("calc-btn");
    var input = document.getElementById("duration");
    var result = document.getElementById("calc-result");
    if (!btn || !input || !result) return;

    function render() {
      var min = parseFloat(input.value);
      if (!min || min < 1) {
        result.innerHTML = T.calcInvalid;
        return;
      }
      var scale = min / BASE_MIN;
      var totalSec = min * 60;

      var html = '<div class="calc-summary">' + T.calcSummary(min, Math.round(totalSec)) + '</div>';
      html += '<div class="tbl-wrap"><table><thead>' + T.calcHead + '</thead><tbody>';

      LEVELS.forEach(function (lv, idx) {
        var meta = T.levels[idx];
        var frames = Math.floor(totalSec / lv.interval);
        var size;
        if (lv.mid === null) {
          size = T.lockedByTarget;
        } else {
          var mb = (lv.mid * scale).toFixed(1);
          size = '≈ ' + mb + ' MB';
        }
        html += '<tr><td><span class="lvl-badge ' + lv.color + '"><span class="dot"></span>' + lv.id +
          '</span></td><td>' + meta.name + '</td><td>' + frames + ' ' + T.frames + '</td><td>' + size +
          '</td><td class="muted">' + meta.note + '</td></tr>';
      });

      html += '</tbody></table></div>';
      html += '<p class="muted" style="margin-top:8px">' + T.calcFootnote + '</p>';
      result.innerHTML = html;
    }

    btn.addEventListener("click", render);
    input.addEventListener("keydown", function (e) { if (e.key === "Enter") render(); });
    // 初始展示默认值
    render();
  }

  /* ---------- 4. 方案选择器 ---------- */
  // 映射逻辑取自场景速查表
  function initSelector() {
    var panel = document.getElementById("selector-panel");
    if (!panel) return;
    var step1 = document.getElementById("selector-step1");
    var step2 = document.getElementById("selector-step2");
    var step3 = document.getElementById("selector-step3");
    var result = document.getElementById("selector-result");
    var state = { q1: null, q2: null, q3: null };

    function showStep2() {
      step2.style.display = "";
      step2.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }
    function showStep3() {
      step3.style.display = "";
      step3.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }

    function recommend() {
      var q1 = state.q1, q2 = state.q2, q3 = state.q3;
      var lvl, reason;

      // 销售演示 → 必彩色 → L1
      if (q1 === "sales" || q2 === "color") {
        lvl = "l1"; reason = T.selReason.color;
      }
      // 企业内训/知识库：电脑端 → L4
      else if (q1 === "archive" && q3 === "good") {
        lvl = "l4"; reason = T.selReason.archiveGood;
      }
      else if (q1 === "archive") {
        lvl = "l4"; reason = T.selReason.archive;
      }
      // 邮件 → 电脑端 → L4
      else if (q1 === "email" && q3 === "good") {
        lvl = "l4"; reason = T.selReason.emailGood;
      }
      else if (q1 === "email") {
        lvl = "l6"; reason = T.selReason.email;
      }
      // 微信/IM → 手机 → L5
      else if (q1 === "im") {
        if (q3 === "poor") {
          lvl = "l6"; reason = T.selReason.imPoor;
        } else {
          lvl = "l5"; reason = T.selReason.im;
        }
      }
      // 慕课 → 低带宽受众 → L5
      else if (q1 === "mooc") {
        lvl = "l5"; reason = T.selReason.mooc;
      }
      // 离线 → 手机 → L6
      else if (q1 === "offline") {
        lvl = "l6"; reason = T.selReason.offline;
      }
      // 兜底
      else {
        lvl = "l4"; reason = T.selReason.fallback;
      }

      result.innerHTML =
        '<div class="result-card">' +
        '<div class="rc-lvl"><span class="lvl-badge ' + lvl + '"><span class="dot"></span>' + T.lvlName[lvl] + '</span>' + T.selRecommend + '</div>' +
        '<div class="rc-reason">' + reason + '</div>' +
        '<p style="margin-top:10px"><a href="levels.html#' + lvl + '">' + T.selLink + '</a></p>' +
        '</div>';
    }

    // 绑定单选
    step1.addEventListener("change", function (e) {
      if (e.target.name === "q1") {
        state.q1 = e.target.value;
        state.q2 = null; state.q3 = null;
        // 清空后续选择
        step2.querySelectorAll("input").forEach(function (r) { r.checked = false; });
        step3.querySelectorAll("input").forEach(function (r) { r.checked = false; });
        result.innerHTML = "";
        showStep2();
      }
    });
    step2.addEventListener("change", function (e) {
      if (e.target.name === "q2") {
        state.q2 = e.target.value;
        state.q3 = null;
        step3.querySelectorAll("input").forEach(function (r) { r.checked = false; });
        result.innerHTML = "";
        showStep3();
      }
    });
    step3.addEventListener("change", function (e) {
      if (e.target.name === "q3") {
        state.q3 = e.target.value;
        recommend();
      }
    });
  }

  /* ---------- 5. PPT 自检清单（localStorage 持久化） ---------- */
  function initChecklist() {
    var list = document.getElementById("design-checklist");
    if (!list) return;
    var items = list.querySelectorAll("li");
    var KEY = "1f6s-checklist";

    // 读取已保存状态
    var saved = {};
    try { saved = JSON.parse(localStorage.getItem(KEY) || "{}"); } catch (e) {}

    items.forEach(function (li) {
      var k = li.getAttribute("data-key");
      if (saved[k]) li.classList.add("checked");
      li.addEventListener("click", function () {
        li.classList.toggle("checked");
        saved[k] = li.classList.contains("checked");
        try { localStorage.setItem(KEY, JSON.stringify(saved)); } catch (e) {}
      });
    });

    var resetBtn = document.getElementById("reset-checklist");
    if (resetBtn) {
      resetBtn.addEventListener("click", function () {
        items.forEach(function (li) { li.classList.remove("checked"); });
        try { localStorage.removeItem(KEY); } catch (e) {}
      });
    }
  }

  /* ---------- 6. Hero 动效：网格 + 每 6 秒推进的扫描帧线 ---------- */
  function initHeroCanvas() {
    var canvas = document.getElementById("hero-canvas");
    if (!canvas) return;
    if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    var ctx = canvas.getContext("2d");
    if (!ctx) return;

    var W = 0, H = 0;
    var PULSE = 6000; // 与主题呼应：每 6 秒推进一帧

    function resize() {
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = canvas.clientWidth;
      H = canvas.clientHeight;
      canvas.width = Math.round(W * dpr);
      canvas.height = Math.round(H * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
    resize();
    window.addEventListener("resize", resize);

    function frame(now) {
      ctx.clearRect(0, 0, W, H);
      var progress = (now % PULSE) / PULSE;
      var x = progress * W;

      // 扫描线主体
      var grad = ctx.createLinearGradient(x, 0, x, H);
      grad.addColorStop(0, "rgba(34, 211, 238, 0)");
      grad.addColorStop(0.25, "rgba(34, 211, 238, 0.55)");
      grad.addColorStop(0.75, "rgba(163, 230, 53, 0.45)");
      grad.addColorStop(1, "rgba(163, 230, 53, 0)");
      ctx.strokeStyle = grad;
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, H);
      ctx.stroke();

      // 扫描线左侧拖尾（已压缩的时间轴）
      var tail = ctx.createLinearGradient(x - 130, 0, x, 0);
      tail.addColorStop(0, "rgba(34, 211, 238, 0)");
      tail.addColorStop(1, "rgba(34, 211, 238, 0.08)");
      ctx.fillStyle = tail;
      ctx.fillRect(x - 130, 0, 130, H);

      // 扫描线与网格横线的交点微光
      ctx.fillStyle = "rgba(230, 247, 255, 0.5)";
      for (var gy = 21; gy < H; gy += 42) {
        ctx.fillRect(x - 1, gy - 1, 2, 2);
      }

      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }

  /* ---------- 7. 滚动浮现动画 ---------- */
  function initReveal() {
    var els = document.querySelectorAll(
      "main section, .entry-card, .glossary-item, .lvl-section, .redline-cat, .tool-panel"
    );
    if (!els.length) return;
    if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    if (!("IntersectionObserver" in window)) return;

    els.forEach(function (el) { el.classList.add("reveal"); });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.classList.add("revealed");
          io.unobserve(en.target);
        }
      });
    }, { threshold: 0.06, rootMargin: "0px 0px -24px 0px" });
    els.forEach(function (el) { io.observe(el); });
  }

  /* ---------- 启动 ---------- */
  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  ready(function () {
    initNavActive();
    initCopyButtons();
    initCalculator();
    initSelector();
    initChecklist();
    initHeroCanvas();
    initReveal();
  });

})();