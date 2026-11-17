# BUG-001：用户注册接口未正确校验邮箱格式

## 1. 基本信息

- 缺陷编号：BUG-001
- 缺陷标题：用户注册接口未正确校验邮箱格式
- 所属模块：用户注册
- 缺陷类型：接口参数校验
- 优先级：待评估（建议 P2）
- 状态：已复现，待确认/修复

## 2. 测试环境

- 被测系统：https://api.practicesoftwaretesting.com
- 请求方法：POST
- 接口地址：`/users/register`
- 测试工具：Python + Requests + Pytest

## 3. 前置条件

API 服务正常，可以访问用户注册接口。

## 4. 复现步骤

1. 向 `POST /users/register` 发送注册请求。
2. 将 email 设置为 `invalid-69eaf2cd12`。
3. 提交请求并观察响应。
4. 使用另一组独立测试数据 `invalida28c2031.com` 再次提交请求。
5. 检查两次响应状态码及响应内容。

## 5. 预期结果

根据 Swagger 中 UserRequest.email 字段的 format: email 定义，
注册接口应对邮箱格式进行有效校验，拒绝不符合邮箱格式的输入。

Swagger 对注册接口声明了 HTTP 400 Bad Request，
但没有明确声明邮箱格式校验失败时必须返回 HTTP 422。

因此，本缺陷重点关注接口是否拒绝非法邮箱，
具体错误状态码以进一步确认的接口契约为准。

## 6. 实际结果

两种不符合邮箱格式的输入均返回 HTTP 201 Created，接口成功创建用户，并在响应中返回新创建的用户 ID。

## 7. 复现证据

| 测试输入 | 实际状态码 | 预期状态码 | 结果 |
|---|---:|---:|---|
| `invalid-69eaf2cd12` | 201 Created | 422 | 缺陷复现 |
| `invalida28c2031.com` | 201 Created | 422 | 缺陷复现 |

两组测试数据均为独立输入，排除了重复邮箱导致的干扰。

说明：
Swagger 未明确声明 HTTP 422，因此原自动化测试中的
HTTP 422 属于此前设定的测试预期，并非已确认的接口契约。
后续需要调整测试断言，避免将未声明的状态码作为确定依据。
## 8. 影响分析

接口可能接受不符合邮箱格式的数据，导致用户数据质量下降，并可能影响后续账号登录、邮件通知及其他依赖邮箱格式的业务流程。

## 9. 参考依据

Swagger：`POST /users/register`

`UserRequest.email`：
- type: string
- format: email
- maxLength: 256

## 10. 自动化验证

- 测试文件：`tests/api/test_known_bugs.py`
- 测试框架：Pytest
- 测试数量：2
- 复现结果：2 条测试均实际返回 HTTP 201，与预期 HTTP 422 不符
- 复现状态：稳定复现

**当前状态：已复现，待确认/修复。**