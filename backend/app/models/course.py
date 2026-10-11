"""SQLAlchemy database models for courses."""

from sqlalchemy import Column, String, Text, JSON
from app.core.database import Base

class CourseEntity(Base):
    """SQLAlchemy model for a Course."""
    __tablename__ = "courses"

    id = Column(String(50), primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    # Storing the list of prerequisite course IDs as JSON to avoid complex joins
    prerequisites = Column(JSON, nullable=False, default=list)
