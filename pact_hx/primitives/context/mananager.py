# pact_hx/primitives/context/manager.py
"""
PACT Context Manager - Complete Core Logic Implementation

The Context Manager provides situation-aware ethical reasoning and serves as the 
situational intelligence hub of PACT, providing rich contextual awareness that 
makes all other primitives smarter and more adaptive.

Complete Implementation Features:
- Multi-dimensional context analysis (environmental, social, temporal, emotional, etc.)
- Real-time context tracking and change detection
- Pattern recognition and learning from contextual data
- Context-aware recommendations for all primitives
- Adaptive context collection based on relevance and importance
- Cross-primitive context intelligence sharing
- Contextual anomaly detection and insight generation

Integration Points:
- Feeds contextual intelligence to Goal Manager for smarter objective setting
- Provides situational awareness to Value Alignment for nuanced ethical reasoning
- Informs Attention Manager about contextually relevant focus areas
- Guides Memory Manager on contextually appropriate recall and storage
"""

from typing import Dict, Any, List, Optional, Set, Tuple, Union, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum
import time
import uuid
import json
import logging
import asyncio
import threading
from datetime import datetime, timedelta
from collections import defaultdict, deque
import statistics

# Import our comprehensive schemas
from .schemas import (
    def _calculate_context_quality(self, factors: List[ContextFactor]) -> float:
        """Calculate overall context quality score"""
        if not factors:
            return 0.0
        
        # Quality based on number of factors, confidence, and coverage
        factor_count_score = min(len(factors) / 10, 1.0)  # Normalize to max 10 factors
        confidence_score = sum(f.confidence for f in factors) / len(factors)
        
        # Coverage score - how many context types we have
        context_types_covered = len(set(f.type for f in factors))
        coverage_score = context_types_covered / len(ContextType)
        
        # Combined quality score
        quality = (factor_count_score * 0.3 + confidence_score * 0.4 + coverage_score * 0.3)
        return min(quality, 1.0)
    
    def _calculate_average_confidence(self, factors: List[ContextFactor]) -> float:
        """Calculate average confidence across all factors"""
        if not factors:
            return 0.0
        return sum(f.confidence for f in factors) / len(factors)
    
    def _calculate_context_stability(self, factors: List[ContextFactor]) -> float:
        """Calculate context stability based on change frequency"""
        if not factors:
            return 0.0
        
        stability_scores = []
        for factor in factors:
            if factor.change_frequency == "stable":
                stability_scores.append(1.0)
            elif factor.change_frequency == "slow":
                stability_scores.append(0.8)
            elif factor.change_frequency == "moderate":
                stability_scores.append(0.6)
            elif factor.change_frequency == "fast":
                stability_scores.append(0.4)
            else:  # volatile
                stability_scores.append(0.2)
        
        return sum(stability_scores) / len(stability_scores)
    
    def _calculate_context_complexity(self, factors: List[ContextFactor]) -> float:
        """Calculate context complexity based on number and relationships"""
        if not factors:
            return 0.0
        
        # Base complexity from number of factors
        base_complexity = min(len(factors) / 15, 1.0)
        
        # Relationship complexity
        total_relationships = sum(len(f.related_factors) + len(f.dependency_factors) for f in factors)
        relationship_complexity = min(total_relationships / (len(factors) * 3), 1.0)
        
        # Priority spread complexity
        priority_counts = defaultdict(int)
        for factor in factors:
            priority_counts[factor.priority] += 1
        priority_spread = len(priority_counts) / len(ContextPriority)
        
        complexity = (base_complexity * 0.4 + relationship_complexity * 0.4 + priority_spread * 0.2)
        return min(complexity, 1.0)
    
    def _identify_dominant_types(self, factors: List[ContextFactor]) -> List[ContextType]:
        """Identify the dominant context types"""
        type_counts = defaultdict(int)
        type_importance = defaultdict(float)
        
        for factor in factors:
            type_counts[factor.type] += 1
            # Weight by priority
            priority_weights = {
                ContextPriority.CRITICAL: 2.0,
                ContextPriority.HIGH: 1.5,
                ContextPriority.MEDIUM: 1.0,
                ContextPriority.LOW: 0.5,
                ContextPriority.IGNORE: 0.0
            }
            type_importance[factor.type] += priority_weights.get(factor.priority, 1.0)
        
        # Sort by importance
        sorted_types = sorted(type_importance.items(), key=lambda x: x[1], reverse=True)
        
        # Return top 3 types
        return [ctx_type for ctx_type, _ in sorted_types[:3]]
    
    def _generate_situation_summary(self, snapshot: ContextSnapshot) -> str:
        """Generate a human-readable situation summary"""
        summary_parts = []
        
        # Time context
        if snapshot.temporal.current_time_context:
            summary_parts.append(f"{snapshot.temporal.current_time_context} session")
        
        # Location and device
        if snapshot.environmental.location_type and snapshot.environmental.device_type:
            summary_parts.append(f"at {snapshot.environmental.location_type} using {snapshot.environmental.device_type}")
        
        # Social context
        if snapshot.social.interaction_mode:
            summary_parts.append(f"in {snapshot.social.interaction_mode} mode")
        
        # Task context
        if snapshot.task.primary_task_type:
            summary_parts.append(f"working on {snapshot.task.primary_task_type} tasks")
        
        # Emotional state
        if snapshot.emotional.primary_mood:
            summary_parts.append(f"feeling {snapshot.emotional.primary_mood}")
        
        # Stress/pressure indicators
        if snapshot.emotional.stress_level in ["high", "overwhelming"]:
            summary_parts.append(f"with {snapshot.emotional.stress_level} stress")
        elif snapshot.temporal.time_pressure_level in ["urgent", "high"]:
            summary_parts.append(f"under {snapshot.temporal.time_pressure_level} time pressure")
        
        return ", ".join(summary_parts) if summary_parts else "Context analysis in progress"
    
    def get_context_history(self, lookback_hours: int = 24) -> List[ContextSnapshot]:
        """Retrieve historical context snapshots"""
        cutoff_time = time.time() - (lookback_hours * 3600)
        return [
            snapshot for snapshot in self.context_history 
            if snapshot.timestamp >= cutoff_time
        ]


class ContextBridge:
    """Shares contextual intelligence across primitives"""
    
    def __init__(self):
        self.bridge_history: List[Dict[str, Any]] = []
        self.primitive_subscriptions: Dict[str, List[str]] = {}
        self.context_cache: Dict[str, Any] = {}
        
        logger.info("ContextBridge initialized")
    
    def provide_goal_context(self, current_context: ContextSnapshot) -> Dict[str, Any]:
        """Provide contextual intelligence for goal setting"""
        try:
            goal_context = {
                "goal_setting_recommendations": [],
                "timing_guidance": {},
                "priority_suggestions": {},
                "approach_recommendations": {},
                "context_constraints": []
            }
            
            # Timing guidance based on temporal context
            if current_context.temporal.energy_cycle_phase == "peak":
                goal_context["timing_guidance"]["energy"] = "optimal_for_challenging_goals"
                goal_context["goal_setting_recommendations"].append(
                    "High energy detected - good time for ambitious goal setting"
                )
            elif current_context.temporal.energy_cycle_phase == "low":
                goal_context["timing_guidance"]["energy"] = "focus_on_simple_goals"
                goal_context["goal_setting_recommendations"].append(
                    "Low energy phase - consider smaller, achievable goals"
                )
            
            # Task complexity guidance
            if current_context.cognitive.cognitive_load == "overloaded":
                goal_context["approach_recommendations"]["complexity"] = "simplify_goals"
                goal_context["goal_setting_recommendations"].append(
                    "High cognitive load - break down goals into smaller steps"
                )
            
            # Time pressure considerations
            if current_context.temporal.time_pressure_level in ["urgent", "high"]:
                goal_context["priority_suggestions"]["urgency"] = "focus_on_immediate_goals"
                goal_context["goal_setting_recommendations"].append(
                    "Time pressure detected - prioritize immediate, actionable goals"
                )
            
            # Social context considerations
            if current_context.social.interaction_mode in ["small_group", "large_group"]:
                goal_context["approach_recommendations"]["social"] = "collaborative_goals"
                goal_context["goal_setting_recommendations"].append(
                    "Group context - consider collaborative or shared goals"
                )
            
            # Emotional state considerations
            if current_context.emotional.motivation_level == "very_high":
                goal_context["approach_recommendations"]["motivation"] = "leverage_high_motivation"
                goal_context["goal_setting_recommendations"].append(
                    "High motivation - excellent opportunity for stretch goals"
                )
            elif current_context.emotional.stress_level in ["high", "overwhelming"]:
                goal_context["context_constraints"].append("avoid_additional_pressure")
                goal_context["goal_setting_recommendations"].append(
                    "High stress detected - avoid adding pressure with demanding goals"
                )
            
            return goal_context
            
        except Exception as e:
            logger.error(f"Error providing goal context: {e}")
            return {"error": str(e)}
    
    def provide_attention_context(self, current_context: ContextSnapshot) -> Dict[str, Any]:
        """Provide contextual intelligence for attention management"""
        try:
            attention_context = {
                "focus_recommendations": [],
                "distraction_warnings": [],
                "attention_strategies": {},
                "optimal_focus_areas": [],
                "context_based_adjustments": []
            }
            
            # Cognitive load considerations
            if current_context.cognitive.cognitive_load == "overloaded":
                attention_context["focus_recommendations"].append("reduce_cognitive_load")
                attention_context["attention_strategies"]["load_management"] = "simplify_tasks"
                attention_context["context_based_adjustments"].append(
                    "High cognitive load - break tasks into smaller, manageable pieces"
                )
            
            # Environmental distractions
            if current_context.environmental.noise_level in ["noisy", "very_noisy"]:
                attention_context["distraction_warnings"].append("high_noise_environment")
                attention_context["attention_strategies"]["noise"] = "focus_enhancement_needed"
                attention_context["context_based_adjustments"].append(
                    "Noisy environment - recommend noise-canceling or focus techniques"
                )
            
            # Time-based attention optimization
            if current_context.temporal.current_time_context == "morning":
                attention_context["optimal_focus_areas"].append("analytical_tasks")
                attention_context["attention_strategies"]["timing"] = "leverage_morning_clarity"
                attention_context["context_based_adjustments"].append(
                    "Morning context - optimal for focused, analytical work"
                )
            
            return attention_context
            
        except Exception as e:
            logger.error(f"Error providing attention context: {e}")
            return {"error": str(e)}


class ContextAdaptor:
    """Adapts behavior based on contextual changes"""
    
    def __init__(self):
        self.adaptation_history: List[Dict[str, Any]] = []
        self.adaptation_strategies: Dict[str, Callable] = {}
        
        logger.info("ContextAdaptor initialized")
    
    def adapt_to_context(self, context_snapshot: ContextSnapshot) -> List[ContextualRecommendation]:
        """Generate behavior adaptations based on context"""
        try:
            recommendations = []
            
            # Cognitive load adaptations
            if context_snapshot.cognitive.cognitive_load == "overloaded":
                rec = create_contextual_recommendation(
                    target_primitive="all",
                    title="Reduce Cognitive Complexity",
                    description="High cognitive load detected - simplify interactions and break down complex tasks",
                    recommendation_type="adaptation",
                    priority=ContextPriority.HIGH,
                    specific_actions=[
                        "Break complex tasks into smaller steps",
                        "Reduce information density in responses",
                        "Provide clear, simple guidance",
                        "Avoid introducing new concepts"
                    ],
                    expected_benefits=["Reduced mental strain", "Better task completion", "Improved user experience"],
                    confidence=0.8
                )
                recommendations.append(rec)
            
            # Time pressure adaptations
            if context_snapshot.temporal.time_pressure_level in ["urgent", "high"]:
                rec = create_contextual_recommendation(
                    target_primitive="all",
                    title="Optimize for Time Efficiency",
                    description="Time pressure detected - prioritize speed and efficiency",
                    recommendation_type="timing",
                    priority=ContextPriority.HIGH,
                    specific_actions=[
                        "Provide concise, direct responses",
                        "Focus on immediate actionable items",
                        "Defer non-essential activities",
                        "Highlight time-sensitive priorities"
                    ],
                    expected_benefits=["Faster task completion", "Reduced time stress", "Better prioritization"],
                    confidence=0.9
                )
                recommendations.append(rec)
            
            # Energy optimization adaptations
            if context_snapshot.temporal.energy_cycle_phase == "peak":
                rec = create_contextual_recommendation(
                    target_primitive="goal_manager",
                    title="Leverage Peak Energy",
                    description="Peak energy phase detected - optimal time for challenging goals",
                    recommendation_type="timing",
                    priority=ContextPriority.MEDIUM,
                    specific_actions=[
                        "Suggest ambitious or challenging goals",
                        "Recommend tackling difficult tasks",
                        "Encourage creative or complex work",
                        "Support stretch objectives"
                    ],
                    expected_benefits=["Higher achievement potential", "Better use of natural rhythms", "Increased satisfaction"],
                    confidence=0.7
                )
                recommendations.append(rec)
            
            logger.info(f"Generated {len(recommendations)} contextual adaptations")
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating context adaptations: {e}")
            return []
    
    def suggest_context_actions(self, context_snapshot: ContextSnapshot) -> List[str]:
        """Suggest specific actions based on current context"""
        try:
            suggestions = []
            
            # Time-based suggestions
            if context_snapshot.temporal.current_time_context == "morning":
                suggestions.append("Plan daily priorities and challenging tasks")
                suggestions.append("Review goals and set intentions for the day")
            elif context_snapshot.temporal.current_time_context == "afternoon":
                suggestions.append("Focus on creative or collaborative work")
                suggestions.append("Take strategic breaks to maintain energy")
            
            # Energy-based suggestions
            if context_snapshot.temporal.energy_cycle_phase == "peak":
                suggestions.append("Tackle your most challenging or important tasks")
                suggestions.append("Engage in creative or problem-solving activities")
            elif context_snapshot.temporal.energy_cycle_phase == "low":
                suggestions.append("Focus on routine tasks or administrative work")
                suggestions.append("Consider taking a break or switching to lighter activities")
            
            # Mood-based suggestions
            if context_snapshot.emotional.primary_mood == "focused":
                suggestions.append("Take advantage of high focus for deep work")
                suggestions.append("Minimize interruptions and distractions")
            
            return suggestions[:5]  # Return top 5 suggestions
            
        except Exception as e:
            logger.error(f"Error generating context suggestions: {e}")
            return ["Take a moment to assess your current situation"]


class ContextManager:
    """
    Main Context Manager - Provides situation-aware intelligence
    
    The Context Manager is the situational intelligence hub of PACT,
    providing rich contextual awareness that makes all other primitives
    smarter and more adaptive.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        
        # Initialize core components
        self.analyzer = ContextAnalyzer()
        self.tracker = ContextTracker()
        self.bridge = ContextBridge()
        self.adaptor = ContextAdaptor()
        
        # Current state
        self.current_context = ContextSnapshot()
        self.is_active = False
        self.context_update_interval = self.config.get("update_interval", 30)  # seconds
        self.last_update_time = 0
        
        # Performance metrics
        self.context_metrics = ContextMetrics()
        
        # Context collection sources
        self.context_sources: Dict[str, Callable] = {}
        self.auto_collection_enabled = self.config.get("auto_collection", True)
        
        logger.info("ContextManager initialized")
    
    def start(self) -> None:
        """Start context management"""
        try:
            self.is_active = True
            
            # Initialize context sources
            self._initialize_context_sources()
            
            # Perform initial context collection
            self._collect_initial_context()
            
            logger.info("ContextManager started")
            
        except Exception as e:
            logger.error(f"Error starting ContextManager: {e}")
            self.is_active = False
    
    def stop(self) -> None:
        """Stop context management"""
        try:
            self.is_active = False
            logger.info("ContextManager stopped")
            
        except Exception as e:
            logger.error(f"Error stopping ContextManager: {e}")
    
    def _initialize_context_sources(self):
        """Initialize available context sources"""
        self.context_sources = {
            "system_time": self._get_system_time_context,
            "environment": self._get_environment_context,
        }
    
    def _collect_initial_context(self):
        """Collect initial context on startup"""
        try:
            initial_context = self._collect_context_from_sources()
            if initial_context:
                self.update_context(initial_context)
            
        except Exception as e:
            logger.error(f"Error collecting initial context: {e}")
    
    def _collect_context_from_sources(self) -> Dict[str, Any]:
        """Collect context from all available sources"""
        context_data = {}
        
        for source_name, source_func in self.context_sources.items():
            try:
                source_data = source_func()
                if source_data:
                    context_data[source_name] = source_data
            except Exception as e:
                logger.error(f"Error collecting from source {source_name}: {e}")
        
        return context_data
    
    def _get_system_time_context(self) -> Dict[str, Any]:
        """Get system time-based context"""
        current_time = time.time()
        dt = datetime.fromtimestamp(current_time)
        
        return {
            "current_time": current_time,
            "hour": dt.hour,
            "day_of_week": dt.weekday(),
            "month": dt.month,
        }
    
    def _get_environment_context(self) -> Dict[str, Any]:
        """Get environmental context"""
        return {
            "device_type": "laptop",
            "location": "office",
            "network_status": "connected",
        }
    
    def update_context(self, raw_context: Dict[str, Any]) -> ContextSnapshot:
        """Update current contextual understanding"""
        try:
            self.last_update_time = time.time()
            
            # Analyze different aspects of context
            all_factors = []
            
            # Environmental analysis
            env_factors = self.analyzer.analyze_environment(raw_context.get("environment", {}))
            all_factors.extend(env_factors)
            
            # Social analysis
            social_factors = self.analyzer.analyze_social_context(raw_context.get("social", {}))
            all_factors.extend(social_factors)
            
            # Temporal analysis
            temporal_factors = self.analyzer.analyze_temporal_context(raw_context.get("temporal", {}))
            all_factors.extend(temporal_factors)
            
            # Task analysis
            task_factors = self.analyzer.analyze_task_context(raw_context.get("task", {}))
            all_factors.extend(task_factors)
            
            # Emotional analysis
            emotional_factors = self.analyzer.analyze_emotional_context(raw_context.get("emotional", {}))
            all_factors.extend(emotional_factors)
            
            # Cognitive analysis
            cognitive_factors = self.analyzer.analyze_cognitive_context(raw_context.get("cognitive", {}))
            all_factors.extend(cognitive_factors)
            
            # Update context tracking
            self.current_context = self.tracker.update_context(all_factors)
            
            # Update metrics
            self._update_metrics(all_factors)
            
            logger.debug(f"Context updated with {len(all_factors)} factors")
            return self.current_context
            
        except Exception as e:
            logger.error(f"Error updating context: {e}")
            return self.current_context
    
    def get_current_context(self) -> ContextSnapshot:
        """Get current contextual state"""
        return self.current_context
    
    def get_contextual_recommendations(self, domain: str = "all") -> List[ContextualRecommendation]:
        """Get context-specific recommendations for a domain"""
        try:
            # Generate adaptations based on current context
            recommendations = self.adaptor.adapt_to_context(self.current_context)
            
            # Filter by domain if specified
            if domain != "all":
                recommendations = [
                    rec for rec in recommendations 
                    if rec.target_primitive == domain or rec.target_primitive == "all"
                ]
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error getting contextual recommendations: {e}")
            return []
    
    def get_context_for_primitive(self, primitive_name: str) -> Dict[str, Any]:
        """Get contextual intelligence for a specific primitive"""
        try:
            if primitive_name == "goal_manager":
                return self.bridge.provide_goal_context(self.current_context)
            elif primitive_name == "attention_manager":
                return self.bridge.provide_attention_context(self.current_context)
            else:
                # Generic context for unknown primitives
                return {
                    "context_summary": self.current_context.situation_summary,
                    "context_quality": self.current_context.overall_context_quality,
                    "dominant_factors": [f.type.value for f in self.current_context.context_factors[:5]]
                }
                
        except Exception as e:
            logger.error(f"Error getting context for primitive {primitive_name}: {e}")
            return {"error": str(e)}
    
    def assess_context_quality(self) -> Dict[str, float]:
        """Assess quality and completeness of current context"""
        try:
            quality_assessment = {
                "overall_quality": self.current_context.overall_context_quality,
                "confidence": self.current_context.context_confidence,
                "stability": self.current_context.context_stability,
                "complexity": self.current_context.context_complexity,
            }
            
            return quality_assessment
            
        except Exception as e:
            logger.error(f"Error assessing context quality: {e}")
            return {"error": 0.0}
    
    def _update_metrics(self, factors: List[ContextFactor]):
        """Update context management metrics"""
        try:
            self.context_metrics.total_factors_tracked += len(factors)
            self.context_metrics.active_context_types = len(set(f.type for f in factors))
            
            # Update quality metrics
            quality_assessment = self.assess_context_quality()
            self.context_metrics.context_quality_score = quality_assessment.get("overall_quality", 0.0)
            
            # Update calculation timestamp
            self.context_metrics.calculated_at = time.time()
            
        except Exception as e:
            logger.error(f"Error updating metrics: {e}")
    
    def get_context_insights(self) -> Dict[str, Any]:
        """Generate insights from current context"""
        try:
            return generate_context_insights(self.current_context)
        except Exception as e:
            logger.error(f"Error generating context insights: {e}")
            return {}
    
    def get_status_report(self) -> Dict[str, Any]:
        """Generate comprehensive status report"""
        try:
            return {
                "is_active": self.is_active,
                "current_context_id": self.current_context.id,
                "context_quality": self.assess_context_quality(),
                "context_insights": self.get_context_insights(),
                "metrics": asdict(self.context_metrics),
                "last_update": self.last_update_time,
                "context_summary": self.current_context.situation_summary
            }
        except Exception as e:
            logger.error(f"Error generating status report: {e}")
            return {"error": str(e), "is_active": self.is_active}


# Factory function for easy instantiation
def create_context_manager(config: Optional[Dict[str, Any]] = None) -> ContextManager:
    """Create and configure a ContextManager instance"""
    return ContextManager(config)


# Demonstration function
async def demonstrate_context_manager():
    """Demonstrate the Context Manager in action"""
    print("🌍 Demonstrating Context Manager - Situational Intelligence Hub")
    
    # Create the manager
    manager = create_context_manager({
        "auto_collection": True,
        "update_interval": 30
    })
    
    # Start the system
    manager.start()
    
    # Simulate context update
    print("\n📊 Updating context with sample data...")
    sample_context = {
        "environment": {
            "location": "home_office",
            "device_type": "laptop",
            "ambient_conditions": {
                "noise_level": "quiet",
                "lighting": "natural"
            },
            "connectivity": "excellent"
        },
        "social": {
            "interaction_mode": "solo",
            "relationship_type": "professional",
            "communication_style": "direct"
        },
        "temporal": {
            "schedule_pressure": "moderate",
            "next_commitment_minutes": 120,
            "energy_cycle": "peak"
        },
        "task": {
            "task_type": "creative",
            "complexity": "moderate",
            "progress": 0.3,
            "current_goals": ["complete_project", "learn_new_skill"],
            "blockers": []
        },
        "emotional": {
            "mood": "focused",
            "stress_level": "low",
            "motivation": "high",
            "energy": "good"
        },
        "cognitive": {
            "attention_state": "focused",
            "cognitive_load": "optimal",
            "mental_clarity": "clear"
        }
    }
    
    snapshot = manager.update_context(sample_context)
    print(f"   Context updated: {snapshot.id}")
    print(f"   Situation: {snapshot.situation_summary}")
    
    # Get context quality assessment
    print(f"\n📈 Context Quality Assessment:")
    quality = manager.assess_context_quality()
    for metric, score in quality.items():
        print(f"   {metric}: {score:.2f}")
    
    # Get contextual recommendations
    print(f"\n💡 Contextual Recommendations:")
    recommendations = manager.get_contextual_recommendations()
    for rec in recommendations[:3]:  # Show top 3
        print(f"   • {rec.title} (Priority: {rec.priority.value})")
        print(f"     {rec.description}")
    
    # Get context for specific primitives
    print(f"\n🎯 Context for Goal Manager:")
    goal_context = manager.get_context_for_primitive("goal_manager")
    for key, value in goal_context.items():
        if isinstance(value, list) and value:
            print(f"   {key}: {', '.join(value[:2])}")
        elif not isinstance(value, (dict, list)):
            print(f"   {key}: {value}")
    
    # Get insights
    print(f"\n🔍 Context Insights:")
    insights = manager.get_context_insights()
    for category, items in insights.items():
        if items:
            print(f"   {category}: {items[0] if isinstance(items, list) else items}")
    
    # Get status report
    print(f"\n📊 Context Manager Status:")
    status = manager.get_status_report()
    print(f"   Active: {status['is_active']}")
    print(f"   Quality Score: {status['context_quality']['overall_quality']:.2f}")
    
    # Stop the system
    manager.stop()
    print(f"\n✅ Context Manager demonstration complete!")


if __name__ == "__main__":
    # Example usage and testing
    print("🚀 Context Manager - Complete Implementation")
    print("🌍 Situational intelligence that makes every primitive smarter!")
    
    # Run demonstration
    import asyncio
    asyncio.run(demonstrate_context_manager())
ContextType, ContextScope, ContextPriority, ContextConfidence,
    EnvironmentalType, SocialContextType, TemporalContextType, EmotionalContextType,
    ContextFactor, EnvironmentalContext, SocialContext, TemporalContext,
    TaskContext, EmotionalContext, CognitiveContext, HistoricalContext,
    ContextSnapshot, ContextPattern, ContextChange, ContextualRecommendation,
    ContextMetrics,
    create_context_factor, create_environmental_context, create_social_context,
    create_temporal_context, create_task_context, create_emotional_context,
    create_cognitive_context, create_context_snapshot, create_contextual_recommendation,
    create_context_pattern, create_context_change,
    validate_context_factor, validate_context_snapshot,
    calculate_context_staleness, calculate_context_relevance,
    merge_context_snapshots, detect_context_anomalies, generate_context_insights
)

logger = logging.getLogger(__name__)


class ContextAnalyzer:
    """Analyzes and interprets contextual information from multiple sources"""
    
    def __init__(self, sensitivity_threshold: float = 0.3):
        self.sensitivity_threshold = sensitivity_threshold
        self.analysis_history: List[Dict[str, Any]] = []
        self.context_sources: Dict[str, Callable] = {}
        self.analysis_patterns: Dict[str, Any] = {}
        
        # Initialize analysis capabilities
        self._initialize_analysis_patterns()
        
        logger.info("ContextAnalyzer initialized")
    
    def _initialize_analysis_patterns(self):
        """Initialize patterns for context analysis"""
        self.analysis_patterns = {
            "time_patterns": {
                "morning": {"energy": "rising", "focus": "high", "creativity": "moderate"},
                "afternoon": {"energy": "stable", "focus": "moderate", "creativity": "high"},
                "evening": {"energy": "declining", "focus": "low", "creativity": "moderate"},
                "night": {"energy": "low", "focus": "very_low", "creativity": "variable"}
            },
            "device_patterns": {
                "mobile": {"attention_span": "short", "task_complexity": "low", "urgency": "high"},
                "laptop": {"attention_span": "medium", "task_complexity": "medium", "urgency": "moderate"},
                "desktop": {"attention_span": "long", "task_complexity": "high", "urgency": "low"}
            },
            "social_patterns": {
                "solo": {"focus_capacity": "high", "decision_speed": "fast", "creativity": "high"},
                "small_group": {"collaboration": "high", "consensus_needed": "moderate", "energy": "moderate"},
                "large_group": {"formal_behavior": "high", "decision_speed": "slow", "energy": "variable"}
            }
        }
    
    def analyze_environment(self, raw_context: Dict[str, Any]) -> List[ContextFactor]:
        """Analyze environmental contextual factors"""
        try:
            factors = []
            
            # Location analysis
            location = raw_context.get("location", "unknown")
            location_factor = create_context_factor(
                ContextType.ENVIRONMENTAL,
                "location_type",
                location,
                subtype="physical_location",
                priority=ContextPriority.HIGH,
                confidence=0.9,
                source="system_detection"
            )
            factors.append(location_factor)
            
            # Device analysis
            device_type = raw_context.get("device_type", "unknown")
            device_patterns = self.analysis_patterns.get("device_patterns", {}).get(device_type, {})
            
            device_factor = create_context_factor(
                ContextType.ENVIRONMENTAL,
                "device_context",
                device_type,
                subtype="device_context",
                priority=ContextPriority.MEDIUM,
                confidence=0.8,
                metadata={"patterns": device_patterns}
            )
            factors.append(device_factor)
            
            # Ambient conditions
            if "ambient_conditions" in raw_context:
                ambient = raw_context["ambient_conditions"]
                
                # Noise level
                if "noise_level" in ambient:
                    noise_factor = create_context_factor(
                        ContextType.ENVIRONMENTAL,
                        "noise_level",
                        ambient["noise_level"],
                        subtype="ambient_conditions",
                        priority=ContextPriority.MEDIUM,
                        confidence=0.7
                    )
                    factors.append(noise_factor)
                
                # Lighting
                if "lighting" in ambient:
                    lighting_factor = create_context_factor(
                        ContextType.ENVIRONMENTAL,
                        "lighting_condition",
                        ambient["lighting"],
                        subtype="ambient_conditions",
                        priority=ContextPriority.LOW,
                        confidence=0.6
                    )
                    factors.append(lighting_factor)
            
            # Network connectivity
            connectivity = raw_context.get("connectivity", "unknown")
            if connectivity != "unknown":
                connectivity_factor = create_context_factor(
                    ContextType.ENVIRONMENTAL,
                    "network_connectivity",
                    connectivity,
                    subtype="network_conditions",
                    priority=ContextPriority.MEDIUM if connectivity in ["poor", "offline"] else ContextPriority.LOW,
                    confidence=0.9
                )
                factors.append(connectivity_factor)
            
            logger.debug(f"Analyzed environment: {len(factors)} factors identified")
            return factors
            
        except Exception as e:
            logger.error(f"Error analyzing environment: {e}")
            return []
    
    def analyze_social_context(self, interaction_data: Dict[str, Any]) -> List[ContextFactor]:
        """Analyze social and cultural contextual factors"""
        try:
            factors = []
            
            # Interaction mode
            interaction_mode = interaction_data.get("interaction_mode", "solo")
            social_patterns = self.analysis_patterns.get("social_patterns", {}).get(interaction_mode, {})
            
            interaction_factor = create_context_factor(
                ContextType.SOCIAL,
                "interaction_mode",
                interaction_mode,
                subtype="relationship_dynamics",
                priority=ContextPriority.HIGH,
                confidence=0.9,
                metadata={"patterns": social_patterns}
            )
            factors.append(interaction_factor)
            
            # Relationship type
            relationship = interaction_data.get("relationship_type", "unknown")
            if relationship != "unknown":
                relationship_factor = create_context_factor(
                    ContextType.SOCIAL,
                    "relationship_type",
                    relationship,
                    subtype="relationship_dynamics",
                    priority=ContextPriority.HIGH,
                    confidence=0.8
                )
                factors.append(relationship_factor)
            
            # Communication style preference
            comm_style = interaction_data.get("communication_style", "unknown")
            if comm_style != "unknown":
                comm_factor = create_context_factor(
                    ContextType.SOCIAL,
                    "communication_style",
                    comm_style,
                    subtype="communication_style",
                    priority=ContextPriority.MEDIUM,
                    confidence=0.7
                )
                factors.append(comm_factor)
            
            # Cultural context
            cultural_context = interaction_data.get("cultural_context", {})
            if cultural_context:
                for key, value in cultural_context.items():
                    cultural_factor = create_context_factor(
                        ContextType.SOCIAL,
                        f"cultural_{key}",
                        value,
                        subtype="cultural_norms",
                        priority=ContextPriority.MEDIUM,
                        confidence=0.6
                    )
                    factors.append(cultural_factor)
            
            # Team dynamics
            team_data = interaction_data.get("team_context", {})
            if team_data:
                team_size = team_data.get("size", 1)
                team_factor = create_context_factor(
                    ContextType.SOCIAL,
                    "team_size",
                    team_size,
                    subtype="team_context",
                    priority=ContextPriority.MEDIUM,
                    confidence=0.8
                )
                factors.append(team_factor)
                
                if "dynamics" in team_data:
                    dynamics_factor = create_context_factor(
                        ContextType.SOCIAL,
                        "team_dynamics",
                        team_data["dynamics"],
                        subtype="team_context",
                        priority=ContextPriority.HIGH,
                        confidence=0.7
                    )
                    factors.append(dynamics_factor)
            
            logger.debug(f"Analyzed social context: {len(factors)} factors identified")
            return factors
            
        except Exception as e:
            logger.error(f"Error analyzing social context: {e}")
            return []
    
    def analyze_temporal_context(self, timing_data: Dict[str, Any]) -> List[ContextFactor]:
        """Analyze timing and temporal contextual factors"""
        try:
            factors = []
            current_time = time.time()
            current_hour = datetime.fromtimestamp(current_time).hour
            
            # Time of day analysis
            if 5 <= current_hour < 12:
                time_context = "morning"
            elif 12 <= current_hour < 17:
                time_context = "afternoon"
            elif 17 <= current_hour < 22:
                time_context = "evening"
            else:
                time_context = "night"
            
            time_patterns = self.analysis_patterns.get("time_patterns", {}).get(time_context, {})
            
            time_factor = create_context_factor(
                ContextType.TEMPORAL,
                "time_of_day",
                time_context,
                subtype="time_of_day",
                priority=ContextPriority.HIGH,
                confidence=1.0,
                metadata={"patterns": time_patterns, "hour": current_hour}
            )
            factors.append(time_factor)
            
            # Day of week
            weekday = datetime.fromtimestamp(current_time).weekday()
            day_names = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
            day_context = day_names[weekday]
            
            day_factor = create_context_factor(
                ContextType.TEMPORAL,
                "day_of_week",
                day_context,
                subtype="day_of_week",
                priority=ContextPriority.MEDIUM,
                confidence=1.0,
                metadata={"weekday_number": weekday}
            )
            factors.append(day_factor)
            
            # Schedule pressure
            schedule_pressure = timing_data.get("schedule_pressure", "unknown")
            if schedule_pressure != "unknown":
                pressure_factor = create_context_factor(
                    ContextType.TEMPORAL,
                    "schedule_pressure",
                    schedule_pressure,
                    subtype="schedule_pressure",
                    priority=ContextPriority.HIGH if schedule_pressure in ["urgent", "high"] else ContextPriority.MEDIUM,
                    confidence=0.8
                )
                factors.append(pressure_factor)
            
            # Next commitment
            next_commitment = timing_data.get("next_commitment_minutes")
            if next_commitment is not None:
                urgency = "immediate" if next_commitment < 15 else \
                         "soon" if next_commitment < 60 else \
                         "later" if next_commitment < 240 else "distant"
                
                commitment_factor = create_context_factor(
                    ContextType.TEMPORAL,
                    "next_commitment",
                    urgency,
                    subtype="deadline_proximity",
                    priority=ContextPriority.HIGH if urgency in ["immediate", "soon"] else ContextPriority.MEDIUM,
                    confidence=0.9,
                    metadata={"minutes_until": next_commitment}
                )
                factors.append(commitment_factor)
            
            # Energy cycle (based on time patterns)
            energy_cycle = timing_data.get("energy_cycle", time_patterns.get("energy", "unknown"))
            if energy_cycle != "unknown":
                energy_factor = create_context_factor(
                    ContextType.TEMPORAL,
                    "energy_cycle",
                    energy_cycle,
                    subtype="energy_rhythm",
                    priority=ContextPriority.MEDIUM,
                    confidence=0.7
                )
                factors.append(energy_factor)
            
            logger.debug(f"Analyzed temporal context: {len(factors)} factors identified")
            return factors
            
        except Exception as e:
            logger.error(f"Error analyzing temporal context: {e}")
            return []
    
    def analyze_task_context(self, task_data: Dict[str, Any]) -> List[ContextFactor]:
        """Analyze current task and workflow context"""
        try:
            factors = []
            
            # Primary task type
            task_type = task_data.get("task_type", "unknown")
            if task_type != "unknown":
                task_factor = create_context_factor(
                    ContextType.TASK,
                    "primary_task_type",
                    task_type,
                    priority=ContextPriority.HIGH,
                    confidence=0.8
                )
                factors.append(task_factor)
            
            # Task complexity
            complexity = task_data.get("complexity", "unknown")
            if complexity != "unknown":
                complexity_factor = create_context_factor(
                    ContextType.TASK,
                    "task_complexity",
                    complexity,
                    priority=ContextPriority.HIGH,
                    confidence=0.7
                )
                factors.append(complexity_factor)
            
            # Task progress
            progress = task_data.get("progress", 0.0)
            if progress > 0:
                progress_stage = "starting" if progress < 0.2 else \
                               "developing" if progress < 0.5 else \
                               "advancing" if progress < 0.8 else "completing"
                
                progress_factor = create_context_factor(
                    ContextType.TASK,
                    "task_progress",
                    progress_stage,
                    priority=ContextPriority.MEDIUM,
                    confidence=0.8,
                    metadata={"progress_value": progress}
                )
                factors.append(progress_factor)
            
            # Current goals
            current_goals = task_data.get("current_goals", [])
            if current_goals:
                goals_factor = create_context_factor(
                    ContextType.TASK,
                    "active_goals",
                    len(current_goals),
                    priority=ContextPriority.MEDIUM,
                    confidence=0.9,
                    metadata={"goals": current_goals}
                )
                factors.append(goals_factor)
            
            # Workflow stage
            workflow_stage = task_data.get("workflow_stage", "unknown")
            if workflow_stage != "unknown":
                workflow_factor = create_context_factor(
                    ContextType.TASK,
                    "workflow_stage",
                    workflow_stage,
                    priority=ContextPriority.MEDIUM,
                    confidence=0.8
                )
                factors.append(workflow_factor)
            
            # Blockers
            blockers = task_data.get("blockers", [])
            if blockers:
                blocker_factor = create_context_factor(
                    ContextType.TASK,
                    "task_blockers",
                    len(blockers),
                    priority=ContextPriority.HIGH,
                    confidence=0.9,
                    metadata={"blockers": blockers}
                )
                factors.append(blocker_factor)
            
            logger.debug(f"Analyzed task context: {len(factors)} factors identified")
            return factors
            
        except Exception as e:
            logger.error(f"Error analyzing task context: {e}")
            return []
    
    def analyze_emotional_context(self, emotional_data: Dict[str, Any]) -> List[ContextFactor]:
        """Analyze emotional and psychological context"""
        try:
            factors = []
            
            # Primary mood
            mood = emotional_data.get("mood", "unknown")
            if mood != "unknown":
                mood_factor = create_context_factor(
                    ContextType.EMOTIONAL,
                    "primary_mood",
                    mood,
                    subtype="mood_state",
                    priority=ContextPriority.HIGH,
                    confidence=0.8
                )
                factors.append(mood_factor)
            
            # Stress level
            stress = emotional_data.get("stress_level", "unknown")
            if stress != "unknown":
                stress_factor = create_context_factor(
                    ContextType.EMOTIONAL,
                    "stress_level",
                    stress,
                    subtype="stress_level",
                    priority=ContextPriority.HIGH if stress in ["high", "overwhelming"] else ContextPriority.MEDIUM,
                    confidence=0.7
                )
                factors.append(stress_factor)
            
            # Motivation level
            motivation = emotional_data.get("motivation", "unknown")
            if motivation != "unknown":
                motivation_factor = create_context_factor(
                    ContextType.EMOTIONAL,
                    "motivation_level",
                    motivation,
                    subtype="motivation_level",
                    priority=ContextPriority.HIGH,
                    confidence=0.8
                )
                factors.append(motivation_factor)
            
            # Energy level
            energy = emotional_data.get("energy", "unknown")
            if energy != "unknown":
                energy_factor = create_context_factor(
                    ContextType.EMOTIONAL,
                    "energy_level",
                    energy,
                    subtype="energy_level",
                    priority=ContextPriority.MEDIUM,
                    confidence=0.7
                )
                factors.append(energy_factor)
            
            # Confidence level
            confidence_level = emotional_data.get("confidence", "unknown")
            if confidence_level != "unknown":
                confidence_factor = create_context_factor(
                    ContextType.EMOTIONAL,
                    "confidence_level",
                    confidence_level,
                    subtype="confidence_level",
                    priority=ContextPriority.MEDIUM,
                    confidence=0.6
                )
                factors.append(confidence_factor)
            
            logger.debug(f"Analyzed emotional context: {len(factors)} factors identified")
            return factors
            
        except Exception as e:
            logger.error(f"Error analyzing emotional context: {e}")
            return []
    
    def analyze_cognitive_context(self, cognitive_data: Dict[str, Any]) -> List[ContextFactor]:
        """Analyze cognitive state and mental context"""
        try:
            factors = []
            
            # Attention state
            attention = cognitive_data.get("attention_state", "unknown")
            if attention != "unknown":
                attention_factor = create_context_factor(
                    ContextType.COGNITIVE,
                    "attention_state",
                    attention,
                    priority=ContextPriority.HIGH,
                    confidence=0.8
                )
                factors.append(attention_factor)
            
            # Cognitive load
            cognitive_load = cognitive_data.get("cognitive_load", "unknown")
            if cognitive_load != "unknown":
                load_factor = create_context_factor(
                    ContextType.COGNITIVE,
                    "cognitive_load",
                    cognitive_load,
                    priority=ContextPriority.HIGH if cognitive_load in ["heavy", "overloaded"] else ContextPriority.MEDIUM,
                    confidence=0.7
                )
                factors.append(load_factor)
            
            # Mental clarity
            clarity = cognitive_data.get("mental_clarity", "unknown")
            if clarity != "unknown":
                clarity_factor = create_context_factor(
                    ContextType.COGNITIVE,
                    "mental_clarity",
                    clarity,
                    priority=ContextPriority.MEDIUM,
                    confidence=0.6
                )
                factors.append(clarity_factor)
            
            # Focus capacity
            focus_capacity = cognitive_data.get("focus_capacity", "unknown")
            if focus_capacity != "unknown":
                focus_factor = create_context_factor(
                    ContextType.COGNITIVE,
                    "focus_capacity",
                    focus_capacity,
                    priority=ContextPriority.HIGH,
                    confidence=0.7
                )
                factors.append(focus_factor)
            
            logger.debug(f"Analyzed cognitive context: {len(factors)} factors identified")
            return factors
            
        except Exception as e:
            logger.error(f"Error analyzing cognitive context: {e}")
            return []


class ContextTracker:
    """Maintains and tracks contextual state over time"""
    
    def __init__(self, max_history_size: int = 100):
        self.max_history_size = max_history_size
        self.context_history: deque = deque(maxlen=max_history_size)
        self.current_snapshot: Optional[ContextSnapshot] = None
        self.tracked_patterns: Dict[str, ContextPattern] = {}
        self.change_history: List[ContextChange] = []
        
        # Change detection thresholds
        self.significant_change_threshold = 0.3
        self.major_change_threshold = 0.6
        
        logger.info("ContextTracker initialized")
    
    def update_context(self, new_factors: List[ContextFactor]) -> ContextSnapshot:
        """Update current context with new factors"""
        try:
            # Create new snapshot
            new_snapshot = self._create_snapshot_from_factors(new_factors)
            
            # Detect changes if we have previous context
            if self.current_snapshot:
                context_change = self._detect_context_changes(self.current_snapshot, new_snapshot)
                if context_change:
                    self.change_history.append(context_change)
                    logger.info(f"Context change detected: {context_change.change_significance}")
            
            # Update current snapshot
            previous_id = self.current_snapshot.id if self.current_snapshot else None
            new_snapshot.previous_snapshot_id = previous_id
            
            self.current_snapshot = new_snapshot
            self.context_history.append(new_snapshot)
            
            # Update patterns
            self._update_patterns(new_snapshot)
            
            logger.debug(f"Context updated: {len(new_factors)} factors, snapshot {new_snapshot.id}")
            return new_snapshot
            
        except Exception as e:
            logger.error(f"Error updating context: {e}")
            return self.current_snapshot or ContextSnapshot()
    
    def _create_snapshot_from_factors(self, factors: List[ContextFactor]) -> ContextSnapshot:
        """Create a context snapshot from individual factors"""
        snapshot = ContextSnapshot()
        snapshot.context_factors = factors
        
        # Organize factors by type and populate specific context objects
        factors_by_type = defaultdict(list)
        for factor in factors:
            factors_by_type[factor.type].append(factor)
        
        # Populate environmental context
        env_factors = factors_by_type[ContextType.ENVIRONMENTAL]
        snapshot.environmental = self._create_environmental_context(env_factors)
        
        # Populate social context
        social_factors = factors_by_type[ContextType.SOCIAL]
        snapshot.social = self._create_social_context(social_factors)
        
        # Populate temporal context
        temporal_factors = factors_by_type[ContextType.TEMPORAL]
        snapshot.temporal = self._create_temporal_context(temporal_factors)
        
        # Populate task context
        task_factors = factors_by_type[ContextType.TASK]
        snapshot.task = self._create_task_context(task_factors)
        
        # Populate emotional context
        emotional_factors = factors_by_type[ContextType.EMOTIONAL]
        snapshot.emotional = self._create_emotional_context(emotional_factors)
        
        # Populate cognitive context
        cognitive_factors = factors_by_type[ContextType.COGNITIVE]
        snapshot.cognitive = self._create_cognitive_context(cognitive_factors)
        
        # Calculate aggregate metrics
        snapshot.overall_context_quality = self._calculate_context_quality(factors)
        snapshot.context_confidence = self._calculate_average_confidence(factors)
        snapshot.context_stability = self._calculate_context_stability(factors)
        snapshot.context_complexity = self._calculate_context_complexity(factors)
        
        # Identify dominant context types
        snapshot.dominant_context_types = self._identify_dominant_types(factors)
        
        # Generate situation summary
        snapshot.situation_summary = self._generate_situation_summary(snapshot)
        
        return snapshot
    
    def _create_environmental_context(self, factors: List[ContextFactor]) -> EnvironmentalContext:
        """Create environmental context from factors"""
        env_context = EnvironmentalContext()
        
        for factor in factors:
            if factor.key == "location_type":
                env_context.location_type = str(factor.value)
            elif factor.key == "device_context":
                env_context.device_type = str(factor.value)
            elif factor.key == "noise_level":
                env_context.noise_level = str(factor.value)
            elif factor.key == "lighting_condition":
                env_context.lighting_condition = str(factor.value)
            elif factor.key == "network_connectivity":
                env_context.connectivity_quality = str(factor.value)
        
        return env_context
    
    def _create_social_context(self, factors: List[ContextFactor]) -> SocialContext:
        """Create social context from factors"""
        social_context = SocialContext()
        
        for factor in factors:
            if factor.key == "interaction_mode":
                social_context.interaction_mode = str(factor.value)
            elif factor.key == "relationship_type":
                social_context.relationship_type = str(factor.value)
            elif factor.key == "communication_style":
                social_context.preferred_communication_style = str(factor.value)
            elif factor.key == "team_size":
                social_context.team_size = int(factor.value) if isinstance(factor.value, (int, float)) else 0
            elif factor.key == "team_dynamics":
                social_context.team_dynamics = str(factor.value)
        
        return social_context
    
    def _create_temporal_context(self, factors: List[ContextFactor]) -> TemporalContext:
        """Create temporal context from factors"""
        temporal_context = TemporalContext()
        
        for factor in factors:
            if factor.key == "time_of_day":
                temporal_context.current_time_context = str(factor.value)
            elif factor.key == "day_of_week":
                temporal_context.day_of_week_context = str(factor.value)
            elif factor.key == "schedule_pressure":
                temporal_context.time_pressure_level = str(factor.value)
            elif factor.key == "next_commitment":
                temporal_context.next_commitment_minutes = factor.metadata.get("minutes_until")
            elif factor.key == "energy_cycle":
                temporal_context.energy_cycle_phase = str(factor.value)
        
        return temporal_context
    
    def _create_task_context(self, factors: List[ContextFactor]) -> TaskContext:
        """Create task context from factors"""
        task_context = TaskContext()
        
        for factor in factors:
            if factor.key == "primary_task_type":
                task_context.primary_task_type = str(factor.value)
            elif factor.key == "task_complexity":
                task_context.task_complexity = str(factor.value)
            elif factor.key == "task_progress":
                task_context.workflow_stage = str(factor.value)
                task_context.task_progress = factor.metadata.get("progress_value", 0.0)
            elif factor.key == "active_goals":
                task_context.immediate_goals = factor.metadata.get("goals", [])
            elif factor.key == "workflow_stage":
                task_context.workflow_stage = str(factor.value)
            elif factor.key == "task_blockers":
                task_context.blockers = factor.metadata.get("blockers", [])
        
        return task_context
    
    def _create_emotional_context(self, factors: List[ContextFactor]) -> EmotionalContext:
        """Create emotional context from factors"""
        emotional_context = EmotionalContext()
        
        for factor in factors:
            if factor.key == "primary_mood":
                emotional_context.primary_mood = str(factor.value)
            elif factor.key == "stress_level":
                emotional_context.stress_level = str(factor.value)
            elif factor.key == "motivation_level":
                emotional_context.motivation_level = str(factor.value)
            elif factor.key == "energy_level":
                emotional_context.mental_energy = str(factor.value)
            elif factor.key == "confidence_level":
                emotional_context.confidence_level = str(factor.value)
        
        return emotional_context
    
    def _create_cognitive_context(self, factors: List[ContextFactor]) -> CognitiveContext:
        """Create cognitive context from factors"""
        cognitive_context = CognitiveContext()
        
        for factor in factors:
            if factor.key == "attention_state":
                cognitive_context.attention_state = str(factor.value)
            elif factor.key == "cognitive_load":
                cognitive_context.cognitive_load = str(factor.value)
            elif factor.key == "mental_clarity":
                cognitive_context.mental_clarity = str(factor.value)
            elif factor.key == "focus_capacity":
                cognitive_context.concentration_quality = str(factor.value)
        
        return cognitive_context
