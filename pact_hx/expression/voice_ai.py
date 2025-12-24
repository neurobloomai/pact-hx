"""
PACT-HX Voice AI Expression
Expressing epistemic states in conversational voice interfaces
"""

from .base import ExpressionStrategy, ExpressionContext
import sys
sys.path.append('..')
from pact_ax.primitives.epistemic import EpistemicState, ConfidenceLevel


class VoiceAIExpression(ExpressionStrategy):
    """
    Voice AI expression strategy.
    Natural conversation with appropriate hedging.
    """
    
    # Voice-appropriate templates (shorter, more natural)
    CONFIDENT_TEMPLATES = [
        "{answer}",
        "Yes, {answer}",
        "Sure, {answer}",
        "Absolutely. {answer}"
    ]
    
    MODERATE_TEMPLATES = [
        "I think {answer}, though I'm not completely certain.",
        "Based on what I know, {answer}. Want me to double-check that?",
        "I believe {answer}, but let me verify to be sure.",
        "{answer} - at least that's my understanding. Should I confirm that?"
    ]
    
    UNCERTAIN_TEMPLATES = [
        "I'm not sure about that. Let me look it up for you.",
        "I don't have reliable information on that. Want me to search?",
        "That's outside what I know well. I can search for current information if you'd like.",
        "I'm not confident about my answer there. Let me find accurate information."
    ]
    
    UNKNOWN_TEMPLATES = [
        "I don't know that one. Let me search for you.",
        "I'm not sure. Want me to look that up?",
        "I don't have that information. Should I find it?",
        "That's not something I know. I can search if you want."
    ]
    
    def express_confident(self, state: EpistemicState, context: ExpressionContext) -> str:
        """Express confident response in voice context"""
        template = self._select_natural_template(self.CONFIDENT_TEMPLATES, state)
        message = template.format(answer=state.value)
        
        # Keep it conversational and brief
        return message
    
    def express_uncertain(self, state: EpistemicState, context: ExpressionContext) -> str:
        """Express uncertain response in voice context"""
        template = self._select_natural_template(self.MODERATE_TEMPLATES, state)
        message = template.format(answer=state.value if state.value else "this")
        
        return message
    
    def express_unknown(self, state: EpistemicState, context: ExpressionContext) -> str:
        """Express 'I don't know' in voice context"""
        template = self._select_natural_template(self.UNKNOWN_TEMPLATES, state)
        message = template
        
        # Offer to search or get more info
        return message
    
    def express_delegation(self, state: EpistemicState, delegate_to: str, context: ExpressionContext) -> str:
        """Express delegation in voice context"""
        if delegate_to == "search":
            return "Let me search for that information."
        elif delegate_to == "human":
            return "Let me connect you with someone who can help better."
        else:
            return f"Let me transfer you to {delegate_to}."
    
    def _select_natural_template(self, templates: list, state: EpistemicState) -> str:
        """
        Select template that sounds most natural.
        Could be based on conversation flow, user patterns, etc.
        """
        # Simple selection - could use more sophisticated NLU
        return templates[0]
    
    def add_conversational_markers(self, message: str, context: ExpressionContext) -> str:
        """
        Add natural conversational markers.
        Makes voice sound more human-like.
        """
        # Add thinking markers for uncertain responses
        if "not sure" in message or "don't know" in message:
            message = "Hmm. " + message
        
        # Add confirming markers for confident responses
        # (but not overused - that sounds robotic)
        
        return message


class VoiceConfidenceIndicators:
    """
    Subtle ways to indicate confidence in voice.
    Prosody, hedging, qualifiers.
    """
    
    @staticmethod
    def add_hedging(message: str, confidence: ConfidenceLevel) -> str:
        """
        Add appropriate hedging based on confidence.
        Voice equivalent of confidence display.
        """
        if confidence == ConfidenceLevel.CERTAIN:
            # No hedging
            return message
        
        elif confidence == ConfidenceLevel.CONFIDENT:
            # Minimal hedging
            hedges = ["I believe", "I think", "As far as I know"]
            # Could add hedge to beginning
            return message
        
        elif confidence == ConfidenceLevel.MODERATE:
            # Clear hedging
            hedges = ["I'm fairly sure", "I think", "probably", "likely"]
            return message
        
        elif confidence == ConfidenceLevel.LOW:
            # Strong hedging
            hedges = ["I'm not sure, but", "I think maybe", "possibly"]
            return message
        
        else:  # UNKNOWN
            # Explicit uncertainty
            return "I don't know. " + message
    
    @staticmethod
    def suggest_verification(confidence: ConfidenceLevel) -> str:
        """
        Suggest verification for lower confidence.
        Collaborative uncertainty handling.
        """
        if confidence.value < 0.6:
            return "Want me to verify that?"
        elif confidence.value < 0.8:
            return "Should I double-check?"
        else:
            return ""


class VoiceErrorRecovery:
    """
    Handle errors and misunderstandings gracefully in voice.
    """
    
    @staticmethod
    def handle_misunderstanding(state: EpistemicState) -> str:
        """When AI realizes it misunderstood"""
        return "Actually, I think I misunderstood. Could you rephrase that?"
    
    @staticmethod
    def handle_clarification_needed(state: EpistemicState) -> str:
        """When AI needs more info"""
        clarifications = [
            "Can you tell me more about that?",
            "Could you be more specific?",
            "What aspect are you most interested in?"
        ]
        return clarifications[0]
    
    @staticmethod
    def handle_out_of_domain(state: EpistemicState) -> str:
        """When query is outside capabilities"""
        return "That's outside what I can help with, but I can try to find resources for you."
