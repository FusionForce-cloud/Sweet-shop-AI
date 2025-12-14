def test_register(client):
    response = client.post("/api/auth/register", json={"username": "testuser_reg", "password": "testpass"})
    assert response.status_code == 200
    assert response.json() == {"msg": "User registered"}

def test_login(client):
    client.post("/api/auth/register", json={"username": "testuser_login", "password": "testpass"})
    response = client.post("/api/auth/login", json={"username": "testuser_login", "password": "testpass"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client):
    response = client.post("/api/auth/login", json={"username": "nonexistent", "password": "wrong"})
    assert response.status_code == 401