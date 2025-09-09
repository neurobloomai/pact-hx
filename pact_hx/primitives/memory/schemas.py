# pact_hx/primitives/memory/schemas.py
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from enum import Enum

class MemoryType(str, Enum):
    """Types of memory in PACT-HX system"""
    EPISODIC = "episodic"      # Specific conversations/events
    SEMANTIC = "semantic"      # Patterns and learned knowledge
    IDENTITY = "identity"      # Core user traits and preferences

class EmotionalValence(str, Enum):
    """Emotional tone of memories"""
    POSITIVE = "positive"
    NEGATIVE = "negative" 
    NEUTRAL = "neutral"
    MIXED = "mixed"

class MemoryEntry(BaseModel):
    """Individual memory entry - core standalone structure"""
    memory_id: str = Field(..., description="Unique identifier for this memory")
    memory_type: MemoryType = Field(..., description="Type of memory")
    content: str = Field(..., description="The actual memory content")
    timestamp: datetime = Field(default_factory=datetime.now)
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Confidence in this memory")
    emotional_valence: EmotionalValence = Field(default=EmotionalValence.NEUTRAL)
    importance: float = Field(default=0.5, ge=0.0, le=1.0, description="Importance score for consolidation")
    
    # Core metadata that works standalone
    entities: List[str] = Field(default_factory=list, description="Key entities mentioned")
    topics: List[str] = Field(default_factory=list, description="Topics discussed")
    user_feedback: Optional[str] = Field(None, description="User feedback on this interaction")
    
    # Collaboration interfaces (optional)
    attention_context: Optional[Dict[str, Any]] = Field(None, description="Attention state when memory created")
    tone_signals: Optional[Dict[str, float]] = Field(None, description="Tone adaptation signals")
    value_alignment: Optional[Dict[str, Any]] = Field(None, description="Value alignment context")
    
    # Cross-primitive learnings
    collaboration_signals: Optional[Dict[str, Any]] = Field(None, description="Signals from other primitives")

class ConsolidationRule(BaseModel):
    """Rules for memory consolidation - episodic → semantic → identity"""
    trigger_threshold: float = Field(default=0.8, description="Confidence threshold for consolidation")
    pattern_similarity: float = Field(default=0.7, description="Similarity threshold for pattern recognition")
    temporal_decay: float = Field(default=0.1, description="How much memories fade over time")
    importance_boost: float = Field(default=0.2, description="Boost for emotionally significant memories")

class MemoryState(BaseModel):
    """Complete memory state for an agent - sovereign yet collaborative"""
    agent_id: str
    
    # Core memory stores (independent operation)
    episodic_memories: List[MemoryEntry] = Field(default_factory=list)
    semantic_patterns: Dict[str, Any] = Field(default_factory=dict) 
    identity_traits: Dict[str, float] = Field(default_factory=dict)
    
    # Consolidation and learning
    consolidation_rules: ConsolidationRule = Field(default_factory=ConsolidationRule)
    last_consolidation: datetime = Field(default_factory=datetime.now)
    total_memories: int = Field(default=0)
    
    # Collaboration state (optional)
    collaboration_enabled: bool = Field(default=False)
    primitive_partnerships: List[str] = Field(default_factory=list)
    
    # Performance metrics
    retrieval_accuracy: float = Field(default=0.0)
    consolidation_efficiency: float = Field(default=0.0)
