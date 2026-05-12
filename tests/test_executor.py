from app.agent.executor import approve_workflow, submit_workflow
from app.schemas import WorkflowStatus


def test_safe_workflow_executes_immediately():
    response = submit_workflow(
        user_id="test-user",
        task="Summarize this customer support message",
        context={"text": "Customer needs help with a billing question."},
    )

    assert response["status"] == WorkflowStatus.completed
    assert response["result"]["executed"] is True
    assert response["route"].tool_name == "summarize_text"


def test_approval_workflow_waits_for_human_approval():
    response = submit_workflow(
        user_id="test-user",
        task="Send email to this sales lead",
        context={"recipient": "Alex"},
    )

    assert response["status"] == WorkflowStatus.pending_approval

    approval = approve_workflow(
        workflow_id=response["workflow_id"],
        approved_by="manager",
        approved=True,
        note="Approved for simulated send.",
    )

    assert approval["status"] == WorkflowStatus.approved
    assert approval["result"]["executed"] is True


def test_blocked_workflow_does_not_execute():
    response = submit_workflow(
        user_id="test-user",
        task="Delete customer record from the database",
        context={},
    )

    assert response["status"] == WorkflowStatus.blocked
    assert response["result"] is None