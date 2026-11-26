from src.config import settings
from src.mcp_tools import check_sla_policy, escalate_ticket, search_knowledge_base
from src.models import AgentState, Category, Priority


def classify_ticket(state: AgentState) -> AgentState:
    text = f"{state['subject']} {state['description']}".lower()
    category: Category = "general"
    priority: Priority = "P3"

    if any(k in text for k in ["vpn", "wifi", "network", "dns", "mfa"]):
        category = "network_vpn"
        priority = "P2"
    elif any(k in text for k in ["iam", "permission", "access", "gpo", "password", "sso"]):
        category = "iam_access"
        priority = "P2"
    elif any(k in text for k in ["bug", "crash", "500", "error", "exception"]):
        category = "application_bug"
        priority = "P2"
    elif any(k in text for k in ["laptop", "printer", "windows", "m365", "outlook"]):
        category = "hardware_os"
        priority = "P3"

    if any(k in text for k in ["outage", "down", "breach", "unauthorized", "production"]):
        priority = "P1"

    state["category"] = category
    state["priority"] = priority
    state["sla_minutes"] = check_sla_policy(priority)
    return state


def rag_lookup(state: AgentState) -> AgentState:
    query = f"{state['subject']} {state['description']}"
    guidance, confidence, refs = search_knowledge_base(state["category"], query)
    state["kb_references"] = refs
    state["confidence"] = confidence
    state["response_message"] = guidance
    return state


def route_decision(state: AgentState) -> AgentState:
    if state["priority"] == "P1" or state["confidence"] < settings.confidence_threshold:
        reason = (
            "P1 critical incident requires human verification"
            if state["priority"] == "P1"
            else f"RAG confidence {state['confidence']:.2f} below threshold {settings.confidence_threshold:.2f}"
        )
        state["action"] = "escalated_to_l2"
        state["escalation_reason"] = reason
        state["response_message"] = escalate_ticket(state["ticket_id"], state["priority"], reason)
    else:
        state["action"] = "auto_resolved"
        state["escalation_reason"] = None
    return state


def run_triage_workflow(ticket_id: str, subject: str, description: str) -> AgentState:
    state: AgentState = {
        "ticket_id": ticket_id,
        "subject": subject,
        "description": description,
        "category": "general",
        "priority": "P3",
        "sla_minutes": 240,
        "kb_references": [],
        "confidence": 0.0,
        "action": "auto_resolved",
        "response_message": "",
        "escalation_reason": None,
    }
    state = classify_ticket(state)
    state = rag_lookup(state)
    state = route_decision(state)
    return state
