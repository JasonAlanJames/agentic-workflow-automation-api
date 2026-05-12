from app.agent.policy import evaluate_task_risk
from app.schemas import AgentRoute, WorkflowDecision


def select_tool(task: str, decision: WorkflowDecision) -> str | None:
    if decision == WorkflowDecision.blocked_unsafe:
        return None

    normalized = task.lower()

    if "summarize" in normalized:
        return "summarize_text"

    if "classify" in normalized or "tag" in normalized or "prioritize" in normalized:
        return "classify_request"

    if "draft" in normalized or "reply" in normalized:
        return "draft_response"

    if "send email" in normalized or "send message" in normalized or "external message" in normalized:
        return "send_external_message"

    if "refund" in normalized or "charge" in normalized or "billing" in normalized:
        return "payment_action"

    return "general_workflow_action"


def route_workflow(task: str) -> AgentRoute:
    decision, risk_flags, reason = evaluate_task_risk(task)
    tool_name = select_tool(task, decision)

    return AgentRoute(
        decision=decision,
        tool_name=tool_name,
        reason=reason,
        risk_flags=risk_flags,
    )