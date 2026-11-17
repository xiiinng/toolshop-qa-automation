from pages.home_page import HomePage


def test_homepage_loads(page):
    """验证商城首页及商品列表能够正常加载"""

    home_page = HomePage(page)

    home_page.open()

    # 验证页面标题
    assert home_page.get_title() == (
        "Practice Software Testing - Toolshop - v5.0"
    )

    # 验证首页核心搜索元素
    assert home_page.is_homepage_loaded()

    # 验证商品列表
    product_count = home_page.get_product_count()
    assert product_count > 0

    # 验证第一个商品的名称和价格
    product_name = home_page.get_first_product_name()
    product_price = home_page.get_first_product_price()

    assert product_name
    assert product_price.startswith("$")

    print(f"商品数量：{product_count}")
    print(f"第一个商品：{product_name}")
    print(f"商品价格：{product_price}")