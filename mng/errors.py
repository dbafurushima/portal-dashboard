import enum
from typing import NamedTuple

Error = NamedTuple('Info', [
    ('code', int),
    ('text', str),
])


def error_to_user(msg):
    print('\n>> Ops... error, %s\n' % msg)


class Errors(enum.Enum):

    HTTP_401_UNAUTHORIZED = Error(
        401, 
        ('you are not allowed to access this feature'
        'or perform this operation')
    )

    HTTP_500_INTERNAL_ERROR = Error(
        500,
        ('Internal server error, encountered an unexpected condition that '
        'prevented it from fulfilling the request.')
    )

    UNABLE_TO_CONNECT_SERVER = Error(
        1,
        ('unable to connect to server, you may be disconnected or the '
        'server may be offline.')
    )

    @classmethod
    def name_and_error(cls, error) -> tuple:
        return error.value.code, error.name, error.value.text

    @classmethod
    def pprint_error(cls, error) -> str:
        error_code, error_name, error_tex = Errors.name_and_error(error)
        return '\nERROR::%s [%s]\n%s' % (error_name, error_code, error_tex)
