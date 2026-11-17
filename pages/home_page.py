
from playwright.sync_api import Page

from pages.base_page import BasePage


class HomePage(BasePage):
    """商城首页页面对象"""

    URL = "https://practicesoftwaretesting.com/#/"

    def __init__(self, page: Page):
        super().__init__(page)

        self.product_cards = page.locator(
            'a[data-test^="product-"][href*="/product/"]'
        )

        self.product_names = page.locator(
            '[data-test="product-name"]'
        )

        self.search_input = page.locator(
            '[data-test="search-query"]'
        )
        self.search_button = page.locator(
            '[data-test="search-submit"]'
        )

    def open(self):
        """打开商城首页"""
        self.page.goto(
            self.URL,
            wait_until="domcontentloaded",
            timeout=60000
        )

    def get_title(self) -> str:
        """获取首页标题"""
        return self.page.title()

    def is_homepage_loaded(self) -> bool:
        """判断商城首页的核心搜索元素是否加载成功"""
        search_input = self.page.get_by_placeholder("Search")
        search_input.wait_for(state="visible", timeout=15000)
        return search_input.is_visible()

    def get_product_count(self) -> int:
        """获取当前页面商品卡片数量"""
        self.product_cards.first.wait_for(
            state="visible",
            timeout=20000
        )
        return self.product_cards.count()

    def get_first_product_name(self) -> str:
        """获取第一个商品名称"""
        return self.product_names.first.inner_text().strip()

    def get_first_product_price(self) -> str:
        """获取第一个商品价格"""
        return self.product_cards.first.locator(
            '[data-test="product-price"]'
        ).inner_text().strip()

    def get_all_product_names(self) -> list[str]:
        """获取当前页面所有商品名称"""
        return [
            name.strip()
            for name in self.product_names.all_inner_texts()
        ]

    def search_product(self, keyword: str):
        """根据关键词搜索商品"""
        self.search_input.fill(keyword)
        self.search_button.click()

    def get_search_result_names(self) -> list[str]:
        """获取当前搜索结果中的商品名称"""

        return [
            name.strip()
            for name in self.product_names.all_inner_texts()
        ]

    def sort_products(self, sort_value: str):
        """根据指定规则对商品进行排序"""

        sort_select = self.page.locator(
            '[data-test="sort"]'
        )

        sort_select.select_option(sort_value)

    def get_all_product_prices(self) -> list[float]:
        """获取当前页面所有商品价格"""

        prices = self.page.locator(
            '[data-test="product-price"]'
        ).all_inner_texts()

        return [
            float(price.replace("$", "").strip())
            for price in prices
        ]