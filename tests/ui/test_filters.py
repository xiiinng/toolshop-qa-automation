from pages.home_page import HomePage


def test_filter_products_by_hammer_category(page):
    """验证勾选 Hammer 分类后，商品列表发生相应变化"""

    home_page = HomePage(page)
    home_page.open()

    # 等待首页商品加载
    home_page.get_product_count()

    # 记录筛选前的商品
    before_names = home_page.get_all_product_names()

    # 勾选 Hammer 分类
    category_checkbox = page.get_by_label(
        "Hammer",
        exact=True
    )
    category_checkbox.check()

    # 等待商品列表更新
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

    # 获取筛选后的商品
    after_names = home_page.get_all_product_names()

    # 验证筛选结果
    assert category_checkbox.is_checked()
    assert after_names
    assert after_names != before_names
    assert all(
        "hammer" in name.lower()
        for name in after_names
    ), f"存在不属于 Hammer 分类的商品：{after_names}"

    print("筛选前商品数量：", len(before_names))
    print("筛选后商品数量：", len(after_names))
    print("筛选结果：", after_names)


def test_filter_eco_friendly_products(page):
    """验证环保筛选只展示带有环保标识的商品"""

    home_page = HomePage(page)
    home_page.open()

    # 等待首页商品加载
    home_page.get_product_count()

    # 记录筛选前商品
    before_names = home_page.get_all_product_names()

    # 勾选环保筛选
    eco_checkbox = page.get_by_label(
        "Show only eco-friendly products",
        exact=True
    )
    eco_checkbox.check()

    # 等待商品列表更新
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

    # 获取筛选后的商品卡片
    product_cards = home_page.product_cards

    after_names = home_page.get_all_product_names()

    # 验证筛选状态和结果
    assert eco_checkbox.is_checked()
    assert after_names
    assert after_names != before_names

    for index in range(product_cards.count()):
        card = product_cards.nth(index)

        product_name = card.locator(
            '[data-test="product-name"]'
        ).inner_text().strip()

        eco_badge = card.locator(
            '[data-test="eco-badge"]'
        )

        assert eco_badge.count() == 1, (
            f"商品 {product_name} 缺少环保标识"
        )

    print("筛选前商品数量：", len(before_names))
    print("筛选后商品数量：", len(after_names))
    print("环保筛选结果：", after_names)