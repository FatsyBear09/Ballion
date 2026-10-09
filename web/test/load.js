// Load the exported game data (web/data/index.js + every web/data/p/<id>.js) the way the browser does,
// returning {tiers, themes, prompts}; each prompt is its index entry plus .ans.
var fs = require("fs"), path = require("path"), vm = require("vm");
module.exports = function () {
  var dir = path.join(__dirname, "..", "data");
  var ctx = { window: {}, BallionData: null };
  var loaded = {};
  ctx.BallionData = { add: function (p) { loaded[p.id] = p; }, names: function () {} };
  vm.createContext(ctx);
  vm.runInContext(fs.readFileSync(path.join(dir, "index.js"), "utf8"), ctx);
  fs.readdirSync(path.join(dir, "p")).forEach(function (f) {
    vm.runInContext(fs.readFileSync(path.join(dir, "p", f), "utf8"), ctx);
  });
  var data = ctx.window.BALLION_INDEX;
  data.prompts.forEach(function (p) { p.ans = loaded[p.id].ans; });
  return data;
};
