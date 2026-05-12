from typing import Any, Dict


def summarize_text(task: str, context: Dict[str, Any]) -> Dict[str, Any]:
    source_text = context.get("text", task)

    summary = source_text[:220]
    if len(source_text) > 220:
        summary += "..."

    return {
        "tool": "summarize_text",
        "summary": summary,
        "executed": True,
    }


def classify_request(task: str, context: Dict[str, Any]) -> Dict[str, Any]:
    normalized = task.lower()

    if "urgent" in normalized or "refund" in normalized or "billing" in normalized:
        category = "high_priority"
    elif "sales" in normalized or "lead" in normalized:
        category = "sales"
    elif "support" in normalized or "issue" in normalized:
        category = "support"
    else:
        category = "general"

    return {
        "tool": "classify_request",
        "category": category,
        "executed": True,
    }


def draft_response(task: str, context: Dict[str, Any]) -> Dict[str, Any]:
    recipient = context.get("recipient", "customer")

    return {
        "tool": "draft_response",
        "draft": (
            f"Hello {recipient}, thank you for reaching out. "
            "I reviewed your request and will follow up with the next appropriate steps."
        ),
        "executed": True,
    }


def send_external_message(task: str, context: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "tool": "send_external_message",
        "message": "External message simulated. No real message was sent.",
        "executed": True,
    }


def payment_action(task: str, context: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "tool": "payment_action",
        "message": "Payment action simulated. No real payment system was modified.",
        "executed": True,
    }


def general_workflow_action(task: str, context: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "tool": "general_workflow_action",
        "message": "General workflow action simulated.",
        "executed": True,
    }


TOOL_REGISTRY = {
    "summarize_text": summarize_text,
    "classify_request": classify_request,
    "draft_response": draft_response,
    "send_external_message": send_external_message,
    "payment_action": payment_action,
    "general_workflow_action": general_workflow_action,
}