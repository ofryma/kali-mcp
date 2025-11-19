"""MCP Server package for Kali Linux Tools"""

from .mcp_setup import setup_mcp_server
from .kali_client import KaliToolsClient, DEFAULT_REQUEST_TIMEOUT

__all__ = ['setup_mcp_server', 'KaliToolsClient', 'DEFAULT_REQUEST_TIMEOUT']

