from app.session.schemas import SessionCreate, SessionResponse
from app.core.database import get_db
from app.core.custom_logger import CustomLogger
from app.session.dao import SessionDAO
from app.session.models import SessionDetails
from app.core.open_ai_service import OpenAIService
from sqlalchemy.orm import Session

logger = CustomLogger()

class SessionService:
    """
    Service layer responsible for handling the business logic related to sessions.
    """

    @staticmethod
    def get_formatted_chat_history(chat_history):
        """
        Formats the chat history for display.
        
        Args:
        - chat_history (List[ChatHistory]): The list of chat history entries.
        
        Returns:
        - List[str]: The formatted chat history entries.
        """
        return [
            f"Learner: {entry.learner_response}\nAI: {entry.llm_response}"
            for entry in chat_history
        ]
    
    @staticmethod
    def create_session(db: Session, session_data: SessionCreate) -> SessionResponse:
        """
        Creates a new session by mapping the learning goal to its ID and saving the session to the database.
        
        Args:
        - db (Session): The database session used for querying and committing to the database.
        - session_data (SessionCreate): Data containing learner level and learning goal to create the session.
        
        Returns:
        - SessionResponse: The response containing the session details.
        
        Raises:
        - Exception: If the learning goal cannot be found or other database issues arise.
        """
        try:
            logger.info(f"Looking up learning goal: {session_data.learning_goal}", event_type='create_session')
            learning_goal = SessionDAO.get_learning_goal_by_name(db, session_data.learning_goal)
            if not learning_goal:
                logger.error(f"Learning goal '%s' not found in the database: {session_data.learning_goal}", event_type='create_session')
                return None  # Goal not found, will be handled in the endpoint
            
            new_session = SessionDetails(
                learning_goal_id=learning_goal.id,
                student_initial_level=session_data.learner_level,
                student_current_level=session_data.learner_level  # Initially same as initial level
            )

            logger.info("Creating new session in the database.", event_type='create_session')
            created_session = SessionDAO.create_session(db, new_session)
            
            logger.info(f"Session created with ID: {created_session.id}", event_type='create_session')
            return SessionResponse(
                id=created_session.id,
                learning_goal=learning_goal.learning_goal_names,
                student_initial_level=created_session.student_initial_level,
                student_current_level=created_session.student_current_level
            )
        
        except Exception as e:
            logger.error(f"Error occurred while creating the session: {str(e)}", event_type='create_session')
            raise Exception("An error occurred while creating the session.")
        
    @staticmethod
    def get_recommendation(db: Session, id):
        """
        Get recommendation for a session.
        
        Args:
        - id (int): The session id for which recommendation is required.
        - db (Session): The database session, provided by dependency injection.
        
        Returns:
        - str: The recommendation for the session.
        
        Raises:
        - HTTPException: If the session is not found.
        """
        try:
            chat_history = SessionDAO.get_complete_chat_history(db, id)
            formatted_chat_history = SessionService().get_formatted_chat_history(chat_history)

            logger.info(f'formatted_chat_history: {formatted_chat_history}', event_type='get_recommendation')

            details = SessionDAO.get_learning_goal_and_session_details(db, id)

            system_prompt = "You are an educational AI tutor."
            openai_service = OpenAIService()

            system_prompt = '''
            You are a learning assistant (GPT) designed to help students by analyzing their progress, chat history, and performance to provide personalized recommendations and identify knowledge gaps. Given the learner's current level, the learning topic, and the entire conversation between the trainer (you) and the learner, your goal is to:

            1. Recommend personalized next steps for the learner.
            2. Identify any existing knowledge gaps or areas for improvement based on the chat history.

            Please provide proper formatted response in points for both the parts.
            '''
            user_prompt = f'''
            1. Learner Level: {details.student_initial_level}
            2. Learning Goal: {details.learning_goal_names}
            3. Chat History: {formatted_chat_history}
            '''

            ai_response = openai_service.generate_response(system_prompt, user_prompt)

            return ai_response
        except Exception as e:
            logger.error(f"Error occurred while fetching the session: {str(e)}", event_type='get_recommendation')
            raise Exception("An error occurred while fetching the session.")