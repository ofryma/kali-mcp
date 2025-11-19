"""Metagoofil metadata extraction tool"""

from typing import Dict, Any


def register_metagoofil_tool(mcp, kali_client):
    """Register Metagoofil tool with the MCP server"""
    
    @mcp.tool()
    def metagoofil_scan(domain: str, file_types: str = "pdf,doc,xls,ppt", limit: str = "100", additional_args: str = "") -> Dict[str, Any]:
        """
        Execute Metagoofil for metadata extraction from documents.
        
        Args:
            domain: Target domain
            file_types: Comma-separated list of file types
            limit: Maximum number of files to download
            additional_args: Additional Metagoofil arguments
            
        Returns:
            Extracted metadata
        """
        data = {
            "domain": domain,
            "file_types": file_types,
            "limit": limit,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/metagoofil", data)

