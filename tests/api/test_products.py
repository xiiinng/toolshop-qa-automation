import pytest

def test_get_products(api_client):
    """验证获取商品列表接口"""

    # 发送 GET 请求
    response = api_client.get("/products")

    # 1. 验证 HTTP 状态码
    assert response.status_code == 200

    # 2. 验证响应可以解析为 JSON
    result = response.json()

    # 3. 验证响应数据结构
    assert "current_page" in result
    assert "data" in result
    assert "total" in result

    # 4. 验证商品列表类型
    assert isinstance(result["data"], list)

    # 5. 验证商品列表不为空
    assert len(result["data"]) > 0

    # 6. 验证商品基本字段
    product = result["data"][0]

    assert "id" in product
    assert "name" in product
    assert "price" in product

    print(f"商品总数: {result['total']}")
    print(f"当前页商品数量: {len(result['data'])}")


def test_get_products_page_2(api_client):
    """验证商品列表分页功能"""

    response = api_client.get(
        "/products",
        params={"page": 2}
    )

    assert response.status_code == 200

    result = response.json()

    assert result["current_page"] == 2
    assert isinstance(result["data"], list)
    assert len(result["data"]) > 0


def test_get_products_price_ascending(api_client):
    """验证商品价格升序排序"""

    response = api_client.get(
        "/products",
        params={"sort": "price,asc"}
    )

    assert response.status_code == 200

    result = response.json()

    prices = [
        product["price"]
        for product in result["data"]
    ]

    assert len(prices) > 0
    assert prices == sorted(prices)


def test_get_products_price_range(api_client):
    """验证商品价格区间筛选"""

    response = api_client.get(
        "/products",
        params={"between": "price,10,30"}
    )

    assert response.status_code == 200

    result = response.json()

    assert len(result["data"]) > 0

    for product in result["data"]:
        assert 10 <= product["price"] <= 30


def test_get_rental_products(api_client):
    """验证租赁商品筛选"""

    response = api_client.get(
        "/products",
        params={"is_rental": "true"}
    )

    assert response.status_code == 200

    result = response.json()

    assert len(result["data"]) > 0

    for product in result["data"]:
        assert product["is_rental"] is True



@pytest.mark.parametrize(
    "filter_param, nested_key",
    [
        ("by_brand", "brand"),
        ("by_category", "category")
    ]
)
def test_get_products_by_filter(api_client, filter_param, nested_key):
    """验证商品品牌和分类筛选"""

    # 第一步：获取商品列表，动态提取有效筛选 ID
    source_response = api_client.get("/products")

    assert source_response.status_code == 200

    source_data = source_response.json()["data"]

    assert len(source_data) > 0

    filter_id = source_data[0][nested_key]["id"]

    # 第二步：使用有效 ID 进行筛选
    response = api_client.get(
        "/products",
        params={filter_param: filter_id}
    )

    assert response.status_code == 200

    result = response.json()

    # 第三步：验证筛选结果
    assert result["total"] > 0
    assert len(result["data"]) > 0

    for product in result["data"]:
        assert product[nested_key]["id"] == filter_id


@pytest.mark.parametrize(
    "page",
    [0, -1, 999999]
)
def test_get_products_invalid_page(api_client, page):
    """验证异常页码参数"""

    response = api_client.get(
        "/products",
        params={"page": page}
    )

    # 接口应正常处理请求，不应出现服务器内部错误
    assert response.status_code < 500


def test_get_products_field_types(api_client):
    """验证商品核心字段的数据类型"""

    response = api_client.get("/products")

    assert response.status_code == 200

    result = response.json()

    assert isinstance(result["current_page"], int)
    assert isinstance(result["total"], int)
    assert isinstance(result["data"], list)

    product = result["data"][0]

    assert isinstance(product["id"], str)
    assert isinstance(product["name"], str)
    assert isinstance(product["price"], (int, float))
    assert isinstance(product["in_stock"], bool)
    assert isinstance(product["is_rental"], bool)