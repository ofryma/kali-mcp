"""Integration tests for the complete MCP server"""
import pytest
from unittest.mock import patch, Mock
import responses


@pytest.mark.integration
class TestEndToEndFlow:
    """End-to-end integration tests"""
    
    @responses.activate
    def test_health_check_flow(self):
        """Test complete health check flow"""
        from server.kali_client import KaliToolsClient
        
        # Mock the API server response
        responses.add(
            responses.GET,
            "http://localhost:5001/health",
            json={
                "status": "healthy",
                "message": "Server is running",
                "tools_status": {"nmap": True},
                "all_essential_tools_available": True
            },
            status=200
        )
        
        client = KaliToolsClient("http://localhost:5001")
        result = client.check_health()
        
        assert result["status"] == "healthy"
        assert result["all_essential_tools_available"] is True
    
    @responses.activate
    def test_nmap_scan_flow(self):
        """Test complete nmap scan flow"""
        from server.kali_client import KaliToolsClient
        
        # Mock the API server response
        responses.add(
            responses.POST,
            "http://localhost:5001/api/tools/nmap",
            json={
                "stdout": "Nmap scan report for 127.0.0.1\nPORT STATE SERVICE\n22/tcp open ssh",
                "stderr": "",
                "return_code": 0,
                "success": True,
                "timed_out": False,
                "partial_results": False
            },
            status=200
        )
        
        client = KaliToolsClient("http://localhost:5001")
        result = client.safe_post("api/tools/nmap", {
            "target": "127.0.0.1",
            "scan_type": "-sV"
        })
        
        assert result["success"] is True
        assert "Nmap scan report" in result["stdout"]
    
    @responses.activate
    def test_command_execution_flow(self):
        """Test complete command execution flow"""
        from server.kali_client import KaliToolsClient
        
        responses.add(
            responses.POST,
            "http://localhost:5001/api/command",
            json={
                "stdout": "test output",
                "stderr": "",
                "return_code": 0,
                "success": True,
                "timed_out": False,
                "partial_results": False
            },
            status=200
        )
        
        client = KaliToolsClient("http://localhost:5001")
        result = client.execute_command("echo test")
        
        assert result["success"] is True
        assert result["stdout"] == "test output"


@pytest.mark.integration
@pytest.mark.network
class TestRealServerInteraction:
    """Tests that require a running server (skip by default)"""
    
    @pytest.mark.skip(reason="Requires running Kali server")
    def test_real_health_check(self):
        """Test health check against real server"""
        from server.kali_client import KaliToolsClient
        
        client = KaliToolsClient("http://localhost:5001", timeout=5)
        result = client.check_health()
        
        assert "status" in result
    
    @pytest.mark.skip(reason="Requires running Kali server")
    def test_real_command_execution(self):
        """Test command execution against real server"""
        from server.kali_client import KaliToolsClient
        
        client = KaliToolsClient("http://localhost:5001", timeout=5)
        result = client.execute_command("echo test")
        
        assert "stdout" in result

