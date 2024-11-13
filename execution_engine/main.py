from fastapi import APIRouter
import requests
from pydantic import BaseModel
import json
from orchestrator_service.response_schema import ExecutionPlanResponse

router = APIRouter()

class ExecutionQuery(BaseModel):
    user_prompt: str


@router.post("/query")
def generate_execution_plan(query: ExecutionQuery):
    execution_plan = requests.post(
        "http://localhost:8000/orchestrator/plan",
        json={
            "task_description": query.user_prompt
        })

    execution_plan = execution_plan.json()

    output = execute_plan(execution_plan)
    return output# This should be structured as a dictionary outlining the steps


def execute_plan(plan):
    return plan