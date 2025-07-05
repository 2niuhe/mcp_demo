# MCP Client Demo

A simplified MCP client that connects to MCP servers and demonstrates basic tool listing and execution functionality.

## Features

- Connects to MCP servers defined in the configuration file
- Lists available tools from all connected servers
- Allows interactive tool execution with parameter input
- Clean, minimal implementation for learning MCP protocol

## Setup

1. Make sure you have Python 3.8+ installed
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The client is configured using the `servers_config.json` file, which defines the MCP servers to connect to. Each server entry includes:

- `command`: The command to run the server (e.g., `python`)
- `args`: The arguments to pass to the command (e.g., `["../server/calculator.py"]`)
- `env`: Optional environment variables to set for the server

Example configuration:
```json
{
  "mcpServers": {
    "calculator": {
      "command": "python",
      "args": ["../server/calculator.py"],
      "env": {}
    }
  }
}
```

## Usage

Run the client:
```bash
python mcp_client_demo.py
```

### Available Commands

- `tools` - List all available tools from all connected servers
- `execute` - Execute a tool interactively
- `exit` - Exit the program

### Example Workflow

1. Start the client
2. Use `tools` command to see available tools
3. Use `execute` command to run a tool:
   - Select the server name
   - Enter the tool name
   - Provide required parameters
   - See the execution result

## Example Session

```
=== MCP Client Demo ===
Connecting to servers...

Commands:
  1. tools - List available tools
  2. execute - Execute a tool
  3. exit - Exit the program

Enter command: tools

=== Available Tools ===

Server: calculator
  Tool: add
    Description: Add two numbers(两个数字相加)
    Parameters:
      - a: First number (required)
      - b: Second number (required)

Enter command: execute

Enter server name: calculator
Enter tool name: add
Enter arguments:
  a (number): 5
  b (number): 3

Result: 8.0
```

## Architecture

This simplified implementation demonstrates:

- **Core MCP Protocol**: Basic client-server communication
- **Tool Discovery**: Listing available tools from servers
- **Tool Execution**: Interactive parameter input and execution
- **Clean Structure**: Minimal code for easy understanding

Perfect for learning the MCP protocol basics!
