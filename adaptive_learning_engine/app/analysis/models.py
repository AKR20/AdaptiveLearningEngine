from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ChatHistory(Base):
    """
    Represents the chat history for a learning session.

    Attributes:
        id (int): The primary key, auto-incremented.
        session_id (int): Foreign key linking to SessionDetails.
        llm_response (str): The response generated by the language model.
        learner_response (str): The response provided by the learner.

    Relationships:
        session (SessionDetails): Many-to-one relationship with SessionDetails.
    """
    __tablename__ = 'chat_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey('session_details.id'), nullable=False)
    llm_response = Column(String, nullable=False)
    learner_response = Column(String, nullable=False)

    # Relationship to SessionDetails
    session = relationship("SessionDetails", back_populates="chat_histories")