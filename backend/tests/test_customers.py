def test_create_customer(client):
    response = client.post(
        "/customers/",
        json={"full_name": "John Doe", "email": "john@example.com", "phone": "1234567890"}
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["full_name"] == "John Doe"
    assert data["email"] == "john@example.com"
    assert "id" in data
    assert data["current_balance"] == 0.0

def test_get_customers(client):
    response = client.get("/customers/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_get_customer(client):
    response = client.post(
        "/customers/",
        json={"full_name": "Jane Doe", "email": "jane@example.com"}
    )
    customer_id = response.json()["id"]

    response = client.get(f"/customers/{customer_id}")
    assert response.status_code == 200
    assert response.json()["full_name"] == "Jane Doe"

def test_update_customer(client):
    response = client.post(
        "/customers/",
        json={"full_name": "To Update", "email": "update@example.com"}
    )
    customer_id = response.json()["id"]

    response = client.put(
        f"/customers/{customer_id}",
        json={"full_name": "Updated Name"}
    )
    assert response.status_code == 200
    assert response.json()["full_name"] == "Updated Name"

def test_delete_customer(client):
    response = client.post(
        "/customers/",
        json={"full_name": "To Delete", "email": "delete@example.com"}
    )
    customer_id = response.json()["id"]

    response = client.delete(f"/customers/{customer_id}")
    assert response.status_code == 200

    response = client.get(f"/customers/{customer_id}")
    assert response.status_code == 404
