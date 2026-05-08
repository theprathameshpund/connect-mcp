from mcp_local.transport import legacy_sse_session


async def create_session(mcp_url):
    session_context = legacy_sse_session(mcp_url)
    session = await session_context.__aenter__()

    return session, session_context
