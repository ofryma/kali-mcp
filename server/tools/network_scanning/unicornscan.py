"""Unicornscan advanced network reconnaissance tool"""

from typing import Dict, Any


def register_unicornscan_tool(mcp, kali_client):
    """Register the Unicornscan tool with the MCP server"""
    
    @mcp.tool()
    def unicornscan_scan(target: str, mode: str = "tcp", ports: str = "1-65535", additional_args: str = "") -> Dict[str, Any]:
        """
        Execute Unicornscan for advanced network reconnaissance.
        
        Args:
            target: The IP address or hostname to scan
            mode: Scan mode (tcp, udp)
            ports: Port range to scan
            additional_args: Additional Unicornscan arguments
            
        Returns:
            Scan results
        """
        data = {
            "target": target,
            "mode": mode,
            "ports": ports,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/unicornscan", data)

