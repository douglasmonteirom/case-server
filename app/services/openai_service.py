from openai import OpenAI, OpenAIError
from app.config import OPENAI_API_KEY
from typing import List
from openai.types.chat import ChatCompletionMessageParam


class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    async def chat(self, messages: List[ChatCompletionMessageParam], model: str = "gpt-3.5-turbo") -> str:
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages
            )
            return response.choices[0].message.content or ""
        except OpenAIError as e:
            return f"Erro ao acessar OpenAI: {str(e)}" 
