from sqlalchemy.orm import Session
from app.chatWithLearner.models import ChatHistory
from app.core.custom_logger import CustomLogger

logger = CustomLogger()

class AnalysisDAO:
    """
    Data Access Object (DAO) class for interacting with the database for chat-related operations.
    It includes methods for fetching session details, learning goals, chat history, and storing chat entries.
    """

    @staticmethod
    def fetch_chat_history(db_session: Session, session_identifier: int):
        """
        Retrieves the complete chat history for a given session.

        Args:
            db_session (Session): Database session for executing queries.
            session_identifier (int): The ID of the session for which chat history is fetched.

        Returns:
            list: A list of ChatHistory objects containing the session's chat records.

        Raises:
            Exception: If the chat history retrieval process fails.
        """
        try:
            chat_records = (
                db_session.query(ChatHistory)
                .filter_by(session_id=session_identifier)
                .order_by(ChatHistory.id.desc())
                .all()
            )
            if not chat_records:
                logger.warning(f"No chat history found for session ID {session_identifier}.", event_type='CHAT_HISTORY_NOT_FOUND')
            logger.info(f"Chat history successfully retrieved for session ID {session_identifier}.", event_type='CHAT_HISTORY_RETRIEVED')
            return chat_records
        except Exception as error:
            logger.error(f"Failed to retrieve chat history for session ID {session_identifier}: {str(error)}", event_type='CHAT_HISTORY_RETRIEVAL_ERROR')
            raise Exception(f"Failed to retrieve chat history: {str(error)}")