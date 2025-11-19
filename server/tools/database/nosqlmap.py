"""NoSQLMap NoSQL database scanner"""

from typing import Dict, Any


def register_nosqlmap_tool(mcp, kali_client):
    """Register NoSQLMap tool with the MCP server"""
    
    @mcp.tool()
    def nosqlmap_scan(url: str, method: str = "GET", data: str = "", additional_args: str = "") -> Dict[str, Any]:
        """
        Execute NoSQLMap for NoSQL injection testing.
        
        Args:
            url: Target URL
            method: HTTP method (GET, POST)
            data: POST data
            additional_args: Additional NoSQLMap arguments
            
        Returns:
            Scan results
        """
        data_payload = {
            "url": url,
            "method": method,
            "data": data,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/nosqlmap", data_payload)

