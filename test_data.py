URLS = {
    'registration': "https://stellarburgers.nomoreparties.site/api/auth/register",
    'login': "https://stellarburgers.nomoreparties.site/api/auth/login",
    'edit': "https://stellarburgers.nomoreparties.site/api/auth/user",
    'create_order': "https://stellarburgers.nomoreparties.site/api/orders",
    'get_order': "https://stellarburgers.nomoreparties.site/api/orders",
    'delete': "https://stellarburgers.nomoreparties.site/api/auth/user"
}

credentials = {
    "email": "anton_shik@yandex.ru",
    "password": "qwerty000",
    "name": "Anton"
}

Tokens = {
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
