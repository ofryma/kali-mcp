"""Wifite automated wireless attack tool"""

from typing import Dict, Any


def register_wifite_tool(mcp, kali_client):
    """Register the Wifite tool with the MCP server"""
    
    @mcp.tool()
    def wifite_attack(interface: str = "", target_bssid: str = "", additional_args: str = "") -> Dict[str, Any]:
        """
        Execute Wifite automated wireless attacks.
        
        Args:
            interface: Wireless interface (auto-detected if not specified)
            target_bssid: Target specific BSSID
            additional_args: Additional Wifite arguments
            
        Returns:
            Attack results
        """
        data = {
            "interface": interface,
            "target_bssid": target_bssid,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/wifite", data)

