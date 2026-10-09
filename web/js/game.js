/* Ballion game flow: title -> 7 rounds -> final.
 * Depends on BALLION_INDEX, BallionData, BallionMatcher, BallionScene, BallionAudio. */
(function () {
  "use strict";

  var DATA = window.BALLION_INDEX;
  var M = window.BallionMatcher;
  // A game never repeats a prompt family (siblings like "<season> knockout scorers"), and a mixed
  // game (Daily, or Free Play across all themes) takes at most MAX_PER_THEME prompts from one theme.
  var ROUNDS = 7, SECONDS = 30, MAX_PER_FAMILY = 1, MAX_PER_THEME = 2;
  var LAUNCH = Date.UTC(2026, 9, 3); // Daily #1
  var TIER_NAMES = ["COMMON", "UNCOMMON", "RARE", "SUPER RARE", "ULTRA RARE", "LEGENDARY"];
  var TIER_EMOJI = ["⬜", "🟩", "🟦", "🔵", "🟪", "🟨"];
  var css = getComputedStyle(document.documentElement);
  var TIER_COLORS = [0, 1, 2, 3, 4, 5].map(function (i) { return css.getPropertyValue("--t" + i).trim(); });
  // Same hues, lightened where the base colour is too dark to read as text on the navy panels.
  var TEXT_COLORS = TIER_COLORS.slice(); TEXT_COLORS[3] = css.getPropertyValue("--t3-text").trim() || "#7d93ff";

  // Index entries gain .ans once their data/p/<id>.js has loaded (see ensureLoaded).
  var byId = {};
  DATA.prompts.forEach(function (p) { byId[p.id] = p; });
  var THEME_NAME = {};
  DATA.themes.forEach(function (t) { THEME_NAME[t.key] = t.name; });
  BallionData.onNames = M.addGlobalNames;

  function ensureLoaded(ids, cb) {
    BallionData.load(ids, function (failed) {
      ids.forEach(function (id) {
        var d = BallionData.prompts[id];
        if (d && !byId[id].ans) { byId[id].ans = d.ans; M.addGlobal(byId[id]); }
      });
      cb(failed);
    });
  }

  var $ = function (id) { return document.getElementById(id); };
  var el = {
    hud: $("hud"), round: $("hud-round"), time: $("hud-time"), score: $("hud-score"), fill: $("timer-fill"),
    overlay: $("title-overlay"), title: $("screen-title"), roundScreen: $("screen-round"), final: $("screen-final"),
    kicker: $("prompt-kicker"), text: $("prompt-text"), fine: $("prompt-fine"),
    form: $("answer-form"), input: $("answer-input"), kickBtn: $("kick-btn"), feedback: $("feedback"), misses: $("misses"),
    result: $("result"), badge: $("result-badge"), pts: $("result-pts"), answer: $("result-answer"), rarest: $("result-rarest"),
    allSummary: $("result-all-summary"), all: $("result-all"), next: $("next-btn"),
    pins: $("track-pins"), trackBall: $("track-ball"),
  };

  // ---------- seeded RNG ----------
  function xmur3(str) {
    for (var i = 0, h = 1779033703 ^ str.length; i < str.length; i++) { h = Math.imul(h ^ str.charCodeAt(i), 3432918353); h = (h << 13) | (h >>> 19); }
    return function () { h = Math.imul(h ^ (h >>> 16), 2246822507); h = Math.imul(h ^ (h >>> 13), 3266489909); return (h ^= h >>> 16) >>> 0; };
  }
  function mulberry32(a) {
    return function () { a |= 0; a = (a + 0x6d2b79f5) | 0; var t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  }
  // theme: a theme key, or null for a mix of every theme.
  function pickPrompts(seedStr, theme) {
    var rnd = mulberry32(xmur3(seedStr)());
    var ids = DATA.prompts.filter(function (p) { return !theme || p.th === theme; }).map(function (p) { return p.id; });
    for (var i = ids.length - 1; i > 0; i--) { var j = Math.floor(rnd() * (i + 1)); var tmp = ids[i]; ids[i] = ids[j]; ids[j] = tmp; }
    var out = [], perFamily = {}, perTheme = {};
    ids.forEach(function (id) {
      var p = byId[id];
      if (out.length >= ROUNDS || (perFamily[p.g] || 0) >= MAX_PER_FAMILY) return;
      if (!theme && (perTheme[p.th] || 0) >= MAX_PER_THEME) return;
      out.push(id);
      perFamily[p.g] = (perFamily[p.g] || 0) + 1;
      perTheme[p.th] = (perTheme[p.th] || 0) + 1;
    });
    // Tiny pools can't satisfy the limits; top up rather than play a short game.
    ids.forEach(function (id) { if (out.length < ROUNDS && out.indexOf(id) < 0) out.push(id); });
    return out;
  }
  function today() {
    var d = new Date();
    var key = d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
    var num = Math.floor((Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()) - LAUNCH) / 864e5) + 1;
    return { key: key, num: Math.max(1, num) };
  }

  // ---------- storage (best effort) ----------
  function load(k) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : null; } catch (e) { return null; } }
  function save(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }

  // ---------- state ----------
  var S = null;       // current game
  var timer = null;

  function show(screen) {
    [el.title, el.roundScreen, el.final].forEach(function (s) { s.hidden = s !== screen; });
    el.overlay.hidden = screen !== el.title;
    el.hud.hidden = screen === el.title;
  }

  function goHome() {
    stopTimer();
    S = null;
    BallionScene.reset();
    clearPins();
    var d = today(), done = load("ballion-daily-" + d.key);
    $("daily-btn").textContent = done ? "DAILY #" + d.num + " · VIEW RESULT" : "DAILY CHALLENGE #" + d.num;
    $("daily-sub").textContent = done ? "Today's score: " + done.score + " — new prompts tomorrow" : "Same 7 prompts for everyone today";
    show(el.title);
  }

  var starting = false;
  // mode "daily" (mixed themes, seeded by date) or "free"; theme = key or null for all themes.
  // onStarted (optional) runs once round 1 is on screen.
  function startGame(mode, theme, onStarted) {
    if (starting) return;
    BallionAudio.unlock();
    var d = today();
    if (mode === "daily") {
      var done = load("ballion-daily-" + d.key);
      if (done) { S = done; showFinal(true); return; }
      theme = null;
    }
    var seed = mode === "daily" ? "ballion-daily-" + d.key : "free-" + Date.now() + "-" + Math.random();
    var ids = pickPrompts(seed, theme || null);
    var status = $("load-status");
    starting = true;
    status.hidden = false; status.classList.remove("load-error"); status.textContent = "Loading prompts…";
    ensureLoaded(ids, function (failed) {
      starting = false;
      if (failed) {
        status.textContent = "Couldn't load the prompts. Check your connection and try again.";
        status.classList.add("load-error");
        return;
      }
      status.hidden = true;
      S = { mode: mode, theme: theme || null, day: d.num, key: d.key, prompts: ids, round: 0, results: [], score: 0 };
      clearPins();
      show(el.roundScreen);
      startRound();
      if (onStarted) onStarted();
    });
  }

  function gameName(s) {
    if (s.mode === "daily") return "DAILY #" + s.day;
    return s.theme ? THEME_NAME[s.theme].toUpperCase() : "FREE PLAY";
  }

  // ---------- rounds ----------
  function startRound() {
    var p = byId[S.prompts[S.round]];
    S.phase = "input";
    S.misses = [];
    el.round.textContent = (S.round + 1) + "/" + ROUNDS;
    el.score.textContent = S.score;
    el.kicker.textContent = "ROUND " + (S.round + 1) + (S.theme ? "" : " · " + THEME_NAME[p.th].toUpperCase()) +
      " · " + p.ans.length + " ANSWERS";
    el.text.textContent = p.q;
    el.fine.textContent = p.f ? "(" + p.f + ")" : "";
    el.input.value = "";
    el.input.disabled = false; el.kickBtn.disabled = false;
    el.feedback.textContent = ""; el.feedback.className = "feedback";
    el.misses.innerHTML = "";
    el.result.hidden = true;
    el.trackBall.classList.remove("on");
    BallionScene.reset();
    el.input.focus();
    startTimer();
  }

  function startTimer() {
    stopTimer();
    S.deadline = performance.now() + SECONDS * 1000;
    var lastSec = SECONDS;
    function tick() {
      var left = Math.max(0, S.deadline - performance.now());
      var sec = Math.ceil(left / 1000);
      el.time.textContent = sec;
      el.fill.style.transform = "scaleX(" + (left / (SECONDS * 1000)) + ")";
      el.fill.classList.toggle("low", sec <= 10);
      if (sec !== lastSec && sec <= 5 && sec > 0) BallionAudio.tick();
      lastSec = sec;
      if (left <= 0) { stopTimer(); timeout(); return; }
      timer = BallionRAF(tick);
    }
    timer = BallionRAF(tick);
  }
  function stopTimer() { if (timer) BallionCancelRAF(timer); timer = null; }

  function submit(value) {
    if (!S || S.phase !== "input") return;
    var p = byId[S.prompts[S.round]];
    var raw = (value !== undefined ? value : el.input.value).trim();
    if (!raw) return;
    var r = M.match(p, raw);
    if (r.kind === "exact" || r.kind === "corrected") return accept(r.index, r.kind === "corrected" ? raw : null);
    BallionAudio.wrong();
    el.input.classList.remove("shake"); void el.input.offsetWidth; el.input.classList.add("shake");
    el.feedback.className = "feedback bad";
    if (r.kind === "ambiguous") {
      el.feedback.textContent = "Which one do you mean? ";
      r.options.slice(0, 4).forEach(function (name) {
        var b = document.createElement("button");
        b.type = "button"; b.className = "pick"; b.textContent = name;
        b.addEventListener("click", function () { submit(name); });
        el.feedback.appendChild(b);
      });
    } else {
      el.feedback.textContent = "✗ Not on the list — keep trying!";
      if (S.misses.indexOf(raw) < 0) {
        S.misses.push(raw);
        var s = document.createElement("s"); s.textContent = raw; el.misses.appendChild(s);
      }
    }
    el.input.select();
  }

  function accept(index, typed) {
    stopTimer();
    var p = byId[S.prompts[S.round]];
    var a = p.ans[index];
    var pts = DATA.tiers[a.t].pts;
    S.phase = "kicking";
    S.results.push({ pid: p.id, q: p.q, answer: a.n, typed: typed, tier: a.t, pts: pts });
    el.input.disabled = true; el.kickBtn.disabled = true;
    el.feedback.className = "feedback good";
    el.feedback.textContent = typed ? "✓ " + a.n + " (autocorrected from “" + typed + "”)" : "✓ " + a.n;
    el.trackBall.classList.add("on");
    BallionScene.kick(pts, a.t, function () { addPin(pts, a.t); showResult(); });
  }

  function timeout() {
    if (!S || S.phase !== "input") return;
    var p = byId[S.prompts[S.round]];
    S.phase = "kicking";
    S.results.push({ pid: p.id, q: p.q, answer: null, tier: -1, pts: 0 });
    el.input.disabled = true; el.kickBtn.disabled = true;
    el.feedback.className = "feedback bad";
    el.feedback.textContent = "⏱ Time's up!";
    BallionScene.whiff(showResult);
  }

  function showResult() {
    var res = S.results[S.round];
    var p = byId[res.pid];
    S.phase = "result";
    S.score += res.pts;
    countUp(el.score, S.score - res.pts, S.score);
    var t = res.tier;
    el.badge.textContent = t >= 0 ? TIER_NAMES[t] : "MISS";
    el.badge.className = "badge" + (t >= 0 ? " t" + t : "");
    el.badge.style.setProperty("--c", t >= 0 ? TIER_COLORS[t] : "#3a3f5c");
    el.pts.textContent = "+" + res.pts + " · " + res.pts + " m";
    el.pts.style.color = t >= 0 ? TEXT_COLORS[t] : "var(--ink-dim)";
    el.answer.innerHTML = "";
    el.answer.append(res.answer ? "You said " : "No answer this round.");
    if (res.answer) {
      var b = document.createElement("b"); b.textContent = res.answer; el.answer.append(b);
      if (res.typed) { var sm = document.createElement("small"); sm.textContent = " (typed “" + res.typed + "”)"; el.answer.append(sm); }
    }
    // rarest answers they could have given
    var sorted = p.ans.slice().sort(function (x, y) { return y.t - x.t; });
    var rare = sorted.filter(function (a) { return a.t >= 4 && a.n !== res.answer; }).slice(0, 4);
    el.rarest.innerHTML = "";
    if (rare.length) {
      el.rarest.append("Rarest picks: ");
      rare.forEach(function (a, i) {
        var s = document.createElement("b"); s.textContent = a.n; s.style.color = TEXT_COLORS[a.t];
        el.rarest.append(s); if (i < rare.length - 1) el.rarest.append(", ");
      });
    }
    el.allSummary.textContent = "All " + p.ans.length + " answers";
    el.all.innerHTML = "";
    sorted.forEach(function (a) {
      var c = document.createElement("span");
      c.className = "chip t" + a.t + (a.n === res.answer ? " mine" : "");
      c.style.setProperty("--c", TIER_COLORS[a.t]);
      c.textContent = a.n;
      c.title = TIER_NAMES[a.t];
      el.all.appendChild(c);
    });
    el.result.querySelector("details").open = false;
    el.next.textContent = S.round === ROUNDS - 1 ? "FINAL WHISTLE" : "NEXT ROUND";
    el.result.hidden = false;
    el.next.focus();
  }

  function next() {
    if (!S || S.phase !== "result") return;
    S.round++;
    if (S.round >= ROUNDS) return finish();
    startRound();
  }

  function finish() {
    S.phase = "final";
    if (S.mode === "daily") save("ballion-daily-" + S.key, { mode: "daily", day: S.day, key: S.key, results: S.results, score: S.score });
    showFinal(false);
  }

  function showFinal(fromSave) {
    show(el.final);
    BallionScene.reset();
    clearPins();
    S.results.forEach(function (r) { if (r.tier >= 0) addPin(r.pts, r.tier); });
    el.round.textContent = ROUNDS + "/" + ROUNDS;
    el.score.textContent = S.score;
    el.time.textContent = "–"; el.fill.style.transform = "scaleX(0)";
    $("final-label").textContent = gameName(S) + " · FULL TIME";
    if (fromSave) $("final-score").textContent = S.score; else countUp($("final-score"), 0, S.score);
    $("final-meters").textContent = "Total distance: " + S.score + " m · " + goalsText(S.results.filter(function (r) { return r.tier === 5; }).length);
    var ol = $("final-rounds"); ol.innerHTML = "";
    S.results.forEach(function (r, i) {
      var li = document.createElement("li");
      li.style.setProperty("--c", r.tier >= 0 ? TIER_COLORS[r.tier] : "#3a3f5c");
      li.style.setProperty("--ct", r.tier >= 0 ? TEXT_COLORS[r.tier] : "#7a809e");
      var n = document.createElement("span"); n.textContent = i + 1;
      var mid = document.createElement("span");
      var q = document.createElement("span"); q.className = "q"; q.textContent = r.q;
      mid.appendChild(q); mid.append(r.answer || "— no answer —");
      var pts = document.createElement("span"); pts.className = "pts"; pts.textContent = (r.tier >= 0 ? TIER_NAMES[r.tier] : "MISS") + " +" + r.pts;
      li.append(n, mid, pts); ol.appendChild(li);
    });
    $("share-note").textContent = "";
    $("again-btn").textContent = S.mode === "daily" ? "FREE PLAY" : "PLAY AGAIN";
  }

  function goalsText(n) { return n === 1 ? "1 goal" : n + " goals"; }

  function shareText() {
    var head = S.mode === "daily" ? "Ballion #" + S.day : "Ballion (" + (S.theme ? THEME_NAME[S.theme] : "free play") + ")";
    var row = S.results.map(function (r) { return r.tier >= 0 ? TIER_EMOJI[r.tier] : "⬛"; }).join("");
    return head + " — " + S.score + "/700 ⚽\n" + row + "\nballion.io";
  }
  function share() {
    var txt = shareText();
    var note = $("share-note");
    function fallback() {
      var ta = document.createElement("textarea"); ta.value = txt; document.body.appendChild(ta); ta.select();
      try { document.execCommand("copy"); note.textContent = "Copied to clipboard!"; } catch (e) { note.textContent = txt; }
      ta.remove();
    }
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(txt).then(function () { note.textContent = "Copied to clipboard!"; }, fallback);
    else fallback();
  }

  // ---------- distance track ----------
  function addPin(m, tier) {
    var pin = document.createElement("span");
    pin.className = "track-pin";
    pin.style.left = Math.min(100, m) + "%";
    pin.style.setProperty("--c", TIER_COLORS[tier]);
    el.pins.appendChild(pin);
  }
  function clearPins() { el.pins.innerHTML = ""; el.trackBall.classList.remove("on"); }
  BallionScene.onProgress(function (m) { el.trackBall.style.left = Math.min(100, m) + "%"; });

  function countUp(node, from, to) {
    var t0 = performance.now(), dur = 600;
    (function step(now) {
      var u = Math.min(1, (now - t0) / dur);
      node.textContent = Math.round(from + (to - from) * u);
      if (u < 1) BallionRAF(step);
    })(t0);
  }

  // ---------- wiring ----------
  BallionScene.init($("scene"), TIER_COLORS);
  el.form.addEventListener("submit", function (e) { e.preventDefault(); submit(); });
  el.next.addEventListener("click", next);
  $("daily-btn").addEventListener("click", function () { startGame("daily"); });
  $("free-btn").addEventListener("click", function () { startGame("free", null); });
  // Free Play theme menu: one button per theme, after the mixed "ALL THEMES" button (#free-btn).
  var grid = $("theme-grid");
  DATA.themes.forEach(function (t) {
    if (!t.n) return;
    var b = document.createElement("button");
    b.className = "btn theme-btn"; b.type = "button"; b.dataset.theme = t.key;
    b.innerHTML = "<span></span><small></small>";
    b.firstChild.textContent = t.name.toUpperCase();
    b.lastChild.textContent = t.n + " prompts";
    b.addEventListener("click", function () { startGame("free", t.key); });
    grid.appendChild(b);
  });
  $("free-btn").lastChild.textContent = DATA.prompts.length + " prompts";
  // Daily -> free play across all themes; free play -> another game in the same theme.
  $("again-btn").addEventListener("click", function () { startGame("free", S && S.mode === "free" ? S.theme : null); });
  $("share-btn").addEventListener("click", share);
  $("home-btn").addEventListener("click", goHome);
  $("help-btn").addEventListener("click", function () { $("help").showModal(); });
  var mute = $("mute-btn");
  mute.setAttribute("aria-pressed", BallionAudio.isMuted() ? "true" : "false");
  mute.addEventListener("click", function () { mute.setAttribute("aria-pressed", BallionAudio.toggle() ? "true" : "false"); });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && S && S.phase === "result" && document.activeElement !== el.next) { e.preventDefault(); next(); }
  });

  var legend = $("legend");
  DATA.tiers.forEach(function (t, i) {
    var li = document.createElement("li");
    li.style.setProperty("--c", TIER_COLORS[i]);
    li.innerHTML = "<span style='color:" + TEXT_COLORS[i] + "'>" + TIER_NAMES[i] + "</span> " + t.pts + " m";
    legend.appendChild(li);
  });
  $("foot-count").textContent = DATA.prompts.length + " prompts · " + DATA.prompts.reduce(function (s, p) { return s + p.n; }, 0) + " answers";

  // Debug hooks for screenshots: ?shot=kick&m=60&tier=3&t=1.2  |  ?shot=round  |  ?shot=final
  var qs = new URLSearchParams(location.search);
  var shot = qs.get("shot");
  if (shot === "kick") { show(el.title); el.overlay.hidden = true; BallionScene.debugFreeze(+qs.get("m"), +qs.get("tier"), +qs.get("t")); }
  else if (shot === "round") { startGame("daily"); }
  else if (shot === "result") {
    startGame("daily", null, function () {
      var p0 = byId[S.prompts[0]];
      var idx = p0.ans.findIndex(function (a) { return a.t === +(qs.get("tier") || 3); });
      accept(idx, qs.get("typed")); BallionScene.reset(); showResult(); el.result.querySelector("details").open = qs.get("open") === "1";
    });
  }
  else if (shot === "final") {
    startGame("free", qs.get("theme"), function () {
      for (var r = 0; r < ROUNDS; r++) { var pr = byId[S.prompts[r]]; var tt = [5, 2, 0, 4, 1, 3, -1][r]; if (tt < 0) { S.results.push({ pid: pr.id, q: pr.q, answer: null, tier: -1, pts: 0 }); } else { var a2 = pr.ans.find(function (a) { return a.t === tt; }); S.results.push({ pid: pr.id, q: pr.q, answer: a2.n, tier: tt, pts: DATA.tiers[tt].pts }); S.score += DATA.tiers[tt].pts; } }
      stopTimer(); showFinal(true);
    });
  }
  else goHome();
  // The "different real entity" list isn't needed to start playing, so fetch it after everything else.
  setTimeout(BallionData.loadNames, 0);
  if (qs.get("help") === "1") $("help").showModal();
  window.BALLION_READY = true;
  $("load-status").hidden = true;
})();

/* Self-test (?selftest=1[&theme=pl]): plays a full free game through the real UI paths and writes a
 * summary into <body data-selftest>, so a headless browser can verify the flow end to end. */
(function () {
  var qs = new URLSearchParams(location.search);
  if (qs.get("selftest") !== "1") return;
  var log = [];
  var $ = function (id) { return document.getElementById(id); };
  function wait(cond, cb, n) { n = n || 0; if (cond()) return cb(); if (n > 4000) { log.push("TIMEOUT"); return done(); } setTimeout(function () { wait(cond, cb, n + 1); }, 20); }
  function done() { document.body.setAttribute("data-selftest", log.join(" | ")); }
  var themeBtn = qs.get("theme") && document.querySelector('.theme-btn[data-theme="' + qs.get("theme") + '"]');
  (themeBtn || $("free-btn")).click();
  var round = 0;
  wait(function () { return !$("screen-round").hidden; }, function play() {
    var text = $("prompt-text").textContent;
    var p = window.BALLION_INDEX.prompts.find(function (x) { return x.q === text && x.ans; });
    if (round === 0) log.push("theme=" + (themeBtn ? qs.get("theme") : "all") + " first=" + p.id);
    var input = $("answer-input");
    input.value = "zzqx not a player"; $("kick-btn").click();
    var missOk = /Not on the list/.test($("feedback").textContent);
    if (round === 3) { log.push("r" + round + ":timeout-test"); }
    else {
      var a = p.ans[(round * 7) % p.ans.length];
      var typo = a.n.length > 7 ? a.n.slice(0, 3) + a.n.slice(4) : a.n; // drop one char
      input.value = typo; $("kick-btn").click();
      log.push("r" + round + ":" + (missOk ? "miss-ok," : "miss-FAIL,") + a.n + "<-" + typo + "=" + $("feedback").textContent.slice(0, 40));
    }
    var deadline = round === 3 ? 40000 : 0;
    if (round === 3) { /* let the 30 s timer run out */ }
    wait(function () { return !$("result").hidden; }, function () {
      log.push("badge=" + $("result-badge").textContent);
      round++;
      $("next-btn").click();
      if (round < 7) wait(function () { return $("result").hidden; }, play);
      else wait(function () { return !$("screen-final").hidden; }, function () {
        setTimeout(function () {
          log.push("FINAL score=" + $("final-score").textContent + " rounds=" + $("final-rounds").children.length + " share=" + JSON.stringify($("final-rounds").innerText.length > 0));
          done();
        }, 1000);
      });
    });
  });
})();

/* Layout probe (?layout=1): reports elements wider than the viewport into <body data-layout>. */
(function () {
  if (new URLSearchParams(location.search).get("layout") !== "1") return;
  setTimeout(function () {
    var vw = document.documentElement.clientWidth, out = ["vw=" + vw, "scrollW=" + document.documentElement.scrollWidth];
    document.querySelectorAll("body *").forEach(function (n) {
      var r = n.getBoundingClientRect();
      if (r.right > vw + 1 && r.width > 0) out.push((n.id || n.className || n.tagName) + ":" + Math.round(r.width) + "w/" + Math.round(r.right) + "r");
    });
    document.body.setAttribute("data-layout", out.slice(0, 25).join(" | "));
  }, 500);
})();
