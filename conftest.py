import uuid
import pytest

from api.client import APIClient


@pytest.fixture(scope="session")
def project_name():
    return "ToolShop QA"


@pytest.fixture(scope="session")
def api_client():
    """创建 API 客户端，整个测试会话复用"""
    client = APIClient()
    yield client
    client.close()


@pytest.fixture
def create_registered_user(api_client):
    """创建一个随机测试用户"""

    def _create():
        email = f"toolshop.test.{uuid.uuid4().hex[:10]}@example.com"
        password = f"Qa@{uuid.uuid4().hex}9Z"

        payload = {
            "first_name": "Test",
            "last_name": "Automation",
            "email": email,
            "password": password
        }

        response = api_client.request(
            "POST",
            "/users/register",
            json=payload
        )

        assert response.status_code == 201

        return {
            "email": email,
            "password": password,
            "id": response.json()["id"]
        }

    return _create