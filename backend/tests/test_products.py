def test_create_product(client):
    response = client.post(
        "/products/",
        json={"name": "Test Product", "barcode": "123456", "price": 10.5, "stock_quantity": 100}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Product"
    assert data["barcode"] == "123456"
    assert data["price"] == 10.5
    assert data["stock_quantity"] == 100
    assert "id" in data

def test_get_products(client):
    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_get_product(client):
    response = client.post(
        "/products/",
        json={"name": "Another Product", "barcode": "654321", "price": 20.0}
    )
    product_id = response.json()["id"]

    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Another Product"

def test_update_product(client):
    response = client.post(
        "/products/",
        json={"name": "Product Update", "barcode": "111111", "price": 5.0}
    )
    product_id = response.json()["id"]

    response = client.put(
        f"/products/{product_id}",
        json={"name": "Updated Product", "price": 15.0}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Product"
    assert response.json()["price"] == 15.0

def test_delete_product(client):
    response = client.post(
        "/products/",
        json={"name": "Product Delete", "barcode": "222222", "price": 1.0}
    )
    product_id = response.json()["id"]

    response = client.delete(f"/products/{product_id}")
    assert response.status_code == 200

    response = client.get(f"/products/{product_id}")
    assert response.status_code == 404
