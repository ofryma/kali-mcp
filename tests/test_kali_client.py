"""Tests for KaliToolsClient"""
import pytest
import responses
from unittest.mock import Mock, patch
from server.kali_client import KaliToolsClient


class TestKaliToolsClient:
    """Test suite for KaliToolsClient"""
    
    def test_client_initialization(self):
        """Test client initialization"""
        client = KaliToolsClient("http://localhost:5001", timeout=60)
        assert client.server_url == "http://localhost:5001"
        assert client.timeout == 60
    
    def test_client_strips_trailing_slash(self):
        """Test that trailing slash is removed from server URL"""
        client = KaliToolsClient("http://localhost:5001/", timeout=60)
        assert client.server_url == "http://localhost:5001"
    
    @responses.activate
    def test_safe_get_success(self):
        """Test successful GET request"""
        responses.add(
            responses.GET,
            "http://localhost:5001/health",
            json={"status": "healthy"},
            status=200
        )
        
        client = KaliToolsClient("http://localhost:5001")
        result = client.safe_get("health")
        
        assert result["status"] == "healthy"
    
    @responses.activate
    def test_safe_get_with_params(self):
        """Test GET request with query parameters"""
        responses.add(
            responses.GET,
            "http://localhost:5001/api/test",
            json={"result": "success"},
            status=200
        )
        
        client = KaliToolsClient("http://localhost:5001")
        result = client.safe_get("api/test", params={"param1": "value1"})
        
        assert result["result"] == "success"
    
    @responses.activate
    def test_safe_get_error(self):
        """Test GET request error handling"""
        responses.add(
            responses.GET,
            "http://localhost:5001/health",
            json={"error": "Server error"},
            status=500
        )
        
        client = KaliToolsClient("http://localhost:5001")
        result = client.safe_get("health")
        
        assert "error" in result
        assert result["success"] is False
    
    @responses.activate
    def test_safe_post_success(self):
        """Test successful POST request"""
        responses.add(
            responses.POST,
            "http://localhost:5001/api/command",
            json={"stdout": "output", "success": True},
            status=200
        )
        
        client = KaliToolsClient("http://localhost:5001")
        result = client.safe_post("api/command", {"command": "ls"})
        
        assert result["success"] is True
        assert "stdout" in result
    
    @responses.activate
    def test_safe_post_error(self):
        """Test POST request error handling"""
        responses.add(
            responses.POST,
            "http://localhost:5001/api/command",
            json={"error": "Command failed"},
            status=400
        )
        
        client = KaliToolsClient("http://localhost:5001")
        result = client.safe_post("api/command", {"command": "invalid"})
        
        assert "error" in result
        assert result["success"] is False
    
    @responses.activate
    def test_execute_command(self):
        """Test execute_command method"""
        responses.add(
            responses.POST,
            "http://localhost:5001/api/command",
            json={"stdout": "output", "success": True},
            status=200
        )
        
        client = KaliToolsClient("http://localhost:5001")
        result = client.execute_command("echo test")
        
        assert result["success"] is True
    
    @responses.activate
    def test_check_health(self):
        """Test check_health method"""
        responses.add(
            responses.GET,
            "http://localhost:5001/health",
            json={"status": "healthy", "all_essential_tools_available": True},
            status=200
        )
        
        client = KaliToolsClient("http://localhost:5001")
        result = client.check_health()
        
        assert result["status"] == "healthy"
        assert result["all_essential_tools_available"] is True
    
    def test_safe_post_network_error(self):
        """Test POST request with network error"""
        client = KaliToolsClient("http://invalid-server:5001")
        result = client.safe_post("api/command", {"command": "test"})
        
        assert "error" in result
        assert result["success"] is False
    
    def test_safe_get_network_error(self):
        """Test GET request with network error"""
        client = KaliToolsClient("http://invalid-server:5001")
        result = client.safe_get("health")
        
        assert "error" in result
        assert result["success"] is False

