from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.analysis.services import AnalysisService
from app.analysis.router import analysis
from app.core.custom_logger import CustomLogger

logger = CustomLogger()

app = FastAPI()

@analysis.post("/analytics/student/{session_id}")
def analyse_chat(session_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to analyze a chat session for adaptive learning. It stores the chat history and generates the next question based on the learner's responses.

    Args:
        session_id (int): The ID of the chat session.
        db (Session): Database session dependency to interact with the database.

    Returns:
        dict: The response from the AI after processing the chat.

    Raises:
        HTTPException: If there is an error while processing the chat request.
    """
    try:
        logger.info(f"Received chat request for session ID {session_id}", event_type='chat_request_received')

        # Process the chat using the AnalysisService
        response = AnalysisService().analyze_chat(db, session_id)

        if not response:
            logger.error(f"Failed to process chat request for session ID {session_id}", event_type = 'chat_processing_failed')
            raise HTTPException(status_code=400, detail="Failed to process chat request")
        
        logger.info(f"Chat processed successfully for session ID {session_id}", event_type='chat_processed')
        return response
    
    except Exception as e:
        logger.error(f"Error in analyse_chat for session ID {session_id}: {str(e)}", event_type = 'chat_endpoint_error')
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")