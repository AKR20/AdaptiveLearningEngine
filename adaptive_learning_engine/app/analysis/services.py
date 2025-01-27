from sqlalchemy.orm import Session
from app.analysis.dao import AnalysisDAO
from app.core.open_ai_service import OpenAIService
from app.core.custom_logger import CustomLogger

logger = CustomLogger()

class AnalysisService:
    """
    Service class for handling chat interactions with the learner. 
    It retrieves session details, generates AI responses, and stores chat history.
    """
    @staticmethod
    def analyze_chat(db_session: Session, session_identifier: int):
        """
        Processes a chat request by retrieving session details, generating an AI response, and storing chat history.

        Args:
            db_session (Session): Database session for executing queries.
            session_identifier (int): The ID of the session for which chat is analyzed.

        Returns:
            dict: AI-generated response to the learner's input.

        Raises:
            Exception: If any part of the process fails.
        """
        try:
            logger.info(f"Processing chat request for session ID: {session_identifier}", event_type='PROCESS_CHAT_REQUEST')

            chat_history = AnalysisDAO().fetch_chat_history(db_session, session_identifier)

            # Format chat history for GPT prompt
            formatted_chat_history = [
                f"Learner: {entry.learner_response}\nAI: {entry.llm_response}"
                for entry in chat_history
            ]

            system_prompt = (
                '''
                You are an AI system designed to analyze a tutoring session transcript between an AI tutor and a learner. The transcript is provided by the user as an array of messages.

                1. Read through each message in the transcript carefully.
                2. Identify every time the AI tutor asks the learner a question (e.g., "What is X?", "Can you solve Y?"). Count how many questions were asked in total.
                3. Find all instances where the learner provided a wrong answer and was corrected by the tutor. Count how many times the learner answered incorrectly.
                4. Identify any misconceptions or misunderstandings the learner might have demonstrated (for example, confusing multiplication steps, making an arithmetic error, etc.).
                5. Based on the entire transcript, provide a concise feedback summary about the learner’s performance and areas to improve.
                6. Return your final result **strictly in valid JSON** with the following structure (do not include any extra keys):
                {
                "total_questions_asked": "<integer>", 
                "total_questions_answered_wrong": "<integer>", 
                "misconceptions": [ "<string>", "<string>" ], 
                "feedback": "<string>" 
                }
                '''
            )

            user_prompt = (
                f'''
                <transcript> = {formatted_chat_history}
                '''
            )
            openai_service = OpenAIService()
            ai_response = openai_service.generate_response_json(system_prompt, user_prompt)

            logger.info("Chat analysis completed successfully.", event_type='CHAT_ANALYSIS_SUCCESS')

            # Return response to the user
            return {
                "session_id": session_identifier,
                "ai_response": ai_response
            }

        except Exception as error:
            logger.error(f"Error processing chat for session ID {session_identifier}: {str(error)}", event_type='CHAT_ANALYSIS_ERROR')
            raise Exception(f"Error processing chat: {str(error)}")