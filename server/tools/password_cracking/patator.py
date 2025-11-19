"""Patator multi-purpose brute-forcer"""

from typing import Dict, Any


def register_patator_tool(mcp, kali_client):
    """Register the Patator tool with the MCP server"""
    
    @mcp.tool()
    def patator_attack(module: str, target: str, username_file: str = "", password_file: str = "", additional_args: str = "") -> Dict[str, Any]:
        """
        Execute Patator for multi-purpose brute-forcing.
        
        Args:
            module: Module to use (ssh_login, ftp_login, http_fuzz, etc.)
            target: Target specification
            username_file: Path to username file
            password_file: Path to password file
            additional_args: Additional Patator arguments
            
        Returns:
            Attack results
        """
        data = {
            "module": module,
            "target": target,
            "username_file": username_file,
            "password_file": password_file,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/patator", data)

