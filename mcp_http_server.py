#!/usr/bin/env python3

"""
MCP HTTP Server - Exposes MCP protocol over HTTP/SSE
Bridges Cursor (via HTTP) to Kali Linux API Server
"""

import sys
import os
import argparse
import logging

from server import KaliToolsClient, DEFAULT_REQUEST_TIMEOUT

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Default configuration
DEFAULT_KALI_SERVER = os.environ.get("KALI_SERVER", "http://localhost:5001")
DEFAULT_MCP_PORT = os.environ.get("MCP_PORT", 5002)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run the Kali MCP HTTP Server")
    parser.add_argument("--kali-server", type=str, default=DEFAULT_KALI_SERVER, 
                      help=f"Kali API server URL (default: {DEFAULT_KALI_SERVER})")
    parser.add_argument("--port", type=int, default=DEFAULT_MCP_PORT,
                      help=f"Port for MCP HTTP server (default: {DEFAULT_MCP_PORT})")
    parser.add_argument("--host", type=str, default="0.0.0.0",
                      help="Host to bind the server to (default: 0.0.0.0)")
    parser.add_argument("--timeout", type=int, default=DEFAULT_REQUEST_TIMEOUT,
                      help=f"Request timeout in seconds (default: {DEFAULT_REQUEST_TIMEOUT})")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    return parser.parse_args()

def main():
    """Main entry point for the MCP HTTP server."""
    args = parse_args()
    
    # Set environment variables BEFORE any MCP imports - FastMCP reads these at startup
    os.environ["MCP_STREAMABLE_HTTP_HOST"] = args.host
    os.environ["MCP_STREAMABLE_HTTP_PORT"] = str(args.port)
    
    # Import server module AFTER setting environment variables
    from server import setup_mcp_server
    
    # Configure logging based on debug flag
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")
    
    # Initialize the Kali Tools client
    kali_client = KaliToolsClient(args.kali_server, args.timeout)
    
    # Check server health and log the result
    health = kali_client.check_health()
    if "error" in health:
        logger.warning(f"Unable to connect to Kali API server at {args.kali_server}: {health['error']}")
        logger.warning("MCP server will start, but tool execution may fail")
    else:
        logger.info(f"Successfully connected to Kali API server at {args.kali_server}")
        logger.info(f"Server health status: {health['status']}")
        if not health.get("all_essential_tools_available", False):
            logger.warning("Not all essential tools are available on the Kali server")
            missing_tools = [tool for tool, available in health.get("tools_status", {}).items() if not available]
            if missing_tools:
                logger.warning(f"Missing tools: {', '.join(missing_tools)}")
    
    # Set up and run the MCP server
    mcp = setup_mcp_server(kali_client)
    logger.info(f"Starting Kali MCP HTTP server on {args.host}:{args.port}")
    
    # Run with streamable HTTP transport
    mcp.run(transport="sse")

if __name__ == "__main__":
    main()

