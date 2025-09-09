from typing import Dict, List, Any, Optional
from pydantic import BaseModel
import time

class AttentionState(BaseModel):
    current_focus: List[str] = []
    focus_history: List[Dict[str, Any]] = []
    salience_weights: Dict[str, float] = {}
    last_updated: float = 0.0

class AttentionManager:
    """Manages personalized attention for human interactions"""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.state = AttentionState()
    
    def update_attention(self, entities: List[str], context: str) -> Dict[str, Any]:
        """Update attention based on new input"""
        timestamp = time.time()
        
        # Update current focus
        self.state.current_focus = entities[:5]  # Keep top 5
        
        # Update salience weights
        for entity in entities:
            current_weight = self.state.salience_weights.get(entity, 0.0)
            self.state.salience_weights[entity] = min(current_weight + 0.1, 1.0)
        
        # Record in history
        self.state.focus_history.append({
            "timestamp": timestamp,
            "entities": entities,
            "context": context[:100]  # Truncated context
        })
        
        # Keep history manageable
        if len(self.state.focus_history) > 100:
            self.state.focus_history = self.state.focus_history[-50:]
        
        self.state.last_updated = timestamp
        
        return {
            "current_focus": self.state.current_focus,
            "salience_weights": dict(list(self.state.salience_weights.items())[:10])
        }
    
    def get_attention_context(self) -> Dict[str, Any]:
        """Get current attention context for other primitives"""
        return {
            "focus": self.state.current_focus,
            "weights": self.state.salience_weights,
            "last_updated": self.state.last_updated
        }
