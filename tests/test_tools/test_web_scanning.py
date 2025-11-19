"""Tests for web scanning tools"""
import pytest
from unittest.mock import Mock


class TestGobusterTool:
    """Test suite for Gobuster tool"""
    
    def test_gobuster_dir_scan(self, mock_kali_client):
        """Test gobuster directory scan"""
        from server.tools.web_scanning.gobuster import register_gobuster_tool
        
        mock_mcp = Mock()
        tool_func = None
        
        def capture_tool():
            def decorator(func):
                nonlocal tool_func
                tool_func = func
                return func
            return decorator
        
        mock_mcp.tool = capture_tool
        register_gobuster_tool(mock_mcp, mock_kali_client)
        
        result = tool_func(url="http://example.com", mode="dir")
        
        mock_kali_client.safe_post.assert_called_once()
        call_args = mock_kali_client.safe_post.call_args
        assert call_args[0][0] == "api/tools/gobuster"
        assert call_args[0][1]["url"] == "http://example.com"
        assert call_args[0][1]["mode"] == "dir"


class TestNiktoTool:
    """Test suite for Nikto tool"""
    
    def test_nikto_basic_scan(self, mock_kali_client):
        """Test basic nikto scan"""
        from server.tools.web_scanning.nikto import register_nikto_tool
        
        mock_mcp = Mock()
        tool_func = None
        
        def capture_tool():
            def decorator(func):
                nonlocal tool_func
                tool_func = func
                return func
            return decorator
        
        mock_mcp.tool = capture_tool
        register_nikto_tool(mock_mcp, mock_kali_client)
        
        result = tool_func(target="http://example.com")
        
        mock_kali_client.safe_post.assert_called_once()


class TestSqlmapTool:
    """Test suite for SQLmap tool"""
    
    def test_sqlmap_basic(self, mock_kali_client):
        """Test basic sqlmap scan"""
        from server.tools.web_scanning.sqlmap import register_sqlmap_tool
        
        mock_mcp = Mock()
        tool_func = None
        
        def capture_tool():
            def decorator(func):
                nonlocal tool_func
                tool_func = func
                return func
            return decorator
        
        mock_mcp.tool = capture_tool
        register_sqlmap_tool(mock_mcp, mock_kali_client)
        
        result = tool_func(url="http://example.com/page?id=1")
        
        mock_kali_client.safe_post.assert_called_once()
        call_args = mock_kali_client.safe_post.call_args
        assert call_args[0][1]["url"] == "http://example.com/page?id=1"

