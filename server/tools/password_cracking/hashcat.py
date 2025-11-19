"""Hashcat advanced password recovery tool"""

from typing import Dict, Any


def register_hashcat_tool(mcp, kali_client):
    """Register the Hashcat tool with the MCP server"""
    
    @mcp.tool()
    def hashcat_crack(hash_file: str, wordlist: str = "/usr/share/wordlists/rockyou.txt", hash_type: str = "0", attack_mode: str = "0", additional_args: str = "") -> Dict[str, Any]:
        """
        Execute Hashcat for password recovery.
        
        Args:
            hash_file: Path to file containing hashes
            wordlist: Path to wordlist file
            hash_type: Hash type number (e.g., 0=MD5, 1000=NTLM, 1800=sha512crypt)
            attack_mode: Attack mode (0=straight, 1=combination, 3=brute-force)
            additional_args: Additional Hashcat arguments
            
        Returns:
            Cracking results
        """
        data = {
            "hash_file": hash_file,
            "wordlist": wordlist,
            "hash_type": hash_type,
            "attack_mode": attack_mode,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/hashcat", data)

