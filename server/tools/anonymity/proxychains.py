"""ProxyChains redirect connections through proxy servers"""

from typing import Dict, Any


def register_proxychains_tool(mcp, kali_client):
    """Register ProxyChains tool with the MCP server"""
    
    @mcp.tool()
    def proxychains_run(command: str, config_file: str = "", additional_args: str = "") -> Dict[str, Any]:
        """
        Execute command through ProxyChains.
        
        Args:
            command: Command to execute through proxy chain
            config_file: Path to ProxyChains config file
            additional_args: Additional ProxyChains arguments
            
        Returns:
            Execution results
        """
        data = {
            "command": command,
            "config_file": config_file,
            "additional_args": additional_args
        }
        return kali_client.safe_post("api/tools/proxychains", data)

