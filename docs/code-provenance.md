# Code Provenance and Review Log

## Team

- Noah Hicks
- Taha Zakir

## Use of AI

OpenAI Codex was used in Operator/Agent mode to scaffold the bounded TM1 service and in Critic mode to challenge its correctness, security, explainability, and run instructions. Noah Hicks and Taha Zakir remain responsible for understanding and approving every retained file.

| Date | Mode | Work and files | Origin | Human decision or review |
|---|---|---|---|---|
| 2026-07-16 | Human direction | Select a fresh project and a minimal university-services Q&A API | Noah Hicks | Approved project scope and authorized implementation for review. |
| 2026-07-16 | Operator/Agent | Devcontainer, Python package, FastAPI routes, provider interface, tests, SAM template, diagram source, and documentation | OpenAI Codex generated the initial implementation from the assignment brief and course constraints. | Noah Hicks and Taha Zakir reviewed and approved all retained code on 2026-07-17. |
| 2026-07-16 | Critic | Validation, logging, unsupported-provider behavior, infrastructure claims, security boundary, run instructions, and test coverage | OpenAI Codex reviewed the generated repository and recorded findings in `docs/critic-review.md`. | Both teammates reviewed the resolved findings and approved the final local implementation on 2026-07-17; live AWS claims remain intentionally unverified. |
| 2026-07-16 | Verification | Lint, five automated tests, live local endpoint smoke test, diagram render, SAM validation, and SAM build | OpenAI Codex ran the checks and captured their scope in `docs/verification.md`. | Local evidence passed and was reviewed by both teammates. Learner Lab deployment remains unverified. |
| 2026-07-17 | Human review | Code, tests, API behavior, diagram, SAM resources, documentation, and retained agent-generated files | Noah Hicks and Taha Zakir | Both reviewers completed the checklist and approved all retained code with no changes requested. |

## Prompt Summaries

### Operator/Agent

Create the smallest runnable FastAPI service for TM1. It must accept a question at `POST /ask`, return the required structured stub response, include a devcontainer and automated tests, keep provider access behind an interface, and provide a conservative API Gateway/Lambda SAM template. Do not require credentials or claim unperformed AWS validation.

### Critic

Review the repository as a skeptical teammate. Check whether a new contributor can run it, whether invalid input fails clearly, whether generated code is explainable, whether logs expose question content, whether the provider boundary actually works, whether the AWS template matches the code layout, and whether documentation distinguishes implemented, planned, and live-validated behavior.

## Human Review Gate

From the project root, run `.\scripts\review_check.ps1` in PowerShell or `make review` in the devcontainer. Use `.\scripts\review_check.ps1 -IncludeSam` when the AWS SAM CLI is available. These commands provide repeatable evidence but do not replace human understanding. Before submission, each teammate should complete these items and record the result below.

- [x] Explain `AskRequest`, `AskResponse`, and the blank-input behavior.
- [x] Explain why the stub provider is behind `AnswerProvider`.
- [x] Run `python -m pytest` and `python -m ruff check .`.
- [x] Start the API and call `/health` and `/ask`.
- [x] Review the SAM resources and compare them with the diagram.
- [x] Verify live Learner Lab results or label the AWS deployment as unverified.

**Noah Hicks review:** Passed - all retained code reviewed and approved

**Noah Hicks review date:** 2026-07-17

**Taha Zakir review:** Passed - all retained code reviewed and approved

**Taha Zakir review date:** 2026-07-17

**Changes requested:** None after final review
