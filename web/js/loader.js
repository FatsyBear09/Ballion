/* Ballion data loader. data/index.js (every prompt's text and theme) loads up front; each prompt's
 * answers live in data/p/<id>.js and are fetched on demand, so a game downloads only its 7 prompts.
 * Plain <script> tags rather than fetch(), so the game also works when opened straight from disk. */
(function () {
  "use strict";
  var version = (window.BALLION_INDEX && window.BALLION_INDEX.v) || "";

  function script(src, done) {
    var s = document.createElement("script");
    s.src = src + (version ? "?v=" + version : "");
    s.onload = function () { done(true); };
    s.onerror = function () { s.remove(); done(false); };
    document.head.appendChild(s);
  }

  var BD = window.BallionData = {
    prompts: {},          // id -> {id, ans}
    onNames: null,        // set by the game: receives the global alias list
    add: function (p) { BD.prompts[p.id] = p; },
    names: function (list) { if (BD.onNames) BD.onNames(list); },

    // Load the given prompt ids; cb(failedIds or null).
    load: function (ids, cb) {
      var left = ids.filter(function (id) { return !BD.prompts[id]; });
      if (!left.length) return cb(null);
      var pending = left.length, failed = [];
      left.forEach(function (id) {
        script("data/p/" + id + ".js", function (ok) {
          if (!ok || !BD.prompts[id]) failed.push(id);
          if (--pending === 0) cb(failed.length ? failed : null);
        });
      });
    },

    loadNames: function () { script("data/names.js", function () {}); },
  };
})();
