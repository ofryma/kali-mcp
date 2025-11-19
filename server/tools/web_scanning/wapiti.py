"""Wapiti web application vulnerability scanner"""

from typing import Dict, Any


def register_wapiti_tool(mcp, kali_client):
    """Register the Wapiti tool with the MCP server"""
    
    @mcp.tool()
    def wapiti_scan(url: str, scope: str = "page", modules: str = "", additional_args: str = "") -> Dict[str, Any]:
        """
        Execute Wapiti for web application vulnerability scanning.
        
        Args:
            url: The target URL to scan
            scope: Scan scope (page, folder, domain, punk)
            modules: Comma-separated list of modules to use
            additional_args: Additional Wapiti arguments
            
        Returns:
            Scan results
        """
        data = {
            "url": url,
            "scope": scope,
            "modules": modules,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/wapiti", data)

