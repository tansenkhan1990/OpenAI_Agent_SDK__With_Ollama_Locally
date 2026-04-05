from pydantic import BaseModel, Field
from typing import Literal, List
import uuid

class AgentResponse(BaseModel):
    ticket_id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    status: Literal["Success", "Failed", "Action-Needed"]
    summary: str = Field(..., description="What was done in natural language.")
    affected_count: int = 0