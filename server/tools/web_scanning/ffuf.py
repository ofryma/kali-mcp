"""Ffuf fast web fuzzer"""

from typing import Dict, Any


def register_ffuf_tool(mcp, kali_client):
    """Register the Ffuf tool with the MCP server"""
    
    @mcp.tool()
    def ffuf_scan(url: str, wordlist: str = "/usr/share/wordlists/dirb/common.txt", mode: str = "dir", additional_args: str = "") -> Dict[str, Any]:
        """
        Execute Ffuf for fast web fuzzing.
        
        Args:
            url: The target URL with FUZZ placeholder
            wordlist: Path to wordlist file
            mode: Fuzzing mode (dir, vhost, param)
            additional_args: Additional Ffuf arguments
            
        Returns:
            Fuzzing results
        """
        data = {
            "url": url,
            "wordlist": wordlist,
            "mode": mode,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/ffuf", data)

