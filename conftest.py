import pytest
import requests
from test_data import urls, tokens


@pytest.fixture
def registration_user(request):
    def _registration_user(payload):
        reg_response = requests.post(urls["registration"], json=payload)
        reg_response_data = reg_response.json()
        full_access_token = reg_response_data['accessToken']
        tokens['accessToken'] = full_access_token[len("Bearer "):]
        tokens['refreshToken'] = reg_response_data['refreshToken']

        def delete_user():
            headers = {
                'Authorization': f'Bearer {tokens["accessToken"]}'
            }
            requests.delete(urls["delete"], headers=headers)

        request.addfinalizer(delete_user)
        return reg_response

    return _registration_user
