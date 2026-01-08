from mcp.server.fastmcp import FastMCP
import os
from pathlib import Path
import subprocess as sp

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
    
# Git related tools

@mcp.tool()
def git_status(path: str) -> str:
    try: 
        return sp.run(
            f"git -C {path} status",
            shell=True,
            capture_output=True,
            text=True
        ).stdout.strip()
    except Exception as e:
        return str(e)
    
@mcp.tool()
def git_get_HEAD(path: str) -> str:
    try:
        return sp.run(
            f"git -C {path} rev-parse HEAD",
            capture_output=True,
            text=True
        ).stdout.strip()
    except Exception as e:
        return str(e)
    
@mcp.tool()
def git_check_if_repo(path: str) -> bool:
    '''Checks if the provided path leads to a git repository.'''
    try:
        # TODO: Replace with test -d statement and return a string to be more MCP friendly.
        sp.run(
            f"git -C {path} rev-parse",
            check=True,
            capture_output=True
        )
        return True
    except Exception:
        return False
    

    

if __name__ == "__main__":
    mcp.run() # stdio by default


'''Add FIND command functionality for posix compliance and tree to allow
    the MCP client to generate prettier looking directory graphs.'''