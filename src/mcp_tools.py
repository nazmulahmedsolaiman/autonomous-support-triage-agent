from typing import Dict, List, Tuple


KB_ARTICLES: Dict[str, Tuple[str, float, str]] = {
    "network_vpn": (
        "KB-101: Reset VPN split-tunnel cache, verify MFA token sync, and restart the VPN client.",
        0.86,
        "https://kb.internal/network/vpn-mfa-reset",
    ),
    "iam_access": (
        "KB-204: Verify least-privilege IAM group membership and trigger GPO / SSO token refresh.",
        0.82,
        "https://kb.internal/iam/access-refresh",
    ),
    "application_bug": (
        "KB-309: Capture HAR/console logs and escalate reproducible application defects to L2/Vendor.",
        0.55,
        "https://kb.internal/apps/bug-escalation",
    ),
    "hardware_os": (
        "KB-412: Run Windows/M365 diagnostics, check driver updates, and verify peripheral connectivity.",
        0.80,
        "https://kb.internal/desktop/hardware-checks",
    ),
    "general": (
        "KB-001: Standard L1 intake checklist and user verification.",
        0.60,
        "https://kb.internal/general/intake",
    ),
}

SLA_POLICY_MINUTES: Dict[str, int] = {
    "P1": 15,
    "P2": 60,
    "P3": 240,
    "P4": 1440,
}


def search_knowledge_base(category: str, query: str) -> Tuple[str, float, List[str]]:
    """MCP tool: retrieves grounded KB guidance and confidence score (Qdrant fallback-ready)."""
    guidance, score, ref = KB_ARTICLES.get(category, KB_ARTICLES["general"])
    if "outage" in query.lower() or "security" in query.lower():
        score = min(score, 0.50)
    return guidance, score, [ref]


def check_sla_policy(priority: str) -> int:
    """MCP tool: returns target SLA resolution window in minutes."""
    return SLA_POLICY_MINUTES.get(priority, 240)


def escalate_ticket(ticket_id: str, priority: str, reason: str) -> str:
    """MCP tool: formats structured L2/Vendor escalation payload."""
    return f"Escalated {ticket_id} ({priority}) to L2 Engineering: {reason}"
