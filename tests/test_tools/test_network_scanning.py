"""Tests for network scanning tools"""
import pytest
from unittest.mock import Mock, MagicMock


class TestNmapTool:
    """Test suite for Nmap tool"""
    
    def test_nmap_scan_basic(self, mock_kali_client):
        """Test basic nmap scan"""
        from server.tools.network_scanning.nmap import register_nmap_tool
        
        mock_mcp = Mock()
        tool_func = None
        
        def capture_tool():
            def decorator(func):
                nonlocal tool_func
                tool_func = func
                return func
            return decorator
        
        mock_mcp.tool = capture_tool
        register_nmap_tool(mock_mcp, mock_kali_client)
        
        # Call the tool function
        result = tool_func(target="127.0.0.1")
        
        # Verify kali_client was called correctly
        mock_kali_client.safe_post.assert_called_once()
        call_args = mock_kali_client.safe_post.call_args
        assert call_args[0][0] == "api/tools/nmap"
        assert call_args[0][1]["target"] == "127.0.0.1"
    
    def test_nmap_scan_with_ports(self, mock_kali_client):
        """Test nmap scan with specific ports"""
        from server.tools.network_scanning.nmap import register_nmap_tool
        
        mock_mcp = Mock()
        tool_func = None
        
        def capture_tool():
            def decorator(func):
                nonlocal tool_func
                tool_func = func
                return func
            return decorator
        
        mock_mcp.tool = capture_tool
        register_nmap_tool(mock_mcp, mock_kali_client)
        
        result = tool_func(target="127.0.0.1", ports="80,443", scan_type="-sV")
        
        call_args = mock_kali_client.safe_post.call_args
        assert call_args[0][1]["ports"] == "80,443"
        assert call_args[0][1]["scan_type"] == "-sV"


class TestMasscanTool:
    """Test suite for Masscan tool"""
    
    def test_masscan_basic(self, mock_kali_client):
        """Test basic masscan"""
        from server.tools.network_scanning.masscan import register_masscan_tool
        
        mock_mcp = Mock()
        tool_func = None
        
        def capture_tool():
            def decorator(func):
                nonlocal tool_func
                tool_func = func
                return func
            return decorator
        
        mock_mcp.tool = capture_tool
        register_masscan_tool(mock_mcp, mock_kali_client)
        
        result = tool_func(target="192.168.1.0/24")
        
        mock_kali_client.safe_post.assert_called_once()
        call_args = mock_kali_client.safe_post.call_args
        assert call_args[0][0] == "api/tools/masscan"


class TestArpingTool:
    """Test suite for Arping tool"""
    
    def test_arping_basic(self, mock_kali_client):
        """Test basic arping"""
        from server.tools.network_scanning.arping import register_arping_tool
        
        mock_mcp = Mock()
        tool_func = None
        
        def capture_tool():
            def decorator(func):
                nonlocal tool_func
                tool_func = func
                return func
            return decorator
        
        mock_mcp.tool = capture_tool
        register_arping_tool(mock_mcp, mock_kali_client)
        
        result = tool_func(target="192.168.1.1")
        
        mock_kali_client.safe_post.assert_called_once()

