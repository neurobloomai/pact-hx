# pact_hx/primitives/tone_adapt/schemas.py
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum

class ToneDimension(str, Enum):
    """Core dimensions of communication tone"""
    FORMALITY = "formality"           # casual ↔ professional
    DIRECTNESS = "directness"         # diplomatic ↔ blunt
    ENTHUSIASM = "enthusiasm"         # reserved ↔ energetic
    TECHNICAL_DEPTH = "technical_depth"  # simple ↔ detailed
    EMOTIONAL_WARMTH = "emotional_warmth"  # neutral ↔ empathetic
    CONFIDENCE = "confidence"         # uncertain ↔ assertive
    PACE = "pace"                    # slow ↔ fast
    HUMOR = "humor"                  # serious ↔ playful

class ToneProfile(BaseModel):
    """User's preferred communication style profile"""
    user_id: str
    baseline_preferences: Dict[ToneDimension, float] = Field(
        default_factory=dict,
        description="Base tone preferences [-1.0 to 1.0] for each dimension"
    )
    contextual_modifiers: Dict[str, Dict[ToneDimension, float]] = Field(
        default_factory=dict,
        description="Context-specific tone adjustments"
    )
    adaptation_sensitivity: float = Field(
        default=0.5, ge=0.0, le=1.0,
        description="How quickly to adapt to user feedback"
    )
    confidence_score: float = Field(
        default=0.0, ge=0.0, le=1.0,
        description="Confidence in current tone profile"
    )
    last_updated: datetime = Field(default_factory=datetime.now)

class ToneContext(BaseModel):
    """Current conversational context affecting tone"""
    conversation_type: Optional[str] = None  # "casual", "professional", "support", "teaching"
    user_emotional_state: Optional[str] = None  # "frustrated", "excited", "confused", "happy"
    topic_domain: Optional[str] = None  # "technical", "personal", "business", "creative"
    urgency_level: Optional[str] = None  # "low", "medium", "high", "urgent"
    relationship_stage: Optional[str] = None  # "new", "developing", "established", "expert"
    
    # Collaboration inputs
    attention_signals: Optional[Dict[str, Any]] = None
    memory_signals: Optional[Dict[str, Any]] = None
    value_signals: Optional[Dict[str, Any]] = None

class ToneAdjustment(BaseModel):
    """Specific tone adjustment for current interaction"""
    adjustment_id: str
    target_dimensions: Dict[ToneDimension, float] = Field(
        description="Target tone values for this interaction"
    )
    context: ToneContext
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str = Field(description="Why this adjustment was made")
    timestamp: datetime = Field(default_factory=datetime.now)
    
    # Performance tracking
    user_feedback: Optional[str] = None  # "positive", "negative", "neutral"
    effectiveness_score: Optional[float] = None

class ToneCalibration(BaseModel):
    """Learning data for tone adaptation"""
    user_responses: List[Dict[str, Any]] = Field(default_factory=list)
    successful_adjustments: List[ToneAdjustment] = Field(default_factory=list)
    failed_adjustments: List[ToneAdjustment] = Field(default_factory=list)
    adaptation_patterns: Dict[str, Any] = Field(default_factory=dict)

class ToneState(BaseModel):
    """Complete tone adaptation state"""
    agent_id: str
    user_profile: ToneProfile
    current_adjustment: Optional[ToneAdjustment] = None
    calibration_data: ToneCalibration = Field(default_factory=ToneCalibration)
    
    # Collaboration state
    collaboration_enabled: bool = Field(default=False)
    primitive_partnerships: List[str] = Field(default_factory=list)
    
    # Performance metrics
    adaptation_accuracy: float = Field(default=0.0)
    user_satisfaction_trend: float = Field(default=0.0)
    total_adjustments: int = Field(default=0)

