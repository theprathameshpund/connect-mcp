const os = require("os");
const path = require("path");
const fs = require("fs-extra");

function getClaudePath() {
  const home = os.homedir();
  const platform = os.platform();

  // 🪟 WINDOWS
  if (platform === "win32") {
    const appData = process.env.APPDATA;

    // 1. Try UWP path (Windows Store version)
    const localAppData = process.env.LOCALAPPDATA;

    if (localAppData) {
      const packagesPath = path.join(localAppData, "Packages");

      if (fs.existsSync(packagesPath)) {
        const dirs = fs.readdirSync(packagesPath);

        const claudeDir = dirs.find((dir) =>
          dir.toLowerCase().includes("claude")
        );

        if (claudeDir) {
          const uwpPath = path.join(
            packagesPath,
            claudeDir,
            "LocalCache",
            "Roaming",
            "Claude",
            "claude_desktop_config.json"
          );

          return uwpPath;
        }
      }
    }

    // 2. Fallback to normal path
    return path.join(appData, "Claude", "claude_desktop_config.json");
  }

  // 🍎 macOS
  if (platform === "darwin") {
    return path.join(
      home,
      "Library",
      "Application Support",
      "Claude",
      "claude_desktop_config.json"
    );
  }

  // 🐧 Linux
  return path.join(
    home,
    ".config",
    "Claude",
    "claude_desktop_config.json"
  );
}

module.exports = getClaudePath;