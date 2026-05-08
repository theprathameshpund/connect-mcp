import os

from utils.file_utils import write_json


def create_mcp_config(plugin_root, server_url, transport, server_name):
    config = {
        "mcpServers": {
            server_name: {
                "type": "http",
                "url": server_url,
                "transport": transport
            }
        }
    }

    write_json(os.path.join(plugin_root, ".mcp.json"), config)
