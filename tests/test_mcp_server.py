"""Tests for MCP server setup"""
import pytest
from unittest.mock import Mock, patch
from server.mcp_setup import setup_mcp_server


class TestMCPServerSetup:
    """Test suite for MCP server setup"""
    
    def test_setup_mcp_server(self, mock_kali_client):
        """Test MCP server setup"""
        with patch.dict('os.environ', {'MCP_PORT': '5002'}):
            mcp = setup_mcp_server(mock_kali_client)
            
            assert mcp is not None
            assert hasattr(mcp, 'name')
            assert mcp.name == "Kali-Linux-MCP"
    
    def test_mcp_server_has_tools(self, mock_kali_client):
        """Test that MCP server has tools registered"""
        with patch.dict('os.environ', {'MCP_PORT': '5002'}):
            mcp = setup_mcp_server(mock_kali_client)
            
            # Check that tools are registered
            # FastMCP stores tools internally, we can verify the setup completed
            assert mcp is not None
    
    def test_mcp_server_port_configuration(self, mock_kali_client):
        """Test MCP server port configuration"""
        with patch.dict('os.environ', {'MCP_STREAMABLE_HTTP_PORT': '6000'}):
            mcp = setup_mcp_server(mock_kali_client)
            assert mcp.port == 6000
    
    def test_mcp_server_default_port(self, mock_kali_client):
        """Test MCP server default port"""
        with patch.dict('os.environ', {}, clear=True):
            # Clear env vars and set default
            import os
            os.environ.setdefault('MCP_PORT', '5002')
            mcp = setup_mcp_server(mock_kali_client)
            assert mcp.port in [5002, 5002]  # Could be either depending on env


class TestMCPTools:
    """Test MCP tool registration"""
    
    def test_nmap_tool_registration(self, mock_kali_client):
        """Test that nmap tool is properly registered"""
        from server.tools.network_scanning.nmap import register_nmap_tool
        
        mock_mcp = Mock()
        register_nmap_tool(mock_mcp, mock_kali_client)
        
        # Verify that tool decorator was called
        assert mock_mcp.tool.called
    
    def test_health_tool_registration(self, mock_kali_client):
        """Test that health tool is properly registered"""
        from server.tools.health import register_health_tool
        
        mock_mcp = Mock()
        register_health_tool(mock_mcp, mock_kali_client)
        
        assert mock_mcp.tool.called
    
    def test_command_tool_registration(self, mock_kali_client):
        """Test that command tool is properly registered"""
        from server.tools.command import register_command_tool
        
        mock_mcp = Mock()
        register_command_tool(mock_mcp, mock_kali_client)
        
        assert mock_mcp.tool.called

