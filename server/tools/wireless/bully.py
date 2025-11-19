"""Bully WPS brute force implementation"""

from typing import Dict, Any


def register_bully_tool(mcp, kali_client):
    """Register the Bully tool with the MCP server"""
    
    @mcp.tool()
    def bully_attack(interface: str, bssid: str, channel: str = "", additional_args: str = "") -> Dict[str, Any]:
        """
        Execute Bully WPS brute force attack.
        
        Args:
            interface: Wireless interface in monitor mode
            bssid: Target BSSID (MAC address)
            channel: WiFi channel
            additional_args: Additional Bully arguments
            
        Returns:
            Attack results
        """
        data = {
            "interface": interface,
            "bssid": bssid,
            "channel": channel,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/bully", data)

