# pact_hx/primitives/collaborative_intelligence/schemas.py
"""
PACT Collaborative Intelligence Primitive Schemas

The Collaborative Intelligence Orchestrator serves as the central coordination hub
for all PACT primitives, enabling seamless human-AI collaboration that feels natural,
purposeful, and effective. This is the conductor of the PACT symphony.

Educational Focus:
Designed with education domain in mind, supporting:
- Student-Teacher-AI triangular collaboration
- Adaptive learning pathway orchestration
- Multi-modal educational content coordination
- Collaborative problem-solving workflows
- Personalized learning experience management

Core Responsibilities:
- Primitive Coordination: Orchestrating interactions between all PACT primitives
- Collaboration Workflow: Managing complex multi-step educational interactions
- Context Synthesis: Combining insights from multiple primitives for coherent responses
- Educational Orchestration: Coordinating learning activities and assessments
- Adaptive Coordination: Dynamically adjusting collaboration patterns based on learning outcomes

Schema Categories:
- Collaboration Session Management
- Primitive Coordination and Communication
- Educational Workflow Orchestration
- Learning Context and State Management
- Multi-Agent Collaboration Patterns
- Educational Outcome Tracking
"""

from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any, Union, Set, Tuple
from pydantic import BaseModel, Field, validator, root_validator
from uuid import UUID, uuid4
import numpy as np

# ============================================================================
# Core Enums and Constants
# ============================================================================

class CollaborationType(str, Enum):
    """Types of collaborative interactions"""
    STUDENT_AI = "student_ai"                    # Direct student-AI collaboration
    TEACHER_AI = "teacher_ai"                    # Teacher-AI collaboration
    STUDENT_TEACHER_AI = "student_teacher_ai"    # Three-way collaboration
    PEER_AI = "peer_ai"                          # Peer-to-peer with AI facilitation
    GROUP_AI = "group_ai"                        # Group learning with AI coordination
    PARENT_STUDENT_AI = "parent_student_ai"      # Family learning collaboration
    TUTOR_STUDENT_AI = "tutor_student_ai"        # Tutoring sessions
    RESEARCH_AI = "research_ai"                  # Research collaboration

class EducationalContext(str, Enum):
    """Educational contexts for collaboration"""
    CLASSROOM = "classroom"                      # Traditional classroom setting
    ONLINE_LEARNING = "online_learning"          # Online/remote learning
    TUTORING = "tutoring"                        # One-on-one tutoring
    HOMEWORK_HELP = "homework_help"              # Homework assistance
    PROJECT_WORK = "project_work"                # Project-based learning
    ASSESSMENT = "assessment"                    # Testing and evaluation
    RESEARCH = "research"                        # Academic research
    CREATIVE_PROJECT = "creative_project"        # Creative/artistic projects
    SKILL_PRACTICE = "skill_practice"            # Skill development and practice
    EXPLORATION = "exploration"                  # Open-ended exploration

class LearningMode(str, Enum):
    """Different modes of learning collaboration"""
    GUIDED_DISCOVERY = "guided_discovery"        # AI guides student discovery
    SOCRATIC_METHOD = "socratic_method"          # Question-based learning
    COLLABORATIVE_PROBLEM_SOLVING = "collaborative_problem_solving"
    ADAPTIVE_INSTRUCTION = "adaptive_instruction" # Personalized instruction
    PEER_LEARNING = "peer_learning"              # Student-to-student learning
    EXPERIENTIAL = "experiential"                # Learning by doing
    REFLECTIVE = "reflective"                    # Reflection-based learning
    GAMIFIED = "gamified"                        # Game-based learning

class CollaborationPhase(str, Enum):
    """Phases of collaborative learning sessions"""
    INITIALIZATION = "initialization"            # Setting up collaboration
    GOAL_ALIGNMENT = "goal_alignment"            # Aligning learning goals
    EXPLORATION = "exploration"                  # Exploring topics/problems
    ANALYSIS = "analysis"                        # Deep analysis phase
    SYNTHESIS = "synthesis"                      # Combining insights
    APPLICATION = "application"                  # Applying knowledge
    REFLECTION = "reflection"                    # Reflecting on learning
    ASSESSMENT = "assessment"                    # Evaluating progress
    PLANNING = "planning"                        # Planning next steps
    COMPLETION = "completion"                    # Wrapping up session

class PrimitiveRole(str, Enum):
    """Roles that primitives can play in collaboration"""
    PRIMARY_ORCHESTRATOR = "primary_orchestrator"     # Leads the interaction
    CONTENT_PROVIDER = "content_provider"             # Provides information
    SKILL_ASSESSOR = "skill_assessor"                 # Evaluates abilities
    GOAL_MANAGER = "goal_manager"                     # Manages objectives
    CONTEXT_KEEPER = "context_keeper"                # Maintains context
    EMPATHY_PROVIDER = "empathy_provider"             # Provides emotional support
    CREATIVE_FACILITATOR = "creative_facilitator"    # Enables creativity
    REASONING_SUPPORT = "reasoning_support"          # Supports logical thinking
    ETHICS_GUARDIAN = "ethics_guardian"              # Ensures ethical behavior
    ADAPTATION_ENGINE = "adaptation_engine"          # Adapts to user needs
    EXPLANATION_GENERATOR = "explanation_generator"   # Creates explanations
    TRUST_BUILDER = "trust_builder"                  # Builds user trust

class InteractionComplexity(str, Enum):
    """Complexity levels of collaborative interactions"""
    SIMPLE = "simple"                    # Single primitive, straightforward
    MODERATE = "moderate"                # Few primitives, some coordination
    COMPLEX = "complex"                  # Multiple primitives, complex coordination
    VERY_COMPLEX = "very_complex"        # Many primitives, intricate workflows
    ADAPTIVE = "adaptive"                # Dynamically changing complexity

class EducationalOutcome(str, Enum):
    """Types of educational outcomes to track"""
    KNOWLEDGE_GAINED = "knowledge_gained"
    SKILL_DEVELOPED = "skill_developed"
    UNDERSTANDING_DEEPENED = "understanding_deepened"
    PROBLEM_SOLVED = "problem_solved"
    CREATIVITY_ENHANCED = "creativity_enhanced"
    CONFIDENCE_BUILT = "confidence_built"
    CURIOSITY_SPARKED = "curiosity_sparked"
    COLLABORATION_IMPROVED = "collaboration_improved"
    CRITICAL_THINKING = "critical_thinking"
    EMOTIONAL_GROWTH = "emotional_growth"

# ============================================================================
# Core Schema Models
# ============================================================================

class BaseCollaborationModel(BaseModel):
    """Base model for all collaboration-related schemas"""
    id: str = Field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            timedelta: lambda v: v.total_seconds(),
            np.float64: float,
            np.float32: float,
        }

class PrimitiveStateSchema(BaseModel):
    """Schema representing the state of a PACT primitive"""
    primitive_name: str = Field(..., description="Name of the primitive")
    primitive_type: str = Field(..., description="Type/category of primitive")
    current_role: PrimitiveRole = Field(..., description="Current role in collaboration")
    status: str = Field(default="active", description="Current status")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Confidence in current state")
    
    # Primitive capabilities and current state
    capabilities: Dict[str, Any] = Field(default_factory=dict, description="Available capabilities")
    current_context: Dict[str, Any] = Field(default_factory=dict, description="Current context")
    performance_metrics: Dict[str, float] = Field(default_factory=dict, description="Performance metrics")
    
    # Educational context
    educational_focus: Optional[str] = Field(None, description="Current educational focus")
    learning_objectives: List[str] = Field(default_factory=list, description="Active learning objectives")
    
    # Collaboration state
    interaction_history: List[str] = Field(default_factory=list, description="Recent interactions")
    collaboration_readiness: float = Field(default=1.0, ge=0.0, le=1.0, description="Readiness to collaborate")
    
    last_updated: datetime = Field(default_factory=datetime.now)

class EducationalCollaborationContextSchema(BaseModel):
    """Schema for educational collaboration context"""
    # Participant information
    student_profile: Dict[str, Any] = Field(default_factory=dict, description="Student characteristics")
    teacher_profile: Optional[Dict[str, Any]] = Field(None, description="Teacher characteristics")
    peer_profiles: List[Dict[str, Any]] = Field(default_factory=list, description="Peer characteristics")
    
    # Educational setting
    educational_context: EducationalContext = Field(..., description="Type of educational setting")
    subject_area: str = Field(..., description="Academic subject or domain")
    grade_level: Optional[str] = Field(None, description="Grade level or academic level")
    curriculum_standards: List[str] = Field(default_factory=list, description="Relevant curriculum standards")
    
    # Learning environment
    learning_mode: LearningMode = Field(..., description="Mode of learning")
    available_resources: List[str] = Field(default_factory=list, description="Available learning resources")
    time_constraints: Optional[timedelta] = Field(None, description="Time limitations")
    
    # Session goals and objectives
    primary_learning_objectives: List[str] = Field(..., description="Main learning goals")
    secondary_objectives: List[str] = Field(default_factory=list, description="Secondary learning goals")
    success_criteria: List[str] = Field(default_factory=list, description="How to measure success")
    
    # Adaptive factors
    learning_preferences: Dict[str, Any] = Field(default_factory=dict, description="Preferred learning styles")
    accessibility_needs: List[str] = Field(default_factory=list, description="Accessibility requirements")
    emotional_state: Optional[str] = Field(None, description="Current emotional state")
    motivation_level: float = Field(default=0.7, ge=0.0, le=1.0, description="Motivation level")

class CollaborationWorkflowSchema(BaseCollaborationModel):
    """Schema for orchestrating collaborative workflows"""
    workflow_id: str = Field(default_factory=lambda: f"workflow_{uuid4()}")
    workflow_name: str = Field(..., description="Name of the workflow")
    collaboration_type: CollaborationType = Field(..., description="Type of collaboration")
    
    # Workflow structure
    phases: List[CollaborationPhase] = Field(..., description="Phases of the workflow")
    current_phase: CollaborationPhase = Field(..., description="Current phase")
    phase_progress: Dict[str, float] = Field(default_factory=dict, description="Progress in each phase")
    
    # Primitive orchestration
    participating_primitives: List[str] = Field(..., description="Primitives involved in workflow")
    primitive_assignments: Dict[str, List[PrimitiveRole]] = Field(
        default_factory=dict, description="Role assignments for each primitive"
    )
    coordination_rules: List[Dict[str, Any]] = Field(
        default_factory=list, description="Rules for primitive coordination"
    )
    
    # Educational context
    educational_context: EducationalCollaborationContextSchema = Field(
        ..., description="Educational context for this workflow"
    )
    
    # Workflow execution
    started_at: datetime = Field(default_factory=datetime.now)
    estimated_duration: Optional[timedelta] = Field(None, description="Estimated workflow duration")
    actual_duration: Optional[timedelta] = Field(None, description="Actual duration when completed")
    
    # Adaptation and flexibility
    adaptation_triggers: List[str] = Field(default_factory=list, description="Conditions that trigger adaptation")
    fallback_strategies: List[str] = Field(default_factory=list, description="Backup plans")
    complexity_level: InteractionComplexity = Field(default=InteractionComplexity.MODERATE)
    
    # Outcomes and assessment
    target_outcomes: List[EducationalOutcome] = Field(..., description="Desired educational outcomes")
    achieved_outcomes: List[str] = Field(default_factory=list, description="Outcomes achieved so far")
    success_metrics: Dict[str, float] = Field(default_factory=dict, description="Success measurements")

class PrimitiveInteractionSchema(BaseCollaborationModel):
    """Schema for interactions between primitives"""
    interaction_id: str = Field(default_factory=lambda: f"interaction_{uuid4()}")
    workflow_id: str = Field(..., description="Associated workflow ID")
    
    # Interaction participants
    initiating_primitive: str = Field(..., description="Primitive that initiated interaction")
    target_primitives: List[str] = Field(..., description="Primitives being interacted with")
    interaction_type: str = Field(..., description="Type of interaction")
    
    # Interaction content
    request_payload: Dict[str, Any] = Field(..., description="Data sent in interaction")
    response_payload: Dict[str, Any] = Field(default_factory=dict, description="Response data")
    context_shared: Dict[str, Any] = Field(default_factory=dict, description="Shared context")
    
    # Educational relevance
    educational_purpose: str = Field(..., description="Educational purpose of interaction")
    learning_impact: Optional[str] = Field(None, description="Expected impact on learning")
    
    # Execution details
    initiated_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = Field(None, description="When interaction completed")
    success: bool = Field(default=True, description="Whether interaction succeeded")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    
    # Quality metrics
    response_time: float = Field(default=0.0, ge=0.0, description="Response time in seconds")
    accuracy: float = Field(default=1.0, ge=0.0, le=1.0, description="Accuracy of interaction")
    user_satisfaction: Optional[float] = Field(None, ge=0.0, le=1.0, description="User satisfaction")

class CollaborationSessionSchema(BaseCollaborationModel):
    """Schema for complete collaboration sessions"""
    session_id: str = Field(default_factory=lambda: f"session_{uuid4()}")
    session_name: Optional[str] = Field(None, description="Human-readable session name")
    
    # Session participants
    participants: Dict[str, Any] = Field(..., description="Human participants in session")
    ai_participants: List[str] = Field(..., description="AI primitives participating")
    collaboration_type: CollaborationType = Field(..., description="Type of collaboration")
    
    # Session structure
    active_workflows: List[str] = Field(default_factory=list, description="Currently active workflows")
    completed_workflows: List[str] = Field(default_factory=list, description="Completed workflows")
    session_goals: List[str] = Field(..., description="Overall session goals")
    
    # Educational context
    educational_context: EducationalCollaborationContextSchema = Field(
        ..., description="Educational context for session"
    )
    
    # Session timeline
    started_at: datetime = Field(default_factory=datetime.now)
    scheduled_end: Optional[datetime] = Field(None, description="Scheduled end time")
    actual_end: Optional[datetime] = Field(None, description="Actual end time")
    
    # Session dynamics
    interaction_count: int = Field(default=0, ge=0, description="Number of interactions")
    phase_transitions: List[str] = Field(default_factory=list, description="Phase transition history")
    adaptation_events: List[str] = Field(default_factory=list, description="Adaptation events")
    
    # Quality and outcomes
    overall_effectiveness: float = Field(default=0.0, ge=0.0, le=1.0, description="Overall effectiveness")
    learning_progress: Dict[str, float] = Field(default_factory=dict, description="Learning progress metrics")
    user_engagement: float = Field(default=0.0, ge=0.0, le=1.0, description="User engagement level")
    educational_outcomes: List[str] = Field(default_factory=list, description="Educational outcomes achieved")

# ============================================================================
# Specialized Educational Schemas
# ============================================================================

class LearningPathwaySchema(BaseCollaborationModel):
    """Schema for adaptive learning pathway management"""
    pathway_id: str = Field(default_factory=lambda: f"pathway_{uuid4()}")
    student_id: str = Field(..., description="Student identifier")
    subject_area: str = Field(..., description="Academic subject")
    
    # Pathway structure
    learning_objectives: List[str] = Field(..., description="Learning objectives for pathway")
    milestones: List[Dict[str, Any]] = Field(..., description="Key milestones and checkpoints")
    current_milestone: str = Field(..., description="Current milestone")
    
    # Adaptive elements
    difficulty_level: float = Field(default=0.5, ge=0.0, le=1.0, description="Current difficulty level")
    pacing: str = Field(default="moderate", description="Learning pace")
    preferred_modalities: List[str] = Field(default_factory=list, description="Preferred learning modalities")
    
    # Progress tracking
    completion_percentage: float = Field(default=0.0, ge=0.0, le=100.0, description="Pathway completion")
    time_invested: timedelta = Field(default=timedelta(0), description="Time spent on pathway")
    success_rate: float = Field(default=0.0, ge=0.0, le=1.0, description="Success rate on activities")
    
    # Collaboration history
    collaborative_sessions: List[str] = Field(default_factory=list, description="Associated collaboration sessions")
    ai_support_sessions: List[str] = Field(default_factory=list, description="AI support sessions")
    
    # Personalization
    learning_style_profile: Dict[str, Any] = Field(default_factory=dict, description="Learning style information")
    strength_areas: List[str] = Field(default_factory=list, description="Student's strength areas")
    improvement_areas: List[str] = Field(default_factory=list, description="Areas for improvement")
    
    last_updated: datetime = Field(default_factory=datetime.now)

class EducationalAssessmentSchema(BaseCollaborationModel):
    """Schema for educational assessments and evaluations"""
    assessment_id: str = Field(default_factory=lambda: f"assessment_{uuid4()}")
    session_id: str = Field(..., description="Associated collaboration session")
    student_id: str = Field(..., description="Student being assessed")
    
    # Assessment details
    assessment_type: str = Field(..., description="Type of assessment")
    subject_area: str = Field(..., description="Academic subject being assessed")
    learning_objectives: List[str] = Field(..., description="Learning objectives being evaluated")
    
    # Assessment methodology
    assessment_method: str = Field(..., description="How assessment was conducted")
    ai_primitives_involved: List[str] = Field(..., description="AI primitives that contributed to assessment")
    human_evaluators: List[str] = Field(default_factory=list, description="Human evaluators involved")
    
    # Results and scores
    overall_score: float = Field(..., ge=0.0, le=1.0, description="Overall assessment score")
    objective_scores: Dict[str, float] = Field(default_factory=dict, description="Scores per learning objective")
    skill_assessments: Dict[str, float] = Field(default_factory=dict, description="Skill-specific assessments")
    
    # Qualitative feedback
    strengths_identified: List[str] = Field(default_factory=list, description="Identified strengths")
    areas_for_improvement: List[str] = Field(default_factory=list, description="Areas needing improvement")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations for next steps")
    
    # Assessment quality
    assessment_confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Confidence in assessment")
    assessment_fairness: float = Field(default=1.0, ge=0.0, le=1.0, description="Fairness of assessment")
    bias_check_results: Dict[str, Any] = Field(default_factory=dict, description="Bias analysis results")
    
    assessed_at: datetime = Field(default_factory=datetime.now)

class CollaborativeProblemSolvingSchema(BaseCollaborationModel):
    """Schema for collaborative problem-solving activities"""
    problem_id: str = Field(default_factory=lambda: f"problem_{uuid4()}")
    session_id: str = Field(..., description="Associated collaboration session")
    
    # Problem definition
    problem_statement: str = Field(..., description="Clear statement of the problem")
    problem_type: str = Field(..., description="Type/category of problem")
    complexity_level: InteractionComplexity = Field(..., description="Problem complexity")
    subject_domain: str = Field(..., description="Academic domain of problem")
    
    # Problem-solving process
    solution_approach: str = Field(..., description="Approach being used to solve problem")
    steps_planned: List[str] = Field(..., description="Planned solution steps")
    steps_completed: List[str] = Field(default_factory=list, description="Completed steps")
    current_step: Optional[str] = Field(None, description="Current step being worked on")
    
    # Collaboration dynamics
    participant_roles: Dict[str, str] = Field(..., description="Roles of each participant")
    ai_contributions: List[str] = Field(default_factory=list, description="Ways AI is contributing")
    human_contributions: List[str] = Field(default_factory=list, description="Ways humans are contributing")
    
    # Problem-solving progress
    progress_percentage: float = Field(default=0.0, ge=0.0, le=100.0, description="Progress toward solution")
    obstacles_encountered: List[str] = Field(default_factory=list, description="Obstacles faced")
    breakthroughs_achieved: List[str] = Field(default_factory=list, description="Key breakthroughs")
    
    # Solution quality
    solution_found: bool = Field(default=False, description="Whether solution was found")
    solution_quality: Optional[float] = Field(None, ge=0.0, le=1.0, description="Quality of solution")
    solution_creativity: Optional[float] = Field(None, ge=0.0, le=1.0, description="Creativity of solution")
    learning_achieved: List[str] = Field(default_factory=list, description="Learning outcomes from process")
    
    started_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = Field(None, description="When problem solving completed")

# ============================================================================
# Request/Response Schemas for API
# ============================================================================

class InitiateCollaborationRequest(BaseModel):
    """Request to initiate a new collaboration session"""
    collaboration_type: CollaborationType = Field(..., description="Type of collaboration")
    participants: Dict[str, Any] = Field(..., description="Human participants")
    educational_context: EducationalCollaborationContextSchema = Field(..., description="Educational context")
    session_goals: List[str] = Field(..., description="Goals for the session")
    preferred_ai_primitives: Optional[List[str]] = Field(None, description="Preferred AI primitives")
    time_limit: Optional[timedelta] = Field(None, description="Session time limit")
    special_requirements: List[str] = Field(default_factory=list, description="Special requirements")

class CollaborationActionRequest(BaseModel):
    """Request to perform an action within a collaboration"""
    session_id: str = Field(..., description="Target session ID")
    action_type: str = Field(..., description="Type of action to perform")
    action_parameters: Dict[str, Any] = Field(default_factory=dict, description="Action parameters")
    requesting_participant: str = Field(..., description="Who is requesting the action")
    priority: str = Field(default="normal", description="Action priority")
    expected_outcome: Optional[str] = Field(None, description="Expected outcome of action")

class PrimitiveCoordinationRequest(BaseModel):
    """Request to coordinate specific primitives"""
    session_id: str = Field(..., description="Target session ID")
    target_primitives: List[str] = Field(..., description="Primitives to coordinate")
    coordination_type: str = Field(..., description="Type of coordination needed")
    context: Dict[str, Any] = Field(..., description="Context for coordination")
    expected_roles: Dict[str, List[PrimitiveRole]] = Field(default_factory=dict, description="Expected primitive roles")

class EducationalAssessmentRequest(BaseModel):
    """Request for educational assessment"""
    session_id: str = Field(..., description="Session to assess")
    student_id: str = Field(..., description="Student to assess")
    assessment_type: str = Field(..., description="Type of assessment")
    learning_objectives: List[str] = Field(..., description="Objectives to assess")
    assessment_criteria: List[str] = Field(default_factory=list, description="Assessment criteria")
    include_recommendations: bool = Field(default=True, description="Include improvement recommendations")

class LearningPathwayRequest(BaseModel):
    """Request for learning pathway management"""
    student_id: str = Field(..., description="Target student")
    subject_area: str = Field(..., description="Academic subject")
    current_level: Optional[str] = Field(None, description="Current skill level")
    learning_goals: List[str] = Field(..., description="Learning goals")
    time_frame: Optional[timedelta] = Field(None, description="Desired time frame")
    preferences: Dict[str, Any] = Field(default_factory=dict, description="Learning preferences")

# ============================================================================
# Factory Functions and Utilities
# ============================================================================

def create_educational_collaboration_context(
    student_profile: Dict[str, Any],
    subject_area: str,
    learning_objectives: List[str],
    **kwargs
) -> EducationalCollaborationContextSchema:
    """Factory function to create educational collaboration context"""
    return EducationalCollaborationContextSchema(
        student_profile=student_profile,
        educational_context=kwargs.get("educational_context", EducationalContext.ONLINE_LEARNING),
        subject_area=subject_area,
        learning_mode=kwargs.get("learning_mode", LearningMode.ADAPTIVE_INSTRUCTION),
        primary_learning_objectives=learning_objectives,
        **kwargs
    )

def create_collaboration_workflow(
    workflow_name: str,
    collaboration_type: CollaborationType,
    educational_context: EducationalCollaborationContextSchema,
    participating_primitives: List[str],
    **kwargs
) -> CollaborationWorkflowSchema:
    """Factory function to create collaboration workflow"""
    default_phases = [
        CollaborationPhase.INITIALIZATION,
        CollaborationPhase.GOAL_ALIGNMENT,
        CollaborationPhase.EXPLORATION,
        CollaborationPhase.APPLICATION,
        CollaborationPhase.REFLECTION
    ]
    
    return CollaborationWorkflowSchema(
        workflow_name=workflow_name,
        collaboration_type=collaboration_type,
        phases=kwargs.get("phases", default_phases),
        current_phase=CollaborationPhase.INITIALIZATION,
        participating_primitives=participating_primitives,
        educational_context=educational_context,
        target_outcomes=kwargs.get("target_outcomes", [EducationalOutcome.KNOWLEDGE_GAINED]),
        **kwargs
    )

def create_primitive_state(
    primitive_name: str,
    primitive_type: str,
    current_role: PrimitiveRole,
    **kwargs
) -> PrimitiveStateSchema:
    """Factory function to create primitive state"""
    return PrimitiveStateSchema(
        primitive_name=primitive_name,
        primitive_type=primitive_type,
        current_role=current_role,
        **kwargs
    )

# ============================================================================
# Validation and Helper Functions
# ============================================================================

def validate_collaboration_workflow(workflow: CollaborationWorkflowSchema) -> List[str]:
    """Validate collaboration workflow consistency"""
    errors = []
    
    # Check phase consistency
    if workflow.current_phase not in workflow.phases:
        errors.append("Current phase not in workflow phases")
    
    # Check primitive assignments
    for primitive in workflow.participating_primitives:
        if primitive not in workflow.primitive_assignments:
            errors.append(f"No role assignment for primitive: {primitive}")
    
    # Check educational context alignment
    if not workflow.educational_context.primary_learning_objectives:
        errors.append("No primary learning objectives specified")
    
    # Check outcome alignment
    if not workflow.target_outcomes:
        errors.append("No target outcomes specified")
    
    return errors

def calculate_collaboration_effectiveness(
    session: CollaborationSessionSchema,
    interactions: List[PrimitiveInteractionSchema]
) -> float:
    """Calculate overall collaboration effectiveness"""
    if not interactions:
        return 0.0
    
    # Factor 1: Interaction success rate
    successful_interactions = sum(1 for i in interactions if i.success)
    success_rate = successful_interactions / len(interactions)
    
    # Factor 2: Response time efficiency
    avg_response_time = np.mean([i.response_time for i in interactions])
    time_efficiency = max(0.0, 1.0 - (avg_response_time / 10.0))  # Assume 10s is poor
    
    # Factor 3: User satisfaction
    satisfaction_scores = [i.user_satisfaction for i in interactions if i.user_satisfaction is not None]
    avg_satisfaction = np.mean(satisfaction_scores) if satisfaction_scores else 0.7
    
    # Factor 4: Educational outcome achievement
    outcome_score = len(session.educational_outcomes) / max(1, len(session.session_goals))
    outcome_score = min(1.0, outcome_score)
    
    # Weighted combination
    effectiveness = (
        0.3 * success_rate +
        0.2 * time_efficiency +
        0.3 * avg_satisfaction +
        0.2 * outcome_score
    )
    
    return min(1.0, max(0.0, effectiveness))

def suggest_primitive_roles(
    collaboration_type: CollaborationType,
    educational_context: EducationalCollaborationContextSchema,
    available_primitives: List[str]
) -> Dict[str, List[PrimitiveRole]]:
    """Suggest optimal primitive role assignments"""
    role_suggestions = {}
    
    # Base role assignments for common primitives
    base_assignments = {
        "goal": [PrimitiveRole.GOAL_MANAGER],
        "empathetic_interaction": [PrimitiveRole.EMPATHY_PROVIDER, PrimitiveRole.TRUST_BUILDER],
        "adaptive_reasoning": [PrimitiveRole.REASONING_SUPPORT],
        "creative_synthesis": [PrimitiveRole.CREATIVE_FACILITATOR],
def suggest_primitive_roles(
    collaboration_type: CollaborationType,
    educational_context: EducationalCollaborationContextSchema,
    available_primitives: List[str]
) -> Dict[str, List[PrimitiveRole]]:
    """Suggest optimal primitive role assignments"""
    role_suggestions = {}
    
    # Base role assignments for common primitives
    base_assignments = {
        "goal": [PrimitiveRole.GOAL_MANAGER],
        "empathetic_interaction": [PrimitiveRole.EMPATHY_PROVIDER, PrimitiveRole.TRUST_BUILDER],
        "adaptive_reasoning": [PrimitiveRole.REASONING_SUPPORT],
        "creative_synthesis": [PrimitiveRole.CREATIVE_FACILITATOR],
        "contextual_memory": [PrimitiveRole.CONTEXT_KEEPER],
        "value_alignment": [PrimitiveRole.ETHICS_GUARDIAN],
        "explainable_ai": [PrimitiveRole.EXPLANATION_GENERATOR],
        "continuous_adaptation": [PrimitiveRole.ADAPTATION_ENGINE],
        "meta_learning": [PrimitiveRole.SKILL_ASSESSOR],
        "collaborative_intelligence": [PrimitiveRole.PRIMARY_ORCHESTRATOR]
    }
    
    # Assign base roles
    for primitive in available_primitives:
        if primitive in base_assignments:
            role_suggestions[primitive] = base_assignments[primitive].copy()
        else:
            role_suggestions[primitive] = [PrimitiveRole.CONTENT_PROVIDER]
    
    # Adjust based on collaboration type
    if collaboration_type == CollaborationType.STUDENT_AI:
        # Student-AI collaboration emphasizes personalization and support
        if "empathetic_interaction" in role_suggestions:
            role_suggestions["empathetic_interaction"].append(PrimitiveRole.PRIMARY_ORCHESTRATOR)
        if "adaptive_reasoning" in role_suggestions:
            role_suggestions["adaptive_reasoning"].append(PrimitiveRole.CONTENT_PROVIDER)
    
    elif collaboration_type == CollaborationType.TEACHER_AI:
        # Teacher-AI collaboration emphasizes assessment and planning
        if "meta_learning" in role_suggestions:
            role_suggestions["meta_learning"].extend([PrimitiveRole.SKILL_ASSESSOR, PrimitiveRole.CONTENT_PROVIDER])
        if "goal" in role_suggestions:
            role_suggestions["goal"].append(PrimitiveRole.CONTENT_PROVIDER)
    
    elif collaboration_type == CollaborationType.GROUP_AI:
        # Group collaboration emphasizes coordination and facilitation
        if "collaborative_intelligence" in role_suggestions:
            role_suggestions["collaborative_intelligence"].append(PrimitiveRole.CONTENT_PROVIDER)
        if "creative_synthesis" in role_suggestions:
            role_suggestions["creative_synthesis"].append(PrimitiveRole.PRIMARY_ORCHESTRATOR)
    
    # Adjust based on learning mode
    if educational_context.learning_mode == LearningMode.SOCRATIC_METHOD:
        if "adaptive_reasoning" in role_suggestions:
            role_suggestions["adaptive_reasoning"].append(PrimitiveRole.PRIMARY_ORCHESTRATOR)
    
    elif educational_context.learning_mode == LearningMode.CREATIVE_PROJECT:
        if "creative_synthesis" in role_suggestions:
            role_suggestions["creative_synthesis"].append(PrimitiveRole.PRIMARY_ORCHESTRATOR)
    
    elif educational_context.learning_mode == LearningMode.COLLABORATIVE_PROBLEM_SOLVING:
        if "collaborative_intelligence" in role_suggestions:
            role_suggestions["collaborative_intelligence"].append(PrimitiveRole.PRIMARY_ORCHESTRATOR)
    
    return role_suggestions

def analyze_educational_effectiveness(
    session: CollaborationSessionSchema,
    assessments: List[EducationalAssessmentSchema],
    pathways: List[LearningPathwaySchema]
) -> Dict[str, Any]:
    """Analyze educational effectiveness of collaboration"""
    analysis = {
        "overall_effectiveness": 0.0,
        "learning_progress": {},
        "engagement_metrics": {},
        "outcome_achievement": {},
        "recommendations": []
    }
    
    if not assessments:
        return analysis
    
    # Calculate learning progress
    avg_scores = {}
    for assessment in assessments:
        for objective, score in assessment.objective_scores.items():
            if objective not in avg_scores:
                avg_scores[objective] = []
            avg_scores[objective].append(score)
    
    for objective, scores in avg_scores.items():
        analysis["learning_progress"][objective] = {
            "average_score": np.mean(scores),
            "improvement": scores[-1] - scores[0] if len(scores) > 1 else 0.0,
            "consistency": 1.0 - np.std(scores) if len(scores) > 1 else 1.0
        }
    
    # Analyze engagement
    analysis["engagement_metrics"] = {
        "session_duration": session.actual_end - session.started_at if session.actual_end else None,
        "interaction_frequency": session.interaction_count / max(1, len(session.active_workflows)),
        "user_engagement": session.user_engagement,
        "adaptation_responsiveness": len(session.adaptation_events)
    }
    
    # Outcome achievement analysis
    total_outcomes = len(session.session_goals)
    achieved_outcomes = len(session.educational_outcomes)
    analysis["outcome_achievement"] = {
        "completion_rate": achieved_outcomes / max(1, total_outcomes),
        "quality_score": np.mean([a.overall_score for a in assessments]),
        "outcome_types": list(set(session.educational_outcomes))
    }
    
    # Overall effectiveness
    progress_score = np.mean([p["average_score"] for p in analysis["learning_progress"].values()]) if analysis["learning_progress"] else 0.5
    engagement_score = session.user_engagement
    achievement_score = analysis["outcome_achievement"]["completion_rate"]
    
    analysis["overall_effectiveness"] = (
        0.4 * progress_score +
        0.3 * engagement_score +
        0.3 * achievement_score
    )
    
    # Generate recommendations
    if analysis["overall_effectiveness"] < 0.6:
        analysis["recommendations"].append("Consider adjusting collaboration approach for better engagement")
    
    if engagement_score < 0.5:
        analysis["recommendations"].append("Focus on improving user engagement through more interactive activities")
    
    if achievement_score < 0.7:
        analysis["recommendations"].append("Review learning objectives and ensure they are achievable and well-defined")
    
    return analysis

def optimize_primitive_coordination(
    current_assignments: Dict[str, List[PrimitiveRole]],
    performance_metrics: Dict[str, Dict[str, float]],
    educational_goals: List[str]
) -> Dict[str, List[PrimitiveRole]]:
    """Optimize primitive role assignments based on performance"""
    optimized_assignments = current_assignments.copy()
    
    # Identify underperforming primitives
    underperformers = []
    for primitive, metrics in performance_metrics.items():
        avg_performance = np.mean(list(metrics.values()))
        if avg_performance < 0.6:  # Performance threshold
            underperformers.append(primitive)
    
    # Redistribute roles from underperformers
    for primitive in underperformers:
        if primitive in optimized_assignments:
            roles = optimized_assignments[primitive]
            
            # Remove non-essential roles
            essential_roles = [PrimitiveRole.PRIMARY_ORCHESTRATOR, PrimitiveRole.ETHICS_GUARDIAN]
            optimized_assignments[primitive] = [r for r in roles if r in essential_roles]
            
            # Redistribute removed roles to better performers
            removed_roles = [r for r in roles if r not in essential_roles]
            for role in removed_roles:
                # Find best performer for this role
                best_primitive = max(
                    performance_metrics.keys(),
                    key=lambda p: performance_metrics[p].get("effectiveness", 0.0)
                )
                if best_primitive != primitive:
                    optimized_assignments[best_primitive].append(role)
    
    return optimized_assignments

# ============================================================================
# Educational Domain Specific Helpers
# ============================================================================

class EducationalCollaborationPatterns:
    """Predefined collaboration patterns for educational contexts"""
    
    @staticmethod
    def get_socratic_dialogue_pattern() -> Dict[str, Any]:
        """Pattern for Socratic method teaching"""
        return {
            "phases": [
                CollaborationPhase.INITIALIZATION,
                CollaborationPhase.EXPLORATION,
                CollaborationPhase.ANALYSIS,
                CollaborationPhase.SYNTHESIS,
                CollaborationPhase.REFLECTION
            ],
            "primitive_roles": {
                "adaptive_reasoning": [PrimitiveRole.PRIMARY_ORCHESTRATOR, PrimitiveRole.REASONING_SUPPORT],
                "empathetic_interaction": [PrimitiveRole.EMPATHY_PROVIDER],
                "goal": [PrimitiveRole.GOAL_MANAGER],
                "contextual_memory": [PrimitiveRole.CONTEXT_KEEPER]
            },
            "interaction_rules": [
                "Ask probing questions rather than providing direct answers",
                "Guide student to discover answers through reasoning",
                "Provide encouragement and support throughout process",
                "Help student reflect on learning process"
            ]
        }
    
    @staticmethod
    def get_collaborative_project_pattern() -> Dict[str, Any]:
        """Pattern for collaborative project work"""
        return {
            "phases": [
                CollaborationPhase.INITIALIZATION,
                CollaborationPhase.GOAL_ALIGNMENT,
                CollaborationPhase.PLANNING,
                CollaborationPhase.APPLICATION,
                CollaborationPhase.SYNTHESIS,
                CollaborationPhase.ASSESSMENT
            ],
            "primitive_roles": {
                "collaborative_intelligence": [PrimitiveRole.PRIMARY_ORCHESTRATOR],
                "creative_synthesis": [PrimitiveRole.CREATIVE_FACILITATOR],
                "goal": [PrimitiveRole.GOAL_MANAGER],
                "adaptive_reasoning": [PrimitiveRole.REASONING_SUPPORT],
                "meta_learning": [PrimitiveRole.SKILL_ASSESSOR]
            },
            "interaction_rules": [
                "Facilitate equal participation from all members",
                "Encourage creative problem-solving approaches",
                "Monitor progress toward project goals",
                "Provide feedback and guidance as needed"
            ]
        }
    
    @staticmethod
    def get_personalized_tutoring_pattern() -> Dict[str, Any]:
        """Pattern for one-on-one personalized tutoring"""
        return {
            "phases": [
                CollaborationPhase.INITIALIZATION,
                CollaborationPhase.ASSESSMENT,
                CollaborationPhase.GOAL_ALIGNMENT,
                CollaborationPhase.APPLICATION,
                CollaborationPhase.REFLECTION
            ],
            "primitive_roles": {
                "empathetic_interaction": [PrimitiveRole.PRIMARY_ORCHESTRATOR, PrimitiveRole.EMPATHY_PROVIDER],
                "adaptive_reasoning": [PrimitiveRole.REASONING_SUPPORT],
                "meta_learning": [PrimitiveRole.SKILL_ASSESSOR],
                "goal": [PrimitiveRole.GOAL_MANAGER],
                "continuous_adaptation": [PrimitiveRole.ADAPTATION_ENGINE]
            },
            "interaction_rules": [
                "Adapt to student's learning pace and style",
                "Provide personalized feedback and encouragement",
                "Monitor emotional state and adjust approach",
                "Focus on building confidence and understanding"
            ]
        }
    
    @staticmethod
    def get_pattern_for_context(
        collaboration_type: CollaborationType,
        learning_mode: LearningMode,
        educational_context: EducationalContext
    ) -> Dict[str, Any]:
        """Get the most appropriate pattern for given context"""
        
        # Pattern selection logic
        if learning_mode == LearningMode.SOCRATIC_METHOD:
            return EducationalCollaborationPatterns.get_socratic_dialogue_pattern()
        
        elif learning_mode == LearningMode.COLLABORATIVE_PROBLEM_SOLVING:
            return EducationalCollaborationPatterns.get_collaborative_project_pattern()
        
        elif collaboration_type == CollaborationType.STUDENT_AI and educational_context == EducationalContext.TUTORING:
            return EducationalCollaborationPatterns.get_personalized_tutoring_pattern()
        
        else:
            # Default adaptive pattern
            return {
                "phases": [
                    CollaborationPhase.INITIALIZATION,
                    CollaborationPhase.GOAL_ALIGNMENT,
                    CollaborationPhase.APPLICATION,
                    CollaborationPhase.REFLECTION
                ],
                "primitive_roles": {
                    "collaborative_intelligence": [PrimitiveRole.PRIMARY_ORCHESTRATOR],
                    "empathetic_interaction": [PrimitiveRole.EMPATHY_PROVIDER],
                    "adaptive_reasoning": [PrimitiveRole.REASONING_SUPPORT],
                    "goal": [PrimitiveRole.GOAL_MANAGER]
                },
                "interaction_rules": [
                    "Adapt to user needs and preferences",
                    "Maintain focus on learning objectives",
                    "Provide appropriate level of challenge",
                    "Encourage active participation"
                ]
            }

# ============================================================================
# Performance and Quality Metrics
# ============================================================================

def calculate_primitive_collaboration_score(
    primitive_name: str,
    interactions: List[PrimitiveInteractionSchema],
    role_assignments: List[PrimitiveRole]
) -> Dict[str, float]:
    """Calculate collaboration effectiveness score for a primitive"""
    if not interactions:
        return {"overall_score": 0.0}
    
    primitive_interactions = [i for i in interactions if 
                            primitive_name == i.initiating_primitive or 
                            primitive_name in i.target_primitives]
    
    if not primitive_interactions:
        return {"overall_score": 0.0}
    
    # Calculate various performance metrics
    success_rate = sum(1 for i in primitive_interactions if i.success) / len(primitive_interactions)
    avg_response_time = np.mean([i.response_time for i in primitive_interactions])
    avg_accuracy = np.mean([i.accuracy for i in primitive_interactions])
    
    # User satisfaction (if available)
    satisfaction_scores = [i.user_satisfaction for i in primitive_interactions if i.user_satisfaction is not None]
    avg_satisfaction = np.mean(satisfaction_scores) if satisfaction_scores else 0.7
    
    # Role fulfillment assessment (simplified)
    role_performance = 0.8  # Would be calculated based on specific role expectations
    
    # Overall collaboration score
    overall_score = (
        0.25 * success_rate +
        0.20 * min(1.0, max(0.0, 1.0 - avg_response_time / 5.0)) +  # Response time factor
        0.25 * avg_accuracy +
        0.20 * avg_satisfaction +
        0.10 * role_performance
    )
    
    return {
        "overall_score": overall_score,
        "success_rate": success_rate,
        "response_time": avg_response_time,
        "accuracy": avg_accuracy,
        "user_satisfaction": avg_satisfaction,
        "role_performance": role_performance
    }

def generate_collaboration_insights(
    session: CollaborationSessionSchema,
    workflows: List[CollaborationWorkflowSchema],
    interactions: List[PrimitiveInteractionSchema]
) -> Dict[str, Any]:
    """Generate insights about collaboration effectiveness"""
    insights = {
        "session_summary": {},
        "workflow_analysis": {},
        "primitive_performance": {},
        "educational_impact": {},
        "recommendations": []
    }
    
    # Session summary
    session_duration = (session.actual_end - session.started_at) if session.actual_end else datetime.now() - session.started_at
    insights["session_summary"] = {
        "duration": session_duration.total_seconds() / 60,  # minutes
        "total_interactions": len(interactions),
        "workflows_completed": len(session.completed_workflows),
        "overall_effectiveness": session.overall_effectiveness,
        "user_engagement": session.user_engagement
    }
    
    # Workflow analysis
    for workflow in workflows:
        workflow_interactions = [i for i in interactions if i.workflow_id == workflow.workflow_id]
        insights["workflow_analysis"][workflow.workflow_id] = {
            "completion_status": "completed" if workflow.workflow_id in session.completed_workflows else "active",
            "phase_progress": workflow.phase_progress,
            "interaction_count": len(workflow_interactions),
            "success_rate": sum(1 for i in workflow_interactions if i.success) / max(1, len(workflow_interactions))
        }
    
    # Primitive performance analysis
    all_primitives = set()
    for interaction in interactions:
        all_primitives.add(interaction.initiating_primitive)
        all_primitives.update(interaction.target_primitives)
    
    for primitive in all_primitives:
        role_assignments = []  # Would get from workflow data
        insights["primitive_performance"][primitive] = calculate_primitive_collaboration_score(
            primitive, interactions, role_assignments
        )
    
    # Educational impact assessment
    insights["educational_impact"] = {
        "learning_objectives_addressed": len(session.session_goals),
        "educational_outcomes_achieved": len(session.educational_outcomes),
        "estimated_learning_gain": session.learning_progress,
        "engagement_level": session.user_engagement
    }
    
    # Generate recommendations
    if session.overall_effectiveness < 0.7:
        insights["recommendations"].append("Consider adjusting primitive coordination to improve effectiveness")
    
    if session.user_engagement < 0.6:
        insights["recommendations"].append("Focus on increasing user engagement through more interactive elements")
    
    avg_primitive_performance = np.mean([p["overall_score"] for p in insights["primitive_performance"].values()])
    if avg_primitive_performance < 0.7:
        insights["recommendations"].append("Review primitive performance and consider role reassignments")
    
    return insights

# ============================================================================
# Export All Schemas and Functions
# ============================================================================

__all__ = [
    # Enums
    "CollaborationType", "EducationalContext", "LearningMode", "CollaborationPhase",
    "PrimitiveRole", "InteractionComplexity", "EducationalOutcome",
    
    # Core Schemas
    "BaseCollaborationModel", "PrimitiveStateSchema", "EducationalCollaborationContextSchema",
    "CollaborationWorkflowSchema", "PrimitiveInteractionSchema", "CollaborationSessionSchema",
    
    # Educational Schemas
    "LearningPathwaySchema", "EducationalAssessmentSchema", "CollaborativeProblemSolvingSchema",
    
    # Request/Response Schemas
    "InitiateCollaborationRequest", "CollaborationActionRequest", "PrimitiveCoordinationRequest",
    "EducationalAssessmentRequest", "LearningPathwayRequest",
    
    # Factory Functions
    "create_educational_collaboration_context", "create_collaboration_workflow", "create_primitive_state",
    
    # Validation and Analysis Functions
    "validate_collaboration_workflow", "calculate_collaboration_effectiveness", "suggest_primitive_roles",
    "analyze_educational_effectiveness", "optimize_primitive_coordination",
    
    # Educational Patterns
    "EducationalCollaborationPatterns",
    
    # Performance and Quality Functions
    "calculate_primitive_collaboration_score", "generate_collaboration_insights"
]
