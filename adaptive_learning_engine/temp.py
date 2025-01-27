from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import random

# Create Base here to ensure it's used consistently
Base = declarative_base()

# Define the LearningGoals model
class LearningGoals(Base):
    __tablename__ = 'learning_goals'

    id = Column(Integer, primary_key=True, autoincrement=True)
    learning_goal_names = Column(String, nullable=False)

    # Relationship to SessionDetails
    session_details = relationship("SessionDetails", back_populates="learning_goal")

# Define the SessionDetails model
class SessionDetails(Base):
    __tablename__ = 'session_details'

    id = Column(Integer, primary_key=True, autoincrement=True)
    learning_goal_id = Column(Integer, ForeignKey('learning_goals.id'), nullable=False)
    student_initial_level = Column(String, nullable=False)
    student_current_level = Column(String, nullable=False)

    # Relationship to LearningGoals
    learning_goal = relationship("LearningGoals", back_populates="session_details")
    # Relationship to ChatHistory
    chat_histories = relationship("ChatHistory", back_populates="session")

# Define the ChatHistory model
class ChatHistory(Base):
    __tablename__ = 'chat_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey('session_details.id'), nullable=False)
    llm_response = Column(String, nullable=False)
    learner_response = Column(String, nullable=False)

    # Relationship to SessionDetails
    session = relationship("SessionDetails", back_populates="chat_histories")

# Define the database URL
DATABASE_URL = "sqlite:///./AdaptiveLearning.db"

# Create engine and session local
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables in the database
Base.metadata.create_all(bind=engine)

# Define a list of student levels and learning goals for sample data
student_levels = ["beginner", "intermediate", "advanced"]
learning_goal_names = [
    "Arithmetic", "Algebra", "Geometry", "Trigonometry", "Calculus",
    "Probability", "Statistics", "Number Theory", "Linear Algebra", 
    "Discrete Mathematics", "Set Theory", "Differential Equations", 
    "Complex Numbers", "Mathematical Logic", "Combinatorics", "Topology",
    "Graph Theory", "Mathematical Modelling", "Real Analysis", "Functional Analysis",
    "Vector Calculus", "Numerical Methods", "Optimization Techniques", 
    "Game Theory", "Boolean Algebra", "Financial Mathematics", 
    "Cryptography", "Fractals and Chaos Theory", "Applied Mathematics", 
    "Differential Geometry"
]

# Insert learning goals into the database
db_session = SessionLocal()

# Insert learning goals if the table is empty
existing_goals = db_session.query(LearningGoals).count()
if existing_goals == 0:
    for goal_name in learning_goal_names:
        goal = LearningGoals(learning_goal_names=goal_name)
        db_session.add(goal)
    db_session.commit()
    print("Learning goals inserted successfully!")

# Retrieve all learning goal IDs
learning_goals = db_session.query(LearningGoals).all()
learning_goal_ids = [goal.id for goal in learning_goals]

# Insert dummy session details
dummy_sessions = []
for i in range(1, 26):  # Loop for 25 sessions
    session = SessionDetails(
        learning_goal_id=random.choice(learning_goal_ids),
        student_initial_level='beginner',
        student_current_level=random.choice(student_levels)
    )
    dummy_sessions.append(session)

# Add sessions to the database
db_session.add_all(dummy_sessions)
db_session.commit()
db_session.close()

print("Dummy session data inserted successfully!")