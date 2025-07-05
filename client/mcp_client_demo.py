#!/usr/bin/env python3
"""
MCP Client Demo

A simplified MCP client that connects to MCP servers and demonstrates
basic tool listing and execution functionality.
"""

import asyncio
import json
import logging
import os
import shutil
from contextlib import AsyncExitStack
from typing import Any, Dict, List, Optional

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class MCPServer:
    """Manages connection to an MCP server and tool execution."""

    def __init__(self, name: str, config: Dict[str, Any]) -> None:
        self.name = name
        self.config = config
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.tools: List[Dict[str, Any]] = []

    async def connect(self) -> None:
        """Connect to the MCP server."""
        command = (
            shutil.which("npx")
            if self.config["command"] == "npx"
            else self.config["command"]
        )
        if command is None:
            raise ValueError(f"Invalid command for server {self.name}: {self.config['command']}")

        logger.info(f"Connecting to {self.name} server...")
        server_params = StdioServerParameters(
            command=command,
            args=self.config["args"],
            env={**os.environ, **self.config.get("env", {})}
        )
        
        try:
            stdio_transport = await self.exit_stack.enter_async_context(
                stdio_client(server_params)
            )
            read, write = stdio_transport
            session = await self.exit_stack.enter_async_context(
                ClientSession(read, write)
            )
            await session.initialize()
            self.session = session
            logger.info(f"Successfully connected to {self.name} server")
        except Exception as e:
            logger.error(f"Error connecting to server {self.name}: {e}")
            await self.disconnect()
            raise

    async def get_tools(self) -> List[Dict[str, Any]]:
        """Get available tools from the server."""
        if not self.session:
            raise RuntimeError(f"Server {self.name} not connected")

        logger.info(f"Getting tools from {self.name} server...")
        tools_response = await self.session.list_tools()
        tools = []

        for item in tools_response:
            if isinstance(item, tuple) and item[0] == "tools":
                for tool in item[1]:
                    tools.append({
                        "name": tool.name,
                        "description": tool.description,
                        "input_schema": tool.inputSchema
                    })
        
        self.tools = tools
        return tools

    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a tool on the server."""
        if not self.session:
            raise RuntimeError(f"Server {self.name} not connected")

        logger.info(f"Executing tool {tool_name} on {self.name} server...")
        try:
            result = await self.session.call_tool(tool_name, arguments)
            logger.info(f"Tool execution successful")
            return result
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {e}")
            raise

    async def disconnect(self) -> None:
        """Disconnect from the server."""
        try:
            await self.exit_stack.aclose()
            self.session = None
            logger.info(f"Disconnected from {self.name} server")
        except Exception as e:
            logger.error(f"Error disconnecting from server {self.name}: {e}")


class MCPClientDemo:
    """Simple MCP client for demonstration purposes."""

    def __init__(self, config_path: str) -> None:
        self.config_path = config_path
        self.servers: Dict[str, MCPServer] = {}
        self.load_config()

    def load_config(self) -> None:
        """Load server configuration from JSON file."""
        try:
            with open(self.config_path, "r") as f:
                config = json.load(f)
                
            for server_name, server_config in config["mcpServers"].items():
                self.servers[server_name] = MCPServer(server_name, server_config)
                
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {self.config_path}")
            raise
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in configuration file: {self.config_path}")
            raise

    async def setup_servers(self) -> None:
        """Connect to all configured servers."""
        for server in self.servers.values():
            try:
                await server.connect()
                await server.get_tools()
            except Exception as e:
                logger.error(f"Failed to setup server {server.name}: {e}")

    async def cleanup_servers(self) -> None:
        """Disconnect from all servers."""
        for server in self.servers.values():
            await server.disconnect()

    def print_available_tools(self) -> None:
        """Print all available tools from all servers."""
        print("\n=== Available Tools ===")
        for server_name, server in self.servers.items():
            print(f"\nServer: {server_name}")
            if not server.tools:
                print("  No tools available")
                continue

            print(f"  Tools:\n {json.dumps(server.tools, indent=2)}")
            print('--------------------------------')
            for tool in server.tools:
                print(f"  Tool: {tool['name']}")
                print(f"    Description: {tool['description']}")
                
                # Show parameters
                schema = tool['input_schema']
                if 'properties' in schema:
                    print("    Parameters:")
                    for param_name, param_info in schema['properties'].items():
                        required = param_name in schema.get('required', [])
                        print(f"      - {param_name}: {param_info.get('description', 'No description')} {'(required)' if required else ''}")

    async def execute_tool_interactive(self) -> None:
        """Execute a tool interactively."""
        # Show available tools
        self.print_available_tools()
        
        # Get user input
        server_name = input("\nEnter server name: ").strip()
        if server_name not in self.servers:
            print(f"Server '{server_name}' not found")
            return
            
        server = self.servers[server_name]
        if not server.tools:
            print("No tools available on this server")
            return
            
        tool_name = input("Enter tool name: ").strip()
        tool = next((t for t in server.tools if t['name'] == tool_name), None)
        if not tool:
            print(f"Tool '{tool_name}' not found")
            return
            
        # Get arguments
        arguments = {}
        schema = tool['input_schema']
        if 'properties' in schema:
            print("Enter arguments:")
            for param_name, param_info in schema['properties'].items():
                param_type = param_info.get('type', 'string')
                value = input(f"  {param_name} ({param_type}): ").strip()
                
                # Simple type conversion
                if param_type == 'number' or param_type == 'integer':
                    try:
                        arguments[param_name] = float(value) if param_type == 'number' else int(value)
                    except ValueError:
                        print(f"Invalid {param_type} value: {value}")
                        return
                else:
                    arguments[param_name] = value
        
        # Execute the tool
        try:
            result = await server.execute_tool(tool_name, arguments)
            print(f"\nResult: {result}")
        except Exception as e:
            print(f"Error executing tool: {e}")

    async def run_interactive(self) -> None:
        """Run the interactive client."""
        print("=== MCP Client Demo ===")
        print("Connecting to servers...")
        
        await self.setup_servers()
        
        try:
            while True:
                print("\nCommands:")
                print("  1. tools - List available tools")
                print("  2. execute - Execute a tool")
                print("  3. exit - Exit the program")
                
                command = input("\nEnter command: ").strip().lower()
                
                if command in ['exit', 'quit']:
                    break
                elif command == 'tools':
                    self.print_available_tools()
                elif command == 'execute':
                    await self.execute_tool_interactive()
                else:
                    print("Unknown command. Please try again.")
                    
        finally:
            await self.cleanup_servers()


async def main() -> None:
    """Main entry point."""
    config_path = "servers_config.json"
    
    try:
        client = MCPClientDemo(config_path)
        await client.run_interactive()
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        logger.error(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
