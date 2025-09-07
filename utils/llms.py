import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

class LLMModel:
    def __init__(self, model_name="gemini-1.5-flash"):
        if not API_KEY:
            raise ValueError("GEMINI_API_KEY is not set in the environment.")
        self.model_name = model_name
        self.google_model = ChatGoogleGenerativeAI(google_api_key=API_KEY, model=self.model_name)

    def get_model(self):
        return self.google_model
