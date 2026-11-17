
import requests

from config.settings import BASE_URL, TIMEOUT


class APIClient:
    """统一 API 请求客户端"""

    def __init__(self):
        self.session = requests.Session()

        # 当前环境已验证：绕过系统代理后可以正常访问测试 API
        self.session.trust_env = False

    def request(self, method, endpoint, **kwargs):
        """发送通用 HTTP 请求"""
        url = f"{BASE_URL.rstrip('/')}/{endpoint.lstrip('/')}"

        # 设置默认超时时间
        kwargs.setdefault("timeout", TIMEOUT)

        response = self.session.request(
            method=method,
            url=url,
            **kwargs
        )

        return response

    def get(self, endpoint, params=None, **kwargs):
        """发送 GET 请求"""
        return self.request(
            "GET",
            endpoint,
            params=params,
            **kwargs
        )

    def close(self):
        """关闭 Session"""
        self.session.close()
