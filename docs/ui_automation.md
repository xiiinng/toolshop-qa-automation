# ToolShop QA — UI 自动化测试设计与执行报告

## 1. 测试目标

基于 Practice Software Testing 在线商城，使用 Playwright + Pytest 构建 UI 自动化测试框架，验证商城核心页面及业务功能的正确性。

本阶段重点：

- 验证商城首页及商品列表正常加载。
- 验证商品搜索、排序和筛选功能。
- 验证登录页面及异常登录场景。
- 使用 Page Object Model（POM）模式管理页面元素和操作。
- 提高自动化测试的可维护性与执行稳定性。

## 2. 测试环境

| 项目 | 版本或说明 |
|---|---|
| 操作系统 | Windows 10 |
| Python | 3.11.7 |
| 测试框架 | Pytest 9.2.0 |
| UI 自动化工具 | Playwright |
| 浏览器 | Chromium |
| 浏览器运行模式 | Headed |
| 被测系统 | Practice Software Testing |
| 测试地址 | https://practicesoftwaretesting.com/ |

## 3. 技术方案

### 3.1 技术栈

- Python：自动化测试开发语言。
- Pytest：测试用例组织、Fixture 管理及断言。
- Playwright：浏览器自动化操作。
- Page Object Model：页面对象设计模式。

### 3.2 项目结构

```text
toolshop-qa-automation/
├── pages/
│   ├── base_page.py
│   ├── home_page.py
│   └── login_page.py
│
├── tests/
│   └── ui/
│       ├── test_smoke.py
│       ├── test_products.py
│       ├── test_sort.py
│       ├── test_filters.py
│       └── test_login.py
│
└── docs/
    └── ui_automation.md
```

### 3.3 POM 设计

将页面元素定位和业务操作封装到独立页面类中，降低测试用例对页面实现细节的依赖。

**BasePage：**

封装通用浏览器操作：

- click：点击元素。
- fill：填写输入框。
- get_text：获取元素文本。
- is_visible：判断元素是否可见。
- wait_for_visible：等待元素可见。

**HomePage：**

封装商城首页操作：

- 打开商城首页。
- 获取商品数量、名称和价格。
- 搜索商品。
- 对商品进行排序。
- 获取商品价格列表。

**LoginPage：**

封装登录页面操作：

- 判断登录页面是否加载。
- 输入邮箱和密码。
- 提交登录表单。
- 获取登录错误提示。

## 4. UI 自动化测试场景

本阶段共实现10条正式 UI 自动化测试。

| 编号 | 测试场景 | 测试内容 |
|---|---|---|
| UI-001 | 首页加载 | 验证首页标题、搜索框和商品列表 |
| UI-002 | 商品列表展示 | 验证商品卡片正常显示 |
| UI-003 | 商品信息展示 | 验证商品名称和价格不为空 |
| UI-004 | 商品搜索 | 输入关键词并验证搜索结果 |
| UI-005 | 价格升序 | 验证商品价格按升序排列 |
| UI-006 | 价格降序 | 验证商品价格按降序排列 |
| UI-007 | 分类筛选 | 验证 Hammer 分类筛选结果 |
| UI-008 | 环保筛选 | 验证环保商品筛选结果及标识 |
| UI-009 | 登录页面加载 | 验证邮箱、密码、登录按钮等元素 |
| UI-010 | 无效凭据登录 | 验证错误提示内容及登录失败状态 |

## 5. 自动化测试稳定性实践

### 5.1 显式等待

针对商品搜索结果异步更新的问题，使用 Playwright 的响应监听机制，等待搜索请求完成后再检查结果。

针对商品排序，使用 `page.wait_for_function()` 等待页面价格列表满足排序条件，避免读取尚未更新的旧数据。

不使用固定时间的 `sleep` 作为正式测试同步方案。

### 5.2 动态数据断言

商品数据可能随线上环境变化，因此测试尽量基于页面实际返回的数据进行断言，而不是硬编码商品数量、商品 ID 或完整商品列表。

### 5.3 真实浏览器验证

当前 UI 自动化使用 Chromium Headed 模式运行。

有效账号登录时，Playwright 跳转账户页面后触发 Cloudflare 安全验证。使用相同账号和密码在普通 Chrome 中可以正常登录，因此该情况作为自动化环境限制记录，不作为商城登录缺陷。

## 6. 测试执行结果

### 6.1 执行命令

```powershell
python -m pytest `
    tests/ui/test_smoke.py `
    tests/ui/test_products.py `
    tests/ui/test_sort.py `
    tests/ui/test_filters.py `
    tests/ui/test_login.py `
    --browser chromium --headed -v -s
```

### 6.2 执行统计

| 指标 | 结果 |
|---|---:|
| 正式测试文件 | 5 |
| 测试用例总数 | 10 |
| 通过 | 10 |
| 失败 | 0 |
| 跳过 | 0 |
| 执行耗时 | 46.05 秒 |

**最终结果：10 passed, 1 warning in 46.05s**

### 6.3 测试观察

- 商品搜索能够返回符合关键词的商品。
- 商品价格升序、降序均符合预期。
- Hammer 分类筛选能够改变商品列表。
- 环保筛选能够展示带有环保标识的商品。
- 无效凭据登录能够正确显示错误提示。
- 有效账号在普通 Chrome 中登录成功，但 Playwright 自动化账户页访问受到 Cloudflare 验证限制。

### 6.4 已知警告

执行过程中出现 `PytestRemovedIn10Warning`，来自 pytest-playwright 插件内部的 session-scoped fixture。

该警告不影响本次测试执行结果，后续可在插件升级时重新验证兼容性。

## 7. 本阶段总结

本阶段完成了基于 Playwright + Pytest 的 UI 自动化测试实践：

1. 建立页面对象模型，封装首页和登录页面操作。
2. 完成商品列表、搜索、排序、筛选及登录异常场景自动化。
3. 使用显式等待处理页面异步更新。
4. 完成10条正式 UI 测试的全量回归，全部通过。
5. 识别并记录线上环境的 Cloudflare 自动化访问限制。

后续将在 Day6 继续进行探索性测试、缺陷分析、缺陷报告整理及回归验证。