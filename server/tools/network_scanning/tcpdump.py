"""TCPDump packet analyzer and sniffer"""

from typing import Dict, Any


def register_tcpdump_tool(mcp, kali_client):
    """Register the TCPDump tool with the MCP server"""
    
    @mcp.tool()
    def tcpdump_capture(interface: str = "eth0", filter_expr: str = "", count: str = "100", output_file: str = "", additional_args: str = "") -> Dict[str, Any]:
        """
        Execute TCPDump for packet capture and analysis.
        
        Args:
            interface: Network interface to capture from
            filter_expr: BPF filter expression (e.g., "tcp port 80")
            count: Number of packets to capture
            output_file: Output file path for pcap
            additional_args: Additional TCPDump arguments
            
        Returns:
            Capture results
        """
        data = {
            "interface": interface,
            "filter_expr": filter_expr,
            "count": count,
            "output_file": output_file,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/tcpdump", data)

