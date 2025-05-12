base_url = "https://stellarburgers.nomoreparties.site/api"

urls = {
    'registration': f"{base_url}/auth/register",
    'login': f"{base_url}/auth/login",
    'edit': f"{base_url}/auth/user",
    'create_order': f"{base_url}/orders",
    'get_order': f"{base_url}/orders",
    'delete': f"{base_url}/auth/user"
}

credentials = {
    "email": "anton_shik@yandex.ru",
    "password": "qwerty000",
    "name": "Anton"
}

tokens = {
    'accessToken': '',
    'refreshToken': ''
}

test_data_to_edit = {
    "email": "anton_shik_new@yandex.ru",
    "password": "FAKEpassword000",
    "name": "Antonio"
}

test_ingredients = {
    "ingredients": ["61c0c5a71d1f82001bdaaa75", "61c0c5a71d1f82001bdaaa6c"]
}

no_ingredients = {
    "ingredients": []
}

invalid_ingredient = {
    "ingredients": ["fakeingredient111"]
}
