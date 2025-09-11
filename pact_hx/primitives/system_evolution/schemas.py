# pact_hx/primitives/system_evolution/schemas.py
"""
PACT System Evolution Manager Schemas

Defines all data structures, validation schemas, and type definitions
for the System Evolution Manager meta-primitive. These schemas ensure
type safety, data validation, and consistent interfaces across the
evolutionary intelligence system.

Schema Categories:
- Core Evolution Data Types
- Metric and Performance Schemas  
- Insight and Pattern Schemas
- Optimization and Action Schemas
- Collaboration Outcome Schemas
- System State and Health Schemas
- Configuration and Control Schemas
"""

from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any, Union, Set
from pydantic import BaseModel, Field, validator, root_validator
from uuid import UUID, uuid4
import numpy as np

# ============================================================================
# Core Enums and Constants
# ============================================================================

class EvolutionPhase(str, Enum):
    """System evolution phases"""
    OBSERVATION = "observation"
    ANALYSIS = "analysis" 
    LEARNING = "learning"
    OPTIMIZATION = "optimization"
    EVOLUTION = "evolution"
    VALIDATION = "validation"
    INTEGRATION = "integration"
    IDLE = "idle"
    ERROR = "error"

class MetricType(str, Enum):
    """Types of system metrics"""
    PERFORMANCE = "performance"
    COLLABORATION = "collaboration"
    ETHICAL = "ethical"
    EFFICIENCY = "efficiency"
    USER_SATISFACTION = "user_satisfaction"
    ALIGNMENT = "alignment"
    EMERGENT = "emergent"
    TRUST = "trust"
    CREATIVITY = "creativity"
    ACCURACY = "accuracy"
    RESPONSE_TIME = "response_time"
    RESOURCE_USAGE = "resource_usage"

class PrimitiveHealth(str, Enum):
    """Health status of system primitives"""
    OPTIMAL = "optimal"
    GOOD = "good"
    DEGRADED = "degraded"
    CRITICAL = "critical"
    FAILING = "failing"
    UNKNOWN = "unknown"

class InsightCategory(str, Enum):
    """Categories of evolution insights"""
    USER_SATISFACTION = "user_satisfaction"
    EFFICIENCY = "efficiency"
    PERFORMANCE_ANOMALY = "performance_anomaly"
    PRIMITIVE_USAGE = "primitive_usage"
    EMERGENT_BEHAVIOR = "emergent_behavior"
    ETHICAL_ALIGNMENT = "ethical_alignment"
    TRUST_CALIBRATION = "trust_calibration"
    COLLABORATION_PATTERN = "collaboration_pattern"
    RESOURCE_OPTIMIZATION = "resource_optimization"
    CAPABILITY_GAP = "capability_gap"

class OptimizationType(str, Enum):
    """Types of optimization actions"""
    PARAMETER_TUNING = "parameter_tuning"
    INTERACTION_ADJUSTMENT = "interaction_adjustment"
    RESOURCE_ALLOCATION = "resource_allocation"
    CAPABILITY_ENHANCEMENT = "capability_enhancement"
    ARCHITECTURAL_CHANGE = "architectural_change"
    WORKFLOW_OPTIMIZATION = "workflow_optimization"
    PRIMITIVE_INTEGRATION = "primitive_integration"

class PrimitiveType(str, Enum):
    """Types of PACT primitives"""
    COLLABORATIVE_INTELLIGENCE = "collaborative_intelligence"
    ADAPTIVE_REASONING = "adaptive_reasoning"
    EMPATHETIC_INTERACTION = "empathetic_interaction"
    CONTEXTUAL_MEMORY = "contextual_memory"
    VALUE_ALIGNMENT = "value_alignment"
    UNCERTAINTY_HANDLING = "uncertainty_handling"
    CREATIVE_SYNTHESIS = "creative_synthesis"
    META_LEARNING = "meta_learning"
    EXPLAINABLE_AI = "explainable_ai"
    CONTINUOUS_ADAPTATION = "continuous_adaptation"
    ETHICAL_REASONING = "ethical_reasoning"
    TRUST_CALIBRATION = "trust_calibration"
    SYSTEM_EVOLUTION = "system_evolution"
    TONE_ADAPTATION = "tone_adaptation"  # Adaptive tone and communication style
    GOAL_ALIGNMENT = "goal_alignment"    # Goal understanding and alignment

# ============================================================================
# Core Data Schemas
# ============================================================================

class BaseEvolutionModel(BaseModel):
    """Base model for all evolution schemas"""
    id: str = Field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            np.float64: float,
            np.float32: float,
            np.int64: int,
            np.int32: int,
        }

class SystemMetricSchema(BaseEvolutionModel):
    """Schema for individual system metrics"""
    name: str = Field(..., description="Metric name")
    value: float = Field(..., description="Metric value")
    metric_type: MetricType = Field(..., description="Type of metric")
    primitive_source: str = Field(..., description="Source primitive")
    context: Dict[str, Any] = Field(default_factory=dict, description="Additional context")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Confidence in metric")
    tags: List[str] = Field(default_factory=list, description="Metric tags")
    
    @validator('value')
    def validate_value(cls, v):
        if not isinstance(v, (int, float)) or np.isnan(v) or np.isinf(v):
            raise ValueError("Metric value must be a finite number")
        return float(v)

class ResourceUsageSchema(BaseModel):
    """Schema for resource usage metrics"""
    cpu_percent: float = Field(default=0.0, ge=0.0, le=100.0)
    memory_mb: float = Field(default=0.0, ge=0.0)
    disk_io_mb: float = Field(default=0.0, ge=0.0)
    network_io_mb: float = Field(default=0.0, ge=0.0)
    gpu_percent: float = Field(default=0.0, ge=0.0, le=100.0)
    custom_metrics: Dict[str, float] = Field(default_factory=dict)

class PrimitivePerformanceSchema(BaseEvolutionModel):
    """Schema for primitive performance metrics"""
    primitive_name: str = Field(..., description="Name of the primitive")
    primitive_type: PrimitiveType = Field(..., description="Type of primitive")
    health_status: PrimitiveHealth = Field(..., description="Current health status")
    response_time: float = Field(default=0.0, ge=0.0, description="Average response time (ms)")
    accuracy: float = Field(default=0.0, ge=0.0, le=1.0, description="Accuracy score")
    efficiency: float = Field(default=0.0, ge=0.0, le=1.0, description="Efficiency score")
    user_satisfaction: float = Field(default=0.0, ge=0.0, le=1.0, description="User satisfaction")
    ethical_alignment: float = Field(default=1.0, ge=0.0, le=1.0, description="Ethical alignment")
    resource_usage: ResourceUsageSchema = Field(default_factory=ResourceUsageSchema)
    error_rate: float = Field(default=0.0, ge=0.0, le=1.0, description="Error rate")
    throughput: float = Field(default=0.0, ge=0.0, description="Requests per second")
    availability: float = Field(default=1.0, ge=0.0, le=1.0, description="Availability percentage")
    last_updated: datetime = Field(default_factory=datetime.now)

# ============================================================================
# Collaboration and Outcome Schemas
# ============================================================================

class UserFeedbackSchema(BaseModel):
    """Schema for user feedback"""
    overall_rating: int = Field(..., ge=1, le=5, description="Overall rating (1-5)")
    helpfulness: int = Field(default=3, ge=1, le=5, description="Helpfulness rating")
    clarity: int = Field(default=3, ge=1, le=5, description="Clarity rating")
    relevance: int = Field(default=3, ge=1, le=5, description="Relevance rating")
    speed: int = Field(default=3, ge=1, le=5, description="Response speed rating")
    empathy: int = Field(default=3, ge=1, le=5, description="Empathy rating")
    creativity: int = Field(default=3, ge=1, le=5, description="Creativity rating")
    text_feedback: Optional[str] = Field(None, description="Free-form text feedback")
    suggested_improvements: List[str] = Field(default_factory=list)
    pain_points: List[str] = Field(default_factory=list)

class TaskOutcomeSchema(BaseModel):
    """Schema for task completion outcomes"""
    task_type: str = Field(..., description="Type of task")
    completion_status: str = Field(..., description="Completion status")
    completion_percentage: float = Field(..., ge=0.0, le=100.0)
    quality_score: float = Field(default=0.0, ge=0.0, le=1.0)
    time_to_completion: float = Field(default=0.0, ge=0.0, description="Time in seconds")
    iterations_required: int = Field(default=1, ge=1, description="Number of iterations")
    user_effort_level: float = Field(default=0.5, ge=0.0, le=1.0, description="User effort required")

class CollaborationOutcomeSchema(BaseEvolutionModel):
    """Schema for human-AI collaboration outcomes"""
    session_id: str = Field(..., description="Unique session identifier")
    user_id: Optional[str] = Field(None, description="Anonymous user identifier")
    primitives_used: List[str] = Field(..., description="List of primitives used")
    primitive_interactions: Dict[str, int] = Field(default_factory=dict, description="Interaction counts")
    
    # Core outcome metrics
    user_satisfaction: float = Field(..., ge=0.0, le=1.0, description="Overall user satisfaction")
    task_completion: float = Field(..., ge=0.0, le=1.0, description="Task completion score")
    ethical_alignment: float = Field(..., ge=0.0, le=1.0, description="Ethical alignment score")
    efficiency_score: float = Field(..., ge=0.0, le=1.0, description="Collaboration efficiency")
    creativity_score: float = Field(..., ge=0.0, le=1.0, description="Creative output quality")
    trust_level: float = Field(..., ge=0.0, le=1.0, description="User trust level")
    
    # Detailed feedback and outcomes
    user_feedback: UserFeedbackSchema = Field(..., description="User feedback")
    task_outcome: TaskOutcomeSchema = Field(..., description="Task completion details")
    
    # Session metadata
    duration: float = Field(..., ge=0.0, description="Session duration in seconds")
    message_count: int = Field(default=0, ge=0, description="Number of messages exchanged")
    context_switches: int = Field(default=0, ge=0, description="Number of context switches")
    
    # Additional metrics
    learning_occurred: bool = Field(default=False, description="Whether learning occurred")
    novelty_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Novelty of interaction")
    complexity_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Task complexity")

# ============================================================================
# Insight and Pattern Schemas
# ============================================================================

class EvolutionInsightSchema(BaseEvolutionModel):
    """Schema for evolution insights discovered by the system"""
    insight_id: str = Field(default_factory=lambda: f"insight_{uuid4()}")
    category: InsightCategory = Field(..., description="Insight category")
    title: str = Field(..., description="Brief insight title")
    description: str = Field(..., description="Detailed insight description")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in insight")
    impact_score: float = Field(..., ge=0.0, le=1.0, description="Expected impact score")
    urgency: float = Field(default=0.5, ge=0.0, le=1.0, description="Urgency of addressing")
    
    # Affected components
    affected_primitives: List[str] = Field(..., description="Affected primitive names")
    affected_metrics: List[str] = Field(default_factory=list, description="Affected metrics")
    
    # Recommendations
    recommended_actions: List[str] = Field(..., description="Recommended actions")
    success_criteria: List[str] = Field(default_factory=list, description="Success criteria")
    risk_factors: List[str] = Field(default_factory=list, description="Risk factors")
    
    # Validation and lifecycle
    discovered_at: datetime = Field(default_factory=datetime.now)
    validated: bool = Field(default=False, description="Whether insight is validated")
    validation_confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    acted_upon: bool = Field(default=False, description="Whether action was taken")
    outcome_tracked: bool = Field(default=False, description="Whether outcome is tracked")
    
    # Supporting data
    supporting_data: Dict[str, Any] = Field(default_factory=dict)
    correlations: List[str] = Field(default_factory=list, description="Related insights")
    
    @validator('recommended_actions')
    def validate_actions(cls, v):
        if not v:
            raise ValueError("At least one recommended action is required")
        return v

class PatternSchema(BaseEvolutionModel):
    """Schema for detected patterns in system behavior"""
    pattern_id: str = Field(default_factory=lambda: f"pattern_{uuid4()}")
    pattern_type: str = Field(..., description="Type of pattern")
    pattern_name: str = Field(..., description="Human-readable pattern name")
    description: str = Field(..., description="Pattern description")
    
    # Pattern characteristics
    frequency: float = Field(..., ge=0.0, description="Pattern frequency")
    strength: float = Field(..., ge=0.0, le=1.0, description="Pattern strength")
    stability: float = Field(..., ge=0.0, le=1.0, description="Pattern stability")
    predictive_power: float = Field(default=0.0, ge=0.0, le=1.0)
    
    # Pattern context
    context_conditions: Dict[str, Any] = Field(default_factory=dict)
    temporal_characteristics: Dict[str, Any] = Field(default_factory=dict)
    affected_primitives: List[str] = Field(default_factory=list)
    
    # Pattern data
    sample_data: List[Dict[str, Any]] = Field(default_factory=list)
    statistical_measures: Dict[str, float] = Field(default_factory=dict)
    
    discovered_at: datetime = Field(default_factory=datetime.now)
    last_observed: datetime = Field(default_factory=datetime.now)
    observation_count: int = Field(default=1, ge=1)

# ============================================================================
# Optimization and Action Schemas
# ============================================================================

class OptimizationParameterSchema(BaseModel):
    """Schema for optimization parameters"""
    name: str = Field(..., description="Parameter name")
    current_value: Any = Field(..., description="Current parameter value")
    suggested_value: Any = Field(..., description="Suggested new value")
    value_type: str = Field(..., description="Parameter value type")
    min_value: Optional[float] = Field(None, description="Minimum allowed value")
    max_value: Optional[float] = Field(None, description="Maximum allowed value")
    impact_estimate: float = Field(default=0.0, ge=0.0, le=1.0, description="Expected impact")

class OptimizationActionSchema(BaseEvolutionModel):
    """Schema for optimization actions"""
    action_id: str = Field(default_factory=lambda: f"action_{uuid4()}")
    target_primitive: str = Field(..., description="Target primitive name")
    action_type: OptimizationType = Field(..., description="Type of optimization")
    title: str = Field(..., description="Action title")
    description: str = Field(..., description="Detailed action description")
    
    # Action parameters
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Action parameters")
    parameter_details: List[OptimizationParameterSchema] = Field(default_factory=list)
    
    # Impact assessment
    expected_impact: float = Field(..., ge=0.0, le=1.0, description="Expected positive impact")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in action")
    priority: int = Field(..., ge=1, le=5, description="Action priority (1=highest)")
    urgency: float = Field(default=0.5, ge=0.0, le=1.0, description="Action urgency")
    
    # Resource requirements
    estimated_effort: float = Field(..., ge=0.0, description="Estimated effort (hours)")
    resource_requirements: Dict[str, float] = Field(default_factory=dict)
    risk_level: float = Field(default=0.5, ge=0.0, le=1.0, description="Risk level")
    
    # Dependencies and constraints
    dependencies: List[str] = Field(default_factory=list, description="Dependency action IDs")
    prerequisites: List[str] = Field(default_factory=list, description="Prerequisites")
    constraints: List[str] = Field(default_factory=list, description="Constraints")
    
    # Execution tracking
    status: str = Field(default="planned", description="Action status")
    scheduled_time: Optional[datetime] = Field(None, description="Scheduled execution time")
    execution_window: Optional[timedelta] = Field(None, description="Execution time window")
    
    # Success criteria
    success_metrics: List[str] = Field(default_factory=list)
    rollback_plan: Dict[str, Any] = Field(default_factory=dict)

class OptimizationResultSchema(BaseEvolutionModel):
    """Schema for optimization execution results"""
    action_id: str = Field(..., description="Associated action ID")
    execution_start: datetime = Field(..., description="Execution start time")
    execution_end: datetime = Field(..., description="Execution end time")
    success: bool = Field(..., description="Whether execution succeeded")
    
    # Result details
    changes_made: Dict[str, Any] = Field(default_factory=dict)
    metrics_before: Dict[str, float] = Field(default_factory=dict)
    metrics_after: Dict[str, float] = Field(default_factory=dict)
    improvement_achieved: Dict[str, float] = Field(default_factory=dict)
    
    # Execution metadata
    actual_effort: float = Field(default=0.0, ge=0.0, description="Actual effort used")
    resources_used: Dict[str, float] = Field(default_factory=dict)
    side_effects: List[str] = Field(default_factory=list)
    
    # Error handling
    error_message: Optional[str] = Field(None, description="Error message if failed")
    rollback_executed: bool = Field(default=False, description="Whether rollback was executed")
    rollback_success: bool = Field(default=True, description="Whether rollback succeeded")

# ============================================================================
# System State and Configuration Schemas
# ============================================================================

class SystemHealthSchema(BaseEvolutionModel):
    """Schema for overall system health"""
    overall_health: PrimitiveHealth = Field(..., description="Overall system health")
    health_score: float = Field(..., ge=0.0, le=1.0, description="Numeric health score")
    
    # Component health
    primitive_health: Dict[str, PrimitiveHealth] = Field(default_factory=dict)
    critical_issues: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    
    # Performance indicators
    avg_response_time: float = Field(default=0.0, ge=0.0)
    avg_user_satisfaction: float = Field(default=0.0, ge=0.0, le=1.0)
    avg_efficiency: float = Field(default=0.0, ge=0.0, le=1.0)
    avg_ethical_alignment: float = Field(default=1.0, ge=0.0, le=1.0)
    
    # System metrics
    total_sessions: int = Field(default=0, ge=0)
    total_primitives: int = Field(default=0, ge=0)
    uptime: timedelta = Field(default=timedelta(0))
    last_evolution: Optional[datetime] = Field(None)

class EvolutionConfigSchema(BaseModel):
    """Schema for evolution manager configuration"""
    # Evolution control
    auto_evolution_enabled: bool = Field(default=True)
    evolution_interval_hours: float = Field(default=1.0, gt=0.0)
    min_data_threshold: int = Field(default=50, ge=1)
    
    # Analysis thresholds
    insight_confidence_threshold: float = Field(default=0.5, ge=0.0, le=1.0)
    pattern_strength_threshold: float = Field(default=0.7, ge=0.0, le=1.0)
    anomaly_detection_threshold: float = Field(default=2.0, gt=0.0)
    
    # Optimization settings
    optimization_batch_size: int = Field(default=5, ge=1)
    max_concurrent_optimizations: int = Field(default=3, ge=1)
    optimization_cooldown_hours: float = Field(default=0.5, ge=0.0)
    
    # Monitoring settings
    performance_monitoring_interval: int = Field(default=300, ge=60)  # seconds
    health_check_interval: int = Field(default=180, ge=30)  # seconds
    metric_retention_hours: int = Field(default=168, ge=24)  # 1 week default
    
    # Safety settings
    max_parameter_change_percent: float = Field(default=20.0, gt=0.0, le=100.0)
    require_validation_for_critical: bool = Field(default=True)
    enable_rollback: bool = Field(default=True)
    
    # Logging and debugging
    log_level: str = Field(default="INFO")
    detailed_metrics: bool = Field(default=False)
    debug_insights: bool = Field(default=False)

class SystemStateSchema(BaseEvolutionModel):
    """Schema for complete system state"""
    evolution_phase: EvolutionPhase = Field(..., description="Current evolution phase")
    evolution_cycle_count: int = Field(default=0, ge=0)
    last_evolution_time: datetime = Field(default_factory=datetime.now)
    
    # System health and performance
    system_health: SystemHealthSchema = Field(..., description="Overall system health")
    primitive_performances: Dict[str, PrimitivePerformanceSchema] = Field(default_factory=dict)
    
    # Evolution data
    active_insights: List[EvolutionInsightSchema] = Field(default_factory=list)
    pending_optimizations: List[OptimizationActionSchema] = Field(default_factory=list)
    recent_patterns: List[PatternSchema] = Field(default_factory=list)
    
    # Configuration
    config: EvolutionConfigSchema = Field(default_factory=EvolutionConfigSchema)
    
    # Statistics
    total_insights_generated: int = Field(default=0, ge=0)
    total_optimizations_executed: int = Field(default=0, ge=0)
    total_collaboration_sessions: int = Field(default=0, ge=0)
    
    # Error tracking
    recent_errors: List[str] = Field(default_factory=list)
    error_count: int = Field(default=0, ge=0)

# ============================================================================
# Request/Response Schemas for API
# ============================================================================

class EvolutionStatusRequest(BaseModel):
    """Request schema for evolution status"""
    include_primitive_details: bool = Field(default=True)
    include_recent_insights: bool = Field(default=True)
    insights_limit: int = Field(default=10, ge=1, le=100)

class TriggerEvolutionRequest(BaseModel):
    """Request schema for triggering evolution"""
    force_execution: bool = Field(default=False)
    target_primitives: Optional[List[str]] = Field(None)
    skip_validation: bool = Field(default=False)

class InsightQueryRequest(BaseModel):
    """Request schema for querying insights"""
    category: Optional[InsightCategory] = Field(None)
    primitive_name: Optional[str] = Field(None)
    min_confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    min_impact: float = Field(default=0.0, ge=0.0, le=1.0)
    limit: int = Field(default=50, ge=1, le=500)
    include_unvalidated: bool = Field(default=False)

class PerformanceQueryRequest(BaseModel):
    """Request schema for performance queries"""
    primitive_name: Optional[str] = Field(None)
    metric_type: Optional[MetricType] = Field(None)
    time_window_hours: float = Field(default=24.0, gt=0.0)
    include_detailed_metrics: bool = Field(default=False)

class ConfigUpdateRequest(BaseModel):
    """Request schema for configuration updates"""
    config_updates: Dict[str, Any] = Field(..., description="Configuration updates")
    validate_only: bool = Field(default=False)
    apply_immediately: bool = Field(default=True)

# ============================================================================
# Validation Helpers and Custom Validators
# ============================================================================

def validate_primitive_name(name: str) -> bool:
    """Validate primitive name format"""
    valid_names = [pt.value for pt in PrimitiveType]
    return name in valid_names

def validate_metric_value_range(value: float, metric_type: MetricType) -> bool:
    """Validate metric value is in expected range for type"""
    if metric_type in [MetricType.USER_SATISFACTION, MetricType.EFFICIENCY, 
                      MetricType.ALIGNMENT, MetricType.TRUST, MetricType.ACCURACY]:
        return 0.0 <= value <= 1.0
    elif metric_type == MetricType.RESPONSE_TIME:
        return value >= 0.0
    else:
        return True  # Other metrics can have any valid float value

def validate_insight_consistency(insight: EvolutionInsightSchema) -> List[str]:
    """Validate insight internal consistency"""
    errors = []
    
    # Check if confidence and impact scores are consistent
    if insight.confidence > 0.9 and insight.impact_score < 0.1:
        errors.append("High confidence insight should have higher impact score")
    
    # Check if recommended actions match category
    category_action_map = {
        InsightCategory.USER_SATISFACTION: ["empathy", "interaction", "personalization"],
        InsightCategory.EFFICIENCY: ["optimization", "streamline", "resource"],
        InsightCategory.PERFORMANCE_ANOMALY: ["investigate", "monitor", "adjust"],
    }
    
    if insight.category in category_action_map:
        expected_keywords = category_action_map[insight.category]
        action_text = " ".join(insight.recommended_actions).lower()
        if not any(keyword in action_text for keyword in expected_keywords):
            errors.append(f"Recommended actions don't align with category {insight.category}")
    
    return errors

# ============================================================================
# Schema Factory Functions
# ============================================================================

def create_metric_schema(name: str, value: float, metric_type: MetricType, 
                        primitive_source: str, **kwargs) -> SystemMetricSchema:
    """Factory function to create metric schema with validation"""
    return SystemMetricSchema(
        name=name,
        value=value,
        metric_type=metric_type,
        primitive_source=primitive_source,
        **kwargs
    )

def create_collaboration_outcome_schema(session_id: str, primitives_used: List[str],
                                      user_satisfaction: float, **kwargs) -> CollaborationOutcomeSchema:
    """Factory function to create collaboration outcome schema"""
    # Create default feedback if not provided
    if 'user_feedback' not in kwargs:
        kwargs['user_feedback'] = UserFeedbackSchema(
            overall_rating=max(1, min(5, int(user_satisfaction * 5))),
            helpfulness=3,
            clarity=3,
            relevance=3,
            speed=3,
            empathy=3,
            creativity=3
        )
    
    # Create default task outcome if not provided
    if 'task_outcome' not in kwargs:
        kwargs['task_outcome'] = TaskOutcomeSchema(
            task_type="general",
            completion_status="completed",
            completion_percentage=user_satisfaction * 100,
            quality_score=user_satisfaction
        )
    
    return CollaborationOutcomeSchema(
        session_id=session_id,
        primitives_used=primitives_used,
        user_satisfaction=user_satisfaction,
        **kwargs
    )

def create_insight_schema(category: InsightCategory, description: str, 
                         confidence: float, impact_score: float,
                         affected_primitives: List[str], 
                         recommended_actions: List[str], **kwargs) -> EvolutionInsightSchema:
    """Factory function to create insight schema with validation"""
    insight = EvolutionInsightSchema(
        category=category,
        title=f"{category.value.replace('_', ' ').title()} Insight",
        description=description,
        confidence=confidence,
        impact_score=impact_score,
        affected_primitives=affected_primitives,
        recommended_actions=recommended_actions,
        **kwargs
    )
    
    # Validate consistency
    errors = validate_insight_consistency(insight)
    if errors:
        raise ValueError(f"Insight validation failed: {errors}")
    
    return insight

# ============================================================================
# Export All Schemas
# ============================================================================

__all__ = [
    # Enums
    "EvolutionPhase", "MetricType", "PrimitiveHealth", "InsightCategory", 
    "OptimizationType", "PrimitiveType",
    
    # Core Schemas
    "BaseEvolutionModel", "SystemMetricSchema", "ResourceUsageSchema",
    "PrimitivePerformanceSchema",
    
    # Collaboration Schemas
    "UserFeedbackSchema", "TaskOutcomeSchema", "CollaborationOutcomeSchema",
    
    # Insight and Pattern Schemas
    "EvolutionInsightSchema", "PatternSchema",
    
    # Optimization Schemas
    "OptimizationParameterSchema", "OptimizationActionSchema", "OptimizationResultSchema",
    
    # System State Schemas
    "SystemHealthSchema", "EvolutionConfigSchema", "SystemStateSchema",
    
    # Request/Response Schemas
    "EvolutionStatusRequest", "TriggerEvolutionRequest", "InsightQueryRequest",
    "PerformanceQueryRequest", "ConfigUpdateRequest",
    
    # Factory Functions
    "create_metric_schema", "create_collaboration_outcome_schema", "create_insight_schema",
    
    # Validation Functions
    "validate_primitive_name", "validate_metric_value_range", "validate_insight_consistency"
]

# ============================================================================
# Example Schema Usage and Testing
# ============================================================================

def create_sample_schemas():
    """Create sample schemas for testing and documentation"""
    
    # Sample metric
    sample_metric = create_metric_schema(
        name="response_time",
        value=125.5,
        metric_type=MetricType.RESPONSE_TIME,
        primitive_source="adaptive_reasoning",
        context={"request_type": "complex_analysis", "user_context": "expert"},
        confidence=0.95,
        tags=["performance", "latency"]
    )
    
    # Sample collaboration outcome
    sample_outcome = create_collaboration_outcome_schema(
        session_id="session_12345",
        primitives_used=["empathetic_interaction", "adaptive_reasoning", "creative_synthesis"],
        user_satisfaction=0.85,
        task_completion=0.92,
        ethical_alignment=0.98,
        efficiency_score=0.78,
        creativity_score=0.88,
        trust_level=0.82,
        duration=320.5,
        message_count=15,
        context_switches=3,
        learning_occurred=True,
        novelty_score=0.65,
        complexity_score=0.72
    )
    
    # Sample insight
    sample_insight = create_insight_schema(
        category=InsightCategory.USER_SATISFACTION,
        description="User satisfaction has been declining over recent collaborations, particularly in complex reasoning tasks",
        confidence=0.82,
        impact_score=0.75,
        affected_primitives=["adaptive_reasoning", "empathetic_interaction"],
        recommended_actions=[
            "Review empathetic interaction patterns for complex tasks",
            "Analyze user feedback for reasoning clarity issues",
            "Adjust response personalization for expert users"
        ],
        urgency=0.7,
        supporting_data={
            "trend_analysis": {"slope": -0.12, "r_squared": 0.76},
            "affected_sessions": 23,
            "time_period": "last_7_days"
        },
        success_criteria=[
            "User satisfaction increases by 15% within 2 weeks",
            "Positive feedback on reasoning clarity improves",
            "Complex task completion rates stabilize above 85%"
        ],
        risk_factors=[
            "Over-adjustment may reduce efficiency",
            "Changes may affect other user segments"
        ]
    )
    
    # Sample optimization action
    sample_action = OptimizationActionSchema(
        target_primitive="empathetic_interaction",
        action_type=OptimizationType.PARAMETER_TUNING,
        title="Enhance Empathy for Complex Tasks",
        description="Adjust empathetic interaction parameters to better support users during complex reasoning tasks",
        parameters={
            "emotional_sensitivity": 1.2,
            "response_warmth": 1.15,
            "complexity_awareness": 1.3,
            "expert_mode_empathy": True
        },
        parameter_details=[
            OptimizationParameterSchema(
                name="emotional_sensitivity",
                current_value=1.0,
                suggested_value=1.2,
                value_type="float",
                min_value=0.5,
                max_value=2.0,
                impact_estimate=0.3
            ),
            OptimizationParameterSchema(
                name="response_warmth",
                current_value=1.0,
                suggested_value=1.15,
                value_type="float",
                min_value=0.5,
                max_value=2.0,
                impact_estimate=0.25
            )
        ],
        expected_impact=0.35,
        confidence=0.78,
        priority=2,
        urgency=0.7,
        estimated_effort=2.5,
        resource_requirements={"cpu_hours": 0.5, "memory_gb": 1.0},
        risk_level=0.3,
        success_metrics=[
            "user_satisfaction_improvement",
            "complex_task_completion_rate",
            "empathy_rating_increase"
        ],
        rollback_plan={
            "restore_parameters": {
                "emotional_sensitivity": 1.0,
                "response_warmth": 1.0,
                "complexity_awareness": 1.0,
                "expert_mode_empathy": False
            },
            "validation_metrics": ["user_satisfaction", "response_time"]
        }
    )
    
    # Sample primitive performance
    sample_performance = PrimitivePerformanceSchema(
        primitive_name="adaptive_reasoning",
        primitive_type=PrimitiveType.ADAPTIVE_REASONING,
        health_status=PrimitiveHealth.GOOD,
        response_time=145.2,
        accuracy=0.87,
        efficiency=0.82,
        user_satisfaction=0.79,
        ethical_alignment=0.96,
        resource_usage=ResourceUsageSchema(
            cpu_percent=25.5,
            memory_mb=512.0,
            disk_io_mb=12.3,
            network_io_mb=45.7,
            gpu_percent=15.2,
            custom_metrics={"reasoning_depth": 3.2, "branch_factor": 4.1}
        ),
        error_rate=0.03,
        throughput=2.4,
        availability=0.998
    )
    
    # Sample system health
    sample_health = SystemHealthSchema(
        overall_health=PrimitiveHealth.GOOD,
        health_score=0.83,
        primitive_health={
            "adaptive_reasoning": PrimitiveHealth.GOOD,
            "empathetic_interaction": PrimitiveHealth.OPTIMAL,
            "creative_synthesis": PrimitiveHealth.DEGRADED,
            "value_alignment": PrimitiveHealth.OPTIMAL
        },
        critical_issues=[],
        warnings=[
            "Creative synthesis showing elevated response times",
            "Memory usage trending upward for reasoning primitive"
        ],
        avg_response_time=132.5,
        avg_user_satisfaction=0.81,
        avg_efficiency=0.85,
        avg_ethical_alignment=0.97,
        total_sessions=1247,
        total_primitives=12,
        uptime=timedelta(days=15, hours=8, minutes=23),
        last_evolution=datetime.now() - timedelta(hours=2, minutes=15)
    )
    
    # Sample evolution configuration
    sample_config = EvolutionConfigSchema(
        auto_evolution_enabled=True,
        evolution_interval_hours=1.5,
        min_data_threshold=75,
        insight_confidence_threshold=0.6,
        pattern_strength_threshold=0.75,
        anomaly_detection_threshold=2.5,
        optimization_batch_size=3,
        max_concurrent_optimizations=2,
        optimization_cooldown_hours=0.75,
        performance_monitoring_interval=240,
        health_check_interval=120,
        metric_retention_hours=336,  # 2 weeks
        max_parameter_change_percent=15.0,
        require_validation_for_critical=True,
        enable_rollback=True,
        log_level="DEBUG",
        detailed_metrics=True,
        debug_insights=True
    )
    
    return {
        "metric": sample_metric,
        "collaboration_outcome": sample_outcome,
        "insight": sample_insight,
        "optimization_action": sample_action,
        "primitive_performance": sample_performance,
        "system_health": sample_health,
        "configuration": sample_config
    }

# ============================================================================
# Schema Validation and Testing Utilities
# ============================================================================

def validate_schema_consistency():
    """Validate that all schemas are consistent and work together"""
    try:
        samples = create_sample_schemas()
        
        # Test serialization/deserialization
        for name, schema in samples.items():
            json_str = schema.json()
            reconstructed = type(schema).parse_raw(json_str)
            assert reconstructed == schema, f"Serialization failed for {name}"
        
        # Test factory functions
        metric = create_metric_schema("test", 0.5, MetricType.EFFICIENCY, "test_primitive")
        assert metric.name == "test"
        assert metric.value == 0.5
        
        # Test validation functions
        assert validate_primitive_name("adaptive_reasoning") == True
        assert validate_primitive_name("invalid_primitive") == False
        
        assert validate_metric_value_range(0.5, MetricType.USER_SATISFACTION) == True
        assert validate_metric_value_range(1.5, MetricType.USER_SATISFACTION) == False
        
        print("✅ All schema validations passed!")
        return True
        
    except Exception as e:
        print(f"❌ Schema validation failed: {e}")
        return False

def get_schema_documentation():
    """Generate documentation for all schemas"""
    doc = {
        "System Evolution Manager Schemas": {
            "description": "Complete type system for PACT System Evolution Manager",
            "categories": {
                "Core Data Types": [
                    "SystemMetricSchema - Individual system metrics",
                    "PrimitivePerformanceSchema - Primitive health and performance",
                    "CollaborationOutcomeSchema - Human-AI collaboration results"
                ],
                "Intelligence & Learning": [
                    "EvolutionInsightSchema - Discovered patterns and insights",
                    "PatternSchema - Behavioral patterns in system data",
                    "OptimizationActionSchema - System improvement actions"
                ],
                "System Management": [
                    "SystemHealthSchema - Overall system health status", 
                    "EvolutionConfigSchema - Manager configuration",
                    "SystemStateSchema - Complete system state snapshot"
                ],
                "API & Requests": [
                    "EvolutionStatusRequest - Status query parameters",
                    "TriggerEvolutionRequest - Evolution trigger parameters",
                    "InsightQueryRequest - Insight search parameters"
                ]
            },
            "key_features": [
                "Comprehensive type safety with Pydantic validation",
                "Hierarchical schema inheritance from BaseEvolutionModel", 
                "Built-in JSON serialization with custom encoders",
                "Factory functions for common schema creation patterns",
                "Cross-validation between related schemas",
                "Extensible enums for categorization and typing"
            ],
            "usage_patterns": [
                "Use factory functions for consistent object creation",
                "Leverage validation functions before processing",
                "Extend BaseEvolutionModel for new schema types",
                "Utilize enum types for type-safe categorization"
            ]
        }
    }
    
    return doc

# ============================================================================
# Advanced Schema Utilities
# ============================================================================

class SchemaEvolutionTracker:
    """Tracks schema version changes for backward compatibility"""
    
    def __init__(self):
        self.schema_versions = {
            "SystemMetricSchema": "1.0.0",
            "CollaborationOutcomeSchema": "1.0.0", 
            "EvolutionInsightSchema": "1.0.0",
            "OptimizationActionSchema": "1.0.0",
            "SystemHealthSchema": "1.0.0"
        }
        self.compatibility_matrix = {}
    
    def register_schema_change(self, schema_name: str, version: str, 
                             breaking_changes: List[str] = None):
        """Register a schema version change"""
        self.schema_versions[schema_name] = version
        if breaking_changes:
            self.compatibility_matrix[f"{schema_name}_{version}"] = breaking_changes
    
    def check_compatibility(self, schema_name: str, target_version: str) -> bool:
        """Check if schema version is compatible"""
        current_version = self.schema_versions.get(schema_name)
        if not current_version:
            return False
        
        # Simple version comparison (in production, use proper semver)
        return current_version >= target_version

class SchemaTransformer:
    """Transforms data between different schema versions"""
    
    def __init__(self):
        self.transformers = {}
    
    def register_transformer(self, from_schema: str, to_schema: str, 
                           transform_func: callable):
        """Register a transformation function between schema versions"""
        key = f"{from_schema}_to_{to_schema}"
        self.transformers[key] = transform_func
    
    def transform(self, data: dict, from_schema: str, to_schema: str) -> dict:
        """Transform data from one schema version to another"""
        key = f"{from_schema}_to_{to_schema}"
        transformer = self.transformers.get(key)
        
        if not transformer:
            raise ValueError(f"No transformer found for {key}")
        
        return transformer(data)

# ============================================================================
# Schema Registry and Metadata
# ============================================================================

SCHEMA_REGISTRY = {
    "metrics": {
        "primary": SystemMetricSchema,
        "related": [ResourceUsageSchema],
        "description": "System performance and behavior metrics"
    },
    "collaboration": {
        "primary": CollaborationOutcomeSchema,
        "related": [UserFeedbackSchema, TaskOutcomeSchema],
        "description": "Human-AI collaboration outcomes and feedback"
    },
    "insights": {
        "primary": EvolutionInsightSchema,
        "related": [PatternSchema],
        "description": "Discovered insights and behavioral patterns"
    },
    "optimization": {
        "primary": OptimizationActionSchema,
        "related": [OptimizationParameterSchema, OptimizationResultSchema],
        "description": "System optimization actions and results"
    },
    "system_state": {
        "primary": SystemStateSchema,
        "related": [SystemHealthSchema, PrimitivePerformanceSchema],
        "description": "Complete system state and health information"
    },
    "configuration": {
        "primary": EvolutionConfigSchema,
        "related": [],
        "description": "Evolution manager configuration parameters"
    }
}

def get_schema_by_category(category: str):
    """Get schema information by category"""
    return SCHEMA_REGISTRY.get(category, {})

def get_all_schema_categories():
    """Get all available schema categories"""
    return list(SCHEMA_REGISTRY.keys())

def validate_schema_relationships():
    """Validate that schema relationships are properly defined"""
    errors = []
    
    for category, info in SCHEMA_REGISTRY.items():
        primary_schema = info.get("primary")
        if not primary_schema:
            errors.append(f"Category {category} missing primary schema")
            continue
        
        # Check if primary schema inherits from BaseEvolutionModel
        if not issubclass(primary_schema, BaseEvolutionModel):
            errors.append(f"Primary schema {primary_schema.__name__} should inherit from BaseEvolutionModel")
    
    return errors

# ============================================================================
# Testing and Development Utilities  
# ============================================================================

def generate_test_data(schema_class, count: int = 1):
    """Generate test data for a given schema class"""
    test_data = []
    
    for i in range(count):
        if schema_class == SystemMetricSchema:
            data = create_metric_schema(
                name=f"test_metric_{i}",
                value=np.random.random(),
                metric_type=np.random.choice(list(MetricType)),
                primitive_source=np.random.choice(["test_primitive_a", "test_primitive_b"])
            )
        elif schema_class == CollaborationOutcomeSchema:
            data = create_collaboration_outcome_schema(
                session_id=f"test_session_{i}",
                primitives_used=["test_primitive"],
                user_satisfaction=np.random.random(),
                task_completion=np.random.random(),
                ethical_alignment=np.random.random(),
                efficiency_score=np.random.random(),
                creativity_score=np.random.random(),
                trust_level=np.random.random(),
                duration=np.random.uniform(60, 3600)
            )
        else:
            # For other schemas, create with minimal required fields
            data = schema_class()
        
        test_data.append(data)
    
    return test_data if count > 1 else test_data[0]

def benchmark_schema_performance():
    """Benchmark schema serialization/deserialization performance"""
    import time
    
    results = {}
    test_schemas = [
        SystemMetricSchema,
        CollaborationOutcomeSchema, 
        EvolutionInsightSchema,
        OptimizationActionSchema
    ]
    
    for schema_class in test_schemas:
        # Generate test data
        test_data = generate_test_data(schema_class, 100)
        if not isinstance(test_data, list):
            test_data = [test_data]
        
        # Benchmark serialization
        start_time = time.time()
        for data in test_data:
            json_str = data.json()
        serialize_time = time.time() - start_time
        
        # Benchmark deserialization  
        json_strings = [data.json() for data in test_data]
        start_time = time.time()
        for json_str in json_strings:
            schema_class.parse_raw(json_str)
        deserialize_time = time.time() - start_time
        
        results[schema_class.__name__] = {
            "serialize_time": serialize_time,
            "deserialize_time": deserialize_time,
            "total_time": serialize_time + deserialize_time
        }
    
    return results

if __name__ == "__main__":
    # Run validation tests
    print("Running schema validation tests...")
    validate_schema_consistency()
    
    # Check schema relationships
    relationship_errors = validate_schema_relationships()
    if relationship_errors:
        print("Schema relationship errors:", relationship_errors)
    else:
        print("✅ Schema relationships validated")
    
    # Generate sample data
    print("\nGenerating sample schemas...")
    samples = create_sample_schemas()
    for name, schema in samples.items():
        print(f"✅ Created sample {name}: {type(schema).__name__}")
    
    # Benchmark performance
    print("\nBenchmarking schema performance...")
    perf_results = benchmark_schema_performance()
    for schema_name, times in perf_results.items():
        print(f"{schema_name}: {times['total_time']:.4f}s total")
    
    print("\n🎉 Schema system validation complete!")
