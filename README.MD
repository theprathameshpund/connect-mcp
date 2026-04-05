# 🚀 connect-mcp

> Connect any MCP server to Claude Desktop in seconds — no config editing, no guesswork.

---

## ⚡ The Problem

Integrating an MCP server into Claude Desktop usually means:

- Finding config file manually
- Editing JSON
- Debugging errors blindly
- Restarting app repeatedly

One mistake → everything breaks ❌

---

## ✅ The Solution
```bash
npx connect-mcp --url  claude
```

👉 Done. Your MCP server is connected.

---

## 🚀 Quick Start
```bash
npx connect-mcp --url http://localhost:8000/mcp claude
```

Restart Claude Desktop → Your tools are live ✅

---

## 🔌 3 Ways to Connect MCP

### 1️⃣ CLI (Recommended)
```bash
npx connect-mcp --url  claude
```

**Example:**
```bash
npx connect-mcp --url https://your-domain.com/mcp claude
```

---

### 2️⃣ Direct URL (Auto Claude Mode)
```bash
npx connect-mcp --url 
```

👉 Automatically connects to Claude

---

### 3️⃣ Interactive Mode
```bash
npx connect-mcp
```

👉 Prompts you for:
- MCP URL
- Platform

---

## ⚠️ IMPORTANT (Very Critical)

✅ Always use:
/mcp

❌ Never use:
/mcp/sse

👉 `/sse` is an internal endpoint — will **FAIL**

---

## 🧠 How It Works

Claude expects config like:
```json
{
  "mcpServers": {
    "loan": {
      "transport": {
        "type": "http",
        "url": "http://localhost:8000/mcp"
      }
    }
  }
}
```

👉 This tool:
- Finds your config file
- Safely updates it
- Validates structure
- Avoids breaking existing config

---

## 📂 Config Location

| OS      | Path                                                                 |
|---------|----------------------------------------------------------------------|
| Windows | `%APPDATA%\Claude\claude_desktop_config.json`                        |
| macOS   | `~/Library/Application Support/Claude/claude_desktop_config.json`   |

---

## ⚙️ Requirements

- Node.js >= 16
- Claude Desktop installed

---

## 🧪 Example MCP Server
```bash
npx connect-mcp --url http://localhost:8000/mcp claude
```

Then in Claude:

> "Create a loan for Rahul of 5000"

👉 Your MCP tool gets called automatically ✅

---

## 🔥 Supported Transport

| Type             | Supported |
|------------------|-----------|
| HTTP (SSE)       | ✅         |
| Local Command    | ❌ (coming soon) |

---

## 🧩 Platform Support

| Platform       | Status |
|----------------|--------|
| Claude Desktop | ✅      |
| Cursor         | 🚧      |
| VS Code        | 🚧      |

---

## ❓ FAQ

**Do I need to restart Claude?**  
Yes — required.

**Will this overwrite my config?**  
No — only updates `mcpServers`.

**Does this support ngrok?**  
⚠️ Not reliable (SSE issues). Use instead:
- `localhost` (best for local dev)
- Cloudflare Tunnel (recommended for production)

**Can I use my own MCP server?**  
Yes — that's the main use case.

---

## 🚀 Roadmap

- [ ] Cursor support
- [ ] VS Code support
- [ ] MCP validation
- [ ] Tool discovery preview
- [ ] Cloud deployment helpers

---

## 🤝 Contributing

PRs welcome.

---

## 📜 License

MIT © theprathameshpund