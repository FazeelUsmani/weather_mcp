# test.py
import asyncio
from fastmcp import Client

async def main():
    client = Client("http://127.0.0.1:4000/mcp")   # autodetect transport
    async with client:
        result = await client.call_tool("get_weather",
                                        {"location": "Paris"})
        print(result)

asyncio.run(main())