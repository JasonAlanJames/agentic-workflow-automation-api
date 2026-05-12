from app.schemas import WorkflowDecision


BLOCKED_KEYWORDS = [
    "delete customer",
    "delete user",
    "erase database",
    "drop table",
    "steal",
    "bypass",
    "disable security",
    "leak",
    "exfiltrate",
]

APPROVAL_KEYWORDS = [
    "send email",
    "send message",
    "refund",
    "charge",
    "purchase",
    "cancel subscription",
    "update billing",
    "external message",
    "post publicly",
]

SAFE_KEYWORDS = [
    "summarize",
    "classify",
    "draft",
    "extract",
    "analyze",
    "tag",
    "prioritize",
    "create internal note",
]


def evaluate_task_risk(task: str) -> tuple[WorkflowDecision, list[str], str]:
    normalized = task.lower()
    risk_flags: list[str] = []

    for keyword in BLOCKED_KEYWORDS:
        if keyword in normalized:
            risk_flags.append(f"blocked_keyword:{keyword}")
            return (
                WorkflowDecision.blocked_unsafe,
                risk_flags,
                "The requested task contains unsafe or destructive intent and cannot be executed.",
            )

    for keyword in APPROVAL_KEYWORDS:
        if keyword in normalized:
            risk_flags.append(f"approval_keyword:{keyword}")
            return (
                WorkflowDecision.requires_approval,
                risk_flags,
                "The task may affect an external system, customer, payment, or public channel and requires human approval.",
            )

    for keyword in SAFE_KEYWORDS:
        if keyword in normalized:
            return (
                WorkflowDecision.safe_auto_execute,
                risk_flags,
                "The task is informational or internal and can be executed automatically.",
            )

    return (
        WorkflowDecision.requires_approval,
        ["unknown_intent"],
        "The task intent is not confidently classified, so human approval is required.",
    )