"""Shells & Persistence tools package"""

from .weevely import register_weevely_tool
from .netcat import register_netcat_tool
from .socat import register_socat_tool
from .msfvenom import register_msfvenom_tool

__all__ = [
    'register_weevely_tool',
    'register_netcat_tool',
    'register_socat_tool',
    'register_msfvenom_tool',
]

