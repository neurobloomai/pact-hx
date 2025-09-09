# pact_hx/api/routes/memory.py
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

from ...primitives.memory.manager import MemoryManager
from ...primitives.memory.schemas import MemoryEntry, MemoryType, EmotionalValence

router = APIRouter(prefix="/memory", tags=["memory"])

# Global manager registry (replace with proper storage in production)
managers: Dict[str, MemoryManager] = {}

# ========== REQUEST/RESPONSE MODELS ==========

class StoreMemoryRequest(BaseModel):
    agent_id: str
    content: str
    memory_type: MemoryType = MemoryType.EPISODIC
    entities: Optional[List[str]] = None
    topics: Optional[List[str]] = None
    emotional_valence: EmotionalValence = EmotionalValence.NEUTRAL
    
    # Collaboration hints (optional)
    attention_context: Optional[Dict[str, Any]] = None
    tone_signals: Optional[Dict[str, float]] = None
    value_alignment: Optional[Dict[str, Any]] = None

class RetrieveMemoryRequest(BaseModel):
    agent_id: str
    query: str
    memory_types: Optional[List[MemoryType]] = None
    limit: int = Field(default=10, ge=1, le=100)
    min_confidence: float = Field(default=0.3, ge=0.0, le=1.0)

class MemoryResponse(BaseModel):
    memory_id: str
    content: str
    memory_type: MemoryType
    timestamp: datetime
    confidence: float
    importance: float
    emotional_valence: EmotionalValence
    entities: List[str]
    topics: List[str]
    pact_version: str = "0.1.0"

class MemorySummaryResponse(BaseModel):
    agent_id: str
    total_memories: int
    episodic_count: int
    semantic_patterns: int
    identity_traits: int
    last_consolidation: datetime
    consolidation_efficiency: float
    collaboration_enabled: bool
    active_partnerships: List[str]
    pact_version: str = "0.1.0"

class ConsolidationResponse(BaseModel):
    agent_id: str
    consolidation_stats: Dict[str, Any]
    success: bool
    message: str
    pact_version: str = "0.1.0"

class CollaborationRequest(BaseModel):
    agent_id: str
    primitive_type: str
    enable: bool = True

class ContextShareResponse(BaseModel):
    agent_id: str
    context_type: str
    context_data: Dict[str, Any]
    confidence: float
    pact_version: str = "0.1.0"

# ========== CORE MEMORY ENDPOINTS ==========

@router.post("/store", response_model=MemoryResponse)
async def store_memory(request: StoreMemoryRequest):
    """
    Store a memory - sovereign operation with optional collaboration
    """
    
    # Get or create manager
    if request.agent_id not in managers:
        managers[request.agent_id] = MemoryManager(request.agent_id, enable_collaboration=True)
    
    manager = managers[request.agent_id]
    
    # Prepare collaboration hints
    collaboration_hints = {}
    if request.attention_context:
        collaboration_hints["attention_context"] = request.attention_context
    if request.tone_signals:
        collaboration_hints["tone_signals"] = request.tone_signals
    if request.value_alignment:
        collaboration_hints["value_alignment"] = request.value_alignment
    
    # Store memory (works with or without collaboration)
    memory_entry = manager.store_memory(
        content=request.content,
        memory_type=request.memory_type,
        entities=request.entities or [],
        topics=request.topics or [],
        emotional_valence=request.emotional_valence,
        **collaboration_hints
    )
    
    return MemoryResponse(
        memory_id=memory_entry.memory_id,
        content=memory_entry.content,
        memory_type=memory_entry.memory_type,
        timestamp=memory_entry.timestamp,
        confidence=memory_entry.confidence,
        importance=memory_entry.importance,
        emotional_valence=memory_entry.emotional_valence,
        entities=memory_entry.entities,
        topics=memory_entry.topics
    )

@router.post("/retrieve", response_model=List[MemoryResponse])
async def retrieve_memories(request: RetrieveMemoryRequest):
    """
    Retrieve relevant memories - sophisticated standalone capability
    """
    
    if request.agent_id not in managers:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    manager = managers[request.agent_id]
    
    memories = manager.retrieve_memories(
        query=request.query,
        memory_types=request.memory_types,
        limit=request.limit,
        min_confidence=request.min_confidence
    )
    
    return [
        MemoryResponse(
            memory_id=memory.memory_id,
            content=memory.content,
            memory_type=memory.memory_type,
            timestamp=memory.timestamp,
            confidence=memory.confidence,
            importance=memory.importance,
            emotional_valence=memory.emotional_valence,
            entities=memory.entities,
            topics=memory.topics
        )
        for memory in memories
    ]

@router.get("/{agent_id}/summary", response_model=MemorySummaryResponse)
async def get_memory_summary(agent_id: str):
    """
    Get memory state summary - standalone diagnostics
    """
    
    if agent_id not in managers:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    manager = managers[agent_id]
    summary = manager.get_memory_summary()
    
    return MemorySummaryResponse(
        agent_id=agent_id,
        **summary
    )

@router.post("/{agent_id}/consolidate", response_model=ConsolidationResponse)
async def consolidate_memories(agent_id: str):
    """
    Trigger memory consolidation - episodic → semantic → identity
    """
    
    if agent_id not in managers:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    manager = managers[agent_id]
    
    try:
        stats = manager.consolidate_memories()
        return ConsolidationResponse(
            agent_id=agent_id,
            consolidation_stats=stats,
            success=True,
            message="Memory consolidation completed successfully"
        )
    except Exception as e:
        return ConsolidationResponse(
            agent_id=agent_id,
            consolidation_stats={},
            success=False,
            message=f"Consolidation failed: {str(e)}"
        )

# ========== COLLABORATION ENDPOINTS ==========

@router.post("/{agent_id}/collaboration/enable")
async def enable_collaboration(agent_id: str, request: CollaborationRequest):
    """
    Enable collaboration with another primitive
    """
    
    if agent_id not in managers:
        managers[agent_id] = MemoryManager(agent_id, enable_collaboration=True)
    
    manager = managers[agent_id]
    
    if request.enable:
        # Note: In real implementation, would need reference to actual primitive
        manager.enable_collaboration_with(request.primitive_type, None)
        message = f"Collaboration enabled with {request.primitive_type}"
    else:
        # Disable collaboration logic
        if request.primitive_type in manager.collaboration_interfaces:
            del manager.collaboration_interfaces[request.primitive_type]
            if request.primitive_type in manager.state.primitive_partnerships:
                manager.state.primitive_partnerships.remove(request.primitive_type)
            message = f"Collaboration disabled with {request.primitive_type}"
        else:
            message = f"No active collaboration with {request.primitive_type}"
    
    return {
        "agent_id": agent_id,
        "primitive_type": request.primitive_type,
        "collaboration_enabled": request.enable,
        "message": message,
        "active_partnerships": manager.state.primitive_partnerships
    }

@router.get("/{agent_id}/context/{context_type}", response_model=ContextShareResponse)
async def share_context(
    agent_id: str, 
    context_type: str = Query(..., regex="^(recent|identity|semantic)$")
):
    """
    Share memory context with other primitives
    Context types: recent, identity, semantic
    """
    
    if agent_id not in managers:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    manager = managers[agent_id]
    
    try:
        context_data = manager.share_memory_context(context_type)
        return ContextShareResponse(
            agent_id=agent_id,
            context_type=context_type,
            context_data=context_data,
            confidence=context_data.get("confidence", 0.5)
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to generate context: {str(e)}")

@router.post("/{agent_id}/collaboration/signal")
async def receive_collaboration_signal(
    agent_id: str,
    primitive_type: str,
    signal_data: Dict[str, Any]
):
    """
    Receive collaboration signal from another primitive
    """
    
    if agent_id not in managers:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    manager = managers[agent_id]
    
    try:
        manager.receive_collaboration_signal(primitive_type, signal_data)
        return {
            "agent_id": agent_id,
            "primitive_type": primitive_type,
            "signal_processed": True,
            "message": f"Signal from {primitive_type} processed successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process signal: {str(e)}")

# ========== ADVANCED QUERY ENDPOINTS ==========

@router.get("/{agent_id}/memories/by-type/{memory_type}")
async def get_memories_by_type(
    agent_id: str,
    memory_type: MemoryType,
    limit: int = Query(default=20, ge=1, le=100),
    min_confidence: float = Query(default=0.0, ge=0.0, le=1.0)
):
    """
    Get memories filtered by type
    """
    
    if agent_id not in managers:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    manager = managers[agent_id]
    
    if memory_type == MemoryType.EPISODIC:
        memories = [m for m in manager.state.episodic_memories 
                   if m.confidence >= min_confidence][:limit]
    elif memory_type == MemoryType.SEMANTIC:
        # Convert semantic patterns to memory entries for consistency
        memories = []
        for key, pattern in list(manager.state.semantic_patterns.items())[:limit]:
            memories.append({
                "memory_id": f"semantic_{key}",
                "content": pattern.get("content", key),
                "memory_type": MemoryType.SEMANTIC,
                "confidence": pattern.get("confidence", 0.7),
                "timestamp": pattern.get("created", datetime.now()),
                "importance": 0.7,
                "emotional_valence": EmotionalValence.NEUTRAL,
                "entities": [],
                "topics": [key]
            })
    elif memory_type == MemoryType.IDENTITY:
        # Convert identity traits to memory entries
        memories = []
        for trait, strength in list(manager.state.identity_traits.items())[:limit]:
            if strength >= min_confidence:
                memories.append({
                    "memory_id": f"identity_{trait}",
                    "content": f"Identity trait: {trait} (strength: {strength:.2f})",
                    "memory_type": MemoryType.IDENTITY,
                    "confidence": strength,
                    "timestamp": datetime.now(),
                    "importance": strength,
                    "emotional_valence": EmotionalValence.NEUTRAL,
                    "entities": [],
                    "topics": [trait]
                })
    
    return [
        MemoryResponse(**memory) if isinstance(memory, dict) else MemoryResponse(
            memory_id=memory.memory_id,
            content=memory.content,
            memory_type=memory.memory_type,
            timestamp=memory.timestamp,
            confidence=memory.confidence,
            importance=memory.importance,
            emotional_valence=memory.emotional_valence,
            entities=memory.entities,
            topics=memory.topics
        )
        for memory in memories
    ]

@router.get("/{agent_id}/analytics")
async def get_memory_analytics(agent_id: str):
    """
    Get memory analytics and insights
    """
    
    if agent_id not in managers:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    manager = managers[agent_id]
    
    # Calculate analytics
    episodic_memories = manager.state.episodic_memories
    
    # Emotional distribution
    emotional_distribution = {}
    for valence in EmotionalValence:
        count = len([m for m in episodic_memories if m.emotional_valence == valence])
        emotional_distribution[valence.value] = count
    
    # Topic frequency
    topic_frequency = {}
    for memory in episodic_memories:
        for topic in memory.topics:
            topic_frequency[topic] = topic_frequency.get(topic, 0) + 1
    
    # Entity frequency
    entity_frequency = {}
    for memory in episodic_memories:
        for entity in memory.entities:
            entity_frequency[entity] = entity_frequency.get(entity, 0) + 1
    
    # Average metrics
    avg_confidence = sum(m.confidence for m in episodic_memories) / len(episodic_memories) if episodic_memories else 0
    avg_importance = sum(m.importance for m in episodic_memories) / len(episodic_memories) if episodic_memories else 0
    
    return {
        "agent_id": agent_id,
        "analytics": {
            "memory_counts": {
                "episodic": len(episodic_memories),
                "semantic": len(manager.state.semantic_patterns),
                "identity": len(manager.state.identity_traits)
            },
            "emotional_distribution": emotional_distribution,
            "top_topics": dict(sorted(topic_frequency.items(), key=lambda x: x[1], reverse=True)[:10]),
            "top_entities": dict(sorted(entity_frequency.items(), key=lambda x: x[1], reverse=True)[:10]),
            "average_confidence": round(avg_confidence, 3),
            "average_importance": round(avg_importance, 3),
            "consolidation_efficiency": manager.state.consolidation_efficiency,
            "collaboration_status": {
                "enabled": manager.state.collaboration_enabled,
                "active_partnerships": manager.state.primitive_partnerships
            }
        },
        "pact_version": "0.1.0"
    }

# ========== UTILITY ENDPOINTS ==========

@router.delete("/{agent_id}/memories/{memory_id}")
async def delete_memory(agent_id: str, memory_id: str):
    """
    Delete a specific memory
    """
    
    if agent_id not in managers:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    manager = managers[agent_id]
    
    # Find and remove memory
    for i, memory in enumerate(manager.state.episodic_memories):
        if memory.memory_id == memory_id:
            deleted_memory = manager.state.episodic_memories.pop(i)
            return {
                "agent_id": agent_id,
                "memory_id": memory_id,
                "deleted": True,
                "message": "Memory deleted successfully"
            }
    
    raise HTTPException(status_code=404, detail="Memory not found")

@router.post("/{agent_id}/reset")
async def reset_memory(agent_id: str, confirm: bool = False):
    """
    Reset all memory for an agent (use with caution)
    """
    
    if not confirm:
        raise HTTPException(status_code=400, detail="Must set confirm=true to reset memory")
    
    if agent_id in managers:
        del managers[agent_id]
    
    return {
        "agent_id": agent_id,
        "reset": True,
        "message": "All memory data reset for agent"
    }

# ========== HEALTH CHECK ==========

@router.get("/health")
async def memory_health_check():
    """
    Health check for memory service
    """
    return {
        "service": "pact-hx-memory",
        "status": "healthy",
        "version": "0.1.0",
        "active_agents": len(managers),
        "total_memories": sum(len(m.state.episodic_memories) for m in managers.values()),
        "collaboration_enabled_agents": len([m for m in managers.values() if m.state.collaboration_enabled])
    }
