# MCP Client Demo

A simplified implementation of an MCP client that connects to MCP servers, lists available tools, and allows execution of tools through a simple chat interface.

## Features

- Connects to multiple MCP servers defined in the configuration file
- Lists available tools from all connected servers
- Allows you to execute tools interactively
- Provides a chat mode that uses an LLM to interpret requests and execute tools

## Setup

1. Make sure you have Python 3.8+ installed
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and add your API keys:
   ```bash
   cp .env.example .env
   # Then edit .env with your actual API keys
   ```

## Configuration

The client is configured using the `servers_config.json` file, which defines the MCP servers to connect to. Each server entry includes:

- `command`: The command to run the server (e.g., `python`)
- `args`: The arguments to pass to the command (e.g., `["calculator.py"]`)
- `env`: Optional environment variables to set for the server

Example configuration:
```json
{
  "mcpServers": {
    "calculator": {
      "command": "python",
      "args": ["calculator.py"],
      "env": {}
    },
    "file_manager": {
      "command": "python",
      "args": ["file_manager.py"],
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

- `tools`: List all available tools from all connected servers
- `execute`: Execute a tool interactively
- `chat`: Start chat mode with LLM (requires API key)
- `help`: Show available commands
- `exit`/`quit`: Exit the program

### Chat Mode

The chat mode uses the DeepSeek model to interpret your requests and execute appropriate tools. When the LLM determines a tool should be used, it will format its response as a JSON object with the server, tool, and arguments. The client will then execute the tool and send the result back to the LLM for a final response.

## Environment Variables

- `OPENWEATHER_API_KEY`: API key for the OpenWeatherMap service (used by the weather_service MCP server)
- `LLM_API_KEY`: API key for the DeepSeek LLM service (used by the chat mode)

## Adding New MCP Servers

To add a new MCP server:

1. Add the server configuration to `servers_config.json`
2. Restart the client

## Troubleshooting

- If you encounter connection issues, make sure the MCP servers are running
- If the chat mode doesn't work, check your LLM API key in the `.env` file
- For other issues, check the logs for error messages
