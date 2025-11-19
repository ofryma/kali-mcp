"""Medusa parallel login brute-forcer"""

from typing import Dict, Any


def register_medusa_tool(mcp, kali_client):
    """Register the Medusa tool with the MCP server"""
    
    @mcp.tool()
    def medusa_attack(target: str, service: str, username: str = "", username_file: str = "", password: str = "", password_file: str = "", additional_args: str = "") -> Dict[str, Any]:
        """
        Execute Medusa for parallel login brute-forcing.
        
        Args:
            target: Target IP or hostname
            service: Service to attack (ssh, ftp, http, etc.)
            username: Single username to try
            username_file: Path to username file
            password: Single password to try
            password_file: Path to password file
            additional_args: Additional Medusa arguments
            
        Returns:
            Attack results
        """
        data = {
            "target": target,
            "service": service,
            "username": username,
            "username_file": username_file,
            "password": password,
            "password_file": password_file,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/medusa", data)

