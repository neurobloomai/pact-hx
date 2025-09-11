# pact_hx/primitives/collaborative_intelligence/manager.py
"""
PACT Collaborative Intelligence Manager - The Orchestration Hub

The Collaborative Intelligence Manager serves as the central coordination hub for all
PACT primitives, orchestrating seamless human-AI collaboration that feels natural,
purposeful, and educationally effective.

Educational Mission:
Designed specifically for the education domain pilot, this manager orchestrates
learning experiences that adapt to each student's needs, learning style, and goals.
It coordinates multiple AI primitives to create cohesive, personalized educational
journeys that enhance rather than replace human teaching and learning.

Core Orchestration Responsibilities:
- Session Management: Initiating and managing collaborative learning sessions
- Primitive Coordination: Coordinating multiple PACT primitives for coherent responses
- Workflow Orchestration: Managing complex multi-step educational interactions
- Adaptive Learning: Dynamically adjusting collaboration based on learning outcomes
- Educational Assessment: Coordinating assessment across multiple primitives
- Context Synthesis: Combining insights from multiple sources for coherent responses

Educational Philosophy:
Every interaction should advance learning. The manager ensures that AI assistance
is not just helpful, but pedagogically sound, developmentally appropriate, and
aligned with educational best practices.
"""

import asyncio
import json
import logging
import time
from collections import defaultdict, deque
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Set, Tuple, Union, Callable
from dataclasses import asdict
import numpy as np

from .schemas import (
    CollaborationType, EducationalContext, LearningMode, CollaborationPhase,
    PrimitiveRole, InteractionComplexity, EducationalOutcome,
    CollaborationSessionSchema, CollaborationWorkflowSchema, PrimitiveInteractionSchema,
    PrimitiveStateSchema, EducationalCollaborationContextSchema, LearningPathwaySchema,
    EducationalAssessmentSchema, CollaborativeProblemSolvingSchema,
    InitiateCollaborationRequest, CollaborationActionRequest, PrimitiveCoordinationRequest,
    EducationalAssessmentRequest, LearningPathwayRequest,
    create_educational_collaboration_context, create_collaboration_workflow,
    create_primitive_state, validate_collaboration_workflow,
    calculate_collaboration_effectiveness, suggest_primitive_roles,
    EducationalCollaborationPatterns, calculate_primitive_collaboration_score,
    generate_collaboration_insights
)

logger = logging.getLogger(__name__)

class PrimitiveCoordinator:
    """Coordinates interactions between PACT primitives"""
    
    def __init__(self):
        self.registered_primitives: Dict[str, Any] = {}
        self.primitive_states: Dict[str, PrimitiveStateSchema] = {}
        self.interaction_history: List[PrimitiveInteractionSchema] = []
        self.coordination_rules: Dict[str, List[Callable]] = defaultdict(list)
        
    async def register_primitive(self, primitive_name: str, primitive_instance: Any, 
                                initial_role: PrimitiveRole = PrimitiveRole.CONTENT_PROVIDER):
        """Register a PACT primitive for coordination"""
        self.registered_primitives[primitive_name] = primitive_instance
        
        # Create initial state
        self.primitive_states[primitive_name] = create_primitive_state(
            primitive_name=primitive_name,
            primitive_type=self._get_primitive_type(primitive_name),
            current_role=initial_role,
            status="active",
            collaboration_readiness=1.0
        )
        
        logger.info(f"Registered primitive: {primitive_name} with role: {initial_role.value}")
    
    def _get_primitive_type(self, primitive_name: str) -> str:
        """Determine primitive type from name"""
        type_mapping = {
            "goal": "goal_management",
            "empathetic_interaction": "emotional_intelligence",
            "adaptive_reasoning": "reasoning_engine",
            "creative_synthesis": "creative_engine",
            "meta_learning": "learning_optimization",
            "contextual_memory": "memory_management",
            "value_alignment": "ethical_framework",
            "trust_calibration": "trust_management",
            "explainable_ai": "explanation_engine",
            "continuous_adaptation": "adaptation_engine",
            "uncertainty_handling": "uncertainty_management",
            "ethical_reasoning": "ethical_reasoning"
        }
        return type_mapping.get(primitive_name, "general_primitive")
    
    async def coordinate_primitives(self, coordination_request: PrimitiveCoordinationRequest) -> Dict[str, Any]:
        """Coordinate multiple primitives for a specific task"""
        logger.info(f"Coordinating primitives: {coordination_request.target_primitives}")
        
        coordination_result = {
            "success": True,
            "coordination_id": f"coord_{int(time.time())}",
            "primitive_responses": {},
            "synthesized_response": {},
            "coordination_quality": 0.0
        }
        
        try:
            # Phase 1: Validate primitive availability
            available_primitives = self._validate_primitive_availability(coordination_request.target_primitives)
            if not available_primitives:
                return {"success": False, "error": "No available primitives for coordination"}
            
            # Phase 2: Determine coordination strategy
            coordination_strategy = await self._determine_coordination_strategy(
                coordination_request, available_primitives
            )
            
            # Phase 3: Execute coordinated interaction
            primitive_responses = await self._execute_coordinated_interaction(
                coordination_request, coordination_strategy
            )
            coordination_result["primitive_responses"] = primitive_responses
            
            # Phase 4: Synthesize responses
            synthesized_response = await self._synthesize_primitive_responses(
                primitive_responses, coordination_request.context
            )
            coordination_result["synthesized_response"] = synthesized_response
            
            # Phase 5: Evaluate coordination quality
            coordination_quality = self._evaluate_coordination_quality(
                coordination_request, primitive_responses, synthesized_response
            )
            coordination_result["coordination_quality"] = coordination_quality
            
            # Record interaction
            await self._record_coordination_interaction(coordination_request, coordination_result)
            
            logger.info(f"Coordination completed with quality: {coordination_quality:.2f}")
            
        except Exception as e:
            logger.error(f"Coordination failed: {e}")
            coordination_result.update({"success": False, "error": str(e)})
        
        return coordination_result
    
    def _validate_primitive_availability(self, target_primitives: List[str]) -> List[str]:
        """Validate which target primitives are available"""
        available = []
        for primitive in target_primitives:
            if primitive in self.registered_primitives:
                state = self.primitive_states.get(primitive)
                if state and state.status == "active" and state.collaboration_readiness > 0.5:
                    available.append(primitive)
        return available
    
    async def _determine_coordination_strategy(self, request: PrimitiveCoordinationRequest, 
                                             available_primitives: List[str]) -> Dict[str, Any]:
        """Determine the best coordination strategy"""
        strategy = {
            "execution_order": [],
            "interaction_type": "sequential",
            "role_assignments": {},
            "context_sharing": True,
            "response_synthesis": "weighted_combination"
        }
        
        # Determine execution order based on primitive dependencies and roles
        if request.coordination_type == "educational_explanation":
            priority_order = ["adaptive_reasoning", "empathetic_interaction", "explainable_ai", "creative_synthesis"]
            strategy["execution_order"] = [p for p in priority_order if p in available_primitives]
            strategy["execution_order"].extend([p for p in available_primitives if p not in strategy["execution_order"]])
            
        elif request.coordination_type == "creative_learning":
            priority_order = ["creative_synthesis", "adaptive_reasoning", "empathetic_interaction"]
            strategy["execution_order"] = [p for p in priority_order if p in available_primitives]
            strategy["execution_order"].extend([p for p in available_primitives if p not in strategy["execution_order"]])
            
        elif request.coordination_type == "assessment":
            priority_order = ["meta_learning", "adaptive_reasoning", "empathetic_interaction"]
            strategy["execution_order"] = [p for p in priority_order if p in available_primitives]
            strategy["execution_order"].extend([p for p in available_primitives if p not in strategy["execution_order"]])
            
        else:
            strategy["execution_order"] = available_primitives
        
        # Assign roles based on expected roles from request
        for primitive in available_primitives:
            expected_roles = request.expected_roles.get(primitive, [PrimitiveRole.CONTENT_PROVIDER])
            strategy["role_assignments"][primitive] = expected_roles[0]
        
        return strategy
    
    async def _execute_coordinated_interaction(self, request: PrimitiveCoordinationRequest,
                                             strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the coordinated interaction across primitives"""
        primitive_responses = {}
        shared_context = request.context.copy()
        
        for primitive_name in strategy["execution_order"]:
            try:
                primitive_instance = self.registered_primitives[primitive_name]
                role = strategy["role_assignments"].get(primitive_name, PrimitiveRole.CONTENT_PROVIDER)
                
                primitive_request = self._prepare_primitive_request(
                    primitive_name, role, shared_context, request
                )
                
                response = await self._call_primitive(primitive_instance, primitive_request)
                primitive_responses[primitive_name] = response
                
                if strategy.get("context_sharing", True):
                    shared_context[f"{primitive_name}_response"] = response
                    shared_context[f"{primitive_name}_insights"] = response.get("insights", {})
                
                interaction = PrimitiveInteractionSchema(
                    workflow_id=request.session_id,
                    initiating_primitive="collaborative_intelligence",
                    target_primitives=[primitive_name],
                    interaction_type=request.coordination_type,
                    request_payload=primitive_request,
                    response_payload=response,
                    context_shared=shared_context,
                    educational_purpose=f"Coordination for {request.coordination_type}",
                    success=response.get("success", True)
                )
                self.interaction_history.append(interaction)
                
            except Exception as e:
                logger.error(f"Error executing {primitive_name}: {e}")
                primitive_responses[primitive_name] = {"success": False, "error": str(e)}
        
        return primitive_responses
    
    def _prepare_primitive_request(self, primitive_name: str, role: PrimitiveRole, 
                                  context: Dict[str, Any], original_request: PrimitiveCoordinationRequest) -> Dict[str, Any]:
        """Prepare request tailored for specific primitive"""
        base_request = {
            "context": context,
            "role": role.value,
            "coordination_type": original_request.coordination_type,
            "session_id": original_request.session_id
        }
        
        if primitive_name == "goal":
            base_request.update({
                "action": "analyze_learning_goals",
                "educational_context": context.get("educational_context", {})
            })
        elif primitive_name == "empathetic_interaction":
            base_request.update({
                "action": "provide_empathetic_support",
                "emotional_context": context.get("emotional_state", "neutral"),
                "support_type": "educational"
            })
        elif primitive_name == "adaptive_reasoning":
            base_request.update({
                "action": "educational_reasoning",
                "reasoning_type": "pedagogical",
                "complexity_level": context.get("complexity_level", "moderate")
            })
        elif primitive_name == "creative_synthesis":
            base_request.update({
                "action": "creative_educational_content",
                "creativity_focus": "learning_enhancement",
                "subject_area": context.get("subject_area", "general")
            })
        elif primitive_name == "meta_learning":
            base_request.update({
                "action": "assess_learning_progress",
                "assessment_type": "formative",
                "learning_objectives": context.get("learning_objectives", [])
            })
        
        return base_request
    
    async def _call_primitive(self, primitive_instance: Any, request: Dict[str, Any]) -> Dict[str, Any]:
        """Call a primitive with the prepared request"""
        try:
            if hasattr(primitive_instance, 'process_coordination_request'):
                return await primitive_instance.process_coordination_request(request)
            elif hasattr(primitive_instance, 'process_request'):
                return await primitive_instance.process_request(request)
            else:
                return {
                    "success": True,
                    "response": f"Educational response from {request.get('primitive_name', 'unknown')}",
                    "confidence": 0.8,
                    "educational_value": 0.7,
                    "insights": {"coordination_role": request.get("role", "content_provider")}
                }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _synthesize_primitive_responses(self, primitive_responses: Dict[str, Any], 
                                            context: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize responses from multiple primitives into coherent output"""
        synthesis = {
            "primary_response": "",
            "supporting_insights": [],
            "educational_recommendations": [],
            "confidence_score": 0.0,
            "coherence_score": 0.0
        }
        
        successful_responses = {k: v for k, v in primitive_responses.items() if v.get("success", False)}
        
        if not successful_responses:
            return {"success": False, "error": "No successful primitive responses to synthesize"}
        
        response_components = {}
        confidence_scores = []
        
        for primitive, response in successful_responses.items():
            response_components[primitive] = {
                "content": response.get("response", ""),
                "insights": response.get("insights", {}),
                "confidence": response.get("confidence", 0.5),
                "educational_value": response.get("educational_value", 0.5)
            }
            confidence_scores.append(response.get("confidence", 0.5))
        
        synthesis["primary_response"] = await self._create_coherent_response(response_components, context)
        
        all_insights = []
        for primitive, component in response_components.items():
            insights = component["insights"]
            if insights:
                all_insights.append(f"{primitive}: {insights}")
        synthesis["supporting_insights"] = all_insights
        
        synthesis["educational_recommendations"] = await self._generate_educational_recommendations(
            response_components, context
        )
        
        synthesis["confidence_score"] = np.mean(confidence_scores) if confidence_scores else 0.0
        synthesis["coherence_score"] = self._calculate_coherence_score(response_components)
        
        return synthesis
    
    async def _create_coherent_response(self, response_components: Dict[str, Dict], 
                                       context: Dict[str, Any]) -> str:
        """Create a coherent response from multiple primitive outputs"""
        priority_order = ["adaptive_reasoning", "empathetic_interaction", "creative_synthesis", "meta_learning"]
        
        primary_content = ""
        supporting_content = []
        
        for primitive in priority_order:
            if primitive in response_components:
                component = response_components[primitive]
                if component["content"] and component["educational_value"] > 0.6:
                    primary_content = component["content"]
                    break
        
        if not primary_content:
            best_primitive = max(
                response_components.keys(),
                key=lambda p: response_components[p]["educational_value"] * response_components[p]["confidence"]
            )
            primary_content = response_components[best_primitive]["content"]
        
        for primitive, component in response_components.items():
            content = component["content"]
            if content and content != primary_content and component["educational_value"] > 0.4:
                supporting_content.append(content)
        
        if supporting_content:
            coherent_response = f"{primary_content}\n\nAdditional insights: {' '.join(supporting_content[:2])}"
        else:
            coherent_response = primary_content
        
        return coherent_response
    
    async def _generate_educational_recommendations(self, response_components: Dict[str, Dict],
                                                   context: Dict[str, Any]) -> List[str]:
        """Generate educational recommendations from primitive responses"""
        recommendations = []
        
        avg_confidence = np.mean([comp["confidence"] for comp in response_components.values()])
        avg_educational_value = np.mean([comp["educational_value"] for comp in response_components.values()])
        
        if avg_confidence < 0.7:
            recommendations.append("Consider seeking additional clarification or resources")
        
        if avg_educational_value > 0.8:
            recommendations.append("This appears to be a high-value learning opportunity")
        
        if "meta_learning" in response_components:
            meta_insights = response_components["meta_learning"]["insights"]
            if "learning_gaps" in meta_insights:
                recommendations.append("Focus on addressing identified learning gaps")
        
        if "empathetic_interaction" in response_components:
            empathy_insights = response_components["empathetic_interaction"]["insights"]
            if "emotional_support_needed" in empathy_insights:
                recommendations.append("Consider emotional support and encouragement")
        
        return recommendations
    
    def _calculate_coherence_score(self, response_components: Dict[str, Dict]) -> float:
        """Calculate how coherent the combined response is"""
        if len(response_components) < 2:
            return 1.0
        
        confidences = [comp["confidence"] for comp in response_components.values()]
        educational_values = [comp["educational_value"] for comp in response_components.values()]
        
        confidence_variance = np.var(confidences)
        value_variance = np.var(educational_values)
        
        coherence = 1.0 - min(1.0, (confidence_variance + value_variance) / 2.0)
        return coherence
    
    def _evaluate_coordination_quality(self, request: PrimitiveCoordinationRequest,
                                     primitive_responses: Dict[str, Any],
                                     synthesized_response: Dict[str, Any]) -> float:
        """Evaluate the quality of the coordination"""
        quality_factors = []
        
        successful_responses = sum(1 for r in primitive_responses.values() if r.get("success", False))
        success_rate = successful_responses / max(1, len(primitive_responses))
        quality_factors.append(success_rate)
        
        coherence_score = synthesized_response.get("coherence_score", 0.0)
        quality_factors.append(coherence_score)
        
        confidence_score = synthesized_response.get("confidence_score", 0.0)
        quality_factors.append(confidence_score)
        
        educational_values = [r.get("educational_value", 0.0) for r in primitive_responses.values() if r.get("success")]
        avg_educational_value = np.mean(educational_values) if educational_values else 0.0
        quality_factors.append(avg_educational_value)
        
        weights = [0.3, 0.25, 0.25, 0.2]
        quality_score = sum(w * f for w, f in zip(weights, quality_factors))
        
        return min(1.0, max(0.0, quality_score))
    
    async def _record_coordination_interaction(self, request: PrimitiveCoordinationRequest,
                                             result: Dict[str, Any]):
        """Record the coordination interaction for analysis"""
        coordination_interaction = PrimitiveInteractionSchema(
            workflow_id=request.session_id,
            initiating_primitive="collaborative_intelligence",
            target_primitives=request.target_primitives,
            interaction_type=f"coordination_{request.coordination_type}",
            request_payload={"session_id": request.session_id, "coordination_type": request.coordination_type},
            response_payload=result,
            educational_purpose=f"Coordinated {request.coordination_type}",
            success=result.get("success", False),
            response_time=0.0,
            accuracy=result.get("coordination_quality", 0.0)
        )
        
        self.interaction_history.append(coordination_interaction)

class EducationalWorkflowOrchestrator:
    """Orchestrates complex educational workflows"""
    
    def __init__(self, primitive_coordinator: PrimitiveCoordinator):
        self.primitive_coordinator = primitive_coordinator
        self.active_workflows: Dict[str, CollaborationWorkflowSchema] = {}
        self.workflow_templates = self._load_workflow_templates()
        
    def _load_workflow_templates(self) -> Dict[str, Dict[str, Any]]:
        """Load predefined workflow templates for educational contexts"""
        return {
            "socratic_dialogue": EducationalCollaborationPatterns.get_socratic_dialogue_pattern(),
            "collaborative_project": EducationalCollaborationPatterns.get_collaborative_project_pattern(),
            "personalized_tutoring": EducationalCollaborationPatterns.get_personalized_tutoring_pattern()
        }
    
    async def initiate_workflow(self, workflow_request: InitiateCollaborationRequest) -> Dict[str, Any]:
        """Initiate a new educational workflow"""
        logger.info(f"Initiating workflow: {workflow_request.collaboration_type.value}")
        
        try:
            pattern = self._select_workflow_pattern(workflow_request)
            
            workflow = create_collaboration_workflow(
                workflow_name=f"{workflow_request.collaboration_type.value}_workflow",
                collaboration_type=workflow_request.collaboration_type,
                educational_context=workflow_request.educational_context,
                participating_primitives=workflow_request.preferred_ai_primitives or list(pattern["primitive_roles"].keys()),
                phases=pattern["phases"],
                target_outcomes=[EducationalOutcome.KNOWLEDGE_GAINED, EducationalOutcome.SKILL_DEVELOPED],
                primitive_assignments=pattern["primitive_roles"],
                coordination_rules=[{"rule": rule} for rule in pattern.get("interaction_rules", [])]
            )
            
            validation_errors = validate_collaboration_workflow(workflow)
            if validation_errors:
                return {"success": False, "errors": validation_errors}
            
            self.active_workflows[workflow.workflow_id] = workflow
            
            await self._initialize_primitive_roles(workflow)
            await self._transition_to_phase(workflow.workflow_id, workflow.phases[0])
            
            logger.info(f"Workflow initiated: {workflow.workflow_id}")
            
            return {
                "success": True,
                "workflow_id": workflow.workflow_id,
                "current_phase": workflow.current_phase.value,
                "participating_primitives": workflow.participating_primitives,
                "estimated_duration": workflow.estimated_duration
            }
            
        except Exception as e:
            logger.error(f"Failed to initiate workflow: {e}")
            return {"success": False, "error": str(e)}
    
    def _select_workflow_pattern(self, request: InitiateCollaborationRequest) -> Dict[str, Any]:
        """Select appropriate workflow pattern based on request"""
        return EducationalCollaborationPatterns.get_pattern_for_context(
            request.collaboration_type,
            request.educational_context.learning_mode,
            request.educational_context.educational_context
        )
    
    async def _initialize_primitive_roles(self, workflow: CollaborationWorkflowSchema):
        """Initialize roles for all participating primitives"""
        for primitive_name, roles in workflow.primitive_assignments.items():
            if primitive_name in self.primitive_coordinator.registered_primitives:
                state = self.primitive_coordinator.primitive_states[primitive_name]
                state.current_role = roles[0] if isinstance(roles, list) else roles
                state.educational_focus = workflow.educational_context.subject_area
                state.learning_objectives = workflow.educational_context.primary_learning_objectives
                
                logger.info(f"Assigned role {state.current_role.value} to {primitive_name}")
    
    async def _transition_to_phase(self, workflow_id: str, new_phase: CollaborationPhase):
        """Transition workflow to a new phase"""
        if workflow_id not in self.active_workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        workflow = self.active_workflows[workflow_id]
        old_phase = workflow.current_phase
        workflow.current_phase = new_phase
        
        workflow.phase_progress[new_phase.value] = 0.0
        
        await self._notify_phase_transition(workflow, old_phase, new_phase)
        
        logger.info(f"Workflow {workflow_id} transitioned from {old_phase.value} to {new_phase.value}")
    
    async def _notify_phase_transition(self, workflow: CollaborationWorkflowSchema,
                                     old_phase: CollaborationPhase, new_phase: CollaborationPhase):
        """Notify all participating primitives about phase transition"""
        notification_context = {
            "workflow_id": workflow.workflow_id,
            "old_phase": old_phase.value,
            "new_phase": new_phase.value,
            "educational_context": asdict(workflow.educational_context),
            "learning_objectives": workflow.educational_context.primary_learning_objectives
        }
        
        for primitive_name in workflow.participating_primitives:
            try:
                coordination_request = PrimitiveCoordinationRequest(
                    session_id=workflow.workflow_id,
                    target_primitives=[primitive_name],
                    coordination_type="phase_transition",
                    context=notification_context
                )
                
                await self.primitive_coordinator.coordinate_primitives(coordination_request)
                
            except Exception as e:
                logger.warning(f"Failed to notify {primitive_name} about phase transition: {e}")
    
    async def execute_workflow_action(self, action_request: CollaborationActionRequest) -> Dict[str, Any]:
        """Execute an action within a workflow"""
        workflow_id = action_request.session_id
        
        if workflow_id not in self.active_workflows:
            return {"success": False, "error": "Workflow not found"}
        
        workflow = self.active_workflows[workflow_id]
        
        try:
            target_primitives = self._determine_action_primitives(action_request, workflow)
            
            coordination_request = PrimitiveCoordinationRequest(
                session_id=workflow_id,
                target_primitives=target_primitives,
                coordination_type=action_request.action_type,
                context={
                    "action_parameters": action_request.action_parameters,
                    "educational_context": asdict(workflow.educational_context),
                    "current_phase": workflow.current_phase.value,
                    "workflow_progress": workflow.phase_progress
                },
                expected_roles=workflow.primitive_assignments
            )
            
            coordination_result = await self.primitive_coordinator.coordinate_primitives(coordination_request)
            
            await self._update_workflow_progress(workflow, action_request, coordination_result)
            await self._check_phase_transition(workflow)
            
            return {
                "success": coordination_result["success"],
                "workflow_id": workflow_id,
                "current_phase": workflow.current_phase.value,
                "coordination_result": coordination_result,
                "phase_progress": workflow.phase_progress.get(workflow.current_phase.value, 0.0)
            }
            
        except Exception as e:
            logger.error(f"Error executing workflow action: {e}")
            return {"success": False, "error": str(e)}
    
    def _determine_action_primitives(self, action_request: CollaborationActionRequest,
                                   workflow: CollaborationWorkflowSchema) -> List[str]:
        """Determine which primitives should be involved in the action"""
        action_type = action_request.action_type
        
        if action_type == "explain_concept":
            return ["adaptive_reasoning", "empathetic_interaction", "explainable_ai"]
        elif action_type == "assess_understanding":
            return ["meta_learning", "adaptive_reasoning", "empathetic_interaction"]
        elif action_type == "provide_feedback":
            return ["empathetic_interaction", "meta_learning"]
        elif action_type == "generate_creative_exercise":
            return ["creative_synthesis", "adaptive_reasoning", "goal"]
        elif action_type == "adapt_difficulty":
            return ["meta_learning", "continuous_adaptation", "adaptive_reasoning"]
        else:
            return workflow.participating_primitives
    
    async def _update_workflow_progress(self, workflow: CollaborationWorkflowSchema,
                                       action_request: CollaborationActionRequest,
                                       coordination_result: Dict[str, Any]):
        """Update workflow progress based on action execution"""
        current_phase = workflow.current_phase.value
        
        if coordination_result["success"]:
            quality_score = coordination_result.get("coordination_quality", 0.5)
            progress_increment = 0.1 * (1 + quality_score)
        else:
            progress_increment = 0.02
        
        current_progress = workflow.phase_progress.get(current_phase, 0.0)
        new_progress = min(1.0, current_progress + progress_increment)
        workflow.phase_progress[current_phase] = new_progress
        
        logger.debug(f"Updated phase {current_phase} progress to {new_progress:.2f}")
    
    async def _check_phase_transition(self, workflow: CollaborationWorkflowSchema):
        """Check if workflow should transition to next phase"""
        current_phase = workflow.current_phase
        current_progress = workflow.phase_progress.get(current_phase.value, 0.0)
        
        if current_progress >= 0.8:
            current_phase_index = workflow.phases.index(current_phase)
            
            if current_phase_index < len(workflow.phases) - 1:
                next_phase = workflow.phases[current_phase_index + 1]
                await self._transition_to_phase(workflow.workflow_id, next_phase)
    
    async def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get current status of a workflow"""
        if workflow_id not in self.active_workflows:
            return {"success": False, "error": "Workflow not found"}
        
        workflow = self.active_workflows[workflow_id]
        
        return {
            "success": True,
            "workflow_id": workflow_id,
            "workflow_name": workflow.workflow_name,
            "collaboration_type": workflow.collaboration_type.value,
            "current_phase": workflow.current_phase.value,
            "phase_progress": workflow.phase_progress,
            "overall_progress": self._calculate_overall_progress(workflow),
            "participating_primitives": workflow.participating_primitives,
            "educational_context": {
                "subject_area": workflow.educational_context.subject_area,
                "learning_mode": workflow.educational_context.learning_mode.value,
                "primary_objectives": workflow.educational_context.primary_learning_objectives
            },
            "target_outcomes": [outcome.value for outcome in workflow.target_outcomes],
            "achieved_outcomes": workflow.achieved_outcomes
        }
    
    def _calculate_overall_progress(self, workflow: CollaborationWorkflowSchema) -> float:
        """Calculate overall workflow progress"""
        if not workflow.phases:
            return 0.0
        
        total_phases = len(workflow.phases)
        completed_phases = 0
        current_phase_weight = 0.0
        
        for i, phase in enumerate(workflow.phases):
            phase_progress = workflow.phase_progress.get(phase.value, 0.0)
            
            if phase_progress >= 1.0:
                completed_phases += 1
            elif phase == workflow.current_phase:
                current_phase_weight = phase_progress
        
        overall_progress = (completed_phases + current_phase_weight) / total_phases
        return min(1.0, overall_progress)

class EducationalSessionManager:
    """Manages complete educational collaboration sessions"""
    
    def __init__(self, workflow_orchestrator: EducationalWorkflowOrchestrator):
        self.workflow_orchestrator = workflow_orchestrator
        self.active_sessions: Dict[str, CollaborationSessionSchema] = {}
        self.session_assessments: Dict[str, List[EducationalAssessmentSchema]] = defaultdict(list)
        self.learning_pathways: Dict[str, LearningPathwaySchema] = {}
        
    async def initiate_session(self, session_request: InitiateCollaborationRequest) -> Dict[str, Any]:
        """Initiate a new educational collaboration session"""
        logger.info(f"Initiating session: {session_request.collaboration_type.value}")
        
        try:
            session = CollaborationSessionSchema(
                session_name=f"{session_request.collaboration_type.value} Session",
                participants=session_request.participants,
                ai_participants=session_request.preferred_ai_primitives or [],
                collaboration_type=session_request.collaboration_type,
                session_goals=session_request.session_goals,
                educational_context=session_request.educational_context
            )
            
            self.active_sessions[session.session_id] = session
            
            workflow_result = await self.workflow_orchestrator.initiate_workflow(session_request)
            
            if workflow_result["success"]:
                session.active_workflows.append(workflow_result["workflow_id"])
                await self._initialize_learning_pathway(session)
                
                logger.info(f"Session initiated: {session.session_id}")
                
                return {
                    "success": True,
                    "session_id": session.session_id,
                    "workflow_id": workflow_result["workflow_id"],
                    "session_goals": session.session_goals,
                    "educational_context": asdict(session.educational_context),
                    "estimated_duration": session_request.time_limit
                }
            else:
                return {"success": False, "error": "Failed to initiate workflow", "details": workflow_result}
                
        except Exception as e:
            logger.error(f"Failed to initiate session: {e}")
            return {"success": False, "error": str(e)}
    
    async def _initialize_learning_pathway(self, session: CollaborationSessionSchema):
        """Initialize learning pathway for the session"""
        student_info = None
        for participant_id, participant_data in session.participants.items():
            if participant_data.get("role") == "student":
                student_info = participant_data
                break
        
        if student_info:
            pathway = LearningPathwaySchema(
                student_id=student_info.get("id", "unknown"),
                subject_area=session.educational_context.subject_area,
                learning_objectives=session.educational_context.primary_learning_objectives,
                collaborative_sessions=[session.session_id],
                learning_style_profile=session.educational_context.learning_preferences
            )
            
            self.learning_pathways[session.session_id] = pathway
    
    async def process_session_action(self, action_request: CollaborationActionRequest) -> Dict[str, Any]:
        """Process an action within a session"""
        session_id = action_request.session_id
        
        if session_id not in self.active_sessions:
            return {"success": False, "error": "Session not found"}
        
        session = self.active_sessions[session_id]
        
        try:
            action_result = await self.workflow_orchestrator.execute_workflow_action(action_request)
            
            session.interaction_count += 1
            
            if session_id in self.learning_pathways:
                await self._update_learning_pathway_progress(session_id, action_request, action_result)
            
            await self._check_adaptive_adjustments(session, action_result)
            
            return action_result
            
        except Exception as e:
            logger.error(f"Error processing session action: {e}")
            return {"success": False, "error": str(e)}
    
    async def _update_learning_pathway_progress(self, session_id: str,
                                               action_request: CollaborationActionRequest,
                                               action_result: Dict[str, Any]):
        """Update learning pathway based on session progress"""
        pathway = self.learning_pathways[session_id]
        
        pathway.time_invested += timedelta(minutes=1)
        
        if action_result["success"]:
            quality = action_result.get("coordination_result", {}).get("coordination_quality", 0.5)
            current_success = pathway.success_rate
            pathway.success_rate = 0.9 * current_success + 0.1 * quality
        
        await self._check_milestone_progress(pathway, action_request)
    
    async def _check_milestone_progress(self, pathway: LearningPathwaySchema,
                                       action_request: CollaborationActionRequest):
        """Check if student has reached learning milestones"""
        if pathway.success_rate > 0.8 and len(pathway.collaborative_sessions) > 5:
            pathway.completion_percentage = min(100.0, pathway.completion_percentage + 10.0)
            
            if pathway.completion_percentage >= 100.0:
                logger.info(f"Learning pathway completed for student {pathway.student_id}")
    
    async def _check_adaptive_adjustments(self, session: CollaborationSessionSchema,
                                         action_result: Dict[str, Any]):
        """Check if adaptive adjustments are needed"""
        coordination_quality = action_result.get("coordination_result", {}).get("coordination_quality", 0.5)
        
        if coordination_quality < 0.6:
            session.adaptation_events.append(f"Low coordination quality detected: {coordination_quality:.2f}")
            logger.info(f"Adaptive adjustment triggered for session {session.session_id}")
    
    async def conduct_assessment(self, assessment_request: EducationalAssessmentRequest) -> Dict[str, Any]:
        """Conduct educational assessment"""
        session_id = assessment_request.session_id
        
        if session_id not in self.active_sessions:
            return {"success": False, "error": "Session not found"}
        
        session = self.active_sessions[session_id]
        
        try:
            coordination_request = PrimitiveCoordinationRequest(
                session_id=session_id,
                target_primitives=["meta_learning", "adaptive_reasoning", "empathetic_interaction"],
                coordination_type="assessment",
                context={
                    "assessment_type": assessment_request.assessment_type,
                    "learning_objectives": assessment_request.learning_objectives,
                    "student_id": assessment_request.student_id,
                    "educational_context": asdict(session.educational_context)
                }
            )
            
            coordination_result = await self.workflow_orchestrator.primitive_coordinator.coordinate_primitives(
                coordination_request
            )
            
            if coordination_result["success"]:
                assessment = EducationalAssessmentSchema(
                    session_id=session_id,
                    student_id=assessment_request.student_id,
                    assessment_type=assessment_request.assessment_type,
                    subject_area=session.educational_context.subject_area,
                    learning_objectives=assessment_request.learning_objectives,
                    assessment_method="ai_coordinated_assessment",
                    ai_primitives_involved=coordination_request.target_primitives,
                    overall_score=coordination_result.get("coordination_quality", 0.0),
                    assessment_confidence=coordination_result["synthesized_response"].get("confidence_score", 0.0),
                    recommendations=coordination_result["synthesized_response"].get("educational_recommendations", [])
                )
                
                self.session_assessments[session_id].append(assessment)
                
                if assessment.overall_score > 0.7:
                    session.educational_outcomes.append(EducationalOutcome.UNDERSTANDING_DEEPENED.value)
                
                return {
                    "success": True,
                    "assessment_id": assessment.assessment_id,
                    "overall_score": assessment.overall_score,
                    "recommendations": assessment.recommendations,
                    "confidence": assessment.assessment_confidence
                }
            else:
                return {"success": False, "error": "Assessment coordination failed"}
                
        except Exception as e:
            logger.error(f"Assessment failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """Get comprehensive session summary"""
        if session_id not in self.active_sessions:
            return {"success": False, "error": "Session not found"}
        
        session = self.active_sessions[session_id]
        assessments = self.session_assessments.get(session_id, [])
        pathway = self.learning_pathways.get(session_id)
        
        workflow_statuses = []
        for workflow_id in session.active_workflows:
            status = await self.workflow_orchestrator.get_workflow_status(workflow_id)
            if status["success"]:
                workflow_statuses.append(status)
        
        interaction_history = self.workflow_orchestrator.primitive_coordinator.interaction_history
        session_interactions = [i for i in interaction_history if i.workflow_id in session.active_workflows]
        
        session_effectiveness = calculate_collaboration_effectiveness(session, session_interactions)
        session.overall_effectiveness = session_effectiveness
        
        summary = {
            "success": True,
            "session_id": session_id,
            "session_overview": {
                "name": session.session_name,
                "collaboration_type": session.collaboration_type.value,
                "duration": (datetime.now() - session.started_at).total_seconds() / 60,
                "interaction_count": session.interaction_count,
                "overall_effectiveness": session_effectiveness
            },
            "educational_context": {
                "subject_area": session.educational_context.subject_area,
                "learning_objectives": session.educational_context.primary_learning_objectives,
                "learning_mode": session.educational_context.learning_mode.value
            },
            "progress": {
                "session_goals": session.session_goals,
                "achieved_outcomes": session.educational_outcomes,
                "workflow_progress": [
                    {"workflow_id": ws["workflow_id"], "progress": ws["overall_progress"]}
                    for ws in workflow_statuses
                ]
            },
            "assessments": [
                {
                    "assessment_id": a.assessment_id,
                    "type": a.assessment_type,
                    "score": a.overall_score,
                    "confidence": a.assessment_confidence
                }
                for a in assessments
            ],
            "learning_pathway": {
                "completion": pathway.completion_percentage if pathway else 0.0,
                "success_rate": pathway.success_rate if pathway else 0.0,
                "time_invested": pathway.time_invested.total_seconds() / 60 if pathway else 0.0
            } if pathway else None,
            "primitive_performance": self._analyze_primitive_performance(session_interactions),
            "recommendations": self._generate_session_recommendations(session, assessments, pathway)
        }
        
        return summary
    
    def _analyze_primitive_performance(self, interactions: List[PrimitiveInteractionSchema]) -> Dict[str, Any]:
        """Analyze performance of primitives in the session"""
        primitive_stats = defaultdict(lambda: {"interactions": 0, "successes": 0, "avg_response_time": 0.0})
        
        for interaction in interactions:
            primitive = interaction.initiating_primitive
            primitive_stats[primitive]["interactions"] += 1
            if interaction.success:
                primitive_stats[primitive]["successes"] += 1
            primitive_stats[primitive]["avg_response_time"] += interaction.response_time
            
            for target in interaction.target_primitives:
                primitive_stats[target]["interactions"] += 1
                if interaction.success:
                    primitive_stats[target]["successes"] += 1
        
        performance_summary = {}
        for primitive, stats in primitive_stats.items():
            if stats["interactions"] > 0:
                performance_summary[primitive] = {
                    "success_rate": stats["successes"] / stats["interactions"],
                    "avg_response_time": stats["avg_response_time"] / stats["interactions"],
                    "total_interactions": stats["interactions"]
                }
        
        return performance_summary
    
    def _generate_session_recommendations(self, session: CollaborationSessionSchema,
                                         assessments: List[EducationalAssessmentSchema],
                                         pathway: Optional[LearningPathwaySchema]) -> List[str]:
        """Generate recommendations for session improvement"""
        recommendations = []
        
        if session.overall_effectiveness < 0.7:
            recommendations.append("Consider adjusting collaboration approach to improve effectiveness")
        
        if session.user_engagement < 0.6:
            recommendations.append("Focus on increasing engagement through more interactive activities")
        
        if assessments:
            avg_assessment_score = np.mean([a.overall_score for a in assessments])
            if avg_assessment_score < 0.6:
                recommendations.append("Review learning objectives and provide additional support")
            elif avg_assessment_score > 0.9:
                recommendations.append("Consider increasing challenge level for advanced learning")
        
        if pathway:
            if pathway.success_rate < 0.6:
                recommendations.append("Adjust difficulty level and provide more scaffolding")
            if pathway.completion_percentage < 20 and len(pathway.collaborative_sessions) > 3:
                recommendations.append("Review learning approach and consider alternative strategies")
        
        if session.interaction_count < 5:
            recommendations.append("Encourage more active participation and interaction")
        
        return recommendations

class CollaborativeIntelligenceManager:
    """Main Collaborative Intelligence Manager - The Orchestration Hub"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or self._get_default_config()
        
        # Core components
        self.primitive_coordinator = PrimitiveCoordinator()
        self.workflow_orchestrator = EducationalWorkflowOrchestrator(self.primitive_coordinator)
        self.session_manager = EducationalSessionManager(self.workflow_orchestrator)
        
        # System state
        self.system_stats = {
            "total_sessions": 0,
            "active_sessions": 0,
            "total_interactions": 0,
            "avg_session_effectiveness": 0.0,
            "primitive_utilization": {}
        }
        
        logger.info("Collaborative Intelligence Manager initialized")
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "max_concurrent_sessions": 100,
            "session_timeout_hours": 8,
            "auto_assessment_enabled": True,
            "adaptive_adjustment_enabled": True,
            "coordination_quality_threshold": 0.7,
            "performance_monitoring_enabled": True
        }
    
    # Public API Methods
    
    async def register_primitive(self, primitive_name: str, primitive_instance: Any) -> Dict[str, Any]:
        """Register a PACT primitive for coordination"""
        try:
            await self.primitive_coordinator.register_primitive(primitive_name, primitive_instance)
            return {"success": True, "primitive": primitive_name, "status": "registered"}
        except Exception as e:
            logger.error(f"Failed to register primitive {primitive_name}: {e}")
            return {"success": False, "error": str(e)}
    
    async def initiate_educational_session(self, session_request: InitiateCollaborationRequest) -> Dict[str, Any]:
        """Initiate a new educational collaboration session"""
        try:
            result = await self.session_manager.initiate_session(session_request)
            
            if result["success"]:
                self.system_stats["total_sessions"] += 1
                self.system_stats["active_sessions"] += 1
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to initiate session: {e}")
            return {"success": False, "error": str(e)}
    
    async def process_educational_action(self, action_request: CollaborationActionRequest) -> Dict[str, Any]:
        """Process an educational action within a session"""
        try:
            result = await self.session_manager.process_session_action(action_request)
            
            if result.get("success"):
                self.system_stats["total_interactions"] += 1
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to process action: {e}")
            return {"success": False, "error": str(e)}
    
    async def coordinate_primitives(self, coordination_request: PrimitiveCoordinationRequest) -> Dict[str, Any]:
        """Coordinate multiple primitives for a specific educational task"""
        try:
            return await self.primitive_coordinator.coordinate_primitives(coordination_request)
        except Exception as e:
            logger.error(f"Primitive coordination failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def conduct_educational_assessment(self, assessment_request: EducationalAssessmentRequest) -> Dict[str, Any]:
        """Conduct educational assessment across multiple primitives"""
        try:
            return await self.session_manager.conduct_assessment(assessment_request)
        except Exception as e:
            logger.error(f"Assessment failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_session_status(self, session_id: str) -> Dict[str, Any]:
        """Get current status of an educational session"""
        try:
            return await self.session_manager.get_session_summary(session_id)
        except Exception as e:
            logger.error(f"Failed to get session status: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_system_insights(self) -> Dict[str, Any]:
        """Get insights about overall system performance"""
        try:
            interaction_history = self.primitive_coordinator.interaction_history
            active_sessions = self.session_manager.active_sessions
            
            if interaction_history:
                success_rate = sum(1 for i in interaction_history if i.success) / len(interaction_history)
                avg_response_time = np.mean([i.response_time for i in interaction_history])
            else:
                success_rate = 0.0
                avg_response_time = 0.0
            
            primitive_usage = defaultdict(int)
            for interaction in interaction_history:
                primitive_usage[interaction.initiating_primitive] += 1
                for target in interaction.target_primitives:
                    primitive_usage[target] += 1
            
            if active_sessions:
                session_effectiveness = [s.overall_effectiveness for s in active_sessions.values()]
                avg_effectiveness = np.mean(session_effectiveness)
            else:
                avg_effectiveness = 0.0
            
            return {
                "success": True,
                "system_overview": {
                    "total_sessions": self.system_stats["total_sessions"],
                    "active_sessions": len(active_sessions),
                    "total_interactions": len(interaction_history),
                    "registered_primitives": len(self.primitive_coordinator.registered_primitives)
                },
                "performance_metrics": {
                    "overall_success_rate": success_rate,
                    "avg_response_time": avg_response_time,
                    "avg_session_effectiveness": avg_effectiveness
                },
                "primitive_utilization": dict(primitive_usage),
                "recent_interactions": len([i for i in interaction_history if 
                                          (datetime.now() - i.timestamp).total_seconds() < 3600])
            }
            
        except Exception as e:
            logger.error(f"Failed to get system insights: {e}")
            return {"success": False, "error": str(e)}
    
    async def optimize_system_performance(self) -> Dict[str, Any]:
        """Optimize system performance based on current metrics"""
        try:
            optimization_results = []
            
            interaction_history = self.primitive_coordinator.interaction_history
            primitive_performance = {}
            
            for primitive_name in self.primitive_coordinator.registered_primitives:
                performance = calculate_primitive_collaboration_score(
                    primitive_name, interaction_history, []
                )
                primitive_performance[primitive_name] = performance
            
            underperforming_primitives = [
                name for name, perf in primitive_performance.items()
                if perf["overall_score"] < 0.6
            ]
            
            if underperforming_primitives:
                optimization_results.append(f"Identified {len(underperforming_primitives)} underperforming primitives")
                
                for primitive in underperforming_primitives:
                    if primitive in self.primitive_coordinator.primitive_states:
                        state = self.primitive_coordinator.primitive_states[primitive]
                        state.collaboration_readiness = 0.8
                        optimization_results.append(f"Reset collaboration readiness for {primitive}")
            
            active_workflows = self.workflow_orchestrator.active_workflows
            for workflow_id, workflow in active_workflows.items():
                overall_progress = self.workflow_orchestrator._calculate_overall_progress(workflow)
                if overall_progress < 0.3:
                    optimization_results.append(f"Flagged slow workflow: {workflow_id}")
            
            return {
                "success": True,
                "optimizations_performed": len(optimization_results),
                "optimization_details": optimization_results,
                "primitive_performance": primitive_performance
            }
            
        except Exception as e:
            logger.error(f"Optimization failed: {e}")
            return {"success": False, "error": str(e)}

# Factory function for easy initialization
async def create_collaborative_intelligence_manager(config: Optional[Dict[str, Any]] = None) -> CollaborativeIntelligenceManager:
    """Factory function to create and initialize Collaborative Intelligence Manager"""
    manager = CollaborativeIntelligenceManager(config)
    return manager

# Educational domain demo
async def demo_educational_collaboration():
    """Demonstrate collaborative intelligence for educational contexts"""
    print("=== PACT Collaborative Intelligence - Educational Demo ===\n")
    
    # Initialize the manager
    manager = await create_collaborative_intelligence_manager()
    
    # Simulate registering primitives
    print("1. Registering PACT primitives...")
    primitives_to_register = [
        "goal", "empathetic_interaction", "adaptive_reasoning", 
        "creative_synthesis", "meta_learning", "contextual_memory"
    ]
    
    for primitive_name in primitives_to_register:
        mock_primitive = type(f"Mock{primitive_name.title()}", (), {
            "process_coordination_request": lambda req: {
                "success": True, 
                "response": f"Educational response from {primitive_name}",
                "confidence": 0.8,
                "educational_value": 0.7
            }
        })()
        
        result = await manager.register_primitive(primitive_name, mock_primitive)
        print(f"   Registered {primitive_name}: {result['success']}")
    
    # Create educational collaboration context
    print("\n2. Creating educational session...")
    educational_context = create_educational_collaboration_context(
        student_profile={
            "id": "student_123",
            "name": "Alex",
            "grade_level": "10th",
            "learning_style": "visual_kinesthetic"
        },
        subject_area="Mathematics",
        learning_objectives=[
            "Understand quadratic equations",
            "Apply quadratic formula",
            "Graph quadratic functions"
        ],
        educational_context=EducationalContext.ONLINE_LEARNING,
        learning_mode=LearningMode.ADAPTIVE_INSTRUCTION
    )
    
    # Initiate session
    session_request = InitiateCollaborationRequest(
        collaboration_type=CollaborationType.STUDENT_AI,
        participants={"student_123": {"role": "student", "name": "Alex"}},
        educational_context=educational_context,
        session_goals=[
            "Master quadratic equations",
            "Build confidence in algebra",
            "Prepare for upcoming test"
        ],
        preferred_ai_primitives=["goal", "empathetic_interaction", "adaptive_reasoning", "meta_learning"]
    )
    
    session_result = await manager.initiate_educational_session(session_request)
    print(f"   Session initiated: {session_result['success']}")
    if session_result["success"]:
        session_id = session_result["session_id"]
        print(f"   Session ID: {session_id}")
    
    # Simulate educational interactions
    print("\n3. Simulating educational interactions...")
    
    educational_actions = [
        {
            "action_type": "explain_concept",
            "action_parameters": {"concept": "quadratic_equations", "difficulty": "beginner"}
        },
        {
            "action_type": "assess_understanding",
            "action_parameters": {"topic": "quadratic_formula", "assessment_type": "formative"}
        },
        {
            "action_type": "provide_feedback",
            "action_parameters": {"student_response": "I think I understand the basics", "encouragement": True}
        },
        {
            "action_type": "generate_creative_exercise",
            "action_parameters": {"topic": "quadratic_graphing", "creativity_level": "moderate"}
        }
    ]
    
    for i, action_params in enumerate(educational_actions):
        action_request = CollaborationActionRequest(
            session_id=session_id,
            requesting_participant="student_123",
            **action_params
        )
        
        action_result = await manager.process_educational_action(action_request)
        print(f"   Action {i+1} ({action_params['action_type']}): {action_result['success']}")
        if action_result["success"]:
            quality = action_result.get("coordination_result", {}).get("coordination_quality", 0.0)
            print(f"     Coordination quality: {quality:.2f}")
    
    # Conduct assessment
    print("\n4. Conducting educational assessment...")
    assessment_request = EducationalAssessmentRequest(
        session_id=session_id,
        student_id="student_123",
        assessment_type="comprehensive_review",
        learning_objectives=["Understand quadratic equations", "Apply quadratic formula"]
    )
    
    assessment_result = await manager.conduct_educational_assessment(assessment_request)
    print(f"   Assessment completed: {assessment_result['success']}")
    if assessment_result["success"]:
        print(f"   Overall score: {assessment_result['overall_score']:.2f}")
        print(f"   Recommendations: {len(assessment_result['recommendations'])}")
    
    # Get session summary
    print("\n5. Session summary:")
    summary = await manager.get_session_status(session_id)
    if summary["success"]:
        overview = summary["session_overview"]
        print(f"   Duration: {overview['duration']:.1f} minutes")
        print(f"   Interactions: {overview['interaction_count']}")
        print(f"   Effectiveness: {overview['overall_effectiveness']:.2f}")
        print(f"   Achieved outcomes: {len(summary['progress']['achieved_outcomes'])}")
    
    # Get system insights
    print("\n6. System insights:")
    insights = await manager.get_system_insights()
    if insights["success"]:
        overview = insights["system_overview"]
        performance = insights["performance_metrics"]
        print(f"   Total sessions: {overview['total_sessions']}")
        print(f"   Success rate: {performance['overall_success_rate']:.2f}")
        print(f"   Avg effectiveness: {performance['avg_session_effectiveness']:.2f}")
    
    print("\n=== Educational Demo Complete ===")

# Export main classes and functions
__all__ = [
    "CollaborativeIntelligenceManager",
    "PrimitiveCoordinator",
    "EducationalWorkflowOrchestrator", 
    "EducationalSessionManager",
    "create_collaborative_intelligence_manager",
    "demo_educational_collaboration"
]

if __name__ == "__main__":
    # Run the educational demo
    import asyncio
    asyncio.run(demo_educational_collaboration())
