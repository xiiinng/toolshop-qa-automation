from pages.home_page import HomePage


def test_inspect_sort_request(page):
    """探索商品排序时的网络请求"""

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

    # 执行价格升序
    home_page.sort_products("price,asc")

    # 等待页面更新
    page.wait_for_timeout(3000)

    print("\n========== 商品排序请求分析 ==========")
    print("当前排序值：", page.locator(
        '[data-test="sort"]'
    ).input_value())

    print("\n商品 API 请求：")
    for url in product_requests:
        print(url)

    print("\n当前商品价格：", home_page.get_all_product_prices())

    print("当前商品名称：", home_page.get_all_product_names())