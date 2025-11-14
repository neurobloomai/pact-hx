# main.py
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
import uuid
import json

# SQLite setup
DATABASE_URL = "sqlite:///./pact.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Models
class Session(Base):
    __tablename__ = "sessions"
    id = Column(String, primary_key=True)
    messages = Column(Text, default="[]")  # JSON string

Base.metadata.create_all(bind=engine)

# Pydantic models for request validation
class InteractionRequest(BaseModel):
    user_message: str
    ai_message: str

# API
app = FastAPI(title="PACT API", version="0.1.0")

@app.post("/sessions")
def create_session():
    """Create a new session"""
    session_id = str(uuid.uuid4())
    db = SessionLocal()
    try:
        db.add(Session(id=session_id, messages="[]"))
        db.commit()
        return {"session_id": session_id}
    finally:
        db.close()

@app.get("/sessions/{session_id}/context")
def get_context(session_id: str):
    """Get conversation context for a session"""
    db = SessionLocal()
    try:
        session = db.query(Session).filter(Session.id == session_id).first()
        if not session:
            return {"error": "not found"}
        
        # Parse messages
        messages = json.loads(session.messages) if session.messages else []
        
        return {
            "messages": messages,
            "emotional_state": "neutral"  # TODO: Implement emotional analysis
        }
    finally:
        db.close()

@app.post("/sessions/{session_id}/interactions")
def save_interaction(session_id: str, interaction: InteractionRequest):
    """Save an interaction (JSON body)"""
    db = SessionLocal()
    try:
        session = db.query(Session).filter(Session.id == session_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Parse existing messages
        messages = json.loads(session.messages) if session.messages else []
        
        # Add new messages
        messages.append({
            "role": "user",
            "content": interaction.user_message
        })
        messages.append({
            "role": "assistant",
            "content": interaction.ai_message
        })
        
        # Save back
        session.messages = json.dumps(messages)
        db.commit()
        
        return {
            "interaction_id": f"int_{len(messages)}",
            "saved": True
        }
    finally:
        db.close()

@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "ok"}

@app.get("/")
def root():
    """Root endpoint"""
    return {
        "service": "PACT API",
        "version": "0.1.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "create_session": "POST /sessions",
            "get_context": "GET /sessions/{id}/context",
            "save_interaction": "POST /sessions/{id}/interactions"
        }
    }
