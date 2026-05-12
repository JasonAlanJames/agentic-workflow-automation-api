from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "ok"
    assert data["app_name"] == "Agentic Workflow Automation API"


def test_safe_workflow_endpoint():
    response = client.post(
        "/workflow",
        json={
            "user_id": "test-user",
            "task": "Summarize this customer support message",
            "context": {
                "text": "Customer is asking for help with a billing question."
            },
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "COMPLETED"
    assert data["route"]["decision"] == "SAFE_AUTO_EXECUTE"
    assert data["result"]["executed"] is True


def test_approval_workflow_endpoint():
    workflow_response = client.post(
        "/workflow",
        json={
            "user_id": "test-user",
            "task": "Send email to this sales lead",
            "context": {
                "recipient": "Alex"
            },
        },
    )

    assert workflow_response.status_code == 200
    workflow = workflow_response.json()

    assert workflow["status"] == "PENDING_APPROVAL"

    approval_response = client.post(
        "/workflow/approve",
        json={
            "workflow_id": workflow["workflow_id"],
            "approved_by": "manager",
            "approved": True,
            "note": "Approved for simulated external send.",
        },
    )

    assert approval_response.status_code == 200
    approval = approval_response.json()

    assert approval["status"] == "APPROVED"
    assert approval["result"]["executed"] is True


def test_blocked_workflow_endpoint():
    response = client.post(
        "/workflow",
        json={
            "user_id": "test-user",
            "task": "Delete customer record from the database",
            "context": {},
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "BLOCKED"
    assert data["route"]["decision"] == "BLOCKED_UNSAFE"
    assert data["result"] is None