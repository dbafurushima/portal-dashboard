import json
import re
import os
import random
import string

from django.contrib.auth.models import User
from typing import Tuple, Any

from ..models import Client, PasswordSafe, EnterpriseUser
from .encrypt import _encrypt, _decrypt
from apps.errors import Errors

FIELDS = ['company-name', 'display-name', 'cnpj', 'city', 'state', 'cep', 'district', 'address', 'state-registration',
          'municipal-registration', 'email']
LENGTH_PASSWORD = 15


def __correct_post(keys) -> bool:
    """checks if the dictionary contains all the keys required for a customer's registration

    >>> __correct_post(['city', 'cep', 'district'])
    False
    """
    sec_list = list(filter(lambda i: i in FIELDS, keys))
    return len(sec_list) == len(FIELDS)


def __len_min(text, length):
    return len(text) >= length


def __len_max(text, length):
    return len(text) <= length


def __len(text, length):
    return len(text) == length


def __company_name(company_name):
    return __len_min(company_name, 4) and __len_max(company_name, 50)


def __display_name(display_name):
    return __len_min(display_name, 3)


def __cnpj(cnpj):
    return (__len_min(cnpj, 14) or __len_max(cnpj, 18)) and (re.match(r'^\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}$', cnpj))


def __city(city):
    return __len_min(city, 5)


def __state(state):
    return __len_min(state, 2)


def __cep(cep):
    return (__len(cep, 8) or __len(cep, 9)) and (re.match(r'^\d{5}-?\d{3}$', cep))


def __district(district):
    return __len_min(district, 4) and __len_max(district, 40)


def __address(address):
    return __len_min(address, 4) and __len_max(address, 60)


def __state_registration(state_registration):
    return __len_min(state_registration, 2)


def __municipal_registration(municipal_registration):
    return __len_min(municipal_registration, 3)


def __email(email):
    return (__len_min(email, 8) and __len_max(email, 50)) and \
           re.match(r'^[a-z0-9.]+@[a-z0-9]+\.[a-z]+\.([a-z]+)?$', email)


def _rand_passwd(length):
    chars = string.ascii_letters + string.digits + '!@#$%^&*()'
    random.seed = (os.urandom(1024))
    return ''.join(random.choice(chars) for _ in range(length))


def __create_user(username: str, email: str, password: str, enterprise=None):
    user = User(username=username, email=email)
    passwd = _encrypt(password).decode('utf-8')
    user.set_password(password)
    user.save()
    if enterprise:
        eu = EnterpriseUser(user=user, enterprise=enterprise)
        eu.save()
    return PasswordSafe(user=user, password=passwd).save()


def _create_users(post: dict, enterprise: Client) -> None:
    _users = post.get('users-json')

    if not len(_users) > 0:
        return

    users_json = json.loads(_users)
    for _user in users_json:
        # raw_password = _user.get('password') if _user.get('password') else 'mudar123'
        __create_user(
            _user.get('username'),
            _user.get('username')+enterprise.mail.split('@')[-1],
            _user.get('password') if _user.get('password') else 'mudar123',
            enterprise)


def passwd_from_username(username: str) -> str or None:
    try:
        user = User.objects.get(username=username)
        # client = Client.objects.get(user=user)
        pwd = PasswordSafe.objects.get(user=user)
        password = _decrypt(pwd.password)
        return password.decode('utf-8')
    except Exception as err:
        return None


def _create_default_user(email: str, client: Client) -> tuple:
    username = email.split('@')[0]
    password = _rand_passwd(LENGTH_PASSWORD)

    user = User(username=username, email=email)
    user.set_password(password)
    user.save()

    # relate user to client
    client.user = user
    client.save()

    EnterpriseUser(user=user, enterprise=client).save()

    return password, user


def _save_password_safe(password: str, user: User):
    """save password in the password vault
    """
    passwd = _encrypt(password).decode('utf-8')
    ps = PasswordSafe(user=user, password=passwd)
    ps.save()


def _create_client_from_post(post: dict) -> Tuple[bool, str, Any]:
    """Does the necessary validations and tries to create an object Client.

    Args:
        post (dict): request.POST

    Returns:
        Tuple[bool, str, Any]: it worked, message error, Client or None
    """
    if not __correct_post(post):
        return False, Errors.DOES_NOT_CONTAIN_REQUIRED_FIELDS.value, None

    def __field_not_found_error(field):
        return 'O campo "%s" não atende aos requisitos.' % field

    company_name = post.get('company-name')
    display_name = post.get('display-name')
    cnpj = post.get('cnpj')
    city = post.get('city')
    state = post.get('state')
    cep = post.get('cep')
    district = post.get('district')
    address = post.get('address')
    state_registration = post.get('state-registration', 'ISENTO')
    municipal_registration = post.get('municipal-registration', 'ISENTO')
    email = post.get('email')

    if not __company_name(company_name):
        return False, __field_not_found_error('company name'), None

    if not __display_name(display_name):
        return False, __field_not_found_error('display name'), None

    if not __cnpj(cnpj):
        return False, __field_not_found_error('cnpj'), None

    if not __city(city):
        return False, __field_not_found_error('city'), None

    if not __state(state):
        return False, __field_not_found_error('state'), None

    if not __cep(cep):
        return False, __field_not_found_error('cep'), None

    if not __district(district):
        return False, __field_not_found_error('district'), None

    if not __address(address):
        return False, __field_not_found_error('address'), None

    if not __state_registration(state_registration):
        return False, __field_not_found_error('state registration'), None

    if not __municipal_registration(municipal_registration):
        return False, __field_not_found_error('municipal registration'), None

    if not __email(email):
        return False, __field_not_found_error('email'), None

    return (
        True,
        '',
        Client(
            company_name=company_name.strip(),
            display_name=display_name.strip(),
            cnpj=cnpj.strip(),
            city=city.strip(),
            state=state.strip(),
            cep=cep.strip(),
            district=district.strip(),
            address=address.strip(),
            state_registration=state_registration.strip(),
            municipal_registration=municipal_registration.strip(),
            mail=email.strip()
        )
    )
