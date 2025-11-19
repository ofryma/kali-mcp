"""XSStrike advanced XSS detection suite"""

from typing import Dict, Any


def register_xsstrike_tool(mcp, kali_client):
    """Register the XSStrike tool with the MCP server"""
    
    @mcp.tool()
    def xsstrike_scan(url: str, data: str = "", crawl: bool = False, additional_args: str = "") -> Dict[str, Any]:
        """
        Execute XSStrike for advanced XSS detection.
        
        Args:
            url: The target URL
            data: POST data string
            crawl: Enable crawling mode
            additional_args: Additional XSStrike arguments
            
        Returns:
            Scan results
        """
        data_payload = {
            "url": url,
            "data": data,
            "crawl": crawl,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/xsstrike", data_payload)

