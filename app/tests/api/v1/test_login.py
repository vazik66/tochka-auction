from fastapi.testclient import TestClient
from app.tests.utils.utils import wrap_to_jsonrpc
from app.core.config import settings


def test_get_access_token(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(
        f"/api/v1/jsonrpc", data=wrap_to_jsonrpc(login_data, "login_access_token")
    )
    tokens = r.json()
    assert "access_token" in tokens["result"]
    assert tokens["result"]["access_token"]
