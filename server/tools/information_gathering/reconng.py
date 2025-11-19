"""Recon-ng full-featured reconnaissance framework"""

from typing import Dict, Any


def register_reconng_tool(mcp, kali_client):
    """Register Recon-ng tool with the MCP server"""
    
    @mcp.tool()
    def reconng_run(workspace: str, module: str, target: str, additional_args: str = "") -> Dict[str, Any]:
        """
        Execute Recon-ng reconnaissance modules.
        
        Args:
            workspace: Workspace name
            module: Module to execute
            target: Target specification
            additional_args: Additional Recon-ng arguments
            
        Returns:
            Reconnaissance results
        """
        data = {
            "workspace": workspace,
            "module": module,
            "target": target,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/reconng", data)

