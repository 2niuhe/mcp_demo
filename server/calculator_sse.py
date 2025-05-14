#!/usr/bin/env python3
"""
Calculator MCP Server with SSE Transport

This server provides calculator functionality through MCP protocol using SSE transport.
"""

from mcp.server.fastmcp import FastMCP, Context
import math
import uvicorn
import os

# Instantiate an MCP server
mcp = FastMCP("Calculator MCP Server")

# DEFINE TOOLS

# Addition tool
@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers"""
    return a + b

# Subtraction tool
@mcp.tool()
def subtract(a: float, b: float) -> float:
    """Subtract two numbers"""
    return a - b

# Multiplication tool
@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers"""
    return a * b

# Division tool
@mcp.tool() 
def divide(a: float, b: float) -> float:
    """Divide two numbers"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# Factorial tool
@mcp.tool()
def factorial(a: int) -> int:
    """Calculate the factorial of a number"""
    if a < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    return math.factorial(a)

# Log tool
@mcp.tool()
def log(a: float, base: float = math.e) -> float:
    """Calculate logarithm of a number with optional base (default is natural log)"""
    if a <= 0:
        raise ValueError("Logarithm is not defined for non-positive numbers")
    if base <= 0 or base == 1:
        raise ValueError("Base must be positive and not equal to 1")
    return math.log(a, base) if base != math.e else math.log(a)

# Remainder tool
@mcp.tool()
def remainder(a: float, b: float) -> float:
    """Calculate remainder of division (modulo operation)"""
    if b == 0:
        raise ValueError("Cannot calculate remainder with divisor of zero")
    return a % b

# Sin tool
@mcp.tool()
def sin(angle: float, degrees: bool = True) -> float:
    """Calculate sine of an angle (default in degrees)"""
    if degrees:
        angle = math.radians(angle)
    return math.sin(angle)

# Cos tool
@mcp.tool()
def cos(angle: float, degrees: bool = True) -> float:
    """Calculate cosine of an angle (default in degrees)"""
    if degrees:
        angle = math.radians(angle)
    return math.cos(angle)

# Tan tool
@mcp.tool()
def tan(angle: float, degrees: bool = True) -> float:
    """Calculate tangent of an angle (default in degrees)"""
    if degrees:
        angle = math.radians(angle)
    return math.tan(angle)

# Power tool
@mcp.tool()
def power(base: float, exponent: float) -> float:
    """Calculate base raised to the power of exponent"""
    return math.pow(base, exponent)

# Square root tool
@mcp.tool()
def sqrt(a: float) -> float:
    """Calculate the square root of a number"""
    if a < 0:
        raise ValueError("Square root is not defined for negative numbers")
    return math.sqrt(a)

# DEFINE RESOURCES

# Calculator info resource
@mcp.resource("calculator://info")
def get_calculator_info() -> str:
    """Get information about the calculator"""
    return "This is a scientific calculator server that provides various mathematical operations through MCP."

# Operations list resource
@mcp.resource("calculator://operations")
def get_operations() -> str:
    """Get a list of supported operations"""
    operations = [
        "add - Addition of two numbers",
        "subtract - Subtraction of two numbers",
        "multiply - Multiplication of two numbers",
        "divide - Division of two numbers",
        "factorial - Factorial of a number",
        "log - Logarithm of a number",
        "remainder - Remainder of division",
        "sin - Sine of an angle",
        "cos - Cosine of an angle",
        "tan - Tangent of an angle",
        "power - Base raised to an exponent",
        "sqrt - Square root of a number"
    ]
    return "\n".join(operations)

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}! Welcome to the Calculator MCP Server."

# Run the server with SSE transport
if __name__ == "__main__":
    # Default to port 8000 if not specified
    port = int(os.environ.get("PORT", 8000))
    
    # Create a FastAPI app with SSE transport
    app = mcp.sse_app()
    
    print(f"Starting Calculator MCP Server with SSE transport on port {port}")
    print(f"Available at http://localhost:{port}/sse")
    
    # Run the server
    uvicorn.run(app, host="0.0.0.0", port=port)
