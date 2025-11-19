"""Password Cracking tools package"""

from .hydra import register_hydra_tool
from .john import register_john_tool
from .hashcat import register_hashcat_tool
from .medusa import register_medusa_tool
from .crackmapexec import register_crackmapexec_tool
from .patator import register_patator_tool
from .fcrackzip import register_fcrackzip_tool

__all__ = [
    'register_hydra_tool',
    'register_john_tool',
    'register_hashcat_tool',
    'register_medusa_tool',
    'register_crackmapexec_tool',
    'register_patator_tool',
    'register_fcrackzip_tool',
]

