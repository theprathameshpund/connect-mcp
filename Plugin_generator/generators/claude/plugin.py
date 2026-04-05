import os
from utils.file_utils import ensure_dir, write_json
from config import PLUGIN_NAME, PLUGIN_DESCRIPTION, AUTHOR_NAME


def create_plugin_json(plugin_root):

    plugin_dir = os.path.join(plugin_root, ".claude-plugin")

    ensure_dir(plugin_dir)

    plugin_json = {
        "name": PLUGIN_NAME,
        "description": PLUGIN_DESCRIPTION,
        "version": "1.0.0",
        "author": {
            "name": AUTHOR_NAME
        }
    }

    write_json(os.path.join(plugin_dir, "plugin.json"), plugin_json)