"""Evil-WinRM Windows Remote Management shell"""

from typing import Dict, Any


def register_evil_winrm_tool(mcp, kali_client):
    """Register the Evil-WinRM tool with the MCP server"""
    
    @mcp.tool()
    def evil_winrm_connect(target: str, username: str, password: str = "", hash: str = "", additional_args: str = "") -> Dict[str, Any]:
        """
        Execute Evil-WinRM for Windows Remote Management shell.
        
        Args:
            target: Target IP or hostname
            username: Username for authentication
            password: Password for authentication
            hash: NTLM hash for pass-the-hash
            additional_args: Additional Evil-WinRM arguments
            
        Returns:
            Connection results
        """
        data = {
            "target": target,
            "username": username,
            "password": password,
            "hash": hash,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/evil_winrm", data)

