def wait_for_price_sort(page, direction: str):
    """等待商品价格完成排序"""

    page.wait_for_function(
        """direction => {
            const elements = Array.from(
                document.querySelectorAll(
                    '[data-test="product-price"]'
                )
            );

            const prices = elements.map(element =>
                Number(
                    element.innerText.replace(/[^0-9.]/g, '')
                )
            );

            if (prices.length < 2) {
                return false;
            }

            return prices.every((price, index) => {
                if (index === 0) {
                    return true;
                }

                return direction === 'asc'
                    ? prices[index - 1] <= price
                    : prices[index - 1] >= price;
            });
        }""",
        arg=direction,
        timeout=15000
    )

from pages.home_page import HomePage


def test_sort_products_by_price_ascending(page):
    """验证商品价格升序排序"""

    home_page = HomePage(page)
    home_page.open()

    home_page.product_cards.first.wait_for(
        state="visible",
        timeout=20000
    )

    home_page.sort_products("price,asc")
    wait_for_price_sort(page, "asc")

    prices = home_page.get_all_product_prices()

    assert len(prices) > 0

    assert prices == sorted(prices), (
        f"商品价格没有按照升序排列：{prices}"
    )

    print("价格升序结果：", prices)


def test_sort_products_by_price_descending(page):
    """验证商品价格降序排序"""

    home_page = HomePage(page)
    home_page.open()

    home_page.product_cards.first.wait_for(
        state="visible",
        timeout=20000
    )

    home_page.sort_products("price,desc")
    wait_for_price_sort(page, "desc")

    prices = home_page.get_all_product_prices()

    assert len(prices) > 0

    assert prices == sorted(prices, reverse=True), (
        f"商品价格没有按照降序排列：{prices}"
    )

    print("价格降序结果：", prices)