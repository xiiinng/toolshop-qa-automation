def test_inspect_login_empty_credentials(api_client):
    """探索登录接口对空邮箱和空密码的处理"""

    payload = {
        "email": "",
        "password": ""
    }

    response = api_client.request(
        "POST",
        "/users/login",
        json=payload
    )

    print("测试输入：", payload)
    print("实际状态码：", response.status_code)
    print("实际响应内容：", response.text)