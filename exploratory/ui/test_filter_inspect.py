
from pages.home_page import HomePage


def test_inspect_filter_controls(page):
    """探索商城首页的商品筛选控件"""

    home_page = HomePage(page)
    home_page.open()

    home_page.product_cards.first.wait_for(
        state="visible",
        timeout=20000
    )

    selects = page.locator("select")

    print("\n========== 筛选控件探索 ==========")
    print("下拉框数量：", selects.count())

    for index in range(selects.count()):
        select = selects.nth(index)

        print(f"\n第 {index + 1} 个下拉框")
        print("data-test：", select.get_attribute("data-test"))
        print("当前值：", select.input_value())

        options = select.locator("option")

        for option_index in range(options.count()):
            option = options.nth(option_index)

            print(
                "选项：",
                option.inner_text().strip(),
                "| value：",
                option.get_attribute("value")
            )


    print("\n========== 品牌和分类名称探索 ==========")

    checkboxes = page.locator('input[type="checkbox"]')

    for index in range(checkboxes.count()):
        checkbox = checkboxes.nth(index)

        info = checkbox.evaluate("""
            element => ({
                testId: element.getAttribute('data-test'),
                id: element.id,
                value: element.value,
                parentTag: element.parentElement.tagName,
                parentText: element.parentElement.innerText.trim(),
                grandparentText:
                    element.parentElement.parentElement.innerText.trim()
            })
        """)

        print(f"\n第 {index + 1} 个复选框：")
        print("data-test：", info["testId"])
        print("id：", info["id"])
        print("value：", info["value"])
        print("父元素：", info["parentTag"])
        print("父元素文本：", info["parentText"])
        print("上级元素文本：", info["grandparentText"])


def test_inspect_brand_filter_behavior(page):
    """探索品牌筛选的实际行为"""

    home_page = HomePage(page)
    home_page.open()

    home_page.product_cards.first.wait_for(
        state="visible",
        timeout=20000
    )

    # 记录商品相关请求
    product_requests = []

    def capture_request(request):
        if "/products" in request.url:
            product_requests.append(request.url)

    page.on("request", capture_request)

    # 获取筛选前商品数量
    before_count = home_page.product_cards.count()

    print("\n========== 品牌筛选前 ==========")
    print("商品数量：", before_count)
    print("商品名称：", home_page.get_all_product_names())

    # 选择 ForgeFlex Tools
    brand_checkbox = page.get_by_label(
        "ForgeFlex Tools",
        exact=True
    )

    brand_checkbox.check()



    # 暂时等待页面更新，用于探索
    page.wait_for_timeout(3000)

    print("\n========== 品牌筛选后 ==========")
    print("复选框是否选中：", brand_checkbox.is_checked())
    print("商品数量：", home_page.product_cards.count())
    print("商品名称：", home_page.get_all_product_names())

    print("\n商品卡片文本：")
    for index in range(home_page.product_cards.count()):
        print(
            home_page.product_cards.nth(index).inner_text()
        )

    print("\n商品相关请求：")
    for url in product_requests:
        print(url)


    print("\n========== 商品卡片 DOM 信息 ==========")

    print(
        "品牌复选框 value：",
        brand_checkbox.get_attribute("value")
    )

    for index in range(home_page.product_cards.count()):
        card = home_page.product_cards.nth(index)

        print(f"\n第 {index + 1} 个商品：")
        print("商品名称：", card.locator(
            '[data-test="product-name"]'
        ).inner_text().strip())

        print("商品链接：", card.get_attribute("href"))

        print("商品卡片 data-test：", card.get_attribute("data-test"))

        print("商品卡片 HTML：", card.evaluate(
            "element => element.outerHTML"
        )[:1500])


    print("\n========== 商品详情接口探索 ==========")

    detail_responses = []

    def capture_response(response):
        if "/products/" in response.url:
            detail_responses.append(response)

    page.on("response", capture_response)

    print("\n========== 详情页接口请求探索 ==========")

    detail_requests = []
    detail_responses = []

    page.on(
        "request",
        lambda request: detail_requests.append(request)
        if request.resource_type in ("xhr", "fetch")
        else None
    )

    page.on(
        "response",
        lambda response: detail_responses.append(response)
        if response.request.resource_type in ("xhr", "fetch")
        else None
    )

    # 点击筛选后的第一个商品
    home_page.product_cards.first.click()

    # 等待商品详情页面加载
    page.wait_for_url("**/product/**", timeout=15000)

    page.wait_for_load_state(
        "domcontentloaded",
        timeout=15000
    )

    print("当前 URL：", page.url)

    # 仅用于本次探索，等待接口请求完成
    page.wait_for_timeout(3000)

    print("\n========== 详情页接口请求 ==========")

    print("\n接口请求：")
    for request in detail_requests:
        print(request.method, request.url)

    print("\n接口响应：")
    for response in detail_responses:
        print(response.status, response.url)

    for response in detail_responses:
        print("\n请求 URL：", response.url)
        print("响应状态：", response.status)

        try:
            print("响应 JSON：", response.json())
        except Exception:
            print("响应不是 JSON")

    print("\n========== 商品详情页信息探索 ==========")

    # 输出详情页可见文本
    detail_text = page.locator("body").inner_text()
    print("\n详情页可见文本：")
    print(detail_text)

    print("\n========== 品牌元素 DOM 探索 ==========")

    brand_elements = page.get_by_text(
        "ForgeFlex Tools",
        exact=True
    )

    print("品牌文本定位数量：", brand_elements.count())

    for index in range(brand_elements.count()):
        element = brand_elements.nth(index)

        print(
            f"第 {index + 1} 个品牌元素：",
            element.evaluate(
                "(el) => el.outerHTML"
            )
        )

    # 检查页面中是否存在品牌相关元素
    brand_elements = page.get_by_text(
        "Brand",
        exact=True
    )

    print("\n品牌标签数量：", brand_elements.count())

    if brand_elements.count() > 0:
        for index in range(brand_elements.count()):
            element = brand_elements.nth(index)
            print(
                f"品牌标签 {index + 1} 的父元素：",
                element.locator("..").inner_text()
            )


def test_inspect_category_filter_behavior(page):
    """探索商品分类筛选行为"""

    from pages.home_page import HomePage

    home_page = HomePage(page)
    home_page.open()

    # 等待首页商品加载
    home_page.get_product_count()

    # 记录筛选前的商品名称
    before_names = home_page.get_all_product_names()
    print("\n筛选前商品：", before_names)

    # 定位 Hammer 分类复选框
    category_checkbox = page.get_by_label(
        "Hammer",
        exact=True
    )

    print("Hammer 复选框数量：", category_checkbox.count())

    # 勾选分类
    category_checkbox.check()

    # 等待商品列表发生变化
    page.wait_for_function(
        """(before) => {
            const names = Array.from(
                document.querySelectorAll('[data-test="product-name"]')
            ).map(el => el.textContent.trim());

            return names.length > 0 && names.join("|") !== before;
        }""",
        arg="|".join(before_names),
        timeout=15000
    )

    # 获取筛选后的商品名称
    after_names = home_page.get_all_product_names()

    print("筛选后商品：", after_names)
    print("筛选前商品数量：", len(before_names))
    print("筛选后商品数量：", len(after_names))
    print("复选框是否选中：", category_checkbox.is_checked())


def test_inspect_eco_filter_behavior(page):
    """探索环保商品筛选行为"""

    from pages.home_page import HomePage

    home_page = HomePage(page)
    home_page.open()

    home_page.get_product_count()

    before_names = home_page.get_all_product_names()
    print("\n筛选前商品：", before_names)

    eco_checkbox = page.get_by_label(
        "Show only eco-friendly products",
        exact=True
    )

    print("环保筛选控件数量：", eco_checkbox.count())

    eco_checkbox.check()

    page.wait_for_function(
        """(before) => {
            const names = Array.from(
                document.querySelectorAll('[data-test="product-name"]')
            ).map(el => el.textContent.trim());

            return names.length > 0 && names.join("|") !== before;
        }""",
        arg="|".join(before_names),
        timeout=15000
    )

    after_names = home_page.get_all_product_names()

    print("\n========== 环保标识验证 ==========")

    product_cards = home_page.product_cards

    for index in range(product_cards.count()):
        card = product_cards.nth(index)

        product_name = card.locator(
            '[data-test="product-name"]'
        ).inner_text().strip()

        eco_badge = card.locator(
            '[data-test="eco-badge"]'
        )

        print(
            f"商品：{product_name} | "
            f"环保标识数量：{eco_badge.count()}"
        )

    print("筛选后商品：", after_names)
    print("筛选前商品数量：", len(before_names))
    print("筛选后商品数量：", len(after_names))
    print("复选框是否选中：", eco_checkbox.is_checked())
