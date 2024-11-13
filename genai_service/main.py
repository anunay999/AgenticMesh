import json

from fastapi import HTTPException, APIRouter
import requests
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from openai import models
from pandas.io.sql import execute
from pydantic import BaseModel
from orchestrator_service.response_schema import ExecutionPlanResponse


from genai_service.config import settings  # Import the settings from config.py


router = APIRouter()

class GenAIQuery(BaseModel):
    persona: str
    user_prompt: str

@router.post("/query")
def query_chat_ai(data: GenAIQuery) -> dict:
    persona = data.persona
    user_prompt = data.user_prompt

    # Construct the messages array with persona and user input
    messages = [
        {
            "role": "assistant",
            "content": persona
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]

    try:
        # Initialize the appropriate chat model based on the environment
        if settings.environment == "local":
            # Use ChatOllama for local environment
            chat_model = ChatOllama(model="llama3.2")
        else:
            # Use ChatOpenAI for production environment
            chat_model = ChatOpenAI(api_key=settings.genai_api_key)

        # Interact with the model using LangChain's abstraction
        response = chat_model.invoke(messages)

        response = json.loads(response.content)

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))