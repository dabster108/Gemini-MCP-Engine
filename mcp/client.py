import asyncio
import os
from dotenv import load_dotenv
from google import genai
from fastmcp import FastMCP, Client as MCPClient
import httpx

# Load environment variables
load_dotenv()

# Your Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

# Initialize Gemini client
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

# FastAPI URL for MCP (if needed)
FASTAPI_URL = "http://0.0.0.0:8001"

async def setup_mcp_client():
    """Fetch OpenAPI spec from FastAPI and create MCP client"""
    async with httpx.AsyncClient(base_url=FASTAPI_URL) as client:
        resp = await client.get("/openapi.json")
        resp.raise_for_status()
        openapi_spec = resp.json()

        # Create MCP client from full OpenAPI spec
        mcp = FastMCP.from_openapi(openapi_spec=openapi_spec, client=client, name="GEMINI API")
        return MCPClient(mcp)

# Initialize MCP client
mcp_client = asyncio.run(setup_mcp_client())

async def chat_loop():
    """Interactive chat loop using Gemini + MCP tools"""
    print("Chat with Gemini (type 'exit' to quit)")
    chat_history = []

    # System prompt: instructs Gemini to use MCP for calculations
    system_prompt = (
        "You are a helpful assistant. "
        "If the user asks for math or multiplication, call the MCP tool instead of solving yourself. "
        "Use the MCP session to execute the tool and return the result."
    )

    async with mcp_client as client_session:
        while True:
            user_input = input("You: ").strip()
            if user_input.lower() in ("exit", "quit"):
                print("Goodbye!")
                break
            if not user_input:
                continue

            # Append user message
            chat_history.append({"role": "user", "parts": [{"text": user_input}]})

            # Combine system prompt with chat history
            full_prompt = [{"role": "system", "parts": [{"text": system_prompt}]}] + chat_history

            try:
                # Generate response using Gemini
                response = await gemini_client.aio.models.generate_content(
                model="gemini-1.5-turbo",
                contents=full_prompt,
                config=genai.types.GenerateContentConfig(
                    temperature=0.7,
                    tools=[client_session],  # Pass MCP session as a tool
                 )
)

                # Display response
                print("Gemini:", response.text)
                chat_history.append({"role": "model", "parts": [{"text": response.text}]})

            except genai.errors.ClientError as e:
                # Handle API errors
                print(f"[ERROR] {e}")
            except Exception as e:
                print(f"[UNEXPECTED ERROR] {e}")

if __name__ == "__main__":
    asyncio.run(chat_loop())
