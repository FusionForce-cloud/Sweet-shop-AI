import pytest

def test_add_sweet(client):
    # Register admin
    client.post("/api/auth/register", json={"username": "admin", "password": "admin"})
    login_response = client.post("/api/auth/login", json={"username": "admin", "password": "admin"})
    token = login_response.json()["access_token"]
    response = client.post("/api/sweets/", json={"name": "Chocolate", "category": "Candy", "price": 2.5, "quantity": 10}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Chocolate"
    assert data["id"] is not None

def test_list_sweets(client):
    # Register admin and add sweet
    client.post("/api/auth/register", json={"username": "admin", "password": "admin"})
    login_response = client.post("/api/auth/login", json={"username": "admin", "password": "admin"})
    token = login_response.json()["access_token"]
    client.post("/api/sweets/", json={"name": "Lollipop", "category": "Candy", "price": 1.0, "quantity": 5}, headers={"Authorization": f"Bearer {token}"})
    response = client.get("/api/sweets/")
    assert response.status_code == 200
    sweets = response.json()
    assert len(sweets) >= 1

def test_purchase_sweet(client):
    # Register admin and add sweet
    client.post("/api/auth/register", json={"username": "admin", "password": "admin"})
    login_response = client.post("/api/auth/login", json={"username": "admin", "password": "admin"})
    token = login_response.json()["access_token"]
    add_response = client.post("/api/sweets/", json={"name": "Gummy", "category": "Candy", "price": 3.0, "quantity": 2}, headers={"Authorization": f"Bearer {token}"})
    sweet_id = add_response.json()["id"]
    # Register user
    client.post("/api/auth/register", json={"username": "user", "password": "pass"})
    login_response = client.post("/api/auth/login", json={"username": "user", "password": "pass"})
    token = login_response.json()["access_token"]
    # Purchase with auth
    response = client.post(f"/api/sweets/{sweet_id}/purchase", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 1

def test_search_sweets(client):
    # Register admin and add sweets
    client.post("/api/auth/register", json={"username": "admin", "password": "admin"})
    login_response = client.post("/api/auth/login", json={"username": "admin", "password": "admin"})
    token = login_response.json()["access_token"]
    client.post("/api/sweets/", json={"name": "Unique Chocolate Bar Search", "category": "Candy", "price": 2.5, "quantity": 10}, headers={"Authorization": f"Bearer {token}"})
    client.post("/api/sweets/", json={"name": "Vanilla Ice Cream Search", "category": "Dessert", "price": 4.0, "quantity": 5}, headers={"Authorization": f"Bearer {token}"})
    # Search by name
    response = client.get("/api/sweets/search?name=Unique")
    assert response.status_code == 200
    sweets = response.json()
    assert len(sweets) == 1
    assert sweets[0]["name"] == "Unique Chocolate Bar Search"

def test_update_sweet(client):
    # Register admin and add sweet
    client.post("/api/auth/register", json={"username": "admin", "password": "admin"})
    login_response = client.post("/api/auth/login", json={"username": "admin", "password": "admin"})
    token = login_response.json()["access_token"]
    add_response = client.post("/api/sweets/", json={"name": "Old Name", "category": "Candy", "price": 1.0, "quantity": 5}, headers={"Authorization": f"Bearer {token}"})
    sweet_id = add_response.json()["id"]
    # Update
    response = client.put(f"/api/sweets/{sweet_id}", json={"name": "New Name", "price": 1.5}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Name"
    assert data["price"] == 1.5

def test_delete_sweet(client):
    # Register admin and add sweet
    client.post("/api/auth/register", json={"username": "admin", "password": "admin"})
    login_response = client.post("/api/auth/login", json={"username": "admin", "password": "admin"})
    token = login_response.json()["access_token"]
    add_response = client.post("/api/sweets/", json={"name": "To Delete", "category": "Candy", "price": 1.0, "quantity": 5}, headers={"Authorization": f"Bearer {token}"})
    sweet_id = add_response.json()["id"]
    # Delete
    response = client.delete(f"/api/sweets/{sweet_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    # Check not in list
    list_response = client.get("/api/sweets/")
    sweets = list_response.json()
    assert not any(s["id"] == sweet_id for s in sweets)

def test_restock_sweet(client):
    # Register admin and add sweet
    client.post("/api/auth/register", json={"username": "admin", "password": "admin"})
    login_response = client.post("/api/auth/login", json={"username": "admin", "password": "admin"})
    token = login_response.json()["access_token"]
    add_response = client.post("/api/sweets/", json={"name": "Restock Me", "category": "Candy", "price": 1.0, "quantity": 2}, headers={"Authorization": f"Bearer {token}"})
    sweet_id = add_response.json()["id"]
    # Restock
    response = client.post(f"/api/sweets/{sweet_id}/restock?quantity=3", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 5