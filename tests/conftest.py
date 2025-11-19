"""Pytest configuration and fixtures"""
import pytest
import sys
import os
from unittest.mock import Mock, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server.kali_client import KaliToolsClient


@pytest.fixture
def mock_kali_client():
    """Create a mock KaliToolsClient"""
    client = Mock(spec=KaliToolsClient)
    client.server_url = "http://localhost:5001"
    client.timeout = 300
    
    # Default successful response
    client.safe_post.return_value = {
        "stdout": "Mock output",
        "stderr": "",
        "return_code": 0,
        "success": True,
        "timed_out": False,
        "partial_results": False
    }
    
    client.safe_get.return_value = {
        "status": "healthy",
        "message": "Kali Linux Tools API Server is running",
        "tools_status": {
            "nmap": True,
            "gobuster": True,
            "dirb": True,
            "nikto": True
        },
        "all_essential_tools_available": True
    }
    
    client.check_health.return_value = client.safe_get.return_value
    client.execute_command.return_value = client.safe_post.return_value
    
    return client


@pytest.fixture
def kali_client():
    """Create a real KaliToolsClient for integration tests"""
    return KaliToolsClient("http://localhost:5001", timeout=10)


@pytest.fixture
def flask_app():
    """Create Flask app for testing"""
    import kali_server
    app = kali_server.app
    app.config['TESTING'] = True
    return app


@pytest.fixture
def flask_client(flask_app):
    """Create Flask test client"""
    return flask_app.test_client()


@pytest.fixture
def sample_nmap_response():
    """Sample nmap scan response"""
    return {
        "stdout": """Starting Nmap 7.94 ( https://nmap.org )
Nmap scan report for scanme.nmap.org (45.33.32.156)
Host is up (0.081s latency).
Not shown: 996 closed ports
PORT      STATE SERVICE
22/tcp    open  ssh
80/tcp    open  http
443/tcp   open  https
9929/tcp  open  nping-echo

Nmap done: 1 IP address (1 host up) scanned in 2.15 seconds""",
        "stderr": "",
        "return_code": 0,
        "success": True,
        "timed_out": False,
        "partial_results": False
    }


@pytest.fixture
def sample_error_response():
    """Sample error response"""
    return {
        "stdout": "",
        "stderr": "Error: Invalid target",
        "return_code": 1,
        "success": False,
        "timed_out": False,
        "partial_results": False
    }


@pytest.fixture
def sample_timeout_response():
    """Sample timeout response"""
    return {
        "stdout": "Partial output before timeout...",
        "stderr": "",
        "return_code": -1,
        "success": True,
        "timed_out": True,
        "partial_results": True
    }

