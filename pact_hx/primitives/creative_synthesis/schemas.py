# pact_hx/primitives/creative_synthesis/schemas.py
"""
PACT Creative Synthesis Engine Schemas

The Creative Synthesis Engine transforms educational content into engaging, memorable,
and innovative learning experiences. It's the imagination engine that makes learning
feel like an adventure rather than a chore.

Educational Mission:
Every concept can be made engaging. Every problem can become a story. Every lesson
can spark curiosity. The Creative Synthesis Engine believes that creativity is not
just about arts - it's about making connections, seeing patterns, and approaching
challenges from unexpected angles.

Core Creative Responsibilities:
- Content Transformation: Turn dry concepts into engaging narratives and activities
- Multi-Modal Learning: Create visual, auditory, kinesthetic, and interactive experiences
- Metaphor Generation: Find powerful analogies and metaphors for complex concepts
- Story-Based Learning: Embed learning objectives in compelling narratives
- Creative Problem-Solving: Generate multiple innovative approaches to challenges
- Personalized Content: Adapt creative content to individual interests and learning styles
- Gamification: Transform learning activities into engaging game-like experiences

Creative Philosophy:
Creativity in education isn't about making things "fun" for fun's sake - it's about:
- Making abstract concepts concrete and relatable
- Creating emotional connections to learning material
- Stimulating curiosity and wonder
- Encouraging divergent thinking and exploration
- Building confidence through creative expression
- Making learning memorable through unique experiences

Integration with Educational Goals:
Every creative output serves pedagogical purposes:
- Enhances understanding through multiple representations
- Accommodates different learning styles and preferences
- Increases engagement and motivation
- Develops creative thinking skills
- Builds emotional connections to subject matter
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

class CreativeMode(str, Enum):
    """Different modes of creative synthesis"""
    STORYTELLING = "storytelling"                    # Narrative-based learning
    METAPHOR_BUILDING = "metaphor_building"          # Analogies and metaphors
    GAMIFICATION = "gamification"                    # Game-based learning
    VISUALIZATION = "visualization"                  # Visual representations
    EXPERIENTIAL = "experiential"                    # Hands-on experiences
    ROLE_PLAYING = "role_playing"                    # Character-based learning
    ARTISTIC_EXPRESSION = "artistic_expression"      # Creative arts integration
    PROBLEM_REFRAMING = "problem_reframing"          # Alternative problem perspectives
    SCENARIO_BUILDING = "scenario_building"          # Situational learning
    INTERACTIVE_DIALOGUE = "interactive_dialogue"    # Conversational creativity

class CreativityLevel(str, Enum):
    """Levels of creativity intensity"""
    SUBTLE = "subtle"                     # Light creative touches
    MODERATE = "moderate"                 # Balanced creativity and structure
    HIGH = "high"                        # Strong creative elements
    IMMERSIVE = "immersive"              # Fully creative experience
    TRANSFORMATIVE = "transformative"     # Completely reimagined approach

class LearningModality(str, Enum):
    """Different ways of experiencing content"""
    VISUAL = "visual"                    # Images, diagrams, videos
    AUDITORY = "auditory"                # Sounds, music, speech
    KINESTHETIC = "kinesthetic"          # Movement, touch, manipulation
    LOGICAL = "logical"                  # Patterns, sequences, analysis
    SOCIAL = "social"                    # Group activities, discussion
    SOLITARY = "solitary"                # Individual reflection, study
    LINGUISTIC = "linguistic"            # Words, language, writing
    MATHEMATICAL = "mathematical"        # Numbers, formulas, calculations
    SPATIAL = "spatial"                  # 3D thinking, navigation
    MUSICAL = "musical"                  # Rhythm, melody, harmony

class CreativeOutputType(str, Enum):
    """Types of creative outputs"""
    STORY = "story"                      # Narrative content
    METAPHOR = "metaphor"                # Analogical content
    GAME = "game"                        # Interactive game
    VISUALIZATION = "visualization"      # Visual representation
    ACTIVITY = "activity"                # Learning activity
    SCENARIO = "scenario"                # Situational context
    CHARACTER = "character"              # Educational persona
    WORLD = "world"                      # Learning environment
    CHALLENGE = "challenge"              # Creative problem
    EXPERIENCE = "experience"            # Immersive learning journey

class EngagementFactor(str, Enum):
    """Factors that drive engagement"""
    CURIOSITY = "curiosity"              # Questions and mysteries
    SURPRISE = "surprise"                # Unexpected elements
    HUMOR = "humor"                      # Fun and laughter
    CHALLENGE = "challenge"              # Appropriate difficulty
    RELEVANCE = "relevance"              # Personal connection
    AGENCY = "agency"                    # Student control and choice
    MASTERY = "mastery"                  # Skill development
    PURPOSE = "purpose"                  # Meaningful goals
    SOCIAL_CONNECTION = "social_connection"  # Peer interaction
    ACHIEVEMENT = "achievement"          # Recognition and progress

class CreativeConstraint(str, Enum):
    """Constraints that guide creative output"""
    AGE_APPROPRIATE = "age_appropriate"   # Suitable for target age
    CURRICULUM_ALIGNED = "curriculum_aligned"  # Meets learning standards
    TIME_LIMITED = "time_limited"        # Fits available time
    RESOURCE_CONSCIOUS = "resource_conscious"  # Uses available materials
    CULTURALLY_SENSITIVE = "culturally_sensitive"  # Respectful and inclusive
    ATTENTION_SPAN = "attention_span"    # Matches student focus capacity
    PRIOR_KNOWLEDGE = "prior_knowledge"  # Builds on existing understanding
    LEARNING_GOALS = "learning_goals"    # Serves educational objectives
    SAFETY_FOCUSED = "safety_focused"    # Physically and emotionally safe
    TECHNOLOGY_APPROPRIATE = "technology_appropriate"  # Suitable tech use

# ============================================================================
# Core Schema Models
# ============================================================================

class BaseCreativeModel(BaseModel):
    """Base model for all creative synthesis schemas"""
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

class CreativeContextSchema(BaseModel):
    """Schema defining the context for creative synthesis"""
    # Learning context
    subject_area: str = Field(..., description="Academic subject or domain")
    learning_objectives: List[str] = Field(..., description="Specific learning goals")
    target_concepts: List[str] = Field(..., description="Key concepts to be learned")
    difficulty_level: str = Field(default="moderate", description="Complexity level")
    
    # Student context
    age_group: str = Field(..., description="Target age group or grade level")
    learning_style_preferences: List[LearningModality] = Field(default_factory=list)
    interests: List[str] = Field(default_factory=list, description="Student interests and hobbies")
    cultural_background: List[str] = Field(default_factory=list, description="Cultural considerations")
    prior_knowledge: Dict[str, str] = Field(default_factory=dict, description="Existing knowledge base")
    
    # Creative parameters
    creativity_level: CreativityLevel = Field(default=CreativityLevel.MODERATE)
    preferred_modalities: List[LearningModality] = Field(default_factory=list)
    engagement_priorities: List[EngagementFactor] = Field(default_factory=list)
    
    # Constraints and requirements
    time_constraints: Optional[timedelta] = Field(None, description="Available time")
    resource_constraints: List[str] = Field(default_factory=list, description="Available resources")
    platform_constraints: List[str] = Field(default_factory=list, description="Technology limitations")
    creative_constraints: List[CreativeConstraint] = Field(default_factory=list)
    
    # Session context
    session_id: Optional[str] = Field(None, description="Associated learning session")
    collaborative_context: Optional[str] = Field(None, description="Group or individual learning")

class CreativeElementSchema(BaseModel):
    """Schema for individual creative elements"""
    element_id: str = Field(default_factory=lambda: f"element_{uuid4()}")
    element_type: str = Field(..., description="Type of creative element")
    title: str = Field(..., description="Element title or name")
    description: str = Field(..., description="Detailed description")
    content: Dict[str, Any] = Field(..., description="Element content and details")
    
    # Educational alignment
    learning_objective_alignment: List[str] = Field(default_factory=list)
    concept_reinforcement: List[str] = Field(default_factory=list)
    skill_development: List[str] = Field(default_factory=list)
    
    # Creative properties
    creativity_techniques: List[str] = Field(default_factory=list, description="Creative methods used")
    engagement_factors: List[EngagementFactor] = Field(default_factory=list)
    modalities_addressed: List[LearningModality] = Field(default_factory=list)
    
    # Quality metrics
    originality_score: float = Field(default=0.5, ge=0.0, le=1.0, description="How original/unique")
    relevance_score: float = Field(default=0.5, ge=0.0, le=1.0, description="Educational relevance")
    engagement_potential: float = Field(default=0.5, ge=0.0, le=1.0, description="Expected engagement")
    implementation_complexity: float = Field(default=0.5, ge=0.0, le=1.0, description="Difficulty to implement")
    
    # Usage information
    estimated_duration: Optional[timedelta] = Field(None, description="Time to experience/complete")
    required_resources: List[str] = Field(default_factory=list, description="Needed materials/tools")
    setup_instructions: List[str] = Field(default_factory=list, description="How to set up")

class StoryBasedLearningSchema(BaseCreativeModel):
    """Schema for story-based learning experiences"""
    story_id: str = Field(default_factory=lambda: f"story_{uuid4()}")
    title: str = Field(..., description="Story title")
    genre: str = Field(default="educational_adventure", description="Story genre")
    
    # Story structure
    setting: Dict[str, Any] = Field(..., description="Story setting and world")
    characters: List[Dict[str, Any]] = Field(..., description="Story characters")
    plot_outline: List[str] = Field(..., description="Main plot points")
    conflict_resolution: str = Field(..., description="How story resolves")
    
    # Educational integration
    learning_moments: List[Dict[str, Any]] = Field(..., description="Key learning points in story")
    concept_embedding: Dict[str, str] = Field(..., description="How concepts are woven in")
    interactive_elements: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Story delivery
    narrative_style: str = Field(default="engaging", description="Tone and style")
    reading_level: str = Field(..., description="Appropriate reading level")
    multimedia_elements: List[str] = Field(default_factory=list, description="Visual, audio components")
    
    # Engagement design
    cliffhangers: List[str] = Field(default_factory=list, description="Suspenseful moments")
    student_choice_points: List[Dict[str, Any]] = Field(default_factory=list)
    problem_solving_moments: List[Dict[str, Any]] = Field(default_factory=list)

class MetaphorMappingSchema(BaseCreativeModel):
    """Schema for metaphor and analogy creation"""
    metaphor_id: str = Field(default_factory=lambda: f"metaphor_{uuid4()}")
    source_concept: str = Field(..., description="Familiar concept being used as metaphor")
    target_concept: str = Field(..., description="Complex concept being explained")
    
    # Metaphor structure
    similarity_mapping: Dict[str, str] = Field(..., description="How concepts map to each other")
    key_correspondences: List[Dict[str, Any]] = Field(..., description="Important parallels")
    metaphor_limitations: List[str] = Field(default_factory=list, description="Where metaphor breaks down")
    
    # Presentation
    metaphor_narrative: str = Field(..., description="How metaphor is presented")
    visual_elements: List[str] = Field(default_factory=list, description="Supporting visuals")
    interactive_exploration: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Educational effectiveness
    conceptual_clarity: float = Field(default=0.7, ge=0.0, le=1.0, description="How well it clarifies")
    memorability: float = Field(default=0.7, ge=0.0, le=1.0, description="How memorable it is")
    accessibility: float = Field(default=0.7, ge=0.0, le=1.0, description="How accessible to target audience")

class GameBasedLearningSchema(BaseCreativeModel):
    """Schema for gamified learning experiences"""
    game_id: str = Field(default_factory=lambda: f"game_{uuid4()}")
    game_title: str = Field(..., description="Game name")
    game_type: str = Field(..., description="Type of game (puzzle, adventure, simulation, etc.)")
    
    # Game mechanics
    core_mechanics: List[str] = Field(..., description="Main game mechanics")
    player_actions: List[str] = Field(..., description="What players can do")
    win_conditions: List[str] = Field(..., description="How to succeed")
    challenge_progression: List[Dict[str, Any]] = Field(..., description="How difficulty increases")
    
    # Educational integration
    learning_through_play: Dict[str, str] = Field(..., description="How learning happens in game")
    skill_practice_opportunities: List[Dict[str, Any]] = Field(..., description="Skill development moments")
    knowledge_checkpoints: List[Dict[str, Any]] = Field(..., description="Assessment points")
    
    # Engagement systems
    reward_system: Dict[str, Any] = Field(..., description="How players are rewarded")
    progress_tracking: Dict[str, Any] = Field(..., description="Progress visualization")
    social_elements: List[str] = Field(default_factory=list, description="Multiplayer/social features")
    
    # Implementation
    technology_requirements: List[str] = Field(default_factory=list)
    physical_components: List[str] = Field(default_factory=list)
    facilitator_role: Optional[str] = Field(None, description="Teacher/facilitator involvement")

class VisualizationSchema(BaseCreativeModel):
    """Schema for creative visual representations"""
    visualization_id: str = Field(default_factory=lambda: f"viz_{uuid4()}")
    visualization_type: str = Field(..., description="Type of visualization")
    title: str = Field(..., description="Visualization title")
    
    # Visual design
    visual_metaphor: Optional[str] = Field(None, description="Central visual metaphor")
    color_scheme: Dict[str, str] = Field(default_factory=dict, description="Color choices and meanings")
    layout_structure: str = Field(..., description="How elements are arranged")
    interactive_elements: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Content mapping
    concept_to_visual_mapping: Dict[str, str] = Field(..., description="How concepts become visual")
    data_encoding: Dict[str, str] = Field(default_factory=dict, description="How information is encoded")
    narrative_flow: List[str] = Field(default_factory=list, description="Visual storytelling sequence")
    
    # Educational purpose
    cognitive_load_considerations: List[str] = Field(default_factory=list)
    attention_guidance: List[str] = Field(default_factory=list, description="How to guide viewer focus")
    comprehension_scaffolds: List[str] = Field(default_factory=list, description="Supports for understanding")

class ExperientialLearningSchema(BaseCreativeModel):
    """Schema for hands-on, experiential learning activities"""
    experience_id: str = Field(default_factory=lambda: f"exp_{uuid4()}")
    experience_title: str = Field(..., description="Experience name")
    experience_type: str = Field(..., description="Type of hands-on experience")
    
    # Experience design
    sensory_engagement: List[LearningModality] = Field(..., description="Senses involved")
    physical_activities: List[Dict[str, Any]] = Field(..., description="What students physically do")
    exploration_opportunities: List[str] = Field(..., description="Open-ended discovery moments")
    
    # Learning through doing
    skill_practice: List[Dict[str, Any]] = Field(..., description="Skills practiced through experience")
    concept_discovery: List[Dict[str, Any]] = Field(..., description="Concepts discovered through doing")
    reflection_prompts: List[str] = Field(..., description="Questions for reflection")
    
    # Practical considerations
    space_requirements: List[str] = Field(default_factory=list, description="Physical space needed")
    material_requirements: List[str] = Field(default_factory=list, description="Materials and tools")
    safety_considerations: List[str] = Field(default_factory=list, description="Safety precautions")
    time_structure: Dict[str, Any] = Field(..., description="How time is organized")

# ============================================================================
# Creative Synthesis Outputs
# ============================================================================

class CreativeSynthesisOutputSchema(BaseCreativeModel):
    """Schema for complete creative synthesis outputs"""
    output_id: str = Field(default_factory=lambda: f"creative_output_{uuid4()}")
    request_id: str = Field(..., description="ID of the request that generated this")
    output_type: CreativeOutputType = Field(..., description="Type of creative output")
    
    # Core content
    primary_content: Dict[str, Any] = Field(..., description="Main creative content")
    supporting_elements: List[CreativeElementSchema] = Field(default_factory=list)
    alternative_versions: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Educational alignment
    learning_objective_fulfillment: Dict[str, float] = Field(default_factory=dict)
    concept_coverage: Dict[str, str] = Field(default_factory=dict)
    skill_development_opportunities: List[str] = Field(default_factory=list)
    
    # Creative quality
    originality_analysis: Dict[str, Any] = Field(default_factory=dict)
    engagement_prediction: Dict[str, float] = Field(default_factory=dict)
    multi_modal_richness: Dict[LearningModality, float] = Field(default_factory=dict)
    
    # Implementation guidance
    implementation_steps: List[str] = Field(default_factory=list)
    adaptation_suggestions: List[str] = Field(default_factory=list)
    extension_possibilities: List[str] = Field(default_factory=list)
    
    # Quality assurance
    age_appropriateness_check: bool = Field(default=True)
    cultural_sensitivity_check: bool = Field(default=True)
    educational_soundness_check: bool = Field(default=True)
    feasibility_check: bool = Field(default=True)

class CreativeProcessInsightSchema(BaseCreativeModel):
    """Schema capturing insights from the creative process"""
    process_id: str = Field(default_factory=lambda: f"process_{uuid4()}")
    output_id: str = Field(..., description="Associated output ID")
    
    # Process analysis
    creative_techniques_used: List[str] = Field(..., description="Creativity methods applied")
    inspiration_sources: List[str] = Field(default_factory=list, description="What inspired the ideas")
    iteration_history: List[Dict[str, Any]] = Field(default_factory=list, description="How ideas evolved")
    
    # Decision rationale
    design_decisions: List[Dict[str, Any]] = Field(default_factory=list)
    trade_offs_considered: List[Dict[str, Any]] = Field(default_factory=list)
    alternative_approaches: List[str] = Field(default_factory=list)
    
    # Learning from process
    successful_elements: List[str] = Field(default_factory=list)
    challenges_encountered: List[str] = Field(default_factory=list)
    lessons_learned: List[str] = Field(default_factory=list)
    future_improvements: List[str] = Field(default_factory=list)

# ============================================================================
# Request/Response Schemas for API
# ============================================================================

class CreativeSynthesisRequest(BaseModel):
    """Request for creative synthesis"""
    request_type: CreativeMode = Field(..., description="Type of creative synthesis requested")
    creative_context: CreativeContextSchema = Field(..., description="Context for creativity")
    
    # Specific requirements
    output_preferences: List[CreativeOutputType] = Field(default_factory=list)
    must_include_elements: List[str] = Field(default_factory=list, description="Required elements")
    avoid_elements: List[str] = Field(default_factory=list, description="Elements to avoid")
    
    # Quality expectations
    minimum_originality: float = Field(default=0.3, ge=0.0, le=1.0)
    minimum_engagement: float = Field(default=0.5, ge=0.0, le=1.0)
    maximum_complexity: float = Field(default=0.8, ge=0.0, le=1.0)
    
    # Delivery options
    provide_alternatives: bool = Field(default=True, description="Generate multiple options")
    include_implementation_guide: bool = Field(default=True)
    include_adaptation_suggestions: bool = Field(default=True)

class StoryGenerationRequest(BaseModel):
    """Specific request for story-based learning"""
    learning_objectives: List[str] = Field(..., description="What story should teach")
    story_parameters: Dict[str, Any] = Field(default_factory=dict)
    character_preferences: List[str] = Field(default_factory=list)
    setting_preferences: List[str] = Field(default_factory=list)
    story_length: str = Field(default="medium", description="Short, medium, or long")
    interactive_level: str = Field(default="moderate", description="How interactive")

class MetaphorGenerationRequest(BaseModel):
    """Request for metaphor and analogy creation"""
    complex_concept: str = Field(..., description="Concept needing explanation")
    familiar_domains: List[str] = Field(default_factory=list, description="Familiar areas for metaphors")
    metaphor_purpose: str = Field(..., description="What metaphor should accomplish")
    audience_background: Dict[str, Any] = Field(default_factory=dict)

class GameDesignRequest(BaseModel):
    """Request for educational game design"""
    learning_goals: List[str] = Field(..., description="Educational objectives")
    game_style_preferences: List[str] = Field(default_factory=list)
    technology_constraints: List[str] = Field(default_factory=list)
    player_count: str = Field(default="individual", description="Individual or group")
    session_duration: Optional[timedelta] = Field(None, description="Intended play time")

class VisualizationRequest(BaseModel):
    """Request for educational visualization"""
    concepts_to_visualize: List[str] = Field(..., description="What to make visual")
    visualization_purpose: str = Field(..., description="Goal of visualization")
    data_types: List[str] = Field(default_factory=list, description="Types of information to show")
    interaction_requirements: List[str] = Field(default_factory=list)
    aesthetic_preferences: Dict[str, Any] = Field(default_factory=dict)

class ExperienceDesignRequest(BaseModel):
    """Request for experiential learning design"""
    learning_through_doing_goals: List[str] = Field(..., description="What to learn by doing")
    available_resources: List[str] = Field(default_factory=list)
    space_constraints: List[str] = Field(default_factory=list)
    safety_requirements: List[str] = Field(default_factory=list)
    group_size: Optional[int] = Field(None, description="Number of participants")

# ============================================================================
# Quality Assessment and Feedback Schemas
# ============================================================================

class CreativeQualityAssessmentSchema(BaseCreativeModel):
    """Schema for assessing quality of creative outputs"""
    assessment_id: str = Field(default_factory=lambda: f"assessment_{uuid4()}")
    output_id: str = Field(..., description="Creative output being assessed")
    assessor_type: str = Field(..., description="Who/what did the assessment")
    
    # Quality dimensions
    originality_score: float = Field(..., ge=0.0, le=1.0, description="How original and unique")
    relevance_score: float = Field(..., ge=0.0, le=1.0, description="Educational relevance")
    engagement_score: float = Field(..., ge=0.0, le=1.0, description="Predicted engagement")
    feasibility_score: float = Field(..., ge=0.0, le=1.0, description="How realistic to implement")
    educational_value: float = Field(..., ge=0.0, le=1.0, description="Learning potential")
    
    # Detailed feedback
    strengths: List[str] = Field(default_factory=list, description="What works well")
    areas_for_improvement: List[str] = Field(default_factory=list, description="What could be better")
    implementation_challenges: List[str] = Field(default_factory=list)
    adaptation_opportunities: List[str] = Field(default_factory=list)
    
    # Recommendations
    recommended_modifications: List[str] = Field(default_factory=list)
    alternative_approaches: List[str] = Field(default_factory=list)
    follow_up_possibilities: List[str] = Field(default_factory=list)

class StudentEngagementFeedbackSchema(BaseCreativeModel):
    """Schema for capturing student feedback on creative content"""
    feedback_id: str = Field(default_factory=lambda: f"feedback_{uuid4()}")
    output_id: str = Field(..., description="Creative output being reviewed")
    student_id: Optional[str] = Field(None, description="Student providing feedback")
    
    # Engagement metrics
    interest_level: float = Field(..., ge=0.0, le=1.0, description="How interesting")
    fun_factor: float = Field(..., ge=0.0, le=1.0, description="How enjoyable")
    challenge_appropriateness: float = Field(..., ge=0.0, le=1.0, description="Good challenge level")
    clarity: float = Field(..., ge=0.0, le=1.0, description="How clear and understandable")
    
    # Learning impact
    understanding_improvement: float = Field(..., ge=0.0, le=1.0, description="Helped understanding")
    memorability: float = Field(..., ge=0.0, le=1.0, description="How memorable")
    motivation_impact: float = Field(..., ge=0.0, le=1.0, description="Increased motivation")
    
    # Qualitative feedback
    favorite_elements: List[str] = Field(default_factory=list, description="What they liked most")
    confusing_elements: List[str] = Field(default_factory=list, description="What was unclear")
    suggestions: List[str] = Field(default_factory=list, description="Their improvement ideas")
    
    # Context
    completion_rate: float = Field(default=1.0, ge=0.0, le=1.0, description="How much they completed")
    time_spent: Optional[timedelta] = Field(None, description="Time engaged with content")
    collaboration_context: Optional[str] = Field(None, description="Individual or group experience")

# ============================================================================
# Factory Functions and Utilities
# ============================================================================

def create_creative_context(
    subject_area: str,
    learning_objectives: List[str],
    age_group: str,
    **kwargs
) -> CreativeContextSchema:
    """Factory function to create creative context"""
    return CreativeContextSchema(
        subject_area=subject_area,
        learning_objectives=learning_objectives,
        target_concepts=kwargs.get("target_concepts", learning_objectives),
        age_group=age_group,
        **kwargs
    )

def create_story_request(
    learning_objectives: List[str],
    creative_context: CreativeContextSchema,
    **kwargs
) -> StoryGenerationRequest:
    """Factory function to create story generation request"""
    return StoryGenerationRequest(
        learning_objectives=learning_objectives,
        **kwargs
    )

def create_game_request(
    learning_goals: List[str],
    creative_context: CreativeContextSchema,
    **kwargs
) -> GameDesignRequest:
    """Factory function to create game design request"""
    return GameDesignRequest(
        learning_goals=learning_goals,
        **kwargs
    )

# ============================================================================
# Validation and Helper Functions
# ============================================================================

def validate_creative_output_quality(output: CreativeSynthesisOutputSchema) -> List[str]:
    """Validate the quality of creative output"""
    issues = []
    
    # Check educational alignment
    if not output.learning_objective_fulfillment:
        issues.append("No learning objective fulfillment specified")
    
    # Check age appropriateness
    if not output.age_appropriateness_check:
        issues.append("Age appropriateness not verified")
    
    # Check feasibility
    if not output.feasibility_check:
        issues.append("Implementation feasibility not verified")
    
    # Check content completeness
    if not output.primary_content:
        issues.append("No primary content provided")
    
    return issues

def calculate_engagement_potential(
    engagement_factors: List[EngagementFactor],
    modalities: List[LearningModality],
    creativity_level: CreativityLevel
) -> float:
    """Calculate predicted engagement potential"""
    base_score = 0.5
    
    # Boost for engagement factors
    factor_boost = len(engagement_factors) * 0.1
    
    # Boost for multi-modal approach
    modality_boost = len(modalities) * 0.05
    
    # Boost for creativity level
    creativity_mapping = {
        CreativityLevel.SUBTLE: 0.0,
        CreativityLevel.MODERATE: 0.1,
        CreativityLevel.HIGH: 0.2,
        CreativityLevel.IMMERSIVE: 0.3,
        CreativityLevel.TRANSFORMATIVE: 0.4
    }
    creativity_boost = creativity_mapping.get(creativity_level, 0.1)
    
    final_score = base_score + factor_boost + modality_boost + creativity_boost
    return min(1.0, final_score)

def suggest_creative_enhancements(
    current_output: CreativeSynthesisOutputSchema,
    target_engagement: float = 0.8
) -> List[str]:
    """Suggest ways to enhance creative output"""
    suggestions = []
    
    current_engagement = current_output.engagement_prediction.get("overall", 0.5)
    
    if current_engagement < target_engagement:
        gap = target_engagement - current_engagement
        
        if gap > 0.3:
            suggestions.extend([
                "Consider adding interactive elements to increase engagement",
                "Incorporate storytelling or narrative elements",
                "Add gamification elements like challenges or rewards",
                "Include multi-sensory components (visual, auditory, kinesthetic)"
            ])
        elif gap > 0.2:
            suggestions.extend([
                "Add more surprising or unexpected elements",
                "Increase student choice and agency in the experience",
                "Connect to student interests and real-world relevance"
            ])
        else:
            suggestions.extend([
                "Fine-tune the challenge level for optimal engagement",
                "Add social or collaborative elements"
            ])
    
    # Check for missing modalities
    addressed_modalities = current_output.multi_modal_richness.keys()
    important_modalities = [LearningModality.VISUAL, LearningModality.KINESTHETIC, LearningModality.SOCIAL]
    
    for modality in important_modalities:
        if modality not in addressed_modalities:
            suggestions.append(f"Consider adding {modality.value} learning elements")
    
    # Check originality
    originality = current_output.originality_analysis.get("score", 0.5)
    if originality < 0.6:
        suggestions.append("Explore more unique or unexpected approaches to the content")
    
    return suggestions

def analyze_creative_accessibility(
    output: CreativeSynthesisOutputSchema,
    accessibility_requirements: List[str]
) -> Dict[str, Any]:
    """Analyze how accessible the creative output is"""
    analysis = {
        "overall_accessibility": 0.8,  # Default good accessibility
        "accessibility_features": [],
        "barriers_identified": [],
        "improvement_suggestions": []
    }
    
    # Check for common accessibility considerations
    if "visual_impairment" in accessibility_requirements:
        # Check if content has audio alternatives
        modalities = output.multi_modal_richness.keys()
        if LearningModality.AUDITORY in modalities:
            analysis["accessibility_features"].append("Audio content available for visual impairments")
        else:
            analysis["barriers_identified"].append("Limited audio alternatives for visual content")
            analysis["improvement_suggestions"].append("Add audio descriptions or narration")
    
    if "hearing_impairment" in accessibility_requirements:
        if LearningModality.VISUAL in modalities:
            analysis["accessibility_features"].append("Visual content available for hearing impairments")
        else:
            analysis["barriers_identified"].append("Limited visual alternatives for audio content")
            analysis["improvement_suggestions"].append("Add visual captions or sign language")
    
    if "motor_impairment" in accessibility_requirements:
        # Check if kinesthetic elements have alternatives
        if LearningModality.KINESTHETIC in modalities:
            analysis["improvement_suggestions"].append("Ensure kinesthetic activities have accessible alternatives")
    
    if "cognitive_differences" in accessibility_requirements:
        analysis["improvement_suggestions"].extend([
            "Provide content at multiple complexity levels",
            "Include clear navigation and structure",
            "Offer extended time options"
        ])
    
    # Calculate overall accessibility score
    total_requirements = len(accessibility_requirements)
    if total_requirements > 0:
        addressed_requirements = len(analysis["accessibility_features"])
        analysis["overall_accessibility"] = min(1.0, addressed_requirements / total_requirements + 0.3)
    
    return analysis

def generate_adaptation_strategies(
    base_output: CreativeSynthesisOutputSchema,
    different_contexts: List[CreativeContextSchema]
) -> Dict[str, List[str]]:
    """Generate strategies for adapting creative content to different contexts"""
    adaptations = {}
    
    for context in different_contexts:
        context_key = f"{context.age_group}_{context.subject_area}"
        strategies = []
        
        # Age-based adaptations
        if "younger" in context.age_group.lower():
            strategies.extend([
                "Simplify language and concepts",
                "Add more visual and interactive elements",
                "Shorten attention span requirements",
                "Increase scaffolding and guidance"
            ])
        elif "older" in context.age_group.lower():
            strategies.extend([
                "Increase complexity and depth",
                "Add more independent exploration opportunities",
                "Include real-world applications",
                "Provide extension challenges"
            ])
        
        # Subject-based adaptations
        if context.subject_area != base_output.primary_content.get("subject_area"):
            strategies.append(f"Adapt examples and context to {context.subject_area}")
            strategies.append("Modify vocabulary for subject-specific terminology")
        
        # Learning style adaptations
        preferred_modalities = context.preferred_modalities
        for modality in preferred_modalities:
            if modality not in base_output.multi_modal_richness:
                strategies.append(f"Add {modality.value} learning components")
        
        # Creativity level adaptations
        if context.creativity_level != base_output.primary_content.get("creativity_level"):
            if context.creativity_level == CreativityLevel.SUBTLE:
                strategies.append("Reduce creative elements for more straightforward presentation")
            elif context.creativity_level == CreativityLevel.IMMERSIVE:
                strategies.append("Enhance creative elements for more immersive experience")
        
        adaptations[context_key] = strategies
    
    return adaptations

# ============================================================================
# Creative Technique Definitions
# ============================================================================

class CreativeTechnique:
    """Base class for creative techniques"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    def apply(self, content: Dict[str, Any], context: CreativeContextSchema) -> Dict[str, Any]:
        """Apply the creative technique to content"""
        raise NotImplementedError

class StorytellingTechniques:
    """Collection of storytelling creativity techniques"""
    
    @staticmethod
    def get_techniques() -> Dict[str, str]:
        return {
            "hero_journey": "Structure learning as a hero's journey with challenges and growth",
            "mystery_narrative": "Present concepts as mysteries to be solved",
            "character_perspective": "Tell story from unusual character viewpoints",
            "time_travel": "Use time travel to explore historical concepts",
            "parallel_worlds": "Compare concepts through parallel world scenarios",
            "personification": "Give concepts personalities and relationships",
            "quest_structure": "Frame learning as a quest with goals and obstacles",
            "dialogue_driven": "Teach through character conversations and debates"
        }

class MetaphorTechniques:
    """Collection of metaphor and analogy techniques"""
    
    @staticmethod
    def get_techniques() -> Dict[str, str]:
        return {
            "structural_mapping": "Map structural relationships between domains",
            "functional_analogy": "Focus on how things work similarly",
            "causal_mapping": "Map cause-and-effect relationships",
            "system_metaphor": "Use entire systems as metaphors (body, machine, ecosystem)",
            "journey_metaphor": "Frame learning as a journey or adventure",
            "building_metaphor": "Use construction and architecture analogies",
            "sports_metaphor": "Use athletic and game analogies",
            "nature_metaphor": "Draw from natural processes and phenomena"
        }

class GameificationTechniques:
    """Collection of gamification techniques"""
    
    @staticmethod
    def get_techniques() -> Dict[str, str]:
        return {
            "point_systems": "Award points for learning achievements",
            "level_progression": "Organize learning into progressive levels",
            "achievement_badges": "Recognize specific accomplishments",
            "leaderboards": "Create friendly competition",
            "quest_lines": "Chain related learning activities",
            "choice_branching": "Give students meaningful choices",
            "resource_management": "Manage limited resources strategically",
            "collaborative_challenges": "Team-based problem solving",
            "mystery_solving": "Uncover hidden information through learning",
            "creation_challenges": "Build or create something through learning"
        }

class VisualizationTechniques:
    """Collection of visualization creativity techniques"""
    
    @staticmethod
    def get_techniques() -> Dict[str, str]:
        return {
            "concept_mapping": "Visual networks of related ideas",
            "infographic_narrative": "Tell stories through data visualization",
            "interactive_diagrams": "Manipulatable visual representations",
            "layered_revelation": "Progressively reveal information visually",
            "perspective_shifting": "Show concepts from multiple viewpoints",
            "scale_manipulation": "Play with size and scale for emphasis",
            "animation_sequencing": "Use motion to show processes",
            "metaphorical_design": "Visual metaphors and symbolic representation"
        }

# ============================================================================
# Educational Impact Metrics
# ============================================================================

class EducationalImpactSchema(BaseCreativeModel):
    """Schema for measuring educational impact of creative content"""
    impact_id: str = Field(default_factory=lambda: f"impact_{uuid4()}")
    output_id: str = Field(..., description="Creative output being measured")
    
    # Learning outcome metrics
    knowledge_retention: float = Field(default=0.0, ge=0.0, le=1.0, description="How well information is retained")
    skill_transfer: float = Field(default=0.0, ge=0.0, le=1.0, description="Ability to apply skills in new contexts")
    conceptual_understanding: float = Field(default=0.0, ge=0.0, le=1.0, description="Deep understanding of concepts")
    creative_thinking_development: float = Field(default=0.0, ge=0.0, le=1.0, description="Growth in creative thinking")
    
    # Engagement metrics
    time_on_task: timedelta = Field(default=timedelta(0), description="Time spent engaged with content")
    completion_rate: float = Field(default=0.0, ge=0.0, le=1.0, description="Percentage who complete the experience")
    voluntary_re_engagement: float = Field(default=0.0, ge=0.0, le=1.0, description="Students who choose to return")
    peer_sharing: float = Field(default=0.0, ge=0.0, le=1.0, description="Students who share with others")
    
    # Affective outcomes
    curiosity_increase: float = Field(default=0.0, ge=0.0, le=1.0, description="Growth in curiosity about subject")
    confidence_building: float = Field(default=0.0, ge=0.0, le=1.0, description="Increased confidence in abilities")
    intrinsic_motivation: float = Field(default=0.0, ge=0.0, le=1.0, description="Internal motivation to learn")
    positive_associations: float = Field(default=0.0, ge=0.0, le=1.0, description="Positive feelings toward subject")
    
    # Long-term impact
    sustained_interest: Optional[float] = Field(None, ge=0.0, le=1.0, description="Continued interest over time")
    influence_on_future_learning: Optional[float] = Field(None, ge=0.0, le=1.0, description="Impact on future learning choices")
    
    # Measurement context
    measurement_method: str = Field(..., description="How impact was measured")
    measurement_timeframe: timedelta = Field(..., description="When impact was measured after experience")
    sample_size: int = Field(..., ge=1, description="Number of students measured")

# ============================================================================
# Creative Collaboration Schemas
# ============================================================================

class CollaborativeCreationSchema(BaseCreativeModel):
    """Schema for collaborative creative processes"""
    collaboration_id: str = Field(default_factory=lambda: f"collab_{uuid4()}")
    participants: List[Dict[str, Any]] = Field(..., description="Participants in creative collaboration")
    
    # Collaboration structure
    collaboration_model: str = Field(..., description="How collaboration is organized")
    role_assignments: Dict[str, str] = Field(..., description="Who does what")
    communication_channels: List[str] = Field(..., description="How participants communicate")
    
    # Creative process
    ideation_methods: List[str] = Field(..., description="How ideas are generated")
    evaluation_criteria: List[str] = Field(..., description="How ideas are assessed")
    iteration_process: str = Field(..., description="How ideas are refined")
    
    # Outputs and outcomes
    individual_contributions: Dict[str, List[str]] = Field(default_factory=dict)
    collaborative_outputs: List[str] = Field(default_factory=list)
    synergistic_elements: List[str] = Field(default_factory=list, description="Ideas that emerged from collaboration")
    
    # Process insights
    collaboration_challenges: List[str] = Field(default_factory=list)
    successful_strategies: List[str] = Field(default_factory=list)
    lessons_learned: List[str] = Field(default_factory=list)

# ============================================================================
# Personalization and Adaptation Schemas
# ============================================================================

class PersonalizedCreativeSchema(BaseCreativeModel):
    """Schema for personalized creative content"""
    personalization_id: str = Field(default_factory=lambda: f"personal_{uuid4()}")
    base_content_id: str = Field(..., description="Original content being personalized")
    target_student_profile: Dict[str, Any] = Field(..., description="Student this is personalized for")
    
    # Personalization factors
    interest_alignment: Dict[str, str] = Field(..., description="How content connects to student interests")
    learning_style_adaptations: Dict[LearningModality, List[str]] = Field(default_factory=dict)
    cultural_connections: List[str] = Field(default_factory=list)
    difficulty_adjustments: Dict[str, Any] = Field(default_factory=dict)
    
    # Personalized elements
    customized_examples: List[str] = Field(default_factory=list)
    tailored_characters: List[Dict[str, Any]] = Field(default_factory=list)
    relevant_scenarios: List[str] = Field(default_factory=list)
    personal_connections: List[str] = Field(default_factory=list)
    
    # Effectiveness tracking
    personalization_effectiveness: float = Field(default=0.0, ge=0.0, le=1.0)
    student_resonance: float = Field(default=0.0, ge=0.0, le=1.0)
    engagement_improvement: float = Field(default=0.0, ge=0.0, le=1.0)

# ============================================================================
# Export All Schemas and Functions
# ============================================================================

__all__ = [
    # Enums
    "CreativeMode", "CreativityLevel", "LearningModality", "CreativeOutputType",
    "EngagementFactor", "CreativeConstraint",
    
    # Core Schemas
    "BaseCreativeModel", "CreativeContextSchema", "CreativeElementSchema",
    "CreativeSynthesisOutputSchema", "CreativeProcessInsightSchema",
    
    # Specialized Creative Schemas
    "StoryBasedLearningSchema", "MetaphorMappingSchema", "GameBasedLearningSchema",
    "VisualizationSchema", "ExperientialLearningSchema",
    
    # Request Schemas
    "CreativeSynthesisRequest", "StoryGenerationRequest", "MetaphorGenerationRequest",
    "GameDesignRequest", "VisualizationRequest", "ExperienceDesignRequest",
    
    # Quality and Feedback Schemas
    "CreativeQualityAssessmentSchema", "StudentEngagementFeedbackSchema",
    "EducationalImpactSchema",
    
    # Collaboration and Personalization
    "CollaborativeCreationSchema", "PersonalizedCreativeSchema",
    
    # Factory Functions
    "create_creative_context", "create_story_request", "create_game_request",
    
    # Validation and Analysis Functions
    "validate_creative_output_quality", "calculate_engagement_potential",
    "suggest_creative_enhancements", "analyze_creative_accessibility",
    "generate_adaptation_strategies",
    
    # Creative Techniques
    "CreativeTechnique", "StorytellingTechniques", "MetaphorTechniques",
    "GameificationTechniques", "VisualizationTechniques"
]
