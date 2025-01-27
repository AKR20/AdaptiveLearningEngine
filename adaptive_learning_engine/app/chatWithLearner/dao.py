from sqlalchemy.orm import Session
from app.chatWithLearner.models import ChatHistory, LearningGoals, SessionDetails
from app.core.custom_logger import CustomLogger

logger = CustomLogger()

class ChatDAO:
    """
    Data Access Object (DAO) class for interacting with the database for chat-related operations.
    It includes methods for fetching session details, learning goals, chat history, and storing chat entries.
    """

    @staticmethod
    def get_session_by_id(db: Session, session_id: int):
        """
        Fetch session details by session ID.
        
        Args:
            db (Session): Database session for executing queries.
            session_id (int): The ID of the session to fetch.
        
        Returns:
            SessionDetails: The session details corresponding to the session ID.
        
        Raises:
            Exception: If the session is not found.
        """
        try:
            session = db.query(SessionDetails).filter(SessionDetails.id == session_id).first()
            if not session:
                logger.warning(f"Session with ID {session_id} not found.", event_type='session_not_found')
                raise Exception("Session not found.")
            logger.info(f"Session with ID {session_id} fetched successfully.", event_type='session_fetched')
            return session
        except Exception as e:
            logger.error(f"Error fetching session with ID {session_id}: {str(e)}", event_type='session_fetch_error')
            raise Exception(f"Error fetching session: {str(e)}")

    @staticmethod
    def get_learning_goal_by_session(db: Session, session_id: int):
        """
        Get learning goal name using session_id by joining SessionDetails and LearningGoals.
        
        Args:
            db (Session): Database session for executing queries.
            session_id (int): The session ID to fetch the associated learning goal.

        Returns:
            str: The learning goal name.
        
        Raises:
            Exception: If the learning goal is not found for the session.
        """
        try:
            learning_goal = (
                db.query(LearningGoals.learning_goal_names)
                .join(SessionDetails, SessionDetails.learning_goal_id == LearningGoals.id)
                .filter(SessionDetails.id == session_id)
                .first()
            )
            if not learning_goal:
                logger.warning(f"Learning goal not found for session ID {session_id}.", event_type='learning_goal_not_found')
                raise Exception("Learning goal not found for the session.")
            logger.info(f"Learning goal fetched successfully for session ID {session_id}.", event_type='learning_goal_fetched')
            return learning_goal
        except Exception as e:
            logger.error(f"Error fetching learning goal for session ID {session_id}: {str(e)}", event_type='learning_goal_fetch_error')
            raise Exception(f"Error fetching learning goal: {str(e)}")

    @staticmethod
    def get_recent_chat_history(db: Session, session_id: int, limit: int):
        """
        Get the last 'limit' number of chat interactions for a session.
        
        Args:
            db (Session): Database session for executing queries.
            session_id (int): The ID of the session for which chat history is fetched.
            limit (int): The number of recent chat messages to retrieve.
        
        Returns:
            list: A list of ChatHistory objects.
        
        Raises:
            Exception: If the chat history fetch fails.
        """
        try:
            chat_history = (
                db.query(ChatHistory)
                .filter_by(session_id=session_id)
                .order_by(ChatHistory.id.desc())
                .limit(limit)
                .all()
            )
            if not chat_history:
                logger.warning(f"No chat history found for session ID {session_id}.", event_type='no_chat_history')
            logger.info(f"Recent chat history fetched successfully for session ID {session_id}.", event_type='chat_history_fetched')
            return chat_history
        except Exception as e:
            logger.error(f"Error fetching chat history for session ID {session_id}: {str(e)}", event_type='chat_history_fetch_error')
            raise Exception(f"Error fetching chat history: {str(e)}")

    @staticmethod
    def store_chat_history(db: Session, session_id: int, ai_response: str, learner_response: str):
        """
        Store a new chat entry in the database.
        
        Args:
            db (Session): Database session for executing queries.
            session_id (int): The ID of the session for which the chat history is stored.
            ai_response (str): The AI-generated response to be stored.
            learner_response (str): The learner's response to be stored.
        
        Raises:
            Exception: If the chat entry cannot be stored.
        """
        try:
            chat_entry = ChatHistory(
                session_id=session_id,
                llm_response=ai_response,
                learner_response=learner_response
            )
            db.add(chat_entry)
            db.commit()
            db.refresh(chat_entry)
            logger.info(f"Chat history stored successfully for session ID {session_id}.", event_type='chat_history_stored')
        except Exception as e:
            logger.error(f"Error storing chat history for session ID {session_id}: {str(e)}", event_type='chat_history_store_error')
            raise Exception(f"Error storing chat history: {str(e)}")