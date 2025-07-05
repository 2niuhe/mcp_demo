# Calculator MCP Server

A simple calculator MCP server that demonstrates the Model Context Protocol (MCP) with multiple transport implementations.

## Features

- **Single Tool**: Addition operation only (for demo simplicity)
- **Three Transport Modes**: STDIO, HTTP, and SSE
- **Clean Architecture**: Single file implementation with proper error handling and logging

## Usage

### STDIO Transport (Default)

```bash
python calculator.py
```

This is the default mode that communicates through standard input/output, typically used by MCP clients.

### HTTP Transport

```bash
python calculator.py --http
```

Or with custom host and port:

```bash
python calculator.py --http --host 0.0.0.0 --port 8080
```

The server will be available at `http://localhost:8008` (or your custom host:port).

### SSE Transport (Server-Sent Events)

```bash
python calculator.py --sse
```

Or with custom host and port:

```bash
python calculator.py --sse --host 0.0.0.0 --port 8080
```

The server will be available at `http://localhost:8008/sse` (or your custom host:port).

## Available Tools

### add

Adds two numbers together.

**Parameters:**
- `a` (float): First number
- `b` (float): Second number

**Returns:**
- `float`: The sum of a and b

**Example:**
```
add(2.5, 3.7) → 6.2
```

## Testing

You can test the server using the MCP Inspector:

1. Install MCP Inspector:
   ```bash
   pip install "mcp[cli]"
   ```

2. Run the server in one terminal:
   ```bash
   python calculator.py
   ```

3. In another terminal, run MCP Inspector:
   ```bash
   mcp inspect
   ```

4. Follow the prompts to connect to your MCP server and test the addition tool.

## Architecture

This implementation demonstrates:

- **FastMCP**: Using the FastMCP library for easy MCP server creation
- **Multiple Transports**: Support for STDIO, HTTP, and SSE in a single file
- **Error Handling**: Proper exception handling and logging
- **Command Line Interface**: Argument parsing for different transport modes

Perfect for blog articles and tutorials about MCP protocol implementation!
