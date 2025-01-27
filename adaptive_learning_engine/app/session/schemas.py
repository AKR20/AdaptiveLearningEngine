from pydantic import BaseModel

class SessionCreate(BaseModel):
    learner_level: str
    learning_goal: str

class SessionResponse(BaseModel):
    id: int
    learning_goal: str
    student_initial_level: str
    student_current_level: str