import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("API_KEY")
FRONTEND_URL = os.getenv("FRONTEND_URL")