/* Ballion answer matcher: alias lookup + conservative typo correction.
 *
 * match(prompt, input) returns one of
 *   {kind: "exact",     index}            input is a known name/alias of exactly one answer
 *   {kind: "corrected", index, typed}     close typo of exactly one answer's name/alias
 *   {kind: "ambiguous", options: [names]} input fits several answers equally well
 *   {kind: "miss"}                        not (close to) any answer
 *
 * Correction is deliberately strict: it only fires when the input is within a small edit
 * distance of an alias (scaled with length), the best answer is clearly better than the
 * runner-up, and the input is not itself the exact name of a *different* known entity
 * (e.g. "Phil Neville" never autocorrects to "Gary Neville").
 */
(function (root) {
  "use strict";

  var TRANSLIT = { "ø": "o", "æ": "ae", "œ": "oe", "ß": "ss", "ł": "l", "đ": "d", "ð": "d", "þ": "th", "ı": "i" };

  function norm(s) {
    s = String(s || "").toLowerCase().replace(/[øæœßłđðþı]/g, function (c) { return TRANSLIT[c]; });
    s = s.normalize("NFKD").replace(/[̀-ͯ]/g, "");
    s = s.replace(/&/g, " and ").replace(/[^a-z0-9 ]+/g, " ");
    return s.replace(/\s+/g, " ").trim();
  }

  // Optimal string alignment distance (Levenshtein + adjacent transpositions), with early exit.
  function editDistance(a, b, max) {
    var la = a.length, lb = b.length;
    if (Math.abs(la - lb) > max) return max + 1;
    var prev2 = null, prev = new Array(lb + 1), cur;
    for (var j = 0; j <= lb; j++) prev[j] = j;
    for (var i = 1; i <= la; i++) {
      cur = new Array(lb + 1);
      cur[0] = i;
      var rowMin = cur[0];
      for (j = 1; j <= lb; j++) {
        var cost = a.charCodeAt(i - 1) === b.charCodeAt(j - 1) ? 0 : 1;
        var v = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost);
        if (i > 1 && j > 1 && a[i - 1] === b[j - 2] && a[i - 2] === b[j - 1]) v = Math.min(v, prev2[j - 2] + 1);
        cur[j] = v;
        if (v < rowMin) rowMin = v;
      }
      if (rowMin > max) return max + 1;
      prev2 = prev;
      prev = cur;
    }
    return prev[lb];
  }

  // How many typos we tolerate for an input of this length.
  function allowance(len) {
    if (len <= 3) return 0;
    if (len <= 5) return 1;
    if (len <= 10) return 2;
    return 3;
  }

  function buildIndex(prompt) {
    if (prompt._index) return prompt._index;
    var exact = {};
    var entries = [];
    prompt.ans.forEach(function (a, i) {
      var names = a.a.slice();
      names.push(norm(a.n));
      names.forEach(function (al) {
        (exact[al] = exact[al] || []).indexOf(i) < 0 && exact[al].push(i);
        entries.push({ alias: al, compact: al.replace(/ /g, ""), index: i });
      });
    });
    var first = {};
    prompt.ans.forEach(function (a, i) { if (a.fn) (first[a.fn] = first[a.fn] || []).push(i); });
    prompt._index = { exact: exact, entries: entries, first: first };
    return prompt._index;
  }

  var globalNames = null; // every alias of every answer in every prompt
  function buildGlobal(prompts) {
    globalNames = {};
    prompts.forEach(function (p) {
      p.ans.forEach(function (a) {
        a.a.forEach(function (al) { globalNames[al] = true; });
        globalNames[norm(a.n)] = true;
      });
    });
  }

  function match(prompt, input) {
    var q = norm(input);
    if (!q) return { kind: "miss" };
    var idx = buildIndex(prompt);

    var hits = idx.exact[q];
    if (hits && hits.length === 1) return { kind: "exact", index: hits[0] };
    if (hits && hits.length > 1) {
      // "Ronaldo" is both R9's display name and Cristiano's surname: the display name wins.
      var byName = hits.filter(function (i) { return norm(prompt.ans[i].n) === q; });
      if (byName.length === 1) return { kind: "exact", index: byName[0] };
      return { kind: "ambiguous", options: hits.map(function (i) { return prompt.ans[i].n; }) };
    }

    // First names ("Cristiano", "Zlatan") count when only one answer in this prompt has it.
    var fn = idx.first[q];
    if (fn && fn.length === 1) return { kind: "exact", index: fn[0] };
    if (fn && fn.length > 1) return { kind: "ambiguous", options: fn.map(function (i) { return prompt.ans[i].n; }) };

    // A correctly spelled name of some other entity is a real (wrong) answer, not a typo.
    if (globalNames && globalNames[q]) return { kind: "miss" };

    var max = allowance(q.length);
    if (max === 0) return { kind: "miss" };
    var qc = q.replace(/ /g, "");
    var best = {}; // answer index -> best distance
    idx.entries.forEach(function (e) {
      if (e.alias.length < 4) return; // never fuzzy-match very short aliases
      var d = Math.min(editDistance(q, e.alias, max), editDistance(qc, e.compact, max));
      // Scale tolerance with the alias too, so "cole" can't reach "cobi jones".
      if (d <= max && d <= allowance(e.alias.length) && (best[e.index] === undefined || d < best[e.index])) best[e.index] = d;
    });
    var ranked = Object.keys(best).map(Number).sort(function (a, b) { return best[a] - best[b]; });
    if (!ranked.length) return { kind: "miss" };
    var top = best[ranked[0]];
    var tied = ranked.filter(function (i) { return best[i] === top; });
    if (tied.length > 1) {
      // Tie-break on the display name itself ("Wemley Stadium" -> Wembley Stadium, not the original one).
      var dn = tied.map(function (i) { return editDistance(q, norm(prompt.ans[i].n), 6); });
      var minD = Math.min.apply(null, dn);
      var winners = tied.filter(function (i, k) { return dn[k] === minD; });
      if (winners.length === 1 && minD <= max) return { kind: "corrected", index: winners[0], typed: input };
      return { kind: "ambiguous", options: tied.map(function (i) { return prompt.ans[i].n; }) };
    }
    return { kind: "corrected", index: ranked[0], typed: input };
  }

  var api = { norm: norm, editDistance: editDistance, match: match, buildGlobal: buildGlobal };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.BallionMatcher = api;
})(this);
