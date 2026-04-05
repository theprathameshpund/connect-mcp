import os
from utils.file_utils import ensure_dir, write_file


def create_skill(tool, skills_dir):

    tool_name = tool["name"]
    description = tool.get("description", "No description provided.")

    skill_folder = os.path.join(skills_dir, tool_name)

    ensure_dir(skill_folder)

    skill_path = os.path.join(skill_folder, "SKILL.md")

    content = f"""---
name: {tool_name}
---

name: {tool_name}
description: {description}
---

When using the {tool_name} tool:

1. Understand the user's request related to {tool_name}
2. Confirm any required details before calling the tool
3. Use the `{tool_name}` MCP tool to perform the operation
4. Return the result clearly to the user
"""

    write_file(skill_path, content)


def generate_skills(tools, plugin_root):

    skills_dir = os.path.join(plugin_root, "skills")

    ensure_dir(skills_dir)

    for tool in tools:
        create_skill(tool, skills_dir)