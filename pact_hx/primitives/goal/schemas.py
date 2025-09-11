# pact_hx/primitives/goal/schemas.py
"""
PACT Goal Primitive Schemas

Defines comprehensive data structures for goal understanding, tracking, alignment,
and achievement within the PACT system. Goals are the foundation of meaningful
human-AI collaboration - understanding what users truly want to accomplish
enables the system to provide more effective, contextual, and valuable assistance.

Goal Philosophy:
- Goals exist at multiple levels: immediate tasks, session objectives, long-term aspirations
- Goal understanding evolves through interaction and context
- Goal alignment requires balancing explicit statements with implicit intentions
- Goal achievement involves both task completion and user satisfaction
- Goals can be ambiguous, conflicting, or evolving - the system must handle this gracefully

Schema Categories:
- Core Goal Definitions and Types
- Goal Hierarchy and Relationships  
- Goal Progress and Achievement Tracking
- Goal Alignment and Conflict Resolution
- User Intent and Preference Modeling
- Goal Context and Environmental Factors
"""

from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any, Union, Set, Tuple
from pydantic import BaseModel, Field, validator, root_validator
from uuid import UUID, uuid4
import numpy as np

# ============================================================================
# Core Enums and Constants
# ============================================================================

class GoalType(str, Enum):
    """Types of goals in the system"""
    IMMEDIATE = "immediate"           # Current task or question
    SESSION = "session"               # Goals for this interaction session
    PROJECT = "project"               # Multi-session project goals
    LEARNING = "learning"             # Knowledge acquisition goals
    CREATIVE = "creative"             # Creative output goals
    ANALYTICAL = "analytical"         # Analysis and understanding goals
    PROBLEM_SOLVING = "problem_solving"  # Problem resolution goals
    EXPLORATORY = "exploratory"       # Open-ended exploration
    COLLABORATIVE = "collaborative"   # Collaboration improvement goals
    LONG_TERM = "long_term"          # Extended timeline goals

class GoalStatus(str, Enum):
    """Goal completion and progress status"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    PARTIALLY_COMPLETE = "partially_complete"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    PAUSED = "paused"
    CANCELLED = "cancelled"
    REVISED = "revised"
    FAILED = "failed"

class GoalPriority(str, Enum):
    """Goal priority levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    DEFERRED = "deferred"

class GoalComplexity(str, Enum):
    """Goal complexity assessment"""
    TRIVIAL = "trivial"
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    VERY_COMPLEX = "very_complex"

class GoalClarity(str, Enum):
    """How clearly defined the goal is"""
    CRYSTAL_CLEAR = "crystal_clear"
    CLEAR = "clear"
    SOMEWHAT_CLEAR = "somewhat_clear"
    AMBIGUOUS = "ambiguous"
    VERY_AMBIGUOUS = "very_ambiguous"

class IntentConfidence(str, Enum):
    """Confidence in understanding user intent"""
    VERY_HIGH = "very_high"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    VERY_LOW = "very_low"

class GoalOrigin(str, Enum):
    """How the goal was identified/originated"""
    EXPLICIT_USER_STATEMENT = "explicit_user_statement"
    INFERRED_FROM_CONTEXT = "inferred_from_context"
    DERIVED_FROM_BEHAVIOR = "derived_from_behavior"
    SYSTEM_SUGGESTED = "system_suggested"
    COLLABORATIVE_REFINEMENT = "collaborative_refinement"
    HISTORICAL_PATTERN = "historical_pattern"

class ConflictType(str, Enum):
    """Types of goal conflicts"""
    RESOURCE_CONFLICT = "resource_conflict"
    TIME_CONFLICT = "time_conflict"
    PRIORITY_CONFLICT = "priority_conflict"
    VALUE_CONFLICT = "value_conflict"
    LOGICAL_CONFLICT = "logical_conflict"
    CONTEXT_CONFLICT = "context_conflict"

# ============================================================================
# Core Goal Schemas
# ============================================================================

class BaseGoalModel(BaseModel):
    """Base model for all goal-related schemas"""
    id: str = Field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            timedelta: lambda v: v.total_seconds(),
            np.float64: float,
            np.float32: float,
        }

class GoalMetricSchema(BaseModel):
    """Schema for goal achievement metrics"""
    metric_name: str = Field(..., description="Name of the metric")
    target_value: float = Field(..., description="Target value for success")
    current_value: float = Field(default=0.0, description="Current achieved value")
    unit: str = Field(default="", description="Unit of measurement")
    is_binary: bool = Field(default=False, description="Whether metric is binary (done/not done)")
    weight: float = Field(default=1.0, ge=0.0, le=1.0, description="Importance weight")
    
    @property
    def completion_percentage(self) -> float:
        """Calculate completion percentage"""
        if self.is_binary:
            return 100.0 if self.current_value >= self.target_value else 0.0
        
        if self.target_value == 0:
            return 100.0 if self.current_value == 0 else 0.0
        
        return min(100.0, (self.current_value / self.target_value) * 100.0)

class SuccessCriteriaSchema(BaseModel):
    """Schema defining success criteria for goals"""
    criteria_id: str = Field(default_factory=lambda: str(uuid4()))
    description: str = Field(..., description="Human-readable success criteria")
    metrics: List[GoalMetricSchema] = Field(default_factory=list, description="Quantifiable metrics")
    qualitative_indicators: List[str] = Field(default_factory=list, description="Qualitative success signs")
    user_satisfaction_threshold: float = Field(default=0.7, ge=0.0, le=1.0)
    time_constraint: Optional[timedelta] = Field(None, description="Time limit for achievement")
    required_resources: List[str] = Field(default_factory=list, description="Required resources")

class GoalContextSchema(BaseModel):
    """Schema for goal context and environmental factors"""
    user_context: Dict[str, Any] = Field(default_factory=dict, description="User's current context")
    session_context: Dict[str, Any] = Field(default_factory=dict, description="Session-specific context")
    domain_context: str = Field(default="general", description="Domain or field of the goal")
    urgency_factors: List[str] = Field(default_factory=list, description="Factors affecting urgency")
    constraints: List[str] = Field(default_factory=list, description="Known constraints")
    enabling_factors: List[str] = Field(default_factory=list, description="Factors that help achievement")
    stakeholders: List[str] = Field(default_factory=list, description="People affected by goal achievement")

class GoalSchema(BaseGoalModel):
    """Core schema for representing goals"""
    goal_id: str = Field(default_factory=lambda: f"goal_{uuid4()}")
    title: str = Field(..., description="Brief goal title")
    description: str = Field(..., description="Detailed goal description")
    goal_type: GoalType = Field(..., description="Type/category of goal")
    
    # Goal characteristics
    priority: GoalPriority = Field(default=GoalPriority.MEDIUM)
    complexity: GoalComplexity = Field(default=GoalComplexity.MODERATE)
    clarity: GoalClarity = Field(default=GoalClarity.CLEAR)
    origin: GoalOrigin = Field(..., description="How this goal was identified")
    
    # Status and progress
    status: GoalStatus = Field(default=GoalStatus.NOT_STARTED)
    progress_percentage: float = Field(default=0.0, ge=0.0, le=100.0)
    
    # Success definition
    success_criteria: SuccessCriteriaSchema = Field(..., description="How success is defined")
    
    # Context and relationships
    context: GoalContextSchema = Field(default_factory=GoalContextSchema)
    parent_goal_id: Optional[str] = Field(None, description="Parent goal if this is a sub-goal")
    sub_goal_ids: List[str] = Field(default_factory=list, description="Child sub-goals")
    related_goal_ids: List[str] = Field(default_factory=list, description="Related goals")
    
    # Timing
    created_at: datetime = Field(default_factory=datetime.now)
    start_time: Optional[datetime] = Field(None, description="When work on goal began")
    target_completion: Optional[datetime] = Field(None, description="Target completion time")
    actual_completion: Optional[datetime] = Field(None, description="Actual completion time")
    estimated_duration: Optional[timedelta] = Field(None, description="Estimated time to complete")
    
    # User and system information
    user_id: Optional[str] = Field(None, description="Associated user identifier")
    session_id: Optional[str] = Field(None, description="Session where goal was identified")
    
    # Confidence and uncertainty
    intent_confidence: IntentConfidence = Field(default=IntentConfidence.MEDIUM)
    uncertainty_factors: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    
    # Metadata
    tags: List[str] = Field(default_factory=list, description="Goal tags for categorization")
    notes: List[str] = Field(default_factory=list, description="Additional notes")
    
    @validator('progress_percentage')
    def validate_progress(cls, v, values):
        if 'status' in values:
            status = values['status']
            if status == GoalStatus.NOT_STARTED and v > 0:
                raise ValueError("Progress should be 0 for not started goals")
            elif status == GoalStatus.COMPLETED and v < 100:
                raise ValueError("Progress should be 100 for completed goals")
        return v

# ============================================================================
# Goal Hierarchy and Relationship Schemas
# ============================================================================

class GoalHierarchySchema(BaseGoalModel):
    """Schema for goal hierarchical relationships"""
    hierarchy_id: str = Field(default_factory=lambda: f"hierarchy_{uuid4()}")
    root_goal_id: str = Field(..., description="Top-level goal ID")
    goal_tree: Dict[str, List[str]] = Field(..., description="Tree structure: parent -> [children]")
    depth_map: Dict[str, int] = Field(..., description="Goal ID -> depth level")
    dependency_graph: Dict[str, List[str]] = Field(default_factory=dict, description="Dependencies between goals")
    
    def get_goal_depth(self, goal_id: str) -> int:
        """Get the depth level of a goal"""
        return self.depth_map.get(goal_id, 0)
    
    def get_children(self, goal_id: str) -> List[str]:
        """Get direct children of a goal"""
        return self.goal_tree.get(goal_id, [])
    
    def get_dependencies(self, goal_id: str) -> List[str]:
        """Get goals that this goal depends on"""
        return self.dependency_graph.get(goal_id, [])

class GoalRelationshipSchema(BaseGoalModel):
    """Schema for relationships between goals"""
    relationship_id: str = Field(default_factory=lambda: f"rel_{uuid4()}")
    goal_a_id: str = Field(..., description="First goal ID")
    goal_b_id: str = Field(..., description="Second goal ID")
    relationship_type: str = Field(..., description="Type of relationship")
    strength: float = Field(default=1.0, ge=0.0, le=1.0, description="Relationship strength")
    description: Optional[str] = Field(None, description="Relationship description")
    created_at: datetime = Field(default_factory=datetime.now)
    
    # Common relationship types: "depends_on", "conflicts_with", "supports", 
    # "enables", "blocks", "similar_to", "alternative_to"

# ============================================================================
# Intent and User Modeling Schemas
# ============================================================================

class UserIntentSchema(BaseGoalModel):
    """Schema for modeling user intent"""
    intent_id: str = Field(default_factory=lambda: f"intent_{uuid4()}")
    user_id: Optional[str] = Field(None, description="User identifier")
    session_id: str = Field(..., description="Session identifier")
    
    # Intent details
    primary_intent: str = Field(..., description="Primary user intent")
    secondary_intents: List[str] = Field(default_factory=list, description="Secondary intents")
    implicit_intents: List[str] = Field(default_factory=list, description="Inferred implicit intents")
    
    # Confidence and uncertainty
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence in intent understanding")
    ambiguity_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Level of ambiguity")
    
    # Context that influenced intent understanding
    contextual_clues: List[str] = Field(default_factory=list, description="Clues used to infer intent")
    user_statements: List[str] = Field(default_factory=list, description="Direct user statements")
    behavioral_indicators: List[str] = Field(default_factory=list, description="Behavioral patterns observed")
    
    # Intent evolution
    original_intent: Optional[str] = Field(None, description="Original intent if changed")
    intent_evolution: List[Dict[str, Any]] = Field(default_factory=list, description="How intent has evolved")
    
    # Associated goals
    associated_goal_ids: List[str] = Field(default_factory=list, description="Goals derived from this intent")

class UserPreferenceSchema(BaseModel):
    """Schema for user preferences affecting goal pursuit"""
    preference_id: str = Field(default_factory=lambda: f"pref_{uuid4()}")
    user_id: Optional[str] = Field(None, description="User identifier")
    
    # Preference categories
    communication_preferences: Dict[str, Any] = Field(default_factory=dict)
    work_style_preferences: Dict[str, Any] = Field(default_factory=dict)
    goal_preferences: Dict[str, Any] = Field(default_factory=dict)
    collaboration_preferences: Dict[str, Any] = Field(default_factory=dict)
    
    # Preference strength and confidence
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    learned_from: List[str] = Field(default_factory=list, description="How preferences were learned")
    last_updated: datetime = Field(default_factory=datetime.now)

# ============================================================================
# Goal Progress and Achievement Schemas
# ============================================================================

class GoalProgressEventSchema(BaseGoalModel):
    """Schema for tracking goal progress events"""
    event_id: str = Field(default_factory=lambda: f"event_{uuid4()}")
    goal_id: str = Field(..., description="Associated goal ID")
    event_type: str = Field(..., description="Type of progress event")
    
    # Progress details
    previous_progress: float = Field(..., ge=0.0, le=100.0)
    new_progress: float = Field(..., ge=0.0, le=100.0)
    progress_delta: float = Field(..., description="Change in progress")
    
    # Event context
    description: str = Field(..., description="Description of what happened")
    contributing_factors: List[str] = Field(default_factory=list)
    obstacles_encountered: List[str] = Field(default_factory=list)
    
    # Metrics updates
    updated_metrics: List[GoalMetricSchema] = Field(default_factory=list)
    
    # System and user info
    user_action: Optional[str] = Field(None, description="User action that triggered progress")
    system_contribution: Optional[str] = Field(None, description="How system contributed")
    
    event_timestamp: datetime = Field(default_factory=datetime.now)

class GoalAchievementSchema(BaseGoalModel):
    """Schema for goal achievement and completion"""
    achievement_id: str = Field(default_factory=lambda: f"achievement_{uuid4()}")
    goal_id: str = Field(..., description="Achieved goal ID")
    
    # Achievement details
    completion_time: datetime = Field(default_factory=datetime.now)
    total_duration: timedelta = Field(..., description="Total time from start to completion")
    final_progress: float = Field(..., ge=0.0, le=100.0)
    
    # Success assessment
    success_criteria_met: List[str] = Field(default_factory=list)
    success_criteria_missed: List[str] = Field(default_factory=list)
    overall_success_score: float = Field(..., ge=0.0, le=1.0)
    
    # User satisfaction
    user_satisfaction: float = Field(..., ge=0.0, le=1.0)
    user_feedback: Optional[str] = Field(None, description="User feedback on achievement")
    
    # Achievement quality
    quality_score: float = Field(default=1.0, ge=0.0, le=1.0)
    efficiency_score: float = Field(default=1.0, ge=0.0, le=1.0)
    creativity_score: float = Field(default=0.5, ge=0.0, le=1.0)
    
    # Lessons learned
    what_worked_well: List[str] = Field(default_factory=list)
    what_could_improve: List[str] = Field(default_factory=list)
    insights_gained: List[str] = Field(default_factory=list)
    
    # Impact assessment
    broader_impact: Optional[str] = Field(None, description="Impact beyond immediate goal")
    follow_up_goals: List[str] = Field(default_factory=list, description="Goals spawned from this achievement")

# ============================================================================
# Goal Conflict and Alignment Schemas
# ============================================================================

class GoalConflictSchema(BaseGoalModel):
    """Schema for goal conflicts and tensions"""
    conflict_id: str = Field(default_factory=lambda: f"conflict_{uuid4()}")
    conflicting_goal_ids: List[str] = Field(..., description="Goals in conflict")
    conflict_type: ConflictType = Field(..., description="Type of conflict")
    
    # Conflict details
    severity: float = Field(..., ge=0.0, le=1.0, description="Conflict severity")
    description: str = Field(..., description="Description of the conflict")
    
    # Impact assessment
    affected_goals: List[str] = Field(default_factory=list)
    potential_impact: str = Field(..., description="Potential impact if unresolved")
    
    # Resolution information
    resolution_status: str = Field(default="unresolved")
    resolution_strategy: Optional[str] = Field(None, description="Strategy to resolve conflict")
    resolution_notes: List[str] = Field(default_factory=list)
    
    # Discovery information
    discovered_at: datetime = Field(default_factory=datetime.now)
    discovered_by: str = Field(default="system", description="How conflict was discovered")

class GoalAlignmentSchema(BaseGoalModel):
    """Schema for goal alignment assessment"""
    alignment_id: str = Field(default_factory=lambda: f"alignment_{uuid4()}")
    primary_goal_id: str = Field(..., description="Primary goal being assessed")
    
    # Alignment dimensions
    user_value_alignment: float = Field(..., ge=0.0, le=1.0, description="Alignment with user values")
    system_capability_alignment: float = Field(..., ge=0.0, le=1.0, description="Alignment with system capabilities")
    context_alignment: float = Field(..., ge=0.0, le=1.0, description="Alignment with current context")
    resource_alignment: float = Field(..., ge=0.0, le=1.0, description="Alignment with available resources")
    
    # Overall alignment
    overall_alignment_score: float = Field(..., ge=0.0, le=1.0, description="Overall alignment score")
    alignment_confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in alignment assessment")
    
    # Alignment factors
    supporting_factors: List[str] = Field(default_factory=list, description="Factors supporting alignment")
    misalignment_factors: List[str] = Field(default_factory=list, description="Factors causing misalignment")
    
    # Recommendations
    alignment_recommendations: List[str] = Field(default_factory=list, description="Ways to improve alignment")
    
    assessed_at: datetime = Field(default_factory=datetime.now)

# ============================================================================
# Request/Response Schemas for Goal Management API
# ============================================================================

class CreateGoalRequest(BaseModel):
    """Request schema for creating new goals"""
    title: str = Field(..., description="Goal title")
    description: str = Field(..., description="Goal description")
    goal_type: GoalType = Field(..., description="Type of goal")
    priority: GoalPriority = Field(default=GoalPriority.MEDIUM)
    success_criteria: SuccessCriteriaSchema = Field(..., description="Success criteria")
    context: Optional[GoalContextSchema] = Field(None, description="Goal context")
    parent_goal_id: Optional[str] = Field(None, description="Parent goal if sub-goal")
    target_completion: Optional[datetime] = Field(None, description="Target completion time")
    tags: List[str] = Field(default_factory=list, description="Goal tags")

class UpdateGoalRequest(BaseModel):
    """Request schema for updating goals"""
    goal_id: str = Field(..., description="Goal ID to update")
    updates: Dict[str, Any] = Field(..., description="Fields to update")
    reason: Optional[str] = Field(None, description="Reason for update")

class GoalQueryRequest(BaseModel):
    """Request schema for querying goals"""
    user_id: Optional[str] = Field(None, description="Filter by user ID")
    session_id: Optional[str] = Field(None, description="Filter by session ID") 
    goal_type: Optional[GoalType] = Field(None, description="Filter by goal type")
    status: Optional[GoalStatus] = Field(None, description="Filter by status")
    priority: Optional[GoalPriority] = Field(None, description="Filter by priority")
    tags: Optional[List[str]] = Field(None, description="Filter by tags")
    include_completed: bool = Field(default=True, description="Include completed goals")
    include_sub_goals: bool = Field(default=True, description="Include sub-goals")
    limit: int = Field(default=50, ge=1, le=500, description="Maximum results")

class GoalProgressRequest(BaseModel):
    """Request schema for updating goal progress"""
    goal_id: str = Field(..., description="Goal ID")
    progress_percentage: float = Field(..., ge=0.0, le=100.0, description="New progress percentage")
    description: str = Field(..., description="Description of progress made")
    updated_metrics: Optional[List[GoalMetricSchema]] = Field(None, description="Updated metrics")
    user_action: Optional[str] = Field(None, description="User action that contributed")

class GoalRecommendationRequest(BaseModel):
    """Request schema for goal recommendations"""
    user_id: Optional[str] = Field(None, description="User ID for personalization")
    current_context: Dict[str, Any] = Field(default_factory=dict, description="Current context")
    existing_goals: List[str] = Field(default_factory=list, description="Existing goal IDs")
    recommendation_type: str = Field(default="next_steps", description="Type of recommendation needed")
    max_recommendations: int = Field(default=5, ge=1, le=20, description="Maximum recommendations")

# ============================================================================
# Factory Functions and Utilities
# ============================================================================

def create_simple_goal(title: str, description: str, goal_type: GoalType, **kwargs) -> GoalSchema:
    """Factory function to create a simple goal with minimal requirements"""
    
    # Create default success criteria if not provided
    if 'success_criteria' not in kwargs:
        kwargs['success_criteria'] = SuccessCriteriaSchema(
            description=f"Successfully complete: {title}",
            metrics=[GoalMetricSchema(
                metric_name="completion",
                target_value=1.0,
                is_binary=True,
                unit="complete"
            )]
        )
    
    return GoalSchema(
        title=title,
        description=description,
        goal_type=goal_type,
        origin=GoalOrigin.EXPLICIT_USER_STATEMENT,
        **kwargs
    )

def create_goal_hierarchy(root_goal: GoalSchema, sub_goals: List[GoalSchema]) -> GoalHierarchySchema:
    """Create a goal hierarchy from a root goal and sub-goals"""
    goal_tree = {root_goal.goal_id: [sg.goal_id for sg in sub_goals]}
    depth_map = {root_goal.goal_id: 0}
    
    for sub_goal in sub_goals:
        sub_goal.parent_goal_id = root_goal.goal_id
        depth_map[sub_goal.goal_id] = 1
        goal_tree[sub_goal.goal_id] = []
    
    root_goal.sub_goal_ids = [sg.goal_id for sg in sub_goals]
    
    return GoalHierarchySchema(
        root_goal_id=root_goal.goal_id,
        goal_tree=goal_tree,
        depth_map=depth_map
    )

# ============================================================================
# Validation and Helper Functions
# ============================================================================

def validate_goal_consistency(goal: GoalSchema) -> List[str]:
    """Validate internal consistency of a goal"""
    errors = []
    
    # Check status vs progress consistency
    if goal.status == GoalStatus.NOT_STARTED and goal.progress_percentage > 0:
        errors.append("Goal marked as not started but has progress > 0")
    
    if goal.status == GoalStatus.COMPLETED and goal.progress_percentage < 100:
        errors.append("Goal marked as completed but progress < 100%")
    
    # Check time consistency
    if goal.start_time and goal.target_completion:
        if goal.start_time > goal.target_completion:
            errors.append("Start time is after target completion time")
    
    if goal.actual_completion and goal.start_time:
        if goal.actual_completion < goal.start_time:
            errors.append("Completion time is before start time")
    
    # Check hierarchy consistency
    if goal.parent_goal_id and goal.parent_goal_id == goal.goal_id:
        errors.append("Goal cannot be its own parent")
    
    if goal.goal_id in goal.sub_goal_ids:
        errors.append("Goal cannot be its own sub-goal")
    
    return errors

def calculate_goal_health_score(goal: GoalSchema) -> float:
    """Calculate a health score for a goal based on various factors"""
    score = 1.0
    
    # Penalty for low clarity
    if goal.clarity == GoalClarity.VERY_AMBIGUOUS:
        score *= 0.5
    elif goal.clarity == GoalClarity.AMBIGUOUS:
        score *= 0.7
    
    # Penalty for low intent confidence
    if goal.intent_confidence == IntentConfidence.VERY_LOW:
        score *= 0.6
    elif goal.intent_confidence == IntentConfidence.LOW:
        score *= 0.8
    
    # Penalty for blocked status
    if goal.status == GoalStatus.BLOCKED:
        score *= 0.3
    elif goal.status == GoalStatus.FAILED:
        score *= 0.1
    
    # Bonus for progress
    if goal.progress_percentage > 0:
        score *= (1.0 + goal.progress_percentage / 200.0)  # Small bonus for progress
    
    return min(1.0, max(0.0, score))

# ============================================================================
# Export All Schemas
# ============================================================================

__all__ = [
    # Enums
    "GoalType", "GoalStatus", "GoalPriority", "GoalComplexity", "GoalClarity",
    "IntentConfidence", "GoalOrigin", "ConflictType",
    
    # Core Schemas
    "BaseGoalModel", "GoalMetricSchema", "SuccessCriteriaSchema", "GoalContextSchema", "GoalSchema",
    
    # Hierarchy and Relationships
    "GoalHierarchySchema", "GoalRelationshipSchema",
    
    # Intent and User Modeling
    "UserIntentSchema", "UserPreferenceSchema",
    
    # Progress and Achievement
    "GoalProgressEventSchema", "GoalAchievementSchema",
    
    # Conflict and Alignment
    "GoalConflictSchema", "GoalAlignmentSchema",
    
    # Request/Response Schemas
    "CreateGoalRequest", "UpdateGoalRequest", "GoalQueryRequest", 
    "GoalProgressRequest", "GoalRecommendationRequest",
    
    # Factory Functions
    "create_simple_goal", "create_goal_hierarchy",
    
    # Validation Functions
    "validate_goal_consistency", "calculate_goal_health_score"
]
