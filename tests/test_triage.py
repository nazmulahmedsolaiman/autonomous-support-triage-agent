from src.graph import run_triage_workflow


def test_vpn_ticket_auto_resolves():
    result = run_triage_workflow(
        ticket_id="INC-1001",
        subject="VPN disconnects after MFA",
        description="Cannot stay connected to corporate VPN.",
    )
    assert result["category"] == "network_vpn"
    assert result["action"] == "auto_resolved"
    assert result["confidence"] >= 0.75


def test_p1_outage_escalates():
    result = run_triage_workflow(
        ticket_id="INC-1002",
        subject="Production server outage",
        description="All users experiencing 500 errors in production.",
    )
    assert result["priority"] == "P1"
    assert result["sla_minutes"] == 15
    assert result["action"] == "escalated_to_l2"
