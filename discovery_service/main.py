from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from registry_service import models  # Import models from registry_service
from registry_service.database import get_db
from registry_service.schemas import AgentResponse
from typing import List, Optional
import json

router = APIRouter()

def parse_list(value: str):
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return []

@router.get("/", response_model=List[AgentResponse])
def discover_agents(
    purpose: Optional[str] = None,
    capability: Optional[str] = None,
    owner: Optional[str] = None,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    sort_by: Optional[str] = None
):
    query = db.query(models.Agent)
    if purpose:
        query = query.filter(models.Agent.purpose == purpose)
    if owner:
        query = query.filter(models.Agent.owner == owner)
    if capability:
        query = query.filter(models.Agent.capabilities.contains(capability))
    if sort_by in ["purpose", "owner", "status"]:
        query = query.order_by(getattr(models.Agent, sort_by))
    agents = query.offset(skip).limit(limit).all()
    return [
        {
            "agent_id": agent.agent_id,
            "purpose": agent.purpose,
            "owner": agent.owner,
            "capabilities": parse_list(agent.capabilities),
            "policies": parse_list(agent.policies),
            "status": agent.status
        }
        for agent in agents
    ]