from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.chatWithLearner.schemas import ChatRequest, ChatResponse
from app.chatWithLearner.services import ChatService
from app.chatWithLearner.router import chat
from app.core.custom_logger import CustomLogger

logger = CustomLogger()

app = FastAPI()

@chat.post("/chat-with-gpt", response_model=ChatResponse)
def chat_with_gpt(chat_request: ChatRequest, db: Session = Depends(get_db)):
    """
    Endpoint to initiate a chat session with GPT for adaptive learning.
    It stores the chat history and generates the next question based on the learner's responses.

    Args:
        chat_request (ChatRequest): The chat request containing session data and learner's response.
        db (Session): Database session dependency to interact with the database.

    Returns:
        ChatResponse: The response from the AI after processing the chat.

    Raises:
        HTTPException: If there is an error while processing the chat request.
    """
    try:
        logger.info(f"Received chat request for session ID {chat_request.session_id}", event_type='chat_request_received')

        # Call the service to process the chat
        response = ChatService.process_chat(db, chat_request)

        if not response:
            logger.error(f"Failed to process chat request for session ID {chat_request.session_id}", event_type='chat_processing_failed')
            raise HTTPException(status_code=400, detail="Failed to process chat request")
        
        logger.info(f"Chat processed successfully for session ID {chat_request.session_id}", event_type='chat_processed')
        return response
    
    except Exception as e:
        logger.error(f"Error in chat_with_gpt for session ID {chat_request.session_id}: {str(e)}", event_type='chat_endpoint_error')
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")