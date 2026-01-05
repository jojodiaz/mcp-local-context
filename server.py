from mcp.server.fastmcp import FastMCP
import os
from pathlib import Path

# Initialize FastMCP server
mcp = FastMCP("local-repo-editor")

@mcp.tool()
def list_directory(path: str) -> str:
    """Lists files and directories in the given path."""
    try:
        p = Path(path)
        if not p.exists():
            return f"Error: Path '{path}' does not exist."
        if not p.is_dir():
            return f"Error: Path '{path}' is not a directory."
        
        items = []
        for item in p.iterdir():
            type_str = "DIR " if item.is_dir() else "FILE"
            items.append(f"{type_str:<5} {item.name}")
        
        return "\n".join(sorted(items))
    except Exception as e:
        return f"Error listing directory: {str(e)}"

@mcp.tool()
def read_file(path: str) -> str:
    """Reads the content of a file."""
    try:
        p = Path(path)
        if not p.exists():
            return f"Error: File '{path}' does not exist."
        if not p.is_file():
            return f"Error: Path '{path}' is not a file."
            
        return p.read_text(encoding='utf-8')
    except Exception as e:
        return f"Error reading file: {str(e)}"

@mcp.tool()
def write_file(path: str, content: str) -> str:
    """Writes content to a file. Overwrites if exists."""
    try:
        p = Path(path)
        p.write_text(content, encoding='utf-8')
        return f"Successfully wrote to '{path}'"
    except Exception as e:
        return f"Error writing file: {str(e)}"

@mcp.tool()
def create_directory(path: str) -> str:
    """Creates a new directory."""
    try:
        p = Path(path)
        p.mkdir(parents=True, exist_ok=True)
        return f"Successfully created directory '{path}'"
    except Exception as e:
        return f"Error creating directory: {str(e)}"

if __name__ == "__main__":
    mcp.run() # stdio by default


# TREE AND FIND