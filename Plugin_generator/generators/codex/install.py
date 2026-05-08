import json
import os
import shutil
from pathlib import Path

from utils.file_utils import ensure_dir, write_json


def _ensure_child_path(parent, child):
    parent_path = Path(parent).resolve()
    child_path = Path(child).resolve()
    if os.path.commonpath([str(parent_path), str(child_path)]) != str(parent_path):
        raise ValueError(f"Refusing to write outside {parent_path}: {child_path}")
    return child_path


def _load_marketplace(path):
    if not os.path.exists(path):
        return {
            "name": "local-connect-mcp",
            "interface": {
                "displayName": "Local Connect MCP"
            },
            "plugins": []
        }

    with open(path, "r", encoding="utf-8") as f:
        marketplace = json.load(f)

    marketplace.setdefault("name", "local-connect-mcp")
    marketplace.setdefault("interface", {})
    marketplace["interface"].setdefault("displayName", "Local Connect MCP")
    marketplace.setdefault("plugins", [])
    return marketplace


def _marketplace_entry(plugin_name):
    return {
        "name": plugin_name,
        "source": {
            "source": "local",
            "path": f"./plugins/{plugin_name}"
        },
        "policy": {
            "installation": "AVAILABLE",
            "authentication": "ON_INSTALL"
        },
        "category": "Productivity"
    }


def _upsert_marketplace_plugin(marketplace, plugin_name):
    entry = _marketplace_entry(plugin_name)
    plugins = marketplace["plugins"]

    for index, plugin in enumerate(plugins):
        if plugin.get("name") == plugin_name:
            plugins[index] = entry
            return

    plugins.append(entry)


def install_codex_plugin(generated_plugin_root, plugin_name, workspace_root):
    workspace = Path(workspace_root).resolve()
    plugins_root = workspace / "plugins"
    target_plugin_root = _ensure_child_path(plugins_root, plugins_root / plugin_name)

    ensure_dir(plugins_root)

    if target_plugin_root.exists():
        shutil.rmtree(target_plugin_root)

    shutil.copytree(generated_plugin_root, target_plugin_root)

    marketplace_dir = workspace / ".agents" / "plugins"
    ensure_dir(marketplace_dir)
    marketplace_path = marketplace_dir / "marketplace.json"

    marketplace = _load_marketplace(marketplace_path)
    _upsert_marketplace_plugin(marketplace, plugin_name)
    write_json(marketplace_path, marketplace)

    return str(target_plugin_root), str(marketplace_path)
