#!/usr/bin/env node

const { Command } = require("commander");
const setupClaude = require("./commands/claude");
const runCowork   = require("./commands/cowork");
const setupVSCode = require("./commands/vscode");
const inquirer    = require("inquirer");

const program = new Command();

program
  .name("connect-mcp")
  .description("One-click MCP integration tool")
  .version("0.1.2");

// ✅ GLOBAL OPTION
program.option("--url <url>", "MCP server URL");
program.option("--insiders",   "Target VS Code Insiders instead of stable VS Code");

// =========================================================
// ✅ CLAUDE COMMAND
// =========================================================
program
  .command("claude")
  .description("Connect MCP to Claude Desktop")
  .action(async () => {
    const { url } = program.opts();
    if (!url) { console.error("❌ Error: --url is required"); process.exit(1); }
    await setupClaude(url);
  });

// =========================================================
// ✅ COWORK / CODE COMMAND
// =========================================================
program
  .command("cowork")
  .description("Generate MCP plugin (cowork/code)")
  .action(async () => {
    const { url } = program.opts();
    if (!url) { console.error("❌ Error: --url is required"); process.exit(1); }
    await runCowork(url);
  });

// =========================================================
// ✅ VSCODE COMMAND  (NEW)
// =========================================================
program
  .command("vscode")
  .description("Connect MCP to VS Code (GitHub Copilot / Agent mode)")
  .action(async () => {
    const { url, insiders } = program.opts();
    if (!url) { console.error("❌ Error: --url is required"); process.exit(1); }
    await setupVSCode(url, { insiders });
  });

// =========================================================
// ✅ INTERACTIVE MODE
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
          return "Please enter a valid URL (e.g. https://example.com/mcp)";
        }
      },
    },
    {
      type: "list",
      name: "platform",
      message: "Select platform to connect:",
      choices: [
        { name: "Claude Desktop",               value: "claude"  },
        { name: "Claude CoWork / Code Plugin",  value: "cowork"  },
        { name: "VS Code (GitHub Copilot)",      value: "vscode"  },
        { name: "VS Code Insiders",              value: "vscode-insiders" },
        { name: "Cursor (coming soon)",          value: "cursor",  disabled: true },
      ],
    },
  ]);

  if (answers.platform === "claude")          { await setupClaude(answers.url); }
  if (answers.platform === "cowork")          { await runCowork(answers.url);   }
  if (answers.platform === "vscode")          { await setupVSCode(answers.url, { insiders: false }); }
  if (answers.platform === "vscode-insiders") { await setupVSCode(answers.url, { insiders: true  }); }
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
  const knownCommands = ["claude", "cowork", "vscode"];
  const hasCommand = knownCommands.some((c) => args.includes(c));

  if (options.url && !hasCommand) {
    return setupClaude(options.url);
  }
}

main();