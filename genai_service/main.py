from fastapi import HTTPException, APIRouter
import requests
from pydantic import BaseModel

from genai_service.config import settings  # Import the settings from config.py


router = APIRouter()

class GenAIQuery(BaseModel):
    persona: str
    user_prompt: str


@router.post("/query")
def query_genai(data: GenAIQuery):
    persona = data.persona
    user_prompt = data.user_prompt
    try:
        # Constructing the messages array with persona and user input
        messages = [
            {
                "role": "system",
                "content": persona
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]

        # Determine if running in a local environment
        if settings.environment == "local":
            # Bypass API key logic for local environment
            headers = {
                "Content-Type": "application/json"
            }
        else:
            # Include API key for non-local environments
            headers = {
                "Authorization": f"Bearer {settings.genai_api_key}",
                "Content-Type": "application/json"
            }

        data = {
            "messages": messages
        }

        response = requests.post("{0}{1}".format(settings.genai_api_url, settings.genai_chat_url), headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))