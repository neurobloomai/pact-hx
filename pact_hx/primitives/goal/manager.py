# pact_hx/primitives/goal/manager.py
"""
PACT Goal Primitive Manager

The Goal Manager is responsible for understanding, tracking, aligning, and helping
achieve user goals within the PACT system. It serves as the intelligent coordinator
that ensures all AI assistance is purposeful and aligned with what users truly want
to accomplish.

Core Responsibilities:
- Goal Discovery: Identifying explicit and implicit user goals
- Goal Understanding: Clarifying ambiguous goals through intelligent questioning
- Goal Hierarchy: Managing relationships between goals and sub-goals
- Goal Tracking: Monitoring progress and updating goal status
- Goal Alignment: Ensuring goals align with user values and system capabilities
- Goal Conflict Resolution: Detecting and resolving conflicting goals
- Goal Achievement: Orchestrating resources to help users achieve their goals

Goal Philosophy:
Goals are the foundation of meaningful human-AI collaboration. Without understanding
what users want to achieve, AI assistance becomes reactive rather than proactive,
generic rather than personalized, and efficient rather than effective.

The Goal Manager operates on multiple time horizons:
- Immediate: Current task or question (seconds to minutes)
- Session: Goals for this interaction (minutes to hours)
- Project: Multi-session objectives (days to weeks)
- Long-term: Extended aspirations (weeks to months)

Integration Philosophy:
The Goal Manager works closely with other PACT primitives:
- Contextual Memory: Understanding goal context and history
- Empathetic Interaction: Surfacing goals through empathetic dialogue
- Value Alignment: Ensuring goals align with user values
- Adaptive Reasoning: Breaking down complex goals into achievable steps
- Trust Calibration: Building confidence in goal understanding
"""

import asyncio
import json
import logging
import time
from collections import defaultdict, deque
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Set, Tuple, Union
from dataclasses import asdict
import numpy as np

from .schemas import (
    GoalSchema, GoalType, GoalStatus, GoalPriority, GoalComplexity, GoalClarity,
    IntentConfidence, GoalOrigin, ConflictType, UserIntentSchema, UserPreferenceSchema,
    GoalHierarchySchema, GoalRelationshipSchema, GoalProgressEventSchema,
    GoalAchievementSchema, GoalConflictSchema, GoalAlignmentSchema,
    CreateGoalRequest, UpdateGoalRequest, GoalQueryRequest, GoalProgressRequest,
    GoalRecommendationRequest, create_simple_goal, create_goal_hierarchy,
    validate_goal_consistency, calculate_goal_health_score
)

logger = logging.getLogger(__name__)

class GoalDiscoveryEngine:
    """Discovers explicit and implicit goals from user interactions"""
    
    def __init__(self):
        self.intent_patterns = self._load_intent_patterns()
        self.goal_indicators = self._load_goal_indicators()
        self.context_analyzers = {}
        
    def _load_intent_patterns(self) -> Dict[str, List[str]]:
        """Load patterns that indicate different types of goals"""
        return {
            GoalType.IMMEDIATE: [
                "help me", "I need to", "how do I", "can you", "please",
                "I want to know", "explain", "show me", "what is"
            ],
            GoalType.LEARNING: [
                "learn about", "understand", "study", "master", "get better at",
                "improve my knowledge", "become proficient", "develop skills"
            ],
            GoalType.CREATIVE: [
                "create", "design", "write", "compose", "generate", "build",
                "make something", "come up with", "brainstorm", "invent"
            ],
            GoalType.ANALYTICAL: [
                "analyze", "evaluate", "assess", "compare", "investigate",
                "research", "examine", "review", "study the data"
            ],
            GoalType.PROBLEM_SOLVING: [
                "solve", "fix", "resolve", "troubleshoot", "debug", "overcome",
                "find a solution", "work around", "address the issue"
            ],
            GoalType.PROJECT: [
                "working on", "project", "long-term", "over time", "eventually",
                "my goal is", "I'm trying to", "planning to"
            ]
        }
    
    def _load_goal_indicators(self) -> Dict[str, float]:
        """Load indicators and their weights for goal detection"""
        return {
            "question_words": 0.8,  # who, what, when, where, why, how
            "action_verbs": 0.9,    # want, need, should, must, will
            "outcome_words": 0.7,   # result, achieve, complete, finish
            "time_references": 0.6, # today, tomorrow, this week, by Friday
            "priority_words": 0.8,  # urgent, important, critical, asap
            "emotional_words": 0.5, # frustrated, excited, worried, hopeful
        }
    
    async def discover_goals_from_message(self, message: str, context: Dict[str, Any]) -> List[GoalSchema]:
        """Discover goals from a user message"""
        discovered_goals = []
        
        # Analyze message for explicit goals
        explicit_goals = await self._extract_explicit_goals(message, context)
        discovered_goals.extend(explicit_goals)
        
        # Infer implicit goals from context and patterns
        implicit_goals = await self._infer_implicit_goals(message, context)
        discovered_goals.extend(implicit_goals)
        
        # Classify and prioritize discovered goals
        for goal in discovered_goals:
            await self._classify_goal(goal, message, context)
            await self._assess_goal_clarity(goal, message)
        
        return discovered_goals
    
    async def _extract_explicit_goals(self, message: str, context: Dict[str, Any]) -> List[GoalSchema]:
        """Extract explicitly stated goals from message"""
        explicit_goals = []
        message_lower = message.lower()
        
        # Look for direct goal statements
        goal_phrases = [
            "my goal is", "I want to", "I need to", "I'm trying to",
            "I hope to", "I plan to", "I aim to", "help me"
        ]
        
        for phrase in goal_phrases:
            if phrase in message_lower:
                # Extract the goal description after the phrase
                start_idx = message_lower.find(phrase)
                goal_text = message[start_idx + len(phrase):].strip()
                
                # Clean up the goal text
                goal_text = self._clean_goal_text(goal_text)
                
                if goal_text:
                    goal_type = await self._determine_goal_type(goal_text)
                    
                    goal = create_simple_goal(
                        title=self._generate_goal_title(goal_text),
                        description=goal_text,
                        goal_type=goal_type,
                        origin=GoalOrigin.EXPLICIT_USER_STATEMENT,
                        intent_confidence=IntentConfidence.HIGH,
                        clarity=GoalClarity.CLEAR,
                        context={"user_message": message, "session_context": context}
                    )
                    
                    explicit_goals.append(goal)
        
        return explicit_goals
    
    async def _infer_implicit_goals(self, message: str, context: Dict[str, Any]) -> List[GoalSchema]:
        """Infer implicit goals from message patterns and context"""
        implicit_goals = []
        message_lower = message.lower()
        
        # Analyze question patterns
        if any(q in message_lower for q in ["how", "what", "why", "when", "where"]):
            goal = create_simple_goal(
                title="Learn/Understand Information",
                description=f"Understand information related to: {message[:100]}...",
                goal_type=GoalType.LEARNING,
                origin=GoalOrigin.INFERRED_FROM_CONTEXT,
                intent_confidence=IntentConfidence.MEDIUM,
                clarity=GoalClarity.SOMEWHAT_CLEAR,
                priority=GoalPriority.MEDIUM
            )
            implicit_goals.append(goal)
        
        # Analyze problem-solving patterns
        problem_indicators = ["error", "issue", "problem", "not working", "broken", "stuck"]
        if any(indicator in message_lower for indicator in problem_indicators):
            goal = create_simple_goal(
                title="Resolve Problem/Issue",
                description=f"Solve problem mentioned in: {message[:100]}...",
                goal_type=GoalType.PROBLEM_SOLVING,
                origin=GoalOrigin.INFERRED_FROM_CONTEXT,
                intent_confidence=IntentConfidence.MEDIUM,
                clarity=GoalClarity.AMBIGUOUS,
                priority=GoalPriority.HIGH
            )
            implicit_goals.append(goal)
        
        # Analyze creation patterns
        creation_indicators = ["create", "make", "build", "design", "write", "generate"]
        if any(indicator in message_lower for indicator in creation_indicators):
            goal = create_simple_goal(
                title="Create Something",
                description=f"Create/build something related to: {message[:100]}...",
                goal_type=GoalType.CREATIVE,
                origin=GoalOrigin.INFERRED_FROM_CONTEXT,
                intent_confidence=IntentConfidence.MEDIUM,
                clarity=GoalClarity.SOMEWHAT_CLEAR,
                priority=GoalPriority.MEDIUM
            )
            implicit_goals.append(goal)
        
        return implicit_goals
    
    async def _determine_goal_type(self, goal_text: str) -> GoalType:
        """Determine the most likely goal type from goal text"""
        text_lower = goal_text.lower()
        scores = defaultdict(float)
        
        # Score against each goal type's patterns
        for goal_type, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if pattern in text_lower:
                    scores[goal_type] += 1.0 / len(patterns)  # Normalized score
        
        # Return the highest scoring type, or IMMEDIATE as default
        if scores:
            return max(scores.keys(), key=lambda k: scores[k])
        return GoalType.IMMEDIATE
    
    def _clean_goal_text(self, text: str) -> str:
        """Clean and normalize goal text"""
        # Remove extra whitespace
        text = " ".join(text.split())
        
        # Remove trailing punctuation that might break sentences
        text = text.rstrip(".,!?;:")
        
        # Ensure reasonable length
        if len(text) > 500:
            text = text[:500] + "..."
        
        return text
    
    def _generate_goal_title(self, description: str) -> str:
        """Generate a concise title from goal description"""
        words = description.split()
        if len(words) <= 8:
            return description
        
        # Take first 6 words and add ellipsis
        return " ".join(words[:6]) + "..."
    
    async def _classify_goal(self, goal: GoalSchema, message: str, context: Dict[str, Any]):
        """Classify goal complexity, priority, etc."""
        message_lower = message.lower()
        
        # Assess priority from urgency indicators
        if any(urgent in message_lower for urgent in ["urgent", "asap", "immediately", "critical"]):
            goal.priority = GoalPriority.CRITICAL
        elif any(high in message_lower for high in ["important", "soon", "quickly", "need"]):
            goal.priority = GoalPriority.HIGH
        elif any(low in message_lower for low in ["eventually", "sometime", "when possible"]):
            goal.priority = GoalPriority.LOW
        
        # Assess complexity from message length and vocabulary
        complexity_score = len(message.split()) / 50.0  # Rough heuristic
        if complexity_score > 1.0:
            goal.complexity = GoalComplexity.COMPLEX
        elif complexity_score > 0.5:
            goal.complexity = GoalComplexity.MODERATE
        else:
            goal.complexity = GoalComplexity.SIMPLE
    
    async def _assess_goal_clarity(self, goal: GoalSchema, message: str):
        """Assess how clearly the goal is defined"""
        message_lower = message.lower()
        
        # Count clarity indicators
        vague_indicators = ["maybe", "might", "perhaps", "not sure", "unclear", "don't know"]
        clear_indicators = ["specifically", "exactly", "precisely", "clearly", "definitely"]
        
        vague_count = sum(1 for indicator in vague_indicators if indicator in message_lower)
        clear_count = sum(1 for indicator in clear_indicators if indicator in message_lower)
        
        if clear_count > vague_count:
            goal.clarity = GoalClarity.CLEAR
        elif vague_count > clear_count:
            goal.clarity = GoalClarity.AMBIGUOUS
        
        # Adjust intent confidence based on clarity
        if goal.clarity == GoalClarity.AMBIGUOUS:
            if goal.intent_confidence == IntentConfidence.HIGH:
                goal.intent_confidence = IntentConfidence.MEDIUM

class GoalTracker:
    """Tracks goal progress and maintains goal state"""
    
    def __init__(self):
        self.active_goals: Dict[str, GoalSchema] = {}
        self.goal_history: Dict[str, List[GoalProgressEventSchema]] = defaultdict(list)
        self.achievements: Dict[str, GoalAchievementSchema] = {}
        
    async def add_goal(self, goal: GoalSchema) -> str:
        """Add a new goal to tracking"""
        self.active_goals[goal.goal_id] = goal
        
        # Create initial progress event
        initial_event = GoalProgressEventSchema(
            goal_id=goal.goal_id,
            event_type="goal_created",
            previous_progress=0.0,
            new_progress=goal.progress_percentage,
            progress_delta=goal.progress_percentage,
            description=f"Goal created: {goal.title}",
            event_timestamp=datetime.now()
        )
        
        self.goal_history[goal.goal_id].append(initial_event)
        
        logger.info(f"Added goal to tracking: {goal.title} ({goal.goal_id})")
        return goal.goal_id
    
    async def update_goal_progress(self, goal_id: str, progress_request: GoalProgressRequest) -> bool:
        """Update progress on a tracked goal"""
        if goal_id not in self.active_goals:
            logger.warning(f"Goal {goal_id} not found for progress update")
            return False
        
        goal = self.active_goals[goal_id]
        previous_progress = goal.progress_percentage
        
        # Update goal progress
        goal.progress_percentage = progress_request.progress_percentage
        
        # Update status based on progress
        if progress_request.progress_percentage >= 100.0:
            goal.status = GoalStatus.COMPLETED
            goal.actual_completion = datetime.now()
        elif progress_request.progress_percentage > 0 and goal.status == GoalStatus.NOT_STARTED:
            goal.status = GoalStatus.IN_PROGRESS
            goal.start_time = datetime.now()
        elif progress_request.progress_percentage > 0:
            goal.status = GoalStatus.IN_PROGRESS
        
        # Create progress event
        progress_event = GoalProgressEventSchema(
            goal_id=goal_id,
            event_type="progress_update",
            previous_progress=previous_progress,
            new_progress=progress_request.progress_percentage,
            progress_delta=progress_request.progress_percentage - previous_progress,
            description=progress_request.description,
            updated_metrics=progress_request.updated_metrics or [],
            user_action=progress_request.user_action,
            event_timestamp=datetime.now()
        )
        
        self.goal_history[goal_id].append(progress_event)
        
        # Check if goal is completed
        if goal.status == GoalStatus.COMPLETED:
            await self._mark_goal_completed(goal)
        
        logger.info(f"Updated goal progress: {goal.title} -> {progress_request.progress_percentage}%")
        return True
    
    async def _mark_goal_completed(self, goal: GoalSchema):
        """Mark a goal as completed and create achievement record"""
        completion_time = goal.actual_completion or datetime.now()
        start_time = goal.start_time or goal.created_at
        duration = completion_time - start_time
        
        # Create achievement record
        achievement = GoalAchievementSchema(
            goal_id=goal.goal_id,
            completion_time=completion_time,
            total_duration=duration,
            final_progress=goal.progress_percentage,
            overall_success_score=1.0,
            user_satisfaction=0.8,
            quality_score=1.0,
            efficiency_score=self._calculate_efficiency_score(goal, duration),
            what_worked_well=["Goal completed successfully"],
            insights_gained=[f"Completed {goal.goal_type.value} goal in {duration}"]
        )
        
        self.achievements[goal.goal_id] = achievement
        
        # Move from active to completed
        if goal.goal_id in self.active_goals:
            del self.active_goals[goal.goal_id]
        
        logger.info(f"Goal completed: {goal.title}")
    
    def _calculate_efficiency_score(self, goal: GoalSchema, actual_duration: timedelta) -> float:
        """Calculate efficiency score based on estimated vs actual duration"""
        if not goal.estimated_duration:
            return 1.0
        
        ratio = goal.estimated_duration.total_seconds() / actual_duration.total_seconds()
        
        if ratio >= 1.0:
            return min(1.0, ratio / 2.0 + 0.5)
        else:
            return max(0.0, ratio)
    
    async def get_goal(self, goal_id: str) -> Optional[GoalSchema]:
        """Get a goal by ID"""
        return self.active_goals.get(goal_id)
    
    async def get_goals_by_criteria(self, query: GoalQueryRequest) -> List[GoalSchema]:
        """Get goals matching specified criteria"""
        matching_goals = []
        
        for goal in self.active_goals.values():
            if self._goal_matches_criteria(goal, query):
                matching_goals.append(goal)
        
        # Sort by priority and creation time
        matching_goals.sort(key=lambda g: (g.priority.value, g.created_at))
        
        return matching_goals[:query.limit]
    
    def _goal_matches_criteria(self, goal: GoalSchema, query: GoalQueryRequest) -> bool:
        """Check if goal matches query criteria"""
        if query.user_id and goal.user_id != query.user_id:
            return False
        
        if query.session_id and goal.session_id != query.session_id:
            return False
        
        if query.goal_type and goal.goal_type != query.goal_type:
            return False
        
        if query.status and goal.status != query.status:
            return False
        
        if query.priority and goal.priority != query.priority:
            return False
        
        if not query.include_completed and goal.status == GoalStatus.COMPLETED:
            return False
        
        if query.tags:
            if not any(tag in goal.tags for tag in query.tags):
                return False
        
        return True
    
    async def get_goal_progress_history(self, goal_id: str) -> List[GoalProgressEventSchema]:
        """Get progress history for a goal"""
        return self.goal_history.get(goal_id, [])

class GoalAlignmentEngine:
    """Ensures goals align with user values and system capabilities"""
    
    def __init__(self):
        self.alignment_cache: Dict[str, GoalAlignmentSchema] = {}
        self.user_preferences: Dict[str, UserPreferenceSchema] = {}
        
    async def assess_goal_alignment(self, goal: GoalSchema, user_context: Dict[str, Any]) -> GoalAlignmentSchema:
        """Assess how well a goal aligns with user values and system capabilities"""
        
        # Check cache first
        cache_key = f"{goal.goal_id}_{hash(str(user_context))}"
        if cache_key in self.alignment_cache:
            return self.alignment_cache[cache_key]
        
        # Assess different alignment dimensions
        user_value_alignment = await self._assess_user_value_alignment(goal, user_context)
        capability_alignment = await self._assess_system_capability_alignment(goal)
        context_alignment = await self._assess_context_alignment(goal, user_context)
        resource_alignment = await self._assess_resource_alignment(goal)
        
        # Calculate overall alignment
        overall_alignment = np.mean([
            user_value_alignment,
            capability_alignment, 
            context_alignment,
            resource_alignment
        ])
        
        # Create alignment assessment
        alignment = GoalAlignmentSchema(
            primary_goal_id=goal.goal_id,
            user_value_alignment=user_value_alignment,
            system_capability_alignment=capability_alignment,
            context_alignment=context_alignment,
            resource_alignment=resource_alignment,
            overall_alignment_score=overall_alignment,
            alignment_confidence=0.8,
            supporting_factors=await self._identify_supporting_factors(goal, user_context),
            misalignment_factors=await self._identify_misalignment_factors(goal, user_context),
            alignment_recommendations=await self._generate_alignment_recommendations(goal, overall_alignment)
        )
        
        self.alignment_cache[cache_key] = alignment
        return alignment
    
    async def _assess_user_value_alignment(self, goal: GoalSchema, user_context: Dict[str, Any]) -> float:
        """Assess alignment with user values"""
        alignment_score = 0.8
        
        # Check for ethical concerns
        ethical_flags = ["harm", "illegal", "unethical", "dangerous"]
        if any(flag in goal.description.lower() for flag in ethical_flags):
            alignment_score *= 0.3
        
        # Boost score for learning and creative goals
        if goal.goal_type in [GoalType.LEARNING, GoalType.CREATIVE]:
            alignment_score *= 1.1
        
        return min(1.0, alignment_score)
    
    async def _assess_system_capability_alignment(self, goal: GoalSchema) -> float:
        """Assess alignment with system capabilities"""
        capability_scores = {
            GoalType.IMMEDIATE: 0.9,
            GoalType.LEARNING: 0.8,
            GoalType.ANALYTICAL: 0.85,
            GoalType.CREATIVE: 0.7,
            GoalType.PROBLEM_SOLVING: 0.8,
            GoalType.EXPLORATORY: 0.75,
            GoalType.COLLABORATIVE: 0.85,
            GoalType.SESSION: 0.9,
            GoalType.PROJECT: 0.6,
            GoalType.LONG_TERM: 0.4
        }
        
        base_score = capability_scores.get(goal.goal_type, 0.5)
        
        # Adjust based on goal complexity
        if goal.complexity == GoalComplexity.VERY_COMPLEX:
            base_score *= 0.7
        elif goal.complexity == GoalComplexity.COMPLEX:
            base_score *= 0.85
        elif goal.complexity == GoalComplexity.SIMPLE:
            base_score *= 1.1
        
        return base_score
    
    async def _assess_context_alignment(self, goal: GoalSchema, user_context: Dict[str, Any]) -> float:
        """Assess alignment with current context"""
        alignment_score = 0.8
        
        # Check time alignment
        current_hour = datetime.now().hour
        if goal.goal_type == GoalType.LEARNING and 6 <= current_hour <= 22:
            alignment_score *= 1.1
        elif goal.goal_type == GoalType.CREATIVE and (8 <= current_hour <= 11 or 14 <= current_hour <= 17):
            alignment_score *= 1.1
        
        return min(1.0, alignment_score)
    
    async def _assess_resource_alignment(self, goal: GoalSchema) -> float:
        """Assess alignment with available resources"""
        base_alignment = 0.8
        
        if goal.complexity == GoalComplexity.VERY_COMPLEX:
            base_alignment *= 0.6
        elif goal.complexity == GoalComplexity.COMPLEX:
            base_alignment *= 0.8
        
        return base_alignment
    
    async def _identify_supporting_factors(self, goal: GoalSchema, user_context: Dict[str, Any]) -> List[str]:
        """Identify factors that support goal alignment"""
        factors = []
        
        if goal.clarity in [GoalClarity.CLEAR, GoalClarity.CRYSTAL_CLEAR]:
            factors.append("Goal is clearly defined")
        
        if goal.intent_confidence in [IntentConfidence.HIGH, IntentConfidence.VERY_HIGH]:
            factors.append("High confidence in understanding user intent")
        
        if goal.goal_type in [GoalType.LEARNING, GoalType.ANALYTICAL]:
            factors.append("Goal type aligns well with system strengths")
        
        return factors
    
    async def _identify_misalignment_factors(self, goal: GoalSchema, user_context: Dict[str, Any]) -> List[str]:
        """Identify factors that create misalignment"""
        factors = []
        
        if goal.clarity == GoalClarity.VERY_AMBIGUOUS:
            factors.append("Goal is very ambiguously defined")
        
        if goal.intent_confidence == IntentConfidence.VERY_LOW:
            factors.append("Low confidence in understanding user intent")
        
        if goal.complexity == GoalComplexity.VERY_COMPLEX:
            factors.append("Goal complexity may exceed system capabilities")
        
        return factors
    
    async def _generate_alignment_recommendations(self, goal: GoalSchema, alignment_score: float) -> List[str]:
        """Generate recommendations to improve alignment"""
        recommendations = []
        
        if alignment_score < 0.5:
            recommendations.append("Consider breaking down this goal into smaller, more manageable sub-goals")
            recommendations.append("Clarify the goal requirements and success criteria")
        
        if goal.clarity in [GoalClarity.AMBIGUOUS, GoalClarity.VERY_AMBIGUOUS]:
            recommendations.append("Ask clarifying questions to better understand the goal")
        
        return recommendations

class GoalConflictResolver:
    """Detects and resolves conflicts between goals"""
    
    def __init__(self):
        self.detected_conflicts: Dict[str, GoalConflictSchema] = {}
        
    async def detect_conflicts(self, goals: List[GoalSchema]) -> List[GoalConflictSchema]:
        """Detect conflicts between a set of goals"""
        conflicts = []
        
        # Check all pairs of goals for conflicts
        for i, goal_a in enumerate(goals):
            for goal_b in goals[i+1:]:
                conflict = await self._analyze_goal_pair(goal_a, goal_b)
                if conflict:
                    conflicts.append(conflict)
                    self.detected_conflicts[conflict.conflict_id] = conflict
        
        return conflicts
    
    async def _analyze_goal_pair(self, goal_a: GoalSchema, goal_b: GoalSchema) -> Optional[GoalConflictSchema]:
        """Analyze two goals for potential conflicts"""
        
        # Check for time conflicts
        time_conflict = await self._check_time_conflict(goal_a, goal_b)
        if time_conflict:
            return time_conflict
        
        # Check for priority conflicts
        priority_conflict = await self._check_priority_conflict(goal_a, goal_b)
        if priority_conflict:
            return priority_conflict
        
        return None
    
    async def _check_time_conflict(self, goal_a: GoalSchema, goal_b: GoalSchema) -> Optional[GoalConflictSchema]:
        """Check for time-based conflicts between goals"""
        if not (goal_a.target_completion and goal_b.target_completion):
            return None
        
        if (goal_a.priority in [GoalPriority.CRITICAL, GoalPriority.HIGH] and 
            goal_b.priority in [GoalPriority.CRITICAL, GoalPriority.HIGH]):
            
            time_diff = abs((goal_a.target_completion - goal_b.target_completion).total_seconds())
            
            if time_diff < 3600:  # Within 1 hour
                return GoalConflictSchema(
                    conflicting_goal_ids=[goal_a.goal_id, goal_b.goal_id],
                    conflict_type=ConflictType.TIME_CONFLICT,
                    severity=0.8,
                    description=f"Goals '{goal_a.title}' and '{goal_b.title}' have conflicting time requirements",
                    potential_impact="Both goals may not be achievable within the specified timeframes",
                    resolution_strategy="Prioritize goals or adjust timelines"
                )
        
        return None
    
    async def _check_priority_conflict(self, goal_a: GoalSchema, goal_b: GoalSchema) -> Optional[GoalConflictSchema]:
        """Check for priority-based conflicts"""
        if (goal_a.priority == GoalPriority.CRITICAL and 
            goal_b.priority == GoalPriority.CRITICAL and
            goal_a.goal_type == goal_b.goal_type):
            
            return GoalConflictSchema(
                conflicting_goal_ids=[goal_a.goal_id, goal_b.goal_id],
                conflict_type=ConflictType.PRIORITY_CONFLICT,
                severity=0.7,
                description=f"Multiple critical goals of same type: '{goal_a.title}' and '{goal_b.title}'",
                potential_impact="User attention may be divided, reducing effectiveness",
                resolution_strategy="Sequence goals or merge if possible"
            )
        
        return None

class GoalRecommendationEngine:
    """Provides intelligent goal recommendations and suggestions"""
    
    def __init__(self):
        self.recommendation_models = {}
        self.goal_patterns = defaultdict(list)
        
    async def recommend_next_actions(self, goal: GoalSchema, context: Dict[str, Any]) -> List[str]:
        """Recommend next actions for achieving a goal"""
        recommendations = []
        
        # Base recommendations on goal type
        if goal.goal_type == GoalType.LEARNING:
            recommendations.extend([
                "Break down the learning topic into key concepts",
                "Identify prerequisite knowledge needed",
                "Find reliable learning resources",
                "Set up a learning schedule"
            ])
        elif goal.goal_type == GoalType.CREATIVE:
            recommendations.extend([
                "Brainstorm initial ideas and concepts",
                "Research inspiration and examples",
                "Create a rough outline or prototype",
                "Gather necessary tools and materials"
            ])
        elif goal.goal_type == GoalType.PROBLEM_SOLVING:
            recommendations.extend([
                "Clearly define the problem",
                "Gather relevant information",
                "Identify potential solutions",
                "Evaluate pros and cons of each solution"
            ])
