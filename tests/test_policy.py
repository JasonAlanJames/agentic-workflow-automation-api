from app.agent.policy import evaluate_task_risk
from app.schemas import WorkflowDecision


def test_safe_task_is_auto_executable():
    decision, risk_flags, reason = evaluate_task_risk(
        "Summarize this customer support message"
    )

    assert decision == WorkflowDecision.safe_auto_execute
    assert risk_flags == []
    assert "automatically" in reason


def test_external_action_requires_approval():
    decision, risk_flags, reason = evaluate_task_risk(
        "Send email to this sales lead"
    )

    assert decision == WorkflowDecision.requires_approval
    assert risk_flags
    assert "approval" in reason.lower()


def test_destructive_action_is_blocked():
    decision, risk_flags, reason = evaluate_task_risk(
        "Delete customer record from the database"
    )

    assert decision == WorkflowDecision.blocked_unsafe
    assert risk_flags
    assert "cannot be executed" in reason