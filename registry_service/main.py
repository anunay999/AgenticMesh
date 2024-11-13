from typing import List, Optional

from fastapi import FastAPI, HTTPException, Depends, APIRouter, Query
from sqlalchemy.orm import Session
from registry_service import models, schemas
from registry_service.database import engine, Base, get_db
import json  # Import json to handle conversion between strings and lists

from registry_service.models import Agent
from langchain_ollama import ChatOllama


# Initialize the database
Base.metadata.create_all(bind=engine)

router = APIRouter()

# Include the registry and discovery_service routers

def parse_list(value: str):
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return []  # Return an empty list if parsing fails

@router.post("/agents/", response_model=schemas.AgentResponse)
def register_agent(agent: schemas.AgentCreate, db: Session = Depends(get_db)):
    db_agent = db.query(models.Agent).filter(models.Agent.agent_id == agent.agent_id).first()
    if db_agent:
        raise HTTPException(status_code=400, detail="Agent already registered")
    new_agent = models.Agent(
        agent_id=agent.agent_id,
        purpose=agent.purpose,
        owner=agent.owner,
        capabilities=json.dumps(agent.capabilities),  # Convert list to string for storage
        policies=json.dumps(agent.policies),  # Convert list to string for storage
        status=agent.status,
    )
    db.add(new_agent)
    db.commit()
    db.refresh(new_agent)
    return {
        "agent_id": new_agent.agent_id,
        "purpose": new_agent.purpose,
        "owner": new_agent.owner,
        "capabilities": parse_list(new_agent.capabilities),  # Convert string back to list
        "policies": parse_list(new_agent.policies),  # Convert string back to list
        "status": new_agent.status
    }

@router.get("/agents/{agent_id}", response_model=schemas.AgentResponse)
def get_agent(agent_id: str, db: Session = Depends(get_db)):
    agent = db.query(models.Agent).filter(models.Agent.agent_id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {
        "agent_id": agent.agent_id,
        "purpose": agent.purpose,
        "owner": agent.owner,
        "capabilities": parse_list(agent.capabilities),  # Convert string back to list
        "policies": parse_list(agent.policies),  # Convert string back to list
        "status": agent.status
    }

@router.put("/agents/{agent_id}", response_model=schemas.AgentResponse)
def update_agent(agent_id: str, updates: schemas.AgentUpdate, db: Session = Depends(get_db)):
    agent = db.query(models.Agent).filter(models.Agent.agent_id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    update_data = updates.dict(exclude_unset=True)
    for key, value in update_data.items():
        if key in ["capabilities", "policies"] and value is not None:
            setattr(agent, key, json.dumps(value))  # Convert list to string for storage
        else:
            setattr(agent, key, value)
    db.commit()
    db.refresh(agent)
    return {
        "agent_id": agent.agent_id,
        "purpose": agent.purpose,
        "owner": agent.owner,
        "capabilities": parse_list(agent.capabilities),  # Convert string back to list
        "policies": parse_list(agent.policies),  # Convert string back to list
        "status": agent.status
    }

@router.get("/agents/", response_model=list[schemas.AgentResponse])
def get_all_agents(db: Session = Depends(get_db)):
    agents = db.query(models.Agent).all()
    # Convert capabilities and policies from strings back to lists
    return [
        {
            "agent_id": agent.agent_id,
            "purpose": agent.purpose,
            "owner": agent.owner,
            "capabilities": parse_list(agent.capabilities),  # Convert string back to list
            "policies": parse_list(agent.policies),  # Convert string back to list
            "status": agent.status
        }
        for agent in agents
    ]


def query_agents(purpose: Optional[str], capabilities: List[str], db: Session):
    agents = get_all_agents(db)

    filtered_agents = [
        agent for agent in agents
        if (purpose and agent["purpose"] == purpose) or
           (capabilities and any(cap in agent["capabilities"] for cap in capabilities))
    ]
    return filtered_agents

@router.get("/agents/search/", response_model=List[schemas.AgentResponse])
def search_agents(
    purpose: Optional[str] = Query(None, description="Filter agents by purpose"),
    capability: Optional[List[str]] = Query(None, description="Filter agents by one or more capabilities"),
    db: Session = Depends(get_db)
):
    """
    Searches for agents based on provided criteria (purpose, capabilities).
    """
    capabilities_list = capability if capability else []
    agents = query_agents(purpose=purpose, capabilities=capabilities_list, db=db)
    return agents