
from playwright.sync_api import Page

from pages.base_page import BasePage


class LoginPage(BasePage):
    """商城登录页面对象"""

    def __init__(self, page: Page):
        super().__init__(page)

        # 邮箱输入框
        self.email_input = page.locator(
            '[data-test="email"]'
        )

        # 密码输入框
        self.password_input = page.locator(
            '[data-test="password"]'
        )

        # 登录按钮
        self.login_button = page.locator(
            '[data-test="login-submit"]'
        )

        # 注册链接
        self.register_link = page.locator(
            'a[href="/auth/register"]'
        )

        # 忘记密码链接
        self.forgot_password_link = page.locator(
            'a[href="/auth/forgot-password"]'
        )

        # 登录失败提示
        self.error_message = page.get_by_text(
            "Invalid email or password",
            exact=True
        )

    def is_login_page_loaded(self) -> bool:
        """判断登录页面是否加载成功"""
        self.email_input.wait_for(state="visible")
        self.password_input.wait_for(state="visible")

        return (
            self.email_input.is_visible()
            and self.password_input.is_visible()
        )

    def login(self, email: str, password: str):
        """执行登录操作"""
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()

    def get_error_message(self) -> str:
        """获取登录失败提示文本"""
        return self.error_message.inner_text().strip()
