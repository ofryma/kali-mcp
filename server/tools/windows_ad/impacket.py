"""Impacket collection tools"""

from typing import Dict, Any


def register_impacket_tool(mcp, kali_client):
    """Register Impacket tools with the MCP server"""
    
    @mcp.tool()
    def impacket_run(script: str, target: str, username: str = "", password: str = "", hash: str = "", additional_args: str = "") -> Dict[str, Any]:
        """
        Execute Impacket scripts for network protocol manipulation.
        
        Args:
            script: Impacket script to run (psexec, smbexec, wmiexec, secretsdump, etc.)
            target: Target specification (IP or hostname)
            username: Username for authentication
            password: Password for authentication
            hash: NTLM hash for pass-the-hash
            additional_args: Additional script arguments
            
        Returns:
            Execution results
        """
        data = {
            "script": script,
            "target": target,
            "username": username,
            "password": password,
            "hash": hash,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/impacket", data)

