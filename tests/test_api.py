import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.providers.factory import create_provider


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
async def client() -> AsyncClient:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as test_client:
        yield test_client


@pytest.mark.anyio
async def test_health_reports_stub_provider(client: AsyncClient) -> None:
    response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "provider": "stub"}


@pytest.mark.anyio
async def test_ask_returns_structured_stub_response(client: AsyncClient) -> None:
    response = await client.post(
        "/ask", json={"question": "Where is the registrar's office?"}
    )

    assert response.status_code == 200
    assert response.json() == {
        "answer": "Stub response for: Where is the registrar's office?",
        "sources": [],
        "confidence": "stub",
        "escalation_flag": False,
    }


@pytest.mark.anyio
async def test_ask_rejects_blank_question(client: AsyncClient) -> None:
    response = await client.post("/ask", json={"question": "   "})

    assert response.status_code == 422


@pytest.mark.anyio
async def test_ask_rejects_missing_question(client: AsyncClient) -> None:
    response = await client.post("/ask", json={})

    assert response.status_code == 422


def test_provider_factory_rejects_unsupported_provider() -> None:
    with pytest.raises(ValueError, match="Unsupported MODEL_PROVIDER"):
        create_provider("unconfigured-model")
