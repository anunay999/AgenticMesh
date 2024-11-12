from sqlalchemy import Column, String, Text
from registry_service.database import Base

class Agent(Base):
    __tablename__ = "agents"

    agent_id = Column(String, primary_key=True, index=True)
    purpose = Column(String, index=True)
    owner = Column(String)
    capabilities = Column(Text)  # JSON string for simplicity
    policies = Column(Text)
    status = Column(String, default="inactive")