import pytest
import random
import string
from faker import Faker


def random_email():
    username_length = random.randint(6, 12)
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=username_length))
    return f"{username}@yandex.ru"


def random_password():
    password_length = random.randint(8, 16)
    password_characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choices(password_characters, k=password_length))


def random_name():
    fake = Faker()
    return fake.name()


def random_credentials():
   credentials = {
       "email": random_email(),
       "password": random_password(),
       "name": random_name()
   }
   return credentials