
from pages.home_page import HomePage
from pages.login_page import LoginPage


def test_login_page_loads(page):
    """验证用户能够从商城首页进入登录页面"""

    # 打开商城首页
    home_page = HomePage(page)
    home_page.open()

    # 等待商品加载
    home_page.get_product_count()

    # 点击 Sign in
    page.get_by_text(
        "Sign in",
        exact=True
    ).click()

    # 创建登录页面对象
    login_page = LoginPage(page)

    # 验证登录页面加载
    assert login_page.is_login_page_loaded()

    # 验证核心元素
    assert login_page.login_button.is_visible()
    assert login_page.register_link.is_visible()
    assert login_page.forgot_password_link.is_visible()

    print("登录页面加载成功")
    print("邮箱输入框、密码输入框、登录按钮均正常")



def test_login_with_invalid_credentials(page):
    """验证使用无效登录凭据时系统显示错误提示"""

    home_page = HomePage(page)
    home_page.open()
    home_page.get_product_count()

    # 进入登录页面
    page.get_by_text(
        "Sign in",
        exact=True
    ).click()

    login_page = LoginPage(page)
    assert login_page.is_login_page_loaded()

    # 输入无效凭据
    login_page.login(
        email="toolshop.invalid.user@example.com",
        password="WrongPassword@123"
    )

    # 等待错误提示出现
    login_page.error_message.wait_for(
        state="visible",
        timeout=15000
    )

    # 验证错误提示
    assert login_page.get_error_message() == (
        "Invalid email or password"
    )

    # 验证登录失败后仍停留在登录页面
    assert "/auth/login" in page.url

    print("无效凭据登录失败，错误提示正常")
