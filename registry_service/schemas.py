from pydantic import BaseModel
from typing import Optional, List

class AgentBase(BaseModel):
    agent_id: str
    purpose: str
    owner: str
    capabilities: List[str]
    policies: List[str]
    status: Optional[str] = "inactive"

class AgentCreate(AgentBase):
    pass

class AgentUpdate(BaseModel):
    purpose: Optional[str] = None
    owner: Optional[str] = None
    capabilities: Optional[List[str]] = None
    policies: Optional[List[str]] = None
    status: Optional[str] = None

class AgentResponse(AgentBase):
    class Config:
        orm_mode = True