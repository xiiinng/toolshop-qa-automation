from pages.home_page import HomePage


def test_inspect_search_elements(page):
    """验证搜索框和搜索按钮定位是否正确"""

    home_page = HomePage(page)
    home_page.open()

    home_page.product_cards.first.wait_for(
        state="visible",
        timeout=20000
    )

    assert home_page.search_input.count() == 1
    assert home_page.search_button.count() == 1

    assert home_page.search_input.is_visible()
    assert home_page.search_button.is_visible()

    print("搜索框和搜索按钮定位验证通过")