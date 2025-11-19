"""Enum4linux Windows/Samba enumeration tool"""

from typing import Dict, Any


def register_enum4linux_tool(mcp, kali_client):
    """Register the Enum4linux tool with the MCP server"""
    
    @mcp.tool()
    def enum4linux_scan(target: str, additional_args: str = "-a") -> Dict[str, Any]:
        """
        Execute Enum4linux Windows/Samba enumeration tool.
        
        Args:
            target: The target IP or hostname
            additional_args: Additional enum4linux arguments
            
        Returns:
            Enumeration results
        """
        data = {
            "target": target,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/enum4linux", data)

