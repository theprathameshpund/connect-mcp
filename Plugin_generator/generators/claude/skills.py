import os
from utils.file_utils import ensure_dir, write_file


def create_skill(tool, skills_dir):


    tool_name = tool["name"]
    description = tool.get("description", "No description provided.")
    parameters = tool.get("parameters", {})
    # ...existing code...
    # Parameter table
    param_table = "| Parameter | Type | Required | Description |\n|-----------|------|----------|-------------|\n"
    param_rows = []
    for param, meta in parameters.get("properties", {}).items():
        param_type = meta.get("type", "string")
        required = "✅ Yes" if param in parameters.get("required", []) else "❌ No"
        desc = meta.get("description", "")
        param_rows.append(f"| `{param}` | `{param_type}` | {required} | {desc} |\n")
    if param_rows:
        param_table += "".join(param_rows)
    else:
        param_table = ""

    skill_folder = os.path.join(skills_dir, tool_name)
    ensure_dir(skill_folder)
    skill_path = os.path.join(skill_folder, "SKILL.md")

    # Compose sections only if data is available
    sections = []
    # Header
    sections.append(f"---\nname: {tool_name}\ndescription: >\n  {description}\n---\n")
    # Title
    sections.append(f"# {tool_name.title()} Skill\n")
    # Description
    if description:
        sections.append(f"{description}\n")
    # Parameters
    if param_table:
        sections.append("## Parameters\n\n" + param_table + "\n")

    content = "\n".join(sections)
    write_file(skill_path, content)


def generate_skills(tools, plugin_root):

    skills_dir = os.path.join(plugin_root, "skills")

    ensure_dir(skills_dir)

    for tool in tools:
        create_skill(tool, skills_dir)