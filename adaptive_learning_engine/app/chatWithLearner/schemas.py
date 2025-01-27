from pydantic import BaseModel

class ChatRequest(BaseModel):
    session_id: int
    learner_response: str

class ChatResponse(BaseModel):
    session_id: int
    learner_input: str
    ai_response: str
