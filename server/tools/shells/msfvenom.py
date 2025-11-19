"""Msfvenom payload generator"""

from typing import Dict, Any


def register_msfvenom_tool(mcp, kali_client):
    """Register Msfvenom tool with the MCP server"""
    
    @mcp.tool()
    def msfvenom_generate(payload: str, lhost: str, lport: str = "4444", format: str = "elf", output_file: str = "", additional_args: str = "") -> Dict[str, Any]:
        """
        Execute Msfvenom to generate payloads.
        
        Args:
            payload: Payload type (e.g., linux/x64/shell_reverse_tcp)
            lhost: Local host IP for reverse connection
            lport: Local port for reverse connection
            format: Output format (elf, exe, raw, python, etc.)
            output_file: Output file path
            additional_args: Additional Msfvenom arguments
            
        Returns:
            Generation results
        """
        data = {
            "payload": payload,
            "lhost": lhost,
            "lport": lport,
            "format": format,
            "output_file": output_file,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/msfvenom", data)

