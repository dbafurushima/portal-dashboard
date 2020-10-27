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
        ('"dict" does not contain all required fields.')
    )

    DATABASE_UNKNOWN_INTERNAL_ERROR = Error(
        20,
        ('internal error not cataloged in the database')
    )

    @classmethod
    def name_and_error(cls, error) -> tuple:
        return error.name, error.name
