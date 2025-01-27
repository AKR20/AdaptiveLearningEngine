import os
from sqlalchemy.orm import Session
from openai import AzureOpenAI
from app.chatWithLearner.dao import ChatDAO
from app.chatWithLearner.schemas import ChatRequest, ChatResponse
from app.core.open_ai_service import OpenAIService
from app.core.custom_logger import CustomLogger

logger = CustomLogger()

class ChatService:
    """
    Service class for handling chat interactions with the learner. 
    It retrieves session details, generates AI responses, and stores chat history.
    """

    @staticmethod
    def process_chat(db: Session, chat_request: ChatRequest) -> ChatResponse:
        """
        Process a chat request by retrieving session details, generating an AI response, and storing chat history.

        Args:
            db (Session): Database session for executing queries.
            chat_request (ChatRequest): The chat request containing session ID and learner's input.

        Returns:
            ChatResponse: AI-generated response to the learner's input.

        Raises:
            Exception: If any part of the process fails.
        """
        try:
            logger.info(f"Processing chat request for session ID: {chat_request.session_id}", event_type='process_chat')

            # Fetch session details
            session = ChatDAO.get_session_by_id(db, chat_request.session_id)
            if not session:
                logger.error("Session not found.", event_type='session_not_found')
                raise Exception("Invalid session ID.")

            # Get learning goal name
            learning_goal = ChatDAO.get_learning_goal_by_session(db, chat_request.session_id)
            if not learning_goal:
                logger.error("Learning goal not found.", event_type='learning_goal_not_found')
                raise Exception("Learning goal not found for this session.")

            # Retrieve last 3 chat history messages for context
            chat_history = ChatDAO.get_recent_chat_history(db, chat_request.session_id, limit=3)

            # Format chat history for GPT prompt
            formatted_chat_history = [
                f"Learner: {entry.learner_response}\nAI: {entry.llm_response}"
                for entry in chat_history
            ]

            user_prompt = (
f'''
You are an intelligent tutor AI designed to validate user answers and adjust question difficulty dynamically based on the question-answer history of the learner.
### Instructions:

1. **Learning Goal:** {learning_goal.learning_goal_names}  
2. **Current Difficulty Level:** {session.student_current_level}  
3. **Chat History:** 
   - {formatted_chat_history}
4. **Latest Learner Response:** 
   - {chat_request.learner_response}

---

### Adaptive Learning Flow:

- **If this is the first conversation (empty chat history or learner response):**  
  - Provide an overview of the topic "{learning_goal.learning_goal_names}" to help the learner get started.  
  - Avoid asking direct questions initially; instead, explain key concepts and fundamentals.

- **If there is existing chat history:**  
  - Validate the user's most recent response and compare it to the correct answer.  
  - Follow these response guidelines based on the evaluation:
    1. **Correct Answer:**  
       - Provide positive reinforcement and progress the learner to the next level of difficulty.  
       - Example response: "Great job! Let's move to a more challenging question..."
    2. **Partially Correct Answer:**  
       - Acknowledge the learner’s effort, clarify mistakes, and provide helpful explanations.  
       - Example response: "You're on the right track, but consider this aspect..."
    3. **Incorrect Answer:**  
       - Respond empathetically and offer detailed guidance on the correct answer.  
       - Lower the difficulty level if necessary (unless already at Beginner level).  
       - Example response: "That's okay! Here’s an explanation to help you understand better..."

- **Generating Next Question:**  
  - Based on the learner’s performance, dynamically adjust the next question's difficulty and focus on reinforcing key concepts.  
  - Ensure questions progressively build understanding without overwhelming the learner.

**Example 1: First Conversation (No Chat History)**  

_Input:_  
- Topic: "Algebra"  
- Level: "Beginner"  
- Chat History: (empty)  
- Learner Response: (empty)  

_Output:_  
"Welcome! Algebra is the study of variables and how they interact. Let's start by understanding basic terms like variables, coefficients, and equations. For example, in 2x + 3 = 7, can you identify the variable?"

---

**Example 2: Correct Answer**  

_Input:_  
- Topic: "Geometry"  
- Level: "Intermediate"  
- Question: "What is the sum of interior angles in a triangle?"  
- Learner Response: "180 degrees"  

_Output:_  
"Great job! You're correct. The sum of interior angles in a triangle is always 180 degrees. Let's try something more challenging: How do you calculate the angles in an isosceles triangle if one of the base angles is 50 degrees?"

---

**Example 3: Partially Correct Answer**  

_Input:_  
- Topic: "Physics"  
- Level: "Advanced"  
- Question: "What is Newton's Second Law?"  
- Learner Response: "Force equals acceleration."  

_Output:_  
"You're close! Newton's Second Law states that force equals mass times acceleration (F = ma). Let's dive deeper into how this applies in real-world scenarios."

---

**Example 4: Incorrect Answer**  

_Input:_  
- Topic: "Biology"  
- Level: "Beginner"  
- Question: "What is the function of mitochondria?"  
- Learner Response: "It helps in digestion."  

_Output:_  
"That's a good attempt! However, mitochondria are known as the powerhouse of the cell because they generate energy. Let’s try again: What role do mitochondria play in cellular respiration?"

---

### **Generating the Next Question:**  
- Based on the student's performance, formulate an appropriate follow-up question that gradually builds understanding without overwhelming the learner.
'''
            )

            system_prompt = "You are an educational AI tutor."
            openai_service = OpenAIService()
            ai_response = openai_service.generate_response(system_prompt, user_prompt)

            # Store chat history in the database
            ChatDAO.store_chat_history(db, session.id, ai_response, chat_request.learner_response)

            logger.info("Chat successfully processed.", event_type='chat_success')

            # Return response to the user
            return ChatResponse(
                session_id=session.id,
                learner_input=chat_request.learner_response,
                ai_response=ai_response
            )

        except Exception as e:
            logger.error(f"Error processing chat: {str(e)}", event_type='chat_processing_error')
            raise Exception(str(e))