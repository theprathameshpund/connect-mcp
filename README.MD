# 🚀 connect-mcp

> Connect any MCP server to Claude Desktop, Claude CoWork/Code **or VS Code** in seconds — no config editing, no guesswork.

---

## ⚡ The Problem

Integrating an MCP server usually means:

- Finding config file manually
- Editing JSON
- Debugging errors blindly
- Restarting the app repeatedly

One mistake → everything breaks ❌

---

## ✅ The Solution
```bash
npx connect-mcp
```

👉 Answer two questions → Done. Your MCP server is connected.

---

## 🚀 Quick Start

### Claude Desktop
```bash
npx connect-mcp --url http://localhost:8000/mcp claude
```
Restart Claude Desktop → Your tools are live ✅

### VS Code (GitHub Copilot / Agent mode)
```bash
npx connect-mcp --url http://localhost:8000/mcp vscode
```
Reload VS Code → Open GitHub Copilot Chat → Agent mode → 🔌 icon → Server is live ✅

---

## 🔌 Supported Platforms

| Platform                   | Status |
|----------------------------|--------|
| Claude Desktop             | ✅      |
| Claude CoWork / Code       | ✅      |
| VS Code (GitHub Copilot)   | ✅ NEW  |
| VS Code Insiders           | ✅ NEW  |
| Cursor                     | 🚧 Coming soon |

---

## 🔌 3 Ways to Connect MCP

### 1️⃣ CLI (Recommended)

**Claude Desktop:**
```bash
npx connect-mcp --url <MCP_URL> claude
```

**VS Code:**
```bash
npx connect-mcp --url <MCP_URL> vscode
```

**VS Code Insiders:**
```bash
npx connect-mcp --url <MCP_URL> --insiders vscode
```

**Claude CoWork / Code:**
```bash
npx connect-mcp --url <MCP_URL> cowork
```

---

### 2️⃣ Direct URL (Auto Claude Mode)
```bash
npx connect-mcp --url <MCP_URL>
```
👉 Automatically connects to Claude Desktop.

---

### 3️⃣ Interactive Mode
```bash
npx connect-mcp
```

👉 Prompts you for:
- MCP server URL
- Platform (Claude Desktop / CoWork / **VS Code** / VS Code Insiders)

---

## ⚠️ IMPORTANT (Very Critical)

✅ Always use: `/mcp`

❌ Never use: `/mcp/sse`

👉 `/sse` is an internal endpoint — will **FAIL**

---

## 🧠 How VS Code MCP Config Works

VS Code reads MCP servers from:

| OS      | Path                                         |
|---------|----------------------------------------------|
| Windows | `%APPDATA%\Code\User\mcp.json`               |
| macOS   | `~/Library/Application Support/Code/User/mcp.json` |
| Linux   | `~/.config/Code/User/mcp.json`               |

**VS Code Insiders:** Replace `Code` with `Code - Insiders` in the paths above.

The `connect-mcp vscode` command writes this config automatically:

```json
{
  "servers": {
    "localhost": {
      "type": "http",
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

After connecting:
1. Reload VS Code: `Ctrl+Shift+P` → **Developer: Reload Window**
2. Open **GitHub Copilot Chat** (Ctrl+Alt+I)
3. Switch to **Agent mode** → Click the 🔌 plugin icon
4. Your MCP tools will appear there ✅

---

## 🧠 How Claude Desktop MCP Config Works

Claude expects config like:
```json
{
  "mcpServers": {
    "localhost": {
      "command": "npx",
      "args": ["mcp-remote", "http://localhost:8000/mcp"]
    }
  }
}
```

| OS      | Path                                                                |
|---------|---------------------------------------------------------------------|
| Windows | `%APPDATA%\Claude\claude_desktop_config.json`                       |
| macOS   | `~/Library/Application Support/Claude/claude_desktop_config.json`  |

---

## ⚙️ Requirements

- Node.js >= 16
- For Claude Desktop: Claude Desktop installed
- For VS Code: VS Code with GitHub Copilot extension and `chat.mcp.enabled` set to `true`

---

## 🧪 Example Usage

```bash
# Connect a local dev server to VS Code
npx connect-mcp --url http://localhost:8000/mcp vscode

# Connect a production server to Claude Desktop
npx connect-mcp --url https://your-domain.com/mcp claude

# Interactive — let it guide you
npx connect-mcp
```

---

## 🔥 Supported Transport

| Type          | Supported    |
|---------------|--------------|
| HTTP (SSE)    | ✅            |
| Local Command | ❌ (coming soon) |

---

## ❓ FAQ

**Do I need to restart VS Code after connecting?**
Yes — run `Ctrl+Shift+P` → **Developer: Reload Window**, or close and reopen VS Code.

**Do I need to restart Claude Desktop?**
Yes — required.

**Will this overwrite my config?**
No — it only adds/updates the specific server entry. All other existing entries are preserved.

**Does this support ngrok?**
⚠️ Not reliable (SSE issues). Use instead:
- `localhost` (best for local dev)
- Cloudflare Tunnel (recommended for production)

**Can I use my own MCP server?**
Yes — that's the main use case.

**What VS Code version supports MCP?**
VS Code 1.99+ with GitHub Copilot extension.

---

## 🚀 Roadmap

- [x] Claude Desktop support
- [x] Claude CoWork / Code support
- [x] VS Code (GitHub Copilot) support
- [ ] Cursor support
- [ ] MCP validation (ping server before writing config)
- [ ] Tool discovery preview
- [ ] Cloud deployment helpers

---

## 🤝 Contributing

PRs welcome.

---

## 📜 License

MIT © theprathameshpund