#!/usr/bin/env node

const { Command } = require("commander");
const setupClaude = require("./commands/claude");
const inquirer = require("inquirer"); // ✅ FIXED

const program = new Command();

program
  .name("connect-mcp")
  .description("One-click MCP integration tool")
  .version("1.0.0");

// ✅ GLOBAL OPTION
program.option("--url <url>", "MCP server URL");

// ✅ COMMAND: Claude (explicit)
program
  .command("claude")
  .description("Connect MCP to Claude Desktop")
  .requiredOption("--url <url>", "MCP server URL")
  .action(async (options) => {
    await setupClaude(options.url);
  });

// ✅ INTERACTIVE MODE (UPDATED)
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
        {
          name: "Claude Desktop",
          value: "claude",
        },
        {
          name: "Cursor (coming soon)",
          value: "cursor",
          disabled: true,
        },
        {
          name: "VS Code (coming soon)",
          value: "vscode",
          disabled: true,
        },
      ],
    },
  ]);

  // ✅ SAFE CHECK
  if (answers.platform === "claude") {
    await setupClaude(answers.url);
  }
}

// ✅ MAIN LOGIC (UPDATED)
async function main() {
  const args = process.argv.slice(2);

  // Case 1: No args → interactive
  if (args.length === 0) {
    return interactiveMode();
  }

  // Parse CLI
  program.parse(process.argv);

  const options = program.opts();

  // Case 2: Only --url → default to Claude
  if (options.url && !args.includes("claude")) {
    return setupClaude(options.url);
  }
}

main();