"""Binwalk firmware analysis tool"""

from typing import Dict, Any


def register_binwalk_tool(mcp, kali_client):
    """Register Binwalk tool with the MCP server"""
    
    @mcp.tool()
    def binwalk_analyze(file_path: str, extract: bool = False, additional_args: str = "") -> Dict[str, Any]:
        """
        Execute Binwalk for firmware analysis.
        
        Args:
            file_path: Path to file to analyze
            extract: Extract discovered files
            additional_args: Additional Binwalk arguments
            
        Returns:
            Analysis results
        """
        data = {
            "file_path": file_path,
            "extract": extract,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/binwalk", data)

