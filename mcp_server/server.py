"""
Opportunity OS - MCP Server
This module runs the Model Context Protocol (MCP) server using FastMCP.
It exposes the four search tools for the Opportunity Agent.
"""

import sys
from fastmcp import FastMCP
# 5. Direct import of the sibling 'tools' module (to avoid package import naming conflicts)
try:
    import tools
except ImportError:
    from mcp_server import tools

# Initialize FastMCP Server
mcp = FastMCP("Opportunity-OS-MCP-Server")


@mcp.tool()
def search_hackathons(domain: str) -> list:
    """
    Search for hackathons in a given domain (e.g. Technology, Mechanical, Medical, Business, Design, Law).
    
    Args:
        domain: The career or academic domain to search for hackathons.
        
    Returns:
        A list of hackathons matching the domain.
    """
    print(f"Server executing: search_hackathons for domain '{domain}'", file=sys.stderr)
    return tools.search_hackathons(domain)


@mcp.tool()
def search_internships(domain: str) -> list:
    """
    Search for internship opportunities in a given domain (e.g. Technology, Mechanical, Medical, Business, Design, Law).
    
    Args:
        domain: The career or academic domain to search for internships.
        
    Returns:
        A list of internships matching the domain.
    """
    print(f"Server executing: search_internships for domain '{domain}'", file=sys.stderr)
    return tools.search_internships(domain)


@mcp.tool()
def search_open_source(domain: str) -> list:
    """
    Search for open-source programs and projects in a given domain (e.g. Technology, Mechanical, Medical, Business, Design, Law).
    
    Args:
        domain: The career or academic domain to search for open source projects.
        
    Returns:
        A list of open source projects matching the domain.
    """
    print(f"Server executing: search_open_source for domain '{domain}'", file=sys.stderr)
    return tools.search_open_source(domain)


@mcp.tool()
def search_competitions(domain: str) -> list:
    """
    Search for competitions, challenges, and contests in a given domain (e.g. Technology, Mechanical, Medical, Business, Design, Law).
    
    Args:
        domain: The career or academic domain to search for competitions.
        
    Returns:
        A list of competitions matching the domain.
    """
    print(f"Server executing: search_competitions for domain '{domain}'", file=sys.stderr)
    return tools.search_competitions(domain)


if __name__ == "__main__":
    # Runs the MCP server (defaulting to stdio transport)
    mcp.run()
