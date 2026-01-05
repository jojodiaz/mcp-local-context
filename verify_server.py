import asyncio
import os
import sys

# Add the virtual environment site-packages to python path
sys.path.append(os.path.abspath("."))

from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.session import ClientSession
from mcp.types import ClientRequest, CallToolRequest, Tool

server_script = "/Users/grendel/repos/mcp_test/server.py"
python_executable = "/Users/grendel/repos/mcp_test/.venv/bin/python"

async def run():
    print(f"Connecting to server at {server_script}...")
    
    server_params = StdioServerParameters(
        command=python_executable,
        args=[server_script],
        env=os.environ.copy()
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            print("Connected! Initializing...")
            await session.initialize()
            
            print("Listing tools...")
            tools = await session.list_tools()
            print(f"Found {len(tools.tools)} tools")
            for t in tools.tools:
                print(f"- {t.name}: {t.description}")
            
            # Test list_directory
            print("\n--- Testing list_directory ---")
            cwd = os.getcwd()
            print(f"Listing current directory: {cwd}")
            result = await session.call_tool("list_directory", arguments={"path": cwd})
            print_tool_result(result)

            # Test write_file
            print("\n--- Testing write_file ---")
            test_file = os.path.join(cwd, "test_mcp_file.txt")
            print(f"Writing to file: {test_file}")
            result = await session.call_tool("write_file", arguments={"path": test_file, "content": "Hello from MCP Client!"})
            print_tool_result(result)

            # Test read_file
            print("\n--- Testing read_file ---")
            print(f"Reading file: {test_file}")
            result = await session.call_tool("read_file", arguments={"path": test_file})
            print_tool_result(result)

            # Cleanup
            if os.path.exists(test_file):
                os.remove(test_file)
                print(f"\nCleaned up {test_file}")

def print_tool_result(result):
    content = ""
    if hasattr(result, 'content'):
        for item in result.content:
            if hasattr(item, 'text'):
                content += item.text
    print("Result:")
    print(content if content else result)

if __name__ == "__main__":
    try:
        asyncio.run(run())
    except Exception as e:
        print(f"Failed to run client: {e}")
