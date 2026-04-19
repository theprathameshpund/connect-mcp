import os
from utils.file_utils import write_json
from config import MCP_SERVER_URL, PLUGIN_NAME


def create_mcp_config(plugin_root, server_url):
    config = {
        "servers": [
            {
                "name": PLUGIN_NAME,
                "url": server_url,
                "transport": "sse"
            }
        ]
    }
    write_json(os.path.join(plugin_root, ".mcp.json"), config)