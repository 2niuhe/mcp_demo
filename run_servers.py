#!/usr/bin/env python3
"""
MCP Server Runner Script

This script provides a simple interface to run any of the MCP servers
in this repository.
"""

import subprocess
import os
import sys

def print_help():
    """Print help message"""
    print("MCP Server Runner")
    print("\nAvailable commands:")
    print("  calculator      Run the Calculator MCP Server")
    print("  file_manager    Run the File Manager MCP Server")
    print("  weather_service Run the Weather Service MCP Server")
    print("  list            List all available MCP servers")
    print("  help            Show this help message")
    print("\nUsage: python run_servers.py [command]")

def calculator():
    """Run the Calculator MCP Server"""
    print("Starting Calculator MCP Server...")
    subprocess.run([sys.executable, "calculator.py"])

def file_manager():
    """Run the File Manager MCP Server"""
    print("Starting File Manager MCP Server...")
    subprocess.run([sys.executable, "file_manager.py"])

def weather_service():
    """Run the Weather Service MCP Server"""
    # Check if .env file exists
    if not os.path.exists(".env"):
        print("Warning: .env file not found. Creating from .env.example...")
        if os.path.exists(".env.example"):
            with open(".env.example", "r") as example, open(".env", "w") as env:
                env.write(example.read())
            print("Created .env file. Please edit it to add your OpenWeatherMap API key.")
        else:
            print("Error: .env.example file not found.")
            return
    
    print("Starting Weather Service MCP Server...")
    subprocess.run([sys.executable, "weather_service.py"])

def inspect():
    """Run MCP Inspector to test MCP servers"""
    print("Starting MCP Inspector...")
    subprocess.run(["mcp", "inspect"])

def list_servers():
    """List all available MCP servers"""
    servers = [
        {"name": "Calculator", "file": "calculator.py", "description": "Mathematical operations"},
        {"name": "File Manager", "file": "file_manager.py", "description": "File system operations"},
        {"name": "Weather Service", "file": "weather_service.py", "description": "Weather data from OpenWeatherMap"}
    ]
    
    print("Available MCP Servers:")
    for server in servers:
        print(f"- {server['name']} ({server['file']}): {server['description']}")

if __name__ == "__main__":
    commands = {
        "calculator": calculator,
        "file_manager": file_manager,
        "weather_service": weather_service,
        "inspect": inspect,
        "list": list_servers,
        "help": print_help
    }
    
    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        print_help()
    else:
        commands[sys.argv[1]]()
