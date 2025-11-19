"""Generic command execution tool"""

from typing import Dict, Any


def register_command_tool(mcp, kali_client):
    """Register the command execution tool with the MCP server"""
    
    @mcp.tool()
    def execute_command(command: str) -> Dict[str, Any]:
        """
        Execute an arbitrary command on the Kali server.
        
        Args:
            command: The command to execute
            
        Returns:
            Command execution results
        """
        return kali_client.execute_command(command)

