# main.py
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid

# SQLite setup
DATABASE_URL = "sqlite:///./pact.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Model
class Session(Base):
    __tablename__ = "sessions"
    id = Column(String, primary_key=True)
    messages = Column(Text)  # JSON string

Base.metadata.create_all(bind=engine)

# API
app = FastAPI()

@app.post("/sessions")
def create_session():
    session_id = str(uuid.uuid4())
    db = SessionLocal()
    db.add(Session(id=session_id, messages="[]"))
    db.commit()
    db.close()
    return {"session_id": session_id}

@app.get("/sessions/{session_id}/context")
def get_context(session_id: str):
    db = SessionLocal()
    session = db.query(Session).filter(Session.id == session_id).first()
    db.close()
    if not session:
        return {"error": "not found"}
    return {"messages": [], "emotional_state": "neutral"}

@app.post("/sessions/{session_id}/interactions")
def save_interaction(session_id: str, user_message: str, ai_message: str):
    # Save to DB
    return {"interaction_id": "saved"}

@app.get("/health")
def health():
    return {"status": "ok"}
