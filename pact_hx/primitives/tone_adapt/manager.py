# pact_hx/primitives/tone_adapt/manager.py
import uuid
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from collections import defaultdict, Counter

from .schemas import (
    ToneDimension, ToneProfile, ToneContext, ToneAdjustment, 
    ToneCalibration, ToneState
)

class ToneAdaptationManager:
    """
    Sovereign Tone Adaptation Primitive for PACT-HX
    
    Philosophy: Powerful alone, transcendent when collaborating
    - Adapts communication style independently using user feedback
    - Enhances adaptation using attention, memory, and value signals
    - Maintains baseline personality while contextually adapting
    """
    
    def __init__(self, agent_id: str, user_id: str = None, enable_collaboration: bool = False):
        self.agent_id = agent_id
        self.user_id = user_id or agent_id
        
        # Initialize with neutral baseline tone
        baseline_tone = {
            ToneDimension.FORMALITY: 0.0,
            ToneDimension.DIRECTNESS: 0.0,
            ToneDimension.ENTHUSIASM: 0.0,
            ToneDimension.TECHNICAL_DEPTH: 0.0,
            ToneDimension.EMOTIONAL_WARMTH: 0.0,
            ToneDimension.CONFIDENCE: 0.0,
            ToneDimension.PACE: 0.0,
            ToneDimension.HUMOR: 0.0
        }
        
        self.state = ToneState(
            agent_id=agent_id,
            user_profile=ToneProfile(
                user_id=self.user_id,
                baseline_preferences=baseline_tone
            ),
            collaboration_enabled=enable_collaboration
        )
        
        self.collaboration_interfaces = {}
        
        # Adaptation parameters
        self.learning_rate = 0.1
        self.adaptation_threshold = 0.3
        self.confidence_decay = 0.05
    
    # ========== CORE INDEPENDENT FUNCTIONALITY ==========
    
    def adapt_tone(
        self, 
        context: ToneContext,
        user_feedback: Optional[str] = None,
        **collaboration_hints
    ) -> ToneAdjustment:
        """
        Adapt communication tone - sovereign operation with optional collaboration
        """
        
        # Calculate base tone adjustment from context
        base_adjustment = self._calculate_contextual_tone(context)
        
        # Apply collaboration enhancements if enabled
        if self.state.collaboration_enabled and collaboration_hints:
            base_adjustment = self._enhance_with_collaboration(base_adjustment, collaboration_hints)
        
        # Apply user feedback learning
        if user_feedback:
            base_adjustment = self._apply_feedback_learning(base_adjustment, user_feedback)
        
        # Create tone adjustment
        adjustment = ToneAdjustment(
            adjustment_id=str(uuid.uuid4()),
            target_dimensions=base_adjustment,
            context=context,
            confidence=self._calculate_adjustment_confidence(base_adjustment, context),
            reasoning=self._generate_reasoning(base_adjustment, context)
        )
        
        # Store current adjustment
        self.state.current_adjustment = adjustment
        self.state.total_adjustments += 1
        
        # Update user profile based on successful patterns
        self._update_user_profile(adjustment)
        
        return adjustment
    
    def get_current_tone(self) -> Dict[ToneDimension, float]:
        """Get current tone settings - standalone capability"""
        
        if self.state.current_adjustment:
            return self.state.current_adjustment.target_dimensions.copy()
        else:
            return self.state.user_profile.baseline_preferences.copy()
    
    def provide_feedback(self, feedback_type: str, feedback_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Learn from user feedback - core adaptation intelligence
        """
        
        if not self.state.current_adjustment:
            return {"error": "No current adjustment to provide feedback on"}
        
        # Update current adjustment with feedback
        self.state.current_adjustment.user_feedback = feedback_type
        
        if feedback_type == "positive":
            self.state.current_adjustment.effectiveness_score = 0.8
            self.state.calibration_data.successful_adjustments.append(self.state.current_adjustment)
            self._reinforce_successful_pattern()
        elif feedback_type == "negative":
            self.state.current_adjustment.effectiveness_score = 0.2
            self.state.calibration_data.failed_adjustments.append(self.state.current_adjustment)
            self._learn_from_failure()
        else:  # neutral
            self.state.current_adjustment.effectiveness_score = 0.5
        
        # Update adaptation accuracy
        self._update_adaptation_metrics()
        
        return {
            "feedback_processed": True,
            "adjustment_id": self.state.current_adjustment.adjustment_id,
            "learning_applied": feedback_type in ["positive", "negative"],
            "new_adaptation_accuracy": self.state.adaptation_accuracy
        }
    
    def generate_style_guidance(self, content: str) -> Dict[str, Any]:
        """
        Generate style guidance for content based on current tone - standalone capability
        """
        
        current_tone = self.get_current_tone()
        
        guidance = {
            "tone_adjustments": current_tone,
            "style_recommendations": {},
            "confidence": self.state.user_profile.confidence_score
        }
        
        # Generate specific style recommendations
        for dimension, value in current_tone.items():
            guidance["style_recommendations"][dimension.value] = self._get_style_recommendation(dimension, value)
        
        # Content-specific adjustments
        content_analysis = self._analyze_content_requirements(content)
        guidance["content_specific"] = content_analysis
        
        return guidance
    
    def get_adaptation_summary(self) -> Dict[str, Any]:
        """Get adaptation performance summary - standalone diagnostics"""
        
        return {
            "user_id": self.user_id,
            "total_adjustments": self.state.total_adjustments,
            "adaptation_accuracy": self.state.adaptation_accuracy,
            "user_satisfaction_trend": self.state.user_satisfaction_trend,
            "profile_confidence": self.state.user_profile.confidence_score,
            "successful_patterns": len(self.state.calibration_data.successful_adjustments),
            "failed_patterns": len(self.state.calibration_data.failed_adjustments),
            "baseline_preferences": self.state.user_profile.baseline_preferences,
            "collaboration_enabled": self.state.collaboration_enabled,
            "active_partnerships": self.state.primitive_partnerships
        }
    
    # ========== COLLABORATION INTERFACES ==========
    
    def enable_collaboration_with(self, primitive_type: str, primitive_instance: Any):
        """Enable collaboration with another PACT primitive"""
        self.state.collaboration_enabled = True
        self.collaboration_interfaces[primitive_type] = primitive_instance
        if primitive_type not in self.state.primitive_partnerships:
            self.state.primitive_partnerships.append(primitive_type)
    
    def share_tone_context(self) -> Dict[str, Any]:
        """Share current tone context with other primitives"""
        current_tone = self.get_current_tone()
        
        return {
            "current_tone_profile": current_tone,
            "user_communication_preferences": self.state.user_profile.baseline_preferences,
            "emotional_adaptability": {
                "warmth_preference": current_tone.get(ToneDimension.EMOTIONAL_WARMTH, 0.0),
                "enthusiasm_level": current_tone.get(ToneDimension.ENTHUSIASM, 0.0),
                "formality_preference": current_tone.get(ToneDimension.FORMALITY, 0.0)
            },
            "adaptation_confidence": self.state.user_profile.confidence_score,
            "context_sensitivity": self.state.user_profile.adaptation_sensitivity
        }
    
    def receive_collaboration_signal(self, primitive_type: str, signal_data: Dict[str, Any]):
        """Receive and process signals from other primitives"""
        if not self.state.collaboration_enabled:
            return
        
        if primitive_type == "attention":
            # Attention signals help adjust enthusiasm and pace based on user focus
            self._process_attention_signals(signal_data)
        elif primitive_type == "memory":
            # Memory signals help maintain consistent tone based on past interactions
            self._process_memory_signals(signal_data)
        elif primitive_type == "values":
            # Value signals help adjust formality and directness appropriately
            self._process_value_signals(signal_data)
    
    # ========== INTERNAL HELPER METHODS ==========
    
    def _calculate_contextual_tone(self, context: ToneContext) -> Dict[ToneDimension, float]:
        """Calculate tone adjustment based on context - core intelligence"""
        
        # Start with baseline preferences
        adjusted_tone = self.state.user_profile.baseline_preferences.copy()
        
        # Apply contextual modifications
        if context.conversation_type:
            contextual_mods = self._get_conversation_type_modifiers(context.conversation_type)
            for dimension, modifier in contextual_mods.items():
                adjusted_tone[dimension] = self._blend_values(
                    adjusted_tone[dimension], modifier, 0.3
                )
        
        if context.user_emotional_state:
            emotional_mods = self._get_emotional_state_modifiers(context.user_emotional_state)
            for dimension, modifier in emotional_mods.items():
                adjusted_tone[dimension] = self._blend_values(
                    adjusted_tone[dimension], modifier, 0.4
                )
        
        if context.topic_domain:
            domain_mods = self._get_topic_domain_modifiers(context.topic_domain)
            for dimension, modifier in domain_mods.items():
                adjusted_tone[dimension] = self._blend_values(
                    adjusted_tone[dimension], modifier, 0.2
                )
        
        if context.urgency_level:
            urgency_mods = self._get_urgency_modifiers(context.urgency_level)
            for dimension, modifier in urgency_mods.items():
                adjusted_tone[dimension] = self._blend_values(
                    adjusted_tone[dimension], modifier, 0.5
                )
        
        # Ensure values stay within bounds
        for dimension in adjusted_tone:
            adjusted_tone[dimension] = max(-1.0, min(1.0, adjusted_tone[dimension]))
        
        return adjusted_tone
    
    def _enhance_with_collaboration(self, base_tone: Dict[ToneDimension, float], hints: Dict[str, Any]) -> Dict[ToneDimension, float]:
        """Enhance tone with collaboration signals"""
        enhanced_tone = base_tone.copy()
        
        # Attention collaboration
        if "attention_context" in hints:
            attention_data = hints["attention_context"]
            # High attention -> more enthusiasm and pace
            if attention_data.get("focus_intensity", 0) > 0.7:
                enhanced_tone[ToneDimension.ENTHUSIASM] += 0.2
                enhanced_tone[ToneDimension.PACE] += 0.1
            # Low attention -> more warmth and slower pace
            elif attention_data.get("focus_intensity", 0) < 0.3:
                enhanced_tone[ToneDimension.EMOTIONAL_WARMTH] += 0.2
                enhanced_tone[ToneDimension.PACE] -= 0.2
        
        # Memory collaboration
        if "memory_context" in hints:
            memory_data = hints["memory_context"]
            # Established relationship -> more casual, confident
            if memory_data.get("interaction_count", 0) > 10:
                enhanced_tone[ToneDimension.FORMALITY] -= 0.1
                enhanced_tone[ToneDimension.CONFIDENCE] += 0.1
            # Recent positive interactions -> more warmth
            if memory_data.get("recent_sentiment", "neutral") == "positive":
                enhanced_tone[ToneDimension.EMOTIONAL_WARMTH] += 0.1
                enhanced_tone[ToneDimension.HUMOR] += 0.1
        
        # Value collaboration
        if "value_context" in hints:
            value_data = hints["value_context"]
            # High value alignment -> more confident, direct
            if value_data.get("alignment_score", 0) > 0.8:
                enhanced_tone[ToneDimension.CONFIDENCE] += 0.1
                enhanced_tone[ToneDimension.DIRECTNESS] += 0.1
        
        # Ensure bounds
        for dimension in enhanced_tone:
            enhanced_tone[dimension] = max(-1.0, min(1.0, enhanced_tone[dimension]))
        
        return enhanced_tone
    
    def _apply_feedback_learning(self, base_tone: Dict[ToneDimension, float], feedback: str) -> Dict[ToneDimension, float]:
        """Apply learning from user feedback"""
        learned_tone = base_tone.copy()
        
        # Simple feedback learning
        if feedback == "too_formal":
            learned_tone[ToneDimension.FORMALITY] -= self.learning_rate
        elif feedback == "too_casual":
            learned_tone[ToneDimension.FORMALITY] += self.learning_rate
        elif feedback == "too_direct":
            learned_tone[ToneDimension.DIRECTNESS] -= self.learning_rate
        elif feedback == "too_indirect":
            learned_tone[ToneDimension.DIRECTNESS] += self.learning_rate
        elif feedback == "more_enthusiasm":
            learned_tone[ToneDimension.ENTHUSIASM] += self.learning_rate
        elif feedback == "less_enthusiasm":
            learned_tone[ToneDimension.ENTHUSIASM] -= self.learning_rate
        elif feedback == "more_warmth":
            learned_tone[ToneDimension.EMOTIONAL_WARMTH] += self.learning_rate
        elif feedback == "more_technical":
            learned_tone[ToneDimension.TECHNICAL_DEPTH] += self.learning_rate
        elif feedback == "less_technical":
            learned_tone[ToneDimension.TECHNICAL_DEPTH] -= self.learning_rate
        
        return learned_tone
    
    def _calculate_adjustment_confidence(self, adjustment: Dict[ToneDimension, float], context: ToneContext) -> float:
        """Calculate confidence in tone adjustment"""
        
        # Base confidence from user profile
        base_confidence = self.state.user_profile.confidence_score
        
        # Adjust based on context clarity
        context_clarity = 0.5
        if context.conversation_type:
            context_clarity += 0.1
        if context.user_emotional_state:
            context_clarity += 0.2
        if context.topic_domain:
            context_clarity += 0.1
        if context.urgency_level:
            context_clarity += 0.1
        
        # Adjust based on how much we're changing from baseline
        change_magnitude = sum(
            abs(adjustment[dim] - self.state.user_profile.baseline_preferences[dim])
            for dim in adjustment
        ) / len(adjustment)
        
        confidence = (base_confidence + context_clarity) * (1 - change_magnitude * 0.3)
        return max(0.0, min(1.0, confidence))
    
    def _generate_reasoning(self, adjustment: Dict[ToneDimension, float], context: ToneContext) -> str:
        """Generate human-readable reasoning for tone adjustment"""
        
        significant_changes = []
        for dimension, value in adjustment.items():
            baseline = self.state.user_profile.baseline_preferences[dimension]
            change = abs(value - baseline)
            if change > 0.2:
                direction = "increased" if value > baseline else "decreased"
                significant_changes.append(f"{dimension.value} {direction}")
        
        reasoning_parts = []
        
        if context.conversation_type:
            reasoning_parts.append(f"Adjusted for {context.conversation_type} conversation")
        
        if context.user_emotional_state:
            reasoning_parts.append(f"Responding to user's {context.user_emotional_state} state")
        
        if context.urgency_level and context.urgency_level in ["high", "urgent"]:
            reasoning_parts.append("Increased directness and pace for urgency")
        
        if significant_changes:
            reasoning_parts.append(f"Key changes: {', '.join(significant_changes)}")
        
        return "; ".join(reasoning_parts) if reasoning_parts else "Maintaining baseline tone"
    
    def _blend_values(self, base: float, modifier: float, strength: float) -> float:
        """Blend base value with modifier using specified strength"""
        return base + (modifier - base) * strength
    
    def _get_conversation_type_modifiers(self, conv_type: str) -> Dict[ToneDimension, float]:
        """Get tone modifiers for conversation type"""
        modifiers = {
            "professional": {
                ToneDimension.FORMALITY: 0.6,
                ToneDimension.CONFIDENCE: 0.4,
                ToneDimension.HUMOR: -0.3
            },
            "casual": {
                ToneDimension.FORMALITY: -0.4,
                ToneDimension.EMOTIONAL_WARMTH: 0.3,
                ToneDimension.HUMOR: 0.2
            },
            "support": {
                ToneDimension.EMOTIONAL_WARMTH: 0.6,
                ToneDimension.DIRECTNESS: -0.2,
                ToneDimension.PACE: -0.3
            },
            "teaching": {
                ToneDimension.TECHNICAL_DEPTH: 0.4,
                ToneDimension.CONFIDENCE: 0.3,
                ToneDimension.PACE: -0.2
            }
        }
        return modifiers.get(conv_type, {})
    
    def _get_emotional_state_modifiers(self, emotional_state: str) -> Dict[ToneDimension, float]:
        """Get tone modifiers for user emotional state"""
        modifiers = {
            "frustrated": {
                ToneDimension.EMOTIONAL_WARMTH: 0.4,
                ToneDimension.PACE: -0.3,
                ToneDimension.DIRECTNESS: -0.2
            },
            "excited": {
                ToneDimension.ENTHUSIASM: 0.5,
                ToneDimension.PACE: 0.3,
                ToneDimension.HUMOR: 0.2
            },
            "confused": {
                ToneDimension.TECHNICAL_DEPTH: -0.3,
                ToneDimension.PACE: -0.4,
                ToneDimension.EMOTIONAL_WARMTH: 0.3
            },
            "happy": {
                ToneDimension.EMOTIONAL_WARMTH: 0.3,
                ToneDimension.HUMOR: 0.2,
                ToneDimension.ENTHUSIASM: 0.2
            }
        }
        return modifiers.get(emotional_state, {})
    
    def _get_topic_domain_modifiers(self, domain: str) -> Dict[ToneDimension, float]:
        """Get tone modifiers for topic domain"""
        modifiers = {
            "technical": {
                ToneDimension.TECHNICAL_DEPTH: 0.4,
                ToneDimension.CONFIDENCE: 0.2,
                ToneDimension.FORMALITY: 0.2
            },
            "personal": {
                ToneDimension.EMOTIONAL_WARMTH: 0.4,
                ToneDimension.FORMALITY: -0.3,
                ToneDimension.DIRECTNESS: -0.2
            },
            "creative": {
                ToneDimension.ENTHUSIASM: 0.3,
                ToneDimension.HUMOR: 0.2,
                ToneDimension.FORMALITY: -0.2
            }
        }
        return modifiers.get(domain, {})
    
    def _get_urgency_modifiers(self, urgency: str) -> Dict[ToneDimension, float]:
        """Get tone modifiers for urgency level"""
        modifiers = {
            "high": {
                ToneDimension.DIRECTNESS: 0.4,
                ToneDimension.PACE: 0.3,
                ToneDimension.CONFIDENCE: 0.2
            },
            "urgent": {
                ToneDimension.DIRECTNESS: 0.6,
                ToneDimension.PACE: 0.5,
                ToneDimension.FORMALITY: -0.2
            },
            "low": {
                ToneDimension.PACE: -0.2,
                ToneDimension.EMOTIONAL_WARMTH: 0.2
            }
        }
        return modifiers.get(urgency, {})
    
    def _get_style_recommendation(self, dimension: ToneDimension, value: float) -> str:
        """Get style recommendation for dimension value"""
        
        recommendations = {
            ToneDimension.FORMALITY: {
                (-1.0, -0.3): "Use casual language, contractions, informal expressions",
                (-0.3, 0.3): "Balance formal and casual elements as appropriate",
                (0.3, 1.0): "Use professional language, proper grammar, formal structure"
            },
            ToneDimension.DIRECTNESS: {
                (-1.0, -0.3): "Use diplomatic language, soften statements, include qualifiers",
                (-0.3, 0.3): "Be clear but considerate in communication",
                (0.3, 1.0): "Be direct and straightforward, get to the point quickly"
            },
            ToneDimension.ENTHUSIASM: {
                (-1.0, -0.3): "Maintain reserved, measured tone",
                (-0.3, 0.3): "Show moderate interest and engagement",
                (0.3, 1.0): "Express excitement, use energetic language, show passion"
            },
            ToneDimension.EMOTIONAL_WARMTH: {
                (-1.0, -0.3): "Maintain professional distance, focus on facts",
                (-0.3, 0.3): "Show appropriate empathy and understanding",
                (0.3, 1.0): "Express care, use supportive language, acknowledge emotions"
            }
        }
        
        if dimension in recommendations:
            for (low, high), recommendation in recommendations[dimension].items():
                if low <= value <= high:
                    return recommendation
        
        return f"Adjust {dimension.value} to level {value:.1f}"
    
    def _analyze_content_requirements(self, content: str) -> Dict[str, Any]:
        """Analyze content for specific tone requirements"""
        
        analysis = {
            "recommended_adjustments": {},
            "content_type": "general",
            "complexity_level": "medium"
        }
        
        # Simple content analysis
        if len(content.split()) > 100:
            analysis["recommended_adjustments"][ToneDimension.PACE] = -0.2
            analysis["complexity_level"] = "high"
        
        if any(word in content.lower() for word in ["error", "problem", "issue", "help"]):
            analysis["recommended_adjustments"][ToneDimension.EMOTIONAL_WARMTH] = 0.3
            analysis["content_type"] = "support"
        
        if any(word in content.lower() for word in ["excited", "amazing", "great", "awesome"]):
            analysis["recommended_adjustments"][ToneDimension.ENTHUSIASM] = 0.2
            analysis["content_type"] = "positive"
        
        return analysis
    
    # Placeholder methods for full implementation
    def _update_user_profile(self, adjustment: ToneAdjustment):
        """Update user profile based on successful adjustment"""
        # Implement profile learning logic
        pass
    
    def _reinforce_successful_pattern(self):
        """Reinforce successful tone patterns"""
        # Implement pattern reinforcement
        pass
    
    def _learn_from_failure(self):
        """Learn from failed tone adjustments"""
        # Implement failure learning
        pass
    
    def _update_adaptation_metrics(self):
        """Update adaptation performance metrics"""
        # Calculate new accuracy based on recent feedback
        recent_adjustments = self.state.calibration_data.successful_adjustments[-10:]
        if recent_adjustments:
            success_rate = len([a for a in recent_adjustments if a.effectiveness_score > 0.6]) / len(recent_adjustments)
            self.state.adaptation_accuracy = success_rate
    
    def _process_attention_signals(self, signal_data: Dict[str, Any]):
        """Process attention collaboration signals"""
        # Implement attention signal processing
        pass
    
    def _process_memory_signals(self, signal_data: Dict[str, Any]):
        """Process memory collaboration signals"""
        # Implement memory signal processing
        pass
    
    def _process_value_signals(self, signal_data: Dict[str, Any]):
        """Process value alignment signals"""
        # Implement value signal processing
        pass
