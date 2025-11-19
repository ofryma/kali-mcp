"""DNSEnum DNS enumeration tool"""

from typing import Dict, Any


def register_dnsenum_tool(mcp, kali_client):
    """Register DNSEnum tool with the MCP server"""
    
    @mcp.tool()
    def dnsenum_scan(domain: str, dns_server: str = "", additional_args: str = "") -> Dict[str, Any]:
        """
        Execute DNSEnum for DNS enumeration.
        
        Args:
            domain: Target domain
            dns_server: DNS server to use
            additional_args: Additional DNSEnum arguments
            
        Returns:
            Enumeration results
        """
        data = {
            "domain": domain,
            "dns_server": dns_server,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/dnsenum", data)

