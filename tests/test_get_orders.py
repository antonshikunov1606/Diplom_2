import allure
import requests
from response_definitions import ErrorResponses
from test_data import urls, tokens, test_ingredients
from helpers import random_credentials


class TestGetOrders:
    @allure.title("Получение заказа под авторизованным пользователем")
    def test_get_order_with_authorized_returns_order(self, registration_user):
        payload = random_credentials()
        ingredients = test_ingredients

        with allure.step('Регистрация нового пользователя'):
            registration_user(payload)

        headers = {
            'Authorization': f'Bearer {tokens["accessToken"]}'
        }

        with allure.step('Создание заказа'):
            response = requests.post(urls['create_order'], json=ingredients, headers=headers)

        login_response = requests.get(urls['get_order'], headers=headers)
        login_response_data = login_response.json()
        actual_status = login_response_data['success']
        actual_ingredients = login_response_data['orders'][0]['ingredients']
        expected_status = True
        expected_ingredients = test_ingredients["ingredients"]
        assert login_response.status_code == 200, f'Ожидаем код 200, но получили {login_response.status_code}'
        assert actual_status == expected_status, \
            f"Ожидаем статус: {expected_status}, но получили: {actual_status}."
        assert actual_ingredients == expected_ingredients, \
            f'Ожидаем список ингредиентов: {expected_ingredients}, но получили {actual_ingredients}'

    @allure.title("Получение заказа без авторизации")
    def test_get_order_without_authorized_not_allowed(self, registration_user):
        login_response = requests.get(urls['get_order'])
        login_response_data = login_response.json()
        actual_status = login_response_data['success']
        actual_message = login_response_data['message']
        expected_status = False
        expected_message = ErrorResponses.NOT_AUTHORIZED
        assert login_response.status_code == 401, f'Ожидаем код 401, но получили {login_response.status_code}'
        assert actual_status == expected_status, \
            f"Ожидаем статус: {expected_status}, но получили: {actual_status}."
        assert actual_message == expected_message, \
            f'Ожидаем ответ: {expected_status}, но получили {actual_message}'
