# Learner Lab Deployment Check

The local API and tests do not require AWS credentials. Use this sequence only after starting an AWS Academy Learner Lab session and obtaining its temporary credentials.

## Validate and Build

```bash
sam validate --lint --template-file infra/template.yaml
sam build --template-file infra/template.yaml
```

## Deploy

```bash
sam deploy --guided
```

Suggested first-run answers:

- Stack name: `tm1-cmu-services-api`
- Region: the Learner Lab region shown in the console, commonly `us-east-1`
- Confirm changes before deploy: `Y`
- Allow SAM CLI IAM role creation: `Y`
- Save arguments to configuration file: `Y`

## Evidence to Capture

- `ApiBaseUrl` stack output.
- Successful `GET /health` response.
- Successful `POST /ask` response with the documented JSON shape.
- CloudWatch log stream showing the request identifier, provider, character count, and latency without question content.
- Any Learner Lab permission error, including the blocked service and action.

## Guardrails

- Keep `MODEL_PROVIDER=stub`; no model credential is needed for TM1.
- Do not add broad managed policies to get around a Learner Lab restriction.
- Delete the stack after evidence is captured if the class does not require it to remain available.
- If API Gateway or Lambda is blocked, document that fact and run the same service on one Academy EC2 instance as the fallback.
