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


# pact_hx/primitives/memory/manager.py
import uuid
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from collections import defaultdict, Counter
import math

from .schemas import MemoryEntry, MemoryState, MemoryType, EmotionalValence, ConsolidationRule

class MemoryManager:
    """
    Sovereign Memory Primitive for PACT-HX
    
    Philosophy: Powerful alone, transcendent when collaborating
    - Works independently without any other primitives
    - Offers collaboration interfaces for emergent behaviors
    - Maintains its own intelligence and decision-making
    """
    
    def __init__(self, agent_id: str, enable_collaboration: bool = False):
        self.agent_id = agent_id
        self.state = MemoryState(agent_id=agent_id, collaboration_enabled=enable_collaboration)
        self.collaboration_interfaces = {}
        
        # Independent capabilities
        self.similarity_threshold = 0.75
        self.max_episodic_memories = 1000
        self.consolidation_frequency = timedelta(hours=24)
        
    # ========== CORE INDEPENDENT FUNCTIONALITY ==========
    
    def store_memory(self, content: str, memory_type: MemoryType = MemoryType.EPISODIC, 
                    entities: List[str] = None, topics: List[str] = None,
                    emotional_valence: EmotionalValence = EmotionalValence.NEUTRAL,
                    **collaboration_hints) -> MemoryEntry:
        """
        Store a memory - works perfectly standalone
        Collaboration hints are optional enhancements
        """
        
        memory_entry = MemoryEntry(
            memory_id=str(uuid.uuid4()),
            memory_type=memory_type,
            content=content,
            entities=entities or [],
            topics=topics or [],
            emotional_valence=emotional_valence,
            importance=self._calculate_importance(content, entities, topics)
        )
        
        # Optional collaboration enhancement
        if collaboration_hints and self.state.collaboration_enabled:
            memory_entry = self._enhance_with_collaboration(memory_entry, collaboration_hints)
        
        # Store based on type
        if memory_type == MemoryType.EPISODIC:
            self.state.episodic_memories.append(memory_entry)
            self._manage_episodic_capacity()
        elif memory_type == MemoryType.SEMANTIC:
            self._store_semantic_pattern(memory_entry)
        elif memory_type == MemoryType.IDENTITY:
            self._update_identity_traits(memory_entry)
            
        self.state.total_memories += 1
        
        # Trigger consolidation if needed
        if self._should_consolidate():
            self.consolidate_memories()
            
        return memory_entry
    
    def retrieve_memories(self, query: str, memory_types: List[MemoryType] = None, 
                         limit: int = 10, min_confidence: float = 0.3) -> List[MemoryEntry]:
        """
        Retrieve relevant memories - sophisticated standalone capability
        """
        if memory_types is None:
            memory_types = [MemoryType.EPISODIC, MemoryType.SEMANTIC, MemoryType.IDENTITY]
            
        relevant_memories = []
        
        # Search episodic memories
        if MemoryType.EPISODIC in memory_types:
            for memory in self.state.episodic_memories:
                relevance = self._calculate_relevance(query, memory)
                if relevance >= min_confidence:
                    relevant_memories.append((memory, relevance))
        
        # Search semantic patterns
        if MemoryType.SEMANTIC in memory_types:
            semantic_matches = self._search_semantic_patterns(query, min_confidence)
            relevant_memories.extend(semantic_matches)
        
        # Search identity traits
        if MemoryType.IDENTITY in memory_types:
            identity_matches = self._search_identity_traits(query, min_confidence)
            relevant_memories.extend(identity_matches)
        
        # Sort by relevance and return top results
        relevant_memories.sort(key=lambda x: x[1], reverse=True)
        return [memory for memory, _ in relevant_memories[:limit]]
    
    def consolidate_memories(self) -> Dict[str, Any]:
        """
        Intelligent memory consolidation - episodic → semantic → identity
        Pure memory intelligence, no external dependencies
        """
        consolidation_stats = {
            "episodic_processed": 0,
            "semantic_patterns_found": 0,
            "identity_updates": 0,
            "memories_archived": 0
        }
        
        # Find patterns in episodic memories
        patterns = self._identify_patterns()
        for pattern in patterns:
            semantic_entry = self._create_semantic_memory(pattern)
            self._store_semantic_pattern(semantic_entry)
            consolidation_stats["semantic_patterns_found"] += 1
        
        # Update identity traits based on patterns
        identity_updates = self._extract_identity_signals(patterns)
        for trait, strength in identity_updates.items():
            self._update_identity_trait(trait, strength)
            consolidation_stats["identity_updates"] += 1
        
        # Archive old episodic memories
        archived = self._archive_old_memories()
        consolidation_stats["memories_archived"] = len(archived)
        consolidation_stats["episodic_processed"] = len(self.state.episodic_memories)
        
        self.state.last_consolidation = datetime.now()
        
        # Update efficiency metrics
        self.state.consolidation_efficiency = self._calculate_consolidation_efficiency()
        
        return consolidation_stats
    
    def get_memory_summary(self) -> Dict[str, Any]:
        """Get current memory state summary - standalone diagnostics"""
        return {
            "total_memories": self.state.total_memories,
            "episodic_count": len(self.state.episodic_memories),
            "semantic_patterns": len(self.state.semantic_patterns),
            "identity_traits": len(self.state.identity_traits),
            "last_consolidation": self.state.last_consolidation,
            "consolidation_efficiency": self.state.consolidation_efficiency,
            "collaboration_enabled": self.state.collaboration_enabled,
            "active_partnerships": self.state.primitive_partnerships
        }
    
    # ========== COLLABORATION INTERFACES ==========
    
    def enable_collaboration_with(self, primitive_type: str, primitive_instance: Any):
        """Enable collaboration with another PACT primitive"""
        self.state.collaboration_enabled = True
        self.collaboration_interfaces[primitive_type] = primitive_instance
        if primitive_type not in self.state.primitive_partnerships:
            self.state.primitive_partnerships.append(primitive_type)
    
    def share_memory_context(self, context_type: str = "recent") -> Dict[str, Any]:
        """Share memory context with other primitives"""
        if context_type == "recent":
            recent_memories = self.state.episodic_memories[-5:]
            return {
                "recent_topics": self._extract_topics(recent_memories),
                "recent_entities": self._extract_entities(recent_memories),
                "emotional_trend": self._calculate_emotional_trend(recent_memories),
                "confidence": 0.8
            }
        elif context_type == "identity":
            return {
                "core_traits": dict(list(self.state.identity_traits.items())[:10]),
                "preferences": self._get_preferences(),
                "behavioral_patterns": self._get_behavioral_patterns(),
                "confidence": 0.9
            }
        elif context_type == "semantic":
            return {
                "learned_patterns": dict(list(self.state.semantic_patterns.items())[:20]),
                "knowledge_domains": self._get_knowledge_domains(),
                "expertise_areas": self._get_expertise_areas(),
                "confidence": 0.7
            }
    
    def receive_collaboration_signal(self, primitive_type: str, signal_data: Dict[str, Any]):
        """Receive and process signals from other primitives"""
        if not self.state.collaboration_enabled:
            return
            
        if primitive_type == "attention":
            # Attention signals help prioritize memory storage and retrieval
            self._process_attention_signals(signal_data)
        elif primitive_type == "tone":
            # Tone signals help with emotional memory classification
            self._process_tone_signals(signal_data)
        elif primitive_type == "values":
            # Value signals help with importance weighting
            self._process_value_signals(signal_data)
    
    # ========== INTERNAL HELPER METHODS ==========
    
    def _calculate_importance(self, content: str, entities: List[str], topics: List[str]) -> float:
        """Calculate memory importance - pure memory intelligence"""
        base_importance = 0.5
        
        # Length and complexity
        if len(content) > 200:
            base_importance += 0.1
        
        # Entity richness
        base_importance += min(len(entities) * 0.05, 0.2)
        
        # Topic diversity
        base_importance += min(len(topics) * 0.03, 0.15)
        
        # Keyword significance
        important_keywords = ["important", "remember", "always", "never", "love", "hate"]
        for keyword in important_keywords:
            if keyword.lower() in content.lower():
                base_importance += 0.1
                break
        
        return min(base_importance, 1.0)
    
    def _calculate_relevance(self, query: str, memory: MemoryEntry) -> float:
        """Calculate query-memory relevance using simple similarity"""
        query_words = set(query.lower().split())
        content_words = set(memory.content.lower().split())
        entity_words = set([e.lower() for e in memory.entities])
        topic_words = set([t.lower() for t in memory.topics])
        
        all_memory_words = content_words.union(entity_words).union(topic_words)
        
        if not query_words or not all_memory_words:
            return 0.0
        
        intersection = query_words.intersection(all_memory_words)
        union = query_words.union(all_memory_words)
        
        jaccard_similarity = len(intersection) / len(union) if union else 0
        
        # Boost for exact entity/topic matches
        exact_entity_match = any(entity.lower() in query.lower() for entity in memory.entities)
        exact_topic_match = any(topic.lower() in query.lower() for topic in memory.topics)
        
        relevance = jaccard_similarity
        if exact_entity_match:
            relevance += 0.2
        if exact_topic_match:
            relevance += 0.15
        
        # Apply confidence and importance weights
        relevance *= memory.confidence * (0.5 + 0.5 * memory.importance)
        
        return min(relevance, 1.0)
    
    def _enhance_with_collaboration(self, memory: MemoryEntry, hints: Dict[str, Any]) -> MemoryEntry:
        """Enhance memory with collaboration hints"""
        if "attention_context" in hints:
            memory.attention_context = hints["attention_context"]
            # Boost importance if high attention
            if hints["attention_context"].get("salience", 0) > 0.7:
                memory.importance = min(memory.importance + 0.1, 1.0)
        
        if "tone_signals" in hints:
            memory.tone_signals = hints["tone_signals"]
            # Adjust emotional valence based on tone
            tone_emotional = hints["tone_signals"].get("emotional_warmth", 0)
            if tone_emotional > 0.5 and memory.emotional_valence == EmotionalValence.NEUTRAL:
                memory.emotional_valence = EmotionalValence.POSITIVE
            elif tone_emotional < -0.5 and memory.emotional_valence == EmotionalValence.NEUTRAL:
                memory.emotional_valence = EmotionalValence.NEGATIVE
        
        if "value_alignment" in hints:
            memory.value_alignment = hints["value_alignment"]
            # Boost importance for value-aligned content
            if hints["value_alignment"].get("alignment_score", 0) > 0.8:
                memory.importance = min(memory.importance + 0.15, 1.0)
        
        return memory
    
    def _should_consolidate(self) -> bool:
        """Determine if memory consolidation should run"""
        time_threshold = datetime.now() - self.state.last_consolidation > self.consolidation_frequency
        memory_threshold = len(self.state.episodic_memories) > 100
        return time_threshold or memory_threshold
    
    def _identify_patterns(self) -> List[Dict[str, Any]]:
        """Identify patterns in episodic memories for semantic consolidation"""
        patterns = []
        
        # Topic clustering
        topic_frequency = Counter()
        entity_frequency = Counter()
        
        for memory in self.state.episodic_memories:
            for topic in memory.topics:
                topic_frequency[topic] += 1
            for entity in memory.entities:
                entity_frequency[entity] += 1
        
        # Identify frequent patterns
        for topic, freq in topic_frequency.most_common(10):
            if freq >= 3:  # Pattern threshold
                related_memories = [m for m in self.state.episodic_memories if topic in m.topics]
                patterns.append({
                    "type": "topic_pattern",
                    "key": topic,
                    "frequency": freq,
                    "memories": related_memories,
                    "confidence": min(freq / 10.0, 1.0)
                })
        
        return patterns
    
    def _create_semantic_memory(self, pattern: Dict[str, Any]) -> MemoryEntry:
        """Create semantic memory from identified pattern"""
        return MemoryEntry(
            memory_id=str(uuid.uuid4()),
            memory_type=MemoryType.SEMANTIC,
            content=f"Pattern: {pattern['key']} (frequency: {pattern['frequency']})",
            confidence=pattern["confidence"],
            importance=0.7,
            topics=[pattern["key"]],
            entities=list(set([e for m in pattern["memories"] for e in m.entities]))
        )
    
    def _manage_episodic_capacity(self):
        """Manage episodic memory capacity"""
        if len(self.state.episodic_memories) > self.max_episodic_memories:
            # Remove oldest, least important memories
            self.state.episodic_memories.sort(key=lambda m: (m.importance, m.timestamp))
            self.state.episodic_memories = self.state.episodic_memories[100:]  # Keep most recent 900
    
    def _calculate_consolidation_efficiency(self) -> float:
        """Calculate how efficiently memory consolidation is working"""
        if self.state.total_memories == 0:
            return 0.0
        
        semantic_ratio = len(self.state.semantic_patterns) / max(self.state.total_memories, 1)
        identity_ratio = len(self.state.identity_traits) / max(self.state.total_memories, 1) 
        
        return min((semantic_ratio + identity_ratio) * 2, 1.0)
    
    # Additional helper methods for collaboration
    def _extract_topics(self, memories: List[MemoryEntry]) -> List[str]:
        """Extract topics from memory list"""
        topics = []
        for memory in memories:
            topics.extend(memory.topics)
        return list(set(topics))
    
    def _extract_entities(self, memories: List[MemoryEntry]) -> List[str]:
        """Extract entities from memory list"""
        entities = []
        for memory in memories:
            entities.extend(memory.entities)
        return list(set(entities))
    
    def _calculate_emotional_trend(self, memories: List[MemoryEntry]) -> str:
        """Calculate emotional trend from recent memories"""
        if not memories:
            return "neutral"
        
        valence_counts = Counter([m.emotional_valence for m in memories])
        most_common = valence_counts.most_common(1)[0][0]
        return most_common.value
    
    # Placeholder methods for full implementation
    def _store_semantic_pattern(self, memory: MemoryEntry):
        """Store semantic pattern"""
        key = memory.topics[0] if memory.topics else memory.content[:50]
        self.state.semantic_patterns[key] = {
            "content": memory.content,
            "confidence": memory.confidence,
            "created": memory.timestamp
        }
    
    def _update_identity_traits(self, memory: MemoryEntry):
        """Update identity traits based on memory"""
        # Extract potential traits from content
        trait_keywords = {
            "creative": ["creative", "art", "design", "innovative"],
            "analytical": ["analyze", "data", "logic", "systematic"],
            "social": ["friend", "team", "social", "collaborative"],
            "technical": ["code", "programming", "technical", "engineering"]
        }
        
        for trait, keywords in trait_keywords.items():
            if any(keyword in memory.content.lower() for keyword in keywords):
                current = self.state.identity_traits.get(trait, 0.0)
                self.state.identity_traits[trait] = min(current + 0.1, 1.0)
    
    def _search_semantic_patterns(self, query: str, min_confidence: float) -> List[Tuple[MemoryEntry, float]]:
        """Search semantic patterns - placeholder for now"""
        return []
    
    def _search_identity_traits(self, query: str, min_confidence: float) -> List[Tuple[MemoryEntry, float]]:
        """Search identity traits - placeholder for now"""
        return []
    
    def _extract_identity_signals(self, patterns: List[Dict[str, Any]]) -> Dict[str, float]:
        """Extract identity signals from patterns"""
        return {}
    
    def _update_identity_trait(self, trait: str, strength: float):
        """Update specific identity trait"""
        current = self.state.identity_traits.get(trait, 0.0)
        self.state.identity_traits[trait] = min(current + strength, 1.0)
    
    def _archive_old_memories(self) -> List[MemoryEntry]:
        """Archive old memories"""
        return []
    
    def _get_preferences(self) -> Dict[str, Any]:
        """Get user preferences from identity"""
        return {}
    
    def _get_behavioral_patterns(self) -> Dict[str, Any]:
        """Get behavioral patterns"""
        return {}
    
    def _get_knowledge_domains(self) -> List[str]:
        """Get knowledge domains"""
        return []
    
    def _get_expertise_areas(self) -> List[str]:
        """Get expertise areas"""
        return []
    
    def _process_attention_signals(self, signal_data: Dict[str, Any]):
        """Process signals from attention primitive"""
        pass
    
    def _process_tone_signals(self, signal_data: Dict[str, Any]):
        """Process signals from tone primitive"""
        pass
    
    def _process_value_signals(self, signal_data: Dict[str, Any]):
        """Process signals from values primitive"""
        pass
