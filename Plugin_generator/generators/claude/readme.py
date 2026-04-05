import os
from utils.file_utils import write_file
from config import AUTHOR_NAME


def create_readme(plugin_root, tools):

    readme_path = os.path.join(plugin_root, "README.md")

    capabilities = ""
    for tool in tools:
        readable_name = tool["name"].replace("_", " ").title()
        capabilities += f"- {readable_name}\n"

    words = []
    for tool in tools:
        words.extend(tool["name"].split("_"))

    common_words = {}
    for w in words:
        common_words[w] = common_words.get(w, 0) + 1

    sorted_words = sorted(common_words.items(), key=lambda x: -x[1])

    domain_word = sorted_words[0][0] if sorted_words else "MCP"
    domain_title = domain_word.capitalize()

    overview = f"This plugin enables Claude to interact with a {domain_title.lower()} system using MCP tools."

    content = f"""# {domain_title} MCP Plugin

## Overview

{overview}

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

## Architecture

Claude (CoWork)
        |
        v
Claude Plugin
        |
        v
MCP Server (SSE)
        |
        v
Backend System

---

## How It Works

- Claude reads skills from the `skills/` directory
- Each skill maps to an MCP tool
- The MCP server executes tool calls
- Results are returned to Claude

---

## Notes

- MCP server must be running and accessible
- Uses SSE transport
- Plugin generated automatically from MCP server

---

## Author

{AUTHOR_NAME}
"""

    write_file(readme_path, content)