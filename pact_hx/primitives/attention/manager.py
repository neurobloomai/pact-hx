# pact_hx/primitives/attention/manager.py
"""
PACT-HX Attention Manager

Core implementation of the attention primitive for cognitive focus management.
This is the foundational primitive that determines what matters most in
conversations and provides attention context to all other primitives.

Architecture: Sovereign primitive with collaboration interfaces
- Works powerfully alone (independent cognitive processing)
- Provides rich signals for memory, tone, and value primitives
- Learns from user feedback and behavioral patterns
"""

import time
import math
import re
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Set, Union
from collections import defaultdict, Counter
import logging

from .schemas import (
    AttentionScope, AttentionTrigger, EntityType,
    AttentionEntity, AttentionFocus, AttentionTransition,
    AttentionDecayRule, AttentionConfiguration, AttentionState,
    AttentionContextResponse, AttentionUpdateResponse
)

logger = logging.getLogger(__name__)

class AttentionManager:
    """
    Sovereign Attention Primitive for PACT-HX
    
    The cognitive foundation that determines what matters most to users.
    Provides attention context and focus management for all AI interactions.
    
    Core Capabilities:
    - Entity salience tracking with temporal decay
    - Focus transition analysis and prediction
    - Collaborative signal integration
    - User feedback learning and adaptation
    - Performance monitoring and optimization
    """
    
    def __init__(
        self, 
        agent_id: str, 
        user_id: Optional[str] = None,
        config: Optional[AttentionConfiguration] = None,
        enable_collaboration: bool = False
    ):
        self.agent_id = agent_id
        self.user_id = user_id or agent_id
        
        # Initialize state with configuration
        self.state = AttentionState(
            agent_id=agent_id,
            user_id=self.user_id,
            config=config or AttentionConfiguration(),
            collaboration_enabled=enable_collaboration
        )
        
        # Collaboration interfaces
        self.collaboration_interfaces = {}
        
        # Processing parameters (can be tuned)
        self.entity_extraction_min_length = 3
        self.novelty_bonus_threshold = 0.7
        self.context_window_size = 500  # characters
        
        # Performance tracking
        self._last_performance_update = datetime.now()
        self._feedback_buffer = []
        
        logger.info(f"AttentionManager initialized for agent {agent_id}")
    
    # ========== CORE ATTENTION PROCESSING ==========
    
    def update_attention(
        self, 
        entities: List[str], 
        context: str,
        user_emphasis: Optional[Dict[str, float]] = None,
        explicit_focus: Optional[List[str]] = None,
        context_type: Optional[str] = None,
        **collaboration_hints
    ) -> AttentionUpdateResponse:
        """
        Update attention state based on new input
        
        This is the primary interface for updating attention. It processes
        new entities, analyzes focus shifts, and updates internal state.
        
        Args:
            entities: List of entities mentioned in current input
            context: Full context/conversation content
            user_emphasis: Explicit user emphasis signals {entity: weight}
            explicit_focus: User explicitly stated focus entities
            context_type: Type of context (casual, professional, urgent, etc.)
            **collaboration_hints: Optional signals from other primitives
            
        Returns:
            AttentionUpdateResponse with current state and changes
        """
        
        start_time = time.time()
        logger.debug(f"Updating attention for {len(entities)} entities")
        
        # Store previous state for comparison
        previous_focus = self.state.current_focus.primary_entities if self.state.current_focus else []
        
        try:
            # 1. Process and score entities
            processed_entities = self._process_entities(
                entities, context, user_emphasis or {}, explicit_focus or []
            )
            
            # 2. Determine if focus should shift
            focus_analysis = self._analyze_focus_shift_need(
                processed_entities, context, context_type
            )
            
            # 3. Apply collaboration enhancements
            if self.state.collaboration_enabled and collaboration_hints:
                focus_analysis = self._enhance_with_collaboration(
                    focus_analysis, collaboration_hints
                )
            
            # 4. Update entity tracking
            new_entities_tracked = 0
            for entity_data in processed_entities:
                if self._update_entity_tracking(entity_data):
                    new_entities_tracked += 1
            
            # 5. Execute focus transition if needed
            focus_changed = False
            transition_info = None
            
            if focus_analysis["should_shift"]:
                new_focus = self._create_new_focus(
                    processed_entities, context, focus_analysis, context_type
                )
                transition_info = self._transition_focus(
                    new_focus, focus_analysis["transition_type"]
                )
                focus_changed = True
                logger.info(f"Focus shifted: {focus_analysis['primary_reason']}")
            else:
                # Update current focus without shifting
                self._update_current_focus(processed_entities, context)
            
            # 6. Apply attention decay
            self._apply_attention_decay()
            
            # 7. Update performance metrics
            self._update_performance_metrics()
            
            # 8. Update state metadata
            self.state.total_interactions += 1
            self.state.last_updated = datetime.now()
            
            # 9. Generate response
            current_focus = self.state.current_focus.primary_entities if self.state.current_focus else []
            salience_weights = self.get_salience_scores(current_focus)
            focus_quality = self.state.current_focus.calculate_overall_quality() if self.state.current_focus else 0.0
            
            processing_time = time.time() - start_time
            logger.debug(f"Attention update completed in {processing_time:.3f}s")
            
            return AttentionUpdateResponse(
                agent_id=self.agent_id,
                update_successful=True,
                focus_changed=focus_changed,
                new_entities_tracked=new_entities_tracked,
                current_focus=current_focus,
                salience_weights=salience_weights,
                focus_quality_score=focus_quality,
                transition_info=transition_info
            )
            
        except Exception as e:
            logger.error(f"Error updating attention: {str(e)}")
            return AttentionUpdateResponse(
                agent_id=self.agent_id,
                update_successful=False,
                focus_changed=False,
                new_entities_tracked=0,
                current_focus=[],
                salience_weights={},
                focus_quality_score=0.0
            )
    
    def get_attention_context(self, context_type: str = "current") -> Dict[str, Any]:
        """
        Get current attention context for other primitives
        
        Primary interface for collaboration - provides rich attention
        signals that other primitives can use for enhancement.
        
        Args:
            context_type: Type of context to return
                - "current": Current focus and salience weights
                - "focused_entities": Detailed entity information
                - "trends": Attention trends and patterns
                - "full": Comprehensive attention state
                - "signals": Collaboration-specific signals
        """
        
        if context_type == "current":
            return self._get_current_context()
        elif context_type == "focused_entities":
            return self._get_focused_entities_context()
        elif context_type == "trends":
            return self._get_attention_trends_context()
        elif context_type == "full":
            return self._get_full_context()
        elif context_type == "signals":
            return self._get_collaboration_signals()
        else:
            logger.warning(f"Unknown context type: {context_type}")
            return self._get_current_context()
    
    def get_salience_scores(self, entities: Optional[List[str]] = None) -> Dict[str, float]:
        """
        Get salience scores for entities
        
        Args:
            entities: Specific entities to get scores for, or None for all
            
        Returns:
            Dictionary mapping entity_id to salience score
        """
        
        if entities is None:
            # Return all tracked entities
            return {
                entity_id: entity.salience_score 
                for entity_id, entity in self.state.tracked_entities.items()
                if entity.salience_score > 0.01  # Filter very low scores
            }
        else:
            # Return specific entities
            scores = {}
            for entity in entities:
                entity_id = entity.lower()
                if entity_id in self.state.tracked_entities:
                    scores[entity] = self.state.tracked_entities[entity_id].salience_score
                else:
                    scores[entity] = 0.0
            return scores
    
    # ========== COLLABORATION INTERFACES ==========
    
    def enable_collaboration_with(self, primitive_type: str, primitive_instance: Any):
        """Enable collaboration with another PACT primitive"""
        self.state.collaboration_enabled = True
        self.collaboration_interfaces[primitive_type] = primitive_instance
        
        if primitive_type not in self.state.primitive_partnerships:
            self.state.primitive_partnerships.append(primitive_type)
            
        logger.info(f"Enabled collaboration with {primitive_type}")
    
    def share_attention_signals(self) -> Dict[str, Any]:
        """
        Share attention signals with other primitives
        
        Primary collaboration interface - provides rich attention context
        that other primitives can use for their own processing.
        """
        
        try:
            current_entities = []
            focus_strength = 0.0
            focus_confidence = 0.0
            
            if self.state.current_focus:
                current_entities = self.state.current_focus.primary_entities
                focus_strength = self.state.current_focus.focus_strength
                focus_confidence = self.state.current_focus.focus_confidence
            
            # Get top salient entities
            top_entities = self.state.get_top_entities(10)
            
            # Calculate attention trends
            trends = self._calculate_attention_trends()
            
            return {
                "agent_id": self.agent_id,
                "current_focus_entities": current_entities,
                "focus_strength": focus_strength,
                "focus_confidence": focus_confidence,
                "focus_stability": self.state.focus_stability_score,
                "top_salient_entities": dict(top_entities),
                "attention_trends": trends,
                "focus_diversity": self.state.calculate_focus_diversity(),
                "entity_relationships": dict(list(self.state.entity_relationships.items())[:20]),
                "signal_timestamp": datetime.now(),
                "signal_confidence": min(focus_confidence + 0.2, 1.0),
                "collaboration_context": {
                    "total_interactions": self.state.total_interactions,
                    "adaptation_rate": self.state.adaptation_rate,
                    "user_alignment": self.state.user_alignment_score
                }
            }
            
        except Exception as e:
            logger.error(f"Error sharing attention signals: {str(e)}")
            return {
                "agent_id": self.agent_id,
                "current_focus_entities": [],
                "signal_confidence": 0.0,
                "error": str(e)
            }
    
    def receive_collaboration_signal(self, primitive_type: str, signal_data: Dict[str, Any]):
        """
        Process signals from other primitives
        
        Allows other primitives to influence attention processing
        through structured collaboration signals.
        """
        
        if not self.state.collaboration_enabled:
            logger.debug(f"Ignoring signal from {primitive_type} - collaboration disabled")
            return
        
        try:
            # Store signal with timestamp
            self.state.external_signals[primitive_type] = {
                "data": signal_data,
                "received_at": datetime.now(),
                "processed": False
            }
            
            # Process specific primitive signals
            if primitive_type == "memory":
                self._process_memory_signals(signal_data)
            elif primitive_type == "tone":
                self._process_tone_signals(signal_data)
            elif primitive_type == "values":
                self._process_value_signals(signal_data)
            else:
                logger.warning(f"Unknown primitive type for collaboration: {primitive_type}")
            
            # Mark as processed
            self.state.external_signals[primitive_type]["processed"] = True
            
            logger.debug(f"Processed collaboration signal from {primitive_type}")
            
        except Exception as e:
            logger.error(f"Error processing signal from {primitive_type}: {str(e)}")
    
    # ========== INTERNAL PROCESSING METHODS ==========
    
    def _process_entities(
        self, 
        entities: List[str], 
        context: str, 
        user_emphasis: Dict[str, float],
        explicit_focus: List[str],
        simulate: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Process and score entities for attention relevance
        
        Core entity processing pipeline that extracts, classifies,
        and scores entities for attention worthiness.
        """
        
        processed = []
        context_lower = context.lower()
        
        for entity in entities:
            # Skip if too short or common stopwords
            if (len(entity) < self.entity_extraction_min_length or 
                entity.lower() in self._get_stopwords()):
                continue
            
            entity_id = entity.lower()
            
            # Extract entity data
            entity_data = {
                "entity_id": entity_id,
                "entity_value": entity,
                "entity_type": self._classify_entity_type(entity),
                
                # Core scoring components
                "context_score": self._calculate_context_score(entity, context),
                "emphasis_score": user_emphasis.get(entity, 0.0),
                "frequency_score": self._calculate_frequency_score(entity, context),
                "novelty_score": self._calculate_novelty_score(entity_id, simulate),
                "position_score": self._calculate_position_score(entity, context),
                
                # Special signals
                "explicit_focus": entity in explicit_focus,
                "user_emphasized": entity in user_emphasis,
            }
            
            # Calculate composite attention score
            entity_data["attention_score"] = self._calculate_attention_score(entity_data)
            
            # Add metadata for learning
            entity_data["processing_timestamp"] = datetime.now()
            entity_data["context_length"] = len(context)
            
            processed.append(entity_data)
        
        # Sort by attention score
        processed.sort(key=lambda x: x["attention_score"], reverse=True)
        
        logger.debug(f"Processed {len(processed)} entities, top score: {processed[0]['attention_score'] if processed else 0:.3f}")
        
        return processed
    
    def _calculate_attention_score(self, entity_data: Dict[str, Any]) -> float:
        """Calculate composite attention score for entity"""
        
        # Base scoring weights
        weights = {
            "context_score": 0.30,
            "emphasis_score": 0.25,
            "frequency_score": 0.20,
            "novelty_score": 0.15,
            "position_score": 0.10,
        }
        
        # Calculate weighted sum
        base_score = sum(
            entity_data.get(score_type, 0.0) * weight
            for score_type, weight in weights.items()
        )
        
        # Apply bonuses for special signals
        bonus = 0.0
        
        if entity_data.get("explicit_focus", False):
            bonus += 0.3
            
        if entity_data.get("user_emphasized", False):
            bonus += 0.2
        
        # Apply novelty bonus if entity is very novel
        if entity_data.get("novelty_score", 0.0) > self.novelty_bonus_threshold:
            bonus += 0.15
        
        final_score = min(base_score + bonus, 1.0)
        
        return final_score
    
    def _calculate_context_score(self, entity: str, context: str) -> float:
        """Calculate importance of entity in current context"""
        
        entity_lower = entity.lower()
        context_lower = context.lower()
        
        if entity_lower not in context_lower:
            return 0.0
        
        score = 0.0
        
        # Position scoring (earlier mentions = more important)
        first_occurrence = context_lower.find(entity_lower)
        if first_occurrence != -1:
            position_score = 1.0 - (first_occurrence / max(len(context), 1))
            score += position_score * 0.3
        
        # Frequency scoring
        frequency = context_lower.count(entity_lower)
        frequency_score = min(frequency / 3.0, 1.0)
        score += frequency_score * 0.4
        
        # Emphasis markers
        emphasis_patterns = [
            f"'{entity}'", f'"{entity}"', f"*{entity}*", 
            entity.upper(), f"!{entity}", f"{entity}!"
        ]
        
        for pattern in emphasis_patterns:
            if pattern in context:
                score += 0.2
                break
        
        # Surrounding context importance
        importance_words = {"important", "key", "main", "primary", "focus", "remember", "note"}
        words_around = self._get_surrounding_words(entity, context, window=5)
        
        if any(word in importance_words for word in words_around):
            score += 0.1
        
        return min(score, 1.0)
    
    def _calculate_frequency_score(self, entity: str, context: str) -> float:
        """Calculate frequency-based importance"""
        mentions = context.lower().count(entity.lower())
        
        if mentions == 0:
            return 0.0
        elif mentions == 1:
            return 0.3
        else:
            # Logarithmic scaling to prevent over-weighting
            return min(0.3 + 0.7 * math.log(mentions) / math.log(5), 1.0)
    
    def _calculate_novelty_score(self, entity_id: str, simulate: bool = False) -> float:
        """Calculate novelty score for entity"""
        
        if simulate or entity_id not in self.state.tracked_entities:
            return 1.0  # Completely novel
        
        entity = self.state.tracked_entities[entity_id]
        
        # Base novelty decreases with mention count
        mention_novelty = 1.0 / (1.0 + math.log(entity.mention_count + 1))
        
        # Temporal novelty - more novel if not mentioned recently
        time_since_last = (datetime.now() - entity.last_mentioned).total_seconds()
        max_time = 7 * 24 * 3600  # 1 week
        temporal_novelty = min(time_since_last / max_time, 1.0)
        
        # Combine novelties
        combined_novelty = 0.6 * mention_novelty + 0.4 * temporal_novelty
        
        return min(combined_novelty, 1.0)
    
    def _calculate_position_score(self, entity: str, context: str) -> float:
        """Calculate importance based on position in context"""
        
        entity_lower = entity.lower()
        context_lower = context.lower()
        
        first_occurrence = context_lower.find(entity_lower)
        if first_occurrence == -1:
            return 0.0
        
        # Earlier positions get higher scores
        position_ratio = first_occurrence / len(context_lower)
        return 1.0 - position_ratio
    
    def _analyze_focus_shift_need(
        self, 
        processed_entities: List[Dict[str, Any]], 
        context: str,
        context_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze whether attention focus should shift
        
        Core decision-making logic for attention transitions.
        """
        
        analysis = {
            "should_shift": False,
            "shift_confidence": 0.0,
            "transition_type": "smooth",
            "primary_reason": "no_shift_needed",
            "stability_impact": 0.0,
            "prediction_confidence": 0.8
        }
        
        # No current focus = definitely shift
        if not self.state.current_focus:
            analysis.update({
                "should_shift": True,
                "shift_confidence": 1.0,
                "transition_type": "initial",
                "primary_reason": "no_current_focus"
            })
            return analysis
        
        current_primary = set(self.state.current_focus.primary_entities)
        new_primary_candidates = set(e["entity_id"] for e in processed_entities[:3])
        
        # Calculate focus overlap
        overlap = len(current_primary & new_primary_candidates)
        overlap_ratio = overlap / max(len(current_primary), 1)
        
        # Analyze attention scores
        max_new_attention = max([e["attention_score"] for e in processed_entities], default=0.0)
        current_focus_strength = self.state.current_focus.focus_strength
        current_focus_confidence = self.state.current_focus.focus_confidence
        
        # Check for explicit focus signals
        explicit_signals = self._detect_explicit_focus_signals(context)
        
        # Decision logic
        if explicit_signals["has_explicit_signal"]:
            # User explicitly directed attention
            analysis.update({
                "should_shift": True,
                "shift_confidence": 0.9,
                "transition_type": "triggered",
                "primary_reason": "explicit_user_signal"
            })
            
        elif overlap_ratio < 0.2 and max_new_attention > current_focus_strength + 0.3:
            # Completely different entities with high attention scores
            analysis.update({
                "should_shift": True,
                "shift_confidence": min(max_new_attention - current_focus_strength + 0.2, 1.0),
                "transition_type": "abrupt",
                "primary_reason": "high_attention_new_entities"
            })
            
        elif overlap_ratio < 0.5 and max_new_attention > current_focus_strength + 0.1:
            # Moderate overlap but significantly higher attention
            analysis.update({
                "should_shift": True,
                "shift_confidence": 0.6,
                "transition_type": "smooth",
                "primary_reason": "gradual_attention_shift"
            })
            
        elif current_focus_confidence < 0.3:
            # Current focus has very low confidence
            analysis.update({
                "should_shift": True,
                "shift_confidence": 0.7,
                "transition_type": "correction",
                "primary_reason": "low_confidence_current_focus"
            })
        
        # Calculate stability impact
        if analysis["should_shift"]:
            stability_impact = 1.0 - overlap_ratio
            analysis["stability_impact"] = stability_impact
        
        return analysis
    
    def _create_new_focus(
        self, 
        processed_entities: List[Dict[str, Any]], 
        context: str,
        shift_analysis: Dict[str, Any],
        context_type: Optional[str] = None
    ) -> AttentionFocus:
        """Create new attention focus from processed entities"""
        
        # Select entities for focus levels
        primary_count = min(self.state.config.max_concurrent_focus, len(processed_entities))
        primary_entities = [e["entity_id"] for e in processed_entities[:primary_count]]
        secondary_entities = [e["entity_id"] for e in processed_entities[primary_count:primary_count+3]]
        
        # Calculate focus metrics
        focus_strength = min(
            sum(e["attention_score"] for e in processed_entities[:primary_count]) / max(primary_count, 1),
            1.0
        )
        
        focus_confidence = shift_analysis["shift_confidence"]
        
        # Calculate stability based on transition type
        stability_mapping = {
            "initial": 0.5,
            "smooth": 0.8,
            "abrupt": 0.3,
            "triggered": 0.9,
            "correction": 0.4
        }
        focus_stability = stability_mapping.get(shift_analysis["transition_type"], 0.5)
        
        # Calculate clarity based on entity score distribution
        if len(processed_entities) >= 2:
            top_score = processed_entities[0]["attention_score"]
            second_score = processed_entities[1]["attention_score"]
            score_gap = top_score - second_score
            focus_clarity = min(score_gap + 0.3, 1.0)
        else:
            focus_clarity = 0.7
        
        # Determine scope and trigger
        scope = self._determine_focus_scope(processed_entities, context, context_type)
        trigger = self._determine_attention_trigger(shift_analysis)
        
        return AttentionFocus(
            scope=scope,
            primary_entities=primary_entities,
            secondary_entities=secondary_entities,
            focus_strength=focus_strength,
            focus_confidence=focus_confidence,
            focus_stability=focus_stability,
            focus_clarity=focus_clarity,
            trigger=trigger,
            trigger_confidence=shift_analysis.get("prediction_confidence", 0.8),
            context_summary=context[:self.context_window_size]
        )
    
    def _transition_focus(self, new_focus: AttentionFocus, transition_type: str) -> Dict[str, Any]:
        """Execute focus transition and record transition data"""
        
        # Create transition record
        transition = AttentionTransition(
            from_focus=self.state.current_focus.focus_id if self.state.current_focus else None,
            to_focus=new_focus.focus_id,
            transition_type=transition_type,
            transition_reason=f"Focus shift due to {new_focus.trigger.value}",
            transition_strength=new_focus.focus_strength,
            occurred_at=datetime.now()
        )
        
        # Calculate transition metrics
        if self.state.current_focus:
            # Calculate context overlap
            old_entities = set(self.state.current_focus.primary_entities)
            new_entities = set(new_focus.primary_entities)
            overlap = len(old_entities & new_entities)
            total = len(old_entities | new_entities)
            transition.context_overlap = overlap / max(total, 1)
            
            # Calculate smoothness
            if transition.context_overlap > 0.6:
                transition.transition_smoothness = 0.8
            elif transition.context_overlap > 0.3:
                transition.transition_smoothness = 0.5
            else:
                transition.transition_smoothness = 0.2
            
            # Close previous focus
            self.state.current_focus.actual_duration = (
                datetime.now() - self.state.current_focus.started_at
            ).total_seconds()
            
            # Store in history
            self.state.focus_history.append(self.state.current_focus)
            
            # Manage history size
            if len(self.state.focus_history) > self.state.config.max_focus_history:
                self.state.focus_history = self.state.focus_history[-self.state.config.max_focus_history:]
        
        # Set new focus
        self.state.current_focus = new_focus
        
        # Update focus stack
        self.state.focus_stack.append(new_focus)
        if len(self.state.focus_stack) > 10:
            self.state.focus_stack = self.state.focus_stack[-10:]
        
        # Record transition
        self.state.transition_history.append(transition)
        
        # Update counters
        self.state.total_focus_shifts += 1
        
        return {
            "transition_id": transition.transition_id,
            "transition_type": transition_type,
            "context_overlap": transition.context_overlap,
            "transition_smoothness": transition.transition_smoothness
        }
    
    def _update_current_focus(self, processed_entities: List[Dict[str, Any]], context: str):
        """Update current focus without shifting"""
        
        if not self.state.current_focus:
            return
        
        # Update focus strength based on new entities
        new_entity_scores = [e["attention_score"] for e in processed_entities[:3]]
        if new_entity_scores:
            avg_new_score = sum(new_entity_scores) / len(new_entity_scores)
            
            # Blend with current strength
            blend_weight = 0.3
            self.state.current_focus.focus_strength = (
                (1 - blend_weight) * self.state.current_focus.focus_strength +
                blend_weight * avg_new_score
            )
        
        # Update timestamp
        self.state.current_focus.last_updated = datetime.now()
    
    def _update_entity_tracking(self, entity_data: Dict[str, Any]) -> bool:
        """Update or create entity tracking. Returns True if new entity created."""
        
        entity_id = entity_data["entity_id"]
        current_time = datetime.now()
        
        if entity_id in self.state.tracked_entities:
            # Update existing entity
            entity = self.state.tracked_entities[entity_id]
            
            # Update salience using exponential moving average
            learning_rate = self.state.config.learning_rate
            entity.update_salience(entity_data["attention_score"], learning_rate)
            
            # Update temporal data
            entity.last_mentioned = current_time
            entity.mention_count += 1
            entity.updated_at = current_time
            
            return False
            
        else:
            # Create new entity
            entity = AttentionEntity(
                entity_id=entity_id,
                entity_type=EntityType(entity_data.get("entity_type", "unknown")),
                entity_value=entity_data["entity_value"],
                salience_score=entity_data["attention_score"],
                confidence_score=0.8,
                first_mentioned=current_time,
                last_mentioned=current_time,
                mention_count=1
            )
            
            self.state.tracked_entities[entity_id] = entity
            self.state.total_entities_tracked += 1
            
            # Manage entity capacity
            if len(self.state.tracked_entities) > self.state.config.max_tracked_entities:
                self._prune_low_salience_entities()
            
            return True
    
    def _apply_attention_decay(self):
        """Apply attention decay to all tracked entities"""
        
        current_time = datetime.now()
        
        # Only apply decay if enough time has passed
        time_since_last_decay = (current_time - self.state.last_decay_applied).total_seconds()
        if time_since_last_decay < self.state.decay_rules.decay_interval:
            return
        
        entities_to_remove = []
