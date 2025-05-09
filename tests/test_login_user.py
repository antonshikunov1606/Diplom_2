import allure
import pytest
import requests
from response_definitions import ErrorResponses
from test_data import urls, credentials


class TestLoginUser:
    @allure.title("Проверка авторизации пользователя")
    def test_successful_login_courier(self, registration_user):
        payload = credentials

        with allure.step('Регистрация нового пользователя'):
            registration_user(payload)

        login_response = requests.post(urls['login'], json={
            "email": payload['email'], "password": payload['password']})
        login_response_data = login_response.json()
        actual_status = login_response_data['success']
        expected_status = True
        assert login_response.status_code == 200, f'Ожидаем код 200, но получили {login_response.status_code}'
        assert actual_status == expected_status, \
            f"Ожидаем статус: {expected_status}, но получили: {actual_status}."

    @allure.title("Проверка авторизации пользователя с неверным логином и паролем")
    @pytest.mark.parametrize("incorrect_data", [
        {"email": credentials["email"], "password": "fakepassword"},
        {"email": "fake_email@yandex.ru", "password": credentials["password"]}
    ])
    def test_login_with_incorrect_data_not_allowed(self, incorrect_data, registration_user):
        payload = credentials

        with allure.step('Регистрация нового пользователя'):
            registration_user(payload)

        login_response = requests.post(urls['login'], json=incorrect_data)
        login_response_data = login_response.json()
        actual_status = login_response_data['success']
        actual_message = login_response_data['message']
        expected_status = False
        expected_message = ErrorResponses.INCORRECT_DATA
        assert login_response.status_code == 401, f'Ожидаем код 401, но получили {login_response.status_code}'
        assert actual_status == expected_status, \
            f"Ожидаем статус: {expected_status}, но получили: {actual_status}."
        assert actual_message == expected_message, \
            f'Ожидаем ответ: {expected_message}, но получили: {actual_message}'
