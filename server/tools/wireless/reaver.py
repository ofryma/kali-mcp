"""Reaver WPS brute force attack tool"""

from typing import Dict, Any


def register_reaver_tool(mcp, kali_client):
    """Register the Reaver tool with the MCP server"""
    
    @mcp.tool()
    def reaver_attack(interface: str, bssid: str, channel: str = "", additional_args: str = "") -> Dict[str, Any]:
        """
        Execute Reaver WPS brute force attack.
        
        Args:
            interface: Wireless interface in monitor mode
            bssid: Target BSSID (MAC address)
            channel: WiFi channel
            additional_args: Additional Reaver arguments
            
        Returns:
            Attack results
        """
        data = {
            "interface": interface,
            "bssid": bssid,
            "channel": channel,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/reaver", data)

