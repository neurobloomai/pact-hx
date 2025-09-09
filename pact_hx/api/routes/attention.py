from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from ...primitives.attention.manager import AttentionManager

router = APIRouter(prefix="/attention", tags=["attention"])

# Global manager registry (replace with proper storage)
managers: Dict[str, AttentionManager] = {}

class AttentionUpdateRequest(BaseModel):
    agent_id: str
    entities: List[str]
    context: str

class AttentionResponse(BaseModel):
    current_focus: List[str]
    salience_weights: Dict[str, float]
    pact_version: str = "0.1.0"

@router.post("/update", response_model=AttentionResponse)
async def update_attention(request: AttentionUpdateRequest):
    """Update attention state for an agent"""
    
    # Get or create manager
    if request.agent_id not in managers:
        managers[request.agent_id] = AttentionManager(request.agent_id)
    
    manager = managers[request.agent_id]
    result = manager.update_attention(request.entities, request.context)
    
    return AttentionResponse(
        current_focus=result["current_focus"],
        salience_weights=result["salience_weights"]
    )

@router.get("/{agent_id}", response_model=AttentionResponse)
async def get_attention(agent_id: str):
    """Get current attention state for an agent"""
    
    if agent_id not in managers:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    manager = managers[agent_id]
    context = manager.get_attention_context()
    
    return AttentionResponse(
        current_focus=context["focus"],
        salience_weights=context["weights"]
    )
