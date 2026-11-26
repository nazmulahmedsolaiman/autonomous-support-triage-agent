from typing import List, Literal, Optional, TypedDict
from pydantic import BaseModel, Field


Priority = Literal["P1", "P2", "P3", "P4"]
Category = Literal["network_vpn", "iam_access", "application_bug", "hardware_os", "general"]


class TicketInput(BaseModel):
    ticket_id: str = Field(..., examples=["INC-1042"])
    user_email: str = Field(..., examples=["user@company.com"])
    subject: str = Field(..., min_length=3)
    description: str = Field(..., min_length=5)


class TriageResponse(BaseModel):
    ticket_id: str
    category: Category
    priority: Priority
    sla_minutes: int
    action: Literal["auto_resolved", "escalated_to_l2"]
    confidence: float
    kb_references: List[str]
    response_message: str
    escalation_reason: Optional[str] = None


class AgentState(TypedDict):
    ticket_id: str
    subject: str
    description: str
    category: Category
    priority: Priority
    sla_minutes: int
    kb_references: List[str]
    confidence: float
    action: str
    response_message: str
    escalation_reason: Optional[str]
