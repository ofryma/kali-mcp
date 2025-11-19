"""Aircrack-ng WiFi security auditing suite"""

from typing import Dict, Any


def register_aircrack_tool(mcp, kali_client):
    """Register the Aircrack-ng tool with the MCP server"""
    
    @mcp.tool()
    def aircrack_attack(capture_file: str, wordlist: str = "/usr/share/wordlists/rockyou.txt", bssid: str = "", additional_args: str = "") -> Dict[str, Any]:
        """
        Execute Aircrack-ng to crack WiFi passwords.
        
        Args:
            capture_file: Path to capture file (.cap or .pcap)
            wordlist: Path to wordlist file
            bssid: Target BSSID (MAC address)
            additional_args: Additional Aircrack-ng arguments
            
        Returns:
            Cracking results
        """
        data = {
            "capture_file": capture_file,
            "wordlist": wordlist,
            "bssid": bssid,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/aircrack", data)

