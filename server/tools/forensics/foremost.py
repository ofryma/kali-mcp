"""Foremost file recovery tool"""

from typing import Dict, Any


def register_foremost_tool(mcp, kali_client):
    """Register Foremost tool with the MCP server"""
    
    @mcp.tool()
    def foremost_recover(file_path: str, output_dir: str = "/tmp/foremost_output", file_types: str = "", additional_args: str = "") -> Dict[str, Any]:
        """
        Execute Foremost for file recovery.
        
        Args:
            file_path: Path to disk image or file
            output_dir: Output directory for recovered files
            file_types: File types to recover (e.g., jpg,png,pdf)
            additional_args: Additional Foremost arguments
            
        Returns:
            Recovery results
        """
        data = {
            "file_path": file_path,
            "output_dir": output_dir,
            "file_types": file_types,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/foremost", data)

