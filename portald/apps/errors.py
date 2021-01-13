import enum
from typing import NamedTuple

Error = NamedTuple(
    'Error',
    [
        ('code', int),
        ('text', str),
    ]
)


class Errors(enum.Enum):
    HTTP_400_BAD_REQUEST = Error(
        400,
        ('Incorrect request, some field does not meet the pre-defined '
         'specifications or is missing')
    )

    HTTP_401_UNAUTHORIZED = Error(401,
                                  ('you are not allowed to access this feature'
                                   'or perform this operation')
                                  )

    HTTP_500_INTERNAL_ERROR = Error(
        500,
        ('Internal server error, encountered an unexpected condition that '
         'prevented it from fulfilling the request.')
    )

    DOES_NOT_CONTAIN_REQUIRED_FIELDS = Error(
        1,
        '"dict" does not contain all required fields.'
    )

    DATABASE_UNKNOWN_INTERNAL_ERROR = Error(
        20,
        'internal error not cataloged in the database'
    )

    CONNECTION_REFUSED = Error(
        30,
        'Could not close connection to the host, check if it is available or accessible.'
    )

    @classmethod
    def name_and_error(cls, error) -> tuple:
        return error.code, error.name

    @classmethod
    def print_error(cls, error) -> str:
        return '[%s] %s' % (error.code, error.name)
