"""SpiderFoot OSINT automation tool"""

from typing import Dict, Any


def register_spiderfoot_tool(mcp, kali_client):
    """Register SpiderFoot tool with the MCP server"""
    
    @mcp.tool()
    def spiderfoot_scan(target: str, modules: str = "all", additional_args: str = "") -> Dict[str, Any]:
        """
        Execute SpiderFoot OSINT automation scan.
        
        Args:
            target: Target (domain, IP, email, etc.)
            modules: Modules to use (all or comma-separated list)
            additional_args: Additional SpiderFoot arguments
            
        Returns:
            Scan results
        """
        data = {
            "target": target,
            "modules": modules,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/spiderfoot", data)

