from fastapi import APIRouter
import requests
from langchain_ollama import ChatOllama
from pydantic import BaseModel
import json
from langchain_core.messages import AIMessage

from orchestrator_service.response_schema import GenAIResponse, ExecutionPlanResponse

router = APIRouter()

class OrchestratorQuery(BaseModel):
    task_description: str


@router.post("/plan")
def generate_execution_plan(query: OrchestratorQuery) -> dict:
    """
    Generates an execution plan for the given task description using a GenAI service.
    """
    response = requests.post(
        "http://localhost:8000/genai/query",
        json={
            "persona": "You are an expert orchestrator tasked with generating detailed execution plans for complex tasks.",
            "user_prompt": f"""
            "{query.task_description}". For each step in the plan, only provide the following and nothing else:

            1. A unique task identifier (task_id).
            2. A description of the task.
            3. A persona that captures the essence of the role responsible for completing the task, describing their mindset, approach, and goals.
            4. The primary capability required to accomplish the task.
            5. A list of dependencies (if applicable) that indicate which tasks must be completed before this task can start.

            Use this structure to provide your response:

            {{
              "execution_plan": [
                {{
                  "task_id": "task_001",
                  "description": "Clean customer data",
                  "persona": "You are a meticulous data cleaner who ensures data quality and consistency.",
                  "capability": "data cleaning",
                  "dependencies": []
                }},
                {{
                  "task_id": "task_002",
                  "description": "Analyze customer data",
                  "persona": "You are a data analyst who uncovers trends and insights from datasets.",
                  "capability": "data analysis",
                  "dependencies": ["task_001"]
                }},
                {{
                  "task_id": "task_003",
                  "description": "Train a predictive model using customer data",
                  "persona": "You are a machine learning engineer who builds and tunes predictive models.",
                  "capability": "model training",
                  "dependencies": ["task_002"]
                }},
                {{
                  "task_id": "task_004",
                  "description": "Optimize the trained model for deployment",
                  "persona": "You are a model optimizer who ensures models run efficiently in production.",
                  "capability": "optimization",
                  "dependencies": ["task_003"]
                }}
              ]
            }}
            """
        }
    )

    return response.json()  # This should be structured as a dictionary outlining the steps