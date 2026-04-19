const getVSCodePath = require("../utils/getVSCodePath");
const readConfig = require("../utils/readConfig");
const writeConfig = require("../utils/writeConfig");
const logger = require("../utils/logger");

/**
 * Connects an MCP server to VS Code by writing to the global mcp.json file.
 *
 * VS Code uses a "servers" key (not "mcpServers") with the following structure
 * for HTTP/SSE remote servers:
 *
 * {
 *   "servers": {
 *     "my-server": {
 *       "type": "http",
 *       "url": "https://example.com/mcp"
 *     }
 *   }
 * }
 *
 * @param {string} url - The MCP server URL (must be a valid URL)
 * @param {{ insiders?: boolean }} [opts] - Optional flags
 */
async function setupVSCode(url, opts = {}) {
  try {
    const { insiders = false } = opts;
    const configPath = getVSCodePath(insiders);

    logger.info(`VS Code MCP config path: ${configPath}`);

    // Read existing config or start fresh
    let config = await readConfig(configPath);

    // VS Code uses "servers" (not "mcpServers")
    if (!config.servers) {
      config.servers = {};
    }

    // Derive a clean server name from the hostname
    const parsedUrl = new URL(url);
    const serverName = parsedUrl.hostname.replace(/\./g, "-") || "mcp-server";

    if (config.servers[serverName]) {
      logger.warn(`Server "${serverName}" already exists in VS Code config. Updating...`);
    }

    // VS Code HTTP transport format
    config.servers[serverName] = {
      type: "http",
      url: url,
    };

    await writeConfig(configPath, config);

    logger.success(`MCP server "${serverName}" added to VS Code!`);
    logger.info(`Config saved at: ${configPath}`);
    logger.info("Reload VS Code (Ctrl+Shift+P → Developer: Reload Window) to apply changes.");
    logger.info("Then open GitHub Copilot Chat → Agent mode → 🔌 icon to verify your server.");

  } catch (err) {
    logger.error(`Failed to configure VS Code: ${err.message}`);
    process.exit(1);
  }
}

module.exports = setupVSCode;
