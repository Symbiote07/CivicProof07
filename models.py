from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Setup SQLite DB (Fast and easy for hackathons)
DATABASE_URL = "sqlite:///./civicproof.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- The "Knowledge Graph" Entities ---

class Booth(Base):
    __tablename__ = "booths"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)  # e.g., "Sector 14, Gali 3"
    location_lat = Column(String)
    location_long = Column(String)
    
    # Relationships
    voters = relationship("Voter", back_populates="booth")
    tasks = relationship("Task", back_populates="booth")

class Voter(Base):
    __tablename__ = "voters"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String)
    segment = Column(String) # e.g., "Youth", "Senior"
    
    booth_id = Column(Integer, ForeignKey("booths.id"))
    booth = relationship("Booth", back_populates="voters")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String) # e.g., "Fix Streetlight"
    status = Column(String, default="Pending") # Pending, Verified, Rejected
    image_url = Column(String, nullable=True) # The "After" photo
    
    booth_id = Column(Integer, ForeignKey("booths.id"))
    booth = relationship("Booth", back_populates="tasks")

# Create the tables
Base.metadata.create_all(bind=engine)