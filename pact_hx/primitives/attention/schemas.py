# pact_hx/primitives/attention/schemas.py
"""
PACT-HX Attention Primitive Schemas

Foundation schemas for cognitive attention management in AI systems.
These schemas define the core data structures for tracking what matters
to users and how attention shifts over time.

Core Philosophy: Attention is the cognitive foundation that determines
what gets stored in memory, how tone adapts, and what values apply.
"""

from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from enum import Enum
import uuid

# ========== ENUMS AND CONSTANTS ==========

class AttentionScope(str, Enum):
    """Scope of attention focus - how broad the attention span is"""
    IMMEDIATE = "immediate"         # Current conversation turn (seconds)
    SESSION = "session"             # Current conversation session (minutes)  
    RELATIONSHIP = "relationship"   # Long-term user relationship (days/weeks)
    DOMAIN = "domain"              # Subject matter domain (persistent)

class AttentionTrigger(str, Enum):
    """What triggered an attention shift"""
    USER_EXPLICIT = "user_explicit"         # User directly mentioned/emphasized
    CONTEXT_SHIFT = "context_shift"         # Topic/context naturally changed
    IMPORTANCE_SIGNAL = "importance_signal" # High importance content detected
    EMOTIONAL_SIGNAL = "emotional_signal"   # Emotional content detected
    REPETITION = "repetition"               # User repeated/emphasized something
    COLLABORATION = "collaboration"         # Signal from another primitive
    DECAY = "decay"                        # Natural attention decay over time

class EntityType(str, Enum):
    """Types of entities that can receive attention"""
    PERSON = "person"              # People, names, pronouns
    CONCEPT = "concept"            # Abstract concepts, ideas
    TOPIC = "topic"               # Discussion topics, subjects
    TASK = "task"                 # Actions, goals, todos
    EMOTION = "emotion"           # Emotional states, feelings
    REFERENCE = "reference"       # URLs, documents, external refs
    TEMPORAL = "temporal"         # Time references, dates, schedules
    LOCATION = "location"         # Places, geographic references
    OBJECT = "object"             # Physical or digital objects
    UNKNOWN = "unknown"           # Unclassified entities

# ========== CORE ENTITY SCHEMAS ==========

class AttentionEntity(BaseModel):
    """
    Individual entity being tracked by attention system
    
    Represents a single concept, person, topic, or object that the
    attention system is monitoring for importance and relevance.
    """
    
    # Identity
    entity_id: str = Field(..., description="Unique identifier for this entity")
    entity_type: EntityType = Field(..., description="Classification of entity type")
    entity_value: str = Field(..., description="The actual entity text/value")
    canonical_form: Optional[str] = Field(None, description="Normalized form of entity")
    
    # Core attention metrics
    salience_score: float = Field(
        default=0.5, 
        ge=0.0, 
        le=1.0, 
        description="Current importance/salience score"
    )
    confidence_score: float = Field(
        default=0.8,
        ge=0.0,
        le=1.0,
        description="Confidence in entity identification"
    )
    
    # Temporal tracking
    first_mentioned: datetime = Field(default_factory=datetime.now)
    last_mentioned: datetime = Field(default_factory=datetime.now)
    mention_count: int = Field(default=1, ge=1, description="Total times mentioned")
    focus_duration: float = Field(default=0.0, ge=0.0, description="Total focus time (seconds)")
    
    # Context and relationships
    contexts: List[str] = Field(
        default_factory=list, 
        description="Contexts where entity appeared"
    )
    co_occurring_entities: Dict[str, int] = Field(
        default_factory=dict, 
        description="Entities that frequently appear together"
    )
    semantic_neighbors: List[str] = Field(
        default_factory=list,
        description="Semantically related entities"
    )
    
    # User interaction signals
    user_emphasis: float = Field(
        default=0.0, 
        ge=-1.0, 
        le=1.0, 
        description="User's explicit emphasis on this entity"
    )
    emotional_valence: Optional[str] = Field(
        None, 
        description="Emotional association (positive/negative/neutral)"
    )
    user_corrections: int = Field(
        default=0, 
        description="Number of times user corrected focus on this entity"
    )
    
    # Learning and adaptation
    importance_trend: List[float] = Field(
        default_factory=list, 
        description="Historical importance scores"
    )
    attention_patterns: Dict[str, Any] = Field(
        default_factory=dict,
        description="Learned patterns about when this entity is important"
    )
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    @validator('salience_score', 'confidence_score', 'user_emphasis')
    def validate_scores(cls, v):
        """Ensure scores are within valid bounds"""
        return max(-1.0, min(1.0, v))
    
    def update_salience(self, new_score: float, learning_rate: float = 0.3):
        """Update salience using exponential moving average"""
        self.salience_score = (1 - learning_rate) * self.salience_score + learning_rate * new_score
        self.importance_trend.append(self.salience_score)
        
        # Keep trend history manageable
        if len(self.importance_trend) > 50:
            self.importance_trend = self.importance_trend[-50:]
        
        self.updated_at = datetime.now()

# ========== FOCUS MANAGEMENT SCHEMAS ==========

class AttentionFocus(BaseModel):
    """
    Represents a specific attention focus state
    
    Defines what the attention system is currently focusing on,
    including primary and secondary entities, confidence levels,
    and contextual information.
    """
    
    # Identity
    focus_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    scope: AttentionScope = Field(..., description="Scope of this attention focus")
    
    # Entity composition
    primary_entities: List[str] = Field(
        ..., 
        description="Main entities in focus (entity_ids)"
    )
    secondary_entities: List[str] = Field(
        default_factory=list, 
        description="Secondary/supporting entities"
    )
    background_entities: List[str] = Field(
        default_factory=list,
        description="Entities in background awareness"
    )
    
    # Focus strength and quality
    focus_strength: float = Field(
        default=0.5,
        ge=0.0, 
        le=1.0, 
        description="How strong/intense is this focus"
    )
    focus_confidence: float = Field(
        default=0.5,
        ge=0.0, 
        le=1.0, 
        description="Confidence in focus accuracy"
    )
    focus_stability: float = Field(
        default=0.5, 
        ge=0.0, 
        le=1.0, 
        description="How stable/persistent is this focus"
    )
    focus_clarity: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="How clear/well-defined is this focus"
    )
    
    # Temporal aspects
    started_at: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)
    expected_duration: Optional[float] = Field(
        None, 
        description="Expected focus duration in seconds"
    )
    actual_duration: Optional[float] = Field(
        None,
        description="Actual focus duration when completed"
    )
    
    # Context and causation
    trigger: AttentionTrigger = Field(..., description="What triggered this focus")
    trigger_confidence: float = Field(
        default=0.8,
        ge=0.0,
        le=1.0,
        description="Confidence in trigger identification"
    )
    context_summary: str = Field(
        ..., 
        max_length=500,
        description="Summary of the context that created this focus"
    )
    
    # Relationships
    parent_focus: Optional[str] = Field(
        None, 
        description="Parent focus ID if this is a sub-focus"
    )
    child_focuses: List[str] = Field(
        default_factory=list,
        description="Child focus IDs spawned from this focus"
    )
    related_focuses: List[str] = Field(
        default_factory=list, 
        description="Related/similar focus IDs"
    )
    
    # Performance tracking
    user_alignment: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="How well this focus aligned with user intent"
    )
    effectiveness_score: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="How effective this focus was"
    )
    
    def calculate_overall_quality(self) -> float:
        """Calculate overall focus quality score"""
        quality_factors = [
            self.focus_strength,
            self.focus_confidence,
            self.focus_stability,
            self.focus_clarity
        ]
        
        return sum(quality_factors) / len(quality_factors)
    
    def is_active(self) -> bool:
        """Check if this focus is currently active"""
        return self.actual_duration is None

# ========== TRANSITION SCHEMAS ==========

class AttentionTransition(BaseModel):
    """
    Record of attention transition between focuses
    
    Captures how and why attention shifted from one focus to another,
    including transition quality and user response.
    """
    
    # Identity
    transition_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    
    # Transition path
    from_focus: Optional[str] = Field(None, description="Previous focus ID")
    to_focus: str = Field(..., description="New focus ID")
    
    # Transition characteristics
    transition_type: str = Field(
        ..., 
        description="Type: smooth, abrupt, triggered, decay, branched"
    )
    transition_reason: str = Field(
        ..., 
        description="Why attention shifted"
    )
    transition_strength: float = Field(
        default=0.5,
        ge=0.0, 
        le=1.0, 
        description="How strong/dramatic was the shift"
    )
    transition_smoothness: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="How smooth vs jarring was the transition"
    )
    
    # Timing information
    occurred_at: datetime = Field(default_factory=datetime.now)
    transition_duration: float = Field(
        default=0.0, 
        ge=0.0,
        description="How long the transition took (seconds)"
    )
    preparation_time: float = Field(
        default=0.0,
        ge=0.0,
        description="Time spent preparing for transition"
    )
    
    # Contextual factors
    context_overlap: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="How much context overlapped between focuses"
    )
    user_triggered: bool = Field(
        default=False,
        description="Whether user explicitly triggered this transition"
    )
    
    # Quality and performance
    transition_quality: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Overall quality of this transition"
    )
    user_followed: Optional[bool] = Field(
        None, 
        description="Did user successfully follow the transition"
    )
    user_satisfaction: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="User satisfaction with transition"
    )
    
    # Learning signals
    success_indicators: List[str] = Field(
        default_factory=list,
        description="Indicators that transition was successful"
    )
    failure_indicators: List[str] = Field(
        default_factory=list,
        description="Indicators that transition was problematic"
    )

# ========== CONFIGURATION SCHEMAS ==========

class AttentionDecayRule(BaseModel):
    """
    Rules for how attention decays over time
    
    Defines mathematical functions and parameters for how entity
    salience scores decrease over time without reinforcement.
    """
    
    # Decay function configuration
    decay_function: str = Field(
        default="exponential", 
        description="Decay function: linear, exponential, logarithmic, custom"
    )
    decay_rate: float = Field(
        default=0.1, 
        ge=0.0, 
        le=1.0, 
        description="Base decay rate (0 = no decay, 1 = immediate decay)"
    )
    decay_interval: float = Field(
        default=3600.0,
        ge=1.0,
        description="Decay interval in seconds (how often decay is applied)"
    )
    
    # Decay resistance factors
    minimum_salience: float = Field(
        default=0.05, 
        ge=0.0, 
        le=1.0, 
        description="Minimum salience before entity is pruned"
    )
    importance_resistance: float = Field(
        default=0.8,
        ge=0.0,
        le=1.0,
        description="How much importance resists decay"
    )
    emotional_resistance: float = Field(
        default=0.9,
        ge=0.0,
        le=1.0,
        description="How much emotional association resists decay"
    )
    recency_resistance: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="How much recent mention resists decay"
    )
    
    # Context-specific modifiers
    context_modifiers: Dict[str, float] = Field(
        default_factory=dict, 
        description="Decay rate modifiers by context type"
    )
    entity_type_modifiers: Dict[EntityType, float] = Field(
        default_factory=dict,
        description="Decay rate modifiers by entity type"
    )
    
    # Advanced parameters
    cascade_decay: bool = Field(
        default=False,
        description="Whether decay cascades to related entities"
    )
    adaptive_decay: bool = Field(
        default=True,
        description="Whether decay adapts based on user patterns"
    )

class AttentionConfiguration(BaseModel):
    """
    Configuration parameters for attention management
    
    Defines operational parameters, thresholds, and behavioral
    settings for the attention primitive.
    """
    
    # Capacity limits
    max_tracked_entities: int = Field(
        default=1000, 
        ge=10,
        description="Maximum entities to track simultaneously"
    )
    max_focus_history: int = Field(
        default=100,
        ge=5,
        description="Maximum focus history to maintain"
    )
    max_concurrent_focus: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Maximum entities in primary focus"
    )
    
    # Processing thresholds
    salience_threshold: float = Field(
        default=0.3,
        ge=0.0,
        le=1.0,
        description="Minimum salience for focus consideration"
    )
    focus_stability_threshold: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Threshold for stable focus maintenance"
    )
    transition_threshold: float = Field(
        default=0.4,
        ge=0.0,
        le=1.0,
        description="Threshold for triggering focus transitions"
    )
    
    # Learning parameters
    learning_rate: float = Field(
        default=0.1,
        ge=0.01,
        le=1.0,
        description="Rate of adaptation from feedback"
    )
    feedback_sensitivity: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Sensitivity to user feedback signals"
    )
    
    # Collaboration settings
    collaboration_weight: float = Field(
        default=0.3,
        ge=0.0,
        le=1.0,
        description="Weight given to collaboration signals"
    )
    signal_trust_threshold: float = Field(
        default=0.6,
        ge=0.0,
        le=1.0,
        description="Minimum trust for external signals"
    )

# ========== STATE MANAGEMENT SCHEMAS ==========

class AttentionState(BaseModel):
    """
    Complete attention state for an agent
    
    Root state object containing all attention-related data,
    configuration, and operational state for a single agent.
    """
    
    # Identity and metadata
    agent_id: str = Field(..., description="Unique agent identifier")
    user_id: Optional[str] = Field(None, description="Associated user identifier")
    session_id: Optional[str] = Field(None, description="Current session identifier")
    
    # Current operational state
    current_focus: Optional[AttentionFocus] = Field(
        None, 
        description="Current active attention focus"
    )
    focus_stack: List[AttentionFocus] = Field(
        default_factory=list, 
        description="Stack of recent focuses for context"
    )
    pending_transitions: List[str] = Field(
        default_factory=list,
        description="Focus transitions queued for execution"
    )
    
    # Entity tracking
    tracked_entities: Dict[str, AttentionEntity] = Field(
        default_factory=dict, 
        description="All entities currently being tracked"
    )
    entity_relationships: Dict[str, List[str]] = Field(
        default_factory=dict, 
        description="Graph of entity relationships"
    )
    entity_clusters: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="Clusters of related entities"
    )
    
    # Historical data
    focus_history: List[AttentionFocus] = Field(
        default_factory=list, 
        description="Historical focus records"
    )
    transition_history: List[AttentionTransition] = Field(
        default_factory=list, 
        description="Historical transition records"
    )
    
    # Configuration and rules
    config: AttentionConfiguration = Field(
        default_factory=AttentionConfiguration,
        description="Attention configuration parameters"
    )
    decay_rules: AttentionDecayRule = Field(
        default_factory=AttentionDecayRule,
        description="Attention decay configuration"
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
    signal_history: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="History of external signals"
    )
    
    # Performance and analytics
    attention_accuracy: float = Field(
        default=0.0, 
        description="Overall attention prediction accuracy"
    )
    focus_stability_score: float = Field(
        default=0.0, 
        description="Stability of focus transitions"
    )
    user_alignment_score: float = Field(
        default=0.0, 
        description="Alignment with user intent"
    )
    adaptation_rate: float = Field(
        default=0.0,
        description="Rate of successful adaptation"
    )
    
    # Operational metrics
    total_interactions: int = Field(default=0)
    total_focus_shifts: int = Field(default=0)
    total_entities_tracked: int = Field(default=0)
    average_focus_duration: float = Field(default=0.0)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)
    last_decay_applied: datetime = Field(default_factory=datetime.now)
    last_optimization: datetime = Field(default_factory=datetime.now)
    
    def get_active_entities(self) -> List[str]:
        """Get currently active/focused entity IDs"""
        if self.current_focus:
            return self.current_focus.primary_entities + self.current_focus.secondary_entities
        return []
    
    def get_top_entities(self, limit: int = 10) -> List[Tuple[str, float]]:
        """Get top entities by salience score"""
        sorted_entities = sorted(
            self.tracked_entities.items(),
            key=lambda x: x[1].salience_score,
            reverse=True
        )
        return [(entity_id, entity.salience_score) for entity_id, entity in sorted_entities[:limit]]
    
    def calculate_focus_diversity(self) -> float:
        """Calculate diversity of recent focuses"""
        if len(self.focus_history) < 2:
            return 0.0
        
        recent_entities = set()
        for focus in self.focus_history[-10:]:  # Last 10 focuses
            recent_entities.update(focus.primary_entities)
        
        return min(len(recent_entities) / 20.0, 1.0)  # Normalize to 20 max entities

# ========== API RESPONSE SCHEMAS ==========

class AttentionContextResponse(BaseModel):
    """Response schema for attention context requests"""
    
    agent_id: str
    current_focus: Optional[List[str]] = None
    salience_weights: Dict[str, float] = Field(default_factory=dict)
    focus_strength: float = 0.0
    focus_confidence: float = 0.0
    attention_stability: float = 0.0
    total_tracked_entities: int = 0
    last_updated: datetime
    pact_version: str = "0.1.0"

class AttentionUpdateResponse(BaseModel):
    """Response schema for attention updates"""
    
    agent_id: str
    update_successful: bool
    focus_changed: bool
    new_entities_tracked: int
    current_focus: List[str]
    salience_weights: Dict[str, float]
    focus_quality_score: float
    transition_info: Optional[Dict[str, Any]] = None
    pact_version: str = "0.1.0"

class AttentionAnalyticsResponse(BaseModel):
    """Response schema for attention analytics"""
    
    agent_id: str
    performance_metrics: Dict[str, float]
    entity_statistics: Dict[str, Any]
    focus_patterns: Dict[str, Any]
    transition_analysis: Dict[str, Any]
    collaboration_status: Dict[str, Any]
    recommendations: List[str]
    pact_version: str = "0.1.0"
