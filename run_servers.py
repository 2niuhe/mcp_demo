#!/usr/bin/env python3
"""
MCP Server Runner Script

This script provides a simple interface to run any of the MCP servers
in this repository.
"""

import subprocess
import os
import sys

# Define server directory
SERVER_DIR = os.path.join(os.path.dirname(__file__), "server")

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
    server_path = os.path.join(SERVER_DIR, "calculator.py")
    subprocess.run([sys.executable, server_path])

def file_manager():
    """Run the File Manager MCP Server"""
    print("Starting File Manager MCP Server...")
    server_path = os.path.join(SERVER_DIR, "file_manager.py")
    subprocess.run([sys.executable, server_path])

def weather_service():
    """Run the Weather Service MCP Server"""
    # Check if .env file exists
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    env_example_path = os.path.join(os.path.dirname(__file__), ".env.example")
    
    if not os.path.exists(env_path):
        print("Warning: .env file not found. Creating from .env.example...")
        if os.path.exists(env_example_path):
            with open(env_example_path, "r") as example, open(env_path, "w") as env:
                env.write(example.read())
            print("Created .env file. Please edit it to add your OpenWeatherMap API key.")
            print("Then run this command again.")
            return
        else:
            print("Error: .env.example file not found. Cannot create .env file.")
            return

    print("Starting Weather Service MCP Server...")
    server_path = os.path.join(SERVER_DIR, "weather_service.py")
    subprocess.run([sys.executable, server_path])

def inspect():
    """Run MCP Inspector to test MCP servers"""
    print("Starting MCP Inspector...")
    subprocess.run([sys.executable, "-m", "mcp.cli", "inspect"])

def list_servers():
    """List all available MCP servers"""
    print("Available MCP Servers:")
    print("  Calculator MCP Server")
    print("    - Provides mathematical operations as MCP tools")
    print("    - Run with: python run_servers.py calculator")
    print("\n  File Manager MCP Server")
    print("    - Provides file system operations as MCP tools")
    print("    - Run with: python run_servers.py file_manager")
    print("\n  Weather Service MCP Server")
    print("    - Provides weather data from OpenWeatherMap API")
    print("    - Requires OpenWeatherMap API key in .env file")
    print("    - Run with: python run_servers.py weather_service")

if __name__ == "__main__":
    commands = {
        "calculator": calculator,
        "file_manager": file_manager,
        "weather_service": weather_service,
        "inspect": inspect,
        "list": list_servers,
        "help": print_help,
    }

    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        print_help()
    else:
        commands[sys.argv[1]]()
