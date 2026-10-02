/* Tiny 8-bit sound effects with WebAudio (no files). window.BallionAudio */
(function () {
  "use strict";
  var ac = null, muted = false;
  try { muted = localStorage.getItem("ballion-muted") === "1"; } catch (e) {}

  function ctx() {
    if (!ac) { try { ac = new (window.AudioContext || window.webkitAudioContext)(); } catch (e) { return null; } }
    if (ac.state === "suspended") ac.resume();
    return ac;
  }
  function tone(freq, dur, type, vol, when, slideTo) {
    var a = ctx(); if (!a || muted) return;
    var t0 = a.currentTime + (when || 0);
    var o = a.createOscillator(), g = a.createGain();
    o.type = type || "square";
    o.frequency.setValueAtTime(freq, t0);
    if (slideTo) o.frequency.exponentialRampToValueAtTime(slideTo, t0 + dur);
    g.gain.setValueAtTime(vol || 0.08, t0);
    g.gain.exponentialRampToValueAtTime(0.0001, t0 + dur);
    o.connect(g); g.connect(a.destination);
    o.start(t0); o.stop(t0 + dur + 0.02);
  }
  function noise(dur, vol, when, lp) {
    var a = ctx(); if (!a || muted) return;
    var t0 = a.currentTime + (when || 0);
    var buf = a.createBuffer(1, Math.floor(a.sampleRate * dur), a.sampleRate);
    var d = buf.getChannelData(0);
    for (var i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
    var src = a.createBufferSource(), g = a.createGain(), f = a.createBiquadFilter();
    f.type = "lowpass"; f.frequency.value = lp || 1200;
    src.buffer = buf;
    g.gain.setValueAtTime(0.0001, t0);
    g.gain.exponentialRampToValueAtTime(vol || 0.1, t0 + Math.min(0.3, dur / 3));
    g.gain.exponentialRampToValueAtTime(0.0001, t0 + dur);
    src.connect(f); f.connect(g); g.connect(a.destination);
    src.start(t0);
  }

  window.BallionAudio = {
    unlock: function () { ctx(); },
    isMuted: function () { return muted; },
    toggle: function () {
      muted = !muted;
      try { localStorage.setItem("ballion-muted", muted ? "1" : "0"); } catch (e) {}
      return muted;
    },
    kick: function () { tone(120, 0.12, "triangle", 0.25, 0, 50); noise(0.08, 0.12, 0, 3000); },
    whiff: function () { tone(400, 0.25, "square", 0.05, 0, 120); },
    land: function (tier) {
      tone(90, 0.1, "triangle", 0.2);
      var notes = [[262], [262, 330], [262, 330, 392], [330, 392, 494], [392, 494, 587, 784]][tier] || [262];
      notes.forEach(function (f, i) { tone(f, 0.14, "square", 0.06, 0.1 + i * 0.09); });
      if (tier >= 3) noise(1.2, 0.05 + tier * 0.01, 0.1, 900);
    },
    goal: function () {
      [523, 659, 784, 1047, 784, 1047].forEach(function (f, i) { tone(f, 0.18, "square", 0.07, i * 0.11); });
      noise(2.2, 0.12, 0, 1000);
    },
    wrong: function () { tone(150, 0.18, "square", 0.06, 0, 110); },
    tick: function () { tone(880, 0.05, "square", 0.04); },
    click: function () { tone(660, 0.04, "square", 0.03); },
  };
})();
