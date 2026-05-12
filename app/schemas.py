from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class WorkflowDecision(str, Enum):
    safe_auto_execute = "SAFE_AUTO_EXECUTE"
    requires_approval = "REQUIRES_APPROVAL"
    blocked_unsafe = "BLOCKED_UNSAFE"


class WorkflowStatus(str, Enum):
    completed = "COMPLETED"
    pending_approval = "PENDING_APPROVAL"
    blocked = "BLOCKED"
    approved = "APPROVED"
    rejected = "REJECTED"


class HealthResponse(BaseModel):
    status: str
    app_name: str
    version: str


class WorkflowRequest(BaseModel):
    user_id: str = Field(..., min_length=2)
    task: str = Field(..., min_length=5)
    context: Optional[Dict[str, Any]] = Field(default_factory=dict)


class AgentRoute(BaseModel):
    decision: WorkflowDecision
    tool_name: Optional[str]
    reason: str
    risk_flags: List[str] = Field(default_factory=list)


class WorkflowResponse(BaseModel):
    workflow_id: str
    status: WorkflowStatus
    route: AgentRoute
    result: Optional[Dict[str, Any]] = None
    audit_log: List[Dict[str, Any]]


class ApprovalRequest(BaseModel):
    workflow_id: str
    approved_by: str
    approved: bool
    note: Optional[str] = None


class ApprovalResponse(BaseModel):
    workflow_id: str
    status: WorkflowStatus
    result: Optional[Dict[str, Any]] = None
    audit_log: List[Dict[str, Any]]