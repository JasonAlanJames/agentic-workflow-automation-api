import uuid
from typing import Any, Dict

from app.agent.router import route_workflow
from app.schemas import WorkflowDecision, WorkflowStatus
from app.storage.audit_log import get_workflow_events, write_audit_event
from app.tools.business_tools import TOOL_REGISTRY


PENDING_WORKFLOWS: Dict[str, Dict[str, Any]] = {}


def execute_tool(tool_name: str, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
    tool = TOOL_REGISTRY.get(tool_name)

    if tool is None:
        return {
            "tool": tool_name,
            "executed": False,
            "error": "Tool not found.",
        }

    return tool(task, context)


def submit_workflow(user_id: str, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
    workflow_id = str(uuid.uuid4())
    route = route_workflow(task)

    write_audit_event(
        {
            "workflow_id": workflow_id,
            "event": "workflow_submitted",
            "user_id": user_id,
            "task": task,
        }
    )

    write_audit_event(
        {
            "workflow_id": workflow_id,
            "event": "agent_route_created",
            "decision": route.decision.value,
            "tool_name": route.tool_name,
            "reason": route.reason,
            "risk_flags": route.risk_flags,
        }
    )

    if route.decision == WorkflowDecision.blocked_unsafe:
        write_audit_event(
            {
                "workflow_id": workflow_id,
                "event": "workflow_blocked",
                "reason": route.reason,
            }
        )

        return {
            "workflow_id": workflow_id,
            "status": WorkflowStatus.blocked,
            "route": route,
            "result": None,
            "audit_log": get_workflow_events(workflow_id),
        }

    if route.decision == WorkflowDecision.requires_approval:
        PENDING_WORKFLOWS[workflow_id] = {
            "user_id": user_id,
            "task": task,
            "context": context,
            "route": route,
        }

        write_audit_event(
            {
                "workflow_id": workflow_id,
                "event": "workflow_pending_approval",
                "reason": route.reason,
            }
        )

        return {
            "workflow_id": workflow_id,
            "status": WorkflowStatus.pending_approval,
            "route": route,
            "result": None,
            "audit_log": get_workflow_events(workflow_id),
        }

    result = execute_tool(route.tool_name or "general_workflow_action", task, context)

    write_audit_event(
        {
            "workflow_id": workflow_id,
            "event": "tool_executed",
            "tool_name": route.tool_name,
            "result": result,
        }
    )

    return {
        "workflow_id": workflow_id,
        "status": WorkflowStatus.completed,
        "route": route,
        "result": result,
        "audit_log": get_workflow_events(workflow_id),
    }


def approve_workflow(
    workflow_id: str,
    approved_by: str,
    approved: bool,
    note: str | None = None,
) -> Dict[str, Any]:
    pending = PENDING_WORKFLOWS.get(workflow_id)

    if pending is None:
        return {
            "workflow_id": workflow_id,
            "status": WorkflowStatus.rejected,
            "result": {
                "executed": False,
                "error": "Workflow not found or no longer pending approval.",
            },
            "audit_log": get_workflow_events(workflow_id),
        }

    write_audit_event(
        {
            "workflow_id": workflow_id,
            "event": "approval_decision_recorded",
            "approved_by": approved_by,
            "approved": approved,
            "note": note,
        }
    )

    if not approved:
        PENDING_WORKFLOWS.pop(workflow_id, None)

        write_audit_event(
            {
                "workflow_id": workflow_id,
                "event": "workflow_rejected",
            }
        )

        return {
            "workflow_id": workflow_id,
            "status": WorkflowStatus.rejected,
            "result": None,
            "audit_log": get_workflow_events(workflow_id),
        }

    route = pending["route"]
    result = execute_tool(
        route.tool_name or "general_workflow_action",
        pending["task"],
        pending["context"],
    )

    PENDING_WORKFLOWS.pop(workflow_id, None)

    write_audit_event(
        {
            "workflow_id": workflow_id,
            "event": "approved_tool_executed",
            "tool_name": route.tool_name,
            "result": result,
        }
    )

    return {
        "workflow_id": workflow_id,
        "status": WorkflowStatus.approved,
        "result": result,
        "audit_log": get_workflow_events(workflow_id),
    }