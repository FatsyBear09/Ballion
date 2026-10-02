/* Ballion stadium scene: 8-bit pixel art drawn procedurally on a 400x225 canvas.
 *
 * World units: 1 m = PX_PER_M pixels. The kick spot is at KICK_X, the far goal line 100 m away.
 * API (window.BallionScene):
 *   init(canvas, tierColors)  set up and start the render loop
 *   reset()                   kicker idle at the spot, camera home
 *   kick(meters, tier, done)  run-up + kick; ball travels `meters`; tier 5 (legendary) = goal
 *   whiff(done)               timeout: kicker misses the ball and falls over
 *   onProgress(fn)            fn(meters) while the ball travels (for the distance track)
 */
(function () {
  "use strict";

  // Frame scheduler. Headless self-tests have no rAF under virtual time, so they use timers.
  var raf = /[?&]selftest=1/.test(location.search)
    ? function (fn) { return setTimeout(function () { fn(performance.now()); }, 16); }
    : function (fn) { return requestAnimationFrame(fn); };
  window.BallionRAF = raf;
  window.BallionCancelRAF = /[?&]selftest=1/.test(location.search) ? clearTimeout : cancelAnimationFrame;

  var W = 400, H = 225;
  var GROUND = 196;            // y of the ball/kicker ground line
  var PX_PER_M = 10;
  var KICK_X = 60;
  var GOAL_X = KICK_X + 100 * PX_PER_M;
  var WORLD_W = GOAL_X + 80;
  var STAND_PARALLAX = 0.6, TOWER_PARALLAX = 0.3;

  var C = {
    outline: "#120f1f", skin: "#e0ac69", skinD: "#b07a45", hair: "#2b1a10",
    shirt: "#e63946", shirtD: "#a4161a", shorts: "#f1faee", shortsD: "#c4ccc4", boot: "#15121c",
    ball: "#f8f8f2", ballD: "#1b1b24",
    sky0: "#070b1e", sky1: "#18214a", stand: "#161a33", standLine: "#232a4d", roof: "#0d1024",
    grassA: "#2f8f3a", grassB: "#287e32", grassFar: "#246f2d", line: "#e8f5e9",
  };
  var tierColors = ["#9aa4b2", "#3ecf5a", "#3a8dff", "#2f4fd8", "#a646ff", "#ffcf26"];

  // ---------- tiny 3x5 pixel font (for in-world labels) ----------
  var FONT = {
    "0": "111101101101111", "1": "010110010010111", "2": "111001111100111", "3": "111001111001111",
    "4": "101101111001001", "5": "111100111001111", "6": "111100111101111", "7": "111001001001001",
    "8": "111101111101111", "9": "111101111001111", "A": "010101111101101", "B": "110101110101110",
    "C": "111100100100111", "D": "110101101101110", "E": "111100111100111", "G": "111100101101111",
    "I": "111010010010111", "L": "100100100100111", "M": "101111111101101", "N": "110101101101101",
    "O": "111101101101111", "R": "110101110101101", "S": "111100111001111", "T": "111010010010010",
    "!": "010010010000010", " ": "000000000000000",
  };
  function textWidth(s, scale) { return (s.length * 4 - 1) * (scale || 1); }
  function drawText(ctx, s, x, y, color, scale, shadow) {
    scale = scale || 1;
    if (shadow) { var o = Math.max(1, Math.round(scale / 3)); drawText(ctx, s, x + o, y + o, shadow, scale); }
    ctx.fillStyle = color;
    for (var i = 0; i < s.length; i++) {
      var g = FONT[s[i]] || FONT[" "];
      for (var p = 0; p < 15; p++) if (g[p] === "1") ctx.fillRect(x + (i * 4 + (p % 3)) * scale, y + Math.floor(p / 3) * scale, scale, scale);
    }
  }

  // ---------- deterministic noise ----------
  function hash(n) { n = (n ^ 61) ^ (n >>> 16); n = n + (n << 3); n = n ^ (n >>> 4); n = Math.imul(n, 0x27d4eb2d); return ((n ^ (n >>> 15)) >>> 0) / 4294967296; }

  // ---------- pixel primitives ----------
  function thickLine(ctx, x0, y0, x1, y1, w, color) {
    ctx.fillStyle = color;
    var dx = x1 - x0, dy = y1 - y0, len = Math.max(Math.abs(dx), Math.abs(dy), 1);
    var off = Math.floor(w / 2);
    for (var s = 0; s <= len; s += 0.5) {
      var px = Math.round(x0 + dx * s / len), py = Math.round(y0 + dy * s / len);
      ctx.fillRect(px - off, py - off, w, w);
    }
  }
  function disc(ctx, cx, cy, r, color) {
    ctx.fillStyle = color;
    for (var y = -r; y <= r; y++) for (var x = -r; x <= r; x++) if (x * x + y * y <= r * r + r * 0.8) ctx.fillRect(cx + x, cy + y, 1, 1);
  }

  // ---------- kicker ----------
  // Pose angles are degrees from straight down; positive rotates toward the facing direction (+x).
  var POSES = {
    idle:   { lean: 2, bt: -6, bs: -4, ft: 6, fs: 4, ba1: -10, ba2: -4, fa1: 10, fa2: 18, y: 0 },
    idle2:  { lean: 3, bt: -6, bs: -4, ft: 6, fs: 4, ba1: -12, ba2: -6, fa1: 12, fa2: 22, y: 1 },
    runA:   { lean: 14, bt: -35, bs: -80, ft: 35, fs: 5, ba1: 45, ba2: 90, fa1: -40, fa2: -10, y: -1 },
    runB:   { lean: 14, bt: 30, bs: -10, ft: -30, fs: -75, ba1: -40, ba2: -10, fa1: 45, fa2: 90, y: -2 },
    windup: { lean: -6, bt: 12, bs: 2, ft: -40, fs: -95, ba1: 70, ba2: 85, fa1: -55, fa2: -30, y: 0 },
    strike: { lean: 4, bt: 14, bs: 4, ft: 25, fs: 15, ba1: 40, ba2: 60, fa1: -30, fa2: -10, y: 0 },
    follow: { lean: -12, bt: 10, bs: 2, ft: 85, fs: 75, ba1: 100, ba2: 120, fa1: -70, fa2: -50, y: 0 },
    cheer:  { lean: 0, bt: -8, bs: -4, ft: 8, fs: 4, ba1: 165, ba2: 175, fa1: 160, fa2: 175, y: 0 },
    cheer2: { lean: 0, bt: -16, bs: -40, ft: 16, fs: -30, ba1: 175, ba2: 180, fa1: 170, fa2: 180, y: -6 },
    clap:   { lean: 4, bt: -6, bs: -4, ft: 6, fs: 4, ba1: 50, ba2: 95, fa1: 40, fa2: 100, y: 0 },
    shrug:  { lean: 0, bt: -6, bs: -4, ft: 6, fs: 4, ba1: 60, ba2: 150, fa1: 50, fa2: 140, y: 0 },
    fallen: { lean: -88, bt: 60, bs: 75, ft: 100, fs: 110, ba1: 120, ba2: 170, fa1: 60, fa2: 90, y: 13 },
  };
  function lerpPose(a, b, t) {
    var o = {};
    for (var k in a) o[k] = a[k] + (b[k] - a[k]) * t;
    return o;
  }
  function pt(x, y, deg, len) { var r = deg * Math.PI / 180; return [x + Math.sin(r) * len, y + Math.cos(r) * len]; }

  function drawKicker(ctx, x, pose) {
    var hipY = GROUND - 16 + pose.y;
    var hip = [x, hipY];
    var lean = pose.lean * Math.PI / 180;
    var neck = [x + Math.sin(lean) * 11, hipY - Math.cos(lean) * 11];
    var shoulder = [x + Math.sin(lean) * 9, hipY - Math.cos(lean) * 9];
    var head = [Math.round(neck[0] + Math.sin(lean) * 5), Math.round(neck[1] - Math.cos(lean) * 5)];
    function leg(t, s) { var k = pt(hip[0], hip[1], t, 8); return [k, pt(k[0], k[1], s, 8)]; }
    function arm(a1, a2) { var e = pt(shoulder[0], shoulder[1], a1, 6); return [e, pt(e[0], e[1], a2, 5)]; }
    var back = leg(pose.bt, pose.bs), front = leg(pose.ft, pose.fs);
    var bArm = arm(pose.ba1, pose.ba2), fArm = arm(pose.fa1, pose.fa2);

    function limbLeg(L, shade, pass) {
      var k = L[0], f = L[1];
      if (pass === 0) {
        thickLine(ctx, hip[0], hip[1], k[0], k[1], 5, C.outline);
        thickLine(ctx, k[0], k[1], f[0], f[1], 5, C.outline);
        thickLine(ctx, f[0], f[1], f[0] + 3, f[1], 4, C.outline);
        return;
      }
      var mid = [(hip[0] + k[0]) / 2, (hip[1] + k[1]) / 2];
      thickLine(ctx, mid[0], mid[1], k[0], k[1], 3, shade ? C.skinD : C.skin);
      thickLine(ctx, hip[0], hip[1], mid[0], mid[1], 3, shade ? C.shortsD : C.shorts);
      var kneeMid = [(k[0] * 0.7 + f[0] * 0.3), (k[1] * 0.7 + f[1] * 0.3)];
      thickLine(ctx, k[0], k[1], kneeMid[0], kneeMid[1], 3, shade ? C.skinD : C.skin);
      thickLine(ctx, kneeMid[0], kneeMid[1], f[0], f[1], 3, shade ? C.shirtD : C.shirt);
      thickLine(ctx, f[0], f[1], f[0] + 3, f[1], 2, C.boot);
    }
    function limbArm(A, shade, pass) {
      var e = A[0], h = A[1];
      if (pass === 0) {
        thickLine(ctx, shoulder[0], shoulder[1], e[0], e[1], 4, C.outline);
        thickLine(ctx, e[0], e[1], h[0], h[1], 4, C.outline);
        return;
      }
      var sleeve = [(shoulder[0] * 0.4 + e[0] * 0.6), (shoulder[1] * 0.4 + e[1] * 0.6)];
      thickLine(ctx, shoulder[0], shoulder[1], sleeve[0], sleeve[1], 2, shade ? C.shirtD : C.shirt);
      thickLine(ctx, sleeve[0], sleeve[1], e[0], e[1], 2, shade ? C.skinD : C.skin);
      thickLine(ctx, e[0], e[1], h[0], h[1], 2, shade ? C.skinD : C.skin);
    }
    // pass 0: outline silhouette; pass 1: fill
    for (var pass = 0; pass < 2; pass++) {
      limbArm(bArm, true, pass);
      limbLeg(back, true, pass);
      if (pass === 0) thickLine(ctx, hip[0], hip[1], neck[0], neck[1], 9, C.outline);
      else {
        thickLine(ctx, hip[0], hip[1], neck[0], neck[1], 7, C.shirt);
        thickLine(ctx, hip[0] - Math.cos(lean) * 2, hip[1] - Math.sin(lean) * 2, neck[0] - Math.cos(lean) * 2, neck[1] - Math.sin(lean) * 2, 2, C.shirtD);
        thickLine(ctx, hip[0], hip[1], hip[0] + Math.sin(lean), hip[1] - Math.cos(lean), 7, C.shorts);
      }
      limbLeg(front, false, pass);
      limbArm(fArm, false, pass);
      if (pass === 0) disc(ctx, head[0], head[1], 5, C.outline);
      else {
        disc(ctx, head[0], head[1], 4, C.skin);
        ctx.fillStyle = C.hair;
        for (var yy = -4; yy <= 4; yy++) for (var xx = -4; xx <= 4; xx++) {
          if (xx * xx + yy * yy > 19) continue;
          if (yy <= -2 || (xx <= -2 && yy <= 1)) ctx.fillRect(head[0] + xx, head[1] + yy, 1, 1);
        }
        ctx.fillStyle = C.outline;
        ctx.fillRect(head[0] + 2, head[1] - 1, 1, 1);           // eye
        ctx.fillStyle = C.skinD;
        ctx.fillRect(head[0] + 4, head[1], 1, 1);               // nose
      }
    }
  }

  // ---------- ball ----------
  function drawBall(ctx, x, y, spin) {
    x = Math.round(x); y = Math.round(y);
    disc(ctx, x, y, 4, C.outline);
    disc(ctx, x, y, 3, C.ball);
    ctx.fillStyle = C.ballD;
    var f = Math.floor(spin) % 4;
    var patches = [[[0, 0], [-2, -2], [2, 1]], [[1, -1], [-2, 1], [1, 2]], [[0, 1], [2, -2], [-2, -1]], [[-1, 0], [1, -2], [2, 2]]][f];
    patches.forEach(function (p) { ctx.fillRect(x + p[0], y + p[1], 1, 1); });
    ctx.fillRect(x + patches[0][0] + 1, y + patches[0][1], 1, 1);
  }

  // ---------- static layers (pre-rendered) ----------
  var standsA, standsB, sky, standW;
  function buildLayers() {
    sky = document.createElement("canvas"); sky.width = W; sky.height = H;
    var s = sky.getContext("2d");
    var bands = 12;
    for (var i = 0; i < bands; i++) {
      var t = i / (bands - 1);
      s.fillStyle = mix(C.sky0, C.sky1, t);
      s.fillRect(0, Math.floor(i * 90 / bands), W, Math.ceil(90 / bands) + 1);
    }
    for (i = 0; i < 70; i++) {
      s.fillStyle = hash(i * 7 + 1) > 0.8 ? "#ffffff" : "#8ea0d8";
      s.fillRect(Math.floor(hash(i * 13 + 5) * W), Math.floor(hash(i * 17 + 3) * 70), 1, 1);
    }

    standW = Math.ceil(WORLD_W * STAND_PARALLAX + W);
    standsA = document.createElement("canvas"); standsA.width = standW; standsA.height = H;
    standsB = document.createElement("canvas"); standsB.width = standW; standsB.height = H;
    [standsA, standsB].forEach(function (cv, excited) {
      var c = cv.getContext("2d");
      // roof
      c.fillStyle = C.roof; c.fillRect(0, 62, standW, 9);
      c.fillStyle = "#2a3157"; c.fillRect(0, 70, standW, 1);
      for (var x = 0; x < standW; x += 24) { c.fillStyle = "#30386a"; c.fillRect(x, 62, 2, 9); }
      // stand body
      c.fillStyle = C.stand; c.fillRect(0, 71, standW, 79);
      // crowd rows
      var shirts = ["#e63946", "#e63946", "#f1faee", "#f1faee", "#e63946", "#457b9d", "#ffd166", "#06d6a0", "#ef476f", "#8d99ae", "#1d3557"];
      var skins = ["#e0ac69", "#c68642", "#8d5524", "#f1c27d", "#ffdbac"];
      for (var row = 0; row < 15; row++) {
        var y = 74 + row * 5;
        c.fillStyle = C.standLine; c.fillRect(0, y + 4, standW, 1);
        for (x = (row % 2) * 2; x < standW; x += 4) {
          var n = hash(row * 100003 + x);
          if (n < 0.1) continue; // empty seat
          var up = excited && hash(x * 31 + row) > 0.35 ? 1 : 0;
          c.fillStyle = shirts[Math.floor(hash(n * 1e6) * shirts.length)];
          c.fillRect(x, y + 2 - up, 3, 2);
          c.fillStyle = skins[Math.floor(hash(n * 7e5 + 3) * skins.length)];
          c.fillRect(x + 1, y + 0 - up, 2, 2);
          if (up && hash(x + row * 7) > 0.5) { c.fillStyle = skins[0]; c.fillRect(x, y - 2, 1, 2); c.fillRect(x + 3, y - 2, 1, 2); }
        }
      }
      // front wall of stand
      c.fillStyle = "#0f1228"; c.fillRect(0, 148, standW, 3);
    });
  }
  function mix(a, b, t) {
    var pa = parseInt(a.slice(1), 16), pb = parseInt(b.slice(1), 16);
    var r = Math.round(((pa >> 16) & 255) * (1 - t) + ((pb >> 16) & 255) * t);
    var g = Math.round(((pa >> 8) & 255) * (1 - t) + ((pb >> 8) & 255) * t);
    var bl = Math.round((pa & 255) * (1 - t) + (pb & 255) * t);
    return "rgb(" + r + "," + g + "," + bl + ")";
  }

  // ---------- state ----------
  var ctx, canvas;
  var cam = 0, camTarget = 0;
  var mode = "idle", t = 0, last = 0;
  var kick = null;          // {meters, tier, path, launchT, done, cb}
  var excitement = 0.15;
  var particles = [];
  var flash = 0, shake = 0, netBulge = 0;
  var progressFn = null;

  function buildPath(meters) {
    // Returns list of segments {x0, x1 (m), h (px apex), h1 (px end height), dur (s)}
    if (meters >= 100) {
      return [
        { x0: 0, x1: 101.6, h: 90, h1: 9, dur: 1.45, ease: false },
        { x0: 101.6, x1: 102.2, h: 2, h1: 0, dur: 0.35, ease: false, inNet: true },
      ];
    }
    var D = meters;
    var hmax = Math.max(14, Math.min(110, D * PX_PER_M * 0.8 * 0.32));
    var flight = 0.55 + 0.85 * Math.sqrt(D / 100);
    return [
      { x0: 0, x1: D * 0.8, h: hmax, h1: 0, dur: flight },
      { x0: D * 0.8, x1: D * 0.94, h: hmax * 0.16, h1: 0, dur: 0.32 },
      { x0: D * 0.94, x1: D * 0.985, h: hmax * 0.04, h1: 0, dur: 0.16 },
      { x0: D * 0.985, x1: D, h: 0, h1: 0, dur: 0.35, ease: true },
    ];
  }
  function pathAt(path, tt) {
    for (var i = 0; i < path.length; i++) {
      var s = path[i];
      if (tt <= s.dur || i === path.length - 1) {
        var u = Math.max(0, Math.min(1, tt / s.dur));
        var ux = s.ease ? 1 - (1 - u) * (1 - u) : u;
        return { m: s.x0 + (s.x1 - s.x0) * ux, h: 4 * s.h * u * (1 - u) + (s.h1 || 0) * u, seg: i, u: u, done: i === path.length - 1 && u >= 1 };
      }
      tt -= s.dur;
    }
  }

  var RUN = 0.36, STRIKE = 0.47;

  function kickerPose() {
    if (mode === "idle") return lerpPose(POSES.idle, POSES.idle2, (Math.sin(t * 3) + 1) / 2);
    var k = kick, kt = t - k.start;
    var fx = KICK_X - 22;
    if (kt < RUN) {
      var frame = Math.floor(kt / 0.09) % 2 ? POSES.runA : POSES.runB;
      return { pose: frame, x: fx + (kt / RUN) * 12 };
    }
    var x = fx + 12;
    if (kt < STRIKE) return { pose: lerpPose(POSES.windup, POSES.strike, (kt - RUN) / (STRIKE - RUN)), x: x };
    if (kt < STRIKE + 0.12) return { pose: lerpPose(POSES.strike, POSES.follow, (kt - STRIKE) / 0.12), x: x };
    if (k.whiff) {
      if (kt < STRIKE + 0.45) return { pose: POSES.follow, x: x };
      return { pose: lerpPose(POSES.follow, POSES.fallen, Math.min(1, (kt - STRIKE - 0.45) / 0.25)), x: x };
    }
    if (kt < STRIKE + 0.7) return { pose: POSES.follow, x: x };
    var reactT = kt - STRIKE - 0.7;
    var r = k.tier >= 4 ? (Math.floor(reactT / 0.25) % 2 ? POSES.cheer2 : POSES.cheer) :
            k.tier >= 2 ? (Math.floor(reactT / 0.2) % 2 ? POSES.clap : POSES.idle) : POSES.shrug;
    return { pose: lerpPose(POSES.follow, r, Math.min(1, reactT / 0.2)), x: x };
  }

  function update(dt) {
    t += dt;
    if (mode === "kick" && kick) {
      var kt = t - kick.start;
      if (!kick.whiff && kt >= STRIKE) {
        var p = pathAt(kick.path, kt - STRIKE);
        kick.ball = p;
        if (progressFn) progressFn(p.m);
        if (kick.tier === 5 && p.seg === 1 && !kick.scored) {
          kick.scored = true; netBulge = 1; flash = 1; shake = 6; excitement = 1;
          for (var i = 0; i < 90; i++) particles.push({ x: Math.random() * W, y: -Math.random() * 60, vx: (Math.random() - 0.5) * 30, vy: 20 + Math.random() * 40, c: Math.random() > 0.4 ? tierColors[5] : "#ffffff", life: 3 + Math.random() * 2 });
          if (window.BallionAudio) BallionAudio.goal();
        }
        if (kick.trail) { kick.trail.push({ x: KICK_X + p.m * PX_PER_M, y: GROUND - 4 - p.h, a: 1 }); if (kick.trail.length > 40) kick.trail.shift(); }
        if (p.done && !kick.finished) {
          kick.finished = true;
          excitement = [0.2, 0.35, 0.5, 0.7, 0.9, 1][kick.tier];
          if (kick.tier !== 5 && window.BallionAudio) BallionAudio.land(kick.tier);
          setTimeout(function () { var cb = kick && kick.cb; if (cb) { kick.cb = null; cb(); } }, kick.tier === 5 ? 1300 : 700);
        }
        camTarget = KICK_X + p.m * PX_PER_M - 150;
      }
      if (kick.whiff && kt > STRIKE + 1.1 && !kick.finished) {
        kick.finished = true;
        setTimeout(function () { var cb = kick && kick.cb; if (cb) { kick.cb = null; cb(); } }, 400);
      }
      if (!kick.launched && kt >= STRIKE) {
        kick.launched = true;
        if (window.BallionAudio) BallionAudio[kick.whiff ? "whiff" : "kick"](kick.tier);
      }
    }
    camTarget = Math.max(0, Math.min(WORLD_W - W, camTarget));
    cam += (camTarget - cam) * Math.min(1, dt * 5);
    excitement += (0.15 - excitement) * dt * 0.15;
    flash = Math.max(0, flash - dt * 1.5);
    shake = Math.max(0, shake - dt * 10);
    netBulge = Math.max(0, netBulge - dt * 0.8);
    particles.forEach(function (p) { p.x += p.vx * dt; p.y += p.vy * dt; p.vy += 15 * dt; p.life -= dt; });
    particles = particles.filter(function (p) { return p.life > 0 && p.y < H + 10; });
  }

  function render() {
    var sx = shake ? Math.round((Math.random() - 0.5) * shake) : 0;
    var sy = shake ? Math.round((Math.random() - 0.5) * shake) : 0;
    ctx.save();
    ctx.translate(sx, sy);
    ctx.drawImage(sky, 0, 0);
    var c = Math.round(cam);

    // floodlight towers
    for (var tx = 30; tx < WORLD_W * TOWER_PARALLAX + W; tx += 210) {
      var x = Math.round(tx - c * TOWER_PARALLAX);
      if (x < -40 || x > W + 40) continue;
      ctx.fillStyle = "#2b3155"; ctx.fillRect(x + 7, 14, 2, 50);
      ctx.fillStyle = "#3a4170"; ctx.fillRect(x, 8, 16, 8);
      for (var ly = 0; ly < 2; ly++) for (var lx = 0; lx < 5; lx++) {
        ctx.fillStyle = (hash(lx + ly * 5 + Math.floor(t * 2)) > 0.97) ? "#fff7c2" : "#fffbe6";
        ctx.fillRect(x + 1 + lx * 3, 9 + ly * 3, 2, 2);
      }
      var g = ctx.createRadialGradient(x + 8, 12, 1, x + 8, 12, 46);
      g.addColorStop(0, "rgba(255,248,210,0.35)"); g.addColorStop(1, "rgba(255,248,210,0)");
      ctx.fillStyle = g; ctx.fillRect(x - 40, -30, 96, 90);
    }

    // stands (calm layer + excited columns)
    var so = Math.round(c * STAND_PARALLAX);
    ctx.drawImage(standsA, so, 0, W, H, 0, 0, W, H);
    var tick = Math.floor(t * 6);
    for (var col = 0; col < W; col += 4) {
      if (hash(((col + so) >> 2) * 977 + tick) < excitement * 0.6) ctx.drawImage(standsB, col + so, 60, 4, 92, col, 60, 4, 92);
    }

    ctx.fillStyle = "rgba(6,8,24,0.42)"; ctx.fillRect(0, 71, W, 79);

    // world-space layers
    ctx.save();
    ctx.translate(-c, 0);
    // ad boards
    var boards = ["#1d3557", "#e63946", "#2a9d8f", "#6a4c93"];
    for (var bx = -40, bi = 0; bx < WORLD_W + 80; bx += 72, bi++) {
      if (bx + 72 < c || bx > c + W) continue;
      ctx.fillStyle = "#05060f"; ctx.fillRect(bx, 150, 72, 12);
      ctx.fillStyle = boards[bi % boards.length]; ctx.fillRect(bx + 1, 151, 70, 10);
      drawText(ctx, bi % 3 === 2 ? "GOAL!" : "BALLION", bx + 36 - Math.floor(textWidth(bi % 3 === 2 ? "GOAL!" : "BALLION") / 2), 153, "#f1faee");
    }
    // pitch
    ctx.fillStyle = C.grassFar; ctx.fillRect(c, 162, W, 6);
    for (var m = -10; m < 115; m += 5) {
      var px = KICK_X + m * PX_PER_M;
      if (px + 50 < c || px > c + W) continue;
      ctx.fillStyle = (Math.floor(m / 5) % 2 === 0) ? C.grassA : C.grassB;
      ctx.fillRect(px, 168, 50, H - 168);
    }
    ctx.fillStyle = C.line; ctx.fillRect(c, 167, W, 1);
    // goal line + distance markings
    for (m = 0; m <= 100; m += 10) {
      px = KICK_X + m * PX_PER_M;
      ctx.fillStyle = "rgba(232,245,233,0.55)";
      ctx.fillRect(px, GROUND + 3, 1, 3);
      var label = m + "M";
      drawText(ctx, label, px - Math.floor(textWidth(label) / 2), 210, "rgba(232,245,233,0.7)");
    }
    ctx.fillStyle = C.line; ctx.fillRect(GOAL_X, 168, 1, H - 168);
    ctx.fillRect(KICK_X - 1, GROUND + 1, 3, 2); // penalty-style spot under the ball
    // tier cones at thresholds
    [10, 25, 40, 60, 85].forEach(function (mm, i) {
      var cx = KICK_X + mm * PX_PER_M;
      ctx.fillStyle = C.outline; ctx.fillRect(cx - 3, GROUND - 13, 7, 1);
      for (var r = 0; r < 6; r++) {
        ctx.fillStyle = r === 2 ? "#ffffff" : tierColors[i];
        ctx.fillRect(cx - Math.floor(r / 2), GROUND - 18 + r, 1 + 2 * Math.floor(r / 2), 1);
      }
      ctx.fillStyle = tierColors[i]; ctx.fillRect(cx - 3, GROUND - 12, 7, 1);
    });
    // goal (side view): near post, crossbar running back, net
    var top = GROUND - 26, back = GOAL_X + 22;
    ctx.fillStyle = "rgba(220,230,240,0.35)";
    for (var nx = GOAL_X + 3; nx < back; nx += 3) {
      var bulge = netBulge * 5 * Math.sin(((nx - GOAL_X) / 22) * Math.PI);
      for (var ny = top + 2; ny < GROUND; ny += 3) ctx.fillRect(Math.round(nx + bulge * ((ny - top) / 26)), ny, 1, 1);
    }
    thickLine(ctx, GOAL_X + 14, top, back + netBulge * 4, GROUND, 1, "rgba(220,230,240,0.6)");
    ctx.fillStyle = "#ffffff";
    ctx.fillRect(GOAL_X - 1, top, 3, GROUND - top + 1);   // near post
    ctx.fillRect(GOAL_X - 1, top, 16, 2);                 // crossbar (receding)
    ctx.fillStyle = tierColors[5]; ctx.fillRect(GOAL_X - 1, top - 6, 1, 6);   // corner flag
    ctx.fillRect(GOAL_X, top - 6, 4, 3);

    // trail
    if (kick && kick.trail) kick.trail.forEach(function (p, i) {
      ctx.globalAlpha = (i / kick.trail.length) * 0.9;
      ctx.fillStyle = tierColors[kick.tier];
      ctx.fillRect(Math.round(p.x) - 1, Math.round(p.y) - 1, 3, 3);
    });
    ctx.globalAlpha = 1;

    // landing flag
    if (kick && kick.finished && !kick.whiff && kick.tier < 5) {
      var fxp = Math.round(KICK_X + kick.meters * PX_PER_M) + 6;
      ctx.fillStyle = "#e8e8e8"; ctx.fillRect(fxp, GROUND - 22, 1, 22);
      ctx.fillStyle = tierColors[kick.tier];
      for (var fy = 0; fy < 7; fy++) ctx.fillRect(fxp + 1, GROUND - 22 + fy, 9 - Math.abs(3 - fy), 1);
      var lab = kick.meters + "M", lw = textWidth(lab, 2), lx = fxp - Math.floor(lw / 2);
      ctx.fillStyle = "rgba(10,13,31,0.85)"; ctx.fillRect(lx - 4, GROUND - 40, lw + 8, 18);
      ctx.fillStyle = tierColors[kick.tier]; ctx.fillRect(lx - 4, GROUND - 23, lw + 8, 1);
      drawText(ctx, lab, lx, GROUND - 36, kick.tier === 3 ? "#9fb3ff" : tierColors[kick.tier], 2);
    }

    // kicker
    var kp = kickerPose();
    if (mode === "idle") drawKicker(ctx, KICK_X - 10, kp);
    else drawKicker(ctx, Math.round(kp.x), kp.pose);

    // ball + shadow
    var bm = 0, bh = 0;
    if (kick && kick.ball) { bm = kick.ball.m; bh = kick.ball.h; }
    var bx2 = KICK_X + bm * PX_PER_M + 3;
    var inGoal = bm > 100;
    if (!inGoal) {
      ctx.fillStyle = "rgba(0,0,0,0.35)";
      var sw = Math.max(2, 7 - Math.floor(bh / 18));
      ctx.fillRect(Math.round(bx2 - sw / 2), GROUND + 1, sw, 2);
    }
    if (bh > 6 && kick && !kick.whiff) {
      ctx.globalAlpha = 0.55; disc(ctx, Math.round(bx2), Math.round(GROUND - 3 - bh), 6, tierColors[kick.tier]); ctx.globalAlpha = 1;
    }
    var wob = kick && kick.whiff && t - kick.start > STRIKE && t - kick.start < STRIKE + 0.4 ? Math.round(Math.sin(t * 60)) : 0;
    drawBall(ctx, bx2 + wob, GROUND - 3 - bh, kick && kick.ball && !kick.ball.done ? (t * 18) : 0);
    if (inGoal) { // net in front of the ball
      ctx.fillStyle = "rgba(220,230,240,0.45)";
      for (nx = GOAL_X + 2; nx < back; nx += 4) ctx.fillRect(nx + Math.round(netBulge * 3), top + 4, 1, GROUND - top - 4);
    }
    ctx.restore();

    // screen-space effects
    particles.forEach(function (p) { ctx.fillStyle = p.c; ctx.fillRect(Math.round(p.x), Math.round(p.y), 2, 2); });
    if (kick && kick.scored) {
      var s = "GOAL!", sc = 6, wv = textWidth(s, sc);
      var bob = Math.round(Math.sin(t * 6) * 2);
      drawText(ctx, s, Math.round(W / 2 - wv / 2), 30 + bob, tierColors[5], sc, C.outline);
    }
    if (flash > 0) { ctx.fillStyle = "rgba(255,240,180," + (flash * 0.5) + ")"; ctx.fillRect(0, 0, W, H); }
    ctx.restore();
  }

  function loop(now) {
    var dt = last ? Math.min(0.05, (now - last) / 1000) : 0;
    last = now;
    update(dt);
    render();
    raf(loop);
  }

  window.BallionScene = {
    init: function (cv, colors) {
      canvas = cv; ctx = canvas.getContext("2d");
      canvas.width = W; canvas.height = H;
      ctx.imageSmoothingEnabled = false;
      if (colors) tierColors = colors;
      buildLayers();
      raf(loop);
    },
    reset: function () { mode = "idle"; kick = null; camTarget = 0; particles = []; netBulge = 0; flash = 0; },
    kick: function (meters, tier, done) {
      mode = "kick";
      kick = { meters: meters, tier: tier, path: buildPath(meters), start: t, cb: done, trail: [], ball: null };
      excitement = 0.4;
    },
    whiff: function (done) {
      mode = "kick";
      kick = { meters: 0, tier: 0, whiff: true, start: t, cb: done, ball: null };
    },
    onProgress: function (fn) { progressFn = fn; },
    // Debug helper: freeze the scene at a point in a kick (used for screenshots).
    debugFreeze: function (meters, tier, seconds) {
      this.kick(meters, tier, null);
      var steps = Math.round(seconds / 0.02);
      for (var i = 0; i < steps; i++) update(0.02);
      cam = camTarget;
      render();
      update = function () {};
    },
    W: W, H: H,
  };
})();
