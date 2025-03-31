# MCP Demo

This repository contains examples of Model Context Protocol (MCP) servers implemented using the Python MCP SDK.

## What is MCP?

Model Context Protocol (MCP) provides a standard, secure, real-time, and two-way communication interface for AI systems to connect with external tools, API services, and data sources.

Unlike traditional API integrations which require separate code, documentation, authentication methods, and maintenance, MCP provides a single, standardized way for AI models to interact with external systems.

## Setup

1. Make sure you have Python 3.8+ installed
2. Set up a virtual environment:
   ```bash
   # Create virtual environment
   python -m venv .venv
   
   # Activate virtual environment
   # On macOS/Linux:
   source .venv/bin/activate
   # On Windows:
   .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. For the weather service, copy `.env.example` to `.env` and add your OpenWeatherMap API key:
   ```bash
   cp .env.example .env
   # Then edit .env with your API key
   ```

## Available MCP Servers

This repository includes three example MCP servers:

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

## Integration with AI Systems

These MCP servers can be integrated with AI systems that support the MCP protocol, such as Windsurf IDE. Follow the instructions in your AI system's documentation for connecting to MCP servers.

## License

This project is provided as an example implementation of the MCP protocol.
