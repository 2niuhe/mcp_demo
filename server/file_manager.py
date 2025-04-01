# Import necessary libraries
from mcp.server.fastmcp import FastMCP
import os
import json
from datetime import datetime
from typing import List, Dict, Optional

# Instantiate an MCP server client
mcp = FastMCP("File Manager MCP Server")

# DEFINE TOOLS

@mcp.tool()
def list_files(directory: str = ".") -> List[Dict]:
    """
    List all files in a directory
    
    Args:
        directory: The directory path to list files from (default: current directory)
        
    Returns:
        A list of dictionaries containing file information
    """
    files = []
    try:
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            stats = os.stat(item_path)
            file_info = {
                "name": item,
                "path": os.path.abspath(item_path),
                "size": stats.st_size,
                "is_directory": os.path.isdir(item_path),
                "modified": datetime.fromtimestamp(stats.st_mtime).isoformat()
            }
            files.append(file_info)
        return files
    except Exception as e:
        return [{"error": str(e)}]

@mcp.tool()
def read_file(file_path: str) -> str:
    """
    Read the contents of a file
    
    Args:
        file_path: Path to the file to read
        
    Returns:
        The contents of the file as a string
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

@mcp.tool()
def write_file(file_path: str, content: str) -> str:
    """
    Write content to a file
    
    Args:
        file_path: Path to the file to write
        content: Content to write to the file
        
    Returns:
        Success message or error
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {file_path}"
    except Exception as e:
        return f"Error writing to file: {str(e)}"

@mcp.tool()
def create_directory(directory_path: str) -> str:
    """
    Create a new directory
    
    Args:
        directory_path: Path to the directory to create
        
    Returns:
        Success message or error
    """
    try:
        os.makedirs(directory_path, exist_ok=True)
        return f"Successfully created directory {directory_path}"
    except Exception as e:
        return f"Error creating directory: {str(e)}"

@mcp.tool()
def get_file_info(file_path: str) -> Dict:
    """
    Get detailed information about a file
    
    Args:
        file_path: Path to the file
        
    Returns:
        Dictionary containing file information
    """
    try:
        stats = os.stat(file_path)
        return {
            "name": os.path.basename(file_path),
            "path": os.path.abspath(file_path),
            "size": stats.st_size,
            "is_directory": os.path.isdir(file_path),
            "created": datetime.fromtimestamp(stats.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(stats.st_mtime).isoformat(),
            "accessed": datetime.fromtimestamp(stats.st_atime).isoformat(),
            "exists": os.path.exists(file_path)
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def search_files(directory: str = ".", pattern: str = "*") -> List[str]:
    """
    Search for files matching a pattern in a directory
    
    Args:
        directory: The directory to search in (default: current directory)
        pattern: The pattern to match (supports * and ? wildcards)
        
    Returns:
        List of matching file paths
    """
    import glob
    try:
        search_path = os.path.join(directory, pattern)
        return glob.glob(search_path)
    except Exception as e:
        return [f"Error searching files: {str(e)}"]

# DEFINE RESOURCES

@mcp.resource("file://{file_path}")
def get_file_resource(file_path: str) -> str:
    """
    Get file contents as a resource
    
    Args:
        file_path: Path to the file
        
    Returns:
        The contents of the file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

# Execute and return the stdio output
if __name__ == "__main__":
    mcp.run(transport="stdio")
