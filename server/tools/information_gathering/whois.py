"""Whois domain registration information lookup"""

from typing import Dict, Any


def register_whois_tool(mcp, kali_client):
    """Register Whois tool with the MCP server"""
    
    @mcp.tool()
    def whois_lookup(target: str, additional_args: str = "") -> Dict[str, Any]:
        """
        Execute Whois lookup for domain registration information.
        
        Args:
            target: Domain or IP address
            additional_args: Additional Whois arguments
            
        Returns:
            Registration information
        """
        data = {
            "target": target,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/whois", data)

