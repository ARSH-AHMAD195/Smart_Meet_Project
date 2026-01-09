from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from App.core.database import Base # Import Base from the defined database file

# --- Enums (for ActionItem status) ---
class ActionStatus(enum.Enum):
    PENDING = "pending"
    INPROGRESS = "inprogress"
    COMPLETE = "complete"
    CANCELLED = "cancelled"

# --- Core Models ---

class User(Base):
    """Database model for a User."""
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(100), index=True)

    # Relationship to ActionItem (tasks assigned to this user)
    assigned_actions = relationship("ActionItem", back_populates="assignee")


class Team(Base):
    """Database model for a Team/Group."""
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    project_description = Column(String(255), nullable=True, index=True)
    
    # Relationship to Meeting (meetings organized by this team)
    meetings = relationship("Meeting", back_populates="team")


class Meeting(Base):
    """Database model for a scheduled meeting."""
    __tablename__ = "meetings"
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), index=True)
    date = Column(DateTime, default=func.now())
    topic = Column(String(255), nullable=False)
    
    # Relationships
    team = relationship("Team", back_populates="meetings")
    # One-to-one relationship with Transcript
    
    summary = relationship("MeetSummary", uselist=False)
    transcript = relationship("Transcript", back_populates="meeting", uselist=False) 
    action_items = relationship("ActionItem", back_populates="meeting")


class Transcript(Base):
    """Database model for the raw meeting text."""
    __tablename__ = "transcripts"
    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"), unique=True, index=True)
    # Use Text for potentially very large strings (raw transcript)
    raw_text = Column(Text) 
    
    # Relationships
    meeting = relationship("Meeting", back_populates="transcript")


class ActionItem(Base):
    """Database model for a task or decision extracted from a meeting."""
    __tablename__ = "action_items"
    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"))
    task = Column(String(500))
    # Assignee is nullable in case the item is unassigned initially
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    due_date = Column(DateTime, nullable=True)
    # Store enum values as strings in the database
    status = Column(Enum(ActionStatus, name='action_status'), default=ActionStatus.PENDING)

    # Relationships
    meeting = relationship("Meeting", back_populates="action_items")
    assignee = relationship("User", back_populates="assigned_actions")


class MeetSummary(Base):

    __tablename__ = "meet_summary"
    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"))
    summary = Column(String(500))
    date = Column(DateTime, nullable=True)

    meeting = relationship("Meeting", back_populates="summary")