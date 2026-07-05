"""
Opportunity OS - MCP Client
This module provides a client wrapper for the Model Context Protocol (MCP) server.
It handles launching the server as a subprocess, managing the connection, 
and providing a clean interface for executing tools.
"""

import asyncio
import sys
import os
from pathlib import Path
from contextlib import AsyncExitStack

# Dynamically import the official third-party 'mcp' SDK under 'mcp_official' to avoid conflicts
if 'mcp_official' not in sys.modules:
    _original_path = sys.path.copy()
    _mcp_pkg_dir = os.path.dirname(os.path.abspath(__file__))
    _parent_dir = os.path.dirname(_mcp_pkg_dir)
    sys.path = [p for p in sys.path if os.path.abspath(p) not in (_mcp_pkg_dir, _parent_dir, "", ".")]
    
    # Temporarily remove local 'mcp' package from sys.modules
    local_mcp = sys.modules.pop('mcp', None)
    
    # Load official SDK
    import mcp as official_mcp
    sys.modules['mcp_official'] = official_mcp
    
    # Restore local 'mcp' mapping
    if local_mcp:
        sys.modules['mcp'] = local_mcp
        
    sys.path = _original_path

# Import official SDK components safely from 'mcp_official'
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPClient:
    """
    An async client for managing communication with the local MCP server over stdio.
    """
    def __init__(self):
        # Resolve the server path dynamically relative to this file
        server_path = Path(__file__).parent / "server.py"
        
        # Configure connection parameter to run 'python' with the path to the server.
        # sys.executable ensures the client uses the same virtual environment as the app.
        self.server_params = StdioServerParameters(
            command=sys.executable,
            args=[str(server_path)],
            env=None
        )
        self.read = None
        self.write = None
        self.session = None
        self.exit_stack = None

    async def __aenter__(self):
        """Starts the server process and establishes the session."""
        self.exit_stack = AsyncExitStack()
        try:
            # Launch the server subprocess over stdio transport
            self.read, self.write = await self.exit_stack.enter_async_context(
                stdio_client(self.server_params)
            )
            
            # Establish the client session
            self.session = await self.exit_stack.enter_async_context(
                ClientSession(self.read, self.write)
            )
            
            # Initialize connection handshake
            await self.session.initialize()
            return self
        except Exception as e:
            # Clean up if connection fails
            await self.exit_stack.aclose()
            raise RuntimeError(f"Failed to start/connect to MCP Server: {str(e)}")

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Closes the session and stops the server process."""
        if self.exit_stack:
            await self.exit_stack.aclose()

    async def get_available_tools(self) -> list:
        """
        Retrieves the list of tools exposed by the MCP server.
        
        Returns:
            list: List of tool definitions.
        """
        if not self.session:
            raise RuntimeError("MCP session is not active.")
        
        response = await self.session.list_tools()
        return response.tools

    async def call_tool(self, tool_name: str, arguments: dict) -> str:
        """
        Invokes a tool on the MCP server and returns the result as a string.
        
        Args:
            tool_name (str): The name of the tool to execute.
            arguments (dict): The arguments to pass to the tool.
            
        Returns:
            str: The text content returned by the tool.
        """
        if not self.session:
            raise RuntimeError("MCP session is not active.")
        
        # Execute tool via the session
        result = await self.session.call_tool(tool_name, arguments)
        
        # Parse and extract text content from the response blocks
        text_content = []
        for block in result.content:
            # Handle different types of content blocks returned by the SDK
            if hasattr(block, "text"):
                text_content.append(block.text)
            elif isinstance(block, dict) and "text" in block:
                text_content.append(block["text"])
            else:
                text_content.append(str(block))
                
        return "\n".join(text_content)
