from pydantic import BaseModel, Field
from typing import Literal, List
import uuid

class SupportTicket(BaseModel):
    """The final structured object returned to the user."""
    ticket_id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    issue_category: Literal["Hardware", "Software", "Access", "Inventory"]
    resolution_steps: List[str]
    status: Literal["Resolved", "Needs-Human", "Parts-Ordered"]
    summary: str