#!/usr/bin/env python3

# This script connect the MCP AI agent to Kali Linux terminal and API Server.

# some of the code here was inspired from https://github.com/whit3rabbit0/project_astro , be sure to check them out

import argparse
import json
import logging
import os
import subprocess
import sys
import traceback
import threading
from typing import Dict, Any
from flask import Flask, request, jsonify

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Configuration
API_PORT = int(os.environ.get("API_PORT", 5001))
DEBUG_MODE = os.environ.get("DEBUG_MODE", "0").lower() in ("1", "true", "yes", "y")
COMMAND_TIMEOUT = 180  # 5 minutes default timeout

app = Flask(__name__)

class CommandExecutor:
    """Class to handle command execution with better timeout management"""
    
    def __init__(self, command: str, timeout: int = COMMAND_TIMEOUT):
        self.command = command
        self.timeout = timeout
        self.process = None
        self.stdout_data = ""
        self.stderr_data = ""
        self.stdout_thread = None
        self.stderr_thread = None
        self.return_code = None
        self.timed_out = False
    
    def _read_stdout(self):
        """Thread function to continuously read stdout"""
        for line in iter(self.process.stdout.readline, ''):
            self.stdout_data += line
    
    def _read_stderr(self):
        """Thread function to continuously read stderr"""
        for line in iter(self.process.stderr.readline, ''):
            self.stderr_data += line
    
    def execute(self) -> Dict[str, Any]:
        """Execute the command and handle timeout gracefully"""
        logger.info(f"Executing command: {self.command}")
        
        try:
            self.process = subprocess.Popen(
                self.command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1  # Line buffered
            )
            
            # Start threads to read output continuously
            self.stdout_thread = threading.Thread(target=self._read_stdout)
            self.stderr_thread = threading.Thread(target=self._read_stderr)
            self.stdout_thread.daemon = True
            self.stderr_thread.daemon = True
            self.stdout_thread.start()
            self.stderr_thread.start()
            
            # Wait for the process to complete or timeout
            try:
                self.return_code = self.process.wait(timeout=self.timeout)
                # Process completed, join the threads
                self.stdout_thread.join()
                self.stderr_thread.join()
            except subprocess.TimeoutExpired:
                # Process timed out but we might have partial results
                self.timed_out = True
                logger.warning(f"Command timed out after {self.timeout} seconds. Terminating process.")
                
                # Try to terminate gracefully first
                self.process.terminate()
                try:
                    self.process.wait(timeout=5)  # Give it 5 seconds to terminate
                except subprocess.TimeoutExpired:
                    # Force kill if it doesn't terminate
                    logger.warning("Process not responding to termination. Killing.")
                    self.process.kill()
                
                # Update final output
                self.return_code = -1
            
            # Always consider it a success if we have output, even with timeout
            success = True if self.timed_out and (self.stdout_data or self.stderr_data) else (self.return_code == 0)
            
            return {
                "stdout": self.stdout_data,
                "stderr": self.stderr_data,
                "return_code": self.return_code,
                "success": success,
                "timed_out": self.timed_out,
                "partial_results": self.timed_out and (self.stdout_data or self.stderr_data)
            }
        
        except Exception as e:
            logger.error(f"Error executing command: {str(e)}")
            logger.error(traceback.format_exc())
            return {
                "stdout": self.stdout_data,
                "stderr": f"Error executing command: {str(e)}\n{self.stderr_data}",
                "return_code": -1,
                "success": False,
                "timed_out": False,
                "partial_results": bool(self.stdout_data or self.stderr_data)
            }


def execute_command(command: str) -> Dict[str, Any]:
    """
    Execute a shell command and return the result
    
    Args:
        command: The command to execute
        
    Returns:
        A dictionary containing the stdout, stderr, and return code
    """
    executor = CommandExecutor(command)
    return executor.execute()


@app.route("/api/command", methods=["POST"])
def generic_command():
    """Execute any command provided in the request."""
    try:
        params = request.json
        command = params.get("command", "")
        
        if not command:
            logger.warning("Command endpoint called without command parameter")
            return jsonify({
                "error": "Command parameter is required"
            }), 400
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in command endpoint: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            "error": f"Server error: {str(e)}"
        }), 500


@app.route("/api/tools/nmap", methods=["POST"])
def nmap():
    """Execute nmap scan with the provided parameters."""
    try:
        params = request.json
        target = params.get("target", "")
        scan_type = params.get("scan_type", "-sCV")
        ports = params.get("ports", "")
        additional_args = params.get("additional_args", "-T4 -Pn")
        
        if not target:
            logger.warning("Nmap called without target parameter")
            return jsonify({
                "error": "Target parameter is required"
            }), 400        
        
        command = f"nmap {scan_type}"
        
        if ports:
            command += f" -p {ports}"
        
        if additional_args:
            # Basic validation for additional args - more sophisticated validation would be better
            command += f" {additional_args}"
        
        command += f" {target}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in nmap endpoint: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            "error": f"Server error: {str(e)}"
        }), 500

@app.route("/api/tools/gobuster", methods=["POST"])
def gobuster():
    """Execute gobuster with the provided parameters."""
    try:
        params = request.json
        url = params.get("url", "")
        mode = params.get("mode", "dir")
        wordlist = params.get("wordlist", "/usr/share/wordlists/dirb/common.txt")
        additional_args = params.get("additional_args", "")
        
        if not url:
            logger.warning("Gobuster called without URL parameter")
            return jsonify({
                "error": "URL parameter is required"
            }), 400
        
        # Validate mode
        if mode not in ["dir", "dns", "fuzz", "vhost"]:
            logger.warning(f"Invalid gobuster mode: {mode}")
            return jsonify({
                "error": f"Invalid mode: {mode}. Must be one of: dir, dns, fuzz, vhost"
            }), 400
        
        command = f"gobuster {mode} -u {url} -w {wordlist}"
        
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in gobuster endpoint: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            "error": f"Server error: {str(e)}"
        }), 500

@app.route("/api/tools/dirb", methods=["POST"])
def dirb():
    """Execute dirb with the provided parameters."""
    try:
        params = request.json
        url = params.get("url", "")
        wordlist = params.get("wordlist", "/usr/share/wordlists/dirb/common.txt")
        additional_args = params.get("additional_args", "")
        
        if not url:
            logger.warning("Dirb called without URL parameter")
            return jsonify({
                "error": "URL parameter is required"
            }), 400
        
        command = f"dirb {url} {wordlist}"
        
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in dirb endpoint: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            "error": f"Server error: {str(e)}"
        }), 500

@app.route("/api/tools/nikto", methods=["POST"])
def nikto():
    """Execute nikto with the provided parameters."""
    try:
        params = request.json
        target = params.get("target", "")
        additional_args = params.get("additional_args", "")
        
        if not target:
            logger.warning("Nikto called without target parameter")
            return jsonify({
                "error": "Target parameter is required"
            }), 400
        
        command = f"nikto -h {target}"
        
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in nikto endpoint: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            "error": f"Server error: {str(e)}"
        }), 500

@app.route("/api/tools/sqlmap", methods=["POST"])
def sqlmap():
    """Execute sqlmap with the provided parameters."""
    try:
        params = request.json
        url = params.get("url", "")
        data = params.get("data", "")
        additional_args = params.get("additional_args", "")
        
        if not url:
            logger.warning("SQLMap called without URL parameter")
            return jsonify({
                "error": "URL parameter is required"
            }), 400
        
        command = f"sqlmap -u {url} --batch"
        
        if data:
            command += f" --data=\"{data}\""
        
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in sqlmap endpoint: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            "error": f"Server error: {str(e)}"
        }), 500

@app.route("/api/tools/metasploit", methods=["POST"])
def metasploit():
    """Execute metasploit module with the provided parameters."""
    try:
        params = request.json
        module = params.get("module", "")
        options = params.get("options", {})
        
        if not module:
            logger.warning("Metasploit called without module parameter")
            return jsonify({
                "error": "Module parameter is required"
            }), 400
        
        # Format options for Metasploit
        options_str = ""
        for key, value in options.items():
            options_str += f" {key}={value}"
        
        # Create an MSF resource script
        resource_content = f"use {module}\n"
        for key, value in options.items():
            resource_content += f"set {key} {value}\n"
        resource_content += "exploit\n"
        
        # Save resource script to a temporary file
        resource_file = "/tmp/mcp_msf_resource.rc"
        with open(resource_file, "w") as f:
            f.write(resource_content)
        
        command = f"msfconsole -q -r {resource_file}"
        result = execute_command(command)
        
        # Clean up the temporary file
        try:
            os.remove(resource_file)
        except Exception as e:
            logger.warning(f"Error removing temporary resource file: {str(e)}")
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in metasploit endpoint: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            "error": f"Server error: {str(e)}"
        }), 500

@app.route("/api/tools/hydra", methods=["POST"])
def hydra():
    """Execute hydra with the provided parameters."""
    try:
        params = request.json
        target = params.get("target", "")
        service = params.get("service", "")
        username = params.get("username", "")
        username_file = params.get("username_file", "")
        password = params.get("password", "")
        password_file = params.get("password_file", "")
        additional_args = params.get("additional_args", "")
        
        if not target or not service:
            logger.warning("Hydra called without target or service parameter")
            return jsonify({
                "error": "Target and service parameters are required"
            }), 400
        
        if not (username or username_file) or not (password or password_file):
            logger.warning("Hydra called without username/password parameters")
            return jsonify({
                "error": "Username/username_file and password/password_file are required"
            }), 400
        
        command = f"hydra -t 4"
        
        if username:
            command += f" -l {username}"
        elif username_file:
            command += f" -L {username_file}"
        
        if password:
            command += f" -p {password}"
        elif password_file:
            command += f" -P {password_file}"
        
        if additional_args:
            command += f" {additional_args}"
        
        command += f" {target} {service}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in hydra endpoint: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            "error": f"Server error: {str(e)}"
        }), 500

@app.route("/api/tools/john", methods=["POST"])
def john():
    """Execute john with the provided parameters."""
    try:
        params = request.json
        hash_file = params.get("hash_file", "")
        wordlist = params.get("wordlist", "/usr/share/wordlists/rockyou.txt")
        format_type = params.get("format", "")
        additional_args = params.get("additional_args", "")
        
        if not hash_file:
            logger.warning("John called without hash_file parameter")
            return jsonify({
                "error": "Hash file parameter is required"
            }), 400
        
        command = f"john"
        
        if format_type:
            command += f" --format={format_type}"
        
        if wordlist:
            command += f" --wordlist={wordlist}"
        
        if additional_args:
            command += f" {additional_args}"
        
        command += f" {hash_file}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in john endpoint: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            "error": f"Server error: {str(e)}"
        }), 500

@app.route("/api/tools/wpscan", methods=["POST"])
def wpscan():
    """Execute wpscan with the provided parameters."""
    try:
        params = request.json
        url = params.get("url", "")
        additional_args = params.get("additional_args", "")
        
        if not url:
            logger.warning("WPScan called without URL parameter")
            return jsonify({
                "error": "URL parameter is required"
            }), 400
        
        command = f"wpscan --url {url}"
        
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in wpscan endpoint: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            "error": f"Server error: {str(e)}"
        }), 500

@app.route("/api/tools/enum4linux", methods=["POST"])
def enum4linux():
    """Execute enum4linux with the provided parameters."""
    try:
        params = request.json
        target = params.get("target", "")
        additional_args = params.get("additional_args", "-a")
        
        if not target:
            logger.warning("Enum4linux called without target parameter")
            return jsonify({
                "error": "Target parameter is required"
            }), 400
        
        command = f"enum4linux {additional_args} {target}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in enum4linux endpoint: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            "error": f"Server error: {str(e)}"
        }), 500

# ============================================================================
# NETWORK SCANNING TOOLS
# ============================================================================

@app.route("/api/tools/masscan", methods=["POST"])
def masscan():
    """Execute masscan with the provided parameters."""
    try:
        params = request.json
        target = params.get("target", "")
        ports = params.get("ports", "0-65535")
        rate = params.get("rate", "1000")
        additional_args = params.get("additional_args", "")
        
        if not target:
            return jsonify({"error": "Target parameter is required"}), 400
        
        command = f"masscan {target} -p{ports} --rate {rate}"
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in masscan endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/netdiscover", methods=["POST"])
def netdiscover():
    """Execute netdiscover with the provided parameters."""
    try:
        params = request.json
        range_param = params.get("range", "")
        interface = params.get("interface", "")
        passive_mode = params.get("passive_mode", False)
        additional_args = params.get("additional_args", "")
        
        command = "netdiscover"
        if range_param:
            command += f" -r {range_param}"
        if interface:
            command += f" -i {interface}"
        if passive_mode:
            command += " -p"
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in netdiscover endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/hping3", methods=["POST"])
def hping3():
    """Execute hping3 with the provided parameters."""
    try:
        params = request.json
        target = params.get("target", "")
        mode = params.get("mode", "syn")
        port = params.get("port", "80")
        count = params.get("count", "3")
        additional_args = params.get("additional_args", "")
        
        if not target:
            return jsonify({"error": "Target parameter is required"}), 400
        
        mode_flags = {"syn": "-S", "udp": "--udp", "icmp": "--icmp", "raw": "--rawip"}
        command = f"hping3 {mode_flags.get(mode, '-S')} -p {port} -c {count}"
        if additional_args:
            command += f" {additional_args}"
        command += f" {target}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in hping3 endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/unicornscan", methods=["POST"])
def unicornscan():
    """Execute unicornscan with the provided parameters."""
    try:
        params = request.json
        target = params.get("target", "")
        mode = params.get("mode", "tcp")
        ports = params.get("ports", "1-65535")
        additional_args = params.get("additional_args", "")
        
        if not target:
            return jsonify({"error": "Target parameter is required"}), 400
        
        mode_flag = "T" if mode == "tcp" else "U"
        command = f"unicornscan -m{mode_flag} -p {ports}"
        if additional_args:
            command += f" {additional_args}"
        command += f" {target}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in unicornscan endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/arping", methods=["POST"])
def arping():
    """Execute arping with the provided parameters."""
    try:
        params = request.json
        target = params.get("target", "")
        interface = params.get("interface", "")
        count = params.get("count", "4")
        additional_args = params.get("additional_args", "")
        
        if not target:
            return jsonify({"error": "Target parameter is required"}), 400
        
        command = f"arping -c {count}"
        if interface:
            command += f" -I {interface}"
        if additional_args:
            command += f" {additional_args}"
        command += f" {target}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in arping endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/tcpdump", methods=["POST"])
def tcpdump():
    """Execute tcpdump with the provided parameters."""
    try:
        params = request.json
        interface = params.get("interface", "eth0")
        filter_expr = params.get("filter_expr", "")
        count = params.get("count", "100")
        output_file = params.get("output_file", "")
        additional_args = params.get("additional_args", "")
        
        command = f"tcpdump -i {interface} -c {count}"
        if output_file:
            command += f" -w {output_file}"
        if additional_args:
            command += f" {additional_args}"
        if filter_expr:
            command += f" '{filter_expr}'"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in tcpdump endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/tshark", methods=["POST"])
def tshark():
    """Execute tshark with the provided parameters."""
    try:
        params = request.json
        interface = params.get("interface", "eth0")
        filter_expr = params.get("filter_expr", "")
        count = params.get("count", "100")
        read_file = params.get("read_file", "")
        additional_args = params.get("additional_args", "")
        
        if read_file:
            command = f"tshark -r {read_file}"
        else:
            command = f"tshark -i {interface} -c {count}"
        
        if filter_expr:
            command += f" -Y '{filter_expr}'"
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in tshark endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

# ============================================================================
# WEB APPLICATION SECURITY TOOLS
# ============================================================================

@app.route("/api/tools/zap", methods=["POST"])
def zap():
    """Execute OWASP ZAP with the provided parameters."""
    try:
        params = request.json
        target = params.get("target", "")
        scan_type = params.get("scan_type", "baseline")
        additional_args = params.get("additional_args", "")
        
        if not target:
            return jsonify({"error": "Target parameter is required"}), 400
        
        command = f"zap-{scan_type}.py -t {target}"
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in zap endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/wfuzz", methods=["POST"])
def wfuzz():
    """Execute wfuzz with the provided parameters."""
    try:
        params = request.json
        url = params.get("url", "")
        wordlist = params.get("wordlist", "/usr/share/wordlists/dirb/common.txt")
        payload_position = params.get("payload_position", "FUZZ")
        additional_args = params.get("additional_args", "")
        
        if not url:
            return jsonify({"error": "URL parameter is required"}), 400
        
        command = f"wfuzz -w {wordlist}"
        if additional_args:
            command += f" {additional_args}"
        command += f" {url}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in wfuzz endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/ffuf", methods=["POST"])
def ffuf():
    """Execute ffuf with the provided parameters."""
    try:
        params = request.json
        url = params.get("url", "")
        wordlist = params.get("wordlist", "/usr/share/wordlists/dirb/common.txt")
        mode = params.get("mode", "dir")
        additional_args = params.get("additional_args", "")
        
        if not url:
            return jsonify({"error": "URL parameter is required"}), 400
        
        command = f"ffuf -u {url} -w {wordlist}"
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in ffuf endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/whatweb", methods=["POST"])
def whatweb():
    """Execute whatweb with the provided parameters."""
    try:
        params = request.json
        target = params.get("target", "")
        aggression = params.get("aggression", "1")
        additional_args = params.get("additional_args", "")
        
        if not target:
            return jsonify({"error": "Target parameter is required"}), 400
        
        command = f"whatweb -a {aggression}"
        if additional_args:
            command += f" {additional_args}"
        command += f" {target}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in whatweb endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/sublist3r", methods=["POST"])
def sublist3r():
    """Execute sublist3r with the provided parameters."""
    try:
        params = request.json
        domain = params.get("domain", "")
        bruteforce = params.get("bruteforce", False)
        ports = params.get("ports", "")
        additional_args = params.get("additional_args", "")
        
        if not domain:
            return jsonify({"error": "Domain parameter is required"}), 400
        
        command = f"sublist3r -d {domain}"
        if bruteforce:
            command += " -b"
        if ports:
            command += f" -p {ports}"
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in sublist3r endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/amass", methods=["POST"])
def amass():
    """Execute amass with the provided parameters."""
    try:
        params = request.json
        domain = params.get("domain", "")
        mode = params.get("mode", "enum")
        passive = params.get("passive", False)
        additional_args = params.get("additional_args", "")
        
        if not domain:
            return jsonify({"error": "Domain parameter is required"}), 400
        
        command = f"amass {mode} -d {domain}"
        if passive:
            command += " -passive"
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in amass endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/wapiti", methods=["POST"])
def wapiti():
    """Execute wapiti with the provided parameters."""
    try:
        params = request.json
        url = params.get("url", "")
        scope = params.get("scope", "page")
        modules = params.get("modules", "")
        additional_args = params.get("additional_args", "")
        
        if not url:
            return jsonify({"error": "URL parameter is required"}), 400
        
        command = f"wapiti -u {url} --scope {scope}"
        if modules:
            command += f" -m {modules}"
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in wapiti endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/commix", methods=["POST"])
def commix():
    """Execute commix with the provided parameters."""
    try:
        params = request.json
        url = params.get("url", "")
        data = params.get("data", "")
        cookie = params.get("cookie", "")
        additional_args = params.get("additional_args", "")
        
        if not url:
            return jsonify({"error": "URL parameter is required"}), 400
        
        command = f"commix --url={url} --batch"
        if data:
            command += f" --data='{data}'"
        if cookie:
            command += f" --cookie='{cookie}'"
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in commix endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/xsstrike", methods=["POST"])
def xsstrike():
    """Execute xsstrike with the provided parameters."""
    try:
        params = request.json
        url = params.get("url", "")
        data = params.get("data", "")
        crawl = params.get("crawl", False)
        additional_args = params.get("additional_args", "")
        
        if not url:
            return jsonify({"error": "URL parameter is required"}), 400
        
        command = f"xsstrike -u {url}"
        if data:
            command += f" --data '{data}'"
        if crawl:
            command += " --crawl"
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in xsstrike endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/skipfish", methods=["POST"])
def skipfish():
    """Execute skipfish with the provided parameters."""
    try:
        params = request.json
        url = params.get("url", "")
        output_dir = params.get("output_dir", "/tmp/skipfish_results")
        wordlist = params.get("wordlist", "")
        additional_args = params.get("additional_args", "")
        
        if not url:
            return jsonify({"error": "URL parameter is required"}), 400
        
        command = f"skipfish -o {output_dir}"
        if wordlist:
            command += f" -W {wordlist}"
        if additional_args:
            command += f" {additional_args}"
        command += f" {url}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in skipfish endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

# ============================================================================
# PASSWORD CRACKING TOOLS
# ============================================================================

@app.route("/api/tools/hashcat", methods=["POST"])
def hashcat():
    """Execute hashcat with the provided parameters."""
    try:
        params = request.json
        hash_file = params.get("hash_file", "")
        wordlist = params.get("wordlist", "/usr/share/wordlists/rockyou.txt")
        hash_type = params.get("hash_type", "0")
        attack_mode = params.get("attack_mode", "0")
        additional_args = params.get("additional_args", "")
        
        if not hash_file:
            return jsonify({"error": "Hash file parameter is required"}), 400
        
        command = f"hashcat -m {hash_type} -a {attack_mode} {hash_file} {wordlist}"
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in hashcat endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/medusa", methods=["POST"])
def medusa():
    """Execute medusa with the provided parameters."""
    try:
        params = request.json
        target = params.get("target", "")
        service = params.get("service", "")
        username = params.get("username", "")
        username_file = params.get("username_file", "")
        password = params.get("password", "")
        password_file = params.get("password_file", "")
        additional_args = params.get("additional_args", "")
        
        if not target or not service:
            return jsonify({"error": "Target and service parameters are required"}), 400
        
        command = f"medusa -h {target} -M {service}"
        if username:
            command += f" -u {username}"
        elif username_file:
            command += f" -U {username_file}"
        if password:
            command += f" -p {password}"
        elif password_file:
            command += f" -P {password_file}"
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in medusa endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/crackmapexec", methods=["POST"])
def crackmapexec():
    """Execute crackmapexec with the provided parameters."""
    try:
        params = request.json
        target = params.get("target", "")
        protocol = params.get("protocol", "smb")
        username = params.get("username", "")
        password = params.get("password", "")
        hash_param = params.get("hash", "")
        additional_args = params.get("additional_args", "")
        
        if not target:
            return jsonify({"error": "Target parameter is required"}), 400
        
        command = f"crackmapexec {protocol} {target}"
        if username:
            command += f" -u {username}"
        if password:
            command += f" -p {password}"
        elif hash_param:
            command += f" -H {hash_param}"
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in crackmapexec endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/patator", methods=["POST"])
def patator():
    """Execute patator with the provided parameters."""
    try:
        params = request.json
        module = params.get("module", "")
        target = params.get("target", "")
        username_file = params.get("username_file", "")
        password_file = params.get("password_file", "")
        additional_args = params.get("additional_args", "")
        
        if not module or not target:
            return jsonify({"error": "Module and target parameters are required"}), 400
        
        command = f"patator {module} host={target}"
        if username_file:
            command += f" user=FILE0 0={username_file}"
        if password_file:
            command += f" password=FILE1 1={password_file}"
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in patator endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/fcrackzip", methods=["POST"])
def fcrackzip():
    """Execute fcrackzip with the provided parameters."""
    try:
        params = request.json
        zip_file = params.get("zip_file", "")
        wordlist = params.get("wordlist", "")
        bruteforce = params.get("bruteforce", False)
        charset = params.get("charset", "aA1")
        additional_args = params.get("additional_args", "")
        
        if not zip_file:
            return jsonify({"error": "ZIP file parameter is required"}), 400
        
        if bruteforce:
            command = f"fcrackzip -b -c '{charset}' -l 1-8"
        elif wordlist:
            command = f"fcrackzip -D -p {wordlist}"
        else:
            return jsonify({"error": "Either wordlist or bruteforce mode required"}), 400
        
        if additional_args:
            command += f" {additional_args}"
        command += f" {zip_file}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in fcrackzip endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

# ============================================================================
# EXPLOITATION TOOLS
# ============================================================================

@app.route("/api/tools/searchsploit", methods=["POST"])
def searchsploit():
    """Execute searchsploit with the provided parameters."""
    try:
        params = request.json
        query = params.get("query", "")
        exact = params.get("exact", False)
        json_output = params.get("json_output", True)
        additional_args = params.get("additional_args", "")
        
        if not query:
            return jsonify({"error": "Query parameter is required"}), 400
        
        command = f"searchsploit"
        if exact:
            command += " -e"
        if json_output:
            command += " -j"
        if additional_args:
            command += f" {additional_args}"
        command += f" {query}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in searchsploit endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/beef", methods=["POST"])
def beef():
    """Execute beef with the provided parameters."""
    try:
        params = request.json
        port = params.get("port", "3000")
        additional_args = params.get("additional_args", "")
        
        command = f"beef-xss -p {port}"
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in beef endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/setoolkit", methods=["POST"])
def setoolkit():
    """Execute setoolkit with the provided parameters."""
    try:
        params = request.json
        attack_vector = params.get("attack_vector", "")
        payload = params.get("payload", "")
        target = params.get("target", "")
        additional_args = params.get("additional_args", "")
        
        # SET requires interactive mode, so this is a placeholder
        command = f"setoolkit"
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in setoolkit endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/routersploit", methods=["POST"])
def routersploit():
    """Execute routersploit with the provided parameters."""
    try:
        params = request.json
        module = params.get("module", "")
        target = params.get("target", "")
        port = params.get("port", "")
        additional_options = params.get("additional_options", "")
        
        if not module or not target:
            return jsonify({"error": "Module and target parameters are required"}), 400
        
        # RouterSploit requires interactive mode, this is simplified
        command = f"routersploit -m {module} -t {target}"
        if port:
            command += f" -p {port}"
        if additional_options:
            command += f" {additional_options}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in routersploit endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

# ============================================================================
# WIRELESS ATTACK TOOLS
# ============================================================================

@app.route("/api/tools/aircrack", methods=["POST"])
def aircrack():
    """Execute aircrack-ng with the provided parameters."""
    try:
        params = request.json
        capture_file = params.get("capture_file", "")
        wordlist = params.get("wordlist", "/usr/share/wordlists/rockyou.txt")
        bssid = params.get("bssid", "")
        additional_args = params.get("additional_args", "")
        
        if not capture_file:
            return jsonify({"error": "Capture file parameter is required"}), 400
        
        command = f"aircrack-ng -w {wordlist}"
        if bssid:
            command += f" -b {bssid}"
        if additional_args:
            command += f" {additional_args}"
        command += f" {capture_file}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in aircrack endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/reaver", methods=["POST"])
def reaver():
    """Execute reaver with the provided parameters."""
    try:
        params = request.json
        interface = params.get("interface", "")
        bssid = params.get("bssid", "")
        channel = params.get("channel", "")
        additional_args = params.get("additional_args", "")
        
        if not interface or not bssid:
            return jsonify({"error": "Interface and BSSID parameters are required"}), 400
        
        command = f"reaver -i {interface} -b {bssid}"
        if channel:
            command += f" -c {channel}"
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in reaver endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/bully", methods=["POST"])
def bully():
    """Execute bully with the provided parameters."""
    try:
        params = request.json
        interface = params.get("interface", "")
        bssid = params.get("bssid", "")
        channel = params.get("channel", "")
        additional_args = params.get("additional_args", "")
        
        if not interface or not bssid:
            return jsonify({"error": "Interface and BSSID parameters are required"}), 400
        
        command = f"bully {interface} -b {bssid}"
        if channel:
            command += f" -c {channel}"
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in bully endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/wifite", methods=["POST"])
def wifite():
    """Execute wifite with the provided parameters."""
    try:
        params = request.json
        interface = params.get("interface", "")
        target_bssid = params.get("target_bssid", "")
        additional_args = params.get("additional_args", "")
        
        command = "wifite"
        if interface:
            command += f" -i {interface}"
        if target_bssid:
            command += f" --bssid {target_bssid}"
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in wifite endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/kismet", methods=["POST"])
def kismet():
    """Execute kismet with the provided parameters."""
    try:
        params = request.json
        interface = params.get("interface", "")
        duration = params.get("duration", "60")
        additional_args = params.get("additional_args", "")
        
        if not interface:
            return jsonify({"error": "Interface parameter is required"}), 400
        
        command = f"timeout {duration} kismet -c {interface}"
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in kismet endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

# ============================================================================
# WINDOWS/ACTIVE DIRECTORY TOOLS
# ============================================================================

@app.route("/api/tools/responder", methods=["POST"])
def responder():
    """Execute responder with the provided parameters."""
    try:
        params = request.json
        interface = params.get("interface", "")
        analyze = params.get("analyze", False)
        wpad = params.get("wpad", True)
        additional_args = params.get("additional_args", "")
        
        if not interface:
            return jsonify({"error": "Interface parameter is required"}), 400
        
        command = f"responder -I {interface}"
        if analyze:
            command += " -A"
        if wpad:
            command += " -w"
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in responder endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/impacket", methods=["POST"])
def impacket():
    """Execute impacket scripts with the provided parameters."""
    try:
        params = request.json
        script = params.get("script", "")
        target = params.get("target", "")
        username = params.get("username", "")
        password = params.get("password", "")
        hash_param = params.get("hash", "")
        additional_args = params.get("additional_args", "")
        
        if not script or not target:
            return jsonify({"error": "Script and target parameters are required"}), 400
        
        # Construct authentication
        auth = ""
        if username:
            if password:
                auth = f"{username}:{password}@"
            elif hash_param:
                auth = f"{username}@"
        
        command = f"{script}.py {auth}{target}"
        if hash_param and username:
            command += f" -hashes :{hash_param}"
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in impacket endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/evil_winrm", methods=["POST"])
def evil_winrm():
    """Execute evil-winrm with the provided parameters."""
    try:
        params = request.json
        target = params.get("target", "")
        username = params.get("username", "")
        password = params.get("password", "")
        hash_param = params.get("hash", "")
        additional_args = params.get("additional_args", "")
        
        if not target or not username:
            return jsonify({"error": "Target and username parameters are required"}), 400
        
        command = f"evil-winrm -i {target} -u {username}"
        if password:
            command += f" -p {password}"
        elif hash_param:
            command += f" -H {hash_param}"
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in evil_winrm endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/kerbrute", methods=["POST"])
def kerbrute():
    """Execute kerbrute with the provided parameters."""
    try:
        params = request.json
        domain = params.get("domain", "")
        dc_ip = params.get("dc_ip", "")
        mode = params.get("mode", "userenum")
        wordlist = params.get("wordlist", "")
        additional_args = params.get("additional_args", "")
        
        if not domain or not dc_ip:
            return jsonify({"error": "Domain and DC IP parameters are required"}), 400
        
        command = f"kerbrute {mode} --dc {dc_ip} -d {domain}"
        if wordlist:
            command += f" {wordlist}"
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in kerbrute endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/mimikatz", methods=["POST"])
def mimikatz():
    """Execute mimikatz with the provided parameters."""
    try:
        params = request.json
        command_param = params.get("command", "")
        target = params.get("target", "")
        additional_args = params.get("additional_args", "")
        
        if not command_param:
            return jsonify({"error": "Command parameter is required"}), 400
        
        # Mimikatz requires Windows, this is a placeholder
        command = f"mimikatz '{command_param}'"
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in mimikatz endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

# ============================================================================
# INFORMATION GATHERING TOOLS
# ============================================================================

@app.route("/api/tools/theharvester", methods=["POST"])
def theharvester():
    """Execute theharvester with the provided parameters."""
    try:
        params = request.json
        domain = params.get("domain", "")
        sources = params.get("sources", "all")
        limit = params.get("limit", "500")
        additional_args = params.get("additional_args", "")
        
        if not domain:
            return jsonify({"error": "Domain parameter is required"}), 400
        
        command = f"theHarvester -d {domain} -b {sources} -l {limit}"
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in theharvester endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/reconng", methods=["POST"])
def reconng():
    """Execute recon-ng with the provided parameters."""
    try:
        params = request.json
        workspace = params.get("workspace", "default")
        module = params.get("module", "")
        target = params.get("target", "")
        additional_args = params.get("additional_args", "")
        
        if not module or not target:
            return jsonify({"error": "Module and target parameters are required"}), 400
        
        command = f"recon-ng -w {workspace} -m {module} -o SOURCE={target}"
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in reconng endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/shodan", methods=["POST"])
def shodan():
    """Execute shodan CLI with the provided parameters."""
    try:
        params = request.json
        query = params.get("query", "")
        limit = params.get("limit", "100")
        additional_args = params.get("additional_args", "")
        
        if not query:
            return jsonify({"error": "Query parameter is required"}), 400
        
        command = f"shodan search --limit {limit}"
        if additional_args:
            command += f" {additional_args}"
        command += f" '{query}'"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in shodan endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/spiderfoot", methods=["POST"])
def spiderfoot():
    """Execute spiderfoot with the provided parameters."""
    try:
        params = request.json
        target = params.get("target", "")
        modules = params.get("modules", "all")
        additional_args = params.get("additional_args", "")
        
        if not target:
            return jsonify({"error": "Target parameter is required"}), 400
        
        command = f"spiderfoot -s {target} -m {modules}"
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in spiderfoot endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/dnsenum", methods=["POST"])
def dnsenum():
    """Execute dnsenum with the provided parameters."""
    try:
        params = request.json
        domain = params.get("domain", "")
        dns_server = params.get("dns_server", "")
        additional_args = params.get("additional_args", "")
        
        if not domain:
            return jsonify({"error": "Domain parameter is required"}), 400
        
        command = f"dnsenum"
        if dns_server:
            command += f" --dnsserver {dns_server}"
        if additional_args:
            command += f" {additional_args}"
        command += f" {domain}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in dnsenum endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/fierce", methods=["POST"])
def fierce():
    """Execute fierce with the provided parameters."""
    try:
        params = request.json
        domain = params.get("domain", "")
        dns_server = params.get("dns_server", "")
        additional_args = params.get("additional_args", "")
        
        if not domain:
            return jsonify({"error": "Domain parameter is required"}), 400
        
        command = f"fierce --domain {domain}"
        if dns_server:
            command += f" --dns-servers {dns_server}"
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in fierce endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/dnsrecon", methods=["POST"])
def dnsrecon():
    """Execute dnsrecon with the provided parameters."""
    try:
        params = request.json
        domain = params.get("domain", "")
        scan_type = params.get("scan_type", "std")
        additional_args = params.get("additional_args", "")
        
        if not domain:
            return jsonify({"error": "Domain parameter is required"}), 400
        
        command = f"dnsrecon -d {domain} -t {scan_type}"
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in dnsrecon endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/whois", methods=["POST"])
def whois():
    """Execute whois with the provided parameters."""
    try:
        params = request.json
        target = params.get("target", "")
        additional_args = params.get("additional_args", "")
        
        if not target:
            return jsonify({"error": "Target parameter is required"}), 400
        
        command = f"whois"
        if additional_args:
            command += f" {additional_args}"
        command += f" {target}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in whois endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/metagoofil", methods=["POST"])
def metagoofil():
    """Execute metagoofil with the provided parameters."""
    try:
        params = request.json
        domain = params.get("domain", "")
        file_types = params.get("file_types", "pdf,doc,xls,ppt")
        limit = params.get("limit", "100")
        additional_args = params.get("additional_args", "")
        
        if not domain:
            return jsonify({"error": "Domain parameter is required"}), 400
        
        command = f"metagoofil -d {domain} -t {file_types} -l {limit} -o /tmp/metagoofil -f results.html"
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in metagoofil endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

# ============================================================================
# SHELL & PERSISTENCE TOOLS
# ============================================================================

@app.route("/api/tools/weevely", methods=["POST"])
def weevely():
    """Execute weevely with the provided parameters."""
    try:
        params = request.json
        mode = params.get("mode", "")
        url = params.get("url", "")
        password = params.get("password", "")
        output_file = params.get("output_file", "")
        additional_args = params.get("additional_args", "")
        
        if mode == "generate" and output_file and password:
            command = f"weevely generate {password} {output_file}"
        elif mode == "connect" and url and password:
            command = f"weevely {url} {password}"
        else:
            return jsonify({"error": "Invalid parameters for weevely mode"}), 400
        
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in weevely endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/netcat", methods=["POST"])
def netcat():
    """Execute netcat with the provided parameters."""
    try:
        params = request.json
        mode = params.get("mode", "")
        target = params.get("target", "")
        port = params.get("port", "4444")
        additional_args = params.get("additional_args", "")
        
        if mode == "listen":
            command = f"nc -lvnp {port}"
        elif mode == "connect" and target:
            command = f"nc {target} {port}"
        else:
            return jsonify({"error": "Invalid parameters for netcat mode"}), 400
        
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in netcat endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/socat", methods=["POST"])
def socat():
    """Execute socat with the provided parameters."""
    try:
        params = request.json
        source = params.get("source", "")
        destination = params.get("destination", "")
        additional_args = params.get("additional_args", "")
        
        if not source or not destination:
            return jsonify({"error": "Source and destination parameters are required"}), 400
        
        command = f"socat {source} {destination}"
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in socat endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/msfvenom", methods=["POST"])
def msfvenom():
    """Execute msfvenom with the provided parameters."""
    try:
        params = request.json
        payload = params.get("payload", "")
        lhost = params.get("lhost", "")
        lport = params.get("lport", "4444")
        format_param = params.get("format", "elf")
        output_file = params.get("output_file", "")
        additional_args = params.get("additional_args", "")
        
        if not payload or not lhost:
            return jsonify({"error": "Payload and LHOST parameters are required"}), 400
        
        command = f"msfvenom -p {payload} LHOST={lhost} LPORT={lport} -f {format_param}"
        if output_file:
            command += f" -o {output_file}"
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in msfvenom endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

# ============================================================================
# VULNERABILITY SCANNING TOOLS
# ============================================================================

@app.route("/api/tools/openvas", methods=["POST"])
def openvas():
    """Execute openvas with the provided parameters."""
    try:
        params = request.json
        target = params.get("target", "")
        scan_config = params.get("scan_config", "full_and_fast")
        additional_args = params.get("additional_args", "")
        
        if not target:
            return jsonify({"error": "Target parameter is required"}), 400
        
        # OpenVAS requires GVM/GSA setup, this is simplified
        command = f"gvm-cli --gmp-username admin --gmp-password admin socket --xml '<create_target><name>{target}</name><hosts>{target}</hosts></create_target>'"
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in openvas endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/nuclei", methods=["POST"])
def nuclei():
    """Execute nuclei with the provided parameters."""
    try:
        params = request.json
        target = params.get("target", "")
        templates = params.get("templates", "")
        severity = params.get("severity", "")
        additional_args = params.get("additional_args", "")
        
        if not target:
            return jsonify({"error": "Target parameter is required"}), 400
        
        command = f"nuclei -u {target}"
        if templates:
            command += f" -t {templates}"
        if severity:
            command += f" -s {severity}"
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in nuclei endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/lynis", methods=["POST"])
def lynis():
    """Execute lynis with the provided parameters."""
    try:
        params = request.json
        audit_type = params.get("audit_type", "system")
        additional_args = params.get("additional_args", "")
        
        command = f"lynis audit {audit_type}"
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in lynis endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

# ============================================================================
# DATABASE TOOLS
# ============================================================================

@app.route("/api/tools/nosqlmap", methods=["POST"])
def nosqlmap():
    """Execute nosqlmap with the provided parameters."""
    try:
        params = request.json
        url = params.get("url", "")
        method = params.get("method", "GET")
        data = params.get("data", "")
        additional_args = params.get("additional_args", "")
        
        if not url:
            return jsonify({"error": "URL parameter is required"}), 400
        
        command = f"nosqlmap -u {url}"
        if method == "POST" and data:
            command += f" --data '{data}'"
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in nosqlmap endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

# ============================================================================
# FORENSICS TOOLS
# ============================================================================

@app.route("/api/tools/binwalk", methods=["POST"])
def binwalk():
    """Execute binwalk with the provided parameters."""
    try:
        params = request.json
        file_path = params.get("file_path", "")
        extract = params.get("extract", False)
        additional_args = params.get("additional_args", "")
        
        if not file_path:
            return jsonify({"error": "File path parameter is required"}), 400
        
        command = f"binwalk"
        if extract:
            command += " -e"
        if additional_args:
            command += f" {additional_args}"
        command += f" {file_path}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in binwalk endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/api/tools/foremost", methods=["POST"])
def foremost():
    """Execute foremost with the provided parameters."""
    try:
        params = request.json
        file_path = params.get("file_path", "")
        output_dir = params.get("output_dir", "/tmp/foremost_output")
        file_types = params.get("file_types", "")
        additional_args = params.get("additional_args", "")
        
        if not file_path:
            return jsonify({"error": "File path parameter is required"}), 400
        
        command = f"foremost -o {output_dir}"
        if file_types:
            command += f" -t {file_types}"
        if additional_args:
            command += f" {additional_args}"
        command += f" -i {file_path}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in foremost endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

# ============================================================================
# ANONYMITY & PROXY TOOLS
# ============================================================================

@app.route("/api/tools/proxychains", methods=["POST"])
def proxychains():
    """Execute proxychains with the provided parameters."""
    try:
        params = request.json
        command_param = params.get("command", "")
        config_file = params.get("config_file", "")
        additional_args = params.get("additional_args", "")
        
        if not command_param:
            return jsonify({"error": "Command parameter is required"}), 400
        
        command = "proxychains"
        if config_file:
            command += f" -f {config_file}"
        if additional_args:
            command += f" {additional_args}"
        command += f" {command_param}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in proxychains endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

# ============================================================================
# MOBILE & API TESTING TOOLS
# ============================================================================

@app.route("/api/tools/apktool", methods=["POST"])
def apktool():
    """Execute apktool with the provided parameters."""
    try:
        params = request.json
        mode = params.get("mode", "")
        apk_path = params.get("apk_path", "")
        output_dir = params.get("output_dir", "")
        additional_args = params.get("additional_args", "")
        
        if not mode or not apk_path:
            return jsonify({"error": "Mode and APK path parameters are required"}), 400
        
        if mode == "decode":
            command = f"apktool d {apk_path}"
            if output_dir:
                command += f" -o {output_dir}"
        elif mode == "build":
            command = f"apktool b {apk_path}"
            if output_dir:
                command += f" -o {output_dir}"
        else:
            return jsonify({"error": "Invalid mode. Use 'decode' or 'build'"}), 400
        
        if additional_args:
            command += f" {additional_args}"
        
        result = execute_command(command)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in apktool endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

# Health check endpoint
@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    # Check if essential tools are installed
    essential_tools = ["nmap", "gobuster", "dirb", "nikto"]
    tools_status = {}
    
    for tool in essential_tools:
        try:
            result = execute_command(f"which {tool}")
            tools_status[tool] = result["success"]
        except:
            tools_status[tool] = False
    
    all_essential_tools_available = all(tools_status.values())
    
    return jsonify({
        "status": "healthy",
        "message": "Kali Linux Tools API Server is running",
        "tools_status": tools_status,
        "all_essential_tools_available": all_essential_tools_available
    })

@app.route("/mcp/capabilities", methods=["GET"])
def get_capabilities():
    # Return tool capabilities similar to our existing MCP server
    pass

@app.route("/mcp/tools/kali_tools/<tool_name>", methods=["POST"])
def execute_tool(tool_name):
    # Direct tool execution without going through the API server
    pass

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run the Kali Linux API Server")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--port", type=int, default=API_PORT, help=f"Port for the API server (default: {API_PORT})")
    parser.add_argument("--ip", type=str, default="127.0.0.1", help="IP address to bind the server to (default: 127.0.0.1 for localhost only)")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    
    # Set configuration from command line arguments
    if args.debug:
        DEBUG_MODE = True
        os.environ["DEBUG_MODE"] = "1"
        logger.setLevel(logging.DEBUG)
    
    if args.port != API_PORT:
        API_PORT = args.port
    
    logger.info(f"Starting Kali Linux Tools API Server on {args.ip}:{API_PORT}")
    app.run(host=args.ip, port=API_PORT, debug=DEBUG_MODE)
