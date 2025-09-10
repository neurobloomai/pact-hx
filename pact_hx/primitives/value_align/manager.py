# pact_hx/primitives/value_align/manager.py
"""
PACT-HX Value Alignment Manager

Core implementation of the value alignment primitive for ethical constraint
and alignment checking in AI systems. This is the ethical foundation that
ensures all AI decisions and behaviors align with human values.

Architecture: Sovereign primitive with collaboration interfaces
- Works powerfully alone (independent ethical reasoning)
- Provides ethical constraints and guidance to other primitives
- Learns from user feedback and ethical outcomes
- Adapts to cultural and personal value contexts
"""

import time
import re
import uuid
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Set, Union
from collections import defaultdict, Counter
import logging

from .schemas import (
    ValueDomain, ValuePriority, ConflictSeverity, ConflictResolution,
    ValueConstraint, ValueConflict, ValueAlignment, ValueDetectionRule,
    ValueAlignmentConfiguration, ValueAlignmentState,
    ValueAlignmentResponse, ValueConflictResponse, ValueContextResponse
)

logger = logging.getLogger(__name__)

class ValueAlignmentManager:
    """
    Sovereign Value Alignment Primitive for PACT-HX
    
    The ethical foundation that ensures AI decisions align with human values.
    Provides value constraint checking, conflict resolution, and ethical
    guidance for all AI interactions.
    
    Core Capabilities:
    - Real-time value alignment assessment
    - Ethical conflict detection and resolution
    - Cultural and personal value adaptation
    - Collaborative ethical guidance for other primitives
    - Learning from ethical outcomes and feedback
    """
    
    def __init__(
        self,
        agent_id: str,
        user_id: Optional[str] = None,
        config: Optional[ValueAlignmentConfiguration] = None,
        enable_collaboration: bool = False
    ):
        self.agent_id = agent_id
        self.user_id = user_id or agent_id
        
        # Initialize state with configuration
        self.state = ValueAlignmentState(
            agent_id=agent_id,
            user_id=self.user_id,
            config=config or ValueAlignmentConfiguration(),
            collaboration_enabled=enable_collaboration
        )
        
        # Collaboration interfaces
        self.collaboration_interfaces = {}
        
        # Initialize with default value constraints and detection rules
        self._initialize_default_constraints()
        self._initialize_default_detection_rules()
        
        # Performance tracking
        self._last_performance_update = datetime.now()
        self._feedback_buffer = []
        
        logger.info(f"ValueAlignmentManager initialized for agent {agent_id}")
    
    # ========== CORE VALUE ALIGNMENT PROCESSING ==========
    
    def assess_value_alignment(
        self,
        proposed_action: str,
        context: str,
        entities_involved: Optional[List[str]] = None,
        stakeholders: Optional[List[str]] = None,
        **collaboration_hints
    ) -> ValueAlignmentResponse:
        """
        Assess how well a proposed action aligns with established values
        
        This is the primary interface for value alignment checking. It evaluates
        proposed actions against value constraints and detects potential conflicts.
        
        Args:
            proposed_action: Description of the action to assess
            context: Context in which the action would take place
            entities_involved: Entities that would be affected
            stakeholders: Stakeholders who might be impacted
            **collaboration_hints: Optional signals from other primitives
            
        Returns:
            ValueAlignmentResponse with alignment scores and recommendations
        """
        
        start_time = time.time()
        logger.debug(f"Assessing value alignment for action: {proposed_action[:50]}...")
        
        try:
            # 1. Create alignment assessment
            alignment = ValueAlignment(
                assessed_action=proposed_action,
                overall_score=0.0,
                confidence=0.0
            )
            
            # 2. Assess alignment across all value domains
            domain_assessments = self._assess_domain_alignment(
                proposed_action, context, entities_involved, stakeholders
            )
            
            # 3. Apply collaboration enhancements
            if self.state.collaboration_enabled and collaboration_hints:
                domain_assessments = self._enhance_with_collaboration(
                    domain_assessments, collaboration_hints
                )
            
            # 4. Calculate overall alignment score
            overall_score, confidence = self._calculate_overall_alignment(domain_assessments)
            alignment.overall_score = overall_score
            alignment.confidence = confidence
            alignment.domain_scores = {
                domain.value: score for domain, score in domain_assessments.items()
            }
            
            # 5. Detect potential conflicts
            conflicts = self._detect_value_conflicts(
                proposed_action, context, domain_assessments
            )
            
            # 6. Generate recommendations
            recommendations = self._generate_alignment_recommendations(
                alignment, domain_assessments, conflicts
            )
            
            # 7. Determine if attention is required
            requires_attention = (
                overall_score < 0.6 or 
                len(conflicts) > 0 or 
                confidence < 0.5 or
                any(severity in [ConflictSeverity.SEVERE, ConflictSeverity.MODERATE] 
                    for _, severity in conflicts)
            )
            
            # 8. Store alignment assessment
            alignment.positive_alignments = self._extract_positive_alignments(domain_assessments)
            alignment.negative_alignments = self._extract_negative_alignments(domain_assessments)
            alignment.improvement_suggestions = recommendations
            
            self.state.alignment_history.append(alignment)
            self.state.total_alignments_assessed += 1
            
            # 9. Manage history size
            if len(self.state.alignment_history) > 100:
                self.state.alignment_history = self.state.alignment_history[-50:]
            
            # 10. Update performance metrics
            self._update_performance_metrics()
            self.state.last_updated = datetime.now()
            
            processing_time = time.time() - start_time
            logger.debug(f"Value alignment assessment completed in {processing_time:.3f}s")
            
            return ValueAlignmentResponse(
                agent_id=self.agent_id,
                alignment_id=alignment.alignment_id,
                overall_score=overall_score,
                confidence=confidence,
                domain_scores=alignment.domain_scores,
                conflicts_detected=[conflict_id for conflict_id, _ in conflicts],
                recommendations=recommendations,
                requires_attention=requires_attention
            )
            
        except Exception as e:
            logger.error(f"Error assessing value alignment: {str(e)}")
            return ValueAlignmentResponse(
                agent_id=self.agent_id,
                alignment_id=str(uuid.uuid4()),
                overall_score=0.5,  # Neutral score on error
                confidence=0.0,
                domain_scores={},
                conflicts_detected=[],
                recommendations=["Error in alignment assessment - please review manually"],
                requires_attention=True
            )
    
    def resolve_value_conflict(
        self,
        conflict_id: str,
        resolution_choice: str,
        user_input: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Resolve a specific value conflict based on chosen strategy
        
        Args:
            conflict_id: ID of the conflict to resolve
            resolution_choice: Chosen resolution strategy
            user_input: Additional user input for resolution
            
        Returns:
            Dictionary with resolution results and outcomes
        """
        
        if conflict_id not in self.state.active_conflicts:
            return {
                "success": False,
                "error": "Conflict not found",
                "conflict_id": conflict_id
            }
        
        conflict = self.state.active_conflicts[conflict_id]
        
        try:
            # Execute resolution strategy
            resolution_outcome = self._execute_resolution_strategy(
                conflict, resolution_choice, user_input
            )
            
            # Update conflict with resolution
            conflict.resolved_at = datetime.now()
            conflict.resolution_outcome = resolution_outcome["outcome"]
            conflict.user_response = user_input.get("response") if user_input else None
            
            # Move to resolved conflicts
            self.state.resolved_conflicts.append(conflict)
            del self.state.active_conflicts[conflict_id]
            
            # Update performance metrics
            self.state.total_conflicts_resolved += 1
            self._update_resolution_success_rate(resolution_outcome["success"])
            
            # Learn from resolution
            self._learn_from_resolution(conflict, resolution_outcome)
            
            logger.info(f"Resolved conflict {conflict_id} with strategy {resolution_choice}")
            
            return {
                "success": True,
                "conflict_id": conflict_id,
                "resolution_strategy": resolution_choice,
                "outcome": resolution_outcome["outcome"],
                "lessons_learned": resolution_outcome.get("lessons", [])
            }
            
        except Exception as e:
            logger.error(f"Error resolving conflict {conflict_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "conflict_id": conflict_id
            }
    
    def update_user_values(
        self,
        value_updates: Dict[ValueDomain, float],
        context: Optional[str] = None,
        source: str = "user_explicit"
    ) -> Dict[str, Any]:
        """
        Update user's value profile based on explicit input or learned preferences
        
        Args:
            value_updates: Updates to value domain importance weights
            context: Context for the value update
            source: Source of the update (user_explicit, learned, inferred)
            
        Returns:
            Summary of value profile changes
        """
        
        try:
            changes_made = {}
            
            for domain, new_weight in value_updates.items():
                if isinstance(domain, str):
                    domain = ValueDomain(domain)
                    
                old_weight = self.state.user_value_profile.get(domain, 0.5)
                
                # Apply learning rate for non-explicit updates
                if source != "user_explicit":
                    learning_rate = self.state.config.learning_rate
                    blended_weight = old_weight * (1 - learning_rate) + new_weight * learning_rate
                    self.state.user_value_profile[domain] = blended_weight
                else:
                    self.state.user_value_profile[domain] = new_weight
                
                changes_made[domain.value] = {
                    "old_weight": old_weight,
                    "new_weight": self.state.user_value_profile[domain],
                    "change": self.state.user_value_profile[domain] - old_weight
                }
            
            # Update related constraints based on new value weights
            self._adjust_constraints_based_on_values()
            
            # Store value update for learning
            self._feedback_buffer.append({
                "timestamp": datetime.now(),
                "type": "value_update",
                "source": source,
                "changes": changes_made,
                "context": context
            })
            
            logger.info(f"Updated user value profile: {len(changes_made)} domains changed")
            
            return {
                "success": True,
                "changes_made": changes_made,
                "updated_profile": dict(self.state.user_value_profile),
                "context": context
            }
            
        except Exception as e:
            logger.error(f"Error updating user values: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    # ========== COLLABORATION INTERFACES ==========
    
    def enable_collaboration_with(self, primitive_type: str, primitive_instance: Any):
        """Enable collaboration with another PACT primitive"""
        self.state.collaboration_enabled = True
        self.collaboration_interfaces[primitive_type] = primitive_instance
        
        if primitive_type not in self.state.primitive_partnerships:
            self.state.primitive_partnerships.append(primitive_type)
            
        logger.info(f"Enabled collaboration with {primitive_type}")
    
    def share_ethical_context(self, context_type: str = "guidance") -> Dict[str, Any]:
        """
        Share ethical context and guidance with other primitives
        
        Primary collaboration interface - provides ethical constraints
        and guidance that other primitives can use in their processing.
        
        Args:
            context_type: Type of context to share
                - "guidance": General ethical guidance
                - "constraints": Specific constraints to apply
                - "risks": Ethical risks to be aware of
                - "opportunities": Opportunities to demonstrate values
        """
        
        try:
            if context_type == "guidance":
                return self._generate_ethical_guidance()
            elif context_type == "constraints":
                return self._generate_constraint_guidance()
            elif context_type == "risks":
                return self._generate_risk_guidance()
            elif context_type == "opportunities":
                return self._generate_opportunity_guidance()
            else:
                return self._generate_ethical_guidance()  # Default
                
        except Exception as e:
            logger.error(f"Error sharing ethical context: {str(e)}")
            return {
                "agent_id": self.agent_id,
                "ethical_significance": 0.5,
                "guidance": "Error generating ethical guidance",
                "error": str(e)
            }
    
    def receive_collaboration_signal(self, primitive_type: str, signal_data: Dict[str, Any]):
        """
        Process signals from other primitives for ethical consideration
        
        Allows other primitives to request ethical review of their
        proposed actions or share context that affects ethical decisions.
        """
        
        if not self.state.collaboration_enabled:
            logger.debug(f"Ignoring signal from {primitive_type} - collaboration disabled")
            return
        
        try:
            # Store signal with timestamp
            self.state.external_signals[primitive_type] = {
                "data": signal_data,
                "received_at": datetime.now(),
                "processed": False
            }
            
            # Process specific primitive signals
            if primitive_type == "attention":
                self._process_attention_signals(signal_data)
            elif primitive_type == "memory":
                self._process_memory_signals(signal_data)
            elif primitive_type == "tone":
                self._process_tone_signals(signal_data)
            else:
                logger.warning(f"Unknown primitive type for collaboration: {primitive_type}")
            
            # Mark as processed
            self.state.external_signals[primitive_type]["processed"] = True
            
            logger.debug(f"Processed collaboration signal from {primitive_type}")
            
        except Exception as e:
            logger.error(f"Error processing signal from {primitive_type}: {str(e)}")
    
    # ========== INTERNAL PROCESSING METHODS ==========
    
    def _assess_domain_alignment(
        self,
        proposed_action: str,
        context: str,
        entities_involved: Optional[List[str]] = None,
        stakeholders: Optional[List[str]] = None
    ) -> Dict[ValueDomain, float]:
        """Assess alignment across all value domains"""
        
        domain_scores = {}
        
        for domain in ValueDomain:
            score = self._assess_single_domain(
                domain, proposed_action, context, entities_involved, stakeholders
            )
            domain_scores[domain] = score
        
        return domain_scores
    
    def _assess_single_domain(
        self,
        domain: ValueDomain,
        proposed_action: str,
        context: str,
        entities_involved: Optional[List[str]] = None,
        stakeholders: Optional[List[str]] = None
    ) -> float:
        """Assess alignment for a single value domain"""
        
        # Get domain-specific constraints
        domain_constraints = [
            constraint for constraint in self.state.active_constraints.values()
            if constraint.domain == domain
        ]
        
        if not domain_constraints:
            return 0.7  # Neutral score when no constraints exist
        
        # Calculate alignment based on constraints
        alignment_scores = []
        
        for constraint in domain_constraints:
            constraint_score = self._evaluate_constraint_alignment(
                constraint, proposed_action, context
            )
            # Weight by constraint strength
            weighted_score = constraint_score * constraint.strength
            alignment_scores.append(weighted_score)
        
        # Apply domain-specific assessment logic
        domain_score = self._apply_domain_specific_logic(
            domain, proposed_action, context, alignment_scores
        )
        
        # Weight by user's importance of this domain
        user_importance = self.state.get_domain_importance(domain)
        final_score = domain_score * (0.5 + 0.5 * user_importance)
        
        return min(max(final_score, 0.0), 1.0)
    
    def _evaluate_constraint_alignment(
        self,
        constraint: ValueConstraint,
        proposed_action: str,
        context: str
    ) -> float:
        """Evaluate how well an action aligns with a specific constraint"""
        
        # Check for violation indicators
        violation_score = 0.0
        for indicator in constraint.violation_indicators:
            if self._matches_indicator(indicator, proposed_action, context):
                violation_score += 1.0
        
        # Check for positive indicators
        positive_score = 0.0
        for indicator in constraint.positive_indicators:
            if self._matches_indicator(indicator, proposed_action, context):
                positive_score += 1.0
        
        # Calculate base alignment score
        total_indicators = len(constraint.violation_indicators) + len(constraint.positive_indicators)
        if total_indicators == 0:
            return 0.7  # Neutral when no indicators
        
        # Violations hurt more than positives help (precautionary principle)
        violation_weight = 0.7
        positive_weight = 0.3
        
        violation_ratio = violation_score / max(len(constraint.violation_indicators), 1)
        positive_ratio = positive_score / max(len(constraint.positive_indicators), 1)
        
        alignment_score = (
            (1.0 - violation_ratio) * violation_weight +
            positive_ratio * positive_weight
        )
        
        # Apply constraint flexibility
        if alignment_score < 0.5:  # Poor alignment
            # Flexibility allows for some tolerance
            adjusted_score = alignment_score + (0.5 - alignment_score) * constraint.flexibility
            return adjusted_score
        
        return alignment_score
    
    def _apply_domain_specific_logic(
        self,
        domain: ValueDomain,
        proposed_action: str,
        context: str,
        constraint_scores: List[float]
    ) -> float:
        """Apply domain-specific assessment logic"""
        
        if not constraint_scores:
            return 0.7
        
        base_score = sum(constraint_scores) / len(constraint_scores)
        
        # Domain-specific adjustments
        if domain == ValueDomain.SAFETY:
            # Safety is critical - be more conservative
            return min(base_score, self._assess_safety_specifically(proposed_action, context))
        
        elif domain == ValueDomain.PRIVACY:
            # Privacy requires special attention to data handling
            return min(base_score, self._assess_privacy_specifically(proposed_action, context))
        
        elif domain == ValueDomain.AUTONOMY:
            # Autonomy requires respect for user choice
            return min(base_score, self._assess_autonomy_specifically(proposed_action, context))
        
        elif domain == ValueDomain.FAIRNESS:
            # Fairness requires consideration of bias and discrimination
            return min(base_score, self._assess_fairness_specifically(proposed_action, context))
        
        else:
            # For other domains, use average constraint score
            return base_score
    
    def _assess_safety_specifically(self, proposed_action: str, context: str) -> float:
        """Specific safety assessment logic"""
        
        # Look for safety-related keywords and patterns
        safety_risks = [
            "harm", "hurt", "damage", "dangerous", "risk", "unsafe", "injury",
            "threat", "violence", "abuse", "exploit", "manipulate"
        ]
        
        action_lower = proposed_action.lower()
        context_lower = context.lower()
        
        risk_indicators = 0
        for risk in safety_risks:
            if risk in action_lower or risk in context_lower:
                risk_indicators += 1
        
        if risk_indicators > 0:
            # Higher risk = lower safety score
            safety_score = max(0.1, 1.0 - (risk_indicators * 0.2))
            return safety_score
        
        # Look for positive safety indicators
        safety_positives = [
            "safe", "secure", "protect", "careful", "cautious", "responsible"
        ]
        
        positive_indicators = 0
        for positive in safety_positives:
            if positive in action_lower or positive in context_lower:
                positive_indicators += 1
        
        if positive_indicators > 0:
            return min(1.0, 0.8 + positive_indicators * 0.1)
        
        return 0.7  # Neutral safety score
    
    def _assess_privacy_specifically(self, proposed_action: str, context: str) -> float:
        """Specific privacy assessment logic"""
        
        # Look for privacy-related concerns
        privacy_risks = [
            "personal information", "private data", "confidential", "secret",
            "share data", "collect information", "track", "monitor", "record",
            "store personal", "access private"
        ]
        
        action_lower = proposed_action.lower()
        context_lower = context.lower()
        
        for risk in privacy_risks:
            if risk in action_lower or risk in context_lower:
                return 0.3  # Privacy risk detected
        
        # Look for privacy-positive indicators
        privacy_positives = [
            "anonymize", "encrypt", "secure", "private", "confidential handling",
            "user consent", "opt-in", "permission"
        ]
        
        for positive in privacy_positives:
            if positive in action_lower or positive in context_lower:
                return 0.9
        
        return 0.7  # Neutral privacy score
    
    def _assess_autonomy_specifically(self, proposed_action: str, context: str) -> float:
        """Specific autonomy assessment logic"""
        
        # Look for autonomy concerns
        autonomy_risks = [
            "force", "require", "must", "no choice", "automatic", "without asking",
            "override", "ignore preferences", "decide for user"
        ]
        
        action_lower = proposed_action.lower()
        context_lower = context.lower()
        
        for risk in autonomy_risks:
            if risk in action_lower or risk in context_lower:
                return 0.3
        
        # Look for autonomy-positive indicators
        autonomy_positives = [
            "user choice", "optional", "user decides", "ask user", "with permission",
            "user control", "user preference", "let user choose"
        ]
        
        for positive in autonomy_positives:
            if positive in action_lower or positive in context_lower:
                return 0.9
        
        return 0.7  # Neutral autonomy score
    
    def _assess_fairness_specifically(self, proposed_action: str, context: str) -> float:
        """Specific fairness assessment logic"""
        
        # Look for fairness concerns
        fairness_risks = [
            "discriminate", "bias", "unfair", "prejudice", "exclude", "favor",
            "stereotype", "unequal", "partial", "preferential treatment"
        ]
        
        action_lower = proposed_action.lower()
        context_lower = context.lower()
        
        for risk in fairness_risks:
            if risk in action_lower or risk in context_lower:
                return 0.3
        
        # Look for fairness-positive indicators
        fairness_positives = [
            "fair", "equal", "unbiased", "inclusive", "diverse", "equitable",
            "same treatment", "consistent", "impartial"
        ]
        
        for positive in fairness_positives:
            if positive in action_lower or positive in context_lower:
                return 0.9
        
        return 0.7  # Neutral fairness score
    
    def _matches_indicator(self, indicator: str, proposed_action: str, context: str) -> bool:
        """Check if an indicator pattern matches the action or context"""
        
        # Simple keyword matching - could be enhanced with NLP
        indicator_lower = indicator.lower()
        action_lower = proposed_action.lower()
        context_lower = context.lower()
        
        # Check for exact phrase match
        if indicator_lower in action_lower or indicator_lower in context_lower:
            return True
        
        return False
    
    def _calculate_overall_alignment(self, domain_assessments: Dict[ValueDomain, float]) -> Tuple[float, float]:
        """Calculate overall alignment score and confidence"""
        
        if not domain_assessments:
            return 0.5, 0.0
        
        # Weight by user's domain importance
        weighted_scores = []
        weights = []
        
        for domain, score in domain_assessments.items():
            user_importance = self.state.get_domain_importance(domain)
            weighted_scores.append(score * user_importance)
            weights.append(user_importance)
        
        # Calculate weighted average
        if sum(weights) > 0:
            overall_score = sum(weighted_scores) / sum(weights)
        else:
            overall_score = sum(domain_assessments.values()) / len(domain_assessments)
        
        # Calculate confidence based on consistency of domain scores
        score_variance = sum((score - overall_score) ** 2 for score in domain_assessments.values())
        score_variance /= len(domain_assessments)
        
        # Higher variance = lower confidence
        confidence = max(0.1, 1.0 - math.sqrt(score_variance))
        
        return overall_score, confidence
    
    def _detect_value_conflicts(
        self,
        proposed_action: str,
        context: str,
        domain_assessments: Dict[ValueDomain, float]
    ) -> List[Tuple[str, ConflictSeverity]]:
        """Detect value conflicts based on domain assessments"""
        
        conflicts = []
        
        # Check for low-scoring domains (potential conflicts)
        for domain, score in domain_assessments.items():
            if score < self.state.config.conflict_threshold:
                conflict = self._create_value_conflict(
                    domain, score, proposed_action, context
                )
                
                if conflict:
                    conflicts.append((conflict.conflict_id, conflict.severity))
        
        return conflicts
    
    def _create_value_conflict(
        self,
        domain: ValueDomain,
        score: float,
        proposed_action: str,
        context: str
    ) -> Optional[ValueConflict]:
        """Create a value conflict for a low-scoring domain"""
        
        # Determine severity based on score and domain importance
        user_importance = self.state.get_domain_importance(domain)
        adjusted_score = score * user_importance
        
        if adjusted_score < 0.2:
            severity = ConflictSeverity.SEVERE
        elif adjusted_score < 0.4:
            severity = ConflictSeverity.MODERATE
        elif adjusted_score < 0.6:
            severity = ConflictSeverity.MILD
        else:
            return None  # Not significant enough to be a conflict
        
        # Find relevant constraints for this domain
        domain_constraints = [
            c for c in self.state.active_constraints.values()
            if c.domain == domain
        ]
        
        primary_constraint = domain_constraints[0] if domain_constraints else None
        
        # Create conflict
        conflict = ValueConflict(
            severity=severity,
            conflict_type=f"{domain.value}_alignment_low",
            primary_constraint=primary_constraint.constraint_id if primary_constraint else "",
            proposed_action=proposed_action,
            context_description=context[:200],
            conflict_details=f"Action may not align well with {domain.value} values (score: {score:.2f})",
            suggested_resolution=self._suggest_conflict_resolution(domain, severity, score),
            resolution_confidence=0.7
        )
        
        # Store conflict
        self.state.active_conflicts[conflict.conflict_id] = conflict
        self.state.total_conflicts_detected += 1
        
        return conflict
    
    def _suggest_conflict_resolution(
        self,
        domain: ValueDomain,
        severity: ConflictSeverity,
        score: float
    ) -> ConflictResolution:
        """Suggest appropriate resolution strategy for a conflict"""
        
        # Safety and privacy conflicts require careful handling
        if domain in [ValueDomain.SAFETY, ValueDomain.PRIVACY]:
            if severity == ConflictSeverity.SEVERE:
                return ConflictResolution.GRACEFUL_DECLINE
            else:
                return ConflictResolution.SEEK_CLARIFICATION
        
        # Autonomy conflicts should give user choice
        if domain == ValueDomain.AUTONOMY:
            return ConflictResolution.USER_CHOICE
        
        # For other domains, base on severity
        if severity == ConflictSeverity.SEVERE:
            return ConflictResolution.ESCALATE_HUMAN
        elif severity == ConflictSeverity.MODERATE:
            return ConflictResolution.SEEK_CLARIFICATION
        else:
            return ConflictResolution.USER_CHOICE
    
    def _generate_alignment_recommendations(
        self,
        alignment: ValueAlignment,
        domain_assessments: Dict[ValueDomain, float],
        conflicts: List[Tuple[str, ConflictSeverity]]
    ) -> List[str]:
        """Generate recommendations for improving value alignment"""
        
        recommendations = []
        
        # Recommendations for low-scoring domains
        for domain, score in domain_assessments.items():
            if score < 0.6:
                recommendations.append(self._get_domain_improvement_suggestion(domain))
        
        # General recommendations based on conflicts
        if len(conflicts) > 2:
            recommendations.append("Consider breaking down the action into smaller, more aligned steps")
        
        if alignment.overall_score < 0.5:
            recommendations.append("Seek explicit user guidance before proceeding")
        
        return recommendations[:5]  # Limit to top 5 recommendations
    
    def _get_domain_improvement_suggestion(self, domain: ValueDomain) -> str:
        """Get improvement suggestion for a specific domain"""
        
        suggestions = {
            ValueDomain.SAFETY: "Ensure no potential harm to users or others",
            ValueDomain.PRIVACY: "Consider data protection and user confidentiality",
            ValueDomain.AUTONOMY: "Respect user choice and decision-making authority",
            ValueDomain.FAIRNESS: "Ensure equal treatment and avoid bias",
            ValueDomain.TRANSPARENCY: "Be clear about intentions and processes",
            ValueDomain.BENEFICENCE: "Focus on positive outcomes and helping",
            ValueDomain.NON_MALEFICENCE: "Carefully avoid any potential harm",
            ValueDomain.RESPECT: "Show respect for human dignity and cultural values",
            ValueDomain.AUTHENTICITY: "Maintain honesty and genuine interaction",
            ValueDomain.RESPONSIBILITY: "Take accountability for actions and outcomes"
        }
        
        return suggestions.get(domain, f"Consider improving alignment with {domain.value}")
    
    def _extract_positive_alignments(self, domain_assessments: Dict[ValueDomain, float]) -> List[str]:
        """Extract positive alignment aspects from domain assessments"""
        
        positives = []
        for domain, score in domain_assessments.items():
            if score > 0.7:
                positives.append(f"Strong alignment with {domain.value} values")
        
        return positives
    
    def _extract_negative_alignments(self, domain_assessments: Dict[ValueDomain, float]) -> List[str]:
        """Extract negative alignment aspects from domain assessments"""
        
        negatives = []
        for domain, score in domain_assessments.items():
            if score < 0.4:
                negatives.append(f"Potential conflict with {domain.value} values")
        
        return negatives
    
    # ========== CONFLICT RESOLUTION ==========
    
    def _execute_resolution_strategy(
        self,
        conflict: ValueConflict,
        resolution_choice: str,
        user_input: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute a specific conflict resolution strategy"""
        
        try:
            resolution_enum = ConflictResolution(resolution_choice)
        except ValueError:
            resolution_enum = ConflictResolution.SEEK_CLARIFICATION
        
        if resolution_enum == ConflictResolution.USER_CHOICE:
            return self._execute_user_choice_resolution(conflict, user_input)
        
        elif resolution_enum == ConflictResolution.PRIORITIZE_SAFETY:
            return self._execute_safety_priority_resolution(conflict)
        
        elif resolution_enum == ConflictResolution.SEEK_CLARIFICATION:
            return self._execute_clarification_resolution(conflict, user_input)
        
        elif resolution_enum == ConflictResolution.GRACEFUL_DECLINE:
            return self._execute_graceful_decline_resolution(conflict)
        
        elif resolution_enum == ConflictResolution.ESCALATE_HUMAN:
            return self._execute_human_escalation_resolution(conflict)
        
        else:  # CONTEXT_DEPENDENT
            return self._execute_context_dependent_resolution(conflict, user_input)
    
    def _execute_user_choice_resolution(
        self,
        conflict: ValueConflict,
        user_input: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Let user decide how to resolve the conflict"""
        
        if not user_input or "user_decision" not in user_input:
            return {
                "success": False,
                "outcome": "awaiting_user_decision",
                "requires_input": True,
                "message": "User decision required to resolve conflict"
            }
        
        user_decision = user_input["user_decision"]
        
        # Update user value profile based on their decision
        if "value_preference" in user_input:
            self._learn_from_user_decision(conflict, user_input["value_preference"])
        
        return {
            "success": True,
            "outcome": f"resolved_by_user_choice_{user_decision}",
            "user_decision": user_decision,
            "lessons": [f"User prefers {user_decision} approach for {conflict.conflict_type} conflicts"]
        }
    
    def _execute_safety_priority_resolution(self, conflict: ValueConflict) -> Dict[str, Any]:
        """Prioritize safety in conflict resolution"""
        
        return {
            "success": True,
            "outcome": "resolved_prioritizing_safety",
            "action_taken": "chose_safer_alternative",
            "lessons": ["Safety prioritized over other values in conflict resolution"]
        }
    
    def _execute_clarification_resolution(
        self,
        conflict: ValueConflict,
        user_input: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Seek clarification to resolve conflict"""
        
        if not user_input or "clarification" not in user_input:
            return {
                "success": False,
                "outcome": "awaiting_clarification",
                "requires_input": True,
                "message": f"Need clarification about {conflict.conflict_type}"
            }
        
        clarification = user_input["clarification"]
        
        # Use clarification to update understanding
        self._process_user_clarification(conflict, clarification)
        
        return {
            "success": True,
            "outcome": "resolved_with_clarification",
            "clarification_received": clarification,
            "lessons": ["User clarification helped resolve value conflict"]
        }
    
    def _execute_graceful_decline_resolution(self, conflict: ValueConflict) -> Dict[str, Any]:
        """Politely decline to take the action that caused conflict"""
        
        return {
            "success": True,
            "outcome": "gracefully_declined",
            "action_taken": "declined_action",
            "lessons": [f"Declined action due to {conflict.conflict_type} conflict"]
        }
    
    def _execute_human_escalation_resolution(self, conflict: ValueConflict) -> Dict[str, Any]:
        """Escalate conflict to human oversight"""
        
        return {
            "success": True,
            "outcome": "escalated_to_human",
            "action_taken": "escalated",
            "lessons": [f"Escalated {conflict.severity.value} {conflict.conflict_type} conflict"]
        }
    
    def _execute_context_dependent_resolution(
        self,
        conflict: ValueConflict,
        user_input: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Resolve based on specific context"""
        
        # Analyze context to determine best resolution
        if "urgent" in conflict.context_description.lower():
            return self._execute_safety_priority_resolution(conflict)
        elif "personal" in conflict.context_description.lower():
            return self._execute_user_choice_resolution(conflict, user_input)
        else:
            return self._execute_clarification_resolution(conflict, user_input)
    
    # ========== LEARNING AND ADAPTATION ==========
    
    def _learn_from_resolution(self, conflict: ValueConflict, resolution_outcome: Dict[str, Any]):
        """Learn from conflict resolution outcomes"""
        
        # Update conflict resolution success rate
        success = resolution_outcome.get("success", False)
        
        # Learn about user preferences
        if "user_decision" in resolution_outcome:
            self._update_user_preference_from_resolution(conflict, resolution_outcome)
        
        # Add lessons learned
        lessons = resolution_outcome.get("lessons", [])
        conflict.lessons_learned.extend(lessons)
    
    def _learn_from_user_decision(self, conflict: ValueConflict, value_preference: Dict[str, float]):
        """Learn from user's value preferences in conflict resolution"""
        
        # Update user value profile
        updates = {}
        for domain_str, preference in value_preference.items():
            try:
                domain = ValueDomain(domain_str)
                updates[domain] = preference
            except ValueError:
                continue
        
        if updates:
            self.update_user_values(updates, source="learned_from_conflict")
    
    def _process_user_clarification(self, conflict: ValueConflict, clarification: str):
        """Process user clarification to improve future conflict detection"""
        
        # Extract insights from clarification
        clarification_lower = clarification.lower()
        
        # Look for value-related keywords
        value_keywords = {
            "safety": ValueDomain.SAFETY,
            "privacy": ValueDomain.PRIVACY,
            "choice": ValueDomain.AUTONOMY,
            "fair": ValueDomain.FAIRNESS,
            "honest": ValueDomain.TRANSPARENCY
        }
        
        value_updates = {}
        for keyword, domain in value_keywords.items():
            if keyword in clarification_lower:
                # User mentioned this value - increase importance
                current_importance = self.state.get_domain_importance(domain)
                value_updates[domain] = min(current_importance + 0.1, 1.0)
        
        if value_updates:
            self.update_user_values(value_updates, context=clarification, source="clarification")
    
    def _update_user_preference_from_resolution(self, conflict: ValueConflict, outcome: Dict[str, Any]):
        """Update user preferences based on resolution choices"""
        
        user_decision = outcome.get("user_decision", "")
        
        # Infer value preferences from decision
        preference_updates = {}
        
        if "safety" in user_decision.lower():
            preference_updates[ValueDomain.SAFETY] = min(
                self.state.get_domain_importance(ValueDomain.SAFETY) + 0.1, 1.0
            )
        
        if "privacy" in user_decision.lower():
            preference_updates[ValueDomain.PRIVACY] = min(
                self.state.get_domain_importance(ValueDomain.PRIVACY) + 0.1, 1.0
            )
        
        if "choice" in user_decision.lower() or "decide" in user_decision.lower():
            preference_updates[ValueDomain.AUTONOMY] = min(
                self.state.get_domain_importance(ValueDomain.AUTONOMY) + 0.1, 1.0
            )
        
        if preference_updates:
            self.update_user_values(preference_updates, source="resolution_preference")
    
    # ========== COLLABORATION ENHANCEMENT ==========
    
    def _enhance_with_collaboration(
        self,
        domain_assessments: Dict[ValueDomain, float],
        collaboration_hints: Dict[str, Any]
    ) -> Dict[ValueDomain, float]:
        """Enhance domain assessments with collaboration signals"""
        
        enhanced_assessments = domain_assessments.copy()
        
        # Attention collaboration
        if "attention_context" in collaboration_hints:
            attention_data = collaboration_hints["attention_context"]
            
            # High attention on sensitive entities should increase privacy concerns
            high_attention_entities = attention_data.get("current_focus_entities", [])
            if any("personal" in entity.lower() or "private" in entity.lower() 
                   for entity in high_attention_entities):
                enhanced_assessments[ValueDomain.PRIVACY] *= 0.9  # Slight penalty
        
        # Memory collaboration
        if "memory_context" in collaboration_hints:
            memory_data = collaboration_hints["memory_context"]
            
            # Storing personal information should trigger privacy considerations
            if memory_data.get("storing_personal_info", False):
                enhanced_assessments[ValueDomain.PRIVACY] *= 0.8
            
            # User corrections in memory suggest autonomy importance
            if memory_data.get("user_corrections", 0) > 0:
                enhanced_assessments[ValueDomain.AUTONOMY] = min(
                    enhanced_assessments[ValueDomain.AUTONOMY] + 0.1, 1.0
                )
        
        # Tone collaboration
        if "tone_context" in collaboration_hints:
            tone_data = collaboration_hints["tone_context"]
            
            # Manipulative tone adaptation could violate authenticity
            manipulation_risk = tone_data.get("manipulation_risk", 0.0)
            if manipulation_risk > 0.5:
                enhanced_assessments[ValueDomain.AUTHENTICITY] *= (1 - manipulation_risk)
        
        return enhanced_assessments
    
    def _generate_ethical_guidance(self) -> Dict[str, Any]:
        """Generate general ethical guidance for other primitives"""
        
        # Calculate overall ethical significance
        active_conflicts = len(self.state.active_conflicts)
        recent_alignments = self.state.get_recent_alignments(hours=1)
        avg_recent_alignment = (
            sum(a.overall_score for a in recent_alignments) / len(recent_alignments)
            if recent_alignments else 0.7
        )
        
        ethical_significance = min(1.0, (active_conflicts * 0.2) + (1.0 - avg_recent_alignment))
        
        # Generate guidance based on current state
        guidance = {
            "agent_id": self.agent_id,
            "ethical_significance": ethical_significance,
            "active_constraints": list(self.state.active_constraints.keys()),
            "high_priority_values": [
                domain.value for domain, importance in self.state.user_value_profile.items()
                if importance > 0.7
            ],
            "attention_needed": [
                conflict_id for conflict_id, conflict in self.state.active_conflicts.items()
                if conflict.severity in [ConflictSeverity.SEVERE, ConflictSeverity.MODERATE]
            ],
            "general_recommendations": self._generate_general_ethical_recommendations()
        }
        
        return guidance
    
    def _generate_constraint_guidance(self) -> Dict[str, Any]:
        """Generate specific constraint guidance"""
        
        active_constraints = {}
        for constraint_id, constraint in self.state.active_constraints.items():
            if constraint.priority in [ValuePriority.CRITICAL, ValuePriority.HIGH]:
                active_constraints[constraint_id] = {
                    "domain": constraint.domain.value,
                    "strength": constraint.strength,
                    "priority": constraint.priority.value,
                    "violation_indicators": constraint.violation_indicators[:3],  # Top 3
                    "flexibility": constraint.flexibility
                }
        
        return {
            "agent_id": self.agent_id,
            "high_priority_constraints": active_constraints,
            "constraint_count": len(self.state.active_constraints),
            "critical_domains": [
                domain.value for domain, importance in self.state.user_value_profile.items()
                if importance > 0.8
            ]
        }
    
    def _generate_risk_guidance(self) -> Dict[str, Any]:
        """Generate ethical risk guidance"""
        
        current_risks = []
        
        # Risks from active conflicts
        for conflict in self.state.active_conflicts.values():
            if conflict.severity in [ConflictSeverity.SEVERE, ConflictSeverity.MODERATE]:
                current_risks.extend(conflict.potential_harms[:2])  # Top 2 harms
        
        return {
            "agent_id": self.agent_id,
            "current_ethical_risks": current_risks[:5],
            "risk_level": "high" if len(current_risks) > 3 else "moderate" if len(current_risks) > 1 else "low",
            "monitoring_needed": len(self.state.active_conflicts) > 0
        }
    
    def _generate_opportunity_guidance(self) -> Dict[str, Any]:
        """Generate ethical opportunity guidance"""
        
        opportunities = []
        
        # Opportunities from user value profile
        for domain, importance in self.state.user_value_profile.items():
            if importance > 0.8:
                opportunities.append(f"User highly values {domain.value} - opportunity for positive impact")
        
        return {
            "agent_id": self.agent_id,
            "ethical_opportunities": opportunities[:5],
            "value_demonstration_potential": len(opportunities),
            "user_values_to_highlight": [
                domain.value for domain, importance in self.state.user_value_profile.items()
                if importance > 0.7
            ]
        }
    
    def _generate_general_ethical_recommendations(self) -> List[str]:
        """Generate general ethical recommendations"""
        
        recommendations = []
        
        # Based on active conflicts
        if len(self.state.active_conflicts) > 2:
            recommendations.append("Be extra cautious with ethically sensitive actions")
        
        # Based on user value profile
        high_value_domains = [
            domain.value for domain, importance in self.state.user_value_profile.items()
            if importance > 0.8
        ]
        
        if "safety" in high_value_domains:
            recommendations.append("Prioritize safety considerations in all decisions")
        
        if "privacy" in high_value_domains:
            recommendations.append("Be especially careful with personal information")
        
        if "autonomy" in high_value_domains:
            recommendations.append("Always respect user choice and decision-making")
        
        return recommendations[:3]  # Top 3 recommendations
    
    # ========== COLLABORATION SIGNAL PROCESSING ==========
    
    def _process_attention_signals(self, signal_data: Dict[str, Any]):
        """Process signals from attention primitive"""
        
        try:
            # Monitor attention on ethically sensitive entities
            current_focus = signal_data.get("current_focus_entities", [])
            
            for entity in current_focus:
                # Check if entity triggers ethical concerns
                if self._is_ethically_sensitive_entity(entity):
                    # Increase monitoring for related value domains
                    logger.info(f"Increased ethical monitoring for entity: {entity}")
            
            # Adjust detection sensitivity based on attention patterns
            focus_stability = signal_data.get("focus_stability", 0.5)
            if focus_stability < 0.3:
                # Unstable attention might indicate user confusion - increase ethical sensitivity
                self.state.config.global_sensitivity = min(
                    self.state.config.global_sensitivity * 1.1, 1.0
                )
        
        except Exception as e:
            logger.error(f"Error processing attention signals: {str(e)}")
    
    def _process_memory_signals(self, signal_data: Dict[str, Any]):
        """Process signals from memory primitive"""
        
        try:
            # Monitor memory storage for ethical implications
            stored_content_type = signal_data.get("content_type", "general")
            
            if stored_content_type in ["personal", "sensitive", "private"]:
                # Storing sensitive information - check privacy constraints
                privacy_constraints = [
                    c for c in self.state.active_constraints.values()
                    if c.domain == ValueDomain.PRIVACY
                ]
                
                for constraint in privacy_constraints:
                    if constraint.priority in [ValuePriority.CRITICAL, ValuePriority.HIGH]:
                        logger.info(f"Privacy-sensitive memory storage detected")
            
            # Learn from memory patterns about user values
            frequent_topics = signal_data.get("frequent_topics", [])
            if "privacy" in frequent_topics:
                # User often mentions privacy - likely important value
                current_privacy_importance = self.state.get_domain_importance(ValueDomain.PRIVACY)
                self.update_user_values(
                    {ValueDomain.PRIVACY: min(current_privacy_importance + 0.05, 1.0)},
                    source="memory_pattern"
                )
        
        except Exception as e:
            logger.error(f"Error processing memory signals: {str(e)}")
    
    def _process_tone_signals(self, signal_data: Dict[str, Any]):
        """Process signals from tone primitive"""
        
        try:
            # Monitor tone adaptation for authenticity concerns
            tone_change_magnitude = signal_data.get("adaptation_magnitude", 0.0)
            
            if tone_change_magnitude > 0.7:
                # Large tone changes might indicate authenticity concerns
                authenticity_score = self._assess_authenticity_risk(signal_data)
                
                if authenticity_score < 0.5:
                    # Create potential authenticity conflict
                    self._flag_authenticity_concern(signal_data)
            
            # Monitor for manipulation risks
            persuasion_level = signal_data.get("persuasion_level", 0.0)
            if persuasion_level > 0.8:
                # High persuasion might conflict with respect and autonomy
                self._flag_manipulation_risk(signal_data)
        
        except Exception as e:
            logger.error(f"Error processing tone signals: {str(e)}")
    
    # ========== HELPER METHODS ==========
    
    def _is_ethically_sensitive_entity(self, entity: str) -> bool:
        """Check if an entity is ethically sensitive"""
        
        sensitive_keywords = [
            "personal", "private", "confidential", "secret", "password",
            "medical", "financial", "political", "religious", "intimate"
        ]
        
        entity_lower = entity.lower()
        return any(keyword in entity_lower for keyword in sensitive_keywords)
    
    def _assess_authenticity_risk(self, tone_signals: Dict[str, Any]) -> float:
        """Assess authenticity risk from tone adaptation"""
        
        # Simplified authenticity risk assessment
        adaptation_magnitude = tone_signals.get("adaptation_magnitude", 0.0)
        user_initiated = tone_signals.get("user_initiated", True)
        
        if user_initiated:
            return 0.8  # Low risk if user requested
        else:
            # Higher adaptation without user request = higher authenticity risk
            return max(0.1, 1.0 - adaptation_magnitude)
    
    def _flag_authenticity_concern(self, tone_signals: Dict[str, Any]):
        """Flag an authenticity concern based on tone adaptation"""
        
        # Create a mild conflict for authenticity
        conflict = ValueConflict(
            severity=ConflictSeverity.MILD,
            conflict_type="authenticity_concern",
            primary_constraint="",
            proposed_action="tone_adaptation",
            context_description="Large tone adaptation without explicit user request",
            conflict_details="Tone adaptation magnitude might affect authenticity",
            suggested_resolution=ConflictResolution.SEEK_CLARIFICATION,
            resolution_confidence=0.6
        )
        
        self.state.active_conflicts[conflict.conflict_id] = conflict
    
    def _flag_manipulation_risk(self, tone_signals: Dict[str, Any]):
        """Flag manipulation risk based on tone adaptation"""
        
        conflict = ValueConflict(
            severity=ConflictSeverity.MODERATE,
            conflict_type="manipulation_risk",
            primary_constraint="",
            proposed_action="persuasive_tone_adaptation",
            context_description="High persuasion level in tone adaptation",
            conflict_details="Highly persuasive tone might conflict with user autonomy and respect",
            suggested_resolution=ConflictResolution.USER_CHOICE,
            resolution_confidence=0.7
        )
        
        self.state.active_conflicts[conflict.conflict_id] = conflict
    
    def _adjust_constraints_based_on_values(self):
        """Adjust constraint strengths based on updated user values"""
        
        for constraint in self.state.active_constraints.values():
            domain_importance = self.state.get_domain_importance(constraint.domain)
            
            # Adjust personal importance based on user value profile
            constraint.personal_importance = domain_importance
            
            # Adjust flexibility (higher user importance = less flexibility)
            if domain_importance > 0.8:
                constraint.flexibility = max(constraint.flexibility * 0.8, 0.1)
            elif domain_importance < 0.3:
                constraint.flexibility = min(constraint.flexibility * 1.2, 0.9)
    
    def _update_resolution_success_rate(self, success: bool):
        """Update conflict resolution success rate"""
        
        # Simple moving average
        current_rate = self.state.conflict_resolution_success_rate
        total_resolved = self.state.total_conflicts_resolved
        
        if total_resolved == 1:
            self.state.conflict_resolution_success_rate = 1.0 if success else 0.0
        else:
            # Weighted moving average
            weight = 1.0 / total_resolved
            self.state.conflict_resolution_success_rate = (
                current_rate * (1 - weight) + (1.0 if success else 0.0) * weight
            )
    
    def _update_performance_metrics(self):
        """Update value alignment performance metrics"""
        
        current_time = datetime.now()
        
        # Only update if enough time has passed
        if (current_time - self._last_performance_update).total_seconds() < 300:  # 5 minutes
            return
        
        # Update alignment accuracy based on recent feedback
        if self._feedback_buffer:
            recent_feedback = [
                f for f in self._feedback_buffer 
                if (current_time - f["timestamp"]).total_seconds() < 3600  # Last hour
            ]
            
            if recent_feedback:
                positive_feedback = len([
                    f for f in recent_feedback 
                    if f["type"] in ["alignment_correct", "good_ethical_decision"]
                ])
                total_feedback = len(recent_feedback)
                self.state.alignment_accuracy = positive_feedback / total_feedback
        
        self._last_performance_update = current_time
    
    # ========== INITIALIZATION METHODS ==========
    
    def _initialize_default_constraints(self):
        """Initialize default value constraints"""
        
        # Safety constraints
        safety_constraint = ValueConstraint(
            domain=ValueDomain.SAFETY,
            constraint_name="Basic Safety",
            description="Avoid actions that could cause harm to users or others",
            priority=ValuePriority.CRITICAL,
            strength=0.9,
            flexibility=0.1,
            violation_indicators=[
                "harm", "hurt", "damage", "dangerous", "risk", "unsafe", "injury",
                "threat", "violence", "abuse"
            ],
            positive_indicators=[
                "safe", "secure", "protect", "careful", "cautious", "responsible"
            ],
            source="system_default"
        )
        self.state.active_constraints[safety_constraint.constraint_id] = safety_constraint
        
        # Privacy constraints
        privacy_constraint = ValueConstraint(
            domain=ValueDomain.PRIVACY,
            constraint_name="Data Privacy",
            description="Protect user privacy and personal information",
            priority=ValuePriority.HIGH,
            strength=0.8,
            flexibility=0.2,
            violation_indicators=[
                "share personal", "collect data", "track", "monitor", "record private",
                "access confidential", "expose information"
            ],
            positive_indicators=[
                "anonymize", "encrypt", "secure", "private", "confidential",
                "user consent", "permission"
            ],
            source="system_default"
        )
        self.state.active_constraints[privacy_constraint.constraint_id] = privacy_constraint
        
        # Autonomy constraints
        autonomy_constraint = ValueConstraint(
            domain=ValueDomain.AUTONOMY,
            constraint_name="User Autonomy",
            description="Respect user choice and decision-making authority",
            priority=ValuePriority.HIGH,
            strength=0.8,
            flexibility=0.3,
            violation_indicators=[
                "force", "require", "must", "no choice", "automatic", "without asking",
                "override", "ignore preferences", "decide for user"
            ],
            positive_indicators=[
                "user choice", "optional", "user decides", "ask user", "with permission",
                "user control", "user preference"
            ],
            source="system_default"
        )
        self.state.active_constraints[autonomy_constraint.constraint_id] = autonomy_constraint
        
        # Transparency constraints
        transparency_constraint = ValueConstraint(
            domain=ValueDomain.TRANSPARENCY,
            constraint_name="Transparency",
            description="Be honest and transparent about AI capabilities and limitations",
            priority=ValuePriority.MEDIUM,
            strength=0.7,
            flexibility=0.3,
            violation_indicators=[
                "hide", "conceal", "mislead", "deceive", "lie", "false claim",
                "pretend to be human"
            ],
            positive_indicators=[
                "honest", "transparent", "clear", "explain", "disclose", "admit limitations",
                "I am an AI"
            ],
            source="system_default"
        )
        self.state.active_constraints[transparency_constraint.constraint_id] = transparency_constraint
    
    def _initialize_default_detection_rules(self):
        """Initialize default value detection rules"""
        
        # Safety detection rule
        safety_rule = ValueDetectionRule(
            rule_name="Safety Risk Detection",
            target_domain=ValueDomain.SAFETY,
            keyword_triggers=[
                "harm", "hurt", "damage", "dangerous", "risk", "unsafe", "threat"
            ],
            sensitivity=0.7,
            confidence_threshold=0.6,
            alert_severity=ConflictSeverity.MODERATE,
            blocks_action=True
        )
        self.state.detection_rules[safety_rule.rule_id] = safety_rule
        
        # Privacy detection rule
        privacy_rule = ValueDetectionRule(
            rule_name="Privacy Risk Detection",
            target_domain=ValueDomain.PRIVACY,
            keyword_triggers=[
                "personal information", "private data", "share data", "collect information"
            ],
            sensitivity=0.6,
            confidence_threshold=0.5,
            alert_severity=ConflictSeverity.MODERATE,
            requires_user_input=True
        )
        self.state.detection_rules[privacy_rule.rule_id] = privacy_rule
    
    # ========== PUBLIC UTILITY METHODS ==========
    
    def get_value_alignment_summary(self) -> Dict[str, Any]:
        """Get comprehensive value alignment state summary"""
        
        # Calculate recent alignment health
        recent_alignments = self.state.get_recent_alignments(hours=24)
        if recent_alignments:
            avg_alignment = sum(a.overall_score for a in recent_alignments) / len(recent_alignments)
        else:
            avg_alignment = 0.7
        
        return {
            "agent_id": self.agent_id,
            "overall_alignment_health": avg_alignment,
            "active_conflicts": len(self.state.active_conflicts),
            "resolved_conflicts": len(self.state.resolved_conflicts),
            "user_value_profile": dict(self.state.user_value_profile),
            "performance_metrics": {
                "alignment_accuracy": self.state.alignment_accuracy,
                "resolution_success_rate": self.state.conflict_resolution_success_rate,
            },
            "collaboration_status": {
                "enabled": self.state.collaboration_enabled,
                "active_partnerships": self.state.primitive_partnerships
            }
        }
