# CMU Services API

This repository is the TM1 foundation for a university-services question-answering system. It proves one narrow contract: accept a question, route it through a provider interface, and return a structured response. TM1 uses a deterministic stub so every teammate can run and explain the service without credentials.

## Team

- Noah Hicks
- Taha Zakir

## Implemented Now

- FastAPI application with `POST /ask` and `GET /health`.
- Input validation and a stable response schema.
- Deterministic stub provider behind a replaceable provider interface.
- Tests for the valid, blank, and missing-question paths.
- VS Code devcontainer and one-command local startup.
- AWS SAM template for an API Gateway and Lambda deployment candidate.
- Architecture diagram, narrative, Critic review, and code-provenance log.

Amazon S3, Bedrock or an external model, and a secrets service are shown as future integrations. They are not represented as implemented TM1 features.

## Run Locally

### Devcontainer

1. Clone the repository.
2. Open it in VS Code and select **Reopen in Container**.
3. Start the API:

```bash
make run
```

The container installs the project and development dependencies automatically. API documentation is available at `http://localhost:8000/docs`.

### Existing Python 3.11+

```bash
python -m venv .venv
# PowerShell: .\.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -e ".[dev]"
python -m uvicorn app.main:app --app-dir src --reload
```

## Exercise the Contract

PowerShell:

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri http://localhost:8000/ask `
  -ContentType 'application/json' `
  -Body '{"question":"Where is the registrar''s office?"}'
```

Expected JSON:

```json
{
  "answer": "Stub response for: Where is the registrar's office?",
  "sources": [],
  "confidence": "stub",
  "escalation_flag": false
}
```

## Verify the Repository

For the complete local human-review run on Windows:

```powershell
.\scripts\review_check.ps1
```

Add `-IncludeSam` to validate and rebuild the AWS deployment candidate as part of the same run. The script changes no provenance approvals; after reviewing the output and code, record the result in [`docs/code-provenance.md`](docs/code-provenance.md).

Inside the devcontainer or another environment with `make`:

```bash
make review
```

The narrower automated check remains available as:

```bash
make check
```

Equivalent commands on a machine without `make`:

```bash
python -m ruff check .
python -m pytest
```

## Repository Map

```text
.devcontainer/             Reproducible Python development environment
src/app/                   API, request models, and provider boundary
tests/                     Contract and validation tests
infra/template.yaml        AWS SAM deployment candidate
docs/architecture/         Diagram, source, and component descriptions
docs/architecture-narrative.md
docs/code-provenance.md
docs/critic-review.md
scripts/                   Repeatable diagram and review helpers
```

## Architecture Decision

The cloud candidate uses Amazon API Gateway as the HTTPS boundary and AWS Lambda as the compute layer. Mangum adapts the same FastAPI application used locally, which keeps the contract and tests independent of the hosting choice. CloudWatch receives operational logs through the Lambda execution role. IAM remains least privilege: the current function needs only its basic logging permissions.

The provider interface is the deliberate extension point. `MODEL_PROVIDER=stub` is the only accepted TM1 setting. A later Bedrock or external-model provider can be added without changing `POST /ask`, but it should be enabled only after source handling, authorization, privacy, cost limits, and escalation behavior are defined.

## Learner Lab Validation

The SAM template is deployable source, not evidence of a completed Academy deployment. Before submission, the team should use Learner Lab to verify that API Gateway, Lambda, CloudWatch, IAM role creation, and AWS X-Ray tracing are permitted. The commands and evidence checklist are in [`infra/README.md`](infra/README.md). If the sandbox blocks this path, the same FastAPI service can run on one EC2 instance; the public contract does not change.

## Review Gate

Noah Hicks and Taha Zakir completed the review gate on July 17, 2026. Both teammates tested and approved all retained code and confirmed that they can explain the request model, provider boundary, Lambda adapter, tests, and SAM resources. The completed checklist is recorded in [`docs/code-provenance.md`](docs/code-provenance.md). The Learner Lab deployment remains unverified until live sandbox checks pass.
