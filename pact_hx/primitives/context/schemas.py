# pact_hx/primitives/context/schemas.py
"""
PACT Context Manager - Complete Schemas

Comprehensive data schemas for the Context Manager that provides situational 
intelligence and environmental awareness to all other primitives in the PACT system.

The Context Manager serves as the situational intelligence hub, providing rich
contextual awareness that makes all other primitives smarter and more adaptive.

Key Schema Categories:
- Environmental Context: Physical and digital environment factors
- Social Context: Human relationships, cultural factors, team dynamics
- Temporal Context: Time-based patterns, schedules, deadlines, rhythms
- Task Context: Current objectives, workflows, project states
- Emotional Context: Mood, sentiment, energy levels, emotional climate
- Historical Context: Past patterns, learned preferences, outcome history
- Meta Context: Context about context, awareness levels, confidence scores

Integration Points:
- Feeds Goal Manager with situation-appropriate objective setting
- Informs Value Alignment with cultural and situational ethical nuances
- Guides Attention Manager toward contextually relevant focus areas
- Provides Memory Manager with contextual relevance for storage/retrieval
"""

from typing import Dict, Any, List, Optional, Set, Tuple, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
import time
import uuid
from datetime import datetime, timedelta
import json

# ==================== CORE ENUMS ====================

class ContextType(Enum):
    """Types of context the manager tracks"""
    ENVIRONMENTAL = "environmental"    # Physical/digital environment
    SOCIAL = "social"                 # Relationships, cultural factors
    TEMPORAL = "temporal"             # Time-based patterns and constraints
    TASK = "task"                     # Current objectives and workflows
    EMOTIONAL = "emotional"           # Mood, sentiment, energy levels
    HISTORICAL = "historical"         # Past patterns and outcomes
    COGNITIVE = "cognitive"           # Mental state, focus, cognitive load
    COMMUNICATION = "communication"   # Communication patterns and styles
    TECHNICAL = "technical"           # System states, tool availability
    META = "meta"                     # Context about context itself


class ContextScope(Enum):
    """Scope or range of contextual influence"""
    IMMEDIATE = "immediate"           # Current moment, instant context
    SESSION = "session"               # Current interaction session
    DAILY = "daily"                   # Daily patterns and context
    WEEKLY = "weekly"                 # Weekly cycles and patterns
    PROJECT = "project"               # Project-specific context
    RELATIONSHIP = "relationship"     # Ongoing relationship context
    SEASONAL = "seasonal"             # Seasonal or long-term patterns
    CULTURAL = "cultural"             # Cultural and societal context
    UNIVERSAL = "universal"           # Universal human context


class ContextPriority(Enum):
    """Priority levels for different contextual factors"""
    CRITICAL = "critical"             # Must be considered immediately
    HIGH = "high"                     # Strongly influences decisions
    MEDIUM = "medium"                 # Moderately influences decisions
    LOW = "low"                       # Background influence
    IGNORE = "ignore"                 # Can be safely ignored


class ContextConfidence(Enum):
    """Confidence levels in contextual information"""
    CERTAIN = "certain"               # 0.9-1.0 confidence
    HIGH = "high"                     # 0.7-0.9 confidence
    MEDIUM = "medium"                 # 0.5-0.7 confidence
    LOW = "low"                       # 0.3-0.5 confidence
    UNCERTAIN = "uncertain"           # 0.0-0.3 confidence


class EnvironmentalType(Enum):
    """Types of environmental context"""
    PHYSICAL_LOCATION = "physical_location"     # Where the user is
    DIGITAL_ENVIRONMENT = "digital_environment" # What digital tools/apps
    AMBIENT_CONDITIONS = "ambient_conditions"   # Noise, lighting, etc.
    DEVICE_CONTEXT = "device_context"          # What device being used
    NETWORK_CONDITIONS = "network_conditions"   # Connectivity status
    WORKSPACE_SETUP = "workspace_setup"        # Physical workspace


class SocialContextType(Enum):
    """Types of social context"""
    RELATIONSHIP_DYNAMICS = "relationship_dynamics"   # Who user is with
    TEAM_CONTEXT = "team_context"                     # Team state/dynamics
    CULTURAL_NORMS = "cultural_norms"                 # Cultural expectations
    COMMUNICATION_STYLE = "communication_style"       # Preferred comm style
    SOCIAL_ENERGY = "social_energy"                   # Social battery level
    HIERARCHY_CONTEXT = "hierarchy_context"           # Org/social hierarchy


class TemporalContextType(Enum):
    """Types of temporal context"""
    TIME_OF_DAY = "time_of_day"                   # Morning, afternoon, etc.
    DAY_OF_WEEK = "day_of_week"                   # Monday energy vs Friday
    SCHEDULE_PRESSURE = "schedule_pressure"        # How pressed for time
    DEADLINE_PROXIMITY = "deadline_proximity"      # How close to deadlines
    ENERGY_RHYTHM = "energy_rhythm"               # Personal energy cycles
    MEETING_CONTEXT = "meeting_context"           # In/before/after meetings


class EmotionalContextType(Enum):
    """Types of emotional context"""
    MOOD_STATE = "mood_state"                     # Current emotional state
    STRESS_LEVEL = "stress_level"                 # Current stress level
    MOTIVATION_LEVEL = "motivation_level"         # How motivated/engaged
    CONFIDENCE_LEVEL = "confidence_level"         # How confident feeling
    EMOTIONAL_CLIMATE = "emotional_climate"       # Overall emotional environment
    ENERGY_LEVEL = "energy_level"                # Physical/mental energy


# ==================== CORE DATA STRUCTURES ====================

@dataclass
class ContextFactor:
    """Individual contextual element with rich metadata"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: ContextType
    subtype: str = ""  # Specific subtype (e.g., "time_of_day" for temporal)
    key: str = ""      # Specific factor name
    value: Any = None  # The actual contextual value
    
    # Confidence and reliability
    confidence: float = 1.0  # 0-1 scale
    confidence_level: ContextConfidence = ContextConfidence.HIGH
    reliability: float = 1.0  # How reliable this source typically is
    
    # Importance and influence
    priority: ContextPriority = ContextPriority.MEDIUM
    influence_weight: float = 0.5  # How much this affects decisions
    scope: ContextScope = ContextScope.SESSION
    
    # Temporal information
    timestamp: float = field(default_factory=time.time)
    validity_duration: Optional[float] = None  # How long this context is valid
    expiry_time: Optional[float] = None
    staleness_tolerance: float = 3600  # Seconds before considered stale
    
    # Source and provenance
    source: str = "unknown"
    source_type: str = "system"  # system, user, sensor, inference, etc.
    collection_method: str = "direct"  # direct, inferred, learned, etc.
    
    # Contextual relationships
    related_factors: List[str] = field(default_factory=list)  # IDs of related factors
    dependency_factors: List[str] = field(default_factory=list)  # Factors this depends on
    influences_factors: List[str] = field(default_factory=list)  # Factors this influences
    
    # Change tracking
    change_frequency: str = "stable"  # stable, slow, moderate, fast, volatile
    last_change_time: float = field(default_factory=time.time)
    change_magnitude: float = 0.0  # How much it changed (0-1 scale)
    trend_direction: str = "stable"  # increasing, decreasing, stable, oscillating
    
    # Validation and quality
    is_validated: bool = False
    validation_method: str = ""
    quality_score: float = 1.0  # Overall quality of this context factor
    
    # Rich metadata
    description: str = ""
    tags: Set[str] = field(default_factory=set)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EnvironmentalContext:
    """Environmental context information"""
    location_type: str = ""  # office, home, cafe, mobile, etc.
    location_specific: str = ""  # specific location if known
    device_type: str = ""  # laptop, mobile, tablet, desktop, etc.
    screen_size: str = ""  # small, medium, large
    input_methods: List[str] = field(default_factory=list)  # keyboard, touch, voice
    
    # Physical environment
    lighting_condition: str = ""  # bright, dim, natural, artificial
    noise_level: str = ""  # quiet, moderate, noisy, very_noisy
    ambient_temperature: str = ""  # comfortable, hot, cold
    privacy_level: str = ""  # private, semi_private, public
    
    # Digital environment
    application_context: str = ""  # what app/environment they're in
    browser_context: str = ""  # if in browser, what type of content
    notification_state: str = ""  # notifications on/off/limited
    connectivity_quality: str = ""  # excellent, good, poor, offline
    
    # Workspace setup
    workspace_quality: str = ""  # ergonomic, cramped, comfortable
    available_tools: List[str] = field(default_factory=list)
    workspace_distractions: List[str] = field(default_factory=list)
    
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SocialContext:
    """Social and interpersonal context"""
    interaction_mode: str = ""  # solo, one_on_one, small_group, large_group
    relationship_type: str = ""  # colleague, friend, manager, stranger, etc.
    communication_formality: str = ""  # formal, informal, casual
    cultural_context: str = ""  # cultural background considerations
    
    # Team/group dynamics
    team_size: int = 0
    team_familiarity: str = ""  # well_known, somewhat_known, new
    team_dynamics: str = ""  # collaborative, competitive, supportive
    hierarchy_present: bool = False
    decision_maker_present: bool = False
    
    # Communication patterns
    preferred_communication_style: str = ""  # direct, diplomatic, encouraging
    communication_urgency: str = ""  # immediate, normal, patient
    feedback_style_preference: str = ""  # direct, gentle, detailed
    
    # Social energy and capacity
    social_battery_level: str = ""  # full, medium, low, drained
    interpersonal_comfort: str = ""  # very_comfortable, comfortable, neutral, awkward
    collaboration_readiness: str = ""  # eager, willing, reluctant, unavailable
    
    # Cultural and contextual factors
    time_zone_considerations: List[str] = field(default_factory=list)
    cultural_sensitivities: List[str] = field(default_factory=list)
    language_preferences: List[str] = field(default_factory=list)
    
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TemporalContext:
    """Time-based context and patterns"""
    current_time_context: str = ""  # morning, afternoon, evening, night
    day_of_week_context: str = ""  # monday_blues, friday_energy, weekend_mode
    time_pressure_level: str = ""  # relaxed, moderate, urgent, crisis
    
    # Schedule and deadlines
    next_commitment_minutes: Optional[int] = None
    available_time_blocks: List[str] = field(default_factory=list)
    upcoming_deadlines: List[Dict[str, Any]] = field(default_factory=list)
    schedule_density: str = ""  # light, moderate, packed, overwhelming
    
    # Personal rhythms and patterns
    energy_cycle_phase: str = ""  # peak, good, declining, low
    focus_time_remaining: Optional[int] = None  # estimated minutes of good focus
    productivity_window: str = ""  # prime_time, good_time, off_peak
    
    # Timing preferences and patterns
    preferred_interaction_length: str = ""  # quick, normal, extended, unlimited
    attention_span_estimate: int = 0  # estimated minutes
    break_need_level: str = ""  # no_break_needed, could_use_break, needs_break
    
    # Calendar and schedule awareness
    meeting_context: str = ""  # before_meeting, in_meeting, after_meeting, no_meetings
    meeting_fatigue_level: str = ""  # fresh, moderate, tired, exhausted
    context_switching_cost: str = ""  # low, moderate, high
    
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TaskContext:
    """Current task and workflow context"""
    primary_task_type: str = ""  # creative, analytical, administrative, learning
    task_complexity: str = ""  # simple, moderate, complex, very_complex
    task_urgency: str = ""  # low, medium, high, critical
    task_progress: float = 0.0  # 0-1 completion estimate
    
    # Workflow state
    workflow_stage: str = ""  # planning, executing, reviewing, completing
    current_focus_area: str = ""  # what aspect they're working on
    decision_points: List[str] = field(default_factory=list)
    blockers: List[str] = field(default_factory=list)
    
    # Cognitive requirements
    required_thinking_type: str = ""  # convergent, divergent, critical, creative
    cognitive_load_level: str = ""  # light, moderate, heavy, overloaded
    multitasking_level: str = ""  # single_focus, light_multi, heavy_multi
    
    # Task goals and objectives
    immediate_goals: List[str] = field(default_factory=list)
    session_goals: List[str] = field(default_factory=list)
    success_criteria: List[str] = field(default_factory=list)
    
    # Tools and resources
    required_tools: List[str] = field(default_factory=list)
    available_resources: List[str] = field(default_factory=list)
    knowledge_gaps: List[str] = field(default_factory=list)
    
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EmotionalContext:
    """Emotional and psychological context"""
    primary_mood: str = ""  # happy, focused, stressed, excited, etc.
    mood_intensity: str = ""  # mild, moderate, strong, intense
    mood_stability: str = ""  # stable, fluctuating, volatile
    emotional_trajectory: str = ""  # improving, stable, declining
    
    # Stress and pressure
    stress_level: str = ""  # minimal, low, moderate, high, overwhelming
    stress_sources: List[str] = field(default_factory=list)
    coping_capacity: str = ""  # high, moderate, low, depleted
    
    # Motivation and engagement
    motivation_level: str = ""  # very_high, high, moderate, low, very_low
    engagement_level: str = ""  # fully_engaged, engaged, neutral, disengaged
    interest_level: str = ""  # very_interested, interested, neutral, bored
    
    # Confidence and capability feelings
    confidence_level: str = ""  # very_confident, confident, uncertain, insecure
    competence_feeling: str = ""  # expert, competent, learning, struggling
    autonomy_feeling: str = ""  # fully_autonomous, guided, dependent, overwhelmed
    
    # Energy and capacity
    mental_energy: str = ""  # high, medium, low, depleted
    emotional_energy: str = ""  # full, good, moderate, low, drained
    physical_energy: str = ""  # energetic, normal, tired, exhausted
    
    # Emotional needs and preferences
    support_need_level: str = ""  # independent, light_support, moderate_support, high_support
    feedback_receptivity: str = ""  # very_open, open, selective, defensive
    risk_tolerance: str = ""  # high, moderate, low, risk_averse
    
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CognitiveContext:
    """Cognitive state and mental context"""
    attention_state: str = ""  # focused, scattered, distracted, hyperfocused
    cognitive_load: str = ""  # light, optimal, heavy, overloaded
    processing_speed: str = ""  # fast, normal, slow, impaired
    working_memory_state: str = ""  # clear, busy, full, overwhelmed
    
    # Thinking patterns
    thinking_style: str = ""  # analytical, intuitive, creative, systematic
    problem_solving_mode: str = ""  # exploring, converging, stuck, breakthrough
    decision_making_state: str = ""  # decisive, deliberating, conflicted, paralyzed
    
    # Mental clarity and sharpness
    mental_clarity: str = ""  # crystal_clear, clear, foggy, confused
    concentration_quality: str = ""  # excellent, good, poor, impossible
    mental_fatigue_level: str = ""  # fresh, slight, moderate, severe
    
    # Learning and comprehension
    learning_readiness: str = ""  # very_ready, ready, moderate, poor
    comprehension_speed: str = ""  # fast, normal, slow, struggling
    retention_capacity: str = ""  # excellent, good, moderate, poor
    
    # Creative and innovative capacity
    creative_openness: str = ""  # very_open, open, moderate, closed
    innovation_readiness: str = ""  # breakthrough_ready, open, conservative, rigid
    
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class HistoricalContext:
    """Historical patterns and learned context"""
    interaction_history_summary: str = ""
    successful_patterns: List[str] = field(default_factory=list)
    challenging_patterns: List[str] = field(default_factory=list)
    learned_preferences: Dict[str, Any] = field(default_factory=dict)
    
    # Pattern recognition
    recurring_themes: List[str] = field(default_factory=list)
    seasonal_patterns: Dict[str, Any] = field(default_factory=dict)
    progression_patterns: List[str] = field(default_factory=list)
    
    # Success and failure patterns
    high_success_contexts: List[Dict[str, Any]] = field(default_factory=list)
    challenging_contexts: List[Dict[str, Any]] = field(default_factory=list)
    adaptation_history: List[Dict[str, Any]] = field(default_factory=list)
    
    # Learning and growth tracking
    skill_progression: Dict[str, Any] = field(default_factory=dict)
    knowledge_growth: Dict[str, Any] = field(default_factory=dict)
    behavioral_changes: List[Dict[str, Any]] = field(default_factory=list)
    
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ContextSnapshot:
    """Complete contextual state at a point in time"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)
    
    # Core context components
    environmental: EnvironmentalContext = field(default_factory=EnvironmentalContext)
    social: SocialContext = field(default_factory=SocialContext)
    temporal: TemporalContext = field(default_factory=TemporalContext)
    task: TaskContext = field(default_factory=TaskContext)
    emotional: EmotionalContext = field(default_factory=EmotionalContext)
    cognitive: CognitiveContext = field(default_factory=CognitiveContext)
    historical: HistoricalContext = field(default_factory=HistoricalContext)
    
    # Individual context factors
    context_factors: List[ContextFactor] = field(default_factory=list)
    
    # Aggregate metrics
    overall_context_quality: float = 0.0  # How rich/complete the context is
    context_confidence: float = 0.0  # Average confidence across factors
    context_stability: float = 0.0  # How stable/consistent the context is
    context_complexity: float = 0.0  # How complex/nuanced the situation is
    
    # Context relationships and patterns
    dominant_context_types: List[ContextType] = field(default_factory=list)
    context_interactions: Dict[str, Any] = field(default_factory=dict)
    emergent_patterns: List[str] = field(default_factory=list)
    
    # Situational summary
    situation_summary: str = ""
    key_considerations: List[str] = field(default_factory=list)
    adaptation_recommendations: List[str] = field(default_factory=list)
    
    # Context hash for change detection
    context_hash: str = ""
    previous_snapshot_id: Optional[str] = None
    context_delta: Dict[str, Any] = field(default_factory=dict)
    
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ContextPattern:
    """Identified pattern in contextual information"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    pattern_type: str = ""  # recurring, seasonal, causal, correlational
    name: str = ""
    description: str = ""
    
    # Pattern characteristics
    frequency: str = ""  # once, rare, occasional, frequent, constant
    reliability: float = 0.0  # How reliably this pattern occurs
    predictive_power: float = 0.0  # How well this predicts outcomes
    
    # Pattern components
    trigger_conditions: List[Dict[str, Any]] = field(default_factory=list)
    context_signature: Dict[str, Any] = field(default_factory=dict)
    typical_outcomes: List[str] = field(default_factory=list)
    
    # Temporal aspects
    typical_duration: Optional[float] = None
    seasonal_variation: bool = False
    time_of_day_sensitivity: bool = False
    
    # Discovery and validation
    first_observed: float = field(default_factory=time.time)
    last_observed: float = field(default_factory=time.time)
    observation_count: int = 0
    confidence_level: float = 0.0
    
    # Impact and importance
    impact_on_outcomes: str = ""  # high, medium, low, negligible
    actionability: str = ""  # highly_actionable, somewhat_actionable, informational
    
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ContextChange:
    """Represents a change in contextual state"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)
    change_type: str = ""  # sudden, gradual, periodic, triggered
    
    # Change details
    changed_factors: List[str] = field(default_factory=list)  # Factor IDs that changed
    change_magnitude: float = 0.0  # Overall magnitude of change (0-1)
    change_significance: str = ""  # minor, moderate, major, critical
    
    # Before and after states
    previous_snapshot_id: str = ""
    current_snapshot_id: str = ""
    context_delta: Dict[str, Any] = field(default_factory=dict)
    
    # Change triggers and causes
    suspected_triggers: List[str] = field(default_factory=list)
    change_cascade_effects: List[str] = field(default_factory=list)
    adaptation_required: bool = False
    
    # Impact assessment
    impact_on_goals: str = ""  # positive, neutral, negative, blocking
    recommended_adaptations: List[str] = field(default_factory=list)
    urgency_level: str = ""  # immediate, soon, eventually, monitor
    
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ContextualRecommendation:
    """Recommendation based on contextual analysis"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    target_primitive: str = ""  # Which primitive this recommendation is for
    recommendation_type: str = ""  # adaptation, focus, timing, approach
    
    # Recommendation content
    title: str = ""
    description: str = ""
    specific_actions: List[str] = field(default_factory=list)
    
    # Contextual basis
    triggering_context: Dict[str, Any] = field(default_factory=dict)
    supporting_patterns: List[str] = field(default_factory=list)  # Pattern IDs
    confidence: float = 0.0
    
    # Implementation guidance
    priority: ContextPriority = ContextPriority.MEDIUM
    timing: str = ""  # immediate, next_interaction, when_appropriate
    duration: str = ""  # one_time, session, ongoing
    
    # Expected outcomes
    expected_benefits: List[str] = field(default_factory=list)
    success_metrics: List[str] = field(default_factory=list)
    potential_risks: List[str] = field(default_factory=list)
    
    # Tracking
    created_at: float = field(default_factory=time.time)
    applied: bool = False
    applied_at: Optional[float] = None
    effectiveness_score: Optional[float] = None
    
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ContextMetrics:
    """Metrics for context management performance"""
    # Context collection metrics
    total_factors_tracked: int = 0
    active_context_types: int = 0
    context_collection_rate: float = 0.0  # factors per minute
    context_quality_score: float = 0.0
    
    # Pattern recognition metrics
    patterns_identified: int = 0
    pattern_reliability_avg: float = 0.0
    predictive_accuracy: float = 0.0
    false_pattern_rate: float = 0.0
    
    # Change detection metrics
    context_changes_detected: int = 0
    change_detection_latency: float = 0.0  # seconds
    change_prediction_accuracy: float = 0.0
    adaptation_success_rate: float = 0.0
    
    # Recommendation metrics
    recommendations_generated: int = 0
    recommendations_accepted: int = 0
    recommendation_effectiveness: float = 0.0
    user_satisfaction_with_context: float = 0.0
    
    # Integration metrics
    primitive_integrations: int = 0
    cross_primitive_insights: int = 0
    context_utilization_rate: float = 0.0
    
    # Quality and reliability metrics
    context_completeness: float = 0.0  # How complete context picture is
    context_accuracy: float = 0.0  # How accurate context assessment is
    context_freshness: float = 0.0  # How up-to-date context is
    context_relevance: float = 0.0  # How relevant to current needs
    
    # Performance metrics
    context_processing_time: float = 0.0  # milliseconds
    memory_usage: float = 0.0  # MB
    cpu_usage: float = 0.0  # percentage
    
    # Calculation metadata
    calculated_at: float = field(default_factory=time.time)
    calculation_period: str = "session"  # session, daily, weekly, monthly
    
    metadata: Dict[str, Any] = field(default_factory=dict)


# ==================== HELPER FUNCTIONS ====================

def create_context_factor(
    context_type: ContextType,
    key: str,
    value: Any,
    subtype: str = "",
    priority: ContextPriority = ContextPriority.MEDIUM,
    **kwargs
) -> ContextFactor:
    """Helper function to create a ContextFactor with common defaults"""
    return ContextFactor(
        type=context_type,
        subtype=subtype,
        key=key,
        value=value,
        priority=priority,
        **kwargs
    )


def create_environmental_context(
    location_type: str = "",
    device_type: str = "",
    **kwargs
) -> EnvironmentalContext:
    """Helper function to create EnvironmentalContext"""
    return EnvironmentalContext(
        location_type=location_type,
        device_type=device_type,
        **kwargs
    )


def create_social_context(
    interaction_mode: str = "",
    relationship_type: str = "",
    **kwargs
) -> SocialContext:
    """Helper function to create SocialContext"""
    return SocialContext(
        interaction_mode=interaction_mode,
        relationship_type=relationship_type,
        **kwargs
    )


def create_temporal_context(
    current_time_context: str = "",
    time_pressure_level: str = "",
    **kwargs
) -> TemporalContext:
    """Helper function to create TemporalContext"""
    return TemporalContext(
        current_time_context=current_time_context,
        time_pressure_level=time_pressure_level,
        **kwargs
    )


def create_task_context(
    primary_task_type: str = "",
    task_complexity: str = "",
    **kwargs
) -> TaskContext:
    """Helper function to create TaskContext"""
    return TaskContext(
        primary_task_type=primary_task_type,
        task_complexity=task_complexity,
        **kwargs
    )


def create_emotional_context(
    primary_mood: str = "",
    stress_level: str = "",
    **kwargs
) -> EmotionalContext:
    """Helper function to create EmotionalContext"""
    return EmotionalContext(
        primary_mood=primary_mood,
        stress_level=stress_level,
        **kwargs
    )


def create_cognitive_context(
    attention_state: str = "",
    cognitive_load: str = "",
    **kwargs
) -> CognitiveContext:
    """Helper function to create CognitiveContext"""
    return CognitiveContext(
        attention_state=attention_state,
        cognitive_load=cognitive_load,
        **kwargs
    )


def create_context_snapshot(
    environmental: Optional[EnvironmentalContext] = None,
    social: Optional[SocialContext] = None,
    temporal: Optional[TemporalContext] = None,
    task: Optional[TaskContext] = None,
    emotional: Optional[EmotionalContext] = None,
    cognitive: Optional[CognitiveContext] = None,
    **kwargs
) -> ContextSnapshot:
    """Helper function to create a comprehensive ContextSnapshot"""
    return ContextSnapshot(
        environmental=environmental or EnvironmentalContext(),
        social=social or SocialContext(),
        temporal=temporal or TemporalContext(),
        task=task or TaskContext(),
        emotional=emotional or EmotionalContext(),
        cognitive=cognitive or CognitiveContext(),
        **kwargs
    )


def create_contextual_recommendation(
    target_primitive: str,
    title: str,
    description: str,
    recommendation_type: str = "adaptation",
    priority: ContextPriority = ContextPriority.MEDIUM,
    **kwargs
) -> ContextualRecommendation:
    """Helper function to create ContextualRecommendation"""
    return ContextualRecommendation(
        target_primitive=target_primitive,
        title=title,
        description=description,
        recommendation_type=recommendation_type,
        priority=priority,
        **kwargs
    )


def create_context_pattern(
    pattern_type: str,
    name: str,
    description: str,
    **kwargs
) -> ContextPattern:
    """Helper function to create ContextPattern"""
    return ContextPattern(
        pattern_type=pattern_type,
        name=name,
        description=description,
        **kwargs
    )


def create_context_change(
    change_type: str,
    previous_snapshot_id: str,
    current_snapshot_id: str,
    **kwargs
) -> ContextChange:
    """Helper function to create ContextChange"""
    return ContextChange(
        change_type=change_type,
        previous_snapshot_id=previous_snapshot_id,
        current_snapshot_id=current_snapshot_id,
        **kwargs
    )


# ==================== VALIDATION HELPERS ====================

def validate_context_factor(factor: ContextFactor) -> Tuple[bool, List[str]]:
    """Validate a ContextFactor for completeness and consistency"""
    errors = []
    
    if not factor.key.strip():
        errors.append("Context factor key is required")
    
    if factor.value is None:
        errors.append("Context factor value cannot be None")
    
    if factor.confidence < 0 or factor.confidence > 1:
        errors.append("Confidence must be between 0 and 1")
    
    if factor.influence_weight < 0 or factor.influence_weight > 1:
        errors.append("Influence weight must be between 0 and 1")
    
    if factor.reliability < 0 or factor.reliability > 1:
        errors.append("Reliability must be between 0 and 1")
    
    if factor.quality_score < 0 or factor.quality_score > 1:
        errors.append("Quality score must be between 0 and 1")
    
    if factor.staleness_tolerance < 0:
        errors.append("Staleness tolerance cannot be negative")
    
    return len(errors) == 0, errors


def validate_context_snapshot(snapshot: ContextSnapshot) -> Tuple[bool, List[str]]:
    """Validate a ContextSnapshot for completeness and consistency"""
    errors = []
    
    if snapshot.overall_context_quality < 0 or snapshot.overall_context_quality > 1:
        errors.append("Overall context quality must be between 0 and 1")
    
    if snapshot.context_confidence < 0 or snapshot.context_confidence > 1:
        errors.append("Context confidence must be between 0 and 1")
    
    if snapshot.context_stability < 0 or snapshot.context_stability > 1:
        errors.append("Context stability must be between 0 and 1")
    
    if snapshot.context_complexity < 0 or snapshot.context_complexity > 1:
        errors.append("Context complexity must be between 0 and 1")
    
    # Validate individual context factors
    for factor in snapshot.context_factors:
        factor_valid, factor_errors = validate_context_factor(factor)
        if not factor_valid:
            errors.extend([f"Factor {factor.key}: {error}" for error in factor_errors])
    
    return len(errors) == 0, errors


def validate_contextual_recommendation(rec: ContextualRecommendation) -> Tuple[bool, List[str]]:
    """Validate a ContextualRecommendation for completeness"""
    errors = []
    
    if not rec.target_primitive.strip():
        errors.append("Target primitive is required")
    
    if not rec.title.strip():
        errors.append("Recommendation title is required")
    
    if not rec.description.strip():
        errors.append("Recommendation description is required")
    
    if rec.confidence < 0 or rec.confidence > 1:
        errors.append("Confidence must be between 0 and 1")
    
    if rec.effectiveness_score is not None and (rec.effectiveness_score < 0 or rec.effectiveness_score > 1):
        errors.append("Effectiveness score must be between 0 and 1")
    
    return len(errors) == 0, errors


def validate_context_pattern(pattern: ContextPattern) -> Tuple[bool, List[str]]:
    """Validate a ContextPattern for consistency"""
    errors = []
    
    if not pattern.name.strip():
        errors.append("Pattern name is required")
    
    if not pattern.description.strip():
        errors.append("Pattern description is required")
    
    if pattern.reliability < 0 or pattern.reliability > 1:
        errors.append("Reliability must be between 0 and 1")
    
    if pattern.predictive_power < 0 or pattern.predictive_power > 1:
        errors.append("Predictive power must be between 0 and 1")
    
    if pattern.confidence_level < 0 or pattern.confidence_level > 1:
        errors.append("Confidence level must be between 0 and 1")
    
    if pattern.observation_count < 0:
        errors.append("Observation count cannot be negative")
    
    return len(errors) == 0, errors


# ==================== UTILITY FUNCTIONS ====================

def calculate_context_staleness(factor: ContextFactor, current_time: Optional[float] = None) -> float:
    """Calculate how stale a context factor is (0=fresh, 1=completely stale)"""
    current_time = current_time or time.time()
    age = current_time - factor.timestamp
    
    if factor.staleness_tolerance <= 0:
        return 0.0  # Never stale if no tolerance set
    
    staleness = min(age / factor.staleness_tolerance, 1.0)
    return staleness


def calculate_context_relevance(factor: ContextFactor, target_context: Dict[str, Any]) -> float:
    """Calculate how relevant a context factor is to a target context"""
    relevance_score = 0.0
    
    # Priority-based relevance
    priority_scores = {
        ContextPriority.CRITICAL: 1.0,
        ContextPriority.HIGH: 0.8,
        ContextPriority.MEDIUM: 0.5,
        ContextPriority.LOW: 0.2,
        ContextPriority.IGNORE: 0.0
    }
    relevance_score += priority_scores.get(factor.priority, 0.5) * 0.4
    
    # Scope-based relevance
    target_scope = target_context.get("scope", ContextScope.SESSION)
    if factor.scope == target_scope:
        relevance_score += 0.3
    elif abs(list(ContextScope).index(factor.scope) - list(ContextScope).index(target_scope)) <= 1:
        relevance_score += 0.15
    
    # Type-based relevance
    target_types = target_context.get("relevant_types", [])
    if factor.type in target_types:
        relevance_score += 0.3
    
    return min(relevance_score, 1.0)


def merge_context_snapshots(snapshots: List[ContextSnapshot], weights: Optional[List[float]] = None) -> ContextSnapshot:
    """Merge multiple context snapshots into a single comprehensive snapshot"""
    if not snapshots:
        return ContextSnapshot()
    
    if len(snapshots) == 1:
        return snapshots[0]
    
    weights = weights or [1.0] * len(snapshots)
    total_weight = sum(weights)
    
    # Normalize weights
    weights = [w / total_weight for w in weights]
    
    merged = ContextSnapshot()
    
    # Merge aggregate metrics using weighted averages
    merged.overall_context_quality = sum(s.overall_context_quality * w for s, w in zip(snapshots, weights))
    merged.context_confidence = sum(s.context_confidence * w for s, w in zip(snapshots, weights))
    merged.context_stability = sum(s.context_stability * w for s, w in zip(snapshots, weights))
    merged.context_complexity = sum(s.context_complexity * w for s, w in zip(snapshots, weights))
    
    # Collect all context factors
    all_factors = []
    for snapshot in snapshots:
        all_factors.extend(snapshot.context_factors)
    
    # Remove duplicates based on key, keeping highest confidence
    factor_map = {}
    for factor in all_factors:
        key = f"{factor.type.value}:{factor.key}"
        if key not in factor_map or factor.confidence > factor_map[key].confidence:
            factor_map[key] = factor
    
    merged.context_factors = list(factor_map.values())
    
    # Merge situational summary
    summaries = [s.situation_summary for s in snapshots if s.situation_summary]
    merged.situation_summary = "; ".join(summaries)
    
    # Collect all considerations and recommendations
    all_considerations = []
    all_recommendations = []
    for snapshot in snapshots:
        all_considerations.extend(snapshot.key_considerations)
        all_recommendations.extend(snapshot.adaptation_recommendations)
    
    merged.key_considerations = list(set(all_considerations))
    merged.adaptation_recommendations = list(set(all_recommendations))
    
    return merged


def detect_context_anomalies(current: ContextSnapshot, historical: List[ContextSnapshot]) -> List[Dict[str, Any]]:
    """Detect anomalies in current context compared to historical patterns"""
    anomalies = []
    
    if not historical:
        return anomalies
    
    # Calculate historical averages for key metrics
    historical_quality = [s.overall_context_quality for s in historical]
    historical_confidence = [s.context_confidence for s in historical]
    historical_stability = [s.context_stability for s in historical]
    
    avg_quality = sum(historical_quality) / len(historical_quality)
    avg_confidence = sum(historical_confidence) / len(historical_confidence)
    avg_stability = sum(historical_stability) / len(historical_stability)
    
    # Check for significant deviations
    quality_deviation = abs(current.overall_context_quality - avg_quality)
    confidence_deviation = abs(current.context_confidence - avg_confidence)
    stability_deviation = abs(current.context_stability - avg_stability)
    
    anomaly_threshold = 0.3  # 30% deviation threshold
    
    if quality_deviation > anomaly_threshold:
        anomalies.append({
            "type": "context_quality_anomaly",
            "current_value": current.overall_context_quality,
            "expected_value": avg_quality,
            "deviation": quality_deviation,
            "severity": "high" if quality_deviation > 0.5 else "medium"
        })
    
    if confidence_deviation > anomaly_threshold:
        anomalies.append({
            "type": "context_confidence_anomaly",
            "current_value": current.context_confidence,
            "expected_value": avg_confidence,
            "deviation": confidence_deviation,
            "severity": "high" if confidence_deviation > 0.5 else "medium"
        })
    
    if stability_deviation > anomaly_threshold:
        anomalies.append({
            "type": "context_stability_anomaly",
            "current_value": current.context_stability,
            "expected_value": avg_stability,
            "deviation": stability_deviation,
            "severity": "high" if stability_deviation > 0.5 else "medium"
        })
    
    return anomalies


def generate_context_insights(snapshot: ContextSnapshot) -> Dict[str, Any]:
    """Generate insights from a context snapshot"""
    insights = {
        "primary_context_drivers": [],
        "context_quality_assessment": "",
        "attention_recommendations": [],
        "collaboration_insights": [],
        "timing_insights": [],
        "mood_context_notes": []
    }
    
    # Identify primary context drivers
    high_priority_factors = [f for f in snapshot.context_factors if f.priority == ContextPriority.CRITICAL or f.priority == ContextPriority.HIGH]
    insights["primary_context_drivers"] = [f"{f.type.value}: {f.key}" for f in high_priority_factors[:5]]
    
    # Assess context quality
    if snapshot.overall_context_quality > 0.8:
        insights["context_quality_assessment"] = "Excellent context visibility with high confidence"
    elif snapshot.overall_context_quality > 0.6:
        insights["context_quality_assessment"] = "Good context understanding with moderate confidence"
    elif snapshot.overall_context_quality > 0.4:
        insights["context_quality_assessment"] = "Limited context visibility, some uncertainty"
    else:
        insights["context_quality_assessment"] = "Poor context understanding, high uncertainty"
    
    # Generate attention recommendations based on context
    if snapshot.cognitive.attention_state == "scattered":
        insights["attention_recommendations"].append("Consider focused work techniques to improve concentration")
    
    if snapshot.temporal.time_pressure_level == "urgent":
        insights["attention_recommendations"].append("Prioritize critical tasks given time pressure")
    
    if snapshot.cognitive.cognitive_load == "overloaded":
        insights["attention_recommendations"].append("Reduce cognitive load by simplifying current tasks")
    
    # Generate collaboration insights
    if snapshot.social.social_battery_level == "low":
        insights["collaboration_insights"].append("Consider asynchronous collaboration to preserve social energy")
    
    if snapshot.social.team_dynamics == "collaborative":
        insights["collaboration_insights"].append("Good opportunity for group brainstorming or team decision-making")
    
    # Generate timing insights
    if snapshot.temporal.energy_cycle_phase == "peak":
        insights["timing_insights"].append("Optimal time for challenging or creative work")
    
    if snapshot.temporal.next_commitment_minutes and snapshot.temporal.next_commitment_minutes < 30:
        insights["timing_insights"].append("Limited time available before next commitment")
    
    # Generate mood context notes
    if snapshot.emotional.stress_level in ["high", "overwhelming"]:
        insights["mood_context_notes"].append("High stress detected - consider stress reduction techniques")
    
    if snapshot.emotional.motivation_level == "very_high":
        insights["mood_context_notes"].append("High motivation - good opportunity for ambitious goals")
    
    return insights


# ==================== SCHEMA REGISTRY ====================

CONTEXT_SCHEMA_REGISTRY = {
    "ContextFactor": ContextFactor,
    "EnvironmentalContext": EnvironmentalContext,
    "SocialContext": SocialContext,
    "TemporalContext": TemporalContext,
    "TaskContext": TaskContext,
    "EmotionalContext": EmotionalContext,
    "CognitiveContext": CognitiveContext,
    "HistoricalContext": HistoricalContext,
    "ContextSnapshot": ContextSnapshot,
    "ContextPattern": ContextPattern,
    "ContextChange": ContextChange,
    "ContextualRecommendation": ContextualRecommendation,
    "ContextMetrics": ContextMetrics,
}

# Export all schemas for easy importing
__all__ = [
    # Enums
    "ContextType", "ContextScope", "ContextPriority", "ContextConfidence",
    "EnvironmentalType", "SocialContextType", "TemporalContextType", "EmotionalContextType",
    
    # Core Data Structures
    "ContextFactor", "EnvironmentalContext", "SocialContext", "TemporalContext",
    "TaskContext", "EmotionalContext", "CognitiveContext", "HistoricalContext",
    "ContextSnapshot", "ContextPattern", "ContextChange", "ContextualRecommendation",
    "ContextMetrics",
    
    # Helper Functions
    "create_context_factor", "create_environmental_context", "create_social_context",
    "create_temporal_context", "create_task_context", "create_emotional_context",
    "create_cognitive_context", "create_context_snapshot", "create_contextual_recommendation",
    "create_context_pattern", "create_context_change",
    
    # Validation Functions
    "validate_context_factor", "validate_context_snapshot", 
    "validate_contextual_recommendation", "validate_context_pattern",
    
    # Utility Functions
    "calculate_context_staleness", "calculate_context_relevance", 
    "merge_context_snapshots", "detect_context_anomalies", "generate_context_insights",
    
    # Registry
    "CONTEXT_SCHEMA_REGISTRY"
]

if __name__ == "__main__":
    print("🌍 Context Manager Schemas Loaded!")
    print(f"📊 {len(CONTEXT_SCHEMA_REGISTRY)} schema types available")
    print("🧠 Complete situational intelligence architecture ready!")
    
    # Example usage demonstration
    print("\n🎯 Example Usage:")
    
    # Create environmental context
    env_context = create_environmental_context(
        location_type="home_office",
        device_type="laptop",
        lighting_condition="natural",
        noise_level="quiet"
    )
    print(f"✅ Created EnvironmentalContext: {env_context.location_type}")
    
    # Create emotional context
    emotional_context = create_emotional_context(
        primary_mood="focused",
        stress_level="low",
        motivation_level="high"
    )
    print(f"✅ Created EmotionalContext: {emotional_context.primary_mood}")
    
    # Create temporal context
    temporal_context = create_temporal_context(
        current_time_context="morning",
        time_pressure_level="relaxed",
        energy_cycle_phase="peak"
    )
    print(f"✅ Created TemporalContext: {temporal_context.current_time_context}")
    
    # Create comprehensive context snapshot
    snapshot = create_context_snapshot(
        environmental=env_context,
        emotional=emotional_context,
        temporal=temporal_context
    )
    print(f"✅ Created ContextSnapshot: {snapshot.id}")
    
    # Generate insights
    insights = generate_context_insights(snapshot)
    print(f"✅ Generated insights: {len(insights)} categories")
    
    # Create contextual recommendation
    recommendation = create_contextual_recommendation(
        target_primitive="goal_manager",
        title="Optimal Goal Setting Context",
        description="Current context is ideal for ambitious goal setting",
        recommendation_type="timing"
    )
    print(f"✅ Created Recommendation: {recommendation.title}")
    
    print("\n🌟 Context Manager schemas are ready for implementation!")
    print("🚀 Situational intelligence awaits!")
