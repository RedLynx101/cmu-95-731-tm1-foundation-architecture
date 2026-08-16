# Verification Record

Verified locally and reviewed by the team on July 17, 2026.

Team: Noah Hicks and Taha Zakir.

| Check | Result | Evidence |
|---|---|---|
| Python environment | Pass | Python 3.12.13 in the project virtual environment. |
| Static checks | Pass | Ruff reported `All checks passed!`. |
| Automated tests | Pass | Five tests passed: health, valid question, blank question, missing question, and unsupported provider. |
| Live API smoke test | Pass | A local Uvicorn process returned the documented JSON from `/health` and `/ask`, then shut down cleanly. |
| Repeatable review harness | Pass | `scripts/review_check.ps1` runs Ruff, pytest, the live smoke test, and the diagram rebuild, with optional SAM validation and build. |
| Architecture diagram | Pass | PNG rendered at 1800 x 1160 and was visually inspected; an ambiguous credential connector was corrected and re-rendered. |
| SAM template validation | Pass | AWS SAM CLI 1.137.1 reported `infra/template.yaml is a valid SAM Template`. |
| SAM build | Pass | AWS SAM packaged the Python 3.12 Lambda source and dependencies under `.aws-sam/build`. |
| Human review | Pass | Noah Hicks and Taha Zakir reviewed, tested, and approved all retained code on July 17, 2026. |
| GitHub repository | Pass | Approved source was committed to `main` and published at `https://github.com/RedLynx101/cmu-95-731-tm1-foundation-architecture`. Public visibility was reconfirmed on August 16, 2026. |

## Not Yet Verified

- Opening and rebuilding inside the VS Code devcontainer.
- Deployment through the temporary AWS Academy Learner Lab session.
- Public API Gateway URL and CloudWatch evidence from the live sandbox.
- Canvas submission.

These are deliberately excluded from the pass claims above. The local application and deployment package are ready for those checks.

## Public-presentation reconciliation — August 16, 2026

- Repository visibility: public.
- Reuse license: none surfaced; public visibility is not represented as open-source licensing.
- Scope boundary retained: the deterministic stub and local contract are implemented; API Gateway, Lambda, CloudWatch, IAM, S3, Bedrock or another external model, and secrets storage remain candidate or future components exactly as labeled in the architecture.
- No claim of a live AWS deployment was added.
