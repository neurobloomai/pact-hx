from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel

class PACTConfig(BaseModel):
    """Base configuration for all PACT primitives"""
    version: str = "0.1.0"
    agent_id: str
    session_id: Optional[str] = None
    
class PACTPrimitive(ABC):
    """Abstract base class for all PACT-HX primitives"""
    
    def __init__(self, config: PACTConfig):
        self.config = config
        self.version = "0.1.0"
    
    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input through this primitive"""
        pass
    
    @abstractmethod
    def get_state(self) -> Dict[str, Any]:
        """Get current state for serialization"""
        pass
    
    @abstractmethod
    def load_state(self, state: Dict[str, Any]) -> None:
        """Load state from serialization"""
        pass
