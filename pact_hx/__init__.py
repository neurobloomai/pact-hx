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

# Personalization layer (existing work)
from .personalization.attention import AttentionManager
from .personalization.memory import MemoryManager
from .personalization.tone_adapt import ToneAdaptationManager
from .personalization.value_align import ValueAlignmentManager

# Expression layer (new work)
from .expression.base import ExpressionContext, Domain, CommunicationStyle
from .expression.orchestrator import ExpressionOrchestrator
from .expression.customer_care import CustomerCareExpression, CustomerCareEscalation
from .expression.mental_health import MentalHealthExpression, TherapeuticSafety
from .expression.voice_ai import VoiceAIExpression, VoiceConfidenceIndicators

__all__ = [
    # Version
    "__version__",
    
    # Core
    "PACTPrimitive",
    "PACTConfig",
    
    # Personalization
    "AttentionManager",
    "MemoryManager",
    "ToneAdaptationManager",
    "ValueAlignmentManager",
    
    # Expression
    "ExpressionOrchestrator",
    "ExpressionContext",
    "Domain",
    "CommunicationStyle",
    "CustomerCareExpression",
    "CustomerCareEscalation",
    "MentalHealthExpression",
    "TherapeuticSafety",
    "VoiceAIExpression",
    "VoiceConfidenceIndicators",
]
