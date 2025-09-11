# pact_hx/primitives/creative_synthesis/manager.py
"""
PACT Creative Synthesis Engine Manager

The Creative Synthesis Engine is the imagination powerhouse that transforms 
educational content into engaging, memorable, and innovative learning experiences. 
It's the magic that turns "boring" lessons into adventures, complex concepts into 
relatable stories, and passive learning into active exploration.

Educational Transformation Mission:
Every concept can spark wonder. Every lesson can become an adventure. 
Every student can find their path to understanding through creativity.

The Creative Synthesis Engine believes that when learning engages the imagination, 
it becomes unforgettable.

Core Creative Powers:
- Story Weaving: Transform any concept into compelling narratives
- Metaphor Magic: Create powerful analogies that make complex ideas click
- Game Alchemy: Turn learning objectives into engaging challenges and quests
- Visual Enchantment: Create stunning visualizations that reveal hidden patterns
- Experience Crafting: Design hands-on activities that make abstract concepts tangible
- Surprise Engineering: Add unexpected elements that spark curiosity and delight
- Multi-Modal Orchestration: Engage all senses and learning styles simultaneously

Creative Philosophy for Education:
Creativity isn't decoration - it's illumination. Every creative element serves learning:
- Stories create emotional connections to content
- Metaphors build bridges to understanding
- Games provide safe spaces for experimentation
- Visualizations reveal invisible relationships
- Experiences make learning visceral and memorable
- Surprises keep minds open and engaged

The Creative Process:
1. Understand the Learning Goal (What must students achieve?)
2. Know the Student (Who are we creating for?)
3. Find the Creative Hook (What will capture their imagination?)
4. Design the Experience (How will creativity serve learning?)
5. Test and Iterate (How can we make it even better?)

Integration with PACT Ecosystem:
- Receives learning objectives from Goal Primitive
- Gets student context from Empathetic Interaction
- Collaborates with Adaptive Reasoning for pedagogical soundness
- Works with Contextual Memory for personalization
- Reports to System Evolution for continuous improvement
"""

import asyncio
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import json
import random
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class CreativeModality(Enum):
    """Different creative approaches available"""
    STORY = "story"
    METAPHOR = "metaphor"
    GAME = "game"
    VISUAL = "visual"
    EXPERIENCE = "experience"
    SURPRISE = "surprise"
    MULTIMODAL = "multimodal"


class LearningStyle(Enum):
    """Learning style preferences"""
    VISUAL = "visual"
    AUDITORY = "auditory"
    KINESTHETIC = "kinesthetic"
    READING_WRITING = "reading_writing"
    LOGICAL = "logical"
    SOCIAL = "social"
    SOLITARY = "solitary"


@dataclass
class CreativeHook:
    """A creative element that captures imagination"""
    type: CreativeModality
    title: str
    description: str
    engagement_score: float
    learning_alignment: float
    implementation_complexity: int  # 1-10 scale
    materials_needed: List[str] = field(default_factory=list)
    time_estimate: int = 0  # minutes
    age_appropriateness: Tuple[int, int] = (5, 18)  # min, max age


@dataclass
class LearningExperience:
    """A complete creative learning experience"""
    title: str
    objective: str
    creative_hooks: List[CreativeHook]
    narrative_thread: str
    activities: List[Dict[str, Any]]
    assessment_integration: Dict[str, Any]
    personalization_notes: List[str]
    surprise_elements: List[str]
    multi_sensory_components: Dict[str, Any]


@dataclass
class StudentCreativeProfile:
    """Student's creative preferences and response patterns"""
    preferred_modalities: List[CreativeModality]
    learning_styles: List[LearningStyle]
    engagement_history: Dict[str, float]
    creative_strengths: List[str]
    challenge_areas: List[str]
    interest_themes: List[str]
    attention_span: int  # minutes
    collaboration_preference: str  # "individual", "small_group", "large_group"


class CreativeSynthesisManager:
    """
    The heart of educational creativity - transforms learning objectives
    into magical, memorable experiences that ignite student imagination
    while ensuring deep learning occurs.
    """
    
    def __init__(self):
        self.creative_patterns = self._initialize_creative_patterns()
        self.story_templates = self._initialize_story_templates()
        self.metaphor_database = self._initialize_metaphor_database()
        self.game_mechanics = self._initialize_game_mechanics()
        self.surprise_catalog = self._initialize_surprise_catalog()
        
        # Learning effectiveness tracking
        self.experience_effectiveness = {}
        self.student_response_patterns = {}
        
        # Integration points with other PACT primitives
        self.goal_primitive = None
        self.empathetic_interaction = None
        self.adaptive_reasoning = None
        self.contextual_memory = None
        self.system_evolution = None
    
    def _initialize_creative_patterns(self) -> Dict[str, Any]:
        """Initialize patterns for different creative approaches"""
        return {
            "story_structures": [
                {
                    "name": "Hero's Journey Learning",
                    "template": "student_as_hero",
                    "phases": ["call_to_adventure", "mentorship", "challenges", "revelation", "return"],
                    "best_for": ["complex_concepts", "skill_development", "character_building"]
                },
                {
                    "name": "Mystery Investigation",
                    "template": "detective_story",
                    "phases": ["problem_discovery", "clue_gathering", "hypothesis", "testing", "solution"],
                    "best_for": ["scientific_method", "critical_thinking", "research_skills"]
                },
                {
                    "name": "Time Travel Adventure",
                    "template": "temporal_exploration",
                    "phases": ["departure", "historical_immersion", "interaction", "learning", "return"],
                    "best_for": ["history", "cause_effect", "cultural_understanding"]
                }
            ],
            "metaphor_categories": {
                "nature": ["ecosystem", "seasons", "weather", "animals", "plants"],
                "technology": ["machines", "networks", "computers", "tools"],
                "sports": ["teamwork", "strategy", "competition", "training"],
                "cooking": ["recipes", "ingredients", "processes", "flavors"],
                "building": ["foundation", "structure", "tools", "blueprints"],
                "journey": ["paths", "destinations", "obstacles", "companions"]
            },
            "game_elements": [
                "quests", "levels", "achievements", "leaderboards", "collaboration",
                "resource_management", "strategy", "puzzles", "exploration", "creation"
            ]
        }
    
    def _initialize_story_templates(self) -> Dict[str, Any]:
        """Story frameworks for different learning scenarios"""
        return {
            "concept_introduction": {
                "opening": "In a world where {concept} holds the key to {benefit}...",
                "conflict": "But understanding {concept} requires overcoming {challenge}...",
                "resolution": "Through {learning_method}, our heroes discover {insight}..."
            },
            "skill_building": {
                "opening": "Every master of {skill} began as an apprentice...",
                "journey": "Through practice, mistakes, and gradual improvement...",
                "mastery": "Until one day, {skill} becomes second nature..."
            },
            "problem_solving": {
                "setup": "A puzzling situation emerges: {problem}",
                "investigation": "Our team of investigators uses {method} to explore...",
                "breakthrough": "The aha moment arrives when we realize {solution}..."
            }
        }
    
    def _initialize_metaphor_database(self) -> Dict[str, List[Dict]]:
        """Database of powerful learning metaphors"""
        return {
            "mathematics": [
                {
                    "concept": "algebra",
                    "metaphor": "detective_work",
                    "explanation": "Variables are mysteries to solve, equations are clues"
                },
                {
                    "concept": "geometry",
                    "metaphor": "architecture",
                    "explanation": "Shapes are building blocks, proofs are blueprints"
                }
            ],
            "science": [
                {
                    "concept": "atoms",
                    "metaphor": "social_network",
                    "explanation": "Atoms are like people who form relationships (bonds)"
                },
                {
                    "concept": "ecosystem",
                    "metaphor": "neighborhood",
                    "explanation": "Different species are neighbors with various relationships"
                }
            ],
            "language": [
                {
                    "concept": "grammar",
                    "metaphor": "traffic_rules",
                    "explanation": "Rules that help words flow smoothly and safely"
                },
                {
                    "concept": "writing",
                    "metaphor": "cooking",
                    "explanation": "Ideas are ingredients, structure is the recipe"
                }
            ]
        }
    
    def _initialize_game_mechanics(self) -> Dict[str, Any]:
        """Game elements that enhance learning"""
        return {
            "progression_systems": [
                {
                    "name": "skill_trees",
                    "description": "Visual progression through interconnected abilities",
                    "best_for": ["complex_subjects", "long_term_learning"]
                },
                {
                    "name": "achievement_badges",
                    "description": "Recognition for specific accomplishments",
                    "best_for": ["motivation", "diverse_goals"]
                }
            ],
            "engagement_mechanics": [
                {
                    "name": "collaborative_challenges",
                    "description": "Team-based problem solving",
                    "social_component": True
                },
                {
                    "name": "discovery_quests",
                    "description": "Self-directed exploration with guidance",
                    "autonomy_component": True
                }
            ]
        }
    
    def _initialize_surprise_catalog(self) -> Dict[str, List[str]]:
        """Elements of surprise that spark curiosity"""
        return {
            "unexpected_connections": [
                "How music theory relates to mathematics",
                "Why cooking is applied chemistry",
                "How video games teach physics"
            ],
            "perspective_shifts": [
                "Seeing history from multiple viewpoints",
                "Understanding problems through different roles",
                "Exploring concepts at different scales"
            ],
            "interactive_reveals": [
                "Hidden information revealed through action",
                "Concepts that emerge from student discovery",
                "Surprising outcomes from student choices"
            ]
        }
    
    async def create_learning_experience(
        self,
        learning_objective: str,
        student_profile: StudentCreativeProfile,
        subject_context: Dict[str, Any],
        constraints: Optional[Dict[str, Any]] = None
    ) -> LearningExperience:
        """
        Create a comprehensive creative learning experience tailored
        to the student and objective.
        """
        logger.info(f"Creating creative learning experience for: {learning_objective}")
        
        # Step 1: Understand the Learning Goal
        learning_analysis = await self._analyze_learning_objective(learning_objective, subject_context)
        
        # Step 2: Know the Student
        creative_preferences = await self._analyze_student_creativity(student_profile)
        
        # Step 3: Find the Creative Hook
        creative_hooks = await self._generate_creative_hooks(
            learning_analysis, creative_preferences, constraints
        )
        
        # Step 4: Design the Experience
        experience = await self._design_complete_experience(
            learning_objective, creative_hooks, student_profile, learning_analysis
        )
        
        # Step 5: Add Surprise Elements
        experience = await self._add_surprise_elements(experience, student_profile)
        
        return experience
    
    async def _analyze_learning_objective(
        self, 
        objective: str, 
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze what type of learning experience is needed"""
        
        # Determine learning type
        learning_types = []
        if any(word in objective.lower() for word in ['understand', 'explain', 'describe']):
            learning_types.append('conceptual')
        if any(word in objective.lower() for word in ['solve', 'calculate', 'apply']):
            learning_types.append('procedural')
        if any(word in objective.lower() for word in ['create', 'design', 'build']):
            learning_types.append('creative')
        if any(word in objective.lower() for word in ['analyze', 'evaluate', 'compare']):
            learning_types.append('critical_thinking')
        
        # Assess complexity
        complexity_indicators = len([word for word in objective.split() if len(word) > 6])
        complexity = min(10, max(1, complexity_indicators))
        
        # Identify key concepts
        key_concepts = await self._extract_key_concepts(objective, context)
        
        return {
            'learning_types': learning_types,
            'complexity': complexity,
            'key_concepts': key_concepts,
            'subject_domain': context.get('subject', 'general'),
            'prerequisites': context.get('prerequisites', []),
            'time_available': context.get('time_limit', 60)
        }
    
    async def _extract_key_concepts(self, objective: str, context: Dict[str, Any]) -> List[str]:
        """Extract the main concepts to be learned"""
        # This would typically use NLP, but for now we'll use heuristics
        words = objective.lower().split()
        
        # Remove common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        content_words = [word for word in words if word not in stop_words and len(word) > 3]
        
        # Add context-specific concepts
        if 'key_concepts' in context:
            content_words.extend(context['key_concepts'])
        
        return list(set(content_words[:5]))  # Top 5 unique concepts
    
    async def _analyze_student_creativity(
        self, 
        profile: StudentCreativeProfile
    ) -> Dict[str, Any]:
        """Analyze student's creative preferences and optimal engagement strategies"""
        
        primary_modalities = profile.preferred_modalities[:3]
        learning_style_weights = {style.value: 1.0 for style in profile.learning_styles}
        
        # Calculate engagement patterns
        avg_engagement = sum(profile.engagement_history.values()) / len(profile.engagement_history) if profile.engagement_history else 0.5
        
        # Determine optimal challenge level
        challenge_preference = "moderate"
        if avg_engagement > 0.8:
            challenge_preference = "high"
        elif avg_engagement < 0.4:
            challenge_preference = "gentle"
        
        return {
            'primary_modalities': primary_modalities,
            'learning_style_weights': learning_style_weights,
            'engagement_level': avg_engagement,
            'challenge_preference': challenge_preference,
            'social_preference': profile.collaboration_preference,
            'attention_span': profile.attention_span,
            'interest_hooks': profile.interest_themes
        }
    
    async def _generate_creative_hooks(
        self,
        learning_analysis: Dict[str, Any],
        creative_preferences: Dict[str, Any],
        constraints: Optional[Dict[str, Any]]
    ) -> List[CreativeHook]:
        """Generate multiple creative approaches for the learning objective"""
        
        hooks = []
        primary_modalities = creative_preferences['primary_modalities']
        
        # Generate hooks for each preferred modality
        for modality in primary_modalities:
            if modality == CreativeModality.STORY:
                hook = await self._create_story_hook(learning_analysis, creative_preferences)
            elif modality == CreativeModality.METAPHOR:
                hook = await self._create_metaphor_hook(learning_analysis, creative_preferences)
            elif modality == CreativeModality.GAME:
                hook = await self._create_game_hook(learning_analysis, creative_preferences)
            elif modality == CreativeModality.VISUAL:
                hook = await self._create_visual_hook(learning_analysis, creative_preferences)
            elif modality == CreativeModality.EXPERIENCE:
                hook = await self._create_experience_hook(learning_analysis, creative_preferences)
            else:
                continue
            
            if hook and self._meets_constraints(hook, constraints):
                hooks.append(hook)
        
        # Always add a surprise element
        surprise_hook = await self._create_surprise_hook(learning_analysis, creative_preferences)
        if surprise_hook:
            hooks.append(surprise_hook)
        
        # Sort by engagement potential
        hooks.sort(key=lambda h: h.engagement_score * h.learning_alignment, reverse=True)
        
        return hooks[:5]  # Top 5 hooks
    
    async def _create_story_hook(
        self,
        learning_analysis: Dict[str, Any],
        preferences: Dict[str, Any]
    ) -> Optional[CreativeHook]:
        """Create a story-based creative hook"""
        
        concepts = learning_analysis['key_concepts']
        if not concepts:
            return None
        
        # Select appropriate story structure
        story_structures = self.creative_patterns['story_structures']
        suitable_structures = [s for s in story_structures 
                             if any(lt in s['best_for'] for lt in learning_analysis['learning_types'])]
        
        if not suitable_structures:
            suitable_structures = story_structures
        
        selected_structure = random.choice(suitable_structures)
        main_concept = concepts[0] if concepts else "the subject"
        
        # Create story narrative
        story_title = f"The Quest for {main_concept.title()}"
        story_desc = f"Students embark on a {selected_structure['name'].lower()} where they must master {main_concept} to overcome challenges and help others."
        
        # Connect to student interests
        if preferences['interest_hooks']:
            interest = random.choice(preferences['interest_hooks'])
            story_desc += f" The adventure takes place in a world of {interest}."
        
        return CreativeHook(
            type=CreativeModality.STORY,
            title=story_title,
            description=story_desc,
            engagement_score=0.8,
            learning_alignment=0.7,
            implementation_complexity=6,
            materials_needed=["story_outline", "character_sheets", "setting_description"],
            time_estimate=preferences['attention_span'],
            age_appropriateness=(8, 18)
        )
    
    async def _create_metaphor_hook(
        self,
        learning_analysis: Dict[str, Any],
        preferences: Dict[str, Any]
    ) -> Optional[CreativeHook]:
        """Create a metaphor-based creative hook"""
        
        subject = learning_analysis['subject_domain']
        concepts = learning_analysis['key_concepts']
        
        if not concepts:
            return None
        
        # Find relevant metaphors
        metaphors = self.metaphor_database.get(subject, [])
        if not metaphors:
            # Create a generic metaphor based on concept
            main_concept = concepts[0]
            metaphor_categories = list(self.creative_patterns['metaphor_categories'].keys())
            selected_category = random.choice(metaphor_categories)
            metaphor_examples = self.creative_patterns['metaphor_categories'][selected_category]
            
            metaphor_desc = f"Understanding {main_concept} is like exploring {selected_category} - each element has its role and relationships."
        else:
            relevant_metaphor = random.choice(metaphors)
            metaphor_desc = relevant_metaphor['explanation']
        
        return CreativeHook(
            type=CreativeModality.METAPHOR,
            title=f"The {concepts[0].title()} Connection",
            description=metaphor_desc,
            engagement_score=0.7,
            learning_alignment=0.9,
            implementation_complexity=3,
            materials_needed=["visual_aids", "comparison_charts"],
            time_estimate=20,
            age_appropriateness=(6, 18)
        )
    
    async def _create_game_hook(
        self,
        learning_analysis: Dict[str, Any],
        preferences: Dict[str, Any]
    ) -> Optional[CreativeHook]:
        """Create a game-based creative hook"""
        
        concepts = learning_analysis['key_concepts']
        if not concepts:
            return None
        
        # Select game mechanics based on learning type
        if 'procedural' in learning_analysis['learning_types']:
            game_type = "skill_challenge"
            game_desc = f"Master {concepts[0]} through progressive challenges that unlock new abilities"
        elif 'critical_thinking' in learning_analysis['learning_types']:
            game_type = "strategy_game"
            game_desc = f"Use {concepts[0]} knowledge to solve complex scenarios and outwit challenges"
        else:
            game_type = "exploration_adventure"
            game_desc = f"Discover the secrets of {concepts[0]} through interactive exploration"
        
        # Add social element if preferred
        if preferences['social_preference'] != 'solitary':
            game_desc += " with teammates"
        
        return CreativeHook(
            type=CreativeModality.GAME,
            title=f"The {concepts[0].title()} Challenge",
            description=game_desc,
            engagement_score=0.9,
            learning_alignment=0.8,
            implementation_complexity=7,
            materials_needed=["game_rules", "scoring_system", "challenge_cards"],
            time_estimate=preferences['attention_span'],
            age_appropriateness=(8, 18)
        )
    
    async def _create_visual_hook(
        self,
        learning_analysis: Dict[str, Any],
        preferences: Dict[str, Any]
    ) -> Optional[CreativeHook]:
        """Create a visual-based creative hook"""
        
        concepts = learning_analysis['key_concepts']
        if not concepts:
            return None
        
        visual_approaches = [
            "interactive_diagram",
            "concept_map",
            "infographic_creation",
            "visual_story",
            "data_visualization"
        ]
        
        selected_approach = random.choice(visual_approaches)
        
        return CreativeHook(
            type=CreativeModality.VISUAL,
            title=f"Visualizing {concepts[0].title()}",
            description=f"Create stunning {selected_approach}s that reveal the hidden patterns and connections in {concepts[0]}",
            engagement_score=0.8,
            learning_alignment=0.8,
            implementation_complexity=5,
            materials_needed=["design_tools", "templates", "color_coding_system"],
            time_estimate=30,
            age_appropriateness=(5, 18)
        )
    
    async def _create_experience_hook(
        self,
        learning_analysis: Dict[str, Any],
        preferences: Dict[str, Any]
    ) -> Optional[CreativeHook]:
        """Create an experiential creative hook"""
        
        concepts = learning_analysis['key_concepts']
        if not concepts:
            return None
        
        experience_types = [
            "hands_on_experiment",
            "role_playing_scenario",
            "simulation_activity",
            "real_world_application",
            "maker_project"
        ]
        
        selected_type = random.choice(experience_types)
        
        return CreativeHook(
            type=CreativeModality.EXPERIENCE,
            title=f"Living {concepts[0].title()}",
            description=f"Experience {concepts[0]} through {selected_type} that makes abstract concepts tangible and memorable",
            engagement_score=0.9,
            learning_alignment=0.9,
            implementation_complexity=8,
            materials_needed=["activity_materials", "setup_guide", "safety_equipment"],
            time_estimate=45,
            age_appropriateness=(6, 18)
        )
    
    async def _create_surprise_hook(
        self,
        learning_analysis: Dict[str, Any],
        preferences: Dict[str, Any]
    ) -> Optional[CreativeHook]:
        """Create a surprise element that sparks curiosity"""
        
        concepts = learning_analysis['key_concepts']
        if not concepts:
            return None
        
        surprise_categories = list(self.surprise_catalog.keys())
        selected_category = random.choice(surprise_categories)
        surprise_examples = self.surprise_catalog[selected_category]
        
        return CreativeHook(
            type=CreativeModality.SURPRISE,
            title="The Unexpected Connection",
            description=f"Discover surprising connections between {concepts[0]} and unexpected domains that will change how you see the world",
            engagement_score=0.7,
            learning_alignment=0.6,
            implementation_complexity=4,
            materials_needed=["surprise_reveal_materials"],
            time_estimate=15,
            age_appropriateness=(8, 18)
        )
    
    def _meets_constraints(self, hook: CreativeHook, constraints: Optional[Dict[str, Any]]) -> bool:
        """Check if a creative hook meets the given constraints"""
        if not constraints:
            return True
        
        if 'max_time' in constraints and hook.time_estimate > constraints['max_time']:
            return False
        
        if 'max_complexity' in constraints and hook.implementation_complexity > constraints['max_complexity']:
            return False
        
        if 'required_materials' in constraints:
            required = set(constraints['required_materials'])
            available = set(hook.materials_needed)
            if not required.issubset(available):
                return False
        
        return True
    
    async def _design_complete_experience(
        self,
        objective: str,
        hooks: List[CreativeHook],
        student_profile: StudentCreativeProfile,
        learning_analysis: Dict[str, Any]
    ) -> LearningExperience:
        """Design the complete learning experience integrating all elements"""
        
        if not hooks:
            raise ValueError("No creative hooks available to design experience")
        
        primary_hook = hooks[0]
        supporting_hooks = hooks[1:3]  # Use up to 2 supporting hooks
        
        # Create narrative thread
        narrative = await self._create_narrative_thread(primary_hook, learning_analysis)
        
        # Design activities
        activities = await self._design_activities(hooks, learning_analysis, student_profile)
        
        # Create assessment integration
        assessment = await self._design_creative_assessment(objective, hooks, student_profile)
        
        # Generate personalization notes
        personalization = await self._create_personalization_notes(student_profile, hooks)
        
        # Design multi-sensory components
        multi_sensory = await self._design_multi_sensory_components(hooks, student_profile)
        
        return LearningExperience(
            title=primary_hook.title,
            objective=objective,
            creative_hooks=hooks,
            narrative_thread=narrative,
            activities=activities,
            assessment_integration=assessment,
            personalization_notes=personalization,
            surprise_elements=[],  # Will be added later
            multi_sensory_components=multi_sensory
        )
    
    async def _create_narrative_thread(
        self,
        primary_hook: CreativeHook,
        learning_analysis: Dict[str, Any]
    ) -> str:
        """Create an overarching narrative that connects all learning elements"""
        
        concepts = learning_analysis['key_concepts']
        main_concept = concepts[0] if concepts else "the subject"
        
        if primary_hook.type == CreativeModality.STORY:
            return f"Our learning journey follows heroes who must master {main_concept} to overcome challenges and help their community. Each lesson reveals new powers and deeper understanding."
        
        elif primary_hook.type == CreativeModality.GAME:
            return f"Welcome to the {main_concept} Academy, where students progress through levels of mastery, unlocking new abilities and taking on greater challenges."
        
        elif primary_hook.type == CreativeModality.EXPERIENCE:
            return f"Step into the world where {main_concept} comes alive through hands-on discovery, real-world application, and tangible experimentation."
        
        else:
            return f"Embark on a creative exploration of {main_concept}, where every discovery builds toward mastery and understanding."
    
    async def _design_activities(
        self,
        hooks: List[CreativeHook],
        learning_analysis: Dict[str, Any],
        student_profile: StudentCreativeProfile
    ) -> List[Dict[str, Any]]:
        """Design specific activities for each creative hook"""
        
        activities = []
        
        for i, hook in enumerate(hooks[:3]):  # Limit to 3 main activities
            activity = {
                'name': f"Activity {i+1}: {hook.title}",
                'type': hook.type.value,
                'description': hook.description,
                'duration': hook.time_estimate,
                'materials': hook.materials_needed,
                'instructions': await self._generate_activity_instructions(hook, learning_analysis),
                'learning_outcomes': await self._define_learning_outcomes(hook, learning_analysis),
                'adaptation_notes': await self._create_adaptation_notes(hook, student_profile)
            }
            activities.append(activity)
        
        return activities
    
    async def _generate_activity_instructions(
        self,
        hook: CreativeHook,
        learning_analysis: Dict[str, Any]
    ) -> List[str]:
        """Generate step-by-step instructions for the activity"""
        
        concepts = learning_analysis['key_concepts']
        main_concept = concepts[0] if concepts else "the concept"
        
        if hook.type == CreativeModality.STORY:
            return [
                f"1. Introduce the story world and characters",
                f"2. Present the challenge related to {main_concept}",
                f"3. Guide students through the learning journey",
                f"4. Have students apply {main_concept} to overcome obstacles",
                f"5. Celebrate the victory and reflect on learning"
            ]
        
        elif hook.type == CreativeModality.GAME:
            return [
                f"1. Explain the game rules and objectives",
                f"2. Demonstrate how {main_concept} knowledge helps in the game",
                f"3. Start with easier challenges to build confidence",
                f"4. Increase difficulty as students master skills",
                f"5. Debrief on strategies and learning insights"
            ]
        
        elif hook.type == CreativeModality.VISUAL:
            return [
                f"1. Show examples of effective visual representations",
                f"2. Brainstorm key aspects of {main_concept} to visualize",
                f"3. Create initial sketches or drafts",
                f"4. Develop and refine the visual representation",
                f"5. Present and explain the final visualization"
            ]
        
        else:
            return [
                f"1. Set up the learning environment",
                f"2. Introduce {main_concept} through the creative approach",
                f"3. Guide hands-on exploration and discovery",
                f"4. Encourage experimentation and hypothesis testing",
                f"5. Reflect on discoveries and consolidate learning"
            ]
    
    async def _define_learning_outcomes(
        self,
        hook: CreativeHook,
        learning_analysis: Dict[str, Any]
    ) -> List[str]:
        """Define specific learning outcomes for the activity"""
        
        concepts = learning_analysis['key_concepts']
        learning_types = learning_analysis['learning_types']
        
        outcomes = []
        
        # Base outcomes for all activities
        if concepts:
            outcomes.append(f"Students will demonstrate understanding of {concepts[0]}")
        
        # Type-specific outcomes
        if 'conceptual' in learning_types:
            outcomes.append("Students will explain key concepts in their own words")
        
        if 'procedural' in learning_types:
            outcomes.append("Students will apply learned procedures to solve new problems")
        
        if 'creative' in learning_types:
            outcomes.append("Students will create original solutions or expressions")
        
        if 'critical_thinking' in learning_types:
            outcomes.append("Students will analyze and evaluate different approaches")
        
        # Hook-specific outcomes
        if hook.type == CreativeModality.STORY:
            outcomes.append("Students will connect learning to narrative elements")
        elif hook.type == CreativeModality.GAME:
            outcomes.append("Students will demonstrate strategic thinking and problem-solving")
        elif hook.type == CreativeModality.VISUAL:
            outcomes.append("Students will communicate ideas through visual representation")
        elif hook.type == CreativeModality.EXPERIENCE:
            outcomes.append("Students will make tangible connections between theory and practice")
        
        return outcomes
    
    async def _create_adaptation_notes(
        self,
        hook: CreativeHook,
        student_profile: StudentCreativeProfile
    ) -> List[str]:
        """Create notes for adapting the activity to student needs"""
        
        adaptations = []
        
        # Learning style adaptations
        if LearningStyle.VISUAL in student_profile.learning_styles:
            adaptations.append("Include visual aids, diagrams, and color coding")
        
        if LearningStyle.AUDITORY in student_profile.learning_styles:
            adaptations.append("Incorporate discussions, explanations, and audio elements")
        
        if LearningStyle.KINESTHETIC in student_profile.learning_styles:
            adaptations.append("Add movement, hands-on manipulation, and physical activity")
        
        if LearningStyle.SOCIAL in student_profile.learning_styles:
            adaptations.append("Include group work, peer collaboration, and shared reflection")
        
        if LearningStyle.SOLITARY in student_profile.learning_styles:
            adaptations.append("Provide individual reflection time and personal goal setting")
        
        # Attention span adaptations
        if student_profile.attention_span < 20:
            adaptations.append("Break into shorter segments with frequent check-ins")
        elif student_profile.attention_span > 45:
            adaptations.append("Allow for deeper exploration and extended investigation")
        
        # Interest-based adaptations
        for interest in student_profile.interest_themes:
            adaptations.append(f"Connect concepts to {interest} when possible")
        
        return adaptations
    
    async def _design_creative_assessment(
        self,
        objective: str,
        hooks: List[CreativeHook],
        student_profile: StudentCreativeProfile
    ) -> Dict[str, Any]:
        """Design assessment that integrates creativity with learning evaluation"""
        
        primary_hook = hooks[0] if hooks else None
        
        assessment_methods = []
        
        # Portfolio-based assessment
        assessment_methods.append({
            'type': 'creative_portfolio',
            'description': 'Collection of creative works demonstrating learning progression',
            'components': [
                'initial_ideas_and_sketches',
                'process_documentation',
                'final_creative_product',
                'reflection_on_learning'
            ]
        })
        
        # Performance-based assessment
        if primary_hook and primary_hook.type in [CreativeModality.STORY, CreativeModality.GAME, CreativeModality.EXPERIENCE]:
            assessment_methods.append({
                'type': 'performance_demonstration',
                'description': 'Show learning through action and application',
                'components': [
                    'skill_demonstration',
                    'problem_solving_in_action',
                    'peer_teaching_or_explanation'
                ]
            })
        
        # Self-assessment and reflection
        assessment_methods.append({
            'type': 'reflective_assessment',
            'description': 'Student self-evaluation of learning and growth',
            'components': [
                'learning_goal_progress',
                'creative_process_reflection',
                'connection_to_personal_interests',
                'future_learning_planning'
            ]
        })
        
        return {
            'methods': assessment_methods,
            'rubric_focus': 'creativity_and_understanding',
            'feedback_approach': 'growth_oriented',
            'student_choice_elements': ['presentation_format', 'expression_medium', 'collaboration_level']
        }
    
    async def _create_personalization_notes(
        self,
        student_profile: StudentCreativeProfile,
        hooks: List[CreativeHook]
    ) -> List[str]:
        """Create personalization notes for the complete experience"""
        
        notes = []
        
        # Engagement history insights
        if student_profile.engagement_history:
            avg_engagement = sum(student_profile.engagement_history.values()) / len(student_profile.engagement_history)
            if avg_engagement > 0.8:
                notes.append("Student shows high engagement - provide advanced challenges and leadership opportunities")
            elif avg_engagement < 0.4:
                notes.append("Student needs additional motivation - focus on success experiences and interest connections")
        
        # Creative strengths leverage
        for strength in student_profile.creative_strengths:
            notes.append(f"Leverage student's strength in {strength} as an entry point for learning")
        
        # Challenge area support
        for challenge in student_profile.challenge_areas:
            notes.append(f"Provide additional support and scaffolding for {challenge}")
        
        # Collaboration preferences
        if student_profile.collaboration_preference == "individual":
            notes.append("Respect need for individual work time while providing optional collaboration")
        elif student_profile.collaboration_preference == "small_group":
            notes.append("Design activities for 2-4 student groups with clear roles")
        elif student_profile.collaboration_preference == "large_group":
            notes.append("Include whole-class activities and community building elements")
        
        # Modality preferences
        preferred_modalities = [m.value for m in student_profile.preferred_modalities]
        notes.append(f"Emphasize {', '.join(preferred_modalities)} approaches for optimal engagement")
        
        return notes
    
    async def _design_multi_sensory_components(
        self,
        hooks: List[CreativeHook],
        student_profile: StudentCreativeProfile
    ) -> Dict[str, Any]:
        """Design components that engage multiple senses"""
        
        components = {
            'visual': [],
            'auditory': [],
            'tactile': [],
            'kinesthetic': [],
            'environmental': []
        }
        
        # Visual components
        components['visual'].extend([
            'color_coded_materials',
            'visual_progress_tracking',
            'infographic_summaries',
            'student_created_visuals'
        ])
        
        # Auditory components
        components['auditory'].extend([
            'background_music_for_focus',
            'sound_effects_for_engagement',
            'verbal_explanation_opportunities',
            'discussion_and_sharing_time'
        ])
        
        # Tactile components
        components['tactile'].extend([
            'manipulative_materials',
            'texture_based_learning_aids',
            'hands_on_creation_activities',
            'physical_model_building'
        ])
        
        # Kinesthetic components
        components['kinesthetic'].extend([
            'movement_based_activities',
            'gesture_and_demonstration',
            'role_playing_and_acting',
            'physical_space_utilization'
        ])
        
        # Environmental components
        components['environmental'].extend([
            'flexible_seating_arrangements',
            'natural_lighting_when_possible',
            'temperature_and_comfort_considerations',
            'noise_level_management'
        ])
        
        return components
    
    async def _add_surprise_elements(
        self,
        experience: LearningExperience,
        student_profile: StudentCreativeProfile
    ) -> LearningExperience:
        """Add surprise elements to spark curiosity and delight"""
        
        surprises = []
        
        # Unexpected connections
        surprises.append("Reveal surprising real-world applications of the concepts")
        surprises.append("Show connections to student's personal interests")
        surprises.append("Introduce guest expert or unusual perspective")
        
        # Interactive reveals
        surprises.append("Hidden information unlocked through student discovery")
        surprises.append("Unexpected twist in the narrative or challenge")
        surprises.append("Student choice that changes the learning path")
        
        # Perspective shifts
        surprises.append("View the concept from an unusual angle or scale")
        surprises.append("Role reversal where students become the teachers")
        surprises.append("Time-shift perspective (past, future, or different era)")
        
        # Select 2-3 surprises that fit the experience
        selected_surprises = random.sample(surprises, min(3, len(surprises)))
        
        experience.surprise_elements = selected_surprises
        return experience
    
    async def evaluate_experience_effectiveness(
        self,
        experience_id: str,
        student_responses: Dict[str, Any],
        learning_outcomes: Dict[str, Any]
    ) -> Dict[str, float]:
        """Evaluate how effective the creative experience was"""
        
        effectiveness_metrics = {
            'engagement_level': 0.0,
            'learning_achievement': 0.0,
            'creative_expression': 0.0,
            'retention_prediction': 0.0,
            'student_satisfaction': 0.0
        }
        
        # Analyze engagement
        if 'engagement_scores' in student_responses:
            effectiveness_metrics['engagement_level'] = sum(student_responses['engagement_scores']) / len(student_responses['engagement_scores'])
        
        # Analyze learning achievement
        if 'assessment_results' in learning_outcomes:
            effectiveness_metrics['learning_achievement'] = learning_outcomes['assessment_results'].get('average_score', 0.0)
        
        # Analyze creative expression
        if 'creativity_ratings' in student_responses:
            effectiveness_metrics['creative_expression'] = sum(student_responses['creativity_ratings']) / len(student_responses['creativity_ratings'])
        
        # Predict retention based on engagement and creativity
        effectiveness_metrics['retention_prediction'] = (
            effectiveness_metrics['engagement_level'] * 0.4 +
            effectiveness_metrics['creative_expression'] * 0.3 +
            effectiveness_metrics['learning_achievement'] * 0.3
        )
        
        # Student satisfaction
        if 'satisfaction_survey' in student_responses:
            effectiveness_metrics['student_satisfaction'] = student_responses['satisfaction_survey'].get('overall_rating', 0.0)
        
        # Store for future improvements
        self.experience_effectiveness[experience_id] = effectiveness_metrics
        
        return effectiveness_metrics
    
    async def refine_creative_approach(
        self,
        student_id: str,
        experience_effectiveness: Dict[str, float],
        student_feedback: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Refine future creative approaches based on effectiveness and feedback"""
        
        # Update student creative profile
        if student_id not in self.student_response_patterns:
            self.student_response_patterns[student_id] = {
                'effective_modalities': {},
                'preference_trends': {},
                'engagement_patterns': {},
                'learning_style_effectiveness': {}
            }
        
        patterns = self.student_response_patterns[student_id]
        
        # Track modality effectiveness
        if 'preferred_modality' in student_feedback:
            modality = student_feedback['preferred_modality']
            if modality not in patterns['effective_modalities']:
                patterns['effective_modalities'][modality] = []
            patterns['effective_modalities'][modality].append(experience_effectiveness['engagement_level'])
        
        # Track preference trends
        if 'activity_preferences' in student_feedback:
            for activity, rating in student_feedback['activity_preferences'].items():
                if activity not in patterns['preference_trends']:
                    patterns['preference_trends'][activity] = []
                patterns['preference_trends'][activity].append(rating)
        
        # Generate recommendations
        recommendations = {
            'prioritize_modalities': [],
            'avoid_approaches': [],
            'increase_elements': [],
            'adjust_complexity': 'maintain',
            'social_learning_adjustment': 'maintain'
        }
        
        # Analyze most effective modalities
        if patterns['effective_modalities']:
            avg_effectiveness = {
                modality: sum(scores) / len(scores)
                for modality, scores in patterns['effective_modalities'].items()
            }
            recommendations['prioritize_modalities'] = [
                modality for modality, avg in avg_effectiveness.items() if avg > 0.7
            ]
        
        # Complexity adjustment
        if experience_effectiveness['engagement_level'] < 0.4:
            recommendations['adjust_complexity'] = 'decrease'
        elif experience_effectiveness['engagement_level'] > 0.9 and experience_effectiveness['learning_achievement'] > 0.8:
            recommendations['adjust_complexity'] = 'increase'
        
        # Element adjustments
        if 'most_engaging_elements' in student_feedback:
            recommendations['increase_elements'] = student_feedback['most_engaging_elements']
        
        if 'least_engaging_elements' in student_feedback:
            recommendations['avoid_approaches'] = student_feedback['least_engaging_elements']
        
        return recommendations
    
    async def generate_creativity_report(
        self,
        time_period: str,
        student_group: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate a report on creative learning effectiveness"""
        
        report = {
            'period': time_period,
            'student_group': student_group,
            'summary_metrics': {},
            'trend_analysis': {},
            'successful_approaches': [],
            'improvement_opportunities': [],
            'recommendations': []
        }
        
        # Calculate summary metrics
        all_effectiveness = list(self.experience_effectiveness.values())
        if all_effectiveness:
            report['summary_metrics'] = {
                'average_engagement': sum(e['engagement_level'] for e in all_effectiveness) / len(all_effectiveness),
                'average_learning_achievement': sum(e['learning_achievement'] for e in all_effectiveness) / len(all_effectiveness),
                'average_creativity': sum(e['creative_expression'] for e in all_effectiveness) / len(all_effectiveness),
                'average_satisfaction': sum(e['student_satisfaction'] for e in all_effectiveness) / len(all_effectiveness),
                'total_experiences_created': len(all_effectiveness)
            }
        
        # Identify successful approaches
        if all_effectiveness:
            high_performing = [e for e in all_effectiveness if e['engagement_level'] > 0.8 and e['learning_achievement'] > 0.7]
            report['successful_approaches'] = [
                f"High engagement creative experiences: {len(high_performing)} out of {len(all_effectiveness)}",
                "Most effective creative modalities based on outcomes",
                "Student satisfaction patterns and preferences"
            ]
        
        # Generate recommendations
        report['recommendations'] = [
            "Continue emphasizing multi-modal creative approaches",
            "Increase use of surprise elements and unexpected connections",
            "Develop more personalized creative pathways",
            "Integrate peer collaboration in creative processes",
            "Expand assessment methods to capture creative growth"
        ]
        
        return report
    
    # Integration methods with other PACT primitives
    
    def set_goal_primitive(self, goal_primitive):
        """Set reference to Goal Primitive for learning objective analysis"""
        self.goal_primitive = goal_primitive
    
    def set_empathetic_interaction(self, empathetic_interaction):
        """Set reference to Empathetic Interaction for student understanding"""
        self.empathetic_interaction = empathetic_interaction
    
    def set_adaptive_reasoning(self, adaptive_reasoning):
        """Set reference to Adaptive Reasoning for pedagogical validation"""
        self.adaptive_reasoning = adaptive_reasoning
    
    def set_contextual_memory(self, contextual_memory):
        """Set reference to Contextual Memory for personalization"""
        self.contextual_memory = contextual_memory
    
    def set_system_evolution(self, system_evolution):
        """Set reference to System Evolution for continuous improvement"""
        self.system_evolution = system_evolution
    
    async def collaborate_with_goal_primitive(self, learning_objective: str) -> Dict[str, Any]:
        """Collaborate with Goal Primitive to understand learning requirements"""
        if self.goal_primitive:
            return await self.goal_primitive.analyze_learning_objective(learning_objective)
        return {}
    
    async def collaborate_with_empathetic_interaction(self, student_id: str) -> StudentCreativeProfile:
        """Get student creative profile from Empathetic Interaction"""
        if self.empathetic_interaction:
            student_data = await self.empathetic_interaction.get_student_profile(student_id)
            # Convert to StudentCreativeProfile
            return self._convert_to_creative_profile(student_data)
        return self._default_creative_profile()
    
    def _convert_to_creative_profile(self, student_data: Dict[str, Any]) -> StudentCreativeProfile:
        """Convert general student data to creative profile"""
        return StudentCreativeProfile(
            preferred_modalities=[CreativeModality.STORY, CreativeModality.VISUAL],
            learning_styles=[LearningStyle.VISUAL, LearningStyle.KINESTHETIC],
            engagement_history=student_data.get('engagement_history', {}),
            creative_strengths=student_data.get('creative_strengths', ['visual_arts']),
            challenge_areas=student_data.get('challenge_areas', []),
            interest_themes=student_data.get('interests', ['science', 'adventure']),
            attention_span=student_data.get('attention_span', 30),
            collaboration_preference=student_data.get('collaboration_preference', 'small_group')
        )
    
    def _default_creative_profile(self) -> StudentCreativeProfile:
        """Create a default creative profile when no data is available"""
        return StudentCreativeProfile(
            preferred_modalities=[CreativeModality.STORY, CreativeModality.VISUAL, CreativeModality.GAME],
            learning_styles=[LearningStyle.VISUAL, LearningStyle.KINESTHETIC, LearningStyle.SOCIAL],
            engagement_history={},
            creative_strengths=['curiosity', 'imagination'],
            challenge_areas=[],
            interest_themes=['exploration', 'discovery'],
            attention_span=30,
            collaboration_preference='small_group'
        )


# Example usage and integration
if __name__ == "__main__":
    async def example_usage():
        """Example of how to use the Creative Synthesis Manager"""
        
        # Initialize the manager
        creative_manager = CreativeSynthesisManager()
        
        # Create a sample student profile
        student_profile = StudentCreativeProfile(
            preferred_modalities=[CreativeModality.STORY, CreativeModality.GAME],
            learning_styles=[LearningStyle.VISUAL, LearningStyle.KINESTHETIC, LearningStyle.SOCIAL],
            engagement_history={'math': 0.6, 'science': 0.8, 'reading': 0.7},
            creative_strengths=['storytelling', 'visual_design'],
            challenge_areas=['abstract_concepts'],
            interest_themes=['fantasy', 'technology', 'animals'],
            attention_span=45,
            collaboration_preference='small_group'
        )
        
        # Define learning objective and context
        learning_objective = "Students will understand the water cycle and explain how it affects weather patterns"
        subject_context = {
            'subject': 'science',
            'grade_level': 5,
            'prerequisites': ['basic_weather_knowledge'],
            'time_limit': 60
        }
        
        # Create a creative learning experience
        experience = await creative_manager.create_learning_experience(
            learning_objective=learning_objective,
            student_profile=student_profile,
            subject_context=subject_context,
            constraints={'max_time': 60, 'max_complexity': 7}
        )
        
        print(f"Created experience: {experience.title}")
        print(f"Creative hooks: {len(experience.creative_hooks)}")
        print(f"Activities: {len(experience.activities)}")
        print(f"Surprise elements: {experience.surprise_elements}")
        
        # Simulate experience effectiveness evaluation
        student_responses = {
            'engagement_scores': [0.8, 0.9, 0.7],
            'creativity_ratings': [0.85, 0.8],
            'satisfaction_survey': {'overall_rating': 0.85}
        }
        
        learning_outcomes = {
            'assessment_results': {'average_score': 0.82}
        }
        
        effectiveness = await creative_manager.evaluate_experience_effectiveness(
            experience_id="water_cycle_adventure",
            student_responses=student_responses,
            learning_outcomes=learning_outcomes
        )
        
        print(f"Experience effectiveness: {effectiveness}")
        
        # Generate refinement recommendations
        student_feedback = {
            'preferred_modality': 'story',
            'activity_preferences': {'story_adventure': 0.9, 'visualization': 0.7},
            'most_engaging_elements': ['character_development', 'interactive_exploration'],
            'least_engaging_elements': ['solo_reading']
        }
        
        recommendations = await creative_manager.refine_creative_approach(
            student_id="student_123",
            experience_effectiveness=effectiveness,
            student_feedback=student_feedback
        )
        
        print(f"Future recommendations: {recommendations}")
    
    # Run the example
    asyncio.run(example_usage())
