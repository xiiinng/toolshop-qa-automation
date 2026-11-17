
def test_inspect_login_page(page):
    """通过首页 Sign in 入口进入登录页面"""

    page.goto(
        "https://practicesoftwaretesting.com/#/",
        wait_until="domcontentloaded",
        timeout=60000
    )

    # 等待首页商品加载
    page.locator(
        'a[data-test^="product-"][href*="/product/"]'
    ).first.wait_for(
        state="visible",
        timeout=20000
    )

    # 查看 Sign in 链接
    sign_in = page.get_by_text(
        "Sign in",
        exact=True
    )

    print("Sign in 元素数量：", sign_in.count())

    # 点击登录入口
    sign_in.first.click()

    # 等待页面跳转及渲染
    page.wait_for_timeout(3000)

    print("\n========== 登录页面状态 ==========")
    print("当前 URL：", page.url)
    print("页面标题：", page.title())
    print("页面正文：")
    print(page.locator("body").inner_text()[:2000])


    print("\n========== 输入框详细信息 ==========")

    inputs = page.locator("input")

    for index in range(inputs.count()):
        item = inputs.nth(index)

        print({
            "index": index,
            "type": item.get_attribute("type"),
            "placeholder": item.get_attribute("placeholder"),
            "name": item.get_attribute("name"),
            "data-test": item.get_attribute("data-test"),
            "id": item.get_attribute("id"),
            "aria-label": item.get_attribute("aria-label")
        })

    print("\n========== 按钮详细信息 ==========")

    buttons = page.locator("button")

    for index in range(buttons.count()):
        item = buttons.nth(index)

        print({
            "index": index,
            "text": item.inner_text().strip(),
            "type": item.get_attribute("type"),
            "data-test": item.get_attribute("data-test"),
            "aria-label": item.get_attribute("aria-label")
        })

    print("\n========== 链接详细信息 ==========")

    links = page.locator("a")

    for index in range(links.count()):
        item = links.nth(index)
        text = item.inner_text().strip()

        if "Register" in text or "Forgot" in text:
            print({
                "text": text,
                "href": item.get_attribute("href")
            })

