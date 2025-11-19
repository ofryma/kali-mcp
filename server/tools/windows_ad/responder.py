"""Responder LLMNR/NBT-NS/MDNS poisoner"""

from typing import Dict, Any


def register_responder_tool(mcp, kali_client):
    """Register the Responder tool with the MCP server"""
    
    @mcp.tool()
    def responder_attack(interface: str, analyze: bool = False, wpad: bool = True, additional_args: str = "") -> Dict[str, Any]:
        """
        Execute Responder for LLMNR/NBT-NS/MDNS poisoning.
        
        Args:
            interface: Network interface to use
            analyze: Analyze mode only (no poisoning)
            wpad: Enable WPAD rogue proxy server
            additional_args: Additional Responder arguments
            
        Returns:
            Attack results
        """
        data = {
            "interface": interface,
            "analyze": analyze,
            "wpad": wpad,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/responder", data)

