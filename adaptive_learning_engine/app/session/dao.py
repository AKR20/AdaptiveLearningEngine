from sqlalchemy.orm import Session
from app.session.models import SessionDetails, LearningGoals, ChatHistory
from app.core.custom_logger import CustomLogger

logger = CustomLogger()

class SessionDAO:
    """
    Data Access Object (DAO) layer responsible for interacting with the database for session and learning goal data.
    """
    
    @staticmethod
    def get_learning_goal_by_name(db: Session, goal_name: str):
        """
        Retrieves the learning goal object by its name from the database.
        
        Args:
        - db (Session): The database session.
        - goal_name (str): The name of the learning goal to search for.
        
        Returns:
        - LearningGoals: The learning goal object, or None if not found.
        
        Raises:
        - Exception: If there are database issues while querying.
        """
        try:
            logger.info(f"Fetching learning goal by name: {goal_name}", event_type='get_learning_goal_by_name')
            learning_goal = db.query(LearningGoals).filter(LearningGoals.learning_goal_names == goal_name).first()
            if not learning_goal:
                logger.warning(f"Learning goal '{goal_name}' not found:", event_type='get_learning_goal_by_name')
            return learning_goal
        except Exception as e:
            logger.error(f"Error occurred while fetching learning goal by name: {str(e)}", )
            raise Exception("An error occurred while fetching the learning goal.")
    
    @staticmethod
    def create_session(db: Session, session: SessionDetails):
        """
        Adds a new session to the database.
        
        Args:
        - db (Session): The database session.
        - session (SessionDetails): The session object to be added to the database.
        
        Returns:
        - SessionDetails: The created session object.
        
        Raises:
        - Exception: If there are issues with committing the session to the database.
        """
        try:
            logger.info("Adding new session to the database.", event_type='create_session')
            db.add(session)
            db.commit()
            db.refresh(session)
            logger.info(f"Session successfully added with ID: {session.id}", event_type='create_session')
            return session
        except Exception as e:
            logger.error(f"Error occurred while creating the session: {str(e)}", event_type='create_session')
            raise Exception("An error occurred while creating the session.")
        
    @staticmethod
    def get_complete_chat_history(db: Session, session_id: int):
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
    def get_learning_goal_and_session_details(db: Session, session_id: int):
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
            details = (
                db.query(LearningGoals.learning_goal_names,
                         SessionDetails.student_initial_level
                         )
                .join(SessionDetails, SessionDetails.learning_goal_id == LearningGoals.id)
                .filter(SessionDetails.id == session_id)
                .first()
            )
            if not details:
                logger.warning(f"Learning goal not found for session ID {session_id}.", event_type='learning_goal_not_found')
                raise Exception("Learning goal not found for the session.")
            logger.info(f"Learning goal fetched successfully for session ID {session_id}.", event_type='learning_goal_fetched')
            return details
        except Exception as e:
            logger.error(f"Error fetching learning goal for session ID {session_id}: {str(e)}", event_type='learning_goal_fetch_error')
            raise Exception(f"Error fetching learning goal: {str(e)}")