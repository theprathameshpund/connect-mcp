from mcp.client.sse import sse_client
from mcp.client.session import ClientSession


async def create_session(mcp_url):
    streams = await sse_client(mcp_url).__aenter__()
    session = await ClientSession(*streams).__aenter__()

    await session.initialize()

    return session, streams