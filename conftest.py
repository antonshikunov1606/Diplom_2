import pytest
import random
import string
import requests
from faker import Faker
from test_data import URLS, Tokens


@pytest.fixture
def registration_user():
    def _registration_user(payload):
        reg_response = requests.post(URLS["registration"], json=payload)
        reg_response_data = reg_response.json()
        full_access_token = reg_response_data['accessToken']
        Tokens['accessToken'] = full_access_token[len("Bearer "):]
        Tokens['refreshToken'] = reg_response_data['refreshToken']
        return reg_response

    return _registration_user


@pytest.fixture
def delete_user():
    def _delete_user(access_token):
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response_delete = requests.delete(URLS["delete"], headers=headers)
        return response_delete

    return _delete_user


@pytest.fixture
def random_email():
    def generate_random_email():
        username_length = random.randint(6, 12)
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=username_length))
        return f"{username}@yandex.ru"

    return generate_random_email()


@pytest.fixture
def random_password():
    def generate_random_password():
        password_length = random.randint(8, 16)
        password_characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choices(password_characters, k=password_length))

    return generate_random_password()


@pytest.fixture
def random_name():
    fake = Faker()
    return fake.name()
