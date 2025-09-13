#!/usr/bin/env python3
"""
PACT Creative Synthesis API
===========================

FastAPI wrapper for the Creative Synthesis system, providing:
- REST API endpoints for experience generation
- Real-time adaptation capabilities
- WebSocket support for live updates
- Integration with PACT orchestration layer

This converts the existing Creative Synthesis into a scalable API service.
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import asyncio
import json
import uuid
from datetime import datetime
from enum import Enum
import logging
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# Data Models
# ============================================================================

class LearningContext(BaseModel):
    """Student learning context and preferences"""
    student_id: str
    session_id: str
    subject: str
    grade_level: str
    learning_style: str = "visual"  # visual, auditory, kinesthetic, reading
    difficulty_preference: str = "medium"  # easy, medium, hard
    interests: List[str] = []
    current_knowledge_level: float = Field(0.5, ge=0.0, le=1.0)
    engagement_score: float = Field(0.5, ge=0.0, le=1.0)
    attention_span: int = Field(15, ge=5, le=60)  # minutes

class AdaptationTrigger(BaseModel):
    """Triggers for real-time adaptation"""
    trigger_type: str  # engagement_drop, confusion_detected, mastery_achieved
    confidence: float = Field(ge=0.0, le=1.0)
    context: Dict[str, Any] = {}
    timestamp: datetime = Field(default_factory=datetime.now)

class ExperienceRequest(BaseModel):
    """Request for generating educational experience"""
    context: LearningContext
    content_type: str  # lesson, quiz, exercise, explanation
    topic: str
    duration_minutes: int = 15
    adaptation_enabled: bool = True
    real_time_feedback: bool = True

class GeneratedExperience(BaseModel):
    """Generated educational experience response"""
    experience_id: str
    student_id: str
    content_type: str
    topic: str
    content: Dict[str, Any]
    metadata: Dict[str, Any]
    adaptation_points: List[str] = []
    estimated_duration: int
    created_at: datetime = Field(default_factory=datetime.now)

class AdaptationResponse(BaseModel):
    """Real-time adaptation response"""
    adaptation_id: str
    experience_id: str
    adaptation_type: str
    modified_content: Dict[str, Any]
    reasoning: str
    confidence: float
    timestamp: datetime = Field(default_factory=datetime.now)

# ============================================================================
# Creative Synthesis Engine (Core Logic)
# ============================================================================

class CreativeSynthesisEngine:
    """Core creative synthesis logic adapted for API use"""
    
    def __init__(self):
        self.active_experiences: Dict[str, GeneratedExperience] = {}
        self.adaptation_history: Dict[str, List[AdaptationResponse]] = {}
        
    async def generate_experience(self, request: ExperienceRequest) -> GeneratedExperience:
        """Generate educational experience based on context"""
        experience_id = str(uuid.uuid4())
        
        # Core synthesis logic
        content = await self._synthesize_content(request)
        metadata = await self._generate_metadata(request)
        adaptation_points = await self._identify_adaptation_points(request)
        
        experience = GeneratedExperience(
            experience_id=experience_id,
            student_id=request.context.student_id,
            content_type=request.content_type,
            topic=request.topic,
            content=content,
            metadata=metadata,
            adaptation_points=adaptation_points,
            estimated_duration=request.duration_minutes
        )
        
        self.active_experiences[experience_id] = experience
        logger.info(f"Generated experience {experience_id} for student {request.context.student_id}")
        
        return experience
    
    async def adapt_experience(self, experience_id: str, trigger: AdaptationTrigger) -> AdaptationResponse:
        """Adapt existing experience based on real-time triggers"""
        if experience_id not in self.active_experiences:
            raise ValueError(f"Experience {experience_id} not found")
        
        experience = self.active_experiences[experience_id]
        adaptation_id = str(uuid.uuid4())
        
        # Adaptation logic based on trigger type
        modified_content = await self._adapt_content(experience, trigger)
        reasoning = await self._generate_adaptation_reasoning(trigger)
        
        adaptation = AdaptationResponse(
            adaptation_id=adaptation_id,
            experience_id=experience_id,
            adaptation_type=trigger.trigger_type,
            modified_content=modified_content,
            reasoning=reasoning,
            confidence=trigger.confidence
        )
        
        # Store adaptation history
        if experience_id not in self.adaptation_history:
            self.adaptation_history[experience_id] = []
        self.adaptation_history[experience_id].append(adaptation)
        
        # Update the experience
        experience.content.update(modified_content)
        
        logger.info(f"Adapted experience {experience_id}: {trigger.trigger_type}")
        return adaptation
    
    async def _synthesize_content(self, request: ExperienceRequest) -> Dict[str, Any]:
        """Core content synthesis logic"""
        context = request.context
        
        # Simulate content generation based on learning context
        base_content = {
            "title": f"{request.topic} - {request.content_type.title()}",
            "learning_objectives": [
                f"Understand core concepts of {request.topic}",
                f"Apply knowledge through {request.content_type} activities"
            ]
        }
        
        # Adapt based on learning style
        if context.learning_style == "visual":
            base_content["visual_elements"] = [
                "interactive_diagram", "concept_map", "infographic"
            ]
        elif context.learning_style == "auditory":
            base_content["audio_elements"] = [
                "narration", "background_music", "sound_effects"
            ]
        elif context.learning_style == "kinesthetic":
            base_content["interactive_elements"] = [
                "drag_drop", "simulation", "hands_on_activity"
            ]
        
        # Content type specific generation
        if request.content_type == "lesson":
            base_content.update(await self._generate_lesson_content(request))
        elif request.content_type == "quiz":
            base_content.update(await self._generate_quiz_content(request))
        elif request.content_type == "exercise":
            base_content.update(await self._generate_exercise_content(request))
        
        return base_content
    
    async def _generate_lesson_content(self, request: ExperienceRequest) -> Dict[str, Any]:
        """Generate lesson-specific content"""
        difficulty = request.context.difficulty_preference
        knowledge_level = request.context.current_knowledge_level
        
        return {
            "sections": [
                {
                    "title": "Introduction",
                    "content": f"Welcome to learning about {request.topic}",
                    "duration": 3,
                    "difficulty": "easy"
                },
                {
                    "title": "Core Concepts",
                    "content": f"Key ideas in {request.topic}",
                    "duration": 8,
                    "difficulty": difficulty
                },
                {
                    "title": "Practice",
                    "content": f"Apply your {request.topic} knowledge",
                    "duration": 4,
                    "difficulty": "medium" if knowledge_level > 0.6 else "easy"
                }
            ],
            "knowledge_checks": [
                {"question": f"What is the main concept in {request.topic}?", "type": "multiple_choice"},
                {"question": f"How would you apply {request.topic}?", "type": "open_ended"}
            ]
        }
    
    async def _generate_quiz_content(self, request: ExperienceRequest) -> Dict[str, Any]:
        """Generate quiz-specific content"""
        return {
            "questions": [
                {
                    "id": str(uuid.uuid4()),
                    "type": "multiple_choice",
                    "question": f"What is the primary focus of {request.topic}?",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct_answer": "Option A",
                    "difficulty": request.context.difficulty_preference
                },
                {
                    "id": str(uuid.uuid4()),
                    "type": "true_false",
                    "question": f"{request.topic} is an important concept to understand.",
                    "correct_answer": True,
                    "difficulty": "easy"
                }
            ],
            "scoring": {
                "total_points": 100,
                "passing_score": 70,
                "adaptive_difficulty": True
            }
        }
    
    async def _generate_exercise_content(self, request: ExperienceRequest) -> Dict[str, Any]:
        """Generate exercise-specific content"""
        return {
            "tasks": [
                {
                    "id": str(uuid.uuid4()),
                    "title": f"Practice {request.topic}",
                    "description": f"Complete this {request.topic} exercise",
                    "type": "interactive",
                    "estimated_time": request.duration_minutes // 2
                }
            ],
            "resources": [
                {"type": "reference", "title": f"{request.topic} Guide"},
                {"type": "example", "title": f"Sample {request.topic} Solution"}
            ]
        }
    
    async def _generate_metadata(self, request: ExperienceRequest) -> Dict[str, Any]:
        """Generate experience metadata"""
        return {
            "pedagogical_approach": "constructivist",
            "bloom_taxonomy_levels": ["remember", "understand", "apply"],
            "engagement_strategies": ["gamification", "real_time_feedback"],
            "adaptation_sensitivity": 0.7,
            "target_engagement": 0.8
        }
    
    async def _identify_adaptation_points(self, request: ExperienceRequest) -> List[str]:
        """Identify points where adaptation can occur"""
        return [
            "content_difficulty",
            "pacing_speed",
            "explanation_detail",
            "example_complexity",
            "interaction_frequency"
        ]
    
    async def _adapt_content(self, experience: GeneratedExperience, trigger: AdaptationTrigger) -> Dict[str, Any]:
        """Adapt content based on trigger"""
        adaptations = {}
        
        if trigger.trigger_type == "engagement_drop":
            adaptations = {
                "interaction_boost": True,
                "gamification_elements": ["progress_bar", "achievement_badge"],
                "content_simplification": True
            }
        elif trigger.trigger_type == "confusion_detected":
            adaptations = {
                "additional_examples": True,
                "slower_pacing": True,
                "alternative_explanation": True,
                "visual_aids": True
            }
        elif trigger.trigger_type == "mastery_achieved":
            adaptations = {
                "advanced_content": True,
                "challenge_mode": True,
                "peer_teaching_opportunity": True
            }
        
        return adaptations
    
    async def _generate_adaptation_reasoning(self, trigger: AdaptationTrigger) -> str:
        """Generate human-readable reasoning for adaptation"""
        reasoning_map = {
            "engagement_drop": "Student engagement decreased, adding interactive elements and simplifying content",
            "confusion_detected": "Confusion signals detected, providing additional support and examples",
            "mastery_achieved": "Student has mastered current level, providing advanced challenges"
        }
        return reasoning_map.get(trigger.trigger_type, "Adapting based on student needs")

# ============================================================================
# WebSocket Connection Manager
# ============================================================================

class ConnectionManager:
    """Manage WebSocket connections for real-time updates"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.student_sessions: Dict[str, str] = {}  # student_id -> session_id
    
    async def connect(self, websocket: WebSocket, student_id: str, session_id: str):
        """Connect a new WebSocket client"""
        await websocket.accept()
        connection_id = f"{student_id}_{session_id}"
        self.active_connections[connection_id] = websocket
        self.student_sessions[student_id] = session_id
        logger.info(f"WebSocket connected: {connection_id}")
    
    def disconnect(self, student_id: str):
        """Disconnect a WebSocket client"""
        if student_id in self.student_sessions:
            session_id = self.student_sessions[student_id]
            connection_id = f"{student_id}_{session_id}"
            if connection_id in self.active_connections:
                del self.active_connections[connection_id]
            del self.student_sessions[student_id]
            logger.info(f"WebSocket disconnected: {connection_id}")
    
    async def send_personal_message(self, message: dict, student_id: str):
        """Send message to specific student"""
        if student_id in self.student_sessions:
            session_id = self.student_sessions[student_id]
            connection_id = f"{student_id}_{session_id}"
            if connection_id in self.active_connections:
                websocket = self.active_connections[connection_id]
                try:
                    await websocket.send_text(json.dumps(message))
                except Exception as e:
                    logger.error(f"Error sending message to {student_id}: {e}")
                    self.disconnect(student_id)
    
    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        disconnected = []
        for connection_id, websocket in self.active_connections.items():
            try:
                await websocket.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Error broadcasting to {connection_id}: {e}")
                disconnected.append(connection_id)
        
        # Clean up disconnected clients
        for connection_id in disconnected:
            parts = connection_id.split('_', 1)
            if len(parts) == 2:
                student_id = parts[0]
                self.disconnect(student_id)

# ============================================================================
# Global Instances
# ============================================================================

synthesis_engine = CreativeSynthesisEngine()
connection_manager = ConnectionManager()

# ============================================================================
# Lifespan Events
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events"""
    # Startup
    logger.info("🚀 PACT Creative Synthesis API starting up...")
    logger.info("✅ Creative Synthesis Engine initialized")
    logger.info("✅ WebSocket Connection Manager ready")
    logger.info("🌐 API ready for educational experience generation")
    
    yield
    
    # Shutdown
    logger.info("🛑 PACT Creative Synthesis API shutting down...")
    # Close all WebSocket connections
    for connection_id in list(connection_manager.active_connections.keys()):
        parts = connection_id.split('_', 1)
        if len(parts) == 2:
            student_id = parts[0]
            connection_manager.disconnect(student_id)
    logger.info("✅ Cleanup completed")

# ============================================================================
# Initialize FastAPI App
# ============================================================================

app = FastAPI(
    title="PACT Creative Synthesis API",
    description="Real-time educational experience generation and adaptation",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# REST API Endpoints
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def root():
    """API documentation and status page"""
    return """
    <html>
        <head><title>PACT Creative Synthesis API</title></head>
        <body>
            <h1>🎓 PACT Creative Synthesis API</h1>
            <p>Real-time educational experience generation and adaptation</p>
            <h2>Endpoints:</h2>
            <ul>
                <li><strong>POST /generate</strong> - Generate educational experience</li>
                <li><strong>POST /adapt/{experience_id}</strong> - Adapt existing experience</li>
                <li><strong>GET /experience/{experience_id}</strong> - Get experience details</li>
                <li><strong>GET /health</strong> - API health check</li>
                <li><strong>WebSocket /ws/{student_id}/{session_id}</strong> - Real-time updates</li>
            </ul>
            <p><a href="/docs">📚 Interactive API Documentation</a></p>
            <p><a href="/redoc">📖 ReDoc Documentation</a></p>
        </body>
    </html>
    """

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "active_experiences": len(synthesis_engine.active_experiences),
        "active_connections": len(connection_manager.active_connections)
    }

@app.post("/generate", response_model=GeneratedExperience)
async def generate_experience(request: ExperienceRequest, background_tasks: BackgroundTasks):
    """Generate new educational experience"""
    try:
        experience = await synthesis_engine.generate_experience(request)
        
        # Send real-time update via WebSocket
        background_tasks.add_task(
            connection_manager.send_personal_message,
            {
                "type": "experience_generated",
                "experience": experience.dict()
            },
            request.context.student_id
        )
        
        return experience
    except Exception as e:
        logger.error(f"Error generating experience: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/adapt/{experience_id}", response_model=AdaptationResponse)
async def adapt_experience(experience_id: str, trigger: AdaptationTrigger, background_tasks: BackgroundTasks):
    """Adapt existing experience based on real-time trigger"""
    try:
        adaptation = await synthesis_engine.adapt_experience(experience_id, trigger)
        
        # Get student ID from experience
        experience = synthesis_engine.active_experiences.get(experience_id)
        if experience:
            # Send real-time adaptation via WebSocket
            background_tasks.add_task(
                connection_manager.send_personal_message,
                {
                    "type": "experience_adapted",
                    "adaptation": adaptation.dict(),
                    "experience_id": experience_id
                },
                experience.student_id
            )
        
        return adaptation
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error adapting experience: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/experience/{experience_id}", response_model=GeneratedExperience)
async def get_experience(experience_id: str):
    """Get experience details"""
    experience = synthesis_engine.active_experiences.get(experience_id)
    if not experience:
        raise HTTPException(status_code=404, detail="Experience not found")
    return experience

@app.get("/adaptations/{experience_id}")
async def get_adaptations(experience_id: str):
    """Get adaptation history for an experience"""
    adaptations = synthesis_engine.adaptation_history.get(experience_id, [])
    return {"experience_id": experience_id, "adaptations": adaptations}

@app.get("/experiences")
async def list_experiences(student_id: Optional[str] = None):
    """List all active experiences, optionally filtered by student"""
    experiences = list(synthesis_engine.active_experiences.values())
    if student_id:
        experiences = [exp for exp in experiences if exp.student_id == student_id]
    return {"experiences": experiences}

# ============================================================================
# WebSocket Endpoint
# ============================================================================

@app.websocket("/ws/{student_id}/{session_id}")
async def websocket_endpoint(websocket: WebSocket, student_id: str, session_id: str):
    """WebSocket endpoint for real-time updates"""
    await connection_manager.connect(websocket, student_id, session_id)
    
    # Send welcome message
    await websocket.send_text(json.dumps({
        "type": "connection_established",
        "student_id": student_id,
        "session_id": session_id,
        "timestamp": datetime.now().isoformat()
    }))
    
    try:
        while True:
            # Listen for client messages (triggers, feedback, etc.)
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            if message.get("type") == "trigger_adaptation":
                experience_id = message.get("experience_id")
                trigger_data = message.get("trigger")
                
                if experience_id and trigger_data:
                    trigger = AdaptationTrigger(**trigger_data)
                    try:
                        adaptation = await synthesis_engine.adapt_experience(experience_id, trigger)
                        await websocket.send_text(json.dumps({
                            "type": "adaptation_applied",
                            "adaptation": adaptation.dict()
                        }))
                    except Exception as e:
                        await websocket.send_text(json.dumps({
                            "type": "error",
                            "message": str(e)
                        }))
            
    except WebSocketDisconnect:
        connection_manager.disconnect(student_id)
    except Exception as e:
        logger.error(f"WebSocket error for {student_id}: {e}")
        connection_manager.disconnect(student_id)

# ============================================================================
# Main Application Entry Point
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "creative_synthesis_api:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )
