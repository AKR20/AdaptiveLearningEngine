# AdaptiveLearningEngine

## Introduction
The Adaptive Learning Engine leverages advanced algorithms to tailor educational content to each learner. By continuously analyzing performance data, the engine provides customized paths to enhance learning outcomes.

## Features
- Personalized content recommendations
- Real-time performance tracking
- Dynamic difficulty adjustment
- User-friendly interface

## Setup Instructions
1. Clone the repository:
   git clone https://github.com/AKR20/AdaptiveLearningEngine.git
   
2. Navigate to the project directory:
   cd AdaptiveLearningEngine/adaptive_learning_engine

3. Install the required dependencies:
   pip install -r requirements.txt

4. Create DB, tables and insert data.
   python3 temp.py

5. Start the server using uvicorn
   uvicorn app.main:app --host 0.0.0.0 --port 70 --reload

## API Documentation

### 1. Sessions
Handles session creation and recommendation retrieval for learners.

Endpoints:
POST /create-session – Creates a new learning session.
![image](https://github.com/user-attachments/assets/b29e6149-1e48-445d-96cc-c78f2776b001)

POST /session/{id}/recommendation – Retrieves AI-driven recommendations for a session.
![image](https://github.com/user-attachments/assets/04604dfe-1ccb-48b8-b276-874813a5d0d2)

### 2. Analysis
Handles chat session analysis for adaptive learning by storing chat history and generating responses.

Endpoints:
POST /analytics/student/{session_id} – Analyzes a chat session and generates the next response.
![image](https://github.com/user-attachments/assets/82a45edb-349d-4d7a-a13e-263aaed8778b)

### 3. ChatWithLearner
Handles chat interactions with GPT for adaptive learning by storing chat history and generating AI-driven responses.

Endpoints:
POST /chat-with-gpt – Processes learner responses and generates the next question
![image](https://github.com/user-attachments/assets/1ced674e-8e9c-4d0d-957c-9efcc23a63ca)
![image](https://github.com/user-attachments/assets/1c493af5-ffff-4753-bca0-22df7209c9b6)
![image](https://github.com/user-attachments/assets/2c81ee79-d385-41a4-b127-668f25109d7d)
![image](https://github.com/user-attachments/assets/f7593506-0f94-4bac-8d27-54e502d91cc0)
![image](https://github.com/user-attachments/assets/a06d22d7-f24e-4754-860c-0d33b26aca33)
![image](https://github.com/user-attachments/assets/0a2e1ac8-f18c-48d5-ab59-cec0e3a3a7c0)




