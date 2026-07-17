# TM1 Foundation and Architecture Narrative

## What We Built

TM1 is deliberately not a complete campus assistant. It is the smallest service that can prove a useful application contract and give the team a stable base for later work. A client submits a question to `POST /ask`; the FastAPI application validates it, passes it to an answer-provider interface, and returns an answer, source list, confidence label, and escalation flag. The implemented provider is deterministic. It requires no credentials and returns a clearly labeled stub response, which makes the repository reproducible and keeps the team from confusing model behavior with infrastructure behavior.

The repository includes a VS Code devcontainer, install and run commands, automated tests, a health endpoint, an AWS SAM template, and documentation for both the architecture and code provenance. A new teammate can clone the project, reopen it in the container, run `make run`, and call the API. Tests cover the successful contract and rejection of blank or missing questions. The application logs a generated request identifier, provider, question length, and latency, but it does not log the question itself. That is a small but intentional privacy boundary.

## Cloud Services and Data Flow

The proposed cloud path uses Amazon API Gateway and AWS Lambda. API Gateway provides the HTTPS boundary and maps `POST /ask` and `GET /health` to one Lambda function. Lambda runs the same FastAPI application used locally through the Mangum adapter. This keeps the request model and tests independent of whether the service runs on a laptop, in a devcontainer, or in AWS. It also avoids paying for an idle server during a low-volume class prototype.

AWS CloudWatch is the operational evidence layer. Lambda's basic execution role sends application logs there, and the SAM template enables tracing so the team can inspect latency and failures if the Learner Lab permits it. IAM is limited to the basic execution role because the TM1 function does not need to read documents or call a model. This is easier to explain and safer than attaching broad permissions in anticipation of features that do not exist.

The model adapter separates the application from provider-specific code. `MODEL_PROVIDER=stub` is the only implemented configuration. Amazon Bedrock or an external API can be added later as another provider, but that is a future path rather than a hidden dependency. S3 is likewise reserved for approved source documents if retrieval becomes necessary. Secrets Manager or Parameter Store would hold an external credential; no credential belongs in the repository.

## Why This Foundation Is Defensible

The architecture makes three current claims, all of which can be tested: the API runs, invalid input is rejected, and the response shape remains stable behind a provider boundary. It does not claim that the system answers university questions accurately, that retrieval exists, or that the AWS path has already passed Learner Lab restrictions. Those are separate risks and should be validated separately.

Before a real deployment, the service needs authorization, throttling, a defined source-governance process, retention rules, model evaluation, cost controls, and a meaningful escalation policy. Those controls are not useful as decorative boxes in TM1. They become necessary when the service begins handling real users, real institutional content, or a nondeterministic model.

The SAM template is therefore a deployment candidate. The remaining infrastructure task is empirical: start Learner Lab, validate and deploy the template, call both endpoints, and confirm the expected CloudWatch evidence. If the sandbox blocks API Gateway or Lambda, the fallback is one EC2 instance running the same FastAPI service. The hosting choice can change without reopening the application contract, which is the main value of this foundation.
