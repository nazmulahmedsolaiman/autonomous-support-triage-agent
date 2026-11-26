from fastapi import FastAPI
from src.config import settings
from src.graph import run_triage_workflow
from src.models import TicketInput, TriageResponse

app = FastAPI(
    title="Autonomous Enterprise Support & Triage Agent",
    version="1.0.0",
    description="LangGraph + MCP + RAG multi-agent ticket triage API",
)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": settings.app_name}


@app.post("/api/v1/triage", response_model=TriageResponse)
def triage_ticket(ticket: TicketInput):
    result = run_triage_workflow(
        ticket_id=ticket.ticket_id,
        subject=ticket.subject,
        description=ticket.description,
    )
    return TriageResponse(
        ticket_id=result["ticket_id"],
        category=result["category"],
        priority=result["priority"],
        sla_minutes=result["sla_minutes"],
        action=result["action"],
        confidence=result["confidence"],
        kb_references=result["kb_references"],
        response_message=result["response_message"],
        escalation_reason=result["escalation_reason"],
    )
