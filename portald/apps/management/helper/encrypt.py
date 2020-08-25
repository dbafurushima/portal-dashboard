from cryptography.fernet import Fernet
from django.conf import settings


def _encrypt(msg: str or bytes) -> bytes:
    """encrypt message to store in the password vault
    """
    msg = msg.encode() if isinstance(msg, str) else msg
    f = Fernet(settings.KEY)
    return f.encrypt(msg)


def _decrypt(msg: str or bytes) -> bytes:
    """decrypt message for administrator viewing in the password vault
    """
    msg = msg.encode() if isinstance(msg, str) else msg
    f = Fernet(settings.KEY)
    return f.decrypt(msg)
