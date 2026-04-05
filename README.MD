---

### Remove a server
```bash
connect-mcp remove --name <name>
```
```bash
connect-mcp remove --name "filesystem"
# ✔ Removed "filesystem" from Claude Desktop config.
```

---

### View current config

Inspect the raw Claude Desktop configuration file:
```bash
connect-mcp config --show
```

Open the config file directly in your default editor:
```bash
connect-mcp config --edit
```

---

### Validate your config

Check if your current configuration file is valid before restarting Claude Desktop:
```bash
connect-mcp validate
```

---

## How it works

Claude Desktop stores its MCP server configuration in a JSON file at a platform-specific path:

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

`connect-mcp` reads this file, safely merges your new server entry into the `mcpServers` object, validates the result, and writes it back — all without touching anything else in the file.
```json
// What gets added to your config
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-filesystem", "/Users/me/projects"]
    }
  }
}
```

No magic, no hidden state. You can always open the file and see exactly what was changed.

---

## Platform support

| Platform | Status |
|----------|--------|
| macOS | ✅ Supported |
| Windows | ✅ Supported |
| Linux | ⚠️ Claude Desktop not yet available on Linux |

---

## Requirements

- Node.js 18 or later
- Claude Desktop installed ([download here](https://claude.ai/download))

---

## Roadmap

`connect-mcp` is the starting point for a broader ecosystem. Here's what's coming:

**CLI (current)**
- [x] Add / remove / list MCP servers
- [x] Interactive setup wizard
- [x] Config validation
- [ ] One-command updates for existing integrations
- [ ] Import/export integration configs to share with your team
- [ ] Health check: verify a server starts correctly before registering it

**Platform integrations (planned)**
- Claude Desktop ✅
- Cursor
- Windsurf
- VS Code (Copilot)
- Continue.dev

**MCP Hub (coming soon)**

A web platform and registry for discovering, publishing, and managing MCP integrations:
- Browse a marketplace of ready-to-use MCP servers
- One-command install from the registry: `connect-mcp install @community/postgres-mcp`
- Dashboard to monitor connected servers and their health
- Team management: share integration configs across your organisation
- Version pinning and update notifications

---

## Contributing

Contributions are welcome. If you're adding support for a new platform (e.g. Cursor, Windsurf), the core pattern to follow is:

1. Add a config resolver in `src/platforms/` that returns the config file path for that platform
2. Add a reader/writer pair that handles that platform's config schema
3. Register the platform in `src/platforms/index.ts`
4. Add tests in `tests/platforms/`

See [CONTRIBUTING.md](./CONTRIBUTING.md) for the full guide.

---

## Frequently asked questions

**Do I need to restart Claude Desktop after connecting a server?**  
Yes. Claude Desktop reads the config file on startup, so a restart is required for changes to take effect.

**Will this break my existing Claude Desktop config?**  
No. `connect-mcp` only modifies the `mcpServers` key. All other settings are left untouched. A backup of the original config is written to `claude_desktop_config.backup.json` before any change.

**What if the config file doesn't exist yet?**  
`connect-mcp` creates it for you with the correct structure.

**Can I use this with a local MCP server I'm building?**  
Yes, that's the primary use case. Point `--command` at your local script:
```bash
connect-mcp add --name "dev-server" --command "node" --args "./src/index.js"
```

**Is my API key or environment variable stored securely?**  
Environment variables are stored in the Claude Desktop config file in plain text, the same way Claude Desktop expects them. Do not commit your config file to version control.

---

## License

MIT © 2024 — see [LICENSE](./LICENSE) for details.

---

<p align="center">
  Built to make MCP simple. One command at a time.
</p>
