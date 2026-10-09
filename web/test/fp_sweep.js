// Estimate false autocorrections: typo'd names of entities that are NOT valid for a prompt.
var fs = require("fs"), path = require("path");
var M = require("../js/matcher.js");
var data = require("./load.js")();
M.buildGlobal(data.prompts);
var rnd = 12345; function r() { rnd = (rnd * 1103515245 + 12345) % 2147483648; return rnd / 2147483648; }
function typo(s) { var i = Math.floor(r() * (s.length - 1)) + 1; return s.slice(0, i) + s.slice(i + 1); } // drop a char
var tried = 0, wrong = 0, examples = [];
data.prompts.forEach(function (p) {
  var valid = {}; p.ans.forEach(function (a) { valid[a.n] = 1; });
  for (var k = 0; k < 40; k++) {
    var op = data.prompts[Math.floor(r() * data.prompts.length)];
    if (op.th !== p.th || op.g === p.g) continue; // same theme => similar kind of name (hardest case)
    var a = op.ans[Math.floor(r() * op.ans.length)];
    if (valid[a.n] || a.n.length < 6) continue;
    var res = M.match(p, typo(a.n)); tried++;
    if (res.kind === "corrected" || res.kind === "exact") {
      var got = p.ans[res.index].n;
      if (M.norm(got) !== M.norm(a.n)) { wrong++; if (examples.length < 15) examples.push(p.id + ": " + a.n + " -> " + got); }
    }
  }
});
console.log("tried", tried, "false matches", wrong, "(" + (100 * wrong / tried).toFixed(1) + "%)");
examples.forEach(function (e) { console.log("  " + e); });
