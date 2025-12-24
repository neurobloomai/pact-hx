"""
PACT-HX Customer Care Expression
Expressing epistemic states in customer support contexts
"""

from typing import Dict
from .base import ExpressionStrategy, ExpressionContext, CommunicationStyle
import sys
sys.path.append('..')
from pact_ax.primitives.epistemic import EpistemicState, ConfidenceLevel


class CustomerCareExpression(ExpressionStrategy):
    """
    Customer care expression strategy.
    Balance helpfulness with honesty about limitations.
    """
    
    # Template library for different confidence levels
    CONFIDENT_TEMPLATES = [
        "I can help you with that. {answer}",
        "Yes, I have that information. {answer}",
        "Here's what you need to know: {answer}",
        "{answer}"
    ]
    
    MODERATE_TEMPLATES = [
        "Based on my information, {answer}. However, I recommend confirming this with {verification_source}.",
        "I believe {answer}, though I suggest verifying with a specialist to be certain.",
        "From what I know, {answer}. If you need more specific details, I can connect you with {specialist}.",
    ]
    
    UNCERTAIN_TEMPLATES = [
        "I have limited information on this. {partial_answer}. Let me connect you with someone who can provide more complete details.",
        "I'm not entirely certain about this. What I can tell you is {partial_answer}, but I'd recommend speaking with {specialist} for accurate information.",
        "This is outside my area of expertise. I can give you general information ({partial_answer}), but {specialist} would be better equipped to help.",
    ]
    
    UNKNOWN_TEMPLATES = [
        "I don't have that specific information. Let me connect you with {specialist} who can help.",
        "I'm not able to answer that accurately. Would you like me to transfer you to {specialist}?",
        "That's not information I have access to, but {specialist} can definitely help you with that.",
        "I want to make sure you get accurate information, so let me route you to {specialist} who specializes in this area."
    ]
    
    DELEGATION_TEMPLATES = [
        "For the best assistance with this, I'm connecting you with {delegate_name} from our {department} team.",
        "Let me transfer you to {delegate_name}, who specializes in {expertise} and can give you accurate information.",
        "{delegate_name} from {department} will be better equipped to help you with this specific issue.",
    ]
    
    def express_confident(self, state: EpistemicState, context: ExpressionContext) -> str:
        """Express confident response in customer care context"""
        template = self._select_template(self.CONFIDENT_TEMPLATES, context)
        
        # Format the response
        message = template.format(answer=state.value)
        
        # Add empathy if urgency is high
        if context.urgency in ["high", "critical"]:
            message = "I understand this is important. " + message
        
        return message
    
    def express_uncertain(self, state: EpistemicState, context: ExpressionContext) -> str:
        """Express uncertain response in customer care context"""
        # Determine what partial information we can provide
        partial_answer = state.value if state.value else "some general guidance"
        
        # Suggest specialist based on domain
        specialist = self._suggest_specialist(context)
        
        template = self._select_template(self.UNCERTAIN_TEMPLATES, context)
        message = template.format(
            partial_answer=partial_answer,
            specialist=specialist
        )
        
        # Add empathy for uncertain situations
        message = "I want to make sure you get the right information. " + message
        
        return message
    
    def express_unknown(self, state: EpistemicState, context: ExpressionContext) -> str:
        """Express 'I don't know' in customer care context"""
        specialist = self._suggest_specialist(context)
        
        template = self._select_template(self.UNKNOWN_TEMPLATES, context)
        message = template.format(specialist=specialist)
        
        # Add reason for not knowing if available
        if state.uncertainty_reason:
            message += f" ({state.uncertainty_reason})"
        
        return message
    
    def express_delegation(self, state: EpistemicState, delegate_to: str, context: ExpressionContext) -> str:
        """Express delegation in customer care context"""
        # Parse delegate info
        delegate_info = self._parse_delegate_info(delegate_to)
        
        template = self._select_template(self.DELEGATION_TEMPLATES, context)
        message = template.format(
            delegate_name=delegate_info['name'],
            department=delegate_info['department'],
            expertise=delegate_info['expertise']
        )
        
        # Add warm handoff language
        message += " They'll take great care of you."
        
        return message
    
    def _select_template(self, templates: list, context: ExpressionContext) -> str:
        """Select appropriate template based on context"""
        # Simple selection - could be more sophisticated
        if context.style == CommunicationStyle.PROFESSIONAL:
            return templates[0]
        elif context.style == CommunicationStyle.CONVERSATIONAL:
            return templates[-1] if len(templates) > 1 else templates[0]
        else:
            return templates[0]
    
    def _suggest_specialist(self, context: ExpressionContext) -> str:
        """Suggest appropriate specialist based on context"""
        # This would be domain-specific in real implementation
        specialist_map = {
            "billing": "our billing specialist",
            "technical": "our technical support team",
            "account": "our account specialist",
            "product": "our product expert"
        }
        
        # Default
        return "a specialist"
    
    def _parse_delegate_info(self, delegate_to: str) -> Dict[str, str]:
        """Parse delegate string into structured info"""
        # Simplified - real implementation would have better parsing
        return {
            'name': delegate_to,
            'department': "specialist team",
            'expertise': "this area"
        }


class CustomerCareEscalation:
    """
    Handles escalation patterns in customer care.
    When and how to escalate based on epistemic state.
    """
    
    def __init__(self):
        self.escalation_log = []
    
    def should_escalate(
        self,
        state: EpistemicState,
        context: ExpressionContext
    ) -> tuple[bool, str]:
        """
        Determine if situation requires escalation.
        Returns (should_escalate, reason)
        """
        # Always escalate for critical urgency with uncertainty
        if context.urgency == "critical" and state.confidence.value < 0.8:
            return True, "Critical issue requires high-confidence response"
        
        # Escalate if completely unknown
        if state.confidence == ConfidenceLevel.UNKNOWN:
            return True, "Agent has no information on this topic"
        
        # Escalate if repeated interactions without resolution
        if context.previous_interactions > 3 and state.confidence.value < 0.7:
            return True, "Multiple interactions without resolution"
        
        # Don't escalate if confident
        if state.confidence.value >= 0.7:
            return False, "Sufficient confidence to handle"
        
        # Moderate case - offer escalation as option
        if state.confidence.value < 0.5:
            return True, "Low confidence suggests specialist needed"
        
        return False, "Can handle with expressed uncertainty"
    
    def generate_escalation_message(
        self,
        state: EpistemicState,
        context: ExpressionContext,
        escalation_reason: str
    ) -> str:
        """Generate appropriate escalation message"""
        messages = {
            "Critical issue requires high-confidence response": 
                "Given the importance of this issue, I want to make sure you get the most accurate help. Let me connect you with a senior specialist.",
            
            "Agent has no information on this topic":
                "I don't have the information you need, but I can connect you with someone who does.",
            
            "Multiple interactions without resolution":
                "I want to make sure we resolve this for you. Let me bring in a specialist who can provide more detailed assistance.",
            
            "Low confidence suggests specialist needed":
                "To give you the best service, I'd like to connect you with a specialist who can address this more thoroughly."
        }
        
        return messages.get(escalation_reason, "Let me connect you with someone who can better assist you.")
    
    def log_escalation(
        self,
        state: EpistemicState,
        context: ExpressionContext,
        reason: str,
        escalated_to: str
    ):
        """Log escalation for analytics"""
        self.escalation_log.append({
            'confidence': state.confidence.value,
            'domain': context.domain.value,
            'urgency': context.urgency,
            'reason': reason,
            'escalated_to': escalated_to,
            'interaction_count': context.previous_interactions
        })
