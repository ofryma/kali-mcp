"""Tests for CommandExecutor"""
import pytest
import time
from unittest.mock import Mock, patch, MagicMock
import subprocess
import kali_server


class TestCommandExecutor:
    """Test suite for CommandExecutor class"""
    
    def test_initialization(self):
        """Test CommandExecutor initialization"""
        executor = kali_server.CommandExecutor("ls -la", timeout=60)
        assert executor.command == "ls -la"
        assert executor.timeout == 60
        assert executor.stdout_data == ""
        assert executor.stderr_data == ""
        assert executor.timed_out is False
    
    def test_simple_command_success(self):
        """Test execution of a simple successful command"""
        executor = kali_server.CommandExecutor("echo 'test'")
        result = executor.execute()
        
        assert result["success"] is True
        assert result["return_code"] == 0
        assert "test" in result["stdout"]
        assert result["timed_out"] is False
    
    def test_command_with_error(self):
        """Test execution of a command that fails"""
        executor = kali_server.CommandExecutor("ls /nonexistent_directory_xyz")
        result = executor.execute()
        
        assert result["success"] is False
        assert result["return_code"] != 0
        assert len(result["stderr"]) > 0
    
    def test_command_timeout(self):
        """Test command timeout handling"""
        # Command that sleeps for longer than timeout
        executor = kali_server.CommandExecutor("sleep 10", timeout=1)
        result = executor.execute()
        
        assert result["timed_out"] is True
        assert result["return_code"] == -1
    
    @patch('subprocess.Popen')
    def test_command_with_stdout(self, mock_popen):
        """Test command with stdout output"""
        # Mock process
        mock_process = Mock()
        mock_process.stdout.readline.side_effect = ["line1\n", "line2\n", ""]
        mock_process.stderr.readline.side_effect = [""]
        mock_process.wait.return_value = 0
        mock_popen.return_value = mock_process
        
        executor = kali_server.CommandExecutor("test command")
        result = executor.execute()
        
        assert mock_popen.called
    
    @patch('subprocess.Popen')
    def test_command_with_stderr(self, mock_popen):
        """Test command with stderr output"""
        # Mock process
        mock_process = Mock()
        mock_process.stdout.readline.side_effect = [""]
        mock_process.stderr.readline.side_effect = ["error1\n", "error2\n", ""]
        mock_process.wait.return_value = 1
        mock_popen.return_value = mock_process
        
        executor = kali_server.CommandExecutor("test command")
        result = executor.execute()
        
        assert mock_popen.called
    
    @patch('subprocess.Popen')
    def test_timeout_with_partial_results(self, mock_popen):
        """Test timeout handling with partial results"""
        # Mock process that times out
        mock_process = Mock()
        mock_process.stdout.readline.side_effect = ["partial output\n", ""]
        mock_process.stderr.readline.side_effect = [""]
        mock_process.wait.side_effect = subprocess.TimeoutExpired("test", 1)
        mock_process.terminate.return_value = None
        mock_popen.return_value = mock_process
        
        executor = kali_server.CommandExecutor("test command", timeout=1)
        
        # Need to set stdout_data manually since we're mocking threads
        executor.stdout_data = "partial output\n"
        
        with patch.object(executor, '_read_stdout'), \
             patch.object(executor, '_read_stderr'):
            result = executor.execute()
            
            assert result["timed_out"] is True
            assert result["partial_results"] is True
    
    def test_execute_command_function(self):
        """Test the execute_command function"""
        result = kali_server.execute_command("echo 'hello'")
        
        assert isinstance(result, dict)
        assert "stdout" in result
        assert "stderr" in result
        assert "return_code" in result
        assert "success" in result


class TestExecuteCommandFunction:
    """Test the execute_command helper function"""
    
    def test_execute_command_success(self):
        """Test execute_command with successful command"""
        result = kali_server.execute_command("echo test")
        assert result["success"] is True
        assert "test" in result["stdout"]
    
    def test_execute_command_failure(self):
        """Test execute_command with failing command"""
        result = kali_server.execute_command("false")
        assert result["success"] is False
        assert result["return_code"] != 0

