"""OWASP ZAP web application security scanner"""

from typing import Dict, Any


def register_zap_tool(mcp, kali_client):
    """Register the OWASP ZAP tool with the MCP server"""
    
    @mcp.tool()
    def zap_scan(target: str, scan_type: str = "baseline", additional_args: str = "") -> Dict[str, Any]:
        """
        Execute OWASP ZAP web application security scan.
        
        Args:
            target: The target URL to scan
            scan_type: Scan type (baseline, full, api)
            additional_args: Additional ZAP arguments
            
        Returns:
            Scan results
        """
        data = {
            "target": target,
            "scan_type": scan_type,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/zap", data)

