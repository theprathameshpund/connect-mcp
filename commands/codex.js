const runPythonGenerator = require("./pluginGenerator");

module.exports = async function runCodex(url) {
  try {
    await runPythonGenerator(url, "codex", "codex");
  } catch (err) {
    console.error("❌ Python execution failed:", err.message);
    process.exit(1);
  }
};
