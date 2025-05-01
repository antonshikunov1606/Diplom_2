import allure
import pytest
import requests
from response_definitions import ErrorResponses
from test_data import URLS, credentials, Tokens


class TestRegistrationUser:
    @allure.title("Проверка регистрации нового пользователя с правильными данными")
    def test_registration_user_with_all_valid_data(self, delete_user):
        payload = credentials
        reg_response = requests.post(URLS['registration'], json=payload)
        reg_response_data = reg_response.json()
        actual_status = reg_response_data['success']
        expected_status = True
        full_access_token = reg_response_data['accessToken']
        Tokens['accessToken'] = full_access_token[len("Bearer "):]
        try:
            assert reg_response.status_code == 200, f'Ожидаем код 200, но получили {reg_response.status_code}'
            assert actual_status == expected_status, \
                f"Ожидаем статус: {expected_status}, но получили: {actual_status}."
        finally:
            with allure.step('Удаление пользователя'):
                delete_user(Tokens['accessToken'])

    @allure.title("Проверка регистрации пользователя, который уже зарегистрирован")
    def test_registration_user_with_existing_credentials_not_allowed(self, registration_user, delete_user):
        payload = credentials

        with allure.step('Регистрация нового пользователя'):
            registration_user(payload)

        with allure.step('Повторная попытка регистрации этого же пользователя'):
            reg_response = requests.post(URLS['registration'], json=payload)
            reg_response_data = reg_response.json()
            actual_status = reg_response_data['success']
            actual_message = reg_response_data['message']
            expected_status = False
            expected_message = ErrorResponses.USER_ALREADY_EXISTS
            try:
                assert reg_response.status_code == 403, f'Ожидаем код 403, но получили {reg_response.status_code}'
                assert actual_status == expected_status, \
                    f"Ожидаем статус: {expected_status}, но получили: {actual_status}."
                assert actual_message == expected_message, \
                    f'Ожидаем ответ: {expected_message}, но получили: {actual_message}'
            finally:
                with allure.step('Удаление пользователя'):
                    delete_user(Tokens['accessToken'])

    @allure.title("Проверка регистрации нового пользователя без заполнения одного обязательного поля")
    @pytest.mark.parametrize("partial_payload", [
        {"email": credentials["email"], "password": credentials["password"]},
        {"email": credentials["email"], "name": credentials["name"]},
        {"password": credentials["password"], "name": credentials["name"]}
    ])
    def test_registration_user_without_required_data_not_allowed(self, partial_payload):
        reg_response = requests.post(URLS['registration'], json=partial_payload)
        reg_response_data = reg_response.json()
        actual_status = reg_response_data['success']
        actual_message = reg_response_data['message']
        expected_status = False
        expected_message = ErrorResponses.INSUFFICIENT_DATA_FOR_REGISTRATION
        assert reg_response.status_code == 403, f'Ожидаем код 403, но получили {reg_response.status_code}'
        assert actual_status == expected_status, \
            f"Ожидаем статус: {expected_status}, но получили: {actual_status}."
        assert actual_message == expected_message, \
            f'Ожидаем ответ: {expected_message}, но получили: {actual_message}'
