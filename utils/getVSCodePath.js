const os = require("os");
const path = require("path");

/**
 * Returns the path to the VS Code global MCP configuration file (mcp.json).
 * Supports Windows, macOS, and Linux.
 *
 * VS Code MCP config lives in the user-data directory alongside settings.json:
 *   Windows : %APPDATA%\Code\User\mcp.json
 *   macOS   : ~/Library/Application Support/Code/User/mcp.json
 *   Linux   : ~/.config/Code/User/mcp.json
 *
 * For VS Code Insiders, replace "Code" with "Code - Insiders".
 */
function getVSCodePath(insiders = false) {
  const home = os.homedir();
  const platform = os.platform();
  const variant = insiders ? "Code - Insiders" : "Code";

  if (platform === "win32") {
    const appData = process.env.APPDATA || path.join(home, "AppData", "Roaming");
    return path.join(appData, variant, "User", "mcp.json");
  }

  if (platform === "darwin") {
    return path.join(home, "Library", "Application Support", variant, "User", "mcp.json");
  }

  // Linux / other
  return path.join(home, ".config", variant, "User", "mcp.json");
}

module.exports = getVSCodePath;
