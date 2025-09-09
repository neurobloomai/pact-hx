"""
PACT-HX: Human Experience Layer

Provides primitives for personalized AI interactions:
- Attention management
- Memory persistence  
- Tone adaptation
- Value alignment
"""

from .version import __version__
from .core.base_primitive import PACTPrimitive, PACTConfig
from .primitives.attention import AttentionManager
from .primitives.memory import MemoryManager
from .primitives.tone_adapt import ToneAdaptationManager
from .primitives.value_align import ValueAlignmentManager

__all__ = [
    "__version__",
    "PACTPrimitive", 
    "PACTConfig",
    "AttentionManager",
    "MemoryManager", 
    "ToneAdaptationManager",
    "ValueAlignmentManager",
]
