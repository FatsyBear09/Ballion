// Run: node web/test/matcher.test.js
var fs = require("fs"), path = require("path");
var M = require("../js/matcher.js");
var data = require("./load.js")();
M.buildGlobal(data.prompts);
var P = {}; data.prompts.forEach(function (p) { P[p.id] = p; });

var cases = [
  // [prompt, input, expected kind, expected answer name (or null)]
  ["p001", "Thierry Henry", "exact", "Thierry Henry"],
  ["p001", "henry", "exact", "Thierry Henry"],
  ["p001", "Theirry Henri", "corrected", "Thierry Henry"],
  ["p001", "Bergkmap", "corrected", "Dennis Bergkamp"],
  ["p001", "Kolo Toure", "exact", "Kolo Touré"],
  ["p001", "Yaya Toure", "miss", null],
  ["p001", "Cesc Fabregas", "miss", null],
  ["p001", "Lauren", "exact", "Lauren"],
  ["p001", "Ljungburg", "corrected", "Freddie Ljungberg"],
  ["p002", "Ronaldo", "exact", "Ronaldo"],
  ["p002", "Cristiano", "exact", "Cristiano Ronaldo"],
  ["p002", "CR7", "exact", "Cristiano Ronaldo"],
  ["p002", "Mesi", "corrected", "Lionel Messi"],
  ["p002", "Ronaldinho", "miss", null],
  ["p003", "Man Utd", "exact", "Manchester United"],
  ["p003", "Inter", "exact", "Internazionale"],
  ["p003", "Bayern Munchen", "exact", "Bayern Munich"],
  ["p003", "Juventus FC", "exact", "Juventus"],
  ["p003", "Juventas", "corrected", "Juventus"],
  ["p003", "Real Madird", "corrected", "Real Madrid"],
  ["p003", "Celtic", "miss", null],
  ["p044", "Côte d'Ivoire", "exact", "Ivory Coast"],
  ["p044", "USA", "exact", "United States"],
  ["p044", "Holland", "exact", "Netherlands"],
  ["p044", "Brasil", "corrected", "Brazil"],
  ["p083", "Highbury", "exact", "Arsenal Stadium (Highbury)"],
  ["p095", "Figo", "exact", "Luís Figo"],
  ["p001", "Thierry", "exact", "Thierry Henry"],
  ["p024", "Wayne", "exact", "Wayne Rooney"],
  ["p001", "", "miss", null],
  ["p001", "asdfgh", "miss", null],
];
var fail = 0;
cases.forEach(function (c) {
  var r = M.match(P[c[0]], c[1]);
  var name = r.index !== undefined ? P[c[0]].ans[r.index].n : null;
  var ok = r.kind === c[2] && (c[3] === null || name === c[3]);
  if (!ok) fail++;
  console.log((ok ? "ok  " : "FAIL") + "  " + c[0] + "  " + JSON.stringify(c[1]) + " -> " + r.kind + (name ? " " + name : "") + (r.options ? " " + r.options.join(" / ") : ""));
});
console.log(fail ? fail + " failed" : "all " + cases.length + " passed");
process.exit(fail ? 1 : 0);
