#!/usr/bin/env node

const { Command } = require("commander");
const setupClaude = require("./commands/claude");
const inquirer = require("inquirer");

const program = new Command();

program
  .name("connect-mcp")
  .description("One-click MCP integration tool")
  .version("1.0.0");

// ✅ GLOBAL OPTION ONLY
program.option("--url <url>", "MCP server URL");

// ✅ COMMAND: Claude (NO requiredOption here)
program
  .command("claude")
  .description("Connect MCP to Claude Desktop")
  .action(async () => {
    const globalOptions = program.opts();

    if (!globalOptions.url) {
      console.error("❌ Error: --url is required");
      process.exit(1);
    }

    await setupClaude(globalOptions.url);
  });

// ✅ INTERACTIVE MODE
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
        { name: "Cursor (coming soon)", value: "cursor", disabled: true },
        { name: "VS Code (coming soon)", value: "vscode", disabled: true },
      ],
    },
  ]);

  if (answers.platform === "claude") {
    await setupClaude(answers.url);
  }
}

// ✅ MAIN
async function main() {
  const args = process.argv.slice(2);

  // No args → interactive
  if (args.length === 0) {
    return interactiveMode();
  }

  program.parse(process.argv);

  const options = program.opts();

  // Only --url → default to Claude
  if (options.url && !args.includes("claude")) {
    return setupClaude(options.url);
  }
}

main();