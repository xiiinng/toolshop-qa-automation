# ToolShop QA — 测试范围说明

**文档版本：** v1.0  
**项目类型：** Web 商城功能测试与自动化测试  
**被测系统：** Practice Software Testing（Toolshop）

## 1. 项目背景

ToolShop QA 是一个基于 Practice Software Testing 在线商城开展的软件测试实战项目。

项目使用 Python、Pytest、Requests 和 Playwright，围绕商城核心业务开展手工测试、API 自动化测试和 Web UI 自动化测试，最终形成测试用例、自动化脚本、缺陷记录和测试报告。

## 2. 测试目标

1. 验证商城核心业务功能是否符合预期。
2. 验证关键 API 接口的正确性和异常处理能力。
3. 使用 Playwright 实现核心业务流程的 UI 自动化。
4. 记录实际发现的问题，形成规范的缺陷报告。
5. 通过 GitHub Actions 实现自动化测试持续集成。

## 3. 测试范围

### 3.1 商品模块

- 商品列表展示
- 商品详情查看
- 商品价格及图片展示

### 3.2 搜索与筛选模块

- 关键词搜索
- 商品分类筛选
- 品牌筛选
- 搜索无结果场景

### 3.3 用户模块

- 用户登录
- 错误账号或密码登录
- 用户注册
- 登录状态验证

### 3.4 购物车模块

- 添加商品到购物车
- 修改商品数量
- 删除购物车商品
- 商品金额计算

### 3.5 联系表单模块

- 必填项校验
- 邮箱格式校验
- 表单提交
- 提交结果提示

## 4. 测试类型

| 测试类型 | 测试工具 |
|---|---|
| 手工功能测试 | 浏览器 |
| API 自动化测试 | Requests + Pytest |
| UI 自动化测试 | Playwright + Pytest |
| 缺陷管理 | Markdown |
| 测试报告 | pytest-html |
| 持续集成 | GitHub Actions |

## 5. 暂不覆盖的范围

- 真实支付及资金交易
- 大规模性能与压力测试
- 完整生产环境安全测试
- 全浏览器兼容性测试
- 商城后端源码及数据库测试

## 6. 测试环境

| 项目 | 地址或版本 |
|---|---|
| 被测商城 | https://practicesoftwaretesting.com/ |
| API 文档 | https://api.practicesoftwaretesting.com/api/documentation |
| Python | 3.11.7 |
| Pytest | 9.2.0 |
| Requests | 2.34.2 |
| Playwright | 1.65.2 |
| 浏览器 | Chromium |

## 7. 项目交付目标

- 35–45 条手工测试用例
- 15–20 个 API 自动化测试场景
- 8–12 个 UI 自动化测试场景
- 规范的缺陷记录（以实际发现的问题为准）
- 自动化测试报告
- GitHub Actions 自动化测试流程
- 完整的项目 README 文档

**说明：** 以上数量是项目计划目标，实际测试范围和数量根据系统功能及测试进度调整，不虚构测试结果或缺陷。