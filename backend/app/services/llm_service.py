import os

from dotenv import load_dotenv
from groq import AsyncGroq

load_dotenv()


class LLMService:

    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")

        if not self.api_key:
            raise ValueError("GROQ_API_KEY is not configured")

        self.client = AsyncGroq(api_key=self.api_key)

    async def generate_response(self, prompt: str):

        response = await self.client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are WeatherGPT, an intelligent weather assistant. "
                        "Give clear, concise and useful weather-related answers."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=500
        )

        return response.choices[0].message.content
