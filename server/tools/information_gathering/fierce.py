"""Fierce DNS reconnaissance tool"""

from typing import Dict, Any


def register_fierce_tool(mcp, kali_client):
    """Register Fierce tool with the MCP server"""
    
    @mcp.tool()
    def fierce_scan(domain: str, dns_server: str = "", additional_args: str = "") -> Dict[str, Any]:
        """
        Execute Fierce for DNS reconnaissance.
        
        Args:
            domain: Target domain
            dns_server: DNS server to query
            additional_args: Additional Fierce arguments
            
        Returns:
            Reconnaissance results
        """
        data = {
            "domain": domain,
            "dns_server": dns_server,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/fierce", data)

