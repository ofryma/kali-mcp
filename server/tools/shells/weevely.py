"""Weevely weaponized web shell"""

from typing import Dict, Any


def register_weevely_tool(mcp, kali_client):
    """Register Weevely tool with the MCP server"""
    
    @mcp.tool()
    def weevely_run(mode: str, url: str = "", password: str = "", output_file: str = "", additional_args: str = "") -> Dict[str, Any]:
        """
        Execute Weevely web shell operations.
        
        Args:
            mode: Mode (generate or connect)
            url: Target URL (for connect mode)
            password: Shell password
            output_file: Output file for generated shell
            additional_args: Additional Weevely arguments
            
        Returns:
            Execution results
        """
        data = {
            "mode": mode,
            "url": url,
            "password": password,
            "output_file": output_file,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/weevely", data)

