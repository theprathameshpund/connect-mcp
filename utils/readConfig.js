const fs = require("fs-extra");

async function readConfig(configPath) {
  try {
    if (await fs.pathExists(configPath)) {
      return await fs.readJson(configPath);
    }
    return {};
  } catch {
    return {};
  }
}

module.exports = readConfig;