from urllib.parse import urlparse
import re

from config import PLUGIN_NAME


def normalize_name(value):
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    normalized = re.sub(r"-+", "-", normalized)
    return normalized[:64] or "mcp-server"


def plugin_name_from_url(server_url):
    configured_name = normalize_name(PLUGIN_NAME)
    if configured_name and configured_name not in {"temp-mcp", "mcp"}:
        return configured_name

    parsed = urlparse(server_url)
    host = parsed.hostname or "mcp-server"
    return normalize_name(f"{host}-mcp")


def display_name(plugin_name):
    return plugin_name.replace("-", " ").title()
