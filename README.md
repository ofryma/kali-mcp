# Kali Linux MCP Server

A Model Context Protocol (MCP) server that exposes 60+ Kali Linux security tools through an AI-friendly interface. Enables AI assistants like Claude to perform penetration testing and security assessments.

## Features

**Network Scanning**: nmap, masscan, netdiscover, hping3, tcpdump, tshark  
**Web Security**: gobuster, nikto, sqlmap, wpscan, burpsuite, zap, ffuf, nuclei  
**Password Cracking**: hydra, john, hashcat, medusa, crackmapexec  
**Exploitation**: metasploit, searchsploit, beef, routersploit  
**Wireless**: aircrack-ng, reaver, wifite, kismet  
**Windows/AD**: enum4linux, impacket, evil-winrm, kerbrute, mimikatz, responder  
**OSINT**: theharvester, shodan, spiderfoot, amass, sublist3r  
**Forensics**: binwalk, foremost  
**Plus**: shells (netcat, socat, msfvenom), anonymity (proxychains), mobile (apktool)

## Quick Start

### Docker (Recommended)

```bash
# Start Kali API server
make run

# Or manually
docker-compose up -d
python mcp_http_server.py
```

### Manual Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run Kali API server (requires Kali Linux)
python kali_server.py

# Run MCP HTTP server
python mcp_http_server.py --kali-server http://localhost:5001
```

### Configure Cursor/Claude

Add to your MCP settings:

```json
{
  "mcpServers": {
    "kali-tools": {
      "url": "http://localhost:5002/sse"
    }
  }
}
```

## Architecture

- **kali_server.py**: Flask REST API exposing Kali tools
- **mcp_http_server.py**: MCP-over-HTTP bridge to Kali API
- **server/tools/**: Tool implementations organized by category
- **Docker**: Kali Linux container with all tools pre-installed

## Requirements

- Python 3.8+
- Docker (for containerized deployment)
- Kali Linux environment (for manual setup)

## Testing

The project includes a comprehensive test suite using pytest.

### Quick Start

```bash
# Setup test environment
./scripts/setup_tests.sh

# Run all tests
make test

# Run with coverage
make test-coverage

# Run only unit tests (fast)
make test-unit

# Run integration tests
make test-integration
```

### Test Structure

```
tests/
├── test_kali_client.py           # HTTP client tests
├── test_kali_server.py           # Flask API endpoint tests
├── test_command_executor.py      # Command execution tests
├── test_mcp_server.py            # MCP server setup tests
├── test_integration.py           # Integration tests
└── test_tools/                   # Tool-specific tests
    ├── test_network_scanning.py
    ├── test_web_scanning.py
    └── test_password_cracking.py
```

### Available Test Commands

```bash
make test              # Run all tests
make test-unit         # Run unit tests only
make test-integration  # Run integration tests only
make test-coverage     # Run tests with coverage report
make test-file FILE=tests/test_kali_client.py  # Run specific file
make clean             # Clean up test artifacts
make help              # Show all available commands
```

### Coverage Reports

After running `make test-coverage`, view the HTML report:
```bash
open htmlcov/index.html
```

### Continuous Integration

Tests run automatically on GitHub Actions for:
- Multiple Python versions (3.9, 3.10, 3.11, 3.12)
- Every push to main/develop branches
- All pull requests

See [tests/README.md](tests/README.md) for detailed testing documentation.

## License

MIT License - See LICENSE file
