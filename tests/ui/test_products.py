
from pages.home_page import HomePage


def test_product_list_is_displayed(page):
    """验证首页商品列表正常展示"""

    home_page = HomePage(page)
    home_page.open()

    product_count = home_page.get_product_count()
    product_names = home_page.get_all_product_names()

    assert product_count > 0
    assert len(product_names) == product_count


def test_product_cards_have_name_and_price(page):
    """验证商品卡片包含名称和价格"""

    home_page = HomePage(page)
    home_page.open()

    product_count = home_page.get_product_count()

    for index in range(product_count):
        card = home_page.product_cards.nth(index)

        name = card.locator(
            '[data-test="product-name"]'
        ).inner_text().strip()

        price = card.locator(
            '[data-test="product-price"]'
        ).inner_text().strip()

        assert name, f"第 {index + 1} 个商品名称为空"
        assert price.startswith("$"), (
            f"第 {index + 1} 个商品价格格式异常：{price}"
        )

def test_search_product_by_keyword(page):
    """验证用户可以通过关键词搜索商品"""

    home_page = HomePage(page)
    home_page.open()

    keyword = "pliers"

    # 等待搜索接口返回成功
    with page.expect_response(
        lambda response: (
            "/products/search" in response.url
            and response.status == 200
        ),
        timeout=15000
    ):
        home_page.search_product(keyword)

    product_names = home_page.get_search_result_names()

    assert len(product_names) > 0

    for name in product_names:
        assert keyword.lower() in name.lower(), (
            f"搜索结果不符合关键词：{name}"
        )

    print("搜索结果：", product_names)