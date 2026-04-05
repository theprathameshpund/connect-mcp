const { exec } = require("child_process");
const path = require("path");

module.exports = async function runCowork(url) {
  console.log("⚡ Generating MCP plugin (cowork/code)...\n");

  const scriptPath = path.join(__dirname, "../Plugin_generator/main.py");

  exec(
    `python "${scriptPath}" --url ${url} --type cowork`,
    (err, stdout, stderr) => {
      if (err) {
        console.error("❌ Python execution failed:", err.message);
        return;
      }

      if (stderr) {
        console.error(stderr);
      }

      console.log(stdout);
      console.log("\n✅ Plugin generated successfully!");
    }
  );
};