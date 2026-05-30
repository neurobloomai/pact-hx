"""
PACT-HX: Human Experience Layer

Provides two complementary aspects of human-AI interaction:

1. PERSONALIZATION - Adapting to individual users
   - Attention management
   - Memory persistence  
   - Tone adaptation
   - Value alignment

2. EPISTEMIC EXPRESSION - Communicating uncertainty appropriately
   - Domain-specific humility templates
   - Safety-first escalation patterns
   - Confidence translation to natural language
   - Graceful delegation and escalation

Both are essential for human-centered AI systems.
"""

from .version import __version__

# Core primitives
from .core.base_primitive import PACTPrimitive, PACTConfig

# Memory primitive
from .primitives.memory.manager import MemoryManager
from .primitives.memory.schemas import (
    MemoryEntry, MemoryType, EmotionalValence,
)

__all__ = [
    "__version__",
    "PACTPrimitive",
    "PACTConfig",
    "MemoryManager",
    "MemoryEntry",
    "MemoryType",
    "EmotionalValence",
]
