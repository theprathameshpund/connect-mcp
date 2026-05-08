const { spawn } = require("child_process");
const path = require("path");

function runPythonGenerator(url, type, label) {
  return new Promise((resolve, reject) => {
    console.log(`⚡ Generating MCP plugin (${label})...\n`);

    const scriptPath = path.join(__dirname, "../Plugin_generator/main.py");
    const child = spawn(
      "python",
      [scriptPath, "--url", url, "--type", type],
      { stdio: ["ignore", "pipe", "pipe"] }
    );

    let stdout = "";
    let stderr = "";

    child.stdout.on("data", (data) => {
      stdout += data.toString();
    });

    child.stderr.on("data", (data) => {
      stderr += data.toString();
    });

    child.on("error", (err) => {
      reject(new Error(`Failed to start Python: ${err.message}`));
    });

    child.on("close", (code) => {
      if (stdout) {
        console.log(stdout);
      }

      if (stderr) {
        console.error(stderr);
      }

      if (code !== 0) {
        if (stderr.includes("ModuleNotFoundError")) {
          console.error(
            "Install Python dependencies with: python -m pip install -r Plugin_generator\\requirements.txt"
          );
        }
        reject(new Error(`Python generator exited with code ${code}`));
        return;
      }

      console.log("\n✅ Plugin generated successfully!");
      resolve();
    });
  });
}

module.exports = runPythonGenerator;
