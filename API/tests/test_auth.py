import pytest

from tests.models import UserResponse, TokenResponse
from mocks import MockDB


class TestAuth:
    def test_register_success(self, api_client):
        import uuid

        unique_email = f"{uuid.uuid4().hex[:8]}@tester.com"

        user_data = {
            "email": unique_email,
            "password": "testpassword123",
            "first_name": "Tester",
            "last_name": "Tester",
            "phone": "+123456789"
        }

        response = api_client.post(
            "/api/auth/register",
            json=user_data,
            expected_status_code=201
        )

        user = UserResponse(**response.json())
        assert user.email == unique_email
        assert user.first_name == "Tester"
        assert user.last_name == "Tester"
        assert user.phone == "+123456789"

        api_client.user_id = user.id

        login_data = {
            "username": unique_email,
            "password": "testpassword123",

        }

        logun_response = api_client.post(
            "/api/auth/login",
            expected_status_code=200,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        token = TokenResponse(**logun_response.json())
        assert token.access_token is not None

    @pytest.mark.negative
    def test_register_existing_email(self, api_client):
        MockDB.register_user("existing@mail.com", "pass123")
        resp = api_client.post("/api/auth/register", json={
            "email": "existing@mail.com",
            "password": "pass123"
        }, expected_status=400)
        token = TokenResponse(**resp.json())
        assert token.access_token is not None

    @pytest.mark.negative
    @pytest.mark.parametrize("email,password", [
        ("invalid", "ValidPass123"),
        ("valid@mail.com", "123"),
        ("", ""),
    ])
    def test_register_invalid_data(self, api_client, email, password):
        resp = api_client.post("/api/auth/register", json={
            "email": email,
            "password": password
        }, expected_status=422)
        token = TokenResponse(**resp.json())
        assert token.access_token is not None

    @pytest.mark.positive
    def test_login_success(self, api_client):
        MockDB.register_user("login@mail.com", "StrongPass")
        resp = api_client.post("/api/auth/login", json={
            "email": "login@mail.com",
            "password": "StrongPass"
        }, expected_status=200)
        token = TokenResponse(**resp.json())
        assert token.access_token is not None


    @pytest.mark.negative
    def test_login_wrong_credentials(self, api_client):
        resp = api_client.post("/api/auth/login", json={
            "email": "wrong@mail.com",
            "password": "wrong"
        }, expected_status=401)
        token = TokenResponse(**resp.json())
        assert resp["message"] == "Unauthorized"