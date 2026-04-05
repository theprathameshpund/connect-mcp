#!/usr/bin/env node

const { Command } = require("commander");
const setupClaude = require("./commands/claude");
const runCowork = require("./commands/cowork"); // 👈 NEW
const inquirer = require("inquirer");

const program = new Command();

program
  .name("connect-mcp")
  .description("One-click MCP integration tool")
  .version("1.0.0");

// ✅ GLOBAL OPTION
program.option("--url <url>", "MCP server URL");

// =========================================================
// ✅ CLAUDE COMMAND (unchanged)
// =========================================================
program
  .command("claude")
  .description("Connect MCP to Claude Desktop")
  .action(async () => {
    const { url } = program.opts();

    if (!url) {
      console.error("❌ Error: --url is required");
      process.exit(1);
    }

    await setupClaude(url);
  });

// =========================================================
// ✅ COWORK / CODE COMMAND (NEW)
// =========================================================
program
  .command("cowork")
  .description("Generate MCP plugin (cowork/code)")
  .action(async () => {
    const { url } = program.opts();

    if (!url) {
      console.error("❌ Error: --url is required");
      process.exit(1);
    }

    await runCowork(url);
  });

// =========================================================
// ✅ INTERACTIVE MODE (UPDATED)
// =========================================================
async function interactiveMode() {
  const answers = await inquirer.prompt([
    {
      type: "input",
      name: "url",
      message: "Enter MCP server URL:",
      validate: (input) => {
        try {
          new URL(input);
          return true;
        } catch {
          return "Please enter a valid URL";
        }
      },
    },
    {
      type: "list",
      name: "platform",
      message: "Select platform:",
      choices: [
        { name: "Claude Desktop", value: "claude" },
        { name: "Claude CoWork / Code Plugin", value: "cowork" }, // 👈 NEW
        { name: "Cursor (coming soon)", value: "cursor", disabled: true },
        { name: "VS Code (coming soon)", value: "vscode", disabled: true },
      ],
    },
  ]);

  if (answers.platform === "claude") {
    await setupClaude(answers.url);
  }

  if (answers.platform === "cowork") {
    await runCowork(answers.url);
  }
}

// =========================================================
// ✅ MAIN
// =========================================================
async function main() {
  const args = process.argv.slice(2);

  // No args → interactive
  if (args.length === 0) {
    return interactiveMode();
  }

  program.parse(process.argv);

  const options = program.opts();

  // Default fallback → Claude
  if (options.url && !args.includes("claude") && !args.includes("cowork")) {
    return setupClaude(options.url);
  }
}

main();