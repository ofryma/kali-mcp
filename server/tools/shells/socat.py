"""Socat multipurpose relay"""

from typing import Dict, Any


def register_socat_tool(mcp, kali_client):
    """Register Socat tool with the MCP server"""
    
    @mcp.tool()
    def socat_run(source: str, destination: str, additional_args: str = "") -> Dict[str, Any]:
        """
        Execute Socat for data relay operations.
        
        Args:
            source: Source specification (e.g., TCP4-LISTEN:4444)
            destination: Destination specification (e.g., TCP4:target:80)
            additional_args: Additional Socat arguments
            
        Returns:
            Execution results
        """
        data = {
            "source": source,
            "destination": destination,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/socat", data)

