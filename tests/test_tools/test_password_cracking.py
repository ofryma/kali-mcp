"""Tests for password cracking tools"""
import pytest
from unittest.mock import Mock


class TestHydraTool:
    """Test suite for Hydra tool"""
    
    def test_hydra_ssh_attack(self, mock_kali_client):
        """Test hydra SSH brute force"""
        from server.tools.password_cracking.hydra import register_hydra_tool
        
        mock_mcp = Mock()
        tool_func = None
        
        def capture_tool():
            def decorator(func):
                nonlocal tool_func
                tool_func = func
                return func
            return decorator
        
        mock_mcp.tool = capture_tool
        register_hydra_tool(mock_mcp, mock_kali_client)
        
        result = tool_func(
            target="127.0.0.1",
            service="ssh",
            username="admin",
            password="password123"
        )
        
        mock_kali_client.safe_post.assert_called_once()
        call_args = mock_kali_client.safe_post.call_args
        assert call_args[0][0] == "api/tools/hydra"
        assert call_args[0][1]["service"] == "ssh"


class TestJohnTool:
    """Test suite for John the Ripper tool"""
    
    def test_john_basic_crack(self, mock_kali_client):
        """Test basic john crack"""
        from server.tools.password_cracking.john import register_john_tool
        
        mock_mcp = Mock()
        tool_func = None
        
        def capture_tool():
            def decorator(func):
                nonlocal tool_func
                tool_func = func
                return func
            return decorator
        
        mock_mcp.tool = capture_tool
        register_john_tool(mock_mcp, mock_kali_client)
        
        result = tool_func(hash_file="/tmp/hashes.txt")
        
        mock_kali_client.safe_post.assert_called_once()


class TestHashcatTool:
    """Test suite for Hashcat tool"""
    
    def test_hashcat_basic_crack(self, mock_kali_client):
        """Test basic hashcat crack"""
        from server.tools.password_cracking.hashcat import register_hashcat_tool
        
        mock_mcp = Mock()
        tool_func = None
        
        def capture_tool():
            def decorator(func):
                nonlocal tool_func
                tool_func = func
                return func
            return decorator
        
        mock_mcp.tool = capture_tool
        register_hashcat_tool(mock_mcp, mock_kali_client)
        
        result = tool_func(hash_file="/tmp/hashes.txt", hash_type="0")
        
        mock_kali_client.safe_post.assert_called_once()
        call_args = mock_kali_client.safe_post.call_args
        assert call_args[0][1]["hash_type"] == "0"

