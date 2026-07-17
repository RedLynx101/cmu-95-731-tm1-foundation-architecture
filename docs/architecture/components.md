# Architecture Components

- **Client:** Sends a university-services question over HTTPS and receives the stable response schema.
- **Amazon API Gateway:** Exposes `POST /ask` and `GET /health` and routes both requests to one Lambda function.
- **AWS Lambda:** Runs the FastAPI application through Mangum without maintaining an idle server.
- **Model adapter:** Keeps model-specific behavior behind one interface so the API contract does not depend on a provider.
- **Stub provider:** Returns deterministic responses for TM1 testing and demonstrations without credentials or variable model behavior.
- **Amazon CloudWatch:** Receives Lambda logs and metrics for request success, errors, and latency.
- **AWS IAM:** Grants the function only the permissions needed for execution and logging.
- **Amazon S3 (future):** Stores approved source material if later milestones add retrieval.
- **Bedrock or external model (future):** Replaces the stub only after model, privacy, cost, and escalation requirements are defined.
- **Secrets Manager or Parameter Store (future):** Stores external-provider credentials instead of placing them in code or environment files.

Solid connectors show the implemented application path or the proposed TM1 deployment path. Dashed connectors and amber boxes identify later integrations that are deliberately outside the current prototype.
