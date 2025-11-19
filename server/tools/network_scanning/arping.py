"""Arping ARP-level ping utility"""

from typing import Dict, Any


def register_arping_tool(mcp, kali_client):
    """Register the Arping tool with the MCP server"""
    
    @mcp.tool()
    def arping_scan(target: str, interface: str = "", count: str = "4", additional_args: str = "") -> Dict[str, Any]:
        """
        Execute Arping for ARP-level host discovery.
        
        Args:
            target: The target IP address
            interface: Network interface to use
            count: Number of ARP requests to send
            additional_args: Additional Arping arguments
            
        Returns:
            Scan results
        """
        data = {
            "target": target,
            "interface": interface,
            "count": count,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/arping", data)

