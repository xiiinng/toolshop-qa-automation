"""
已知缺陷复现测试

BUG-001：
用户注册接口未正确校验邮箱格式。

测试依据：
Swagger 将 UserRequest.email 定义为 format: email，
但未明确规定邮箱格式校验失败时的具体状态码。

测试策略：
非法邮箱应被服务端拒绝，预期返回 4xx 客户端错误。
如果返回 2xx，说明非法邮箱被成功接受。
如果返回 5xx，则视为服务端异常，不算校验成功。
"""

import uuid

def test_register_user_invalid_email(api_client):
    """验证注册时使用非法邮箱格式"""

    payload = {
        "first_name": "Test",
        "last_name": "Automation",
        "email": f"invalid-{uuid.uuid4().hex[:10]}",
        "password": f"Qa@{uuid.uuid4().hex}9Z"
    }

    response = api_client.request(
        "POST",
        "/users/register",
        json=payload
    )

    print("实际状态码：", response.status_code)
    print("实际响应内容：", response.text)

    assert 400 <= response.status_code < 500, (
        f"非法邮箱应被服务端拒绝，"
        f"实际状态码：{response.status_code}，"
        f"响应内容：{response.text}"
    )


def test_register_user_invalid_email_without_at(api_client):
    """验证不包含 @ 的邮箱是否被拒绝"""

    payload = {
        "first_name": "Test",
        "last_name": "Automation",
        "email": f"invalid{uuid.uuid4().hex[:8]}.com",
        "password": f"Qa@{uuid.uuid4().hex}9Z"
    }

    response = api_client.request(
        "POST",
        "/users/register",
        json=payload
    )

    print("实际状态码：", response.status_code)
    print("实际响应内容：", response.text)

    assert 400 <= response.status_code < 500, (
        f"非法邮箱应被服务端拒绝，"
        f"实际状态码：{response.status_code}，"
        f"响应内容：{response.text}"
    )