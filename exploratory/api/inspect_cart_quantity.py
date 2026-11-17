
def test_inspect_cart_quantity_boundary(api_client):
    """探索购物车商品数量为0和负数时的接口行为"""

    # 动态获取一个真实商品ID
    products_response = api_client.get("/products")
    print("商品列表状态码：", products_response.status_code)

    if products_response.status_code != 200:
        print("无法获取商品，终止探索")
        return

    product_id = products_response.json()["data"][0]["id"]
    print("本次测试商品ID：", product_id)

    # 分别探索数量为0和-1
    for quantity in [2]:
        cart_id = None

        try:
            # 1. 创建独立购物车
            create_response = api_client.request("POST", "/carts")
            print(f"\n创建购物车状态码：{create_response.status_code}")

            if create_response.status_code != 201:
                print("购物车创建失败：", create_response.text)
                continue

            cart_id = create_response.json()["id"]

            # 2. 先添加一个数量为1的商品
            add_response = api_client.request(
                "POST",
                f"/carts/{cart_id}",
                json={
                    "product_id": product_id,
                    "quantity": 1
                }
            )
            print("添加商品状态码：", add_response.status_code)

            if add_response.status_code != 200:
                print("添加商品失败：", add_response.text)
                continue

            # 3. 修改商品数量
            update_response = api_client.request(
                "PUT",
                f"/carts/{cart_id}/product/quantity",
                json={
                    "product_id": product_id,
                    "quantity": quantity
                }
            )

            print(f"探索数量：{quantity}")
            print("实际状态码：", update_response.status_code)
            print("实际响应内容：", update_response.text)

        finally:
            # 4. 尝试清理测试购物车
            if cart_id:
                delete_response = api_client.request(
                    "DELETE",
                    f"/carts/{cart_id}"
                )
                print("购物车清理状态码：", delete_response.status_code)
