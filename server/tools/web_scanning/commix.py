"""Commix command injection exploiter"""

from typing import Dict, Any


def register_commix_tool(mcp, kali_client):
    """Register the Commix tool with the MCP server"""
    
    @mcp.tool()
    def commix_scan(url: str, data: str = "", cookie: str = "", additional_args: str = "") -> Dict[str, Any]:
        """
        Execute Commix for command injection detection and exploitation.
        
        Args:
            url: The target URL
            data: POST data string
            cookie: Cookie string
            additional_args: Additional Commix arguments
            
        Returns:
            Scan results
        """
        data_payload = {
            "url": url,
            "data": data,
            "cookie": cookie,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/commix", data_payload)

