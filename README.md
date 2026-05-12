# Agentic Workflow Automation API

A production-style FastAPI agentic workflow automation API with task routing, tool execution, approval gates, audit logging, Docker, pytest, and GitHub Actions CI.

## Features

- Agentic task routing
- Safe auto-execution for low-risk tasks
- Human approval gates for external or sensitive actions
- Unsafe task blocking
- Simulated business tool execution
- Workflow audit logging
- FastAPI Swagger documentation
- pytest coverage
- Docker support
- GitHub Actions CI

## Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/workflow` | Submit an agentic workflow |
| POST | `/workflow/approve` | Approve or reject a pending workflow |

## Run Locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload