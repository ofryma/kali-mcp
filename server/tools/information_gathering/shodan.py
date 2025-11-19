"""Shodan CLI search engine for Internet-connected devices"""

from typing import Dict, Any


def register_shodan_tool(mcp, kali_client):
    """Register Shodan CLI tool with the MCP server"""
    
    @mcp.tool()
    def shodan_search(query: str, limit: str = "100", additional_args: str = "") -> Dict[str, Any]:
        """
        Execute Shodan search for Internet-connected devices.
        
        Args:
            query: Shodan search query
            limit: Maximum number of results
            additional_args: Additional Shodan arguments
            
        Returns:
            Search results
        """
        data = {
            "query": query,
            "limit": limit,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/shodan", data)

