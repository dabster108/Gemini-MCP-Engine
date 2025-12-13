import asyncio
import httpx
from fastmcp import FastMCP

FASTAPI_URL = "http://0.0.0.0:8001"

async def main():
    """Fetch OpenAPI spec from FastAPI and create MCP server from it"""
    async with httpx.AsyncClient(base_url=FASTAPI_URL) as client:
        try:
            resp = await client.get("/openapi.json")
            resp.raise_for_status()
            openapi_spec = resp.json()
            
            # Create MCP server from OpenAPI spec - tools are created automatically
            mcp = FastMCP.from_openapi(
                openapi_spec=openapi_spec,
                client=client,
                name="GEMINI API"
            )
            
            # Run the MCP server
            await mcp.run_async()
            
        except Exception as e:
            print(f"Failed to connect to FastAPI server at {FASTAPI_URL}: {e}")
            print("Make sure the FastAPI server is running (python main.py).")

if __name__ == "__main__":
    asyncio.run(main())
