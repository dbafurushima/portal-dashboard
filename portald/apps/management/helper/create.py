import json
import re
import os
import random
import string
from django.contrib.auth.models import User
from ..models import Client

FIELDS = ['company-name', 'display-name', 'cnpj', 'city', 'state', 'cep', 'state-registration',
          'municipal-registration']
LENGTH_PASSWORD = 15


def _correct_post(keys) -> bool:
    """checks if the dictionary contains all the keys required for a customer's registration
    """
    sec_list = list(filter(lambda i: i in FIELDS, keys))
    return len(sec_list) == len(FIELDS)


def scape_xss(string):
    pass


def _len_min(string, length):
    return len(string) >= length


def _len_max(string, length):
    return len(string) <= length


def _len(string, length):
    return len(string) == length


def _company_name(company_name):
    return _len_min(company_name, 4) and _len_max(company_name, 50)


def _display_name(display_name):
    return _len_min(display_name, 3)


def _cnpj(cnpj):
    return (_len_min(cnpj, 14) or _len_max(cnpj, 18)) and (re.match(r'^\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}$', cnpj))


def _city(city):
    return _len_min(city, 5)


def _state(state):
    return _len_min(state, 5)


def _cep(cep):
    return (_len(cep, 8) or _len(cep, 9)) and (re.match(r'^\d{5}-?\d{3}$', cep))


def _state_registration(state_registration):
    return _len_min(state_registration, 6)


def _municipal_registration(municipal_registration):
    return _len_min(municipal_registration, 6)


def _rand_passwd(length):
    chars = string.ascii_letters + string.digits + '!@#$%^&*()'
    random.seed = (os.urandom(1024))
    return ''.join(random.choice(chars) for i in range(length))


def create_users(post: dict):
    _users = post.get('users-json')
    if not len(_users) > 0:
        return
    users_json = json.loads(_users)
    for _user in users_json:
        user = User(username=_user.get('username'), email=_user.get('email'))
        if user.save():
            user.set_password(_user.get('password') if _user.get('password') else 'mudar123')
            user.save()


def create_default_user(username):
    user = User(username=username)
    user.save()
    user.set_password(_rand_passwd(LENGTH_PASSWORD))
    user.save()


def create_client(post: dict) -> tuple:
    """valid all fields required to create a client, then returns a Client object or a string
    with the field that does not meet the requirements
    """
    if not _correct_post(post):
        return False, 'does not contain all required fields', 403

    company_name = post.get('company-name')
    display_name = post.get('display-name')
    cnpj = post.get('cnpj')
    city = post.get('city')
    state = post.get('state')
    cep = post.get('cep')
    state_registration = post.get('state-registration')
    municipal_registration = post.get('municipal-registration')

    if not _company_name(company_name):
        return False, 'company name'

    if not _display_name(display_name):
        return False, 'display name'

    if not _cnpj(cnpj):
        return False, 'cnpj'

    if not _city(city):
        return False, 'city'

    if not _state(state):
        return False, 'state'

    if not _cep(cep):
        return False, 'cep'

    if not _state_registration(state_registration):
        return False, 'state registration'

    if not _municipal_registration(municipal_registration):
        return False, 'municipal registration'

    client = Client(company_name=company_name, display_name=display_name, cnpj=cnpj, city=city, state=state, cep=cep,
                    state_registration=state_registration, municipal_registration=municipal_registration)

    return True, client
