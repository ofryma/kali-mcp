"""TShark network protocol analyzer (CLI Wireshark)"""

from typing import Dict, Any


def register_tshark_tool(mcp, kali_client):
    """Register the TShark tool with the MCP server"""
    
    @mcp.tool()
    def tshark_capture(interface: str = "eth0", filter_expr: str = "", count: str = "100", read_file: str = "", additional_args: str = "") -> Dict[str, Any]:
        """
        Execute TShark for network protocol analysis.
        
        Args:
            interface: Network interface to capture from
            filter_expr: Display filter expression
            count: Number of packets to capture
            read_file: Read from pcap file instead of live capture
            additional_args: Additional TShark arguments
            
        Returns:
            Analysis results
        """
        data = {
            "interface": interface,
            "filter_expr": filter_expr,
            "count": count,
            "read_file": read_file,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/tshark", data)

