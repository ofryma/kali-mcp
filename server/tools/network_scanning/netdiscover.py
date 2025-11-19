"""Netdiscover ARP reconnaissance tool"""

from typing import Dict, Any


def register_netdiscover_tool(mcp, kali_client):
    """Register the Netdiscover tool with the MCP server"""
    
    @mcp.tool()
    def netdiscover_scan(range: str = "", interface: str = "", passive_mode: bool = False, additional_args: str = "") -> Dict[str, Any]:
        """
        Execute Netdiscover for network reconnaissance.
        
        Args:
            range: IP range to scan (e.g., 192.168.1.0/24)
            interface: Network interface to use
            passive_mode: Use passive mode (listening only)
            additional_args: Additional Netdiscover arguments
            
        Returns:
            Scan results
        """
        data = {
            "range": range,
            "interface": interface,
            "passive_mode": passive_mode,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/netdiscover", data)

