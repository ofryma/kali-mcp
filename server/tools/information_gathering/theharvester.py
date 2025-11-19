"""TheHarvester email, subdomain and people names harvester"""

from typing import Dict, Any


def register_theharvester_tool(mcp, kali_client):
    """Register TheHarvester tool with the MCP server"""
    
    @mcp.tool()
    def theharvester_scan(domain: str, sources: str = "all", limit: str = "500", additional_args: str = "") -> Dict[str, Any]:
        """
        Execute TheHarvester for OSINT gathering.
        
        Args:
            domain: Target domain
            sources: Data sources (all, google, bing, linkedin, etc.)
            limit: Results limit per source
            additional_args: Additional TheHarvester arguments
            
        Returns:
            Gathered information
        """
        data = {
            "domain": domain,
            "sources": sources,
            "limit": limit,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/theharvester", data)

