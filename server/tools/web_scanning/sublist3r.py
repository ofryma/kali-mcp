"""Sublist3r subdomain enumeration tool"""

from typing import Dict, Any


def register_sublist3r_tool(mcp, kali_client):
    """Register the Sublist3r tool with the MCP server"""
    
    @mcp.tool()
    def sublist3r_scan(domain: str, bruteforce: bool = False, ports: str = "", additional_args: str = "") -> Dict[str, Any]:
        """
        Execute Sublist3r for subdomain enumeration.
        
        Args:
            domain: The target domain
            bruteforce: Enable bruteforce mode
            ports: Comma-separated ports to scan
            additional_args: Additional Sublist3r arguments
            
        Returns:
            Enumeration results
        """
        data = {
            "domain": domain,
            "bruteforce": bruteforce,
            "ports": ports,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/sublist3r", data)

