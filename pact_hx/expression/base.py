"""
PACT-HX Base Expression Framework
Translate epistemic states into human-appropriate communication
"""

from typing import Dict, Optional, Protocol
from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod

import sys
sys.path.append('..')
from pact_ax.primitives.epistemic import EpistemicState, ConfidenceLevel


class CommunicationStyle(Enum):
    """Different styles for expressing uncertainty"""
    PROFESSIONAL = "professional"      # Formal, clear
    CONVERSATIONAL = "conversational"  # Natural, friendly
    CLINICAL = "clinical"              # Therapeutic, careful
    TECHNICAL = "technical"            # Precise, detailed


class Domain(Enum):
    """Application domains with different expression needs"""
    CUSTOMER_CARE = "customer_care"
    MENTAL_HEALTH = "mental_health"
    VOICE_AI = "voice_ai"
    EDUCATION = "education"
    HEALTHCARE = "healthcare"
    LEGAL = "legal"


@dataclass
class ExpressionContext:
    """
    Context for how to express epistemic state.
    Different domains need different expressions.
    """
    domain: Domain
    style: CommunicationStyle
    user_expertise: str = "general"  # general, intermediate, expert
    urgency: str = "normal"  # low, normal, high, critical
    previous_interactions: int = 0
    user_preferences: Dict = None
    
    def __post_init__(self):
        if self.user_preferences is None:
            self.user_preferences = {}


class ExpressionStrategy(ABC):
    """
    Base class for domain-specific expression strategies.
    Each domain implements how to express uncertainty appropriately.
    """
    
    @abstractmethod
    def express_confident(self, state: EpistemicState, context: ExpressionContext) -> str:
        """Express high-confidence response"""
        pass
    
    @abstractmethod
    def express_uncertain(self, state: EpistemicState, context: ExpressionContext) -> str:
        """Express uncertain response"""
        pass
    
    @abstractmethod
    def express_unknown(self, state: EpistemicState, context: ExpressionContext) -> str:
        """Express 'I don't know' response"""
        pass
    
    @abstractmethod
    def express_delegation(self, state: EpistemicState, delegate_to: str, context: ExpressionContext) -> str:
        """Express need to delegate"""
        pass


class BaseExpression:
    """
    Core expression engine.
    Routes to appropriate strategy based on domain and confidence.
    """
    
    def __init__(self):
        self.strategies: Dict[Domain, ExpressionStrategy] = {}
    
    def register_strategy(self, domain: Domain, strategy: ExpressionStrategy):
        """Register domain-specific expression strategy"""
        self.strategies[domain] = strategy
    
    def express(
        self,
        state: EpistemicState,
        context: ExpressionContext,
        delegate_to: Optional[str] = None
    ) -> str:
        """
        Main entry point for expressing epistemic state.
        Routes to appropriate strategy and confidence level.
        """
        # Get strategy for domain
        strategy = self.strategies.get(context.domain)
        if not strategy:
            raise ValueError(f"No strategy registered for domain: {context.domain}")
        
        # Route based on confidence level
        if delegate_to:
            return strategy.express_delegation(state, delegate_to, context)
        elif state.confidence == ConfidenceLevel.UNKNOWN:
            return strategy.express_unknown(state, context)
        elif state.confidence.value < 0.6:
            return strategy.express_uncertain(state, context)
        else:
            return strategy.express_confident(state, context)
    
    def add_empathy(self, message: str, context: ExpressionContext) -> str:
        """
        Add empathetic framing when appropriate.
        Especially important for mental health and customer care.
        """
        if context.domain in [Domain.MENTAL_HEALTH, Domain.CUSTOMER_CARE]:
            empathy_phrases = [
                "I understand this is important to you. ",
                "I appreciate you bringing this up. ",
                "Thank you for your patience. "
            ]
            # Simple heuristic - could be more sophisticated
            if context.urgency in ["high", "critical"]:
                return empathy_phrases[0] + message
        
        return message
    
    def adjust_for_expertise(self, message: str, context: ExpressionContext) -> str:
        """
        Adjust technical depth based on user expertise.
        Experts get more detail, general users get clarity.
        """
        # This is simplified - real implementation would be more nuanced
        if context.user_expertise == "expert":
            # Add technical details
            return message
        elif context.user_expertise == "general":
            # Simplify language
            return message
        
        return message
