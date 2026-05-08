import os

from config import AUTHOR_NAME, PLUGIN_DESCRIPTION
from generators.codex.naming import display_name, plugin_name_from_url
from utils.file_utils import ensure_dir, write_json


def _default_prompts(tools):
    prompts = []
    for tool in tools[:3]:
        readable_name = tool["name"].replace("_", " ")
        prompts.append(f"Use {readable_name} from this MCP server.")
    return prompts or ["Show me the tools from this MCP server."]


def create_plugin_json(plugin_root, server_url, tools):
    plugin_name = plugin_name_from_url(server_url)
    plugin_display_name = display_name(plugin_name)
    description = PLUGIN_DESCRIPTION
    if description.lower().startswith("temp"):
        description = f"Use the {plugin_display_name} MCP server from Codex."

    plugin_dir = os.path.join(plugin_root, ".codex-plugin")
    ensure_dir(plugin_dir)

    plugin_json = {
        "name": plugin_name,
        "version": "1.0.0",
        "description": description,
        "author": {
            "name": AUTHOR_NAME
        },
        "license": "MIT",
        "keywords": ["mcp", "codex", "tools"],
        "mcpServers": "./.mcp.json",
        "interface": {
            "displayName": plugin_display_name,
            "shortDescription": description[:120],
            "longDescription": description,
            "developerName": AUTHOR_NAME,
            "category": "Productivity",
            "capabilities": ["Interactive", "Read", "Write"],
            "defaultPrompt": _default_prompts(tools),
            "brandColor": "#3B82F6",
            "screenshots": []
        }
    }

    write_json(os.path.join(plugin_dir, "plugin.json"), plugin_json)
    return plugin_name
