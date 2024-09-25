import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def auth_headers_customer1():
    client.post(
        "/auth/register",
        json={
            "username": "customer1",
            "full_name": "Customer One",
            "email": "customer1@example.com",
            "password": "password123",
            "phone_number": "1234567890",
            "role": "customer1"
        }
    )
    response = client.post(
        "/auth/login",
        data={"username": "customer1@example.com", "password": "password123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_rate_limiting(auth_headers_customer1):
    for _ in range(5):
        response = client.get("/api/v1/users/1", headers=auth_headers_customer1)
        assert response.status_code == 200

    # Sixth request should return 429 Too Many Requests
    response = client.get("/api/v1/users/1", headers=auth_headers_customer1)
    assert response.status_code == 429
    assert response.text == "Rate limit exceeded. Please try again later."