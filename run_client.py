#!/usr/bin/env python3
"""
MCP Client Runner Script

This script provides a simple interface to run the MCP client.
"""

import os
import sys
import subprocess

# Define client directory and script
CLIENT_DIR = os.path.join(os.path.dirname(__file__), "client")
CLIENT_SCRIPT = os.path.join(CLIENT_DIR, "mcp_client_demo.py")
CONFIG_FILE = os.path.join(CLIENT_DIR, "servers_config.json")

def run_client():
    """Run the MCP Client Demo"""
    print("Starting MCP Client Demo...")
    # Change to client directory to ensure relative paths work correctly
    os.chdir(CLIENT_DIR)
    subprocess.run([sys.executable, CLIENT_SCRIPT])

if __name__ == "__main__":
    run_client()
