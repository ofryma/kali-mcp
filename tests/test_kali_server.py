"""Tests for Flask API endpoints in kali_server.py"""
import pytest
import json
from unittest.mock import patch, Mock


class TestFlaskEndpoints:
    """Test suite for Flask API endpoints"""
    
    def test_health_check_endpoint(self, flask_client):
        """Test the health check endpoint"""
        with patch('kali_server.execute_command') as mock_exec:
            mock_exec.return_value = {"success": True, "stdout": "/usr/bin/nmap"}
            
            response = flask_client.get('/health')
            assert response.status_code == 200
            
            data = json.loads(response.data)
            assert data["status"] == "healthy"
            assert "tools_status" in data
    
    def test_generic_command_endpoint_success(self, flask_client):
        """Test generic command endpoint with valid command"""
        with patch('kali_server.execute_command') as mock_exec:
            mock_exec.return_value = {
                "stdout": "output",
                "stderr": "",
                "return_code": 0,
                "success": True
            }
            
            response = flask_client.post(
                '/api/command',
                data=json.dumps({"command": "echo test"}),
                content_type='application/json'
            )
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data["success"] is True
    
    def test_generic_command_endpoint_missing_command(self, flask_client):
        """Test generic command endpoint without command parameter"""
        response = flask_client.post(
            '/api/command',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
    
    def test_nmap_endpoint_success(self, flask_client):
        """Test nmap endpoint with valid parameters"""
        with patch('kali_server.execute_command') as mock_exec:
            mock_exec.return_value = {
                "stdout": "Nmap scan report",
                "stderr": "",
                "return_code": 0,
                "success": True
            }
            
            response = flask_client.post(
                '/api/tools/nmap',
                data=json.dumps({
                    "target": "127.0.0.1",
                    "scan_type": "-sV",
                    "ports": "80,443"
                }),
                content_type='application/json'
            )
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data["success"] is True
    
    def test_nmap_endpoint_missing_target(self, flask_client):
        """Test nmap endpoint without target parameter"""
        response = flask_client.post(
            '/api/tools/nmap',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
    
    def test_gobuster_endpoint_success(self, flask_client):
        """Test gobuster endpoint with valid parameters"""
        with patch('kali_server.execute_command') as mock_exec:
            mock_exec.return_value = {
                "stdout": "Found: /admin",
                "stderr": "",
                "return_code": 0,
                "success": True
            }
            
            response = flask_client.post(
                '/api/tools/gobuster',
                data=json.dumps({
                    "url": "http://example.com",
                    "mode": "dir"
                }),
                content_type='application/json'
            )
            
            assert response.status_code == 200
    
    def test_gobuster_invalid_mode(self, flask_client):
        """Test gobuster endpoint with invalid mode"""
        response = flask_client.post(
            '/api/tools/gobuster',
            data=json.dumps({
                "url": "http://example.com",
                "mode": "invalid"
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "Invalid mode" in data["error"]
    
    def test_hydra_endpoint_success(self, flask_client):
        """Test hydra endpoint with valid parameters"""
        with patch('kali_server.execute_command') as mock_exec:
            mock_exec.return_value = {
                "stdout": "found credentials",
                "stderr": "",
                "return_code": 0,
                "success": True
            }
            
            response = flask_client.post(
                '/api/tools/hydra',
                data=json.dumps({
                    "target": "127.0.0.1",
                    "service": "ssh",
                    "username": "admin",
                    "password": "test"
                }),
                content_type='application/json'
            )
            
            assert response.status_code == 200
    
    def test_hydra_missing_required_params(self, flask_client):
        """Test hydra endpoint without required parameters"""
        response = flask_client.post(
            '/api/tools/hydra',
            data=json.dumps({
                "target": "127.0.0.1"
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 400
    
    def test_sqlmap_endpoint(self, flask_client):
        """Test sqlmap endpoint"""
        with patch('kali_server.execute_command') as mock_exec:
            mock_exec.return_value = {
                "stdout": "vulnerable",
                "stderr": "",
                "return_code": 0,
                "success": True
            }
            
            response = flask_client.post(
                '/api/tools/sqlmap',
                data=json.dumps({
                    "url": "http://example.com/page?id=1"
                }),
                content_type='application/json'
            )
            
            assert response.status_code == 200
    
    def test_metasploit_endpoint(self, flask_client):
        """Test metasploit endpoint"""
        with patch('kali_server.execute_command') as mock_exec:
            mock_exec.return_value = {
                "stdout": "exploit success",
                "stderr": "",
                "return_code": 0,
                "success": True
            }
            
            response = flask_client.post(
                '/api/tools/metasploit',
                data=json.dumps({
                    "module": "exploit/unix/ftp/vsftpd_234_backdoor",
                    "options": {"RHOSTS": "127.0.0.1"}
                }),
                content_type='application/json'
            )
            
            assert response.status_code == 200
    
    def test_enum4linux_endpoint(self, flask_client):
        """Test enum4linux endpoint"""
        with patch('kali_server.execute_command') as mock_exec:
            mock_exec.return_value = {
                "stdout": "enumeration results",
                "stderr": "",
                "return_code": 0,
                "success": True
            }
            
            response = flask_client.post(
                '/api/tools/enum4linux',
                data=json.dumps({
                    "target": "192.168.1.1"
                }),
                content_type='application/json'
            )
            
            assert response.status_code == 200


class TestErrorHandling:
    """Test error handling in Flask endpoints"""
    
    def test_command_execution_exception(self, flask_client):
        """Test handling of command execution exceptions"""
        with patch('kali_server.execute_command') as mock_exec:
            mock_exec.side_effect = Exception("Test exception")
            
            response = flask_client.post(
                '/api/command',
                data=json.dumps({"command": "test"}),
                content_type='application/json'
            )
            
            assert response.status_code == 500
            data = json.loads(response.data)
            assert "error" in data
    
    def test_invalid_json(self, flask_client):
        """Test handling of invalid JSON"""
        response = flask_client.post(
            '/api/command',
            data="invalid json",
            content_type='application/json'
        )
        
        assert response.status_code in [400, 500]

