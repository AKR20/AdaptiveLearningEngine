import os
from openai import AzureOpenAI
from app.core.custom_logger import CustomLogger

logger = CustomLogger()

class OpenAIService:
    """
    A service class to interact with Azure OpenAI GPT model.
    """

    def __init__(self):
        """
        Initialize the OpenAIService and set up logging.
        """
        self.client = self._get_openai_client()

    def _get_openai_client(self) -> AzureOpenAI:
        """
        Get an instance of the Azure OpenAI client.

        Returns:
            AzureOpenAI: Configured OpenAI client instance.
        """
        try:
            client = AzureOpenAI(
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                api_version="2024-02-01",
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
            )
            logger.info("Successfully initialized OpenAI client.", event_type='openai_client_init')
            return client
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {str(e)}", event_type='openai_client_error')
            raise Exception("Error connecting to AI service. Please try again later.")

    def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        """
        Generate a response from the Azure OpenAI GPT model.

        Args:
            system_prompt (str): The system-level instruction to guide the AI behavior.
            user_prompt (str): The user's input question or request.

        Returns:
            str: The AI-generated response.
        """
        try:
            logger.info("Calling OpenAI GPT model...", event_type='gpt_call')
            response = self.client.chat.completions.create(
                model=os.getenv('AZURE_OPENAI_MODEL_NAME'),
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            ai_response = response.choices[0].message.content
            logger.info("Received response from OpenAI GPT model.", event_type='gpt_response_success')
            return ai_response
        except Exception as e:
            logger.error(f"Error during GPT call: {str(e)}", event_type='gpt_call_error')
            raise Exception("AI response generation failed. Please try again later.")
        
    def generate_response_json(self, system_prompt: str, user_prompt: str) -> str:
        """
        Generate a response from the Azure OpenAI GPT model in JSON format.

        Args:
            system_prompt (str): The system-level instruction to guide the AI behavior.
            user_prompt (str): The user's input question or request.

        Returns:
            str: The AI-generated response.
        """
        try:
            logger.info("Calling OpenAI GPT model...", event_type='gpt_call')
            response = self.client.chat.completions.create(
                model=os.getenv('AZURE_OPENAI_MODEL_NAME'),
                response_format={ "type": "json_object" },
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            ai_response = response.choices[0].message.content
            logger.info("Received response from OpenAI GPT model.", event_type='gpt_response_success')
            return ai_response
        except Exception as e:
            logger.error(f"Error during GPT call: {str(e)}", event_type='gpt_call_error')
            raise Exception("AI response generation failed. Please try again later.")