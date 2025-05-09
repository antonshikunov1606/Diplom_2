import allure
import requests
from response_definitions import ErrorResponses
from test_data import urls, credentials, tokens, test_ingredients, no_ingredients, invalid_ingredient
from helpers import random_credentials


class TestCreateAnOrder:
    @allure.title("Проверка создания заказа без авторизации")
    def test_successful_create_order_without_authorization(self):
        ingredients = test_ingredients

        response = requests.post(urls['create_order'], json=ingredients)
        response_data = response.json()
        actual_status = response_data['success']
        expected_status = True
        assert response.status_code == 200, f'Ожидаем код 200, но получили {response.status_code}'
        assert actual_status == expected_status, \
            f"Ожидаем статус: {expected_status}, но получили: {actual_status}."
        assert 'order' in response_data and isinstance(response_data['order'], dict), \
            '"order" нет в ответе или это не словарь'
        assert 'number' in response_data['order'], '"number" отсутствует в словаре order'

    @allure.title("Проверка создания заказа с авторизацией")
    def test_successful_create_order_with_authorization(self, registration_user):
        ingredients = test_ingredients
        payload = random_credentials

        with allure.step('Регистрация нового пользователя'):
            registration_user(payload)

        headers = {
            'Authorization': f'Bearer {tokens["accessToken"]}'
        }
        response = requests.post(urls['create_order'], json=ingredients, headers=headers)
        response_data = response.json()
        actual_status = response_data['success']
        owner_name = response_data['order']['owner']['name']
        owner_email = response_data['order']['owner']['email']
        expected_status = True
        assert response.status_code == 200, f'Ожидаем код 200, но получили {response.status_code}'
        assert actual_status == expected_status, \
            f"Ожидаем статус: {expected_status}, но получили: {actual_status}."
        assert len(response_data['order']['ingredients']) == 2, \
            f'Количество ингредиентов не 2, а {len(response_data["order"]["ingredients"])}'
        assert owner_name == credentials['name'], f'Ожидаем name {credentials["name"]}, но получили {owner_name}'
        assert owner_email == credentials['email'], f'Ожидаем email {credentials["email"]}, но получили {owner_email}'

    @allure.title("Проверка создания заказа без ингредиентов")
    def test_create_order_without_ingredients_not_created(self):
        ingredients = no_ingredients

        response = requests.post(urls['create_order'], json=ingredients)
        response_data = response.json()
        actual_status = response_data['success']
        actual_message = response_data['message']
        expected_status = False
        expected_message = ErrorResponses.NO_INGREDIENTS
        assert response.status_code == 400, f'Ожидаем код 400, но получили {response.status_code}'
        assert actual_status == expected_status, \
            f"Ожидаем статус: {expected_status}, но получили: {actual_status}."
        assert actual_message == expected_message, \
            f'Ожидаем ответ: {expected_message}, но получили: {actual_message}'

    @allure.title("Проверка создания заказа с указанием невалидного хеша ингредиента")
    def test_create_order_with_invalid_ingredient_not_created(self):
        ingredients = invalid_ingredient

        response = requests.post(urls['create_order'], json=ingredients)
        assert response.status_code == 500, f'Ожидаем код 500, но получили {response.status_code}'
