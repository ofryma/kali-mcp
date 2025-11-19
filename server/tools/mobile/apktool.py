"""APKTool Android APK reverse engineering"""

from typing import Dict, Any


def register_apktool_tool(mcp, kali_client):
    """Register APKTool with the MCP server"""
    
    @mcp.tool()
    def apktool_run(mode: str, apk_path: str, output_dir: str = "", additional_args: str = "") -> Dict[str, Any]:
        """
        Execute APKTool for Android APK analysis.
        
        Args:
            mode: Mode (decode, build)
            apk_path: Path to APK file
            output_dir: Output directory
            additional_args: Additional APKTool arguments
            
        Returns:
            Execution results
        """
        data = {
            "mode": mode,
            "apk_path": apk_path,
            "output_dir": output_dir,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/apktool", data)

