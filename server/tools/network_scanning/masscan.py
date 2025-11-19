"""Masscan ultra-fast port scanner tool"""

from typing import Dict, Any


def register_masscan_tool(mcp, kali_client):
    """Register the Masscan scanning tool with the MCP server"""
    
    @mcp.tool()
    def masscan_scan(target: str, ports: str = "0-65535", rate: str = "1000", additional_args: str = "") -> Dict[str, Any]:
        """
        Execute a Masscan port scan against a target.
        
        Args:
            target: The IP address, CIDR range, or hostname to scan
            ports: Port range to scan (default: 0-65535)
            rate: Packets per second (default: 1000)
            additional_args: Additional Masscan arguments
            
        Returns:
            Scan results
        """
        data = {
            "target": target,
            "ports": ports,
            "rate": rate,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/masscan", data)

