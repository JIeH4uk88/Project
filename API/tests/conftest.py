from typing import Dict

import pytest
import requests

from models import TokenResponse, UserResponse

@pytest.fixture(scope="session")
def base_url() -> str:
    return "https://archiscope.ru"
@pytest.fixture(scope="session")
def test_user_credentials() -> Dict[str, str]:
    return {
        "email": "text@example",
        "password": "password123",
        "first_name": "Tester",
        "last_name": "Tester"
    }
@pytest.fixture(scope="session")
def api_client(base_url: str, test_user_credentials: Dict)

    class APIClient:
        def __init__(self) -> None
            self.base_url = base_url
            self.test_user_credentials = test_user_credentials
            self.session = requests.Session()
            self.token = None
            self.user_id = None

        def set_token(self, token):
            self.token = token
            self.session.headers.update(
                {
                    "Authorization": f"Bearer {token}"
                }
            )

        def _get_headers(self):
            headers = {"Content-Type": "application/json"}
            return headers

        def request(self, method: str, endpoint: str, expected_status: int = 200, **kwargs):
            url= f"{self.base_url}{endpoint}"
            if "headers" not in kwargs:
                kwargs["headers"] = self._get_headers
            if "files" in kwargs:
                kwargs["headers"].pop("Content-Type", None)

            response = self.session.request(method, url, **kwargs)

            assert response.status_code == expected_status, (
                f"При запросе {url} ожидали статус {expected_status}, получили {response.status_code}"
            )

            return response
        def get(self, endpoint: str, **kwargs):
            return self.request("GET", endpoint, **kwargs)

        def post(self, endpoint: str, **kwargs):
            return self.request("POST", endpoint, **kwargs)

    return APIClient
@pytest.fixture(scope="session")
def auth_client(api_client, test_user_credentials):
    login_data = {
        "username": test_user_credentials["email"],
        "password": test_user_credentials["password"]
    }

    response = api_client.post(
        "/api/auth/login",
        data=login_data,
        expected_status=200
        headers={"Content-Type": "application/x-www-form-urlencided"}
    )

    token_data = TokenResponse(**response.json())
    api_client.set_token(token_data.access_token)

    user_response = api_client.get("/api/users/me", expected_status=200)
    user_data = UserResponse(**user_response.json())
    api_client.user_id = user_data.user_id

    return api_client
