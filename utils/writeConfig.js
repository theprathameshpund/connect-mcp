const fs = require("fs-extra");
const path = require("path");

async function writeConfig(configPath, config) {
  await fs.ensureDir(path.dirname(configPath));
  await fs.writeJson(configPath, config, { spaces: 2 });
}

module.exports = writeConfig;