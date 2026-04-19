import asyncio
import os
import sys
import traceback
import argparse

# Fix import path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mcp.client.sse import sse_client
from mcp.client.session import ClientSession

from mcp_local.discovery import discover_tools

from generators.claude.plugin import create_plugin_json
from generators.claude.skills import generate_skills
from generators.claude.readme import create_readme
from generators.claude.mcp_config import create_mcp_config


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
        choices=["cowork", "code"],
        help="Plugin type"
    )

    return parser.parse_args()


# ---------------------------
# MAIN LOGIC
# ---------------------------
async def run_generator(url, plugin_type):

    print(f"\n Starting MCP Plugin Generation ({plugin_type})")
    print(f" URL: {url}\n")

    # ✅ Dynamic output folder
    base_output = os.path.join(os.getcwd(), "Generated_Plugins")
    output_dir = os.path.join(base_output, f"{plugin_type}_plugin")

    try:
        print(" Discovering MCP tools...")

        async with sse_client(
            url,
            headers={"ngrok-skip-browser-warning": "true"}
        ) as streams:

            async with ClientSession(*streams) as session:

                # Initialize session
                await session.initialize()

                # Discover tools
                tools = await discover_tools(session)

                print(f" Found {len(tools)} tools")

                # Ensure output directory
                os.makedirs(output_dir, exist_ok=True)

                # Generate files
                create_plugin_json(output_dir)
                create_mcp_config(output_dir, url)
                create_readme(output_dir, tools)
                generate_skills(tools, output_dir)

                print("\n Plugin generated successfully!")
                print(f" Location: {output_dir}")

    except Exception as e:
        print("\n Error occurred:")
        traceback.print_exc()


# ---------------------------
# ENTRY POINT
# ---------------------------
if __name__ == "__main__":
    args = parse_args()

    if not args.url.endswith("/mcp"):
        print(" Warning: URL should end with /mcp")

    asyncio.run(run_generator(args.url, args.type))