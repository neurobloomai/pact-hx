"""
PACT-HX Mental Health Expression
Expressing epistemic states in therapeutic contexts
CRITICAL: Safety-first approach with high epistemic standards
"""

from typing import Optional
from .base import ExpressionStrategy, ExpressionContext
import sys
sys.path.append('..')
from pact_ax.primitives.epistemic import EpistemicState, ConfidenceLevel


class MentalHealthExpression(ExpressionStrategy):
    """
    Mental health expression strategy.
    Highest epistemic standards - lives depend on humility.
    """
    
    # Confidence threshold for mental health is HIGHER
    SAFE_CONFIDENCE_THRESHOLD = 0.8  # vs 0.6 in other domains
    
    # Therapeutic language templates
    CONFIDENT_TEMPLATES = [
        "Based on our work together, {answer}. How does that resonate with you?",
        "From what we've explored in our sessions, {answer}. What are your thoughts on that?",
        "{answer}. I'm curious how this sits with you?",
    ]
    
    UNCERTAIN_TEMPLATES = [
        "I have some thoughts on this ({partial_answer}), but this really warrants discussion with your therapist who knows your full history.",
        "While I can share some general observations ({partial_answer}), your therapist would be better positioned to help you explore this deeply.",
        "This touches on areas where professional clinical insight is important. I can offer {partial_answer}, but I strongly encourage discussing this with your therapist.",
    ]
    
    UNKNOWN_TEMPLATES = [
        "This is outside my scope as a support tool. I recommend bringing this up with your therapist in your next session.",
        "This really needs professional clinical expertise. Please discuss this with your therapist who can give you the care you need.",
        "I'm not equipped to address this appropriately. Your therapist is the right person to help you with this.",
    ]
    
    # Crisis keywords that always trigger immediate escalation
    CRISIS_KEYWORDS = [
        'suicide', 'suicidal', 'kill myself', 'end my life',
        'hurt myself', 'self-harm', 'cut myself',
        'overdose', 'dying', 'want to die'
    ]
    
    # Topics that ALWAYS require human therapist
    HUMAN_REQUIRED_TOPICS = [
        'diagnosis', 'medication', 'emergency', 'crisis',
        'severe symptoms', 'hospitalization', 'therapy changes'
    ]
    
    def express_confident(self, state: EpistemicState, context: ExpressionContext) -> str:
        """
        Express confident response in therapeutic context.
        Even high confidence includes invitation for user reflection.
        """
        # Mental health ALWAYS invites collaboration
        template = self.CONFIDENT_TEMPLATES[0]
        message = template.format(answer=state.value)
        
        # Add therapeutic framing
        message = self._add_therapeutic_frame(message, state)
        
        return message
    
    def express_uncertain(self, state: EpistemicState, context: ExpressionContext) -> str:
        """
        Express uncertain response in therapeutic context.
        High bar for uncertainty - defer quickly.
        """
        partial_answer = state.value if state.value else "general reflections"
        
        template = self.UNCERTAIN_TEMPLATES[1]  # Default to middle ground
        message = template.format(partial_answer=partial_answer)
        
        # Add emphasis on human therapist importance
        message += " Your therapeutic relationship is the most important resource here."
        
        return message
    
    def express_unknown(self, state: EpistemicState, context: ExpressionContext) -> str:
        """
        Express 'I don't know' in therapeutic context.
        Clear boundaries, immediate referral.
        """
        template = self.UNKNOWN_TEMPLATES[0]
        message = template
        
        # Add reason if available
        if state.uncertainty_reason:
            message += f" ({state.uncertainty_reason})"
        
        # Always provide crisis resources as backup
        message += "\n\nIf this is urgent, please reach out to your therapist directly or contact a crisis line."
        
        return message
    
    def express_delegation(self, state: EpistemicState, delegate_to: str, context: ExpressionContext) -> str:
        """
        Express delegation in therapeutic context.
        Warm, supportive handoff to human clinician.
        """
        message = f"I think it's important that you discuss this with {delegate_to}. "
        message += "They have the clinical expertise and knowledge of your situation to help you properly. "
        message += "Would you like me to help you prepare some notes for that conversation?"
        
        return message
    
    def check_for_crisis(self, user_input: str) -> tuple[bool, Optional[str]]:
        """
        Check if user input indicates crisis.
        Returns (is_crisis, crisis_type)
        """
        user_input_lower = user_input.lower()
        
        for keyword in self.CRISIS_KEYWORDS:
            if keyword in user_input_lower:
                return True, "immediate_danger"
        
        return False, None
    
    def generate_crisis_response(self) -> str:
        """
        Generate immediate crisis response.
        No epistemic uncertainty here - just safety.
        """
        return """I'm concerned about your safety. Please:

1. Call 988 (Suicide & Crisis Lifeline) - available 24/7
2. Text "HELLO" to 741741 (Crisis Text Line)
3. Call 911 if you're in immediate danger
4. Go to your nearest emergency room

Your life matters. Please reach out for help right now."""
    
    def check_requires_human(self, topic: str) -> bool:
        """
        Check if topic absolutely requires human therapist.
        No AI should handle these, regardless of confidence.
        """
        topic_lower = topic.lower()
        
        for required_topic in self.HUMAN_REQUIRED_TOPICS:
            if required_topic in topic_lower:
                return True
        
        return False
    
    def _add_therapeutic_frame(self, message: str, state: EpistemicState) -> str:
        """
        Add therapeutic framing that invites collaboration.
        Never authoritative, always collaborative.
        """
        # Add source transparency if relevant
        if state.source and "session" in state.source:
            prefix = "Reflecting on our previous conversations, "
            message = prefix + message
        
        return message


class TherapeuticSafety:
    """
    Safety guardrails for mental health AI.
    Errs on side of caution, always.
    """
    
    def __init__(self):
        self.safety_log = []
        self.escalation_count = 0
    
    def safety_check(
        self,
        state: EpistemicState,
        user_input: str,
        context: ExpressionContext
    ) -> tuple[bool, str, Optional[str]]:
        """
        Comprehensive safety check.
        Returns (is_safe_to_respond, safety_level, override_message)
        """
        # Crisis check
        expression = MentalHealthExpression()
        is_crisis, crisis_type = expression.check_for_crisis(user_input)
        
        if is_crisis:
            self.log_safety_event("CRISIS_DETECTED", user_input, state)
            return False, "CRISIS", expression.generate_crisis_response()
        
        # Check if topic requires human
        if expression.check_requires_human(user_input):
            self.log_safety_event("HUMAN_REQUIRED", user_input, state)
            override = "This topic requires discussion with a licensed therapist. I'm not qualified to address this properly."
            return False, "HUMAN_REQUIRED", override
        
        # Check confidence threshold
        if state.confidence.value < expression.SAFE_CONFIDENCE_THRESHOLD:
            self.log_safety_event("LOW_CONFIDENCE", user_input, state)
            # Don't override, but flag for uncertain expression
            return True, "LOW_CONFIDENCE", None
        
        # Safe to proceed
        return True, "SAFE", None
    
    def log_safety_event(self, event_type: str, user_input: str, state: EpistemicState):
        """Log safety-related events for review"""
        self.safety_log.append({
            'event_type': event_type,
            'confidence': state.confidence.value,
            'user_input_length': len(user_input),  # Don't log actual content for privacy
            'timestamp': state.timestamp
        })
        
        if event_type in ["CRISIS_DETECTED", "HUMAN_REQUIRED"]:
            self.escalation_count += 1
    
    def get_safety_metrics(self) -> dict:
        """Analytics on safety guardrails"""
        if not self.safety_log:
            return {"message": "No safety events"}
        
        return {
            'total_safety_events': len(self.safety_log),
            'crisis_detections': sum(1 for e in self.safety_log if e['event_type'] == 'CRISIS_DETECTED'),
            'human_required': sum(1 for e in self.safety_log if e['event_type'] == 'HUMAN_REQUIRED'),
            'low_confidence': sum(1 for e in self.safety_log if e['event_type'] == 'LOW_CONFIDENCE'),
            'total_escalations': self.escalation_count
        }
