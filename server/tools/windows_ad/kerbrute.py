"""Kerbrute Kerberos pre-auth brute-forcing"""

from typing import Dict, Any


def register_kerbrute_tool(mcp, kali_client):
    """Register the Kerbrute tool with the MCP server"""
    
    @mcp.tool()
    def kerbrute_attack(domain: str, dc_ip: str, mode: str = "userenum", wordlist: str = "", additional_args: str = "") -> Dict[str, Any]:
        """
        Execute Kerbrute for Kerberos attacks.
        
        Args:
            domain: Target domain
            dc_ip: Domain Controller IP address
            mode: Attack mode (userenum, bruteuser, bruteforce, passwordspray)
            wordlist: Path to wordlist file
            additional_args: Additional Kerbrute arguments
            
        Returns:
            Attack results
        """
        data = {
            "domain": domain,
            "dc_ip": dc_ip,
            "mode": mode,
            "wordlist": wordlist,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/kerbrute", data)

