"""WhatWeb website fingerprinting tool"""

from typing import Dict, Any


def register_whatweb_tool(mcp, kali_client):
    """Register the WhatWeb tool with the MCP server"""
    
    @mcp.tool()
    def whatweb_scan(target: str, aggression: str = "1", additional_args: str = "") -> Dict[str, Any]:
        """
        Execute WhatWeb for website fingerprinting.
        
        Args:
            target: The target URL or IP
            aggression: Aggression level (1-4, default: 1)
            additional_args: Additional WhatWeb arguments
            
        Returns:
            Fingerprinting results
        """
        data = {
            "target": target,
            "aggression": aggression,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/whatweb", data)

