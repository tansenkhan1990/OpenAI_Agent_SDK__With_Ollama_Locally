from pydantic import BaseModel, Field
from typing import Literal, List
import uuid

class AgentResponse(BaseModel):
    """The standard output for every interaction."""
    ticket_id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    status: Literal["Success", "Failed", "Pending"]
    summary: str = Field(..., description="What the agent actually did.")
    logs: List[str] = Field(default_factory=list)