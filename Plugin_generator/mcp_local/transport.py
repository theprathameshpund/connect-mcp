from contextlib import asynccontextmanager
import json

import httpx
from mcp.client.session import ClientSession
from mcp.client.sse import sse_client


STREAMABLE_ACCEPT = "application/json, text/event-stream"
DEFAULT_HEADERS = {
    "accept": STREAMABLE_ACCEPT,
    "content-type": "application/json",
    "ngrok-skip-browser-warning": "true",
}
FALLBACK_STATUS_CODES = {400, 404, 405}
INITIALIZE_PROTOCOL_VERSION = "2025-03-26"


class TransportNegotiationError(RuntimeError):
    pass


def _json_rpc_request(request_id, method, params=None):
    payload = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": method,
    }
    if params is not None:
        payload["params"] = params
    return payload


def _initialize_params():
    return {
        "protocolVersion": INITIALIZE_PROTOCOL_VERSION,
        "capabilities": {},
        "clientInfo": {
            "name": "connect-mcp-plugin-generator",
            "version": "0.2.0",
        },
    }


def _extract_json_rpc_payload(response):
    content_type = response.headers.get("content-type", "").lower()

    if content_type.startswith("application/json"):
        return response.json()

    if content_type.startswith("text/event-stream"):
        for line in response.text.splitlines():
            if line.startswith("data:"):
                data = line.removeprefix("data:").strip()
                if data:
                    return json.loads(data)

    raise TransportNegotiationError(
        f"Unexpected MCP response content type: {content_type or 'unknown'}"
    )


def _raise_for_json_rpc_error(payload, method):
    if isinstance(payload, dict) and payload.get("error"):
        error = payload["error"]
        message = error.get("message", error) if isinstance(error, dict) else error
        raise TransportNegotiationError(f"{method} failed: {message}")


def _tool_from_streamable(tool):
    return {
        "name": tool.get("name"),
        "description": tool.get("description", ""),
        "parameters": tool.get("inputSchema", {}),
    }


async def discover_tools_streamable_http(url):
    headers = dict(DEFAULT_HEADERS)

    async with httpx.AsyncClient(timeout=httpx.Timeout(30.0, read=300.0)) as client:
        initialize = _json_rpc_request(1, "initialize", _initialize_params())
        init_response = await client.post(url, json=initialize, headers=headers)

        if init_response.status_code in FALLBACK_STATUS_CODES:
            return None

        init_response.raise_for_status()
        init_payload = _extract_json_rpc_payload(init_response)
        _raise_for_json_rpc_error(init_payload, "initialize")

        session_id = init_response.headers.get("mcp-session-id")
        request_headers = dict(headers)
        if session_id:
            request_headers["mcp-session-id"] = session_id

        initialized = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
        }
        notify_response = await client.post(url, json=initialized, headers=request_headers)
        if notify_response.status_code not in (200, 202):
            notify_response.raise_for_status()

        tools_response = await client.post(
            url,
            json=_json_rpc_request(2, "tools/list"),
            headers=request_headers,
        )
        tools_response.raise_for_status()
        tools_payload = _extract_json_rpc_payload(tools_response)
        _raise_for_json_rpc_error(tools_payload, "tools/list")

        result = tools_payload.get("result", {}) if isinstance(tools_payload, dict) else {}
        return [_tool_from_streamable(tool) for tool in result.get("tools", [])]


@asynccontextmanager
async def legacy_sse_session(url):
    async with httpx.AsyncClient(timeout=httpx.Timeout(5.0, read=5.0)) as client:
        async with client.stream(
            "GET",
            url,
            headers={
                "accept": "text/event-stream",
                "ngrok-skip-browser-warning": "true",
            },
        ) as response:
            if response.status_code == 405:
                raise TransportNegotiationError(
                    "GET /mcp returned 405, so this server does not expose a legacy SSE stream."
                )

    try:
        async with sse_client(url, headers={"ngrok-skip-browser-warning": "true"}) as streams:
            async with ClientSession(*streams) as session:
                await session.initialize()
                yield session
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 405:
            raise TransportNegotiationError(
                "GET /mcp returned 405, so this server does not expose a legacy SSE stream."
            ) from exc
        raise
