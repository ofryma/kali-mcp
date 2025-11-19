"""Hping3 packet crafting and analysis tool"""

from typing import Dict, Any


def register_hping3_tool(mcp, kali_client):
    """Register the Hping3 tool with the MCP server"""
    
    @mcp.tool()
    def hping3_scan(target: str, mode: str = "syn", port: str = "80", count: str = "3", additional_args: str = "") -> Dict[str, Any]:
        """
        Execute Hping3 for packet crafting and network analysis.
        
        Args:
            target: The target IP address or hostname
            mode: Packet mode (syn, udp, icmp, raw)
            port: Target port
            count: Number of packets to send
            additional_args: Additional Hping3 arguments
            
        Returns:
            Scan results
        """
        data = {
            "target": target,
            "mode": mode,
            "port": port,
            "count": count,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/hping3", data)

