"""CrackMapExec network pentesting tool"""

from typing import Dict, Any


def register_crackmapexec_tool(mcp, kali_client):
    """Register the CrackMapExec tool with the MCP server"""
    
    @mcp.tool()
    def crackmapexec_scan(target: str, protocol: str = "smb", username: str = "", password: str = "", hash: str = "", additional_args: str = "") -> Dict[str, Any]:
        """
        Execute CrackMapExec for network penetration testing.
        
        Args:
            target: Target IP, CIDR, or hostname
            protocol: Protocol to use (smb, ssh, winrm, mssql, ldap)
            username: Username for authentication
            password: Password for authentication
            hash: NTLM hash for pass-the-hash
            additional_args: Additional CrackMapExec arguments
            
        Returns:
            Scan results
        """
        data = {
            "target": target,
            "protocol": protocol,
            "username": username,
            "password": password,
            "hash": hash,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/crackmapexec", data)

