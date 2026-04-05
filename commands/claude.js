const getClaudePath = require("../utils/getClaudePath");
const readConfig = require("../utils/readConfig");
const writeConfig = require("../utils/writeConfig");
const logger = require("../utils/logger");

async function setupClaude(url) {
  try {
    const configPath = getClaudePath();
    console.log("📁 Claude config path:", configPath);

    let config = await readConfig(configPath);

    if (!config.mcpServers) {
      config.mcpServers = {};
    }

    // Generate clean server name
    const serverName = new URL(url).hostname.replace(/\./g, "-");

    if (config.mcpServers[serverName]) {
      logger.warn("Server already exists. Updating...");
    }

    // ✅ NEW FORMAT (IMPORTANT)
    config.mcpServers[serverName] = {
      command: "npx",
      args: ["mcp-remote", url]
    };

    await writeConfig(configPath, config);

    logger.success("MCP server added to Claude Desktop!");
    logger.info("Restart Claude Desktop to apply changes.");

  } catch (err) {
    logger.error(err.message);
  }
}

module.exports = setupClaude;