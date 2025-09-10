import pytest
from httpx import AsyncClient
from main import app

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
    app.dependency_overrides[
        "app.repositories.request_repository.get_request_repository_async"
    ] = lambda: mock_repo
    app.dependency_overrides[
        "app.services.event.event_service.get_async_event_service"
    ] = lambda: mock_event_service

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/requests",
            json={"email": "test@test.com", "vin": "VIN123"}
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
    mock_event_service.dispatch.assert_awaited_once()
    app.dependency_overrides = {}
