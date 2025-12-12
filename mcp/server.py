import asyncio
import httpx
from fastmcp import FastMCP

async def setup_mcp_client():
    async with httpx.AsyncClient(base_url="http://0.0.0.0:8001") as client:
        resp = await client.get("/openapi.json")
        resp.raise_for_status()
        openapi_spec = resp.json()

        # Create FastMCP client from OpenAPI
        mcp = FastMCP.from_openapi(
            openapi_spec,
            client=client,
            name="GEMINI API"
        )
        return mcp

# Run the async setup
mcp_client = asyncio.run(setup_mcp_client())
