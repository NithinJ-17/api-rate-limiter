import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def auth_headers():
    # Register and log in a test user to get the token
    client.post(
        "/auth/register",
        json={
            "username": "test_user",
            "full_name": "Test User",
            "email": "testuser@example.com",
            "password": "password",
            "phone_number": "1234567890",
            "role": "customer1"
        }
    )
    response = client.post(
        "/auth/login",
        data={"username": "testuser@example.com", "password": "password"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200  # Check that login was successful
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_get_user(auth_headers):
    response = client.get("/api/v1/users/1", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["username"] == "test_user"