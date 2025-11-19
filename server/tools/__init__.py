"""MCP Tools package - organized security tool implementations"""

# Network Scanning
from .network_scanning import (
    register_nmap_tool,
    register_masscan_tool,
    register_netdiscover_tool,
    register_hping3_tool,
    register_unicornscan_tool,
    register_arping_tool,
    register_tcpdump_tool,
    register_tshark_tool,
)

# Web Application Security
from .web_scanning import (
    register_gobuster_tool,
    register_dirb_tool,
    register_nikto_tool,
    register_wpscan_tool,
    register_sqlmap_tool,
    register_zap_tool,
    register_wfuzz_tool,
    register_ffuf_tool,
    register_whatweb_tool,
    register_sublist3r_tool,
    register_amass_tool,
    register_wapiti_tool,
    register_commix_tool,
    register_xsstrike_tool,
    register_skipfish_tool,
)

# Password Cracking
from .password_cracking import (
    register_hydra_tool,
    register_john_tool,
    register_hashcat_tool,
    register_medusa_tool,
    register_crackmapexec_tool,
    register_patator_tool,
    register_fcrackzip_tool,
)

# Exploitation
from .exploitation import (
    register_metasploit_tool,
    register_searchsploit_tool,
    register_beef_tool,
    register_setoolkit_tool,
    register_routersploit_tool,
)

# Wireless Attacks
from .wireless import (
    register_aircrack_tool,
    register_reaver_tool,
    register_bully_tool,
    register_wifite_tool,
    register_kismet_tool,
)

# Windows/Active Directory
from .windows_ad import (
    register_enum4linux_tool,
    register_responder_tool,
    register_impacket_tool,
    register_evil_winrm_tool,
    register_kerbrute_tool,
    register_mimikatz_tool,
)

# Information Gathering
from .information_gathering import (
    register_theharvester_tool,
    register_reconng_tool,
    register_shodan_tool,
    register_spiderfoot_tool,
    register_dnsenum_tool,
    register_fierce_tool,
    register_dnsrecon_tool,
    register_whois_tool,
    register_metagoofil_tool,
)

# Shells & Persistence
from .shells import (
    register_weevely_tool,
    register_netcat_tool,
    register_socat_tool,
    register_msfvenom_tool,
)

# Vulnerability Scanning
from .vulnerability_scanning import (
    register_openvas_tool,
    register_nuclei_tool,
    register_lynis_tool,
)

# Database
from .database import (
    register_nosqlmap_tool,
)

# Forensics
from .forensics import (
    register_binwalk_tool,
    register_foremost_tool,
)

# Anonymity & Proxy
from .anonymity import (
    register_proxychains_tool,
)

# Mobile & API Testing
from .mobile import (
    register_apktool_tool,
)

# Utility tools
from .health import register_health_tool
from .command import register_command_tool

__all__ = [
    # Network Scanning
    'register_nmap_tool',
    'register_masscan_tool',
    'register_netdiscover_tool',
    'register_hping3_tool',
    'register_unicornscan_tool',
    'register_arping_tool',
    'register_tcpdump_tool',
    'register_tshark_tool',
    
    # Web Application Security
    'register_gobuster_tool',
    'register_dirb_tool',
    'register_nikto_tool',
    'register_wpscan_tool',
    'register_sqlmap_tool',
    'register_zap_tool',
    'register_wfuzz_tool',
    'register_ffuf_tool',
    'register_whatweb_tool',
    'register_sublist3r_tool',
    'register_amass_tool',
    'register_wapiti_tool',
    'register_commix_tool',
    'register_xsstrike_tool',
    'register_skipfish_tool',
    
    # Password Cracking
    'register_hydra_tool',
    'register_john_tool',
    'register_hashcat_tool',
    'register_medusa_tool',
    'register_crackmapexec_tool',
    'register_patator_tool',
    'register_fcrackzip_tool',
    
    # Exploitation
    'register_metasploit_tool',
    'register_searchsploit_tool',
    'register_beef_tool',
    'register_setoolkit_tool',
    'register_routersploit_tool',
    
    # Wireless Attacks
    'register_aircrack_tool',
    'register_reaver_tool',
    'register_bully_tool',
    'register_wifite_tool',
    'register_kismet_tool',
    
    # Windows/Active Directory
    'register_enum4linux_tool',
    'register_responder_tool',
    'register_impacket_tool',
    'register_evil_winrm_tool',
    'register_kerbrute_tool',
    'register_mimikatz_tool',
    
    # Information Gathering
    'register_theharvester_tool',
    'register_reconng_tool',
    'register_shodan_tool',
    'register_spiderfoot_tool',
    'register_dnsenum_tool',
    'register_fierce_tool',
    'register_dnsrecon_tool',
    'register_whois_tool',
    'register_metagoofil_tool',
    
    # Shells & Persistence
    'register_weevely_tool',
    'register_netcat_tool',
    'register_socat_tool',
    'register_msfvenom_tool',
    
    # Vulnerability Scanning
    'register_openvas_tool',
    'register_nuclei_tool',
    'register_lynis_tool',
    
    # Database
    'register_nosqlmap_tool',
    
    # Forensics
    'register_binwalk_tool',
    'register_foremost_tool',
    
    # Anonymity & Proxy
    'register_proxychains_tool',
    
    # Mobile & API Testing
    'register_apktool_tool',
    
    # Utility
    'register_health_tool',
    'register_command_tool',
]
