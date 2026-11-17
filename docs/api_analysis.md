
# ToolShop QA — API 接口分析

## 一、接口测试目标

通过分析 Practice Software Testing API，
了解商品核心接口的请求方式、参数和响应结构，
为后续 Requests + Pytest 自动化测试做准备。

## 二、接口测试环境

- Base URL: https://api.practicesoftwaretesting.com
- API 文档: https://api.practicesoftwaretesting.com/api/documentation

## 三、商品模块接口分析

### 3.1 商品列表接口

- 接口名称：Retrieve all products
- 请求方法：GET
- 接口路径：/products
- 完整地址：https://api.practicesoftwaretesting.com/products

### 3.2 请求参数

| 参数 | 类型 | 说明 | 验证情况 |
|---|---|---|---|
| by_brand | string | 按品牌 ID 筛选 | PASS |
| by_category | string | 按分类 ID 筛选 | PASS |
| is_rental | string | 筛选租赁商品 | PASS |
| between | string | 价格区间筛选 | PASS |
| sort | string | 商品排序 | PASS |
| page | integer | 分页查询 | PASS |

### 3.3 响应结构

| 字段 | 类型 | 说明 |
|---|---|---|
| current_page | integer | 当前页码 |
| data | array | 商品数据 |
| from | integer/null | 当前页起始记录 |
| last_page | integer | 最后一页 |
| per_page | integer | 每页数量 |
| to | integer/null | 当前页结束记录 |
| total | integer | 商品总数 |

商品对象主要字段：

- id：商品 ID
- name：商品名称
- description：商品描述
- price：商品价格
- is_rental：是否租赁
- in_stock：是否有库存
- is_eco_friendly：是否环保
- brand：品牌信息
- category：分类信息
- product_image：商品图片信息

### 3.4 API 手工探索结果

| 编号 | 测试场景 | 实际结果 | 结论 |
|---|---|---|---|
| API-001 | 获取商品列表 | 正常返回商品 JSON | PASS |
| API-002 | 分页查询 | 第二页数据正常且与第一页不同 | PASS |
| API-003 | 价格升序 | 商品价格从低到高排列 | PASS |
| API-004 | 品牌筛选 | 返回商品品牌均匹配 | PASS |
| API-005 | 分类筛选 | 返回商品分类均匹配 | PASS |
| API-006 | 价格区间 | 商品价格均在 10 到 30 之间 | PASS |
| API-007 | 租赁商品 | 返回商品的 is_rental 均为 true | PASS |

### 3.5 测试过程中的发现

1. 使用旧商品数据中的品牌 ID 和分类 ID 查询时，返回 total=0。
2. 重新获取当前商品数据并使用最新 ID 后，筛选结果正常。
3. 实际响应中的布尔字段使用 true/false，与 Swagger 示例中的 0/1 表现不同。
4. 价格区间查询结果符合指定范围，当前样本未包含边界值 10 和 30。

以上现象已记录为测试观察，不直接认定为系统缺陷。

API 探索发现：注册接口存在密码泄露检测
- 接口：POST /users/register
- 现象：符合基本格式的密码仍可能被拒绝。
- 返回状态码：422
- 原因：密码被识别为曾出现在数据泄露记录中。
- 处理：使用随机生成的测试密码，避免固定弱密码。
- 结论：属于额外业务校验规则，不应直接认定为 Bug。

### 用户认证接口自动化测试结果

| 测试编号 | 测试场景 | 预期结果 | 实际结果 |
|---|---|---|---|
| API-USER-001 | 用户正常注册 | HTTP 201 | PASS |
| API-USER-002 | 新注册用户正常登录 | HTTP 200，返回 Token | PASS |
| API-USER-003 | 有效 Token 获取当前用户 | HTTP 200 | PASS |
| API-USER-004 | 不携带 Token 获取当前用户 | HTTP 401 | PASS |
| API-USER-005 | 使用无效 Token 获取当前用户 | HTTP 401 | PASS |

测试结果：5 passed，0 failed。

测试观察：
- 注册接口会检查密码是否出现在已泄露密码列表中。
- 登录成功后返回 Bearer Token，实际有效期为 300 秒。
- 未认证和无效 Token 均被拒绝，返回 HTTP 401。

## 注册接口边界探索：first_name 最大长度

根据 Swagger 中 `UserRequest.first_name` 的定义，字段最大长度为40。

本次进行了两个边界场景验证：

| 测试场景 | 输入长度 | 实际状态码 | 实际结果 |
|---|---:|---:|---|
| 最大长度边界 | 40 | 201 | 注册成功 |
| 超过最大长度 | 41 | 422 | 请求被拒绝 |

超长输入返回：

```json
{
  "first_name": [
    "The first name field must not be greater than 40 characters."
  ]
}
```

**测试结论：**

接口正确接受40字符的 first_name，并拒绝41字符的输入，符合 Swagger 最大长度约束。本次未发现该字段长度校验缺陷。

### last_name 最大长度边界验证

根据 Swagger 中 `UserRequest.last_name` 的定义，字段最大长度为20。

| 测试场景 | 输入长度 | 实际状态码 | 实际结果 |
|---|---:|---:|---|
| 超过最大长度 | 21 | 422 | 请求被拒绝 |

实际错误信息：

```json
{
  "last_name": [
    "The last name field must not be greater than 20 characters."
  ]
}
```

**测试结论：**

接口正确拒绝21字符的 last_name，返回明确的长度校验错误，符合 Swagger 最大长度约束。本次未发现该字段长度校验缺陷。

### email 最大长度边界验证

根据 Swagger 中 `UserRequest.email` 的定义，字段最大长度为256。

本次构造了一个格式合法、长度为257字符的邮箱，单独验证长度限制。

| 测试场景 | 输入长度 | 实际状态码 | 实际结果 |
|---|---:|---:|---|
| 超过最大长度 | 257 | 422 | 请求被拒绝 |

实际错误信息：

```json
{
  "email": [
    "The email field must not be greater than 256 characters."
  ]
}
```

**测试结论：**

接口正确拒绝257字符的邮箱，返回明确的长度校验错误，符合 Swagger 最大长度约束。本次未发现该字段长度校验缺陷。

### password 最小长度边界验证

根据 Swagger 中 `UserRequest.password` 的定义，密码最小长度为8，并要求包含大写字母、小写字母、数字和符号。

本次使用 `Aa1@xyz` 作为测试密码，长度为7，且包含上述四类字符。

| 测试场景 | 输入长度 | 实际状态码 | 实际结果 |
|---|---:|---:|---|
| 小于最小长度 | 7 | 422 | 请求被拒绝 |

实际错误信息：

```json
{
  "password": [
    "The password field must be at least 8 characters."
  ]
}
```

**测试结论：**

接口正确拒绝7字符密码，返回明确的最小长度校验错误，符合 Swagger 约束。本次未发现密码最小长度校验缺陷。

### password 特殊符号校验

根据 Swagger 中 `UserRequest.password` 的描述，密码必须包含大写字母、小写字母、数字和符号。

本次使用 `Abcdefg1` 作为测试密码：

- 长度为8，满足最小长度要求
- 包含大写字母、小写字母和数字
- 不包含特殊符号

| 测试场景 | 测试输入 | 实际状态码 | 实际结果 |
|---|---|---:|---|
| 缺少特殊符号 | Abcdefg1 | 422 | 请求被拒绝 |

实际错误信息：

```json
{
  "password": [
    "The password field must contain at least one symbol."
  ]
}
```

**测试结论：**

接口正确识别缺少特殊符号的密码，并返回明确的校验错误，符合 Swagger 密码规则。本次未发现该项校验缺陷。

### password 大写字母校验

根据 Swagger 中 `UserRequest.password` 的描述，密码必须包含至少一个大写字母和一个小写字母。

本次使用 `abcdefg1@` 作为测试密码：

- 长度为9，满足最小长度要求
- 包含小写字母、数字和特殊符号
- 不包含大写字母

| 测试场景 | 测试输入 | 实际状态码 | 实际结果 |
|---|---|---:|---|
| 缺少大写字母 | abcdefg1@ | 422 | 请求被拒绝 |

实际错误信息：

```json
{
  "password": [
    "The password field must contain at least one uppercase and one lowercase letter."
  ]
}
```

**测试结论：**

接口正确拒绝缺少大写字母的密码，密码大小写校验生效。本次未发现该项校验缺陷。

### password 小写字母校验

根据 Swagger 中 `UserRequest.password` 的描述，密码必须包含至少一个大写字母和一个小写字母。

本次使用 `ABCDEFG1@` 作为测试密码：

- 长度为9，满足最小长度要求
- 包含大写字母、数字和特殊符号
- 不包含小写字母

| 测试场景 | 测试输入 | 实际状态码 | 实际结果 |
|---|---|---:|---|
| 缺少小写字母 | ABCDEFG1@ | 422 | 请求被拒绝 |

实际错误信息：

```json
{
  "password": [
    "The password field must contain at least one uppercase and one lowercase letter."
  ]
}
```

**测试结论：**

接口正确拒绝缺少小写字母的密码，密码大小写校验生效。本次未发现该项校验缺陷。

### password 数字校验

根据 Swagger 中 `UserRequest.password` 的描述，密码必须包含至少一个数字。

本次使用 `Abcdefgh@` 作为测试密码：

- 长度为9，满足最小长度要求
- 包含大写字母、小写字母和特殊符号
- 不包含数字

| 测试场景 | 测试输入 | 实际状态码 | 实际结果 |
|---|---|---:|---|
| 缺少数字 | Abcdefgh@ | 422 | 请求被拒绝 |

实际错误信息：

```json
{
  "password": [
    "The password field must contain at least one number."
  ]
}
```

**测试结论：**

接口正确拒绝缺少数字的密码，密码数字校验生效。本次未发现该项校验缺陷。

### password 最小长度合法边界验证

根据 Swagger 中 `UserRequest.password` 的定义，密码最小长度为8，并要求包含大写字母、小写字母、数字和符号。

本次使用随机生成的8位密码：

随机生成符合规则的8位密码：`f"Aa1@{uuid.uuid4().hex[:4]}"`

该密码满足长度和字符组成要求。

| 测试场景 | 密码长度 | 实际状态码 | 实际结果 |
|---|---:|---:|---|
| 最小长度合法边界 | 8 | 201 | 注册成功 |

此前使用固定密码 `Aa1@bcde` 时，服务端返回密码已出现在数据泄露记录中的提示。更换随机密码后注册成功，排除了该额外安全检查对最小长度验证的干扰。

**测试结论：**

接口接受满足8位最小长度和字符组成要求的随机密码，密码合法边界验证通过。本次未发现密码最小长度校验缺陷。

### 登录接口：空凭据异常场景

使用空邮箱和空密码调用 `POST /users/login`。

| 测试场景 | 输入 | 实际状态码 | 实际响应 |
|---|---|---:|---|
| 空邮箱、空密码 | email=""，password="" | 401 | Invalid login request |

**测试结论：**

接口拒绝了空凭据登录请求，未观察到异常登录成功。本次未发现明确缺陷。

### 购物车接口：商品数量边界探索

测试接口：`PUT /carts/{cartId}/product/quantity`

测试前置：每次创建独立购物车，获取真实商品ID，先成功添加数量为1的商品，再修改数量。测试结束后删除购物车。

| 测试场景 | 添加商品响应 | 修改数量响应 | 实际结果 |
|---|---:|---:|---|
| quantity = 0 | 200 | 404 | Resource not found |
| quantity = -1 | 200 | 404 | Resource not found |
| quantity = 2 | 200 | 200 | item added or updated |

**测试结论：**

正常数量2能够成功修改，说明本次接口调用方式有效。

数量为0和-1时，接口均返回404。由于Swagger仅声明quantity为integer，没有规定最小值，也没有明确规定非法数量的响应状态码，因此暂不认定为已确认缺陷，保留为待确认的异常行为。

三次测试创建的购物车均成功清理，清理接口返回204。