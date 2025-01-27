from fastapi import HTTPException, Depends
from app.session.schemas import SessionCreate
from app.session.services import SessionService
from app.core.custom_logger import CustomLogger
from app.session.router import session_router
from app.core.database import get_db
from sqlalchemy.orm import Session

logger = CustomLogger()

session_service = SessionService()

@session_router.post("/create-session")
def create_session(session_data: SessionCreate, db: Session = Depends(get_db)):
    """
    Endpoint to create a new session.
    
    Accepts learner level and learning goal, maps the goal name to its ID, 
    and inserts a new session into the database.
    
    Args:
    - session_data (SessionCreate): Input data containing learner level and learning goal.
    - db (Session): The database session, provided by dependency injection.
    
    Returns:
    - SessionResponse: The created session details.
    
    Raises:
    - HTTPException: If the learning goal is invalid or cannot be found.
    """
    try:
        logger.info(f"Creating new session with learning goal: {session_data.learning_goal}", event_type='create_session')
        session = session_service.create_session(db, session_data)
        if not session:
            logger.error(f"Learning goal '%s' not found..{session_data.learning_goal}", event_type='create_session')
            raise HTTPException(status_code=400, detail="Invalid learning goal")
        logger.info(f"Session created successfully with ID: {session.id}",event_type='create_session')
        return session
    except Exception as e:
        logger.error(f"An error occurred while creating the session: {str(e)}", event_type='create_session')
        raise HTTPException(status_code=500, detail="Internal server error")
    
@session_router.post("/session/{id}/recommendation")
def get_recommendation(id: int, db: Session = Depends(get_db)):
    """
    Endpoint to get recommendation for a session.
    
    Accepts session id and returns the recommendation for the session.
    
    Args:
    - id (int): The session id for which recommendation is required.
    - db (Session): The database session, provided by dependency injection.
    
    Returns:
    - str: The recommendation for the session.
    
    Raises:
    - HTTPException: If the session is not found.
    """
    try:
        logger.info(f"Fetching recommendation for session ID: {id}", event_type='get_recommendation')
        recommendation = session_service.get_recommendation(db, id)
        if not recommendation:
            logger.error(f"Session with ID {id} not found.", event_type='get_recommendation')
            raise HTTPException(status_code=404, detail="Session not found")
        logger.info(f"Recommendation fetched successfully for session ID: {id}", event_type='get_recommendation')
        return {"ai_response": recommendation}
    except Exception as e:
        logger.error(f"An error occurred while fetching recommendation for session ID {id}: {str(e)}", event_type='get_recommendation')
        raise HTTPException(status_code=500, detail="Internal server error")