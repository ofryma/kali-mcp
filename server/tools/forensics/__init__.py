"""Forensics tools package"""

from .binwalk import register_binwalk_tool
from .foremost import register_foremost_tool

__all__ = [
    'register_binwalk_tool',
    'register_foremost_tool',
]

