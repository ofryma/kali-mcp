"""Wfuzz web application fuzzer"""

from typing import Dict, Any


def register_wfuzz_tool(mcp, kali_client):
    """Register the Wfuzz tool with the MCP server"""
    
    @mcp.tool()
    def wfuzz_scan(url: str, wordlist: str = "/usr/share/wordlists/dirb/common.txt", payload_position: str = "FUZZ", additional_args: str = "") -> Dict[str, Any]:
        """
        Execute Wfuzz for web application fuzzing.
        
        Args:
            url: The target URL with FUZZ placeholder
            wordlist: Path to wordlist file
            payload_position: Position marker in URL (default: FUZZ)
            additional_args: Additional Wfuzz arguments
            
        Returns:
            Fuzzing results
        """
        data = {
            "url": url,
            "wordlist": wordlist,
            "payload_position": payload_position,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/wfuzz", data)

