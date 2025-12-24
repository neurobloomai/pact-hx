"""
PACT-HX Expression Orchestrator
Coordinates expression strategies and handles cross-cutting concerns
"""

from typing import Optional, Dict
from .base import BaseExpression, ExpressionContext, Domain, CommunicationStyle
from .customer_care import CustomerCareExpression, CustomerCareEscalation
from .mental_health import MentalHealthExpression, TherapeuticSafety
from .voice_ai import VoiceAIExpression, VoiceConfidenceIndicators

import sys
sys.path.append('..')
from pact_ax.primitives.epistemic import EpistemicState


class ExpressionOrchestrator:
    """
    Main orchestrator for PACT-HX expression layer.
    Routes to appropriate domain strategy and applies cross-cutting concerns.
    """
    
    def __init__(self):
        self.base = BaseExpression()
        self.safety_checker = TherapeuticSafety()
        
        # Register all domain strategies
        self._register_strategies()
    
    def _register_strategies(self):
        """Register all available expression strategies"""
        self.base.register_strategy(Domain.CUSTOMER_CARE, CustomerCareExpression())
        self.base.register_strategy(Domain.MENTAL_HEALTH, MentalHealthExpression())
        self.base.register_strategy(Domain.VOICE_AI, VoiceAIExpression())
        # Add more domains as needed
    
    def express(
        self,
        state: EpistemicState,
        context: ExpressionContext,
        user_input: Optional[str] = None,
        delegate_to: Optional[str] = None
    ) -> Dict:
        """
        Main entry point for expression.
        Returns dict with message and metadata.
        """
        # Safety check for mental health
        if context.domain == Domain.MENTAL_HEALTH and user_input:
            is_safe, safety_level, override_message = self.safety_checker.safety_check(
                state, user_input, context
            )
            
            if not is_safe:
                return {
                    'message': override_message,
                    'safety_override': True,
                    'safety_level': safety_level,
                    'should_escalate': True
                }
        
        # Check if should escalate (customer care)
        if context.domain == Domain.CUSTOMER_CARE:
            escalator = CustomerCareEscalation()
            should_escalate, reason = escalator.should_escalate(state, context)
            
            if should_escalate:
                escalation_message = escalator.generate_escalation_message(state, context, reason)
                return {
                    'message': escalation_message,
                    'should_escalate': True,
                    'escalation_reason': reason
                }
        
        # Normal expression flow
        message = self.base.express(state, context, delegate_to)
        
        # Add empathy if appropriate
        message = self.base.add_empathy(message, context)
        
        # Adjust for user expertise
        message = self.base.adjust_for_expertise(message, context)
        
        # Add confidence indicators for voice
        if context.domain == Domain.VOICE_AI:
            message = VoiceConfidenceIndicators.add_hedging(message, state.confidence)
            verification_prompt = VoiceConfidenceIndicators.suggest_verification(state.confidence)
            if verification_prompt:
                message += " " + verification_prompt
        
        return {
            'message': message,
            'confidence': state.confidence.value,
            'should_escalate': False,
            'delegate_to': delegate_to
        }
    
    def batch_express(
        self,
        states: list[EpistemicState],
        context: ExpressionContext
    ) -> list[Dict]:
        """Express multiple epistemic states (for multi-turn conversations)"""
        return [self.express(state, context) for state in states]
