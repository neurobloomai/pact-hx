# pact_hx/primitives/value_align/schemas.py
"""
PACT-HX Value Alignment Schemas

Foundation schemas for ethical constraint and value alignment in AI systems.
These schemas define the core data structures for detecting, tracking, and
resolving value conflicts in AI interactions.

Core Philosophy: Values provide the ethical boundaries and alignment constraints
that guide attention focus, memory storage, and tone adaptation decisions.
"""

from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from enum import Enum
import uuid

# ========== ENUMS AND CONSTANTS ==========

class ValueDomain(str, Enum):
    """Core domains of human values that AI should align with"""
    AUTONOMY = "autonomy"           # User control, choice, self-determination
    PRIVACY = "privacy"             # Data protection, confidentiality, boundaries
    SAFETY = "safety"              # Physical and psychological safety
    FAIRNESS = "fairness"          # Justice, equality, non-discrimination
    TRANSPARENCY = "transparency"   # Honesty, openness, explainability
    BENEFICENCE = "beneficence"    # Doing good, helping, positive impact
    NON_MALEFICENCE = "non_maleficence"  # Avoiding harm, "do no harm"
    RESPECT = "respect"            # Human dignity, cultural sensitivity
    AUTHENTICITY = "authenticity"   # Truthfulness, genuine interaction
    RESPONSIBILITY = "responsibility"  # Accountability, ownership of actions

class ValuePriority(str, Enum):
    """Priority levels for value constraints"""
    CRITICAL = "critical"      # Must never be violated (safety, consent)
    HIGH = "high"             # Should strongly influence decisions
    MEDIUM = "medium"         # Should moderately influence decisions  
    LOW = "low"              # Should weakly influence decisions
    CONTEXTUAL = "contextual" # Priority depends on context

class ConflictSeverity(str, Enum):
    """Severity levels for value conflicts"""
    SEVERE = "severe"         # Fundamental conflict requiring immediate attention
    MODERATE = "moderate"     # Significant conflict needing resolution
    MILD = "mild"            # Minor tension that should be noted
    POTENTIAL = "potential"   # Possible conflict worth monitoring

class ConflictResolution(str, Enum):
    """Strategies for resolving value conflicts"""
    USER_CHOICE = "user_choice"           # Let user decide
    PRIORITIZE_SAFETY = "prioritize_safety"  # Default to safety
    SEEK_CLARIFICATION = "seek_clarification"  # Ask for more information
    GRACEFUL_DECLINE = "graceful_decline"     # Politely refuse to act
    ESCALATE_HUMAN = "escalate_human"         # Escalate to human oversight
    CONTEXT_DEPENDENT = "context_dependent"   # Resolve based on context

# ========== CORE VALUE SCHEMAS ==========

class ValueConstraint(BaseModel):
    """
    Individual value constraint that guides AI behavior
    
    Represents a specific ethical principle or value that should
    influence or constrain AI decisions and actions.
    """
    
    # Identity and classification
    constraint_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    domain: ValueDomain = Field(..., description="Core value domain")
    constraint_name: str = Field(..., description="Human-readable constraint name")
    description: str = Field(..., description="Detailed constraint description")
    
    # Constraint parameters
    priority: ValuePriority = Field(..., description="Priority level of this constraint")
    strength: float = Field(
        default=0.8, 
        ge=0.0, 
        le=1.0, 
        description="Strength of constraint (0=suggestion, 1=absolute)"
    )
    flexibility: float = Field(
        default=0.2,
        ge=0.0,
        le=1.0,
        description="How flexible this constraint is in different contexts"
    )
    
    # Context and applicability
    applicable_contexts: List[str] = Field(
        default_factory=list,
        description="Contexts where this constraint applies"
    )
    exclusion_contexts: List[str] = Field(
        default_factory=list,
        description="Contexts where this constraint doesn't apply"
    )
    
    # User and cultural factors
    user_specified: bool = Field(
        default=False,
        description="Whether user explicitly specified this constraint"
    )
    cultural_context: Optional[str] = Field(
        None,
        description="Cultural context that influences this constraint"
    )
    personal_importance: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="How important this is to the specific user"
    )
    
    # Implementation details
    violation_indicators: List[str] = Field(
        default_factory=list,
        description="Signals that indicate potential violation"
    )
    positive_indicators: List[str] = Field(
        default_factory=list,
        description="Signals that indicate good alignment"
    )
    
    # Learning and adaptation
    violation_history: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="History of violations and responses"
    )
    alignment_feedback: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Feedback on alignment quality"
    )
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    source: str = Field(default="system", description="Source of this constraint")
    
    @validator('strength', 'flexibility', 'personal_importance')
    def validate_bounds(cls, v):
        """Ensure values are within valid bounds"""
        return max(0.0, min(1.0, v))

class ValueConflict(BaseModel):
    """
    Detected conflict between values or between values and actions
    
    Represents a situation where multiple values are in tension
    or where a proposed action conflicts with established values.
    """
    
    # Identity and classification
    conflict_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    severity: ConflictSeverity = Field(..., description="Severity of the conflict")
    conflict_type: str = Field(..., description="Type of conflict detected")
    
    # Conflicting elements
    primary_constraint: str = Field(..., description="Primary constraint ID involved")
    conflicting_constraints: List[str] = Field(
        default_factory=list,
        description="Other constraint IDs in conflict"
    )
    proposed_action: Optional[str] = Field(
        None,
        description="Action that triggered the conflict"
    )
    
    # Context and details
    context_description: str = Field(..., description="Context where conflict arose")
    conflict_details: str = Field(..., description="Detailed description of conflict")
    stakeholders_affected: List[str] = Field(
        default_factory=list,
        description="Who is affected by this conflict"
    )
    
    # Impact assessment
    potential_harms: List[str] = Field(
        default_factory=list,
        description="Potential negative outcomes"
    )
    potential_benefits: List[str] = Field(
        default_factory=list,
        description="Potential positive outcomes"
    )
    uncertainty_factors: List[str] = Field(
        default_factory=list,
        description="Factors that increase uncertainty"
    )
    
    # Resolution information
    suggested_resolution: ConflictResolution = Field(
        ..., 
        description="Suggested approach to resolve conflict"
    )
    resolution_confidence: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Confidence in suggested resolution"
    )
    alternative_resolutions: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Alternative resolution approaches"
    )
    
    # User interaction
    user_notified: bool = Field(default=False)
    user_response: Optional[str] = Field(None, description="User's response to conflict")
    user_resolution_preference: Optional[str] = Field(None)
    
    # Temporal aspects
    detected_at: datetime = Field(default_factory=datetime.now)
    resolution_deadline: Optional[datetime] = Field(None)
    resolved_at: Optional[datetime] = Field(None)
    resolution_outcome: Optional[str] = Field(None)
    
    # Learning and improvement
    resolution_effectiveness: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="How well the resolution worked"
    )
    lessons_learned: List[str] = Field(
        default_factory=list,
        description="Insights gained from this conflict"
    )

class ValueAlignment(BaseModel):
    """
    Assessment of how well an action or decision aligns with values
    
    Represents the degree to which a specific action, decision, or
    behavior aligns with established value constraints.
    """
    
    # Identity
    alignment_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    assessed_action: str = Field(..., description="Action or decision being assessed")
    
    # Overall alignment metrics
    overall_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Overall alignment score (0=poor, 1=excellent)"
    )
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence in alignment assessment"
    )
    
    # Domain-specific scores
    domain_scores: Dict[ValueDomain, float] = Field(
        default_factory=dict,
        description="Alignment scores by value domain"
    )
    
    # Detailed analysis
    positive_alignments: List[str] = Field(
        default_factory=list,
        description="How the action aligns well with values"
    )
    negative_alignments: List[str] = Field(
        default_factory=list,
        description="How the action conflicts with values"
    )
    neutral_aspects: List[str] = Field(
        default_factory=list,
        description="Aspects that are value-neutral"
    )
    
    # Risk and opportunity assessment
    ethical_risks: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Potential ethical risks identified"
    )
    ethical_opportunities: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Opportunities to demonstrate values"
    )
    
    # Contextual factors
    context_factors: List[str] = Field(
        default_factory=list,
        description="Contextual factors affecting alignment"
    )
    stakeholder_impact: Dict[str, str] = Field(
        default_factory=dict,
        description="How different stakeholders are impacted"
    )
    
    # Recommendations
    improvement_suggestions: List[str] = Field(
        default_factory=list,
        description="Ways to improve value alignment"
    )
    alternative_approaches: List[str] = Field(
        default_factory=list,
        description="Alternative approaches with better alignment"
    )
    
    # Metadata
    assessed_at: datetime = Field(default_factory=datetime.now)
    assessment_method: str = Field(default="automated")
    reviewer_notes: Optional[str] = Field(None)

# ========== CONFIGURATION SCHEMAS ==========

class ValueDetectionRule(BaseModel):
    """
    Rules for detecting value-relevant situations and potential conflicts
    """
    
    rule_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    rule_name: str = Field(..., description="Human-readable rule name")
    target_domain: ValueDomain = Field(..., description="Value domain this rule targets")
    
    # Detection triggers
    keyword_triggers: List[str] = Field(
        default_factory=list,
        description="Keywords that trigger this rule"
    )
    pattern_triggers: List[str] = Field(
        default_factory=list,
        description="Text patterns that trigger this rule"
    )
    context_triggers: List[str] = Field(
        default_factory=list,
        description="Contextual situations that trigger this rule"
    )
    behavioral_triggers: List[str] = Field(
        default_factory=list,
        description="User behaviors that trigger this rule"
    )
    
    # Rule parameters
    sensitivity: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="How sensitive this rule is to triggers"
    )
    confidence_threshold: float = Field(
        default=0.6,
        ge=0.0,
        le=1.0,
        description="Confidence threshold for rule activation"
    )
    
    # Actions when triggered
    alert_severity: ConflictSeverity = Field(
        default=ConflictSeverity.MILD,
        description="Severity level when rule triggers"
    )
    requires_user_input: bool = Field(
        default=False,
        description="Whether user input is required when triggered"
    )
    blocks_action: bool = Field(
        default=False,
        description="Whether this rule can block actions"
    )
    
    # Learning and adaptation
    false_positive_count: int = Field(default=0)
    true_positive_count: int = Field(default=0)
    accuracy: float = Field(default=0.0, ge=0.0, le=1.0)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    last_triggered: Optional[datetime] = Field(None)
    enabled: bool = Field(default=True)

class ValueAlignmentConfiguration(BaseModel):
    """
    Configuration parameters for value alignment processing
    """
    
    # Detection sensitivity
    global_sensitivity: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Global sensitivity to value-related issues"
    )
    conflict_threshold: float = Field(
        default=0.6,
        ge=0.0,
        le=1.0,
        description="Threshold for flagging conflicts"
    )
    
    # Processing parameters
    max_conflicts_to_track: int = Field(
        default=100,
        ge=10,
        description="Maximum number of conflicts to track"
    )
    conflict_resolution_timeout: int = Field(
        default=3600,
        description="Timeout for conflict resolution in seconds"
    )
    
    # User interaction
    prompt_user_for_conflicts: bool = Field(
        default=True,
        description="Whether to prompt user for conflict resolution"
    )
    auto_resolve_minor_conflicts: bool = Field(
        default=False,
        description="Whether to auto-resolve minor conflicts"
    )
    
    # Learning parameters
    learning_rate: float = Field(
        default=0.1,
        ge=0.0,
        le=1.0,
        description="Rate of adaptation from feedback"
    )
    feedback_integration_weight: float = Field(
        default=0.3,
        ge=0.0,
        le=1.0,
        description="Weight given to user feedback in learning"
    )
    
    # Collaboration settings
    share_ethical_insights: bool = Field(
        default=True,
        description="Whether to share ethical insights with other primitives"
    )
    trust_external_ethical_signals: bool = Field(
        default=False,
        description="Whether to trust ethical signals from external sources"
    )

# ========== STATE MANAGEMENT SCHEMAS ==========

class ValueAlignmentState(BaseModel):
    """
    Complete value alignment state for an agent
    
    Root state object containing all value-related data, constraints,
    conflicts, and operational state for a single agent.
    """
    
    # Identity and metadata
    agent_id: str = Field(..., description="Unique agent identifier")
    user_id: Optional[str] = Field(None, description="Associated user identifier")
    
    # Value constraints and rules
    active_constraints: Dict[str, ValueConstraint] = Field(
        default_factory=dict,
        description="Currently active value constraints"
    )
    detection_rules: Dict[str, ValueDetectionRule] = Field(
        default_factory=dict,
        description="Rules for detecting value-relevant situations"
    )
    
    # Conflict tracking
    active_conflicts: Dict[str, ValueConflict] = Field(
        default_factory=dict,
        description="Currently unresolved value conflicts"
    )
    resolved_conflicts: List[ValueConflict] = Field(
        default_factory=list,
        description="History of resolved conflicts"
    )
    
    # Alignment history
    alignment_history: List[ValueAlignment] = Field(
        default_factory=list,
        description="History of value alignment assessments"
    )
    
    # User preferences and context
    user_value_profile: Dict[ValueDomain, float] = Field(
        default_factory=dict,
        description="User's relative importance of different value domains"
    )
    cultural_context: Optional[str] = Field(None)
    personal_ethical_framework: Optional[str] = Field(None)
    
    # Configuration
    config: ValueAlignmentConfiguration = Field(
        default_factory=ValueAlignmentConfiguration,
        description="Value alignment configuration"
    )
    
    # Collaboration state
    collaboration_enabled: bool = Field(default=False)
    primitive_partnerships: List[str] = Field(
        default_factory=list,
        description="List of collaborating primitives"
    )
    external_signals: Dict[str, Any] = Field(
        default_factory=dict,
        description="Signals received from other primitives"
    )
    
    # Performance metrics
    alignment_accuracy: float = Field(
        default=0.0,
        description="Accuracy of value alignment predictions"
    )
    conflict_resolution_success_rate: float = Field(
        default=0.0,
        description="Success rate of conflict resolutions"
    )
    user_satisfaction_with_ethics: float = Field(
        default=0.0,
        description="User satisfaction with ethical behavior"
    )
    false_positive_rate: float = Field(
        default=0.0,
        description="Rate of false positive conflict detections"
    )
    
    # Operational metrics
    total_alignments_assessed: int = Field(default=0)
    total_conflicts_detected: int = Field(default=0)
    total_conflicts_resolved: int = Field(default=0)
    average_resolution_time: float = Field(default=0.0)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)
    last_conflict_check: datetime = Field(default_factory=datetime.now)
    
    def get_domain_importance(self, domain: ValueDomain) -> float:
        """Get importance weight for a specific value domain"""
        return self.user_value_profile.get(domain, 0.5)
    
    def get_active_conflict_count(self) -> int:
        """Get count of active unresolved conflicts"""
        return len(self.active_conflicts)
    
    def get_recent_alignments(self, hours: int = 24) -> List[ValueAlignment]:
        """Get recent alignment assessments"""
        cutoff = datetime.now() - timedelta(hours=hours)
        return [
            alignment for alignment in self.alignment_history
            if alignment.assessed_at > cutoff
        ]

# ========== API RESPONSE SCHEMAS ==========

class ValueAlignmentResponse(BaseModel):
    """Response schema for value alignment assessments"""
    
    agent_id: str
    alignment_id: str
    overall_score: float
    confidence: float
    domain_scores: Dict[str, float]
    conflicts_detected: List[str]
    recommendations: List[str]
    requires_attention: bool
    pact_version: str = "0.1.0"

class ValueConflictResponse(BaseModel):
    """Response schema for value conflict detection"""
    
    agent_id: str
    conflict_id: str
    severity: str
    conflict_description: str
    suggested_resolution: str
    resolution_confidence: float
    requires_user_input: bool
    alternative_options: List[str]
    pact_version: str = "0.1.0"

class ValueContextResponse(BaseModel):
    """Response schema for value context sharing"""
    
    agent_id: str
    ethical_significance: float
    active_constraints: List[str]
    ethical_risks: List[str]
    ethical_opportunities: List[str]
    attention_needed: List[str]
    collaboration_guidance: Dict[str, Any]
    pact_version: str = "0.1.0"

class ValueSummaryResponse(BaseModel):
    """Response schema for value alignment summary"""
    
    agent_id: str
    overall_alignment_health: float
    active_conflicts: int
    resolved_conflicts: int
    user_value_profile: Dict[str, float]
    performance_metrics: Dict[str, float]
    recent_ethical_decisions: List[Dict[str, Any]]
    recommendations: List[str]
    pact_version: str = "0.1.0"
