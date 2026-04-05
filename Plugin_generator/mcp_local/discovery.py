async def discover_tools(session):

    tools_response = await session.list_tools()

    tools = []

    for tool in tools_response.tools:
        tools.append({
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.inputSchema
        })

    return tools