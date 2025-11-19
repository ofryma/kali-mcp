"""Skipfish active web application security scanner"""

from typing import Dict, Any


def register_skipfish_tool(mcp, kali_client):
    """Register the Skipfish tool with the MCP server"""
    
    @mcp.tool()
    def skipfish_scan(url: str, output_dir: str = "/tmp/skipfish_results", wordlist: str = "", additional_args: str = "") -> Dict[str, Any]:
        """
        Execute Skipfish for active web application security scanning.
        
        Args:
            url: The target URL
            output_dir: Output directory for results
            wordlist: Path to wordlist file
            additional_args: Additional Skipfish arguments
            
        Returns:
            Scan results
        """
        data = {
            "url": url,
            "output_dir": output_dir,
            "wordlist": wordlist,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/skipfish", data)

