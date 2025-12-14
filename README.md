# Gemini MCP Engine

A powerful integration that connects Google Gemini AI with FastAPI endpoints through the Model Context Protocol (MCP). This project enables Gemini to automatically discover and use your FastAPI endpoints as tools, creating an interactive chat interface that can execute API calls.

## Features

- 🤖 **Gemini AI Integration**: Uses Google's Gemini 2.5 Flash model for intelligent conversations
- 🔌 **FastAPI Integration**: Automatically converts FastAPI endpoints to Gemini tools
- 🛠️ **MCP Support**: Includes both MCP client and server implementations
- 🔄 **Automatic Tool Discovery**: Fetches OpenAPI spec and converts endpoints to function tools
- 💬 **Interactive Chat**: Command-line interface for chatting with Gemini using your API tools

## Architecture

```
┌─────────────────┐
│   FastAPI App   │  (main.py)
│   /multiply     │
└────────┬────────┘
         │ OpenAPI Spec
         ▼
┌─────────────────┐
│   MCP Client    │  (mcp/client.py)
│  Gemini Chat    │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│   MCP Server    │  (mcp/server.py)
│  FastMCP        │
└─────────────────┘
```

## Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager
- Google Gemini API key

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Gemini-MCP-Engine
```

2. Install dependencies using uv:
```bash
uv sync
```

3. Create a `.env` file in the root directory:
```bash
GEMINI_API_KEY=your_api_key_here
```

You can get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

## Usage

### 1. Start the FastAPI Server

In one terminal, start the FastAPI server:

```bash
python main.py
```

The server will run on `http://localhost:8001` and provide:
- API endpoint: `POST /multiply` (multiplies two numbers)
- OpenAPI spec: `GET /openapi.json`

### 2. Run the Gemini Chat Client

In another terminal, start the interactive chat client:

```bash
uv run mcp/client.py
```

The client will:
- Fetch the OpenAPI spec from your FastAPI server
- Convert endpoints to Gemini tools
- Start an interactive chat session

### 3. Chat with Gemini

Example conversation:
```
Chat started! (type 'quit' to exit)

You: What is 15 multiplied by 7?
Assistant: I'll calculate that for you using the multiply tool.

[Gemini calls the /multiply endpoint with a=15, b=7]

Assistant: 15 multiplied by 7 equals 105.

You: quit
```

### 4. Run the MCP Server (Optional)

To run the MCP server using FastMCP:

```bash
uv run mcp/server.py
```

This creates an MCP server that wraps your FastAPI endpoints.

## Project Structure

```
Gemini-MCP-Engine/
├── main.py              # FastAPI application with example endpoints
├── mcp/
│   ├── client.py        # Gemini chat client with tool integration
│   └── server.py        # MCP server using FastMCP
├── pyproject.toml       # Project dependencies
├── .env                 # Environment variables (create this)
└── README.md            # This file
```

## How It Works

### FastAPI to Gemini Tools Conversion

The client automatically:
1. Fetches the OpenAPI specification from your FastAPI server
2. Parses POST endpoints and their request schemas
3. Converts them to Gemini function declarations
4. Makes them available to Gemini as tools

### Function Calling Flow

1. User sends a message to Gemini
2. Gemini analyzes the request and decides if a tool is needed
3. If needed, Gemini makes a function call
4. The client executes the API call to your FastAPI endpoint
5. The result is sent back to Gemini
6. Gemini formulates a natural language response

## Adding New Endpoints

To add new endpoints that Gemini can use:

1. Add a new endpoint to `main.py`:
```python
class AddRequest(BaseModel):
    a: float
    b: float

@app.post("/add")
def add_numbers(data: AddRequest):
    result = data.a + data.b
    return {"a": data.a, "b": data.b, "result": result}
```

2. Restart the FastAPI server
3. The client will automatically discover and include the new endpoint

## Configuration

### Environment Variables

- `GEMINI_API_KEY`: Your Google Gemini API key (required)

### Model Configuration

You can change the Gemini model in `mcp/client.py`:
```python
model="gemini-2.5-flash"  # Change to gemini-1.5-pro, etc.
```

### Server Configuration

The FastAPI server runs on `0.0.0.0:8001` by default. You can modify this in `main.py`.

## Dependencies

- **fastapi**: Web framework for building APIs
- **google-genai**: Google Gemini AI SDK
- **fastmcp**: FastMCP for MCP server implementation
- **httpx**: Async HTTP client
- **pydantic**: Data validation
- **uvicorn**: ASGI server

## Troubleshooting

### "Error: Start FastAPI server first"
- Make sure `main.py` is running on port 8001
- Check that the server is accessible at `http://localhost:8001`

### API Key Issues
- Verify your `GEMINI_API_KEY` is set in `.env`
- Check that your API key is valid and has quota available

### Connection Errors
- Ensure the FastAPI server is running before starting the client
- Check firewall settings if using a different host/port

## License

See [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- [Google Gemini](https://deepmind.google/technologies/gemini/) for the AI model
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [FastMCP](https://github.com/jlowin/fastmcp) for MCP server implementation
