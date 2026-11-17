
def test_inspect_homepage(page):
    """探索首页 DOM，为后续页面对象设计提供依据"""

    api_responses = []
    page_errors = []

    page.on(
        "response",
        lambda response: api_responses.append({
            "url": response.url,
            "status": response.status,
            "resource_type": response.request.resource_type
        })
        if response.request.resource_type in ["xhr", "fetch"]
        else None
    )

    page.on("pageerror", lambda error: page_errors.append(str(error)))

    failed_requests = []
    console_errors = []

    page.on(
        "requestfailed",
        lambda request: failed_requests.append({
            "url": request.url,
            "error": request.failure
        })
    )

    page.on(
        "console",
        lambda message: console_errors.append(message.text)
        if message.type == "error"
        else None
    )

    response = page.goto(
        "https://practicesoftwaretesting.com/#/",
        wait_until="domcontentloaded",
        timeout=60000
    )

    # 等待第一个商品卡片出现
    product_cards = page.locator(
        'a[data-test^="product-"][href*="/product/"]'
    )

    product_cards.first.wait_for(
        state="visible",
        timeout=20000
    )

    print("\n========== 商品列表 ==========")
    print("商品卡片数量:", product_cards.count())

    for i in range(min(product_cards.count(), 5)):
        card = product_cards.nth(i)

        name = card.locator(
            '[data-test="product-name"]'
        ).inner_text()

        price = card.locator(
            '[data-test="product-price"]'
        ).inner_text()

        print(f"商品{i + 1}: {name.strip()} | 价格: {price.strip()}")

    print("\n========== 主文档 HTML 摘要 ==========")
    html = response.text() if response else ""

    print("HTML 长度:", len(html))
    print("是否包含 Cloudflare:", "cloudflare" in html.lower())
    print("是否包含商城入口 root:", "app-root" in html.lower())
    print("HTML 前 1200 个字符:")
    print(html[:1200])

    print("\n========== 主文档响应 ==========")
    print("HTTP 状态码:", response.status if response else "无响应")
    print("最终 URL:", page.url)
    print("页面标题:", page.title())

    print("\n========== 页面基本信息 ==========")
    print("URL:", page.url)
    print("标题:", page.title())

    print("\n========== 页面链接 ==========")
    links = page.locator("a").all()

    for link in links:
        text = link.inner_text().strip()
        href = link.get_attribute("href")

        if text or href:
            print(f"文本: {text!r} | 地址: {href!r}")

    print("\n========== 输入框 ==========")
    inputs = page.locator("input").all()

    for item in inputs:
        print(
            "类型:", item.get_attribute("type"),
            "| placeholder:", item.get_attribute("placeholder"),
            "| name:", item.get_attribute("name")
        )

    print("\n========== 按钮 ==========")
    buttons = page.locator("button").all()

    for button in buttons:
        print("按钮:", button.inner_text().strip())

    print("\n========== 页面正文 ==========")
    print(page.locator("body").inner_text()[:3000])

    print("\n========== XHR / Fetch 请求 ==========")
    for item in api_responses:
        print(item)

    print("\n========== 页面 JavaScript 错误 ==========")
    for error in page_errors:
        print(error)

    assert page.locator("body").is_visible()


    print("\n========== 商品图片 ==========")
    images = page.locator("img").evaluate_all(
        """imgs => imgs.map(img => ({
            alt: img.alt,
            src: img.getAttribute('src')
        }))"""
    )

    for image in images:
        print(image)

    print("\n========== 商品相关链接 ==========")
    links = page.locator("a").evaluate_all(
        """links => links
            .filter(a => a.getAttribute('href')?.toLowerCase().includes('product'))
            .map(a => ({
                text: a.innerText.trim(),
                href: a.getAttribute('href')
            }))"""
    )

    for link in links:
        print(link)


    print("\n========== 页面 JavaScript 文件 ==========")
    scripts = page.locator("script[src]").evaluate_all(
        "scripts => scripts.map(script => script.src)"
    )
    for script in scripts:
        print(script)

    print("\n========== 加载失败的请求 ==========")
    for item in failed_requests:
        print(item)

    print("\n========== Console 错误 ==========")
    for error in console_errors:
        print(error)