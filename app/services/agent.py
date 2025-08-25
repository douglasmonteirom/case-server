import json
from app.services.openai_service import OpenAIService

class EmailAgent:
    def __init__(self, openai_service: OpenAIService):
        self.openai_service = openai_service

    async def analyze_email(self, text: str) -> dict:
        messages = self.build_prompt(text)
        result = await self.openai_service.chat(messages)
        return self.parse_result(result)

    def build_prompt(self, text: str) -> list:
        return [
            {"role": "system", "content": (
                "Você é um assistente que recebe e analisa textos de email, "
                "categoriza o conteúdo em Produtivo ou Improdutivo e sugere uma resposta "
                "adequada no formato JSON: {\"category\": \"...\", \"suggestion\": \"...\"}"
            )},
            {"role": "user", "content": text}
        ]

    def parse_result(self, result: str) -> dict:
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return {"category": "Unknown", "suggestion": result}
