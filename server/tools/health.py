"""Server health check tool"""

from typing import Dict, Any


def register_health_tool(mcp, kali_client):
    """Register the server health tool with the MCP server"""
    
    @mcp.tool()
    def server_health() -> Dict[str, Any]:
        """
        Check the health status of the Kali API server.
        
        Returns:
            Server health information
        """
        return kali_client.check_health()

