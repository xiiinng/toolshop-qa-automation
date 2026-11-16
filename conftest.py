
"""
ToolShop QA - Pytest 公共配置文件
"""

import pytest


@pytest.fixture(scope="session")
def project_name():
    """返回当前自动化测试项目名称。"""
    return "ToolShop QA"
