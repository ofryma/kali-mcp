"""Mimikatz Windows credential extraction"""

from typing import Dict, Any


def register_mimikatz_tool(mcp, kali_client):
    """Register the Mimikatz tool with the MCP server"""
    
    @mcp.tool()
    def mimikatz_run(command: str, target: str = "", additional_args: str = "") -> Dict[str, Any]:
        """
        Execute Mimikatz commands for credential extraction.
        
        Args:
            command: Mimikatz command to execute
            target: Target system (if running remotely)
            additional_args: Additional Mimikatz arguments
            
        Returns:
            Execution results
        """
        data = {
            "command": command,
            "target": target,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/mimikatz", data)

