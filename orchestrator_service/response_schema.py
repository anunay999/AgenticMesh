from pydantic import BaseModel
from typing import Optional, List, Dict, Union

class ExecutionTask(BaseModel):
    task_id: str
    description: str
    persona: str
    capability: str
    dependencies: List[str]

class ExecutionPlanResponse(BaseModel):
    execution_plan: List[ExecutionTask]

class Message(BaseModel):
    role: str
    content: str  # Assuming content is a JSON string representation of ExecutionPlanResponse

class Choice(BaseModel):
    index: int
    message: Message
    logprobs: Optional[Union[Dict, None]]
    finish_reason: str

class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class GenAIResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[Choice]
    usage: Usage
    system_fingerprint: str