
from pages.home_page import HomePage
from pages.login_page import LoginPage


def test_inspect_wrong_password_behavior(page):
    """探索使用不存在的账号登录时，页面如何响应"""

    # 打开首页
    home_page = HomePage(page)
    home_page.open()
    home_page.get_product_count()

    # 进入登录页面
    page.get_by_text("Sign in", exact=True).click()

    login_page = LoginPage(page)
    assert login_page.is_login_page_loaded()

    # 使用不存在的邮箱和错误密码
    login_page.login(
        email="toolshop.invalid.user@example.com",
        password="WrongPassword@123"
    )

    # 等待登录请求完成或页面状态发生变化
    page.wait_for_timeout(3000)

    print("\n========== 错误登录行为探索 ==========")
    print("当前 URL：", page.url)
    print("页面标题：", page.title())

    print("\n页面正文：")
    print(page.locator("body").inner_text()[:2000])

    print("\n邮箱输入框是否可见：",
          login_page.email_input.is_visible())

    print("密码输入框是否可见：",
          login_page.password_input.is_visible())

    page.screenshot(
        path="reports/login_wrong_password.png",
        full_page=True
    )



from pages.home_page import HomePage
from pages.login_page import LoginPage


def test_inspect_valid_login_behavior(page, create_registered_user):
    """探索使用 API 创建的用户通过 UI 登录后的表现"""

    # 通过 API 创建随机测试用户
    user = create_registered_user()

    print("\n测试用户邮箱：", user["email"])
    print("测试用户密码：", user["password"])

    # 打开商城首页
    home_page = HomePage(page)
    home_page.open()
    home_page.get_product_count()

    # 进入登录页面
    page.get_by_text(
        "Sign in",
        exact=True
    ).click()

    # 使用刚创建的账号登录
    login_page = LoginPage(page)
    assert login_page.is_login_page_loaded()

    login_page.login(
        email=user["email"],
        password=user["password"]
    )

    # 探索登录后的页面状态
    page.wait_for_timeout(3000)

    print("\n========== 有效账号登录结果 ==========")
    print("当前 URL：", page.url)
    print("页面标题：", page.title())
    print("\n页面正文：")
    print(page.locator("body").inner_text()[:2000])

    page.screenshot(
        path="reports/login_success_inspect.png",
        full_page=True
    )
