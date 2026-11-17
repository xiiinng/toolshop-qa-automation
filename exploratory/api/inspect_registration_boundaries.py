import uuid


def test_inspect_password_min_length_valid(api_client):
    """探索 password 缺少特殊符号时的接口行为"""

    payload = {
        "first_name": "Test",
        "last_name": "Automation",
        "email": f"boundary.{uuid.uuid4().hex[:10]}@example.com",
        "password": f"Aa1@{uuid.uuid4().hex[:4]}"
    }

    response = api_client.request(
        "POST",
        "/users/register",
        json=payload
    )

    print("password 长度：", len(payload["password"]))
    print("实际状态码：", response.status_code)
    print("实际响应内容：", response.text)