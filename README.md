# ToolShop QA

基于 [Practice Software Testing - Toolshop](https://practicesoftwaretesting.com/) 在线商城构建的 Python 自动化测试项目。围绕商品浏览、搜索、筛选、用户注册与登录等核心业务，实践 API 自动化测试、UI 自动化测试、探索性测试和缺陷分析。

## 项目目标

- 使用 Pytest + Requests 实现 REST API 自动化测试。
- 使用 Playwright 实现 Web UI 自动化测试。
- 使用 Page Object Model（POM）组织页面对象。
- 通过参数化、Fixture、动态测试数据和显式等待提高测试可维护性与稳定性。
- 结合 Swagger 分析接口定义，开展边界测试和异常场景探索。
- 记录测试发现的问题，并形成缺陷报告。

## 技术栈

| 技术 | 用途 |
|---|---|
| Python 3.11 | 测试开发语言 |
| Pytest | 测试框架 |
| Requests | API 自动化测试 |
| Playwright | Web UI 自动化测试 |
| pytest-html | HTML 测试报告 |
| python-dotenv | 环境变量管理 |
| Faker | 测试数据生成 |
| Git | 版本管理 |

## 测试对象

- 前端商城：https://practicesoftwaretesting.com/
- API 服务：https://api.practicesoftwaretesting.com
- API 文档：https://api.practicesoftwaretesting.com/api/documentation

## 项目结构

```text
toolshop-qa-automation/
├── api/                    # API 请求客户端
├── config/                 # 测试配置
├── data/                   # 测试数据
├── docs/                   # 测试文档与分析
├── exploratory/            # 探索性测试脚本
│   ├── api/
│   └── ui/
├── bug_reports/            # 缺陷报告
├── pages/                  # UI 页面对象（POM）
├── tests/
│   ├── api/                # API 自动化测试
│   ├── ui/                 # UI 自动化测试
│   └── manual/             # 手工测试用例
├── utils/                  # 通用工具
├── .env.example            # 环境变量示例
├── conftest.py             # Pytest Fixtures
├── pytest.ini              # Pytest 配置
├── requirements.txt        # 项目依赖
└── README.md
```

## 环境准备

建议使用 Python 3.11。

### 1. 克隆项目

```bash
git clone <你的GitHub仓库地址>
cd toolshop-qa-automation
```

### 2. 创建虚拟环境

```bash
python -m venv .venv
```

Windows PowerShell：

```powershell
.venv\Scripts\Activate.ps1
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 安装 Playwright 浏览器

```bash
playwright install chromium
```

### 5. 配置环境变量

复制 `.env.example` 为 `.env`，根据实际需要修改配置。

## 运行测试

### API 自动化测试

运行商品接口测试：

```bash
python -m pytest tests/api/test_products.py -v
```

运行用户接口测试：

```bash
python -m pytest tests/api/test_users.py -v
```

### UI 自动化测试

UI 测试建议使用有头模式运行：

```bash
python -m pytest tests/ui/ --browser chromium --headed -v
```

### 运行 HTML 报告

```bash
python -m pytest tests/api/test_products.py --html=reports/api-report.html --self-contained-html
```

## 当前测试成果

| 测试类型 | 已完成内容 | 已记录结果 |
|---|---|---|
| 手工测试 | 商品、搜索、筛选、用户、购物车、联系表单 | 35 条 PASS |
| API 自动化 | 商品列表、分页、排序、筛选、字段校验等 | 商品接口 11 条测试通过 |
| UI 自动化 | 首页、商品展示、搜索、排序、筛选、登录页面及异常登录 | 10 passed，1 warning |
| 探索性测试 | 注册字段边界、空凭据、购物车数量边界等 | 已记录探索结果 |
| 缺陷分析 | 注册邮箱格式校验行为 | 已形成 BUG-001，待确认 |

以上为项目阶段性执行结果，不代表所有接口和场景均已通过。

## 测试设计与质量实践

- 使用随机邮箱和动态测试数据，减少测试数据冲突。
- 使用 Fixture 管理 API 客户端和测试用户。
- 使用 POM 分离页面元素定位与测试逻辑。
- 使用 Playwright 自动等待、响应监听和页面状态等待，减少固定时间等待。
- 根据 Swagger 和实际响应设计接口断言。
- 区分业务缺陷、接口契约待确认问题与测试环境异常。
- 对线上测试数据注意清理，避免无意义地重复创建账号。

## 已知限制

- 项目使用公开在线 Demo，服务可用性和测试数据可能发生变化。
- UI 自动化可能受到 Cloudflare 验证影响，建议在本地有头浏览器中运行。
- `test_known_bugs.py` 属于已知问题专项测试，不建议作为常规回归测试反复执行，因为它会向在线服务提交注册请求。
- 探索性测试脚本存放于 `exploratory/`，不属于常规 Pytest 测试集。

## 文档

- `docs/test_scope.md`：测试范围
- `docs/api_analysis.md`：API 接口分析与探索记录
- `docs/ui_automation.md`：UI 自动化设计与执行记录
- `tests/manual/test_cases.md`：手工测试用例
- `bug_reports/`：缺陷报告
