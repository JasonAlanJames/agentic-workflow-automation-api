from fastapi import FastAPI

from app.agent.executor import approve_workflow, submit_workflow
from app.config import get_settings
from app.schemas import (
    ApprovalRequest,
    ApprovalResponse,
    HealthResponse,
    WorkflowRequest,
    WorkflowResponse,
)


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "A production-style agentic workflow automation API with task routing, "
        "tool execution, approval gates, audit logging, Docker, pytest, and "
        "GitHub Actions CI."
    ),
)


@app.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(
        status="ok",
        app_name=settings.app_name,
        version=settings.app_version,
    )


@app.post("/workflow", response_model=WorkflowResponse)
def create_workflow(request: WorkflowRequest):
    return submit_workflow(
        user_id=request.user_id,
        task=request.task,
        context=request.context or {},
    )


@app.post("/workflow/approve", response_model=ApprovalResponse)
def approve(request: ApprovalRequest):
    return approve_workflow(
        workflow_id=request.workflow_id,
        approved_by=request.approved_by,
        approved=request.approved,
        note=request.note,
    )