/* ===================================================================
   「1帧6秒」倡议主题网站 — 共享交互脚本
   功能：导航高亮 / 代码复制 / 体积估算器 / 方案选择器 / 自检清单
   =================================================================== */
(function () {
  "use strict";

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
      btn.textContent = "复制失败";
      setTimeout(function () { btn.textContent = "复制"; }, 1500);
      return;
    }
    ta.remove();
  }

  function flashCopied(btn) {
    btn.classList.add("copied");
    btn.textContent = "已复制 ✓";
    setTimeout(function () {
      btn.classList.remove("copied");
      btn.textContent = "复制";
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
    { id: "L1", name: "标准级",      color: "l1", mid: 32.5, interval: 6,  note: "彩色 CRF32" },
    { id: "L2", name: "黑白级",      color: "l2", mid: 26.0, interval: 6,  note: "黑白 CRF32" },
    { id: "L3", name: "高压缩级",    color: "l3", mid: 20.0, interval: 6,  note: "黑白 CRF34" },
    { id: "L4", name: "智能调优级",  color: "l4", mid: 17.5, interval: 6,  note: "+stillimage ★推荐" },
    { id: "L5", name: "音频极限级",  color: "l5", mid: 15.5, interval: 6,  note: "8k音频" },
    { id: "L6", name: "长间隔级",    color: "l6", mid: 11.0, interval: 10, note: "10秒/360p" },
    { id: "L7", name: "2-Pass级",    color: "l7", mid: null, interval: 10, note: "按目标锁定体积" },
    { id: "L8", name: "H.265极限级", color: "l8", mid: 7.0,  interval: 10, note: "需确认H.265支持" }
  ];

  function initCalculator() {
    var btn = document.getElementById("calc-btn");
    var input = document.getElementById("duration");
    var result = document.getElementById("calc-result");
    if (!btn || !input || !result) return;

    function render() {
      var min = parseFloat(input.value);
      if (!min || min < 1) {
        result.innerHTML = '<p class="danger-text">请输入有效的分钟数（≥1）。</p>';
        return;
      }
      var scale = min / BASE_MIN;
      var totalSec = min * 60;

      var html = '<div class="calc-summary">时长 ' + min + ' 分钟（' + Math.round(totalSec) + ' 秒）的预估：</div>';
      html += '<div class="tbl-wrap"><table><thead><tr><th>级别</th><th>名称</th><th>总帧数</th><th>预估体积</th><th>说明</th></tr></thead><tbody>';

      LEVELS.forEach(function (lv) {
        var frames = Math.floor(totalSec / lv.interval);
        var size;
        if (lv.mid === null) {
          size = '<span class="muted">按目标体积锁定</span>';
        } else {
          var mb = (lv.mid * scale).toFixed(1);
          size = '≈ ' + mb + ' MB';
        }
        html += '<tr><td><span class="lvl-badge ' + lv.color + '"><span class="dot"></span>' + lv.id +
          '</span></td><td>' + lv.name + '</td><td>' + frames + ' 帧</td><td>' + size +
          '</td><td class="muted">' + lv.note + '</td></tr>';
      });

      html += '</tbody></table></div>';
      html += '<p class="muted" style="margin-top:8px">体积为经验区间中值按分钟线性换算，实际受内容复杂度、编码器版本影响。L7 需用 2-Pass 模式锁定目标体积。</p>';
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
      var lvl, name, reason;

      // 销售演示 → 必彩色 → L1
      if (q1 === "sales" || q2 === "color") {
        lvl = "l1"; name = "L1 标准级";
        reason = "需保留彩色与品牌呈现，480p 彩色 CRF32 兼顾专业感与体积。如需投影大屏，可升格为 720p+CRF28。";
      }
      // 合规备案 → L2 查阅版
      else if (q1 === "archive" && q3 === "good") {
        // 企业内训/知识库：电脑端 → L4
        lvl = "l4"; name = "L4 智能调优级";
        reason = "企业内训长期存档，黑白+stillimage 在体积与清晰度间最佳平衡，存储成本可降 80～90%。";
      }
      else if (q1 === "archive") {
        lvl = "l4"; name = "L4 智能调优级";
        reason = "企业内训/知识库标准入库方案；对历史存量批量转码可降为 L5。";
      }
      // 邮件 → 电脑端 → L4
      else if (q1 === "email" && q3 === "good") {
        lvl = "l4"; name = "L4 智能调优级";
        reason = "邮箱附件限制 10～25MB，L4 的 99 分钟约 16～19MB 可稳妥放入；电脑大屏黑白依然清晰。";
      }
      else if (q1 === "email") {
        lvl = "l6"; name = "L6 长间隔级";
        reason = "需控制在 10MB 以内通过附件限制，L6（10秒/360p/8k）牺牲画质换取通过性。";
      }
      // 微信/IM → 手机 → L5
      else if (q1 === "im") {
        if (q3 === "poor") {
          lvl = "l6"; name = "L6 长间隔级";
          reason = "极低带宽下手机小屏观看，360p 足够，体积最小传输最快。";
        } else {
          lvl = "l5"; name = "L5 音频极限级";
          reason = "手机小屏对分辨率不敏感，8k 音频外放足够清晰，4G/5G 秒传。";
        }
      }
      // 慕课 → 低带宽受众 → L5
      else if (q1 === "mooc") {
        lvl = "l5"; name = "L5 音频极限级";
        reason = "面向低带宽受众，极低带宽优化版，兼容老旧设备；若涉配色讲解则退回 L1。";
      }
      // 离线 → 手机 → L6
      else if (q1 === "offline") {
        lvl = "l6"; name = "L6 长间隔级";
        reason = "移动端离线批量下载，每集 &lt;10MB，存储友好；iOS 用户若支持 H.265 可选 L8。";
      }
      // 兜底
      else {
        lvl = "l4"; name = "L4 智能调优级";
        reason = "综合推荐——体积与体验的最佳平衡点。";
      }

      result.innerHTML =
        '<div class="result-card">' +
        '<div class="rc-lvl"><span class="lvl-badge ' + lvl + '"><span class="dot"></span>' + name + '</span> 为你推荐</div>' +
        '<div class="rc-reason">' + reason + '</div>' +
        '<p style="margin-top:10px"><a href="levels.html#' + lvl + '">查看该级别的完整 ffmpeg 命令 →</a></p>' +
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
  });

})();
