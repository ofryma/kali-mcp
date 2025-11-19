"""Netcat TCP/IP swiss army knife"""

from typing import Dict, Any


def register_netcat_tool(mcp, kali_client):
    """Register Netcat tool with the MCP server"""
    
    @mcp.tool()
    def netcat_run(mode: str, target: str = "", port: str = "4444", additional_args: str = "") -> Dict[str, Any]:
        """
        Execute Netcat for network connections.
        
        Args:
            mode: Mode (listen, connect, scan)
            target: Target IP or hostname (for connect mode)
            port: Port number
            additional_args: Additional Netcat arguments
            
        Returns:
            Execution results
        """
        data = {
            "mode": mode,
            "target": target,
            "port": port,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/netcat", data)

