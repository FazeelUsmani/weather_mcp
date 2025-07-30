# server.py
from fastmcp import FastMCP

mcp = FastMCP("Local Weather Service")        # a label models will see

@mcp.tool()
async def get_weather(location: str) -> str:
    """Return a fake weather report (replace with real API)."""
    return f"Weather in {location}: Sunny, 72 °F"

# Optional: add resources or prompts here …

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",          # works with OpenAI / Anthropic
        host="127.0.0.1",
        port=4000,
        reload=True                           # hot‑reload while you edit
    )