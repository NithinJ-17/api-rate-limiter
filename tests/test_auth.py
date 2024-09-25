import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    response = client.post(
        "/auth/register",
        json={
            "username": "test_user",
            "full_name": "Test User",
            "email": "test@example.com",
            "password": "testpassword",
            "phone_number": "1234567890",
            "role": "customer1"
        }
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

def test_login_user():
    # First, register the user
    client.post(
        "/auth/register",
        json={
            "username": "test_user",
            "full_name": "Test User",
            "email": "test@example.com",
            "password": "testpassword",
            "phone_number": "1234567890",
            "role": "customer1"
        }
    )

    # Now, test logging in with the correct credentials
    response = client.post(
        "/auth/login",
        data={"username": "test@example.com", "password": "testpassword"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
