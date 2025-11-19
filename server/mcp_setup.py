"""MCP Server setup and configuration"""
import os

from mcp.server.fastmcp import FastMCP
from .tools import *


def setup_mcp_server(kali_client):
    """
    Set up the MCP server with all tool functions
    
    Args:
        kali_client: Initialized KaliToolsClient instance
        
    Returns:
        Configured FastMCP instance
    """
    port = int(os.environ.get("MCP_STREAMABLE_HTTP_PORT", os.environ.get("MCP_PORT", 5002)))
    
    mcp = FastMCP(
        "Kali-Linux-MCP", 
        instructions="This is a comprehensive MCP server for Kali Linux security tools. It provides access to 60+ penetration testing and security assessment tools organized by category.",
        port=port,
    )
    
    # Network Scanning Tools
    register_nmap_tool(mcp, kali_client)
    register_masscan_tool(mcp, kali_client)
    register_netdiscover_tool(mcp, kali_client)
    register_hping3_tool(mcp, kali_client)
    register_unicornscan_tool(mcp, kali_client)
    register_arping_tool(mcp, kali_client)
    register_tcpdump_tool(mcp, kali_client)
    register_tshark_tool(mcp, kali_client)
    
    # Web Application Security Tools
    register_gobuster_tool(mcp, kali_client)
    register_dirb_tool(mcp, kali_client)
    register_nikto_tool(mcp, kali_client)
    register_wpscan_tool(mcp, kali_client)
    register_sqlmap_tool(mcp, kali_client)
    register_zap_tool(mcp, kali_client)
    register_wfuzz_tool(mcp, kali_client)
    register_ffuf_tool(mcp, kali_client)
    register_whatweb_tool(mcp, kali_client)
    register_sublist3r_tool(mcp, kali_client)
    register_amass_tool(mcp, kali_client)
    register_wapiti_tool(mcp, kali_client)
    register_commix_tool(mcp, kali_client)
    register_xsstrike_tool(mcp, kali_client)
    register_skipfish_tool(mcp, kali_client)
    
    # Password Cracking Tools
    register_hydra_tool(mcp, kali_client)
    register_john_tool(mcp, kali_client)
    register_hashcat_tool(mcp, kali_client)
    register_medusa_tool(mcp, kali_client)
    register_crackmapexec_tool(mcp, kali_client)
    register_patator_tool(mcp, kali_client)
    register_fcrackzip_tool(mcp, kali_client)
    
    # Exploitation Tools
    register_metasploit_tool(mcp, kali_client)
    register_searchsploit_tool(mcp, kali_client)
    register_beef_tool(mcp, kali_client)
    register_setoolkit_tool(mcp, kali_client)
    register_routersploit_tool(mcp, kali_client)
    
    # Wireless Attack Tools
    register_aircrack_tool(mcp, kali_client)
    register_reaver_tool(mcp, kali_client)
    register_bully_tool(mcp, kali_client)
    register_wifite_tool(mcp, kali_client)
    register_kismet_tool(mcp, kali_client)
    
    # Windows/Active Directory Tools
    register_enum4linux_tool(mcp, kali_client)
    register_responder_tool(mcp, kali_client)
    register_impacket_tool(mcp, kali_client)
    register_evil_winrm_tool(mcp, kali_client)
    register_kerbrute_tool(mcp, kali_client)
    register_mimikatz_tool(mcp, kali_client)
    
    # Information Gathering Tools
    register_theharvester_tool(mcp, kali_client)
    register_reconng_tool(mcp, kali_client)
    register_shodan_tool(mcp, kali_client)
    register_spiderfoot_tool(mcp, kali_client)
    register_dnsenum_tool(mcp, kali_client)
    register_fierce_tool(mcp, kali_client)
    register_dnsrecon_tool(mcp, kali_client)
    register_whois_tool(mcp, kali_client)
    register_metagoofil_tool(mcp, kali_client)
    
    # Shell & Persistence Tools
    register_weevely_tool(mcp, kali_client)
    register_netcat_tool(mcp, kali_client)
    register_socat_tool(mcp, kali_client)
    register_msfvenom_tool(mcp, kali_client)
    
    # Vulnerability Scanning Tools
    register_openvas_tool(mcp, kali_client)
    register_nuclei_tool(mcp, kali_client)
    register_lynis_tool(mcp, kali_client)
    
    # Database Tools
    register_nosqlmap_tool(mcp, kali_client)
    
    # Forensics Tools
    register_binwalk_tool(mcp, kali_client)
    register_foremost_tool(mcp, kali_client)
    
    # Anonymity & Proxy Tools
    register_proxychains_tool(mcp, kali_client)
    
    # Mobile & API Testing Tools
    register_apktool_tool(mcp, kali_client)
    
    # Utility Tools
    register_health_tool(mcp, kali_client)
    register_command_tool(mcp, kali_client)
    
    return mcp
