# Agentic Workflow Automation API

A production-style **FastAPI agentic workflow automation API** that demonstrates task routing, simulated tool execution, approval-gated workflows, unsafe action blocking, audit logging, Docker containerization, automated testing, and GitHub Actions CI.

This project is designed as a portfolio-ready backend AI engineering project that shows how agentic systems can safely classify business requests, determine whether approval is required, execute approved actions, and preserve workflow traceability through structured audit logs.

---

## Project Purpose

The purpose of this project is to demonstrate how agentic workflow systems can be built with production-oriented software engineering practices.

The API shows how an AI automation system can:

- Route business requests through a workflow engine
- Determine whether an action is safe to auto-execute
- Require human approval for sensitive or external-facing actions
- Block unsafe or unauthorized requests
- Simulate business tool execution
- Track decisions through audit logs
- Validate workflow behavior with automated tests
- Run locally or inside Docker
- Use GitHub Actions CI for repeatable validation

---

## Features

- Agentic task routing
- Safe auto-execution for low-risk tasks
- Human approval gates for external or sensitive actions
- Unsafe task blocking
- Simulated business tool execution
- Workflow audit logging
- FastAPI Swagger documentation
- Pydantic request and response validation
- pytest test coverage
- Docker support
- GitHub Actions CI
- Portfolio-ready screenshots and documentation

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| FastAPI | API framework |
| Pydantic | Request and response validation |
| Uvicorn | ASGI application server |
| pytest | Automated testing |
| Docker | Containerized deployment |
| GitHub Actions | Continuous integration |
| Swagger / OpenAPI | Interactive API documentation |

---

## Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Confirms the API is running |
| POST | `/workflow` | Submits an agentic workflow request |
| POST | `/workflow/approve` | Approves or rejects a pending workflow |

---

## Workflow Behavior

The API classifies workflow requests into three primary categories:

| Workflow Type | Behavior |
|---|---|
| Safe workflow | Executes automatically |
| Approval-required workflow | Creates a pending workflow that requires human approval |
| Unsafe workflow | Blocks execution and returns a safety-focused response |

This design demonstrates a core pattern in production agentic AI systems: allowing useful automation while preserving human oversight for actions that could create financial, customer-facing, operational, or compliance risk.

---

## Project Structure

```text
agentic-workflow-automation-api/
├── .github/
│   └── workflows/
│       └── ci.yml
├── app/
│   ├── tools/
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   └── schemas.py
├── docs/
│   └── screenshots/
│       ├── agent-decision.png
│       ├── approval-executed-workflow.png
│       ├── approval-required-workflow.png
│       ├── batch-evaluation.png
│       ├── docker-running.png
│       ├── github-actions-ci.png
│       ├── health-endpoint.png
│       ├── pytest-passing.png
│       └── swagger-docs.png
├── reports/
├── tests/
│   ├── test_api.py
│   ├── test_executor.py
│   └── test_policy.py
├── .env.example
├── .gitignore
├── Dockerfile
├── pytest.ini
├── README.md
└── requirements.txt
```

---

## Getting Started

### 1. Clone the repository

```powershell
git clone https://github.com/JasonAlanJames/agentic-workflow-automation-api.git
cd agentic-workflow-automation-api
```

### 2. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Run the API locally

```powershell
uvicorn app.main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

Swagger documentation will be available at:

```text
http://127.0.0.1:8000/docs
```

---

## Run with Docker

### 1. Build the Docker image

```powershell
docker build -t agentic-workflow-automation-api .
```

### 2. Run the container

```powershell
docker run -p 8002:8000 agentic-workflow-automation-api
```

The API will be available at:

```text
http://127.0.0.1:8002
```

Swagger documentation will be available at:

```text
http://127.0.0.1:8002/docs
```

> Note: Port `8002` is used here to avoid conflicts with other local FastAPI portfolio projects that may already be using ports `8000` or `8001`.

---

## Run Tests

Run the automated test suite with:

```powershell
pytest
```

The tests validate API behavior, workflow execution logic, approval policies, and expected safety controls.

---

## GitHub Actions CI

This repository includes a GitHub Actions workflow that runs automated tests when changes are pushed to the `main` branch or submitted through a pull request.

The CI workflow validates that the project installs correctly and that all pytest checks pass in a clean environment.

---

## Screenshots

### Swagger API Documentation

The FastAPI Swagger interface provides interactive documentation for testing the workflow automation endpoints directly in the browser.

![Swagger API Documentation](docs/screenshots/swagger-docs.png)

---

### Health Check Endpoint

The `/health` endpoint confirms that the API is running and ready to receive workflow requests.

![Health Check Endpoint](docs/screenshots/health-endpoint.png)

---

### Agent Decision Workflow

The `/workflow` endpoint evaluates incoming requests and determines whether the workflow should execute automatically, require approval, or be blocked.

![Agent Decision Workflow](docs/screenshots/agent-decision.png)

---

### Approval Required Workflow

Sensitive or external-facing actions are routed into a pending approval state instead of being executed immediately.

![Approval Required Workflow](docs/screenshots/approval-required-workflow.png)

---

### Approval Executed Workflow

After approval is granted through the `/workflow/approve` endpoint, the workflow can proceed through simulated execution.

![Approval Executed Workflow](docs/screenshots/approval-executed-workflow.png)

---

### Batch Evaluation

The workflow logic can be tested across multiple request types to validate routing, approval, and blocking behavior.

![Batch Evaluation](docs/screenshots/batch-evaluation.png)

---

### Dockerized Application Running

The application can be containerized and run through Docker for repeatable local deployment.

![Dockerized Application Running](docs/screenshots/docker-running.png)

---

### pytest Passing

The automated test suite verifies the API routes, policy logic, and simulated executor behavior.

![pytest Passing](docs/screenshots/pytest-passing.png)

---

### GitHub Actions CI Passing

GitHub Actions confirms that the project builds and tests successfully in a clean CI environment.

![GitHub Actions CI Passing](docs/screenshots/github-actions-ci.png)

---

## Example Workflow Request

```json
{
  "task": "Send a customer follow-up email",
  "risk_level": "low",
  "requires_external_action": false
}
```

Example behavior:

```text
The workflow is classified as safe and can be automatically executed.
```

---

## Example Approval-Gated Request

```json
{
  "task": "Issue a customer refund and send confirmation email",
  "risk_level": "high",
  "requires_external_action": true
}
```

Example behavior:

```text
The workflow is placed into a pending approval state before execution.
```

---

## Production Engineering Concepts Demonstrated

This project demonstrates several production-oriented AI engineering concepts:

- Agentic workflow orchestration
- Human-in-the-loop approval gates
- Tool execution abstraction
- Safety-aware workflow classification
- Audit logging for workflow traceability
- API validation using Pydantic schemas
- Automated testing with pytest
- Dockerized API deployment
- CI validation with GitHub Actions
- Professional technical documentation

---

## Portfolio Relevance

This project is designed to demonstrate backend AI engineering and agentic automation skills relevant to roles involving:

- AI Engineer
- Agentic AI Engineer
- Backend Software Engineer
- LLM Application Engineer
- AI Automation Engineer
- Full Stack AI Engineer
- Platform Engineer
- Applied AI Developer

It shows the ability to design agentic systems with safety controls, approval workflows, test coverage, and production-style API structure.

---

## Author

**Jason A. James, B.S. Computer Information Technology**  
AI Engineer | Software Engineer | Agentic AI Developer  

Website: https://jasonajames.com  
LinkedIn: https://www.linkedin.com/in/jasonalanjames  
GitHub: https://github.com/JasonAlanJames  

---

## License

This project is intended for portfolio, educational, and demonstration purposes.
