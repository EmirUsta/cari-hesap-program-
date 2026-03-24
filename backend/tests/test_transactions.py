def test_create_transaction_debt(client):
    # First create a customer
    response = client.post(
        "/customers/",
        json={"full_name": "Transaction Customer", "email": "tc@example.com"}
    )
    customer_id = response.json()["id"]

    # Now create a transaction of type 'debt'
    response = client.post(
        "/transactions/",
        json={
            "customer_id": customer_id,
            "transaction_type": "debt",
            "amount": 50.0,
            "description": "Initial Debt"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == 50.0
    assert data["transaction_type"] == "debt"
    assert "id" in data

    # Verify customer balance was updated (should have increased by 50.0)
    response = client.get(f"/customers/{customer_id}")
    assert response.status_code == 200
    assert response.json()["current_balance"] == 50.0

def test_create_transaction_credit(client):
    # First create a customer
    response = client.post(
        "/customers/",
        json={"full_name": "Credit Customer", "email": "cc@example.com"}
    )
    customer_id = response.json()["id"]

    # Create a debt first
    client.post(
        "/transactions/",
        json={
            "customer_id": customer_id,
            "transaction_type": "debt",
            "amount": 100.0,
            "description": "Debt"
        }
    )

    # Now create a credit transaction
    response = client.post(
        "/transactions/",
        json={
            "customer_id": customer_id,
            "transaction_type": "credit",
            "amount": 30.0,
            "description": "Partial Payment"
        }
    )
    assert response.status_code == 201

    # Verify customer balance was updated (100 - 30 = 70.0)
    response = client.get(f"/customers/{customer_id}")
    assert response.status_code == 200
    assert response.json()["current_balance"] == 70.0

def test_create_transaction_invalid_customer(client):
    response = client.post(
        "/transactions/",
        json={
            "customer_id": 99999, # Invalid ID
            "transaction_type": "debt",
            "amount": 10.0
        }
    )
    assert response.status_code == 400
    assert "Customer not found" in response.text
