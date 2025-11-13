from sqlalchemy import Column, String, Text
from .database import Base

class Session(Base):
    __tablename__ = "sessions"
    id = Column(String, primary_key=True)
    messages = Column(Text)
