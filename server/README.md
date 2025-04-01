# MCP Server Examples

This directory contains examples of Model Context Protocol (MCP) servers implemented using the Python MCP SDK.

## Available MCP Servers

### 1. Calculator Server (`calculator.py`)

A simple calculator that provides mathematical operations as MCP tools.

**Features:**
- Basic arithmetic operations (add, subtract, multiply, divide)
- Advanced math functions (power, square root, cube root, factorial)
- Trigonometric functions (sin, cos, tan)
- Logarithmic functions

**Run the server:**
```bash
python calculator.py
```

### 2. File Manager Server (`file_manager.py`)

A file management server that provides file system operations as MCP tools.

**Features:**
- List files in a directory
- Read file contents
- Write content to files
- Create directories
- Get file information
- Search for files

**Run the server:**
```bash
python file_manager.py
```

### 3. Weather Service Server (`weather_service.py`)

A weather service that fetches data from OpenWeatherMap API.

**Features:**
- Get current weather for a city
- Get weather forecast for up to 5 days
- Get air pollution data for a location
- Get geocoding information for a city

**Setup:**
1. Copy `.env.example` to `.env` in the root directory
2. Add your OpenWeatherMap API key to the `.env` file

**Run the server:**
```bash
python weather_service.py
```

## Testing with MCP Inspector

You can test these MCP servers using the MCP Inspector tool:

1. Install MCP Inspector:
   ```bash
   pip install "mcp[cli]"
   ```

2. Run an MCP server in one terminal:
   ```bash
   python calculator.py
   ```

3. In another terminal, run MCP Inspector:
   ```bash
   mcp inspect
   ```

4. Follow the prompts to connect to your MCP server and test the available tools.
