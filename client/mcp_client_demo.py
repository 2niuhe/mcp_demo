#!/usr/bin/env python3
"""
MCP Client Demo

A simplified implementation of an MCP client based on the provided reference code.
This demo version connects to MCP servers, lists available tools, and allows execution
of tools through a simple chat interface.
"""

import asyncio
import json
import logging
import os
import shutil
from contextlib import AsyncExitStack
from typing import Any, Dict, List, Optional, Tuple

import httpx
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import OpenAI

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

class Config:
    """Simple configuration manager for the MCP client."""

    def __init__(self) -> None:
        """Initialize configuration with environment variables."""
        self.api_key = os.getenv("LLM_API_KEY")
        
    @property
    def llm_api_key(self) -> str:
        """Get the LLM API key."""
        if not self.api_key:
            raise ValueError("LLM_API_KEY not found in environment variables")
        return self.api_key

    @staticmethod
    def load_server_config(file_path: str) -> Dict[str, Any]:
        """Load server configuration from JSON file."""
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {file_path}")
            raise
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in configuration file: {file_path}")
            raise


class Tool:
    """Represents an MCP tool with its metadata."""

    def __init__(self, name: str, description: str, input_schema: Dict[str, Any]) -> None:
        self.name = name
        self.description = description
        self.input_schema = input_schema
        
    def format_for_display(self) -> str:
        """Format tool information for display."""
        args_desc = []
        if "properties" in self.input_schema:
            for param_name, param_info in self.input_schema["properties"].items():
                arg_desc = f"- {param_name}: {param_info.get('description', 'No description')}"
                if param_name in self.input_schema.get("required", []):
                    arg_desc += " (required)"
                args_desc.append(arg_desc)

        return f"""
Tool: {self.name}
Description: {self.description}
Arguments:
{chr(10).join(args_desc)}
"""


class MCPServer:
    """Manages connection to an MCP server and tool execution."""

    def __init__(self, name: str, config: Dict[str, Any]) -> None:
        self.name = name
        self.config = config
        self.session: Optional[ClientSession] = None
        self._cleanup_lock = asyncio.Lock()
        self.exit_stack = AsyncExitStack()
        self.tools: List[Tool] = []

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
            env={**os.environ, **self.config["env"]}
            if self.config.get("env")
            else None,
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

    async def get_tools(self) -> List[Tool]:
        """Get available tools from the server."""
        if not self.session:
            raise RuntimeError(f"Server {self.name} not connected")

        logger.info(f"Getting tools from {self.name} server...")
        tools_response = await self.session.list_tools()
        tools = []

        for item in tools_response:
            if isinstance(item, tuple) and item[0] == "tools":
                for tool in item[1]:
                    tools.append(Tool(tool.name, tool.description, tool.inputSchema))
        
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
        async with self._cleanup_lock:
            try:
                await self.exit_stack.aclose()
                self.session = None
                logger.info(f"Disconnected from {self.name} server")
            except Exception as e:
                logger.error(f"Error disconnecting from server {self.name}: {e}")


class LLMClient:
    """Simple client for interacting with LLM API."""
    
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        
    def get_response(self, messages: List[Dict[str, str]]) -> str:
        """Get a response from the LLM API using OpenAI SDK."""
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                temperature=0.7,
                max_tokens=4096,
                top_p=1,
                stream=False
            )
            return response.choices[0].message.content
        except Exception as e:
            error_message = f"Error getting LLM response: {str(e)}"
            logger.error(error_message)
            return f"Error: {error_message}. Please try again."


class MCPClientDemo:
    """Main class for the MCP Client Demo."""
    
    def __init__(self, config_path: str) -> None:
        self.config = Config()
        self.server_config = self.config.load_server_config(config_path)
        self.servers: Dict[str, MCPServer] = {}
        self.llm_client = None
        if self.config.api_key:
            self.llm_client = LLMClient(self.config.llm_api_key)
        
    async def setup_servers(self) -> None:
        """Set up connections to all configured MCP servers."""
        for name, srv_config in self.server_config["mcpServers"].items():
            server = MCPServer(name, srv_config)
            self.servers[name] = server
            
            try:
                await server.connect()
                await server.get_tools()
            except Exception as e:
                logger.error(f"Failed to set up server {name}: {e}")
                
    async def cleanup_servers(self) -> None:
        """Disconnect from all servers."""
        disconnect_tasks = []
        for server in self.servers.values():
            disconnect_tasks.append(asyncio.create_task(server.disconnect()))
            
        if disconnect_tasks:
            await asyncio.gather(*disconnect_tasks, return_exceptions=True)
            
    def get_all_tools(self) -> List[Tuple[str, Tool]]:
        """Get all available tools from all servers."""
        all_tools = []
        for server_name, server in self.servers.items():
            for tool in server.tools:
                all_tools.append((server_name, tool))
        return all_tools
    
    def print_available_tools(self) -> None:
        """Print all available tools."""
        all_tools = self.get_all_tools()
        
        if not all_tools:
            print("No tools available.")
            return
            
        print("\n=== Available Tools ===")
        for server_name, tool in all_tools:
            print(f"\n[Server: {server_name}]")
            print(tool.format_for_display())
            
    async def execute_tool(self, server_name: str, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a tool on a specific server."""
        if server_name not in self.servers:
            raise ValueError(f"Server {server_name} not found")
            
        server = self.servers[server_name]
        return await server.execute_tool(tool_name, arguments)
    
    async def interactive_mode(self) -> None:
        """Run the client in interactive mode."""
        print("\n=== MCP Client Demo ===")
        print("Type 'help' for available commands, 'exit' to quit")
        
        while True:
            try:
                command = input("\nCommand: ").strip()
                
                if command.lower() in ["exit", "quit"]:
                    break
                    
                if command.lower() == "help":
                    print("\nAvailable commands:")
                    print("  tools       - List all available tools")
                    print("  execute     - Execute a tool")
                    print("  chat        - Start chat mode with LLM")
                    print("  exit/quit   - Exit the program")
                    print("  help        - Show this help message")
                    
                elif command.lower() == "tools":
                    self.print_available_tools()
                    
                elif command.lower() == "execute":
                    await self._handle_execute_command()
                    
                elif command.lower() == "chat":
                    if self.llm_client:
                        await self._handle_chat_mode()
                    else:
                        print("Chat mode not available: LLM_API_KEY not set in environment")
                        
                else:
                    print(f"Unknown command: {command}")
                    print("Type 'help' for available commands")
                    
            except KeyboardInterrupt:
                print("\nExiting...")
                break
                
            except Exception as e:
                logger.error(f"Error: {e}")
                print(f"Error: {e}")
                
    async def _handle_execute_command(self) -> None:
        """Handle the execute command."""
        # List servers
        print("\nAvailable servers:")
        for i, server_name in enumerate(self.servers.keys(), 1):
            print(f"  {i}. {server_name}")
            
        # Select server
        while True:
            try:
                server_idx = int(input("\nSelect server (number): ")) - 1
                server_names = list(self.servers.keys())
                if 0 <= server_idx < len(server_names):
                    selected_server = server_names[server_idx]
                    break
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Please enter a number.")
                
        # List tools for the selected server
        server = self.servers[selected_server]
        print(f"\nTools for {selected_server}:")
        for i, tool in enumerate(server.tools, 1):
            print(f"  {i}. {tool.name} - {tool.description}")
            
        # Select tool
        while True:
            try:
                tool_idx = int(input("\nSelect tool (number): ")) - 1
                if 0 <= tool_idx < len(server.tools):
                    selected_tool = server.tools[tool_idx]
                    break
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Please enter a number.")
                
        # Get arguments
        args = {}
        if "properties" in selected_tool.input_schema:
            print(f"\nEnter arguments for {selected_tool.name}:")
            for param_name, param_info in selected_tool.input_schema["properties"].items():
                is_required = param_name in selected_tool.input_schema.get("required", [])
                param_type = param_info.get("type", "string")
                
                while True:
                    value = input(f"  {param_name} ({param_type}){' (required)' if is_required else ''}: ")
                    
                    if not value and not is_required:
                        break
                    
                    if not value and is_required:
                        print("  This parameter is required.")
                        continue
                        
                    try:
                        if param_type == "integer" or param_type == "number":
                            args[param_name] = int(value)
                        elif param_type == "boolean":
                            args[param_name] = value.lower() in ["true", "yes", "y", "1"]
                        else:
                            args[param_name] = value
                        break
                    except ValueError:
                        print(f"  Invalid {param_type}. Please try again.")
                        
        # Execute tool
        try:
            print(f"\nExecuting {selected_tool.name} on {selected_server}...")
            result = await self.execute_tool(selected_server, selected_tool.name, args)
            print("\nResult:")
            print(json.dumps(result, indent=2))
        except Exception as e:
            print(f"Error executing tool: {e}")
            
    async def _handle_chat_mode(self) -> None:
        """Handle chat mode with LLM."""
        if not self.llm_client:
            print("Chat mode not available: LLM_API_KEY not set in environment")
            return
            
        # Prepare tool descriptions for the LLM
        all_tools = self.get_all_tools()
        tools_description = "\n".join([
            f"[Server: {server_name}]\n{tool.format_for_display()}"
            for server_name, tool in all_tools
        ])
        
        system_message = (
            "You are a helpful assistant with access to these tools:\n\n"
            f"{tools_description}\n"
            "Choose the appropriate tool based on the user's question. "
            "If no tool is needed, reply directly.\n\n"
            "IMPORTANT: When you need to use a tool, you must ONLY respond with "
            "the exact JSON object format below, nothing else:\n"
            "{\n"
            '    "server": "server-name",\n'
            '    "tool": "tool-name",\n'
            '    "arguments": {\n'
            '        "argument-name": "value"\n'
            "    }\n"
            "}\n\n"
            "After receiving a tool's response:\n"
            "1. Transform the raw data into a natural, conversational response\n"
            "2. Keep responses concise but informative\n"
            "3. Focus on the most relevant information\n"
            "4. Use appropriate context from the user's question\n"
            "5. Avoid simply repeating the raw data\n\n"
            "Please use only the tools that are explicitly defined above."
        )
        
        messages = [{"role": "system", "content": system_message}]
        
        print("\n=== Chat Mode ===")
        print("Type 'exit' to return to the main menu")
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                if user_input.lower() in ["exit", "quit"]:
                    break
                    
                messages.append({"role": "user", "content": user_input})
                
                print("\nAssistant: ", end="", flush=True)
                llm_response = self.llm_client.get_response(messages)
                print(llm_response)
                
                # Try to parse as a tool call
                try:
                    tool_call = json.loads(llm_response)
                    if "server" in tool_call and "tool" in tool_call and "arguments" in tool_call:
                        server_name = tool_call["server"]
                        tool_name = tool_call["tool"]
                        arguments = tool_call["arguments"]
                        
                        print(f"\n[Executing tool {tool_name} on {server_name}...]")
                        
                        try:
                            result = await self.execute_tool(server_name, tool_name, arguments)
                            print(f"\n[Tool result: {json.dumps(result, indent=2)}]")
                            
                            # Add the tool call and result to the conversation
                            messages.append({"role": "assistant", "content": llm_response})
                            messages.append({
                                "role": "system", 
                                "content": f"Tool execution result: {json.dumps(result)}"
                            })
                            
                            # Get final response
                            print("\nAssistant: ", end="", flush=True)
                            final_response = self.llm_client.get_response(messages)
                            print(final_response)
                            
                            messages.append({"role": "assistant", "content": final_response})
                            
                        except Exception as e:
                            error_msg = f"Error executing tool: {e}"
                            print(f"\n[{error_msg}]")
                            
                            messages.append({"role": "assistant", "content": llm_response})
                            messages.append({"role": "system", "content": error_msg})
                            
                            print("\nAssistant: ", end="", flush=True)
                            error_response = self.llm_client.get_response(messages)
                            print(error_response)
                            
                            messages.append({"role": "assistant", "content": error_response})
                            
                    else:
                        messages.append({"role": "assistant", "content": llm_response})
                        
                except json.JSONDecodeError:
                    # Not a tool call, just a regular response
                    messages.append({"role": "assistant", "content": llm_response})
                    
            except KeyboardInterrupt:
                print("\nExiting chat mode...")
                break


async def main() -> None:
    """Main entry point for the MCP Client Demo."""
    config_path = "servers_config.json"
    
    client = MCPClientDemo(config_path)
    
    try:
        await client.setup_servers()
        await client.interactive_mode()
    finally:
        await client.cleanup_servers()


if __name__ == "__main__":
    asyncio.run(main())
