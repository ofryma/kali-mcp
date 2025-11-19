"""Amass in-depth DNS enumeration tool"""

from typing import Dict, Any


def register_amass_tool(mcp, kali_client):
    """Register the Amass tool with the MCP server"""
    
    @mcp.tool()
    def amass_scan(domain: str, mode: str = "enum", passive: bool = False, additional_args: str = "") -> Dict[str, Any]:
        """
        Execute Amass for in-depth DNS enumeration.
        
        Args:
            domain: The target domain
            mode: Scan mode (enum, intel, track, db)
            passive: Use passive mode only
            additional_args: Additional Amass arguments
            
        Returns:
            Enumeration results
        """
        data = {
            "domain": domain,
            "mode": mode,
            "passive": passive,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/amass", data)

