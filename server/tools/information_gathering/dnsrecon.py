"""DNSRecon DNS enumeration script"""

from typing import Dict, Any


def register_dnsrecon_tool(mcp, kali_client):
    """Register DNSRecon tool with the MCP server"""
    
    @mcp.tool()
    def dnsrecon_scan(domain: str, scan_type: str = "std", additional_args: str = "") -> Dict[str, Any]:
        """
        Execute DNSRecon for DNS enumeration.
        
        Args:
            domain: Target domain
            scan_type: Scan type (std, axfr, bing, yand, crt, srv, etc.)
            additional_args: Additional DNSRecon arguments
            
        Returns:
            Enumeration results
        """
        data = {
            "domain": domain,
            "scan_type": scan_type,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/dnsrecon", data)

