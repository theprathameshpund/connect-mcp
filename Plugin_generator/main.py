import asyncio
import os
import shutil
import sys
import traceback
import argparse

# Fix import path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mcp_local.discovery import discover_tools
from mcp_local.transport import (
    TransportNegotiationError,
    discover_tools_streamable_http,
    legacy_sse_session,
)

from generators.claude.plugin import create_plugin_json as create_claude_plugin_json
from generators.claude.skills import generate_skills
from generators.claude.readme import create_readme as create_claude_readme
from generators.claude.mcp_config import create_mcp_config as create_claude_mcp_config
from generators.codex.plugin import create_plugin_json as create_codex_plugin_json
from generators.codex.readme import create_readme as create_codex_readme
from generators.codex.mcp_config import create_mcp_config as create_codex_mcp_config
from generators.codex.install import install_codex_plugin


# ---------------------------
# CLI ARGUMENT PARSER
# ---------------------------
def parse_args():
    parser = argparse.ArgumentParser(description="MCP Plugin Generator")

    parser.add_argument(
        "--url",
        type=str,
        required=True,
        help="MCP server URL (must include /mcp)"
    )

    parser.add_argument(
        "--type",
        type=str,
        default="cowork",
        choices=["cowork", "code", "codex"],
        help="Plugin type"
    )

    return parser.parse_args()


# ---------------------------
# MAIN LOGIC
# ---------------------------
async def run_generator(url, plugin_type):

    print(f"\n Starting MCP Plugin Generation ({plugin_type})")
    print(f" URL: {url}\n")

    # Dynamic output folder
    base_output = os.path.join(os.getcwd(), "Generated_Plugins")
    output_dir = os.path.join(base_output, f"{plugin_type}_plugin")

    try:
        print(" Discovering MCP tools...")

        transport = "streamable-http"
        tools = await discover_tools_streamable_http(url)

        if tools is None:
            print(" Streamable HTTP POST was not accepted; trying legacy SSE...")
            transport = "sse"
            async with legacy_sse_session(url) as session:
                tools = await discover_tools(session)

        print(f" Using {transport} transport")
        print(f" Found {len(tools)} tools")

        # Ensure output directory
        os.makedirs(output_dir, exist_ok=True)

        # Generate files
        if plugin_type == "codex":
            skills_dir = os.path.join(output_dir, "skills")
            if os.path.isdir(skills_dir):
                shutil.rmtree(skills_dir)

            server_name = create_codex_plugin_json(output_dir, url, tools)
            create_codex_mcp_config(output_dir, url, transport, server_name)
            create_codex_readme(output_dir, tools, transport, url)
            installed_dir, marketplace_path = install_codex_plugin(
                output_dir,
                server_name,
                os.getcwd(),
            )
        else:
            create_claude_plugin_json(output_dir)
            create_claude_mcp_config(output_dir, url, transport)
            create_claude_readme(output_dir, tools, transport)
            generate_skills(tools, output_dir)

        print("\n Plugin generated successfully!")
        print(f" Location: {output_dir}")
        if plugin_type == "codex":
            print(f" Codex plugin installed at: {installed_dir}")
            print(f" Codex marketplace updated at: {marketplace_path}")
            print(" Restart Codex to see the plugin in settings.")
        return True

    except TransportNegotiationError as e:
        print("\n Could not discover MCP tools:")
        print(f" {e}")
        return False
    except Exception as e:
        print("\n Error occurred:")
        traceback.print_exc()
        return False


# ---------------------------
# ENTRY POINT
# ---------------------------
if __name__ == "__main__":
    args = parse_args()

    if not args.url.endswith("/mcp"):
        print(" Warning: URL should end with /mcp")

    success = asyncio.run(run_generator(args.url, args.type))
    if not success:
        sys.exit(1)
