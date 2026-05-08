import os

from config import AUTHOR_NAME
from generators.codex.naming import display_name, plugin_name_from_url
from utils.file_utils import write_file


def create_readme(plugin_root, tools, transport, server_url):
    plugin_name = plugin_name_from_url(server_url)
    plugin_display_name = display_name(plugin_name)
    readme_path = os.path.join(plugin_root, "README.md")

    capabilities = ""
    for tool in tools:
        readable_name = tool["name"].replace("_", " ").title()
        capabilities += f"- {readable_name}\n"

    content = f"""# {plugin_display_name} Codex Plugin

## Overview

This plugin connects Codex to an MCP server and exposes its tools through the plugin MCP config.

---

## MCP Server

- URL: `{server_url}`
- Transport: `{transport}`

---

## Capabilities

{capabilities}

---

## Available Tools
"""

    for tool in tools:
        content += f"- **{tool['name']}**: {tool.get('description', '')}\n"

    content += f"""

---

## Files

- `.codex-plugin/plugin.json` defines the Codex plugin manifest
- `.mcp.json` points Codex at the MCP server

---

## Author

{AUTHOR_NAME}
"""

    write_file(readme_path, content)
