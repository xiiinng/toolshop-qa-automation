
import uuid


def test_register_user(api_client):
    """验证用户正常注册"""

    # 使用随机邮箱，避免重复注册导致冲突
    email = f"toolshop.qa.{uuid.uuid4().hex[:10]}@example.com"

    payload = {
        "first_name": "Test",
        "last_name": "Automation",
        "email": email,
        "password": f"Qa@{uuid.uuid4().hex}9Z"
    }

    response = api_client.request(
        "POST",
        "/users/register",
        json=payload
    )

    print("实际状态码：", response.status_code)
    print("实际响应内容：", response.text)
    # 验证注册成功状态码
    assert response.status_code == 201

    result = response.json()

    # 验证用户基本信息
    assert result["email"] == email
    assert result["first_name"] == payload["first_name"]
    assert result["last_name"] == payload["last_name"]

    # 验证用户 ID
    assert isinstance(result["id"], str)
    assert result["id"]

    print(f"注册成功，用户邮箱：{email}")
    print(f"用户 ID：{result['id']}")




def test_login_user(api_client, create_registered_user):
    """验证用户使用正确的邮箱和密码登录"""

    user = create_registered_user()

    response = api_client.request(
        "POST",
        "/users/login",
        json={
            "email": user["email"],
            "password": user["password"]
        }
    )

    assert response.status_code == 200

    result = response.json()

    assert result["access_token"]
    assert result["token_type"].lower() == "bearer"
    assert isinstance(result["expires_in"], int)



def test_get_current_user(api_client, create_registered_user):
    """验证登录后可以获取当前用户信息"""

    user = create_registered_user()

    login_response = api_client.request(
        "POST",
        "/users/login",
        json={
            "email": user["email"],
            "password": user["password"]
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = api_client.request(
        "GET",
        "/users/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    result = response.json()

    assert result["email"] == user["email"]
    assert result["first_name"] == "Test"
    assert result["last_name"] == "Automation"
    assert result["id"] == user["id"]


def test_get_current_user_without_token(api_client):
    """验证未携带 Token 访问当前用户接口"""

    response = api_client.get("/users/me")

    # 未认证请求应被拒绝
    assert response.status_code == 401

    result = response.json()

    assert "message" in result

    print("未认证访问已被拒绝")
    print("实际响应：", result)


def test_get_current_user_with_invalid_token(api_client):
    """验证使用无效 Token 访问当前用户接口"""

    response = api_client.get(
        "/users/me",
        headers={
            "Authorization": "Bearer invalid_test_token"
        }
    )

    # 无效 Token 应无法通过身份认证
    assert response.status_code == 401

    print("无效 Token 已被拒绝")
    print("实际响应：", response.text)


def test_register_user_missing_required_field(api_client):
    """验证注册时缺少必填字段"""

    payload = {
        "first_name": "Test",
        # 故意不传 last_name
        "email": f"toolshop.invalid.{uuid.uuid4().hex[:10]}@example.com",
        "password": f"Qa@{uuid.uuid4().hex}9Z"
    }

    response = api_client.request(
        "POST",
        "/users/register",
        json=payload
    )

    print("实际状态码：", response.status_code)
    print("实际响应内容：", response.text)

    # 缺少必填字段时，接口应返回客户端错误
    assert response.status_code == 422

    result = response.json()

    assert "last_name" in result
    assert "The last name field is required." in result["last_name"]



def test_register_user_duplicate_email(api_client):
    """验证使用已注册邮箱重复注册"""

    email = f"toolshop.duplicate.{uuid.uuid4().hex[:10]}@example.com"
    password = f"Qa@{uuid.uuid4().hex}9Z"

    payload = {
        "first_name": "Duplicate",
        "last_name": "Automation",
        "email": email,
        "password": password
    }

    # 第一次注册，应该成功
    first_response = api_client.request(
        "POST",
        "/users/register",
        json=payload
    )

    assert first_response.status_code == 201

    print("第一次注册状态码：", first_response.status_code)

    # 使用完全相同的信息再次注册
    second_response = api_client.request(
        "POST",
        "/users/register",
        json=payload
    )

    print("第二次注册状态码：", second_response.status_code)
    print("第二次注册响应：", second_response.text)

    # 重复注册应该被拒绝
    assert second_response.status_code == 409

    result = second_response.json()

    assert "email" in result
    assert "A customer with this email address already exists." in result["email"]


def test_login_user_wrong_password(api_client, create_registered_user):
    """验证使用错误密码登录会被拒绝"""

    user = create_registered_user()

    response = api_client.request(
        "POST",
        "/users/login",
        json={
            "email": user["email"],
            "password": "WrongPassword@123"
        }
    )

    assert response.status_code == 401

    result = response.json()

    assert result["error"] == "Unauthorized"
    assert "access_token" not in result



def test_login_user_nonexistent_email(api_client):
    """验证使用不存在的邮箱登录"""

    email = f"notexist.{uuid.uuid4().hex[:12]}@example.com"

    response = api_client.request(
        "POST",
        "/users/login",
        json={
            "email": email,
            "password": "Qa@NonExist123"
        }
    )

    print("实际状态码：", response.status_code)
    print("实际响应内容：", response.text)

    # 不存在的用户不应该登录成功
    assert response.status_code == 401

    result = response.json()

    assert result["error"] == "Unauthorized"
    assert "access_token" not in result