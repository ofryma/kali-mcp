"""Kismet wireless network detector and sniffer"""

from typing import Dict, Any


def register_kismet_tool(mcp, kali_client):
    """Register the Kismet tool with the MCP server"""
    
    @mcp.tool()
    def kismet_scan(interface: str, duration: str = "60", additional_args: str = "") -> Dict[str, Any]:
        """
        Execute Kismet wireless network detection.
        
        Args:
            interface: Wireless interface
            duration: Scan duration in seconds
            additional_args: Additional Kismet arguments
            
        Returns:
            Scan results
        """
        data = {
            "interface": interface,
            "duration": duration,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/kismet", data)

