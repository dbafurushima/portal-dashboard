import json
import re
import os
import random
import string
from django.contrib.auth.models import User
from ..models import Client, PasswordSafe, EnterpriseUser
from .encrypt import _encrypt, _decrypt

FIELDS = ['company-name', 'display-name', 'cnpj', 'city', 'state', 'cep', 'state-registration',
          'municipal-registration', 'email']
LENGTH_PASSWORD = 15


def _correct_post(keys) -> bool:
    """checks if the dictionary contains all the keys required for a customer's registration
    """
    sec_list = list(filter(lambda i: i in FIELDS, keys))
    return len(sec_list) == len(FIELDS)


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


def _email(email):
    return (_len_min(email, 8) and _len_max(email, 50)) and \
           re.match(r'^[a-z0-9.]+@[a-z0-9]+\.[a-z]+\.([a-z]+)?$', email)


def _rand_passwd(length):
    chars = string.ascii_letters + string.digits + '!@#$%^&*()'
    random.seed = (os.urandom(1024))
    return ''.join(random.choice(chars) for _ in range(length))


def create_user(username, email, password, enterprise=None):
    user = User(username=username, email=email)
    passwd = _encrypt(password).decode('utf-8')
    user.set_password(password)
    user.save()
    if enterprise:
        eu = EnterpriseUser(user=user, enterprise=enterprise)
        eu.save()
    return PasswordSafe(user=user, password=passwd).save()


def create_users(post: dict, enterprise):
    _users = post.get('users-json')

    if not len(_users) > 0:
        return

    users_json = json.loads(_users)
    for _user in users_json:
        user = User(username=_user.get('username'), email=_user.get('email'))
        raw_password = _user.get('password') if _user.get('password') else 'mudar123'
        passwd = _encrypt(raw_password).decode('utf-8')
        user.set_password(passwd)
        user.save()
        EnterpriseUser(user=user, enterprise=enterprise).save()


def passwd_from_username(username: str) -> str or None:
    try:
        user = User.objects.get(username=username)
        # client = Client.objects.get(user=user)
        pwd = PasswordSafe.objects.get(user=user)
        password = _decrypt(pwd.password)
        return password.decode('utf-8')
    except:
        return None


def create_default_user(email: str, client: Client) -> tuple:
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


def save_password_safe(password: str, user: User):
    """save password in the password vault
    """
    passwd = _encrypt(password).decode('utf-8')
    ps = PasswordSafe(user=user, password=passwd)
    ps.save()


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
    email = post.get('email')

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

    if not _email(email):
        return False, 'email'

    client = Client(company_name=company_name, display_name=display_name, cnpj=cnpj, city=city, state=state, cep=cep,
                    state_registration=state_registration, municipal_registration=municipal_registration)

    return True, client
