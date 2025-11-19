"""Fcrackzip ZIP password cracker"""

from typing import Dict, Any


def register_fcrackzip_tool(mcp, kali_client):
    """Register the Fcrackzip tool with the MCP server"""
    
    @mcp.tool()
    def fcrackzip_crack(zip_file: str, wordlist: str = "", bruteforce: bool = False, charset: str = "aA1", additional_args: str = "") -> Dict[str, Any]:
        """
        Execute Fcrackzip for ZIP password cracking.
        
        Args:
            zip_file: Path to ZIP file
            wordlist: Path to wordlist file (dictionary mode)
            bruteforce: Enable brute-force mode
            charset: Character set for brute-force (a=lower, A=upper, 1=digits)
            additional_args: Additional Fcrackzip arguments
            
        Returns:
            Cracking results
        """
        data = {
            "zip_file": zip_file,
            "wordlist": wordlist,
            "bruteforce": bruteforce,
            "charset": charset,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/fcrackzip", data)

