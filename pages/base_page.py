
from playwright.sync_api import Page, Locator


class BasePage:
    """所有页面对象的基类，封装通用浏览器操作"""

    def __init__(self, page: Page):
        self.page = page

    def click(self, locator: Locator):
        """点击页面元素"""
        locator.click()

    def fill(self, locator: Locator, value: str):
        """向输入框填写内容"""
        locator.fill(value)

    def get_text(self, locator: Locator) -> str:
        """获取页面元素文本"""
        return locator.inner_text()

    def is_visible(self, locator: Locator) -> bool:
        """判断页面元素是否可见"""
        return locator.is_visible()

    def wait_for_visible(self, locator: Locator):
        """等待元素变为可见状态"""
        locator.wait_for(state="visible")
