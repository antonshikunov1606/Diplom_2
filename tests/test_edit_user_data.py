import allure
import pytest
import requests
from response_definitions import ErrorResponses
from test_data import URLS, credentials, Tokens, test_data_to_edit


class TestEditUserData:
    @allure.title("Проверка изменения email")
    def test_successful_edit_email(self, registration_user, delete_user, random_email):
        payload = credentials
        email = random_email

        with allure.step('Регистрация нового пользователя'):
            registration_user(payload)

        headers = {
            'Authorization': f'Bearer {Tokens["accessToken"]}'
        }
        edit_response = requests.patch(URLS['edit'], json={
            "email": email}, headers=headers)
        edit_response_data = edit_response.json()
        actual_status = edit_response_data['success']
        actual_email = edit_response_data['user']['email']
        expected_status = True
        try:
            assert edit_response.status_code == 200, f'Ожидаем код 200, но получили {edit_response.status_code}'
            assert actual_status == expected_status, \
                f"Ожидаем статус: {expected_status}, но получили: {actual_status}."
            assert actual_email == email, f'Ожидаем "email": {email}, но получили: {actual_email}'
        finally:
            with allure.step('Удаление пользователя'):
                delete_user(Tokens['accessToken'])

    @allure.title("Проверка изменения password")
    def test_successful_edit_password(self, registration_user, delete_user, random_password):
        payload = credentials
        password = random_password

        with allure.step('Регистрация нового пользователя'):
            registration_user(payload)

        headers = {
            'Authorization': f'Bearer {Tokens["accessToken"]}'
        }
        edit_response = requests.patch(URLS['edit'], json={
            "password": password}, headers=headers)
        edit_response_data = edit_response.json()
        actual_status = edit_response_data['success']
        expected_status = True
        try:
            assert edit_response.status_code == 200, f'Ожидаем код 200, но получили {edit_response.status_code}'
            assert actual_status == expected_status, \
                f"Ожидаем статус: {expected_status}, но получили: {actual_status}."
        finally:
            with allure.step('Удаление пользователя'):
                delete_user(Tokens['accessToken'])

    @allure.title("Проверка изменения name")
    def test_successful_edit_name(self, registration_user, delete_user, random_name):
        payload = credentials
        name = random_name

        with allure.step('Регистрация нового пользователя'):
            registration_user(payload)

        headers = {
            'Authorization': f'Bearer {Tokens["accessToken"]}'
        }
        edit_response = requests.patch(URLS['edit'], json={
            "name": name}, headers=headers)
        edit_response_data = edit_response.json()
        actual_status = edit_response_data['success']
        actual_name = edit_response_data['user']['name']
        expected_status = True
        try:
            assert edit_response.status_code == 200, f'Ожидаем код 200, но получили {edit_response.status_code}'
            assert actual_status == expected_status, \
                f"Ожидаем статус: {expected_status}, но получили: {actual_status}."
            assert actual_name == name, f'Ожидаем "name": {name}, но получили: {actual_name}'
        finally:
            with allure.step('Удаление пользователя'):
                delete_user(Tokens['accessToken'])

    @allure.title("Проверка изменения данных пользователя без авторизации")
    @pytest.mark.parametrize("new_data", [
        {"email": test_data_to_edit['email']},
        {"password": test_data_to_edit['password']},
        {"name": test_data_to_edit['name']}
    ])
    def test_edit_user_data_without_authorization_not_allowed(self, new_data, registration_user, delete_user):
        payload = credentials

        with allure.step('Регистрация нового пользователя'):
            registration_user(payload)

        edit_response = requests.patch(URLS['edit'], json=new_data)
        edit_response_data = edit_response.json()
        actual_status = edit_response_data['success']
        actual_message = edit_response_data['message']
        expected_status = False
        expected_message = ErrorResponses.NOT_AUTHORIZED
        try:
            assert edit_response.status_code == 401, f'Ожидаем код 401, но получили {edit_response.status_code}'
            assert actual_status == expected_status, \
                f"Ожидаем статус: {expected_status}, но получили: {actual_status}."
            assert actual_message == expected_message, \
                f'Ожидаем ответ: {expected_message}, но получили: {actual_message}'
        finally:
            with allure.step('Удаление пользователя'):
                delete_user(Tokens['accessToken'])
