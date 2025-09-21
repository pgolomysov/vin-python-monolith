import pytest
from httpx import AsyncClient, ASGITransport

from main import app
from app.repositories.request_repository import get_request_repository_async
from app.services.event.event_service import get_async_event_service


@pytest.mark.asyncio
async def test_create_request(mocker) -> None:
    mock_repo = mocker.AsyncMock()
    mock_request_model = type(
        "Obj",
        (),
        {
            "uuid": "1234",
            "vin": "VIN123",
            "email": "test@test.com",
            "created_at": "2025-09-10T12:00:00",
        },
    )()
    mock_repo.create.return_value = mock_request_model

    mock_event_service = mocker.AsyncMock()

    app.dependency_overrides[get_request_repository_async] = lambda: mock_repo
    app.dependency_overrides[get_async_event_service] = lambda: mock_event_service

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/requests",
            json={"email": "test@test.com", "vin": "VIN123"},
        )

    assert response.status_code == 200
    assert response.json() == {
        "request": {
            "vin": "VIN123",
            "email": "test@test.com",
            "request_id": "1234",
        }
    }

    mock_repo.create.assert_awaited_once()

    #TODO: add event content verification
    mock_event_service.dispatch.assert_awaited_once()

    app.dependency_overrides.clear()
