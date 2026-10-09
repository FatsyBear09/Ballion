// For every answer: drop the 4th character (as the browser self-test does) and check it still matches.
var fs = require("fs"), path = require("path");
var M = require("../js/matcher.js");
var data = require("./load.js")();
M.buildGlobal(data.prompts);
var n = 0, bad = {}, ex = [];
data.prompts.forEach(function (p) {
  p.ans.forEach(function (a, i) {
    if (a.n.length <= 7) return;
    var typo = a.n.slice(0, 3) + a.n.slice(4); n++;
    var r = M.match(p, typo);
    var ok = (r.kind === "exact" || r.kind === "corrected") && r.index === i;
    if (!ok) { bad[r.kind] = (bad[r.kind] || 0) + 1; if (ex.length < 25) ex.push(p.id + " " + a.n + " <- " + typo + " => " + r.kind + (r.index !== undefined ? " " + p.ans[r.index].n : "") + (r.options ? " [" + r.options.join(", ") + "]" : "")); }
  });
});
console.log("typos", n, "failed", JSON.stringify(bad));
ex.forEach(function (e) { console.log("  " + e); });
